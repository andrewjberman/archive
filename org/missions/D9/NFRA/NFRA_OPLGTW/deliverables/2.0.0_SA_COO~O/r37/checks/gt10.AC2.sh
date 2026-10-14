#!/usr/bin/env bash
# OPLGTW OG-gt-10 AC2 (round-37 G1-FIX, FWD-22): NO shipped gateway module indexes Path(...).parents at a depth the host does not have.
# The host path /opt/opal-gateway/app/<m>.py has 4 parents (indices 0-3); an index of 4 or more raises IndexError at import there.
# Scans every app/*.py but the by-hand generator gen_rivalfunds_location.py (denominator printed); the guard is a count of indices >= 3 as the margin, want 0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(python - <<'PY'
import glob, re
# gen_rivalfunds_location.py is a repo-side generator run by hand, never imported by the service (its readers load the JSON it writes)
files = sorted(f for f in glob.glob("infra/aws/ec2/opal-gateway/app/*.py") if not f.endswith("gen_rivalfunds_location.py"))
bad = []
for f in files:
    for i, line in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
        if line.lstrip().startswith("#"):
            continue
        for m in re.finditer(r"\.parents\[(\d+)\]", line):
            if int(m.group(1)) >= 3:
                bad.append("%s:%d [%s]" % (f.split("/")[-1], i, m.group(1)))
print("parents[N>=3] in shipped app modules: %d of %d file(s) scanned (want 0)%s" % (len(bad), len(files), (" -- " + ", ".join(bad)) if bad else ""))
raise SystemExit(0 if not bad and len(files) > 20 else 1)
PY
); rc=$?
printf '%s
' "$res" | tr -d ''
[ "$rc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
