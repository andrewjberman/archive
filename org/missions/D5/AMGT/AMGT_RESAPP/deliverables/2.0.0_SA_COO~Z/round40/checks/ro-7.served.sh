#!/usr/bin/env bash
# AMGT_RESAPP round 40 -- capture the SERVED plane for BA_US_Equity into a temp dir (rn-5's served_capture.py, copied so
# it writes nowhere in the repo). Prints the temp dir on its last line. A read (lambda invoke of Opal's own function).
set -u
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT" || exit 2
T="$(mktemp -d)"
cp org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~150/served_capture.py "$T/served_capture.py"
PYTHONPATH="$ROOT" python "$T/served_capture.py" > "$T/capture.log" 2>&1 || { tail -5 "$T/capture.log"; echo "capture failed"; exit 1; }
echo "$T"
