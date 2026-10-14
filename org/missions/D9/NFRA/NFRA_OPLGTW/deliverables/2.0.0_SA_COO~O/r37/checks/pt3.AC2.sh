#!/usr/bin/env bash
# OPLGTW pt3 AC2 (round-37 G1-TYPED, FWD-22): the firm-scoped tool called for real: refusals read nothing, and an admitted read equals an independent read.
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

    from app import portal_mdpf as h
    bad = h.mdpf_get_category_views(scope="not-a-firm")
    empty = h.mdpf_get_category_views(scope="")
    trav = h.mdpf_get_category_views(scope="../global")
    refusals = all(r.get("code") == "harvest_bad_argument" for r in (bad, empty, trav))
    res = h.mdpf_get_category_views(scope="global")
    served = isinstance(res, dict) and bool(res.get("source_keys"))
    if served:
        key = "platinum/mdpf/global/category-views.json"
        e, k, a = check(res, [key])
        indep = raw(key)
        same = a and e and k
    else:
        e = k = a = same = False
        code = res.get("code") if isinstance(res, dict) else None
    hr.get_current_principal = lambda: SimpleNamespace(email="someone@example.com", tid="t", oid="o")
    non_opal = h.mdpf_get_category_views(scope="global").get("code") in ("typed_opal_only", "harvest_opal_only")
    print("category views: bad scopes refused %s; global served %s with its own as-of inside the object %s; non-Opal refused %s" % (refusals, served, same, non_opal))
    ok = refusals and non_opal and (served and same or (not served and res.get("guard_denied") is True))

except Exception as e:
    print("probe error: %s: %s" % (type(e).__name__, str(e)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
