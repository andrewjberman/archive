#!/usr/bin/env bash
# OPLGTW OG-ev-8 AC1 (round 43): the read-only table of the gateway's inline audit-write call sites (round-42 slug item 5; worker row Z-W147-S1: `audit._emit` appends a file and, when AUDIT_S3_BUCKET is set, calls boto3 put_object with default timeouts).
# The denominator is measured HERE: one pattern over every python file under the gateway app/ (the audit module's own internal calls included); every matching line must appear in the record. The pattern matches 81 lines at the cut.
# Record W/AUDIT_SITES.json = {"body": {"sites": [{"file", "line", "call" (<=120 chars), "on_event_loop": "yes|no|unknown", "loop_reason", "timeout_s": number|null, "timeout_reason",
#   "calls_7d": integer|"ABSENT", "calls_7d_source" (when integer) | "absent_reason" (when "ABSENT")}], "frequency_source": "<where calls_7d came from>"|null, "frequency_absent_reason": "<why no site has a count>"|null}}
# A column the worker could not read is ABSENT with its reason, never 0 (a value must carry its claim). If EVERY site has calls_7d ABSENT the record's frequency_absent_reason must say why.
# Override (dry-run controls only): EV8_REC_OVERRIDE.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="${EV8_REC_OVERRIDE:-org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~154/AUDIT_SITES.json}"
[ -f "$REC" ] || { echo "AUDIT_SITES.json absent"; echo "RESULT: FAIL"; exit 1; }
found=$(git grep -nE -e '\baudit\.[A-Za-z_]+\(' -e '\b_emit\(' -- "$GW/app/*.py" | cut -d: -f1,2 | sed "s|^$GW/app/||" | sort -u)
res=$(FOUND="$found" python -I - "$(native "$REC")" <<'PYEOF'
import json, os, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); b = d.get("body", d)
want = sorted(set(x.strip() for x in os.environ.get("FOUND", "").split("\n") if x.strip()))
sites = b.get("sites") or []
have = set(); bad = 0; absent = 0; counted = 0; loop_unknown = 0
for s in sites:
    if not isinstance(s, dict) or not isinstance(s.get("line"), int) or not s.get("file"):
        bad += 1; continue
    ok = s.get("on_event_loop") in ("yes", "no", "unknown") and s.get("loop_reason")
    t = s.get("timeout_s")
    ok = ok and (t is None or (isinstance(t, (int, float)) and not isinstance(t, bool))) and s.get("timeout_reason")
    c = s.get("calls_7d")
    if c == "ABSENT":
        ok = ok and bool(s.get("absent_reason")); absent += 1
    else:
        ok = ok and isinstance(c, int) and not isinstance(c, bool) and c >= 0 and bool(s.get("calls_7d_source")); counted += 1
    if s.get("on_event_loop") == "unknown":
        loop_unknown += 1
    if not ok:
        bad += 1; continue
    f = str(s.get("file", "")).replace(chr(92), "/").split("opal-gateway/app/")[-1]
    have.add("%s:%d" % (f, s["line"]))
missing = [w for w in want if w not in have]
freq_ok = counted > 0 or bool(b.get("frequency_absent_reason"))
ok = len(want) >= 80 and not missing and not bad and freq_ok
print("inline audit-write call sites matched by the pattern under app/: %d (the cut counted 81); listed in the record: %d; matched lines missing from the record: %d (want 0); malformed rows: %d (want 0)" % (len(want), len(have), len(missing), bad))
print("event loop column unknown on %d site(s); frequency counted on %d site(s), ABSENT with a reason on %d; every site ABSENT carries the record-level reason: %s" % (loop_unknown, counted, absent, "yes" if freq_ok else "NO"))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
printf '%s\n' "$res" | sed '$d'
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
