#!/usr/bin/env bash
# MX-s-16 AC2 (control): the writer of record still writes -- in bd-silver-merge's logs of the last 36 hours, the NEWEST
# summary of each graded table (transactions, realized, allocations) reads failures=0 (allocations prints no failures
# field; its summary line being present is its pass). UNREALIZED is printed and NOT graded: at the round-6 base its every
# run reads failures=6 on 6 new files (row NFRA_MCPINDEX-Z-S72); MX-s-16 PHASE A owes that diagnosis.
. "$(dirname "$0")/_root.sh"
AWS="$(pwd)/.tools/aws"
S=$(python -c "import time; print(int((time.time() - 36*3600) * 1000))")
o=$(timeout 60 "$AWS" logs filter-log-events --log-group-name /aws/lambda/bd-silver-merge --start-time "$S" --query 'events[].message' --output text 2>&1 | tr -d '\r' | tr '\t' '\n')
out=$(printf '%s\n' "$o" | python -c '
import re, sys
cur = None; last = {}
for line in sys.stdin:
    if "Incremental Merge [transactions]" in line: cur = "transactions"
    elif "Allocation Incremental Merge" in line: cur = "allocations"
    elif "Realized Incremental Merge" in line and "Unrealized" not in line: cur = "realized"
    elif "Unrealized Incremental Merge" in line: cur = "unrealized"
    if "SUMMARY" in line and cur:
        last[cur] = line.strip()
bad = 0
for t in ("transactions", "realized", "allocations", "unrealized"):
    s = last.get(t)
    if t == "unrealized":
        print("NOT GRADED (Z-S72): unrealized newest: %s" % s); continue
    ok = bool(s) and (t == "allocations" or re.search(r"failures=0([^0-9]|$)", s) is not None)
    bad += not ok
    print("%s %s newest: %s" % ("OK:" if ok else "FAIL:", t, s))
print("graded tables with a clean newest run: %d of 3" % (3 - bad))
sys.exit(0 if bad == 0 else 1)
' 2>&1); rc=$?
printf '%s\n' "$out"
if [ "$rc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
