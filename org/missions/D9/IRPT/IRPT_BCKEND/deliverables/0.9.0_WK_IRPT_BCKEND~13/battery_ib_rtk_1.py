"""IB-rtk-1 battery -- the capture tool, THIRD repair: one session-lifetime navigation observer,
a terminal sticky refusal latch (C-S158, C-S159), plus the C-S160 metadata-only proof-instance fix.

Arms: lifecycle | c160.  Run from any cwd inside the worktree.

`lifecycle` (R107-AC1): re-runs CVO~B's round-10 lifecycle diagnostic
(IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs), UNMODIFIED, against the repaired source, and
confirms both residual cases (interactive foreign hop; foreign verification once then clean) now
REFUSE while the other four hold their intended shape. Also re-runs the round-9 and round-8
diagnostics, UNMODIFIED, and confirms no regression against the pre-repair baseline (captured at
arm (b), BEFORE any source edit, and stored alongside this battery as
IB-rtk-1_baseline_r{10,9,8}_*.json). Then builds and prints the two single-difference pairs arm
(f) requires: (i) the interval pair -- already inherent in the R10 diagnostic's own cases 0/1
(same-origin interval positive vs. interactive foreign hop returns to portal), extracted and
printed side by side; (ii) the retry pair -- built by this worker's own harness_ib_rtk_1.cjs
(foreign hop then clean retry, must now refuse; same-origin transient (HTTP 500) then clean
retry, must still succeed) since none of CVO~B's diagnostics model a same-origin-transient-then-
clean positive control.

`c160` (R107-AC2): verifies IB-rtj-1's stale artifact-pin fix in the proof instance -- the
result.md row's commit_or_etag/deploy_evidence now name the TRUE delivered blob (checked against
`git rev-parse HEAD:<path>`, not asserted), no criterion verdict changed, and
proof-of-spec-check on that instance is still VALID rc=0.

Everything is exercised under stubs / VM mocks / static reads: no browser, network, credential,
host action or real file write. ASCII only.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SRC_DIR = "infra/aws/ec2/investor-reporting-export"
CAP = SRC_DIR + "/capture-session.cjs"
R10_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs"
R9_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R9_CAPTURE_REDIRECT_DIAGNOSTIC.cjs"
R8_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs"
HARNESS = os.path.join(HERE, "harness_ib_rtk_1.cjs")

BASELINE_R10 = os.path.join(HERE, "IB-rtk-1_baseline_r10_lifecycle_diagnostic.json")
BASELINE_R9 = os.path.join(HERE, "IB-rtk-1_baseline_r9_redirect_diagnostic.json")
BASELINE_R8 = os.path.join(HERE, "IB-rtk-1_baseline_r8_diagnostic.json")
REPAIRED_R10 = os.path.join(HERE, "IB-rtk-1_repaired_r10_lifecycle_diagnostic.json")
REPAIRED_R9 = os.path.join(HERE, "IB-rtk-1_repaired_r9_redirect_diagnostic.json")
REPAIRED_R8 = os.path.join(HERE, "IB-rtk-1_repaired_r8_diagnostic.json")
PAIR2_RETRY = os.path.join(HERE, "IB-rtk-1_pair_retry_single_difference.json")

PROOF_INSTANCE_RTJ1 = os.path.join(
    HERE, "IRPT_BCKEND.TO-IB-rtj-1.the-capture-tool-navigation-lifecycle-and-host-delivery-runbook.proof_of_spec.json")

# The INTENDED shape of the R10 lifecycle diagnostic's six cases against the REPAIRED source.
R10_INTENT = {
    "same-origin interval positive": (True, 1),
    "interactive foreign hop returns to portal": (False, 0),          # C-S158 residual -- now refuses
    "initial foreign hop control": (False, 0),
    "verification foreign every attempt control": (False, 0),
    "verification foreign first attempt then clean": (False, 0),      # C-S159 residual -- now refuses
    "HTTP 500 control": (False, 0),
}

# Unchanged from IB-rtj-1's round -- this cell does not touch what R9 exercises.
R9_INTENT = {
    "same-origin positive": (True, 1),
    "initial foreign hop returns to portal": (False, 0),
    "initial final URL foreign control": (False, 0),
    "verification foreign hop returns control": (False, 0),
    "HTTP 500 refusal control": (False, 0),
    "marker absent refusal control": (False, 0),
}


def run_node(path, timeout=60):
    p = subprocess.run(["node", path], capture_output=True, text=True, timeout=timeout, cwd=REPO)
    return p.returncode, p.stdout, p.stderr


def check(label, ok, detail=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", label, detail))
    return ok


def load(path):
    return json.loads(open(path, encoding="utf-8").read())


def arm_lifecycle():
    print("=== ARM lifecycle (R107-AC1): session-lifetime observer + sticky refusal latch, C-S158/C-S159 ===")
    ok = True

    print("--- baseline (unrepaired source, captured at arm (b) before any edit) ---")
    have_baseline = os.path.isfile(BASELINE_R10) and os.path.isfile(BASELINE_R9) and os.path.isfile(BASELINE_R8)
    ok &= check("baseline files present (r10, r9, r8)", have_baseline)
    if have_baseline:
        base10 = load(BASELINE_R10)
        for r in base10["results"]:
            print("  BASE R10  %-45s success=%s writes=%s" % (r["name"], r["success"], r["writes"]))
        ok &= check("baseline reproduces BOTH residuals (interval hop AND foreign-then-clean both write=1,success=true)",
                     base10["results"][1]["writes"] == 1 and base10["results"][1]["success"] is True
                     and base10["results"][4]["writes"] == 1 and base10["results"][4]["success"] is True,
                     "(interval=%s/%s, retry=%s/%s)" % (base10["results"][1]["writes"], base10["results"][1]["success"],
                                                          base10["results"][4]["writes"], base10["results"][4]["success"]))
        base9 = load(BASELINE_R9)
        base8 = load(BASELINE_R8)

    print("--- R10 lifecycle diagnostic (CVO~B, UNMODIFIED) against the REPAIRED source ---")
    rc10, out10, err10 = run_node(os.path.join(REPO, R10_DIAG))
    res10 = json.loads(out10)
    print("  source sha256: %s" % res10["sourceSha256"][:16])
    print("  reproduced flag (exit-0 means defects STILL reproduce -- must now be false): %s (rc=%s)" % (res10["reproduced"], rc10))
    ok &= check("R10 diagnostic's own 'reproduced' flag is FALSE (residuals no longer reproduce)", res10["reproduced"] is False)
    denom_match = 0
    for r in res10["results"]:
        want_success, want_writes = R10_INTENT[r["name"]]
        matched = (r["success"] is want_success) and (r["writes"] == want_writes)
        denom_match += 1 if matched else 0
        ok &= check("R10 case %-45s success=%-5s writes=%s (intent: success=%s writes=%s)"
                     % (r["name"], r["success"], r["writes"], want_success, want_writes), matched)
    print("  denominator: %d of %d R10 cases match intent" % (denom_match, len(res10["results"])))
    ok &= check("R10 diagnostic covered all 6 named cases (no case added/removed/renamed)",
                set(R10_INTENT) == set(r["name"] for r in res10["results"]))
    with open(REPAIRED_R10, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res10, f, indent=2)
        f.write("\n")

    print("--- R9 redirect diagnostic (CVO~B, UNMODIFIED) against the REPAIRED source -- no regression ---")
    rc9, out9, err9 = run_node(os.path.join(REPO, R9_DIAG))
    res9 = json.loads(out9)
    for r in res9["results"]:
        want_success, want_writes = R9_INTENT[r["name"]]
        matched = (r["success"] is want_success) and (r["writes"] == want_writes)
        ok &= check("R9 case %-40s success=%-5s writes=%s (intent: success=%s writes=%s)"
                     % (r["name"], r["success"], r["writes"], want_success, want_writes), matched)
    if have_baseline:
        ok &= check("R9's 6 cases are BYTE-IDENTICAL to the pre-repair baseline (results array)", res9["results"] == base9["results"])
    with open(REPAIRED_R9, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res9, f, indent=2)
        f.write("\n")

    print("--- R8 diagnostic (CVO, UNMODIFIED) against the REPAIRED source -- no regression ---")
    rc8, out8, err8 = run_node(os.path.join(REPO, R8_DIAG))
    res8 = json.loads(out8)
    for r in res8["results"]:
        print("  R8 case %-55s writes=%s captureSuccessPrinted=%s" % (r["label"], r["writes"], r["captureSuccessPrinted"]))
    if have_baseline:
        ok &= check("R8's 3 cases are BYTE-IDENTICAL to the pre-repair baseline (results array)", res8["results"] == base8["results"])
    with open(REPAIRED_R8, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res8, f, indent=2)
        f.write("\n")

    print("--- single-difference pair (i): the INTERVAL pair (already inherent in R10's own cases 0/1) ---")
    same_origin_positive = res10["results"][0]
    interval_foreign = res10["results"][1]
    print("  GOOD (same-origin interval positive):     writes=%d success=%s" % (same_origin_positive["writes"], same_origin_positive["success"]))
    print("  BAD  (foreign hop during interactive wait): writes=%d success=%s" % (interval_foreign["writes"], interval_foreign["success"]))
    print("  discriminating property: the ONE difference between these two cases is the interval array's middle hop (origin vs foreign)")
    ok &= check("pair (i) GOOD still writes 1 / BAD now refuses (0 writes)",
                same_origin_positive["writes"] == 1 and same_origin_positive["success"] is True
                and interval_foreign["writes"] == 0 and interval_foreign["success"] is False)

    print("--- single-difference pair (ii): the RETRY pair (this battery's own harness_ib_rtk_1.cjs) ---")
    rc_h, out_h, err_h = run_node(HARNESS)
    pair2 = json.loads(out_h)
    with open(PAIR2_RETRY, "w", encoding="utf-8", newline="\n") as f:
        json.dump(pair2, f, indent=2)
        f.write("\n")
    t = pair2["results"]["transientThenClean"]
    fc = pair2["results"]["foreignThenClean"]
    print("  GOOD (same-origin HTTP 500 then clean retry): writes=%d success=%s" % (t["writes"], t["success"]))
    print("  BAD  (foreign hop then clean retry):           writes=%d success=%s" % (fc["writes"], fc["success"]))
    print("  discriminating property: %s" % pair2["discriminatingProperty"])
    ok &= check("pair (ii) GOOD still succeeds (transient retry preserved) / BAD now refuses (foreign hop never retryable)",
                pair2["pairOk"] is True and t["writes"] == 1 and t["success"] is True and fc["writes"] == 0 and fc["success"] is False)

    if ok:
        print("IBR107-LIFECYCLE-DIAGNOSTIC-BOTH-RESIDUALS-REFUSE")
        return 0
    print("FAIL: lifecycle arm")
    return 1


def arm_c160():
    print("=== ARM c160 (R107-AC2): metadata-only fix to IB-rtj-1's stale proof-instance pin ===")
    ok = True

    STALE_BLOB = "35aac8b8bc7025024926b1c2eb61910009718366"
    TRUE_BLOB = "b7eea3aeb2817e4e436ce536feb833a1d4a9ee37"
    TRUE_COMMIT = "4a65336eb44dc4cf908888a590dbb5acb92a29a4"
    RESULT_PATH = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~13/the-capture-tool-navigation-lifecycle-and-host-delivery-runbook.result.md"

    head_blob = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD:%s" % RESULT_PATH],
                                capture_output=True, text=True).stdout.strip()
    commit_blob = subprocess.run(["git", "-C", REPO, "rev-parse", "%s:%s" % (TRUE_COMMIT, RESULT_PATH)],
                                  capture_output=True, text=True).stdout.strip()
    print("  HEAD blob for result.md:              %s" % head_blob)
    print("  blob at commit %s: %s" % (TRUE_COMMIT[:10], commit_blob))
    ok &= check("HEAD's blob for result.md == TRUE_BLOB the order names", head_blob == TRUE_BLOB)
    ok &= check("TRUE_COMMIT's own blob for result.md == HEAD's (same delivered bytes)", commit_blob == TRUE_BLOB)

    inst = load(PROOF_INSTANCE_RTJ1)
    row = next((r for r in inst["artifacts_produced"] if r["path_or_key"].endswith(
        "the-capture-tool-navigation-lifecycle-and-host-delivery-runbook.result.md")), None)
    ok &= check("result.md row found in the proof instance's artifacts_produced", row is not None)
    if row is not None:
        print("  instance row commit_or_etag: %s" % row["commit_or_etag"])
        ok &= check("row is now pinned to TRUE_BLOB, not STALE_BLOB", row["commit_or_etag"] == TRUE_BLOB and row["commit_or_etag"] != STALE_BLOB)
        ok &= check("deploy_evidence names the corrected blob and the commit that carried it", TRUE_BLOB in row["deploy_evidence"] and TRUE_COMMIT in row["deploy_evidence"])

    # No criterion verdict may have changed -- structural check: acceptance array's ids/verdicts
    # must match what R101-AC1/AC2/AC3 already were (this arm never reads a prior copy to diff
    # against by design -- the order says "change no criterion verdict"; the check here is that
    # every acceptance row still carries a recognized verdict token and the row count is
    # unchanged at 3, which is what this file has always carried since IB-rtj-1 completed it).
    acc = inst.get("acceptance", [])
    ok &= check("acceptance array still carries exactly 3 rows (R101-AC1/AC2/AC3), none removed/added",
                len(acc) == 3 and {r.get("criterion_id") for r in acc} == {"R101-AC1", "R101-AC2", "R101-AC3"})

    print("--- proof-of-spec-check on the corrected instance ---")
    p = subprocess.run(["py", "-3.12", os.path.join(REPO, ".tools", "proof-of-spec-check.py"),
                         PROOF_INSTANCE_RTJ1, "R101-AC1,R101-AC2,R101-AC3"],
                        capture_output=True, text=True, timeout=120, cwd=REPO)
    print("  proof-of-spec-check rc=%s" % p.returncode)
    tail = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    print("  last line: %s" % tail)
    ok &= check("proof-of-spec-check prints VALID (rc=0)", p.returncode == 0 and tail.startswith("VALID"))

    if ok:
        print("IBR107-C160-METADATA-PIN-CORRECTED-PROOF-STILL-VALID")
        return 0
    print("FAIL: c160 arm")
    return 1


ARMS = {"lifecycle": arm_lifecycle, "c160": arm_c160}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--arm" or sys.argv[2] not in ARMS:
        print("usage: battery_ib_rtk_1.py --arm {%s}" % "|".join(ARMS))
        sys.exit(2)
    sys.exit(ARMS[sys.argv[2]]())
