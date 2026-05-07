# Autonomous Mission Architecture

**Last updated**: 2026-05-07

## Overview

The Yahboom Raspbot V2 can operate autonomously using a three-layer architecture:

```
User/Agent → MCP Server → Ollama (Pi) → Mission Plan JSON → ROS 2 → Robot
```

1. **Input**: A natural-language goal ("patrol the room", "find the dog", "check water bowls")
2. **Planning**: Ollama (Gemma3:1b) on the Raspberry Pi 5 generates a structured mission plan
3. **Execution**: The mission executor ROS 2 node parses the plan and drives the robot

## How It Works

### Step 1 — Mission Request

You send a goal via the webapp (`/missions` page) or MCP tool:

```
Send: "Patrol in a square: move forward 2s, turn left, repeat 4 times, then stop and report battery."
```

The request goes to `POST /api/v1/agent/mission` with the goal text.

### Step 2 — LLM Planning (Ollama on Pi)

The MCP server forwards the goal to Ollama running on the Pi (`http://192.168.1.11:11434`). The LLM (Gemma3:1b by default) generates a structured `MissionPlanV1` JSON:

```json
{
  "intent": "patrol",
  "behavior": "search",
  "target_description": null,
  "voice_feedback": "Starting square patrol. Will report battery on completion.",
  "duration_seconds": 20,
  "search_pattern": "square",
  "nav2_goal": null,
  "use_nav2": false,
  "ros_topic_hints": ["/cmd_vel"],
  "safety_notes": "Keep speed low, stop if obstacle detected"
}
```

### Step 3 — ROS 2 Execution

The mission plan is published to the ROS 2 topic `/boomy/mission`. The **mission executor** node (running in the Docker container alongside the driver) receives it and:

- **search/spin_scan**: Drives in sinusoidal/rotating patterns via `/cmd_vel`, scanning for obstacles
- **vision detection**: Can stop when a target object is matched (requires `/boomy/detections_json`)
- **Nav2 navigation**: Optional `NavigateToPose` for waypoint-based navigation (requires Nav2 stack)
- **Status feedback**: Publishes progress on `/boomy/mission_status`

### Step 4 — Report Back

The mission executor publishes status updates throughout execution. When complete, it reports final state (battery, distance traveled, obstacles found). This appears in the webapp's "Report Back" panel.

## Complex Missions

### "Find our dog"

```
Goal: "Search the apartment with sinusoidal pattern, looking for a brown dog.
       Stop when detected, report position, and play a beep."
```

The Ollama planner decomposes this into:
1. **Intent**: `search`
2. **Behavior**: `sinusoidal_scan`  
3. **Target**: `brown dog`
4. **Detection topic**: `/boomy/detections_json` (E2B vision results)
5. **On match**: Stop motors, publish status with position

The mission executor drives in a weaving pattern while subscribing to vision detections. When the target keywords match, it halts and reports.

### "Check the water bowls"

```
Goal: "Go to the kitchen waypoint, check water bowl level via camera,
       report if low, then return to dock."
```

This requires:
1. **Nav2 waypoint** (`nav2_goal` with kitchen coordinates)
2. **Vision inspection** at the waypoint (camera snapshot, VLM analysis)
3. **Return navigation** to dock position

This is the most advanced mode — currently requires the Nav2 stack (`nav2_msgs`, not installed) and environment mapping (SLAM).

## Current Capabilities

| Feature | Status | Notes |
|---------|--------|-------|
| Natural language → mission plan | Working | Ollama on Pi generates JSON |
| Search patterns (sinusoidal, spin) | Working | Drives via `/cmd_vel` |
| Duration-based execution | Working | Timer-based stop |
| Status reporting | Working | `/boomy/mission_status` |
| Vision target detection | Planned | Needs camera + detector node |
| Nav2 waypoint navigation | Planned | Needs `nav2_msgs` + SLAM map |
| Obstacle avoidance | Partial | Cliff/IR sensors active |

## Configuration

| Env Variable | Default | Description |
|-------------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://192.168.1.11:11434` | Ollama endpoint on Pi |
| `YAHBOOM_MISSION_TOPIC` | `/boomy/mission` | ROS topic for mission JSON |
| `YAHBOOM_GEMINI_API_KEY` | (unset) | Optional Gemini Cloud API key |

## Webapp Integration

- **`/missions`**: Natural language prompt input, sample missions, send button, report panel
- **`/chat`**: AI Companion — chat with the robot via Ollama
- **`/llm`**: Local LLM settings — model selection, provider config
- **`/status`**: Check if ROS, SSH, Ollama are connected before sending missions
