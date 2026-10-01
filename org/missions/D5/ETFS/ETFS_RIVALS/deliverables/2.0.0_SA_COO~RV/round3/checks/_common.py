"""Shared helpers for the ETFS_RIVALS round-3 checks (issuer-written, 2.0.0_SA_COO~RV).

Every check runs from the root of the worktree it grades, imports the package from THAT tree, and reads device-local
captures from the MAIN worktree's .runtime/ (gitignored). Each check prints exactly one verdict line of its own:
'<ID> RESULT: PASS 0 failures' or '<ID> RESULT: FAIL <n> failures'.

Re-exports every round-2 helper (which re-exports round 1's): Verdict, guarded, setup_path, local_path, address,
read_parquets, tmpdir, main_root, archive_files, archive_meta, land, idvz_captures, capture, capture_rows_by_fund,
dividends_path, import_bloomberg, replay, gold_dir, run_idvz_chain, IDVZ_GROUP, PFOE_GROUP.
"""
from __future__ import annotations

import importlib.util
import pathlib
import shutil

_R2 = pathlib.Path(__file__).resolve().parents[2] / "round2" / "checks" / "_common.py"
_spec = importlib.util.spec_from_file_location("_rivals_r2_common", _R2)
_r2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r2)

Verdict, guarded, setup_path, local_path, address = _r2.Verdict, _r2.guarded, _r2.setup_path, _r2.local_path, _r2.address
read_parquets, tmpdir, main_root, archive_files, archive_meta, land = (
    _r2.read_parquets, _r2.tmpdir, _r2.main_root, _r2.archive_files, _r2.archive_meta, _r2.land)
idvz_captures, capture, capture_rows_by_fund, dividends_path = (
    _r2.idvz_captures, _r2.capture, _r2.capture_rows_by_fund, _r2.dividends_path)
import_bloomberg, replay, gold_dir, run_idvz_chain = _r2.import_bloomberg, _r2.replay, _r2.gold_dir, _r2.run_idvz_chain
IDVZ_GROUP, PFOE_GROUP, PFOE_CAPTURES_REL = _r2.IDVZ_GROUP, _r2.PFOE_GROUP, _r2.PFOE_CAPTURES_REL

HOME_LANDING_FMT = "s3://opal-data-etfs/bbg/{d}/constituents/constituents_issuer_fill.parquet"
CHARACTERISTICS_FMT = "s3://opal-data-etfs/bbg/{d}/characteristics.parquet"


def pfoe_capture(date: str) -> pathlib.Path:
    """The PFOE-group Excel BQL census capture for one requested date (real Bloomberg response)."""
    p = main_root() / PFOE_CAPTURES_REL / f"{date}.json"
    if not p.is_file():
        raise SystemExit(f"PFOE capture absent: {p}")
    return p


def mirror_s3(sink_dir: str, s3_uri: str) -> pathlib.Path:
    """READ-ONLY copy of one live S3 object into the local sink at the path the local sink maps that URI to."""
    import boto3

    dest = local_path(sink_dir, s3_uri)
    dest.parent.mkdir(parents=True, exist_ok=True)
    bucket, key = s3_uri[len("s3://"):].split("/", 1)
    boto3.client("s3").download_file(bucket, key, str(dest))
    return dest


def copy_local(src: pathlib.Path, sink_dir: str, s3_uri: str) -> pathlib.Path:
    dest = local_path(sink_dir, s3_uri)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    return dest
