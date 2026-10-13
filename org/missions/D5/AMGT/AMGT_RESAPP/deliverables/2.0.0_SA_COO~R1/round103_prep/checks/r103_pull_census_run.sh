#!/bin/bash
# AMGT_RESAPP round-103 PREP -- FWD-40 (c): run the pull census over every resolved name in FOUR parallel shards, then merge. Run from a repository root.
#   bash r103_pull_census_run.sh <output directory>
# Reads S3 and DynamoDB only (the checkout's own handler, in-process); no write, no function invoke. Prints the merged summary's last three lines.
set -u
OUT="${1:?output directory}"
mkdir -p "$OUT"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT" || exit 1
for i in 0 1 2 3; do
  PYTHONPATH="$ROOT" python "$HERE/r103_pull_census.py" --shard "$i/4" --out "$OUT/shard_$i.json" > "$OUT/shard_$i.txt" 2>&1 &
done
wait
PYTHONPATH="$ROOT" python "$HERE/r103_pull_census.py" --merge "$OUT"/shard_*.json --out "$OUT/pull_census.json" > "$OUT/pull_census.txt" 2>&1
RC=$?
tail -3 "$OUT/pull_census.txt"
exit $RC
