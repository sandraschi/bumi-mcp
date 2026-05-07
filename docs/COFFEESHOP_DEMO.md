# Coffee Shop Demo: Pi in Client Mode

**Scenario**: Boomy goes to a coffee shop, connects to the shop's WiFi, and you control it from your laptop at home (or anywhere) via Tailscale. Live video, telemetry, autonomous missions — all over the internet.

## Network Architecture

```
Your living room                        Coffee Shop
┌─────────────────┐                   ┌─────────────────────┐
│ Laptop (Goliath) │   Tailscale      │ Boomy (Pi 5)        │
│                  │   100.x.x.x      │                      │
│ MCP server:10892 │◄─────────────────│ rosbridge:9090       │
│ Webapp:10893     │   SSH:22         │ SSH:22               │
│                  │   MJPEG stream   │ video_feed:6001      │
└─────────────────┘                   │ Ollama:11434         │
                                      └─────────────────────┘
```

- **Pi acts as WiFi client** (not AP) — connects to the coffee shop's SSID
- **Tailscale** creates a secure WireGuard tunnel between PC and Pi, regardless of network topology (NAT, firewalls, etc.)
- All traffic (rosbridge WebSocket, SSH, MJPEG stream) goes through Tailscale

## Setup

### 1. Install Tailscale on Pi

```bash
# Install (one-time, needs internet — run at home before demo)
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Authenticate in browser — Pi joins your tailnet
```

### 2. Install Tailscale on PC

Download from https://tailscale.com/download — sign in with same account.

### 3. Switch Pi to Client Mode

Run the `coffeeshop_connect.sh` script on the Pi:

```bash
sudo bash /home/pi/coffeeshop_connect.sh "CoffeeShopSSID" "password"
```

This will:
- Stop the Raspbot AP (disable dnsmasq/hostapd)
- Connect to the coffee shop WiFi via NetworkManager
- Print the Pi's IP and Tailscale IP

### 4. Start MCP Server on PC

```powershell
$env:YAHBOOM_IP = "<tailscale-ip-of-pi>"
uv run python -m yahboom_mcp.server --mode dual --port 10892
```

The MCP server connects to rosbridge + SSH through Tailscale. The webapp at `http://localhost:10893/dashboard` works as usual.

### 5. Revert to AP Mode (when back home)

```bash
# Re-enable the Raspbot AP
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq
sudo systemctl restart hostapd
# Or just reboot — the Pi boots back into AP mode
```

## Script: coffeeshop_connect.sh

```bash
#!/bin/bash
# Switch Pi from Raspbot AP to WiFi client mode
# Usage: sudo bash coffeeshop_connect.sh SSID PASSWORD

SSID="$1"
PASS="$2"

if [ -z "$SSID" ]; then
    echo "Usage: $0 SSID [PASSWORD]"
    exit 1
fi

echo "[*] Stopping Raspbot AP services..."
sudo systemctl stop dnsmasq 2>/dev/null || true
sudo systemctl disable dnsmasq 2>/dev/null || true
sudo systemctl stop hostapd 2>/dev/null || true

echo "[*] Connecting to WiFi: $SSID..."
if [ -n "$PASS" ]; then
    sudo nmcli dev wifi connect "$SSID" password "$PASS"
else
    sudo nmcli dev wifi connect "$SSID"
fi

echo "[*] Waiting for IP..."
sleep 5
IP=$(hostname -I | awk '{print $1}')
TAIL=$(tailscale ip -4 2>/dev/null || echo "not installed")

echo ""
echo "=== Boomy is in CLIENT MODE ==="
echo "WiFi IP:      $IP"
echo "Tailscale IP: $TAIL"
echo ""
echo "On your PC, set:"
echo "  \$env:YAHBOOM_IP = \"$TAIL\""
echo "Then start the MCP server."
echo ""
echo "To revert to AP mode: reboot, or run:"
echo "  sudo systemctl enable dnsmasq && sudo systemctl start dnsmasq"
```

## Limitations

- **No direct AP**: In client mode, you can't connect to the Raspbot AP. The Pi is on the coffee shop's network. All control goes through Tailscale.
- **Internet required**: Both Pi and PC need internet for Tailscale. If the coffee shop WiFi has a captive portal, connect the Pi's browser first (SSH + `lynx` or set the portal up at home).
- **Latency**: Video stream adds ~200-500ms over Tailscale. Fine for demo visibility, not for real-time driving.
- **Bandwidth**: MJPEG stream uses ~5-10 Mbps. Most coffee shop WiFi handles this easily.
- **Battery**: Boomy runs on battery during the demo (~1-2 hours with motors + camera + Pi).
