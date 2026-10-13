"""IRPT_DASHBD round 92, TO-DB-b-172 (worker 0.9.0_WK_IRPT_DASHBD~138): the BD_EXCLUDES_SERVED_INCOME read.

Implements RULE_EXCL.md in this folder (committed before any computation on the 23 differing days) as written.
Imports by path and does not edit: ledger_rows.py (worker ~137: read_store, served_declaration, sums, fnum, window_of,
norm_acct, day_str, candidates for the reasons after the new one), tieout_day_read.py and tieout_neither_reasons.py
(the population, the series, the calendar and the amount tie). Reads: the issuer's pull and the stored tables in the
private folders (read only) and FRESH S3 GET and LIST only, of the two stores round 91 named. No vendor call, no
credential, no S3 write, no served value changed.

Usage: python -I excl_income.py <repo_root> <record_out> <private_detail_out> [<surprise_row_id>]
Prints COUNTS, OFFSETS, SIZES and multiples only: no account id, no name, no amount, no date.
"""
import collections
import datetime as dt
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import boto3
from botocore.config import Config

TOL_PP = 0.35
DAY_DIFFERS_PP = 0.01
PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~138/"
FOLDER137 = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~137/"
RULE_FILE = "RULE_EXCL.md"
REASONS = ("BD_EXCLUDES_SERVED_INCOME", "BD_INCOME_PER_LOT", "DUPLICATE_ROW", "BOOKING_DATE_DIFFERS",
           "MISSING_IN_LEDGER", "UNEXPLAINED")
KIND = {"BD_EXCLUDES_SERVED_INCOME": "multiple", "BD_INCOME_PER_LOT": "multiple", "DUPLICATE_ROW": "count",
        "BOOKING_DATE_DIFFERS": "day_offsets", "MISSING_IN_LEDGER": "count"}
PRIV134 = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~134/"
BD_BUCKET = "opal-data-assets"
BD_PREFIX = "blackdiamond/49financial/silver_legacy/transactions/"
FLOW_KINDS = ("Contribution", "Withdrawal")
STORED_TOL = 0.005
BD_SIDE, SV_SIDE = "BD", "SV"
EXCL_NO = 1
PERLOT_NO = 2


def die(msg):
    print("ERROR: " + msg)
    sys.exit(2)


def import_by_path(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode("ascii", "replace").strip()


def excl_test(x):
    """RULE_EXCL.md section 2, TEST: a != 0, m applicable, |(b - s) + a / m| * 100 <= 0.01."""
    a, m = x["a"], x["m"]
    if a == 0 or m is None or m == 0:
        return False
    return abs((x["b"] - x["s"]) + a / m) * 100.0 <= DAY_DIFFERS_PP


def excl_candidate(x, bd_d, lr):
    """RULE_EXCL.md section 2, CORRECTION (served side): V' = V - a; c = (V' - f) / m - 1. EVIDENCE: multiple k."""
    a, m, V, f = x["a"], x["m"], x["V"], x["f"]
    I, _flow = lr.sums(bd_d)  # noqa: E741 -- the rule's own symbol for the day's BD income sum
    k = int(round(I / a)) if I != 0 else 0
    corr = None
    if m is not None and m != 0 and V is not None:
        corr = (V - a - f) / m - 1.0
    return (EXCL_NO, SV_SIDE, corr, k)


def perlot_candidate_b(x, bd_d, lr, nr):
    """RULE_LEDGER_ADDENDUM.md section 3 (Reading B) for reason (2), with the ~137 code's I != 0 clause kept
    (stated in RULE_EXCL.md section 3). CORRECTION (BD side): b' = b - (I - a) / m. EVIDENCE: multiple k."""
    a, m, b = x["a"], x["m"], x["b"]
    I, _flow = lr.sums(bd_d)  # noqa: E741
    inc_rows = [r for r in bd_d if lr.fnum(r.get("income")) != 0.0]
    if a != 0 and len(inc_rows) >= 2 and I != 0:
        k = int(round(I / a))
        if k >= 2 and nr.tie_amt(I, k * a):
            corr = None
            if m is not None and m != 0:
                corr = b - (I - a) / m
            return [(PERLOT_NO, BD_SIDE, corr, k)]
    return []


def assign(x, bd_d, sv_d, sv_win, adj, nr, lr):
    """The first reason of the closed list (RULE_EXCL.md section 1) whose TEST holds and whose correction brings the
    day within 0.01 pp. Reasons (3) to (5) are ~137's, from lr.candidates, renumbered by +1."""
    cands = []
    if excl_test(x):
        cands.append(excl_candidate(x, bd_d, lr))
    cands += perlot_candidate_b(x, bd_d, lr, nr)
    for n, side, corr, ev in lr.candidates(x, bd_d, sv_d, sv_win, adj, nr):
        if n == 1:
            continue
        cands.append((n + 1, side, corr, ev))
    for n, side, corr, ev in cands:
        if corr is None:
            continue
        if side == BD_SIDE:
            ok = abs((corr - x["s"]) * 100.0) <= DAY_DIFFERS_PP
        else:
            ok = abs((x["b"] - corr) * 100.0) <= DAY_DIFFERS_PP
        if ok:
            return n, side, corr, ev
    return None


def main(argv):
    if len(argv) < 4:
        die("usage: python -I excl_income.py <repo_root> <record_out> <private_detail_out> [<surprise_row_id>]")
    root = Path(argv[1]).resolve()
    rec_out, det_out = Path(argv[2]), Path(argv[3])
    row_id = argv[4] if len(argv) > 4 else ""
    tdr = import_by_path(root / PROJ / "tieout" / "tieout_day_read.py", "tieout_day_read")
    nr = import_by_path(root / PROJ / "tieout" / "tieout_neither_reasons.py", "tieout_neither_reasons")
    lr = import_by_path(root / FOLDER137 / "ledger_rows.py", "ledger_rows")

    flow_n, _got, unexpl = tdr.plan_unexplained(root, nr)
    if flow_n != 88 or len(unexpl) != 7:
        die("population does not reproduce")
    pull_rec = tdr.read_json(Path(PRIV134) / "pull" / "DAY_PULL_RECORD.json")
    if pull_rec.get("status") != "COMPLETE" or pull_rec.get("requests") != 7:
        die("the issuer's pull record is not COMPLETE over 7 requests")
    gold = nr.prev.load("read90.pkl")["gold"]
    plan = tdr.read_json(Path(PRIV134) / "DAY_READ_PLAN.json")

    accts = []
    want_bd, want_sv = collections.defaultdict(set), collections.defaultdict(set)
    for i, s in enumerate(unexpl):
        if plan["requests"][i]["account"] != s["acct"]:
            die("plan order differs from the round-89 selection at position %d" % (i + 1))
        series = gold[s["acct"]]
        gdates = sorted(series)
        pos = {d: k for k, d in enumerate(gdates)}
        seg_start, seg_end = s["seg"]["start"], s["seg"]["end"]
        seg_gold = {d for d in gdates if seg_start <= d <= seg_end}
        dates, cums = tdr.series_points(tdr.read_json(Path(PRIV134) / "pull" / ("series_%02d.json" % i)))
        bd_daily = tdr.daily_from_cumulative(cums)
        days = []
        for d, bv in zip(dates, bd_daily):
            g = series.get(d)
            if not g or g.get("r") is None:
                continue
            k = pos[d]
            prev_d = gdates[k - 1] if k > 0 else None
            m = series[prev_d].get("mv") if prev_d else None
            days.append({"d": d, "dt": nr.day_of(d), "b": bv, "s": float(g["r"]), "V": g.get("mv"),
                         "f": float(g.get("flow") or 0.0), "a": float(g.get("inc_recv") or 0.0), "m": m})
        diff = [x for x in days if abs((x["b"] - x["s"]) * 100.0) > DAY_DIFFERS_PP]
        for x in diff:
            want_bd[lr.norm_acct(s["acct"])] |= lr.window_of(x["d"])
            want_sv[lr.norm_acct(s["acct"])] |= lr.window_of(x["d"])
        accts.append({"i": i, "s": s, "seg_start": nr.day_of(seg_start), "seg_gold": seg_gold, "days": days,
                      "diff": diff})

    n_accounts = len(accts)
    n_diff_total = sum(len(a["diff"]) for a in accts)
    if n_accounts != 7 or n_diff_total != 23:
        die("population %d accounts and %d differing days; expected 7 and 23" % (n_accounts, n_diff_total))

    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40,
                                                                   retries={"max_attempts": 8, "mode": "standard"}))
    bd_rows, bd_parts, bd_objs = lr.read_store(s3, BD_BUCKET, BD_PREFIX, "account_number", "return_date",
                                               want_bd, lambda tok: True)
    sv_bucket, sv_prefix, sv_acct_col, sv_date_col = lr.served_declaration(root)
    all_dates = sorted({d for w in want_sv.values() for d in w})
    lo, hi = all_dates[0], all_dates[-1]
    sv_rows, sv_parts, sv_objs = lr.read_store(s3, sv_bucket, sv_prefix, sv_acct_col, sv_date_col, want_sv,
                                               lambda tok: tok.startswith("date=") and lo <= tok[5:] <= hi)

    bd_by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in bd_rows:
        bd_by[lr.norm_acct(r.get("account_number"))][lr.day_str(r.get("return_date"))].append(r)
    sv_by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in sv_rows:
        sv_by[lr.norm_acct(r.get(sv_acct_col))][lr.day_str(r.get(sv_date_col))].append(r)

    per_account, detail = [], []
    closed_n = unexpl_n = 0
    test_held_total = 0
    controls = {"stored_match_days": 0, "stored_mismatch_days": 0, "adjacent_uncovered": 0}
    for a_rec in accts:
        s = a_rec["s"]
        key = lr.norm_acct(s["acct"])
        bd_day = bd_by.get(key, {})
        sv_day = sv_by.get(key, {})
        covered = want_bd.get(key, set())
        for d in sorted(covered):
            inc, flow = lr.sums(bd_day.get(d, []))
            if abs(inc - s["bdi"].get(d, 0.0)) <= STORED_TOL and abs(flow - s["bdf"].get(d, 0.0)) <= STORED_TOL:
                controls["stored_match_days"] += 1
            else:
                controls["stored_mismatch_days"] += 1
        series = gold[s["acct"]]
        counts = {r: 0 for r in REASONS}
        evid = collections.defaultdict(list)
        unexpl_days = []
        final_s = []
        pbd = 1.0
        ndiff = 0
        test_held_acct = 0
        for x in a_rec["days"]:
            if abs((x["b"] - x["s"]) * 100.0) <= DAY_DIFFERS_PP:
                continue
            ndiff += 1
            d = x["d"]
            bd_d = bd_day.get(d, [])
            sv_d = sv_day.get(d, [])
            if excl_test(x):
                test_held_acct += 1
            sv_win = []
            for dd in lr.window_of(d):
                sv_win += sv_day.get(dd, [])
            sv_win = [q for q in sv_win if lr.fnum(q.get("gross_amount")) != 0.0]
            adj = []
            for step in (-1, 1):
                cand = x["dt"]
                for _k in range(lr.ADJ_SEARCH_DAYS):
                    cand = cand + dt.timedelta(days=step)
                    if nr.is_trading(cand):
                        break
                else:
                    continue
                d2 = cand.isoformat()
                if d2 not in a_rec["seg_gold"]:
                    continue
                if d2 not in covered:
                    controls["adjacent_uncovered"] += 1
                    continue
                g2 = series[d2]
                i2, f2 = lr.sums(bd_day.get(d2, []))
                adj.append(((cand - x["dt"]).days, float(g2.get("inc_recv") or 0.0),
                            float(g2.get("flow") or 0.0), i2, f2))
            hit = assign(x, bd_d, sv_d, sv_win, adj, nr, lr)
            if hit is None:
                counts["UNEXPLAINED"] += 1
                unexpl_days.append({"offset": (x["dt"] - a_rec["seg_start"]).days,
                                    "size_pp": round((x["b"] - x["s"]) * 100.0, 4)})
                final_s.append(x["s"])
                detail.append({"acct_index": a_rec["i"], "date": d, "reason": "UNEXPLAINED",
                               "size_pp": (x["b"] - x["s"]) * 100.0})
                continue
            reason_no, side, corr, ev = hit
            name = REASONS[reason_no - 1]
            counts[name] += 1
            evid[name].append(int(ev))
            if side == BD_SIDE:
                pbd *= (1.0 + corr) / (1.0 + x["b"])
                final_s.append(x["s"])
            else:
                final_s.append(corr)
            detail.append({"acct_index": a_rec["i"], "date": d, "reason": name, "side": side, "evidence": int(ev),
                           "size_pp": (x["b"] - x["s"]) * 100.0})
        test_held_total += test_held_acct
        # RULE_LEDGER.md section 2 and 3, and RULE_EXCL.md section 5 and 6
        G = float(s["gross"])
        R0 = 1.0
        for x in a_rec["days"]:
            R0 *= 1.0 + x["s"]
        R0 -= 1.0
        Rc = 1.0
        idx = 0
        for x in a_rec["days"]:
            if abs((x["b"] - x["s"]) * 100.0) > DAY_DIFFERS_PP:
                Rc *= 1.0 + final_s[idx]
                idx += 1
            else:
                Rc *= 1.0 + x["s"]
        Rc -= 1.0
        Gc = (1.0 + G) * pbd - 1.0
        misses = abs(G - R0) * 100.0 > TOL_PP
        recloses = abs(Gc - Rc) * 100.0 <= TOL_PP
        closed = counts["UNEXPLAINED"] == 0 and recloses
        closed_n += 1 if closed else 0
        unexpl_n += 0 if closed else 1
        evidence = {}
        for name in REASONS[:-1]:
            if counts[name] > 0:
                evidence[name] = {"kind": KIND[name], "values": [int(v) for v in evid[name]]}
        per_account.append({"days_differing": ndiff, "by_reason": counts, "evidence": evidence,
                            "unexplained_days": unexpl_days, "uncorrected_window_misses": misses,
                            "window_closed_after_correction": closed})
        print("account %d: days %d differing %d test_held %d by_reason %s uncorrected_misses %s window_closed %s"
              % (a_rec["i"] + 1, len(a_rec["days"]), ndiff, test_held_acct,
                 json.dumps([counts[r] for r in REASONS]), str(misses).lower(), str(closed).lower()))
        for u in unexpl_days:
            print("  UNEXPLAINED offset %d size_pp %s" % (u["offset"], u["size_pp"]))

    code_rel = FOLDER + "excl_income.py"
    rc_ls, _ = git(root, "ls-files", "--error-unmatch", code_rel)
    _, dirty = git(root, "status", "--porcelain", "--", code_rel)
    code_tracked = rc_ls == 0 and dirty == ""
    rule_rel = FOLDER + RULE_FILE
    _, rule_commit = git(root, "log", "-1", "--format=%H", "--", rule_rel)
    _, rule_dirty = git(root, "status", "--porcelain", "--", rule_rel)
    if not rule_commit or rule_dirty:
        die("RULE_EXCL.md is not committed clean")

    det_out.parent.mkdir(parents=True, exist_ok=True)
    det_out.write_bytes((json.dumps({"per_day": detail, "controls": controls, "rule_commit": rule_commit,
                                     "bd_parts": bd_parts, "bd_objects": bd_objs, "bd_rows": len(bd_rows),
                                     "sv_parts": sv_parts, "sv_objects": sv_objs, "sv_rows": len(sv_rows),
                                     "test_held_days": test_held_total},
                                    indent=1, sort_keys=True) + "\n").encode("ascii"))
    print("counts: test_held_days %d; per account by reason shown above; stored match days %d mismatch days %d; "
          "adjacent days not covered %d" % (test_held_total, controls["stored_match_days"],
                                            controls["stored_mismatch_days"], controls["adjacent_uncovered"]))
    print("rows read: BD %d (partitions %d, objects %d); served %d (partitions %d, objects %d)"
          % (len(bd_rows), bd_parts, bd_objs, len(sv_rows), sv_parts, sv_objs))
    print("summary: accounts_closed_with_reasons %d accounts_unexplained %d; code tracked %s"
          % (closed_n, unexpl_n, str(code_tracked).lower()))
    if unexpl_n > 0 and not row_id:
        die("an account stays UNEXPLAINED; a surprise row id is required before the record is written")
    record = {
        "tolerance_pp": TOL_PP,
        "rule": {"file": RULE_FILE, "sha256": sha256_file(root / rule_rel), "commit": rule_commit,
                 "written_before_read": True},
        "reasons_list": list(REASONS),
        "code": {"file": code_rel, "sha256": sha256_file(root / code_rel), "tracked": code_tracked},
        "population": {"accounts": 7, "windows": 7, "differing_days": n_diff_total},
        "test_held_days": test_held_total,
        "round91_pattern_8_days_confirmed": test_held_total == 8,
        "sources": {"bd_transactions_rows_read": len(bd_rows), "served_rows_read": len(sv_rows)},
        "per_account": per_account,
        "summary": {"accounts_closed_with_reasons": closed_n, "accounts_unexplained": unexpl_n},
        "reads": {"vendor_calls": 0, "secret_reads": 0, "s3_writes": 0},
        "served_values_changed": False,
        "limits": ("Counts, offsets and sizes only. Each correction is a single-day recomputation of the day return; "
                   "a closing correction is evidence that a cause is sufficient for the day, not that it is the only "
                   "cause. The served correction recomputes from V, f and m while the test reads the gold return; a "
                   "day is taken only when both hold. A correction does not change the next day's prior value. The "
                   "BD-side denominator is the served prior-day market value. The adjacent-day move is not applied to "
                   "the second day. The served classification is not re-derived; rows are taken whole."),
    }
    if unexpl_n > 0:
        record["surprise_row"] = row_id
    rec_out.write_bytes((json.dumps(record, indent=2, sort_keys=True) + "\n").encode("ascii"))
    print("OK: record written (counts only)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
