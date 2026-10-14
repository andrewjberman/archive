#!/usr/bin/env bash
# OPLGTW OG-ec-2 AC1 (round-37 G2-ECLIPSE, PHASE A): the plan is measured and asked, nothing applied.
#  - W/EC2_PLAN.json: the live converter code differs from the repo's at OG-ec-1's merge, the Terraform plan is exactly one change to the converter, the missing silver set is counted;
#  - W/NEVER_WIDEN_ASK_OG-ec-2.md carries the six headings (diff, widening, order, both branches, rollback, triggers).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS"
[ -f "$W/EC2_PLAN.json" ] && [ -f "$W/NEVER_WIDEN_ASK_OG-ec-2.md" ] || { echo "EC2_PLAN.json or the ask absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/EC2_PLAN.json")" "$(native "$W/NEVER_WIDEN_ASK_OG-ec-2.md")" <<'PYEOF'
import json, re, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
ask = open(sys.argv[2], encoding="utf-8").read().lower()
heads = [h for h in ("diff", "widening", "order", "both branches", "rollback", "triggers") if re.search(r"^#+ .*" + re.escape(h), ask, re.M)]
sha = lambda v: isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) is not None
differ = sha(d.get("live_code_sha256")) and sha(d.get("repo_code_sha256")) and d["live_code_sha256"] != d["repo_code_sha256"]
plan = str(d.get("tf_plan_summary", ""))
one = plan.startswith("0 to add, 1 to change, 0 to destroy")
miss = d.get("missing_silver_count")
print("live converter differs from the repo's: %s; plan '%s' is one change: %s; missing silver count %s; ask headings %d of 6" % ("yes" if differ else "no", plan[:40], "yes" if one else "no", miss, len(heads)))
sys.exit(0 if differ and one and isinstance(miss, int) and miss >= 1 and len(heads) == 6 else 1)
PYEOF
); rc=$?
printf '%s\n' "$res" | tr -d '\r'
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
