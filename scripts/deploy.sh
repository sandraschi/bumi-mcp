#!/usr/bin/env bash
# Deploy all Pi-side files to a fresh yahboom_ros2_final setup.
# Run from the repo root on the PC. Connects via SSH.
# Usage: ./deploy_pi.sh [pi-ip] [ssh-user]
# Default: 192.168.1.11 / pi

set -e
IP="${1:-192.168.1.11}"
USER="${2:-pi}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Boomy Pi Deploy v2.4.1 ==="
echo "Target: $USER@$IP"
echo ""

# ── Config ──────────────────────────────────────────────────────────────────
DRIVER_CT="yahboom_ros2_final"      # driver container name
MISSION_SRC="$REPO_ROOT/ros2/boomy_mission_executor"
ME_PY="$REPO_ROOT/minimal_mission_executor.py"
VB_PY="$REPO_ROOT/vision_bridge.py"

# ── 1. Copy files to Pi host ─────────────────────────────────────────────────
echo "[1/6] Copying files to Pi host..."
scp "$ME_PY" "$VB_PY" "$USER@$IP:/tmp/"
ssh "$USER@$IP" "sudo cp /tmp/minimal_mission_executor.py /minimal_mission_executor.py && sudo cp /tmp/vision_bridge.py /detection_bridge.py 2>/dev/null; mkdir -p /tmp/bme_src"
rsync -a --exclude='__pycache__' --exclude='.ipynb_checkpoints' "$MISSION_SRC/" "$USER@$IP:/tmp/bme_src/"
ssh "$USER@$IP" 'echo OK || echo FAIL'

# ── 2. Build mission executor in container ────────────────────────────────────
echo "[2/6] Building mission executor in container..."
ssh "$USER@$IP" "
docker exec $DRIVER_CT bash -c '
mkdir -p /root/yahboomcar_ws/src/boomy_mission_executor/boomy_mission_executor
mkdir -p /root/yahboomcar_ws/src/boomy_mission_executor/launch
mkdir -p /root/yahboomcar_ws/src/boomy_mission_executor/resource
touch /root/yahboomcar_ws/src/boomy_mission_executor/resource/boomy_mission_executor
'
"
for f in package.xml setup.py setup.cfg; do
    docker cp "$MISSION_SRC/$f" "$DRIVER_CT:/root/yahboomcar_ws/src/boomy_mission_executor/$f"
done
for f in __init__.py mission_executor_node.py detection_utils.py; do
    docker cp "$MISSION_SRC/boomy_mission_executor/$f" "$DRIVER_CT:/root/yahboomcar_ws/src/boomy_mission_executor/boomy_mission_executor/$f"
done
docker cp "$MISSION_SRC/launch/mission_executor.launch.py" "$DRIVER_CT:/root/yahboomcar_ws/src/boomy_mission_executor/launch/"
docker cp "$ME_PY" "$DRIVER_CT:/minimal_mission_executor.py"
docker cp "$VB_PY" "$DRIVER_CT:/detection_bridge.py"
ssh "$USER@$IP" "docker exec $DRIVER_CT bash -c 'source /opt/ros/humble/setup.bash && cd /root/yahboomcar_ws && colcon build --packages-select boomy_mission_executor 2>&1 | tail -3'"
echo "Build complete."

# ── 3. Create entrypoint scripts in container ────────────────────────────────
echo "[3/6] Creating entrypoint scripts..."
ssh "$USER@$IP" 'docker exec -i '"$DRIVER_CT"' bash -c "cat > /entrypoint.sh" <<"EOF"
#!/usr/bin/env bash
set -e
source /opt/ros/humble/setup.bash
[ -f /root/yahboomcar_ws/install/setup.bash ] && source /root/yahboomcar_ws/install/setup.bash
echo "[entry] Starting rosbridge..."
ros2 launch rosbridge_server rosbridge_websocket_launch.xml &
sleep 4
echo "[entry] Starting driver bringup..."
ros2 launch yahboomcar_bringup yahboomcar_bringup.launch.py &
sleep 4
echo "[entry] Starting mission executor..."
PYTHONPATH="/root/yahboomcar_ws/src/boomy_mission_executor:${PYTHONPATH}" python3 -u -c "import rclpy; from boomy_mission_executor.mission_executor_node import main; main()" &
sleep 2
echo "[entry] Starting detection bridge..."
python3 /detection_bridge.py &
echo "[entry] All services running."
wait
EOF
chmod +x '"$DRIVER_CT:/entrypoint.sh"'
'

# ── 4. Fix Ollama binding and kill host rosbridge ─────────────────────────────
echo "[4/6] Configuring Ollama and rosbridge..."
ssh "$USER@$IP" '
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo -e "[Service]\nEnvironment=\"OLLAMA_HOST=0.0.0.0:11434\"" | sudo tee /etc/systemd/system/ollama.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl restart ollama
# Kill host rosbridge if running
PID=$(pgrep -f "rosbridge_websocket" 2>/dev/null || true)
if [ -n "$PID" ]; then
    # Only kill if not in docker
    if ! grep -q "docker" /proc/$PID/cmdline 2>/dev/null; then
        sudo kill $PID 2>/dev/null || true
        echo "Killed host rosbridge PID $PID"
    fi
fi
echo "Ollama configured, host rosbridge cleared."
'

# ── 5. Deploy coffee shop script and auto-bringup ─────────────────────────────
echo "[5/6] Deploying utility scripts on Pi host..."
ssh "$USER@$IP" 'cat > /home/pi/coffeeshop_connect.sh' <"$REPO_ROOT/docs/ops/COFFEESHOP_DEMO.md" 2>/dev/null || true
# Actually, read the script from the doc or use a separate file
# Write a proper coffeeshop script
ssh "$USER@$IP" 'cat > /home/pi/coffeeshop_connect.sh' <<"EOF"
#!/bin/bash
SSID="$1"; PASS="$2"
[ -z "$SSID" ] && { echo "Usage: $0 SSID [PASSWORD]"; exit 1; }
sudo systemctl stop dnsmasq 2>/dev/null || true
sudo systemctl disable dnsmasq 2>/dev/null || true
sudo systemctl stop hostapd 2>/dev/null || true
if [ -n "$PASS" ]; then sudo nmcli dev wifi connect "$SSID" password "$PASS"
else sudo nmcli dev wifi connect "$SSID"; fi
sleep 5; IP=$(hostname -I | awk '{print $1}')
TAIL=$(tailscale ip -4 2>/dev/null || echo "not installed")
echo "Boomy CLIENT MODE — WiFi IP: $IP  Tailscale: $TAIL"
EOF
ssh "$USER@$IP" 'chmod +x /home/pi/coffeeshop_connect.sh'

# Also write auto_bringup.sh
ssh "$USER@$IP" 'cat > /home/pi/auto_bringup.sh' <<"EOF"
#!/bin/bash
CT="yahboom_ros2_final"; SD="yahboom_rosbridge_sidecar"
until docker ps >/dev/null 2>&1; do sleep 1; done
until [ "$(docker inspect -f '{{.State.Running}}' $SD 2>/dev/null)" = "true" ] &&
      [ "$(docker inspect -f '{{.State.Running}}' $CT 2>/dev/null)" = "true" ]; do sleep 2; done
docker exec -d $CT /entrypoint.sh
EOF
ssh "$USER@$IP" 'chmod +x /home/pi/auto_bringup.sh'

# ── 6. Pull and restart ──────────────────────────────────────────────────────
echo "[6/6] Restarting robot services..."
ssh "$USER@$IP" "docker restart $DRIVER_CT"
sleep 5
ssh "$USER@$IP" "docker exec -d $DRIVER_CT /entrypoint.sh"
sleep 12

echo "=== Deploy complete ==="
echo "Pi: $USER@$IP"
echo "To use: set YAHBOOM_IP=$IP and start the MCP server."
echo "For coffee shop mode: ssh $USER@$IP && sudo /home/pi/coffeeshop_connect.sh SSID PASSWORD"
