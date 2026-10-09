"""TO-DB-b-69 (S32): the returns table for ONE day, built by account_return_daily.py at the OLD pin (bc50d5711e, the deployed one) or at HEAD,
by the HEAD handler's own --local compute over the same account set. Run it twice on the kit's interpreter and compare the sha256.

Usage (worktree root): <python> <this file> <old|head> <day> <out.parquet>
The old pin is `git show bc50d5711e:<producer path>` executed as the module `account_return_daily` with __file__ set to the real producer
path, so its repo-relative reads (declaration, classification table, lib) resolve in this worktree exactly as the deployed module's would
in its own package; only the producer's CODE differs between the two runs. Reads S3 only; writes the local parquet and prints its sha256.
"""
import hashlib
import json
import platform
import subprocess
import sys
import types
from pathlib import Path

import numpy
import pandas
import pyarrow

ROOT = Path(__file__).resolve().parents[7]
PRODUCER_REL = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
OLD_PIN = "bc50d5711e"
sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-gold"))


def main(which, day, out):
    import handler as h
    rt = {"python": platform.python_version(), "pandas": pandas.__version__, "numpy": numpy.__version__, "pyarrow": pyarrow.__version__}
    print("RUNTIME " + json.dumps(rt), flush=True)
    if which == "old":
        src = subprocess.run(["git", "show", "%s:%s" % (OLD_PIN, PRODUCER_REL)], cwd=str(ROOT), capture_output=True, check=True).stdout
        print("OLD_PIN_SOURCE_SHA256 " + hashlib.sha256(src).hexdigest(), flush=True)
        path = str(ROOT / PRODUCER_REL)
        mod = types.ModuleType("account_return_daily_oldpin")
        mod.__file__ = path
        sys.modules["account_return_daily_oldpin"] = mod
        exec(compile(src, path, "exec"), mod.__dict__)
        h.ard = mod
    else:
        print("HEAD_SOURCE_SHA256 " + hashlib.sha256((ROOT / PRODUCER_REL).read_bytes()).hexdigest(), flush=True)
    h.local(day, out)
    data = Path(out).read_bytes()
    frame = pandas.read_parquet(out)
    canon = frame.sort_values(list(frame.columns[:2])).reset_index(drop=True).to_csv(index=False).encode("utf-8")
    print("RETURNS_PARQUET_SHA256 %s rows=%d" % (hashlib.sha256(data).hexdigest(), len(frame)), flush=True)
    print("RETURNS_CANON_CSV_SHA256 " + hashlib.sha256(canon).hexdigest(), flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
