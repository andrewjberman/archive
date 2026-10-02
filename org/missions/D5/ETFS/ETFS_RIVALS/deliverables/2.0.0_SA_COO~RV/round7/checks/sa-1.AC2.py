"""RIV-sa-1 AC2 (C-S24 plants 2 and 3): the sweep's AI step has a stated deadline. A run that overruns it publishes
WITHOUT accounts and records FAILED, and the day gets one AI run only (CALL 5: a FAIL is shown, never re-rolled).
FAIL at the base: the sweep never reaches the AI stage when the publish marker exists, so nothing is republished or
recorded.

Interface (prescribed; the issuer copies it into the cell):
- The sweep event field `ai_deadline_s` (seconds, a number; `sweep.trigger_event` passes it through) sets the AI step's
  deadline. When it is absent, the default is the module constant `sweep.AI_DEADLINE_S` (the cell states its value).
  The step never runs past the Lambda's remaining time less `MARGIN_MS`.
- `ai_stage.run_for_day(sink_spec, day, run_path="ad_hoc", deadline_s=None, **kw)`: a run that passes its deadline
  writes NO research_hypotheses object, now or later (no background writer survives the step). It returns
  {"status": "FAILED", "reason": <a text containing "deadline">, "run_path": ...}.
- The sweep still republishes (`event["ai_run"]` = that result, AC1). The page shows the failure, for example as the AI
  card's absence note (`a1["research_hypotheses_note"]`), so a FAIL is shown (CALL 5) and the republish is a real
  page revision.
- One run per page day: once the step has run for a page day (OK or FAILED), a later sweep for that day makes no AI
  call. The cell records the attempt where the sweep reads it; the carrier is its choice, through the address builder.

Fixture (`_s24_sweep`, offline, local sink): as AC1. The transport is stubbed with its FIRST reply delayed 3.0 s, and
the schedule payload gets `"ai_deadline_s": 1.0`.
  - the sweep republishes: the served manifest is a new batch with ONE kept revision (the morning page);
  - its a1_produced.research_hypotheses_run reads status FAILED, and its reason names the deadline ("deadline");
  - the republished page names the failure ("deadline" appears in index.html; the morning page has no such word);
  - no research_hypotheses object, including after the slow reply has drained (2.0 s past it);
  - CALL 5: a second sweep for the same day (instant transport, no ai_deadline_s) makes no AI call and writes no
    research_hypotheses object."""
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _s24_sweep as p  # noqa: E402

DEADLINE_S, SLOW_S = 1.0, 3.0


def run(v):
    spec, s, tmp, r0 = p.start(morning=True)
    morning_html = p.index(s)
    p.gate(True)
    slow = p.Client(slow_s=SLOW_S)
    p.set_client(slow)
    ev = p.schedule_payload(spec, ai_deadline_s=DEADLINE_S)
    print("schedule payload:", ev)
    t0 = time.monotonic()
    r1 = p.sweep(ev)
    took = time.monotonic() - t0
    m1 = p.manifest(s)
    run1 = p.ai_run(m1)
    print("sweep 1:", r1.get("status"), "| took %.1f s" % took, "| client calls:", len(slow.calls),
          "| served manifest batch:", m1.get("batch_id"), "| revisions kept:", len(m1.get("revisions") or []))
    print("research_hypotheses_run:", run1)
    v.check(m1.get("batch_id") not in (None, p.BATCH) and len(m1.get("revisions") or []) == 1,
            "the sweep republishes past the deadline: a new batch with ONE kept revision")
    v.check(run1.get("status") == "FAILED" and "deadline" in str(run1.get("reason") or "").lower(),
            "the manifest records the AI step FAILED with the deadline reason")
    html = p.index(s)
    print("'deadline' in the morning page / the republished page:", "deadline" in morning_html.lower(),
          "deadline" in html.lower())
    v.check("deadline" not in morning_html.lower() and "deadline" in html.lower(),
            "the republished page shows the failure (it names the deadline)")
    if slow.t_first is not None:
        time.sleep(max(0.0, slow.t_first + SLOW_S + 2.0 - time.monotonic()))
    acc = p.accounts(s)
    print("accounts after the slow reply drained:", [u.rsplit("/", 1)[-1] for u in acc], "| client calls:",
          len(slow.calls))
    v.check(acc == [], "no research_hypotheses object, including after the slow reply drained (no late writer)")
    fast = p.Client()
    p.set_client(fast)
    r2 = p.sweep(p.schedule_payload(spec))
    print("sweep 2:", r2.get("status"), "| client built:", p.STATE["built"], "| client calls:", len(fast.calls),
          "| accounts:", len(p.accounts(s)))
    v.check(len(fast.calls) == 0 and p.accounts(s) == [],
            "CALL 5: a second sweep for the day makes no AI call and writes no research_hypotheses object")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
