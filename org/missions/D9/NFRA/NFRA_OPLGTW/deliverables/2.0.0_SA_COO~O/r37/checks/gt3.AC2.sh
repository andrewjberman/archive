#!/usr/bin/env bash
# OPLGTW gt3 AC2 (round-37 G1-TYPED, FWD-22): query_columns top-20 and consensus against the REAL bucket.
# The probe runs the tool function itself against the REAL bucket with the box's credentials and an Opal stand-in
# principal, then re-derives the answer independently (gt_probe_lib: boto3 + pyarrow, no tool under test).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
CK="$(dirname "$0")"; CK="$(cd "$CK" && pwd)"
res=$(CKDIR="$(native "$CK")" timeout 110 python - <<'EOF'
import os, sys
sys.path.insert(0, os.environ["CKDIR"])
import gt_probe_lib as P
ok = False
try:
    c = P.setup()

    from app import harvest_figures as h
    newest = P.newest_part(c, "amgt/harvest/gold/chatter_daily/")
    tbl = P.read_table(c, newest, ["security_key", "day", "articles_total"]).to_pylist()
    day = max(str(r["day"]) for r in tbl)
    top = sorted((r["articles_total"] or 0) for r in tbl if str(r["day"]) == day)[-20:]
    q = h.harvest_query_columns("chatter_daily", ["security_key", "articles_total"], filters=[{"column": "day", "op": "=", "value": day}], order_by="articles_total desc", limit=20)
    rows = q.get("rows") or []
    got = sorted((r.get("articles_total") or 0) for r in rows)
    bad = h.harvest_query_columns("chatter_daily", ["security_key", "no_such_column"])
    big = h.harvest_query_columns("chatter_daily", ["security_key"], limit=500)
    key = P.asml_key(c)
    f = h.harvest_get_fundamentals(key, "consensus")
    print("query top-20 on %s: tool %s vs independent %s; unknown column refused %s; limit 500 clamped to %s; consensus rows for ASML %d; source key is the newest part %s"
          % (day, got == top, "equal" if got == top else "differ", bad.get("code") == "harvest_bad_argument", big.get("limit_applied"), len(f.get("rows") or f.get("figures") or []), q.get("source_keys") == [newest]))
    ok = got == top and len(rows) == 20 and bad.get("code") == "harvest_bad_argument" and big.get("limit_applied") == 200 and len(f.get("rows") or f.get("figures") or []) > 0 and q.get("source_keys") == [newest] and P.envelope_ok(q) and P.envelope_ok(f)

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
