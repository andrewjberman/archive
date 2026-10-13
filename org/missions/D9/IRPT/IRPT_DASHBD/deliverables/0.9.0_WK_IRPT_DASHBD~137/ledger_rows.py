"""IRPT_DASHBD round 91, TO-DB-b-171 (worker 0.9.0_WK_IRPT_DASHBD~137): the ledger rows behind the 23 differing days.

Implements RULE_LEDGER.md in this folder (committed before any read of a transaction or ledger row of the seven
accounts) as written. Reads: round 89's stored tables through tieout_day_read.plan_unexplained (imported by path, not
edited); the issuer's pull (private folder of worker 134, read only); the round-90 gold series through the stored
pickle; and FRESH S3 GET and LIST reads of two stores, all columns, rows of the seven accounts within five calendar
days of a differing day: the Black Diamond landed transactions and the served custody transaction rows (the store the
gold producer's declaration names). No vendor call, no credential, no S3 write.

Usage: python -I ledger_rows.py <repo_root> <record_out_path> <private_detail_out_path> [<surprise_row_id>]
Prints COUNTS, OFFSETS, SIZES and multiples only: no account id, no name, no amount, no date.
"""
import collections
import datetime as dt
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.config import Config

TOL_PP = 0.35
DAY_DIFFERS_PP = 0.01
NEAR_DAYS = 5
ADJ_SEARCH_DAYS = 10
REASONS = ("BD_INCOME_PER_LOT", "DUPLICATE_ROW", "BOOKING_DATE_DIFFERS", "MISSING_IN_LEDGER", "UNEXPLAINED")
KIND = {"BD_INCOME_PER_LOT": "multiple", "DUPLICATE_ROW": "count", "BOOKING_DATE_DIFFERS": "day_offsets",
        "MISSING_IN_LEDGER": "count"}
PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~137/"
DECL = "data/assets/scripts/gold/irpt_reporting/sources.json"
PRIV134 = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~134/"
BD_BUCKET = "opal-data-assets"
BD_PREFIX = "blackdiamond/49financial/silver_legacy/transactions/"
FLOW_KINDS = ("Contribution", "Withdrawal")
STORED_TOL = 0.005
BD_SIDE, SV_SIDE = "BD", "SV"


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


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def norm_acct(x):
    return str(x).strip().lstrip("0")


def day_str(v):
    return str(v)[:10]


def sec_key(r):
    return str(r.get("cusip") or "") or str(r.get("asset_id") or "")


def window_of(d, k=NEAR_DAYS):
    base = dt.date.fromisoformat(d)
    return {(base + dt.timedelta(days=j)).isoformat() for j in range(-k, k + 1)}


def get_bytes(s3, bucket, key):
    last = "none"
    for attempt in range(3):
        try:
            return s3.get_object(Bucket=bucket, Key=key)["Body"].read()
        except Exception as e:  # class name only: a message can carry a key
            last = type(e).__name__
            time.sleep(1.0 * (attempt + 1))
    die("an object could not be read after 3 attempts (%s); it is not folded into an absence" % last)
    return b""


def read_store(s3, bucket, prefix, acct_col, date_col, want, partition_ok):
    """Rows of the wanted accounts whose date (first ten characters) is in that account's window, all columns.

    want maps a normalised account to the set of its window dates. Returns (rows, partitions listed, objects read)."""
    parts = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for cp in page.get("CommonPrefixes", []) or []:
            tok = cp["Prefix"][len(prefix):].rstrip("/")
            if partition_ok(tok):
                parts.append(cp["Prefix"])

    def one(pref):
        keys = []
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=pref):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith(".parquet"):
                    keys.append(o["Key"])
        out, n_obj = [], 0
        for k in keys:
            t = pq.read_table(io.BytesIO(get_bytes(s3, bucket, k)))
            n_obj += 1
            accts = t.column(acct_col).to_pylist()
            dates = t.column(date_col).to_pylist()
            idx = []
            for i, (a, dv) in enumerate(zip(accts, dates)):
                if a is None or dv is None:
                    continue
                win = want.get(norm_acct(a))
                if win and day_str(dv) in win:
                    idx.append(i)
            if idx:
                out += t.take(pa.array(idx, type=pa.int64())).to_pylist()
        return out, n_obj

    rows, objs = [], 0
    with ThreadPoolExecutor(16) as ex:
        for part_rows, n_obj in ex.map(one, parts):
            rows += part_rows
            objs += n_obj
    return rows, len(parts), objs


def served_declaration(root):
    doc = json.loads((Path(root) / DECL).read_text(encoding="utf-8"))
    keys = [k for k in doc if isinstance(doc[k], dict) and not k.startswith("_")]
    if len(keys) != 1:
        die("the producer's declaration names %d custody sources; one is expected" % len(keys))
    e = doc[keys[0]]
    return e["bucket"], e["transactions_prefix"], e["account_column"], e["date_column"]


def sums(rows):
    inc = sum(fnum(r.get("income")) for r in rows)
    flow = sum(fnum(r.get("market_value")) for r in rows if r.get("external_flow") in FLOW_KINDS)
    return inc, flow


def candidates(x, bd_d, sv_d, sv_win, adj, nr):
    """RULE_LEDGER.md section 1, in the closed-list order. Each item: (reason number, side, corrected value or None,
    evidence value). A value of None means the correction needs an absent or zero m(d) or V(d)."""
    b, V, f, a, m = x["b"], x["V"], x["f"], x["a"], x["m"]
    app = m is not None and m != 0
    I, F = sums(bd_d)  # noqa: E741 -- I is the rule's own symbol for the day's BD income sum
    out = []

    def bd_after(rm_inc, rm_flow):
        return (b - rm_inc / m + rm_flow / m) if app else None

    def sv_after(dv, df):
        return ((V + dv - (f + df)) / m - 1.0) if (app and V is not None) else None

    def first_adj(pred):
        for off, a2, f2, i2, f_2 in adj:
            if pred(a2, f2, i2, f_2):
                return off
        return None

    # (1) BD_INCOME_PER_LOT
    inc_rows = [r for r in bd_d if fnum(r.get("income")) != 0.0]
    if a != 0 and len(inc_rows) >= 2 and len({str(r.get("transaction_id")) for r in inc_rows}) >= 2 and I != 0:
        k = int(round(I / a))
        if k >= 2 and nr.tie_amt(I, k * a):
            out.append((1, BD_SIDE, bd_after(I - a, 0.0), k))

    # (2) DUPLICATE_ROW, BD arm then served arm
    groups, amt = collections.Counter(), {}
    for r in bd_d:
        if fnum(r.get("income")) != 0.0:
            key = ("inc", round(fnum(r.get("income")), 2), sec_key(r))
            groups[key] += 1
            amt[key] = fnum(r.get("income"))
        if r.get("external_flow") in FLOW_KINDS and fnum(r.get("market_value")) != 0.0:
            key = ("flow", round(fnum(r.get("market_value")), 2), sec_key(r))
            groups[key] += 1
            amt[key] = fnum(r.get("market_value"))
    dup = {k: c for k, c in groups.items() if c >= 2}
    if dup:
        extra_inc = sum((c - 1) * amt[k] for k, c in dup.items() if k[0] == "inc")
        extra_flow = sum((c - 1) * amt[k] for k, c in dup.items() if k[0] == "flow")
        copies = sum(c - 1 for c in dup.values())
        out.append((2, BD_SIDE, bd_after(extra_inc, extra_flow), copies))
    sv_groups = collections.Counter()
    for r in sv_d:
        g = fnum(r.get("gross_amount"))
        if g != 0.0:
            sv_groups[(round(abs(g), 2), str(r.get("cusip") or ""))] += 1
    for key in sorted(sv_groups):
        c = sv_groups[key]
        if c < 2:
            continue
        x2 = 2.0 * key[0]
        if a != 0 and nr.tie_amt(abs(a), x2):
            out.append((2, SV_SIDE, sv_after(-a / 2.0, 0.0), c - 1))
            break
        if f != 0 and nr.tie_amt(abs(f), x2):
            out.append((2, SV_SIDE, sv_after(0.0, -f / 2.0), c - 1))
            break

    # (3) BOOKING_DATE_DIFFERS: BD income, BD flow, served income, served flow
    if I != 0 and not nr.tie_amt(I, a):
        off = first_adj(lambda a2, f2, i2, f_2: nr.tie_amt(I, a2))
        if off is not None:
            out.append((3, BD_SIDE, bd_after(I, 0.0), off))
    if F != 0 and not nr.tie_amt(F, f):
        off = first_adj(lambda a2, f2, i2, f_2: nr.tie_amt(F, f2))
        if off is not None:
            out.append((3, BD_SIDE, bd_after(0.0, F), off))
    if a != 0 and not nr.tie_amt(a, I):
        off = first_adj(lambda a2, f2, i2, f_2: nr.tie_amt(a, i2))
        if off is not None:
            out.append((3, SV_SIDE, sv_after(-a, 0.0), off))
    if f != 0 and not nr.tie_amt(f, F):
        off = first_adj(lambda a2, f2, i2, f_2: nr.tie_amt(f, f_2))
        if off is not None:
            out.append((3, SV_SIDE, sv_after(0.0, -f), off))

    # (4) MISSING_IN_LEDGER: a BD row with no served row of |gross| within five calendar days
    miss_inc = miss_flow = 0.0
    n_miss = 0
    for r in bd_d:
        cands = []
        if fnum(r.get("income")) != 0.0:
            cands.append(("inc", fnum(r.get("income"))))
        if r.get("external_flow") in FLOW_KINDS and fnum(r.get("market_value")) != 0.0:
            cands.append(("flow", fnum(r.get("market_value"))))
        for kind, val in cands:
            if not any(nr.tie_amt(abs(fnum(q.get("gross_amount"))), abs(val)) for q in sv_win):
                n_miss += 1
                if kind == "inc":
                    miss_inc += val
                else:
                    miss_flow += val
    if n_miss > 0:
        out.append((4, SV_SIDE, sv_after(miss_inc, miss_flow), n_miss))
    return out


def take(cands, x):
    for reason_no, side, corr, ev in cands:
        if corr is None:
            continue
        if side == BD_SIDE:
            ok = abs((corr - x["s"]) * 100.0) <= DAY_DIFFERS_PP
        else:
            ok = abs((x["b"] - corr) * 100.0) <= DAY_DIFFERS_PP
        if ok:
            return reason_no, side, corr, ev
    return None


def main(argv):
    if len(argv) < 4:
        die("usage: python -I ledger_rows.py <repo_root> <record_out> <private_detail_out> [<surprise_row_id>]")
    root = Path(argv[1]).resolve()
    rec_out, det_out = Path(argv[2]), Path(argv[3])
    row_id = argv[4] if len(argv) > 4 else ""
    tdr = import_by_path(root / PROJ / "tieout" / "tieout_day_read.py", "tieout_day_read")
    nr = import_by_path(root / PROJ / "tieout" / "tieout_neither_reasons.py", "tieout_neither_reasons")

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
            want_bd[norm_acct(s["acct"])] |= window_of(x["d"])
            want_sv[norm_acct(s["acct"])] |= window_of(x["d"])
        accts.append({"i": i, "s": s, "seg_start": nr.day_of(seg_start), "seg_gold": seg_gold, "days": days,
                      "diff": diff, "gdates": gdates})

    n_accounts = len(accts)
    n_diff_total = sum(len(a["diff"]) for a in accts)
    if n_accounts != 7 or n_diff_total != 23:
        die("population %d accounts and %d differing days; expected 7 and 23" % (n_accounts, n_diff_total))

    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40,
                                                                   retries={"max_attempts": 8, "mode": "standard"}))
    bd_rows, bd_parts, bd_objs = read_store(s3, BD_BUCKET, BD_PREFIX, "account_number", "return_date",
                                            want_bd, lambda tok: True)
    sv_bucket, sv_prefix, sv_acct_col, sv_date_col = served_declaration(root)
    all_dates = sorted({d for w in want_sv.values() for d in w})
    lo, hi = all_dates[0], all_dates[-1]
    sv_rows, sv_parts, sv_objs = read_store(s3, sv_bucket, sv_prefix, sv_acct_col, sv_date_col, want_sv,
                                            lambda tok: tok.startswith("date=") and lo <= tok[5:] <= hi)

    bd_by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in bd_rows:
        bd_by[norm_acct(r.get("account_number"))][day_str(r.get("return_date"))].append(r)
    sv_by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in sv_rows:
        sv_by[norm_acct(r.get(sv_acct_col))][day_str(r.get(sv_date_col))].append(r)

    per_account, detail = [], []
    closed_n = unexpl_n = 0
    controls = {"stored_match_days": 0, "stored_mismatch_days": 0, "adjacent_uncovered": 0,
                "multi_group_duplicates": 0}
    rows_by_reason = collections.Counter()
    for a_rec in accts:
        s = a_rec["s"]
        key = norm_acct(s["acct"])
        bd_day = bd_by.get(key, {})
        sv_day = sv_by.get(key, {})
        covered = want_bd.get(key, set())
        for d in sorted(covered):
            inc, flow = sums(bd_day.get(d, []))
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
        for j, x in enumerate(a_rec["days"]):
            differs = abs((x["b"] - x["s"]) * 100.0) > DAY_DIFFERS_PP
            if not differs:
                continue
            ndiff += 1
            d = x["d"]
            bd_d = bd_day.get(d, [])
            sv_d = sv_day.get(d, [])
            sv_win = []
            for dd in window_of(d):
                sv_win += sv_day.get(dd, [])
            sv_win = [q for q in sv_win if fnum(q.get("gross_amount")) != 0.0]
            adj = []
            for step in (-1, 1):
                cand = x["dt"]
                for _k in range(ADJ_SEARCH_DAYS):
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
                i2, f2 = sums(bd_day.get(d2, []))
                adj.append(((cand - x["dt"]).days, float(g2.get("inc_recv") or 0.0),
                            float(g2.get("flow") or 0.0), i2, f2))
            cands = candidates(x, bd_d, sv_d, sv_win, adj, nr)
            hit = take(cands, x)
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
            rows_by_reason[name] += 1
            evid[name].append(int(ev))
            if side == BD_SIDE:
                pbd *= (1.0 + corr) / (1.0 + x["b"])
                final_s.append(x["s"])
            else:
                final_s.append(corr)
            detail.append({"acct_index": a_rec["i"], "date": d, "reason": name, "side": side, "evidence": int(ev),
                           "size_pp": (x["b"] - x["s"]) * 100.0})
        # the window: R0, R_c, G_c (RULE_LEDGER section 2 and 3)
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
        print("account %d: days %d differing %d by_reason %s uncorrected_misses %s window_closed %s"
              % (a_rec["i"] + 1, len(a_rec["days"]), ndiff, json.dumps([counts[r] for r in REASONS]),
                 str(misses).lower(), str(closed).lower()))
        for u in unexpl_days:
            print("  UNEXPLAINED offset %d size_pp %s" % (u["offset"], u["size_pp"]))

    code_rel = FOLDER + "ledger_rows.py"
    rc_ls, _ = git(root, "ls-files", "--error-unmatch", code_rel)
    _, dirty = git(root, "status", "--porcelain", "--", code_rel)
    code_tracked = rc_ls == 0 and dirty == ""
    rule_rel = FOLDER + "RULE_LEDGER.md"
    _, rule_commit = git(root, "log", "-1", "--format=%H", "--", rule_rel)
    _, rule_dirty = git(root, "status", "--porcelain", "--", rule_rel)
    if not rule_commit or rule_dirty:
        die("RULE_LEDGER.md is not committed clean")

    det_out.parent.mkdir(parents=True, exist_ok=True)
    det_out.write_bytes((json.dumps({"per_day": detail, "controls": controls, "rule_commit": rule_commit,
                                     "bd_parts": bd_parts, "bd_objects": bd_objs, "bd_rows": len(bd_rows),
                                     "sv_parts": sv_parts, "sv_objects": sv_objs, "sv_rows": len(sv_rows)},
                                    indent=1, sort_keys=True) + "\n").encode("ascii"))
    if unexpl_n > 0 and not row_id:
        die("an account stays UNEXPLAINED; a surprise row id is required")
    record = {
        "tolerance_pp": TOL_PP,
        "rule": {"file": "RULE_LEDGER.md", "sha256": sha256_file(root / rule_rel), "commit": rule_commit,
                 "written_before_read": True},
        "reasons_list": list(REASONS),
        "code": {"file": code_rel, "sha256": sha256_file(root / code_rel), "tracked": code_tracked},
        "population": {"accounts": 7, "windows": 7, "differing_days": n_diff_total},
        "sources": {"bd_transactions_rows_read": len(bd_rows), "served_rows_read": len(sv_rows)},
        "per_account": per_account,
        "summary": {"accounts_closed_with_reasons": closed_n, "accounts_unexplained": unexpl_n},
        "reads": {"vendor_calls": 0, "secret_reads": 0, "s3_writes": 0},
        "served_values_changed": False,
        "limits": ("Counts, offsets and sizes only. Each correction is a single-day recomputation of the day return; "
                   "a closing correction is evidence that a cause is sufficient for the day, not that it is the only "
                   "cause. The BD-side denominator is the served prior-day market value. The adjacent-day move is not "
                   "applied to the second day. The served classification is not re-derived; rows are taken whole."),
    }
    if unexpl_n > 0:
        record["surprise_row"] = row_id
    rec_out.write_bytes((json.dumps(record, indent=2, sort_keys=True) + "\n").encode("ascii"))
    print("controls: stored match days %d mismatch days %d; adjacent days not covered %d"
          % (controls["stored_match_days"], controls["stored_mismatch_days"], controls["adjacent_uncovered"]))
    print("rows read: BD %d (partitions %d, objects %d); served %d (partitions %d, objects %d)"
          % (len(bd_rows), bd_parts, bd_objs, len(sv_rows), sv_parts, sv_objs))
    print("summary: accounts_closed_with_reasons %d accounts_unexplained %d; code tracked %s"
          % (closed_n, unexpl_n, str(code_tracked).lower()))
    print("OK: record written (counts only)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
