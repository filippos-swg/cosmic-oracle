#!/bin/bash
# ASTRA — start everything: oracle loop + local server, then open the experience.
# Usage:  bash run.sh          (or: bash run.sh dashboard | testcard)
cd "$(dirname "$0")"

# 1. dependency check (first run only)
if ! python3 -c "import swisseph" 2>/dev/null; then
  echo "Installing pyswisseph (first run only)..."
  python3 -m pip install --user pyswisseph \
    || python3 -m pip install --break-system-packages pyswisseph \
    || { echo "pip install failed — try: python3 -m ensurepip --user"; exit 1; }
fi

# 2. stop any previous instances (kill by name AND by port — a stale server
#    holding port 8000 would silently keep serving old code)
pkill -f "oracle.py" 2>/dev/null
pkill -f "server.py" 2>/dev/null
sleep 1
STALE=$(lsof -ti :8000 2>/dev/null)
[ -n "$STALE" ] && { echo "killing stale server on port 8000 (pid $STALE)"; kill -9 $STALE; sleep 1; }

# 3. start the oracle loop (writes visual/oracle.json every 60s)
python3 oracle.py > /tmp/astra_oracle.log 2>&1 &
echo "oracle loop started  (log: /tmp/astra_oracle.log)"

# 4. start the local server
python3 visual/server.py > /tmp/astra_server.log 2>&1 &
echo "server started       (log: /tmp/astra_server.log)"
sleep 2

# 5. open the experience
PAGE="tv.html"
[ "$1" = "dashboard" ] && PAGE="index.html"
[ "$1" = "testcard" ]  && PAGE="testcard.html"
open "http://localhost:8000/$PAGE"

echo ""
echo "ASTRA is running:  http://localhost:8000/$PAGE"
echo "Stop everything:   pkill -f oracle.py; pkill -f server.py"

# 6. sanity check: is the running server the current code?
if curl -s "http://localhost:8000/natal?d=1&m=1&y=1990" | grep -q transits; then
  echo "server check:      OK (natal transits active)"
else
  echo "server check:      WARNING — server responding without transits (stale process?)"
fi
