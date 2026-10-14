"""IRPT_DASHBD round 111, cell DB-b-224 (worker 0.9.0_WK_IRPT_DASHBD~179): the PRIVATE dry run of the household daily
return for one firm, and the range tie-out against the account windows.

Usage: python -I dry_run_household_return_r111.py <repo_root> [--list-only]

READS (S3 LIST and GET only): (a) the date= partitions of the firm's irpt account_return_daily gold (the newest 900 when
there are more; every object of each partition read); (b) the newest date= partition of the firm's ADVI household_crosswalk
(one GET of its household_crosswalk.parquet). Both addresses come from lib/opal_naming.address() on the firm's registry row.
WRITES: one private parquet in the private evidence folder, and HOUSEHOLD_TIEOUT_R111.json in this folder (counts and words).
No S3 write, no vendor call, no secret read.
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
REGISTRY_REL = "data/firm_registry.json"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/household_return_daily.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_HOUSEHOLD_RETURN_DAILY_CONTRACT.json"
DELIVER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~179"
DRIVER_REL = DELIVER_REL + "/dry_run_household_return_r111.py"
REC_REL = DELIVER_REL + "/HOUSEHOLD_TIEOUT_R111.json"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~179"
PRIVATE_NAME = "household_return_daily.parquet"
RET_TABLE = "account_return_daily"
XW_TABLE = "household_crosswalk"
XW_FILE = "household_crosswalk.parquet"
MAX_PARTITIONS = 900
DATE_RX = re.compile(r"date=(\d{4}-\d{2}-\d{2})/$")
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
BINS = ("lt_5bp", "5_25bp", "25_100bp", "ge_100bp")
TOL = 1e-9
REASONS = ("household_return_none", "no_account_complete")


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
    if name == "qtd":
        return dt.date(R.year, 3 * ((R.month - 1) // 3) + 1, 1)
    if name == "ytd":
        return dt.date(R.year, 1, 1)
    if name == "last_12_months":
        return one_year_before(R)
    raise SystemExit("ERROR: no start rule for window %s" % name)


def household_cum(dates, rmap, days, anchor):
    """Product of (1 + r_t) over days, minus one. None when the anchor or any day has no row, or any r_t is null, or no day."""
    if not days or anchor not in dates:
        return None
    prod = 1.0
    for d in days:
        if d not in dates:
            return None
        r = rmap[d]
        if r is None:
            return None
        prod *= 1.0 + r
    return prod - 1.0


def account_cum(amap, days):
    if not days:
        return None
    prod = 1.0
    for d in days:
        v = amap.get(d)
        if v is None:
            return None
        prod *= 1.0 + v
    return prod - 1.0


def bin_of(gap):
    bp = gap * 10000.0
    if bp < 5:
        return "lt_5bp"
    if bp < 25:
        return "5_25bp"
    if bp < 100:
        return "25_100bp"
    return "ge_100bp"


def main(argv):
    if len(argv) < 2:
        print("usage: dry_run_household_return_r111.py <repo_root> [--list-only]")
        return 2
    repo = os.path.abspath(argv[1])
    list_only = "--list-only" in argv[2:]
    sys.path.insert(0, repo)
    import lib.opal_naming as naming
    from lib import trading_calendar as tc
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    spec = importlib.util.spec_from_file_location("household_return_daily_dry", os.path.join(repo, MODULE_REL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(os.path.join(repo, CONTRACT_REL), "rb") as fh:
        contract = json.loads(fh.read().decode("utf-8"))
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

    # (b) the newest household crosswalk partition, then the account gold partitions
    xw_parts = {}
    for p in reader.list_prefixes(xw_b, xw_prefix):
        m = DATE_RX.search(p)
        if m:
            xw_parts[m.group(1)] = p
    if not xw_parts:
        raise SystemExit("ERROR: no household_crosswalk date= partition under the granted prefix")
    xw_newest = max(xw_parts)
    xw_bytes = reader.get(xw_b, xw_prefix + "date=" + xw_newest + "/" + XW_FILE)
    import pyarrow.parquet as pq2
    xw_rows = pq2.read_table(io.BytesIO(xw_bytes), columns=["schwab_account_number", "opal_relationship_id"]).to_pylist()

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

    part_map = {}
    for p in reader.list_prefixes(irpt_b, ret_prefix):
        m = DATE_RX.search(p)
        if m:
            part_map[m.group(1)] = p
    listed = len(part_map)
    print("PARTITIONS LISTED (account_return_daily, date= prefixes): %d" % listed)
    if listed == 0:
        raise SystemExit("ERROR: no date= partition under the granted account gold prefix")
    dates_read = sorted(part_map)
    if listed > MAX_PARTITIONS:
        dates_read = dates_read[-MAX_PARTITIONS:]
        print("NOTE: more than %d partitions; reading the newest %d" % (MAX_PARTITIONS, MAX_PARTITIONS))
    if list_only:
        print("LIST-ONLY: stopping before any GET of gold objects")
        return 0

    # (a) every object of every partition read; rows kept only for accounts in the crosswalk (a superset of members)
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

    # membership: the crosswalk households with the accounts present in the gold; a household with none is dropped
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
    total = len(households)
    accounts_total = sum(len(v) for v in households.values())
    multi = sum(1 for v in households.values() if len(v) >= 2)
    print("HOUSEHOLDS: kept %d, dropped (no account in the gold) %d, accounts %d, multi-account %d"
          % (total, dropped, accounts_total, multi))

    table = mod.compute_household_returns(kept, membership)
    table_dates = sorted({r["business_date"] for r in table})
    nontrading = [d for d in table_dates if not tc.is_trading_day(dt.date.fromisoformat(d))]
    print("TABLE: rows %d, dates %s to %s, non-trading dates in the table %d"
          % (len(table), table_dates[0], table_dates[-1], len(nontrading)))

    # THE PRIVATE PARQUET (never AWS)
    schema_version = contract["contract_version"]
    type_of = {"string": pa.string(), "double": pa.float64(), "int64": pa.int64()}
    schema = pa.schema([(n, type_of[t]) for n, t in mod.ARROW_SCHEMA_COLUMNS])
    for r in table:
        r["firm"] = firm
        r["method_version"] = 1
        r["schema_version"] = schema_version
    arrays = [pa.array([r[n] for r in table], type=type_of[t]) for n, t in mod.ARROW_SCHEMA_COLUMNS]
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    private_path = os.path.join(PRIVATE_DIR, PRIVATE_NAME)
    pq.write_table(pa.Table.from_arrays(arrays, schema=schema), private_path)
    with open(private_path, "rb") as fh:
        table_sha = hashlib.sha256(fh.read()).hexdigest()

    # THE RANGE TIE-OUT
    R = dt.date.fromisoformat(table_dates[-1])
    hh_dates, hh_r = {}, {}
    for r in table:
        hh_dates.setdefault(r["household_id"], set()).add(r["business_date"])
        hh_r.setdefault(r["household_id"], {})[r["business_date"]] = r["total_return_daily"]
    acct_ret = {}
    for r in kept:
        if r["account_id"] in membership:
            acct_ret.setdefault(r["account_id"], {})[r["business_date"]] = r["total_return_daily"]

    stats = {w: {"compared": 0, "within": 0, "outside": 0, "bins": {b: 0 for b in BINS},
                 "nc": 0, "reasons": {x: 0 for x in REASONS}} for w in WINDOWS}
    one_hh = set()
    one_max_gap = 0.0
    one_pairs = 0
    one_mismatch = []
    for h in sorted(households):
        dates = hh_dates[h]
        rmap = hh_r[h]
        first = dt.date.fromisoformat(min(dates))
        members = households[h]
        for w in WINDOWS:
            if w == "since_inception":
                anchor = min(dates)
                days = [d.isoformat() for d in tc.trading_days_between(first + dt.timedelta(days=1), R)]
            else:
                S = start_of(w, R)
                anchor = tc.prev_trading_day(S).isoformat()
                days = [d.isoformat() for d in tc.trading_days_between(S, R)]
            hc = household_cum(dates, rmap, days, anchor)
            acum = {a: account_cum(acct_ret.get(a, {}), days) for a in members}
            complete = [v for v in acum.values() if v is not None]
            st = stats[w]
            if hc is None:
                st["nc"] += 1
                st["reasons"]["household_return_none"] += 1
                continue
            if not complete:
                st["nc"] += 1
                st["reasons"]["no_account_complete"] += 1
                continue
            st["compared"] += 1
            lo, hi = min(complete), max(complete)
            if lo - TOL <= hc <= hi + TOL:
                st["within"] += 1
            else:
                gap = (lo - hc) if hc < lo else (hc - hi)
                st["outside"] += 1
                st["bins"][bin_of(gap)] += 1
            if len(members) == 1 and acum[members[0]] is not None:
                one_hh.add(h)
                one_pairs += 1
                one_gap = abs(hc - acum[members[0]])
                one_max_gap = max(one_max_gap, one_gap)
                if one_gap > TOL:
                    one_mismatch.append((h, w))

    for w in WINDOWS:
        st = stats[w]
        print("WINDOW %s: compared %d, within %d, outside %d, bins %s, not comparable %d, reasons %s"
              % (w, st["compared"], st["within"], st["outside"], st["bins"], st["nc"], st["reasons"]))
    print("ONE-ACCOUNT: distinct households compared %d, comparisons %d, max absolute gap %r"
          % (len(one_hh), one_pairs, one_max_gap))
    print("ONE-ACCOUNT MISMATCH: household-window comparisons with a gap above 1e-9: %d, distinct households %d, by window %s"
          % (len(one_mismatch), len({h for h, _w in one_mismatch}),
             {w: sum(1 for _h, x in one_mismatch if x == w) for w in WINDOWS}))

    with open(__file__, "rb") as fh:
        driver_sha = hashlib.sha256(fh.read()).hexdigest()
    rec = {
        "method": {
            "words": ("THE METHOD of household_return_daily (contract 0.1.0, amended on row W179-S1): household daily return r_t is the prior-day-value "
                      "weighted combination of the accounts' own total_return_daily over the accounts with rows on both the previous household date and "
                      "day t (weight = the account's market_value_eod on the previous date); ACCOUNT_MISSING (a missing account or a null account return) "
                      "and NO_PRIOR_VALUE days are null, never zero. A window return is "
                      "the product of (1 + r_t) over the trading days after the window's opening anchor up to and including as_of, minus one; it is null when "
                      "the household has no row on the anchor or on any window day, or any r_t is null. Anchors: the last trading day before the window start "
                      "(qtd, ytd, last_12_months; lib/trading_calendar.py); since_inception opens on the household's first date in the read, so its claim is "
                      "inferred: the read reaches back only to the earliest partition read. An account's window return is the product of (1 + "
                      "total_return_daily) over the same days, complete only with a non-null row on each day. Comparable: household return not null and at "
                      "least one complete member. Range: the minimum and maximum of the complete members' returns; within means inside the range widened by "
                      "1e-9 each side; an outside gap is the distance to the nearer end, binned in basis points. One-account households: the distinct "
                      "households with a window where both the household and the account are complete; max absolute gap over those windows. Reads: LIST of "
                      "the account gold date partitions (newest %d read when more; every object of each read partition read); LIST and one GET of the newest "
                      "crosswalk partition." % MAX_PARTITIONS),
            "claim": "measured",
        },
        "tolerance_assumed": None,
        "households": {"total": total, "accounts_total": accounts_total, "multi_account": multi, "claim": "measured"},
        "windows": {},
        "one_account_households": {"compared": len(one_hh), "max_abs_gap": float(one_max_gap), "claim": "measured"},
        "dry_run": {"first_date": table_dates[0], "last_date": table_dates[-1], "partitions_read": len(dates_read),
                    "table_rows": len(table), "table_sha256": table_sha,
                    "claim": "measured"},
        "reads": {"s3_reads": reader.calls, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "driver": {"file": DRIVER_REL, "sha256": driver_sha, "tracked": True},
        "files_in_repo": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    for w in WINDOWS:
        st = stats[w]
        rec["windows"][w] = {
            "households_compared": st["compared"], "within_range": st["within"], "outside_range": st["outside"],
            "bins": st["bins"], "not_comparable": st["nc"], "not_comparable_reasons": st["reasons"],
            "claim": "inferred" if w == "since_inception" else "measured",
        }
    with open(os.path.join(repo, REC_REL), "w", encoding="ascii", newline="\n") as fh:
        fh.write(json.dumps(rec, indent=2, sort_keys=True) + "\n")
    print("RECORD written: %s" % REC_REL)
    print("PRIVATE parquet: rows %d, sha256 %s" % (len(table), table_sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
