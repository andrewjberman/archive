"""RIV-dt-1 AC1 (W1-S46, CTO round-7 ruling 1): a deadline-aware vendor timeout. The sweep never loses the page to the AI
step: a vendor call cannot outlive the AI deadline, and the deadline leaves a republish reserve.

FAIL at the base: the deadline wrapper checks the clock only before a call starts and after it returns, so a call started
at deadline-epsilon runs to `ai_client.TIMEOUT_S` (120 s); no call is handed a timeout and no reserve exists.

Interface (prescribed; the issuer copies it into the cell):
- `ai_client.RestClient.chat(messages, model, timeout=None)` passes `timeout` (None = TIMEOUT_S) to the transport.
- `ai_stage._DeadlineClient.chat` hands every call `timeout = min(ai_client.TIMEOUT_S, seconds left to the deadline)`.
- `sweep.REPUBLISH_RESERVE_S` (a number, >= 88: the reviewer's measured in-sweep republish; the cell states its value and
  its measurement). The AI deadline is min(event `ai_deadline_s` or AI_DEADLINE_S, remaining - REPUBLISH_RESERVE_S).

Fixture (`_s24_sweep`, offline, local sink, the schedule payload):
- ARM A (the plant): a Lambda-like context with REPUBLISH_RESERVE_S + 5 s remaining, and a vendor whose FIRST call hangs
  until the timeout it is handed (a timeout raises, as the transport does), capped at 12 s when none is handed.
  - every vendor call is handed a timeout, and none is longer than the time left to the deadline at its start (+0.5 s);
  - no vendor call ends after the deadline (+1.0 s);
  - the AI step reads FAILED with the deadline reason, and the page is republished (a new batch, ONE kept revision).
- ARM B (the control, PASSES at the base too): 900 s remaining and an instant vendor -- the step is OK, an account is
  written, the page is republished, and no call is handed a timeout shorter than ai_client.TIMEOUT_S."""
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _s24_sweep as p  # noqa: E402

HANG_CAP_S = 12.0


class HangClient(p.Client):
    """The vendor: the FIRST call hangs until its handed timeout (then raises, as `requests` does), capped at HANG_CAP_S."""

    def __init__(self, hang: bool):
        super().__init__()
        self.hang, self.log = hang, []

    def chat(self, messages, model, timeout=None):
        t0 = time.monotonic()
        rec = {"t0": t0, "timeout": timeout}
        self.log.append(rec)
        try:
            if self.hang and len(self.log) == 1:
                wait = HANG_CAP_S if timeout is None else min(float(timeout), HANG_CAP_S)
                time.sleep(max(0.0, wait))
                if timeout is not None and wait >= float(timeout):
                    raise TimeoutError("offline vendor: read timed out after %.1f s" % wait)
            return super().chat(messages, model)
        finally:
            rec["t1"] = time.monotonic()


def arm_a(v, sw, ai_client):
    reserve = getattr(sw, "REPUBLISH_RESERVE_S", None)
    print("sweep.REPUBLISH_RESERVE_S:", reserve)
    v.check(isinstance(reserve, (int, float)) and float(reserve) >= 88.0,
            "sweep.REPUBLISH_RESERVE_S exists and covers the measured ~88 s in-sweep republish")
    r_s = float(reserve) if isinstance(reserve, (int, float)) else sw.MARGIN_MS / 1000.0
    spec, s, tmp, r0 = p.start(morning=True)
    p.gate(True)
    cl = HangClient(hang=True)
    p.set_client(cl)
    ctx = p.Context(total_ms=int((r_s + 5.0) * 1000))
    deadline_at = ctx.t0 + 5.0  # remaining - reserve, on the monotonic clock
    r = sw.handler_entry(p.schedule_payload(spec), ctx)
    ai = (r.get("detail") or {}).get("ai") or {}
    m = p.manifest(s)
    print("ARM A: sweep", r.get("status"), "| ai", {k: ai.get(k) for k in ("status", "reason")}, "| republish",
          (ai.get("republish") or {}).get("status"), "| manifest batch", m.get("batch_id"), "| revisions",
          len(m.get("revisions") or []))
    calls = [{"timeout": x["timeout"], "left_at_start": round(deadline_at - x["t0"], 2),
              "ran_s": round(x["t1"] - x["t0"], 2), "end_vs_deadline": round(x["t1"] - deadline_at, 2)} for x in cl.log]
    print("ARM A vendor calls:", calls)
    v.check(len(cl.log) >= 1 and all(x["timeout"] is not None for x in cl.log),
            "every vendor call is handed a timeout")
    v.check(len(cl.log) >= 1 and all(x["timeout"] is not None and float(x["timeout"]) <= (deadline_at - x["t0"]) + 0.5
                                     for x in cl.log),
            "no call's timeout is longer than the time left to the AI deadline at its start")
    v.check(all(x["t1"] <= deadline_at + 1.0 for x in cl.log), "no vendor call ends after the AI deadline")
    v.check(ai.get("status") == "FAILED" and "deadline" in str(ai.get("reason") or "").lower(),
            "the AI step reads FAILED with the deadline reason")
    v.check((ai.get("republish") or {}).get("status") == "OK" and m.get("batch_id") not in (None, p.BATCH)
            and len(m.get("revisions") or []) == 1, "the page is republished: a new batch with ONE kept revision")


def arm_b(v, sw, ai_client):
    spec, s, tmp, r0 = p.start(morning=True)
    p.gate(True)
    cl = HangClient(hang=False)
    p.set_client(cl)
    r = sw.handler_entry(p.schedule_payload(spec), p.Context())
    ai = (r.get("detail") or {}).get("ai") or {}
    print("ARM B: sweep", r.get("status"), "| ai", ai.get("status"), "| accounts", len(p.accounts(s)), "| calls",
          len(cl.log), "| timeouts handed", sorted({x["timeout"] for x in cl.log}, key=str))
    v.check(ai.get("status") == "OK" and len(p.accounts(s)) == 1 and (ai.get("republish") or {}).get("status") == "OK",
            "control: with ample time the step is OK, writes one account and republishes")
    v.check(all(x["timeout"] is None or float(x["timeout"]) >= ai_client.TIMEOUT_S - 1.0 for x in cl.log),
            "control: far from the deadline no call is handed a timeout shorter than the vendor's own")


def run(v):
    p.install()
    from rivalfunds import ai_client, sweep as sw

    arm_a(v, sw, ai_client)
    arm_b(v, sw, ai_client)


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
