import { useEffect, useState } from "react";
import { apiGet } from "@/api/client";
import { Card, CardTitle } from "@/components/ui/card";

type HeroPayload = {
  hero: {
    tagline: string;
    specs: Record<string, unknown>;
    programming: string[];
  };
  virtual_twin: {
    message: string;
    mcp_servers: { id: string; role: string }[];
    related_repos: string[];
  };
};

export function VirtualPage() {
  const [data, setData] = useState<HeroPayload | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const h = await apiGet<HeroPayload>("/api/hero");
        setData(h);
      } catch (e) {
        setErr(e instanceof Error ? e.message : String(e));
      }
    })();
  }, []);

  if (err) {
    return <p className="text-amber-400 text-sm">{err}</p>;
  }
  if (!data) {
    return <p className="text-muted-foreground text-sm">Loading…</p>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Virtual twin</h1>
        <p className="text-sm text-muted-foreground mt-1">{data.virtual_twin.message}</p>
      </div>
      <Card>
        <CardTitle className="text-base mb-2">Bumi (physical product)</CardTitle>
        <p className="text-sm text-muted-foreground">{data.hero.tagline}</p>
        <ul className="mt-3 text-sm list-disc pl-5 space-y-1">
          {data.hero.programming.map((p) => (
            <li key={p}>{p}</li>
          ))}
        </ul>
      </Card>
      <div className="grid gap-4 md:grid-cols-2">
        {data.virtual_twin.mcp_servers.map((s) => (
          <Card key={s.id}>
            <CardTitle className="text-base font-mono">{s.id}</CardTitle>
            <p className="text-sm text-muted-foreground mt-2">{s.role}</p>
          </Card>
        ))}
      </div>
      <Card>
        <CardTitle className="text-base mb-2">Related repos</CardTitle>
        <ul className="text-sm space-y-1">
          {data.virtual_twin.related_repos.map((u) => (
            <li key={u}>
              <a href={u} className="text-primary hover:underline break-all">
                {u}
              </a>
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
