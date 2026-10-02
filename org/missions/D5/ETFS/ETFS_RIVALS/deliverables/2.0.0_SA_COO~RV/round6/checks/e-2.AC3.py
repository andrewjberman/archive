"""RIV-e-2 AC3 (W3-S11): G5 converts a dividend by its G3 currency where present, with the exchange-suffix table as the
LABELLED fallback.
Interface: `gold_trade_schedule.dividend_ccy(security_key, g3_currency) -> (ccy, source)`, with source "g3" or
"suffix_table".
- A G3 currency wins over the suffix: a LN listing with G3 "USD" reads ("USD", "g3").
- With no G3 currency, the suffix table answers, labelled: JP -> ("JPY", "suffix_table").
- Control: an LN listing with no G3 currency keeps today's mixed-unit rule (the base currency, labelled "suffix_table")."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import gold_trade_schedule as g

    a = g.dividend_ccy("VOD_LN_Equity", "USD")
    b = g.dividend_ccy("7203_JP_Equity", None)
    ln = g.dividend_ccy("VOD_LN_Equity", None)
    print("LN+g3:", a, "| JP no g3:", b, "| LN no g3:", ln, "| BASE_CCY:", getattr(g, "BASE_CCY", None))
    v.check(a == ("USD", "g3"), "a G3 currency wins and is labelled g3")
    v.check(b == ("JPY", "suffix_table"), "with no G3 currency the suffix table answers, labelled suffix_table")
    v.check(ln == (getattr(g, "BASE_CCY", None), "suffix_table"), "control: LN without G3 keeps the mixed-unit base rule, labelled")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
