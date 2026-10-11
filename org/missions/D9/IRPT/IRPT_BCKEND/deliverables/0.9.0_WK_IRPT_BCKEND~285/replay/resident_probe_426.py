"""IB-pr-426 replay: the resident-side members (durable_job.py, resident_worker.py, resident_main.py) through ONE extracted tree. Run as
    python -I resident_probe426.py <extracted_zip_dir> <label> <out_json>
In-memory fakes only (a job row dict, an SQS fake, a packager stub); sockets refused; no AWS client; synthetic ids. Each step records the
outcome or the exception class, so a member the live package lacks reads as AttributeError there and as the behaviour here:
  durable_job     DynamoGenerationStore.get_state / mark_i3_sent (record the I3 send once, conditionally)
  resident_worker send_ready (I3 once, marker only after the send returned), ResidentGenerationWorker.mark_ready (READY then I3),
                  producer_for (the allow-list switch), poll_package_once (the commentary_ready poll)
  resident_main   main(--once) with a runtime that carries the commentary_ready queue and packager, and with the three-key runtime
ASCII only."""
import contextlib
import io
import json
import os
import socket
import sys
import types

zip_dir, label, out_path = sys.argv[1:4]
sys.dont_write_bytecode = True
sys.path.insert(0, zip_dir)
os.environ.update({"AWS_ACCESS_KEY_ID": "fake", "AWS_SECRET_ACCESS_KEY": "fake", "AWS_DEFAULT_REGION": "us-east-1"})
os.environ.pop("IRPT_ANALYSIS_READY_QUEUE_URL", None)


def _refuse(self, *a, **k):
    raise OSError("OFFLINE-GUARD")


socket.socket.connect = _refuse
_real_gai = socket.getaddrinfo
socket.getaddrinfo = lambda host, *a, **k: _real_gai(host, *a, **k) if host in (None, "localhost", "127.0.0.1", "::1", "") else (_ for _ in ()).throw(OSError("OFFLINE-GUARD"))

import durable_job  # noqa: E402
import resident_worker as rw  # noqa: E402
import resident_main  # noqa: E402

RID = "REQ-" + "ab" * 12
SHA = "d" * 64
out = {"label": label}


def attempt(fn):
    try:
        return fn()
    except BaseException as exc:  # noqa: BLE001 -- recorded
        return "EXC:" + type(exc).__name__ + (":" + str(exc)[:50] if isinstance(exc, (KeyError, ValueError)) else "")


class CondFailed(Exception):
    response = {"Error": {"Code": "ConditionalCheckFailedException"}}


class JobClient:
    def __init__(self):
        self.row = {"state": {"S": "READY"}, "job_detail": {"S": "{}"}, "composition_sha256": {"S": SHA}}
        self.updates = 0

    def get_item(self, **kw):
        return {"Item": dict(self.row)}

    def update_item(self, **kw):
        expr = kw.get("UpdateExpression", "")
        if "i3_sent_at" in expr:
            if "i3_sent_at" in self.row:
                raise CondFailed()
            self.row["i3_sent_at"] = kw["ExpressionAttributeValues"][":at"]
            self.updates += 1
        return {}


# ---- durable_job
jc = JobClient()
store = durable_job.DynamoGenerationStore(jc, tenant="49financial", request_id=RID, composition_sha256=SHA, now=lambda: 1000)
dj = {"get_state_before": attempt(lambda: sorted(store.get_state(RID)))}
dj["mark_first"] = attempt(lambda: store.mark_i3_sent(RID, "2026-01-01T00:00:00Z"))
dj["mark_second_is_a_noop"] = attempt(lambda: store.mark_i3_sent(RID, "2026-01-02T00:00:00Z"))
dj["i3_marker_updates"] = jc.updates
dj["get_state_after"] = attempt(lambda: sorted(store.get_state(RID)))
dj["marker_value_is_the_first"] = attempt(lambda: store.get_state(RID).get("i3_sent_at") == "2026-01-01T00:00:00Z")
out["durable_job"] = dj


# ---- resident_worker
class MarkStore:
    tenant, request_id = "49financial", RID

    def __init__(self, fail=False):
        self.marks, self.states, self.fail = [], [], fail

    def mark_i3_sent(self, request_id, at):
        if self.fail:
            raise RuntimeError("synthetic")
        self.marks.append(request_id)

    def put_state(self, request_id, state, detail):
        self.states.append((state, sorted(detail)))
        return {"state": state}


def run_send(url, send_ok=True, store_fail=False):
    """store_fail uses a fake store whose mark raises; every other case uses the REAL DynamoGenerationStore over the in-memory job row,
    so the I3 marker is written (or not) by durable_job itself and `marks` is the count of marker writes the job row received."""
    if url:
        os.environ["IRPT_ANALYSIS_READY_QUEUE_URL"] = url
    else:
        os.environ.pop("IRPT_ANALYSIS_READY_QUEUE_URL", None)
    sent = []
    jc2 = JobClient()
    st = MarkStore(True) if store_fail else durable_job.DynamoGenerationStore(jc2, tenant="49financial", request_id=RID, composition_sha256=SHA, now=lambda: 1000)

    def send(queue_url, body):
        if not send_ok:
            raise RuntimeError("synthetic send failure")
        sent.append((queue_url, sorted(json.loads(body))))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = attempt(lambda: rw.send_ready(st, send, RID))
    return {"call": r if isinstance(r, str) else "ok", "sent": len(sent), "sent_to_the_configured_url": all(u == url for u, _ in sent),
            "marks": jc2.updates, "log_tokens": sorted({ln.split(" ")[0] + " " + ln.split(" ")[1] for ln in buf.getvalue().splitlines() if ln.startswith(("WARN", "ERROR"))})}


URL = "https://sqs.us-east-1.amazonaws.com/000000000000/irpt-analysis-ready-fake"
out["send_ready"] = {"url_set_send_ok": run_send(URL), "url_unset": run_send(None), "send_fails": run_send(URL, send_ok=False),
                     "mark_fails": run_send(URL, store_fail=True)}

worker = object.__new__(rw.ResidentGenerationWorker)
worker.store = MarkStore()
sent_ready = []
worker.ready_send = lambda url, body: sent_ready.append(url)
os.environ["IRPT_ANALYSIS_READY_QUEUE_URL"] = URL
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    r = attempt(lambda: worker.mark_ready({"report_ref": "x"}, {"ticket_id": "T-1"}))
out["mark_ready"] = {"call": r if isinstance(r, str) else "ok", "states_written": worker.store.states, "i3_sends": len(sent_ready), "marks": len(worker.store.marks)}

out["producer_for"] = {"allow_listed_principal": attempt(lambda: rw.producer_for({"owner": {"principal_id": "andrew@opalinvest.com"}})),
                       "other_principal": attempt(lambda: rw.producer_for({"owner": {"principal_id": "other@example.com"}})),
                       "no_owner": attempt(lambda: rw.producer_for({}))}


class Sqs:
    def __init__(self, bodies):
        self.bodies, self.deleted, self.received = list(bodies), [], 0

    def receive_message(self, **kw):
        self.received += 1
        if self.bodies and kw.get("QueueUrl", "").endswith("package-fake"):
            return {"Messages": [{"Body": self.bodies.pop(0), "ReceiptHandle": "rh-%d" % self.received}]}
        return {}

    def delete_message(self, **kw):
        self.deleted.append(kw["ReceiptHandle"])


def poll_package(body, packager):
    sqs, buf = Sqs([body]), io.StringIO()
    with contextlib.redirect_stdout(buf):
        n = attempt(lambda: rw.poll_package_once(sqs=sqs, queue_url="https://sqs.us-east-1.amazonaws.com/0/package-fake", packager=packager))
    return {"returned": n, "deleted": len(sqs.deleted), "log": sorted(buf.getvalue().strip().splitlines())}


GOOD = json.dumps({"kind": "commentary_ready", "tenant": "49financial", "request_id": RID})
out["poll_package_once"] = {"attached": poll_package(GOOD, lambda body: {"outcome": "ATTACHED"}),
                            "unknown_outcome_keeps_the_message": poll_package(GOOD, lambda body: {"outcome": "WAIT"}),
                            "not_json_refused_by_name": poll_package("not json", lambda body: {"outcome": "ATTACHED"})}


# ---- resident_main
def run_main(runtime):
    mod = types.ModuleType("probe_factory_426")
    mod.build = lambda: runtime
    sys.modules["probe_factory_426"] = mod
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = attempt(lambda: resident_main.main(["--factory", "probe_factory_426:build", "--once"]))
    return {"rc": rc, "stdout": sorted(buf.getvalue().strip().splitlines())}


assembly = object.__new__(rw.ResidentAssembly)
sqs3 = Sqs([])
base = {"assembly": assembly, "sqs": sqs3, "queue_url": "https://sqs.us-east-1.amazonaws.com/0/generation-fake"}
out["main_three_key_runtime"] = run_main(dict(base))
sqs5 = Sqs([GOOD])
five = dict(base, sqs=sqs5, package_queue_url="https://sqs.us-east-1.amazonaws.com/0/package-fake", packager=lambda body: {"outcome": "ATTACHED"})
r5 = run_main(five)
r5["package_messages_deleted"] = len(sqs5.deleted)
out["main_five_key_runtime_with_commentary_queue"] = r5
json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("OK: %s" % label)
