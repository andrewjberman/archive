"""IRPT_DASHBD round 90, TO-DB-b-169 (worker 0.9.0_WK_IRPT_DASHBD~136): the day-grain reasons for the 7 UNEXPLAINED segments.

Implements RULE_DAY.md in this folder (committed before any read of the pulled responses) as written.
Reads, read only: the issuer's pull (private folder ~134/pull/), round 89's stored tables (through
tieout_neither_reasons.py, which reads the private copy of ~133), tieout_day_read.py and tieout_neither_reasons.py
(imported by path, not edited). No vendor call, no credential, no S3 access. Writes the record to the given path and the
per-day detail to the private folder of worker ~136 only.

Usage: python -I day_reasons.py <repo_root> <record_out_path> <private_detail_out_path> [<surprise_row_id>]
Prints COUNTS, OFFSETS and SIZES only: no account id, no date.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

TOL_PP = 0.35
DAY_DIFFERS_PP = 0.01
NEAR_DAYS = 5
REASONS = ("MISSING_PRICE", "FLOW_ABSENT_ONE_SIDE", "FLOW_ON_NON_TRADING_DAY", "INCOME_OFF_FLOW_DAY",
           "BD_ACCRUED_INCOME", "UNEXPLAINED")
PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~136/"
PRIV134 = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~134/"
PRIV136 = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~136/"


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


def flagged(p):
    return p is not None and str(p) != ""


def main(argv):
    if len(argv) < 4:
        die("usage: python -I day_reasons.py <repo_root> <record_out> <detail_out> [<surprise_row_id>]")
    repo = Path(argv[1]).resolve()
    rec_out, detail_out = Path(argv[2]), Path(argv[3])
    row_id = argv[4] if len(argv) > 4 else ""
    tdr = import_by_path(repo / PROJ / "tieout" / "tieout_day_read.py", "tieout_day_read")
    nr = import_by_path(repo / PROJ / "tieout" / "tieout_neither_reasons.py", "tieout_neither_reasons")

    # round 89's selection, re-run by tieout_day_read.plan_unexplained (asserts the round-89 record)
    flow_n, _got, unexpl = tdr.plan_unexplained(repo, nr)
    if flow_n != 88 or len(unexpl) != 7:
        die("population does not reproduce")

    pull_rec = tdr.read_json(Path(PRIV134) / "pull" / "DAY_PULL_RECORD.json")
    if pull_rec.get("status") != "COMPLETE" or pull_rec.get("requests") != 7:
        die("the issuer's pull record is not COMPLETE over 7 requests")
    if pull_rec["http_ok"] + pull_rec["http_failed"] != 7:
        die("pull counts do not sum to 7")
    gold = nr.prev.load("read90.pkl")["gold"]

    per_account, detail, closed_n, unexpl_n = [], [], 0, 0
    series_ctrl_all = True
    for i, s in enumerate(unexpl):
        seg_start, seg_end = s["seg"]["start"], s["seg"]["end"]
        seg_start_d = nr.day_of(seg_start)
        series = gold[s["acct"]]
        gdates = sorted(series)
        pos = {d: k for k, d in enumerate(gdates)}
        win = [d for d in gdates if seg_start <= d <= seg_end]
        bdi, bdf = s["bdi"], s["bdf"]
        bdr = float(s["v"]["bdr"])
        G = float(s["gross"])
        o, b = s["o"], s["b"]
        seg_identity = nr.accrual_identity(o, b)

        dates, cums = tdr.series_points(tdr.read_json(Path(PRIV134) / "pull" / ("series_%02d.json" % i)))
        bd_daily = tdr.daily_from_cumulative(cums)
        ctrl = abs(cums[-1] - bdr) <= 1e-9
        series_ctrl_all = series_ctrl_all and ctrl

        days = []
        for d, bv in zip(dates, bd_daily):
            g = series.get(d)
            if not g or g.get("r") is None:
                continue
            k = pos[d]
            prev_d = gdates[k - 1] if k > 0 else None
            m = series[prev_d].get("mv") if prev_d else None
            days.append({"d": d, "dt": nr.day_of(d), "b": bv, "s": float(g["r"]), "V": g.get("mv"),
                         "f": float(g.get("flow") or 0.0), "a": float(g.get("inc_recv") or 0.0),
                         "price": g.get("price_reason"), "m": m,
                         "F": float(bdf.get(d, 0.0)), "I": float(bdi.get(d, 0.0))})

        def app(x):
            return x["m"] is not None and x["m"] != 0

        def trading(j):
            return nr.is_trading(days[j]["dt"])

        def target_of(j):
            for k in range(j + 1, len(days)):
                if trading(k):
                    return k
            for k in range(j - 1, -1, -1):
                if trading(k):
                    return k
            return None

        def pair_of(x):
            # round 89 1.4 over the segment's gold dates, nearest within NEAR_DAYS, ties to the earlier
            if x["a"] == 0 or x["I"] != 0:
                return None
            cands = []
            for d2 in win:
                if d2 == x["d"]:
                    continue
                off = (nr.day_of(d2) - x["dt"]).days
                if abs(off) > NEAR_DAYS:
                    continue
                if nr.tie_amt(float(bdi.get(d2, 0.0)), x["a"]):
                    cands.append((abs(off), off, d2))
            if not cands:
                return None
            return min(cands)[2]

        def corrected(j):
            """Return (test_holds, corrected_return_or_None, target_index_or_None) for reasons 1..5 on day j."""
            x = days[j]
            out = {}
            # 1 MISSING_PRICE: flat-price day
            t1 = flagged(x["price"])
            out[1] = (t1, 0.0 if (t1 and app(x)) else None, None)
            # 2 FLOW_ABSENT_ONE_SIDE: BD flow replaces the served flow
            t2 = (x["f"] != 0) != (x["F"] != 0)
            c2 = (x["V"] - x["F"]) / x["m"] - 1.0 if (t2 and app(x) and x["V"] is not None) else None
            out[2] = (t2, c2, None)
            # 3 FLOW_ON_NON_TRADING_DAY: source flow removed; target must exist and carry m
            t3 = (not trading(j)) and x["f"] != 0
            tgt = target_of(j) if t3 else None
            ok3 = t3 and app(x) and x["V"] is not None and tgt is not None and app(days[tgt])
            c3 = x["V"] / x["m"] - 1.0 if ok3 else None
            out[3] = (t3, c3, tgt if ok3 else None)
            # 4 INCOME_OFF_FLOW_DAY: income removed from the day that books it, moved to the matched day
            d2 = pair_of(x)
            t4 = d2 is not None
            c4 = None
            if t4 and app(x) and x["V"] is not None:
                vadj = x["V"] - x["a"] if d2 > x["d"] else x["V"] + x["a"]
                c4 = (vadj - x["f"]) / x["m"] - 1.0
            out[4] = (t4, c4, None)
            # 5 BD_ACCRUED_INCOME: day gap between BD income and served income, segment identity holds
            bd_inc, a = x["I"], x["a"]
            t5 = (bd_inc != 0 and abs(bd_inc - a) > max(1.0, 0.001 * abs(bd_inc))) and (not t4) and seg_identity
            c5 = None
            if t5 and app(x) and x["V"] is not None:
                vadj = x["V"] + (bd_inc - a)
                c5 = (vadj - x["f"]) / x["m"] - 1.0
            out[5] = (t5, c5, None)
            return out

        counts = {r: 0 for r in REASONS}
        final = [x["s"] for x in days]
        target_adj = []
        unexpl_days = []
        n_diff = 0
        reasoned = {}
        for j, x in enumerate(days):
            if abs((x["b"] - x["s"]) * 100.0) <= DAY_DIFFERS_PP:
                continue
            n_diff += 1
            cs = corrected(j)
            take = None
            for n in (1, 2, 3, 4, 5):
                test, c, tgt = cs[n]
                if test and c is not None and abs((x["b"] - c) * 100.0) <= DAY_DIFFERS_PP:
                    take = (n, c, tgt)
                    break
            if take is None:
                counts["UNEXPLAINED"] += 1
                unexpl_days.append({"offset": (x["dt"] - seg_start_d).days,
                                    "size_pp": round((x["b"] - x["s"]) * 100.0, 4)})
                detail.append({"acct_index": i, "date": x["d"], "reason": "UNEXPLAINED", "diff_pp": (x["b"] - x["s"]) * 100.0})
                continue
            n, c, tgt = take
            counts[REASONS[n - 1]] += 1
            reasoned[j] = c
            if n == 3:
                target_adj.append((tgt, x["f"] / days[tgt]["m"]))
            detail.append({"acct_index": i, "date": x["d"], "reason": REASONS[n - 1], "diff_pp": (x["b"] - x["s"]) * 100.0,
                           "target": (days[tgt]["d"] if tgt is not None else None)})

        for j, c in reasoned.items():
            final[j] = c
        for tgt, amt in target_adj:
            final[tgt] -= amt

        R0 = 1.0
        for x in days:
            R0 *= 1.0 + x["s"]
        R0 -= 1.0
        Rc = 1.0
        for v in final:
            Rc *= 1.0 + v
        Rc -= 1.0
        uncorrected_misses = abs(G - R0) * 100.0 > TOL_PP
        closed_by_correction = abs(G - Rc) * 100.0 <= TOL_PP
        window_closed = counts["UNEXPLAINED"] == 0 and closed_by_correction
        closed_n += 1 if window_closed else 0
        unexpl_n += 0 if window_closed else 1
        per_account.append({"days": len(days), "days_differing": n_diff, "by_reason": counts,
                            "unexplained_days": unexpl_days, "uncorrected_window_misses": uncorrected_misses,
                            "series_last_equals_stored_window": ctrl, "window_closed_after_correction": window_closed})
        for row in detail[-n_diff:] if n_diff else []:
            row["acct_id_private"] = s["acct"]
        print("account %d: days %d differing %d by_reason %s uncorrected_misses %s series_control %s window_closed %s"
              % (i + 1, len(days), n_diff, json.dumps([counts[r] for r in REASONS]), str(uncorrected_misses).lower(),
                 str(ctrl).lower(), str(window_closed).lower()))
        for u in unexpl_days:
            print("  UNEXPLAINED offset %d size_pp %s" % (u["offset"], u["size_pp"]))

    # the code file and the rule: tracked, clean, and the rule committed before the read
    code_rel = FOLDER + "day_reasons.py"
    rc_ls, _ = git(repo, "ls-files", "--error-unmatch", code_rel)
    _, dirty = git(repo, "status", "--porcelain", "--", code_rel)
    code_tracked = rc_ls == 0 and dirty == ""
    rule_rel = FOLDER + "RULE_DAY.md"
    _, rule_commit = git(repo, "log", "-1", "--format=%H", "--", rule_rel)
    _, rule_dirty = git(repo, "status", "--porcelain", "--", rule_rel)
    if not rule_commit or rule_dirty:
        die("RULE_DAY.md is not committed clean")

    detail_out.parent.mkdir(parents=True, exist_ok=True)
    detail_out.write_bytes((json.dumps({"per_day": detail, "rule_commit": rule_commit}, indent=1, sort_keys=True) + "\n").encode("ascii"))

    if unexpl_n > 0 and not row_id:
        die("an account stays UNEXPLAINED; a surprise row id is required")
    record = {
        "tolerance_pp": TOL_PP,
        "day_differs_pp": DAY_DIFFERS_PP,
        "rule": {"file": "RULE_DAY.md", "sha256": sha256_file(repo / rule_rel), "commit": rule_commit,
                 "written_before_read": True},
        "reasons_list": list(REASONS),
        "code": {"file": code_rel, "sha256": sha256_file(repo / code_rel), "tracked": code_tracked},
        "population": {"accounts": len({s["acct"] for s in unexpl}), "segments": len(unexpl)},
        "pull": {"requests": 7, "http_ok": pull_rec["http_ok"], "http_failed": pull_rec["http_failed"]},
        "per_account": per_account,
        "summary": {"accounts_closed_with_reasons": closed_n, "accounts_unexplained": unexpl_n},
        "reads": {"vendor_calls_by_worker": 0, "secret_reads": 0, "s3_writes": 0},
        "served_values_changed": False,
        "limits": ("Counts, offsets and sizes only. Day corrections are single-day recomputations of the served daily "
                   "return; the fee add-back enters the window test only. A closing correction is evidence that a cause "
                   "is sufficient for the day, not that it is the only cause. Trading-day status is lib/trading_calendar "
                   "as it stands."),
    }
    if unexpl_n > 0:
        record["surprise_row"] = row_id
    rec_out.write_bytes((json.dumps(record, indent=2, sort_keys=True) + "\n").encode("ascii"))
    print("series control all 7: %s" % str(series_ctrl_all).lower())
    print("summary: accounts_closed_with_reasons %d accounts_unexplained %d; code tracked %s" % (closed_n, unexpl_n, str(code_tracked).lower()))
    print("OK: record written (counts only)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
