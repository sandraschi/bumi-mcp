# INTEGRATION — Noetix Bumi physical bot

How bumi-mcp fits the RoboFang fleet and teleoperator-mcp.

## Architecture

```
Pico Browser (WebXR) ──Tailscale──► teleoperator-mcp :10901
                                         │ httpx
                                         ▼
                                   bumi-mcp :10774  (/api/v1/*)
                                         │ roslibpy
                                         ▼
                              rosbridge on Bumi Jetson :9090
                                         │
                              Noetix SDK / ROS 2 stack
```

**Today:** teleoperator uses `BoomyAdapter` → yahboom-mcp. **Next:** `BumiAdapter` → bumi-mcp with humanoid capabilities (`balance_risk=True`, gait not holonomic `cmd_vel`).

## Bring-up checklist (when hardware arrives)

### 1. Network

- Join Bumi Jetson and Goliath to the same Tailscale tailnet (`tailfab45.ts.net` or yours).
- Note Bumi’s `100.x.x.x` address → `BUMI_IP`.

### 2. On the Jetson (vendor / EDU image)

- Confirm ROS 2 Humble (or vendor version) and **rosbridge** on port **9090**.
- Record actual topics: `/joint_states`, `/imu/data`, `/battery_state`, walk command, estop.
- Do **not** reuse Yahboom `/cmd_vel` holonomic patterns on a biped.

### 3. On Goliath (PC)

```powershell
Set-Location D:\Dev\repos\bumi-mcp
Copy-Item .env.example .env
# Edit: BUMI_IP=100.x.x.x, unset BUMI_USE_MOCK_BRIDGE
uv sync --extra robot
just serve
```

Verify:

```powershell
Invoke-RestMethod http://127.0.0.1:10774/api/v1/health
Invoke-RestMethod http://127.0.0.1:10774/api/v1/telemetry
```

### 4. Motion gate (human present, harness if needed)

1. Keep `BUMI_ALLOW_MOTION` unset — telemetry only.
2. After SDK review, set topics in `.env` and `BUMI_ALLOW_MOTION=1`.
3. Test `POST /api/v1/control/estop` before any walk command.
4. Test `POST /api/v1/control/walk?linear=0.05&angular=0` at minimum speed.

### 5. Teleoperator (follow-on)

- Add `BumiAdapter` in teleoperator-mcp pointing at `http://127.0.0.1:10774` (or tailnet).
- Map WebXR stick → `/api/v1/control/walk`, head → `/api/v1/control/head`.
- Enable stricter watchdog and spoken estop (same pattern as Boomy).

## REST contract (teleoperator parity)

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/health` | Connection + mock flag + mode |
| `GET /api/v1/telemetry` | Battery, IMU, joints |
| `POST /api/v1/control/estop` | Immediate safe stop |
| `POST /api/v1/control/walk?linear=&angular=` | Gait velocity (gated) |
| `POST /api/v1/control/head?yaw=&pitch=` | Neck / gaze (when wired) |

## Related fleet docs

- [mcp-central-docs/pico/WEBXR.md](https://github.com/sandraschi/mcp-central-docs/blob/master/pico/WEBXR.md) — Pico + teleoperator
- [teleoperator-mcp](https://github.com/sandraschi/teleoperator-mcp) — WebXR cockpit
- [robotics-mcp NOETIX_BUMI](https://github.com/sandraschi/robotics-mcp) — discovery / info hub

## Yahboom artifacts in this repo

Files under `minimal_mission_executor.py`, `vision_bridge.py`, `ros2/bumi_mission_executor/` are **reference ports** from yahboom-mcp. They are not validated on Bumi. See deprecated banner in `scripts/deploy.sh`.
