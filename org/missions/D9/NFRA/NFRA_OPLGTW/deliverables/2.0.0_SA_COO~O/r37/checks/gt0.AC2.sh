#!/usr/bin/env bash
# OPLGTW gt0 AC2 (round-37 G1-TYPED, FWD-22): the newest-part rule against the REAL chatter_daily prefix.
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

    got = None
    from app import harvest_typed as t
    got = t.newest_part("amgt/harvest/gold/chatter_daily/")
    want = P.newest_part(c, "amgt/harvest/gold/chatter_daily/")
    nparts = sum(1 for pg in c.get_paginator("list_objects_v2").paginate(Bucket=P.BUCKET, Prefix="amgt/harvest/gold/chatter_daily/")
                 for o in pg.get("Contents", []) if o["Key"].endswith(".parquet"))
    print("newest chatter_daily part: tool %s; independent %s; equal=%s; parts listed %d" % (got, want, got == want, nparts))
    ok = bool(got) and got == want and nparts > 1

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
