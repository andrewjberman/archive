"""cj6_replay.py -- AMGT_HARVST HVST-cj-6 step 1d. READ-ONLY replay of the CHANGED gateway harvest tools against the REAL
stored objects. The gateway is NOT called: the tools run in this process, and their harvest_read._client() is replaced by
a read-only wrapper around store._default_client() that forwards list_objects_v2 and get_object on opal-data-harvest and
refuses every other operation. The audit sink is a recorder (no file is written). The principal is a synthetic
Opal-domain stand-in, as in the offline tests.

Changed tools (7 cells per key): harvest_get_fundamentals by kind (consensus, reference, valuation_history, segments,
price) and harvest_query_columns on bestdata, and harvest_security_coverage. Each is called with BP/_LN_Equity and
NG/_LN_Equity in both spellings (raw and encoded). objects_reached = the number of stored objects the body names:
the *_key of a fundamentals kind; the bestdata objects a query read; the objects of the datasets the coverage body
reports present.

REPLAY-OLD: the same calls with the normalizer as the identity in the changed modules (the OLD behaviour, a copy kept
here as a patch of the names, as in cj2_replay.py).

Cells are the (tool, key) pairs with stored objects in at least one spelling. A (tool, key) pair the stored tables hold
in neither spelling is printed as ZERO-BOTH with its table and is not a cell.

Prints cj6_replay.out (newline="\n", ASCII). Budget: 3000 requests and 300 MiB, enforced in the wrapper.

Usage, from the worktree root:  python -u <this file>
"""

import io
import os
import sys
from types import SimpleNamespace
from unittest import mock

ROOT = os.getcwd()
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, GW)
sys.path.insert(0, ROOT)

from app import audit, harvest_figures as hfig, harvest_identity as hid, harvest_read as hr  # noqa: E402
from app import harvest_research as hres  # noqa: E402
from lib.research.harvest import store  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cj6_replay.out")
BUCKET = "opal-data-harvest"
BUDGET_REQUESTS = 3000
BUDGET_BYTES = 300 * 1024 * 1024
OPAL = "hvst.cj6.replay@opalinvest.com"     # synthetic stand-in principal
KEYS = ("BP/_LN_Equity", "BP-SLASH-_LN_Equity", "NG/_LN_Equity", "NG-SLASH-_LN_Equity")
CONTROL = "UNH_US_Equity"
MODULES = (hfig, hid, hres)
FUND_KEYS = ("bestdata_key", "refdata_key", "histdata_key", "segments_key", "price_key")
TABLE = {
    "fundamentals:consensus": "bloomberg/harvest/bronze/bestdata/security_key=<partition>/",
    "fundamentals:reference": "bloomberg/harvest/bronze/refdata/security_key=<partition>/",
    "fundamentals:valuation_history": "bloomberg/harvest/bronze/histdata/security_key=<partition>/",
    "fundamentals:segments": "bloomberg/harvest/bronze/segments/security_key=<partition>/",
    "fundamentals:price": "bloomberg/harvest/bronze/price_history_px_last/ (one series per name)",
    "query:bestdata": "bloomberg/harvest/bronze/bestdata/security_key=<partition>/",
    "coverage": "the KEYED datasets of harvest_identity.py (HIVE partitions and path components)",
}


class BudgetExceeded(Exception):
    pass


class ReadOnly(object):
    """Forwards the two read operations on the harvest bucket; counts requests and GET bytes."""

    def __init__(self, client):
        self._c = client
        self.requests = 0
        self.bytes = 0

    def _spend(self):
        self.requests += 1
        if self.requests > BUDGET_REQUESTS or self.bytes > BUDGET_BYTES:
            raise BudgetExceeded("requests=%d bytes=%d" % (self.requests, self.bytes))

    def list_objects_v2(self, **kw):
        if kw.get("Bucket") != BUCKET:
            raise RuntimeError("replay reads %s only; a list named bucket %r" % (BUCKET, kw.get("Bucket")))
        self._spend()
        return self._c.list_objects_v2(**kw)

    def get_object(self, **kw):
        if kw.get("Bucket") != BUCKET:
            raise RuntimeError("replay reads %s only; a get named bucket %r" % (BUCKET, kw.get("Bucket")))
        self._spend()
        resp = self._c.get_object(**kw)
        data = resp["Body"].read()
        self.bytes += len(data)
        if self.bytes > BUDGET_BYTES:
            raise BudgetExceeded("requests=%d bytes=%d" % (self.requests, self.bytes))
        return {"Body": io.BytesIO(data)}

    def __getattr__(self, name):
        raise RuntimeError("replay is read-only: refuses S3 operation %r" % name)


def emit(lines, text):
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


def named(out):
    """The number of stored objects the body names (see the module docstring)."""
    if "datasets" in out:
        return sum(r["objects"] for r in out["datasets"] if r.get("present"))
    n = sum(1 for k in FUND_KEYS if out.get(k))
    if n:
        return n
    return sum(1 for s in out.get("source_keys") or [] if s.startswith("bloomberg/harvest/bronze/bestdata/"))


def call(tool, key):
    if tool.startswith("fundamentals:"):
        return hfig.harvest_get_fundamentals(key, tool.split(":", 1)[1])
    if tool == "query:bestdata":
        return hfig.harvest_query_columns("bestdata", ["security_key", "fy", "BEST_EPS"], security_keys=[key])
    return hid.harvest_security_coverage(key)


TOOLS = tuple(TABLE)


def old_patches():
    return [mock.patch.multiple(m, canonical_security_key=lambda k: k, slash_safe_key=lambda k: k) for m in MODULES]


def main():
    lines = []
    out_handle = open(OUT_PATH, "w", encoding="utf-8", newline="\n")

    def out(text):
        emit(lines, text)
        out_handle.write(lines[-1] + "\n")
        out_handle.flush()

    ro = ReadOnly(store._default_client())
    principal = SimpleNamespace(email=OPAL, tid="11111111-1111-4111-8111-111111111111",
                                oid="22222222-2222-4222-8222-222222222222")
    with mock.patch.object(hr, "_client", lambda: ro), \
            mock.patch.object(audit, "log_call", lambda *a, **kw: None), \
            mock.patch.object(hr, "get_current_principal", lambda: principal):
        try:
            out("CJ6-REPLAY-HEADER read-only replay of the changed gateway harvest tools (app/harvest_figures.py "
                "fundamentals and query, app/harvest_identity.py coverage) against stored objects; the gateway is not "
                "called; bucket %s; budget requests=%d bytes=%d; objects_reached = stored objects the body names"
                % (BUCKET, BUDGET_REQUESTS, BUDGET_BYTES))
            new = {}
            for tool in TOOLS:
                for key in KEYS:
                    res = call(tool, key)
                    new[(tool, key)] = res
                    out("REPLAY-OTHER %s %s objects_reached=%d" % (tool, key, named(res)))

            old = {}
            with mock.patch.multiple(hfig, canonical_security_key=lambda k: k, slash_safe_key=lambda k: k), \
                    mock.patch.multiple(hid, canonical_security_key=lambda k: k, slash_safe_key=lambda k: k), \
                    mock.patch.multiple(hres, canonical_security_key=lambda k: k, slash_safe_key=lambda k: k):
                for tool in TOOLS:
                    for key in KEYS:
                        res = call(tool, key)
                        old[(tool, key)] = res
                        out("REPLAY-OLD %s %s objects_reached=%d" % (tool, key, named(res)))

            cells = 0
            equal = 0
            for tool in TOOLS:
                for raw, enc in (("BP/_LN_Equity", "BP-SLASH-_LN_Equity"), ("NG/_LN_Equity", "NG-SLASH-_LN_Equity")):
                    a, b = named(new[(tool, raw)]), named(new[(tool, enc)])
                    if a == 0 and b == 0:
                        out("ZERO-BOTH %s %s table=%s" % (tool, raw.split("/")[0], TABLE[tool]))
                        continue
                    cells += 1
                    if a == b and a > 0:
                        equal += 1

            # the coverage split: partition datasets (both spellings read the partition form) against path components
            # (derived/, filings/, packs/, peers/, posture/, raw/, scores/: the caller's spelling, unchanged by the order)
            template = {p: t for p, t, _ in hid.KEYED}
            for key in KEYS:
                res = new[("coverage", key)]
                present = [r for r in res.get("datasets", []) if r.get("present")]
                part = sum(r["objects"] for r in present if template[r["dataset"]] == hid._HIVE)
                path = sum(r["objects"] for r in present if template[r["dataset"]] != hid._HIVE)
                out("REPLAY-OTHER-SPLIT coverage %s partition_objects=%d path_component_objects=%d" % (key, part, path))

            for tool in TOOLS:
                ctl = call(tool, CONTROL)
                out("REPLAY-CONTROL %s %s objects_reached=%d" % (tool, CONTROL, named(ctl)))

            out("REPLAY-OTHER-WHOLE cells=%d reached_both_forms_equal=%d" % (cells, equal))
            out("REPLAY-OTHER-TOTALS gets=%d bytes=%d" % (ro.requests, ro.bytes))
        except BudgetExceeded as exc:
            out("BUDGET-EXCEEDED %s -- replay stopped; no REPLAY-OTHER-WHOLE line" % exc)
            out_handle.close()
            return 2
    out_handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
