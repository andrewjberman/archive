"""AMGT_CORPUS round 39, CRPS-ao-1 -- the daily refresh's same-day skip keys on the PULL date (row Z-S88; round-38 analysis
ruling 6; CTO msg 30045). Issuer's file.

RUN:  PYTHONPATH=<worktree root> python skip_key_check.py
Calls the REAL `model_block_pull.cmd_refresh(dry_run=True)` against an in-memory S3 stub (list_objects_v2 with Prefix and
pagination, and get_paginator("list_objects_v2")); no AWS call, no Bloomberg session. Three registered names, each with a
model block in the store:
  PLANT    derived stamp TODAY 03:00Z (a same-day re-derive), last PULL stamp YESTERDAY      -> must be pulled   (build b1)
  CURRENT  derived stamp TODAY, last PULL stamp TODAY                                           -> must be skipped  (control c1)
  STALE    derived stamp YESTERDAY, last PULL stamp YESTERDAY                                   -> must be pulled   (control c2)
A PULL stamp is planted on BOTH places a pull lands: the pull-log state object (`_state_pull_log_prefix`) and the bronze
refdata + histdata objects (`_bronze_prefix`), so the check does not prescribe which of the two the producer reads.
Prints one line per arm, then `skip build <p>/1 control <q>/2`.
"""
import contextlib
import datetime as dt
import io
import subprocess
import sys

TOP = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
sys.path.insert(0, TOP)
from integrations.bloomberg.research import model_block_pull as mbp  # noqa: E402


class _StubS3:
    def __init__(self, keys):
        self.keys = sorted(keys)

    def list_objects_v2(self, Bucket=None, Prefix="", ContinuationToken=None, **_kw):
        keys = [k for k in self.keys if k.startswith(Prefix)]
        start = int(ContinuationToken) if ContinuationToken else 0
        page = keys[start:start + 3]
        resp = {"Contents": [{"Key": k} for k in page], "KeyCount": len(page), "IsTruncated": start + 3 < len(keys)}
        if resp["IsTruncated"]:
            resp["NextContinuationToken"] = str(start + 3)
        return resp

    def get_paginator(self, name):
        assert name == "list_objects_v2", name
        stub = self

        class _P:
            def paginate(self, Bucket=None, Prefix="", **_kw):
                token = None
                while True:
                    resp = stub.list_objects_v2(Bucket=Bucket, Prefix=Prefix, ContinuationToken=token)
                    yield resp
                    if not resp.get("IsTruncated"):
                        return
                    token = resp["NextContinuationToken"]

        return _P()


def main() -> int:
    now = dt.datetime.utcnow()
    today = now.strftime("%Y%m%d")
    yday = (now - dt.timedelta(days=1)).strftime("%Y%m%d")
    names = {
        "PLANT_US_Equity": (f"{today}T030000Z", f"{yday}T130500Z"),
        "CURRENT_US_Equity": (f"{today}T131000Z", f"{today}T130500Z"),
        "STALE_US_Equity": (f"{yday}T131000Z", f"{yday}T130500Z"),
    }
    keys = []
    for key, (derived, pulled) in names.items():
        keys.append(f"derived/model_block/{key}/{derived}/model_block.json")
        keys.append(f"{mbp._state_pull_log_prefix(key)}{pulled}.json")
        for request in ("refdata", "histdata"):
            keys.append(f"{mbp._bronze_prefix(request, key)}{pulled}.json")
    s3 = _StubS3(keys)
    mbp._registered_security_keys = lambda: list(names)
    mbp._s3 = lambda: s3
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mbp.cmd_refresh(dry_run=True)
    lines = buf.getvalue().splitlines()
    pulled = {ln.split()[2] for ln in lines if ln.startswith("DRY-RUN REFRESH: ")}
    skipped = {ln.split()[2] for ln in lines if ln.startswith("REFRESH SKIP: ")}
    b1 = rc == 0 and "PLANT_US_Equity" in pulled
    c1 = rc == 0 and "CURRENT_US_Equity" in skipped and "CURRENT_US_Equity" not in pulled
    c2 = rc == 0 and "STALE_US_Equity" in pulled
    print(f"ARM b1 {'PASS' if b1 else 'FAIL'} same-day re-derive, pulled yesterday -> pulled {sorted(pulled)}")
    print(f"ARM c1 {'PASS' if c1 else 'FAIL'} pulled today -> skipped {sorted(skipped)}")
    print(f"ARM c2 {'PASS' if c2 else 'FAIL'} stale -> pulled; rc {rc}; last line {lines[-1] if lines else ''!r}")
    print(f"skip build {int(b1)}/1 control {int(c1) + int(c2)}/2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
