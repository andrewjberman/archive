"""HVST-cf-3 census (read-only), AMGT_HARVST round 92. Run from the worktree root, unbuffered,
stdout to the .out:

    python -u org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~164/cf3_census.py > .../cf3_census.out

Two fund-form rules are applied to ONE fetch of the inputs:
  BASELINE -- lib/research/corpus/fund_form.py as committed at a9aecdd593 (pinned by commit, never HEAD),
              loaded as a second module under another name; its own gather_items (fund = row fund).
  NEW      -- the worktree's lib/research/corpus/fund_form.py (holding-only, misfiled reports skipped).
Both gather_items calls read the silver through the SAME rows: store.silver_latest is held to the one
fetched row set for the duration of the two calls, and the counting client memoises every object body, so
each extraction is GET once. Nothing is written: no put, delete, copy or sync; only list-objects-v2 pages
and get-object of the silver parts and of the extraction objects named by each silver row.

Budget enforced: 800 requests (list pages + gets), 300 MiB. `gets=` in the last line is the total request
count; the REQUESTS line before it breaks it down.
"""
import io
import os
import subprocess
import sys
import types

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import fund_form as new  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BASE = "a9aecdd593"
BASE_PATH = "lib/research/corpus/fund_form.py"
BUDGET_REQUESTS = 800
BUDGET_BYTES = 300 * 1024 * 1024
FUND_CLASSES = ("A", "B", "C", "D")


class BudgetExceeded(RuntimeError):
    pass


class CountingClient:
    """Delegates get_paginator/get_object to the real client; counts every list page and every GET,
    memoises each object body so a second read of the same key is free."""

    def __init__(self, real):
        self.real = real
        self.list_pages = 0
        self.get_requests = 0
        self.bytes = 0
        self.cache = {}

    def _spend(self):
        if self.list_pages + self.get_requests + 1 > BUDGET_REQUESTS:
            raise BudgetExceeded("request budget %d exceeded" % BUDGET_REQUESTS)

    def get_paginator(self, operation_name):
        outer = self
        real_paginator = self.real.get_paginator(operation_name)

        class _Paginator:
            def paginate(self, **kwargs):
                for page in real_paginator.paginate(**kwargs):
                    outer._spend()
                    outer.list_pages += 1
                    yield page

        return _Paginator()

    def get_object(self, Bucket, Key):
        if Key not in self.cache:
            self._spend()
            resp = self.real.get_object(Bucket=Bucket, Key=Key)
            body = resp["Body"]
            raw = body.read() if hasattr(body, "read") else body
            self.get_requests += 1
            self.bytes += len(raw)
            if self.bytes > BUDGET_BYTES:
                raise BudgetExceeded("byte budget %d exceeded" % BUDGET_BYTES)
            self.cache[Key] = raw
        return {"Body": io.BytesIO(self.cache[Key])}


def load_baseline():
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    src = subprocess.run(
        ["git", "show", "%s:%s" % (BASE, BASE_PATH)],
        cwd=ROOT, env=env, capture_output=True, check=True,
    ).stdout.decode("utf-8")
    # positive control: the pinned bytes are the pre-amendment module
    assert "def gather_items(client=None):" in src and 'METHOD_VERSION = "1"' in src, "baseline control failed"
    mod = types.ModuleType("fund_form_baseline_%s" % BASE)
    mod.__file__ = "git:%s:%s" % (BASE, BASE_PATH)
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def main():
    base = load_baseline()
    print("# MODULE new=%s METHOD_VERSION=%s" % (new.__file__, new.METHOD_VERSION))
    print("# MODULE baseline=%s METHOD_VERSION=%s" % (base.__file__, base.METHOD_VERSION))

    client = CountingClient(store._default_client())
    raw_latest = store.silver_latest(typed.SOURCE, typed.TABLE, typed.RECORD_KEY_FIELDS, client=client)
    raw_rows = sorted(raw_latest.values(), key=lambda r: (r.get("security_key"), r.get("report_id")))
    by_ek = {}
    for row in raw_rows:
        ek = row["extract_key"]
        if ek in by_ek:
            raise SystemExit("DUPLICATE extract_key %s -- census cannot key reports" % ek)
        by_ek[ek] = row
    print("# DENOMINATOR silver_rows=%d list_pages=%d silver_gets=%d"
          % (len(raw_rows), client.list_pages, client.get_requests))

    real_silver_latest = store.silver_latest
    store.silver_latest = lambda source, table, record_key_fields, client=None: raw_latest
    try:
        base_items, _ = base.gather_items(client=client)
        new_items, _ = new.gather_items(client=client)
    finally:
        store.silver_latest = real_silver_latest
    print("# DENOMINATOR baseline_items=%d new_items=%d (baseline keeps every row; new skips misfiled)"
          % (len(base_items), len(new_items)))

    misfiled = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
    base4 = [(rid, fund, cls, h) for rid, fund, cls, h, _ek in base_items]
    new4 = [(rid, fund, cls, h) for rid, fund, cls, h, _ek in new_items]

    meta = {}
    before = {}
    for rid, fund, cls, _h, ek in base_items:
        key = (by_ek[ek]["security_key"], by_ek[ek]["report_id"])
        meta[key] = (cls, fund, by_ek[ek].get("fund_relation", "absent"))
        if fund and cls in FUND_CLASSES:
            before[key] = fund
    after = {}
    for rid, fund, cls, _h, ek in new_items:
        key = (by_ek[ek]["security_key"], by_ek[ek]["report_id"])
        if fund and cls in FUND_CLASSES:
            after[key] = fund

    gained = sorted(k for k in after if k not in before or before[k] != after[k])
    print("# CHECK gained_or_moved=%d (must be 0)" % len(gained))
    for k in gained:
        print("GAINED %s %s fund=%s" % (k[0], k[1], after[k]))

    dropped = sorted(k for k in before if k not in after)
    dropped_misfiled = 0
    dropped_nonholding = 0
    for k in dropped:
        cls, fund, relation = meta[k]
        if k in misfiled:
            dropped_misfiled += 1
            print("# MISFILED-DROPPED %s %s %s fund=%s relation=%s" % (k[0], k[1], cls, fund, relation))
        else:
            dropped_nonholding += 1
        print("DROPPED %s %s %s fund=%s relation=%s" % (k[0], k[1], cls, fund, relation))

    seen = sorted({f for f in [r[1] for r in base4] + [r[1] for r in new4] if f})
    reports_before = 0
    reports_after = 0
    funds_with_form = []
    for fund in seen:
        rb = base.build(fund, base4)["reports"]
        ra = new.build(fund, new4)["reports"]
        reports_before += rb
        reports_after += ra
        if ra > 0:
            funds_with_form.append(fund)
        print("FUND %s reports_before=%d reports_after=%d" % (fund, rb, ra))
    print("# CHECK sum_before=%d len(before)=%d sum_after=%d len(after)=%d"
          % (reports_before, len(before), reports_after, len(after)))
    print("# DISTINCT_FUNDS baseline=%s new=%s"
          % (",".join(base.distinct_funds(base4)), ",".join(new.distinct_funds(new4))))

    absent_before = base.absent_fund_reports(base4)
    absent_after = new.absent_fund_reports(new4)
    print("REQUESTS list_pages=%d get=%d total=%d bytes=%d"
          % (client.list_pages, client.get_requests, client.list_pages + client.get_requests, client.bytes))
    print("CENSUS-FUND-FORM funds=%d reports_before=%d reports_after=%d dropped_nonholding=%d "
          "dropped_misfiled=%d absent_before=%d absent_after=%d gets=%d bytes=%d"
          % (len(funds_with_form), reports_before, reports_after, dropped_nonholding, dropped_misfiled,
             absent_before, absent_after, client.list_pages + client.get_requests, client.bytes))


if __name__ == "__main__":
    main()
