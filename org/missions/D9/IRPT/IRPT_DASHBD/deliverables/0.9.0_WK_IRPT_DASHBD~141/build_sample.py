"""build_sample.py -- one 49 Financial household of several accounts, built from gold into the
performance-report contract's shape. Writes ONLY to a private folder (never the repo).

Order: IRPT_DASHBD.TO-DB-b-175 (round 94, cell DB-b-175), issuer 2.0.0_SA_COO~D2, serial 0.9.0_WK_IRPT_DASHBD~141.
Run: python -I build_sample.py <repo_root> <private_out_dir>

WRITES (private folder only): HOUSEHOLD_SAMPLE.json (the filled report), PROOF_READ.txt (the proof read, for the issuer),
BUILD_COUNTS.json (counts and booleans only). Nothing is written to the repo.

READS (S3 GET and LIST only; no put, copy, delete, vendor call or secret read):
  - the ADVI household crosswalk: LIST of advi/49financial/gold/household_crosswalk/ (the one granted prefix, issuer's
    ruling, amendment 1), newest date= partition, GET of its household_crosswalk.parquet;
  - the irpt gold tables of firm 49financial named by each sibling contract's "table" field, addressed by
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

UNITS. Dollars are stored as floats rounded to 2 dp. Percent values are stored as percent numbers rounded to 1 dp
(the decimal fraction times 100). Series are lists of dated objects. Account-grain members hold an object keyed by the
custodian account id; a member whose whole source is ABSENT holds the single absent form.

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

FIRM = "49financial"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
ACT_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_ACTIVITY_DAILY_CONTRACT.json"
RET_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
LOT_R_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_LOT_REALIZED_CONTRACT.json"
LOT_U_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_LOT_UNREALIZED_DAILY_CONTRACT.json"
CLS_CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_CLASS_DAILY_CONTRACT.json"
XWALK_PREFIX = "advi/49financial/gold/household_crosswalk/"
TOL = 1.0
MIN_ACCOUNTS = 3
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


def main(repo, out):
    sys.path.insert(0, repo)
    import lib.opal_naming as naming
    from lib import trading_calendar as tc

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
        p = os.path.join(repo, rel)
        with open(p, "rb") as fh:
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
            cols = sibling_columns[src["contract"]]
            if src["field"] not in cols:
                raise SystemExit("ERROR: member %s names field %s absent from its sibling contract" % (m["id"], src["field"]))
            fields_checked += 1

    reader = Reader()
    # newest crosswalk partition, LIST of the granted prefix only
    xw_bucket = naming.address("advi", FIRM, "gold", "household_crosswalk", "date=2000-01-01", "x").split("/")[2]
    xw_date, xw_parts = newest_partition(reader, xw_bucket, XWALK_PREFIX, DATE_PART, "household crosswalk")
    xw_addr = naming.address("advi", FIRM, "gold", "household_crosswalk", "date=%s" % xw_date,
                             "household_crosswalk.parquet")
    b, k = split_s3(xw_addr)
    xw_rows = read_table(reader.get(b, k), ["schwab_account_number", "opal_relationship_id"])

    def gold_table(table):
        probe = naming.address("irpt", FIRM, "gold", table, "date=2000-01-01")
        bucket = split_s3(probe)[0]
        prefix = "irpt/%s/gold/%s/" % (FIRM, table)
        newest, n = newest_partition(reader, bucket, prefix, DATE_PART, table)
        addr = naming.address("irpt", FIRM, "gold", table, "date=%s" % newest, "data.parquet")
        return newest, n, split_s3(addr)

    act_table = sibling_tables[ACT_CONTRACT]
    act_date, act_parts, act_loc = gold_table(act_table)
    act_rows_all = read_table(reader.get(*act_loc), None)
    act_accounts = set()
    act_by_acct = {}
    R = None
    for r in act_rows_all:
        a = r["account_id"]
        act_accounts.add(a)
        d = r["business_date"]
        if R is None or d > R:
            R = d
    R = dt.date.fromisoformat(R)

    ret_date, ret_parts, ret_loc = gold_table(sibling_tables[RET_CONTRACT])
    ret_rows = read_table(reader.get(*ret_loc), ["account_id", "business_date"])
    ret_first = {}
    for r in ret_rows:
        a = r["account_id"]
        d = r["business_date"]
        if a not in ret_first or d < ret_first[a]:
            ret_first[a] = d
    cutoff = one_year_before(R).isoformat()

    # R1 and R2: crosswalk groups
    groups = {}
    for r in xw_rows:
        opal = clean(r.get("opal_relationship_id"))
        acct = clean(r.get("schwab_account_number"))
        if not opal or not acct:
            continue
        groups.setdefault(opal, set()).add(acct)
    n_groups_3 = 0
    eligible = []
    for opal, accts in groups.items():
        present = sorted(a for a in accts if a in act_accounts)
        if len(present) < MIN_ACCOUNTS:
            continue
        n_groups_3 += 1
        # R4
        if all(a in ret_first and ret_first[a] <= cutoff for a in present):
            eligible.append((hashlib.sha256(opal.encode("utf-8")).hexdigest(), opal, present))
    eligible.sort()
    counts = {
        "crosswalk_partitions_listed": xw_parts,
        "households_with_opal_id": len(groups),
        "households_with_3_or_more_gold_accounts": n_groups_3,
        "households_eligible_R4": len(eligible),
        "activity_partitions_listed": act_parts,
        "return_partitions_listed": ret_parts,
        "activity_rows_all_accounts": len(act_rows_all),
        "activity_accounts_all": len(act_accounts),
    }
    if not eligible:
        counts["outcome"] = "NO_ELIGIBLE_HOUSEHOLD"
        return finish_counts(out, counts, reader)
    hh_hash, hh_opal, hh_accts = eligible[0]
    accounts = sorted(hh_accts)
    counts["household_ref_sha256"] = hh_hash
    counts["accounts"] = len(accounts)
    counts["reference_R"] = R.isoformat()

    # activity rows of the chosen household only
    acct_set = set(accounts)
    for r in act_rows_all:
        if r["account_id"] in acct_set:
            act_by_acct.setdefault(r["account_id"], {})[r["business_date"]] = r
    method_versions = sorted({int(r["method_version"]) for r in act_rows_all if r["account_id"] in acct_set})
    counts["activity_method_versions_in_household"] = method_versions
    counts["activity_rows_household"] = sum(len(v) for v in act_by_acct.values())
    del act_rows_all

    # windows: anchors and first expected trading day per account window (same for all accounts)
    wdefs = {}
    for name in ("qtd", "ytd", "last_12_months"):
        s = window_start(name, R)
        anchor = tc.prev_trading_day(s)
        first_exp = next_trading_day(tc, anchor)
        wdefs[name] = {"start": s.isoformat(), "anchor": anchor.isoformat(),
                       "first_trading_day": first_exp.isoformat(), "as_of": R.isoformat()}
    wdefs["since_inception"] = {"start": "account first_data_date (client summary, not granted)",
                                "anchor": None, "first_trading_day": None, "as_of": R.isoformat()}

    # per-account window terms
    T = {}
    for a in accounts:
        T[a] = {}
        for name in ("qtd", "ytd", "last_12_months"):
            w = wdefs[name]
            T[a][name] = window_terms(act_by_acct.get(a, {}), dt.date.fromisoformat(w["anchor"]),
                                      dt.date.fromisoformat(w["first_trading_day"]), R)
        T[a]["since_inception"] = None

    # household window terms: sums with the absent rule
    H = {}
    for name in ("qtd", "ytd", "last_12_months"):
        terms = [T[a][name] for a in accounts]
        H[name] = {}
        for key in ("beginning_value", "net_additions", "net_gain", "ending_value", "contributions",
                    "withdrawals", "income"):
            H[name][key] = hh_sum(terms, key)
        H[name]["days"] = [t["days"] for t in terms]
    H["since_inception"] = None

    # identity checks and the proof read (counts only in the record; the detail goes to PROOF_READ.txt)
    proof_lines = []
    checks = 0
    passed = 0
    per_scope_checks = {}

    def check(scope, name, tset):
        nonlocal checks, passed
        keys = ("beginning_value", "net_additions", "net_gain", "ending_value")
        vals = [tset[k] for k in keys]
        if any(isinstance(v, Absent) for v in vals):
            proof_lines.append("%s %s: NOT GRADED (%s)" % (scope, name, "; ".join(
                sorted({v.reason[:60] for v in vals if isinstance(v, Absent)}))))
            return
        gap = vals[0] + vals[1] + vals[2] - vals[3]
        checks += 1
        ok = abs(gap) <= TOL
        passed += 1 if ok else 0
        per_scope_checks[scope] = per_scope_checks.get(scope, 0) + 1
        proof_lines.append("%s %s: gap=%.2f %s" % (scope, name, gap, "PASS" if ok else "FAIL"))

    for name in CHECK_WINDOWS:
        check("household", name, H[name])
        for a in accounts:
            check("account", name, T[a][name])

    # the sample
    values = {}
    contract_absent = 0
    for m in members:
        src = m["source"]
        if src == "ABSENT":
            contract_absent += 1
    result = build_values(members, accounts, T, H, wdefs, R, reader, naming, tc, act_by_acct, sibling_tables,
                          hh_hash, counts)
    values.update(result)
    missing = [i for i in member_ids if i not in values]
    if missing:
        raise SystemExit("ERROR: %d member ids were not assigned a value (first: %s)" % (len(missing), missing[0]))

    form = to_form(values)
    filled = 0
    absent = 0
    for mid in member_ids:
        if is_absent_form(form[mid]):
            absent += 1
        else:
            filled += 1
    total = len(member_ids)
    problems = shape_problems(members, form)
    counts_members = {"total": total, "filled": filled, "absent": absent, "contract_absent": contract_absent,
                      "absent_forms_inside_filled_members": count_inner_absent(form, member_ids)}
    shape_ok = (not problems) and filled + absent == total and absent >= contract_absent

    # the sample: private only
    layout = {
        "household": {
            "household_ref": hh_hash,
            "as_of": R.isoformat(),
            "accounts": [{"account_key": a, "last_four": a[-4:]} for a in accounts],
        },
        "windows": wdefs,
        "values": form,
        "rows": build_rows(accounts, T, H, wdefs, R, reader, naming, tc, act_by_acct),
    }
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "HOUSEHOLD_SAMPLE.json"), "w", encoding="utf-8") as fh:
        json.dump(layout, fh, indent=1, sort_keys=True)
    with open(os.path.join(out, "PROOF_READ.txt"), "w", encoding="utf-8") as fh:
        fh.write("PROOF READ (private; for the issuer; never in the repo)\n")
        fh.write("reference R=%s window anchors: %s\n" % (R.isoformat(), json.dumps(wdefs, sort_keys=True)))
        for line in proof_lines:
            fh.write(line + "\n")
        fh.write("household value summary: %s\n" % json.dumps(to_form({k: H[k] for k in CHECK_WINDOWS}), default=str,
                                                              sort_keys=True))

    counts.update({
        "members_total": total,
        "members_filled": filled,
        "members_absent": absent,
        "members_contract_absent": contract_absent,
        "absent_forms_inside_filled_members": counts_members["absent_forms_inside_filled_members"],
        "fields_checked_against_sibling_contracts": fields_checked,
        "shape_problems": problems,
        "shape_valid_against_contract": shape_ok,
        "absent_members_never_zero": all(is_absent_form(form[m["id"]]) for m in members if m["source"] == "ABSENT"),
        "identity_checks": checks,
        "identity_passed": passed,
        "identity_checks_per_scope": per_scope_checks,
        "identity_tolerance_dollars": TOL,
        "gold_tables_read": sorted(set(sibling_tables.values()) | {"account_activity_daily", "account_return_daily"}),
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


def build_values(members, accounts, T, H, wdefs, R, reader, naming, tc, act_by_acct, sibling_tables, hh_hash, counts):
    """Every member id is assigned here exactly once. Unknown sourced ids raise (no silent absent)."""
    out = {}
    cs_reason = ("carried by the client summary, which this build does not read (the issuer's ruling keeps the client "
                 "summary and the investor-reporting directory out of scope)")
    si_reason = ("the since-inception window opens on the account's first_data_date, which the client summary carries; "
                 "the client summary is not read in this build, so the window is not built")

    # gold tables needed for lots, class and fee basis
    lot_r = gold_rows(reader, naming, sibling_tables[LOT_R_CONTRACT], ["account_id", "business_date", "cost_basis",
                                                                     "proceeds", "realized_gain", "holding_term"],
                      accounts)
    lot_u = gold_rows(reader, naming, sibling_tables[LOT_U_CONTRACT], ["account_id", "business_date", "cost_basis",
                                                                      "unrealized_gain"], accounts)
    cls = gold_rows(reader, naming, sibling_tables[CLS_CONTRACT], ["account_id", "business_date", "asset_class",
                                                                   "market_value_eod"], accounts)
    counts["lot_realized_rows_read"] = len(lot_r)
    counts["lot_unrealized_rows_read"] = len(lot_u)
    counts["class_rows_read"] = len(cls)

    lot_r_by = {}
    for r in lot_r:
        if r["account_id"] in accounts:
            lot_r_by.setdefault(r["account_id"], []).append(r)
    lot_u_by = {}
    for r in lot_u:
        if r["account_id"] in accounts and r["business_date"] == R.isoformat():
            lot_u_by.setdefault(r["account_id"], []).append(r)
    cls_by = {}
    for r in cls:
        if r["account_id"] in accounts:
            cls_by.setdefault((r["account_id"], r["business_date"]), {}).setdefault(r["asset_class"], 0.0)
            cls_by[(r["account_id"], r["business_date"])][r["asset_class"]] += float(r["market_value_eod"])
    del lot_r, lot_u, cls

    l12_anchor = dt.date.fromisoformat(wdefs["last_12_months"]["anchor"])
    l12_days = sorted({d for a in accounts for d in act_by_acct.get(a, {}) if l12_anchor.isoformat() < d <= R.isoformat()})
    fee_label = fee_basis_label(reader, naming, counts)

    def per_account(fn):
        return {a: fn(a) for a in accounts}

    for m in members:
        mid = m["id"]
        src = m["source"]
        parts = mid.split(".")
        if src == "ABSENT":
            out[mid] = Absent(m["reason"])
            continue
        if isinstance(src, dict) and CS_MARK in src.get("contract", ""):
            out[mid] = Absent(cs_reason)
            continue
        if parts[0] in ("pvs", "avs") and parts[1] == "since_inception":
            out[mid] = Absent(si_reason)
            continue
        if parts[0] == "pvs":
            term = parts[2]
            out[mid] = H[parts[1]][term] if term in H[parts[1]] else Absent("not built")
            continue
        if parts[0] == "avs":
            term = parts[2]
            out[mid] = per_account(lambda a, w=parts[1], t=term: T[a][w][t])
            continue
        if mid == "hold.ending_value":
            out[mid] = H_end(accounts, act_by_acct, R)
            continue
        if mid == "hold.net_gain_last_12_months":
            out[mid] = H["last_12_months"]["net_gain"]
            continue
        if mid == "hold.net_gain_ytd":
            out[mid] = H["ytd"]["net_gain"]
            continue
        if mid == "hold.net_gain_qtd":
            out[mid] = H["qtd"]["net_gain"]
            continue
        if mid == "hold.net_gain_since_inception":
            out[mid] = Absent(si_reason)
            continue
        if mid == "hold.allocation":
            out[mid] = allocation_at(accounts, cls_by, act_by_acct, R)
            continue
        if parts[0] == "act":
            term, grain = parts[1], parts[2]
            if grain == "household":
                out[mid] = act_value(term, accounts, T, H, act_by_acct, R)
            else:
                out[mid] = per_account(lambda a, t=term: act_account_value(t, a, T, act_by_acct, R))
            continue
        if parts[0] == "trgl":
            out[mid] = per_account(lambda a, k=parts[1]: trgl_value(k, lot_r_by.get(a, []), R))
            continue
        if parts[0] == "glr":
            out[mid] = per_account(lambda a, k=parts[1]: glr_value(k, a, lot_r_by, lot_u_by, act_by_acct, R))
            continue
        if mid == "overview.chart.allocation_by_asset_class":
            out[mid] = class_series(l12_days, accounts, cls_by)
            continue
        if mid == "accounts.chart.allocation_by_account":
            out[mid] = account_series(l12_days, accounts, act_by_acct)
            continue
        if mid == "accounts.chart.ending_value_and_net_additions_last_12_months":
            out[mid] = ending_netadd_series(l12_days, accounts, act_by_acct)
            continue
        if mid == "holdings.rows.class_hierarchy":
            out[mid] = ("class level only: Opal's seven asset-class values (" + ", ".join(CLASS_ENUM) +
                        "); the baseline's sub-class rows are not carried by any sibling, so each sub-class cell is absent")
            continue
        if mid == "convention.fee_basis_label":
            out[mid] = fee_label
            continue
        if mid == "cover.as_of_date":
            out[mid] = Absent(cs_reason)
            continue
        if mid in ("convention.inception_per_household_and_account", "convention.not_held_for_entire_period"):
            out[mid] = Absent(cs_reason)
            continue
        if mid == "overview.chart.portfolio_performance_last_12_months":
            out[mid] = Absent("the household performance line needs a household daily return series, which no sibling carries")
            continue
        raise SystemExit("ERROR: sourced member %s has no builder rule" % mid)
    # account-grain members whose value is a dict keyed by account are checked by shape_problems
    return out


def gold_rows(reader, naming, table, columns, accounts):
    """Rows of the newest partition of one gold table, filtered to the household's accounts (a filter, never a sum)."""
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.parquet as pq
    probe = naming.address("irpt", FIRM, "gold", table, "date=2000-01-01")
    bucket = split_s3(probe)[0]
    newest, n = newest_partition(reader, bucket, "irpt/%s/gold/%s/" % (FIRM, table), DATE_PART, table)
    addr = naming.address("irpt", FIRM, "gold", table, "date=%s" % newest, "data.parquet")
    b, k = split_s3(addr)
    tbl = pq.read_table(io.BytesIO(reader.get(b, k)), columns=columns)
    mask = pc.is_in(tbl["account_id"], value_set=pa.array(sorted(accounts)))
    return tbl.filter(mask).to_pylist()


def fee_basis_label(reader, naming, counts):
    mv = counts.get("activity_method_versions_in_household") or []
    if len(mv) != 1:
        return Absent("the activity rows of the household carry more than one method_version; the fee basis is not one value")
    v = mv[0]
    probe = naming.address("irpt", FIRM, "gold", "dim_return_method", "method_version=%d" % v)
    bucket = split_s3(probe)[0]
    listed = reader.list_prefixes(bucket, "irpt/%s/gold/dim_return_method/" % FIRM)
    have = set()
    for p in listed:
        m = METHOD_PART.search(p)
        if m:
            have.add(int(m.group(1)))
    counts["dim_return_method_versions_landed"] = sorted(have)
    if v not in have:
        return Absent("the method_version the activity rows carry (%d) has no dim_return_method row in gold; "
                      "the landed rows are %s" % (v, sorted(have)))
    import pyarrow.parquet as pq
    addr = naming.address("irpt", FIRM, "gold", "dim_return_method", "method_version=%d" % v, "data.parquet")
    b, k = split_s3(addr)
    rows = pq.read_table(io.BytesIO(reader.get(b, k)), columns=["fee_basis"]).to_pylist()
    if not rows or rows[0]["fee_basis"] is None:
        return Absent("the dim_return_method row for this method_version holds no fee_basis")
    return "fee basis: %s (returns and gains are before advisory fees)" % rows[0]["fee_basis"]


def H_end(accounts, act_by_acct, R):
    rd = R.isoformat()
    vals = []
    for a in accounts:
        r = act_by_acct.get(a, {}).get(rd)
        vals.append(Absent("no activity row on as_of") if r is None else float(r["ending_value"]))
    return hh_sum([{"v": v} for v in vals], "v")


def allocation_at(accounts, cls_by, act_by_acct, R):
    rd = R.isoformat()
    end_total = H_end(accounts, act_by_acct, R)
    out = {}
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


ACT_TERMS = ("beginning_value", "contributions", "withdrawals", "net_gain", "income", "ending_value")


def act_value(term, accounts, T, H, act_by_acct, R):
    """The household act.* member: the last-12-months window terms, summed with the absent rule."""
    if term not in ACT_TERMS:
        raise SystemExit("ERROR: act term %s has no rule" % term)
    if term == "ending_value":
        return H_end(accounts, act_by_acct, R)
    return H["last_12_months"][term]


def act_account_value(term, a, T, act_by_acct, R):
    if term not in ACT_TERMS:
        raise SystemExit("ERROR: act term %s has no rule" % term)
    if term == "ending_value":
        r = act_by_acct.get(a, {}).get(R.isoformat())
        return Absent("no activity row on as_of") if r is None else float(r["ending_value"])
    return T[a]["last_12_months"][term]


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


def class_series(days, accounts, cls_by):
    out = []
    for d in days:
        tot = 0.0
        per = {}
        for a in accounts:
            dd = cls_by.get((a, d))
            if dd:
                for c, v in dd.items():
                    per[c] = per.get(c, 0.0) + v
                    tot += v
        shares = {}
        for c in CLASS_ENUM:
            if c in per and tot > 0:
                shares[c] = round(per[c] / tot * 100.0, 1)
            else:
                shares[c] = Absent("no class value on this day")
        out.append({"date": d, "shares": shares})
    return out


def account_series(days, accounts, act_by_acct):
    out = []
    for d in days:
        vals = {}
        for a in accounts:
            r = act_by_acct.get(a, {}).get(d)
            vals[a] = Absent("no activity row on this day") if r is None else float(r["ending_value"])
        total = sum(v for v in vals.values() if not isinstance(v, Absent))
        shares = {}
        for a in accounts:
            v = vals[a]
            if isinstance(v, Absent) or total == 0:
                shares[a] = Absent("no ending value on this day")
            else:
                shares[a] = round(v / total * 100.0, 1)
        out.append({"date": d, "shares": shares})
    return out


def ending_netadd_series(days, accounts, act_by_acct):
    out = []
    for d in days:
        ends = []
        nets = []
        for a in accounts:
            r = act_by_acct.get(a, {}).get(d)
            if r is None:
                ends.append(Absent("no row"))
                nets.append(Absent("no row"))
            else:
                ends.append(float(r["ending_value"]))
                nets.append(float(r["contributions"]) - float(r["withdrawals"]))
        out.append({"date": d,
                    "ending_value": hh_sum([{"v": x} for x in ends], "v"),
                    "net_additions": hh_sum([{"v": x} for x in nets], "v")})
    return out


def build_rows(accounts, T, H, wdefs, R, reader, naming, tc, act_by_acct):
    rows = {
        "account": [{"account_key": a, "label": {"absent": "registration name not held by any sibling contract; "
                                                           "the label carries the last four digits until a name source exists"},
                     "last_four": a[-4:]} for a in accounts],
        "class_household": [{"class": c, "allocation_percent": "see values hold.allocation"} for c in CLASS_ENUM],
        "class_sub_class": Absent("sub-class rows are not carried by any sibling contract").reason,
    }
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python -I build_sample.py <repo_root> <private_out_dir>")
    sys.exit(main(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])))
