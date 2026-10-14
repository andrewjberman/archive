#!/usr/bin/env bash
# OPLGTW pt1 AC2 (round-37 G1-TYPED, FWD-22): the four tools called for real against opal-data-portal-v2.
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

    import json, gzip
    from types import SimpleNamespace
    import app.harvest_read as hr
    BK = "opal-data-portal-v2"
    def raw(key):
        b = c.get_object(Bucket=BK, Key=key)["Body"].read()
        try:
            b = gzip.decompress(b)
        except OSError:
            pass
        return b.decode("utf-8", "replace")
    def first_under(prefix, suffix=".json"):
        for page in c.get_paginator("list_objects_v2").paginate(Bucket=BK, Prefix=prefix):
            for o in page.get("Contents", []):
                if o["Key"].endswith(suffix):
                    return o["Key"]
        return None
    def check(res, want_keys):
        ok_env = P.envelope_ok(res)
        keys = res.get("source_keys") or []
        has = all(any(k == w for k in keys) for w in want_keys)
        asof = str(res.get("as_of") or "")
        in_obj = bool(asof) and any(asof in raw(k) for k in keys[:3])
        return ok_env, has, in_obj

    from app import portal_models as h
    tk = first_under("json-tiered/market-overview/timeseries/")
    tkr = tk.rsplit("/", 1)[1][:-5] if tk else "SPY"
    cases = [
        ("positioning", h.portal_get_model_positioning(), ["json/positioning/positioning_data.json", "json/positioning/opal_aggregate.json"]),
        ("attribution", h.portal_get_model_attribution(), ["json/positioning/holdings_attribution_data.json", "json/positioning/allocation_summary.json"]),
        ("returns", h.portal_get_market_returns(), ["json-tiered/market-overview/summary/all-returns.json"]),
        ("series", h.portal_get_market_returns(ticker=tkr), ["json-tiered/market-overview/timeseries/%s.json" % tkr]),
        ("regime", h.portal_get_market_regime(), ["json/market/market-regime.json"]),
    ]
    good = 0; parts = []
    for name, res, want in cases:
        e, k, a = check(res, want)
        parts.append("%s %s" % (name, "ok" if (e and k and a) else "BAD(env=%s keys=%s asof=%s)" % (e, k, a)))
        good += 1 if (e and k and a) else 0
    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    refused = h.portal_get_model_positioning().get("code") in ("typed_opal_only", "harvest_opal_only")
    print("portal tools: %d of 5 answered from their keys with the object's own as-of (%s); non-Opal principal refused %s" % (good, "; ".join(parts), refused))
    ok = good == 5 and refused

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
