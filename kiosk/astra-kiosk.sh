#!/bin/bash
# ASTRA — launch the experience in Chrome as a kiosk. Called by launchd at
# login; safe to run by hand for a dress rehearsal.
#
# The dedicated user-data-dir matters: on a normal profile Chrome shows
# "Chrome didn't shut down correctly" after any power cut, and a restore bar
# over a 1950s television is the end of the illusion.

# The repo root arrives as $1 from the launchd agent. It is NOT templated into
# this file: install.sh used to sed it in place, which rewrote a tracked file
# and left the repo permanently dirty after every install.
ROOT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
URL="http://localhost:8000/tv.html"
PROFILE="$HOME/Library/Application Support/astra-kiosk-profile"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

[ -x "$CHROME" ] || { echo "Chrome not found at $CHROME"; exit 1; }

# wait for the server — launchd starts everything at once and Chrome is fast
for i in $(seq 1 60); do
  curl -sf -o /dev/null "http://localhost:8000/tv.html" && break
  sleep 1
done

# never sleep, never dim, never blank; -s keeps this tied to the kiosk process
caffeinate -dimsu -w $$ &

exec "$CHROME" \
  --kiosk \
  --user-data-dir="$PROFILE" \
  --noerrdialogs \
  --disable-session-crashed-bubble \
  --disable-infobars \
  --disable-features=Translate,TranslateUI,InfiniteSessionRestore \
  --disable-pinch \
  --overscroll-history-navigation=0 \
  --no-first-run \
  --no-default-browser-check \
  --check-for-update-interval=31536000 \
  --autoplay-policy=no-user-gesture-required \
  --force-device-scale-factor=1 \
  --app="$URL"
