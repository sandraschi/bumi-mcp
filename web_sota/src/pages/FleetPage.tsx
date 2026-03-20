import { useEffect, useState } from "react";
import { ExternalLink } from "lucide-react";
import { apiGet } from "@/api/client";
import { Card, CardTitle } from "@/components/ui/card";

type Hub = { id: string; label: string; description: string; url: string };

export function FleetPage() {
  const [hubs, setHubs] = useState<Hub[]>([]);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const d = await apiGet<{ hubs: Hub[] }>("/api/fleet");
        setHubs(d.hubs);
      } catch (e) {
        setErr(e instanceof Error ? e.message : String(e));
      }
    })();
  }, []);

  if (err) {
    return <p className="text-amber-400 text-sm">{err}</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Fleet</h1>
      <p className="text-sm text-muted-foreground">
        Curated neighbors for virtual + physical robotics. Edit{" "}
        <code className="text-primary">src/bumi_mcp/data/fleet_default.json</code> in the repo.
      </p>
      <div className="grid gap-4 md:grid-cols-2">
        {hubs.map((h) => (
          <Card key={h.id}>
            <div className="flex items-start justify-between gap-2">
              <CardTitle className="text-base">{h.label}</CardTitle>
              <a
                href={h.url}
                target="_blank"
                rel="noreferrer"
                className="text-primary shrink-0"
                title="Open"
              >
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
            <p className="text-sm text-muted-foreground mt-2">{h.description}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}
