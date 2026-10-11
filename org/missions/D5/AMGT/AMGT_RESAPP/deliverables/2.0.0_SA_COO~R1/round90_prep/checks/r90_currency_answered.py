"""AMGT_RESAPP round-90 PREP -- D1-S14, US rows: a peer member the DEMQUE answer covers serves the MEASURED currency.

  python r90_currency_answered.py            (repo root, PYTHONPATH=<repo root>)

Round 89 closed D1-S14 on the plain reasons: the scanner row carries no currency and only a held name's model block states
CRNCY. Request `AMGT_RESAPP-S14-CRNCY-SCANNER-US` (MDPF_DEMQUE) returns CRNCY for the 1,038 United States scanner rows. This cell
is the PURE consumption half, `price_currency.price_currency_fields(member, currencies, unreadable=(), answered=None)`:
`answered` maps a bare scanner ticker to the currency code the answer returned, and nothing here reads a store.

    C1 a United States alphabetic-ticker member the answer covers, with no record key, serves price_currency = the answered code,
       price_currency_claim "measured" and a price_currency_source naming the request.
    C2 a United States member the answer does not cover keeps its plain reason and carries NO currency key (never a default).
    C3 a NON-United-States member whose ticker equals an answered ticker is NOT served (the country gate: a bare ticker is not an
       identity across exchanges).
    C4 an answered value that is not a three-letter upper-case code (a blank, "US", "dollars") is never served; the reason stays.
    C5 control: with answered=None, and for a member that already carries price_currency or names a record key whose figure is
       stated, the output is byte-equal to the round-89 behaviour (the table below is that behaviour, hard-coded).
Verdict: R90 CURRENCY ANSWERED: YES|NO (exit 0|1). At the base (2026-10-11) C1-C4 FAIL (no `answered` parameter), C5 PASSes.
"""
import json
import sys

from lib.research.peers import price_currency as pc

SOURCE_WORD = "AMGT_RESAPP-S14-CRNCY-SCANNER-US"
ANSWERED = {"INTC": "USD", "CSCO": "USD", "BADCODE": "US", "BLANK": "", "ASML": "EUR"}


def member(ticker, country="United States", price=10.0, key=None, stored=None):
    m = {"ticker": ticker, "name": ticker + " Inc", "country": country, "price": price}
    if key:
        m["identity"] = {"security_key": key, "resolution": "MEASURED"}
    if stored:
        m["price_currency"] = stored
    return m


def call(m, currencies=None, unreadable=(), answered="__none__"):
    if answered == "__none__":
        return pc.price_currency_fields(m, currencies or {}, unreadable)
    return pc.price_currency_fields(m, currencies or {}, unreadable, answered=answered)


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def attempt(fn):
    try:
        return fn(), None
    except Exception as exc:  # noqa: BLE001 -- the base raises TypeError on the new parameter; that is the FAIL
        return None, "%s: %s" % (type(exc).__name__, exc)


def main():
    results = []

    out, err = attempt(lambda: call(member("INTC"), answered=ANSWERED))
    ok = (err is None and out.get("price_currency") == "USD" and out.get("price_currency_claim") == "measured"
          and SOURCE_WORD in str(out.get("price_currency_source", "")) and "price_currency_reason" not in out)
    results.append(say(ok, "C1 a covered United States member serves the answered code as MEASURED with its source", err or json.dumps(out)))

    out, err = attempt(lambda: call(member("ZZZZ"), answered=ANSWERED))
    ok = err is None and "price_currency" not in out and out.get("price_currency_reason") == pc.REASON_NO_RECORD
    results.append(say(ok, "C2 an uncovered United States member keeps its plain reason and carries no currency key", err or json.dumps(out)))

    out, err = attempt(lambda: call(member("ASML", country="Netherlands"), answered=ANSWERED))
    ok = err is None and "price_currency" not in out and "price_currency_reason" in out
    results.append(say(ok, "C3 a non-United-States member sharing an answered ticker is not served", err or json.dumps(out)))

    bad = []
    for ticker in ("BADCODE", "BLANK"):
        out, err = attempt(lambda t=ticker: call(member(t), answered=ANSWERED))
        bad.append(err is None and "price_currency" not in out and "price_currency_reason" in out)
    results.append(say(all(bad), "C4 an answered value that is not a three-letter upper-case code is never served", "arms %s" % bad))

    # C5 -- the round-89 behaviour, hard-coded, with and without the new parameter being passed as None.
    base_cases = [
        (member("AAA", stored="CAD"), {}, (), {"price_currency": "CAD"}),
        (member("BBB", price=None), {}, (), {"price_currency_reason": pc.REASON_NO_PRICE}),
        (member("CCC"), {}, (), {"price_currency_reason": pc.REASON_NO_RECORD}),
        (member("DDD", key="DDD_US_Equity"), {"DDD_US_Equity": "USD"}, (), {"price_currency": "USD"}),
        (member("EEE", key="EEE_US_Equity"), {}, (), {"price_currency_reason": pc.REASON_NO_FIGURE}),
        (member("FFF", key="FFF_US_Equity"), {}, ("FFF_US_Equity",), {"price_currency_reason": pc.REASON_UNREADABLE}),
    ]
    ctl = []
    for m, cur, unr, want in base_cases:
        o1, e1 = attempt(lambda: call(m, cur, unr))
        o2, e2 = attempt(lambda: call(m, cur, unr, answered=None))
        ctl.append(e1 is None and o1 == want and (e2 is None and o2 == want or e2 is not None and "answered" in e2))
    # the None-parameter arm only has to hold once the parameter exists; at the base it is the TypeError the build arms report
    results.append(say(all(ctl), "C5 control: every round-89 case is byte-equal (answered absent or None)", "arms %s" % ctl))

    verdict = all(results)
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    print("R90 CURRENCY ANSWERED: %s" % ("YES" if verdict else "NO"))
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
