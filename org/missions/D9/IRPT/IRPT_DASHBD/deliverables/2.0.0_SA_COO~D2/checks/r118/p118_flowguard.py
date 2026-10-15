"""IRPT_DASHBD round 118 (issuer 2.0.0_SA_COO~D2) -- DB-b-231, the flow-guard READ (CTO analysis @5934ffcedc, ruling 1).

  DB-b-231 (~186) the 49 Financial account_return_daily GRADED_DISAGREED rows of 2026-04-21 and of the next five dates by households
                  broken (2026-07-02, 2026-10-13, 2026-09-22, 2026-10-06, 2026-09-16), each classified by which input disagrees
                  (the flow, the value, both, neither, or no prior day). A READ: nothing is written.            DB118-2-AC1

The checker grades FORM and INTERNAL CONSISTENCY, and RECOUNTS from the gold itself (read-only S3 GET of the six date partitions, their
previous-trading-day partitions and the manifests): the rows, the GRADED_DISAGREED rows, the FLOW_UNRECONCILED rows and the five-way cause
split of every date. The worker's counts must equal the checker's recount to the unit.

Cause rule (the one the order states; the checker recomputes it from persisted columns only). For a GRADED_DISAGREED row of account a on date t,
with V = market_value_eod, F = external_flow, p = holdings_price_return and tau = the tolerance in the date's own manifest.json
(thresholds.tolerance), and the account's row on the previous trading day t0 (lib/trading_calendar.prev_trading_day):
  NO_PRIOR        : no row on t0, or V(t0) is not above zero, or V(t), F(t) or p is null
  else v = V(t)/V(t0) - 1, s = |F(t)| / V(t0), value_gap = |v - p| > tau, flow_big = s > tau:
  FLOW            : flow_big and not value_gap
  VALUE           : value_gap and not flow_big
  FLOW_AND_VALUE  : flow_big and value_gap
  NEITHER         : neither

Value-gap profile (the rows whose cause has value_gap true: VALUE and FLOW_AND_VALUE), gap = v - p:
  gap_positive / gap_negative by the sign of gap; band_le_1pct, band_1_to_5pct, band_gt_5pct by |gap| (<= 0.01, <= 0.05, above);
  next day = the next trading day's row of the same account: reversal_next_day when it exists, V(t) is above zero, p is not null and its
  own gap (v' - p') has the opposite sign with |gap'| > tau; no_next_day_row when the account has no row on the next trading day
  or the partition is absent; not_reversed otherwise.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~186/flow_guard_read_r118.py"
DATES = ("2026-04-21", "2026-07-02", "2026-10-13", "2026-09-22", "2026-10-06", "2026-09-16")
CAUSES = ("FLOW", "VALUE", "FLOW_AND_VALUE", "NEITHER", "NO_PRIOR")
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")
FIRM = "49financial"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


# ------------------------------------------------------------------------------------------------ the cause rule (pure)
def cause_of(v_t, f_t, p_t, v_0, tau):
    """The five-way cause of one GRADED_DISAGREED row; None inputs are NO_PRIOR (v_0 is the previous trading day's value)."""
    if v_0 is None or not (v_0 > 0) or v_t is None or f_t is None or p_t is None:
        return "NO_PRIOR"
    v = v_t / v_0 - 1.0
    s = abs(f_t) / v_0
    value_gap = abs(v - p_t) > tau
    flow_big = s > tau
    if flow_big and not value_gap:
        return "FLOW"
    if value_gap and not flow_big:
        return "VALUE"
    if flow_big and value_gap:
        return "FLOW_AND_VALUE"
    return "NEITHER"


def split_rows(rows_t, rows_0, tau):
    """rows_t / rows_0: dict account -> dict(market_value_eod, external_flow, holdings_price_return, guard_state, day_quality).
    Returns (rows, graded_disagreed, flow_unreconciled, by_cause)."""
    by = {c: 0 for c in CAUSES}
    gd = fu = 0
    for a, r in rows_t.items():
        if r.get("day_quality") == "FLOW_UNRECONCILED":
            fu += 1
        if r.get("guard_state") == "GRADED_DISAGREED":
            gd += 1
            z = rows_0.get(a)
            by[cause_of(r.get("market_value_eod"), r.get("external_flow"), r.get("holdings_price_return"),
                        None if z is None else z.get("market_value_eod"), tau)] += 1
    return len(rows_t), gd, fu, by


PROFILE_KEYS = ("value_gap_rows", "gap_positive", "gap_negative", "band_le_1pct", "band_1_to_5pct", "band_gt_5pct",
                "reversal_next_day", "not_reversed", "no_next_day_row")


def gap_of(v_t, p_t, v_0):
    if v_0 is None or not (v_0 > 0) or v_t is None or p_t is None:
        return None
    return (v_t / v_0 - 1.0) - p_t


def profile_rows(rows_t, rows_0, rows_next, tau):
    """The value-gap profile of one date; rows_next is None when the next trading day's partition is absent."""
    out = {k: 0 for k in PROFILE_KEYS}
    for a, r in rows_t.items():
        if r.get("guard_state") != "GRADED_DISAGREED":
            continue
        z = rows_0.get(a)
        v0 = None if z is None else z.get("market_value_eod")
        if cause_of(r.get("market_value_eod"), r.get("external_flow"), r.get("holdings_price_return"), v0, tau) not in ("VALUE", "FLOW_AND_VALUE"):
            continue
        g = gap_of(r.get("market_value_eod"), r.get("holdings_price_return"), v0)
        out["value_gap_rows"] += 1
        out["gap_positive" if g > 0 else "gap_negative"] += 1
        ag = abs(g)
        out["band_le_1pct" if ag <= 0.01 else ("band_1_to_5pct" if ag <= 0.05 else "band_gt_5pct")] += 1
        n = None if rows_next is None else rows_next.get(a)
        if n is None:
            out["no_next_day_row"] += 1
            continue
        g2 = gap_of(n.get("market_value_eod"), n.get("holdings_price_return"), r.get("market_value_eod"))
        if g2 is not None and abs(g2) > tau and (g2 > 0) != (g > 0):
            out["reversal_next_day"] += 1
        else:
            out["not_reversed"] += 1
    return out


# ------------------------------------------------------------------------------------------------ the recount from the gold (read-only GET)
def read_partition(s3, bucket, prefix):
    import pyarrow.parquet as pq
    body = s3.get_object(Bucket=bucket, Key=prefix + "data.parquet")["Body"].read()
    t = pq.read_table(io.BytesIO(body), columns=["account_id", "market_value_eod", "external_flow", "holdings_price_return",
                                                 "guard_state", "day_quality"]).to_pydict()
    out = {}
    for i, a in enumerate(t["account_id"]):
        out[a] = {k: t[k][i] for k in ("market_value_eod", "external_flow", "holdings_price_return", "guard_state", "day_quality")}
    man = json.loads(s3.get_object(Bucket=bucket, Key=prefix + "manifest.json")["Body"].read().decode("utf-8"))
    return out, man


def next_trading_day(tc, d):
    import datetime as dt
    x = dt.date.fromisoformat(d) + dt.timedelta(days=1)
    while not tc.is_trading_day(x.isoformat()):
        x += dt.timedelta(days=1)
    return x.isoformat()


def recount(root, dates):
    sys.path.insert(0, str(root))
    import boto3
    from lib import opal_naming, trading_calendar as tc
    s3 = boto3.client("s3")

    def loc(day):
        addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=%s" % day)
        bucket, key = addr[len("s3://"):].split("/", 1)
        return bucket, key.rstrip("/") + "/"

    res = {}
    for d in dates:
        b, k = loc(d)
        rows_t, man = read_partition(s3, b, k)
        tau = float(man["thresholds"]["tolerance"])
        d0 = str(tc.prev_trading_day(d))
        b0, k0 = loc(d0)
        try:
            rows_0, _ = read_partition(s3, b0, k0)
        except Exception:
            rows_0 = {}
        n, gd, fu, by = split_rows(rows_t, rows_0, tau)
        d1 = next_trading_day(tc, d)
        b1, k1 = loc(d1)
        try:
            rows_next, _ = read_partition(s3, b1, k1)
        except s3.exceptions.NoSuchKey:
            rows_next = None
        res[d] = {"tolerance": tau, "rows": n, "rows_graded_disagreed": gd, "rows_flow_unreconciled": fu, "by_cause": by,
                  "value_gap_profile": profile_rows(rows_t, rows_0, rows_next, tau)}
    return res


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, analysis_text, tracked, analysis_sha):
    need(isinstance(rec, dict), "record is not an object")
    exp = {"dates", "totals", "classification", "tolerance_source", "positive_control", "analysis", "reads",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(set(rec) == exp, "record keys differ: %s" % sorted(set(rec) ^ exp))
    dates = rec["dates"]
    need(isinstance(dates, list) and [x.get("date") for x in dates] == list(DATES), "dates are not exactly the six, in order")
    tot_gd = 0
    tot_by = {c: 0 for c in CAUSES}
    for x in dates:
        need(set(x) == {"date", "tolerance", "rows", "rows_graded_disagreed", "rows_flow_unreconciled", "by_cause", "value_gap_profile", "claim"},
             "a date entry has the wrong keys: %s" % x.get("date"))
        need(x["claim"] in CLAIMS, "claim not in the four words")
        need(is_num(x["tolerance"]) and 0 < x["tolerance"] < 0.1, "tolerance out of range")
        for k in ("rows", "rows_graded_disagreed", "rows_flow_unreconciled"):
            need(is_int(x[k]) and x[k] >= 0, "%s not a count" % k)
        bc = x["by_cause"]
        need(isinstance(bc, dict) and set(bc) == set(CAUSES) and all(is_int(v) and v >= 0 for v in bc.values()),
             "by_cause keys are not the five causes")
        need(sum(bc.values()) == x["rows_graded_disagreed"], "by_cause does not sum to the graded-disagreed rows on %s" % x["date"])
        need(x["rows_graded_disagreed"] <= x["rows"] and x["rows_flow_unreconciled"] <= x["rows"], "counts exceed rows")
        t = truth[x["date"]]
        need(abs(x["tolerance"] - t["tolerance"]) < 1e-12, "tolerance differs from the manifest on %s" % x["date"])
        for k in ("rows", "rows_graded_disagreed", "rows_flow_unreconciled"):
            need(x[k] == t[k], "%s on %s: record %s, recount %s" % (k, x["date"], x[k], t[k]))
        need(bc == t["by_cause"], "by_cause on %s: record %s, recount %s" % (x["date"], bc, t["by_cause"]))
        vp = x["value_gap_profile"]
        need(isinstance(vp, dict) and set(vp) == set(PROFILE_KEYS) and all(is_int(v) and v >= 0 for v in vp.values()),
             "value_gap_profile keys on %s" % x["date"])
        need(vp["value_gap_rows"] == bc["VALUE"] + bc["FLOW_AND_VALUE"], "value_gap_rows is not VALUE + FLOW_AND_VALUE on %s" % x["date"])
        need(vp["gap_positive"] + vp["gap_negative"] == vp["value_gap_rows"], "gap signs do not sum on %s" % x["date"])
        need(vp["band_le_1pct"] + vp["band_1_to_5pct"] + vp["band_gt_5pct"] == vp["value_gap_rows"], "gap bands do not sum on %s" % x["date"])
        need(vp["reversal_next_day"] + vp["not_reversed"] + vp["no_next_day_row"] == vp["value_gap_rows"],
             "next-day split does not sum on %s" % x["date"])
        need(vp == t["value_gap_profile"], "value_gap_profile on %s: record %s, recount %s" % (x["date"], vp, t["value_gap_profile"]))
        tot_gd += x["rows_graded_disagreed"]
        for c in CAUSES:
            tot_by[c] += bc[c]
    tt = rec["totals"]
    need(isinstance(tt, dict) and set(tt) == {"rows_graded_disagreed", "by_cause", "claim"} and tt["claim"] in CLAIMS, "totals form")
    need(tt["rows_graded_disagreed"] == tot_gd and tt["by_cause"] == tot_by, "totals are not the sum of the dates")
    cl = rec["classification"]
    need(isinstance(cl, dict) and set(cl) == {"words", "claim"} and nes(cl["words"]) and cl["claim"] in CLAIMS,
         "classification must be {words, claim}")
    ts = rec["tolerance_source"]
    need(isinstance(ts, dict) and set(ts) == {"file", "key_path", "words"} and all(nes(ts[k]) for k in ts), "tolerance_source form")
    pc = rec["positive_control"]
    need(isinstance(pc, dict) and set(pc) == {"description", "expected", "observed", "passed"} and pc["passed"] is True,
         "positive_control must pass")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and an.get("sha256") == analysis_sha,
         "analysis file, hash or tracked flag is wrong")
    need(tracked, "the analysis script is not tracked")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False
         and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    low = analysis_text.lower()
    need(not [t for t in FOREIGN if t in low], "the analysis script names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the analysis script holds a write call")
    return True


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def is_tracked(root, rel):
    r = subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel], capture_output=True, text=True)
    return r.returncode == 0


def run(root, cid):
    need(cid == "DB118-2-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root, DATES)
    check_record(rec, truth, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), sha(ap))
    t = truth[DATES[0]]
    print("OK: flow-guard read: 2026-04-21 has %d graded-disagreed rows %s (recounted from the gold); six dates match to the unit; "
          "tolerance equals each manifest" % (t["rows_graded_disagreed"], t["by_cause"]))
    return True


# ------------------------------------------------------------------------------------------------ self-test
def selftest(root):
    t = 0.001
    cases = [
        (cause_of(1.10, 0.0, 0.0, 1.0, t), "VALUE"),          # v = 0.10 vs p = 0, no flow
        (cause_of(1.0, 0.5, 0.0, 1.0, t), "FLOW"),            # v = 0 = p, flow share 0.5
        (cause_of(1.10, 0.5, 0.0, 1.0, t), "FLOW_AND_VALUE"),
        (cause_of(1.0005, 0.0, 0.0, 1.0, t), "NEITHER"),      # inside tolerance on both
        (cause_of(1.0, 0.0, 0.0, None, t), "NO_PRIOR"),
        (cause_of(1.0, 0.0, 0.0, 0.0, t), "NO_PRIOR"),
        (cause_of(1.0, 0.0, None, 1.0, t), "NO_PRIOR"),
    ]
    for got, want in cases:
        need(got == want, "cause_of: got %s want %s" % (got, want))
    rt = {"a": dict(market_value_eod=1.1, external_flow=0.0, holdings_price_return=0.0, guard_state="GRADED_DISAGREED", day_quality="FLOW_UNRECONCILED"),
          "b": dict(market_value_eod=1.0, external_flow=0.0, holdings_price_return=0.0, guard_state="GRADED_AGREED", day_quality="MEASURED"),
          "c": dict(market_value_eod=1.0, external_flow=0.5, holdings_price_return=0.0, guard_state="GRADED_DISAGREED", day_quality="FLOW_UNRECONCILED")}
    r0 = {"a": dict(market_value_eod=1.0), "c": dict(market_value_eod=1.0)}
    n, gd, fu, by = split_rows(rt, r0, t)
    need((n, gd, fu) == (3, 2, 2) and by["VALUE"] == 1 and by["FLOW"] == 1 and sum(by.values()) == 2, "split_rows")
    # the value-gap profile on a synthetic day: a (VALUE, positive gap, next day reverses), c (FLOW, not a gap row), d (VALUE, negative, no next row)
    rt2 = {"a": dict(market_value_eod=1.10, external_flow=0.0, holdings_price_return=0.0, guard_state="GRADED_DISAGREED"),
           "c": dict(market_value_eod=1.0, external_flow=0.5, holdings_price_return=0.0, guard_state="GRADED_DISAGREED"),
           "d": dict(market_value_eod=0.90, external_flow=0.0, holdings_price_return=0.0, guard_state="GRADED_DISAGREED")}
    r02 = {"a": dict(market_value_eod=1.0), "c": dict(market_value_eod=1.0), "d": dict(market_value_eod=1.0)}
    rn2 = {"a": dict(market_value_eod=1.10 * 0.95, holdings_price_return=0.0)}      # next day falls 5 percent: opposite sign, reversal
    pf = profile_rows(rt2, r02, rn2, t)
    need(pf["value_gap_rows"] == 2 and pf["gap_positive"] == 1 and pf["gap_negative"] == 1, "profile signs")
    need(pf["reversal_next_day"] == 1 and pf["no_next_day_row"] == 1 and pf["not_reversed"] == 0, "profile next-day split")
    need(pf["band_le_1pct"] + pf["band_1_to_5pct"] + pf["band_gt_5pct"] == 2 and pf["band_le_1pct"] == 0, "profile bands")
    need(profile_rows(rt2, r02, None, t)["no_next_day_row"] == 2, "an absent next partition puts every gap row in no_next_day_row")
    # the record clauses, GREEN arm and one RED arm per clause
    PROF = {"value_gap_rows": 2, "gap_positive": 1, "gap_negative": 1, "band_le_1pct": 1, "band_1_to_5pct": 1, "band_gt_5pct": 0,
            "reversal_next_day": 1, "not_reversed": 0, "no_next_day_row": 1}
    truth = {d: {"tolerance": 0.001244, "rows": 100, "rows_graded_disagreed": 4, "rows_flow_unreconciled": 5,
                 "by_cause": {"FLOW": 1, "VALUE": 1, "FLOW_AND_VALUE": 1, "NEITHER": 1, "NO_PRIOR": 0},
                 "value_gap_profile": dict(PROF)} for d in DATES}

    def good():
        return {
            "dates": [{"date": d, "tolerance": 0.001244, "rows": 100, "rows_graded_disagreed": 4, "rows_flow_unreconciled": 5,
                       "by_cause": {"FLOW": 1, "VALUE": 1, "FLOW_AND_VALUE": 1, "NEITHER": 1, "NO_PRIOR": 0},
                       "value_gap_profile": dict(PROF), "claim": "measured"}
                      for d in DATES],
            "totals": {"rows_graded_disagreed": 24, "by_cause": {"FLOW": 6, "VALUE": 6, "FLOW_AND_VALUE": 6, "NEITHER": 6, "NO_PRIOR": 0},
                       "claim": "measured"},
            "classification": {"words": "five causes from persisted columns", "claim": "inferred"},
            "tolerance_source": {"file": "x/manifest.json", "key_path": "thresholds.tolerance", "words": "the date's own manifest"},
            "positive_control": {"description": "d", "expected": "e", "observed": "o", "passed": True},
            "analysis": {"file": ANALYSIS_REL, "sha256": "ab" * 32, "tracked": True},
            "reads": {"s3_reads": 12, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
            "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(rec, text="x = 1", tracked=True, h="ab" * 32):
        try:
            return check_record(rec, truth, text, tracked, h)
        except Fail:
            return False

    need(grade(good()) is True, "GREEN arm failed")
    r = good()
    r["dates"][0]["rows_graded_disagreed"] = 5
    need(grade(r) is False, "RED: a count off by one must fail")
    r = good()
    r["dates"][1]["by_cause"]["FLOW"] = 2
    need(grade(r) is False, "RED: a cause split that does not sum must fail")
    r = good()
    r["dates"][2]["tolerance"] = 0.002
    need(grade(r) is False, "RED: a tolerance that differs from the manifest must fail")
    r = good()
    r["dates"] = r["dates"][::-1]
    need(grade(r) is False, "RED: dates out of order must fail")
    r = good()
    r["dates"][3]["value_gap_profile"]["gap_positive"] = 2
    need(grade(r) is False, "RED: a profile that does not recount must fail")
    r = good()
    r["dates"][4]["value_gap_profile"]["value_gap_rows"] = 3
    need(grade(r) is False, "RED: a profile whose rows are not VALUE + FLOW_AND_VALUE must fail")
    r = good()
    r["totals"]["rows_graded_disagreed"] = 23
    need(grade(r) is False, "RED: wrong totals must fail")
    r = good()
    r["positive_control"]["passed"] = False
    need(grade(r) is False, "RED: a failed positive control must fail")
    r = good()
    r["classification"]["words"] = "ids 1234567890"
    need(grade(r) is False, "RED: a long digit run must fail")
    need(grade(good(), tracked=False) is False, "RED: an untracked script must fail")
    need(grade(good(), text="s3.put_object(Bucket=b)") is False, "RED: a write call must fail")
    need(grade(good(), text="b = 'opal-data-cottonwood'") is False, "RED: another firm's place must fail")
    need(grade(good(), h="cd" * 32) is False, "RED: a hash mismatch must fail")
    r = good()
    r["pushed"] = True
    need(grade(r) is False, "RED: a push flag must fail")
    print("selftest OK: 7 cause arms, 1 split arm, 4 profile arms, 1 green and 13 red record arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p118_flowguard.py <repo_root> <criterion_id>")
            sys.exit(2)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
    except Exception as e:  # an unreadable gold is a FAIL naming itself, never a pass
        print("FAIL: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
