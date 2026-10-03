"""RIV-r-6 AC2 (repair; grounding_check/5): a digit run INSIDE a market reading's own name, quoted in the text, is part of the
reading's name, not a figure. A trending-topic headline such as "Amazon Secures 20 Years of Nuclear Power" passes.
- The run-time grade (`run_chain`, which holds the readings) and the publish recheck agree. The recheck reads the names from
  the row's `input_vintages` keys (`<source>/<name>`).
- Control: the same digits written OUTSIDE the quoted name ("it rose 20 points") still FAIL."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

HEAD = "Amazon Secures 20 Years of Nuclear Power"


def acct(text):
    return {"kind": "activity_30d", "text": text, "observed": "[]", "inferred": "[]", "cited_rows": "[]",
            "input_vintages": json.dumps({f"trending_topics/{HEAD}": "2026-10-01"}), "grounding": "PASS"}


def run(v):
    c.setup_path()
    from rivalfunds import ai_accounts as ai
    from rivalfunds import guardrails

    ok = guardrails.analysis_grounding([acct(f'The trending topic "{HEAD}" coloured the week.')])
    print("recheck, quoted headline:", ok)
    v.check(ok["status"] == guardrails.PASS, "the publish recheck passes a quoted headline's digits")
    bad = guardrails.analysis_grounding([acct("Sentiment rose 20 points over the week.")])
    print("recheck, bare 20:", bad)
    v.check(bad["status"] == guardrails.FAIL, "control: a bare uncited 20 outside the name still fails")

    g5, g6, hc, bt = c.ai2_tables()
    facts = ai.fact_pack("TXUE", c.AI_DAY, g5, g6, hc, bt)
    readings = [{"source": "trending_topics", "name": HEAD, "value": 0.6, "as_of": "2026-10-01", "status": "fresh",
                 "age_trading_days": 1, "location": "s3://fixture", "series": [["2026-10-01", 0.6]], "reason": None}]
    reply = c.ai2_reply(f'The trending topic "{HEAD}" coloured the week.', [])
    cl = c.StubClient([reply, reply])
    rows = ai.run_chain("TXUE", "rival", c.AI_DAY, facts, readings, cl, "runR6")
    print("run-time grades:", [(r["kind"], r["grounding"], r["grounding_reason"]) for r in rows])
    v.check(len(rows) == 2 and all(r["grounding"] == "PASS" for r in rows), "the run-time grade agrees: PASS")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
