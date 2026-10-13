#!/usr/bin/env bash
# OPLGTW OG-fd-2 AC2 (row Z-S91): W/FD2_DRIFT.json covers EVERY silver family but schwab, read from silver.tf's
# local.silver_families at HEAD (the denominator). Each family carries its packaged-copy drift against source (drift_lines,
# an int) and the drift's owner (drift_owner, non-empty). The release ask NEVER_WIDEN_ASK_OG-fd-2.md exists.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~61"
F="$W/FD2_DRIFT.json"; A="$W/NEVER_WIDEN_ASK_OG-fd-2.md"
{ [ -f "$F" ] && [ -f "$A" ]; } || { echo "drift file or ask absent"; echo "RESULT: FAIL"; exit 1; }
tf=$(mktemp); git show HEAD:infra/aws/terraform/opal-assets/silver.tf > "$tf"
python - "$(native "$F")" "$(native "$tf")" <<'PY'
import json, re, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
tf = open(sys.argv[2], encoding="utf-8").read()
blk = tf[tf.index("silver_families = {"):]
blk = blk[:blk.index("\n  }\n")]
want = set(re.findall(r"^\s{4}([a-z0-9]+)\s*=\s*\{", blk, re.M)) - {"schwab"}
fams = {f.get("family"): f for f in d.get("families", [])}
ok = [k for k in want if k in fams and isinstance(fams[k].get("drift_lines"), int) and fams[k].get("drift_owner")]
print("families required %d (from silver.tf); covered with drift_lines and drift_owner %d; missing %s"
      % (len(want), len(ok), sorted(want - set(ok))))
raise SystemExit(0 if want and len(ok) == len(want) else 1)
PY
rc=$?; rm -f "$tf"
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
