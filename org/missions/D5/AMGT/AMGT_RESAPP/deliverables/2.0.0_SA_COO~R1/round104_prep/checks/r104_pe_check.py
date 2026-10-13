"""AMGT_RESAPP round-104 PREP -- `AMGT-bk-4`: the served historical P/E is PX_LAST / IS_EPS of the same fiscal year (CTO ruling msg 5244 (iii)), and nothing else moves.

  PYTHONPATH=<repo root> python r104_pe_check.py [--workers 4] [--sample SAN_FP_Equity,KPN_NA_Equity,TSM_US_Equity,HSBA_LN_Equity,MA_US_Equity]

For every resolved name the CHECKOUT's own /thesis handler (live pool, GET only) is read, and the LIVE function's /thesis for the same name; then:
    P1 every PE_RATIO row served by the checkout (the figures list of `model` and the top-level `fiscal_year_figures`) equals round(PX_LAST / IS_EPS, 4) of the SAME list's same-year rows;
    P2 a fiscal year whose inputs are absent or whose EPS or price is not positive serves NO PE_RATIO row and carries a `fiscal_unresolved` entry naming the reason (no silent drop):
       the count of years served plus withheld equals the count the live function served as PE_RATIO rows, per name;
    P3 EVERY other figure row, `fiscal_unresolved` entry outside PE_RATIO, `model_cases` and `forecast_figures` is equal to the live function's (nothing else moved);
    P6 a fiscal year whose price and reported EPS are stated in DIFFERENT currencies (GBp over GBP included) serves no P/E row and is withheld with a reason (naming both codes unless an earlier reason applies: EPS or price not positive, an input absent);
    P4 the basis of a derived row starts `price / reported EPS (IS_EPS), FY<year>` (a minor unit of the same currency, GBp over GBP, adds `, the price side brought from GBp to GBP (divided by 100)`) and names `derived_from` PX_LAST and IS_EPS;
    P5 control: the same comparison fed a copy of one derived row with its value moved by 0.01 reads a P1 failure (the arm can see the fault it guards).
Prints the cell count (names x years served / withheld) and, for the sample names, the before (live, Bloomberg's PE_RATIO) and after (derived) value per year.
Verdict: `R104 PE CHECK: YES|NO (<n> of <m> arms; names N, rows R served, W withheld)`; exit 0|1. At the base blob P1, P4 read NO (the base serves Bloomberg's values).
"""
import concurrent.futures
import contextlib
import copy
import io
import json
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.api import scoped_amgt as m  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

SAMPLE = ["SAN_FP_Equity", "KPN_NA_Equity", "TSM_US_Equity", "HSBA_LN_Equity", "MA_US_Equity"]
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(key):
    return {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(key):
    r = json.loads(_LAM.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event(key)).encode())["Payload"].read())
    return json.loads(r.get("body") or "{}")


def local(key):
    with contextlib.redirect_stdout(io.StringIO()):
        r = m.handler(event(key))
    return json.loads(r.get("body") or "{}")


def lists(body):
    return {"model": (body.get("model") or {}).get("fiscal_year_figures") or [], "top": body.get("fiscal_year_figures") or []}


def p1_errors(figs):
    inputs = {}
    for f in figs:
        if f.get("mnemonic") in ("PX_LAST", "IS_EPS"):
            inputs.setdefault(f.get("fiscal_year"), {})[f["mnemonic"]] = (f.get("value"), f.get("currency"))
    bad = []
    for f in figs:
        if f.get("mnemonic") == "PE_RATIO":
            i = inputs.get(f.get("fiscal_year"), {})
            try:
                (px, pc), (eps, ec) = i["PX_LAST"], i["IS_EPS"]
                if pc and ec and pc != ec and m.case_rule.is_minor_unit_quote(pc, ec):
                    px, eps = (px / m.case_rule.MINOR_UNIT_FACTOR, eps) if pc[2:].islower() else (px, eps / m.case_rule.MINOR_UNIT_FACTOR)
                    same = True
                else:
                    same = bool(pc and pc == ec)
                want = round(px / eps, 4) if same else None
            except (KeyError, TypeError, ZeroDivisionError):
                want = None
            if want is None or f.get("value") != want:
                bad.append((f.get("fiscal_year"), f.get("value"), want))
    return bad


def other(figs):
    return [f for f in figs if f.get("mnemonic") != "PE_RATIO"]


def one(key):
    a, b = live(key), local(key)
    la, lb = lists(a), lists(b)
    res = {"key": key, "p1": [], "p2": True, "p3": True, "p4": True, "p6": True, "served": 0, "withheld": 0, "before_after": {}}
    for part in ("model", "top"):
        res["p1"] += p1_errors(lb[part])
    old_years = {f.get("fiscal_year"): f.get("value") for f in la["model"] if f.get("mnemonic") == "PE_RATIO"}
    new_years = {f.get("fiscal_year"): f.get("value") for f in lb["model"] if f.get("mnemonic") == "PE_RATIO"}
    unres = {u.get("fiscal_year"): u.get("reason") for u in (b.get("model") or {}).get("fiscal_unresolved", []) if u.get("mnemonic") == "PE_RATIO"}
    base_unres = {u.get("fiscal_year") for u in (a.get("model") or {}).get("fiscal_unresolved", []) if u.get("mnemonic") == "PE_RATIO"}
    res["served"], res["withheld"] = len(new_years), len([y for y in unres if y in old_years])  # newly withheld: a year the live function SERVED and this build does not
    # P2: each live PE year is either served or withheld with a reason (a year the live function already listed as unresolved stays so)
    for y in old_years:
        if y not in new_years and not unres.get(y):
            res["p2"] = False
    if set(new_years) & set(unres):
        res["p2"] = False
    for y in unres:
        if y not in old_years and y not in base_unres:
            res["p2"] = False
    # P6: a year whose price and reported EPS are in different currencies is withheld, the reason naming both codes
    ccy = {}
    for f in la["model"]:
        if f.get("mnemonic") in ("PX_LAST", "IS_EPS"):
            ccy.setdefault(f.get("fiscal_year"), {})[f["mnemonic"]] = f.get("currency")
    for y, c in ccy.items():
        pc, ec = c.get("PX_LAST"), c.get("IS_EPS")
        if y in old_years and pc and ec and pc != ec and not m.case_rule.is_minor_unit_quote(pc, ec):
            reason = str(unres.get(y) or "")
            named = (pc in reason and ec in reason) or "not positive" in reason or "absent" in reason  # an earlier-listed reason (EPS or price not positive, an input absent) may stand first
            if y in new_years or not named:
                res["p6"] = False
    # P3: nothing else moved
    keep = lambda body: [u for u in (body.get("model") or {}).get("fiscal_unresolved", []) if u.get("mnemonic") != "PE_RATIO"]  # noqa: E731
    res["p3"] = (other(la["model"]) == other(lb["model"]) and other(la["top"]) == other(lb["top"]) and keep(a) == keep(b)
                 and a.get("model_cases") == b.get("model_cases") and (a.get("model") or {}).get("cases") == (b.get("model") or {}).get("cases")
                 and (a.get("model") or {}).get("forecast_figures") == (b.get("model") or {}).get("forecast_figures"))
    for f in lb["model"]:
        if f.get("mnemonic") == "PE_RATIO":
            bs = f.get("basis") or {}
            if not str(bs.get("definition")).startswith("price / reported EPS (IS_EPS), FY%s" % f.get("fiscal_year")) or bs.get("derived_from") != ["PX_LAST", "IS_EPS"]:
                res["p4"] = False
    res["before_after"] = {y: (old_years.get(y), new_years.get(y), unres.get(y) if y in old_years else None) for y in sorted(set(old_years) | set(new_years) | set(unres), key=str)}
    res["control_body"] = lb
    return res


def main():
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    sample = sys.argv[sys.argv.index("--sample") + 1].split(",") if "--sample" in sys.argv else SAMPLE
    real_stdout = sys.stdout  # redirect_stdout across threads can leave a buffer in place: restored after the pool
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    results, failed = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(one, k): k for k in keys}
        for fut in concurrent.futures.as_completed(futs):
            try:
                results.append(fut.result())
            except Exception as exc:  # a failed name is counted and named, never dropped
                failed.append("%s: %s %s" % (futs[fut], type(exc).__name__, str(exc)[:80]))
    sys.stdout = real_stdout
    results.sort(key=lambda r: r["key"])
    p1 = all(not r["p1"] for r in results)
    p2, p3, p4, p6 = (all(r[k] for r in results) for k in ("p2", "p3", "p4", "p6"))
    rows, wh = sum(r["served"] for r in results), sum(r["withheld"] for r in results)
    # P5 control: move one derived value by 0.01 and the same arm must read a failure
    p5 = False
    for r in results:
        figs = copy.deepcopy(r["control_body"]["model"])
        for f in figs:
            if f.get("mnemonic") == "PE_RATIO":
                f["value"] = round(f["value"] + 0.01, 4)
                p5 = bool(p1_errors(figs))
                break
        if p5 or any(f.get("mnemonic") == "PE_RATIO" for f in figs):
            break
    print("names %d (read failures %d) | PE rows served %d, withheld with a reason %d (%d names x years)" % (len(results), len(failed), rows, wh, len(results)))
    classes = {"different currencies": 0, "EPS not positive": 0, "price not positive": 0, "input absent": 0, "currency not stated": 0, "other": 0}
    for r in results:
        for _y, (_b, _a, why) in r["before_after"].items():
            if why:
                key = ("different currencies" if "different currencies" in why else "EPS not positive" if "EPS (IS_EPS) is not positive" in why else "price not positive" if "(PX_LAST) is not positive" in why
                       else "input absent" if "absent" in why else "currency not stated" if "not stated" in why else "other")
                classes[key] += 1
    print("WITHHELD BY REASON: %s" % classes)
    for f in failed[:10]:
        print("  FAILED %s" % f)
    for r in results:
        if r["key"] in sample:
            print("SAMPLE %s (year: before live / after derived / withheld reason)" % r["key"])
            for y, (b, a, why) in r["before_after"].items():
                print("   %s: %s / %s / %s" % (y, b, a, (why or "")[:80]))
    arms = [("P1 each served P/E is price / reported EPS of its year", p1), ("P2 each live P/E year is served or withheld with a reason", p2), ("P3 no other figure, reason, case or forecast moved", p3),
            ("P4 the basis states the derivation", p4), ("P5 the arm sees a value moved by 0.01", p5), ("P6 different-currency years are withheld, both codes named", p6)]
    for name, ok in arms:
        print("   %s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in arms if ok)
    print("R104 PE CHECK: %s (%d of %d arms; names %d, rows %d served, %d withheld)" % ("YES" if n == len(arms) and not failed else "NO", n, len(arms), len(results), rows, wh))
    return 0 if n == len(arms) and not failed else 1


if __name__ == "__main__":
    sys.exit(main())
