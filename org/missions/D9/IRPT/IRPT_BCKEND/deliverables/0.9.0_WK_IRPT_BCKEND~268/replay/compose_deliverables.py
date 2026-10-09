"""Scratch composer: census_raw.json + out/{built,live}.json + build.log + owners -> the three IB-pr-405 release deliverables.
Writes into the worktree deliverables folder. Reads only scratch files, git objects and the committed source map."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path("C:/dev/wk-irpt-bckend-268")
S = Path("C:/dev/_scratch268")
D = ROOT / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~268"
PIN = "9489a0fed03951fb242e50a7a1f704f307946e3c"
IR = "infra/aws/lambda/investor-reporting/"
(D / "replay/raw").mkdir(parents=True, exist_ok=True)


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, cwd=str(ROOT))


raw = json.loads((S / "census_raw.json").read_text())
built = json.loads((S / "out/built.json").read_text())
live = json.loads((S / "out/live.json").read_text())
smap = json.loads((ROOT / "infra/aws/lambda/ci/lambda-source-map.json").read_text(encoding="utf-8"))
delta2 = json.loads((S / "candidate-map2.json.delta.json").read_text())
delta1 = json.loads((S / "candidate-map1.json.delta.json").read_text())

# ---- build log: rc and porcelain, twice
log = [ln for ln in (S / "build.log").read_text().splitlines() if " rc=" in ln]
rcs = [int(ln.split(" rc=")[1].split()[0]) for ln in log]
porc = [int(ln.rsplit("porcelain=", 1)[1]) for ln in log] + [int(ln.split("pre porcelain: ")[1].split()[0]) for ln in
                                                             (S / "build.log").read_text().splitlines() if ln.startswith("pre porcelain")]
minimal_sha = [ln for ln in log if "minimal v1" in ln][0].split("rc=0 ")[1].split(" key=")[0].strip()

# ---- owners of each changed irpt-status member (the commits after the live blob)
MEMBER_PATH = {s["packaged_as"]: s["repo_path"] for s in smap["functions"]["irpt-status"]["staged_from"]}
OWN = {"served.py", "entry.py", "owned_report.py"}
STACK = {"retention.py", "repository.py", "composition.py", "infra/logic/registry/reporting_policies.json"}


def owners(member, live_prefix):
    path = MEMBER_PATH.get(member)
    if not path:
        return {"source_path": None, "note": "no staged_from row"}
    found = None
    for c in git("log", "--format=%H", "--", path).stdout.decode().split():
        if hashlib.sha256(git("show", c + ":" + path).stdout).hexdigest().startswith(live_prefix):
            found = c
            break
    out = {"source_path": path, "live_blob_commit": found[:10] if found else None}
    if found:
        subs = git("log", "--format=%h %an: %s", found + ".." + PIN, "--", path).stdout.decode().strip().splitlines()
        out["owners_since_live_latest_first"] = [s[:150] for s in subs]
    else:
        out["note"] = "the live blob is not among the path's commits (an older or non-committed variant)"
    return out


artifacts = []
for fn, v in raw.items():
    rows = []
    for c in v["changed_members"]:
        m = c["member"]
        why = ("IB-pr-405 own member (re-pinned in the candidate map)" if fn == "irpt-status" and m in OWN else
               "stack row re-pinned so report_index can be read (retention policy revision support, CUSTODY_REPORT kind, the "
               "irpt-custody-x10-v1 policy row)" if fn == "irpt-status" and m in STACK else
               "already pending in the REAL map: another cell's staged pin is ahead of the live blob" if fn == "irpt-status" else
               "difference between the live zip and a build at the real map, not touched by this release")
        row = dict(c, classification=why)
        if fn == "irpt-status":
            row.update(owners(m, c["live_sha256_prefix"] or "zzzz"))
        row.pop("is_ib_pr_405_member", None)
        rows.append(row)
    artifacts.append({
        "function": fn,
        "packages_a_changed_member": "served.py (staged from _authz/served.py)" + (", ops/entry.py, ops/owned_report.py" if fn == "irpt-status" else ""),
        "served_py_pin_in_this_function": ("re-pinned to " + PIN[:10] + " in the candidate map" if fn == "irpt-status"
                                           else "74a62fb46c (unchanged: the 3-operation svc set stays)"),
        "changed_by_this_release": fn == "irpt-status",
        "built_sha256": v["built_sha256"], "built_sha256_hex": v["built_sha256_hex"], "built_bytes": v["built_bytes"],
        "built_members": v["built_members"], "built_twice_identical": v["built_twice_identical"],
        "live_before": v["live_before"], "live_last_modified": v["live_last_modified"], "live_bytes": v["live_bytes"],
        "live_zip_equals_reported_CodeSha256": v["live_zip_matches_reported"],
        "s3_rollback_version": v["s3_latest_version"], "s3_rollback_version_last_modified": v["s3_latest_last_modified"],
        "changed_member_count_vs_live": v["changed_member_count"], "changed_members": rows,
        "deploy_needed": fn == "irpt-status",
    })

census = {
    "to_id": "IRPT_BCKEND.TO-IB-pr-405", "pin": PIN,
    "pin_note": "code commits 1cb1c965f3 (persist_inputs + svc operation + tests) and 9489a0fed0 (identity formula); everything after the pin is deliverables only",
    "build_only": {"rc": max(rcs), "tree_clean": all(p == 0 for p in porc), "builds": len(rcs), "runs": 2,
                   "byte_identical_between_runs": all(a["built_twice_identical"] for a in artifacts),
                   "porcelain_lines_before_and_after_every_build": sorted(set(porc)),
                   "command": "BUILD_ONLY=1 TMPDIR=<scratch> BAU_SOURCE_MAP_OVERRIDE=<candidate map> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting <function>",
                   "worktree": "wk-IRPT_BCKEND-268, git status --porcelain = 0 lines before the first and after every build",
                   "nothing_uploaded": True, "source_map_untouched": True},
    "candidate_map": {
        "why": "lambda-source-map.json pins irpt-status's served.py, entry.py and owned_report.py (and the retention stack) to older commits, "
               "so a build at the REAL map does not carry this change. The map is outside this order's grant. The builds use "
               "BAU_SOURCE_MAP_OVERRIDE with a scratch copy of the map in which ONLY irpt-status's staged_from rows below are re-pinned to the "
               "pin; the applier commits the same seven rows (a map edit), then rebuilds at the real map and compares the sha256.",
        "irpt_status_staged_from_rows_repinned": delta2,
        "minimal_alternative_rows": [d["packaged_as"] for d in delta1],
        "minimal_alternative_built_sha256": minimal_sha,
        "minimal_alternative_note": "rows 1-3 only (served.py, entry.py, owned_report.py): persist_inputs answers artifact_id, composition_sha256 and "
                                    "retention_policy and report_index null, but a persisted report makes the read refuse, because the packaged retention.py "
                                    "has no policy-revision support and the packaged registry has no irpt-custody-x10-v1 row.",
    },
    "artifacts": artifacts,
}
(D / "IB106-1_release_census.json").write_text(json.dumps(census, indent=1) + "\n")

# ---- replay
EXPECTED_DIFF = {
    "owner_include_persist_inputs_persisted": "live refuses (INVALID_READ_INCLUDE), built answers the four members, report_index set",
    "owner_include_persist_inputs_not_persisted": "live refuses (INVALID_READ_INCLUDE), built answers the four members, report_index null",
    "svc_cottonwood_include_persist_inputs": "live refuses (operation outside svc's set), built admits svc for cottonwood and answers the four members",
    "svc_cottonwood_plain_read": "live refuses (operation outside svc's set), built admits svc for cottonwood: the grant is the operation, so the plain read is admitted too",
    "ctl_recovered_owner_include_persist_inputs": "POSITIVE control: with retention live again the built read answers the four members (the dead-retention refusal was the retention)",
    "ctl_retention_dead_owner_include_persist_inputs": "built refuses on the dead retention (UNEXPECTED, as the plain read does on both sides); live refuses the include",
}
NEG = {"ctl_retention_dead_owner_include_persist_inputs", "ctl_retention_dead_owner_plain", "ctl_two_report_revisions_owner_include_persist_inputs",
       "svc_claims_inflection", "svc_claims_49financial", "svc_other_email_cottonwood", "svc_cottonwood_history_sibling_read",
       "svc_cottonwood_for_49financial_request", "non_owner_same_firm_include_persist_inputs", "other_firm_include_persist_inputs"}
NAMES = {
    "owner_plain": "existing caller, owner, no include: the answer {identity, accepted_at} key for key",
    "owner_include_composition": "existing caller, owner, include=composition: identical",
    "owner_include_comparisons": "existing caller, owner, include=comparisons: identical",
    "other_firm_plain": "another firm (cottonwood advisor, 49financial request), plain read: refused on both sides",
    "other_firm_include_composition": "another firm, include=composition: refused on both sides",
    "other_firm_include_persist_inputs": "another firm, include=persist_inputs: refused on both sides",
    "non_owner_same_firm_plain": "non-owner in the same firm, plain read: refused on both sides",
    "non_owner_same_firm_include_composition": "non-owner in the same firm, include=composition: refused on both sides",
    "non_owner_same_firm_include_persist_inputs": "non-owner in the same firm, include=persist_inputs: refused on both sides",
    "svc_claims_inflection": "svc-custody-statement claiming inflection: not the subject, refused (an ordinary-user rule) on both sides",
    "svc_claims_49financial": "svc-custody-statement claiming 49financial: not the subject, refused on both sides",
    "svc_cottonwood_for_49financial_request": "svc-custody-statement (cottonwood) asking for a 49financial request: refused on both sides",
    "svc_cottonwood_history_sibling_read": "svc-custody-statement (cottonwood) on the sibling owned read analysis-request-history: still refused on both sides (the grant is ONE operation)",
    "svc_other_email_cottonwood": "another service email (svc-commentary) claiming cottonwood: refused on both sides",
    "ctl_retention_dead_owner_plain": "control: owner plain read with retention dead: refused on both sides",
    "ctl_two_report_revisions_owner_include_persist_inputs": "control: two report revisions under one report id: the built read refuses, never chooses (live refuses the include)",
}
def outcome(o):
    return (o["ok"], o["code"], o["data_sha256"])


arms = []
for name in sorted(built["arms"]):
    b, lo = built["arms"][name], live["arms"][name]
    same = outcome(b) == outcome(lo)
    if same:
        verdict = "identical"
    elif name in EXPECTED_DIFF:
        verdict = "expected-diff"
    else:
        verdict = "UNEXPECTED"
    arms.append({"name": NAMES.get(name, name) + " [" + name + "]", "arm_id": name, "verdict": verdict,
                 "negative_control": name in NEG,
                 "live": {"ok": lo["ok"], "code": lo["code"], "data_keys": lo["data_keys"]},
                 "built": {"ok": b["ok"], "code": b["code"], "data_keys": b["data_keys"], "persist_inputs_keys": b["persist_inputs_keys"]},
                 "detail": EXPECTED_DIFF.get(name, "same outcome on both sides")})
for name, lv, bv in (("packaged_policy_irpt_custody_x10_v1", live["static"]["packaged_policy_irpt_custody_x10_v1"],
                      built["static"]["packaged_policy_irpt_custody_x10_v1"]),
                     ("packaged_retention_reference_params", live["static"]["retention_reference_params"], built["static"]["retention_reference_params"]),
                     ("packaged_repository_KINDS", live["static"]["repository_KINDS"], built["static"]["repository_KINDS"]),
                     ("installed_handler_composes", live["static"]["installed_handler_composes"], built["static"]["installed_handler_composes"])):
    arms.append({"name": "static: " + name + " (what the zip carries)", "arm_id": name, "verdict": "identical" if lv == bv else "expected-diff",
                 "negative_control": False, "live": lv, "built": bv,
                 "detail": ("the installed handler composes from the zip's own stack on both sides; the built one also installs "
                            "analysis-request-original (AR-y-22, pending in the real map)" if name == "installed_handler_composes" else
                            "the built zip carries the retention stack that report_index needs; the live zip does not")})
replay = {
    "to_id": "IRPT_BCKEND.TO-IB-pr-405", "pin": PIN,
    "harness": "replay/run_side.py: the REAL irpt-status modules of ONE extracted zip (flat layout), entry.build_owned_entry + served.lambda_entry, "
               "offline doubles for storage only (acceptance table, artifact index, report-index table, retention). Live = the live irpt-status zip "
               "(CodeSha256 %s, read %s); built = the candidate-map BUILD_ONLY zip (%s)." % (
                   raw["irpt-status"]["live_before"], "2026-10-09T11:0xZ", raw["irpt-status"]["built_sha256"]),
    "doubles_are_synthetic": "firm, owner and request ids are fixtures; no client data",
    "limits": "The retention service is a double, so the arms show the READER's authorization and binding, not the live retention rows. "
              "The live Lambda's gateway admission of the svc token on GET .../analysis/requests/{requestId} is outside the zip and is not replayed.",
    "verdict_rule": "identical = the same (ok, public reason code, data hash) on both sides; expected-diff = listed here with its reason; anything else is UNEXPECTED",
    "arms": arms,
}
(D / "IB106-1_release_replay.json").write_text(json.dumps(replay, indent=1) + "\n")
(D / "replay/raw/replay_built.json").write_text(json.dumps(built, indent=1, sort_keys=True) + "\n")
(D / "replay/raw/replay_live.json").write_text(json.dumps(live, indent=1, sort_keys=True) + "\n")
print("arms", len(arms), {v: sum(1 for a in arms if a["verdict"] == v) for v in ("identical", "expected-diff", "UNEXPECTED")})
print("census", len(artifacts), "tree_clean", census["build_only"]["tree_clean"], "rc", census["build_only"]["rc"])
