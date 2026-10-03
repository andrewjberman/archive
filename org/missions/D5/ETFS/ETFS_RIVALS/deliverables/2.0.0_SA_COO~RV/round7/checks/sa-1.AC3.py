"""RIV-sa-1 AC3 (CONTROL): with the AI gate UNSET, the sweep makes no AI call, and its result and its writes equal
today's. PASS at the base.

Decided from the code: today, with every marker present, the sweep runs nothing and writes nothing. `run_dag` finds
every batch's output, and `sweep.py:469` finds the publish-page marker. A publish over unchanged inputs also writes
nothing (the publish_page module docstring). The cell keeps both. The AI step and its republish happen only when the
gate is set, so with the gate unset nothing changes and there is NO extra republish. The sweep writes no object at all
(no account, no page, no marker, no state object) and returns what it returns today. Extra `detail` keys are allowed:
the cell may report its AI step there.

Fixture (`_s24_sweep`, offline, local sink): page day 2026-09-30, gate unset throughout, transport stubbed.
  - arm A (marker present, after the morning publish): the sweep builds no AI client and makes no AI call, and every
    file under the local sink is byte-identical before and after it;
  - arm A: its result is today's: status OK, outputs [], detail.ran [], complete true, waiting [], unresolved {};
  - arm B (upstream markers present, no morning publish): the sweep publishes the page once, as today. detail.ran is
    ["publish-page"], its outputs are the page's index and manifest, there is ONE publish-page marker (batch g) and no
    kept revision, no AI client is built and no research_hypotheses object is written."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _s24_sweep as p  # noqa: E402


def run(v):
    spec, s, tmp, r0 = p.start(morning=True)
    from rivalfunds import homes


    stub = p.Client()
    p.set_client(stub)
    before = p.snapshot(tmp)
    r = p.sweep(p.schedule_payload(spec))
    after = p.snapshot(tmp)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    d = r.get("detail") or {}
    print("arm A sweep:", r.get("status"), "| outputs:", r.get("outputs"), "| detail:",
          {k: d.get(k) for k in ("ran", "complete", "waiting", "unresolved")}, "| extra detail keys:",
          sorted(set(d) - {"date", "ran", "stopped_at", "complete", "waiting", "unresolved", "out_of_time"}))
    print("arm A client built:", p.STATE["built"], "| calls:", len(stub.calls), "| files:", len(before),
          "| changed:", changed[:5])
    v.check(p.STATE["built"] == 0 and stub.calls == [] and changed == [] and len(before) > 0,
            "arm A: no AI client, no AI call, every file under the sink byte-identical (no extra republish)")
    v.check(r.get("status") == "OK" and r.get("outputs") == [] and d.get("ran") == [] and d.get("complete") is True
            and d.get("waiting") == [] and d.get("unresolved") == {},
            "arm A: the result is today's (OK, no outputs, nothing ran, complete)")

    spec, s, tmp, _ = p.start(morning=False)
    stub = p.Client()
    p.set_client(stub)
    r = p.sweep(p.schedule_payload(spec))
    d = r.get("detail") or {}
    mk = [m.get("batch_id") for m in p.page_markers(s)]
    man = p.manifest(s)
    want = [homes.page(p.DAY, "index.html"), homes.page(p.DAY, "manifest.json")]
    print("arm B sweep:", r.get("status"), "| ran:", d.get("ran"), "| outputs:", [u.rsplit("/", 1)[-1] for u in
          r.get("outputs") or []], "| marker batches:", mk, "| revisions kept:", len(man.get("revisions") or []),
          "| client built:", p.STATE["built"], "| accounts:", len(p.accounts(s)))
    v.check(d.get("ran") == ["publish-page"] and r.get("outputs") == want and mk == [p.BATCH]
            and man.get("revisions") == [] and p.STATE["built"] == 0 and p.accounts(s) == [],
            "arm B: the sweep publishes the page once as today, with no AI client and no account")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
