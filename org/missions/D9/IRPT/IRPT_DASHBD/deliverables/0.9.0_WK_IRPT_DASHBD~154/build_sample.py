"""build_sample.py -- one 49 Financial household of several accounts, built from gold into the
performance-report contract's shape. Writes ONLY to a private folder (never the repo).

Order: IRPT_DASHBD.TO-DB-b-175 (round 94, cell DB-b-175), issuer 2.0.0_SA_COO~D2, serial 0.9.0_WK_IRPT_DASHBD~141.
Round 101 (DB-b-189, serial 0.9.0_WK_IRPT_DASHBD~154): a copy of the ~141 builder that fills the (a) members of the
classification (ABSENT_CLASSIFICATION.json), takes the firm as an argument, and keeps every firm-keyed address in
firm_adapter(firm), the only function of this file that names a firm's places.
Run: python -I build_sample.py <repo_root> --out <private_out_dir> [--firm <firm_id>]   (default firm 49financial)

WRITES (private folder only): HOUSEHOLD_SAMPLE.json (the filled report), PROOF_READ.txt (the proof read, for the issuer),
BUILD_COUNTS.json (counts and booleans only). Nothing is written to the repo.

READS (S3 GET and LIST only; no put, copy, delete, vendor call or secret read):
  - the ADVI household crosswalk (the household source of firm_adapter): LIST of its prefix (the one granted prefix,
    issuer's ruling, amendment 1), newest date= partition, GET of its household_crosswalk.parquet;
  - the irpt gold tables of the firm named by each sibling contract's "table" field, addressed by
    lib/opal_naming.address(): account_return_daily is LISTed (every date= partition) and each data.parquet is GET
    (the history test and the windows, amendment 3); account_activity_daily, the lot tables and account_class_daily
    are read at their newest date= partition, GET of data.parquet.
  The client summary, the investor-reporting directory and dim_return_method are NOT read (outside this cell's grant,
  amendments 1 and 2); every member the contract sources to them is written ABSENT with its reason in words.

HOUSEHOLD RULE (amendment 3, issuer 2.0.0_SA_COO~D2, 2026-10-13). It supersedes the amendment-2 rule and the rules
R1-R5 of the first seats, which stay in git history. Written BEFORE any figure of this run was read; the only reads before
this text were partition names and column names.
  R1. Grouping: the accounts that share an opal_relationship_id in the newest crosswalk partition. A crosswalk row with a
      null opal_relationship_id or a null schwab_account_number belongs to no household.
  R2. An ACCOUNT of a household is such a crosswalk row whose schwab_account_number is present in the newest
      account_return_daily partition.
  R3. Reference date R = the newest business_date in the newest account_return_daily partition. R is the as_of of every
      window and every figure.
  R4. HISTORY: an account passes when it has at least 252 trading days of return history, counted as the number of
      account_return_daily date= partitions in which the account has a row (every partition is listed and read).
  R5. ELIGIBLE: a household of at least 3 accounts (R2), EVERY one of which passes R4.
  R6. CHOSEN: the eligible household whose sha256 of its opal_relationship_id (utf-8, hex digest) sorts lowest.
  If no household is eligible, the build records the counts (households with 3 or more accounts under R2; households
  eligible under R5; accounts passing R4) and stops. No other household is tried. A partition date is used only for
  R3 and the history count; no date and no id is printed to the record.

WINDOWS (amendment 3(a); supersedes the amendment-2 window rule). The contract's 36 window members (beginning value,
ending value, net additions and net gain for QTD, YTD, last 12 months and since inception in both value summaries, and
the four account returns) are filled FROM account_return_daily by the contract's own folds, as its fold text (version
0.2.0) states them. For a window with start day S, the ANCHOR is the last trading day before S (lib/trading_calendar.py);
the window's days are the trading days after the anchor up to and including R.
  - beginning value = market_value_eod on the anchor; ending value = market_value_eod on R;
  - net additions = the sum of external_flow over the window's days (capital-in positive);
  - net gain = ending - beginning - net additions, a RESIDUAL, never plugged;
  - since inception opens on the account's first valued day (its first row in any date= partition);
  - return = the product of (1 + total_return_daily) over the window's days, minus 1.
ABSENT in words, never zero, by the folds: no row on the anchor day (NOT_SPANNED); SOURCE_LAG on the anchor or on R;
a missing row or a SOURCE_LAG flow on a window day; a null total_return_daily; a GRADED_DISAGREED guard_state. A
household sum is absent when any account term is absent.
ACTIVITY-ONLY members (the activity-table act.* and hold.net_gain_* members, and the household series that need
history): read account_activity_daily. For any window the activity table cannot open (its rows do not reach the window's
opening anchor), the member is {"absent": "history not yet built: gold account_activity_daily holds <N> trading days"},
N the count of its date= partitions (the dates go to the private sample only).
Members sourced outside this cell's grant (the client summary, dim_return_method) are ABSENT with that reason.

FILLED REPORT (contract document.filled_report, version 0.3.0; amendment 4, issuer 2.0.0_SA_COO~D2, round 97). The
filled report is exactly two top-level keys, household and values. household is {household_ref, as_of, first_data_date,
accounts}; each account entry is {account_id (the custodian form), last4, first_data_date (the account's first row in
account_return_daily), window_status (one of MEASURED, NOT_SPANNED, BREAK for each of the four windows)}. The windows block
and the row list are not part of a filled report.

UNITS. Dollars are stored as floats rounded to 2 dp. Percent values are stored as percent numbers rounded to 1 dp
(the decimal fraction times 100). Series are lists of {name, points: [{date, value}]} (a point with no measured figure is
left out; a chart with no measured point holds its absent form). Account-grain members, and the asset-class allocation,
hold {"by_row": {key: figure}}; a member whose whole source is ABSENT holds the single absent form.

IDENTITY CHECKS (amendment 3(c)). Tolerance 1.00 dollar; identity.basis "daily_ledger_and_cross_table". The COUNTED
checks are independent of the window folds:
  (i)   the one-day ledger identity the activity contract's identity_gap column defines: beginning_value + contributions
        - withdrawals + realized + unrealized_change + income - ending_value = 0, for each account and each activity row
        whose previous trading day (lib/trading_calendar.prev_trading_day) also has an activity row for that account;
  (ii)  for each account and each activity day, activity ending_value = account_return_daily market_value_eod that day;
  (iii) for each account and each activity day whose previous trading day has an activity row, activity beginning_value
        = account_return_daily market_value_eod on that previous trading day.
A null on either side of a check is NOT GRADEABLE and is counted as such, never as a pass. A failing check is a finding:
the build records the counts and stops; nothing is adjusted.
window_residual_checks: beginning + net additions + net gain = ending, per window and account and household. It holds by
construction (net gain is the residual), so it is RECORDED SEPARATELY and is NOT counted in identity.checks.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
from urllib.parse import urlparse

DEFAULT_FIRM = "49financial"
REGISTRY_REL = "data/firm_registry.json"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
ACT_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_ACTIVITY_DAILY_CONTRACT.json"
RET_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
LOT_R_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json"
LOT_U_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_LOT_UNREALIZED_DAILY_CONTRACT.json"
CLS_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json"
TOL = 1.0
MIN_ACCOUNTS = 3
HIST_MIN_DAYS = 252
CLASS_ENUM = ["cash", "fixed_income", "equity", "structured", "alternatives", "commodities", "unclassified"]
CS_MARK = "CLIENT_SUMMARY"
DATE_PART = re.compile(r"date=(\d{4}-\d{2}-\d{2})/$")
METHOD_PART = re.compile(r"method_version=(\d+)/$")
WIN_KEYS = ("qtd", "ytd", "last_12_months", "since_inception")
CHECK_WINDOWS = ("qtd", "ytd", "last_12_months")


class Absent(object):
    """An absent form: the gold row holds no value for this term, and the reason is printed in words."""

    def __init__(self, reason):
        self.reason = reason


class Reader(object):
    """GET and LIST only. There is deliberately no put, copy or delete method."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.gets = 0
        self.lists = 0

    def list_prefixes(self, bucket, prefix):
        self.lists += 1
        out = []
        for page in self._s3.get_paginator("list_objects_v2").paginate(
                Bucket=bucket, Prefix=prefix, Delimiter="/"):
            for cp in page.get("CommonPrefixes", []):
                out.append(cp["Prefix"])
        return out

    def get(self, bucket, key):
        self.gets += 1
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def split_s3(addr):
    p = urlparse(addr)
    if p.scheme != "s3" or not p.netloc:
        raise SystemExit("ERROR: address is not an s3 url")
    return p.netloc, p.path.lstrip("/")


_RUN = {}   # set by main(): the repo root, the naming module and the one Reader; read by firm_adapter only


def gold_prefix(ad, table):
    """The key prefix of one irpt gold table of the firm, from the adapter's gold root (no firm name here)."""
    return ad["irpt_gold_root"] + table + "/"


def firm_adapter(firm):
    """THE ONE FUNCTION THAT NAMES A FIRM'S PLACES. Every firm-keyed address the builder uses is derived here: the bucket
    and the key root of the firm's irpt gold tier and of its advi household crosswalk, from lib/opal_naming.address().
    The firm must be enumerated by data/firm_registry.json. A firm whose irpt/<firm>/gold/ prefix holds no object (one
    LIST, nothing read) raises NotImplementedError. No firm id, bucket or prefix is typed in this function."""
    naming = _RUN["naming"]
    with open(os.path.join(_RUN["repo"], REGISTRY_REL), "rb") as fh:
        registry = json.loads(fh.read().decode("utf-8"))
    if firm not in [row.get("firm_id") for row in registry.get("firms", [])]:
        raise SystemExit("ERROR: firm %s is not enumerated by %s" % (firm, REGISTRY_REL))
    irpt_bucket, irpt_key = split_s3(naming.address("irpt", firm, "gold", "account_return_daily", "date=2000-01-01", "x"))
    irpt_root = irpt_key[: irpt_key.index("/account_return_daily/")] + "/"
    if not _RUN["reader"].list_prefixes(irpt_bucket, irpt_root):
        raise NotImplementedError("%s: no gold exists" % firm)
    xw_bucket, xw_key = split_s3(naming.address("advi", firm, "gold", "household_crosswalk", "date=2000-01-01", "x"))
    xw_prefix = xw_key[: xw_key.index("/household_crosswalk/") + len("/household_crosswalk/")]
    return {"firm": firm, "irpt_bucket": irpt_bucket, "irpt_gold_root": irpt_root,
            "xw_bucket": xw_bucket, "xw_prefix": xw_prefix}


def newest_partition(reader, bucket, prefix, rx, label):
    found = []
    for p in reader.list_prefixes(bucket, prefix):
        m = rx.search(p)
        if m:
            found.append(m.group(1))
    if not found:
        raise SystemExit("ERROR: no partition under the granted prefix for %s" % label)
    return max(found), len(found)


def read_table(data, columns=None):
    import pyarrow.parquet as pq
    return pq.read_table(io.BytesIO(data), columns=columns).to_pylist()


def clean(v):
    if v is None:
        return None
    if isinstance(v, float) and v != v:
        return None
    return v


def one_year_before(d):
    try:
        return d.replace(year=d.year - 1)
    except ValueError:
        return d.replace(year=d.year - 1, day=28)


def window_start(name, R):
    if name == "qtd":
        return dt.date(R.year, 3 * ((R.month - 1) // 3) + 1, 1)
    if name == "ytd":
        return dt.date(R.year, 1, 1)
    if name == "last_12_months":
        return one_year_before(R)
    return None


def next_trading_day(tc, d):
    c = d + dt.timedelta(days=1)
    while not tc.is_trading_day(c):
        c += dt.timedelta(days=1)
    return c


def window_terms(rows, anchor, first_expected, R):
    """rows: {business_date: activity row} for one account. Returns the account's terms for one window."""
    rd = R.isoformat()
    ad = anchor.isoformat()
    days = sorted(d for d in rows if ad < d <= rd)
    t = {"days": len(days), "expected_first": first_expected.isoformat()}
    if not days:
        why = "no activity row falls in the window"
        t.update(beginning_value=Absent(why), net_additions=Absent(why), net_gain=Absent(why),
                 ending_value=Absent(why), contributions=Absent(why), withdrawals=Absent(why),
                 income=Absent(why))
        return t
    first = rows[days[0]]
    if days[0] != first_expected.isoformat():
        bv = Absent("the window's first trading day carries no activity row, so no opening value is read")
    elif first["beginning_value"] is None:
        bv = Absent("the opening day carries NO_PRIOR_VALUE: there is no prior-day value to open the window")
    else:
        bv = float(first["beginning_value"])
    t["beginning_value"] = bv
    if rd not in rows:
        ev = Absent("the activity table carries no row for the as_of day, so no ending value is read")
    else:
        ev = float(rows[rd]["ending_value"])
    t["ending_value"] = ev
    contrib = [clean(rows[d]["contributions"]) for d in days]
    withd = [clean(rows[d]["withdrawals"]) for d in days]
    inc = [clean(rows[d]["income"]) for d in days]
    gains = [(clean(rows[d]["realized"]), clean(rows[d]["unrealized_change"]), clean(rows[d]["income"])) for d in days]
    if any(x is None for x in contrib) or any(x is None for x in withd):
        na = Absent("a flow term is null on a day of the window")
        c_sum = Absent("a flow term is null on a day of the window")
        w_sum = c_sum
    else:
        c_sum = sum(contrib)
        w_sum = sum(withd)
        na = c_sum - w_sum
    t["contributions"] = c_sum
    t["withdrawals"] = w_sum
    t["net_additions"] = na
    if any(x is None for g in gains for x in g):
        ng = Absent("a gain term (realized, unrealized_change or income) is null on a day of the window, so the window's net gain is not measured")
        inc_sum = Absent("income is null on a day of the window")
    else:
        ng = sum(a + b + c for a, b, c in gains)
        inc_sum = sum(inc)
    t["net_gain"] = ng
    t["income"] = inc_sum
    return t


def hh_sum(terms, key):
    vals = [t[key] for t in terms]
    for i, v in enumerate(vals, 1):
        if isinstance(v, Absent):
            return Absent("a household figure is absent when any account term is absent: account %d of %d carries: %s"
                          % (i, len(vals), v.reason))
    return sum(vals)


def to_form(v):
    if isinstance(v, Absent):
        return {"absent": v.reason}
    if isinstance(v, dict):
        return {k: to_form(x) for k, x in v.items()}
    if isinstance(v, list):
        return [to_form(x) for x in v]
    if isinstance(v, float):
        return round(v, 2)
    return v


def leaves(v):
    if isinstance(v, dict):
        for x in v.values():
            for y in leaves(x):
                yield y
    elif isinstance(v, list):
        for x in v:
            for y in leaves(x):
                yield y
    else:
        yield v


def is_absent_form(v):
    return isinstance(v, dict) and set(v.keys()) == {"absent"}


def measured_leaves(v):
    """The leaves of a member that carry a figure or a text: absent forms and the series 'date' keys are not measured."""
    if is_absent_form(v):
        return
    if isinstance(v, dict):
        for k, x in v.items():
            if k not in ("date", "name"):
                for y in measured_leaves(x):
                    yield y
    elif isinstance(v, list):
        for x in v:
            for y in measured_leaves(x):
                yield y
    else:
        yield v


def fully_absent(v):
    """True when no figure of the member is measured: every term is an absent form (a member with some accounts
    measured is not fully absent)."""
    return not any(True for _ in measured_leaves(v))


RET_COLS = ["account_id", "business_date", "market_value_eod", "external_flow", "total_return_daily", "day_quality",
            "guard_state"]


def date_partitions(reader, bucket, prefix, rx):
    """{date: partition prefix} for the date= partitions under one prefix (LIST only)."""
    out = {}
    for p in reader.list_prefixes(bucket, prefix):
        m = rx.search(p)
        if m:
            out[m.group(1)] = p
    return out


def trading_days_list(tc, first, last):
    """Every trading day d with first <= d <= last (lib/trading_calendar.py)."""
    out = []
    d = first
    while d <= last:
        if tc.is_trading_day(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


NOT_SPANNED = ("NOT_SPANNED: the account has no account_return_daily row on its opening anchor day, so it did not hold "
               "a value at the window's start (the not-held dash)")


def hist_reason(table, n):
    return "history not yet built: gold %s holds %d trading days" % (table, n)


def absent_terms(reason):
    """The activity-sourced terms of a window the activity table cannot open: each carries the reason in words."""
    keys = ("beginning_value", "net_additions", "net_gain", "ending_value", "contributions", "withdrawals", "income")
    t = {k: Absent(reason) for k in keys}
    t["days"] = 0
    return t


def ret_window_terms(rows, anchor, days, R):
    """rows: {business_date: (market_value_eod, external_flow, total_return_daily, day_quality, guard_state)} for one
    account; anchor: the window's opening anchor day; days: the window's trading days, anchor < d <= R. Returns the
    account's terms by the contract's folds (version 0.2.0): each is a number or an Absent with its reason, never zero."""
    ad, rd = anchor.isoformat(), R.isoformat()
    a = rows.get(ad)
    t = {"days": len(days)}
    if a is None:
        t["beginning_value"] = Absent(NOT_SPANNED)
    elif a[3] == "SOURCE_LAG":
        t["beginning_value"] = Absent("the opening anchor day is SOURCE_LAG, so its value is unknown and the beginning "
                                      "value is not read")
    else:
        t["beginning_value"] = float(a[0])
    e = rows.get(rd)
    if e is None:
        t["ending_value"] = Absent("no account_return_daily row on as_of, so the ending value is not read")
    elif e[3] == "SOURCE_LAG":
        t["ending_value"] = Absent("as_of is SOURCE_LAG, so the ending value is unknown and is not read")
    else:
        t["ending_value"] = float(e[0])
    flows = []
    for d in days:
        r = rows.get(d.isoformat())
        if r is None or r[3] == "SOURCE_LAG":
            flows = None
            break
        flows.append(float(r[1]))
    if flows is None:
        t["net_additions"] = Absent("a window day has no account_return_daily row or a SOURCE_LAG flow, so the net "
                                    "additions are not read")
    else:
        t["net_additions"] = sum(flows)
    bv, ev, na = t["beginning_value"], t["ending_value"], t["net_additions"]
    if any(isinstance(x, Absent) for x in (bv, ev, na)):
        t["net_gain"] = Absent("a term of the residual (beginning value, net additions or ending value) is absent, so "
                               "the net gain is not read")
    else:
        t["net_gain"] = ev - bv - na
    why = None
    if a is None:
        why = NOT_SPANNED
    elif a[3] == "SOURCE_LAG":
        why = "the opening anchor day is SOURCE_LAG, so the return link has no measured start"
    prod = 1.0
    if why is None:
        for d in days:
            r = rows.get(d.isoformat())
            if r is None:
                why = "a window day has no row, so the geometric link breaks and the window is not bridged"
                break
            if r[2] is None:
                why = ("a window day has a null total_return_daily (NOT_MEASURABLE or SOURCE_LAG), so the link breaks "
                       "and the window is not bridged")
                break
            if r[4] == "GRADED_DISAGREED":
                why = "a window day is GRADED_DISAGREED, which serves no number"
                break
            prod *= 1.0 + float(r[2])
    t["return_cumulative"] = Absent(why) if why else round((prod - 1.0) * 100.0, 1)
    return t


def window_status(rows, anchor, days, R):
    """The window's status by the contract's filled_report.window_status_rule: NOT_SPANNED when the account has no
    account_return_daily row on the opening anchor day; BREAK when the anchor is SOURCE_LAG or a day inside the window
    (after the anchor, up to and including as_of) has no row, a SOURCE_LAG row, a null total_return_daily or a
    GRADED_DISAGREED guard_state; else MEASURED. rows: {business_date: (...)} as in ret_window_terms."""
    a = rows.get(anchor.isoformat())
    if a is None:
        return "NOT_SPANNED"
    if a[3] == "SOURCE_LAG":
        return "BREAK"
    for d in days:
        r = rows.get(d.isoformat())
        if r is None or r[3] == "SOURCE_LAG" or r[2] is None or r[4] == "GRADED_DISAGREED":
            return "BREAK"
    return "MEASURED"


def main(repo, out, firm):
    sys.path.insert(0, repo)
    import lib.opal_naming as naming
    from lib import trading_calendar as tc
    _RUN["naming"] = naming
    _RUN["repo"] = repo

    contract_path = os.path.join(repo, CONTRACT_REL)
    with open(contract_path, "rb") as fh:
        contract_bytes = fh.read()
    contract = json.loads(contract_bytes.decode("utf-8"))
    members = contract["members"]
    member_ids = [m["id"] for m in members]
    if len(set(member_ids)) != len(member_ids):
        raise SystemExit("ERROR: contract member ids are not unique")

    # sibling contracts: the gold table of each sourced account member is the sibling's own "table" field
    sibling_tables = {}
    sibling_columns = {}
    siblings = [ACT_CONTRACT, RET_CONTRACT, LOT_R_CONTRACT, LOT_U_CONTRACT, CLS_CONTRACT]
    for m in members:
        src = m.get("source")
        if isinstance(src, dict) and "contract" in src and CS_MARK not in src["contract"]:
            siblings.append(src["contract"])
    for rel in siblings:
        with open(os.path.join(repo, rel), "rb") as fh:
            sib = json.loads(fh.read().decode("utf-8"))
        sibling_tables[rel] = sib["table"]
        cols = sib["columns"]
        if isinstance(cols, dict):
            sibling_columns[rel] = list(cols.keys())
        else:
            sibling_columns[rel] = [c["name"] for c in cols]
    fields_checked = 0
    for m in members:
        src = m.get("source")
        if isinstance(src, dict) and "contract" in src and CS_MARK not in src["contract"]:
            if src["field"] not in sibling_columns[src["contract"]]:
                raise SystemExit("ERROR: member %s names field %s absent from its sibling contract"
                                 % (m["id"], src["field"]))
            fields_checked += 1

    reader = Reader()
    _RUN["reader"] = reader
    ad = firm_adapter(firm)
    # R1-R2 input: the newest household crosswalk partition (the household source of the adapter)
    xw_date, xw_parts = newest_partition(reader, ad["xw_bucket"], ad["xw_prefix"], DATE_PART, "household crosswalk")
    xw_addr = naming.address("advi", firm, "gold", "household_crosswalk", "date=%s" % xw_date,
                             "household_crosswalk.parquet")
    b, k = split_s3(xw_addr)
    xw_rows = read_table(reader.get(b, k), ["schwab_account_number", "opal_relationship_id"])

    # R2-R3: every account_return_daily partition is listed; the newest one gives R and the present accounts
    ret_table = sibling_tables[RET_CONTRACT]
    ret_parts = date_partitions(reader, ad["irpt_bucket"], gold_prefix(ad, ret_table), DATE_PART)
    if not ret_parts:
        raise SystemExit("ERROR: no account_return_daily date= partition under the granted prefix")

    def ret_addr(d):
        return naming.address("irpt", firm, "gold", ret_table, "date=%s" % d, "data.parquet")

    b, k = split_s3(ret_addr(max(ret_parts)))
    newest = read_table(reader.get(b, k), ["account_id", "business_date"])
    R = dt.date.fromisoformat(max(r["business_date"] for r in newest))
    present = {r["account_id"] for r in newest}

    groups = {}
    for r in xw_rows:
        opal = clean(r.get("opal_relationship_id"))
        acct = clean(r.get("schwab_account_number"))
        if not opal or not acct:
            continue
        groups.setdefault(opal, set()).add(acct)
    households = []
    for opal, accts in groups.items():
        pres = sorted(a for a in accts if a in present)
        if len(pres) >= MIN_ACCOUNTS:
            households.append((opal, pres))
    cand = {a for _o, pres in households for a in pres}

    # R4: the history count is the number of date= partitions each candidate account appears in; the rows of the
    # candidate accounts are kept for the windows and the identity checks (a filter, never a sum)
    RET = {a: {} for a in cand}
    hist = {a: 0 for a in cand}
    for d in sorted(ret_parts):
        b, k = split_s3(ret_addr(d))
        seen = set()
        for r in read_table(reader.get(b, k), RET_COLS):
            a = r["account_id"]
            if a in RET:
                RET[a][r["business_date"]] = (float(r["market_value_eod"]), float(r["external_flow"]),
                                             clean(r["total_return_daily"]), r["day_quality"], r["guard_state"])
                seen.add(a)
        for a in seen:
            hist[a] += 1

    # R5-R6: eligible households and the lowest sha256 of the relationship id
    eligible = []
    for opal, pres in households:
        if all(hist[a] >= HIST_MIN_DAYS for a in pres):
            eligible.append((hashlib.sha256(opal.encode("utf-8")).hexdigest(), opal, pres))
    eligible.sort()
    counts = {
        "crosswalk_partitions_listed": xw_parts,
        "return_partitions_listed": len(ret_parts),
        "return_partitions_read": len(ret_parts),
        "crosswalk_households_with_opal_id": len(groups),
        "households_with_3_or_more_accounts_R2": len(households),
        "accounts_present_R2": len(cand),
        "accounts_passing_R4": sum(1 for a in cand if hist[a] >= HIST_MIN_DAYS),
        "households_eligible_R5": len(eligible),
        "reference_R": R.isoformat(),
    }
    if not eligible:
        counts["outcome"] = "NO_ELIGIBLE_HOUSEHOLD"
        return finish_counts(out, counts, reader)
    hh_hash, hh_opal, hh_accts = eligible[0]
    accounts = sorted(hh_accts)
    counts["household_ref_sha256"] = hh_hash
    counts["accounts"] = len(accounts)
    counts["firm"] = firm
    # cover.as_of_date: the newest business_date among the household's account rows of the newest partition
    hh_set = set(accounts)
    hh_asof = max(r["business_date"] for r in newest if r["account_id"] in hh_set)
    counts["cover_as_of_is_reference_R"] = (hh_asof == R.isoformat())

    # the activity rows of the household, every activity partition (a filter, never a sum)
    act_table = sibling_tables[ACT_CONTRACT]
    act_rows, act_dates = gold_rows(reader, naming, ad, act_table, None, accounts, every=True)
    act_by_acct = {}
    for r in act_rows:
        act_by_acct.setdefault(r["account_id"], {})[r["business_date"]] = r
    counts["activity_partitions_listed"] = len(act_dates)
    counts["activity_method_versions_in_household"] = sorted({int(r["method_version"]) for r in act_rows})

    # windows: anchors from the calendar; trading days from the first return partition to R
    TD = trading_days_list(tc, dt.date.fromisoformat(min(ret_parts)), R)
    wdefs = {}
    for name in ("qtd", "ytd", "last_12_months"):
        s = window_start(name, R)
        anchor = tc.prev_trading_day(s)
        wdefs[name] = {"start": s.isoformat(), "anchor": anchor.isoformat(), "as_of": R.isoformat()}
    wdefs["since_inception"] = {"start": "per account: its first valued day", "anchor": None, "as_of": R.isoformat()}

    # return-table terms per account (the 36 window members), and the household sums
    TR = {}
    for a in accounts:
        rows = RET.get(a, {})
        TR[a] = {}
        for name in ("qtd", "ytd", "last_12_months"):
            anchor = dt.date.fromisoformat(wdefs[name]["anchor"])
            TR[a][name] = ret_window_terms(rows, anchor, [d for d in TD if anchor < d <= R], R)
        if rows:
            first = dt.date.fromisoformat(min(rows))
            TR[a]["since_inception"] = ret_window_terms(rows, first, [d for d in TD if first < d <= R], R)
        else:
            TR[a]["since_inception"] = ret_window_terms({}, R, [], R)
    H = {}
    for name in ("qtd", "ytd", "last_12_months", "since_inception"):
        terms = [TR[a][name] for a in accounts]
        H[name] = {key: hh_sum(terms, key) for key in ("beginning_value", "net_additions", "net_gain", "ending_value")}

    # the account entries of the filled report: first_data_date (its first account_return_daily row) and the four
    # window statuses, by the contract's filled_report rules; the since-inception window opens on that first row
    FIRST, STATUS = {}, {}
    for a in accounts:
        rows = RET.get(a, {})
        FIRST[a] = min(rows)
        STATUS[a] = {}
        for name in ("qtd", "ytd", "last_12_months"):
            anchor = dt.date.fromisoformat(wdefs[name]["anchor"])
            STATUS[a][name] = window_status(rows, anchor, [d for d in TD if anchor < d <= R], R)
        first = dt.date.fromisoformat(FIRST[a])
        STATUS[a]["since_inception"] = window_status(rows, first, [d for d in TD if first < d <= R], R)

    # convention.inception_per_household_and_account: the household's earliest first_data_date (per-account dates are
    # the account entries' first_data_date in the household block)
    hh_first = min(FIRST[a] for a in accounts)

    # activity-sourced window terms: a window the activity table cannot open is absent in words
    act_n = len(act_dates)
    TA = {}
    for a in accounts:
        TA[a] = {}
        rows = act_by_acct.get(a, {})
        for name in ("qtd", "ytd", "last_12_months"):
            anchor_s = wdefs[name]["anchor"]
            if anchor_s in act_dates:
                anchor = dt.date.fromisoformat(anchor_s)
                TA[a][name] = window_terms(rows, anchor, next_trading_day(tc, anchor), R)
            else:
                TA[a][name] = absent_terms(hist_reason("account_activity_daily", act_n))
        TA[a]["since_inception"] = absent_terms(hist_reason("account_activity_daily", act_n))

    # identity checks (amendment 3(c)): counted, tolerance 1 dollar; the residual identity is recorded apart
    proof_lines = []
    tally = {"i": [0, 0, 0], "ii": [0, 0, 0], "iii": [0, 0, 0]}   # [checks, passed, not gradeable]
    pairs_none = [0]

    def record(rule, lhs, rhs):
        slot = tally[rule]
        if lhs is None or rhs is None:
            slot[2] += 1
            return
        slot[0] += 1
        gap = lhs - rhs
        if abs(gap) <= TOL:
            slot[1] += 1
        else:
            proof_lines.append("FAIL rule %s gap %.2f" % (rule, gap))

    def ret_mv(a, iso):
        r = RET.get(a, {}).get(iso)
        return None if r is None else r[0]

    for a in accounts:
        rows = act_by_acct.get(a, {})
        for d in sorted(rows):
            row = rows[d]
            prev = tc.prev_trading_day(dt.date.fromisoformat(d)).isoformat()
            ev = clean(row["ending_value"])
            record("ii", ev, ret_mv(a, d))
            if prev not in rows:
                pairs_none[0] += 1
                continue
            parts = [clean(row[k]) for k in ("beginning_value", "contributions", "withdrawals", "realized",
                                             "unrealized_change", "income")]
            if any(p is None for p in parts) or ev is None:
                record("i", None, None)
            else:
                record("i", parts[0] + parts[1] - parts[2] + parts[3] + parts[4] + parts[5], ev)
            record("iii", clean(row["beginning_value"]), ret_mv(a, prev))

    resid = [0, 0]   # [checks, passed]; NOT counted in identity.checks

    def residual(scope, name, t):
        vals = [t[k] for k in ("beginning_value", "net_additions", "net_gain", "ending_value")]
        if any(isinstance(v, Absent) for v in vals):
            return
        resid[0] += 1
        gap = vals[0] + vals[1] + vals[2] - vals[3]
        if abs(gap) <= TOL:
            resid[1] += 1
        proof_lines.append("%s %s residual gap %.2f" % (scope, name, gap))

    for name in ("qtd", "ytd", "last_12_months", "since_inception"):
        residual("household", name, H[name])
        for a in accounts:
            residual("account", name, TR[a][name])

    checks = sum(v[0] for v in tally.values())
    passed = sum(v[1] for v in tally.values())
    not_gradeable = sum(v[2] for v in tally.values())

    values = build_values(members, accounts, TR, TA, H, wdefs, R, reader, naming, tc, act_by_acct, act_dates,
                          sibling_tables, hh_hash, counts, ad, hh_asof, hh_first)
    missing = [i for i in member_ids if i not in values]
    if missing:
        raise SystemExit("ERROR: %d member ids were not assigned a value (first: %s)" % (len(missing), missing[0]))
    form = to_form(values)
    filled = sum(1 for mid in member_ids if not fully_absent(form[mid]))
    total = len(member_ids)
    absent = total - filled
    contract_absent = sum(1 for m in members if m["source"] == "ABSENT")

    # the filled report, exactly as the contract's document.filled_report states it: private only
    layout = {
        "household": {
            "household_ref": hh_hash,
            "as_of": R.isoformat(),
            "first_data_date": min(FIRST[a] for a in accounts),
            "accounts": [{"account_id": a, "last4": a[-4:], "first_data_date": FIRST[a], "window_status": STATUS[a]}
                         for a in accounts],
        },
        "values": form,
    }
    problems = shape_problems(members, form) + layout_problems(members, layout)
    shape_ok = (not problems) and filled + absent == total and absent >= contract_absent
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "HOUSEHOLD_SAMPLE.json"), "w", encoding="utf-8") as fh:
        json.dump(layout, fh, indent=1, sort_keys=True)
    with open(os.path.join(out, "PROOF_READ.txt"), "w", encoding="utf-8") as fh:
        fh.write("PROOF READ (private; for the issuer; never in the repo)\n")
        fh.write("reference R=%s windows: %s\n" % (R.isoformat(), json.dumps(wdefs, sort_keys=True)))
        fh.write("identity tally (rule: checks, passed, not gradeable): %s\n" % json.dumps(tally, sort_keys=True))
        for line in proof_lines:
            fh.write(line + "\n")
        fh.write("household value summary: %s\n" % json.dumps(to_form(H), default=str, sort_keys=True))

    counts.update({
        "members_total": total,
        "members_filled": filled,
        "members_absent": absent,
        "members_contract_absent": contract_absent,
        "absent_forms_inside_filled_members": count_inner_absent(form, member_ids),
        "fields_checked_against_sibling_contracts": fields_checked,
        "shape_problems": problems,
        "shape_valid_against_contract": shape_ok,
        "absent_members_never_zero": all(is_absent_form(form[m["id"]]) for m in members if m["source"] == "ABSENT"),
        "identity_checks": checks,
        "identity_passed": passed,
        "identity_not_gradeable": not_gradeable,
        "identity_by_rule": tally,
        "identity_pairs_without_prior_activity_row": pairs_none[0],
        "identity_tolerance_dollars": TOL,
        "identity_basis": "daily_ledger_and_cross_table",
        "window_residual_checks": resid,
        "gold_tables_read": sorted({ret_table, act_table, "household_crosswalk", sibling_tables[LOT_R_CONTRACT],
                                    sibling_tables[LOT_U_CONTRACT], sibling_tables[CLS_CONTRACT]}),
        "outcome": "BUILT",
    })
    return finish_counts(out, counts, reader)


def finish_counts(out, counts, reader):
    counts["s3_gets"] = reader.gets
    counts["s3_lists"] = reader.lists
    counts["s3_puts"] = 0
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "BUILD_COUNTS.json"), "w", encoding="utf-8") as fh:
        json.dump(counts, fh, indent=1, sort_keys=True)
    print(json.dumps(counts, indent=1, sort_keys=True))
    return 0


def count_inner_absent(values, member_ids):
    n = 0
    for mid in member_ids:
        v = values[mid]
        if is_absent_form(v):
            continue
        for leaf in leaves(v):
            if is_absent_form(leaf):
                n += 1
    return n


def shape_problems(members, values):
    problems = []
    ids = [m["id"] for m in members]
    for m in members:
        v = values.get(m["id"])
        if v is None:
            problems.append("no value for %s" % m["id"])
            continue
        if m["source"] == "ABSENT" and not is_absent_form(v):
            problems.append("contract ABSENT member %s holds a value" % m["id"])
        for leaf in leaves(v):
            if is_absent_form(leaf):
                if not isinstance(leaf["absent"], str) or not leaf["absent"].strip():
                    problems.append("empty absent reason at %s" % m["id"])
            elif leaf is None:
                problems.append("null leaf at %s" % m["id"])
            elif isinstance(leaf, bool):
                problems.append("boolean leaf at %s" % m["id"])
    if len(set(ids)) != len(ids):
        problems.append("duplicate member ids")
    return problems


WINDOW_STATUS_VALUES = ("MEASURED", "NOT_SPANNED", "BREAK")
WINDOW_KEYS_FILLED = ("qtd", "ytd", "last_12_months", "since_inception")


def layout_problems(members, layout):
    """The filled report against document.filled_report: top-level keys, household and account entry fields, window
    statuses from the enum, accounts in account_id order, the household first date, and every per-row member keyed by
    the household's accounts or by an asset class (wrapped in by_row)."""
    problems = []
    if sorted(layout.keys()) != ["household", "values"]:
        problems.append("top-level keys are %r, not household and values" % sorted(layout.keys()))
    hh = layout["household"]
    if sorted(hh.keys()) != ["accounts", "as_of", "first_data_date", "household_ref"]:
        problems.append("household keys are %r" % sorted(hh.keys()))
    accs = hh["accounts"]
    ids = [a["account_id"] for a in accs]
    if ids != sorted(ids) or len(set(ids)) != len(ids):
        problems.append("accounts are not in account_id order without duplicates")
    for a in accs:
        if sorted(a.keys()) != ["account_id", "first_data_date", "last4", "window_status"]:
            problems.append("account entry keys are %r" % sorted(a.keys()))
        ws = a["window_status"]
        if sorted(ws.keys()) != sorted(WINDOW_KEYS_FILLED) or any(v not in WINDOW_STATUS_VALUES for v in ws.values()):
            problems.append("window_status must hold the four windows with a status from the enum")
    if accs and hh["first_data_date"] != min(a["first_data_date"] for a in accs):
        problems.append("household first_data_date is not the earliest account first_data_date")
    keys_ok = set(ids) | set(CLASS_ENUM)
    for m in members:
        v = layout["values"].get(m["id"])
        if isinstance(v, dict) and "by_row" in v:
            if set(v.keys()) != {"by_row"} or not set(v["by_row"].keys()) <= keys_ok:
                problems.append("member %s: by_row must be the only key and hold household accounts or asset classes" % m["id"])
        elif isinstance(v, list):
            if not all(isinstance(s, dict) and sorted(s.keys()) == ["name", "points"] for s in v):
                problems.append("member %s: a series is a list of {name, points}" % m["id"])
    return problems


def build_values(members, accounts, TR, TA, H, wdefs, R, reader, naming, tc, act_by_acct, act_dates, sibling_tables,
                 hh_hash, counts, ad, hh_asof, hh_first):
    """Every member id is assigned here exactly once. Unknown sourced ids raise (no silent absent)."""
    out = {}
    cs_reason = ("carried by the client summary, which this build does not read (the issuer's ruling keeps the client "
                 "summary and the investor-reporting directory out of scope)")
    rd = R.isoformat()

    # the realized lots are partitioned by closing date, so the year-to-date and last-12-months folds read EVERY partition
    lot_r, lot_r_dates = gold_rows(reader, naming, ad, sibling_tables[LOT_R_CONTRACT],
                                   ["account_id", "business_date", "cost_basis", "proceeds", "realized_gain",
                                    "holding_term"], accounts, every=True)
    ytd_lots_open = bool(lot_r_dates) and lot_r_dates[0] <= wdefs["ytd"]["anchor"]
    l12_lots_open = bool(lot_r_dates) and lot_r_dates[0] <= wdefs["last_12_months"]["anchor"]
    lot_hist = hist_reason(sibling_tables[LOT_R_CONTRACT], len(lot_r_dates))
    lot_u, _d2 = gold_rows(reader, naming, ad, sibling_tables[LOT_U_CONTRACT], ["account_id", "business_date", "cost_basis",
                                                                           "unrealized_gain"], accounts)
    cls, cls_dates = gold_rows(reader, naming, ad, sibling_tables[CLS_CONTRACT],
                               ["account_id", "business_date", "asset_class", "market_value_eod"], accounts, every=True)
    counts["lot_realized_rows_read"] = len(lot_r)
    counts["lot_unrealized_rows_read"] = len(lot_u)
    counts["class_rows_read"] = len(cls)
    counts["class_partitions_listed"] = len(cls_dates)

    lot_r_by = {}
    for r in lot_r:
        lot_r_by.setdefault(r["account_id"], []).append(r)
    lot_u_by = {}
    for r in lot_u:
        if r["business_date"] == rd:
            lot_u_by.setdefault(r["account_id"], []).append(r)
    cls_by = {}
    for r in cls:
        key = (r["account_id"], r["business_date"])
        cls_by.setdefault(key, {}).setdefault(r["asset_class"], 0.0)
        cls_by[key][r["asset_class"]] += float(r["market_value_eod"])
    del lot_r, lot_u, cls

    l12_anchor = wdefs["last_12_months"]["anchor"]
    act_open = l12_anchor in act_dates
    act_days_l12 = sorted({d for a in accounts for d in act_by_acct.get(a, {}) if l12_anchor < d <= rd})
    cls_open = l12_anchor in cls_dates
    cls_days_l12 = sorted({d for d in cls_dates if l12_anchor < d <= rd})
    act_hist = hist_reason("account_activity_daily", len(act_dates))
    cls_hist = hist_reason(sibling_tables[CLS_CONTRACT], len(cls_dates))

    def per_account(fn):
        return {"by_row": {a: fn(a) for a in accounts}}

    def hh_term(w, term):
        return hh_sum([TA[a][w] for a in accounts], term)

    for m in members:
        mid = m["id"]
        src = m["source"]
        parts = mid.split(".")
        if src == "ABSENT":
            out[mid] = Absent(m["reason"])
            continue
        if mid == "cover.as_of_date":
            out[mid] = hh_asof
            continue
        if mid == "convention.inception_per_household_and_account":
            out[mid] = hh_first
            continue
        if isinstance(src, dict) and CS_MARK in src.get("contract", ""):
            out[mid] = Absent(cs_reason)
            continue
        if parts[0] == "pvs":
            out[mid] = H[parts[1]][parts[2]]
            continue
        if parts[0] == "avs":
            out[mid] = per_account(lambda a, w=parts[1], t=parts[2]: TR[a][w][t])
            continue
        if parts[0] == "act":
            term, grain = parts[1], parts[2]
            if term == "ending_value":
                if grain == "household":
                    out[mid] = H_end(accounts, act_by_acct, R)
                else:
                    out[mid] = per_account(lambda a: act_account_end(act_by_acct, a, R))
            elif grain == "household":
                out[mid] = hh_term("last_12_months", term)
            else:
                out[mid] = per_account(lambda a, t=term: TA[a]["last_12_months"][t])
            continue
        if mid == "hold.ending_value":
            out[mid] = H_end(accounts, act_by_acct, R)
            continue
        if mid.startswith("hold.net_gain_"):
            out[mid] = hh_term(mid[len("hold.net_gain_"):], "net_gain")
            continue
        if mid == "hold.allocation":
            out[mid] = {"by_row": allocation_at(accounts, cls_by, act_by_acct, R)}
            continue
        if parts[0] == "trgl":
            if not ytd_lots_open:
                out[mid] = per_account(lambda a: Absent(lot_hist))
            else:
                out[mid] = per_account(lambda a, k=parts[1]: trgl_value(k, lot_r_by.get(a, []), R))
            continue
        if parts[0] == "glr":
            if parts[1] == "total_realized_gl" and not l12_lots_open:
                out[mid] = per_account(lambda a: Absent(lot_hist))
            else:
                out[mid] = per_account(lambda a, k=parts[1]: glr_value(k, a, lot_r_by, lot_u_by, act_by_acct, R))
            continue
        if mid == "overview.chart.allocation_by_asset_class":
            out[mid] = series_or_absent(class_series(cls_days_l12, accounts, cls_by), NO_CHART_POINT) if cls_open else Absent(cls_hist)
            continue
        if mid == "accounts.chart.allocation_by_account":
            out[mid] = series_or_absent(account_series(act_days_l12, accounts, act_by_acct), NO_CHART_POINT) if act_open else Absent(act_hist)
            continue
        if mid == "accounts.chart.ending_value_and_net_additions_last_12_months":
            out[mid] = series_or_absent(ending_netadd_series(act_days_l12, accounts, act_by_acct), NO_CHART_POINT) if act_open else Absent(act_hist)
            continue
        if mid == "holdings.rows.class_hierarchy":
            out[mid] = ("class level only: Opal's seven asset-class values (" + ", ".join(CLASS_ENUM) +
                        "); the baseline's sub-class rows are not carried by any sibling, so each sub-class cell is absent")
            continue
        if mid == "convention.fee_basis_label":
            out[mid] = Absent(FEE_REASON)
            continue
        if mid == "convention.not_held_for_entire_period":
            out[mid] = Absent(cs_reason)
            continue
        if mid == "overview.chart.portfolio_performance_last_12_months":
            out[mid] = Absent("the household performance line needs a household daily return series, which no sibling "
                              "carries")
            continue
        raise SystemExit("ERROR: sourced member %s has no builder rule" % mid)
    # account-grain members whose value is a dict keyed by account are checked by shape_problems
    return out


def gold_rows(reader, naming, ad, table, columns, accounts, every=False):
    """Rows of one gold table filtered to the household's accounts (a filter, never a sum). every=False reads the newest
    date= partition; every=True reads all of them. Returns (rows, sorted partition dates); LIST and GET only."""
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq
    parts = date_partitions(reader, ad["irpt_bucket"], gold_prefix(ad, table), DATE_PART)
    if not parts:
        raise SystemExit("ERROR: no date= partition for gold table %s" % table)
    use = sorted(parts) if every else [max(parts)]
    rows = []
    for d in use:
        addr = naming.address("irpt", ad["firm"], "gold", table, "date=%s" % d, "data.parquet")
        b, k = split_s3(addr)
        tbl = pq.read_table(io.BytesIO(reader.get(b, k)), columns=columns)
        mask = pc.is_in(tbl["account_id"], value_set=pa.array(sorted(accounts)))
        rows.extend(tbl.filter(mask).to_pylist())
    return rows, sorted(parts)


FEE_REASON = ("the fee-basis row for method_version 3 is outside this cell's grant: gold dim_return_method is not read "
              "(issuer's amendment 2), so the fee-basis label is absent in words")


def H_end(accounts, act_by_acct, R):
    rd = R.isoformat()
    vals = []
    for a in accounts:
        r = act_by_acct.get(a, {}).get(rd)
        vals.append(Absent("no activity row on as_of") if r is None else float(r["ending_value"]))
    return hh_sum([{"v": v} for v in vals], "v")


def act_account_end(act_by_acct, a, R):
    r = act_by_acct.get(a, {}).get(R.isoformat())
    return Absent("no activity row on as_of") if r is None else float(r["ending_value"])


def allocation_at(accounts, cls_by, act_by_acct, R):
    rd = R.isoformat()
    out = {}
    if not any((a, rd) in cls_by for a in accounts):
        for c in CLASS_ENUM:
            out[c] = Absent("gold account_class_daily holds no row for this household on as_of, so no class share is read")
        return out
    end_total = H_end(accounts, act_by_acct, R)
    if isinstance(end_total, Absent):
        for c in CLASS_ENUM:
            out[c] = Absent("the household ending value is absent on as_of, so no share is taken")
        return out
    for c in CLASS_ENUM:
        mv = 0.0
        seen = False
        for a in accounts:
            d = cls_by.get((a, rd))
            if d is not None and c in d:
                mv += d[c]
                seen = True
        if not seen:
            out[c] = Absent("no holding in this asset class on as_of (a dash in the table, never zero)")
        elif end_total == 0:
            out[c] = Absent("the household ending value is zero on as_of")
        else:
            out[c] = round(mv / end_total * 100.0, 1)
    return out


def trgl_value(key, lots, R):
    ystart = dt.date(R.year, 1, 1).isoformat()
    rd = R.isoformat()
    sel = [r for r in lots if ystart <= r["business_date"] <= rd]
    if key == "cost_basis":
        return round(sum(float(r["cost_basis"]) for r in sel), 2)
    if key == "proceeds":
        return round(sum(float(r["proceeds"]) for r in sel), 2)
    if key == "realized_short_term":
        return round(sum(float(r["realized_gain"]) for r in sel if r["holding_term"] == "SHORT_TERM"), 2)
    if key == "realized_long_term":
        return round(sum(float(r["realized_gain"]) for r in sel if r["holding_term"] == "LONG_TERM"), 2)
    if key == "total_realized_gl":
        return round(sum(float(r["realized_gain"]) for r in sel), 2)
    raise SystemExit("ERROR: trgl key %s has no rule" % key)


def glr_value(key, a, lot_r_by, lot_u_by, act_by_acct, R):
    rd = R.isoformat()
    if key == "cost_basis":
        return round(sum(float(r["cost_basis"]) for r in lot_u_by.get(a, [])), 2)
    if key == "ending_value":
        r = act_by_acct.get(a, {}).get(rd)
        return Absent("no activity row on as_of") if r is None else float(r["ending_value"])
    if key == "total_realized_gl":
        start = one_year_before(R).isoformat()
        return round(sum(float(r["realized_gain"]) for r in lot_r_by.get(a, [])
                         if start <= r["business_date"] <= rd), 2)
    if key == "total_unrealized_gl":
        return round(sum(float(r["unrealized_gain"]) for r in lot_u_by.get(a, [])), 2)
    raise SystemExit("ERROR: glr key %s has no rule" % key)


NO_CHART_POINT = "no figure is measured on any day of the chart's window, so the chart holds no series"


def series_or_absent(lines, reason):
    """A chart's series, or its absent form when no point of any line is measured: a series point has no absent form,
    so an unmeasured point is left out and a chart with no measured point says why, in words."""
    return lines if any(line["points"] for line in lines) else Absent(reason)


def class_series(days, accounts, cls_by):
    """One series per asset class (name = the class): a point per day on which the class is measured, its share of
    the household's class total that day."""
    pts = {c: [] for c in CLASS_ENUM}
    for d in days:
        tot = 0.0
        per = {}
        for a in accounts:
            dd = cls_by.get((a, d))
            if dd:
                for c, v in dd.items():
                    per[c] = per.get(c, 0.0) + v
                    tot += v
        for c in CLASS_ENUM:
            if c in per and tot > 0:
                pts[c].append({"date": d, "value": round(per[c] / tot * 100.0, 1)})
    return [{"name": c, "points": pts[c]} for c in CLASS_ENUM]


def account_series(days, accounts, act_by_acct):
    """One series per account (name = the account id): a point per day on which the account has an ending value, its
    share of the household's ending value that day."""
    pts = {a: [] for a in accounts}
    for d in days:
        vals = {}
        for a in accounts:
            r = act_by_acct.get(a, {}).get(d)
            vals[a] = None if r is None else float(r["ending_value"])
        total = sum(v for v in vals.values() if v is not None)
        for a in accounts:
            if vals[a] is not None and total != 0:
                pts[a].append({"date": d, "value": round(vals[a] / total * 100.0, 1)})
    return [{"name": a, "points": pts[a]} for a in accounts]


def ending_netadd_series(days, accounts, act_by_acct):
    """Two series of the household: ending value and net additions (contributions less withdrawals). A day enters a
    series only when every account carries a row that day (a household sum is never partial)."""
    end_pts, net_pts = [], []
    for d in days:
        ends = []
        nets = []
        for a in accounts:
            r = act_by_acct.get(a, {}).get(d)
            ends.append(None if r is None else float(r["ending_value"]))
            nets.append(None if r is None else float(r["contributions"]) - float(r["withdrawals"]))
        if all(x is not None for x in ends):
            end_pts.append({"date": d, "value": round(sum(ends), 2)})
        if all(x is not None for x in nets):
            net_pts.append({"date": d, "value": round(sum(nets), 2)})
    return [{"name": "ending_value", "points": end_pts}, {"name": "net_additions", "points": net_pts}]


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Build one household sample into a private folder (never the repo).")
    ap.add_argument("repo_root")
    ap.add_argument("--out", required=True, help="the private output folder")
    ap.add_argument("--firm", default=DEFAULT_FIRM, help="a firm_id enumerated by data/firm_registry.json")
    args = ap.parse_args()
    sys.exit(main(os.path.abspath(args.repo_root), os.path.abspath(args.out), args.firm))
