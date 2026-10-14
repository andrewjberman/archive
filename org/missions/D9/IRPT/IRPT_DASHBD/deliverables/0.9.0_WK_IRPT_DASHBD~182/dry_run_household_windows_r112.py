"""IRPT_DASHBD round 112, cell DB-b-227 (worker 0.9.0_WK_IRPT_DASHBD~182): the PRIVATE run of the household window rule.

Usage: python -I dry_run_household_windows_r112.py <repo_root>

READS (S3 LIST and GET only): (a) the date= partitions of the firm's irpt account_return_daily gold dated on or before
2026-10-13 (every object of each partition is read); (b) the newest date= partition of the firm's ADVI household_crosswalk
(one GET of its household_crosswalk.parquet). Both addresses come from lib/opal_naming.address() on the firm's registry row.
The household table is built in memory with compute_household_returns and tied out row for row to round 111's private table
(read only). The window results come from household_window_result. WRITES: one private parquet in the private evidence
folder and HOUSEHOLD_WINDOWS_R112.json in this folder (counts and words). No S3 write, no vendor call, no secret read.
"""
import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
import re
import sys

FIRM_ID = "49financial"
AS_OF = "2026-10-13"
REGISTRY_REL = "data/firm_registry.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/household_return_daily.py"
DELIVER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~182"
DRIVER_REL = DELIVER_REL + "/dry_run_household_windows_r112.py"
REC_REL = DELIVER_REL + "/HOUSEHOLD_WINDOWS_R112.json"
ROUND111_TABLE = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~179/household_return_daily.parquet"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~182"
PRIVATE_NAME = "household_windows_r112.parquet"
RET_TABLE = "account_return_daily"
XW_TABLE = "household_crosswalk"
XW_FILE = "household_crosswalk.parquet"
MAX_PARTITIONS = 900
DATE_RX = re.compile(r"date=(\d{4}-\d{2}-\d{2})/$")
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
TOL = 1e-12
WORDS_FORMS = {
    "source_break_account": "Account <k> of <N> has no measured return on <days> in this period, so the household return for this period is not shown.",
    "source_break_household_no_row": "The household has no row on <days> in this period, so the household return for this period is not shown.",
    "insufficient_history": "This household did not exist at the start of this period.",
}


class Reader(object):
    """LIST and GET only. There is deliberately no put, copy or delete method."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.calls = 0

    def list_prefixes(self, bucket, prefix):
        self.calls += 1
        out = []
        for page in self._s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
            for cp in page.get("CommonPrefixes", []):
                out.append(cp["Prefix"])
        return out

    def list_keys(self, bucket, prefix):
        self.calls += 1
        out = []
        for page in self._s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                out.append(obj["Key"])
        return out

    def get(self, bucket, key):
        self.calls += 1
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def split_s3(addr):
    rest = addr[len("s3://"):]
    bucket, _, key = rest.partition("/")
    return bucket, key.rstrip("/")


def one_year_before(d):
    try:
        return d.replace(year=d.year - 1)
    except ValueError:
        return d.replace(year=d.year - 1, day=28)


def start_of(name, R):
    """the window start days of the report contract's document.windows (quarter_to_date, year_to_date, last_12_months)."""
    if name == "qtd":
        return dt.date(R.year, 3 * ((R.month - 1) // 3) + 1, 1)
    if name == "ytd":
        return dt.date(R.year, 1, 1)
    if name == "last_12_months":
        return one_year_before(R)
    raise SystemExit("ERROR: no start rule for window %s" % name)


def main(argv):
    if len(argv) < 2:
        print("usage: dry_run_household_windows_r112.py <repo_root>")
        return 2
    repo = os.path.abspath(argv[1])
    sys.path.insert(0, repo)
    import lib.opal_naming as naming
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    spec = importlib.util.spec_from_file_location("household_return_daily_r112", os.path.join(repo, MODULE_REL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(os.path.join(repo, REGISTRY_REL), "rb") as fh:
        registry = json.loads(fh.read().decode("utf-8"))
    rows_for_firm = [f for f in registry.get("firms", []) if f.get("firm_id") == FIRM_ID]
    if len(rows_for_firm) != 1:
        raise SystemExit("ERROR: the registry does not enumerate exactly one row for the firm")
    firm = rows_for_firm[0]["firm_id"]

    # ADDRESSES: derived by lib/opal_naming.address() from the registry row; no bucket and no prefix typed here
    irpt_b, irpt_k = split_s3(naming.address("irpt", firm, "gold", RET_TABLE, "date=2000-01-01", "x"))
    irpt_root = irpt_k[: irpt_k.index("/" + RET_TABLE + "/") + 1]
    ret_prefix = irpt_root + RET_TABLE + "/"
    xw_b, xw_k = split_s3(naming.address("advi", firm, "gold", XW_TABLE, "date=2000-01-01", "x"))
    xw_prefix = xw_k[: xw_k.index("/" + XW_TABLE + "/") + len("/" + XW_TABLE + "/")]

    reader = Reader()

    # (b) the newest household crosswalk partition
    xw_parts = {}
    for p in reader.list_prefixes(xw_b, xw_prefix):
        m = DATE_RX.search(p)
        if m:
            xw_parts[m.group(1)] = p
    if not xw_parts:
        raise SystemExit("ERROR: no household_crosswalk date= partition under the granted prefix")
    xw_newest = max(xw_parts)
    xw_bytes = reader.get(xw_b, xw_prefix + "date=" + xw_newest + "/" + XW_FILE)
    xw_rows = pq.read_table(io.BytesIO(xw_bytes), columns=["schwab_account_number", "opal_relationship_id"]).to_pylist()
    acct_to_opal = {}
    groups = {}
    null_pairs = 0
    for r in xw_rows:
        opal = r.get("opal_relationship_id")
        acct = r.get("schwab_account_number")
        if opal is None or acct is None or str(opal).strip() == "" or str(acct).strip() == "":
            null_pairs += 1
            continue
        opal, acct = str(opal), str(acct)
        acct_to_opal.setdefault(acct, set()).add(opal)
        groups.setdefault(opal, set()).add(acct)
    conflicts = sum(1 for a, os_ in acct_to_opal.items() if len(os_) > 1)
    print("CROSSWALK: newest date span %s, rows %d, rows without an account or relationship id %d, accounts in more than one relationship %d"
          % (xw_newest, len(xw_rows), null_pairs, conflicts))
    if conflicts:
        raise SystemExit("STOP: an account maps to more than one household; a surprise row is owed, the method is not adjusted here")

    # (a) the account gold date= partitions dated on or before as_of
    part_map = {}
    for p in reader.list_prefixes(irpt_b, ret_prefix):
        m = DATE_RX.search(p)
        if m:
            part_map[m.group(1)] = p
    listed = len(part_map)
    dates_read = sorted(d for d in part_map if d <= AS_OF)
    print("PARTITIONS LISTED (account_return_daily, date= prefixes): %d; dated on or before as_of: %d; later than as_of, not read: %d"
          % (listed, len(dates_read), listed - len(dates_read)))
    if not dates_read:
        raise SystemExit("ERROR: no date= partition on or before as_of under the granted account gold prefix")
    if len(dates_read) > MAX_PARTITIONS:
        raise SystemExit("STOP: more than %d partitions on or before as_of; a partial read is not the table; no run" % MAX_PARTITIONS)

    wanted = set(acct_to_opal)
    kept = []
    seen_accounts = set()
    seen_pairs = set()
    dup_pairs = 0
    null_values = 0
    empty_partitions = 0
    for d in dates_read:
        keys = [k for k in reader.list_keys(irpt_b, part_map[d].rstrip("/") + "/") if k.endswith(".parquet")]
        if not keys:
            empty_partitions += 1
        for k in sorted(keys):
            tbl = pq.read_table(io.BytesIO(reader.get(irpt_b, k)),
                                columns=["account_id", "business_date", "market_value_eod", "external_flow", "total_return_daily"])
            tbl = tbl.filter(pc.is_in(tbl["account_id"], value_set=pa.array(sorted(wanted), type=tbl.schema.field("account_id").type)))
            for r in tbl.to_pylist():
                acct = r["account_id"]
                if acct is None or str(acct) not in wanted:
                    continue
                acct = str(acct)
                key = (acct, r["business_date"])
                if key in seen_pairs:
                    dup_pairs += 1
                seen_pairs.add(key)
                if r["market_value_eod"] is None or r["external_flow"] is None:
                    null_values += 1
                    continue
                seen_accounts.add(acct)
                kept.append({"account_id": acct, "business_date": str(r["business_date"]),
                             "market_value_eod": float(r["market_value_eod"]), "external_flow": float(r["external_flow"]),
                             "total_return_daily": None if r["total_return_daily"] is None else float(r["total_return_daily"])})
    print("GOLD: partitions read %d, empty partitions %d, rows kept %d, duplicate account-day rows %d, null value rows %d"
          % (len(dates_read), empty_partitions, len(kept), dup_pairs, null_values))
    if dup_pairs or null_values:
        raise SystemExit("STOP: duplicate account-day rows or null values in the gold; a surprise row is owed")

    membership = {}
    households = {}
    dropped = 0
    for opal, accts in groups.items():
        members = sorted(a for a in accts if a in seen_accounts)
        if not members:
            dropped += 1
            continue
        households[opal] = members
        for a in members:
            membership[a] = opal
    print("HOUSEHOLDS: kept %d, dropped (no account in the gold) %d" % (len(households), dropped))

    table = mod.compute_household_returns(kept, membership)
    table_dates = sorted({r["business_date"] for r in table})
    print("TABLE: rows %d, distinct dates %d, last date equals as_of: %s" % (len(table), len(table_dates), table_dates[-1] == AS_OF))
    if table_dates[-1] != AS_OF:
        raise SystemExit("STOP: the table does not end on as_of; no run")

    # THE TIE-OUT against round 111's private table (read only), row for row on household, date, quality and return
    old = pq.read_table(ROUND111_TABLE, columns=["household_id", "business_date", "total_return_daily", "day_quality"]).to_pylist()
    old_map = {(r["household_id"], r["business_date"]): (r["day_quality"], r["total_return_daily"]) for r in old}
    new_map = {(r["household_id"], r["business_date"]): (r["day_quality"], r["total_return_daily"]) for r in table}
    differing = 0
    for key in set(old_map) | set(new_map):
        if key not in old_map or key not in new_map:
            differing += 1
            continue
        qo, ro = old_map[key]
        qn, rn = new_map[key]
        if qo != qn or (ro is None) != (rn is None) or (ro is not None and abs(ro - rn) > TOL):
            differing += 1
    print("TIE-OUT vs round 111: rows now %d, rows in round 111 %d, differing or missing %d" % (len(new_map), len(old_map), differing))
    if differing:
        raise SystemExit("STOP: the table differs from round 111's private table (%d rows); the checker's recount reads round 111's table; BLOCKING, no window run" % differing)

    # THE WINDOWS
    table_days = sorted({r["business_date"] for r in table})
    R = dt.date.fromisoformat(AS_OF)
    rows_by_household = {}
    for r in kept:
        h = membership.get(r["account_id"])
        if h is not None:
            rows_by_household.setdefault(h, []).append(r)
    n_table_households = len({r["household_id"] for r in table})
    if n_table_households != len(households):
        raise SystemExit("STOP: the table holds %d households, the membership %d" % (n_table_households, len(households)))

    tally = {w: {"households_total": 0, "figure": 0, "source_break_account": 0, "source_break_household_no_row": 0, "insufficient_history": 0}
             for w in WINDOWS}
    private_rows = {"household_id": [], "window": [], "class": [], "figure": [], "words": []}
    for h in sorted(households):
        hrows = rows_by_household.get(h, [])
        hmem = {a: h for a in households[h]}
        for w in WINDOWS:
            if w == "since_inception":
                anchor = None
            else:
                S = start_of(w, R).isoformat()
                before = [x for x in table_days if x < S]
                if not before:
                    raise SystemExit("STOP: no table date before the start of window %s" % w)
                anchor = before[-1]
            res = mod.household_window_result(hrows, hmem, h, anchor, AS_OF, table_days)
            absent = res["absent"]
            if absent is None:
                assert res["figure"] is not None
                cls = "figure"
                words = None
            elif absent["kind"] == "INSUFFICIENT_HISTORY":
                assert res["figure"] is None
                cls = "insufficient_history"
                words = absent["absent"]
            else:
                assert res["figure"] is None and absent["kind"] == "SOURCE_BREAK"
                if res["unmeasured"]:
                    cls = "source_break_account"
                else:
                    cls = "source_break_household_no_row"
                words = absent["absent"]
            t = tally[w]
            t["households_total"] += 1
            t[{"figure": "figure", "insufficient_history": "insufficient_history",
               "source_break_account": "source_break_account",
               "source_break_household_no_row": "source_break_household_no_row"}[cls]] += 1
            private_rows["household_id"].append(h)
            private_rows["window"].append(w)
            private_rows["class"].append(cls)
            private_rows["figure"].append(None if res["figure"] is None else float(res["figure"]))
            private_rows["words"].append(words)

    for w in WINDOWS:
        t = tally[w]
        print("WINDOW %s: households %d, figure %d, source_break account %d, source_break household no row %d, insufficient history %d"
              % (w, t["households_total"], t["figure"], t["source_break_account"], t["source_break_household_no_row"], t["insufficient_history"]))

    # THE PRIVATE PARQUET (never AWS)
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    private_path = os.path.join(PRIVATE_DIR, PRIVATE_NAME)
    pq.write_table(pa.table({"household_id": pa.array(private_rows["household_id"], type=pa.string()),
                             "window": pa.array(private_rows["window"], type=pa.string()),
                             "class": pa.array(private_rows["class"], type=pa.string()),
                             "figure": pa.array(private_rows["figure"], type=pa.float64()),
                             "words": pa.array(private_rows["words"], type=pa.string())}), private_path)
    with open(private_path, "rb") as fh:
        private_sha = hashlib.sha256(fh.read()).hexdigest()
    print("PRIVATE parquet written: rows %d, sha256 %s" % (len(private_rows["household_id"]), private_sha))

    with open(__file__, "rb") as fh:
        driver_sha = hashlib.sha256(fh.read()).hexdigest()
    windows = {}
    for w in WINDOWS:
        t = tally[w]
        sb = t["source_break_account"] + t["source_break_household_no_row"]
        windows[w] = {
            "households_total": t["households_total"], "figure": t["figure"], "source_break": sb,
            "source_break_account": t["source_break_account"], "source_break_household_no_row": t["source_break_household_no_row"],
            "insufficient_history": t["insufficient_history"],
            "claim": "inferred" if w == "since_inception" else "measured",
        }
    windows["since_inception"]["note"] = ("the since-inception window opens on each household's first row date in the data this read reaches "
                                          "(the read reaches back only to the earliest partition read), so its claim is inferred")
    rec = {
        "as_of": AS_OF,
        "windows": windows,
        "words_forms": WORDS_FORMS,
        "table_matches_round111": differing == 0,
        "table_rows_differing": differing,
        "reads": {"s3_reads": reader.calls, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "driver": {"file": DRIVER_REL, "sha256": driver_sha, "tracked": True},
        "files_in_repo": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    with open(os.path.join(repo, REC_REL), "w", encoding="ascii", newline="\n") as fh:
        fh.write(json.dumps(rec, indent=2, sort_keys=True) + "\n")
    print("RECORD written: %s" % REC_REL)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
