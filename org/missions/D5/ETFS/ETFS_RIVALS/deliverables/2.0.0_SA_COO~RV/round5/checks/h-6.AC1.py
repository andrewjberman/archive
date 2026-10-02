"""RIV-h-6 AC1 (hop-9 ruling d) -- key resolution is its own G5 column, out of the confidence precedence.

Pure, offline (the test_g2 fixture book, a x1.037 flow with one moved line):
  - an UNRESOLVED book: the trade's `confidence` is FLOW-WINDOW (the inference grade), and `key_resolution` is UNRESOLVED;
  - a RESOLVED book: `key_resolution` is RESOLVED;
  - an alias-resolved book (resolution_method `issuer-alias`): `key_resolution` is ALIAS;
  - control: the existing `key_resolved` column is still written (the change is additive)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import gold_trade_schedule as g
    from rivalfunds.tests.test_g2_trade_schedule import BOOK, _cs, _scale

    moved = dict(_scale(BOOK, 1.037))
    q, p = moved["S3"]
    moved["S3"] = (q * 1.25, p)

    def trade(resolved=True, method=None):
        df = _cs(("2026-09-28", BOOK), ("2026-09-29", moved), resolved=resolved)
        if method:
            df.loc[df["resolution_status"] == "RESOLVED", "resolution_method"] = method
        t = g.infer_trades(df)
        return t.iloc[0].to_dict() if len(t) == 1 else {"_rows": len(t)}

    u = trade(resolved=False)
    print("unresolved:", u.get("confidence"), u.get("key_resolution", "<no column>"))
    v.check(u.get("confidence") == "FLOW-WINDOW" and u.get("key_resolution") == "UNRESOLVED",
            "an unresolved key: confidence FLOW-WINDOW, key_resolution UNRESOLVED")
    r = trade(resolved=True)
    a = trade(resolved=True, method="issuer-alias")
    print("resolved:", r.get("key_resolution", "<no column>"), "| alias:", a.get("key_resolution", "<no column>"))
    v.check(r.get("key_resolution") == "RESOLVED" and a.get("key_resolution") == "ALIAS",
            "a resolved key reads RESOLVED, an issuer-alias key reads ALIAS")
    v.check("key_resolved" in u and "key_resolved" in r, "control: key_resolved is still written")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
