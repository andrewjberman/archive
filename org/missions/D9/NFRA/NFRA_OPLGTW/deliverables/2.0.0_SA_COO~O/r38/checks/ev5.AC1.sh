#!/usr/bin/env bash
# OPLGTW OG-ev-5 AC1 (round 41, the near-empty fees stretch, read only): FEES_TRACE.json is complete and its verdict follows the stated rule.
# W/FEES_TRACE.json = {"body": {"read_at", "window": {"from", "to"}, "stretch": {"from", "to", "days"},
#   "source": {"rows_in_stretch", "median_rows_per_day_outside", "partitions_in_stretch", "partitions_expected_in_stretch"},
#   "account": {"rows_in_stretch", "median_rows_per_day_outside"}, "verdict": "source|account|neither|not_determined"}}. Counts, dates and fixed words only.
#  - every number is a non-negative int (medians may be floats); stretch.days is the day count between from and to (inclusive) and is 30 or more;
#  - near-empty means rows_in_stretch is below 25 percent of (median_rows_per_day_outside x days); the verdict is "source" if the source is near-empty,
#    else "account" if the account is near-empty, else "neither"; "not_determined" is allowed only when a median outside is 0 (nothing to compare);
#  - the source's partitions in the stretch equal the partitions expected (a missing partition is a finding of the source, stated by the verdict);
#  - no e-mail, no digit run of 9 or more (outside the iso dates).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV5_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/FEES_TRACE.json}"
[ -f "$REC" ] || { echo "FEES_TRACE.json is absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$REC")" <<'PYEOF'
import datetime, json, re, sys
raw = open(sys.argv[1], encoding="utf-8").read()
d = json.loads(raw); b = d.get("body", d)
st, src, acc = b.get("stretch") or {}, b.get("source") or {}, b.get("account") or {}
def isint(x): return isinstance(x, int) and not isinstance(x, bool) and x >= 0
def isnum(x): return isinstance(x, (int, float)) and not isinstance(x, bool) and x >= 0
ok = True
try:
    f, t = datetime.date.fromisoformat(st["from"]), datetime.date.fromisoformat(st["to"])
    days = (t - f).days + 1
except Exception:
    days = None
nums = (isint(st.get("days")) and days == st.get("days") and st["days"] >= 30 and isint(src.get("rows_in_stretch")) and isnum(src.get("median_rows_per_day_outside"))
        and isint(src.get("partitions_in_stretch")) and isint(src.get("partitions_expected_in_stretch")) and isint(acc.get("rows_in_stretch")) and isnum(acc.get("median_rows_per_day_outside")))
ok = ok and nums
def near(r):
    base = r.get("median_rows_per_day_outside") or 0
    return base > 0 and r.get("rows_in_stretch", 0) < 0.25 * base * (days or 0)
mid = (src.get("median_rows_per_day_outside") or 0) == 0 or (acc.get("median_rows_per_day_outside") or 0) == 0
if nums:
    want = "source" if near(src) else ("account" if near(acc) else "neither")
    if mid:
        want = "not_determined" if b.get("verdict") == "not_determined" else want
else:
    want = None
verdict_ok = nums and b.get("verdict") == want
parts_ok = nums and src.get("partitions_in_stretch") == src.get("partitions_expected_in_stretch")
ok = ok and verdict_ok and parts_ok
scrub = re.sub(r"\d{4}-\d{2}-\d{2}(T[\d:]+Z?)?", "", raw)
runs = re.findall(r"(?<![\d.-])\d{9,}(?![\d.-])", scrub); mails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", raw)
ok = ok and not runs and not mails
print("stretch: %s days (want 30 or more); source rows %s, account rows %s; partitions in the stretch %s of %s expected" % (
      st.get("days"), src.get("rows_in_stretch"), acc.get("rows_in_stretch"), src.get("partitions_in_stretch"), src.get("partitions_expected_in_stretch")))
print("verdict %s (rule says %s)" % (b.get("verdict"), want))
print("content hygiene: long digit runs %d (want 0); e-mail addresses %d (want 0)" % (len(runs), len(mails)))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
