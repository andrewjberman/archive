#!/usr/bin/env bash
# AMGT_RESAPP round 40 (copied from round 39 unchanged) -- THE ISSUER'S ONE REAL RUN at the round's last merge, on the shared 5174 build (Andrew-direct
# 2026-09-24: portal dev builds use 5174 ONLY, so no worker grades a render; every render-graded outcome is read here,
# once, and the six PNGs it writes are the person-read set FWD-29 names). Prints the main and body tables and, per
# graded column, the PASS count over six states. usage: bash <this> <port> <out-dir-relative-to-repo-root>
set -u
PORT=${1:?port}; OUT=${2:?out dir}
ROOT="$(git rev-parse --show-toplevel)"; cd "$ROOT/portal" || exit 2
mkdir -p "$ROOT/$OUT"
node scripts/ui-contract-check.mjs --port "$PORT" --scope main --out "$ROOT/$OUT" > "$ROOT/$OUT/run.log" 2>&1
echo "contract-check exit=$?"
for scope in main body; do
  echo "== scope=$scope PASS counts over six states =="
  for col in 2:bandContainersTopLevel 3:fonts 4:weights 5:sizes 6:radii 7:shadows 8:lowContrastChars 9:purpleFills; do
    i=${col%%:*}; name=${col#*:}
    n=$(awk -F'\t' -v i="$i" -v s="== scope=$scope" 'index($0,s)==1{f=1;next} /^== /{f=0} f && NF>=11 && $1!="state" && $i=="PASS" {c++} END{print c+0}' "$ROOT/$OUT/run.log")
    echo "  $name PASS $n of 6"
  done
  z=$(awk -F'\t' -v s="== scope=$scope" 'index($0,s)==1{f=1;next} /^== /{f=0} f && NF>=11 && $1!="state" && $12=="0" {c++} END{print c+0}' "$ROOT/$OUT/run.log")
  echo "  clippedTextBlocks==0 $z of 6"
done
ls "$ROOT/$OUT"/*.png 2>/dev/null | wc -l | sed 's/^/PNGs written: /'
