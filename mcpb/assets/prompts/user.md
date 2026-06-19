# Bumi MCP — User Guide

## Quick Start

### Install

```bash
# Clone and setup
git clone https://github.com/sandraschi/bumi-mcp.git
cd bumi-mcp
uv sync

# Verify it works
uv run python -m bumi_mcp --stdio
# Type: {"jsonrpc":"2.0","method":"tools/list","id":1}
# You should see the bumi portmanteau tool listed.
```

### Start the Dashboard (HTTP mode)

```powershell
# Terminal 1: Backend
uv run python -m bumi_mcp --serve

# Terminal 2: Frontend
cd web_sota
npm install
npm run dev
```

Open http://127.0.0.1:10775 in your browser.

### Register in Claude Desktop

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "bumi": {
      "command": "uv",
      "args": ["run", "--directory", "D:\\Dev\\repos\\bumi-mcp", "python", "-m", "bumi_mcp", "--stdio"],
      "env": { "PYTHONPATH": "D:\\Dev\\repos\\bumi-mcp\\src" }
    }
  }
}
```

## Tutorials

### Tutorial 1: Learn About the Bumi Robot

Ask: "What is the Bumi humanoid robot?"

The model calls `bumi(operation="info")` and returns the manufacturer, height, weight, DOF, compute specs, and current shipping status.

For deeper detail: "Give me the full specifications of Bumi" — calls `bumi(operation="specs")` and returns the complete 30+ field structured data.

### Tutorial 2: Market Research

Ask: "Who makes Bumi and how does it compare in the Chinese market?"

The model calls `bumi(operation="market")` and returns Noetix Robotics company background, Series A funding, JD.com listing strategy, competitive landscape against Fourier Intelligence and Unitree, and analysis of the China humanoid robot market projected at 50-100k units/year by 2030.

### Tutorial 3: Developer Onboarding

Ask: "I want to develop for Bumi — where are the SDK and tools?"

The model calls `bumi(operation="sdk_links")` and returns the Noetix GitHub organization URL, Python SDK repository, ROS 2 bridge repository, firmware and diagnostics tools, and the SDK documentation landing page.

### Tutorial 4: Virtual Twin Setup

Ask: "How do I set up a virtual Bumi?"

The model calls `bumi(operation="virtual_twin")` and returns the full digital twin composition:
- Resonite for XR presence (animated Bumi avatar in Resonite worlds)
- WorldLabs for environment understanding (generate 3D worlds from images)
- ROS 2 bridge for research and Gazebo simulation
Instructions for wiring each component.

### Tutorial 5: Fleet Orchestration

Ask: "What other robots can Bumi work with in my fleet?"

The model calls `bumi(operation="fleet_peers")` and returns the RoboFang ecosystem narrative covering yahboom-mcp (companion ground robot), dreame-mcp (environment mapping), and robotics-mcp (ROS 2 bridge).

### Tutorial 6: Robot Status Check

Ask: "Is my Bumi robot connected?"

If BUMI_ROBOT_URL is configured, the model calls `bumi(operation="robot_status")` which pings the robot's health endpoint. If the robot bridge is active on the local API, it returns the robot's mode, connection status, motion allowance, and uptime.

### Tutorial 7: Live Telemetry

Ask: "Show me Bumi's current telemetry"

With a connected robot bridge, the model calls `bumi(operation="telemetry")` and returns live joint positions, IMU orientation, battery level, and motor temperatures. Without a live connection, it returns mock telemetry for development testing.

### Tutorial 8: Emergency Stop

Ask: "Emergency stop Bumi now!"

The model uses `POST /api/v1/control/estop` on the local HTTP server. The estop takes priority over all other control inputs and is logged server-side.

### Tutorial 9: Walk Control

Ask: "Make Bumi walk forward slowly"

The model calls `POST /api/v1/control/walk` with linear=0.3, angular=0.0. Requires BUMI_ALLOW_MOTION=1 and a connected robot bridge. The dashboard virtual page shows live walk status.

### Tutorial 10: Head Control

Ask: "Make Bumi look to the right"

The model calls `POST /api/v1/control/head` with yaw=45, pitch=0. Head positioning is available even in mock mode for testing.

### Tutorial 11: Multi-Step Research Workflow

Ask: "Research Bumi for a procurement decision. Give me the specs, market position, and SDK quality."

This triggers `bumi_agentic_workflow` with a goal that spans three data sources. The LLM plans and executes calls to `bumi(operation="specs")`, `bumi(operation="market")`, and `bumi(operation="sdk_links")` then synthesizes a procurement recommendation.

### Tutorial 12: Quick Start Prompt

Ask: "Give me a quick start for operating Bumi"

The model uses the `bumi_quick_start` prompt with focus="physical" for hardware setup instructions, or focus="virtual" for digital twin setup.

## Common Workflows

### Hardware Setup

1. Set BUMI_ROBOT_URL to the robot's HTTP endpoint
2. Start the server: `uv run python -m bumi_mcp --serve`
3. Check connection: `bumi(operation="robot_status")`
4. Enable motion: set BUMI_ALLOW_MOTION=1
5. Test estop: POST /api/v1/control/estop
6. Test walk: POST /api/v1/control/walk?linear=0.1

### Development Setup

1. Clone and uv sync
2. Run tests: `uv run pytest`
3. Start HTTP mode: `uv run python -m bumi_mcp --serve`
4. Start frontend: `cd web_sota && npm run dev`
5. Access dashboard at http://127.0.0.1:10775

### Virtual Twin Setup

1. Start resonite-mcp and create a Bumi avatar in Resonite
2. Start worldlabs-mcp for environment generation
3. Start robotics-mcp for ROS 2 bridge
4. Call `bumi(operation="virtual_twin")` to verify all connections
5. The dashboard /virtual page shows the live twin map

## Dashboard Pages

| Page | Route | Content |
|------|-------|---------|
| Dashboard | /dashboard | Server status, robot connectivity, quick actions |
| Virtual | /virtual | Fleet twin composition and connection status |
| Fleet | /fleet | All connected RoboFang peers |
| Tools | /tools | Registered MCP tools manifest |
| Chat | (floating) | LLM chat with auto-discovered local models |
| Logging | /logging | Ring-buffer activity log with filter, search, export |
| Settings | /settings | Environment variables reference |
| Help | /help | Full reference with tabs: About, Quickstart, API & Tools, FAQ |

## Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| BUMI_MCP_HOST | 127.0.0.1 | API bind address |
| BUMI_MCP_PORT | 10774 | API port |
| BUMI_ROBOT_URL | (none) | HTTP base URL for physical robot bridge |
| BUMI_IP | (none) | Robot IP address (fleet env override) |
| BUMI_FALLBACK_IP | (none) | Fallback robot IP if primary unreachable |
| BUMI_BRIDGE_PORT | 9090 | ROS 2 bridge TCP port |
| BUMI_ALLOW_MOTION | (none) | Set to 1 to enable walk control commands |
| BUMI_USE_MOCK_BRIDGE | (none) | Set to use mock bridge instead of real hardware |
| BUMI_MCP_TAURI | (none) | Set to 1 automatically by Tauri desktop wrapper |
| BUMI_IMU_TOPIC | /imu/data | ROS 2 IMU topic |
| BUMI_BATTERY_TOPIC | /battery_state | ROS 2 battery topic |
| BUMI_JOINT_STATES_TOPIC | /joint_states | ROS 2 joint states topic |
| BUMI_WALK_CMD_TOPIC | (none) | ROS 2 walk command topic |
| BUMI_ESTOP_TOPIC | (none) | ROS 2 estop topic |

### Ports

| Port | Service |
|------|---------|
| 10774 | Backend (FastAPI + MCP streamable HTTP) |
| 10775 | Frontend (Vite dev server) |

Both ports are registered in the fleet standard reservoir (10700-10800 range).

## Troubleshooting

### "Connection refused" on robot status

Ensure BUMI_ROBOT_URL is set correctly. The robot API must be reachable from the machine running bumi-mcp. Check network connectivity and firewall rules.

### "No module named 'bumi_mcp'"

Ensure PYTHONPATH includes the src/ directory, or run from the repo root with `uv run python -m bumi_mcp`.

### Frontend shows blank page

Ensure the backend is running on port 10774. The Vite dev server proxies /api/* requests to the backend. Check `npm run dev` output for proxy errors.

### Dashboard "/help" returns 404

The frontend SPA must be running (npm run dev) or the built dist must be served with SPA fallback. Direct access to backend port 10774 will only show API JSON.

### LLM providers list is empty

Ensure Ollama (port 11434) or LM Studio (port 1234) is running. The backend auto-discovers them on startup. Check that the services are not blocked by firewall.

### Cannot control robot

Check BUMI_ALLOW_MOTION=1 is set. Verify BUMI_WALK_CMD_TOPIC is configured for your ROS 2 setup. The estop must not be active. All control commands are logged server-side for debugging.

## API Reference

### REST Endpoints

All REST endpoints are under /api/ on port 10774.

#### GET /api/health
Returns server status and service name.
```json
{"status": "ok", "service": "bumi-mcp"}
```

#### GET /api/stats
Returns product, vendor, DOF count, and virtual twin server count.
```json
{"product": "Bumi", "vendor": "Noetix Robotics", "dof": 21, "virtual_twin_servers": 3}
```

#### GET /api/hero
Returns full spec sheet plus virtual twin fleet data.
```json
{"hero": {"product": "Bumi", ...}, "virtual_twin": {"mcp_servers": [...]}}
```

#### GET /api/tools
Returns registered MCP tools manifest.
```json
{"tools": [{"name": "bumi", ...}], "mcp_http_path": "/mcp"}
```

#### GET /api/logs?limit=50&level=INFO&sort=desc
Returns paginated activity log entries.
```json
{"entries": [...], "total": 42, "limit": 50, "offset": 0}
```

#### GET /api/llm/providers
Returns auto-discovered local LLM providers.
```json
{"providers": {"ollama": {"url": "http://127.0.0.1:11434", "models": ["llama3.2:3b", ...]}}}
```

#### POST /api/llm/chat
Chat proxy to local LLM. Body: `{"provider": "ollama", "model": "llama3.2:3b", "messages": [...]}`

#### GET /api/v1/health
Robot bridge health and connection status.
```json
{"status": "online", "robot": "noetix_bumi", "connected": true, "mock": true, "uptime_s": 123.4}
```

#### GET /api/v1/telemetry
Live robot telemetry (requires connected bridge).
```json
{"success": true, "telemetry": {"joints": {...}, "imu": {...}, "battery": {...}}}
```

#### POST /api/v1/control/estop
Emergency stop. Takes priority over all other control.

#### POST /api/v1/control/walk?linear=0.5&angular=0.0
Walk command. `linear` (-1 to 1), `angular` (-1 to 1).

#### POST /api/v1/control/head?yaw=0&pitch=0
Head positioning. `yaw` (-90 to 90), `pitch` (-45 to 45).

#### POST /api/v1/control/manip
Manipulator control. Body: `{"source": "webxr", "left": {...}, "right": {...}}`

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.2.0 | 2026-06 | Added REST v1 API, mock bridge, telemetry, control endpoints, CORS for Tauri, LLM provider discovery, activity log |
| 0.1.0 | 2026-05 | Initial MCP server with product info, market context, SDK links, virtual twin fleet map |
