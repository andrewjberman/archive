"""IRPT_DASHBD round 115, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the gap decomposition read (CTO round-115 analysis, msg 7956).

  DB-i-3 (~303) about 12 Inflection households across the QTD gap bins, each named difference between the Opal derivation and Orion's client factor tested ALONE
              against the round-109 baseline: gross against net of fees, trade against settlement date, flow timing inside a day, income accrual, the cash sweep. The
              explained share per household per variant. A READ: nothing is written to AWS.                                                      DBI115-1-AC1

The checker RECOMPUTES: the sample from round 114's private variant file (all households at 100 bp or more, plus the lowest-sha household of each other bin), the baseline
against round 114's `all` gaps, the identity control (a variant that changes nothing must equal the baseline), and every explained share from the signed gaps.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the pure helpers on synthetic arms
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("p114_bin", str(HERE.parent / "r114" / "p114_bin.py"))
P114 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P114)
Fail, need = P114.Fail, P114.need

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~303/GAP_DECOMPOSITION_R115.json"
REC114_REL = D + "0.9.0_WK_IRPT_DASHBD~301/BASIS_VARIANTS_R114.json"
VARIANTS = ("base", "identity", "gross_fees", "settle_timing", "flow_start_of_day", "flow_midday", "income_accrual", "ex_cash_value", "ex_cash_no_flows")
DIFFERENCES = {
    "gross_vs_net_of_fees": ["gross_fees"],
    "trade_vs_settlement_date": ["settle_timing"],
    "flow_timing_in_a_day": ["flow_start_of_day", "flow_midday"],
    "income_accrual": ["income_accrual"],
    "cash_sweep": ["ex_cash_value", "ex_cash_no_flows"],
}
TESTED_VARIANTS = tuple(v for v in VARIANTS if v not in ("base", "identity"))
STATUSES = ("TESTED", "NOT_TESTABLE")
TOP_BIN = "ge_100bp"
OTHER_BINS = ("lt_5bp", "5_25bp", "25_100bp")
TOL_BP = 0.01
MIN_BASE_BP = 0.01


def share(base, var):
    """Explained share of the baseline signed gap by one variant: (base - var) / base; None when either is null or the base is ~0."""
    if base is None or var is None or base != base or var != var or abs(base) < MIN_BASE_BP:
        return None
    return (base - var) / base


def select_sample(rows):
    """rows: iterable of (household_sha256, gap_bp or None) for the `all` variant -> sorted list: every household at 100 bp or more, plus the lowest sha of each other bin."""
    by = {b: [] for b in P114.BINS}
    for h, g in rows:
        if g is None or g != g:
            continue
        by[P114.bin_of(abs(g))].append(h)
    out = list(by[TOP_BIN])
    for b in OTHER_BINS:
        if by[b]:
            out.append(sorted(by[b])[0])
    return sorted(out)


def check(root):
    import pyarrow.parquet as pq
    rec = P114.load(root, REC_REL)
    P114.no_identifiers(rec)
    P114.common_flags(rec)
    P114.script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 120, "basis_words missing")
    need(rec.get("window") == "qtd", "window must be qtd")
    # the sample, recomputed from round 114's private variant file
    r114 = P114.load(root, REC114_REL)
    f114 = r114["variant_file"]
    need(Path(f114["path"]).is_file() and P114.sha(f114["path"]) == f114["sha256"], "round-114 variant file absent or changed")
    t114 = pq.read_table(f114["path"]).to_pandas()
    ta = t114[t114["variant"] == "all"]
    base114 = {h: g for h, g in zip(ta["household_sha256"], ta["gap_bp"])}
    sample = select_sample(base114.items())
    need(len(sample) >= 9 and sample == sorted(rec.get("sample_households_sha256", [])), "the recorded sample differs from the selection rule applied to round 114")
    # the worker's private file
    vf = rec["variant_file"]
    need(Path(vf["path"]).is_file() and vf["path"].replace("\\", "/").startswith(P114.PRIV), "variant file absent or outside the private folder")
    need(P114.sha(vf["path"]) == vf["sha256"], "variant file sha256 differs from the record")
    t = pq.read_table(vf["path"]).to_pandas()
    need(list(t.columns) == ["household_sha256", "variant", "signed_gap_bp", "reason"], "variant file columns")
    need(len(t) == len(sample) * len(VARIANTS), "variant file rows != sample x variants")
    gaps = {}
    for v in VARIANTS:
        tv = t[t["variant"] == v]
        need(sorted(tv["household_sha256"]) == sample, "variant %s: households differ from the sample (or a repeat)" % v)
        nulls = tv[tv["signed_gap_bp"].isna()]
        need(all(isinstance(x, str) and x.strip() for x in nulls["reason"]), "variant %s: a null gap without a reason" % v)
        gaps[v] = {h: (None if g != g else float(g)) for h, g in zip(tv["household_sha256"], tv["signed_gap_bp"])}
    # the control: base is round 114's `all`, identity changes nothing
    for h in sample:
        need(gaps["base"][h] is not None, "base gap null for a sampled household")
        need(abs(abs(gaps["base"][h]) - abs(base114[h])) <= TOL_BP, "base differs from round 114's all gap for a sampled household")
        need(gaps["identity"][h] is not None and abs(gaps["identity"][h] - gaps["base"][h]) <= TOL_BP, "identity differs from base for a sampled household")
    # the differences and variant statuses
    need(rec.get("differences") == DIFFERENCES, "differences map must be exactly the five named differences")
    need(sorted(rec.get("variants", {})) == sorted(TESTED_VARIANTS), "variants must be exactly the tested variants")
    for v in TESTED_VARIANTS:
        r = rec["variants"][v]
        need(r.get("status") in STATUSES and r.get("claim") in P114.CLAIMS, "variant %s: status or claim" % v)
        need(isinstance(r.get("words"), str) and len(r["words"]) > 20, "variant %s: words" % v)
        non_null = [h for h in sample if gaps[v][h] is not None]
        if r["status"] == "TESTED":
            need(len(non_null) >= 1, "variant %s: TESTED with no computable household" % v)
        else:
            need(len(non_null) == 0, "variant %s: NOT_TESTABLE but gaps are present" % v)
    # the shares, recomputed
    sh = rec.get("explained_share", {})
    need(sorted(sh) == sorted(TESTED_VARIANTS), "explained_share must carry every tested variant")
    best_over_half = 0
    for h in sample:
        best = None
        for v in TESTED_VARIANTS:
            exp = share(gaps["base"][h], gaps[v][h])
            got = sh[v].get(h, "absent")
            need(got != "absent", "explained_share.%s lacks a sampled household" % v)
            need((exp is None) == (got is None) and (exp is None or abs(exp - got) <= 1e-6), "explained_share.%s differs from the recount" % v)
            if exp is not None and (best is None or exp > best):
                best = exp
        if best is not None and best >= 0.5:
            best_over_half += 1
    need(rec.get("households_with_a_single_difference_explaining_half") == best_over_half, "households_with_a_single_difference_explaining_half differs from the recount (%d)" % best_over_half)
    need(rec.get("sample_size") == len(sample), "sample_size")


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    arm("share half", abs(share(10.0, 5.0) - 0.5) < 1e-12)
    arm("share overshoot signed", abs(share(10.0, -5.0) - 1.5) < 1e-12)
    arm("share negative", share(10.0, 15.0) < 0)
    arm("share null", share(None, 1.0) is None and share(1.0, None) is None and share(0.0, 1.0) is None)
    rows = [("h%d" % i, 150.0 + i) for i in range(9)] + [("a2", 60.0), ("a1", 30.0), ("b", 10.0), ("c", 1.0), ("n", None)]
    arm("select_sample", select_sample(rows) == sorted(["h%d" % i for i in range(9)] + ["a1", "b", "c"]))
    arm("diff map covers all tested variants", sorted(v for vs in DIFFERENCES.values() for v in vs) == sorted(TESTED_VARIANTS))
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] != "DBI115-1-AC1":
        print("usage: <root> DBI115-1-AC1")
        sys.exit(2)
    try:
        check(argv[0])
    except Fail as e:
        print("%s FAIL: %s" % (argv[1], e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    except Exception as e:  # a checker error is a FAIL, never a pass
        print("%s FAIL: checker error %s: %s" % (argv[1], type(e).__name__, e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    print("%s PASS" % argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
