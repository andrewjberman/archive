"""Shared helpers for the ETFS_RIVALS round-1 checks (issuer-written, 2.0.0_SA_COO~RV).

Every check runs from the root of the worktree it grades (the worker's), imports the package from THAT tree,
and reads the captured BASG issuer archive from the MAIN worktree's .runtime/ (gitignored, device-local).
Each check prints exactly one verdict line of its own: '<ID> RESULT: PASS 0 failures' or '<ID> RESULT: FAIL <n> failures'.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile

ARCHIVE_REL = ".runtime/amgt-reconn-daily-census-20260929/basg"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()


def repo_root() -> pathlib.Path:
    return pathlib.Path(_git("rev-parse", "--show-toplevel"))


def main_root() -> pathlib.Path:
    common = pathlib.Path(_git("rev-parse", "--path-format=absolute", "--git-common-dir"))
    return common.parent


def setup_path() -> pathlib.Path:
    root = repo_root()
    for p in (str(root / "data" / "etfs" / "scripts"), str(root)):
        if p not in sys.path:
            sys.path.insert(0, p)
    return root


def archive_files(n: int) -> list[pathlib.Path]:
    """The LAST n captured BASG issuer files (report-date order), real bytes the issuer published."""
    arc = main_root() / ARCHIVE_REL
    files = sorted(arc.glob("*.txt"))
    if not files:
        raise SystemExit(f"archive empty or absent: {arc}")
    return files[-n:]


def archive_meta(txt: pathlib.Path) -> dict:
    return json.loads(txt.with_suffix(".json").read_text(encoding="utf-8"))


def basg_rows(txt: pathlib.Path) -> int:
    lines = txt.read_bytes().decode("utf-8-sig").splitlines()
    hdr = lines[0].split("|")
    i = hdr.index("fund_ticker")
    return sum(1 for ln in lines[1:] if ln.strip() and ln.split("|")[i].strip() == "BASG")


def all_rows(txt: pathlib.Path) -> int:
    lines = txt.read_bytes().decode("utf-8-sig").splitlines()
    return sum(1 for ln in lines[1:] if ln.strip())


def land(sink_dir: str, files: list[pathlib.Path]) -> list[dict]:
    """Land real archived bytes through RIV-c-1's land_bronze into a local sink."""
    from rivalfunds.collector_issuer import land_bronze

    out = []
    for f in files:
        meta = archive_meta(f)
        out.append(land_bronze(raw=f.read_bytes(), requested_date=meta["requested_date"],
                               source_url=meta["url"], sink=f"local:{sink_dir}", captured_at=meta["at"]))
    return out


def local_path(sink_dir: str, s3_uri: str) -> pathlib.Path:
    """local:<dir> mirrors s3://<bucket>/<key> as <dir>/<bucket>/<key>."""
    assert s3_uri.startswith("s3://"), s3_uri
    return pathlib.Path(sink_dir) / s3_uri[len("s3://"):]


def address(*a, **k) -> str:
    from lib.opal_naming import address as _address

    return _address(*a, **k)


def run_chain(sink_dir: str, files: list[pathlib.Path], through: str) -> dict:
    """bronze -> silver -> canonical_shape [-> trade_schedule] over real archived days, local sink only."""
    land(sink_dir, files)
    ev = {"mode": "replay", "batch_id": "chk", "sink": f"local:{sink_dir}", "date": archive_meta(files[-1])["requested_date"]}
    res = {}
    from rivalfunds import silver_issuer
    res["silver"] = silver_issuer.handler_entry(dict(ev))
    if through == "silver":
        return res
    from rivalfunds import gold_canonical_shape
    res["canonical"] = gold_canonical_shape.handler_entry(dict(ev))
    if through == "canonical":
        return res
    from rivalfunds import gold_trade_schedule
    res["trades"] = gold_trade_schedule.handler_entry(dict(ev))
    return res


def read_parquets(dir_path: pathlib.Path):
    import pandas as pd

    parts = sorted(dir_path.rglob("*.parquet"))
    if not parts:
        return pd.DataFrame(), 0
    return pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True), len(parts)


class Verdict:
    def __init__(self, cid: str):
        self.cid, self.fails = cid, []

    def check(self, ok: bool, msg: str) -> None:
        print(("OK:   " if ok else "FAIL: ") + msg)
        if not ok:
            self.fails.append(msg)

def guarded(cid: str, fn) -> int:
    """Run the check body; return the failure count. Each check prints its OWN literal verdict line."""
    v = Verdict(cid)
    try:
        fn(v)
    except SystemExit:
        raise
    except Exception as e:  # an import error at the base is the expected FAIL of a build check
        v.check(False, f"exception: {type(e).__name__}: {e}")
    return len(v.fails)


def tmpdir(prefix: str) -> str:
    return tempfile.mkdtemp(prefix=prefix)
