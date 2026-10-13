"""BP-b-6 (ADVI_BDPRCE round 2) -- lot split fixture test. Offline: no S3 call, no write to any bucket.

Loads a RECORDED bronze unrealized export (UNREALIZED_DAILY_2026-10-09.xlsx, read from the data directory
beside the worktree; the xlsx is parsed once and the parse is cached there, keyed by its sha256).
Runs the REPO silver function (legacy, from HEAD) and the PATCHED function (this deliverable) on:
  - the ORIGINAL export (as it is today: no Units / Cost Basis columns);
  - an export WITH two SYNTHETIC columns, 'Units' and 'Cost Basis', generated here so the export looks as it
    will after the template switch. THE TWO COLUMNS ARE SYNTHETIC. They are not in the recorded export.

Prints one last line 'LOT SPLIT TEST: OK <n> arms' (exit 0), or 'LOT SPLIT TEST: FAIL <why>' (exit 1).
With --emit-proof it also writes LOT_PROOF.json beside this file from the values measured in this run.
"""
import sys
import os
import json
import hashlib
import pickle
import importlib.util
import datetime as _dt
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]                       # worktree root: .../org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/<serial>
DATA = ROOT.parent / (ROOT.name + "-data")   # recorded exports, outside the checkout
REPO_MOD = ROOT / "data/black_diamond/scripts/silver/merge-daily-incremental.py"
PATCH_MOD = Path(os.environ.get("BP_B6_PATCH_MOD") or (HERE / "merge_daily_incremental.patched.py"))  # env = mutant control only
XLSX_NAME = "UNREALIZED_DAILY_2026-10-09.xlsx"
XLSX = DATA / XLSX_NAME
EXPORT_KEY = "forwardfill_v2/unrealized/" + XLSX_NAME
OUT = DATA / "out"
LOT_KEY = ["account_id", "asset_id", "open_date", "unit_cost"]
SYNTH = ["units", "cost_basis"]
FIXED_NOW = _dt.datetime(2026, 10, 13, 12, 0, 0, tzinfo=_dt.timezone.utc)


def fail(why):
    print("LOT SPLIT TEST: FAIL " + why)
    sys.exit(1)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if not (REPO_MOD.exists() and (ROOT / "lib/opal_naming.py").exists() and XLSX.exists()):
    fail("inputs missing: repo module, lib/opal_naming.py or the recorded export at %s" % XLSX)
sys.path.insert(0, str(ROOT))

# Real pandas read, wrapped: the Sheet1 and Timestamps frames are read once and served from memory after that.
_REAL_READ_EXCEL = pd.read_excel
_CACHE = {}


def _read_excel(io_, *a, **kw):
    name = str(io_).replace("\\", "/")
    if name.endswith(XLSX_NAME) and kw.get("sheet_name") == "Sheet1":
        return _CACHE["sheet1"].copy(deep=True)
    if name.endswith(XLSX_NAME) and kw.get("sheet_name") == "Timestamps":
        return _CACHE["timestamps"].copy(deep=True)
    return _REAL_READ_EXCEL(io_, *a, **kw)


pd.read_excel = _read_excel


def load_export():
    sha = sha256_file(XLSX)
    cache = DATA / ("sheets_%s.pkl" % sha[:16])
    if cache.exists():
        with open(cache, "rb") as f:
            blob = pickle.load(f)
        how = "cache"
    else:
        blob = {"sheet1": _REAL_READ_EXCEL(XLSX, sheet_name="Sheet1"),
                "timestamps": _REAL_READ_EXCEL(XLSX, sheet_name="Timestamps", header=None)}
        with open(cache, "wb") as f:
            pickle.dump(blob, f, protocol=4)
        how = "parsed"
    _CACHE.update(blob)
    return blob["sheet1"], sha, how


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _FrozenDT(_dt.datetime):
    """Pins _ingested_at so two runs over the same export are byte-comparable."""
    @classmethod
    def now(cls, tz=None):
        return FIXED_NOW if tz is not None else FIXED_NOW.replace(tzinfo=None)


def run_fn(mod, df, arm):
    arm_dir = OUT / arm
    arm_dir.mkdir(parents=True, exist_ok=True)
    mod.LOCAL_DIR = arm_dir
    mod.datetime = _FrozenDT
    uploads = []
    mod._s3_download = lambda key, local: True
    mod._s3_upload = lambda local, key: (uploads.append(("bucket", str(local), key)), True)[1]
    if hasattr(mod, "_s3_upload_addr"):
        mod._s3_upload_addr = lambda local, uri: (uploads.append(("addr", str(local), uri)), True)[1]
    _CACHE["sheet1"] = df
    key, n = mod.process_unrealized_xlsx_to_parquet(XLSX_NAME)
    if key is None or key.startswith("__"):
        fail("%s: function returned %r" % (arm, key))
    date = key.split("/")[-1][: -len(".parquet")]
    legacy_path = arm_dir / (date + ".parquet")
    return {"key": key, "n": n, "date": date, "uploads": uploads,
            "legacy_path": legacy_path, "legacy_bytes": legacy_path.read_bytes()}


def main(emit):
    repo = load_mod("repo_merge_daily", REPO_MOD)
    pat = load_mod("patched_merge_daily", PATCH_MOD)
    df0, sha, how = load_export()
    raw_cols = list(df0.columns)
    print("EXPORT key=%s sha256=%s bytes=%d cache=%s" % (EXPORT_KEY, sha, XLSX.stat().st_size, how))
    print("EXPORT rows=%d cols=%d" % (len(df0), len(raw_cols)))
    print("EXPORT raw column names: %s" % raw_cols)
    if "Units" in raw_cols or "Cost Basis" in raw_cols:
        fail("recorded export already carries Units/Cost Basis; the synthetic arm would not be synthetic")

    dfw = df0.copy(deep=True)
    units = ((dfw["AssetID"].to_numpy(dtype="int64") + np.arange(len(dfw))) % 997 + 1).astype("float64")
    dfw["Units"] = units
    dfw["Cost Basis"] = units * dfw["Unit Cost"].fillna(0.0).to_numpy(dtype="float64")
    print("SYNTHETIC COLUMNS ADDED (not in the recorded export): 'Units', 'Cost Basis' -- generated in this test")

    r_repo_orig = run_fn(repo, df0, "repo_orig")
    r_pat_orig = run_fn(pat, df0, "pat_orig")
    r_pat_with = run_fn(pat, dfw, "pat_with")
    r_repo_with = run_fn(repo, dfw, "repo_with")
    date = r_repo_orig["date"]
    if not (r_pat_orig["date"] == r_pat_with["date"] == r_repo_with["date"] == date):
        fail("partition date differs across runs")

    sha_repo = hashlib.sha256(r_repo_orig["legacy_bytes"]).hexdigest()
    sha_pat_orig = hashlib.sha256(r_pat_orig["legacy_bytes"]).hexdigest()
    sha_pat_with = hashlib.sha256(r_pat_with["legacy_bytes"]).hexdigest()
    legacy_orig = pd.read_parquet(r_pat_orig["legacy_path"])
    legacy_with = pd.read_parquet(r_pat_with["legacy_path"])
    legacy_repo = pd.read_parquet(r_repo_orig["legacy_path"])
    legacy_repo_with = pd.read_parquet(r_repo_with["legacy_path"])

    lot_path = r_pat_with["legacy_path"].parent / ("lots_%s.parquet" % date)
    lot = pd.read_parquet(lot_path)
    lot_rows = len(lot)
    legacy_rows = len(legacy_repo)

    arms = []
    arms.append(("1 legacy repo(orig) bytes == patched(orig) bytes", sha_repo == sha_pat_orig))
    arms.append(("2 legacy patched(with) bytes == repo(orig) bytes", sha_pat_with == sha_repo))
    arms.append(("3 lot rows %d > legacy rows %d and lot key unique"
                 % (lot_rows, legacy_rows),
                 lot_rows > legacy_rows and not lot.duplicated(subset=LOT_KEY).any()))
    arms.append(("4 lot carries units+cost_basis; legacy carries neither (orig and with)",
                 all(c in lot.columns for c in SYNTH)
                 and not any(c in legacy_orig.columns or c in legacy_with.columns for c in SYNTH)))
    lot_uris = [u for u in r_pat_with["uploads"] if u[0] == "addr"]
    from lib.opal_naming import address
    builder_uri = address("blackdiamond", "49financial", "silver", "unrealized_lots", "date=" + date)
    arms.append(("5 lot upload address == builder address, legacy key unchanged",
                 len(lot_uris) == 1 and lot_uris[0][2] == builder_uri
                 and any(u[2] == "silver/unrealized/%s.parquet" % date for u in r_pat_with["uploads"])))
    arms.append(("6 orig export: patched writes no lot table (SKIP path)",
                 not any(u[0] == "addr" for u in r_pat_orig["uploads"])))
    arms.append(("7 negative control: repo(with) legacy DOES carry units+cost_basis (the leak the patch stops)",
                 all(c in legacy_repo_with.columns for c in SYNTH)))

    for label, ok in arms:
        print("ARM %s: %s" % ("PASS" if ok else "FAIL", label))
    print("LEGACY rows=%d cols=%d sha256=%s" % (legacy_rows, len(legacy_repo.columns), sha_repo))
    print("LOT rows=%d (export rows=%d before lot-key dedup; legacy rows=%d after position dedup) columns=%s"
          % (lot_rows, len(dfw), legacy_rows, list(lot.columns)))
    print("LOT address=%s" % builder_uri)
    bad = [label for label, ok in arms if not ok]
    if bad:
        fail("; ".join(bad))

    if emit:
        head = json.loads((DATA / "s3_reads.json").read_text(encoding="utf-8"))
        t_s3 = (DATA / "s3_unrealized_template.json").read_bytes()
        t_pat = (HERE / "unrealized.patched.json").read_bytes()
        t_repo = (ROOT / "data/black_diamond/scripts/bronze/templates/unrealized.json").read_bytes()
        s3_p = json.loads(t_s3.decode("utf-8"))
        pat_p = json.loads(t_pat.decode("utf-8"))
        repo_p = json.loads(t_repo.decode("utf-8"))
        changed = []
        for i, m in enumerate(pat_p["facts"][0]["measures"]):
            if m["isSelected"] != s3_p["facts"][0]["measures"][i]["isSelected"]:
                changed.append("measure %d isSelected" % m["id"])
        proof = {
            "order": "BP-b-6",
            "read_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "claim": "measured",
            "export_key": EXPORT_KEY,
            "export_sha256": sha,
            "export_version_id": head["export"]["VersionId"],
            "legacy_bytes_equal": bool(sha_repo == sha_pat_orig == sha_pat_with),
            "legacy_sha256": sha_repo,
            "lot_rows": int(lot_rows),
            "legacy_rows": int(legacy_rows),
            "keyed_on_lot": bool(not lot.duplicated(subset=LOT_KEY).any()),
            "lot_key": LOT_KEY,
            "address": builder_uri,
            "address_from_builder": True,
            "new_columns_in_legacy": [c for c in SYNTH if c in legacy_with.columns or c in legacy_orig.columns],
            "template": {
                "changed_keys": changed,
                "s3_equals_repo": bool(t_s3 == t_repo),
                "s3_equals_repo_parsed": bool(s3_p == repo_p),
                "s3_equals_repo_after_crlf": bool(t_s3.replace(b"\r\n", b"\n") == t_repo),
                "s3_version_id": head["template"]["VersionId"],
                "s3_bytes": len(t_s3),
                "repo_bytes": len(t_repo),
                "patched_bytes": len(t_pat),
            },
            "synthetic_columns": True,
        }
        (HERE / "LOT_PROOF.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
        print("EMITTED LOT_PROOF.json")
    print("LOT SPLIT TEST: OK %d arms" % len(arms))
    return 0


if __name__ == "__main__":
    sys.exit(main(emit="--emit-proof" in sys.argv))
