#!/usr/bin/env bash
# OPLGTW OG-g-2 AC1 (CTO ruling msg 28154 (2)): WRITE_CAPABLE_GUARD.json states whether a WRITE_CAPABLE principal's
# Schwab request is EVALUATED against its data grant or BYPASSES the entitlement guard, cites the deciding code at the
# live release 3a7d6a7dc8 (every citation resolves: the file exists at that commit and the line is within it), and its
# ungranted-master probe outcome agrees with the verdict (EVALUATES <=> REFUSED; BYPASSES <=> SERVED).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~23/WRITE_CAPABLE_GUARD.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
python - "$(native "$F")" <<'EOF'
import json, subprocess, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); LIVE = "3a7d6a7dc85fe3c54a4b63b27b59055abc9adca7"
v = d.get("guard_verdict"); pr = d.get("probe", {}); cites = d.get("code_citations", [])
good = 0
for c in cites:
    b = subprocess.run(["git", "show", "%s:%s" % (LIVE, c.get("path", ""))], capture_output=True)
    if b.returncode == 0 and 1 <= int(c.get("line", 0)) <= len(b.stdout.splitlines()): good += 1
agree = (v == "EVALUATES" and pr.get("outcome") == "REFUSED") or (v == "BYPASSES" and pr.get("outcome") == "SERVED")
print("verdict %s; probe tier %s outcome %s; citations resolving at 3a7d6a7dc8 %d of %d; verdict and probe agree %s"
      % (v, pr.get("principal_tier"), pr.get("outcome"), good, len(cites), agree))
ok = v in ("EVALUATES", "BYPASSES") and pr.get("principal_tier") == "WRITE_CAPABLE" and cites and good == len(cites) and agree
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
EOF
