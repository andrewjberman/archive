#!/usr/bin/env bash
# OPLGTW pt2 AC2 (round-37 G1-TYPED, FWD-22): the four tools called for real against opal-data-portal-v2.
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

    from app import portal_macro as h
    sk = first_under("json/macro/timeseries/")
    slug = sk.rsplit("/", 1)[1][:-5] if sk else ""
    uk = None
    for page in c.get_paginator("list_objects_v2").paginate(Bucket=BK, Prefix="json/security_scanner/latest/universes/", Delimiter="/"):
        for p in page.get("CommonPrefixes", []):
            uk = p["Prefix"].split("/")[-2]
            break
        if uk:
            break
    cases = [
        ("macro", h.portal_get_macro(), ["json/macro/macro_data.json"]),
        ("series", h.portal_get_macro(slug=slug), ["json/macro/timeseries/%s.json" % slug]),
        ("valuation", h.portal_get_valuation(), ["json/valuation/valuation_data.json", "json/valuation/risk_premium_data.json"]),
        ("scan", h.portal_get_security_scan(universe=uk), ["json/security_scanner/latest/universes/%s/scanner_data.json" % uk]),
        ("freshness", h.portal_get_pipeline_freshness(), ["json/latest/manifest.json"]),
    ]
    good = 0; parts = []
    for name, res, want in cases:
        e, k, a = check(res, want)
        parts.append("%s %s" % (name, "ok" if (e and k and a) else "BAD(env=%s keys=%s asof=%s)" % (e, k, a)))
        good += 1 if (e and k and a) else 0
    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    refused = h.portal_get_macro().get("code") in ("typed_opal_only", "harvest_opal_only")
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
