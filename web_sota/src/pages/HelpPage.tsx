import { Card, CardTitle } from "@/components/ui/card";

export function HelpPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Help</h1>
      <Card>
        <CardTitle className="text-base mb-2">Quick start</CardTitle>
        <ol className="text-sm text-muted-foreground list-decimal pl-5 space-y-2">
          <li>
            Backend: <code className="text-primary">uv sync</code> then{" "}
            <code className="text-primary">uv run python -m bumi_mcp --serve</code>
          </li>
          <li>
            Dashboard: <code className="text-primary">cd web_sota</code> then{" "}
            <code className="text-primary">npm install</code> and{" "}
            <code className="text-primary">npm run dev</code> (or <code>start.ps1</code>)
          </li>
          <li>
            Cursor MCP: stdio command <code className="text-primary">uv run python -m bumi_mcp --stdio</code>{" "}
            with cwd at repo root; set <code className="text-primary">PYTHONPATH=src</code> if needed.
          </li>
        </ol>
      </Card>
      <Card>
        <CardTitle className="text-base mb-2">China retail context</CardTitle>
        <p className="text-sm text-muted-foreground">
          MCP tool <code className="text-primary">bumi(operation=&quot;market&quot;)</code> summarizes
          Noetix, the humbot wave, JD.com example SKUs, and tier-1 walk-up retail — see repo README for
          markdown links.
        </p>
      </Card>
      <Card>
        <CardTitle className="text-base mb-2">Safety</CardTitle>
        <p className="text-sm text-muted-foreground">
          bumi-mcp does not expose raw torque or motion primitives until a vendor-approved bridge is
          integrated. Treat any future control as gated and human-supervised.
        </p>
      </Card>
    </div>
  );
}
