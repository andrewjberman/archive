"""build_sample_inflection.py -- the INFLECTION SAMPLE: one household of several accounts, built IN MEMORY from the
firm's own Orion silver through the round-108 adapter (data/assets/scripts/gold/irpt_reporting/adapters/
inflection_account_dim.py), into the performance-report contract's filled-report shape (document.filled_report).

Order: IRPT_DASHBD.TO-DB-b-214 (round 109, cell DB-b-214), issuer 2.0.0_SA_COO~D2, serial 0.9.0_WK_IRPT_DASHBD~173.
Shape, units, absent forms with kinds, and the model benchmark members and 12-month chart (through the DB-b-204 reader)
are those of the sibling builder (0.9.0_WK_IRPT_DASHBD~169). Every read of that builder's gold tables is replaced by a
read of the firm's silver, and every member whose figure needs an account return table that this firm does not yet
have is absent in words with its kind.

Run: python -I build_sample_inflection.py <repo_root> --out <private_out_dir>

WRITES (private folder only): HOUSEHOLD_SAMPLE.json, PROOF_READ.txt, BUILD_COUNTS.json. Nothing is written to the repo
and nothing is written to S3.

READS (S3 LIST and GET only; no put, copy, delete, vendor call or secret read):
  - the adapter's GET-only reader (InflectionSilverReader), over the two granted prefixes: the newest date= partition of
    fact_positions and fact_assets (one as-of date each), of fact_transactions and fact_performance (their newest
    partition holds the full history); no other partition is listed or read;
  - the served model series, one GET of the served object through the DB-b-204 reader (model_series_windows.py).

HOUSEHOLD RULE (the rule the checker recomputes): among the households of the adapter's account_dim table with 2 or more
accounts, the one whose sha256 of its household id (utf-8, hex digest) sorts lowest. The household id is the Orion
clientId the adapter keys on. The account set is the adapter's account_dim membership of that household.

AS OF: the newest fact_positions partition. Every row of it carries that asOfDate (checked, else the build stops).

ACCOUNT IDENTITY: account_id is the adapter's account key (the Orion account id that account_dim carries). last4 is the
last four characters of the custodian account number carried on the account's fact_positions rows.

FIRST DATA DATE OF AN ACCOUNT (no account return table exists for this firm yet): the earliest transDate of the account
in the newest fact_transactions partition; an account with no transaction there takes the earliest createdDate of its
fact_positions rows. The household's first data date is the earliest of its accounts' first data dates.

WINDOW STATUS (no account return table yet): the window's opening anchor is the last trading day before the window's
first day (lib/trading_calendar.py); NOT_SPANNED where the account's first data date is after that anchor; otherwise
BREAK, because no account return row exists for the window's days. since_inception opens on the account's first data
date and so reads BREAK. This is a derivation from the span, named as such in the record, and is ruled by the CTO.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
import re
import sys

ADAPTER_REL = "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_dim.py"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/adapters/model_series_windows.py"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
ORION_SILVER = "s3://opal-data-assets/orion/inflection/silver/"
TOL = 1.0
MIN_ACCOUNTS = 2
KINDS = ("NO_SOURCE_YET", "INSUFFICIENT_HISTORY", "SOURCE_BREAK")
NSY, IH, SB = KINDS[0], KINDS[1], KINDS[2]
UNHELD = "UNHELD"
CLASS_ENUM = ["cash", "fixed_income", "equity", "structured", "alternatives", "commodities", "unclassified"]
WIN_KEYS = ("qtd", "ytd", "last_12_months", "since_inception")
WINDOW_STATUS_VALUES = ("MEASURED", "NOT_SPANNED", "BREAK")
CHART_ID = "overview.chart.portfolio_performance_last_12_months"
ACCT_WORDS = "Account-level returns are not available for this firm yet."
LOTS_SENTENCE = "Lot-level detail is not available for this account yet."
DATE_RX = re.compile(r"\d{4}-\d{2}-\d{2}")
DATE_PART = re.compile(r"date=(\d{4}-\d{2}-\d{2})/$")
RET_WORDS = ("Opal has no account return table for this firm yet, so no account-grain beginning value, net additions "
             "or net gain is read; a later cell derives the account returns from positions and transactions.")
SPLIT_REASON = ("Opal does not split net additions into contributions, withdrawals and income yet, so no source holds "
                "this figure")
ALLOC_WORDS = ("Opal's seven asset-class values for this firm's holdings come from a classification table this build "
               "does not read, so no class share is taken; a cash share from custodial lines alone would omit the "
               "money-market funds the class rule counts as cash.")
CHART_WORDS = ("the chart needs a twelve-month series of this firm's holdings by class or by account, which this build "
               "does not read yet")
FEE_REASON = ("the fee-basis row is outside this build's grant: the gold dim_return_method table is not read, so the "
              "fee-basis label is absent in words")
CS_WORDS = ("carried by the client summary, which this build does not read (the issuer's ruling keeps the client "
            "summary and the investor-reporting directory out of scope)")
# the window-status words of an account whose first data date is after its window's anchor, and of one that spans it
NOT_SPANNED_WORDS = ("NOT_SPANNED: the account has no data on the window's opening anchor day, so it did not hold a value "
                     "at the window's start (the not-held dash)")


class Absent(object):
    """An absent form: no value for this term, the reason in words, and the kind (one of KINDS). A kind is required."""

    def __init__(self, reason, kind):
        if kind not in KINDS:
            raise SystemExit("ERROR: an absent form needs a kind of %s, got %r" % (list(KINDS), kind))
        self.reason = reason
        self.kind = kind


class ServedGet(object):
    """The served-series reader: one GET of the served object through the adapter's reader client. No other call."""

    def __init__(self, reader, bucket, key):
        self._reader = reader
        self._bucket = bucket
        self._key = key

    def get_object(self, bucket, key):
        if (bucket, key) != (self._bucket, self._key):
            raise PermissionError("the served-series reader is granted one object only")
        self._reader.reads += 1
        resp = self._reader._api().get_object(Bucket=bucket, Key=key)
        return resp["Body"].read(), resp.get("VersionId")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit("ERROR: the module %s is not loadable" % path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def newest_partition(reader, table):
    parts = reader.list_partitions(ORION_SILVER + table)
    if not parts:
        raise SystemExit("ERROR: no date partition under %s" % table)
    return parts[-1]


def read_columns(reader, table, part, columns):
    """The named columns of one silver data.parquet, as a list of row dicts (one GET; the grant is checked by the reader)."""
    import pyarrow.parquet as pq
    uri = ORION_SILVER + table + "/" + part + "/data.parquet"
    bucket, key = reader._split(uri)
    body = reader._api().get_object(Bucket=bucket, Key=key)["Body"].read()
    reader.reads += 1
    return pq.read_table(io.BytesIO(body), columns=columns).to_pylist()


def clean_text(adapter, v):
    return adapter._clean(v)


def pick_household(rows):
    """The household the checker recomputes: among households with 2 or more accounts, the lowest sha256 of the id."""
    by = {}
    for r in rows:
        if r.get("household_id"):
            by.setdefault(str(r["household_id"]), set()).add(str(r["account_id"]))
    elig = {h: a for h, a in by.items() if len(a) >= MIN_ACCOUNTS}
    if not elig:
        return None, set(), 0
    h = min(elig, key=lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())
    return h, elig[h], len(elig)


def to_form(v):
    if isinstance(v, Absent):
        return {"absent": v.reason, "kind": v.kind}
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
    return isinstance(v, dict) and set(v.keys()) == {"absent", "kind"} and isinstance(v["absent"], str) and v["kind"] in KINDS


def absent_forms(v):
    if isinstance(v, dict) and "absent" in v:
        yield v
    elif isinstance(v, dict):
        for x in v.values():
            for y in absent_forms(x):
                yield y
    elif isinstance(v, list):
        for x in v:
            for y in absent_forms(x):
                yield y


def measured_leaves(v):
    if is_absent_form(v) or v == UNHELD:
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
    return not any(True for _ in measured_leaves(v))


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
        for af in absent_forms(v):
            if not is_absent_form(af):
                problems.append("an absent form at %s is not exactly {absent, kind} with a kind of %s" % (m["id"], list(KINDS)))
            elif not af["absent"].strip():
                problems.append("empty absent reason at %s" % m["id"])
        if isinstance(v, dict) and "by_row" in v:
            for key, x in v["by_row"].items():
                if x == UNHELD and key not in CLASS_ENUM:
                    problems.append("UNHELD outside an asset-class key at %s[%s]" % (m["id"], key))
        elif v == UNHELD:
            problems.append("UNHELD outside a by_row asset-class map at %s" % m["id"])
        for leaf in leaves(v):
            if leaf is None:
                problems.append("null leaf at %s" % m["id"])
            elif isinstance(leaf, bool):
                problems.append("boolean leaf at %s" % m["id"])
    if len(set(ids)) != len(ids):
        problems.append("duplicate member ids")
    return problems


def layout_problems(members, layout):
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
        if sorted(ws.keys()) != sorted(WIN_KEYS) or any(v not in WINDOW_STATUS_VALUES for v in ws.values()):
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


def absent_window(rows, lo, R, tc):
    """(reason in words, kind) of a model window the served series does not hold whole."""
    if not rows or rows[0][0] > lo:
        return "the model series does not open on the window's first day %s" % lo.isoformat(), IH
    have = set(d for d, _ in rows)
    miss = [d for d in tc.trading_days_between(lo, R) if d not in have]
    if miss:
        return "the model series holds no return on %d trading day(s) of the window" % len(miss), SB
    return "the model series holds no day of the window", SB


def bench_value(mid, src, series, windows, R, hh_first, mod, tc):
    stem = MODEL_STEMS.get(src.get("served_name"))
    if stem is None or not mid.endswith(stem):
        raise SystemExit("ERROR: member %s names served name %r, which is not its stem" % (mid, src.get("served_name")))
    win = next(w for w in WIN_KEYS if ("." + w + ".") in mid)
    val = windows[stem][win]
    if val is not None:
        return val
    lo = mod._model_lo(win, R, dt.date.fromisoformat(str(hh_first)[:10]))
    reason, kind = absent_window(series[stem], lo, R, tc)
    return Absent(reason, kind)


def cumulative_points(rows, lo, R):
    prod, pts = 1.0, []
    for d, x in rows:
        if lo <= d <= R:
            prod *= 1.0 + x
            pts.append({"date": d.isoformat(), "value": round((prod - 1.0) * 100.0, 1)})
    return pts


def chart_value(series, windows, R, hh_first, mod, tc):
    lo = mod._model_lo("last_12_months", R, dt.date.fromisoformat(str(hh_first)[:10]))
    out = []
    for served, stem in MODEL_STEMS.items():
        if windows[stem]["last_12_months"] is None:
            reason, kind = absent_window(series[stem], lo, R, tc)
            return Absent("chart series %s: %s" % (served, reason), kind)
        out.append({"name": served, "points": cumulative_points(series[stem], lo, R)})
    return out


MODEL_STEMS = {"Ultra-Short Term": "benchmark_ultra_short_term", "Short Term": "benchmark_short_term",
               "Intermediate Term": "benchmark_intermediate_term", "Long Term": "benchmark_long_term"}


def main(repo, out):
    sys.path.insert(0, repo)
    from lib import trading_calendar as tc
    adapter = load_module("inflection_account_dim", os.path.join(repo, ADAPTER_REL))
    mod = load_module("model_series_windows", os.path.join(repo, MODULE_REL))
    with open(os.path.join(repo, CONTRACT_REL), "rb") as fh:
        contract = json.loads(fh.read().decode("utf-8"))
    members = contract["members"]
    member_ids = [m["id"] for m in members]
    if len(set(member_ids)) != len(member_ids):
        raise SystemExit("ERROR: contract member ids are not unique")

    reader = adapter.InflectionSilverReader()
    counts = {"firm": "inflection", "contract_version": contract["contract_version"], "members_in_contract": len(members)}

    # 1. the as-of: the newest fact_positions partition; the account universe: the adapter's account_dim
    pos_part, pos = reader.latest_partition(ORION_SILVER + "fact_positions")
    asset_part, assets = reader.latest_partition(ORION_SILVER + "fact_assets")
    as_of_iso = pos_part[len("date="):]
    R = dt.date.fromisoformat(as_of_iso)
    if set(str(x) for x in pos["asOfDate"].tolist()) != {as_of_iso}:
        raise SystemExit("ERROR: fact_positions asOfDate does not equal its partition date %s" % as_of_iso)
    dim_rows = adapter.build_account_dim(pos, assets).to_pylist()
    counts["account_dim_rows"] = len(dim_rows)
    counts["account_dim_households"] = len({r["household_id"] for r in dim_rows if r["household_id"]})
    counts["account_dim_coverage"] = {c: sum(1 for r in dim_rows if r["coverage"] == c) for c in sorted({r["coverage"] for r in dim_rows})}
    hh_id, accts_set, n_elig = pick_household(dim_rows)
    if hh_id is None:
        raise SystemExit("ERROR: no household with 2 or more accounts in the account dimension")
    accounts = sorted(accts_set)
    hh_int = int(hh_id)
    hh_hash = hashlib.sha256(hh_id.encode("utf-8")).hexdigest()
    counts["households_with_2_or_more_accounts"] = n_elig
    counts["household_accounts"] = len(accounts)
    counts["household_ref_sha256"] = hh_hash
    counts["as_of"] = as_of_iso
    aset = set(accounts)

    # 2. positions of the household at as_of: market value per account, custodian last four, creation dates
    mv, mv_null, rows_n, last4, created = {}, {}, {}, {}, {}
    for a in accounts:
        mv[a], mv_null[a], rows_n[a] = 0.0, 0, 0
    for aid, val, num, cd in zip(pos["accountId"].tolist(), pos["currentValue"].tolist(),
                                 pos["accountNumber"].tolist(), pos["createdDate"].tolist()):
        a = clean_text(adapter, aid)
        if a not in aset:
            continue
        rows_n[a] += 1
        if val is None or val != val:
            mv_null[a] += 1
        else:
            mv[a] += float(val)
        n = clean_text(adapter, num)
        if n and a not in last4:
            last4[a] = n[-4:]
        c = clean_text(adapter, cd)
        if c and DATE_RX.fullmatch(c[:10]) and (a not in created or c[:10] < created[a]):
            created[a] = c[:10]
    counts["positions_rows_household"] = sum(rows_n.values())
    counts["account_positions_rows"] = {a: rows_n[a] for a in accounts}
    missing_last4 = [a for a in accounts if a not in last4]
    if missing_last4:
        raise SystemExit("ERROR: %d account(s) carry no custodian account number on positions" % len(missing_last4))

    # 3. first data dates: the newest fact_transactions partition (full history), else the creation date of positions
    tx_part = newest_partition(reader, "fact_transactions")
    tx_rows = read_columns(reader, "fact_transactions", tx_part, ["accountId", "transDate"])
    tx_first = {}
    for r in tx_rows:
        a = clean_text(adapter, r["accountId"])
        if a not in aset:
            continue
        d = clean_text(adapter, r["transDate"])
        if d and DATE_RX.fullmatch(d[:10]) and (a not in tx_first or d[:10] < tx_first[a]):
            tx_first[a] = d[:10]
    del tx_rows
    first, first_src = {}, {}
    for a in accounts:
        if a in tx_first:
            first[a], first_src[a] = tx_first[a], "transactions"
        elif a in created:
            first[a], first_src[a] = created[a], "positions_created"
        else:
            raise SystemExit("ERROR: no first data date can be read for one account of the household")
    counts["first_date_source_counts"] = {s: sum(1 for a in accounts if first_src[a] == s) for s in sorted(set(first_src.values()))}
    hh_first = min(first.values())
    dt.date.fromisoformat(hh_first)

    # 4. the household's client performance (newest partition): the window-open measurement, words and counts only
    perf_part = newest_partition(reader, "fact_performance")
    perf_rows = read_columns(reader, "fact_performance", perf_part, ["client_id", "date", "factor"])
    perf_dates = set()
    for r in perf_rows:
        if clean_text(adapter, r["client_id"]) == str(hh_int) and r["factor"] is not None and DATE_RX.fullmatch(str(r["date"])[:10]):
            perf_dates.add(str(r["date"])[:10])
    del perf_rows
    counts["client_performance_dates"] = len(perf_dates)
    counts["client_performance_first"] = min(perf_dates) if perf_dates else None
    counts["client_performance_partition"] = perf_part[len("date="):]

    # 5. the trading-day anchors and the account window statuses (the derivation named in the module header)
    anchor = {}
    for name in ("qtd", "ytd", "last_12_months"):
        anchor[name] = tc.prev_trading_day(window_start(name, R))
    windows_open = {}
    for name in ("qtd", "ytd", "last_12_months"):
        windows_open[name] = (anchor[name].isoformat() in perf_dates) and (min(perf_dates) <= anchor[name].isoformat() if perf_dates else False)
    windows_open["since_inception"] = bool(perf_dates) and (R.isoformat() in perf_dates)
    counts["client_performance_opens_on_anchor"] = windows_open
    STATUS = {}
    for a in accounts:
        STATUS[a] = {}
        for name in ("qtd", "ytd", "last_12_months"):
            STATUS[a][name] = "NOT_SPANNED" if dt.date.fromisoformat(first[a]) > anchor[name] else "BREAK"
        STATUS[a]["since_inception"] = "BREAK"

    # 6. the served model series (one GET) and its windows
    series, claim = mod.read_served_series(ServedGet(reader, mod.SERVED_BUCKET, mod.SERVED_KEY))
    model_windows = mod.windows_from_series(series, R, hh_first)
    counts["model_series_trading_days"] = {s: len(v) for s, v in sorted(series.items())}
    counts["model_source"] = claim

    # 7. the members
    values = build_values(members, accounts, mv, mv_null, first, STATUS, R, hh_first, series, model_windows, mod, tc)
    missing = [i for i in member_ids if i not in values]
    if missing:
        raise SystemExit("ERROR: %d member ids were not assigned a value (first: %s)" % (len(missing), missing[0]))
    form = to_form(values)
    filled = sum(1 for mid in member_ids if not fully_absent(form[mid]))
    total = len(member_ids)
    absent = total - filled
    contract_absent = sum(1 for m in members if m["source"] == "ABSENT")
    accts_out = [{"account_id": a, "last4": last4[a], "first_data_date": first[a], "window_status": STATUS[a]}
                 for a in accounts]
    layout = {
        "household": {
            "household_ref": hh_hash,
            "as_of": R.isoformat(),
            "first_data_date": hh_first,
            "accounts": accts_out,
        },
        "values": form,
    }
    problems = shape_problems(members, form) + layout_problems(members, layout)
    shape_ok = (not problems) and filled + absent == total and absent >= contract_absent
    filled_windows = [w for w in ("qtd", "ytd", "last_12_months", "since_inception")
                      if not (isinstance(form["pvs.%s.return_cumulative" % w], dict) and "absent" in form["pvs.%s.return_cumulative" % w])]
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "HOUSEHOLD_SAMPLE.json"), "w", encoding="utf-8") as fh:
        json.dump(layout, fh, indent=1, sort_keys=True)
    with open(os.path.join(out, "PROOF_READ.txt"), "w", encoding="utf-8") as fh:
        fh.write("PROOF READ (private; for the issuer; never in the repo)\n")
        fh.write("reference R=%s anchors: %s\n" % (R.isoformat(), json.dumps({k: v.isoformat() for k, v in anchor.items()}, sort_keys=True)))
        fh.write("household first data date %s; accounts first-date source %s\n" % (hh_first, json.dumps(first_src, sort_keys=True)))
        fh.write("household market value at as_of: %s\n" % json.dumps(round(sum(mv.values()), 2)))

    counts.update({
        "members_total": total,
        "members_filled": filled,
        "members_absent": absent,
        "members_contract_absent": contract_absent,
        "absent_forms_inside_filled_members": count_inner_absent(form, member_ids),
        "shape_problems": problems,
        "shape_valid_against_contract": shape_ok,
        "household_return_windows": filled_windows,
        "outcome": "BUILT",
    })
    counts["s3_reads"] = reader.reads
    counts["s3_writes"] = 0
    with open(os.path.join(out, "BUILD_COUNTS.json"), "w", encoding="utf-8") as fh:
        json.dump(counts, fh, indent=1, sort_keys=True, default=str)
    print(json.dumps({k: v for k, v in counts.items() if k not in ("account_positions_rows",)}, indent=1, sort_keys=True, default=str))
    return 0


def build_values(members, accounts, mv, mv_null, first, STATUS, R, hh_first, series, model_windows, mod, tc):
    """Every member id is assigned here. Unknown sourced ids raise (no silent absent)."""
    out = {}
    rd = R.isoformat()
    hh_absent = [a for a in accounts if mv_null[a]]
    if hh_absent:
        household_mv = Absent("a position of an account carries no market value on as_of, so the household value is not read", SB)
    else:
        household_mv = round(sum(round(mv[a], 2) for a in accounts), 2)
    acct_mv = {a: (Absent("a position of this account carries no market value on as_of", SB) if mv_null[a]
                   else round(mv[a], 2)) for a in accounts}

    def per_account(fn):
        return {"by_row": {a: fn(a) for a in accounts}}

    lot_lines = LOTS_SENTENCE + " No lot source is read for this firm yet (coverage NO_LOTS)."
    for m in members:
        mid = m["id"]
        src = m["source"]
        parts = mid.split(".")
        if src == "ABSENT":
            out[mid] = Absent(m["reason"], NSY)
            continue
        if isinstance(src, dict) and src.get("input") == "model_portfolio_timeseries":
            if mid == CHART_ID:
                out[mid] = chart_value(series, model_windows, R, hh_first, mod, tc)
            else:
                out[mid] = bench_value(mid, src, series, model_windows, R, hh_first, mod, tc)
            continue
        if mid == "cover.as_of_date":
            out[mid] = rd
            continue
        if mid == "convention.inception_per_household_and_account":
            out[mid] = hh_first
            continue
        if mid == "convention.not_held_for_entire_period":
            out[mid] = Absent(CS_WORDS, NSY)
            continue
        if mid == "convention.fee_basis_label":
            out[mid] = Absent(FEE_REASON, NSY)
            continue
        if mid == "holdings.rows.class_hierarchy":
            out[mid] = Absent(ALLOC_WORDS, NSY)
            continue
        if mid == "hold.allocation":
            out[mid] = {"by_row": {c: Absent(ALLOC_WORDS, NSY) for c in CLASS_ENUM}}
            continue
        if mid in ("overview.chart.allocation_by_asset_class", "accounts.chart.allocation_by_account",
                   "accounts.chart.ending_value_and_net_additions_last_12_months"):
            out[mid] = Absent(CHART_WORDS, NSY)
            continue
        if parts[0] == "pvs" and len(parts) == 3:
            if parts[2] == "ending_value":
                out[mid] = household_mv
            else:
                out[mid] = Absent(RET_WORDS, NSY)
            continue
        if mid == "hold.ending_value" or mid == "act.ending_value.household":
            out[mid] = household_mv
            continue
        if mid == "act.ending_value.account":
            out[mid] = per_account(lambda a: acct_mv[a])
            continue
        if parts[0] == "avs" and len(parts) == 3:
            if parts[2] == "ending_value":
                out[mid] = per_account(lambda a: acct_mv[a])
            elif parts[2] == "return_cumulative":
                out[mid] = per_account(lambda a: Absent(ACCT_WORDS, NSY))
            else:
                out[mid] = per_account(lambda a: Absent(RET_WORDS, NSY))
            continue
        if parts[0] == "act" and len(parts) == 3:
            if parts[1] in ("contributions", "withdrawals", "income"):
                out[mid] = Absent(SPLIT_REASON, NSY)
            else:
                out[mid] = Absent(RET_WORDS, NSY) if parts[2] == "household" else per_account(lambda a: Absent(RET_WORDS, NSY))
            continue
        if mid.startswith("hold.net_gain_"):
            out[mid] = Absent(RET_WORDS, NSY)
            continue
        if parts[0] in ("trgl", "glr") and len(parts) == 2:
            out[mid] = per_account(lambda a: Absent(lot_lines, NSY))
            continue
        raise SystemExit("ERROR: sourced member %s has no builder rule" % mid)
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Build the Inflection household sample in memory into a private folder.")
    ap.add_argument("repo_root")
    ap.add_argument("--out", required=True, help="the private output folder (never the repo)")
    args = ap.parse_args()
    sys.exit(main(os.path.abspath(args.repo_root), os.path.abspath(args.out)))
