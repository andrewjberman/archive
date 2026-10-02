"""RIV-ai-2 AC2 (C-AI-GROUNDING; comp-adversary declared on this cell) -- a figure the model writes that matches no cited row
FAILS grounding and is never shown as a pass.

Pure, offline (stub client, the `_common` A1 fixtures):
  - grounding_check("... 1000 ...", [{value: 1000.0}]) passes; a percent of a fraction ("1.25%" against 0.0125) passes;
  - grounding_check with a planted figure 37.2 that no cited row holds fails, and its reason names 37.2;
  - through run_chain: a reply whose text plants 37.2 yields a row with grounding FAIL and a reason naming 37.2;
  - control: the same chain with only cited figures yields rows with grounding PASS (ISO dates are not figures)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import ai_accounts as ai

    ok1, r1 = ai.grounding_check("It added 1000 of S1.", [{"table": "trade_schedule", "key": "k", "revision": "r1", "value": 1000.0}])
    ok2, r2 = ai.grounding_check("S1 added 1.25% to return.", [{"table": "holding_contribution", "key": "k", "revision": "hc1", "value": 0.0125}])
    ok3, r3 = ai.grounding_check("It added 37.2 of S1.", [{"table": "trade_schedule", "key": "k", "revision": "r1", "value": 1000.0}])
    print("plain:", ok1, r1, "| percent:", ok2, r2, "| planted:", ok3, r3)
    v.check(ok1 is True and ok2 is True, "a cited figure passes, plain and as a percent of a fraction")
    v.check(ok3 is False and "37.2" in str(r3), "a planted figure fails and the reason names it")

    g5, g6, hc, bt = c.ai2_tables()
    facts = ai.fact_pack("TXUE", c.AI_DAY, g5, g6, hc, bt)
    fid, val = facts[0]["id"], facts[0]["cited_row"]["value"]
    bad = c.StubClient([c.ai2_reply(f"On 2026-09-15 it moved {val}, and 37.2 more.", [fid]),
                        c.ai2_reply(f"On 2026-09-15 it moved {val}.", [fid])])
    rows = ai.run_chain("TXUE", "rival", c.AI_DAY, facts, c.ai2_readings(), bad, "runG")
    print("planted chain:", [(r.get("kind"), r.get("grounding"), r.get("grounding_reason")) for r in rows])
    v.check(rows and rows[0].get("grounding") == "FAIL" and "37.2" in str(rows[0].get("grounding_reason")),
            "a chain reply planting 37.2 is written grounding FAIL with the reason")
    good = c.StubClient([c.ai2_reply(f"On 2026-09-15 it moved {val}.", [fid]), c.ai2_reply(f"On 2026-09-15 it moved {val}.", [fid])])
    rows = ai.run_chain("TXUE", "rival", c.AI_DAY, facts, c.ai2_readings(), good, "runH")
    print("cited chain:", [(r.get("kind"), r.get("grounding")) for r in rows])
    v.check(len(rows) == 2 and all(r.get("grounding") == "PASS" for r in rows), "control: only cited figures (and a date) pass")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
