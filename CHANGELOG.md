# Changelog

## [0.2.0] — 2026-06-04

### Added

- **Physical-bot bridge scaffold:** `BumiROS2Bridge`, `MockBumiBridge`, lifespan connect on `just serve`.
- **REST v1:** `/api/v1/health`, `/telemetry`, `/control/estop`, `/control/walk`, `/control/head`.
- **MCP:** `bumi(operation=telemetry)`; improved `robot_status`.
- **Docs:** [STATUS.md](STATUS.md), [INTEGRATION.md](INTEGRATION.md).
- **Tests:** `tests/test_api_v1.py` (mock bridge).
- **Deps:** optional `[robot]` extra (`roslibpy`).

### Fixed

- `scripts/deploy.sh` mission path → `ros2/bumi_mission_executor`; marked Yahboom-only deprecated.

### Safety

- Motion requires `BUMI_ALLOW_MOTION=1` and configured SDK topics on hardware.

## [0.1.0]

- Hero product MCP, webapp dashboard, virtual-twin fleet map.
