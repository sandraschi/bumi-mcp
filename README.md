# bumi-mcp (Noetix Bumi Android)

[![GitHub](https://img.shields.io/badge/GitHub-sandraschi%2Fbumi--mcp-181717?logo=github)](https://github.com/sandraschi/bumi-mcp)

<table border="0">
  <tr>
    <td width="220" valign="top">
      <img src="https://www.noetixrobotics.com/mtsc/uploads/Ckeditor/Images/2026-03-26/Bumi.webp" width="220" alt="Noetix Bumi Android">
    </td>
    <td valign="top">
      The <strong>Noetix Bumi</strong> is one of the <strong>newest</strong> humanoids in the consumer/research robot market, offering reasonable performance at a price point (~$1,400) comparable to hi-end car type robots like the Yahboom RosMaster X3. Or, surprisingly, a hi-end smartphone. Bumi is a great toy for tinkerers and kids of all ages and a true breakthrough on the road to ubiquitous service robots. Because of its small size (1 m) it is nonthreatning and kid friendly.
    </td>
  </tr>
</table>


---

## 🤖 The Android: Noetix Bumi

- **Form Factor**: Sleek, minimalistic white "Bipedal Android" chassis.

- **Dimensions**: ~100 cm (3.3 ft) height | ~20 kg weight.
- **Kinematics**: 21 Degrees of Freedom (DOF) with high-torque precision servos.
- **Compute**: Specialized motion control (Base) | Optional NVIDIA Jetson Orin (Research/EDU).
- **Locomotion**: Advanced bipedal walking, stabilization, and expressive gesture control.
- **Identity**: A true "Android" assistant capable of navigating complex human environments.

### 🏗️ Architecture: The "Modular Android"
Bumi utilizes a decoupled **Mothership-Bridge-Controller** design:
1. **Base Control**: In-house Noetix E1-class motion board (21-DOF stability). Runs **Micro-ROS (DDS-XRCE)** for network-native telemetry. Handles hard real-time balance loops.
2. **Local Bridge**: **Raspberry Pi or Jetson (Required)**. Acts as the network bridge for WiFi/5G connectivity.
3. **Remote Mothership**: PC/Workstation (RTX 4090+) for heavy-lift Agentic AI via the local bridge.

> [!IMPORTANT]
> **Hardware Connectivity Note**: The E1 master controller board lacks a native wireless chipset. For wireless mothership control, an intermediate host (Pi/Jetson) is required to bridge the serial/Ethernet stream. Alternatively, an **Ethernet-to-WiFi bridge/dongle** can be used to expose the raw E1 network interface directly to the WLAN.

---

## 📅 Project Status: Autumn 2026

**We do not have a physical Bumi unit yet.** This is our **Autumn Project** hardware target.

> [!IMPORTANT]
> **Active Training Ground**: While the Bumi is in the Virtual Twin phase, we are running the **[yahboom-mcp](file:///D:/Dev/repos/yahboom-mcp)** with a **physical in-house Raspbot (Boomy)**. We use the Yahboom platform as our primary real-world testbed for ROS 2 navigation, semantic SLAM, and agentic autonomy, ensuring that the software stack is battle-tested before the Bumi hardware arrives.

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
