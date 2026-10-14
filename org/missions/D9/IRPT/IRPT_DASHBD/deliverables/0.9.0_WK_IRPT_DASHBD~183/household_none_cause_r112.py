"""IRPT_DASHBD round 112, cell DB-b-228 (worker 0.9.0_WK_IRPT_DASHBD~183) -- the household-None cause read.

READ-ONLY. Reads: the private round-111 household table; the newest household_crosswalk partition (one GET);
every date= partition (newest 900) of the 49 Financial account_return_daily gold, by LIST and GET only.
The addresses come from lib/opal_naming.address() on the firm's registry row. Writes: one private JSON under
C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~183/ and nothing else.
Prints counts, dates and words only: no household or account identifier is printed or stored.

Usage: python -I household_none_cause_r112.py <repo_root>
"""
import collections
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
from pathlib import Path

FIRM_ID = "49financial"
REGISTRY_REL = "data/firm_registry.json"
RET_TABLE = "account_return_daily"
XW_TABLE = "household_crosswalk"
XW_FILE = "household_crosswalk.parquet"
MAX_PARTITIONS = 900
DATE_RX = re.compile(r"date=(\d{4}-\d{2}-\d{2})/$")
TABLE = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~179/household_return_daily.parquet"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~183"
PRIVATE_NAME = "measurements_r112.json"
ANALYSIS_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~183/household_none_cause_r112.py"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
KINDS = ("account_closed_before_as_of", "account_null_return", "account_row_missing_inside_life", "household_no_row")
MEAS, AM, NPV = "MEASURED", "ACCOUNT_MISSING", "NO_PRIOR_VALUE"
NO_ROW = "NO_ROW"
GOLD_COLUMNS = ["account_id", "business_date", "market_value_eod", "external_flow", "total_return_daily",
                "day_quality", "return_basis", "guard_state"]


class Reader(object):
    """LIST and GET only. There is deliberately no method that changes a remote object."""

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


def window_start(name, a):
    if name == "qtd":
        return dt.date(a.year, 3 * ((a.month - 1) // 3) + 1, 1)
    if name == "ytd":
        return dt.date(a.year, 1, 1)
    if name == "last_12_months":
        return one_year_before(a)
    raise SystemExit("ERROR: no start rule for window %s" % name)


def pair_kind(acct_rows, acct_last, a, d):
    """the cause of one unmeasured account-day, by the order's precedence applied to the pair: (1) no row after d."""
    if acct_last[a] <= d:
        return KINDS[0]
    row = acct_rows[a].get(d)
    if row is None:
        return KINDS[2]
    if row[1]:
        return KINDS[1]
    raise RuntimeError("an unmeasured pair whose account row is measured")


def rebuild(members, acct_rows, acct_last):
    """the household daily table, rebuilt as the round-111 module does it (household_return_daily.compute_household_returns):
    per household, the dates on which any member has a row; ACCOUNT_MISSING when an account with a row on the previous
    household date has no row on the day or a null total_return_daily; the named accounts are kept per ACCOUNT_MISSING day."""
    out = {}
    for h, mem in members.items():
        dates = sorted({d for a in mem for d in acct_rows.get(a, {})})
        qual, named = {}, {}
        prev = None
        for t in dates:
            cur = {a: acct_rows[a][t] for a in mem if t in acct_rows.get(a, {})}
            if prev is None:
                qual[t] = NPV
            else:
                before = [a for a in mem if prev in acct_rows.get(a, {})]
                miss = [a for a in before if a not in cur or cur[a][1]]
                if miss:
                    qual[t] = AM
                    named[t] = [(a, pair_kind(acct_rows, acct_last, a, t)) for a in miss]
                else:
                    base = sum(acct_rows[a][prev][2] for a in before)
                    qual[t] = MEAS if base > 0 else NPV
            prev = t
        out[h] = (dates, qual, named)
    return out


def window_result(dates, qual, named, days, anchor, as_of):
    """the window rule for one household (the checker's recount): insufficient, a figure, a SOURCE_BREAK by account
    (first cause by precedence), or a SOURCE_BREAK by household no-row. `events` are the dates on which the household
    has an ACCOUNT_MISSING day or no row inside the window."""
    first = dates[0]
    if anchor is not None and first > anchor:
        return {"status": "insufficient", "events": set()}
    lo = anchor if anchor is not None else first
    dset = set(dates)
    in_w = [d for d in dates if lo < d <= as_of]
    odd = [d for d in in_w if qual[d] not in (MEAS, AM)]
    if odd:
        raise RuntimeError("a window day carries a quality outside MEASURED and ACCOUNT_MISSING")
    am_days = [d for d in in_w if qual[d] == AM]
    no_row_days = [d for d in days if lo < d <= as_of and d not in dset]
    events = set(am_days) | set(no_row_days)
    if am_days:
        kinds = [k for d in am_days for (_a, k) in named[d]]
        kind = next(k for k in KINDS if k in kinds)
        return {"status": "sb_account", "kind": kind, "events": events}
    if no_row_days:
        return {"status": "sb_no_row", "kind": KINDS[3], "events": events}
    return {"status": "figure", "events": set()}


def positive_control():
    """a synthetic week, two accounts per household: H-A's account B is closed from day 4 on (no row after it);
    H-B's account C has a null total_return_daily on day 2 (NOT_MEASURABLE) and later rows; H-C is measured throughout."""
    d = ["2026-01-05", "2026-01-06", "2026-01-07", "2026-01-08", "2026-01-09"]
    rows = {}

    def put(a, i, ret=0.001, dq=MEAS):
        rows.setdefault(a, {})[d[i]] = (dq, ret is None, 100.0, "TWR", "HOLD")

    for i in range(5):
        put("A", i)
    for i in range(3):
        put("B", i)
    for i in range(5):
        put("C", i, ret=None if i == 1 else 0.001, dq="NOT_MEASURABLE" if i == 1 else MEAS)
        put("D", i)
        put("E", i)
        put("F", i)
    acct_last = {a: max(v) for a, v in rows.items()}
    members = {"H-A": ["A", "B"], "H-B": ["C", "D"], "H-C": ["E", "F"]}
    rb = rebuild(members, rows, acct_last)
    got = {}
    for h, (dates, qual, named) in rb.items():
        res = window_result(dates, qual, named, d, None, d[-1])
        got[h] = res.get("kind", res["status"])
    counted = sum(1 for h in got if got[h] not in ("figure", "insufficient"))
    expected = {"H-A": KINDS[0], "H-B": KINDS[1], "H-C": "figure"}
    passed = got == expected and counted == 2
    return {"description": "synthetic week of five days, three households of two synthetic accounts each: H-A has an account closed from day 4 on, H-B an account with a null total_return_daily on day 2, H-C is measured throughout",
            "expected": "H-A account_closed_before_as_of; H-B account_null_return; H-C figure (not counted); households_none 2 of 3",
            "observed": "; ".join("%s %s" % (h, got[h]) for h in sorted(got)) + "; households_none %d of %d" % (counted, len(got)),
            "passed": bool(passed)}


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    pc_res = positive_control()
    print("POSITIVE CONTROL: passed=%s observed=[%s]" % (pc_res["passed"], pc_res["observed"]))
    if not pc_res["passed"]:
        raise SystemExit("STOP: the positive control failed; the classification is not trusted")
    sys.path.insert(0, repo)
    import lib.opal_naming as naming
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    with open(os.path.join(repo, REGISTRY_REL), "rb") as fh:
        registry = json.loads(fh.read().decode("utf-8"))
    rows_for_firm = [f for f in registry.get("firms", []) if f.get("firm_id") == FIRM_ID]
    if len(rows_for_firm) != 1:
        raise SystemExit("ERROR: the registry does not enumerate exactly one row for the firm")
    firm = rows_for_firm[0]["firm_id"]
    irpt_b, irpt_k = split_s3(naming.address("irpt", firm, "gold", RET_TABLE, "date=2000-01-01", "x"))
    irpt_root = irpt_k[: irpt_k.index("/" + RET_TABLE + "/") + 1]
    ret_prefix = irpt_root + RET_TABLE + "/"
    xw_b, xw_k = split_s3(naming.address("advi", firm, "gold", XW_TABLE, "date=2000-01-01", "x"))
    xw_prefix = xw_k[: xw_k.index("/" + XW_TABLE + "/") + len("/" + XW_TABLE + "/")]

    # the private round-111 table (read-only)
    tt = pq.read_table(TABLE, columns=["household_id", "business_date", "total_return_daily", "day_quality"]).to_pydict()
    priv = {}
    for h, d, r, q in zip(tt["household_id"], tt["business_date"], tt["total_return_daily"], tt["day_quality"]):
        priv.setdefault(h, {})[d] = (sys.intern(str(q)), r is None)
    days = sorted({d for d in tt["business_date"]})
    as_of = days[-1]
    print("PRIVATE TABLE: rows %d, households %d, dates %d, as_of %s, quality counts %s"
          % (len(tt["household_id"]), len(priv), len(days), as_of, dict(collections.Counter(tt["day_quality"]))))
    del tt

    reader = Reader()
    # (b) the newest household crosswalk partition
    xw_parts = {}
    for p in reader.list_prefixes(xw_b, xw_prefix):
        m = DATE_RX.search(p)
        if m:
            xw_parts[m.group(1)] = p
    if not xw_parts:
        raise SystemExit("ERROR: no household_crosswalk date= partition under the derived prefix")
    xw_newest = max(xw_parts)
    xw_bytes = reader.get(xw_b, xw_prefix + "date=" + xw_newest + "/" + XW_FILE)
    xw_rows = pq.read_table(io.BytesIO(xw_bytes), columns=["schwab_account_number", "opal_relationship_id"]).to_pylist()
    acct_to_opal, groups, null_pairs = {}, {}, 0
    for r in xw_rows:
        opal, acct = r.get("opal_relationship_id"), r.get("schwab_account_number")
        if opal is None or acct is None or str(opal).strip() == "" or str(acct).strip() == "":
            null_pairs += 1
            continue
        opal, acct = str(opal), str(acct)
        acct_to_opal.setdefault(acct, set()).add(opal)
        groups.setdefault(opal, set()).add(acct)
    conflicts = sum(1 for v in acct_to_opal.values() if len(v) > 1)
    print("CROSSWALK: newest date span %s, rows %d, rows without an id %d, accounts in more than one relationship %d"
          % (xw_newest, len(xw_rows), null_pairs, conflicts))
    if conflicts:
        raise SystemExit("STOP: an account maps to more than one household; a surprise row is owed")

    # (a) the account gold: LIST first, then every object of the newest 900 partitions
    part_map = {}
    for p in reader.list_prefixes(irpt_b, ret_prefix):
        m = DATE_RX.search(p)
        if m:
            part_map[m.group(1)] = p
    listed = len(part_map)
    print("PARTITIONS LISTED (account_return_daily, date= prefixes): %d" % listed)
    if listed == 0:
        raise SystemExit("ERROR: no date= partition under the derived account gold prefix")
    dates_read = sorted(part_map)[-MAX_PARTITIONS:]
    print("PARTITIONS READ: %d (newest %d)" % (len(dates_read), MAX_PARTITIONS))
    wanted = sorted(acct_to_opal)
    wanted_type = None
    acct_rows, acct_last = {}, {}
    dup_pairs = null_values = empty_partitions = 0
    for d in dates_read:
        keys = sorted(k for k in reader.list_keys(irpt_b, part_map[d].rstrip("/") + "/") if k.endswith(".parquet"))
        if not keys:
            empty_partitions += 1
        for k in keys:
            tbl = pq.read_table(io.BytesIO(reader.get(irpt_b, k)), columns=GOLD_COLUMNS)
            if wanted_type is None:
                wanted_type = tbl.schema.field("account_id").type
            tbl = tbl.filter(pc.is_in(tbl["account_id"], value_set=pa.array(wanted, type=wanted_type)))
            for r in tbl.to_pylist():
                a = r["account_id"]
                if a is None or str(a) not in acct_to_opal:
                    continue
                a = str(a)
                bd = str(r["business_date"])
                rowd = acct_rows.setdefault(a, {})
                if bd in rowd:
                    dup_pairs += 1
                    continue
                if r["market_value_eod"] is None or r["external_flow"] is None:
                    null_values += 1
                    continue
                rowd[bd] = (sys.intern(str(r["day_quality"])), r["total_return_daily"] is None,
                            float(r["market_value_eod"]), sys.intern(str(r["return_basis"])), sys.intern(str(r["guard_state"])))
                if bd > acct_last.get(a, ""):
                    acct_last[a] = bd
    print("GOLD: partitions read %d, empty partitions %d, account rows kept %d, duplicate account-day rows %d, null value rows %d, accounts with rows %d"
          % (len(dates_read), empty_partitions, sum(len(v) for v in acct_rows.values()), dup_pairs, null_values, len(acct_rows)))
    if dup_pairs or null_values:
        raise SystemExit("STOP: duplicate account-day rows or null values in the gold; a surprise row is owed")

    # membership, as the round-111 driver: the crosswalk households with the accounts present in the gold
    members, dropped = {}, 0
    for opal, accts in groups.items():
        mem = sorted(a for a in accts if a in acct_rows)
        if not mem:
            dropped += 1
            continue
        members[opal] = mem
    accounts_total = sum(len(v) for v in members.values())
    print("HOUSEHOLDS: rebuilt %d, dropped (no account in the gold) %d, member accounts %d, multi-account %d"
          % (len(members), dropped, accounts_total, sum(1 for v in members.values() if len(v) >= 2)))

    rb = rebuild(members, acct_rows, acct_last)

    # cross-check: the rebuilt daily table equals the private table, household by household, day by day
    hh_set_equal = set(rb) == set(priv)
    mismatch = 0
    for h, (dates, qual, _named) in rb.items():
        p = priv.get(h)
        if p is None or sorted(p) != dates:
            mismatch += 1
            continue
        for d in dates:
            q, isnull = p[d]
            if q != qual[d] or isnull != (qual[d] != MEAS):
                mismatch += 1
    print("REBUILD CHECK: households equal %s; household-day mismatches against the private table %d" % (hh_set_equal, mismatch))
    if mismatch or not hh_set_equal:
        raise SystemExit("STOP: the rebuilt daily table differs from the private table; the memberships are misread")

    # the windows (the checker's rule: anchor = last table date strictly before the start; household first after anchor = INSUFFICIENT_HISTORY)
    a_date = dt.date.fromisoformat(as_of)
    windows, events_by_window, nlist = {}, {}, {}
    for w in WINDOWS:
        if w == "since_inception":
            anchor = None
        else:
            start = window_start(w, a_date).isoformat()
            before = [x for x in days if x < start]
            anchor = before[-1] if before else "0000-00-00"
        cnt = collections.Counter()
        by_kind = collections.Counter()
        ev = collections.Counter()
        none_hh = []
        for h, (dates, qual, named) in rb.items():
            res = window_result(dates, qual, named, days, anchor, as_of)
            cnt[res["status"]] += 1
            if res["status"] in ("sb_account", "sb_no_row"):
                by_kind[res["kind"]] += 1
                none_hh.append(h)
                for d in res["events"]:
                    ev[d] += 1
        windows[w] = {"households_none": sum(by_kind.values()), "by_kind": {k: by_kind.get(k, 0) for k in KINDS},
                      "status_counts": dict(cnt), "anchor": anchor, "claim": "measured"}
        events_by_window[w] = ev
        nlist[w] = len(none_hh)
        print("WINDOW %s: anchor %s, households_none %d, by_kind %s, status %s"
              % (w, anchor, sum(by_kind.values()), {k: by_kind.get(k, 0) for k in KINDS}, dict(cnt)))

    # the top dates per window (the dates with the most affected NONE households)
    for w in WINDOWS:
        top = sorted(events_by_window[w].items(), key=lambda kv: (-kv[1], kv[0]))[:10]
        windows[w]["top_dates"] = [{"date": d, "households_affected": int(c)} for d, c in top]
        print("TOP DATES %s: %s" % (w, ", ".join("%s=%d" % (d, c) for d, c in top[:3])))

    # the unmeasured account-days of every ACCOUNT_MISSING household day of the table
    total_pairs = 0
    by_dq = collections.Counter()
    kind_pairs = collections.Counter()
    pair_dq_kind = collections.Counter()
    basis_c = collections.Counter()
    guard_c = collections.Counter()
    partition_absent = 0
    for h, (dates, qual, named) in rb.items():
        for d, lst in named.items():
            if d not in part_map:
                partition_absent += len(lst)
            for a, k in lst:
                total_pairs += 1
                row = acct_rows[a].get(d)
                dq = row[0] if row is not None else NO_ROW
                by_dq[dq] += 1
                kind_pairs[k] += 1
                pair_dq_kind[(k, dq)] += 1
                if row is not None:
                    basis_c[row[3]] += 1
                    guard_c[row[4]] += 1
    am_days_total = sum(1 for h in rb for d in rb[h][2])
    print("UNMEASURED ACCOUNT-DAYS: total %d over %d ACCOUNT_MISSING household days; by day_quality %s; by kind %s"
          % (total_pairs, am_days_total, dict(by_dq), {k: kind_pairs.get(k, 0) for k in KINDS}))
    print("  pairs whose gold partition for the day is absent: %d; return_basis of the rows %s; guard_state of the rows %s"
          % (partition_absent, dict(basis_c), dict(guard_c)))

    # the household-days with no member row on a table date after the household's first date
    hh_norow = 0
    for h, (dates, qual, named) in rb.items():
        dset = set(dates)
        hh_norow += sum(1 for d in days if d > dates[0] and d not in dset)
    print("HOUSEHOLD NO-ROW DAYS (table dates after the first date with no member row): %d" % hh_norow)

    causes = []
    causes.append({"cause": "an account has no row on the unmeasured day and no row after it, so its gold rows stop before as_of (closed, or the producer stopped writing; the gold alone cannot tell the two apart)",
                   "producer": PRODUCER, "count": kind_pairs.get(KINDS[0], 0), "claim": "inferred"})
    for dq in sorted({x for (k, x) in pair_dq_kind if k == KINDS[1]}):
        causes.append({"cause": "an account row on the unmeasured day carries a null total_return_daily with day_quality %s and later rows exist (the producer marks the day not served)" % dq,
                       "producer": PRODUCER, "count": pair_dq_kind[(KINDS[1], dq)], "claim": "measured"})
    causes.append({"cause": "an account has no row on the unmeasured day but has rows after it (a gap inside its life; the gold carries no reason for the missing row)",
                   "producer": PRODUCER, "count": kind_pairs.get(KINDS[2], 0), "claim": "inferred"})
    causes.append({"cause": "household-days with no member account row on a table date after the household's first date (every member absent; counts household-days, not account-days)",
                   "producer": PRODUCER, "count": hh_norow, "claim": "inferred"})

    private = {
        "as_of": as_of, "windows": {w: {k: v for k, v in windows[w].items() if k != "status_counts" and k != "anchor"} for w in WINDOWS},
        "unmeasured_account_days": {"total": total_pairs, "by_day_quality": dict(by_dq), "claim": "measured"},
        "cause_by_source": causes,
        "denominator": {"households": len(priv), "accounts": accounts_total, "partitions_read": len(dates_read),
                        "scope_words": "the %d households of the private round-111 table over %d table dates; the accounts are the member accounts of those households present in the newest %d gold partitions of the firm"
                                       % (len(priv), len(days), MAX_PARTITIONS)},
        "positive_control": pc_res,
        "reads": {"s3_reads": reader.calls, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False,
    }
    sha = hashlib.sha256(Path(os.path.abspath(__file__)).read_bytes()).hexdigest()
    private["analysis"] = {"file": ANALYSIS_REL, "sha256": sha, "tracked": True}
    private["windows_detail"] = {w: {"anchor": windows[w]["anchor"], "status_counts": windows[w]["status_counts"]} for w in WINDOWS}
    private["rebuild_check"] = {"households_equal": hh_set_equal, "mismatch": mismatch}
    private["partitions_listed"] = listed
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    out_path = os.path.join(PRIVATE_DIR, PRIVATE_NAME)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(private, indent=2, sort_keys=True) + "\n")
    print("PRIVATE RECORD WRITTEN: %s (sha256 %s)" % (out_path, sha))
    print("ANALYSIS SHA256 %s" % sha)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
