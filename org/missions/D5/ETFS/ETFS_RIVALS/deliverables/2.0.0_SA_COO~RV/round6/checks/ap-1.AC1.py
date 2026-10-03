"""RIV-ap-1 AC1: the scheduled AI stage writes the day's accounts ONCE (CALL 5: one run per page day).
Interface (new module `rivalfunds/ai_stage.py`): `ai_stage.run_for_day(sink_spec, day)` calls `ai_accounts.run_day(day,
sink_spec, client=ai_client.default_client(), provenance={"run_path": "scheduled", ...})` when `RIVALFUNDS_AI_ENABLE == "1"`
and the page day holds no `research_hypotheses` object; a second call for the same day calls nothing and writes nothing. The
one-line hookup in `publish_page.handler_entry` (after `produce_a1`) is the issuer's at the merge (C10).
Control: with the gate unset, the stage calls nothing and writes no account.
Offline: the round-5 page fixture builds G5 and the A1 inputs; the client and the market readings are stubbed."""
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import ai_client, ai_stage, homes, market_context, publish_page
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    reply = c.ai2_reply("TXUE added to S1 in the window.", [])
    stub = c.StubClient([reply] * 40)
    ai_client.default_client = lambda: stub
    market_context.read_context = lambda day, *a, **k: c.ai2_readings()

    def objects(s):
        return [u for u in s.list(homes.address("rivalfunds", "etfs", "gold", "research_hypotheses", f"date={tp2.DAY}") + "/")
                if u.endswith(".parquet")]

    os.environ.pop("RIVALFUNDS_AI_ENABLE", None)
    spec0, s0, _ = c.page_fixture()
    publish_page.produce_a1(s0, spec0, tp2.DAY, False)
    ai_stage.run_for_day(spec0, tp2.DAY)
    v.check(objects(s0) == [] and stub.calls == [], "control: gate unset -> no AI call, no account written")

    os.environ["RIVALFUNDS_AI_ENABLE"] = "1"
    os.environ["RIVALFUNDS_OPENAI_SECRET"] = "fixture/openai"
    spec, s, _ = c.page_fixture()
    publish_page.produce_a1(s, spec, tp2.DAY, False)
    ai_stage.run_for_day(spec, tp2.DAY)
    n1, calls1 = len(objects(s)), len(stub.calls)
    ai_stage.run_for_day(spec, tp2.DAY)
    n2, calls2 = len(objects(s)), len(stub.calls)
    print("objects after publish 1 / 2:", n1, n2, "| client calls after 1 / 2:", calls1, calls2)
    v.check(n1 == 1 and calls1 > 0, "gate set -> the first stage call writes exactly one research_hypotheses object")
    v.check(n2 == 1 and calls2 == calls1, "a second call for the same day calls nothing and writes nothing")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
