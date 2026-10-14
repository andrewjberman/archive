#!/usr/bin/env bash
# OPLGTW gt1 AC2 (round-37 G1-TYPED, FWD-22): resolve, the CUSIP not_held correction and coverage against the REAL bucket.
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

    from app import harvest_identity as h
    key = P.asml_key(c)
    r = h.harvest_resolve_security("ASML")
    cu = h.harvest_resolve_security("037833100")
    cov = h.harvest_security_coverage(r.get("security_key") or key or "")
    env = all(P.envelope_ok(x) for x in (r, cu, cov))
    rows = cov.get("datasets") or []
    rowok = len(rows) > 0 and all(("present" in d and "trading_days_behind_t1" in d) for d in rows)
    packs_present = any(d.get("dataset", "").startswith("packs") and d.get("present") for d in rows)
    try:
        c.head_object(Bucket=P.BUCKET, Key="packs/%s/input_ledger.json" % (r.get("security_key") or key)); indep = True
    except Exception:
        indep = False
    print("resolve ASML: status %s, security_key %s; CUSIP query: status %s; coverage datasets %d, rows well-formed %s; packs present %s vs independent head %s; envelope on all three %s"
          % (r.get("status"), "set" if r.get("security_key") else "EMPTY", cu.get("status"), len(rows), rowok, packs_present, indep, env))
    ok = r.get("status") == "exact" and bool(r.get("security_key")) and cu.get("status") == "not_held" and rowok and env and packs_present == indep

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
