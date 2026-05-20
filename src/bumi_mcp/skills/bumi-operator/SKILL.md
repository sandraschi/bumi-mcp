---
name: bumi-operator
description: Operate bumi-mcp for Noetix Bumi specs, OSS links, optional robot bridge, and virtual twin composition via fleet MCPs.
---

# Bumi operator

**Description:** Control and monitor Noetix Bumi humanoid robots. Covers motor control, sensor reading, status monitoring, safety protocols, and fleet deployment across multiple robot instances.

## Trigger Phrases

- "Check Bumi robot status"
- "Get Bumi hardware specs"
- "Show me the virtual twin for Bumi"
- "Deploy Bumi fleet configuration"
- "What SDKs are available for Bumi?"
- "Start Bumi safety check"

## Tools

- `bumi(operation="info")` — Get general server info and available operations.
- `bumi(operation="specs")` — Return Noetix Bumi hardware specifications: degrees of freedom, sensor suite, compute module, battery specs.
- `bumi(operation="sdk_links")` — List OSS SDKs and API references for Bumi development.
- `bumi(operation="robot_status")` — Health check when `BUMI_ROBOT_URL` points at a bridge. Returns connectivity state.
- `bumi(operation="virtual_twin")` — Return composition map for Bumi digital twin. References components that must be rendered in resonite-mcp or robotics-mcp.
- `bumi(operation="fleet_peers")` — List connected fleet MCP instances and their roles.
- `bumi_agentic_workflow(goal="...")` — High-level goal planning when client supports sampling (SEP-1577).

## Physical Safety (CRITICAL)

- **Do NOT** command robot motion directly. bumi-mcp is a spec/bridge layer, not a locomotion controller.
- Use `robot_status` as HTTP health check only when `BUMI_ROBOT_URL` is configured.
- All physical operations require a vendor-approved API gateway with human-in-the-loop gate.
- Safety checks: confirm `robot_status` returns operational before any fleet orchestration that involves the physical Bumi unit.

## Virtual Twin

Call `virtual_twin` for the composition map. Implement traversal in **resonite-mcp** / **robotics-mcp**, not by expecting locomotion APIs inside bumi-mcp. The twin includes: joint hierarchy, sensor positions, skin mesh references, and interaction volumes.

## Fleet Deployment

1. `bumi(operation="status")` — Confirm server up.
2. `bumi(operation="fleet_peers")` — Discover connected MCP peers.
3. `bumi(operation="virtual_twin")` — Get the composition if visual rendering needed.
4. Delegate locomotion/physics to robotics-mcp, visual rendering to resonite-mcp.

## Examples

- "Show me Bumi specs" → `bumi(operation="specs")`
- "What fleet peers are connected to Bumi?" → `bumi(operation="fleet_peers")`
- "Set up Bumi virtual twin in Resonite" → `bumi(operation="virtual_twin")` → pass composition map to `resonite-mcp` tools
