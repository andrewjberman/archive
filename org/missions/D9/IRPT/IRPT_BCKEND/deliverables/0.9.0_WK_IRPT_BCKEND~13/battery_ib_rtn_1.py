"""IB-rtn-1 battery -- the capture tool, SIXTH repair: timeout recognized by TYPE or deadline
STATE only (C-S179, sixth time; the CTO's round-13 analysis REVERSES its own round-12 sign-off
acceptance of row W13-S6 -- an exact-string message match is STILL a message-text comparison).

Arms: typed | metadata. Run from any cwd inside the worktree.

`typed` (R114-AC1): re-derives the CURRENT COMMITTED blob of capture-session.cjs via
`git rev-parse HEAD:<path>` (never a raw working-tree read, per row W13-S3's CRLF-grain lesson).
Loads THIS ROUND'S OWN pre-edit baseline (captured at arm (c), before any source change, against
blob 058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae -- the round-13-repaired blob) for the R13 typed-pair
companion, R12, R11, R10 and R9 and R8. Runs `3.0.0_SA_CVO~B`'s round-13 typed-pair companion
diagnostic (IRPT_BCKEND_R13_TYPED_PAIR_DIAGNOSTIC.cjs), UNMODIFIED, against the current committed
blob and confirms the SPLIT: the genuine TimeoutError case recovers; the TypeError and plain-Error
cases sharing IDENTICAL message text are both now TERMINAL. Then re-runs R11, R10, R9, R8
(UNMODIFIED) and R12 (UNMODIFIED, blob passed EXPLICITLY -- its default is an old blob) against the
SAME committed blob, diffs each against this round's own pre-edit baseline, and confirms every
case's externally-visible verdict is unchanged EXCEPT the two explicitly-named-historical cases
(R11's "same-origin timeout then clean", R12's "actual timeout positive control"), each printed
with its full before/after diff and labeled INTENDED, not a regression, per the CTO's round-13
analysis's explicit, prospective ruling. Then runs this worker's own NEW versioned typed-timeout
fixture (fixture_ib_rtn_1_typed_timeout_v1.cjs, arm (b)) and confirms both its cases genuinely
fired a REAL async timer (realTimerFired=True) and that only the genuinely-typed case recovers.

`metadata` (R114-AC2): confirms C-S174's widened FULL-hash comparison is present in
battery_ib_rtm_1.py's own committed source (no `[:12]` truncation left on the CRLF_VALUE/
BLOB_VALUE comparisons; a git-object read, not a working-tree read) and that its own `--arm
metadata` still PASSES under the wider check; confirms C-S194's re-pin -- the IB-rtm-1 proof
instance's result.md artifact row now cites the FINAL result blob
af259448fd8f1eb4d118fa4e7e9b95a7eb1c04ce at commit 9423390c47, never the STALE STOPPED blob
586021b506...; re-derives that blob independently via `git rev-parse <commit>:<path>` (never
trusting the instance's own claim); and re-runs proof-of-spec-check on the edited instance to
confirm it is still VALID.

Everything is exercised under stubs / VM mocks / static git-object reads: no browser, network,
credential, host action or real filesystem write. ASCII only.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SRC_DIR = "infra/aws/ec2/investor-reporting-export"
CAP = SRC_DIR + "/capture-session.cjs"

R13_COMPANION = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R13_TYPED_PAIR_DIAGNOSTIC.cjs"
R12_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R12_CAPTURE_FAILURE_DIAGNOSTIC.cjs"
R11_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R11_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs"
R10_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs"
R9_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R9_CAPTURE_REDIRECT_DIAGNOSTIC.cjs"
R8_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs"
FIXTURE = os.path.join(HERE, "fixture_ib_rtn_1_typed_timeout_v1.cjs")
BATTERY_RTM1 = os.path.join(HERE, "battery_ib_rtm_1.py")
BATTERY_RTM1_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~13/battery_ib_rtm_1.py"

# The round-13-repaired blob -- THIS round's own "before any edit" reference point, distinct from
# any earlier round's pre-repair blob. Confirmed via git cat-file -p | sha256sum to equal HEAD's
# capture-session.cjs blob before this round's source edit landed.
PRE_ROUND14_BLOB = "058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae"

BASELINE_R13C = os.path.join(HERE, "IB-rtn-1_baseline_r13_typed_pair_companion.json")
BASELINE_R11 = os.path.join(HERE, "IB-rtn-1_baseline_r11_lifecycle_diagnostic.json")
BASELINE_R10 = os.path.join(HERE, "IB-rtn-1_baseline_r10_lifecycle_diagnostic.json")
BASELINE_R9 = os.path.join(HERE, "IB-rtn-1_baseline_r9_redirect_diagnostic.json")
BASELINE_R8 = os.path.join(HERE, "IB-rtn-1_baseline_r8_diagnostic.json")
BASELINE_R12 = os.path.join(HERE, "IB-rtn-1_baseline_r12_diagnostic.json")

IB_RTM_1_PROOF = os.path.join(HERE, "IRPT_BCKEND.TO-IB-rtm-1.the-capture-tool-typed-error-classification-and-truthful-cleanup-report.proof_of_spec.json")

STALE_RESULT_BLOB = "586021b506d99288182b7479dc13f1181cd3ba6d"
FINAL_RESULT_BLOB = "af259448fd8f1eb4d118fa4e7e9b95a7eb1c04ce"
FINAL_RESULT_COMMIT = "9423390c47"
RESULT_MD_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~13/the-capture-tool-typed-error-classification-and-truthful-cleanup-report.result.md"


def run_node(path, timeout=60, args=None):
    argv = ["node", path] + (args or [])
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=REPO)
    return p.returncode, p.stdout, p.stderr


def check(label, ok, detail=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", label, detail))
    return ok


def load(path):
    return json.loads(open(path, encoding="utf-8").read())


def git_blob(path):
    p = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD:" + path], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git rev-parse failed for %s: %s" % (path, p.stderr))
    return p.stdout.strip()


def git_blob_at(commit, path):
    p = subprocess.run(["git", "-C", REPO, "rev-parse", commit + ":" + path], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git rev-parse failed for %s:%s: %s" % (commit, path, p.stderr))
    return p.stdout.strip()


def git_show_text(ref):
    p = subprocess.run(["git", "-C", REPO, "show", ref], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git show failed for %s: %s" % (ref, p.stderr))
    return p.stdout


def run_diag(diag_rel_path, blob=None, timeout=60):
    args = [blob] if blob else None
    rc, out, err = run_node(os.path.join(REPO, diag_rel_path), timeout=timeout, args=args)
    try:
        res = json.loads(out)
    except Exception:
        print("  RAW OUTPUT (json parse failed): %s" % out[:2000])
        raise
    return rc, res, err


VERDICT_FIELDS_GENERIC = ("success", "writes", "exitCode", "verificationCalls", "prompts", "storageCalls")


def diff_results(baseline_results, fresh_results, allowed_flip_names, verdict_fields=VERDICT_FIELDS_GENERIC):
    """Element-wise diff of two 'results'-shaped arrays (same length/order). Returns
    (all_flips_allowed, flips) where flips is [(name, before_dict, after_dict), ...] for every
    element whose verdict fields differ at all. all_flips_allowed is True iff every differing
    element's name is in allowed_flip_names (an UNEXPECTED flip fails the arm)."""
    flips = []
    ok = True
    for a, b in zip(baseline_results, fresh_results):
        name = a.get("name")
        verdict_same = all(a.get(k) == b.get(k) for k in verdict_fields)
        if not verdict_same:
            flips.append((name, {k: a.get(k) for k in verdict_fields}, {k: b.get(k) for k in verdict_fields}))
            if name not in allowed_flip_names:
                ok = False
    return ok, flips


def arm_typed():
    print("=== ARM typed (R114-AC1): timeout recognized by TYPE or deadline STATE only (C-S179, sixth repair) ===")
    ok = True

    blob = git_blob(CAP)
    print("current committed capture-session.cjs blob (git rev-parse HEAD:<path>): %s" % blob)
    ok &= check("current blob differs from this round's own pre-edit baseline blob %s" % PRE_ROUND14_BLOB, blob != PRE_ROUND14_BLOB)

    print("--- (c)/(d) 3.0.0_SA_CVO~B's R13 typed-pair companion, UNMODIFIED, blob passed explicitly ---")
    have_baseline_r13c = os.path.isfile(BASELINE_R13C)
    ok &= check("baseline R13-companion file present (captured at arm (c), before any edit, against %s)" % PRE_ROUND14_BLOB, have_baseline_r13c)
    if have_baseline_r13c:
        base13c = load(BASELINE_R13C)
        print("  BASELINE (pre-edit, blob %s): typeOnlyPairFails=%s" % (base13c["blob"], base13c["typeOnlyPairFails"]))
        ok &= check("baseline reproduces the stated defect (typeOnlyPairFails=True)", base13c["typeOnlyPairFails"] is True)

    rc13c, res13c, err13c = run_diag(R13_COMPANION, blob=blob)
    print("  REPAIRED (blob %s): typeOnlyPairFails=%s" % (res13c["blob"], res13c["typeOnlyPairFails"]))
    ok &= check("blob echoed by diagnostic matches the current committed blob", res13c["blob"] == blob)
    ok &= check("split now HOLDS (typeOnlyPairFails=False -- the counterexample no longer reproduces)", res13c["typeOnlyPairFails"] is False)

    by_name = {r["name"]: r for r in res13c["results"]}
    r_typed = by_name["typed deadline-shaped error"]
    r_same_error = by_name["SAME text, plain Error, no deadline fired"]
    r_same_typeerror = by_name["SAME text, TypeError, no deadline fired"]
    r_punct = by_name["plain Error, one punctuation change"]
    r_unrelated = by_name["typed timeout, unrelated message"]
    r_cert = by_name["ordinary certificate error control"]
    print("  typed TimeoutError:        writes=%d success=%s" % (r_typed["writes"], r_typed["success"]))
    print("  SAME text, plain Error:    writes=%d success=%s" % (r_same_error["writes"], r_same_error["success"]))
    print("  SAME text, TypeError:      writes=%d success=%s" % (r_same_typeerror["writes"], r_same_typeerror["success"]))
    print("  plain Error, punctuation:  writes=%d success=%s" % (r_punct["writes"], r_punct["success"]))
    print("  typed, unrelated message:  writes=%d success=%s" % (r_unrelated["writes"], r_unrelated["success"]))
    print("  ordinary cert error:       writes=%d success=%s" % (r_cert["writes"], r_cert["success"]))
    ok &= check("genuine TimeoutError case RECOVERS (writes=1, success=True)", r_typed["writes"] == 1 and r_typed["success"] is True)
    ok &= check("SAME-text plain Error is now TERMINAL (writes=0, success=False) -- closes W13-S6's counterexample", r_same_error["writes"] == 0 and r_same_error["success"] is False)
    ok &= check("SAME-text TypeError is now TERMINAL (writes=0, success=False)", r_same_typeerror["writes"] == 0 and r_same_typeerror["success"] is False)
    ok &= check("punctuation-changed plain Error stays TERMINAL (unaffected)", r_punct["writes"] == 0 and r_punct["success"] is False)
    ok &= check("typed TimeoutError with UNRELATED message still RECOVERS (proves type-based, not message-based)", r_unrelated["writes"] == 1 and r_unrelated["success"] is True)
    ok &= check("ordinary certificate error stays TERMINAL (unaffected)", r_cert["writes"] == 0 and r_cert["success"] is False)

    print("--- R11/R10/R9/R8 diagnostics (CVO, UNMODIFIED) against the current committed blob ---")
    have_baseline = all(os.path.isfile(p) for p in (BASELINE_R11, BASELINE_R10, BASELINE_R9, BASELINE_R8))
    ok &= check("this round's own pre-edit baseline files present (r11, r10, r9, r8, captured at arm (c))", have_baseline)

    rc11, res11, err11 = run_diag(R11_DIAG, blob=blob)
    base11 = load(BASELINE_R11)
    r11_ok, r11_flips = diff_results(base11["results"], res11["results"], allowed_flip_names={"same-origin timeout then clean"})
    print("  R11: %d of %d cases flipped verdict: %s" % (len(r11_flips), len(base11["results"]), [f[0] for f in r11_flips]))
    for name, before, after in r11_flips:
        print("    FLIP '%s' (named-historical, INTENDED not regression, per CTO round-13 analysis):" % name)
        print("      before (round-13-repaired): %s" % before)
        print("      after  (round-14-repaired): %s" % after)
    ok &= check("R11: ONLY the named-historical case ('same-origin timeout then clean') flipped; every other case unchanged", r11_ok)
    ok &= check("R11: the named-historical case flipped TO terminal (writes=0, success=False) as required",
                len(r11_flips) == 1 and r11_flips[0][2]["writes"] == 0 and r11_flips[0][2]["success"] is False)

    for diag_path, baseline_path, label in ((R10_DIAG, BASELINE_R10, "R10"), (R9_DIAG, BASELINE_R9, "R9"), (R8_DIAG, BASELINE_R8, "R8")):
        rc, res, err = run_diag(diag_path, blob=blob)
        base = load(baseline_path)
        same = res["results"] == base["results"]
        print("  %s: results array BYTE-IDENTICAL to this round's own pre-edit baseline: %s" % (label, same))
        ok &= check("%s: zero drift (byte-identical results array, no historical case in this diagnostic)" % label, same)

    print("--- R12 diagnostic (CVO, UNMODIFIED, blob passed EXPLICITLY as argv[2]) ---")
    have_baseline_r12 = os.path.isfile(BASELINE_R12)
    ok &= check("this round's own pre-edit R12 baseline file present", have_baseline_r12)
    rc12, res12, err12 = run_diag(R12_DIAG, blob=blob)
    base12 = load(BASELINE_R12)
    r12_ok, r12_flips = diff_results(base12["retries"], res12["retries"], allowed_flip_names={"actual timeout positive control"})
    print("  R12 retries: %d of %d cases flipped verdict: %s" % (len(r12_flips), len(base12["retries"]), [f[0] for f in r12_flips]))
    for name, before, after in r12_flips:
        print("    FLIP '%s' (named-historical, INTENDED not regression, per CTO round-13 analysis):" % name)
        print("      before (round-13-repaired): %s" % before)
        print("      after  (round-14-repaired): %s" % after)
    ok &= check("R12 retries: ONLY the named-historical case ('actual timeout positive control') flipped", r12_ok)
    ok &= check("R12 retries: the named-historical case flipped TO terminal (writes=0, success=False)",
                len(r12_flips) == 1 and r12_flips[0][2]["writes"] == 0 and r12_flips[0][2]["success"] is False)
    ok &= check("R12: overall taxonomyCounterexample UNAFFECTED (%s -> %s)" % (base12["taxonomyCounterexample"], res12["taxonomyCounterexample"]),
                base12["taxonomyCounterexample"] == res12["taxonomyCounterexample"])
    ok &= check("R12: overall cleanupCounterexample UNAFFECTED (%s -> %s)" % (base12["cleanupCounterexample"], res12["cleanupCounterexample"]),
                base12["cleanupCounterexample"] == res12["cleanupCounterexample"])
    cleanups_same = res12["cleanups"] == base12["cleanups"]
    ok &= check("R12 cleanups: byte-identical to baseline (no historical case in the cleanup pair)", cleanups_same)

    print("--- this worker's own NEW versioned typed-timeout fixture (arm (b), fixture_ib_rtn_1_typed_timeout_v1.cjs) ---")
    rc_fix, out_fix, err_fix = run_node(FIXTURE, args=[blob])
    fix = json.loads(out_fix)
    g = fix["good"]
    b = fix["bad"]
    print("  GOOD (real timer, genuine instanceof TimeoutErrorClass): realTimerFired=%s elapsedMs=%s writes=%d success=%s"
          % (g["realTimerFired"], g["elapsedMs"], g["writes"], g["success"]))
    print("  BAD  (SAME real timer, plain untyped Error, same text):  realTimerFired=%s elapsedMs=%s writes=%d success=%s"
          % (b["realTimerFired"], b["elapsedMs"], b["writes"], b["success"]))
    ok &= check("fixture: BOTH cases genuinely fired a REAL async timer (realTimerFired=True for both)",
                g["realTimerFired"] is True and b["realTimerFired"] is True)
    ok &= check("fixture: GOOD (genuine TimeoutError identity) recovers, BAD (untyped, same message) stays terminal", fix["pairOk"] is True)

    if ok:
        print("IBR114-TYPE-OR-DEADLINE-STATE-ONLY-SPLIT-PAIR-HOLDS")
        return 0
    print("FAIL: typed arm")
    return 1


def arm_metadata():
    print("=== ARM metadata (R114-AC2): C-S174 full-hash comparison + C-S194 re-pin ===")
    ok = True

    print("--- C-S174: battery_ib_rtm_1.py's own committed source no longer truncates to [:12] ---")
    battery_blob = git_blob(BATTERY_RTM1_REL)
    text = git_show_text(battery_blob)
    has_truncated = ("CRLF_VALUE[:12]" in text) or ("BLOB_VALUE[:12]" in text)
    has_full_crlf = "CRLF_VALUE in observed" in text
    has_full_blob = "BLOB_VALUE in observed" in text
    ok &= check("no [:12] truncation remains on CRLF_VALUE/BLOB_VALUE comparisons in battery_ib_rtm_1.py (git-object read)", not has_truncated)
    ok &= check("CRLF_VALUE now compared in FULL (`CRLF_VALUE in observed`)", has_full_crlf)
    ok &= check("BLOB_VALUE now compared in FULL (`BLOB_VALUE in observed`)", has_full_blob)

    print("--- re-running battery_ib_rtm_1.py --arm metadata to confirm the widened check still PASSES ---")
    p = subprocess.run(["py", "-3.12", BATTERY_RTM1, "--arm", "metadata"], capture_output=True, text=True, cwd=REPO, timeout=300)
    last_line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "<empty>"
    print("  battery_ib_rtm_1.py --arm metadata: rc=%d, last line: %s" % (p.returncode, last_line))
    ok &= check("battery_ib_rtm_1.py --arm metadata still passes with the FULL-hash comparison",
                p.returncode == 0 and "IBR113-METADATA-C174-C187-CORRECTED" in p.stdout)

    print("--- C-S194: IB-rtm-1 proof instance's result.md row re-pinned to the FINAL blob ---")
    rtm1 = load(IB_RTM_1_PROOF)
    result_row = None
    for a in rtm1["artifacts_produced"]:
        if a["path_or_key"].endswith("the-capture-tool-typed-error-classification-and-truthful-cleanup-report.result.md"):
            result_row = a
            break
    ok &= check("result.md artifact row found in IB-rtm-1's proof instance", result_row is not None)
    ok &= check("proof instance's commit_or_etag is no longer the STALE STOPPED blob %s" % STALE_RESULT_BLOB,
                result_row is not None and result_row["commit_or_etag"] != STALE_RESULT_BLOB)
    ok &= check("proof instance's commit_or_etag now equals the FINAL result blob %s" % FINAL_RESULT_BLOB,
                result_row is not None and result_row["commit_or_etag"] == FINAL_RESULT_BLOB)
    ok &= check("deploy_evidence cites the final result commit %s" % FINAL_RESULT_COMMIT,
                result_row is not None and FINAL_RESULT_COMMIT in result_row.get("deploy_evidence", ""))

    true_blob_at_commit = git_blob_at(FINAL_RESULT_COMMIT, RESULT_MD_REL)
    print("  git-object-derived blob at commit %s: %s" % (FINAL_RESULT_COMMIT, true_blob_at_commit))
    ok &= check("git-object-derived blob at the cited commit equals FINAL_RESULT_BLOB (re-derived, not trusted)",
                true_blob_at_commit == FINAL_RESULT_BLOB)

    print("--- re-running proof-of-spec-check on the edited IB-rtm-1 instance ---")
    p2 = subprocess.run(["py", "-3.12", ".tools/proof-of-spec-check.py", IB_RTM_1_PROOF, "R113-AC1,R113-AC2,R113-AC3"],
                         capture_output=True, text=True, cwd=REPO, timeout=120)
    out_or_err = p2.stdout.strip() or p2.stderr.strip()
    last2 = out_or_err.splitlines()[-1] if out_or_err else "<empty>"
    print("  proof-of-spec-check rc=%d, last line: %s" % (p2.returncode, last2))
    ok &= check("IB-rtm-1 proof instance still VALID after the re-pin (rc=0)", p2.returncode == 0)

    if ok:
        print("IBR114-METADATA-C174-C194-CORRECTED")
        return 0
    print("FAIL: metadata arm")
    return 1


ARMS = {"typed": arm_typed, "metadata": arm_metadata}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--arm" or sys.argv[2] not in ARMS:
        print("usage: battery_ib_rtn_1.py --arm {%s}" % "|".join(ARMS))
        sys.exit(2)
    sys.exit(ARMS[sys.argv[2]]())
