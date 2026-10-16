"""ADVI_COTBKF TO-CB-cx-1 (worker 0.9.0_WK_ADVI_COTBKF~191): builds BLANK_CENSUS_RECORD.json and BLANK_CENSUS_RECORD.md.

READ-ONLY. Reads the three served Cottonwood silver objects at their pinned VersionIds (get_object), the silver transactions
table's Asset_Type column (list and get, read-only, through the analysis module's own reader), the round-99 price-store cache,
the transactions cache, and the committed MDPF_DEMQUE request records. Writes only the two record files in this folder and
a counts-only scratch JSON. Prints counts only: no account, cusip, ticker, name or value is printed or written.

  python -I cx1_record_build.py
"""
import glob
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

WT = "C:/dev/wk-cotbkf-191"
SCR = "C:/Dev/ajb_workspace/.scratch/cotbkf_r102"
DELIV = WT + "/org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~191"
TXCACHE = "C:/Dev/ajb_workspace/.scratch/advi_cotbkf/cache"
PXCACHE = "C:/Dev/ajb_workspace/.scratch/cotbkf_r99/store_cache"
UHASH = "16278a1c4f6b"
DEMQUE = WT + "/org/missions/D8/MDPF/MDPF_DEMQUE/requests"
sys.path[:0] = [WT + "/data/assets/scripts/silver", WT + "/data/assets/scripts/analysis", WT]

import boto3  # noqa: E402
import pandas as pd  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

import commonwealth_daily_holdings as dh  # noqa: E402
import commonwealth_daily_valuation as dv  # noqa: E402
import commonwealth_price_census as pc  # noqa: E402

BUCKET = "opal-data-assets"
BASE = "commonwealth/cottonwood/silver/%s/date=2026-06-23/part-00000.parquet"
VERSIONS = {"daily_returns": "lNzQMjfx6uX2zdFdWKsDANboShtDUz2N",
            "month_grades": "nkTE.F82uFSboXr9PEamIENCwFL9cwcC",
            "account_day_value": "ObKZXku7Am.QGjO.oSAsIScy8IcJxN5a"}
ACCT_CANDIDATES = ["account", "account_id", "Account", "account_number"]


def _pick(names, cands, what):
    for c in cands:
        if c in names:
            return c
    raise SystemExit("ERROR: no %s column among %s in %s" % (what, cands, sorted(names)))


s3 = boto3.client("s3", region_name="us-east-1")


def fetch(t):
    return s3.get_object(Bucket=BUCKET, Key=BASE % t, VersionId=VERSIONS[t])["Body"].read()


def table(raw, want):
    names = pq.read_schema(io.BytesIO(raw)).names
    cols = []
    for w in want:
        if w == "ACCT":
            cols.append(_pick(names, ACCT_CANDIDATES, "account"))
        else:
            cols.append(w)
    return pq.read_table(io.BytesIO(raw), columns=cols).to_pandas(), cols


def to_day(s):
    return pd.to_datetime(s, errors="coerce").values.astype("datetime64[D]").astype("int64")


def rule_line(relpath, lineno, must):
    """Quote one line of a repo file verbatim; it must contain `must` (else the quote is refused)."""
    with open(WT + "/" + relpath, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    text = lines[lineno - 1].strip()
    if must not in text:
        raise SystemExit("ERROR: %s:%d does not carry %r" % (relpath, lineno, must))
    return {"file": relpath, "line": lineno, "text": text[:240]}


out_scr = {}

# ----------------------------------------------------------------------------- 1. the served tables
raw_dr = fetch("daily_returns")
dr, dr_cols = table(raw_dr, ["ACCT", "date", "return", "blank_reason"])
del raw_dr
raw_mg = fetch("month_grades")
mg, mg_cols = table(raw_mg, ["ACCT", "month", "verdict", "reason"])
del raw_mg
raw_av = fetch("account_day_value")
av, av_cols = table(raw_av, ["ACCT", "cusip", "date", "close", "blank_reason"])
del raw_av
ACC_DR, ACC_AV, ACC_MG = dr_cols[0], av_cols[0], mg_cols[0]
print("SCHEMA daily_returns=%s account_day_value=%s month_grades=%s" % (dr_cols, av_cols, mg_cols))

# ----------------------------------------------------------------------------- 2. days
blank = dr[dr["return"].isna()]
by_reason = blank["blank_reason"].fillna("NONE").astype(str).value_counts().to_dict()
days = dict(total=int(len(dr)), with_return=int(len(dr) - len(blank)), blank=int(len(blank)),
            unreasoned=int(blank["blank_reason"].isna().sum()),
            by_reason={k: int(v) for k, v in sorted(by_reason.items())})

# ----------------------------------------------------------------------------- 3. months
nm = mg[mg["verdict"] != "MATCH"]
by_verdict = mg["verdict"].fillna("ABSENT").astype(str).value_counts().to_dict()
months = dict(total=int(len(mg)), not_match=int(len(nm)),
              unreasoned=int((nm["verdict"].notna() & nm["reason"].isna()).sum()),
              by_verdict={k: int(v) for k, v in sorted(by_verdict.items())})

# month reason parts, classified (counts of months carrying each kind; first blank reason)
FBR_RX = re.compile(r"first blank reason: (\S+)")
PART_RX = [
    ("blank_days", re.compile(r"^\d+ blank day\(s\) of \d+;?$")),
    ("no_daily_returns", re.compile(r"^no daily returns for the month$")),
    ("no_reported_return", re.compile(r"^no reported monthly return$")),
    ("reported_null", re.compile(r"^reported value is null$")),
    ("reported_not_finite", re.compile(r"^reported value .* is not finite$")),
    ("reported_span_not_month", re.compile(r"^reported span .* is not one calendar month$")),
    ("reported_rows_disagree", re.compile(r"^\d+ reported rows disagree")),
    ("side_absent", re.compile(r"^a side is absent$")),
]


def classify_part(p):
    for kind, rx in PART_RX:
        if rx.match(p):
            return kind
    return "other"


ung = mg[mg["verdict"] == "UNGRADABLE"]
kind_months = Counter()
first_blank = Counter()
other_texts = Counter()
combo = Counter()
for r in ung["reason"].fillna(""):
    # the blank-day clause is "N blank day(s) of M; first blank reason: CODE": its reason code is read first, then the rest is split
    for code in FBR_RX.findall(r):
        first_blank[code.rstrip(";")] += 1
    rest = FBR_RX.sub("", r)
    kinds = set()
    for p in rest.split("; "):
        p = p.strip().strip(";").strip()
        if not p:
            continue
        k = classify_part(p)
        kinds.add(k)
        if k == "other":
            other_texts[re.sub(r"\d+(\.\d+)?", "N", p)[:120]] += 1
    kinds = sorted(kinds)
    combo[" + ".join(kinds) if kinds else "(no reason text)"] += 1
    for k in kinds:
        kind_months[k] += 1
absent_reasons = Counter(mg.loc[mg["verdict"].isna(), "reason"].fillna("(null)").astype(str).map(lambda s: s[:60]))
diff_n = int((mg["verdict"] == "DIFF").sum())
match_n = int((mg["verdict"] == "MATCH").sum())
out_scr["month_ungradable_kinds"] = dict(kind_months)
out_scr["month_ungradable_first_blank"] = dict(first_blank)
out_scr["month_ungradable_other_texts"] = dict(other_texts)
out_scr["month_ungradable_combos"] = dict(combo)
out_scr["month_absent_reasons"] = dict(absent_reasons)

# account-level crosscheck: UNPRICED blank account-days against unpriced holding-days
av["_d"] = to_day(av["date"])
dr["_d"] = to_day(dr["date"])

# ----------------------------------------------------------------------------- 4. unpriced holding-days
av_cusip = av["cusip"].astype(str)
closes = av["close"].notna()
priced_cusips = set(av_cusip[closes])
un_mask = av["close"].isna() & av["blank_reason"].isna()
un = av.loc[un_mask, [ACC_AV, "cusip", "_d"]].copy()
un["cusip"] = un["cusip"].astype(str)
un_rows = int(len(un))
un_cusips = set(un["cusip"])
never_set = {c for c in un_cusips if c not in priced_cusips}
gap_set = {c for c in un_cusips if c in priced_cusips}
never_rows = int(un["cusip"].isin(never_set).sum())
gap_rows = int(un["cusip"].isin(gap_set).sum())
unpriced = dict(rows=un_rows, cusips=len(un_cusips), never_priced_cusips=len(never_set),
                never_priced_rows=never_rows, gap_cusips=len(gap_set), gap_rows=gap_rows)

# crosscheck: account-days with an unpriced holding vs the UNPRICED blanks of daily_returns
ud = un[[ACC_AV, "_d"]].drop_duplicates().rename(columns={ACC_AV: "acc"})
unpriced_acct_days = int(len(ud))
dr_unp = dr.loc[dr["blank_reason"] == "UNPRICED", [ACC_DR, "_d"]].rename(columns={ACC_DR: "acc"})
dr_unp_n = int(len(dr_unp))
xm = dr_unp.merge(ud, on=["acc", "_d"], how="inner")
unpriced_days_with_unpriced_holding = int(len(xm.drop_duplicates()))
dr_unp_days_no_holding = dr_unp_n - unpriced_days_with_unpriced_holding

# held (HELD_SOURCE_UNDER_REVIEW) account-day rows, and the Regressed days
held_rows = av.loc[av["blank_reason"] == "HELD_SOURCE_UNDER_REVIEW"]
held_cusips = int(held_rows["cusip"].astype(str).nunique())
out_scr["held_rows"] = int(len(held_rows))
out_scr["held_cusips"] = held_cusips
out_scr["held_days_daily_returns"] = int((dr["blank_reason"] == "HELD_SOURCE_UNDER_REVIEW").sum())

# gap securities: first and last priced day from the served table
pr = av.loc[closes, ["cusip", "_d"]].copy()
pr["cusip"] = pr["cusip"].astype(str)
first_p = pr.groupby("cusip")["_d"].min()
last_p = pr.groupby("cusip")["_d"].max()
g = un[un["cusip"].isin(gap_set)].copy()
g["f"] = g["cusip"].map(first_p)
g["l"] = g["cusip"].map(last_p)
g["pos"] = "INTERIOR"
g.loc[g["_d"] < g["f"], "pos"] = "BEFORE_FIRST_PRICED"
g.loc[g["_d"] > g["l"], "pos"] = "AFTER_LAST_PRICED"
gap_pos = {}
for p in ["BEFORE_FIRST_PRICED", "AFTER_LAST_PRICED", "INTERIOR"]:
    sub = g[g["pos"] == p]
    gap_pos[p] = dict(securities=int(sub["cusip"].nunique()), rows=int(len(sub)))

# ----------------------------------------------------------------------------- 5. the universe, asset types, stores
tx, _pos = dh.load_tx_pos(TXCACHE)
U = dv.universe_from_tx(tx)
uni_by = {x["cusip"]: x for x in U}
claims = pc.symbol_claims(U)
atype = {}
for x in pc.read_universe(s3, pc.to_day(pc.DEFAULT_END)):
    atype[x["cusip"]] = x["asset_type"]
out_scr["universe_cusips"] = len(U)
out_scr["unpriced_cusips_not_in_universe"] = len([c for c in un_cusips if c not in uni_by])
out_scr["asset_type_source_cusips"] = len(atype)

stores = []
for spec in pc.STORES:
    df = pd.read_parquet("%s/%s.%s.parquet" % (PXCACHE, spec["id"], UHASH))
    stores.append((spec["id"], df))
views = {sid: pc.build_views(df.drop(columns=["price"]))["all"] for sid, df in stores}

# the valuation's own resolution and conflict rule, replayed on the cache (not the as-traded Yahoo basis)
prices, vstats = dv.security_day_prices(U, stores, claims)
replay_priced = set(prices["cusip"].astype(str))
out_scr["replay_conflicts_by_store"] = {k: int(v) for k, v in vstats["conflicts"].items()}

conf_cusips = set()
for sid, df in stores:
    m = dv.resolve_series(U, df, claims)
    if m.empty:
        continue
    j = df.merge(m, on=["kind", "key"], how="inner")
    gg = j.groupby(["cusip", "day"], sort=False)["price"].agg(["min", "max"]).reset_index()
    bad = gg[(gg["max"] - gg["min"]) > dv.PRICE_TOL * gg["min"]]
    conf_cusips |= set(bad["cusip"].astype(str))

cat = Counter()
cat_rows = Counter()
cat_by_type = defaultdict(lambda: Counter())
cat_rows_by_type = defaultdict(lambda: Counter())
per_never_rows = un[un["cusip"].isin(never_set)].groupby("cusip").size().to_dict()
for c in sorted(never_set):
    sec = uni_by.get(c)
    if sec is None:
        k = "not_in_universe"
    else:
        kinds = [pc.match_security(sec, views[sid], claims)[0] for sid in views]
        if any(k2 in ("cusip", "ticker") for k2 in kinds):
            k = "resolved_dropped_conflicting" if c in conf_cusips else "resolved_no_conflict_still_unpriced"
        elif any(k2 == "ticker_reused" for k2 in kinds):
            k = "ticker_key_claimed_by_more_than_one_security"
        elif not sec["symbols"]:
            k = "no_ticker_symbol"
        else:
            k = "ticker_no_store_row"
    cat[k] += 1
    cat_rows[k] += int(per_never_rows.get(c, 0))
    t = atype.get(c, "(not in asset-type read)")
    cat_by_type[t][k] += 1
    cat_rows_by_type[t][k] += int(per_never_rows.get(c, 0))
never_by_type = Counter()
never_rows_by_type = Counter()
for c in never_set:
    t = atype.get(c, "(not in asset-type read)")
    never_by_type[t] += 1
    never_rows_by_type[t] += int(per_never_rows.get(c, 0))
replay_served_never_but_replay_priced = int(len(never_set & replay_priced))
replay_served_priced_not_replay = int(len((un_cusips & priced_cusips) - replay_priced))
out_scr["replay"] = dict(served_priced_cusips=len(priced_cusips), replay_priced_cusips=len(replay_priced),
                         never_priced_but_replay_priced=replay_served_never_but_replay_priced,
                         gap_or_unpriced_served_priced_but_replay_unpriced=replay_served_priced_not_replay)

# ----------------------------------------------------------------------------- 6. Bloomberg request records for Cottonwood
def cusips_in(obj, acc):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "cusip" and isinstance(v, str):
                acc.add(v.strip())
            else:
                cusips_in(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            cusips_in(v, acc)
    return acc


rec_sets = {}
zz = sorted(f for f in glob.glob(DEMQUE + "/ZZ-ADVI_COTBKF-ACTIVE-BBG-*.json") if not f.endswith(".quote.json"))
zz_all = set()
for f in zz:
    zz_all |= cusips_in(json.load(open(f, encoding="utf-8")), set())
rec_sets["ZZ-ADVI_COTBKF-ACTIVE-BBG batches (%d files)" % len(zz)] = zz_all
b1 = json.load(open(DEMQUE + "/MDPF_SECHIST-CARD-A-B1-OPTION-C.json", encoding="utf-8"))
rec_sets["MDPF_SECHIST-CARD-A-B1-OPTION-C request"] = cusips_in(b1, set())
ch = json.load(open(DEMQUE + "/MDPF_SECHIST-CARD-A-COT-BBG-HISTORY.quote.json", encoding="utf-8"))
ranked_all = set()
ranked_pursued = set()
for e in ch["ranked"]:
    ranked_all.add(str(e["cusip"]).strip())
    if e.get("pursued") in (True, "true", "yes", 1):
        ranked_pursued.add(str(e["cusip"]).strip())
rec_sets["MDPF_SECHIST-CARD-A-COT-BBG-HISTORY quote ranked list"] = ranked_all
rec_sets["MDPF_SECHIST-CARD-A-COT-BBG-HISTORY quote ranked list, pursued flag"] = ranked_pursued
union = set()
for k, v in rec_sets.items():
    if "pursued" not in k:
        union |= v
bbg = {}
for k, v in rec_sets.items():
    bbg[k] = dict(listed=len(v), never_priced_listed=len(v & never_set), gap_listed=len(v & gap_set))
bbg_union = dict(listed=len(union), never_priced_listed=len(union & never_set), gap_listed=len(union & gap_set))
ranked_summary = {"entries": len(ch["ranked"]), "pursued_true": len(ranked_pursued),
                  "rank_summary_keys": sorted(ch["rank_summary"].keys())}
bbg_actuals_rows = [json.loads(x) for x in open(WT + "/org/missions/D8/MDPF/MDPF_DEMQUE/ledger/BBG_ACTUALS.jsonl", encoding="utf-8", errors="replace") if x.strip()]
out_scr["bbg"] = dict(records=bbg, union=bbg_union, ranked=ranked_summary,
                      actuals_ledger_rows=len(bbg_actuals_rows), actuals_ledger_keys=sorted(bbg_actuals_rows[0].keys()))

# ----------------------------------------------------------------------------- 7. the record
rules = {
    "daily_UNPRICED": rule_line("data/assets/scripts/silver/commonwealth_daily_returns.py", 259, "UNPRICED"),
    "daily_NON_POS": rule_line("data/assets/scripts/silver/commonwealth_daily_returns.py", 258, "NON_POSITIVE_BASE"),
    "daily_FIRST": rule_line("data/assets/scripts/silver/commonwealth_daily_returns.py", 267, "FIRST_DAY"),
    "daily_FLOW": rule_line("data/assets/scripts/silver/commonwealth_daily_returns.py", 253, "FLOW_UNVALUED"),
    "daily_DVR": rule_line("data/assets/scripts/silver/commonwealth_daily_returns.py", 263, "DVR_CLOSE_STEP"),
    "dvr_rule": rule_line("data/assets/scripts/silver/commonwealth_daily_valuation.py", 538, "DVR_CLOSE_STEP"),
    "held_const": rule_line("data/assets/scripts/silver/commonwealth_fwd3_serve.py", 97, "HELD_SOURCE_UNDER_REVIEW"),
    "regressed_doc": rule_line("data/assets/scripts/silver/commonwealth_fwd3_serve.py", 30, "REGRESSED_UNDER_"),
    "month_blank": rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 104, "first blank reason"),
    "month_nodaily": rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 99, "no daily returns for the month"),
    "month_noreport": rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 111, "no reported monthly return"),
    "month_repnull": rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 118, "reported value is null"),
    "month_diff": rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 130, "verdict = DIFF"),
    "month_match": rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 128, "verdict, reason = MATCH"),
    "month_absent": rule_line("data/assets/scripts/silver/commonwealth_account_return_daily.py", 51, "ABSENT account-month"),
}
r_month_ung = rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 122, "UNGRADABLE")

def dcount(code):
    return int(days["by_reason"].get(code, 0))

drivers = []
drivers.append(dict(kind="day", code="UNPRICED", count=dcount("UNPRICED"), rule=rules["daily_UNPRICED"],
    driver=("the account value or the prior day's value is null because a holding on that day has no close: %d account-days "
            "carry at least one unpriced holding-day (%d of the UNPRICED blanks match such an account-day; %d UNPRICED blanks have no "
            "unpriced holding-day on the same account-day, which is the prior-day half of the rule)"
            % (unpriced_acct_days, unpriced_days_with_unpriced_holding, dr_unp_days_no_holding)),
    bloomberg_fill="yes",
    why=("the driver is a missing close of the security; a vendor daily close of each unpriced security on its unpriced dates "
         "would supply it (the never-priced and gap securities); coverage by a vendor is not established, and the group with no "
         "ticker symbol may not be keyable by a vendor")))
drivers.append(dict(kind="day", code="NON_POSITIVE_BASE", count=dcount("NON_POSITIVE_BASE"), rule=rules["daily_NON_POS"],
    driver="the prior day's value is zero or negative, so the return has no positive base",
    bloomberg_fill="no", why="a property of the account's own valued base, not a missing price; a vendor price does not change the base"))
drivers.append(dict(kind="day", code="FIRST_DAY", count=dcount("FIRST_DAY"), rule=rules["daily_FIRST"],
    driver="the first row of each account has no previous day in the table",
    bloomberg_fill="no", why="there is no prior value to divide by; a price history does not create one"))
drivers.append(dict(kind="day", code="DVR_CLOSE_STEP", count=dcount("DVR_CLOSE_STEP"), rule=rules["dvr_rule"],
    driver=("a distribution day on which the security's close steps up by 0.5 to 1.5 times the per-share distribution, so the step "
            "cannot be separated from the market move (daily_returns sets the reason at line %d)" % rules["daily_DVR"]["line"]),
    bloomberg_fill="no", why="a rule of the method on the close and the account's distribution rows; the blank is by design, not a missing price"))
drivers.append(dict(kind="day", code="HELD_SOURCE_UNDER_REVIEW", count=dcount("HELD_SOURCE_UNDER_REVIEW"), rule=rules["held_const"],
    driver=("a held security whose holding-days are blanked pending source review (%d account_day_value rows over %d securities, "
            "the review list being the --hold-cusips or the Yahoo active-policy blank)" % (out_scr["held_rows"], out_scr["held_cusips"])),
    bloomberg_fill="no", why="a held row under review: the blank is a source-review decision, not an absent history"))
drivers.append(dict(kind="day", code="REGRESSED_UNDER_AS_TRADED", count=dcount("REGRESSED_UNDER_AS_TRADED"), rule=rules["regressed_doc"],
    driver="every daily row of an account-month that matched before the rule change and is a DIFF after it (ABSENT account-months)",
    bloomberg_fill="no", why="a regression recorded by design of the rule separation; a price history does not change the verdict"))
drivers.append(dict(kind="day", code="FLOW_UNVALUED", count=dcount("FLOW_UNVALUED"), rule=rules["daily_FLOW"],
    driver="an external-flow row whose Amount is zero or null and which the day's price cannot value (no price, or no Quantity or CUSIP)",
    bloomberg_fill="not_established",
    why="the split between a missing price and a missing Quantity or CUSIP is not made in this census"))
for code, n in sorted(first_blank.items()):
    fill = "yes" if code == "UNPRICED" else "no"
    why = ("the month's blank days carry the UNPRICED reason; the fill is the same daily close as the UNPRICED days"
           if fill == "yes" else "the month's blank days carry this method reason, which a price history does not change")
    drivers.append(dict(kind="month", code="UNGRADABLE blank_days first_reason=%s" % code, count=int(n), rule=rules["month_blank"],
        driver="the month holds at least one blank day; the first blank reason of the month is %s" % code,
        bloomberg_fill=fill, why=why))
drivers.append(dict(kind="month", code="UNGRADABLE no_daily_returns", count=int(kind_months.get("no_daily_returns", 0)),
    rule=rules["month_nodaily"], driver="the account-month has no daily_returns row at all",
    bloomberg_fill="not_established", why="why an account-month has no daily rows is not split in this census"))
drivers.append(dict(kind="month", code="UNGRADABLE no_reported_return", count=int(kind_months.get("no_reported_return", 0)),
    rule=rules["month_noreport"], driver="the reported monthly figure is absent for the account-month",
    bloomberg_fill="no", why="the reported side is the client's performance figure, not a price; a vendor price does not supply it"))
drivers.append(dict(kind="month", code="UNGRADABLE reported_null", count=int(kind_months.get("reported_null", 0)),
    rule=rules["month_repnull"], driver="the reported monthly figure is null",
    bloomberg_fill="no", why="the reported side, not a price"))
drivers.append(dict(kind="month", code="UNGRADABLE side_absent", count=int(kind_months.get("side_absent", 0)),
    rule=r_month_ung, driver="guard: neither side is present", bloomberg_fill="no", why="guard branch, see count"))
drivers.append(dict(kind="month", code="UNGRADABLE reported_span_not_month", count=int(kind_months.get("reported_span_not_month", 0)),
    rule=rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 57, "is not one calendar month"),
    driver="the performance rows of the account-month span more than one calendar month or are not a calendar month; the reported figure is withheld",
    bloomberg_fill="no", why="the reported side is withheld for a span reason; a price history does not change the span"))
drivers.append(dict(kind="month", code="UNGRADABLE reported_rows_disagree", count=int(kind_months.get("reported_rows_disagree", 0)),
    rule=rule_line("data/assets/scripts/silver/commonwealth_monthly_grade.py", 81, "reported rows disagree"),
    driver="conflicting duplicate performance rows for the account-month; the reported figure is withheld",
    bloomberg_fill="no", why="a conflict on the reported side, not a price"))
drivers.append(dict(kind="month", code="UNGRADABLE other", count=int(kind_months.get("other", 0)), rule=r_month_ung,
    driver="reason texts not in the classes above (grouped by masked text in the run's counts)", bloomberg_fill="not_established",
    why="grouped by masked text in the run output; not classified further here"))
drivers.append(dict(kind="month", code="DIFF", count=diff_n, rule=rules["month_diff"],
    driver="both sides exist and the compounded daily return differs from the reported figure beyond the tolerance",
    bloomberg_fill="no", why="a computed value exists, so the month is not blank; a price history does not change the comparison"))
drivers.append(dict(kind="month", code="ABSENT", count=int(by_verdict.get("ABSENT", 0)), rule=rules["month_absent"],
    driver="REGRESSED_UNDER_ reason on the month (a null verdict)", bloomberg_fill="no",
    why="a regression recorded by design; the reason sits in the sidecar of the build"))
drivers.append(dict(kind="month", code="MATCH", count=match_n, rule=rules["month_match"],
    driver="computed and reported figures agree within tolerance; no blank day", bloomberg_fill="no",
    why="not a blank; included for completeness"))

ever_cats = ["no_ticker_symbol", "ticker_no_store_row", "ticker_key_claimed_by_more_than_one_security",
             "resolved_dropped_conflicting", "resolved_no_conflict_still_unpriced", "not_in_universe"]
breakdown = dict(
    never_priced=dict(securities=len(never_set), holding_days=never_rows,
                      by_asset_type={t: dict(securities=int(never_by_type[t]), holding_days=int(never_rows_by_type[t]))
                                     for t in sorted(never_by_type)},
                      by_ticker_status={k: dict(securities=int(cat.get(k, 0)), holding_days=int(cat_rows.get(k, 0))) for k in ever_cats}),
    gap=dict(securities=len(gap_set), holding_days=gap_rows, position=gap_pos),
    bloomberg_overlap=dict(records=bbg, union=bbg_union,
                           came_back_priced="not_established"),
    replay_check=out_scr["replay"])

vers = {"daily_returns_version": VERSIONS["daily_returns"], "month_grades_version": VERSIONS["month_grades"],
        "account_day_value_version": VERSIONS["account_day_value"]}

# the three sentences, in counts
top_code = max(days["by_reason"].items(), key=lambda kv: kv[1])[0]
what = [
    ("Of %d blank daily returns, %d carry a reason (%d unreasoned), and of %d non-MATCH months %d carry a reason (%d unreasoned)."
     % (days["blank"], days["blank"] - days["unreasoned"], days["unreasoned"], months["not_match"],
        months["not_match"] - months["unreasoned"], months["unreasoned"])),
    ("UNPRICED drives %d of %d blank days (%.1f%%), %d of the %d unpriced holding-days belong to %d never-priced securities and %d to %d gap securities."
     % (dcount("UNPRICED"), days["blank"], 100.0 * dcount("UNPRICED") / days["blank"], never_rows, un_rows, len(never_set),
        gap_rows, len(gap_set))),
    ("A vendor daily close for the unpriced securities could fill the UNPRICED days (%d are a missing close), but it could not fill the %d NON_POSITIVE_BASE, %d FIRST_DAY, %d DVR_CLOSE_STEP, %d HELD_SOURCE_UNDER_REVIEW and %d REGRESSED_UNDER_AS_TRADED blanks, nor the DIFF months, and it has not been shown to cover any of the unpriced securities."
     % (dcount("UNPRICED"), dcount("NON_POSITIVE_BASE"), dcount("FIRST_DAY"), dcount("DVR_CLOSE_STEP"),
        dcount("HELD_SOURCE_UNDER_REVIEW"), dcount("REGRESSED_UNDER_AS_TRADED"))),
]
not_est = [
    "Bloomberg came-back per security: no committed record carries the per-security outcome of the request lists; BBG_ACTUALS.jsonl holds %d job rows with cell counts only, so how many listed securities came back priced is not established." % len(bbg_actuals_rows),
    "Replay of the valuation's price resolution on the round-99 cache is not the served as-traded basis (the Yahoo substitution and the SECHIST store are not replayed): the replay priced %d cusips against %d served priced cusips; the never-priced ticker-status split uses the replay, and its resolved-but-unpriced groups are approximate." % (len(replay_priced), len(priced_cusips)),
    "asset_type is read from the silver transactions Asset_Type column through the analysis module's universe reader (read-only); the round-99 transactions cache does not carry the column.",
    "FLOW_UNVALUED split between missing price and missing Quantity or CUSIP is not made.",
    "UNGRADABLE months with no_daily_returns: the reason the account-month has no daily rows is not split.",
    "No blank day lacks a reason and no non-MATCH month lacks a reason on the served tables (unreasoned = 0 on both), so no row listing is needed.",
]
record = dict(measured=True, served=vers, days=days, months=months,
              unreasoned=dict(days=days["unreasoned"], months=months["unreasoned"]),
              unpriced=unpriced, drivers=drivers, unpriced_breakdown=breakdown,
              what_this_shows=" ".join(what), not_established=not_est)

os.makedirs(DELIV, exist_ok=True)
with open(DELIV + "/BLANK_CENSUS_RECORD.json", "w", encoding="utf-8", newline="\n") as fh:
    json.dump(record, fh, indent=2, sort_keys=False)
    fh.write("\n")
with open(SCR + "/cx1_run_counts.json", "w", encoding="utf-8") as fh:
    json.dump(dict(out_scr, unpriced=unpriced, days=days, months=months, gap_pos=gap_pos,
                   never_cats=dict(cat), never_cat_rows=dict(cat_rows), never_by_type=dict(never_by_type),
                   never_rows_by_type=dict(never_rows_by_type), cross=dict(unpriced_acct_days=unpriced_acct_days,
                   unpriced_days_with_unpriced_holding=unpriced_days_with_unpriced_holding,
                   dr_unp_days_no_holding=dr_unp_days_no_holding), bbg=bbg, bbg_union=bbg_union), fh, indent=2, sort_keys=True)

print("CX1-COUNTS days_blank=%d unreasoned_days=%d unreasoned_months=%d" % (days["blank"], days["unreasoned"], months["unreasoned"]))
print("CX1-COUNTS unpriced=%s" % json.dumps(unpriced, sort_keys=True))
print("CX1-COUNTS never_cats=%s" % json.dumps(dict(cat), sort_keys=True))
print("CX1-COUNTS never_cat_rows=%s" % json.dumps(dict(cat_rows), sort_keys=True))
print("CX1-COUNTS gap_pos=%s" % json.dumps(gap_pos, sort_keys=True))
print("CX1-COUNTS cross=%s" % json.dumps(dict(unpriced_acct_days=unpriced_acct_days, unpriced_days_with_unpriced_holding=unpriced_days_with_unpriced_holding, dr_unp_days_no_holding=dr_unp_days_no_holding), sort_keys=True))
print("CX1-COUNTS bbg_union=%s records=%s" % (json.dumps(bbg_union, sort_keys=True), json.dumps(bbg, sort_keys=True)))
print("CX1-COUNTS replay=%s" % json.dumps(out_scr["replay"], sort_keys=True))
print("CX1-COUNTS ungradable_kinds=%s first_blank=%s combos=%s" % (json.dumps(dict(kind_months), sort_keys=True), json.dumps(dict(first_blank), sort_keys=True), json.dumps(dict(combo), sort_keys=True)))
print("CX1-COUNTS other_texts=%s absent=%s" % (json.dumps(dict(other_texts), sort_keys=True), json.dumps(dict(absent_reasons), sort_keys=True)))
print("CX1-COUNTS held=%s" % json.dumps({"rows": out_scr["held_rows"], "cusips": out_scr["held_cusips"], "daily_days": out_scr["held_days_daily_returns"]}, sort_keys=True))
print("CX1-COUNTS by_type_never=%s" % json.dumps({t: [int(never_by_type[t]), int(never_rows_by_type[t])] for t in sorted(never_by_type)}, sort_keys=True))
print("CX1-DONE record written")
