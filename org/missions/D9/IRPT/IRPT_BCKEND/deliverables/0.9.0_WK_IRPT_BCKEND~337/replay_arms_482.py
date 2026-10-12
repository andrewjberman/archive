"""IB-pr-482 step 4: the four synthetic arms of performance/tests/test_chain_claim.py run on the holdings_gold.py of an EXTRACTED zip.
    python -I replay_arms_482.py <extracted_zip_dir> <label>       (prints one JSON line per arm, then a JSON summary line)
Synthetic gold frames only (the test's own plan, FakeS3, no AWS). The module under test and everything it imports come from <dir> first.
ASCII only."""
import io
import json
import sys

d, label = sys.argv[1], sys.argv[2]
# the zip packages lib/trading_calendar.py and the 49F runner under their repo-relative member names; the test puts those two roots on sys.path
for sub in ("data/assets/scripts/gold/runners_49f", "lib", ""):
    sys.path.insert(0, d + "/" + sub if sub else d)
import pandas as pd  # noqa: E402
import holdings_gold as hg  # noqa: E402
import tenants  # noqa: E402
from ids import opaque_account  # noqa: E402

assert hg.__file__.replace("\\", "/").startswith(d.replace("\\", "/")), hg.__file__
RAW = "0012345678"
ACCOUNT = opaque_account(tenants._CANONICAL_49F, RAW)
BUCKET, PREFIX = "holdings-bucket", "irpt/49financial/gold/holdings_performance_daily/"
RETURN = 0.002
DAYS = ["2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05", "2026-03-06", "2026-03-09", "2026-03-10"]
NO_PRIOR, NON_POSITIVE, ALL_EXCLUDED = "NO-PRIOR-HOLDINGS", "NON-POSITIVE-BASE", "ALL-HOLDINGS-EXCLUDED"


def gold(plan):
    store = {}
    for day in DAYS:
        status, held = plan.get(day, ("OK", 3))
        row = {"account_id": RAW, "business_date": day, "daily_return": RETURN if status == "OK" else None, "account_value": 100.0,
               "excluded_count": 0, "excluded_weight": 0.0, "status": status,
               "held_count": held, "included_count": 0 if status != "OK" else 3, "negative_count": 0, "cash_value": 0.0}
        buf = io.BytesIO()
        pd.DataFrame([row]).to_parquet(buf, index=False)
        store["%sdate=%s/data.parquet" % (PREFIX, day)] = buf.getvalue()
    return store


class FakeS3:
    def __init__(self, objects):
        self.objects = objects

    def get_paginator(self, name):
        store = self

        class Paginator:
            def paginate(self, Bucket, Prefix, Delimiter=None, **kw):
                prefixes = sorted({k[:k.index("/data.parquet") + 1] for k in store.objects if k.startswith(Prefix)})
                yield {"CommonPrefixes": [{"Prefix": p} for p in prefixes]}
        return Paginator()

    def get_object(self, Bucket, Key, **kw):
        return {"Body": io.BytesIO(self.objects[Key]), "VersionId": "v", "ETag": '"e"'}


def find(o):
    if isinstance(o, dict):
        if "days_excluded" in o:
            return o
        for v in o.values():
            r = find(v)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find(v)
            if r:
                return r
    return None


ARMS = [("no-base days only (NO-PRIOR-HOLDINGS and NON-POSITIVE-BASE with held_count 0)", {DAYS[0]: (NO_PRIOR, 0), DAYS[3]: (NON_POSITIVE, 0)}),
        ("ALL-HOLDINGS-EXCLUDED", {DAYS[3]: (ALL_EXCLUDED, 2)}),
        ("NON-POSITIVE-BASE with a prior-day position row (held_count 2)", {DAYS[3]: (NON_POSITIVE, 2)}),
        ("an unnamed status (A-STATUS-THE-PRODUCER-NEVER-WROTE)", {DAYS[3]: ("A-STATUS-THE-PRODUCER-NEVER-WROTE", 0)})]
out = []
for name, plan in ARMS:
    scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["49F"], "permitted_account_set": [ACCOUNT], "resolved_scope": {"scope_ids": [ACCOUNT]}}
    src = hg.HoldingsGoldSource(FakeS3(gold(plan)), bucket=BUCKET, prefix=PREFIX, max_workers=2)
    ans = hg.calculate(scope, hg.SINCE_INCEPTION_START, DAYS[-1], src)
    vf = find(ans["report"]) or {}
    rec = {"label": label, "arm": name, "claim": ans["claim"], "value_facts_claim": vf.get("claim"),
           "days_without_base": vf.get("days_without_base"), "days_with_return_left_out": vf.get("days_with_return_left_out"),
           "days_excluded": vf.get("days_excluded"), "days_linked": vf.get("days_linked"),
           "figure": repr(float(ans["report"]["returns"]["account_detail"][0]["value"]))}
    out.append(rec)
    print(json.dumps(rec, sort_keys=True))
