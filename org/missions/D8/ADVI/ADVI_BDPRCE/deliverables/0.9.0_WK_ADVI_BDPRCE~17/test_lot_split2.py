"""BP-c-5 (ADVI_BDPRCE round 3) -- lot split fixture test with the RULED v1.1 key. Offline: no S3 call, no write.

Loads the RECORDED bronze unrealized export (UNREALIZED_DAILY_2026-10-09.xlsx, sha256 5700843f...), read from the
data directory beside the worktree (C:/dev/wk-bdprce-r3-17b-data). The xlsx is parsed once and cached there by sha256.
Runs the REPO silver function (legacy, from HEAD) and the PATCHED function (merge_daily_incremental.patched2.py) on:
  - the ORIGINAL export (as it is today: no Units / Cost Basis columns);
  - an export WITH two SYNTHETIC columns, 'Units' and 'Cost Basis'. THE TWO COLUMNS ARE SYNTHETIC. They are not in
    the recorded export. Their values are a deterministic hash of each row's 15 recorded columns, so two rows that
    are identical on every recorded column carry identical synthetic values (a row-position value would make
    identical rows look different and hide the fold).

Ruled lot key (PRD v1.1): (relationship_id, account_id, asset_id, open_date, unit_cost), or the export's own lot
identifier where one exists. This export carries no lot identifier column, so key_basis is relationship_id.

Prints ARM lines and the measured counts, then one last line 'LOT SPLIT2 TEST: OK <n> arms' (exit 0), or
'LOT SPLIT2 TEST: FAIL <why>' (exit 1). With --emit-proof it writes LOT_PROOF2.json beside this file BEFORE the
verdict, so a failing run still records its real numbers.
"""
import sys
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
PATCH_MOD = HERE / "merge_daily_incremental.patched2.py"
CAP_JSON = ROOT / "org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~16/CAP.json"
XLSX_NAME = "UNREALIZED_DAILY_2026-10-09.xlsx"
XLSX = DATA / XLSX_NAME
EXPORT_KEY = "forwardfill_v2/unrealized/" + XLSX_NAME
EXPORT_VERSION_ID = "Wf2Pct313A.w7y1GpuSf2f7FfiKUVats"      # get-object --version-id, 2026-10-13
TEMPLATE_ROLLBACK_VERSION_ID = "VgzqQbd.3F3sAlllb6SWsjKZ2XvXgAfE"  # round 2 LOT_PROOF.json, S3 template prior bytes
OUT = DATA / "out2"
LOT_KEY_RAW = ["Relationship ID", "AccountID", "AssetID", "Open Date", "Unit Cost"]   # export headers of the ruled key
LOT_KEY = ["relationship_id", "account_id", "asset_id", "open_date", "unit_cost"]     # snake names in the lot table
LOT_KEY_R4 = ["AccountID", "AssetID", "Open Date", "Unit Cost"]                       # round-2 key, reference only
SYNTH = ["units", "cost_basis"]
FIXED_NOW = _dt.datetime(2026, 10, 13, 12, 0, 0, tzinfo=_dt.timezone.utc)


def fail(why):
    print("LOT SPLIT2 TEST: FAIL " + why)
    sys.exit(1)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if not (REPO_MOD.exists() and PATCH_MOD.exists() and (ROOT / "lib/opal_naming.py").exists() and XLSX.exists()):
    fail("inputs missing: repo module, patched2 module, lib/opal_naming.py or the recorded export at %s" % XLSX)
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


def key_counts(full, key_cols, label):
    """full = export rows with exact duplicates removed. Returns the lot-key counts for one key."""
    lots = len(full.drop_duplicates(subset=key_cols))
    raw_sizes = full.groupby(key_cols, dropna=False, sort=False).size()
    return {"key": label, "lot_rows": int(lots), "rows_folded": int(len(full) - lots),
            "colliding_groups": int((raw_sizes > 1).sum()),
            "rows_in_colliding_groups": int(raw_sizes[raw_sizes > 1].sum())}


def main(emit):
    repo = load_mod("repo_merge_daily", REPO_MOD)
    pat = load_mod("patched_merge_daily", PATCH_MOD)
    df0, sha, how = load_export()
    raw_cols = list(df0.columns)
    print("CALLS: export read by get-object --version-id %s; sha256 verified against the recorded value" % EXPORT_VERSION_ID)
    print("EXPORT key=%s sha256=%s bytes=%d cache=%s" % (EXPORT_KEY, sha, XLSX.stat().st_size, how))
    print("EXPORT rows=%d cols=%d" % (len(df0), len(raw_cols)))
    print("EXPORT raw column names: %s" % raw_cols)
    if "Units" in raw_cols or "Cost Basis" in raw_cols:
        fail("recorded export already carries Units/Cost Basis; the synthetic arm would not be synthetic")
    for c in LOT_KEY_RAW:
        if c not in raw_cols:
            fail("ruled key column missing from the export: %s" % c)

    # ---- the export's own lot identifier: none of the recorded headers is a lot / tax-lot / position id ----
    relationship_distinct = int(df0["Relationship ID"].nunique(dropna=False))
    print("LOT-ID CANDIDATE 'Relationship ID': %d distinct values in %d rows (not unique; not a lot id)"
          % (relationship_distinct, len(df0)))

    # ---- measured counts on the RAW export (no synthetic columns) ----
    raw15 = list(raw_cols)
    full = df0.drop_duplicates(subset=raw15)
    exact_dup = int(len(df0) - len(full))
    null_open = int(df0["Open Date"].isna().sum())
    print("EXPORT exact_duplicate_rows=%d distinct_full_rows=%d null_open_date_rows=%d"
          % (exact_dup, len(full), null_open))
    ruled = key_counts(full, LOT_KEY_RAW, "ruled v1.1 " + " + ".join(LOT_KEY_RAW))
    ref4 = key_counts(full, LOT_KEY_R4, "round-2 key (reference only)")
    wide = key_counts(full, LOT_KEY_RAW + ["Market Value"], "candidate: ruled key + Market Value (reference only)")
    print("KEY ruled: lot_rows=%d rows_folded=%d colliding_groups=%d rows_in_colliding_groups=%d"
          % (ruled["lot_rows"], ruled["rows_folded"], ruled["colliding_groups"], ruled["rows_in_colliding_groups"]))
    print("KEY round-2 (reference): lot_rows=%d rows_folded=%d colliding_groups=%d rows_in_colliding_groups=%d"
          % (ref4["lot_rows"], ref4["rows_folded"], ref4["colliding_groups"], ref4["rows_in_colliding_groups"]))
    print("KEY candidate (reference, NOT ruled): ruled key + Market Value: lot_rows=%d rows_folded=%d colliding_groups=%d"
          % (wide["lot_rows"], wide["rows_folded"], wide["colliding_groups"]))

    # colliding groups under the ruled key still differing on any recorded column (exact duplicates removed)
    gf = full.groupby(LOT_KEY_RAW, dropna=False, sort=False)
    multi = full[gf[LOT_KEY_RAW[0]].transform("size") > 1]
    differing_cols = {}
    for c in raw15:
        if c in LOT_KEY_RAW:
            continue
        n_diff = multi.groupby(LOT_KEY_RAW, dropna=False, sort=False)[c].nunique(dropna=False)
        differing_cols[c] = int((n_diff > 1).sum())
    any_diff_groups = multi.groupby(LOT_KEY_RAW, dropna=False, sort=False).ngroups
    colliding_differing = int(any_diff_groups)
    print("KEY ruled: colliding groups still differing (15 recorded columns) = %d" % colliding_differing)
    print("KEY ruled: per-column count of colliding groups whose rows differ: %s"
          % {k: v for k, v in differing_cols.items() if v})

    # ---- synthetic columns: deterministic function of the row's 15 recorded values ----
    dfw = df0.copy(deep=True)
    h = pd.util.hash_pandas_object(df0[raw15].astype(str), index=False).to_numpy(dtype="uint64")
    units = (h % np.uint64(997) + np.uint64(1)).astype("float64")
    dfw["Units"] = units
    dfw["Cost Basis"] = units * df0["Unit Cost"].fillna(0.0).to_numpy(dtype="float64")
    print("SYNTHETIC COLUMNS ADDED (NOT in the recorded export): 'Units', 'Cost Basis' -- hash of the 15 recorded columns")

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
    lot_unique = not lot.duplicated(subset=LOT_KEY).any()
    lot_uris = [u for u in r_pat_with["uploads"] if u[0] == "addr"]
    from lib.opal_naming import address
    builder_uri = address("blackdiamond", "49financial", "silver", "unrealized_lots", "date=" + date)
    new_cols_legacy = [c for c in SYNTH if c in legacy_with.columns or c in legacy_orig.columns]

    arms = []
    arms.append(("1 legacy repo(orig) bytes == patched(orig) bytes", sha_repo == sha_pat_orig))
    arms.append(("2 legacy patched(with) bytes == repo(orig) bytes", sha_pat_with == sha_repo))
    arms.append(("3 lot rows %d > legacy rows %d and lot key unique" % (lot_rows, legacy_rows),
                 lot_rows > legacy_rows and lot_unique))
    arms.append(("4 lot carries units+cost_basis; legacy carries neither (orig and with)",
                 all(c in lot.columns for c in SYNTH) and not new_cols_legacy))
    arms.append(("5 lot upload address == builder address, legacy key unchanged",
                 len(lot_uris) == 1 and lot_uris[0][2] == builder_uri
                 and any(u[2] == "silver/unrealized/%s.parquet" % date for u in r_pat_with["uploads"])))
    arms.append(("6 orig export: patched writes no lot table (SKIP path)",
                 not any(u[0] == "addr" for u in r_pat_orig["uploads"])))
    arms.append(("7 negative control: repo(with) legacy DOES carry units+cost_basis",
                 all(c in legacy_repo_with.columns for c in SYNTH)))
    arms.append(("8 relationship_id survives into legacy and lot tables",
                 "relationship_id" in legacy_with.columns and "relationship_id" in lot.columns))
    arms.append(("9 rows folded under the ruled key == 0 (measured %d)" % ruled["rows_folded"],
                 ruled["rows_folded"] == 0))
    arms.append(("10 colliding groups still differing under the ruled key == 0 (measured %d)"
                 % colliding_differing, colliding_differing == 0))

    for label, ok in arms:
        print("ARM %s: %s" % ("PASS" if ok else "FAIL", label))
    print("LEGACY rows=%d cols=%d sha256=%s" % (legacy_rows, len(legacy_repo.columns), sha_repo))
    print("LOT rows=%d (distinct full export rows=%d; export rows=%d) columns=%s"
          % (lot_rows, len(full), len(df0), list(lot.columns)))
    print("LOT address=%s" % builder_uri)

    if emit:
        cap = json.loads(CAP_JSON.read_text(encoding="utf-8"))
        proof = {
            "order": "BP-c-5",
            "read_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "claim": "measured",
            "calls": [
                "aws s3api get-object --bucket opal-data-bd --key %s --version-id %s (read; sha256 checked)"
                % (EXPORT_KEY, EXPORT_VERSION_ID),
                "aws s3 cp s3://opal-data-bd/forwardfill_v2/unrealized/_complete/2026-10-09.json (read; marker carries no row count)",
                "aws s3 cp s3://opal-data-bd/forwardfill_v2/unrealized/_complete/2026-07-08.json (read)",
                "aws s3api list-objects-v2 --prefix forwardfill_v2/unrealized/ (read; key listing, rail-checked)",
                "python -I openpyxl read_only on the recorded export (local header and row count)",
            ],
            "export_key": EXPORT_KEY,
            "export_sha256": sha,
            "export_version_id": EXPORT_VERSION_ID,
            "export_rows": int(len(df0)),
            "export_columns": raw_cols,
            "exact_duplicate_rows": exact_dup,
            "distinct_full_rows": int(len(full)),
            "null_open_date_rows": null_open,
            "legacy_bytes_equal": bool(sha_repo == sha_pat_orig == sha_pat_with),
            "legacy_sha256": sha_repo,
            "legacy_rows": int(legacy_rows),
            "lot_rows": int(lot_rows),
            "rows_folded": int(ruled["rows_folded"]),
            "colliding_groups": int(ruled["colliding_groups"]),
            "colliding_groups_differing": int(colliding_differing),
            "differing_columns": differing_cols,
            "key_basis": "relationship_id",
            "lot_key": LOT_KEY,
            "keyed_on_lot": bool(lot_unique),
            "columns_considered_for_lot_id": raw_cols,
            "lot_id_candidate_relationship_id_distinct": relationship_distinct,
            "round2_key_reference": {"key": LOT_KEY_R4, "lot_rows": ref4["lot_rows"],
                                     "rows_folded": ref4["rows_folded"],
                                     "colliding_groups": ref4["colliding_groups"]},
            "wider_key_reference_not_ruled": {"key": LOT_KEY + ["market_value"], "lot_rows": wide["lot_rows"],
                                              "rows_folded": wide["rows_folded"],
                                              "colliding_groups": wide["colliding_groups"]},
            "address": builder_uri,
            "address_from_builder": bool(lot_uris and lot_uris[0][2] == builder_uri),
            "new_columns_in_legacy": new_cols_legacy,
            "synthetic_columns": True,
            "template_rollback_version_id": TEMPLATE_ROLLBACK_VERSION_ID,
            "cap_verdict_read": str(cap.get("verdict")),
            "cap_source": "org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~16/CAP.json",
            "arms": [{"label": label, "pass": bool(ok)} for label, ok in arms],
        }
        (HERE / "LOT_PROOF2.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
        print("EMITTED LOT_PROOF2.json")

    bad = [label for label, ok in arms if not ok]
    if bad:
        fail("; ".join(bad))
    print("LOT SPLIT2 TEST: OK %d arms" % len(arms))
    return 0


if __name__ == "__main__":
    sys.exit(main(emit="--emit-proof" in sys.argv))
