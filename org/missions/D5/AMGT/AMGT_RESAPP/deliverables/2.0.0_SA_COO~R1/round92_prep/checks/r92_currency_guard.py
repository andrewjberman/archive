"""AMGT_RESAPP round-92 PREP -- C-S55: a minor-unit currency is never served beside a major-unit price, and a served currency carries
no stale reason.

  PYTHONPATH=<repo root> python r92_currency_guard.py

Measured 2026-10-11 against the live function (checks/../round92_prep census): 12 member rows on 5 UK securities (AZN, BP, IMB, RIO, SSE)
serve `GBp` beside the scanner's POUND price (AZN 120.32 against the record's PX_LAST 11998.0 GBp), a 100x mislabel; 156 live rows serve a
currency beside the producer's stored `price_currency_reason` text. Every OTHER served currency (USD 125, CHF 9, EUR 8, JPY 6, HKD 1) equals
its record's own CRNCY. The scanner quotes in the MAJOR unit; a record whose CRNCY is a minor-unit code (Bloomberg: a lower-case last letter,
GBp, ZAc; or GBX, ILA) states the quote unit of ITS OWN price, not of the scanner's.

    G1 a record whose CRNCY is GBp, ZAc, GBX or ILA serves NO currency and a plain reason (no conversion, no label).
    G2 control: a record whose CRNCY is EUR, CHF, SGD, USD, JPY or HKD still serves that code, unchanged.
    G3 the route-level decorator `_with_price_currency`: a member with a key to a GBp record carries `price_currency_reason` and no
       `price_currency`; a member with a key to a EUR record carries `price_currency` EUR and NO `price_currency_reason`, even when the
       stored member carried one; a member with no key keeps its plain reason; member count and order are unchanged.
    G4 nothing else moves: `price`, `cap_currency`, `identity` and every other member field are byte-equal.
Verdict: R92 CURRENCY GUARD: YES|NO (exit 0|1). At the base (2026-10-11) G1 and G3 FAIL, G2 and G4 PASS.
"""
import copy
import sys

from lib.research.api import scoped_amgt
from lib.research.peers import price_currency as pc

PRICE = 44.94


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def member(ticker, key=None, **extra):
    m = {"ticker": ticker, "name": ticker + " plc", "country": "United Kingdom", "price": PRICE}
    if key:
        m["identity"] = {"security_key": key, "resolution": "MEASURED"}
        m["security_key"] = key
    m.update(extra)
    return m


def main():
    results = []

    minor = {}
    for code in ("GBp", "ZAc", "GBX", "ILA"):
        out = pc.price_currency_fields(member("X", "X_LN_Equity"), {"X_LN_Equity": code})
        minor[code] = ("price_currency" not in out) and bool(out.get("price_currency_reason"))
    results.append(say(all(minor.values()), "G1 a minor-unit CRNCY serves no currency and a plain reason", str(minor)))

    major = {}
    for code in ("EUR", "CHF", "SGD", "USD", "JPY", "HKD"):
        out = pc.price_currency_fields(member("Y", "Y_FP_Equity"), {"Y_FP_Equity": code})
        major[code] = out.get("price_currency") == code and "price_currency_reason" not in out
    results.append(say(all(major.values()), "G2 control: a major-unit CRNCY is served unchanged", str(major)))

    # G3 / G4 -- the route-level decorator, with the record read and the listing rule stubbed.
    records = {"GSK_LN_Equity": ("OK", "GBp"), "SAN_FP_Equity": ("OK", "EUR")}
    orig_rec, orig_res = scoped_amgt._record_trading_currency, scoped_amgt._resolve_held_form
    scoped_amgt._record_trading_currency = lambda key: records.get(key, ("ABSENT", None))
    scoped_amgt._resolve_held_form = lambda form: None
    stale = "The scanner price for this peer carries no currency, and this peer is not matched to a company record that states its trading currency."
    served = {"members": [
        member("BN7SWP", "GSK_LN_Equity", price_currency_reason=stale),
        member("B0000", "SAN_FP_Equity", price_currency_reason=stale, country="France"),
        member("ZZZ", None, price_currency_reason=stale),
    ]}
    before = copy.deepcopy(served)
    try:
        out = scoped_amgt._with_price_currency(copy.deepcopy(served))
    except Exception as exc:  # noqa: BLE001 -- recorded as the FAIL
        out = None
        err = "%s: %s" % (type(exc).__name__, exc)
    finally:
        scoped_amgt._record_trading_currency, scoped_amgt._resolve_held_form = orig_rec, orig_res
    if out is None:
        results.append(say(False, "G3 route level", err))
        results.append(say(False, "G4 nothing else moves", err))
    else:
        ms = out["members"]
        g3 = (len(ms) == 3 and [m["ticker"] for m in ms] == ["BN7SWP", "B0000", "ZZZ"]
              and "price_currency" not in ms[0] and bool(ms[0].get("price_currency_reason"))
              and ms[1].get("price_currency") == "EUR" and "price_currency_reason" not in ms[1]
              and ms[2].get("price_currency_reason") and "price_currency" not in ms[2])
        results.append(say(bool(g3), "G3 route level: GBp -> reason, EUR -> code with no stale reason, no key -> plain reason",
                           "GBp: %s | EUR: %s | none: %s" % (
                               {k: ms[0].get(k) for k in ("price_currency",) if k in ms[0]} or "reason",
                               ms[1].get("price_currency"), "reason" if ms[2].get("price_currency_reason") else "?")))
        moved = []
        for a, b in zip(before["members"], ms):
            for k in set(a) | set(b):
                if k in ("price_currency", "price_currency_reason"):
                    continue
                if a.get(k) != b.get(k):
                    moved.append((a.get("ticker"), k))
        results.append(say(not moved, "G4 nothing else moves: price, cap_currency, identity and every other field byte-equal", str(moved)))

    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R92 CURRENCY GUARD: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
