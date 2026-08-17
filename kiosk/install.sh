#!/bin/bash
# ASTRA — install the installation MacBook as an appliance (STATUS_REPORT §6).
#
#   bash kiosk/install.sh            install and start
#   bash kiosk/install.sh uninstall  stop and remove
#
# Installs three launchd agents in the LOGIN session (not root): the oracle
# loop, the local server, and Chrome in kiosk mode. All three have KeepAlive,
# so a crash restarts them and a power cut comes back on its own.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS="$HOME/Library/LaunchAgents"
JOBS=(oracle server kiosk)
DOMAIN="gui/$(id -u)"

boot_out() {
  launchctl bootout "$DOMAIN/se.southnorth.astra.$1" 2>/dev/null || true
}

if [ "${1:-}" = "uninstall" ]; then
  for j in "${JOBS[@]}"; do
    boot_out "$j"
    rm -f "$AGENTS/se.southnorth.astra.$j.plist"
    echo "removed  se.southnorth.astra.$j"
  done
  echo "ASTRA agents removed. The repo is untouched."
  exit 0
fi

command -v python3 >/dev/null || { echo "python3 not found"; exit 1; }
python3 -c "import swisseph" 2>/dev/null || {
  echo "pyswisseph missing — run: python3 -m pip install --user pyswisseph"
  exit 1
}
[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] || {
  echo "Google Chrome not installed at the expected path"; exit 1; }

mkdir -p "$AGENTS"

# run.sh and the agents both bind port 8000; leaving a manual copy running
# makes launchd's server flap on ThrottleInterval forever
pkill -f "python3 .*oracle\.py"  2>/dev/null || true
pkill -f "python3 .*server\.py"  2>/dev/null || true

for j in "${JOBS[@]}"; do
  src="$ROOT/kiosk/se.southnorth.astra.$j.plist"
  dst="$AGENTS/se.southnorth.astra.$j.plist"
  sed "s|__ASTRA_ROOT__|$ROOT|g" "$src" > "$dst"
  plutil -lint "$dst" >/dev/null
  boot_out "$j"
  launchctl bootstrap "$DOMAIN" "$dst"
  echo "loaded   se.southnorth.astra.$j"
done

# the kiosk script receives the root as argv from its agent — nothing in the
# repo is rewritten by installing
chmod +x "$ROOT/kiosk/astra-kiosk.sh"

echo
echo "waiting for the server..."
for i in $(seq 1 30); do
  if curl -sf -o /dev/null http://localhost:8000/tv.html; then
    echo "server:  OK"
    break
  fi
  sleep 1
done
curl -sf "http://localhost:8000/natal?d=1&m=1&y=1990" | grep -q transits \
  && echo "natal:   OK (transits active)" \
  || echo "natal:   WARNING — responding without transits"
[ -f "$ROOT/visual/oracle.json" ] && echo "sky:     oracle.json present" \
  || echo "sky:     WARNING — oracle.json not written yet (give it 60s)"

cat <<'NOTES'

Installed. Chrome should now be in kiosk mode on the tv.html ceremony.

  status:  launchctl list | grep astra
  logs:    tail -f /tmp/astra_oracle.log /tmp/astra_server.log
  stop:    bash kiosk/install.sh uninstall

STILL MANUAL — launchd cannot do these, and the piece is not exhibition-ready
until they are done on the machine itself:

  1. System Settings > Users & Groups > auto-login ON for the exhibition user.
  2. Energy: never sleep on power. Closed-lid running needs power AND a display
     attached. `caffeinate` in the kiosk script covers the session, not the
     firmware settings.
  3. Notifications: Do Not Disturb on a permanent schedule. One banner over the
     ceremony ends the illusion.
  4. Software Update: automatic updates OFF. A restart prompt mid-exhibition is
     the single most likely way this piece dies.
  5. Spotlight: exclude the repo folder (indexing spikes the particle engine).
  6. Display resolution set to whatever the CRT converter likes — usually
     800x600 or 720x576. Tune overscan on the converter first, then CSS via
     /testcard.html. Edit only CONFIG.SAFE and CONFIG.TYPE_SCALE in tv.html.
  7. ENTITY_COUNT in tv.html CONFIG: drop to 40000-60000 on the old MacBook.
  8. Weekly reboot for long runs:
       sudo pmset repeat restart MTWRFSU 05:00
  9. Wi-Fi is optional by design. Verify by turning it off and running a full
     ceremony — the ephemeris is local and the page tolerates fetch failure.

NOTES
