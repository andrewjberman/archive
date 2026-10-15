"""IRPT_DASHBD round 113 (worker 0.9.0_WK_IRPT_DASHBD~184) -- DB-b-229, the NOT_MEASURABLE read.

READ-ONLY. Reads: the private round-111 household table; the newest household_crosswalk partition (one GET);
every date= partition (the newest 900) of the 49 Financial account_return_daily gold, by LIST and GET only;
the shared trading calendar lib/trading_calendar.py; the firm registry row. Addresses come from
lib/opal_naming.address() on the firm's registry row, exactly as household_none_cause_r112.py derives them.
Writes: one private JSON under C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~184/
and the record RD_NOT_MEASURABLE_R113.json in this folder. Nothing else.

Population. The household-sense unmeasured account-days are the round-112 population (every account of an
ACCOUNT_MISSING household day that is missing or null on that day); the total must equal round 112's 56,311.
The per-date rows_not_measurable and their splits are FIRM-WIDE: every account row of the gold partition on
that date with day_quality NOT_MEASURABLE, whatever household (if any) the account belongs to.

Classification (one vocabulary; the producer is data/assets/scripts/gold/irpt_reporting/account_return_daily.py):
  NOT_MEASURABLE row -> LINK_BREAK_BASE_ABSENT (no gold row on the previous trading day, lib calendar),
                        LINK_BREAK_BASE_NONPOSITIVE (that row's market_value_eod not above zero),
                        INELIGIBLE_AFTER_COMPUTE (a base above zero exists yet the row is NOT_MEASURABLE),
                        else OTHER.
  FLOW_UNRECONCILED row -> FLOW_UNRECONCILED:<guard_state>.
  no row -> NO_ROW (input "calendar or position").
  null input, first that applies: price (holdings_price_return_reason HOLDINGS_NOT_OK), position (NO_HOLDINGS_ROW),
  flow (day_quality FLOW_UNRECONCILED), calendar (no previous-day row AND no previous-day gold partition),
  prior_value (no previous-day row although the partition exists, or its market_value_eod not above zero), other.

Usage: python -I <this file> <repo_root>      prints counts, dates and words only (no id, no client value)
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
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~184"
PRIVATE_NAME = "not_measurable_r113.json"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~184/RD_NOT_MEASURABLE_R113.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~184/not_measurable_read_r113.py"
R112_REL = D + "0.9.0_WK_IRPT_DASHBD~183/RD_HOUSEHOLD_NONE_CAUSE_R112.json"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/account_return_daily.py"
DAY = "2026-04-21"
GOLD_COLUMNS = ["account_id", "business_date", "market_value_eod", "external_flow", "total_return_daily",
                "day_quality", "return_basis", "guard_state", "holdings_price_return_reason"]
MEAS, AM, NPV = "MEASURED", "ACCOUNT_MISSING", "NO_PRIOR_VALUE"
DQ_NM, DQ_FLOW = "NOT_MEASURABLE", "FLOW_UNRECONCILED"
HPR_NOT_OK, HPR_NO_ROW = "HOLDINGS_NOT_OK", "NO_HOLDINGS_ROW"
GUARDS = ("GRADED_AGREED", "GRADED_DISAGREED", "NOT_GRADED_OUTSIDE_DOMAIN", "NOT_GRADED_NO_NEIGHBOUR", "GUARD_NOT_REACHED")
NM_CODES = ("LINK_BREAK_BASE_ABSENT", "LINK_BREAK_BASE_NONPOSITIVE", "INELIGIBLE_AFTER_COMPUTE", "OTHER")
FLOW_CODES = tuple("FLOW_UNRECONCILED:" + g for g in GUARDS)
ALL_CODES = NM_CODES + ("NO_ROW",) + FLOW_CODES
INPUTS = ("price", "position", "flow", "calendar", "prior_value", "other")
NO_ROW_CAUSE_INPUT = "calendar or position"
EXPECTED_TOTAL = 56311
LONG_DIGITS = re.compile(r"\d{8,}")
# row layout: (day_quality, total_return_daily is null, market_value_eod, return_basis, guard_state, holdings_price_return_reason)
DQ, ISNULL, MV, BASIS, GUARD, HPR = 0, 1, 2, 3, 4, 5


class Stop(Exception):
    pass


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


def classify(row, prev_row, prev_partition_present):
    """One account-day -> (cause code, null input). row / prev_row: layout tuples or None."""
    if row is None:
        return "NO_ROW", NO_ROW_CAUSE_INPUT
    dq, hpr, guard = row[DQ], row[HPR], row[GUARD]
    if dq == DQ_FLOW:
        code, base_input = "FLOW_UNRECONCILED:" + str(guard), "flow"
    elif dq == DQ_NM:
        if prev_row is None:
            code = "LINK_BREAK_BASE_ABSENT"
            base_input = "prior_value" if prev_partition_present else "calendar"
        elif prev_row[MV] is None or not prev_row[MV] > 0:
            code, base_input = "LINK_BREAK_BASE_NONPOSITIVE", "prior_value"
        else:
            code, base_input = "INELIGIBLE_AFTER_COMPUTE", "other"
    else:
        return "UNCLASSIFIED:" + str(dq), "other"
    if hpr == HPR_NOT_OK:
        return code, "price"
    if hpr == HPR_NO_ROW:
        return code, "position"
    if dq == DQ_FLOW:
        return code, "flow"
    return code, base_input


def positive_control():
    """Synthetic account-days, one per branch; the classifier above must land each in its code and input."""
    nm = (DQ_NM, True, 50.0, "NOT_MEASURABLE", "GUARD_NOT_REACHED", None)
    nm_bad_hpr = (DQ_NM, True, 50.0, "NOT_MEASURABLE", "GUARD_NOT_REACHED", HPR_NOT_OK)
    flow_reach = (DQ_FLOW, True, 50.0, "NOT_MEASURABLE", "GUARD_NOT_REACHED", None)
    flow_dis = (DQ_FLOW, True, 50.0, "NOT_MEASURABLE", "GRADED_DISAGREED", None)
    prev_zero = (MEAS, False, 0.0, "TWR", "GRADED_AGREED", None)
    prev_pos = (MEAS, False, 100.0, "TWR", "GRADED_AGREED", None)
    cases = [
        ("link break with no previous row, previous partition present", nm, None, True, "LINK_BREAK_BASE_ABSENT/prior_value"),
        ("link break with no previous row, previous partition absent", nm, None, False, "LINK_BREAK_BASE_ABSENT/calendar"),
        ("link break with a previous value of zero", nm, prev_zero, True, "LINK_BREAK_BASE_NONPOSITIVE/prior_value"),
        ("NOT_MEASURABLE row with a positive base", nm, prev_pos, True, "INELIGIBLE_AFTER_COMPUTE/other"),
        ("FLOW_UNRECONCILED with guard GUARD_NOT_REACHED", flow_reach, prev_pos, True, "FLOW_UNRECONCILED:GUARD_NOT_REACHED/flow"),
        ("FLOW_UNRECONCILED with guard GRADED_DISAGREED", flow_dis, prev_pos, True, "FLOW_UNRECONCILED:GRADED_DISAGREED/flow"),
        ("no row on the day", None, prev_pos, True, "NO_ROW/calendar or position"),
        ("holdings not OK outranks the previous-value break", nm_bad_hpr, prev_zero, True, "LINK_BREAK_BASE_NONPOSITIVE/price"),
    ]
    got = []
    for name, row, prev, present, want in cases:
        code, inp = classify(row, prev, present)
        got.append((name, "%s/%s" % (code, inp), want))
    passed = all(g == w for _n, g, w in got)
    return {"description": "eight synthetic account-days, one per branch: a link break with no previous row (partition present, then absent), a link break with a previous value of zero, a NOT_MEASURABLE row with a positive base, a FLOW_UNRECONCILED row with each of two guard states, a no-row day, and one precedence case (holdings not OK outranks the break)",
            "expected": "; ".join("%s = %s" % (n, w) for n, _g, w in got),
            "observed": "; ".join("%s = %s" % (n, g) for n, g, _w in got),
            "passed": bool(passed)}


def top_after(counts, day, n=5):
    rows = sorted(((c, t) for t, c in counts.items() if t > day), key=lambda x: (-x[0], x[1]))
    return [(t, c) for c, t in rows[:n]]


def broken_by_date(table):
    seen = {}
    for h, t, q in zip(table["household_id"], table["business_date"], table["day_quality"]):
        if q == "ACCOUNT_MISSING":
            seen.setdefault(t, set()).add(h)
    return {t: len(v) for t, v in seen.items()}


def rebuild(members, acct_rows):
    """the household daily table, rebuilt as round 112 did it: per household, ACCOUNT_MISSING when a member with a row
    on the previous household date has no row on the day or a null total_return_daily; `named` lists those accounts."""
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
                miss = [a for a in before if a not in cur or cur[a][ISNULL]]
                if miss:
                    qual[t] = AM
                    named[t] = miss
                else:
                    base = sum(acct_rows[a][prev][MV] for a in before)
                    qual[t] = MEAS if base > 0 else NPV
            prev = t
        out[h] = (dates, qual, named)
    return out


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    pc_res = positive_control()
    print("POSITIVE CONTROL: passed=%s" % pc_res["passed"])
    if not pc_res["passed"]:
        raise Stop("the positive control failed; the classification is not trusted: " + pc_res["observed"])

    sys.path.insert(0, repo)
    sys.path.insert(0, os.path.join(repo, "lib"))
    import lib.opal_naming as naming
    import trading_calendar as tc
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq

    with open(os.path.join(repo, REGISTRY_REL), "rb") as fh:
        registry = json.loads(fh.read().decode("utf-8"))
    rows_for_firm = [f for f in registry.get("firms", []) if f.get("firm_id") == FIRM_ID]
    if len(rows_for_firm) != 1:
        raise Stop("the registry does not enumerate exactly one row for the firm")
    firm = rows_for_firm[0]["firm_id"]
    irpt_b, irpt_k = split_s3(naming.address("irpt", firm, "gold", RET_TABLE, "date=2000-01-01", "x"))
    irpt_root = irpt_k[: irpt_k.index("/" + RET_TABLE + "/") + 1]
    ret_prefix = irpt_root + RET_TABLE + "/"
    xw_b, xw_k = split_s3(naming.address("advi", firm, "gold", XW_TABLE, "date=2000-01-01", "x"))
    xw_prefix = xw_k[: xw_k.index("/" + XW_TABLE + "/") + len("/" + XW_TABLE + "/")]

    # the private round-111 household table (read-only): the recount inputs and the membership cross-check
    tt = pq.read_table(TABLE, columns=["household_id", "business_date", "total_return_daily", "day_quality"]).to_pydict()
    priv = {}
    for h, d, r, q in zip(tt["household_id"], tt["business_date"], tt["total_return_daily"], tt["day_quality"]):
        priv.setdefault(h, {})[d] = (sys.intern(str(q)), r is None)
    table_days = sorted({d for d in tt["business_date"]})
    as_of = table_days[-1]
    counts = broken_by_date({"household_id": tt["household_id"], "business_date": tt["business_date"], "day_quality": tt["day_quality"]})
    print("PRIVATE TABLE: rows %d, households %d, dates %d, as_of %s" % (len(tt["household_id"]), len(priv), len(table_days), as_of))
    del tt

    reader = Reader()
    # (b) the newest household crosswalk partition
    xw_parts = {}
    for p in reader.list_prefixes(xw_b, xw_prefix):
        m = DATE_RX.search(p)
        if m:
            xw_parts[m.group(1)] = p
    if not xw_parts:
        raise Stop("no household_crosswalk date= partition under the derived prefix")
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
        raise Stop("an account maps to more than one household; a surprise row is owed")

    # (a) the account gold: LIST first; the newest 900 partitions
    part_map = {}
    for p in reader.list_prefixes(irpt_b, ret_prefix):
        m = DATE_RX.search(p)
        if m:
            part_map[m.group(1)] = p
    listed = len(part_map)
    print("PARTITIONS LISTED (account_return_daily, date= prefixes): %d" % listed)
    if listed == 0:
        raise Stop("no date= partition under the derived account gold prefix")
    dates_read = sorted(part_map)[-MAX_PARTITIONS:]
    print("PARTITIONS READ: %d (newest %d)" % (len(dates_read), MAX_PARTITIONS))

    wanted = sorted(acct_to_opal)
    wanted_type = None
    acct_rows, acct_last = {}, {}
    dup_pairs = null_values = empty_partitions = 0
    part_rows = {}
    for d in dates_read:
        keys = sorted(k for k in reader.list_keys(irpt_b, part_map[d].rstrip("/") + "/") if k.endswith(".parquet"))
        if not keys:
            empty_partitions += 1
        part_rows[d] = 0
        for k in keys:
            tbl = pq.read_table(io.BytesIO(reader.get(irpt_b, k)), columns=GOLD_COLUMNS)
            part_rows[d] += tbl.num_rows
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
                            float(r["market_value_eod"]), sys.intern(str(r["return_basis"])),
                            sys.intern(str(r["guard_state"])),
                            sys.intern(str(r["holdings_price_return_reason"])) if r["holdings_price_return_reason"] is not None else None)
                if bd > acct_last.get(a, ""):
                    acct_last[a] = bd
    print("GOLD (crosswalk accounts): partitions read %d, empty partitions %d, account rows kept %d, duplicate account-day rows %d, null value rows %d, accounts with rows %d"
          % (len(dates_read), empty_partitions, sum(len(v) for v in acct_rows.values()), dup_pairs, null_values, len(acct_rows)))
    print("GOLD (all accounts): row counts of 2026-04-20, 2026-04-21, 2026-04-22: %s"
          % [part_rows.get(x) for x in ("2026-04-20", DAY, "2026-04-22")])
    if dup_pairs or null_values:
        raise Stop("duplicate account-day rows or null values in the gold; a surprise row is owed")

    # membership, as round 112: the crosswalk households with the accounts present in the gold
    members, dropped = {}, 0
    for opal, accts in groups.items():
        mem = sorted(a for a in accts if a in acct_rows)
        if not mem:
            dropped += 1
            continue
        members[opal] = mem
    print("HOUSEHOLDS: rebuilt %d, dropped (no account in the gold) %d" % (len(members), dropped))
    rb = rebuild(members, acct_rows)

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
        raise Stop("the rebuilt daily table differs from the private table; the memberships are misread")

    # the unmeasured account-days of every ACCOUNT_MISSING household day, classified one by one
    def prev_day(d):
        p = tc.prev_trading_day(dt.date.fromisoformat(d))
        return p.isoformat()

    pairs = []
    for h, (dates, qual, named) in rb.items():
        for d, lst in named.items():
            for a in lst:
                pairs.append((a, d))
    total_pairs = len(pairs)
    print("UNMEASURED ACCOUNT-DAYS (household sense): total %d over %d ACCOUNT_MISSING household days" % (total_pairs, sum(len(v[2]) for v in rb.values())))
    if total_pairs != EXPECTED_TOTAL:
        raise Stop("STOP: the unmeasured account-days total %d differs from round 112's %d; a BLOCKING row is owed" % (total_pairs, EXPECTED_TOTAL))

    # the target dates: 2026-04-21 and the five dates with the most households broken after it (recounted below)
    nxt = [t for t, _c in top_after(counts, DAY)]
    targets = [DAY] + nxt
    cause_c, dq_c, partition_absent = collections.Counter(), collections.Counter(), 0
    bad = collections.Counter()
    diag_pairs = collections.Counter()
    for a, d in pairs:
        pt = prev_day(d)
        pres = pt in part_map
        if not pres:
            partition_absent += 1
        row = acct_rows[a].get(d)
        prev_row = acct_rows[a].get(pt)
        dq_c[row[DQ] if row is not None else "NO_ROW"] += 1
        code, inp = classify(row, prev_row, pres)
        if code not in ALL_CODES or inp not in INPUTS + (NO_ROW_CAUSE_INPUT,):
            bad[code + "/" + inp] += 1
        cause_c[code + "/" + inp] += 1
        if d in targets:
            diag_pairs["%s|%s|%s" % (d, row[DQ] if row is not None else "NO_ROW", code + "/" + inp)] += 1
    print("  day_quality of the pairs: %s; pairs whose previous-day partition is absent: %d" % (dict(dq_c), partition_absent))
    if bad:
        raise Stop("STOP: causes outside the vocabulary of the read %s; a BLOCKING row is owed" % dict(bad))
    if set(dq_c) - {DQ_NM, DQ_FLOW, "NO_ROW"}:
        raise Stop("STOP: a day_quality outside NOT_MEASURABLE / FLOW_UNRECONCILED / no row; a BLOCKING row is owed")
    if cause_c.get("OTHER", 0) or any(k.startswith("OTHER") for k in cause_c):
        raise Stop("STOP: OTHER causes present; a BLOCKING row is owed")
    if sum(cause_c.values()) != EXPECTED_TOTAL:
        raise Stop("STOP: cause counts do not sum to the total")
    print("CAUSES (household sense, %d): %s" % (sum(cause_c.values()), dict(cause_c.most_common())))

    # firm-wide: the target dates and their previous trading days, read once more (every account)
    print("NEXT FIVE (recounted from the private table): %s" % [(t, counts[t]) for t in nxt])
    need_dates = set(targets) | {prev_day(t) for t in targets}
    missing = sorted(t for t in need_dates if t not in part_map)
    if missing:
        raise Stop("STOP: gold partitions absent for %s; an unreadable source is never a zero" % missing)
    firm_rows = {}
    for d in sorted(need_dates):
        rowsd = {}
        for k in sorted(k for k in reader.list_keys(irpt_b, part_map[d].rstrip("/") + "/") if k.endswith(".parquet")):
            tbl = pq.read_table(io.BytesIO(reader.get(irpt_b, k)), columns=GOLD_COLUMNS).to_pydict()
            for i, a in enumerate(tbl["account_id"]):
                if a is None:
                    continue
                if tbl["market_value_eod"][i] is None:
                    mv = None
                else:
                    mv = float(tbl["market_value_eod"][i])
                rowsd[str(a)] = (sys.intern(str(tbl["day_quality"][i])), tbl["total_return_daily"][i] is None, mv,
                                 sys.intern(str(tbl["return_basis"][i])), sys.intern(str(tbl["guard_state"][i])),
                                 sys.intern(str(tbl["holdings_price_return_reason"][i])) if tbl["holdings_price_return_reason"][i] is not None else None)
        firm_rows[d] = rowsd

    firm_diag = {}

    def firm_day(d):
        pt = prev_day(d)
        nm = [(a, r) for a, r in firm_rows[d].items() if r[DQ] == DQ_NM]
        by_code, by_input = collections.Counter(), collections.Counter()
        for a, r in nm:
            prev_row = firm_rows[pt].get(a)
            code, inp = classify(r, prev_row, pt in part_map)
            by_code[code] += 1
            by_input[inp] += 1
        assert sum(by_code.values()) == len(nm) == sum(by_input.values())
        # the day's whole profile, all accounts (diagnostic only; counts)
        firm_diag[d] = {"rows_total": len(firm_rows[d]),
                        "day_quality": dict(collections.Counter(r[DQ] for r in firm_rows[d].values())),
                        "holdings_reason_on_flow_or_nm": dict(collections.Counter(
                            "%s|%s" % (r[DQ], r[HPR]) for r in firm_rows[d].values() if r[DQ] in (DQ_NM, DQ_FLOW)))}
        return {"rows_not_measurable": len(nm), "by_reason_code": dict(by_code), "by_null_input": dict(by_input)}

    def claim_of(block):
        return "inferred" if block["by_reason_code"].get("INELIGIBLE_AFTER_COMPUTE", 0) > 0 else "measured"

    f21 = firm_day(DAY)
    print("DATE %s: rows_not_measurable %d; by reason code %s; by null input %s; households broken %d"
          % (DAY, f21["rows_not_measurable"], f21["by_reason_code"], f21["by_null_input"], counts.get(DAY, 0)))
    print("PROFILE %s (all accounts): %s" % (DAY, firm_diag[DAY]))
    print("PAIRS ON %s (household sense): %s" % (DAY, {k.split("|", 1)[1]: v for k, v in diag_pairs.items() if k.startswith(DAY + "|")}))
    date_0421 = {"date": DAY, "rows_not_measurable": f21["rows_not_measurable"], "households_broken": counts.get(DAY, 0),
                 "by_reason_code": f21["by_reason_code"], "by_null_input": {k: f21["by_null_input"].get(k, 0) for k in INPUTS},
                 "claim": claim_of(f21)}
    next_five = []
    for t in nxt:
        f = firm_day(t)
        print("NEXT %s: households broken %d; rows_not_measurable %d; by reason code %s; by null input %s"
              % (t, counts[t], f["rows_not_measurable"], f["by_reason_code"], f["by_null_input"]))
        next_five.append({"date": t, "households_broken": counts[t], "rows_not_measurable": f["rows_not_measurable"],
                          "by_reason_code": f["by_reason_code"], "by_null_input": {k: f["by_null_input"].get(k, 0) for k in INPUTS},
                          "claim": claim_of(f)})

    # the calendars: the library's answer, and the producer's (range mode day list, line 2130, from the same module)
    lib_answer = bool(tc.is_trading_day(dt.date.fromisoformat(DAY)))
    producer_days = [str(x)[:10] for x in tc.trading_days_between("2026-04-20", "2026-04-22")]
    producer_answer = DAY in producer_days
    weekday = dt.date.fromisoformat(DAY).strftime("%A")
    print("CALENDAR %s: lib is_trading_day %s; producer range-mode day list (2026-04-20..22) %s; weekday %s"
          % (DAY, lib_answer, producer_days, weekday))
    calendars = {
        "date": DAY,
        "lib_trading_calendar_is_trading_day": lib_answer,
        "producer_calendar_is_trading_day": producer_answer,
        "producer_calendar_note": "the producer's range-mode day list is tc.trading_days_between (imported from the shared lib at line 95, called at line 2130) and each day's link day is tc.prev_trading_day (line 1302); the same module answers both, so the producer answer equals the library answer by construction; a --date run (line 2129) takes the given date with no calendar check; %s is a %s and not in the generated NYSE closure list" % (DAY, weekday),
        "producer_calendar_source": {"file": PRODUCER, "line": 2130,
                                     "words": "range mode builds its trading-day list from tc.trading_days_between, the shared lib calendar"},
        "agree": bool(producer_answer is not None and producer_answer == lib_answer),
        "gold_rows_by_date": {"2026-04-20": part_rows.get("2026-04-20"), DAY: part_rows.get(DAY), "2026-04-22": part_rows.get("2026-04-22")},
        "claim": "inferred",
    }

    # the shares over ALL 56,311 household-sense unmeasured account-days
    rec112 = json.loads(Path(os.path.join(repo, R112_REL)).read_bytes().decode("utf-8"))
    r112_total = rec112["unmeasured_account_days"]["total"]
    if r112_total != EXPECTED_TOTAL:
        raise Stop("STOP: round 112's record total %r is not %d" % (r112_total, EXPECTED_TOTAL))
    by_cause = []
    for cause, n in sorted(cause_c.items(), key=lambda kv: (-kv[1], kv[0])):
        by_cause.append({"cause": cause, "count": int(n), "share": round(n / float(total_pairs), 4)})
    shares = {"total_unmeasured_account_days": total_pairs, "by_cause": by_cause,
              "claim": "inferred" if any(k.startswith("INELIGIBLE_AFTER_COMPUTE") for k in cause_c) else "measured"}
    print("TOP CAUSES:")
    for c in by_cause[:5]:
        print("  %s count %d share %.4f" % (c["cause"], c["count"], c["share"]))

    sha = hashlib.sha256(Path(os.path.abspath(__file__)).read_bytes()).hexdigest()
    record = {
        "as_of": as_of,
        "date_0421": date_0421,
        "calendars": calendars,
        "next_five": next_five,
        "shares": shares,
        "producer": {"file": PRODUCER,
                     "reason_code_sites": [
                         {"code": "LINK_BREAK_BASE_ABSENT", "line": 1358},
                         {"code": "LINK_BREAK_BASE_NONPOSITIVE", "line": 1358},
                         {"code": "INELIGIBLE_AFTER_COMPUTE", "line": 1135},
                         {"code": "FLOW_UNRECONCILED", "line": 1505}],
                     "words": "NOT_MEASURABLE is set by the link break whose condition (base absent or not above zero) is at line 1358 and whose set is at lines 1361-1362, by the post-compute ineligibility check (condition at line 1133, set at lines 1134-1135, which persists no reason), and by the source-lag and flow branches; FLOW_UNRECONCILED is set at lines 1505, 1517 and 1522. The gold persists no reason code for the link break or the ineligibility check, so those codes are inferred from the gold's neighbouring rows."},
        "positive_control": {"description": pc_res["description"], "expected": pc_res["expected"], "observed": pc_res["observed"], "passed": True},
        "analysis": {"file": ANALYSIS_REL, "sha256": sha, "tracked": True},
        "reads": {"s3_reads": reader.calls, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "files_in_repo": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    private = {"record": record, "scope": "firm-wide rows_not_measurable and splits (all accounts of the gold partition); household-sense shares (crosswalk accounts)",
               "households_broken_by_date_ge_20260401": {k: v for k, v in sorted(counts.items()) if k >= "2026-04-01"},
               "cause_counts_household_sense": dict(cause_c), "partition_absent_pairs": partition_absent,
               "target_pairs_by_date_dq_cause": dict(diag_pairs), "firm_profile_by_target_date": firm_diag,
               "partitions_listed": listed, "partitions_read": len(dates_read), "rebuild_check": {"households_equal": hh_set_equal, "mismatch": mismatch}}
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(private, indent=2, sort_keys=True) + "\n")
    with open(os.path.join(repo, REC_REL), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(record, indent=2) + "\n")
    print("RECORD WRITTEN: %s" % REC_REL)
    print("PRIVATE WRITTEN: %s" % os.path.join(PRIVATE_DIR, PRIVATE_NAME))
    print("ANALYSIS SHA256 %s; s3 calls %d" % (sha, reader.calls))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Stop as e:
        print("STOP: %s" % e)
        sys.exit(3)
