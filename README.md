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
1. **Base Control**: In-house Noetix E1-class motion board for 21-DOF bipedal stability (Master Actuator).
2. **Local Bridge**: A Raspberry Pi or Jetson host acting as the "Spinal Cord," bridging the E1's serial interface to the network.
3. **Remote Mothership**: Optional high-power PC for heavy-lift Agentic AI and RL inference via the local bridge.

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
