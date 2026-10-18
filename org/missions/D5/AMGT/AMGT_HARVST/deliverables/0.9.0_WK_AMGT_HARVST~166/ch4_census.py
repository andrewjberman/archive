"""ch4_census.py -- AMGT_HARVST HVST-ch-4 read-only census (round 93).

Run from the root of the worktree, in the foreground:
    python -u org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~166/ch4_census.py > ch4_census.out

READS ONLY. It calls fund_form.gather_items (silver rows + extraction objects),
fund_form._stored_documents (the stored research-fund-form/ objects), and builds
every fund's document in memory with fund_form.build_document and
fund_form._inputs_sha16. It never calls write, _run_write, gold_put, a put_object
or any silver writer. Every S3 request goes through a counting wrapper that
aborts above the budget (800 requests, 300 MiB).
"""

from __future__ import annotations

import io
import os
import sys

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import fund_form  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402

MAX_REQUESTS = 800
MAX_BYTES = 300 * 1024 * 1024


class BudgetExceeded(RuntimeError):
    pass


class CountingClient:
    """Wraps a boto3 S3 client: counts every request issued and every object byte read."""

    def __init__(self, inner):
        self._inner = inner
        self.by_op = {}
        self.bytes = 0

    def _count(self, op):
        self.by_op[op] = self.by_op.get(op, 0) + 1
        if self.requests() > MAX_REQUESTS:
            raise BudgetExceeded("request budget exceeded: %d > %d" % (self.requests(), MAX_REQUESTS))

    def requests(self):
        return sum(self.by_op.values())

    def get_object(self, **kwargs):
        self._count("get_object")
        resp = self._inner.get_object(**kwargs)
        data = resp["Body"].read()
        self.bytes += len(data)
        if self.bytes > MAX_BYTES:
            raise BudgetExceeded("byte budget exceeded: %d > %d" % (self.bytes, MAX_BYTES))
        resp["Body"] = io.BytesIO(data)
        return resp

    def get_paginator(self, operation_name):
        inner_pager = self._inner.get_paginator(operation_name)
        counter = self

        class _Pager:
            def paginate(self, **kwargs):
                for page in inner_pager.paginate(**kwargs):
                    counter._count("list_page:%s" % operation_name)
                    yield page

        return _Pager()

    def head_object(self, **kwargs):
        self._count("head_object")
        return self._inner.head_object(**kwargs)


def main():
    assert fund_form.__file__.startswith(ROOT), "fund_form imported from outside the worktree: %s" % fund_form.__file__
    print("SOURCE %s" % fund_form.__file__)
    print("FUNDS %s" % ",".join(fund_form.FUNDS))

    client = CountingClient(store._default_client())

    items, extract_bytes = fund_form.gather_items(client=client)
    four = [(rid, fund, cls, headings) for rid, fund, cls, headings, _ek in items]
    stated = fund_form.distinct_funds(four)
    absent = fund_form.absent_fund_reports(four)
    forms = sorted(set(stated) | set(fund_form.FUNDS))
    print("POPULATION reports=%d stated_funds=%s absent_fund_reports=%d forms=%d"
          % (len(items), ",".join(stated), absent, len(forms)))

    stored = fund_form._stored_documents(client=client)
    prefix = gold.table_prefix(fund_form.TABLE)
    print("STORED-DENOMINATOR objects=%d" % len(stored))

    status = {}
    fund_reports = {}
    for fund in forms:
        inputs = fund_form._inputs_for_fund(fund, items, extract_bytes)
        document = fund_form.build_document(fund, four, inputs)
        name = "%s.json" % fund_form._inputs_sha16(inputs)
        stored_key = prefix + "fund=%s/%s" % (fund_form._slug(fund), name)
        if stored_key not in stored:
            state = "absent"
        elif stored[stored_key].get("content_sha256") == document["content_sha256"]:
            state = "equal"
        else:
            state = "different"
        status[fund] = state
        fund_reports[fund] = document["fields"]["reports"]
        print("FORM %s reports=%d object=%s content_sha256=%s stored=%s"
              % (fund, document["fields"]["reports"], name, document["content_sha256"][:8], state))

    print("REQUESTS by_op=%s total=%d of %d bytes=%d of %d"
          % (sorted(client.by_op.items()), client.requests(), MAX_REQUESTS, client.bytes, MAX_BYTES))
    print("CENSUS-FORMS forms=%d idvz=%s pfoe=%s divz=%s divz_reports=%d gets=%d bytes=%d"
          % (len(forms), status.get("IDVZ", "absent"), status.get("PFOE", "absent"),
             status.get("DIVZ", "absent"), fund_reports.get("DIVZ", -1),
             client.requests(), client.bytes))


if __name__ == "__main__":
    main()
