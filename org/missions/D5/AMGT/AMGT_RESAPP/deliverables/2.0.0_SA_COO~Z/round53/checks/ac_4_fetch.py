"""AMGT_RESAPP round 53, AMGT-ac-4 AC1 (AMENDMENT 1) -- every filings/v1 key goes through crosswalk.slash_safe_key (CTO msg 27175).
`lib/research/filings/fetch.py` `pool_key(security_key, accession, suffix)` builds `filings/v1/<security_key>/<accession>.<suffix>.json`; its
four callers (analyze.py :1345 / :1470 reverify read / :1636 the .analysis.json write; filings/batch.py :478) inherit whatever it builds.
  (a) PLANT: pool_key("BP/_LN_Equity", "000000000000000001", "analysis") == "filings/v1/BP-SLASH-_LN_Equity/000000000000000001.analysis.json"
      and the UNRESOLVED-SOURCE form likewise encoded;
  (b) CONTROL: a slash-free key is byte-identical to today's formula (AMD_US_Equity -> filings/v1/AMD_US_Equity/...);
  (c) THE READ PATH: `analyze.reverify_stored_thesis_driver("BP/_LN_Equity", ..., client=<stub>, dry_run=True)` requests the analysis object
      at the ENCODED key (the stub records every get_object Key and raises after recording; the requested filings/v1 key is read back).
usage: python <this>   (from the repo root; no I/O)"""
import io
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from lib.research.filings import analyze, fetch  # noqa: E402


class Stop(Exception):
    pass


class _Pages:
    def paginate(self, **kw):
        return iter([{"Contents": []}])


class Stub:
    """Lists are empty and any non-filings read answers an empty source document, so the reverify path reaches its filings/v1 analysis
    read; that read is recorded and stops the run (nothing is ever written)."""

    def __init__(self):
        self.keys = []

    def get_paginator(self, name):
        return _Pages()

    def list_objects_v2(self, **kw):
        return {"Contents": []}

    def get_object(self, Bucket=None, Key=None, **kw):
        self.keys.append(Key)
        if str(Key).startswith("filings/v1/"):
            raise Stop(Key)
        return {"Body": io.BytesIO(json.dumps({"excerpt": {"text": ""}}).encode())}

    def __getattr__(self, name):
        def refuse(*a, **kw):
            raise Stop(name)
        return refuse


def main():
    acc = "000000000000000001"
    a = fetch.pool_key("BP/_LN_Equity", acc, "analysis")
    u = fetch.pool_key("NG/_LN_Equity", None, "source")
    c = fetch.pool_key("AMD_US_Equity", acc, "analysis")
    print("(a) %s | %s" % (a, u))
    print("(b) %s" % c)
    ok_a = a == "filings/v1/BP-SLASH-_LN_Equity/%s.analysis.json" % acc and u == "filings/v1/NG-SLASH-_LN_Equity/UNRESOLVED-SOURCE.source.json"
    ok_b = c == "filings/v1/AMD_US_Equity/%s.analysis.json" % acc
    stub = Stub()
    try:
        analyze.reverify_stored_thesis_driver("BP/_LN_Equity", acc, client=stub, dry_run=True)
    except Stop:
        pass
    except Exception as exc:  # a different failure is reported, never hidden
        print("(c) reverify raised %s: %s" % (type(exc).__name__, str(exc)[:160]))
    fk = [k for k in stub.keys if k and k.startswith("filings/v1/")]
    print("(c) filings/v1 keys the read path requested: %s" % fk)
    ok_c = bool(fk) and all("BP-SLASH-_LN_Equity" in k for k in fk)
    ok = ok_a and ok_b and ok_c
    print("EVERY FILINGS/V1 KEY GOES THROUGH SLASH_SAFE_KEY: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
