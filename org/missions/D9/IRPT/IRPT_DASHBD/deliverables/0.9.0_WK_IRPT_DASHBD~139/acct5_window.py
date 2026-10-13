"""IRPT_DASHBD round 93, TO-DB-b-173 (worker 0.9.0_WK_IRPT_DASHBD~139): account 5's window return after its reasoned
days are corrected, against 0.35 pp. ONE figure. DIRECT ACT, LOCAL: no S3 access, no vendor call, no credential.

Reads only stored local files: the issuer's pull of the fifth request's daily series (private ~134 pull/series_04.json),
the stored round-90 tables through tieout_neither_reasons (private ~108/~133 copy, read only), DAY_READ_PLAN.json, and
round 92's committed record for the fifth account. Imports by path, does not edit: tieout_day_read.py and
tieout_neither_reasons.py. The method is round 92's RULE_EXCL.md, reused unchanged and bound by hash:
section 2 (the reason BD_EXCLUDES_SERVED_INCOME: TEST and served CORRECTION) and section 5 (the window method).
The 3 UNEXPLAINED days stay as served. No BD-side correction is taken for this account, so P_bd = 1 and G_c = G.

Usage: python -I acct5_window.py <repo_root> <record_out> <private_detail_out>
Prints COUNTS and the two gaps only. Writes the record (keys fixed by TO-DB-b-173) and the private detail.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

TOL_PP = 0.35
DAY_DIFFERS_PP = 0.01
PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~139/"
RULE_REL = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~138/RULE_EXCL.md"
R92_REL = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~138/EXCLUDES_INCOME_23_DAYS.json"
PRIV134 = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~134/"
ACCT_INDEX = 4          # fifth request of the round-90 plan order = account 5
WANT_REASONED = 4
WANT_UNEXPL = 3
LIMITS = ("The figure is a recomputation of the window return under round 92's stored rule, not a statement of which "
          "system is right.")


def die(msg):
    print("ERROR: " + msg)
    sys.exit(2)


def import_by_path(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode("ascii", "replace").strip()


def excl_test(x):
    """RULE_EXCL.md section 2 TEST: a != 0, m applicable, |(b - s) + a / m| * 100 <= 0.01."""
    a, m = x["a"], x["m"]
    if a == 0 or m is None or m == 0:
        return False
    return abs((x["b"] - x["s"]) + a / m) * 100.0 <= DAY_DIFFERS_PP


def excl_corr(x):
    """RULE_EXCL.md section 2 CORRECTION: c = (V - a - f) / m - 1; needs V non-null and m applicable."""
    a, m, V, f = x["a"], x["m"], x["V"], x["f"]
    if m is None or m == 0 or V is None:
        return None
    return (V - a - f) / m - 1.0


def main(argv):
    if len(argv) < 4:
        die("usage: python -I acct5_window.py <repo_root> <record_out> <private_detail_out>")
    root = Path(argv[1]).resolve()
    rec_out, det_out = Path(argv[2]), Path(argv[3])
    code_rel = FOLDER + "acct5_window.py"
    rc_ls, _ = git(root, "ls-files", "--error-unmatch", code_rel)
    _, dirty = git(root, "status", "--porcelain", "--", code_rel)
    if rc_ls != 0 or dirty:
        die("this module is not tracked and clean; commit it before the record is written")
    code_sha = sha256_bytes((root / code_rel).read_bytes())
    rule_sha = sha256_bytes((root / RULE_REL).read_bytes())

    tdr = import_by_path(root / PROJ / "tieout" / "tieout_day_read.py", "tieout_day_read")
    nr = import_by_path(root / PROJ / "tieout" / "tieout_neither_reasons.py", "tieout_neither_reasons")
    flow_n, _got, unexpl = tdr.plan_unexplained(root, nr)
    if flow_n != 88 or len(unexpl) != 7:
        die("population does not reproduce")
    plan = tdr.read_json(Path(PRIV134) / "DAY_READ_PLAN.json")
    s = unexpl[ACCT_INDEX]
    if plan["requests"][ACCT_INDEX]["account"] != s["acct"]:
        die("plan order differs from the round-89 selection at the fifth position")
    gold = nr.prev.load("read90.pkl")["gold"]
    series = gold[s["acct"]]
    gdates = sorted(series)
    pos = {d: k for k, d in enumerate(gdates)}
    dates, cums = tdr.series_points(tdr.read_json(Path(PRIV134) / "pull" / ("series_%02d.json" % ACCT_INDEX)))
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
    if len(diff) != 7:
        die("account 5 does not show 7 differing days (reproduced %d)" % len(diff))

    # round 92's committed record for the fifth account: the assertion this module must reproduce
    r92 = tdr.read_json(root / R92_REL)
    a5 = r92["per_account"][ACCT_INDEX]
    if a5["days_differing"] != 7 or a5["by_reason"]["BD_EXCLUDES_SERVED_INCOME"] != WANT_REASONED \
            or a5["by_reason"]["UNEXPLAINED"] != WANT_UNEXPL or a5["uncorrected_window_misses"] is not True:
        die("round 92's record for the fifth account does not read 7 days, 4 reasoned, 3 unexplained")
    want_k = sorted(a5["evidence"]["BD_EXCLUDES_SERVED_INCOME"]["values"])

    # reason (1), BD_EXCLUDES_SERVED_INCOME: the first reason of the list, so it decides the reasoned days
    taken, ks, test_held = {}, [], 0
    detail = []
    other_reason2 = 0
    for x in diff:
        d = x["d"]
        inc_sum = float(s["bdi"].get(d, 0.0))
        a = x["a"]
        if excl_test(x):
            test_held += 1
        c = excl_corr(x) if excl_test(x) else None
        hit = c is not None and abs(x["b"] - c) * 100.0 <= DAY_DIFFERS_PP
        if hit:
            taken[d] = c
            ks.append(int(round(inc_sum / a)) if inc_sum != 0 else 0)
        # conservative look at reason (2) on the untaken days, from the stored BD income sum only: the TEST without
        # its two-rows clause and the BD-side correction; a pass here would need the BD rows to settle
        if not hit and a != 0 and inc_sum != 0 and x["m"] not in (None, 0):
            k2 = int(round(inc_sum / a))
            tie = abs(inc_sum - k2 * a) <= max(1.0, 0.001 * abs(k2 * a))
            if k2 >= 2 and tie:
                bprime = x["b"] - (inc_sum - a) / x["m"]
                if abs((bprime - x["s"]) * 100.0) <= DAY_DIFFERS_PP:
                    other_reason2 += 1
        detail.append({"date": d, "reason_1_taken": hit, "size_pp": (x["b"] - x["s"]) * 100.0,
                       "corrected_return": c if hit else None})
    if len(taken) != WANT_REASONED or len(diff) - len(taken) != WANT_UNEXPL:
        die("reason (1) reproduces %d reasoned and %d other days; round 92 has %d and %d"
            % (len(taken), len(diff) - len(taken), WANT_REASONED, WANT_UNEXPL))
    if sorted(ks) != want_k:
        die("reason (1) evidence multiples do not match round 92's committed record")

    # RULE_EXCL.md section 5 and 6: window closure, served values never move
    G = float(s["gross"])
    R0 = 1.0
    for x in days:
        R0 *= 1.0 + x["s"]
    R0 -= 1.0
    Rc = 1.0
    for x in days:
        Rc *= 1.0 + taken.get(x["d"], x["s"])
    Rc -= 1.0
    Gc = G  # P_bd = 1: no BD-side correction is taken for this account
    ug = abs(G - R0) * 100.0
    cg = abs(Gc - Rc) * 100.0
    if ug <= TOL_PP:
        die("the uncorrected window does not miss by more than 0.35 pp (negative arm fails)")
    ug4, cg4 = round(ug, 4), round(cg, 4)
    if ug4 == cg4:
        die("the corrected gap equals the uncorrected gap at four decimals")
    inside = cg <= TOL_PP
    if inside != (cg4 <= TOL_PP):
        die("the four-decimal rounding flips the tolerance verdict; refusing to write")

    record = {
        "tolerance_pp": TOL_PP,
        "rule": {"file": RULE_REL, "sha256": rule_sha, "reused_unchanged": True},
        "code": {"file": code_rel, "sha256": code_sha, "tracked": True},
        "account_index_plan_order": ACCT_INDEX + 1,
        "reasoned_days": WANT_REASONED,
        "unexplained_days": WANT_UNEXPL,
        "uncorrected_gap_pp": ug4,
        "corrected_gap_pp": cg4,
        "inside_tolerance": bool(inside),
        "reads": {"vendor_calls": 0, "secret_reads": 0, "s3_writes": 0, "s3_reads": 0},
        "served_values_changed": False,
        "limits": LIMITS,
    }
    det_out.parent.mkdir(parents=True, exist_ok=True)
    det_out.write_bytes((json.dumps({"days": detail, "test_held_days": test_held,
                                     "reason2_passes_without_rows": other_reason2, "G": G, "R0": R0, "Rc": Rc},
                                    indent=1, sort_keys=True) + "\n").encode("ascii"))
    rec_out.parent.mkdir(parents=True, exist_ok=True)
    rec_out.write_bytes((json.dumps(record, indent=2, sort_keys=True) + "\n").encode("ascii"))
    print("counts: differing days %d; reason (1) taken %d; unexplained %d; test held %d; reason (2) candidates on the "
          "unexplained days without the rows clause %d" % (len(diff), len(taken), len(diff) - len(taken), test_held,
                                                             other_reason2))
    print("reads: vendor_calls 0, secret_reads 0, s3_reads 0, s3_writes 0; served values changed: false")
    print("gap uncorrected %.4f pp; gap corrected %.4f pp; inside 0.35 pp: %s"
          % (ug4, cg4, str(bool(inside)).lower()))
    print("OK: record written (counts and gaps only)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
