#!/usr/bin/env bash
# OPLGTW OG-o-5 AC1, AMENDED A1 (CTO msg 29057; CVO ADJUDICATION_v6.Z: 7.3 is the bucket readback): the runbook's section 7 carries the
# three anchors the order names, and rb.AC1-AC3 still pass (no regression). The MEANING is graded by 3.0.0_SA_CVO~O
# re-running OGO2-J1 at L9; this check proves the text landed where the order says.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
R="infra/aws/ec2/opal-gateway/runbooks/SCHWAB_PILOT_RUNBOOK.md"; C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/round2/checks"
python - "$(native "$R")" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
def sec(a, b):
    m = re.search(r"^### %s\b.*?(?=^### %s\b|^## |\Z)" % (re.escape(a), re.escape(b)), t, re.S | re.M)
    return m.group(0) if m else ""
s71, s72, s73 = sec("7.1", "7.2"), sec("7.2", "7.3"), sec("7.3", "7.4")
a1 = "The deploy template re-renders `schwab`" in s71
a2 = "re-apply 7.1" in s72 and "`integration_enabled=false`" in s72
a4 = "schwab_status.py" in s71
reads = ("get-bucket-versioning", "get-bucket-encryption", "get-public-access-block", "get-bucket-policy-status")
a5 = "Bucket reads:" in s73 and all(r in s73 for r in reads) and s73.count("--bucket opal-data-assets") >= 4
a6 = "schwab_status.py" not in s73 and "does not run the AWS read" not in s73
print("7.1 re-render anchor %s; 7.2 re-apply + integration_enabled=false anchors %s; 7.1 status read %s; 7.3 four bucket reads %s; 7.3 no HEALTH read and no \"does not run\" %s" % (a1, a2, a4, a5, a6))
sys.exit(0 if (a1 and a2 and a4 and a5 and a6) else 1)
PY
arc=$?; n=0
for c in rb.AC1 rb.AC2 rb.AC3; do bash "$C/$c.sh" >/dev/null 2>&1 && n=$((n+1)); done
echo "rb.AC1-AC3 passing $n of 3"
[ "$arc" = 0 ] && [ "$n" = 3 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
