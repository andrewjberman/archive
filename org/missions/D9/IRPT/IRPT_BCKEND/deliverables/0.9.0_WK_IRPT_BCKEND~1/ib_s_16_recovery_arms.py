#!/usr/bin/env python3
"""IRPT_BCKEND IB-s-16 -- the seven per-tenant recovery arms, each driven on the DEPLOYED
job's own entry point, each hashing a SECOND FIRM's real QA objects before and after.

MAPPING (deliberately not one-arm-per-job -- the face names four jobs across seven modes):
  (a) failed_source_partition  -> holdings snapshot (IB-s-12), build_snapshot('cottonwood', ...)
                                   via a FailingS3Proxy -- an INJECTED read failure, the same
                                   fault-injection idiom checkpoint.InjectedKill/job.InjectedKill
                                   already establish for this project's other jobs.
  (b) stale_model_map          -> holdings snapshot's OWN expand_model() (IB-s-12), pure,
                                   offline: a dangling model reference retains its mass as
                                   UNRESOLVED rather than being dropped or renormalised.
  (c) duplicated_event         -> mailbox intake poller (IB-s-6), intake.poller.run_scan driven
                                   TWICE under the SAME owner and store with a delta feed that
                                   re-serves page1 -- a resync, not a crash.
  (d) expired_lease            -> ops.manifests.TenantLease (this cell), generalising
                                   intake.checkpoint.ScanLease onto an explicit tenant/job key.
  (e) queue_replay             -> YCharts generation (IB-s-9), ycharts.generate.job.GenerationJob
                                   .run() invoked twice with the SAME job id/request id -- an
                                   SQS at-least-once redelivery.
  (f) worker_restart           -> the SAME generation job, kill_after={"submitting_before_create"}
                                   then resume=True.
  (g) revocation_mid_job       -> EXPORT (IB-s-14) STAND-IN -- IB-s-14 is not on this branch
                                   (in flight on slot ~4), so this arm drives _authz.Enforcer's
                                   OWN submit_job/consume_job async-job mechanism directly (the
                                   SAME mechanism an export render job would use) and is LABELLED
                                   as a stand-in in every print and in the proof instance.

NO LIVE VENDOR CALL anywhere: (a)/(b) touch Opal's own S3 (not a vendor); (c) uses
intake.graph_client.RecordedTransport (no socket, fixtures only); (e)/(f) use
ycharts.generate.transport.ReplayTransport (no socket); (g) uses in-memory fixtures. Arms
(c)-(g) run entirely offline and make NO real AWS call at all; each one's second-firm hash
pair is therefore MEASURED but expected trivially identical, and this module says so rather
than dressing a vacuous check as a discovery.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import copy
import hashlib
import io
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..", "..", "..", ".."))
_LAMBDA_ROOT = os.path.join(_REPO_ROOT, "infra", "aws", "lambda", "investor-reporting")
_GOLD_IRPT = os.path.join(_REPO_ROOT, "data", "assets", "scripts", "gold", "investor_reporting")
_INTAKE = os.path.join(_LAMBDA_ROOT, "intake")
_GEN = os.path.join(_LAMBDA_ROOT, "ycharts", "generate")
_OPS = os.path.join(_LAMBDA_ROOT, "ops")

for _p in (_GOLD_IRPT, _INTAKE, _GEN,
           os.path.join(_LAMBDA_ROOT, "_authz"), os.path.join(_LAMBDA_ROOT, "_authz", "tests"),
           os.path.join(_LAMBDA_ROOT, "_gate"), os.path.join(_LAMBDA_ROOT, "_keys"),
           os.path.join(_LAMBDA_ROOT, "_scope"), _OPS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import holdings_snapshot as hs   # noqa: E402  IB-s-12, this worker's own cell
import poller                    # noqa: E402  IB-s-6
import checkpoint as ckpt        # noqa: E402  IB-s-6
import graph_client as gc        # noqa: E402  IB-s-6
import outbox as ob              # noqa: E402  IB-s-6
import job as jobmod             # noqa: E402  IB-s-9
import transport as gen_tx       # noqa: E402  IB-s-9
import recipe                    # noqa: E402  IB-s-9
import enforce as authz          # noqa: E402  IB-s-3
import fixtures as authz_fixtures  # noqa: E402  IB-s-3
import gate                      # noqa: E402  IB-s-5
import manifests                 # noqa: E402  this cell, IB-s-16

FIRM_BUCKETS = hs.firm_bucket_map()
QA_PREFIXES = ("investor-reporting/qa/holdings/", "investor-reporting/qa/directory/")


# ============================================================== the shared hash census
def _s3():
    import boto3
    return boto3.client("s3", region_name="us-east-1")


def hash_qa_objects(s3, firm_id, prefixes=QA_PREFIXES):
    """Every object under this firm's QA prefixes, sha256'd. Real S3 reads, never a vendor
    call -- Opal's own evidence bucket. RE-DERIVED every call (row W3-S9's lesson: a cached
    hash manifest is never trusted as authoritative)."""
    bucket = FIRM_BUCKETS[firm_id]
    out = {}
    paginator = s3.get_paginator("list_objects_v2")
    for prefix in prefixes:
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                body = s3.get_object(Bucket=bucket, Key=obj["Key"])["Body"].read()
                out[obj["Key"]] = hashlib.sha256(body).hexdigest()
    return out


def compare_hash_sets(before, after):
    keys = sorted(set(before) | set(after))
    identical = sum(1 for k in keys if before.get(k) == after.get(k))
    diffs = [k for k in keys if before.get(k) != after.get(k)]
    return identical, len(keys), diffs


def second_firm_census(s3, second_firm, action):
    """Runs `action()` between two real hash reads of `second_firm`'s QA objects. Returns a
    dict with N of N and the raw before/after so a caller can also assert on the target."""
    before = hash_qa_objects(s3, second_firm)
    result = action()
    after = hash_qa_objects(s3, second_firm)
    identical, total, diffs = compare_hash_sets(before, after)
    return {"second_firm": second_firm, "identical": identical, "total": total,
            "diffs": diffs, "result": result}


# ============================================================== arm (a) failed source partition
class FailingS3Proxy(object):
    """Wraps a real boto3 client; every call raises immediately -- an INJECTED read failure,
    the SAME fault-injection idiom checkpoint.InjectedKill / job.InjectedKill already
    establish elsewhere in this project. Never a live vendor call: no attribute of this proxy
    ever reaches the network."""

    def __init__(self, real):
        self._real = real
        self.calls = 0

    def __getattr__(self, name):
        real_attr = getattr(self._real, name)
        if not callable(real_attr):
            return real_attr

        def wrapper(*a, **kw):
            self.calls += 1
            raise RuntimeError(
                "INJECTED: simulated failed source partition read (%s call #%d)"
                % (name, self.calls))
        return wrapper


def arm_failed_source_partition(s3, target_firm="cottonwood"):
    before_target = hash_qa_objects(s3, target_firm)
    proxy = FailingS3Proxy(s3)
    outcome = "ok"
    try:
        hs.build_snapshot(target_firm, proxy, as_of=None)
    except Exception as exc:  # noqa: BLE001 -- the injected fault IS the assertion
        outcome = "raised:%s:%s" % (type(exc).__name__, str(exc)[:120])
    after_target = hash_qa_objects(s3, target_firm)
    identical, total, diffs = compare_hash_sets(before_target, after_target)

    # Translate through THIS cell's own StatusEnvelope state mapping (ops/status.py) --
    # never a bespoke ad-hoc label.
    import status as st
    state, code = st.state_for_outcome("missing_source")
    return {
        "target_firm": target_firm,
        "injected_read_calls_before_raise": proxy.calls,
        "raised": outcome != "ok",
        "outcome": outcome,
        "target_qa_objects_unchanged": identical == total and total > 0,
        "target_qa_denominator": total,
        "false_complete_publish_prevented": identical == total and total > 0,
        "status_state": state,
        "status_public_reason_code": code,
    }


# ============================================================== arm (b) stale model map
def arm_stale_model_map():
    """Pure, offline: the SAME algorithm build_cot's model-blend path calls
    (holdings_snapshot.expand_model), with a synthetic model registry carrying a dangling
    reference. No S3 call is made by this arm at all."""
    blend_children = {
        "model-A": [("model-B", 0.6), ("model-MISSING", 0.4)],  # model-MISSING is dangling
        "model-B": [],
    }
    roster_is_opal = {"model-A": True, "model-B": True}
    result = hs.expand_model("model-A", blend_children, roster_is_opal)
    import status as st
    unresolved = result.unresolved_mass
    state, code = st.state_for_outcome("ok", unresolved_mass=unresolved)
    return {
        "model_id": "model-A",
        "leaves": result.leaves,
        "unresolved_mass": unresolved,
        "events": result.events,
        "mass_retained_not_dropped": unresolved > 0.0,
        "status_state": state,
        "status_public_reason_code": code,
    }


# ============================================================== arm (c) duplicated event
_INTAKE_FIXTURES = os.path.join(_INTAKE, "fixtures", "graph")


def _load_intake_fixture(name):
    with io.open(os.path.join(_INTAKE_FIXTURES, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


def _intake_page_script():
    """The SAME three-page replay IB-s-6's own offline suite uses to model 'the same
    message delivered twice' -- reused, not reinvented."""
    return [(200, {}, _load_intake_fixture("delta_page1.json")),
            (200, {}, _load_intake_fixture("delta_page2.json")),
            (200, {}, _load_intake_fixture("delta_page3.json"))]


def _intake_fresh_client(script=None):
    return gc.GraphClient(transport=gc.RecordedTransport(fixture_dir=_INTAKE_FIXTURES, script=script),
                          clock={"sleep": lambda s: None, "now": lambda: 0.0})


def arm_duplicated_event():
    store = ckpt.MemoryStore()
    blobs = poller.MemoryBlobs()
    queue = ob.MemoryQueue()
    r1 = poller.run_scan(client=_intake_fresh_client(), store=store, blobs=blobs, queue=queue,
                         owner="irpt-ib-s-16-dup-arm")
    puts_after_r1 = len(blobs.put_calls)
    sent_after_r1 = len(queue.sent)

    # A mailbox resync: the SAME owner scans again and the delta feed re-serves page1's
    # message (and its siblings) regardless of the stored cursor.
    r2 = poller.run_scan(client=_intake_fresh_client(script=_intake_page_script()), store=store,
                         blobs=blobs, queue=queue, owner="irpt-ib-s-16-dup-arm")
    new_puts = len(blobs.put_calls) - puts_after_r1
    new_sends = len(queue.sent) - sent_after_r1
    return {
        "run1_messages_seen": r1.get("messages_seen"),
        "run1_requests_created": r1.get("requests_created"),
        "run2_messages_seen": r2.get("messages_seen"),
        "run2_requests_created": r2.get("requests_created"),
        "run2_already_complete": r2.get("already_complete"),
        "new_s3_puts_from_resync": new_puts,
        "new_queue_sends_from_resync": new_sends,
        "duplicate_collapsed": new_puts == 0 and new_sends == 0
                                and r2.get("already_complete") == r2.get("messages_seen"),
    }


# ============================================================== arm (d) expired lease
def arm_expired_lease():
    store = ckpt.MemoryStore()
    out = manifests.expired_lease_recovery(
        store, "_opal", "holdings-snapshot-scan", "worker-A", "worker-B",
        ttl_seconds=600, now_fn=lambda: 5_000_000)
    out["arm"] = "expired_lease"
    return out


# ============================================================== generation job factory (e)/(f)
_GEN_FIX = os.path.join(_GEN, "fixtures", "har")
_GEN_BUCKET = "opal-data-ycharts"
_GEN_REQUEST_ID = "REQ-" + "ab" * 12
_GEN_REVISION = 0
_GEN_COVER = {"contact_email": "", "contact_phone": "", "contact_url": "",
             "organization": "Opal Capital", "prepared_by": "Opal Investor Reporting",
             "prepared_for": "Advisor submission", "custom_field": "",
             "report_title": "Comprehensive Overview"}
_GEN_HOLDINGS = [
    {"identifier": "SPY", "identifier_namespace": "TICKER",
     "quantity": {"value": 60000.0, "units": "USD"}},
    {"identifier": "AGG", "identifier_namespace": "TICKER",
     "quantity": {"value": 40000.0, "units": "USD"}},
]


def _gen_fixture(name):
    with open(os.path.join(_GEN_FIX, name), encoding="utf-8") as fh:
        return json.load(fh)


def _gen_pdf_bytes():
    with open(os.path.join(_GEN_FIX, "report.pdf"), "rb") as fh:
        return fh.read()


class _FakeResponse(object):
    def __init__(self, body, status=200, content_type="application/pdf"):
        self._body = body
        self.status = status
        self._ct = content_type

    class _H(object):
        def __init__(self, ct):
            self._ct = ct

        def get_content_type(self):
            return self._ct

    @property
    def headers(self):
        return self._H(self._ct)

    def read(self, n=None):
        return self._body[:n] if n else self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class _FakeOpener(object):
    """Records the request headers -- 'no session cookie reached the signed URL' is a
    MEASUREMENT of the request, per IB-s-9's own idiom."""

    def __init__(self, body):
        self.body = body
        self.requests = []

    def open(self, request, timeout=None):
        self.requests.append(sorted(request.headers))
        return _FakeResponse(self.body)


def _gen_owned_name():
    fingerprint = recipe.holdings_fingerprint(_GEN_HOLDINGS)
    return recipe.portfolio_name(_GEN_REQUEST_ID, _GEN_REVISION, fingerprint), fingerprint


def _gen_base_script(collection_owned_name=None):
    dash = _gen_fixture("dashboard.json")
    templates = _gen_fixture("templates.json")
    collection = copy.deepcopy(_gen_fixture("collection.json"))
    if collection_owned_name:
        collection["body"]["portfolios"][0]["name"] = collection_owned_name
    return {
        ("GET", "/dashboard/"): {"status": 200, "content_type": "text/html", "body": dash["body"]},
        ("GET", "/custom_pdf_reports/generate/14141822"): {"status": 200, "body": templates["14141822"]},
        ("GET", "/custom_pdf_reports/generate/14141824"): {"status": 200, "body": templates["14141824"]},
        ("GET", "/custom_pdf_reports/generate/14141847"): {"status": 200, "body": templates["14141847"]},
        ("POST", "/model_portfolios/fixed/holdings_upload/client"): _gen_fixture("upload_ok.json"),
        ("POST", "/model_portfolios/fixed/"): _gen_fixture("create_201.json"),
        ("GET", "/model_portfolios/fixed/"): collection,
        ("GET", "/model_portfolios/2332060/status"): _gen_fixture("status_ok.json"),
        ("POST", "/custom_pdf_reports/validate_report_securities/14141822"): _gen_fixture("validate_200.json"),
        ("POST", "/custom_pdf_reports/validate_report_securities/14141824"): _gen_fixture("validate_200.json"),
        ("POST", "/custom_pdf_reports/validate_report_securities/14141847"): _gen_fixture("validate_200.json"),
        ("POST", "/custom_pdf_reports/14141822"): _gen_fixture("generate_201.json"),
        ("POST", "/custom_pdf_reports/14141824"): _gen_fixture("generate_201.json"),
        ("POST", "/custom_pdf_reports/14141847"): _gen_fixture("generate_201.json"),
    }


_GEN_SENDER_EVIDENCE = {"verified": "VERIFIED", "original_sender_address": "advisor@49financial.com",
                        "verification_method": "FORWARDING_ARRANGEMENT_HEADERS",
                        "display_from_used": False}


def _gen_ingestion_bound():
    return gate.bind_firm(_GEN_SENDER_EVIDENCE)


def _make_generation_job(script, kill_after=None, store=None, blobs=None):
    """Composes job.GenerationJob directly from primitives (never importing IB-s-9's own
    tests/run_offline_suite.py, which installs a process-wide network guard at IMPORT time
    -- this arm needs REAL S3 access for its second-firm hash census in the SAME process, so
    the guard's side effect would be a self-inflicted false negative on every read after it).
    """
    directory = authz_fixtures.DIRECTORY
    binding = authz.FirmBinding(authz_fixtures.TENANT, directory["firm_id_opaque"])
    settings = recipe.load_settings()
    opener = _FakeOpener(_gen_pdf_bytes())
    transport = gen_tx.ReplayTransport(script)
    job = jobmod.GenerationJob(transport, store or jobmod.JobStore(), blobs or jobmod.MemoryBlobs(),
                               binding, directory, settings, _GEN_BUCKET,
                               bound=_gen_ingestion_bound(), kill_after=kill_after, opener=opener)
    return job, opener


def arm_queue_replay():
    name, _fp = _gen_owned_name()
    store = jobmod.JobStore()
    blobs = jobmod.MemoryBlobs()
    job1, opener1 = _make_generation_job(_gen_base_script(collection_owned_name=name), store=store, blobs=blobs)
    r1 = job1.run("JOB-IB-S-16-REPLAY", _GEN_REQUEST_ID, _GEN_REVISION, _GEN_HOLDINGS,
                 variant="OVERVIEW", cover=_GEN_COVER)

    # A REDELIVERED message: a second invocation, same job id/request id/revision/holdings,
    # sharing the SAME durable store the first one wrote to (what a live worker would hold).
    job2, opener2 = _make_generation_job(_gen_base_script(collection_owned_name=name), store=store, blobs=blobs)
    r2 = job2.run("JOB-IB-S-16-REPLAY", _GEN_REQUEST_ID, _GEN_REVISION, _GEN_HOLDINGS,
                 variant="OVERVIEW", cover=_GEN_COVER)
    return {
        "run1_ok": r1.get("ok"), "run1_artifact_key": r1.get("artifact_key"),
        "run1_vendor_pdf_downloads": len(opener1.requests),
        "run2_ok": r2.get("ok"), "run2_outcome": r2.get("outcome"),
        "run2_vendor_requests": r2.get("vendor_requests"),
        "run2_vendor_pdf_downloads": len(opener2.requests),
        "no_second_vendor_mutation": r2.get("outcome") == "EXISTING_ARTIFACT_REUSED"
                                     and r2.get("vendor_requests") == 0
                                     and len(opener2.requests) == 0,
    }


def arm_worker_restart():
    name, _fp = _gen_owned_name()
    store = jobmod.JobStore()
    blobs = jobmod.MemoryBlobs()
    job1, _opener1 = _make_generation_job(_gen_base_script(collection_owned_name=name), store=store,
                                          blobs=blobs, kill_after={"submitting_before_create"})
    killed = None
    try:
        job1.run("JOB-IB-S-16-RESTART", _GEN_REQUEST_ID, _GEN_REVISION, _GEN_HOLDINGS,
                variant="OVERVIEW", cover=_GEN_COVER)
    except jobmod.InjectedKill as exc:
        killed = str(exc)

    job2, opener2 = _make_generation_job(_gen_base_script(collection_owned_name=name), store=store, blobs=blobs)
    r2 = job2.run("JOB-IB-S-16-RESTART", _GEN_REQUEST_ID, _GEN_REVISION, _GEN_HOLDINGS,
                 variant="OVERVIEW", cover=_GEN_COVER, resume=True)
    record = r2.get("record") or {}
    steps = record.get("steps") or []
    reconcile = next((s for s in steps if s.get("step") == "reconcile"), {})
    return {
        "killed_at": killed,
        "resume_ok": r2.get("ok"),
        "reconcile_reason": reconcile.get("reason"),
        "adopted_by_own_name": reconcile.get("reason") == "OWNED_BY_NAME",
        "newest_row_adopted": reconcile.get("newest_row_adopted"),
        "resubmitted": record.get("resubmitted"),
        "never_adopts_newest": reconcile.get("newest_row_adopted") is False,
        "never_resubmits_after_restart": record.get("resubmitted") is False,
    }


# ============================================================== arm (g) revocation mid-job
# EXPORT (IB-s-14) STAND-IN -- IB-s-14 is not on this branch (in flight, slot ~4). This arm
# drives _authz.Enforcer's OWN async-job mechanism (submit_job/consume_job) directly: the
# SAME mechanism an export render job would use to hand a long-running render off and pick
# its result back up. LABELLED here, in the battery output and in the proof instance.
def arm_revocation_mid_job_export_stand_in():
    deps = authz_fixtures.Deps()
    binding = authz.FirmBinding(authz_fixtures.TENANT, authz_fixtures.OPAQUE_FIRM)
    enforcer = authz.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy,
                              artifacts=dict(authz_fixtures.ARTIFACTS), cache={})
    request = authz.Request(authz_fixtures.headers(), "build_report", "account", authz_fixtures.A1)
    submitted = enforcer.submit_job(request, "IB-S-16-EXPORT-STANDIN-JOB")
    deps.revoke()
    consumed = enforcer.consume_job(
        authz.Request(authz_fixtures.headers(), "build_report"),
        "IB-S-16-EXPORT-STANDIN-JOB", {"secret": "SHOULD-NEVER-BE-RETURNED"})
    deps.restore()
    blob = json.dumps(consumed.as_envelope())
    return {
        "stand_in_for": "IB-s-14 irpt-export-render (not on this branch at this cell's cut)",
        "submitted_ok": submitted.ok,
        "consumed_ok": consumed.ok,
        "consumed_code": getattr(consumed, "code", None),
        "revoked_permission_not_resurrected": (not consumed.ok
                                               and getattr(consumed, "code", None) == "EMPTY_GRANT"),
        "no_result_leak": "SHOULD-NEVER-BE-RETURNED" not in blob,
    }


# ============================================================== driver
ARMS = (
    ("failed_source_partition", "cottonwood", "49financial",
     lambda s3: arm_failed_source_partition(s3, "cottonwood")),
    ("stale_model_map", "cottonwood", "inflection",
     lambda s3: arm_stale_model_map()),
    ("duplicated_event", "49financial(mailbox)", "49financial",
     lambda s3: arm_duplicated_event()),
    ("expired_lease", "_opal(ops-lease)", "cottonwood",
     lambda s3: arm_expired_lease()),
    ("queue_replay", "49financial(generation)", "inflection",
     lambda s3: arm_queue_replay()),
    ("worker_restart", "49financial(generation)", "cottonwood",
     lambda s3: arm_worker_restart()),
    ("revocation_mid_job", "EXPORT-STAND-IN(IB-s-14)", "inflection",
     lambda s3: arm_revocation_mid_job_export_stand_in()),
)


def run_all_arms():
    s3 = _s3()
    out = {"arms": {}}
    for name, target, second_firm, fn in ARMS:
        census = second_firm_census(s3, second_firm, lambda fn=fn: fn(s3))
        out["arms"][name] = {
            "target": target,
            "second_firm": census["second_firm"],
            "second_firm_objects_identical": census["identical"],
            "second_firm_objects_total": census["total"],
            "second_firm_diffs": census["diffs"],
            "second_firm_untouched": census["identical"] == census["total"],
            "result": census["result"],
        }
    return out


def main():
    out = run_all_arms()
    print(json.dumps(out, default=str, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
