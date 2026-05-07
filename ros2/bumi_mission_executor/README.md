# boomy_mission_executor



ROS 2 Humble **Python** node: subscribes to **`std_msgs/String`** JSON on **`/boomy/mission`** (same contract as `yahboom-mcp` `POST /api/v1/agent/mission` → `publish_mission_json`).



## Build (on the Pi, inside your ROS 2 overlay)



```bash

cd ~/yahboomcar_ws/src

# copy or git clone this folder next to your other packages

ln -sf /path/to/yahboom-mcp/ros2/boomy_mission_executor .

cd ~/yahboomcar_ws

source /opt/ros/humble/setup.bash

colcon build --packages-select boomy_mission_executor

source install/setup.bash

```



`nav2_msgs` is listed as a dependency so **`NavigateToPose`** works when Nav2 is installed (`sudo apt install ros-humble-nav2-msgs` or full Nav2 stack). **`use_nav2`** defaults to **true**; set **`use_nav2: false`** if you have no Nav2 stack (the node disables Nav2 automatically if `nav2_msgs` is missing). Nav2 types are imported only when **`use_nav2`** is true at startup.



## Run



```bash

ros2 run boomy_mission_executor mission_executor

```



Or with launch defaults:



```bash

ros2 launch boomy_mission_executor mission_executor.launch.py

```



## Parameters



| Parameter | Default | Meaning |

|-----------|---------|--------|

| `mission_topic` | `/boomy/mission` | Must match **`YAHBOOM_MISSION_TOPIC`** on Goliath. |

| `cmd_vel_topic` | `/cmd_vel` | Holonomic twist output. |

| `max_duration_sec` | `120` | Cap for `estimated_duration_sec` from JSON. |

| `angular_speed` | `0.35` | Scale for yaw during search. |

| `linear_speed` | `0.06` | Scale for XY motion during search. |

| `control_rate_hz` | `10` | Timer rate for motion updates. |

| `use_nav2` | `true` | If true, **`behavior: go_to_waypoint`** with a **`nav2_goal`** object sends **NavigateToPose**. |

| `nav2_action_name` | `navigate_to_pose` | Nav2 action server name (namespace if Nav2 is namespaced). |

| `detections_json_topic` | `/boomy/detections_json` | **`std_msgs/String`** JSON from your vision node; set `""` to disable. During **search**, labels overlapping **`target_description`** stop motion and publish **`target_found`**. |

| `mission_status_topic` | `/boomy/mission_status` | **`std_msgs/String`** JSON status (`mission_received`, `target_found`, `search_timeout`, Nav2 states, etc.). |



## Behavior



- **`behavior`** in `room_search`, `spin_scan`, or **`intent`** `search`: slow patterned motion (forward/strafe/yaw mix) for `estimated_duration_sec` (capped), then publishes zero **`Twist`**. If **`detections_json_topic`** is non-empty and incoming JSON labels match **`target_description`** (token overlap), motion stops early with status **`target_found`**.

- **`behavior: go_to_waypoint`** with **`nav2_goal`** (`frame_id`, `x`, `y`, `yaw_deg`, optional `behavior_tree`) and **`use_nav2: true`**: sends **Nav2 NavigateToPose**; cancels previous Nav2 goal when a new mission arrives.

- Other combinations: logs and does not send motion or Nav2 (extend as needed).



Always keep a physical **estop** reachable; this node is for **indoor lab** speeds only.


