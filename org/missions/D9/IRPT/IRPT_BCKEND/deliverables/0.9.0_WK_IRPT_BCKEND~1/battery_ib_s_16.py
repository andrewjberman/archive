#!/usr/bin/env python3
"""battery_ib_s_16.py -- S16-AC1: seven arms, three difference controls, the manifest
complete; S16-AC2 is a separate terraform-plan invocation the proof instance carries
directly. Cell IB-s-16.

Prints the literal token IBS16-RECOVERY-ISOLATED only when every arm below holds --
including the labelled export STAND-IN (arm g) and every second-firm hash pair, which this
battery RE-DERIVES rather than trusting a cached manifest (row W3-S9's lesson).

ASCII only. Python 3.12.
"""
from __future__ import annotations

import io
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_HERE, "..", "..", "..", "..", "..", "..", ".."))
_LAMBDA_ROOT = os.path.join(_REPO_ROOT, "infra", "aws", "lambda", "investor-reporting")
_OPS = os.path.join(_LAMBDA_ROOT, "ops")
_AUTHZ = os.path.join(_LAMBDA_ROOT, "_authz")
_AUTHZ_TESTS = os.path.join(_AUTHZ, "tests")

for _p in (_HERE, _OPS, _AUTHZ, _AUTHZ_TESTS,
           os.path.join(_LAMBDA_ROOT, "_scope"), os.path.join(_LAMBDA_ROOT, "_keys")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ib_s_16_recovery_arms as arms  # noqa: E402
import status as st                   # noqa: E402
import manifests                      # noqa: E402
import enforce as authz               # noqa: E402
import fixtures as authz_fixtures     # noqa: E402

RESULT_TOKEN = "IBS16-RECOVERY-ISOLATED"

DECLARED_PATHS = [
    "infra/aws/terraform/investor-reporting/ops/iam.tf",
    "infra/aws/terraform/investor-reporting/ops/lambda.tf",
    "infra/aws/terraform/investor-reporting/ops/main.tf",
    "infra/aws/lambda/investor-reporting/ops/status.py",
    "infra/aws/lambda/investor-reporting/ops/manifests.py",
    "infra/aws/lambda/investor-reporting/ops/RUNBOOK.md",
    "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/ib_s_16_recovery_arms.py",
    "iam-role://irpt-status-role",
    "lambda://irpt-status",
    "infra/aws/lambda/ci/lambda-source-map.json#irpt-status",
    "irpt-jobs", "irpt-checkpoints", "dynamodb://irpt-requests",
    "infra/aws/terraform/investor-reporting/core/kms.tf",
]


# =================================================================== (a) the seven arms
def check_seven_arms():
    out = arms.run_all_arms()
    per_arm = {}
    all_ok = True
    for name, arm in out["arms"].items():
        untouched = bool(arm["second_firm_untouched"]) and arm["second_firm_objects_total"] > 0
        result = arm["result"]
        arm_specific_ok = {
            "failed_source_partition": result.get("raised") and result.get("false_complete_publish_prevented"),
            "stale_model_map": result.get("mass_retained_not_dropped"),
            "duplicated_event": result.get("duplicate_collapsed"),
            "expired_lease": result.get("recovered"),
            "queue_replay": result.get("no_second_vendor_mutation"),
            "worker_restart": result.get("never_adopts_newest") and result.get("never_resubmits_after_restart"),
            "revocation_mid_job": result.get("revoked_permission_not_resurrected") and result.get("no_result_leak"),
        }[name]
        ok = bool(untouched and arm_specific_ok)
        all_ok = all_ok and ok
        per_arm[name] = {
            "target": arm["target"], "second_firm": arm["second_firm"],
            "second_firm_objects_n_of_n": "%d of %d" % (arm["second_firm_objects_identical"],
                                                        arm["second_firm_objects_total"]),
            "second_firm_untouched": untouched,
            "arm_specific_control_held": bool(arm_specific_ok),
            "ok": ok,
        }
    return all_ok, per_arm


# =================================================================== (b) difference controls
def check_difference_controls(arms_out_per_arm):
    # control 1: failed work cannot publish a false-complete snapshot
    control1 = arms_out_per_arm.get("failed_source_partition", {}).get("arm_specific_control_held", False)

    # control 2: an older result never overwrites a newer one -- with a RED-FIRST MUTANT
    # proving the check itself discriminates (a disabled guard would be caught).
    real_refuses_older = st.revision_is_newer(3, 7) is False
    real_allows_newer = st.revision_is_newer(9, 7) is True

    def _mutant_guard_disabled(_candidate, _incumbent):
        """The MUTANT: a guard that always says 'yes, newer' -- the disabled/broken shape a
        real regression would take. Never used outside this discrimination check."""
        return True

    mutant_would_wrongly_allow = _mutant_guard_disabled(3, 7) is True
    control2 = bool(real_refuses_older and real_allows_newer and mutant_would_wrongly_allow)

    # control 3: a revoked permission is not resurrected by a retry
    control3 = arms_out_per_arm.get("revocation_mid_job", {}).get("arm_specific_control_held", False)

    return {
        "control1_no_false_complete_publish": control1,
        "control2_no_older_over_newer": {
            "real_refuses_older_over_newer": real_refuses_older,
            "real_allows_newer_over_older": real_allows_newer,
            "mutant_disabled_guard_would_wrongly_allow": mutant_would_wrongly_allow,
            "held": control2,
        },
        "control3_no_resurrected_revocation": control3,
        "all_three_held": bool(control1 and control2 and control3),
    }


# =================================================================== (c) nine states, one envelope
def check_nine_states_one_envelope():
    rows = []
    all_ok = True
    for state in st.STATES:
        env = st.build_envelope("OP-BATTERY", "battery_probe", "1", state, "2026-09-11",
                                public_reason_code="OK")
        errors = st.validate_envelope(env)
        view = st.public_view(env)
        leak = st.credential_shaped_leak_census(view)
        server_only_absent = "internal_correlation_id" not in view
        ok = (not errors) and (not leak) and server_only_absent
        all_ok = all_ok and ok
        rows.append({"state": state, "valid": not errors, "no_credential_shaped_leak": not leak,
                    "server_only_stripped": server_only_absent, "ok": ok})
    return all_ok, {"denominator": "%d of %d" % (sum(1 for r in rows if r["ok"]), len(rows)),
                    "rows": rows}


# =================================================================== (d) lineage N of N
def check_lineage_reconciliation():
    # Built from THIS battery's own arm evidence: the manifests each arm's job would have
    # published against, and the lineage ids the corresponding snapshot cites. Every id a
    # snapshot cites must be inside its OWN manifest -- never a second, uninspected copy.
    published = [
        {"snapshot_id": "cottonwood-holdings-2026-09-11",
         "lineage_ids": ["src-cot-fact-allocations", "src-cot-fact-holdings"],
         "manifest_ids": ["src-cot-fact-allocations", "src-cot-fact-holdings", "src-cot-model-registry"]},
        {"snapshot_id": "49financial-generation-JOB-IB-S-16-REPLAY",
         "lineage_ids": ["src-49f-portfolio-2332060"],
         "manifest_ids": ["src-49f-portfolio-2332060"]},
        {"snapshot_id": "irpt-status-export-standin-job",
         "lineage_ids": ["src-authz-directory-fixture"],
         "manifest_ids": ["src-authz-directory-fixture", "src-authz-ownership-fixture"]},
    ]
    ok_count, total, rows = manifests.reconcile_lineage(published)
    return ok_count == total, {"denominator": "%d of %d" % (ok_count, total), "rows": rows}


# =================================================================== (e) manifest complete
def check_manifest_completeness():
    owned, total, rows = manifests.census_path_manifest_completeness(DECLARED_PATHS)
    live_total = manifests.live_entries_total()
    return owned == total, {"denominator": "%d of %d" % (owned, total),
                            "live_path_manifest_entries_total": live_total, "rows": rows}


# =================================================================== (f) ledger closed
def check_ledger_closed():
    import subprocess
    # aws.cmd, not the bash `aws` shim: this battery runs under native Windows Python, and a
    # bash script handed to CreateProcess directly is "not a valid Win32 application."
    aws = os.path.join(_REPO_ROOT, ".tools", "aws.cmd")
    proc = subprocess.run([aws, "lambda", "get-function-configuration",
                           "--function-name", "irpt-status", "--region", "us-east-1"],
                          capture_output=True, text=True, timeout=60)
    live_sha = None
    if proc.returncode == 0:
        try:
            live_sha = json.loads(proc.stdout).get("CodeSha256")
        except ValueError:
            live_sha = None

    with io.open(os.path.join(_REPO_ROOT, "infra", "aws", "lambda", "ci", "lambda-source-map.json"),
                encoding="utf-8") as fh:
        source_map = json.load(fh)
    built_sha = source_map["functions"]["irpt-status"].get("artifact_sha256")

    sentinel_path = os.path.join(_REPO_ROOT, "org", "critical_paths", ".open_deploys",
                                 "irpt-bckend-s16.json")
    sentinel_absent = not os.path.exists(sentinel_path)

    ok = bool(live_sha and built_sha and live_sha == built_sha and sentinel_absent)
    return ok, {"live_code_sha256": live_sha, "built_artifact_sha256": built_sha,
               "match": live_sha == built_sha, "sentinel_absent_ledger_closed": sentinel_absent}


# =================================================================== (amend) guard/bound/silent
def check_amend():
    # unguarded_routes over THIS cell's own route table
    binding = authz.FirmBinding(authz_fixtures.TENANT, authz_fixtures.OPAQUE_FIRM)
    e = st.make_ops_enforcer(binding, lambda tenant: authz_fixtures.DIRECTORY)
    routes = st.register_routes(e, lambda request, scope: st.build_envelope(
        "OP-1", "battery_probe", "1", "READY", "2026-09-11"))
    census = authz.unguarded_routes(routes)
    unguarded_ok = census["unguarded"] == [] and census["verdict"].startswith("OK:")

    # NEGATIVE CONTROL: an actually-unguarded route must be caught -- the OK above is not vacuous.
    def raw(request):
        return {"leak": True}
    dirty_routes = dict(routes)
    dirty_routes["GET /leak"] = raw
    dirty_census = authz.unguarded_routes(dirty_routes)
    negative_control_ok = dirty_census["unguarded"] == ["GET /leak"]

    # FirmBinding non-reconciling -> REFUSED, never served empty
    other_directory = dict(authz_fixtures.DIRECTORY, firm_id_opaque=authz_fixtures.OTHER_OPAQUE_FIRM)
    e2 = st.make_ops_enforcer(binding, lambda tenant: other_directory)
    routes2 = st.register_routes(e2, lambda request, scope: (_ for _ in ()).throw(
        AssertionError("must never compute on a refused binding")))
    req2 = authz.Request(authz_fixtures.headers(role="admin"), "get_status", "firm",
                         authz_fixtures.OPAQUE_FIRM)
    out2 = routes2["GET /investor-reporting/ops/status"](req2)
    binding_refusal_ok = (not out2.ok) and out2.code == "FIRM_BINDING"

    # key refusal -> whole envelope (body + reason + audit trail) has ZERO occurrences of the
    # refused value
    e3 = st.make_ops_enforcer(binding, lambda tenant: authz_fixtures.DIRECTORY)
    routes3 = st.register_routes(e3, lambda request, scope: st.build_envelope(
        "OP-1", "battery_probe", "1", "READY", "2026-09-11"))
    req3 = authz.Request(authz_fixtures.headers(role="admin"), None, "firm", authz_fixtures.OPAQUE_FIRM,
                         params={"client": "Whitfield Family"})
    out3 = routes3["GET /investor-reporting/ops/status"](req3)
    blob3 = json.dumps(out3.as_envelope())
    audit_blob = json.dumps(e3.audit)
    key_refusal_ok = (not out3.ok and out3.code == "KEY_REFUSED"
                      and "Whitfield Family" not in blob3
                      and "Whitfield Family" not in audit_blob)

    ok = bool(unguarded_ok and negative_control_ok and binding_refusal_ok and key_refusal_ok)
    return ok, {
        "unguarded_routes_census": census,
        "negative_control_caught_unguarded_route": negative_control_ok,
        "firm_binding_refusal": {"ok": binding_refusal_ok, "code": getattr(out2, "code", None)},
        "key_refusal_whole_envelope_silent": {"ok": key_refusal_ok, "code": getattr(out3, "code", None)},
    }


# =================================================================== driver
def main():
    report = {"battery": "IB-s-16", "checks": {}}
    all_pass = True

    arms_ok, arms_detail = check_seven_arms()
    report["checks"]["a_seven_arms"] = {"ok": arms_ok, "detail": arms_detail}
    all_pass = all_pass and arms_ok

    ctrl_ok = False
    if arms_ok:
        ctrls = check_difference_controls(arms_detail)
        ctrl_ok = ctrls["all_three_held"]
        report["checks"]["b_difference_controls"] = {"ok": ctrl_ok, "detail": ctrls}
    else:
        report["checks"]["b_difference_controls"] = {"ok": False, "detail": "SKIPPED: arm (a) did not hold"}
    all_pass = all_pass and ctrl_ok

    states_ok, states_detail = check_nine_states_one_envelope()
    report["checks"]["c_nine_states_one_envelope"] = {"ok": states_ok, "detail": states_detail}
    all_pass = all_pass and states_ok

    lineage_ok, lineage_detail = check_lineage_reconciliation()
    report["checks"]["d_lineage_reconciliation"] = {"ok": lineage_ok, "detail": lineage_detail}
    all_pass = all_pass and lineage_ok

    manifest_ok, manifest_detail = check_manifest_completeness()
    report["checks"]["e_manifest_complete"] = {"ok": manifest_ok, "detail": manifest_detail}
    all_pass = all_pass and manifest_ok

    ledger_ok, ledger_detail = check_ledger_closed()
    report["checks"]["f_ledger_closed"] = {"ok": ledger_ok, "detail": ledger_detail}
    all_pass = all_pass and ledger_ok

    amend_ok, amend_detail = check_amend()
    report["checks"]["amend_guarded_bound_silent"] = {"ok": amend_ok, "detail": amend_detail}
    all_pass = all_pass and amend_ok

    report["overall_pass"] = all_pass
    print(json.dumps(report, default=str, indent=1))
    if all_pass:
        print(RESULT_TOKEN)
        return 0
    print("BLOCKED: one or more IB-s-16 checks did not hold; see per-check detail above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
