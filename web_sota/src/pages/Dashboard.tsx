import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Boxes, Bot, Terminal } from "lucide-react";
import { apiGet } from "@/api/client";
import { Card, CardTitle } from "@/components/ui/card";

type Health = { status: string; service: string };
type Stats = {
  product: string;
  vendor: string;
  dof: number;
  virtual_twin_servers: number;
};

export function Dashboard() {
  const [health, setHealth] = useState<Health | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [h, s] = await Promise.all([
          apiGet<Health>("/api/health"),
          apiGet<Stats>("/api/stats"),
        ]);
        if (!cancelled) {
          setHealth(h);
          setStats(s);
        }
      } catch (e) {
        const m = e instanceof Error ? e.message : String(e);
        if (!cancelled) setErr(m);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const tiles = [
    { to: "/virtual", label: "Virtual twin", desc: "Fleet composition map", icon: Boxes },
    { to: "/fleet", label: "Fleet links", desc: "robotics, Resonite, WorldLabs", icon: Bot },
    { to: "/tools", label: "MCP tools", desc: "stdio + HTTP /mcp", icon: Terminal },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Noetix Bumi</h1>
        <p className="text-muted-foreground text-sm mt-1">
          Hero humanoid MCP — specs, OSS, optional <code className="text-primary">BUMI_ROBOT_URL</code>,
          Resonite path via fleet servers.
        </p>
      </div>

      {err && (
        <div className="rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-2 text-sm">
          API: {err} — start backend on <code>10774</code>:{" "}
          <code className="text-xs">uv run python -m bumi_mcp --serve</code>
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardTitle className="text-sm text-muted-foreground font-normal">API</CardTitle>
          <p className="text-2xl font-semibold mt-1">{health?.status ?? "…"}</p>
        </Card>
        <Card>
          <CardTitle className="text-sm text-muted-foreground font-normal">DOF</CardTitle>
          <p className="text-2xl font-semibold mt-1">{stats?.dof ?? "—"}</p>
        </Card>
        <Card>
          <CardTitle className="text-sm text-muted-foreground font-normal">Virtual twin MCPs</CardTitle>
          <p className="text-2xl font-semibold mt-1">{stats?.virtual_twin_servers ?? "—"}</p>
        </Card>
        <Card>
          <CardTitle className="text-sm text-muted-foreground font-normal">Product</CardTitle>
          <p className="text-lg font-semibold mt-1 leading-tight">{stats?.product ?? "—"}</p>
        </Card>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {tiles.map((t) => (
          <Link key={t.to} to={t.to} className="block group">
            <Card className="h-full transition-transform group-hover:scale-[1.01]">
              <div className="flex gap-3">
                <t.icon className="h-8 w-8 text-primary shrink-0" />
                <div>
                  <CardTitle>{t.label}</CardTitle>
                  <p className="text-sm text-muted-foreground mt-1">{t.desc}</p>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
