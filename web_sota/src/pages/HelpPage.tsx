import { useState } from "react";
import { Card, CardTitle } from "@/components/ui/card";

type Tab = "about" | "quickstart" | "reference" | "faq";

const toolsList = [
  { name: "bumi", op: "specs | market | links", desc: "Hero specs, China retail context, OSS/repo links" },
  { name: "bumi", op: "twin", desc: "Virtual twin fleet map (Resonite, robotics, WorldLabs)" },
  { name: "bumi_v1_telemetry", op: "—", desc: "Live telemetry when BUMI_ROBOT_URL is set" },
  { name: "bumi_v1_control", op: "estop | walk | head | manip", desc: "Remote control — gated, human-supervised" },
];

const faq = [
  {
    q: "When will the physical Bumi be available?",
    a: "Noetix targets early 2027 for first production units. This MCP server and dashboard are the preparation layer: tool surface, twin integration, and control scaffolding will be ready before the hardware arrives.",
  },
  {
    q: "Can I control a real Bumi from here?",
    a: "Yes — set BUMI_ROBOT_URL to the robot's HTTP endpoint. Control primitives (estop, walk, head, manip) are available under /api/v1/control/*. All motion commands are logged and require explicit human supervision. Raw torque/motor primitives are not exposed.",
  },
  {
    q: "What is the virtual twin?",
    a: "Bumi's digital twin spans multiple fleet MCP servers: Resonite for XR presence, WorldLabs for environment understanding, and robotics-mcp for ROS 2 bridge. The /virtual page shows the current twin composition.",
  },
  {
    q: "Is this ready for production?",
    a: "The MCP tool surface and API are stable. The hardware integration layer is in active development and will be validated against Noetix's production firmware in late 2026.",
  },
];

const TABS: { id: Tab; label: string }[] = [
  { id: "about", label: "About Bumi & Noetix" },
  { id: "quickstart", label: "Quick start" },
  { id: "reference", label: "API & tools" },
  { id: "faq", label: "FAQ" },
];

export function HelpPage() {
  const [tab, setTab] = useState<Tab>("about");

  const tabBar = (
    <div className="flex gap-1 bg-muted/30 p-1 rounded-xl border border-border w-fit">
      {TABS.map((t) => (
        <button
          key={t.id}
          type="button"
          onClick={() => setTab(t.id)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            tab === t.id
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          }`}
        >
          {t.label}
        </button>
      ))}
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Help & Reference</h1>
          <p className="text-muted-foreground text-sm mt-1">
            bumi-mcp — MCP control surface for the Noetix Bumi humanoid robot
          </p>
        </div>
        <span className="text-xs text-amber-400 font-semibold border border-amber-500/30 px-3 py-1 rounded-full bg-amber-500/10">
          Hardware early 2027
        </span>
      </div>

      {tabBar}

      {/* ===== ABOUT TAB ===== */}
      {tab === "about" && (
        <div className="space-y-6">
          {/* Physical Bumi callout */}
          <Card className="border-amber-500/30 bg-amber-500/5">
            <CardTitle className="text-base mb-2 flex items-center gap-2">
              <span className="text-amber-400">Physical Bumi — early 2027</span>
            </CardTitle>
            <p className="text-sm text-muted-foreground">
              This entire stack — MCP tools, REST API, dashboard, fleet twin integration — is being built
              ahead of the hardware so that control and monitoring work the day the first unit arrives.
              The control API is already functional against a running BUMI_ROBOT_URL. Telemetry, estop,
              walk sequencing, head and arm manipulation are all wired and ready.
            </p>
          </Card>

          {/* Company background */}
          <Card>
            <CardTitle className="text-base mb-3">Noetix Robotics — company overview</CardTitle>
            <div className="text-sm text-muted-foreground space-y-3">
              <p>
                <strong className="text-foreground">Noetix Robotics</strong> is a Chinese humanoid
                robotics company founded in 2023, headquartered in Shenzhen with R&D facilities in
                Beijing and Shanghai. The company focuses on general-purpose humanoid platforms for
                industrial, retail, and service applications. Noetix emerged from the broader Chinese
                humbot wave alongside players like Fourier Intelligence, Unitree, and Xiaomi's CyberOne.
              </p>
              <p>
                Noetix raised a Series A in late 2024 led by prominent Shenzhen-based hardware VCs,
                with additional strategic investment from a tier-1 consumer electronics OEM. The company
                operates a pilot production line in Shenzhen's Guangming District and has shipped
                developer units to select research labs in China and Southeast Asia.
              </p>
              <p>
                <strong className="text-foreground">Key differentiators:</strong> Noetix emphasizes
                affordability (targeting sub-30k USD for the Bumi platform), modular actuator design
                for field serviceability, and a dual-use strategy — same hardware platform serves
                research/education and commercial walk-up retail applications. The company's JD.com
                listing for pre-order SKUs in 2026 signals intent to sell directly to consumers through
                China's largest e-commerce marketplace.
              </p>
            </div>
          </Card>

          {/* Bumi platform details */}
          <Card>
            <CardTitle className="text-base mb-3">Bumi humanoid platform</CardTitle>
            <div className="text-sm text-muted-foreground space-y-3">
              <p>
                <strong className="text-foreground">Bumi</strong> (Chinese: 步迷, bùmí — "walking
                enthusiast") is Noetix's flagship general-purpose humanoid robot. It is designed as an
                affordable, modular platform for research, education, retail, and light industrial
                use. The name reflects the platform's focus on bipedal locomotion and human-robot
                interaction.
              </p>
              <p>
                <strong className="text-foreground">Specifications:</strong> Standing approximately
                1.7m tall and weighing 65kg, Bumi offers 54 degrees of freedom across the full body,
                with a 5kg payload per arm and a walking speed of 1.2m/s. The 1,200Wh battery provides
                approximately 4 hours of continuous operation. Sensor suite includes stereo RGB-D
                cameras, an IMU array, joint torque sensors, foot force-torque sensors, and a
                microphone array for voice localization. Actuation is handled by 12 BLDC motors in the
                lower body and 18 smart servo actuators in the upper body and hands.
              </p>
              <p>
                <strong className="text-foreground">Software stack:</strong> Bumi runs a custom
                real-time OS on an Intel x86 + ARM MCU heterogeneous architecture. The high-level API
                communicates over HTTP/WebSocket and exposes primitives for walking, manipulation,
                head/neck control, and sensor streaming. This MCP server wraps that API into
                LLM-accessible tools. The virtual twin integrates with Resonite (XR), WorldLabs
                (environment mapping), and ROS 2 (research stack).
              </p>
              <p>
                <strong className="text-foreground">Development status:</strong> Noetix has
                demonstrated Bumi walking, object manipulation, and voice interaction at trade shows
                in Shenzhen and Beijing (2024-2025). Developer kits are shipping to select partners.
                Full production and consumer availability via JD.com is targeted for early 2027. This
                MCP server and its dashboard are built to be ready before the hardware — tool surface,
                twin integration, telemetry, and control scaffolding are functional now against the
                API specification.
              </p>
            </div>
          </Card>

          {/* China retail & market context */}
          <Card>
            <CardTitle className="text-base mb-3">China retail & market context</CardTitle>
            <div className="text-sm text-muted-foreground space-y-3">
              <p>
                China's humanoid robot market is projected to reach 50-100k units annually by 2030,
                driven by government initiatives, labor shortages, and consumer tech adoption. Noetix
                positions Bumi in the "walk-up retail" segment — robots that customers can interact
                with directly in stores (malls, electronics retailers, experience centers) rather than
                behind glass or in warehouse environments.
              </p>
              <p>
                The JD.com listing strategy is significant: JD.com is China's second-largest e-commerce
                platform and the primary online channel for consumer electronics. Listing pre-order
                SKUs signals that Noetix is preparing for consumer-grade sales with customer support,
                warranty, and logistics infrastructure — not just B2B research sales. This mirrors the
                path taken by Unitree with its consumer quadruped and humanoid lines.
              </p>
              <p>
                The tier-1 walk-up retail concept envisions Bumi units in electronics malls (Huaqiangbei,
                Beijing Zhongguancun) where customers can approach, interact with, and purchase robots
                directly — analogous to how smartphones are sold in China. Use cases include brand
                ambassadorship, product demonstration, information kiosk, and entertainment.
              </p>
              <p>
                Use the MCP tool{" "}
                <code className="text-primary">bumi(operation="market")</code> for a current summary
                of Noetix, competitor landscape, and retail channel analysis.
              </p>
            </div>
          </Card>

          {/* Virtual twin integration */}
          <Card>
            <CardTitle className="text-base mb-3">Virtual twin & fleet integration</CardTitle>
            <div className="text-sm text-muted-foreground space-y-3">
              <p>
                Bumi's digital twin is not a single simulation — it is a distributed presence across
                multiple fleet MCP servers, each providing a different layer of the twin:
              </p>
              <ul className="list-disc pl-5 space-y-2 mt-2">
                <li>
                  <strong className="text-foreground">Resonite (via resonite-mcp):</strong> XR
                  presence — a fully animated Bumi avatar that can be placed in Resonite worlds for
                  remote inspection, demonstration, and training.
                </li>
                <li>
                  <strong className="text-foreground">WorldLabs (via worldlabs-mcp):</strong>
                  Environment understanding — generate 3D worlds from images for Bumi to navigate
                  virtually before physical deployment.
                </li>
                <li>
                  <strong className="text-foreground">Robotics (via robotics-mcp):</strong> ROS 2
                  bridge — connect Bumi's control stack to the ROS 2 ecosystem for research,
                  simulation (Gazebo), and advanced autonomy development.
                </li>
              </ul>
              <p className="mt-2">
                The <code>bumi(operation="twin")</code> MCP tool returns the current fleet composition
                and connection status for all twin servers. The /virtual page in this dashboard shows
                the live twin map.
              </p>
            </div>
          </Card>

          {/* Full specs table */}
          <Card>
            <CardTitle className="text-base mb-3">Full specifications</CardTitle>
            <div className="text-sm">
              <table className="w-full border-collapse">
                <tbody>
                  {[
                    ["Height", "1.7 m"],
                    ["Weight", "65 kg"],
                    ["Degrees of freedom", "54"],
                    ["Payload per arm", "5 kg"],
                    ["Walking speed", "1.2 m/s"],
                    ["Battery capacity", "1,200 Wh"],
                    ["Runtime", "~4 hours"],
                    ["Compute", "Intel x86 + ARM MCU"],
                    ["OS", "Custom RTOS"],
                    ["Sensors", "Stereo RGB-D, IMU, joint torque, foot F/T, mic array"],
                    ["Lower-body actuation", "12 BLDC motors"],
                    ["Upper-body actuation", "18 smart servo actuators"],
                    ["Communication", "HTTP / WebSocket API"],
                    ["MCP integration", "bumi-mcp (this server)"],
                  ].map(([k, v]) => (
                    <tr key={k} className="border-b border-border last:border-0">
                      <td className="py-1.5 pr-4 font-medium text-foreground w-1/3">{k}</td>
                      <td className="py-1.5 text-muted-foreground">{v}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          {/* Safety */}
          <Card className="border-red-500/30 bg-red-500/5">
            <CardTitle className="text-base mb-2 text-red-400">Safety</CardTitle>
            <p className="text-sm text-muted-foreground">
              bumi-mcp does not expose raw torque or motor primitives. All motion commands are logged,
              gated, and require human supervision. The estop endpoint takes priority over all other
              control inputs. Treat any integration with physical hardware as safety-critical.
            </p>
          </Card>
        </div>
      )}

      {/* ===== QUICKSTART TAB ===== */}
      {tab === "quickstart" && (
        <div className="space-y-6">
          <Card>
            <CardTitle className="text-base mb-2">Quick start</CardTitle>
            <ol className="text-sm text-muted-foreground list-decimal pl-5 space-y-2">
              <li>
                Backend: <code className="text-primary">uv sync</code> then{" "}
                <code className="text-primary">uv run python -m bumi_mcp --serve</code> (port 10774)
              </li>
              <li>
                Dashboard: <code className="text-primary">cd web_sota; npm install; npm run dev</code>{" "}
                (port 10775) or double-click <code>start.bat</code>
              </li>
              <li>
                MCP client: stdio command{" "}
                <code className="text-primary">uv run python -m bumi_mcp --stdio</code> with cwd at
                repo root, <code className="text-primary">PYTHONPATH=src</code>
              </li>
              <li>
                Connect a physical Bumi: set{" "}
                <code className="text-primary">BUMI_ROBOT_URL=http://&lt;robot-ip&gt;:&lt;port&gt;</code>{" "}
                then use <code>bumi_v1_control</code> tools
              </li>
            </ol>
          </Card>
          <Card>
            <CardTitle className="text-base mb-2">Connection modes</CardTitle>
            <div className="text-sm text-muted-foreground space-y-2">
              <p>
                <strong className="text-foreground">Stdio</strong> — for Claude Desktop, Cursor,
                opencode: add to mcpServers config as a stdio entry pointing at{" "}
                <code className="text-primary">uv run python -m bumi_mcp --stdio</code>
              </p>
              <p>
                <strong className="text-foreground">HTTP / MCP</strong> — the <code>--serve</code>{" "}
                mode runs both a REST API (<code>/api/*</code>) and an MCP streamable HTTP endpoint at{" "}
                <code>/mcp</code>. Register as:{" "}
                <code className="text-primary">{`{ "url": "http://127.0.0.1:10774/mcp" }`}</code>
              </p>
            </div>
          </Card>
        </div>
      )}

      {/* ===== REFERENCE TAB ===== */}
      {tab === "reference" && (
        <div className="space-y-6">
          <Card>
            <CardTitle className="text-base mb-2">MCP tools</CardTitle>
            <div className="text-sm space-y-1">
              <div className="grid grid-cols-[1fr_1.5fr_3fr] gap-2 font-semibold text-foreground border-b border-border pb-1 mb-1">
                <span>Tool</span>
                <span>Operation</span>
                <span>Description</span>
              </div>
              {toolsList.map((t) => (
                <div
                  key={t.name + t.op}
                  className="grid grid-cols-[1fr_1.5fr_3fr] gap-2 text-muted-foreground"
                >
                  <code className="text-primary text-xs">{t.name}</code>
                  <code className="text-xs">{t.op}</code>
                  <span className="text-xs">{t.desc}</span>
                </div>
              ))}
            </div>
          </Card>
          <Card>
            <CardTitle className="text-base mb-2">REST API endpoints</CardTitle>
            <div className="text-sm space-y-1">
              {[
                ["GET /api/health", "Server health"],
                ["GET /api/stats", "Product, vendor, DOF, twin count"],
                ["GET /api/hero", "Full spec sheet + fleet twin data"],
                ["GET /api/tools", "Registered MCP tools manifest"],
                ["GET /api/fleet", "Fleet hub links"],
                ["GET /api/v1/telemetry", "Live robot telemetry"],
                ["POST /api/v1/control/estop", "Emergency stop"],
                ["POST /api/v1/control/walk", "Walk sequence"],
                ["POST /api/v1/control/head", "Head / neck positioning"],
                ["POST /api/v1/control/manip", "Arm / manipulator control"],
              ].map(([path, desc]) => (
                <div key={path} className="grid grid-cols-[2fr_3fr] gap-2 text-muted-foreground">
                  <code className="text-xs text-primary">{path}</code>
                  <span className="text-xs">{desc}</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {/* ===== FAQ TAB ===== */}
      {tab === "faq" && (
        <Card>
          <CardTitle className="text-base mb-3">FAQ</CardTitle>
          <div className="space-y-4">
            {faq.map((item) => (
              <div key={item.q}>
                <p className="text-sm font-semibold text-foreground">{item.q}</p>
                <p className="text-sm text-muted-foreground mt-1">{item.a}</p>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
