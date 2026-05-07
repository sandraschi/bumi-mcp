# Handover — bumi-mcp

**Session**: 2026-05-07
**Operator**: Sandra
**Status**: Ported architecture from yahboom-mcp, pre-scaffold

---

## Status

Bumi is **shipping now** from Noetix Robotics (Beijing). 7 models from ~10,000 CNY (~€1,300). 98cm / 21 DoF / 17kg humanoid. Optional NVIDIA Jetson Orin for EDU models.

**Sales contact**: sales@noetixrobotics.com — no retail/JD.com listing, B2B only.

## Files Copied from yahboom-mcp

| File | Origin | Purpose |
|------|--------|---------|
| `minimal_mission_executor.py` | yahboom-mcp | ROS 2 mission executor with obstacle avoidance + vision matching |
| `vision_bridge.py` | yahboom-mcp | SSD MobileNet v2 COCO detection pipeline |
| `scripts/deploy.sh` | yahboom-mcp | One-shot Orin deploy script |
| `docs/AUTONOMOUS_MISSIONS.md` | yahboom-mcp | Ollama planning → ROS execution pipeline |
| `docs/COFFEESHOP_DEMO.md` | yahboom-mcp | Tailscale remote control setup |
| `ros2/bumi_mission_executor/` | Forked from `boomy_mission_executor` | ROS 2 package for mission execution |

## Architecture

The yahboom-mcp autonomous mission stack transfers directly:
- rosbridge in Docker (same host rosbridge kill fix)
- Mission executor subscribing `/boomy/mission`
- Vision detection bridge
- Tailscale coffee shop setup
- Ollama on device for LLM planning

## Next Actions

1. Contact sales@noetixrobotics.com for EDU-Max quote
2. When Bumi arrives, run `scripts/deploy.sh <tailscale-ip>`
3. Adapt I2C/servo commands to Bumi's SDK

---

## Bumi Product Specs

| Spec | Value |
|------|-------|
| Models | Lite · Air · Pro · Max · EDU-Air · EDU-Pro · EDU-Max |
| Price | From ~10,000 CNY (~€1,300) |
| Height/Weight | 98cm / ~17kg |
| DOF | 21 |
| Compute (base) | 6 TOPS |
| Compute (EDU) | NVIDIA Jetson Orin Nano Super / Orin NX |
| Sensors | RGB camera, IMU |
| Battery | 48V 3.5Ah, 2-3h |
| Connectivity | WiFi + Bluetooth, optional 4G/5G |
| Features | "Bumi Bumi" voice wake, object recognition, auto-standing, OTA |
