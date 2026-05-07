#!/usr/bin/env python3
"""Mission executor with ultrasonic obstacle avoidance and room search patterns."""
import json, math, time, rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Float32, String

OBSTACLE_THRESHOLD_CM = 25.0
REVERSE_DURATION_S = 1.5
TURN_DURATION_S = 2.0


class MissionExecutor(Node):
    def __init__(self):
        super().__init__("mission_executor")
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.status_pub = self.create_publisher(String, "/boomy/mission_status", 10)
        self.buzzer_pub = self.create_publisher(Bool, "/buzzer", 10)
        self.det_pub = self.create_publisher(String, "/boomy/detections_json", 10)
        self.create_subscription(String, "/boomy/mission", self._on_mission, 10)
        self.create_subscription(Float32, "/ultrasonic", self._on_ultrasonic, 10)
        self.create_subscription(String, "/boomy/detections_json", self._on_detections, 10)
        self.timer = None
        self.deadline = 0.0
        self.reverse_until = 0.0
        self.turn_until = 0.0
        self.phase = "idle"
        self.last_plan = {}
        self.last_sonar_cm = 999.0
        self.search_keywords = []
        self.nav_was_blocked = False
        self.target_found = False
        self.found_label = ""
        self.get_logger().info("Mission executor ready (/boomy/mission, /ultrasonic, /boomy/detections_json)")

    def _on_ultrasonic(self, msg):
        self.last_sonar_cm = msg.data

    def _on_detections(self, msg):
        if self.phase != "search" or not self.search_keywords:
            return
        try:
            data = json.loads(msg.data)
            dets = data.get("detections", [])
        except Exception:
            return
        for d in dets:
            label = d.get("label", "").lower()
            for kw in self.search_keywords:
                if kw in label:
                    self.target_found = True
                    self.found_label = d["label"]
                    self.get_logger().info("TARGET FOUND: %s (conf=%.2f)", d["label"], d.get("confidence", 0))
                    self._cancel()
                    self.status("target_found", "Found %s (confidence %.0f%%)" % (d["label"], d.get("confidence", 0) * 100))
                    return

    def _on_mission(self, msg):
        try:
            plan = json.loads(msg.data)
        except Exception:
            self.get_logger().error("Invalid mission JSON")
            return
        self.last_plan = plan
        intent = plan.get("intent", "unknown")
        behavior = plan.get("behavior", "search")
        target = plan.get("target_description", "")
        voice = plan.get("voice_feedback", "")
        dur = float(plan.get("estimated_duration_sec", 60))
        self._cancel()
        self.search_keywords = [w.lower() for w in target.split() if len(w) > 2] if target else []
        self.get_logger().info("%s | behavior=%s target=%r dur=%.0fs", intent, behavior, target, dur)
        self.status("accepted", f"{voice or 'Mission accepted.'}")
        if behavior in ("search", "room_search", "spin_scan", "sinusoidal_scan"):
            self._start_search(dur)
        else:
            self.status("completed", "No motion behavior requested.")

    def _start_search(self, dur):
        self.deadline = time.time() + dur
        self.phase = "search"
        self.nav_was_blocked = False
        self.timer = self.create_timer(0.1, self._search_loop)
        self.status("searching", "Moving in search pattern. Obstacle avoidance active.")

    def _search_loop(self):
        now = time.time()
        if now > self.deadline:
            self._cancel()
            self.status("completed", "Mission duration elapsed.")
            return

        # Handle obstacle avoidance
        if self.last_sonar_cm < OBSTACLE_THRESHOLD_CM and self.reverse_until == 0:
            self.reverse_until = now + REVERSE_DURATION_S
            self.turn_until = now + REVERSE_DURATION_S + TURN_DURATION_S
            self.nav_was_blocked = True
            self.status("avoiding", "Obstacle detected at %.0f cm — avoiding." % self.last_sonar_cm)

        twist = Twist()
        if self.reverse_until > now:
            twist.linear.x = -0.15
            twist.angular.z = 0.0
        elif self.turn_until > now:
            twist.linear.x = 0.0
            twist.angular.z = 0.5
        else:
            self.reverse_until = 0.0
            self.turn_until = 0.0
            twist.linear.x = 0.12
            twist.angular.z = 0.35 * math.sin(now * 1.2)

        self.cmd_pub.publish(twist)

    def _cancel(self):
        if self.timer:
            self.destroy_timer(self.timer)
            self.timer = None
        self.cmd_pub.publish(Twist())
        self.phase = "idle"
        self.reverse_until = 0.0
        self.turn_until = 0.0

    def status(self, status, message=""):
        payload = json.dumps({
            "status": status,
            "message": message,
            "sonar_cm": round(self.last_sonar_cm, 1),
            "was_blocked": self.nav_was_blocked,
        })
        self.status_pub.publish(String(data=payload))
        self.get_logger().info("STATUS: %s", payload)
        if status in ("target_found", "completed"):
            self._beep()

    def _beep(self):
        self.buzzer_pub.publish(Bool(data=True))
        self.create_timer(0.4, lambda: self.buzzer_pub.publish(Bool(data=False))).cancel()


def main():
    rclpy.init()
    node = MissionExecutor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
