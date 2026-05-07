"""
Subscribe to std_msgs/String JSON on /boomy/mission (from yahboom-mcp agent API).

Features:
- Search: timed holonomic /cmd_vel pattern until duration or **detection match**.
- Nav2: optional **NavigateToPose** when ``nav2_goal`` is present and ``use_nav2`` is true.
- Detections: optional **std_msgs/String** JSON (flexible schema) matched against ``target_description``.
- Status: optional **std_msgs/String** JSON on ``mission_status_topic``.
"""

from __future__ import annotations

import json
import math
from typing import Any

import rclpy
from geometry_msgs.msg import PoseStamped, Quaternion, Twist
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import String

from boomy_mission_executor.detection_utils import (
    extract_detection_labels,
    labels_match_target,
    tokenize_target,
)


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _yaw_deg_to_quat(yaw_deg: float) -> Quaternion:
    yaw = math.radians(float(yaw_deg))
    return Quaternion(x=0.0, y=0.0, z=math.sin(yaw / 2.0), w=math.cos(yaw / 2.0))


class MissionExecutorNode(Node):
    def __init__(self) -> None:
        super().__init__("boomy_mission_executor")

        self.declare_parameter("mission_topic", "/boomy/mission")
        self.declare_parameter("cmd_vel_topic", "/cmd_vel")
        self.declare_parameter("max_duration_sec", 120.0)
        self.declare_parameter("angular_speed", 0.35)
        self.declare_parameter("linear_speed", 0.06)
        self.declare_parameter("control_rate_hz", 10.0)
        self.declare_parameter("use_nav2", True)
        self.declare_parameter("nav2_action_name", "navigate_to_pose")
        self.declare_parameter("detections_json_topic", "/boomy/detections_json")
        self.declare_parameter("mission_status_topic", "/boomy/mission_status")

        topic = self.get_parameter("mission_topic").get_parameter_value().string_value
        self._cmd_topic = self.get_parameter("cmd_vel_topic").get_parameter_value().string_value
        self._max_dur = float(self.get_parameter("max_duration_sec").value)
        self._wz = float(self.get_parameter("angular_speed").value)
        self._vx = float(self.get_parameter("linear_speed").value)
        rate = float(self.get_parameter("control_rate_hz").value)
        self._period = 1.0 / _clamp(rate, 4.0, 50.0)

        self._use_nav2 = bool(self.get_parameter("use_nav2").value)
        self._nav2_action = self.get_parameter("nav2_action_name").get_parameter_value().string_value
        det_topic = self.get_parameter("detections_json_topic").get_parameter_value().string_value.strip()
        self._status_topic = (
            self.get_parameter("mission_status_topic").get_parameter_value().string_value.strip()
            or "/boomy/mission_status"
        )

        self._pub = self.create_publisher(Twist, self._cmd_topic, 10)
        self._status_pub = self.create_publisher(String, self._status_topic, 10)
        self.create_subscription(String, topic, self._on_mission, 10)

        if det_topic:
            self.create_subscription(String, det_topic, self._on_detections_json, 10)
            self.get_logger().info("Detection JSON subscription on %r" % (det_topic))

        self._timer = None
        self._deadline_sec = 0.0
        self._start_sec = 0.0
        self._phase = "idle"
        self._last_plan: dict[str, Any] = {}
        self._search_keywords: list[str] = []

        self._nav2_client: ActionClient | None = None
        self._nav2_goal_handle = None
        if self._use_nav2:
            try:
                from nav2_msgs.action import NavigateToPose

                self._NavigateToPose = NavigateToPose
                self._nav2_client = ActionClient(self, NavigateToPose, self._nav2_action)
                self.get_logger().info(
                    "Nav2 enabled: action %r (wait for server before first goal)",
                    self._nav2_action,
                )
            except Exception as e:
                self.get_logger().error("Nav2 requested but nav2_msgs unavailable: %s" % (e))
                self._use_nav2 = False

        self.get_logger().info(
            "boomy_mission_executor listening on %r publishing %r status=%r",
            topic,
            self._cmd_topic,
            self._status_topic,
        )

    def _publish_status(self, payload: dict[str, Any]) -> None:
        try:
            self._status_pub.publish(String(data=json.dumps(payload, ensure_ascii=False)))
        except Exception as e:
            self.get_logger().warn("mission status publish failed: %s" % (e))

    def _stop_motion(self) -> None:
        self._pub.publish(Twist())

    def _cancel_timer(self) -> None:
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _cancel_nav2(self) -> None:
        gh = self._nav2_goal_handle
        self._nav2_goal_handle = None
        if gh is None:
            return
        try:
            cancel_future = gh.cancel_goal_async()
            cancel_future.add_done_callback(lambda _f: None)
        except Exception as e:
            self.get_logger().debug("nav2 cancel: %s" % (e))

    def _on_detections_json(self, msg: String) -> None:
        if self._phase != "search":
            return
        raw = (msg.data or "").strip()
        if not raw or not self._search_keywords:
            return
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            return
        labels = extract_detection_labels(obj)
        if not labels_match_target(labels, self._search_keywords):
            return

        self.get_logger().info("Target match on labels=%s (keywords=%s)" % (labels, self._search_keywords))
        self._cancel_timer()
        self._stop_motion()
        self._phase = "idle"
        self._publish_status(
            {
                "status": "target_found",
                "labels": labels,
                "plan": self._last_plan,
            }
        )

    def _send_nav2_goal(self, ng: dict[str, Any]) -> None:
        if not self._nav2_client or not getattr(self, "_NavigateToPose", None):
            self.get_logger().warn("Nav2 goal skipped (client not available)")
            return
        if not self._nav2_client.server_is_ready():
            self.get_logger().warn("Nav2 action server not ready; retry mission when Nav2 is up")
            self._publish_status({"status": "nav2_not_ready", "plan": self._last_plan})
            return

        self._cancel_nav2()

        frame = str(ng.get("frame_id") or ng.get("frame") or "map")
        x = float(ng.get("x", 0.0))
        y = float(ng.get("y", 0.0))
        yaw_deg = float(ng.get("yaw_deg", ng.get("yaw", 0.0)))

        goal = self._NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = frame
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.position.z = 0.0
        goal.pose.pose.orientation = _yaw_deg_to_quat(yaw_deg)
        goal.behavior_tree = str(ng.get("behavior_tree") or "")

        self.get_logger().info(
            "Sending Nav2 NavigateToPose frame=%s x=%.3f y=%.3f yaw_deg=%.1f",
            frame,
            x,
            y,
            yaw_deg,
        )

        send_future = self._nav2_client.send_goal_async(goal)

        def _done(fut):
            try:
                goal_handle = fut.result()
            except Exception as e:
                self.get_logger().error("Nav2 send_goal failed: %s" % (e))
                return
            if not goal_handle.accepted:
                self.get_logger().warn("Nav2 goal rejected")
                self._publish_status({"status": "nav2_rejected", "plan": self._last_plan})
                return
            self._nav2_goal_handle = goal_handle
            self._publish_status({"status": "nav2_goal_accepted", "plan": self._last_plan})

            result_future = goal_handle.get_result_async()

            def _result_done(rfut):
                try:
                    res = rfut.result().result
                except Exception as ex:
                    self.get_logger().warn("Nav2 result error: %s" % (ex))
                    return
                self.get_logger().info("Nav2 navigation finished")
                self._publish_status(
                    {
                        "status": "nav2_completed",
                        "result_type": str(type(res)),
                        "plan": self._last_plan,
                    }
                )

            result_future.add_done_callback(_result_done)

        send_future.add_done_callback(_done)

    def _on_mission(self, msg: String) -> None:
        raw = (msg.data or "").strip()
        if not raw:
            self.get_logger().warn("Empty mission string")
            return
        try:
            plan = json.loads(raw)
        except json.JSONDecodeError as e:
            self.get_logger().error("Invalid mission JSON: %s" % (e))
            return

        behavior = str(plan.get("behavior") or "idle").lower()
        intent = str(plan.get("intent") or "").lower()
        target = str(plan.get("target_description") or "")
        dur = float(plan.get("estimated_duration_sec") or 45.0)
        dur = _clamp(dur, 3.0, self._max_dur)

        self._cancel_timer()
        self._cancel_nav2()
        self._stop_motion()
        self._last_plan = dict(plan)
        self._start_sec = self.get_clock().now().nanoseconds * 1e-9
        self._deadline_sec = self._start_sec + dur
        self._search_keywords = tokenize_target(target)

        self._publish_status({"status": "mission_received", "behavior": behavior, "intent": intent})

        nav2_goal = plan.get("nav2_goal")
        if behavior == "go_to_waypoint" and isinstance(nav2_goal, dict) and self._use_nav2:
            self._phase = "navigate"
            self._send_nav2_goal(nav2_goal)
            return

        if behavior == "go_to_waypoint" and isinstance(nav2_goal, dict) and not self._use_nav2:
            self.get_logger().warn(
                "go_to_waypoint with nav2_goal but use_nav2 is false — enable parameter use_nav2"
            )

        if behavior in ("room_search", "spin_scan") or intent == "search":
            self._phase = "search"
            self.get_logger().info(
                "Mission search behavior=%s intent=%s target=%r keywords=%r duration=%.1fs",
                behavior,
                intent,
                target,
                self._search_keywords,
                dur,
            )
            self._timer = self.create_timer(self._period, self._tick_search)
            return

        self._phase = "idle"
        self.get_logger().info(
            "Mission idle behavior=%s intent=%s (no motion / no matching branch)",
            behavior,
            intent,
        )

    def _tick_search(self) -> None:
        now = self.get_clock().now().nanoseconds * 1e-9
        if now >= self._deadline_sec:
            self._cancel_timer()
            self._stop_motion()
            self._phase = "idle"
            self.get_logger().info("Mission motion complete (duration elapsed, no detection)")
            self._publish_status({"status": "search_timeout", "plan": self._last_plan})
            return

        t = now - self._start_sec
        twist = Twist()
        twist.linear.x = self._vx * math.sin(t * 0.25)
        twist.linear.y = self._vx * 0.35 * math.cos(t * 0.2)
        twist.angular.z = self._wz * (0.7 + 0.3 * math.sin(t * 0.4))
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        self._pub.publish(twist)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    node = MissionExecutorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node._cancel_nav2()
        node._stop_motion()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
