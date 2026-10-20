#!/usr/bin/env python
"""OG-rl-19 Phase A: assemble W/rl19_release.json and W/PHASE_A_OG-rl-19.json from the records (no value is typed here that a record holds). READ ONLY on AWS (nothing is called). Counts, booleans and short shas only.
usage: python rl19_phasea.py <scratch tests19.json>   (repository root; W/rl19_pa/host_leg.json, oldform_compare.json and W/RL19_PLAN.txt already written)"""
from __future__ import annotations

import io
import json
import re
import shutil
import subprocess
import sys

W = "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/"
P = W + "rl19_pa/"
TREE = "C:/tmp/og-rel-r3c"
BASE, TRUNK = "8e3eddf95916e430e4e9bbf615ca4fd91f9e852f", "a4c6ecfd30ca47a56c317d10ea5dfdcacc8741a4"


def git(*a, cwd=None):
    return subprocess.run(["git"] + list(a), capture_output=True, cwd=cwd)


rel = git("rev-parse", "HEAD", cwd=TREE).stdout.decode().strip()
hl = json.load(io.open(P + "host_leg.json", encoding="utf-8"))
of = json.load(io.open(P + "oldform_compare.json", encoding="utf-8"))
shutil.copyfile(sys.argv[1], P + "tests.json")
t = json.load(io.open(P + "tests.json", encoding="utf-8"))
plan = io.open(W + "RL19_PLAN.txt", encoding="utf-8").read()
pm = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", plan)
targets = re.findall(r"# (aws_iam_role_policy\.\S+) will be updated in-place", plan)
live_host = hl["marker_host"]
json.dump({"base_sha": BASE, "release_sha": rel, "trunk_sha": TRUNK, "live_ref_host": live_host}, io.open(W + "rl19_release.json", "w", encoding="utf-8", newline="\n"), indent=1)
io.open(W + "rl19_release.json", "a", encoding="utf-8").write("\n")
n_red = len(t["named_new_reds_against_live_ref"])
fs = t["full_suite"]
PROCESS_WIDE = (
    "No process, logger, signal, thread, socket, environment key or global config changes. The dual read is code in the Schwab catalog read PER REQUEST: app/integrations/schwab/catalog.py gains, at module level, two re.compile constants "
    "(_MASTER_FOLDER, _FILE_MASTER) and plain function definitions (_firm_form, firm_form_masters, state_bucket, _firm_state, marker_locations, key_in_data) plus changed bodies of Catalog.list_dates and Catalog.read_marker; "
    "app/integrations/schwab/integration.py changes one import line (a function-local `from .catalog import key_in_data`) and one condition. Read, not instrumented: I opened both diffs whole (catalog.py 132 lines changed, integration.py 3). "
    "tools/list does NOT change (the candidate registry counts the same 103 tools on the host as the live ref); the stored grants are untouched; the OLD location keeps being read exactly as today: an old-form master never calls the state bucket "
    "(probe, host, fake client). Two IAM policy bodies change in place, applied separately through safe-apply."
)
body = {
    "release_sha": rel, "base_sha": BASE, "trunk_sha": TRUNK, "live_ref_host": live_host,
    "tests": {"named_passed": t["named_forward"]["passed"], "named_failed": n_red, "named_failed_definition": "named-set failures that do NOT also fail at the base (new reds); the literal count is named_failed_literal",
              "named_failed_literal": t["named_forward"]["failed"], "named_reds_same_at_base": len(t["named_reds_same_at_live_ref"]), "named_both_orders_equal": t["named_forward"]["passed"] == t["named_reverse"]["passed"] and t["named_forward"]["failed"] == t["named_reverse"]["failed"],
              "named_files": t["named_files"], "named_files_new_in_release": t["named_files_new_in_release"],
              "window_set_passed": t["window_forward"]["passed"], "window_set_failed": t["window_forward"]["failed"] + t["window_reverse"]["failed"], "window_both_orders_equal": t["window_forward"]["passed"] == t["window_reverse"]["passed"], "window_files": t["window_files"],
              "suite_difference_named": True, "baseline": "the predicted base 8e3eddf959 (the batch16 release tree, same sparse cone and invocation); the live ref on the host is 13917ef993 and differs from it by the batch16 files only",
              "full_suite": {"release_failed": fs["release_failed"], "base_failed": fs["live_ref_failed"], "only_in_release": fs["only_in_release"], "only_at_base": fs["only_in_live_ref"],
                             "only_in_release_explained": "tests/test_og_sk2.py::test_og_sk2_contract_firm_form_parses_and_copies_are_byte_equal compares the deploy contract copy with org/standards' copy: the release carries the deploy copy (with firm_form) and not the standards copy (it lands in the landing), so it reads red in the release tree alone; it PASSES with trunk's standards copy overlaid (named set, below)."},
              "standards_copy_overlay": t["standards_copy_overlay"], "standards_copy_restored_to_live_ref_bytes": t["standards_copy_restored_to_live_ref_bytes"]},
    "probes": {"sk2_ac1_ok": hl["probe"]["ok"], "sk2_ac1_lines": hl["probe"]["lines"], "not_ok": hl["probe"]["not_ok"], "where": "on the host, in a scratch copy of the service's tree with the four files laid over it, one fresh process under the cgroup hard guard", "guard": hl["guard"]},
    "old_form_unchanged": of["old_form_unchanged"], "old_form_detail": of["per_master"],
    "terraform_plan": {"add": int(pm.group(1)), "change": int(pm.group(2)), "destroy": int(pm.group(3)), "targets": sorted(targets), "at": "trunk a4c6ecfd30 (the working tree's schwab_reader_iam.tf is the same blob), -lock=false, no -out, nothing applied"},
    "host_probe_service": hl["service"], "scratch_removed": hl["scratch_removed"], "candidate_bytes_equal_release": hl["candidate_bytes_equal_release"],
    "process_wide_state": PROCESS_WIDE,
}
io.open(W + "PHASE_A_OG-rl-19.json", "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body}, indent=1) + "\n")
print(json.dumps({k: body[k] for k in ("tests", "probes", "old_form_unchanged", "terraform_plan", "host_probe_service")}, indent=1)[:3000])
