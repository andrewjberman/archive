#!/usr/bin/env python3
"""BATTERY IB-rtg-2 -- THE STATUS LOADER READS THE REAL JOB STORE. Four arms, on the REAL
artifact (`ops/entry.py` + `ops/status_loader.py`, unedited apart from this order's own change).

  (a) THE MUTANT, FIRST           the PRE-FIX shape (`_status_envelope` with no loader supplied)
                                  still raises NoSuchOperation on an exercised job -- proves the
                                  battery would have caught the defect this order fixes
  (b) THE COMPOSITION, DIRECT     `status_loader.status_loader(request, scope, store=...)`
                                  against a `checkpoint.MemoryStore()` -- the SAME offline
                                  stand-in `ops/tests/test_manifests.py` already uses for
                                  `TenantLease` -- for a job the intake/export/render path
                                  ACTUALLY CLAIMED (a lease acquired): returns a StatusEnvelope
                                  that validates, never raises
  (c) THE NEGATIVE CONTROL        a status request for a job NEVER claimed refuses (KeyError,
                                  classified NOT_FOUND by `_authz/errors.reason_for`), never
                                  UNEXPECTED and never a fabricated envelope
  (d) THE WIRING, END TO END      `ops/entry.py`'s own `ENTRY.operations` (the deployed object,
                                  not a re-implementation), with `checkpoint.dynamo_store`
                                  monkeypatched to the SAME MemoryStore-backed store for this
                                  process only (no AWS call, no credential) -- the exercised
                                  route no longer raises NoSuchOperation and the public view
                                  strips `internal_correlation_id`

EVERY COUNT PRINTS ITS DENOMINATOR. NO NETWORK CALL, NO AWS CALL, NO VENDOR CALL, NO DEPLOY.

ASCII only. Exit 0 always: the TOKEN is the verdict, not the exit code.
"""
from __future__ import annotations

import datetime as _dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
PKG = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
OPS = os.path.join(PKG, "ops")
INTAKE = os.path.join(PKG, "intake")
AUTHZ = os.path.join(PKG, "_authz")

for _p in (OPS, INTAKE, AUTHZ, os.path.join(PKG, "_scope"), os.path.join(PKG, "_keys")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# BARE-NAME COLLISION, MEASURED: `ops/entry.py`'s OWN docstring names the hazard ("Two files
# called entry.py in one zip is not a collision a test finds") and `status.py`'s module body
# inserts `_LAMBDA_ROOT/directory` at sys.path[0] as a SIDE EFFECT of import (for its deployed
# `lambda_handler`'s local `import handler`) -- so a bare `import entry` issued AFTER `status`
# has been (re-)imported resolves to `directory/entry.py`, not `ops/entry.py`, with no error at
# all (7 files named `entry.py` in this tree; `errors.py` collides 2 ways). Every module this
# battery re-imports is therefore pinned to its OWN directory here, never resolved by bare-name
# search order.
_HOME = {"entry": OPS, "status_loader": OPS, "status": OPS, "manifests": OPS,
        "checkpoint": INTAKE, "enforce": AUTHZ, "errors": AUTHZ}

RESULTS = []


def arm(name, ok, detail):
    RESULTS.append((name, bool(ok), detail))
    print("[%s] %s -- %s" % ("PASS" if ok else "FAIL", name, detail))


def fresh_import(name):
    """Force a CLEAN import of `name` FROM ITS OWN DIRECTORY (see `_HOME` above), dropping any
    cached module -- so arm (a)'s pre-fix probe and arm (d)'s wired probe never share a module
    object with each other's monkeypatches, AND never silently resolve to a same-named sibling
    module from a different Lambda family."""
    home = _HOME.get(name)
    if home is not None:
        sys.path.insert(0, home)   # freshest entry wins the bare-name search, every call
    for mod in list(sys.modules):
        if mod == name or mod.startswith(name + "."):
            del sys.modules[mod]
    module = __import__(name)
    if home is not None:
        resolved_dir = os.path.dirname(os.path.abspath(module.__file__))
        if os.path.normcase(resolved_dir) != os.path.normcase(home):
            raise AssertionError(
                "bare-name collision: import %r resolved to %r, not the expected %r"
                % (name, module.__file__, home))
    return module


def arm_a_mutant():
    """THE MUTANT: `_status_envelope` called with NO loader and an event carrying none either
    -- the EXACT shape `ops/entry.py` was before this order wired `status_loader.status_loader`
    in. If this arm ever stops raising, the fix stopped being distinguishable from its absence."""
    entry = fresh_import("entry")
    authz = fresh_import("enforce")
    request = authz.Request({"X-Firm-Id": "firm-1"}, "status_summary", object_id="job-mutant-1")
    scope = {"verified_request_firm_id": "firm-1"}
    try:
        entry._status_envelope(request, scope, {}, None)
        arm("mutant_pre_fix_shape_still_raises", False,
            "the PRE-FIX call shape did NOT raise -- this arm cannot discriminate the defect")
    except entry._status.NoSuchOperation as exc:
        arm("mutant_pre_fix_shape_still_raises", True,
            "NoSuchOperation, as before this order: %s" % (str(exc)[:100]))
    except Exception as exc:                                    # noqa: BLE001
        arm("mutant_pre_fix_shape_still_raises", False,
            "raised the WRONG exception type %s: %s" % (type(exc).__name__, exc))


def _claimed_store(checkpoint, manifests, tenant, job, now_ts):
    """A `MemoryStore()` with ONE lease row already acquired at `now_ts` -- simulating "the
    intake/export/render path ACTUALLY RAN and claimed this job"."""
    store = checkpoint.MemoryStore()
    lease = manifests.TenantLease(store, tenant, job, owner="worker-under-test",
                                  now_fn=lambda: now_ts)
    acquired = lease.acquire()
    return store, acquired


def arm_b_composition_direct():
    status_loader = fresh_import("status_loader")
    checkpoint = fresh_import("checkpoint")
    manifests = fresh_import("manifests")
    status = fresh_import("status")
    authz = fresh_import("enforce")

    tenant, job = "firm-1", "job-claimed-1"
    now_ts = int(_dt.datetime.now(tz=_dt.timezone.utc).timestamp())  # REAL wall clock, so the lease's own TTL math is measured against the SAME clock status_loader.py reads at call time, never a fixed date that ages past the TTL
    store, acquired = _claimed_store(checkpoint, manifests, tenant, job, now_ts)
    if not acquired:
        arm("composition_fixture_lease_acquired", False, "fixture setup itself failed to acquire")
        return

    request = authz.Request({"X-Firm-Id": tenant}, "status_summary", object_id=job)
    scope = {"verified_request_firm_id": tenant}
    try:
        envelope = status_loader.status_loader(request, scope, store=store)
    except Exception as exc:                                     # noqa: BLE001
        arm("composition_claimed_job_returns_envelope", False,
            "raised %s: %s" % (type(exc).__name__, exc))
        return
    errors = status.validate_envelope(envelope)
    ok = not errors and envelope.get("state") in status.STATES
    arm("composition_claimed_job_returns_envelope", ok,
        "state=%r validate_envelope errors=%r" % (envelope.get("state"), errors))
    arm("composition_state_is_running_for_a_fresh_unexpired_lease",
        envelope.get("state") == "RUNNING",
        "state=%r (expected RUNNING: lease acquired at now_ts, TTL default 600s, unexpired)"
        % envelope.get("state"))
    arm("composition_never_fabricates_ready",
        envelope.get("state") != "READY",
        "state=%r -- this loader has no completion signal to promote itself to READY on"
        % envelope.get("state"))

    # ---- the EXPIRED-lease branch: UNCERTAIN, never READY, never a raise ----
    expired_store = checkpoint.MemoryStore()
    expired_store.items[("irpt-jobs", (("job", job + "-expired"), ("tenant", tenant)))] = {
        "tenant": tenant, "job": job + "-expired",
        "lease_owner": "worker-under-test", "lease_expires_at": 1, "fence_token": 1}
    request2 = authz.Request({"X-Firm-Id": tenant}, "status_summary",
                             object_id=job + "-expired")
    try:
        envelope2 = status_loader.status_loader(request2, scope, store=expired_store)
        errors2 = status.validate_envelope(envelope2)
        arm("composition_expired_lease_is_uncertain_not_ready",
            not errors2 and envelope2.get("state") == "UNCERTAIN",
            "state=%r validate_envelope errors=%r" % (envelope2.get("state"), errors2))
    except Exception as exc:                                     # noqa: BLE001
        arm("composition_expired_lease_is_uncertain_not_ready", False,
            "raised %s: %s (an expired lease must report UNCERTAIN, never raise)"
            % (type(exc).__name__, exc))


def arm_c_negative_control():
    status_loader = fresh_import("status_loader")
    checkpoint = fresh_import("checkpoint")
    errors_mod = fresh_import("errors")
    authz = fresh_import("enforce")

    store = checkpoint.MemoryStore()   # EMPTY: nothing ever claimed this job
    request = authz.Request({"X-Firm-Id": "firm-1"}, "status_summary",
                            object_id="job-never-claimed")
    scope = {"verified_request_firm_id": "firm-1"}
    try:
        status_loader.status_loader(request, scope, store=store)
        arm("negative_control_unclaimed_job_refuses", False,
            "did NOT raise for a job nobody ever claimed")
        return
    except KeyError as exc:
        code = errors_mod.reason_for(exc)
        arm("negative_control_unclaimed_job_refuses", True,
            "raised KeyError: %s" % (str(exc)[:100]))
        arm("negative_control_classified_not_found_not_unexpected", code == "NOT_FOUND",
            "errors.reason_for(exc) = %r (declared code, never UNEXPECTED)" % code)
    except Exception as exc:                                     # noqa: BLE001
        arm("negative_control_unclaimed_job_refuses", False,
            "raised the WRONG exception type %s: %s" % (type(exc).__name__, exc))

    # ---- missing tenant/job entirely: same refusal, never inferred ----
    request_blank = authz.Request({}, "status_summary")
    scope_blank = {}
    try:
        status_loader.status_loader(request_blank, scope_blank, store=store)
        arm("negative_control_no_tenant_no_job_refuses", False, "did NOT raise")
    except KeyError:
        arm("negative_control_no_tenant_no_job_refuses", True,
            "raised KeyError rather than inferring a tenant or a job")
    except Exception as exc:                                     # noqa: BLE001
        arm("negative_control_no_tenant_no_job_refuses", False,
            "raised the WRONG exception type %s: %s" % (type(exc).__name__, exc))


def arm_d_wiring_end_to_end():
    """THE DEPLOYED OBJECT ITSELF: `entry.ENTRY.operations`, never a re-implementation.
    `checkpoint.dynamo_store` is monkeypatched to return a pre-populated `MemoryStore` for
    THIS PROCESS ONLY -- no AWS call, no credential -- so the real composed call chain
    (`ENTRY.operations[...] -> _status_envelope -> status_loader.status_loader ->
    checkpoint.dynamo_store()`) is exercised end to end offline."""
    entry = fresh_import("entry")
    checkpoint = fresh_import("checkpoint")
    manifests = fresh_import("manifests")
    authz = fresh_import("enforce")

    tenant, job = "firm-1", "job-wired-1"
    now_ts = int(_dt.datetime.now(tz=_dt.timezone.utc).timestamp())  # REAL wall clock, so the lease's own TTL math is measured against the SAME clock status_loader.py reads at call time, never a fixed date that ages past the TTL
    store, acquired = _claimed_store(checkpoint, manifests, tenant, job, now_ts)
    if not acquired:
        arm("wiring_fixture_lease_acquired", False, "fixture setup itself failed to acquire")
        return

    original_dynamo_store = entry._status_loader._ckpt.dynamo_store
    entry._status_loader._ckpt.dynamo_store = lambda: store
    try:
        request = authz.Request({"X-Firm-Id": tenant}, "status_summary", object_id=job)
        scope = {"verified_request_firm_id": tenant}
        compute = entry.ENTRY.operations[entry.OPERATION_SUMMARY]
        try:
            view = compute(request, scope, {}, None)
        except Exception as exc:                                 # noqa: BLE001
            arm("wiring_end_to_end_no_longer_raises_nosuchoperation", False,
                "raised %s: %s" % (type(exc).__name__, exc))
            return
        arm("wiring_end_to_end_no_longer_raises_nosuchoperation", True,
            "returned a public view: state=%r" % view.get("state"))
        arm("wiring_end_to_end_public_view_strips_correlation_id",
            "internal_correlation_id" not in view,
            "keys=%r" % sorted(view.keys()))
    finally:
        entry._status_loader._ckpt.dynamo_store = original_dynamo_store

    # ---- and the OTHER two operations share the SAME bound loader ----
    for op_name, op_const in (("analysis-report", entry.OPERATION_REPORT),
                              ("status-job", entry.OPERATION_JOB)):
        bound_loader = entry.ENTRY.operations[op_const].keywords.get("loader")
        arm("wiring_%s_shares_the_real_loader" % op_const,
            bound_loader is entry._status_loader.status_loader,
            "operation=%r loader=%r" % (op_name, bound_loader))


def main():
    print("BATTERY IB-rtg-2 -- THE STATUS LOADER READS THE REAL JOB STORE")
    print("repo: %s" % REPO)
    print("subjects: ops/entry.py (ENTRY.operations, unedited apart from this order's wiring), "
          "ops/status_loader.py (this order's new module), intake/checkpoint.py's irpt-jobs "
          "store shape (MemoryStore, the SAME offline stand-in ops/tests/test_manifests.py uses)")

    arm_a_mutant()
    arm_b_composition_direct()
    arm_c_negative_control()
    arm_d_wiring_end_to_end()

    print("\n=== VINTAGE OF THE BYTES THIS RUN EXERCISED ======================")
    import subprocess
    proc = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True,
                          text=True, timeout=120)
    rows = [ln for ln in (proc.stdout or "").splitlines()
            if ln[3:].startswith("infra/aws/lambda/investor-reporting/ops/")
            or ln[3:].startswith("infra/aws/lambda/ci/lambda-source-map.json")]
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                          capture_output=True, text=True, timeout=120).stdout.strip()
    print("    HEAD: %s" % head)
    if rows:
        print("    %d subject file(s) NOT YET AT HEAD (uncommitted at run time):" % len(rows))
        for ln in rows:
            print("      %s" % ln)
    else:
        print("    0 subject file(s) differ from HEAD: every byte above is IN THE RECORD.")

    print("\n=== SUMMARY ======================================================")
    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    for n, ok, d in RESULTS:
        print("  %-55s %s" % (n, "PASS" if ok else "FAIL"))
    print("  %d of %d arms PASS" % (passed, len(RESULTS)))
    if passed == len(RESULTS) and RESULTS:
        print("\nIBR73-STATUS-LOADER-SERVES-ENVELOPE")
    else:
        print("\nBLOCKED: %d of %d arms FAIL -- the token is withheld."
              % (len(RESULTS) - passed, len(RESULTS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
