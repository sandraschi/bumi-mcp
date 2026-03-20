"""Noetix Bumi — curated product facts and upstream OSS pointers."""

from __future__ import annotations

from typing import Any

# Hero humanoid (Noetix headline product, 2026). Specs from public materials; verify before motion control.
BUMI_HERO: dict[str, Any] = {
    "product": "Noetix Bumi",
    "vendor": "Noetix Robotics (Beijing) / 诺提克斯",
    "tagline": "Compact consumer humanoid — walking, running, dance, gymnastics; ROS / Linux SDKs.",
    "type": "humanoid",
    "specs": {
        "height_cm": 94,
        "weight_kg": 12,
        "dof": 21,
        "battery": "48 V 3.5 Ah, ~2–3 h runtime",
        "peak_torque_nm": 50,
        "speed_ms": 0.5,
    },
    "interfaces": [
        "USB",
        "HDMI",
        "Ethernet",
        "WiFi",
        "Voice + vision (vendor)",
    ],
    "programming": [
        "Graphical (education)",
        "ROS / ROS2",
        "Python",
        "C++",
    ],
}

NOETIX_GITHUB: list[dict[str, str]] = [
    {
        "name": "noetix_sdk_e1",
        "url": "https://github.com/Noetix-Robotics/noetix_sdk_e1",
        "note": "C++ SDK for E1-class controller (BSD-3-Clause); build on Ubuntu 20.04/22.04.",
    },
    {
        "name": "noetix_n2_gym",
        "url": "https://github.com/Noetix-Robotics/noetix_n2_gym",
        "note": "N2 humanoid RL / Isaac Gym / sim2sim reference.",
    },
]

OPENSOURCE_PAGE = "https://noetixrobotics.com/opensource"

# Context for agents / README — not legal or shopping advice; URLs and availability change.
MARKET_CONTEXT: dict[str, Any] = {
    "noetix_story": (
        "Noetix Robotics (松延动力, Beijing) positions **Bumi** as a compact **consumer / education** "
        "humanoid (~94 cm, ~21 DOF) with Linux/ROS-friendly stacks and JD ecosystem ties (e.g. "
        "**Joy Inside** class integrations on vendor materials). It is one visible face of China’s "
        "push to make humanoids legible to households and schools, not only factories."
    ),
    "china_humbot_explosion": (
        "China’s **humanoid (humbot)** lane scaled fast in 2025–2026: dozens of vendors and models, "
        "heavy patent and production rhetoric, and a **national standard framework** for humanoid "
        "robotics and embodied AI (lifecycle, safety, “brain” compute, applications). The story is "
        "**volume + standards + supply chain**, not only lab demos — which is why consumer SKUs like "
        "Bumi can list on mass retail while still facing **allocation / wait lists**."
    ),
    "standards_press_reference": (
        "English-language overview of the national standard system rollout: "
        "http://www.china.org.cn/2026-03/01/content_118353416.shtml"
    ),
    "buying_channels": [
        {
            "channel": "JD.com (京东) — online",
            "note": (
                "Bumi variants have appeared as **pre-order / retail SKUs** on JD (consumer electronics "
                "channel). SKUs and deposit windows change — read the live listing."
            ),
            "example_urls": [
                "https://item.jd.com/100323634120.html",
                "https://item.jd.com/100323635530.html",
            ],
        },
    ],
    "offline_tier1_china": (
        "**Shenzhen, Shanghai, Beijing** (and other tier-1 hubs) are where **walk-up retail culture** "
        "still matters alongside apps: JD **offline stores / pick-up points**, mall **electronics chains**, "
        "**robotics roadshows**, and dense components corridors (e.g. Shenzhen Huaqiangbei-style zones) "
        "are normal discovery paths for new CE SKUs. **Noetix HQ is in Beijing (Changping / Future Science "
        "City per their site)** — use official sales channels to confirm any **in-person demo, partner "
        "store, or pick-up**; this README does not claim a fixed flagship address."
    ),
    "vendor_contact": "https://noetixrobotics.com/contact-us",
    "disclaimer": "Availability, price, and import rules vary by region. Confirm on JD + vendor before paying.",
}

VIRTUAL_TWIN_FLEET: dict[str, Any] = {
    "message": (
        "Bumi vbot is enabled by the existing sandraschi vbot MCP stack — not implemented inside bumi-mcp. "
        "Compose: robotics-mcp (orchestration, robot_virtual, vbot CRUD, OSC); resonite-mcp (sessions, avatars, worlds); "
        "unity3d-mcp (Editor/batch, Resonite SDK authoring); blender-mcp (meshes, rig/asset prep); "
        "worldlabs-mcp (splats / world ingest → Resonite). Add avatar-mcp or others as your mesh requires."
    ),
    "mcp_servers": [
        {
            "id": "robotics-mcp",
            "role": "Orchestration, vbot CRUD, robot_virtual, Resonite OSC, workflows",
        },
        {"id": "resonite-mcp", "role": "Resonite session, avatar, world tools + webapp"},
        {"id": "unity3d-mcp", "role": "Unity automation, virtual robotics, Resonite SDK pipeline"},
        {"id": "blender-mcp", "role": "3D modeling, rigging, export for game/VR pipelines"},
        {"id": "worldlabs-mcp", "role": "Gaussian splat / world ingest toward Resonite"},
        {"id": "avatar-mcp", "role": "Optional — VRM/avatar bridge where you use it in the stack"},
    ],
    "related_repos": [
        "https://github.com/sandraschi/robotics-mcp (noetix_info + NOETIX_BUMI.md)",
        "https://github.com/sandraschi/unity3d-mcp",
        "https://github.com/sandraschi/blender-mcp",
    ],
}
