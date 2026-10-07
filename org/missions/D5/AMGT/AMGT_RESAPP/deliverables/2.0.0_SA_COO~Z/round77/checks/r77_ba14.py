"""AMGT_RESAPP round 77 -- AMGT-ba-14 (FWD-20, the trailing-trend house FCF forecast v1). Issuer checks.

  python r77_ba14.py --crit AC1|AC2|AC3 [--where local]

AC1 (build)   lib.research.scores.house_fcf.forecast(model_block): FY1-FY3 FCF = revenue x FCF margin, revenue grown at
              the MEDIAN of the last 3-5 annual changes, margin the trailing MEDIAN of FCF / revenue, both from the
              reported history only. Difference control: changing every consensus (BEST_*) figure leaves it EQUAL.
              A name short of history is ABSENT with its reason. The reference is labelled bloomberg_reported_period.
AC2 (build)   house_fcf.universe_summary(records): the sd(D) >= 0.25 gate through divergence.check_degeneracy, and the
              cross-sectional correlation of house FCF to consensus FCF as a reported figure beside it.
AC3 (control) the names the serving adapter reads are unchanged, and score_divergence() with no house forecast stays
              ABSENT with the plain reason. PASSES at the base.

Pure fixtures: no S3 read, no vendor call.
"""
import argparse
import copy
import importlib
import sys

OK = []


def clause(label, ok, detail=""):
    OK.append(bool(ok))
    print("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))


def fig(mnemonic, fy, value, scope="fiscal_year_line_item"):
    return {"scope": scope, "fiscal_year": fy, "mnemonic": mnemonic, "value": value, "unit": "MILLIONS",
            "currency": "USD"}


REV = [100.0, 110.0, 132.0, 138.6, 152.46, 175.329]  # annual changes: .10 .20 .05 .10 .15 -> median .10
MARGIN = [0.08, 0.12, 0.10, 0.10, 0.09, 0.11]        # last five: .12 .10 .10 .09 .11 -> median .10
YEARS = ["2020", "2021", "2022", "2023", "2024", "2025"]


def block(n_years=6, consensus=1000.0):
    figs = []
    for y, r, m in list(zip(YEARS, REV, MARGIN))[-n_years:]:
        figs.append(fig("SALES_REV_TURN", y, r))
        figs.append(fig("CF_FREE_CASH_FLOW", y, r * m))
    for i, fy in enumerate((2026, 2027, 2028)):
        f = fig("BEST_ESTIMATE_FCF", fy, consensus * (i + 1), scope="forecast")
        f["fiscal_period"] = "FY%d" % (i + 1)
        figs.append(f)
        s = fig("BEST_SALES", fy, consensus * 10 * (i + 1), scope="forecast")
        s["fiscal_period"] = "FY%d" % (i + 1)
        figs.append(s)
    figs.append({"scope": "header", "mnemonic": "ERN_ANN_DT_AND_PER", "value": [
        {"announcement_date": "2026-07-28", "period": "2026:Q2"},
        {"announcement_date": "2026-01-27", "period": "2025:A"},
        {"announcement_date": "2025-01-28", "period": "2024:A"}]})
    return {"security_key": "FIX_US_Equity", "figures": figs}


def near(a, b, tol=1e-6):
    return isinstance(a, (int, float)) and abs(a - b) <= tol * max(1.0, abs(b))


def load():
    try:
        return importlib.import_module("lib.research.scores.house_fcf"), None
    except Exception as err:  # noqa: BLE001 -- the base has no module
        return None, "%s: %s" % (type(err).__name__, err)


def ac1():
    mod, err = load()
    clause("C0 lib.research.scores.house_fcf imports", mod is not None, err or "")
    if mod is None:
        return
    out = mod.forecast(block())
    fy1 = (out or {}).get("fy1") or {}
    want_rev = REV[-1] * 1.10
    clause("C1 FY1 revenue = last reported x (1 + median of the last five annual changes)",
           near(fy1.get("revenue"), want_rev), "got %s want %.6f" % (fy1.get("revenue"), want_rev))
    clause("C2 FY1 FCF = FY1 revenue x the trailing median FCF margin",
           near(fy1.get("fcf"), want_rev * 0.10), "got %s want %.6f" % (fy1.get("fcf"), want_rev * 0.10))
    fy3 = (out or {}).get("fy3") or {}
    clause("C3 FY3 compounds the same growth", near(fy3.get("revenue"), REV[-1] * 1.10 ** 3),
           "got %s" % fy3.get("revenue"))
    moved = mod.forecast(block(consensus=987654.0))
    same = all(near(((moved or {}).get(k) or {}).get("fcf"), ((out or {}).get(k) or {}).get("fcf") or float("nan"))
               for k in ("fy1", "fy2", "fy3"))
    clause("C4 difference control: every consensus figure changed, the house forecast is EQUAL", same)
    ref = (out or {}).get("reference") or {}
    clause("C5 the reference is labelled bloomberg_reported_period with the reported year and its announcement date",
           ref.get("source") == "bloomberg_reported_period" and str(ref.get("fiscal_year")) == "2025"
           and ref.get("announcement_date") == "2026-01-27", str(ref)[:160])
    short = mod.forecast(block(n_years=2))
    clause("C6 a name short of history is ABSENT with its reason",
           (short or {}).get("state") != "MEASURED" and bool((short or {}).get("absent_reason"))
           and not ((short or {}).get("fy1") or {}).get("fcf"), str((short or {}).get("absent_reason"))[:120])


def ac2():
    mod, err = load()
    clause("C0 lib.research.scores.house_fcf imports", mod is not None, err or "")
    if mod is None:
        return
    spread = [{"security_key": "K%d" % i, "house_fcf": 100.0 + 10.0 * i, "consensus_fcf": 50.0 + 5.0 * i,
               "D": d} for i, d in enumerate([-1.2, 0.4, 1.9, -0.3, 0.8])]
    out = mod.universe_summary(spread)
    clause("C1 the gate reads sd(D) and serves when it is 0.25 or more",
           isinstance((out or {}).get("sd_D"), (int, float)) and out["sd_D"] >= 0.25 and out.get("served") is True,
           "sd_D %s served %s" % ((out or {}).get("sd_D"), (out or {}).get("served")))
    clause("C2 the correlation of house FCF to consensus FCF is reported beside the gate",
           near((out or {}).get("correlation_house_vs_consensus"), 1.0, 1e-6) and (out or {}).get("n_correlation") == 5,
           "corr %s n %s" % ((out or {}).get("correlation_house_vs_consensus"), (out or {}).get("n_correlation")))
    flat = copy.deepcopy(spread)
    for r, d in zip(flat, [0.10, 0.11, 0.10, 0.12, 0.11]):
        r["D"] = d
    out2 = mod.universe_summary(flat)
    clause("C3 a near-zero spread is NOT served and says why",
           (out2 or {}).get("served") is False and bool((out2 or {}).get("reason")), str((out2 or {}).get("reason"))[:120])
    one = mod.universe_summary(spread[:1])
    clause("C4 fewer than two measured D values is NOT served and says why",
           (one or {}).get("served") is False and bool((one or {}).get("reason")), str((one or {}).get("reason"))[:120])


def ac3():
    from lib.research.scores import divergence, peers_v, robustness

    out = divergence.score_divergence()
    clause("C1 score_divergence() with no house forecast stays ABSENT with the plain reason",
           out.get("D") is None and out.get("absent_reason") == divergence.NO_HOUSE_FORECAST_REASON)
    names = (hasattr(divergence, "LEGACY_NO_HOUSE_FORECAST_REASON") and hasattr(divergence, "NO_HOUSE_FORECAST_REASON")
             and hasattr(peers_v, "LEGACY_MEASURE_NOT_COMPUTABLE_REASON")
             and hasattr(peers_v, "MEASURE_NOT_COMPUTABLE_REASON") and hasattr(robustness, "N_MIN_ELIGIBLE"))
    clause("C2 the five names scoped_amgt._plain_score_record reads still exist", names)
    clause("C3 the degeneracy floor is still 0.25", divergence.DEGENERACY_FLOOR == 0.25)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    {"AC1": ac1, "AC2": ac2, "AC3": ac3}[a.crit]()
    ok = bool(OK) and all(OK)
    print("R77 BA14 %s SERVED: %s" % (a.crit, "YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
