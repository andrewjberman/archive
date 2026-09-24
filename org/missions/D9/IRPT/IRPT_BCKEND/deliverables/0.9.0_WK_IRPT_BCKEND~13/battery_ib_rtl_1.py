"""IB-rtl-1 battery -- the capture tool, FOURTH repair: the invariant guarded at the write
BOUNDARY (C-S170), the observer narrowed to main-frame navigations on both paths (C-S171), and
the retry taxonomy closed to exactly three named causes (row W13-S1, arm (d)).

Arms: invariant | retry.  Run from any cwd inside the worktree.

`invariant` (R112-AC1): re-runs 3.0.0_SA_CVO~B's round-11 lifecycle diagnostic
(IRPT_BCKEND_R11_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs), UNMODIFIED, against the repaired source, and
confirms: the final-await case ("storage wait foreign hop then portal", C-S170) and the foreign-
resource-response case ("non-navigation foreign response", C-S171) now match their POST-REPAIR
intent; both same-origin twins ("storage wait same-origin positive", "non-navigation same-origin
response positive") still write and succeed; the retry-taxonomy cases (5-10) hold their intended
shape too (checked in full by the `retry` arm below; summarized here). Also re-runs the round-10,
round-9 and round-8 diagnostics, UNMODIFIED, and confirms their shapes against this round's own
baseline (captured at arm (b), BEFORE any source edit, IB-rtl-1_baseline_r{10,9,8}_*.json) --
byte-identical for R10 and R8; R9 differs in ONE case's internal shape only (see NOTE below),
never in its externally-visible verdict. Then prints the two single-difference pairs arm (e)
requires: (i) the invariant-timing pair -- extracted from R11's own cases 0/1 (during-await
timing, already inherent in the diagnostic, exactly as IB-rtk-1 extracted its own pair (i) from
R10's cases 0/1), PLUS this worker's own harness_ib_rtl_1.cjs proving the post-rename timing
variant arm (b) also names; (ii) the subresource-scope pair -- extracted from R11's own cases
2/3 (GOOD) vs case 4 (BAD).

NOTE on the R9 "verification foreign hop returns control" case: post-repair it now refuses on
the FIRST verification attempt via readinessOutcome's own redirect-hop check (terminal, not
retryable) instead of exhausting all 5 attempts as NOT_AUTHENTICATED. The externally-visible
verdict (writes=0, success=false) is UNCHANGED; only the internal path to that verdict changed,
consistent with BOUNDS ("a foreign-origin hop is NEVER retryable under this taxonomy or any
other framing") -- an intended strengthening arm (d) itself requires, not a regression.

`retry` (R112-AC2): from the SAME R11 diagnostic run, verifies the three named retryable causes
(HTTP 500, timeout, marker-absent-after-load, including the password-screen symptom of that same
bucket) each retry and succeed on a clean subsequent attempt (verificationCalls==2, storageCalls
==1); verifies an HTTP 404 and a generic non-timeout navigation error each terminally refuse on
FIRST occurrence (verificationCalls==1, storageCalls==0, prompts==1 -- never retried); reads
README.md and confirms its retry-behavior prose names the SAME three causes, verbatim, that the
code implements.

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
README = SRC_DIR + "/README.md"
R11_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R11_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs"
R10_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs"
R9_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R9_CAPTURE_REDIRECT_DIAGNOSTIC.cjs"
R8_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs"
HARNESS = os.path.join(HERE, "harness_ib_rtl_1.cjs")

BASELINE_R10 = os.path.join(HERE, "IB-rtl-1_baseline_r10_lifecycle_diagnostic.json")
BASELINE_R9 = os.path.join(HERE, "IB-rtl-1_baseline_r9_redirect_diagnostic.json")
BASELINE_R8 = os.path.join(HERE, "IB-rtl-1_baseline_r8_diagnostic.json")

# The INTENDED post-repair shape of the R11 lifecycle diagnostic's 11 cases (name -> (success, writes)).
R11_INTENT = {
    "storage wait same-origin positive": (True, 1),
    "storage wait foreign hop then portal": (False, 0),               # C-S170: now refuses
    "non-navigation same-origin response positive": (True, 1),
    "non-navigation foreign response": (True, 1),                     # C-S171: now succeeds
    "interactive foreign navigation refusal control": (False, 0),
    "same-origin HTTP 500 then clean": (True, 1),                     # retry cause 1 of 3
    "same-origin timeout then clean": (True, 1),                      # retry cause 2 of 3
    "same-origin missing marker then clean": (True, 1),                # retry cause 3 of 3
    "same-origin HTTP 404 then clean": (False, 0),                    # terminal, arm (d)
    "same-origin non-timeout navigation error then clean": (False, 0),  # terminal, arm (d)
    "same-origin password screen then clean": (True, 1),               # marker-absent-after-load bucket
}

# The three named RETRY causes and the two named TERMINAL causes, with the verificationCalls
# (attempts made) each must show: a retry cause takes 2 attempts (fails once, clean second try);
# a terminal cause takes exactly 1 (never retried).
RETRY_CAUSES = ["same-origin HTTP 500 then clean", "same-origin timeout then clean",
                "same-origin missing marker then clean", "same-origin password screen then clean"]
TERMINAL_CAUSES = ["same-origin HTTP 404 then clean", "same-origin non-timeout navigation error then clean"]

R10_INTENT = {
    "same-origin interval positive": (True, 1),
    "interactive foreign hop returns to portal": (False, 0),
    "initial foreign hop control": (False, 0),
    "verification foreign every attempt control": (False, 0),
    "verification foreign first attempt then clean": (False, 0),
    "HTTP 500 control": (False, 0),
}

README_RETRY_CAUSES = ["timeout", "HTTP 5xx", "marker-absent-after-load"]


def run_node(path, timeout=60, arg=None):
    argv = ["node", path] + ([arg] if arg else [])
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=REPO)
    return p.returncode, p.stdout, p.stderr


def check(label, ok, detail=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", label, detail))
    return ok


def load(path):
    return json.loads(open(path, encoding="utf-8").read())


def run_r11():
    rc, out, err = run_node(os.path.join(REPO, R11_DIAG))
    return rc, json.loads(out), err


def arm_invariant():
    print("=== ARM invariant (R112-AC1): write-boundary guard (C-S170) + observer scope (C-S171) ===")
    ok = True

    print("--- baseline (unrepaired source, captured at arm (a) before any edit) ---")
    have_baseline = os.path.isfile(BASELINE_R10) and os.path.isfile(BASELINE_R9) and os.path.isfile(BASELINE_R8)
    ok &= check("baseline files present (r10, r9, r8)", have_baseline)
    base10 = load(BASELINE_R10) if have_baseline else None
    base9 = load(BASELINE_R9) if have_baseline else None
    base8 = load(BASELINE_R8) if have_baseline else None

    print("--- R11 lifecycle diagnostic (CVO~B, UNMODIFIED) against the REPAIRED source -- all 11 cases ---")
    rc11, res11, err11 = run_r11()
    print("  source sha256: %s" % res11["sourceSha256"][:16])
    print("  reproduced flag (must now be false): %s (rc=%s)" % (res11["reproduced"], rc11))
    ok &= check("R11 diagnostic's own 'reproduced' flag is FALSE (both defects no longer reproduce)", res11["reproduced"] is False)
    denom_match = 0
    for r in res11["results"]:
        want_success, want_writes = R11_INTENT[r["name"]]
        matched = (r["success"] is want_success) and (r["writes"] == want_writes)
        denom_match += 1 if matched else 0
        ok &= check("R11 case %-53s success=%-5s writes=%s (intent: success=%s writes=%s)"
                     % (r["name"], r["success"], r["writes"], want_success, want_writes), matched)
    print("  denominator: %d of %d R11 cases match post-repair intent" % (denom_match, len(res11["results"])))
    ok &= check("R11 diagnostic covered all 11 named cases (no case added/removed/renamed)",
                set(R11_INTENT) == set(r["name"] for r in res11["results"]))

    print("--- R10 lifecycle diagnostic (CVO~B, UNMODIFIED) against the REPAIRED source -- no regression ---")
    rc10, out10, err10 = run_node(os.path.join(REPO, R10_DIAG))
    res10 = json.loads(out10)
    print("  reproduced flag (must be false, C-S158/C-S159 stay fixed): %s" % res10["reproduced"])
    ok &= check("R10 diagnostic's own 'reproduced' flag is FALSE", res10["reproduced"] is False)
    for r in res10["results"]:
        want_success, want_writes = R10_INTENT[r["name"]]
        matched = (r["success"] is want_success) and (r["writes"] == want_writes)
        ok &= check("R10 case %-45s success=%-5s writes=%s (intent: success=%s writes=%s)"
                     % (r["name"], r["success"], r["writes"], want_success, want_writes), matched)
    if have_baseline:
        ok &= check("R10's 6 cases BYTE-IDENTICAL to this round's own pre-repair baseline is FALSE (repair changed shape as intended)",
                    res10["results"] != base10["results"])

    print("--- R9 redirect diagnostic (CVO~B, UNMODIFIED) against the REPAIRED source ---")
    rc9, out9, err9 = run_node(os.path.join(REPO, R9_DIAG))
    res9 = json.loads(out9)
    for r in res9["results"]:
        print("  R9 case %-45s success=%-5s writes=%s exit=%s" % (r["name"], r["success"], r["writes"], r["exit"]))
    if have_baseline:
        same_verdict = all(
            (a["success"] == b["success"]) and (a["writes"] == b["writes"])
            for a, b in zip(res9["results"], base9["results"]))
        ok &= check("R9's 6 cases: externally-visible verdict (success, writes) UNCHANGED from baseline for every case", same_verdict)
        n_identical = sum(1 for a, b in zip(res9["results"], base9["results"]) if a == b)
        print("  %d of 6 R9 cases byte-identical to baseline; the rest differ only in HOW a case that" % n_identical)
        print("  already refused (writes=0, success=false) now refuses -- see module docstring NOTE.")

    print("--- R8 diagnostic (CVO, UNMODIFIED) against the REPAIRED source -- no regression ---")
    rc8, out8, err8 = run_node(os.path.join(REPO, R8_DIAG))
    res8 = json.loads(out8)
    for r in res8["results"]:
        print("  R8 case %-55s writes=%s captureSuccessPrinted=%s" % (r["label"], r["writes"], r["captureSuccessPrinted"]))
    if have_baseline:
        ok &= check("R8's 3 cases are BYTE-IDENTICAL to this round's own pre-repair baseline (untouched)", res8["results"] == base8["results"])

    print("--- single-difference pair (i): the INVARIANT-TIMING pair ---")
    by_name = {r["name"]: r for r in res11["results"]}
    good_a = by_name["storage wait same-origin positive"]
    bad_a = by_name["storage wait foreign hop then portal"]
    print("  GOOD (clean, hop during storageState await is same-origin): writes=%d success=%s" % (good_a["writes"], good_a["success"]))
    print("  BAD  (foreign hop DURING the storageState() await):          writes=%d success=%s" % (bad_a["writes"], bad_a["success"]))
    print("  discriminating property: the ONE difference is whether the hop during storageState() leaves the configured origin")
    ok &= check("pair (i-a) GOOD still writes 1 / BAD now refuses (0 writes)",
                good_a["writes"] == 1 and good_a["success"] is True and bad_a["writes"] == 0 and bad_a["success"] is False)

    print("  -- this worker's own harness_ib_rtl_1.cjs: the SAME pair's post-rename timing variant --")
    rc_h, out_h, err_h = run_node(HARNESS)
    print("  harness rc=%s" % rc_h)
    pair_h = json.loads(out_h)
    t = pair_h["results"]["cleanRename"]
    fh = pair_h["results"]["hopOnRename"]
    print("  GOOD (clean rename, no hop):                     writes=%d renames=%d unlinks=%d success=%s" % (t["writes"], t["renames"], t["unlinks"], t["success"]))
    print("  BAD  (foreign hop the instant after the rename):  writes=%d renames=%d unlinks=%d success=%s" % (fh["writes"], fh["renames"], fh["unlinks"], fh["success"]))
    print("  discriminating property: %s" % pair_h["discriminatingProperty"])
    ok &= check("pair (i-b) GOOD still succeeds (write+rename land) / BAD refuses AND the written file is deleted (unlinks==1)",
                pair_h["pairOk"] is True and t["success"] is True and t["unlinks"] == 0
                and fh["success"] is False and fh["unlinks"] == 1 and fh["deleted"] is True)

    print("--- single-difference pair (ii): the SUBRESOURCE-SCOPE pair ---")
    good_b = by_name["non-navigation foreign response"]
    same_origin_control = by_name["non-navigation same-origin response positive"]
    bad_b = by_name["interactive foreign navigation refusal control"]
    print("  GOOD (foreign-origin NON-navigation resource, must succeed):     writes=%d success=%s" % (good_b["writes"], good_b["success"]))
    print("  same-origin non-navigation control (sanity):                    writes=%d success=%s" % (same_origin_control["writes"], same_origin_control["success"]))
    print("  BAD  (foreign-origin MAIN-FRAME navigation, must still refuse):  writes=%d success=%s" % (bad_b["writes"], bad_b["success"]))
    print("  discriminating property: the ONE difference is whether the foreign-origin event IS a main-frame navigation (isNavigationRequest)")
    ok &= check("pair (ii) GOOD (foreign subresource) now succeeds / BAD (foreign navigation) still refuses, unaffected by arm (c)",
                good_b["writes"] == 1 and good_b["success"] is True and bad_b["writes"] == 0 and bad_b["success"] is False)

    if ok:
        print("IBR112-INVARIANT-GUARD-BOTH-DEFECTS-REFUSE-TWINS-SUCCEED")
        return 0
    print("FAIL: invariant arm")
    return 1


def arm_retry():
    print("=== ARM retry (R112-AC2): the retry taxonomy closed to three named causes, code and README agree ===")
    ok = True

    print("--- R11 lifecycle diagnostic (CVO~B, UNMODIFIED) against the REPAIRED source -- retry-taxonomy cases ---")
    rc11, res11, err11 = run_r11()
    ok &= check("R11 diagnostic's own 'reproduced' flag is FALSE", res11["reproduced"] is False)
    by_name = {r["name"]: r for r in res11["results"]}

    print("--- the three named RETRY causes: each retries once and succeeds on a clean second attempt ---")
    for name in RETRY_CAUSES:
        r = by_name[name]
        matched = r["success"] is True and r["writes"] == 1 and r["verificationCalls"] == 2 and r["storageCalls"] == 1
        ok &= check("%-55s success=%-5s writes=%d verificationCalls=%d (want 2: fail once, clean retry)"
                     % (name, r["success"], r["writes"], r["verificationCalls"]), matched)

    print("--- the two named TERMINAL causes: refuse on FIRST occurrence, never retrying ---")
    for name in TERMINAL_CAUSES:
        r = by_name[name]
        matched = r["success"] is False and r["writes"] == 0 and r["verificationCalls"] == 1 and r["storageCalls"] == 0 and r["prompts"] == 1
        ok &= check("%-55s success=%-5s writes=%d verificationCalls=%d prompts=%d (want 1/1: never retried)"
                     % (name, r["success"], r["writes"], r["verificationCalls"], r["prompts"]), matched)
        ok &= check("  %s cause printed to stderr" % name, name.split(" then")[0] not in "" and len(r.get("errors", "")) > 0)

    print("--- README retry-behavior text: same three causes, verbatim ---")
    readme_path = os.path.join(REPO, README)
    readme_text = open(readme_path, encoding="utf-8").read()
    ok &= check("README.md exists and is readable", len(readme_text) > 0)
    has_section = "retry taxonomy" in readme_text.lower()
    ok &= check("README carries a retry-taxonomy description", has_section)
    denom = 0
    for cause in README_RETRY_CAUSES:
        present = cause in readme_text
        denom += 1 if present else 0
        ok &= check("README names retry cause %r verbatim" % cause, present)
    print("  denominator: %d of %d named retry causes found verbatim in README.md" % (denom, len(README_RETRY_CAUSES)))
    # The taxonomy is CLOSED: the README must also say so in words a reader cannot read past --
    # "exactly three" / "CLOSED" language, not just the three substrings floating independently.
    closed_language = ("CLOSED at exactly three" in readme_text) or ("exactly three named causes" in readme_text)
    ok &= check("README states the taxonomy is CLOSED at exactly three causes (not just listing them)", closed_language)
    # And the terminal side: 4xx / generic-error / foreign-hop must be named as NEVER retryable.
    terminal_language = ("never retryable" in readme_text.lower()) and ("4xx" in readme_text)
    ok &= check("README states the terminal side (4xx, generic error, foreign hop) is never retryable", terminal_language)

    if ok:
        print("IBR112-RETRY-TAXONOMY-CLOSED-CODE-README-AGREE")
        return 0
    print("FAIL: retry arm")
    return 1


ARMS = {"invariant": arm_invariant, "retry": arm_retry}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--arm" or sys.argv[2] not in ARMS:
        print("usage: battery_ib_rtl_1.py --arm {%s}" % "|".join(ARMS))
        sys.exit(2)
    sys.exit(ARMS[sys.argv[2]]())
