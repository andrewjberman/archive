#!/usr/bin/env bash
# F2-AC2 -- EVERY ASK ANSWERED AND RECORDED WHOLE.
#
# For each instant actually attempted: the answer file PARSES as JSON, carries a
# rows array whose length is printed (D-8 measured 58), and the ask's stderr
# carries a VINTAGE line. The sha256 printed per instant is over the rows array
# as CANONICAL JSON (sorted keys, no whitespace) -- D-8's own `canon`, so key
# order and pretty-printing cannot make two identical answers look different
# nor two different answers look the same. That sha256 is the value site Z's
# record must match at L9; this seat does not and cannot compare them.
#
# A zero-row answer is REFUSED loudly rather than scored as agreement, which is
# the trap D-8's script names in its own header.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
D=org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~1
PY=${PYTHON:-python}

echo "=== f2_answers_recorded.sh -- $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
echo "HEAD=$(git rev-parse HEAD)  BRANCH=$(git rev-parse --abbrev-ref HEAD)"
echo

"$PY" - "$D" <<'PY'
import hashlib
import io
import json
import os
import re
import sys

D = sys.argv[1]
LABELS = ["T0", "T1", "T2"]


def read(p):
    return io.open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


attempted, recorded = 0, 0
counts, sha_lines, vintages = [], [], []
vintage_all = True

for lb in LABELS:
    cap = read(os.path.join(D, "f2_ask_%s.txt" % lb))
    # ATTEMPTED means the capture says the ask was FIRED. A capture that exists
    # but carries no terminal status (an instant still in its polled wait, or a
    # run that died mid-flight) is NO-CAPTURE, not a failed answer: scoring it
    # as attempted would put a zero in a numerator for an ask that never ran.
    if cap is None:
        state = "NO-CAPTURE"
    elif re.search(r"^LAPTOP_STATUS_%s=MISSED" % lb, cap, re.M):
        state = "MISSED"
    elif re.search(r"^LAPTOP_STATUS_%s=ASKED" % lb, cap, re.M):
        state = "ASKED"
    else:
        state = "NO-CAPTURE"
    if state != "ASKED":
        print("--- %s: %s -- excluded from numerator AND denominator" % (lb, state))
        continue
    attempted += 1
    ans_p = os.path.join(D, "f2_answer_%s.json" % lb)
    err_p = os.path.join(D, "f2_answer_%s.err" % lb)
    print("--- %s ---" % lb)
    print("  answer_file=%s bytes=%s" % (ans_p, os.path.getsize(ans_p) if os.path.exists(ans_p) else "ABSENT"))
    ok = True
    try:
        doc = json.load(io.open(ans_p, encoding="utf-8"))
    except Exception as ex:
        print("  PARSE=FAILED (%s)" % ex)
        ok = False
        doc = None
    if doc is not None:
        rows = doc.get("rows") if isinstance(doc, dict) else doc
        rows = rows or []
        canon = json.dumps(rows, sort_keys=True, separators=(",", ":"))
        sha = hashlib.sha256(canon.encode("utf-8")).hexdigest()
        print("  PARSE=OK rows=%d canon_bytes=%d" % (len(rows), len(canon)))
        print("  ROWS_SHA256_%s=%s" % (lb, sha))
        if not rows:
            print("  REFUSED: ZERO rows -- an empty answer is not an answer; it would compare EQUAL to any other empty answer")
            ok = False
        counts.append(str(len(rows)))
        sha_lines.append("%s=%s" % (lb, sha))
    err = read(err_p) or ""
    m = re.search(r"vintage=([^\s\]]+)", err)
    v = m.group(1) if m else "UNREAD"
    print("  VINTAGE_%s=%s" % (lb, v))
    print("  VINTAGE_LINE_VERBATIM: %s" % (err.strip().splitlines()[0] if err.strip() else "(stderr empty)"))
    if v == "UNREAD":
        vintage_all = False
        ok = False
    if ok:
        recorded += 1

print()
print("--- THE SHA256 SITE Z's RECORD MUST MATCH (this seat cannot read site Z; L9 compares) ---")
for s in sha_lines:
    print("  %s" % s)
print()
print("--- F2-AC2 VERDICT LINES ---")
print("ANSWERS_RECORDED=%d of %d" % (recorded, attempted))
print("ROWS_COUNT_EACH=%s" % ",".join(counts))
print("VINTAGE_EACH_PRESENT=%s" % str(bool(vintage_all and attempted)).lower())
PY
echo "=== f2_answers_recorded.sh END ==="
