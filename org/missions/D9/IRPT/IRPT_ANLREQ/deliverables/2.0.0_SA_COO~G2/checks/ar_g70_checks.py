"""IRPT_ANLREQ AR-g-70 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g70_checks.py repair    the four observed gaps of price_source.py and swap_replacement.py are closed (ten cases)
    python ar_g70_checks.py regress   the round-7 checks (ar_g51 g51 and hygiene, ar_g52 g52 and hygiene) still print OK

Prints one RESULT line: AR-G70-OK / AR-G70-FAIL or AR-G70-REGRESS-OK / AR-G70-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import importlib.util
import json
import os
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
HERE = os.path.dirname(os.path.abspath(__file__))
EQ = {"asset_class": "Equity", "sub_asset_class": "US Large Cap"}
BOND = {"asset_class": "Fixed Income", "sub_asset_class": "Short Term"}


def load(name):
    spec = importlib.util.spec_from_file_location(name, R + name + ".py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def refusal(fn, **kw):
    try:
        fn(**kw)
    except ValueError as exc:
        return str(exc)
    except Exception as exc:
        return "WRONG-TYPE:" + type(exc).__name__
    return "NO-REFUSAL"


def tier(data):
    def fn(symbol, start, end):
        return data.get(symbol, [])
    return fn


def price_cases(ps):
    out = {}
    base = {"symbols": ["SPY"], "start": "2026-10-01", "end": "2026-10-14", "readers": {"estate": tier({})}, "as_of": "2026-10-14"}

    def call(**kw):
        return ps.resolve_prices(**{**base, **kw})
    out["bare str symbols refused"] = refusal(call, symbols="SPY") == "PRICE_SYMBOLS"
    out["non-iterable symbols refused"] = refusal(call, symbols=None) == "PRICE_SYMBOLS" and refusal(call, symbols=5) == "PRICE_SYMBOLS"
    out["impossible calendar dates refused"] = (refusal(call, start="2026-13-45") == "PRICE_WINDOW"
                                                 and refusal(call, end="2026-02-30") == "PRICE_WINDOW"
                                                 and refusal(call, as_of="2026-00-10") == "PRICE_WINDOW")
    out["start after end refused"] = refusal(call, start="2026-10-15", end="2026-10-14") == "PRICE_WINDOW"
    r = call(readers={"estate": tier({"SPY": [("2026-02-30", 5.0), ("2026-10-13", 6.0)]})})
    out["impossible row date dropped"] = r["series"]["SPY"]["rows"] == [["2026-10-13", 6.0]]
    r = call(symbols=("spy", "QQQ"), readers={"estate": tier({"SPY": [("2026-10-13", 6.0)]})})
    out["a tuple of symbols is still accepted"] = list(r["series"]) == ["SPY", "QQQ"]
    return out


def swap_cases(sr):
    out = {}
    pool = [{"ticker": "AAA", **EQ}, {"ticker": "BBB", **EQ}, {"ticker": "DDD", **BOND}]

    def pick(**kw):
        args = {"missing": "MISS", "classification": EQ, "pool_rows": pool, "model_proposals": [],
                "history_days": lambda t: {"AAA": 100, "BBB": 200, "CCC": 900}.get(t)}
        args.update(kw)
        return sr.choose_replacement(**args)

    def boom(ticker):
        raise RuntimeError("secret-xyz-token")
    r = pick(model_proposals=["CCC"], classify=boom)
    reasons = {d["ticker"]: d["reason"] for d in r["dropped"]}
    out["classify error dropped, not raised, not leaked"] = (r["replacement"] == "BBB" and reasons.get("CCC") == "NOT_CLASSIFIED"
                                                             and "secret-xyz-token" not in json.dumps(r))
    two_classes = pool + [{"ticker": "BBB", **BOND}]
    r = pick(pool_rows=two_classes)
    reasons = {d["ticker"]: d["reason"] for d in r["dropped"]}
    out["ticker with two classes is ambiguous"] = (r["replacement"] == "AAA" and reasons.get("BBB") == "CLASS_AMBIGUOUS"
                                                    and all(c["ticker"] != "BBB" for c in r["candidates"]))
    r = pick(pool_rows=two_classes, model_proposals=["BBB"])
    out["an ambiguous proposal is dropped too"] = r["replacement"] == "AAA" and all(c["ticker"] != "BBB" for c in r["candidates"])
    dup = pool + [{"ticker": "bbb ", **EQ}]
    r = pick(pool_rows=dup)
    out["same ticker twice, same class, one candidate"] = r["replacement"] == "BBB" and [c["ticker"] for c in r["candidates"]].count("BBB") == 1
    return out


def run(cmd):
    out = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if ln.strip()]
    return out.returncode, (lines[-1] if lines else "(no output)")


def main(mode):
    if mode == "repair":
        try:
            ps, sr = load("price_source"), load("swap_replacement")
            got = {**price_cases(ps), **swap_cases(sr)}
        except Exception as exc:
            print("AR-G70-FAIL %s: %s" % (type(exc).__name__, str(exc)[:200]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        print("cases %d, wrong %s" % (len(got), wrong or "none"))
        if wrong:
            print("AR-G70-FAIL wrong=%s" % wrong)
            return 1
        print("AR-G70-OK cases=%d" % len(got))
        return 0
    if mode == "regress":
        checks = [("ar_g51_checks.py", "g51", "AR-G51-OK"), ("ar_g51_checks.py", "hygiene", "AR-G51-HYGIENE-OK"),
                  ("ar_g52_checks.py", "g52", "AR-G52-OK"), ("ar_g52_checks.py", "hygiene", "AR-G52-HYGIENE-OK")]
        bad = []
        for script, arg, want in checks:
            rc, line = run([os.path.join(HERE, script), arg])
            print("%s %s: %s" % (script, arg, line[:120]))
            if rc != 0 or not line.startswith(want):
                bad.append("%s %s" % (script, arg))
        if bad:
            print("AR-G70-REGRESS-FAIL %s" % bad)
            return 1
        print("AR-G70-REGRESS-OK checks=%d" % len(checks))
        return 0
    print("usage: ar_g70_checks.py repair|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
