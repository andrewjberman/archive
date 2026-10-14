"""BP-c-5 (ADVI_BDPRCE round 3, PRD v1.3 re-seat) -- lot split fixture test, lot key WITH units. Offline: no S3 call.

Lot key under test (PRD v1.3, CTO call 67ac): (relationship_id, account_id, asset_id, open_date, unit_cost, units).
Market Value does not join the key. The recorded export carries NO Units column, so a zero-fold proof cannot be made
here: the zero is DEFERRED to the first real export under the apply's pair.

Loads the RECORDED bronze unrealized export (UNREALIZED_DAILY_2026-10-09.xlsx, sha256 5700843f...) from the data
directory of seat 0.9.0_WK_ADVI_BDPRCE~17 (read only; a parse cache is read from there when present, else written to
this seat's data directory). Runs the REPO silver function (legacy, from HEAD) and the PATCHED function
(merge_daily_incremental.patched3.py) on:
  - the ORIGINAL export (as it is today: no Units / Cost Basis columns) -- the SKIP path, no lot table;
  - an export WITH two SYNTHETIC columns, 'Units' and 'Cost Basis'. THE TWO COLUMNS ARE SYNTHETIC. They are not in
    the recorded export. Their values are a deterministic hash of each row's 15 recorded columns. Because the hash
    reads every recorded column, a synthetic 'units' separates rows that differ on ANY column, so a lot-table row
    count on the synthetic export is NOT evidence of a fold in either direction. It is labelled as such everywhere.
  - the five-column key (the pre-v1.3 key) run through the same patched module, to measure what it would fold.

Arms (10): 1-8 as the first seat's (legacy bytes equal, lot table larger and unique on its key, units and cost basis
in the lot table and in neither legacy table, the builder address, the relationship id survives); 9 the planted-frame
key check (units in the key); 10 the five-column fold measured by the module equals an INDEPENDENT pandas recount on
the raw rows (the number is printed; it is not asserted to be zero).

Prints ARM lines, the measured counts, then one last line 'LOT SPLIT3 TEST: OK <n> arms' (exit 0), or
'LOT SPLIT3 TEST: FAIL <why>' (exit 1). With --emit-proof it writes LOT_PROOF3.json beside this file BEFORE the
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
ROOT = HERE.parents[6]                            # worktree root: .../org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/<serial>
DATA_IN = ROOT.parent / "wk-bdprce-r3-17b-data"   # recorded export (read only), seat ~17's download
DATA_OUT = ROOT.parent / (ROOT.name + "-data")    # this seat's outputs and parse cache
REPO_MOD = ROOT / "data/black_diamond/scripts/silver/merge-daily-incremental.py"
PATCH_MOD = HERE / "merge_daily_incremental.patched3.py"
CAP_JSON = ROOT / "org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~16/CAP.json"
XLSX_NAME = "UNREALIZED_DAILY_2026-10-09.xlsx"
XLSX = DATA_IN / XLSX_NAME
EXPECTED_SHA = "5700843f9e661364910a5bbb9d9d4b60521775922539f47b066a10d80039ef5b"
EXPORT_KEY = "forwardfill_v2/unrealized/" + XLSX_NAME
EXPORT_VERSION_ID = "Wf2Pct313A.w7y1GpuSf2f7FfiKUVats"      # get-object --version-id, seat ~17, 2026-10-13
TEMPLATE_ROLLBACK_VERSION_ID = "VgzqQbd.3F3sAlllb6SWsjKZ2XvXgAfE"  # round 2 LOT_PROOF.json, template.s3_version_id
OUT = DATA_OUT / "out3"
LOT_KEY_RAW = ["Relationship ID", "AccountID", "AssetID", "Open Date", "Unit Cost"]   # five-column key, export headers
LOT_KEY_FIVE = ["relationship_id", "account_id", "asset_id", "open_date", "unit_cost"]  # the same, snake names
LOT_KEY_V13 = LOT_KEY_FIVE + ["units"]                                                  # PRD v1.3 key (reference)
SYNTH = ["units", "cost_basis"]
# Pinned to the value seat ~17 used, so the legacy bytes (which carry _ingested_at) compare with its recorded sha256.
FIXED_NOW = _dt.datetime(2026, 10, 13, 12, 0, 0, tzinfo=_dt.timezone.utc)


def fail(why):
    print("LOT SPLIT3 TEST: FAIL " + why)
    sys.exit(1)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


if not (REPO_MOD.exists() and PATCH_MOD.exists() and (ROOT / "lib/opal_naming.py").exists() and XLSX.exists()):
    fail("inputs missing: repo module, patched3 module, lib/opal_naming.py or the recorded export at %s" % XLSX)
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
    if sha != EXPECTED_SHA:
        fail("export sha256 %s != the recorded %s" % (sha, EXPECTED_SHA))
    name = "sheets_%s.pkl" % sha[:16]
    cache_read = [p for p in (DATA_OUT / name, DATA_IN / name) if p.exists()]
    if cache_read:
        with open(cache_read[0], "rb") as f:
            blob = pickle.load(f)
        how = "cache(%s)" % cache_read[0].parent.name
    else:
        blob = {"sheet1": _REAL_READ_EXCEL(XLSX, sheet_name="Sheet1"),
                "timestamps": _REAL_READ_EXCEL(XLSX, sheet_name="Timestamps", header=None)}
        DATA_OUT.mkdir(parents=True, exist_ok=True)
        with open(DATA_OUT / name, "wb") as f:
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
    pat_v13 = list(pat.LOT_KEY_COLS)
    if pat_v13 != LOT_KEY_V13:
        fail("patched module lot key %s is not the PRD v1.3 key %s" % (pat_v13, LOT_KEY_V13))
    df0, sha, how = load_export()
    raw_cols = list(df0.columns)
    print("CALLS: recorded export read locally; sha256 verified against the recorded value (fetched by seat ~17, "
          "get-object --version-id %s; not re-fetched here)" % EXPORT_VERSION_ID)
    print("EXPORT key=%s sha256=%s bytes=%d parse=%s" % (EXPORT_KEY, sha, XLSX.stat().st_size, how))
    print("EXPORT rows=%d cols=%d" % (len(df0), len(raw_cols)))
    print("EXPORT raw column names: %s" % raw_cols)
    print("EXPORT has NO Units column and NO Cost Basis column: the v1.3 zero cannot be measured on this export.")
    if "Units" in raw_cols or "Cost Basis" in raw_cols:
        fail("recorded export already carries Units/Cost Basis; the synthetic arm would not be synthetic")
    for c in LOT_KEY_RAW:
        if c not in raw_cols:
            fail("five-column key column missing from the export: %s" % c)
    print("PATCHED LOT KEY (PRD v1.3): %s" % pat_v13)

    # ---- the export's own lot identifier: none of the recorded headers is a lot / tax-lot / position id ----
    relationship_distinct = int(df0["Relationship ID"].nunique(dropna=False))
    print("LOT-ID CANDIDATE 'Relationship ID': %d distinct values in %d rows (not unique; not a lot id)"
          % (relationship_distinct, len(df0)))

    # ---- the five-column key, counted INDEPENDENTLY on the raw rows (plain pandas; no patched code) ----
    recount_five = int(len(df0) - len(df0.drop_duplicates(subset=LOT_KEY_RAW)))
    full = df0.drop_duplicates(subset=list(df0.columns))
    exact_dup = int(len(df0) - len(full))
    null_open = int(df0["Open Date"].isna().sum())
    print("EXPORT exact_duplicate_rows=%d distinct_full_rows=%d null_open_date_rows=%d"
          % (exact_dup, len(full), null_open))
    print("RECOUNT (independent, pandas on raw rows): five-column key would fold %d rows" % recount_five)

    # colliding groups under the five-column key still differing on any recorded column (reference, not a gate)
    gf = full.groupby(LOT_KEY_RAW, dropna=False, sort=False)
    multi = full[gf[LOT_KEY_RAW[0]].transform("size") > 1]
    differing_cols = {}
    for c in raw_cols:
        if c in LOT_KEY_RAW:
            continue
        n_diff = multi.groupby(LOT_KEY_RAW, dropna=False, sort=False)[c].nunique(dropna=False)
        differing_cols[c] = int((n_diff > 1).sum())
    five_colliding_groups = int(full.groupby(LOT_KEY_RAW, dropna=False, sort=False).size().gt(1).sum())
    print("FIVE-COLUMN KEY: colliding groups=%d; groups whose rows differ, per column: %s"
          % (five_colliding_groups, {k: v for k, v in differing_cols.items() if v}))

    # ---- synthetic columns: deterministic function of the row's 15 recorded values ----
    dfw = df0.copy(deep=True)
    h = pd.util.hash_pandas_object(df0[raw_cols].astype(str), index=False).to_numpy(dtype="uint64")
    units = (h % np.uint64(997) + np.uint64(1)).astype("float64")
    dfw["Units"] = units
    dfw["Cost Basis"] = units * df0["Unit Cost"].fillna(0.0).to_numpy(dtype="float64")
    print("SYNTHETIC COLUMNS ADDED (NOT in the recorded export): 'Units', 'Cost Basis' -- hash of the 15 recorded "
          "columns; a lot count on this export is synthetic and is NOT evidence of a fold")

    r_repo_orig = run_fn(repo, df0, "repo_orig")
    r_pat_orig = run_fn(pat, df0, "pat_orig")
    r_pat_with = run_fn(pat, dfw, "pat_with")
    r_repo_with = run_fn(repo, dfw, "repo_with")
    # the same patched module with the FIVE-column key, to measure the fold it would make through its own code
    pat5 = load_mod("patched_merge_daily_five", PATCH_MOD)
    pat5.LOT_KEY_COLS = list(LOT_KEY_FIVE)
    r_pat_five = run_fn(pat5, dfw, "pat_five_with")
    date = r_repo_orig["date"]
    if not (r_pat_orig["date"] == r_pat_with["date"] == r_repo_with["date"] == r_pat_five["date"] == date):
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
    lot_rows = len(lot)                       # v1.3 key, SYNTHETIC units
    legacy_rows = len(legacy_repo)
    lot_unique = all(c in lot.columns for c in pat_v13) and not lot.duplicated(subset=pat_v13).any()
    lot5 = pd.read_parquet(r_pat_five["legacy_path"].parent / ("lots_%s.parquet" % date))
    folded_five_module = int(len(df0) - len(lot5))   # what the patched module folds under the five-column key
    rows_folded_v13_synth = int(len(full) - lot_rows)
    lot_uris = [u for u in r_pat_with["uploads"] if u[0] == "addr"]
    from lib.opal_naming import address
    builder_uri = address("blackdiamond", "49financial", "silver", "unrealized_lots", "date=" + date)
    new_cols_legacy = [c for c in SYNTH if c in legacy_with.columns or c in legacy_orig.columns]

    # ---- arm 9: planted frame, the v1.3 key on the module's own function ----
    def planted(units_b, name_b):
        rows = [
            {"relationship_id": "PLANT-REL", "account_id": "PLANT-ACC", "asset_id": "PLANT-AST",
             "open_date": "2026-01-02", "unit_cost": 10.0, "units": 100.0, "cost_basis": 1000.0,
             "asset_name": "PLANT A", "_source_file": "planted", "_ingested_at": "planted"},
            {"relationship_id": "PLANT-REL", "account_id": "PLANT-ACC", "asset_id": "PLANT-AST",
             "open_date": "2026-01-02", "unit_cost": 10.0, "units": units_b, "cost_basis": units_b * 10.0,
             "asset_name": name_b, "_source_file": "planted", "_ingested_at": "planted"},
        ]
        return pd.DataFrame(rows)
    p_diff = planted(50.0, "PLANT A")        # equal on the five old columns, different units
    p_same = planted(100.0, "PLANT B")       # equal on all six key columns, different asset_name (a non-key column)
    lots_diff, _, n_diff = pat.build_unrealized_lots(p_diff)
    lots_same, _, n_same = pat.build_unrealized_lots(p_same)
    five_on_plant = int(len(p_diff) - len(p_diff.drop_duplicates(subset=LOT_KEY_FIVE)))
    print("PLANTED: five-column key folds %d of 2 rows (the old key would merge them)" % five_on_plant)
    print("PLANTED: v1.3 key, units differ -> lot rows %s; units equal -> lot rows %s" % (n_diff, n_same))

    arms = []
    arms.append(("1 legacy repo(orig) bytes == patched(orig) bytes", sha_repo == sha_pat_orig))
    arms.append(("2 legacy patched(with) bytes == repo(orig) bytes", sha_pat_with == sha_repo))
    arms.append(("3 lot rows %d (SYNTHETIC units) > legacy rows %d and lot key unique on the v1.3 key"
                 % (lot_rows, legacy_rows), lot_rows > legacy_rows and lot_unique))
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
    arms.append(("9 planted frame, v1.3 key: units differ -> 2 lots (equal on the five old columns, both survive); "
                 "units equal -> 1 lot (folds)",
                 n_diff == 2 and n_same == 1 and "units" in lots_diff.columns and five_on_plant == 1))
    arms.append(("10 five-column fold measured by the patched module %d == independent recount %d "
                 "(the number is printed, not asserted to be zero)" % (folded_five_module, recount_five),
                 folded_five_module == recount_five))

    for label, ok in arms:
        print("ARM %s: %s" % ("PASS" if ok else "FAIL", label))
    print("LEGACY rows=%d cols=%d sha256=%s" % (legacy_rows, len(legacy_repo.columns), sha_repo))
    print("LOT (v1.3 key, SYNTHETIC units) rows=%d (distinct full export rows=%d; export rows=%d) columns=%s"
          % (lot_rows, len(full), len(df0), list(lot.columns)))
    print("LOT (five-column key, through the patched module) rows=%d -> folds %d"
          % (len(lot5), folded_five_module))
    print("LOT address=%s" % builder_uri)
    print("ZERO-FOLD PROOF DEFERRED: the recorded export carries no Units column, so no fixture can prove a zero "
          "under the v1.3 key. The zero is deferred to the first real export under the apply's pair (PRD v1.3, call 67ac).")

    if emit:
        cap = json.loads(CAP_JSON.read_text(encoding="utf-8"))
        proof = {
            "order": "BP-c-5",
            "read_at": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "claim": "measured",
            "calls": [
                "local read of the recorded export (sha256 verified against the recorded value; fetched by seat "
                "0.9.0_WK_ADVI_BDPRCE~17 by get-object --version-id %s; not re-fetched by this seat)" % EXPORT_VERSION_ID,
                "aws s3api list-objects-v2 --bucket opal-data-bd --prefix forwardfill_v2/unrealized/ (read; 91 keys: "
                "76 daily xlsx, one per date, 15 _complete markers, 0 other; no slice objects)",
                "python pandas on the recorded export, offline (no S3 write, no upload, no producer run)",
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
            "lot_rows_basis": "v1.3 key on SYNTHETIC units (hash of the 15 recorded columns); not evidence of a fold",
            "synthetic_units_folded": rows_folded_v13_synth,
            "key_basis": "relationship_id",
            "keyed_on_lot": bool(lot_unique),
            "lot_key": list(pat_v13),
            "units_in_key": bool("units" in pat_v13),
            "folded_without_units": int(folded_five_module),
            "recount_without_units": int(recount_five),
            "zero_fold": "deferred_to_first_real_export",
            "five_column_colliding_groups": five_colliding_groups,
            "five_column_differing_columns": differing_cols,
            "columns_considered_for_lot_id": raw_cols,
            "lot_id_candidate_relationship_id_distinct": relationship_distinct,
            "planted_frame": {"five_column_fold": five_on_plant, "v13_lots_units_differ": int(n_diff),
                              "v13_lots_units_equal": int(n_same)},
            "address": builder_uri,
            "address_from_builder": bool(lot_uris and lot_uris[0][2] == builder_uri),
            "new_columns_in_legacy": new_cols_legacy,
            "synthetic_columns": True,
            "template_rollback_version_id": TEMPLATE_ROLLBACK_VERSION_ID,
            "cap_verdict_read": str(cap.get("verdict")),
            "cap_source": "org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~16/CAP.json",
            "arms": [{"label": label, "pass": bool(ok)} for label, ok in arms],
        }
        (HERE / "LOT_PROOF3.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
        print("EMITTED LOT_PROOF3.json")

    bad = [label for label, ok in arms if not ok]
    if bad:
        fail("; ".join(bad))
    print("LOT SPLIT3 TEST: OK %d arms" % len(arms))
    return 0


if __name__ == "__main__":
    sys.exit(main(emit="--emit-proof" in sys.argv))
