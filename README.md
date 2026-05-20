# Bumi MCP — Noetix Bumi Humanoid Robot Control

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

**MCP server + ROS 2 control for the Noetix Bumi humanoid robot.**

> Ported architecture from yahboom-mcp (Raspbot v2). Designed for Bumi EDU models with NVIDIA Jetson Orin.

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

This repo adapts the proven yahboom-mcp stack for Bumi:

```
PC (Goliath) ──Tailscale── Bumi (Jetson Orin)
                              │
                         rosbridge:9090
                              │
                         mission_executor
                              │
                         Bumi SDK (motion, vision, sensors)
```

- **rosbridge** in Docker (same fix pattern: disable host rosbridge, use container)
- **Mission executor** from yahboom-mcp — subscribes `/boomy/mission`, executes autonomous behaviors
- **Vision detection** — SSD MobileNet v2 COCO (same bridge, Bumi's camera input)
- **Coffee shop demo** — Tailscale WiFi client mode for remote control
- **Ollama** on device for LLM-based mission planning (Gemma3:1b or larger on Orin)

## Files

| File | Origin | Purpose |
|------|--------|---------|
| `minimal_mission_executor.py` | yahboom-mcp | ROS 2 mission executor with obstacle avoidance + vision matching |
| `vision_bridge.py` | yahboom-mcp | SSD MobileNet v2 COCO detection -> `/boomy/detections_json` |
| `scripts/deploy.sh` | yahboom-mcp | One-shot Pi/Orin deploy script |
| `docs/AUTONOMOUS_MISSIONS.md` | yahboom-mcp | Ollama planning -> ROS execution pipeline |
| `docs/COFFEESHOP_DEMO.md` | yahboom-mcp | Tailscale remote control setup |
| `ros2/bumi_mission_executor/` | Forked from `boomy_mission_executor` | ROS 2 package for mission execution |

## Quick Start

```powershell
git clone https://github.com/sandraschi/bumi-mcp
cd bumi-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:


## Getting Started

1. Set up Tailscale on Bumi and your PC
2. Install rosbridge in Docker on Bumi's Orin
3. `./scripts/deploy.sh <bumi-tailscale-ip>`
4. `YAHBOOM_IP=<bumi-tailscale-ip> uv run python -m mcp_bridge`

## License

MIT
