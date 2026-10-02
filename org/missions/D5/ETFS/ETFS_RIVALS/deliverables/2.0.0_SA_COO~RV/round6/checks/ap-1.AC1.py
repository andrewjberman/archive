"""RIV-ap-1 AC1: the scheduled publish writes the day's AI accounts ONCE (CALL 5: one run per page day).
`publish_page.handler_entry`, after `produce_a1` and before `load_a1`, calls `ai_accounts.run_day(day, sink,
client=ai_accounts.default_client(), provenance={"run_path": "scheduled", ...})` when `RIVALFUNDS_AI_ENABLE == "1"` and the
page day holds no `research_hypotheses` object. A second publish of the same day calls nothing and writes nothing.
Control: with the gate unset, a publish calls nothing and writes no account.
Offline: the round-5 page fixture; the client and the market readings are stubbed (no vendor call)."""
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import ai_accounts, homes, market_context, publish_page
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    reply = c.ai2_reply("TXUE added to S1 in the window.", [])
    stub = c.StubClient([reply] * 40)
    ai_accounts.default_client = lambda: stub
    market_context.read_context = lambda day, *a, **k: c.ai2_readings()

    def objects(s):
        return [u for u in s.list(homes.address("rivalfunds", "etfs", "gold", "research_hypotheses", f"date={tp2.DAY}") + "/")
                if u.endswith(".parquet")]

    os.environ.pop("RIVALFUNDS_AI_ENABLE", None)
    spec0, s0, _ = c.page_fixture()
    publish_page.handler_entry({"date": tp2.DAY, "mode": "daily", "batch_id": "ap1-off", "sink": spec0})
    v.check(objects(s0) == [] and stub.calls == [], "control: gate unset -> no AI call, no account written")

    os.environ["RIVALFUNDS_AI_ENABLE"] = "1"
    os.environ["RIVALFUNDS_OPENAI_SECRET"] = "fixture/openai"
    spec, s, _ = c.page_fixture()
    publish_page.handler_entry({"date": tp2.DAY, "mode": "daily", "batch_id": "ap1-a", "sink": spec})
    n1, calls1 = len(objects(s)), len(stub.calls)
    publish_page.handler_entry({"date": tp2.DAY, "mode": "daily", "batch_id": "ap1-b", "sink": spec})
    n2, calls2 = len(objects(s)), len(stub.calls)
    print("objects after publish 1 / 2:", n1, n2, "| client calls after 1 / 2:", calls1, calls2)
    v.check(n1 == 1 and calls1 > 0, "gate set -> the first publish writes exactly one research_hypotheses object")
    v.check(n2 == 1 and calls2 == calls1, "a second publish of the same day calls nothing and writes nothing")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
