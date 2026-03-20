---
name: bumi-operator
description: Operate bumi-mcp for Noetix Bumi specs, OSS links, optional robot bridge, and virtual twin composition via fleet MCPs.
---

# Bumi operator

## Tools

- `bumi(operation="info"|"specs"|"sdk_links"|"robot_status"|"virtual_twin"|"fleet_peers")`
- `bumi_agentic_workflow(goal="...")` when the client supports sampling (SEP-1577).

## Physical safety

Do not command motion without vendor-approved API and human gate. Use `robot_status` only as HTTP health when `BUMI_ROBOT_URL` points at your bridge.

## Virtual twin

Call `virtual_twin` for the composition map. Implement traversal in **resonite-mcp** / **robotics-mcp**, not by expecting locomotion APIs inside bumi-mcp.
