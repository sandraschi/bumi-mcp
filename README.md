# bumi-mcp (Noetix Bumi Android)

[![GitHub](https://img.shields.io/badge/GitHub-sandraschi%2Fbumi--mcp-181717?logo=github)](https://github.com/sandraschi/bumi-mcp)

**Bumi** is a sleek, 1-meter-tall humanoid (android) research platform by **Noetix Robotics** (松延动力). This repository serves as the **Autumn 2026** mission-control gateway—linking the upcoming physical unit with a federated, DDS-powered AI orchestration layer.

---

## 🤖 The Android: Noetix Bumi

The **Bumi** (v2 SOTA series) is one of the most agile and hardware-diverse humanoids in the consumer-research bracket, offering industrial-grade performance at a price point (~$1,400) comparable to high-end mobile robots like the ROSMASTER X3 PLUS.

- **Form Factor**: Sleek, minimalistic white "Bipedal Android" chassis.
- **Dimensions**: ~100 cm (3.3 ft) height | ~20 kg weight.
- **Kinematics**: 21 Degrees of Freedom (DOF) with high-torque precision servos.
- **Compute**: On-board NVIDIA Jetson Orin Nano/NX series for real-time inference.
- **Locomotion**: Advanced bipedal walking, stabilization, and expressive gesture control.
- **Identity**: A true "Android" assistant capable of navigating complex human environments.

---

## 📅 Project Status: Autumn 2026

**We do not have a physical Bumi unit yet.** This is our **Autumn Project** hardware target.

> [!IMPORTANT]
> **Working on it!** While the physical unit is not yet in the sandraschi lab, the **FOSS software stack is already available**. We are leveraging the DDS-based SDK and Noetix reinforcement learning environments to build a **Full Virtual Twin (Bumi VT)**.

### The Virtual Path
Since Noetix provides the open-source **[noetix_sdk_bumi](https://github.com/Noetix-Robotics/noetix_sdk_bumi)**, we are developing the logic, the MCP interfaces, and the motion controllers today. We build in the virtual realm so that the deployment to the physical chassis in Autumn 2026 is a "zero-day" integration.

- **Simulation**: Isaac Gym / Isaac Lab (via `noetix_n2_gym`).
- **Control**: Low-level joint torque and high-level gait control via DDS bridge.
- **Status**: Virtual Twin Composition Map in progress.

---

## 🏗️ The Virtual Twin Stack

The **Bumi vbot** is enabled by our existing federated MCP fleet:
- **robotics-mcp**: High-level orchestration and `robot_virtual` OSC paths.
- **resonite-mcp**: Presence, avatars, and session scaling.
- **unity3d-mcp**: SDK authoring and batch rig processing.
- **blender-mcp**: Mesh preparation and rig-hardening.

---

## 🕹️ Interface & Tools

Bumi-MCP exposes a standards-compliant interface for agentic control:
- **`bumi(operation="specs")`**: Returns the latest hardware/software manifests.
- **`bumi(operation="virtual_twin")`**: Status of the simulation-to-real (Sim2Real) bridge.
- **`bumi_agentic_workflow(goal)`**: SEP-1577 autonomous planning over the Bumi stack.

## License

MIT - 2026 sandraschi
