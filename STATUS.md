# STATUS — bumi-mcp physical bot readiness

**Version:** 0.2.0 · **Updated:** 2026-06-04

## Summary

| Layer | Status | Notes |
|-------|--------|-------|
| Product / OSS info MCP | ✅ Ready | `bumi(operation=info\|specs\|sdk_links\|market)` |
| Webapp (10775) | ✅ Specs dashboard | No teleop UI yet |
| REST `/api/v1/health` | ✅ Ready | Mock or rosbridge |
| REST `/api/v1/telemetry` | ✅ Ready | IMU, battery, joint_states |
| REST `/api/v1/control/estop` | ⚠️ Scaffold | Mock OK; hardware needs `BUMI_ESTOP_TOPIC` |
| REST `/api/v1/control/walk` | ⚠️ Gated | Requires `BUMI_ALLOW_MOTION=1` + walk topic from SDK |
| REST `/api/v1/control/head` | ⚠️ Stub | Returns not wired until neck API mapped |
| rosbridge on Jetson | ❌ Not shipped | Install when EDU unit arrives |
| teleoperator `BumiAdapter` | ❌ Not started | Depends on stable REST contract (this repo) |
| Yahboom mission executor copy | 🗄️ Reference only | Holonomic `/cmd_vel` — **not** for biped |

## Modes

| Env | Use |
|-----|-----|
| `BUMI_USE_MOCK_BRIDGE=1` | Dev, CI, teleoperator contract tests |
| `BUMI_IP=<tailnet>` + `uv sync --extra robot` | Physical rosbridge on Bumi Jetson |
| `BUMI_ALLOW_MOTION=1` | Only after SDK topic validation on hardware |

## Blockers before first physical motion

1. Noetix EDU unit + SDK/ROS topic documentation
2. Map walk / estop / head to vendor topics (replace placeholders in `.env.example`)
3. Human-supervised smoke test on stand before teleoperator wiring
4. `BumiAdapter` in teleoperator-mcp (separate PR)

See [INTEGRATION.md](INTEGRATION.md) for bring-up sequence.
