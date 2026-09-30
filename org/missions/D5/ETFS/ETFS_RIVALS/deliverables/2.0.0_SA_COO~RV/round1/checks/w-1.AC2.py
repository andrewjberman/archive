"""RIV-w-1 AC2 -- the live seam: the module's own day listing against the REAL bucket prefix (read-only).

Before RIV-d-2 nothing is published, so zero days is the expected live answer; the criterion is that the real
listing runs through the module's code, parses every CommonPrefix it gets, and raises nothing."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    root = c.setup_path()
    sys.path.insert(0, str(root / "infra" / "aws" / "ec2" / "opal-gateway"))
    from app import rivalfunds_view as rv

    days = rv._list_days()
    print("live days:", days)
    v.check(isinstance(days, list), f"_list_days() returned a list ({type(days).__name__})")
    v.check(all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d)) for d in days), f"every listed day is YYYY-MM-DD ({len(days)} day(s))")
    bucket, prefix = rv._location()
    want = c.address("rivalfunds", "etfs", "platinum", "page", "date=X")
    v.check(f"s3://{bucket}/{prefix}" == want.rsplit("date=X", 1)[0], f"_location() is the builder's page prefix ({bucket}/{prefix})")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
