# Bumi MCP — Noetix Bumi Humanoid Robot Control

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**MCP server + REST bridge scaffold for the Noetix Bumi humanoid.**

> v0.2 adds `/api/v1/*` (health, telemetry, gated control) and mock bridge for CI/teleoperator prep. Full physical motion awaits EDU hardware + Noetix SDK topic mapping — see [STATUS.md](STATUS.md) and [INTEGRATION.md](INTEGRATION.md).

---

## Bumi Product Info

| Spec | Value |
|------|-------|
| **Manufacturer** | Noetix Robotics (Beijing) — 北京松延动力科技集团股份有限公司 |
| **Website** | [noetixrobotics.com](https://noetixrobotics.com/en/product/n2/1262) |
| **Models** | Lite · Air · Pro · Max · EDU-Air · EDU-Pro · EDU-Max |
| **Price** | From ~10,000 CNY (~€1,300 / ~$1,400) — "world's first 10k-CNY class humanoid" |
| **Height/Weight** | 98cm / ~17kg |
| **DOF** | 21 (6 per leg, 4 per arm, 1 lumbar, hands) |
| **Compute (base)** | 6 TOPS |
| **Compute (EDU)** | NVIDIA Jetson Orin Nano Super / Orin NX |
| **Sensors** | RGB camera, IMU |
| **Battery** | 48V 3.5Ah, 2-3h runtime, quick-swap |
| **Connectivity** | WiFi + Bluetooth, optional 4G/5G |
| **Knee torque** | 70 N·m |
| **Status** | **Shipping** — thousands of orders placed (Dec 2025 news) |

### Features (from Noetix)
- "Bumi Bumi" voice wake word + interaction
- Object recognition (RGB camera)
- One-click auto-standing on startup
- Mobile app control + visual programming
- Smart OTA updates
- Autonomous lying down / standing up
- Open Source SDK & development tools

### Ordering

No direct e-commerce (no JD.com, Amazon, etc.). Noetix sells B2B through their sales team:

| Contact | Details |
|---------|---------|
| **Sales email** | sales@noetixrobotics.com |
| **Hotline** | 400-096-9300 (Mon-Fri 10:00-19:00 Beijing) |
| **WeChat** | Scan QR code on [noetixrobotics.com/en/contact-us](https://noetixrobotics.com/en/contact-us) |
| **Inquiry form** | [noetixrobotics.com/en/contact-us?t=a](https://www.noetixrobotics.com/en/contact-us?t=a) |
| **Partner inquiry** | [Become an agent](https://www.noetixrobotics.com/en/eco-partnership) |

Pricing from ~10,000 CNY (~€1,300) for Lite model. Models: Lite · Air · Pro · Max · EDU-Air · EDU-Pro · EDU-Max. Price depends on model and quantity — contact sales for quote.

---

## Architecture

```
PC (Goliath) ──Tailscale── Bumi (Jetson Orin)
                              │
                         rosbridge :9090
                              │
                         bumi-mcp :10774  (/api/v1)
                              │
                         Noetix SDK (walk, joints, estop)
```

- **Mock mode:** `BUMI_USE_MOCK_BRIDGE=1` — no hardware (default in `.env.example`)
- **Physical:** `BUMI_IP=<tailnet>` + `uv sync --extra robot`
- **Yahboom copies** in `ros2/`, `minimal_mission_executor.py` — reference only, not biped-safe

## Files (physical path)

| File | Purpose |
|------|---------|
| `src/bumi_mcp/core/ros2_bridge.py` | roslibpy telemetry + gated walk/estop |
| `src/bumi_mcp/testing/mock_bridge.py` | CI / dev stand-in |
| `src/bumi_mcp/api_v1.py` | teleoperator-facing REST |
| `STATUS.md` / `INTEGRATION.md` | Readiness + bring-up |

## Legacy Yahboom ports (reference)

| File | Origin | Purpose |
|------|--------|---------|
| `minimal_mission_executor.py` | yahboom-mcp | Holonomic missions — **not for Bumi** |
| `vision_bridge.py` | yahboom-mcp | COCO detection bridge |
| `scripts/deploy.sh` | yahboom-mcp | **Deprecated** Pi deploy |
| `ros2/bumi_mission_executor/` | boomy fork | Wheeled mission package |

## Quick Start

```powershell
git clone https://github.com/sandraschi/bumi-mcp
cd bumi-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just serve` with `.env` from `.env.example` (mock bridge by default).

```powershell
Copy-Item .env.example .env
just serve
Invoke-RestMethod http://127.0.0.1:10774/api/v1/health
just test
just ci
```

### Physical bot

See **[INTEGRATION.md](INTEGRATION.md)** — `BUMI_IP`, `uv sync --extra robot`, telemetry first, then gated motion.

## License

MIT
