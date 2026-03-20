# bumi-mcp

[![GitHub](https://img.shields.io/badge/GitHub-sandraschi%2Fbumi--mcp-181717?logo=github)](https://github.com/sandraschi/bumi-mcp)

**Canonical repo:** [github.com/sandraschi/bumi-mcp](https://github.com/sandraschi/bumi-mcp) · `git clone https://github.com/sandraschi/bumi-mcp.git`

**Noetix Bumi** humanoid — FastMCP **3.1** MCP server with SOTA web dashboard, hero specs, Noetix OSS links, optional local robot HTTP ping, and a **virtual-twin composition map**. The **Bumi vbot** is not built inside this repo; it is **enabled by your existing vbot stack**: **robotics-mcp** (orchestration, `robot_virtual`, OSC, vbot CRUD), **resonite-mcp** (sessions, avatars, worlds), **unity3d-mcp** (Editor / batch / Resonite SDK authoring), **blender-mcp** (meshes, rig prep, assets), **worldlabs-mcp** (splats / world ingest toward Resonite), plus other fleet MCPs and their webapps as you wire them.

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1-blue)](https://gofastmcp.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Physical Bumi vs virtual Bumi (read this)

**We do not have a physical Bumi unit yet.** This repo is real software; the robot on the loading dock is not.

- **Supply:** Noetix is **heavily oversubscribed**. If you are queueing for hardware, assume **months**, not weeks, before a unit ships — and treat any date as tentative until the box arrives.
- **What you can do today:** A **Bumi vbot** (virtual twin) is **eminently doable now** because the **sandraschi fleet already ships vbot-oriented MCP servers and dashboards** — e.g. **robotics-mcp**, **resonite-mcp**, **unity3d-mcp**, **blender-mcp**, **worldlabs-mcp** (and peers like **avatar-mcp** where you use it). Model in Unity or Blender, drive presence in Resonite, orchestrate from **robotics-mcp**; **bumi-mcp** stays the **Bumi-specific** layer (specs, OSS, prompts, fleet hints). Same MCP habits — **deliberate prep** for the day the physical bot shows up.
- **`BUMI_ROBOT_URL` / `robot_status`:** For future use when *you* have a local HTTP bridge to a real Bumi or sim; until then, expect `connected: false` and use the **virtual** path above.

## Noetix, China’s humbot wave, and where buying actually happens

**Noetix** (松延动力, Beijing) is part of the **consumer/education humanoid** story in China — Bumi is positioned as a compact home- or school-friendly “humbot” with ROS/Linux-friendly tooling and ecosystem hooks (including **JD**-side integrations on vendor materials), not only industrial arms.

**The “humbot explosion”** (2025–2026) is structural: many vendors and models, aggressive roadmaps, and a **national standard system** for humanoid robotics and embodied AI (common specs, safety, applications, compute). That combination — **retail channels + standards + manufacturing depth** — is why SKUs like Bumi can show up next to phones on **e-commerce** while still hitting **allocation and wait lists**.

**Buying (verify live pages before paying):**

- **[JD.com (京东)](https://www.jd.com)** — Bumi variants have been listed as consumer SKUs (pre-order / deposit windows move fast). Example listing hubs: [Pro-class SKU](https://item.jd.com/100323634120.html), [EDU-oriented SKU](https://item.jd.com/100323635530.html) — treat as **examples**, not guarantees of current stock.
- **Walk-up and offline in tier-1 cities** — **Shenzhen, Shanghai, Beijing** remain the practical mesh of **app commerce + physical retail**: JD **pick-up / offline stores**, mall **electronics chains**, **robotics demos**, and dense CE corridors (Shenzhen’s component ecosystems are the textbook case). Those are realistic places people **discover and close** humbot purchases — but **exact Noetix pop-ups or partner stores change by campaign**, so confirm with **[Noetix contact / sales](https://noetixrobotics.com/contact-us)** and the **live JD listing**, not this README.

**In MCP:** `bumi(operation="market")` returns structured copy of this context for agents.

## Ports

| Service | Port |
|--------|------|
| Backend (FastAPI + MCP `/mcp`) | **10774** |
| Frontend (Vite) | **10775** |

## Quick start

```powershell
cd D:\Dev\repos\bumi-mcp
uv sync
uv run python -m bumi_mcp --serve
```

Other terminal:

```powershell
cd D:\Dev\repos\bumi-mcp\web_sota
.\start.ps1
```

**Cursor MCP (stdio):**

```json
{
  "mcpServers": {
    "bumi-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/bumi-mcp", "run", "python", "-m", "bumi_mcp", "--stdio"],
      "env": { "PYTHONPATH": "D:/Dev/repos/bumi-mcp/src" }
    }
  }
}
```

## Tools

- **`bumi(operation=...)`** — `info` | `specs` | `sdk_links` | `market` | `robot_status` | `virtual_twin` | `fleet_peers`
- **`bumi_agentic_workflow(goal)`** — SEP-1577 sampling over Bumi + fleet context
- **Prompt:** `bumi_quick_start` (focus: physical | virtual | fleet)

## Environment

| Variable | Purpose |
|----------|---------|
| `BUMI_MCP_HOST` | Bind host (default `127.0.0.1`) |
| `BUMI_MCP_PORT` | Backend port (default `10774`) |
| `BUMI_ROBOT_URL` | Optional HTTP base for a local bridge; `robot_status` tries `/health`, `/api/health`, `/status` |

## What this is / isn’t

- **Is:** Product + OSS discovery, fleet documentation, **virtual-twin roadmap**, optional health probe when a bridge exists, agentic planning hook. A sane way to **practice the mesh** before hardware lands.
- **Isn’t:** A claim that we ship or own physical Bumi today, or vendor-certified torque/motion APIs (those come **after** hardware + documented interfaces).

## Related (vbot stack)

- [robotics-mcp](https://github.com/sandraschi/robotics-mcp) — `noetix_info`, vbot CRUD, `robot_virtual`, Resonite OSC, workflows
- [resonite-mcp](https://github.com/sandraschi/resonite-mcp) — Resonite automation + webapp
- [unity3d-mcp](https://github.com/sandraschi/unity3d-mcp) — Unity Editor / batch / robotics pipelines
- [blender-mcp](https://github.com/sandraschi/blender-mcp) — 3D assets and rig work
- [worldlabs-mcp](https://github.com/sandraschi/worldlabs-mcp) — splat / world paths toward Resonite
- [mcp-central-docs/projects/bumi-mcp](https://github.com/sandraschi/mcp-central-docs/tree/master/projects/bumi-mcp) — central index

## License

MIT
