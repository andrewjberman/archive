"""RIV-ai-2 AC1 (FWD-16, FWD-17; amendment A1) -- the two prompts run as ONE chained history over cited facts, write versioned G12
rows, never for a benchmark, and never rewrite an earlier run.

Pure, offline (stub client, local sink; the `_common` A1 fixtures, day 2026-10-02):
  - fact_pack('TXUE', ...) cites a row for every fact ({table, key, revision, value}); no fact cites the 2026-08-03 window
    (outside the rolling 30 days);
  - run_chain makes exactly two chat calls; the second call's messages START with the first call's messages, then carry the
    first reply as an assistant message (one shared, cacheable prefix);
  - two rows come back, kinds activity_30d then direction_verdict, sharing the run_id, each with model_version, prompt_version
    and input_vintages naming the readings' as_of;
  - a benchmark (role index_control) returns no rows and makes no call;
  - append-only: write_rows for run A then run B leaves run A's object byte-identical, and writing run A again is refused."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import ai_accounts as ai
    from rivalfunds import sinks

    g5, g6, hc, bt = c.ai2_tables()
    facts = ai.fact_pack("TXUE", c.AI_DAY, g5, g6, hc, bt)
    print(f"{len(facts)} facts:", [(f.get("id"), (f.get("cited_row") or {}).get("table")) for f in facts][:8])
    cites = [f.get("cited_row") or {} for f in facts]
    v.check(facts and all({"table", "key", "revision", "value"} <= set(r) for r in cites)
            and not any("2026-08-03" in json.dumps(r, default=str) for r in cites),
            "every fact cites {table, key, revision, value}; none cites the window outside the 30 days")
    fid = facts[0]["id"]
    val = facts[0]["cited_row"]["value"]
    txt = f"The fund's largest recent figure was {val}."
    cl = c.StubClient([c.ai2_reply(txt, [fid]), c.ai2_reply(txt, [fid])])
    rows = ai.run_chain("TXUE", "rival", c.AI_DAY, facts, c.ai2_readings(), cl, "runA")
    print("calls:", len(cl.calls), "| rows:", [r.get("kind") for r in rows])
    first, second = (cl.calls + [None, None])[:2]
    chained = (first is not None and second is not None and second[:len(first)] == first
               and any(txt in str(m.get("content")) for m in second[len(first):] if m.get("role") == "assistant"))
    v.check(len(cl.calls) == 2 and chained, "two chat calls; the second carries the first's messages, then its reply")
    v.check([r.get("kind") for r in rows] == ["activity_30d", "direction_verdict"]
            and len({r.get("run_id") for r in rows}) == 1
            and all(r.get("model_version") and r.get("prompt_version") and "2026-10-01" in json.dumps(r.get("input_vintages"), default=str)
                    for r in rows),
            "rows activity_30d then direction_verdict, one run_id, model and prompt versions, input vintages")
    cb = c.StubClient([])
    v.check(ai.run_chain("SCHY", "index_control", c.AI_DAY, facts, c.ai2_readings(), cb, "runX") == [] and cb.calls == [],
            "a benchmark gets no account and no call")
    spec = f"local:{c.tmpdir('rv_ai2_')}"
    s = sinks.get_sink(spec)
    ua = ai.write_rows(s, c.AI_DAY, rows)
    before = s.get(ua)
    rows_b = [dict(r, run_id="runB") for r in rows]
    ub = ai.write_rows(s, c.AI_DAY, rows_b)
    try:
        ai.write_rows(s, c.AI_DAY, rows)
        again = "written"
    except Exception as e:  # noqa: BLE001 -- the refusal is the expected outcome
        again = f"refused: {type(e).__name__}"
    print("objects:", ua, ub, "| rewrite of run A:", again)
    v.check(ua != ub and s.get(ua) == before and again.startswith("refused"),
            "append-only: run B is a new object, run A's bytes are unchanged, rewriting run A is refused")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
