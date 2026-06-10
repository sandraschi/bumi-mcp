import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Box,
  Boxes,
  Bot,
  Cpu,
  Gauge,
  Globe,
  Hand,
  Ruler,
  Terminal,
  Weight,
  Zap,
} from "lucide-react";
import { apiGet } from "@/api/client";
import { Card, CardTitle } from "@/components/ui/card";

type Health = { status: string; service: string };
type HeroSpecs = {
  height_cm: number;
  weight_kg: number;
  dof: number;
  battery: string;
  peak_torque_nm: number;
  speed_ms: number;
};
type HeroData = {
  product: string;
  vendor: string;
  tagline: string;
  type: string;
  status: string;
  availability: string;
  specs: HeroSpecs;
  interfaces: string[];
  programming: string[];
  links: Record<string, string>;
};
type FullResponse = { hero: HeroData; virtual_twin: Record<string, unknown> };

export function Dashboard() {
  const [health, setHealth] = useState<Health | null>(null);
  const [hero, setHero] = useState<HeroData | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const [h, f] = await Promise.all([
        apiGet<Health>("/api/health"),
        apiGet<FullResponse>("/api/hero"),
      ]);
      setHealth(h);
      setHero(f?.hero ?? null);
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const s = hero?.specs;
  const statCards = [
    { label: "Height", value: s ? `${s.height_cm}cm` : "—", icon: Ruler },
    { label: "Weight", value: s ? `${s.weight_kg}kg` : "—", icon: Weight },
    { label: "DOF", value: s ? String(s.dof) : "—", icon: Gauge },
    { label: "Peak torque", value: s ? `${s.peak_torque_nm}Nm` : "—", icon: Zap },
    { label: "Speed", value: s ? `${s.speed_ms}m/s` : "—", icon: Bot },
    { label: "Battery", value: s ? s.battery : "—", icon: Cpu },
    { label: "Interfaces", value: hero?.interfaces ? String(hero.interfaces.length) : "—", icon: Hand },
    { label: "Languages", value: hero?.programming ? String(hero.programming.length) : "—", icon: Box },
  ];

  const tiles = [
    { to: "/virtual", label: "Virtual twin", desc: "Fleet integration and twin map", icon: Boxes },
    { to: "/fleet", label: "Fleet links", desc: "robotics, Resonite, WorldLabs bridge", icon: Globe },
    { to: "/tools", label: "MCP tools", desc: "stdio + HTTP /mcp tool surface", icon: Terminal },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Noetix Bumi</h1>
          <p className="text-muted-foreground text-base mt-1 max-w-2xl">
            {hero?.tagline ?? "Hero humanoid — specs, OSS links, virtual-twin guidance"}
          </p>
          <p className="text-amber-400 text-sm font-semibold mt-2 flex items-center gap-2">
            <Zap size={16} />
            Physical unit expected early 2027. This dashboard is the preparation layer for control,
            telemetry, and twin integration.
          </p>
        </div>
        <div className="text-right text-xs text-muted-foreground">
          <div>{hero?.vendor ?? "—"}</div>
          <div className="mt-1">
            <span
              className={`inline-block w-2 h-2 rounded-full mr-1 ${
                health?.status === "ok" ? "bg-green-500" : "bg-amber-500"
              }`}
            />
            {health?.status ?? "offline"}
          </div>
        </div>
      </div>

      {err && (
        <div className="rounded-lg border border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm">
          API: {err} — start backend on port 10774:{" "}
          <code className="text-xs">uv run python -m bumi_mcp --serve</code>
        </div>
      )}

      {/* Specs grid */}
      <div>
        <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <Cpu size={20} className="text-primary" /> Specifications
        </h2>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {statCards.map((st) => (
            <Card key={st.label}>
              <div className="flex items-center gap-3">
                <st.icon className="h-5 w-5 text-primary shrink-0" />
                <div className="min-w-0">
                  <CardTitle className="text-xs text-muted-foreground font-normal uppercase tracking-wider">
                    {st.label}
                  </CardTitle>
                  <p className="text-xl font-semibold mt-0.5">{st.value}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Interfaces & Programming tags */}
      {hero && (
        <div className="grid gap-6 sm:grid-cols-2">
          {hero.interfaces && hero.interfaces.length > 0 && (
            <Card>
              <CardTitle className="text-sm mb-2 flex items-center gap-2">
                <Hand size={16} className="text-primary" /> Interfaces
              </CardTitle>
              <div className="flex flex-wrap gap-1.5">
                {hero.interfaces.map((item) => (
                  <span
                    key={item}
                    className="text-xs px-2 py-0.5 rounded-full bg-primary/10 border border-primary/20 text-primary"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </Card>
          )}
          {hero.programming && hero.programming.length > 0 && (
            <Card>
              <CardTitle className="text-sm mb-2 flex items-center gap-2">
                <Box size={16} className="text-primary" /> Programming
              </CardTitle>
              <div className="flex flex-wrap gap-1.5">
                {hero.programming.map((item) => (
                  <span
                    key={item}
                    className="text-xs px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}

      {/* Links */}
      {hero?.links && Object.keys(hero.links).length > 0 && (
        <Card>
          <CardTitle className="text-sm mb-2">Links</CardTitle>
          <div className="flex flex-wrap gap-x-6 gap-y-1">
            {Object.entries(hero.links).map(([k, v]) => (
              <a
                key={k}
                href={v}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary hover:underline"
              >
                {k}
              </a>
            ))}
          </div>
        </Card>
      )}

      {/* Nav tiles */}
      <div className="grid gap-4 sm:grid-cols-3">
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
