import { Card, CardTitle } from "@/components/ui/card";

export function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Settings</h1>
      <Card>
        <CardTitle className="text-base mb-3">Environment</CardTitle>
        <dl className="text-sm space-y-2 font-mono">
          <div>
            <dt className="text-muted-foreground">BUMI_MCP_HOST</dt>
            <dd>API bind (default 127.0.0.1)</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">BUMI_MCP_PORT</dt>
            <dd>API port (default 10774)</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">BUMI_ROBOT_URL</dt>
            <dd>Optional HTTP base for local bridge — enables bumi(operation=&quot;robot_status&quot;)</dd>
          </div>
        </dl>
      </Card>
    </div>
  );
}
