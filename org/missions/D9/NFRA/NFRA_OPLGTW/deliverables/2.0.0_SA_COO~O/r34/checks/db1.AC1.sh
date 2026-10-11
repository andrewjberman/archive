#!/usr/bin/env bash
# OPLGTW OG-db-1 AC1 (round-34 E6, row Z-S85): trunk's deploy-to-ec2.sh carries the OG-tl-1 allowlist read exactly as the
# live release does. meeting_allowlist.json is read as many times at HEAD as at the live ref; the script parses
# (bash -n); and the .env printf keeps every key that the live release or the cut base wrote, so nothing is dropped.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F=infra/aws/ec2/opal-gateway/deploy-to-ec2.sh
LIVE=c3af8687e4; CUT=522c85edf89629ae40bfb18f2176e991faf5f6f8
n_head=$(grep -c 'meeting_allowlist.json' "$F"); n_live=$(MSYS_NO_PATHCONV=1 git show "$LIVE:$F" | grep -c 'meeting_allowlist.json')
syn=no; bash -n "$F" && syn=yes
keys=$(python - "$LIVE" "$CUT" "$F" <<'PY'
import re, subprocess, sys
live, cut, f = sys.argv[1:4]
def keys(text):
    lines = [l for l in text.split("\n") if l.startswith("printf 'MOCK_GRAPH=0")]
    if len(lines) != 1:
        return None
    fmt = lines[0].split("'")[1]
    return set(re.findall(r"(?:^|\\n)([A-Z][A-Z0-9_]*)=", fmt))
show = lambda r: subprocess.run(["git", "show", "%s:%s" % (r, f)], capture_output=True).stdout.decode("utf-8")
head = keys(open(f, encoding="utf-8").read()); need = (keys(show(live)) or set()) | (keys(show(cut)) or set())
if head is None:
    print("printf line not found exactly once"); raise SystemExit(0)
missing = sorted(need - head)
print("required .env keys %d; at HEAD %d; missing %d %s" % (len(need), len(head), len(missing), missing))
PY
)
echo "meeting_allowlist.json reads: HEAD $n_head, live $n_live (want equal, >=1); bash -n: $syn"
echo "$keys"
if [ "$n_head" = "$n_live" ] && [ "$n_head" -ge 1 ] && [ "$syn" = yes ] && printf '%s' "$keys" | grep -q "missing 0 "; then
  echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
