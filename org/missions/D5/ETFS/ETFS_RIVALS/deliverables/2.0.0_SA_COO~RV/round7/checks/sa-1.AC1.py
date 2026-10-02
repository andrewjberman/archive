"""RIV-sa-1 AC1 (C-S24, round-6 ruling 1): the day's page is ALREADY published by the gateless morning publish (its
publish-page marker is present) and holds no research_hypotheses object. The 09:00 ET sweep, run with its own
EventBridge schedule payload and the AI gate set, reaches the AI stage as ITS OWN STEP, writes ONE research_hypotheses
object and republishes the page. FAIL at the base: `sweep.py:469-472` skips the publish whenever the marker exists, and
the AI stage runs only inside publish-page, so the sweep makes no AI call (no account, no second revision).

Interface (prescribed; the issuer copies it into the cell):
- `sweep.handler_entry(event, context)`: after the graph (`run_dag`), when RIVALFUNDS_AI_ENABLE == "1" and the day holds
  a publish-page marker, it runs `ai_stage.run_for_day(sink, date, run_path=..., deadline_s=...)` as its own step. When
  that step ran (status OK or FAILED), it republishes the day through `publish_page.handler_entry` under a NEW batch id,
  passing the step's result as `event["ai_run"]`.
- `publish_page.handler_entry`: given `event["ai_run"]`, the manifest's `a1_produced.research_hypotheses_run` is that
  result ({status, reason, run_id, run_path}) and the publish makes no AI call of its own. No vendor call ever runs
  before a page write.
- The gate stays on the daily Lambda only (round-6 ap-1 AC3), never on publish-page.

Fixture (`_s24_sweep`, offline, local sink): page day 2026-09-30; every upstream marker planted; the morning publish
(batch g, gate unset). The transport is stubbed (instant replies).
  - control: after the morning publish the day holds the publish-page marker and the page and no research_hypotheses
    object, and the sweep's graph runs no upstream stage (every marker present, as on 2026-10-02);
  - the sweep makes AI calls, and the day then holds exactly ONE research_hypotheses object;
  - the page is republished: the served manifest is a new batch with ONE kept revision (the morning page), it names the
    account object among its inputs, and its a1_produced.research_hypotheses_run reads status OK with the account's
    run_id;
  - one run per page day on the OK path (CALL 5): a second sweep with the same payload makes no AI call, and the day
    still holds ONE object."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _s24_sweep as p  # noqa: E402


def run(v):
    spec, s, tmp, r0 = p.start(morning=True)
    m0 = p.manifest(s)
    pre = {"marker_batches": [m.get("batch_id") for m in p.page_markers(s)], "page": p.index(s) != "",
           "manifest_batch": m0.get("batch_id"), "accounts": len(p.accounts(s))}
    print("morning publish:", (r0 or {}).get("status"), "|", pre, "| research_hypotheses_run:", p.ai_run(m0))
    p.gate(True)
    stub = p.Client()
    p.set_client(stub)
    ev = p.schedule_payload(spec)
    print("schedule payload:", ev)
    r1 = p.sweep(ev)
    d1 = r1.get("detail") or {}
    print("sweep 1:", r1.get("status"), "| ran:", d1.get("ran"), "| detail keys:", sorted(d1),
          "| upstream stages run:", p.STATE["unexpected"])
    v.check(pre == {"marker_batches": [p.BATCH], "page": True, "manifest_batch": p.BATCH, "accounts": 0}
            and p.STATE["unexpected"] == [],
            "control: the morning publish left the marker and the page and no account; the graph runs no upstream "
            "stage")
    acc = p.accounts(s)
    m1 = p.manifest(s)
    print("client calls:", len(stub.calls), "| accounts:", [u.rsplit("/", 1)[-1] for u in acc])
    v.check(len(stub.calls) > 0 and len(acc) == 1,
            "the sweep reaches the AI stage and writes exactly ONE research_hypotheses object")
    run = p.ai_run(m1)
    acc_in = [i.get("uri") for i in m1.get("inputs", []) if i.get("kind") == "research_hypotheses"]
    print("served manifest batch:", m1.get("batch_id"), "| revisions kept:", len(m1.get("revisions") or []),
          "| research_hypotheses_run:", run, "| account inputs:", [str(u).rsplit("/", 1)[-1] for u in acc_in])
    v.check(m1.get("batch_id") not in (None, p.BATCH) and len(m1.get("revisions") or []) == 1 and len(acc) == 1
            and acc_in == acc and run.get("status") == "OK" and run.get("run_id") == p.run_id_of(acc[0]),
            "the page is republished: a new batch, ONE kept revision, the account among its inputs, "
            "research_hypotheses_run status OK with the account's run_id")
    n_calls = len(stub.calls)
    r2 = p.sweep(p.schedule_payload(spec))
    print("sweep 2:", r2.get("status"), "| new client calls:", len(stub.calls) - n_calls, "| accounts:",
          len(p.accounts(s)))
    v.check(len(stub.calls) == n_calls and len(p.accounts(s)) == 1,
            "one run per page day: a second sweep makes no AI call and the day still holds ONE object")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
