"""Launch the Boomy mission executor (subscribes to /boomy/mission, publishes /cmd_vel)."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            Node(
                package="boomy_mission_executor",
                executable="mission_executor",
                name="boomy_mission_executor",
                output="screen",
                parameters=[
                    {
                        "mission_topic": "/boomy/mission",
                        "cmd_vel_topic": "/cmd_vel",
                        "max_duration_sec": 120.0,
                        "angular_speed": 0.35,
                        "linear_speed": 0.06,
                        "control_rate_hz": 10.0,
                        "use_nav2": True,
                        "nav2_action_name": "navigate_to_pose",
                        "detections_json_topic": "/boomy/detections_json",
                        "mission_status_topic": "/boomy/mission_status",
                    }
                ],
            ),
        ]
    )
