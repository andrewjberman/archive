"""AMGT_RESAPP round 51, AMGT-zz-6 AC1 -- the thesis driver's chart series from the filing's own verified points (CTO round-50 ruling 5;
DSGN FWD-1). ASML_NA_Equity's stored analysis (filings/v1/ASML_NA_Equity/000162828026011378.analysis.json) holds 3 driver points and
resolution 'cited', but its chart reads ABSENT: the filing branch of `thesis_driver_chart` needs >= 2 points carrying a span, which a
re-verification against the source excerpt supplies.

`lib.research.filings.analyze.reverify_stored_thesis_driver(security_key, accession, client=None, dry_run=False)` must accept
`dry_run=True`: compute exactly as today, WRITE NOTHING, return (doc, key, receipt) with a receipt string naming the dry run. This
check REFUSES to call it without that parameter (today's function rewrites the stored object unconditionally), and wraps the S3
client so any put raises. Then `scoped_amgt.thesis_driver_chart(<the re-verified driver>, [])` must read status SERVED, source
'filing', >= 2 numeric points.
usage: python <this>   (from the repo root; reads S3 read-only)"""
import inspect
import os
import sys

sys.path.insert(0, os.getcwd())
KEY = "ASML_NA_Equity"
ACCESSION = "000162828026011378"


class NoWrite:
    def __init__(self, real):
        self._real = real

    def put_object(self, *a, **kw):
        raise RuntimeError("the dry run attempted an S3 put")

    def __getattr__(self, name):
        return getattr(self._real, name)


def main():
    import boto3
    from lib.research.filings import analyze
    from lib.research.api import scoped_amgt as sa
    params = inspect.signature(analyze.reverify_stored_thesis_driver).parameters
    if "dry_run" not in params:
        print("reverify_stored_thesis_driver takes no dry_run (params: %s) -- NOT called (it would rewrite the stored object)" % ", ".join(params))
        print("THE DRIVER CHART IS SERVED FROM THE FILING'S VERIFIED POINTS: NO")
        return 1
    doc, key, receipt = analyze.reverify_stored_thesis_driver(KEY, ACCESSION, client=NoWrite(boto3.client("s3", region_name="us-east-1")), dry_run=True)
    driver = (doc or {}).get("thesis_driver") or {}
    pts = driver.get("points") or []
    chart = sa.thesis_driver_chart(driver, []) or {}
    cpts = chart.get("points") or []
    print("dry run receipt: %r; re-verified points %d (with span %d); chart %s source %r points %d" % (
        str(receipt)[:80], len(pts), sum(1 for p in pts if p.get("span")), chart.get("status"), chart.get("source"), len(cpts)))

    def num(v):
        try:
            float(str(v).replace(",", ""))
            return True
        except (TypeError, ValueError):
            return False
    ok = (isinstance(receipt, str) and "DRY" in receipt.upper() and chart.get("status") == "SERVED" and chart.get("source") == "filing"
          and len(cpts) >= 2 and all(num(p.get("value")) for p in cpts))
    print("THE DRIVER CHART IS SERVED FROM THE FILING'S VERIFIED POINTS: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
