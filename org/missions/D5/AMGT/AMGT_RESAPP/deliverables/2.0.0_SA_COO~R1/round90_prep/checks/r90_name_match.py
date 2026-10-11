"""AMGT_RESAPP round-90 PREP -- D1-S14, non-US rows: a peer member the numeric-ticker rule does not own resolves through the
pool by the SAME exact-name rule, or stays byte-equal.

  python r90_name_match.py            (repo root, PYTHONPATH=<repo root>)

`_with_numeric_tickers` (AMGT-av-5) resolves an ALL-DIGIT ticker by its Japan code form or by a held company's exact name token
(a name two held companies share is not matched). Measured 2026-10-11 against the six scanner universes: it serves 29 of the 769
all-digit non-US rows (22 by name, 7 by Japan code); 23 of the other 1,047 non-US rows (SEDOL stems, star tickers, class-share
tickers) name exactly one held company and are NOT served. This cell extends the SAME rule to them:

    N1 a SEDOL-stem member whose name token names exactly one held company serves that key, identity MEASURED, matched_as
       company_name.
    N2 a star-ticker member does the same.
    N3 a member whose name names no held company stays byte-equal (no key, no reason added).
    N4 a name two held companies share is NOT matched (byte-equal).
    N5 a United States ALPHABETIC ticker is not touched (nn-2 owns it), even when its name matches.
    N6 control: an all-digit ticker is answered exactly as before (numeric_fields), and a member already MEASURED is untouched.
    N7 route level: through `_with_numeric_tickers`, a served peer set keeps its member count and order, the matchable
       non-numeric member gains `security_key` and `identity`, every other member is byte-equal.
Verdict: R90 NAME MATCH: YES|NO (exit 0|1). At the base (2026-10-11) N1-N5 and N7 FAIL (no such function, no such arm), N6 PASSes.
"""
import copy
import json
import sys

from lib.research.api import scoped_amgt
from lib.research.peers import numeric_tickers as nt

IDX = {
    nt.name_token("ASML Holding NV"): ["ASML_NA_Equity"],
    nt.name_token("Shopify, Inc. Class A"): ["SHOP_CN_Equity"],
    nt.name_token("Shared Name Corp"): ["SHR_US_Equity", "SHR_LN_Equity"],
    nt.name_token("Novartis AG"): ["NOVN_SW_Equity"],
}


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def attempt(fn):
    try:
        return fn(), None
    except Exception as exc:  # noqa: BLE001 -- at the base the function does not exist; that is the FAIL
        return None, "%s: %s" % (type(exc).__name__, exc)


def member(ticker, name, country="Switzerland", **extra):
    m = {"ticker": ticker, "name": name, "country": country, "price": 10.0}
    m.update(extra)
    return m


def match(m):
    return nt.name_match_fields(m, IDX, lambda n: n)


def main():
    results = []

    out, err = attempt(lambda: match(member("B929F4", "ASML Holding NV", country="Netherlands")))
    ok = (err is None and out.get("security_key") == "ASML_NA_Equity"
          and (out.get("identity") or {}).get("resolution") == "MEASURED"
          and (out.get("identity") or {}).get("matched_as") == "company_name")
    results.append(say(ok, "N1 a SEDOL-stem member naming one held company serves its key as MEASURED, matched_as company_name",
                       err or json.dumps(out)))

    out, err = attempt(lambda: match(member("*SHOP", "Shopify, Inc. Class A", country="Canada")))
    ok = err is None and out.get("security_key") == "SHOP_CN_Equity"
    results.append(say(ok, "N2 a star-ticker member naming one held company serves its key", err or json.dumps(out)))

    out, err = attempt(lambda: match(member("ZZ9999", "Nobody Holdings Ltd")))
    results.append(say(err is None and out == {}, "N3 an unmatched name adds nothing (no key, no reason)", err or json.dumps(out)))

    out, err = attempt(lambda: match(member("SHR1", "Shared Name Corp")))
    results.append(say(err is None and out == {}, "N4 a name two held companies share is not matched", err or json.dumps(out)))

    out, err = attempt(lambda: match(member("ASMLX", "ASML Holding NV", country="United States")))
    results.append(say(err is None and out == {}, "N5 a United States alphabetic ticker is left to nn-2", err or json.dumps(out)))

    # N6 -- the all-digit rule is untouched, and a MEASURED member is never re-matched.
    num = member("710306", "Novartis AG")
    got = nt.numeric_fields(num, lambda f: None, IDX, lambda n: n)
    want_ok = got.get("security_key") == "NOVN_SW_Equity" and got["identity"]["matched_as"] == "company_name"
    done = member("B929F4", "ASML Holding NV", identity={"resolution": "MEASURED", "security_key": "ASML_NA_Equity"},
                  security_key="ASML_NA_Equity")
    out, err = attempt(lambda: match(done))
    ok = want_ok and (err is None and out == {} or (err is not None and "name_match_fields" in err))
    results.append(say(ok, "N6 control: an all-digit ticker is answered as before; a MEASURED member is untouched",
                       err or "numeric_fields -> %s" % got.get("security_key")))

    # N7 -- route level.
    served = {"members": [
        member("B929F4", "ASML Holding NV", country="Netherlands"),
        member("ZZ9999", "Nobody Holdings Ltd"),
        member("INTC", "Intel Corp", country="United States"),
        member("710306", "Novartis AG"),
    ]}
    before = copy.deepcopy(served)
    orig_index, orig_resolve = scoped_amgt._held_name_index, scoped_amgt._resolve_held_form
    scoped_amgt._held_name_index = lambda: IDX
    scoped_amgt._resolve_held_form = lambda form: None
    try:
        out, err = attempt(lambda: scoped_amgt._with_numeric_tickers(copy.deepcopy(served)))
    finally:
        scoped_amgt._held_name_index, scoped_amgt._resolve_held_form = orig_index, orig_resolve
    ok = False
    detail = err or ""
    if err is None:
        ms = out["members"]
        same_shape = [m["ticker"] for m in ms] == [m["ticker"] for m in before["members"]]
        gained = ms[0].get("security_key") == "ASML_NA_Equity" and (ms[0].get("identity") or {}).get("matched_as") == "company_name"
        untouched = ms[1] == before["members"][1] and ms[2] == before["members"][2]
        numeric_ok = ms[3].get("security_key") == "NOVN_SW_Equity"
        ok = same_shape and gained and untouched and numeric_ok
        detail = "shape=%s gained=%s untouched=%s numeric=%s" % (same_shape, gained, untouched, numeric_ok)
    results.append(say(ok, "N7 route level: the matchable non-numeric member gains its key, every other member is byte-equal", detail))

    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    verdict = all(results)
    print("R90 NAME MATCH: %s" % ("YES" if verdict else "NO"))
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
