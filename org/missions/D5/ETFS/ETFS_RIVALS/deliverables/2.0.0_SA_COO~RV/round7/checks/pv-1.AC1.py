"""RIV-pv-1 AC1 (round-6 ruling 3, P2): `run_path` is "scheduled" only on the sweep schedule's own run. An `only` fire,
or any other hand-made event, stamps "ad_hoc". FAIL at the base: `ai_stage.run_for_day` hard-codes provenance
{"run_path": "scheduled"}, so the 09-30 `only:[publish-page]` fire was stamped "scheduled", and the page manifest
carries no run_path at all.

Interface (prescribed; the issuer copies it into the cell):
- The sweep schedule's input (`gen_policies.py` -> `generated.auto.tfvars.json`, the schedule targeting the daily
  Lambda) carries `"run_path": "scheduled"`, and `sweep.trigger_event` passes it through. The sweep stamps "scheduled"
  only for an event that carries run_path "scheduled" and no `only`; every other event stamps "ad_hoc". The check reads
  the payload from the graded tree's generated tfvars, so the schedule change lands in the same cell.
- `ai_stage.run_for_day(sink_spec, day, run_path="ad_hoc", deadline_s=None, **kw)`: the default is "ad_hoc". The value
  goes into every account row's `input_manifest` (the A1 manifest contract) and into the result as `run_path`.
- `publish_page` copies `run_path` into the page manifest's `a1_produced.research_hypotheses_run`, beside status,
  reason and run_id.
- With the gate set, an `only` fire that includes publish-page still writes the day's account when the day holds none.
Residual (stated, not graded): a seat that replays the schedule's payload verbatim stamps "scheduled". The organic
09:00 ET run is told apart by its trigger, which is the CTO's acceptance (ruling 2).

Fixture (`_s24_sweep`, offline, local sink): three fresh sinks for page day 2026-09-30, gate set, transport stubbed.
  - arm 1, an `only` fire (marker present after the morning publish): {"only": ["publish-page"], "date": "2026-09-30",
    "mode": "daily", "batch_id": "rv-ai-adhoc", "sink": <local>} through `sweep.handler_entry`. The account rows'
    run_path is "ad_hoc", and the served manifest's research_hypotheses_run.run_path is "ad_hoc".
  - arm 2, the schedule (upstream markers present, no morning publish): the schedule payload. The rows read
    "scheduled", and the manifest reads "scheduled".
  - arm 3, a hand-made sweep event with no run_path: {"date": "2026-09-30", "mode": "daily", "sink": <local>}, no
    morning publish. The rows read "ad_hoc"."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _s24_sweep as p  # noqa: E402


def fire(morning, event_of):
    spec, s, tmp, _ = p.start(morning=morning)
    p.gate(True)
    stub = p.Client()
    p.set_client(stub)
    ev = event_of(spec)
    r = p.sweep(ev)
    acc = p.accounts(s)
    rows = p.run_paths(s, acc[0]) if len(acc) == 1 else None
    man = p.ai_run(p.manifest(s))
    print("event:", {k: v for k, v in ev.items() if k != "sink"}, "| sweep:", r.get("status"), "| accounts:", len(acc),
          "| rows' run_path:", rows, "| manifest research_hypotheses_run:", man)
    return rows, man.get("run_path")


def run(v):
    rows, man = fire(True, lambda spec: {"only": ["publish-page"], "date": p.DAY, "mode": "daily",
                                         "batch_id": "rv-ai-adhoc", "sink": spec})
    v.check(rows == ["ad_hoc"], "arm 1: an only:[publish-page] fire stamps the account rows run_path ad_hoc")
    v.check(man == "ad_hoc", "arm 1: the page manifest's research_hypotheses_run.run_path is ad_hoc")
    rows, man = fire(False, lambda spec: p.schedule_payload(spec))
    v.check(rows == ["scheduled"], "arm 2: the schedule's own payload stamps the account rows run_path scheduled")
    v.check(man == "scheduled", "arm 2: the page manifest's research_hypotheses_run.run_path is scheduled")
    rows, _ = fire(False, lambda spec: {"date": p.DAY, "mode": "daily", "sink": spec})
    v.check(rows == ["ad_hoc"], "arm 3: a hand-made sweep event (no run_path) stamps the account rows run_path ad_hoc")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
