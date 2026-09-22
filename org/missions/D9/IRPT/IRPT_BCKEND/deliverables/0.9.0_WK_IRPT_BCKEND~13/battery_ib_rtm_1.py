"""IB-rtm-1 battery -- the capture tool, FIFTH repair: typed error classification (C-S179) and
truthful cleanup reporting (C-S180).

Arms: classify | metadata. Run from any cwd inside the worktree.

`classify` (R113-AC1): re-derives the CURRENT COMMITTED blob of capture-session.cjs via
`git rev-parse HEAD:<path>` (never a raw working-tree read, per row W13-S3's CRLF-grain lesson),
then runs 3.0.0_SA_CVO~B's round-12 diagnostic (IRPT_BCKEND_R12_CAPTURE_FAILURE_DIAGNOSTIC.cjs),
UNMODIFIED, against that blob and confirms all seven cases: the timeout-text-confusable case
(C-S179) and the untruthful-cleanup case (C-S180) now behave correctly; the actual-timeout
positive still recovers; the HTTP 404 control stays terminal. Then re-runs the round-11,
round-10, round-9 and round-8 diagnostics, UNMODIFIED, against the SAME blob and compares them
to this round's own pre-repair baseline (captured at arm (c), before any source edit,
IB-rtm-1_baseline_r{11,10,9,8}_*.json) -- byte-identical for R10, R9, R8; R11 differs in ONE
case's error-message TEXT only (an added "(error.name=...)" annotation on an already-terminal
case), never in any of its externally-visible fields (success, writes, exitCode, verificationCalls,
prompts, storageCalls) -- see NOTE below. Then prints this worker's own harness_ib_rtm_1.cjs's two
single-difference pairs (arm (d)(i), (d)(ii)).

NOTE on arm (a)'s implementation and row W13-S6: a literal `error.name === 'TimeoutError'`-ONLY
classification correctly closes C-S179's counterexample but was MEASURED to regress two
long-standing reference diagnostics' own "actual timeout" positive controls (R11's "same-origin
timeout then clean" case and R12's "actual timeout positive control"), because every upstream
CVO diagnostic's mock throws a plain Error() for a simulated timeout and never sets `.name`
(unlike real Playwright). Arm (a) itself names a SECOND path -- "the tool's own deadline firing"
-- implemented here as an EXACT-STRING match (`isOwnDeadlineMessage`, capture-session.cjs) against
the ONE deterministic message this tool's own configured GOTO_TIMEOUT_MS produces; this is neither
a regular expression nor a substring search over free text (C-S179's actual defect shape), and it
closes both C-S179's counterexample AND avoids the regression. Filed as row IRPT_BCKEND-W13-S6,
left to 3.0.0_SA_CVO~B's adjudication, not self-graduated.

`metadata` (R113-AC2, widened by IB-rto-1/R115-AC1): reads C-S174's corrected
controls.mutant.observed text (IB-rtk-1's proof instance) and confirms it names the
CRLF/checkout-grain value and the git-object sha256, with no "typo"/"transcription error"
language; reads C-S187's corrected result.md artifact row (IB-rtl-1's proof instance) and
confirms it is re-pinned to the post-publish HEAD blob/commit and that the "no real S3 action"
exclusion is scoped to the pass it actually applies to (never blanket-claiming the sixth-pass
publish, which DID perform a real S3 put-object/get-object, never happened).

IB-rto-1 (C-S196) widening: this chain's own round-13/14 C-S174 metadata fix itself carried a
TRANSPOSED CRLF hash value and a MISATTRIBUTED LF hash (crediting a worktree-mode diagnostic read
for producing the git-object/LF value -- backwards; a worktree read on this CRLF-checkout box
produces the CRLF value, never the LF value). Never again compares stored text against a
hardcoded constant copied from the proof: `recompute_lf_value()` and `recompute_crlf_value()`
independently re-derive BOTH values from `capture-session.cjs`'s ACTUAL bytes at the historical
commit the citation is about (`HISTORICAL_COMMIT`), fresh, EVERY time this arm runs -- the LF/
git-object value via `git cat-file -p`, cross-checked against `git show` (both must agree); the
CRLF/checkout-grain value via an ACTUAL raw checkout-index read on this box (`git read-tree` +
`git checkout-index` into a throwaway scratch work-tree via a redirected GIT_WORK_TREE/
GIT_INDEX_FILE -- this REPO's own index and working tree are never touched), never a hardcoded
string and never a simulated substitution. The arm then FAILS if the stored proof text disagrees
with either freshly-recomputed value, FAILS if the known-wrong transposed substring
(`WRONG_TRANSPOSED_SUBSTRING`) is found ANYWHERE in this worker's own deliverables directory
(enumerated, denominator printed), and FAILS if the stored text still carries the specific wrong
misattribution phrasing this cell corrected.

Everything is exercised under stubs / VM mocks / static reads: no browser, network, credential,
host action or real file write. ASCII only.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
SRC_DIR = "infra/aws/ec2/investor-reporting-export"
CAP = SRC_DIR + "/capture-session.cjs"
README = SRC_DIR + "/README.md"
R12_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R12_CAPTURE_FAILURE_DIAGNOSTIC.cjs"
R11_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R11_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs"
R10_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R10_CAPTURE_LIFECYCLE_DIAGNOSTIC.cjs"
R9_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R9_CAPTURE_REDIRECT_DIAGNOSTIC.cjs"
R8_DIAG = "org/tier1_exec/3.0.0_SA_CVO/deliverables/IRPT_BCKEND_R8_CAPTURE_DIAGNOSTIC.cjs"
HARNESS = os.path.join(HERE, "harness_ib_rtm_1.cjs")

BASELINE_R11 = os.path.join(HERE, "IB-rtm-1_baseline_r11_lifecycle_diagnostic.json")
BASELINE_R10 = os.path.join(HERE, "IB-rtm-1_baseline_r10_lifecycle_diagnostic.json")
BASELINE_R9 = os.path.join(HERE, "IB-rtm-1_baseline_r9_redirect_diagnostic.json")
BASELINE_R8 = os.path.join(HERE, "IB-rtm-1_baseline_r8_diagnostic.json")

IB_RTK_1_PROOF = os.path.join(HERE, "IRPT_BCKEND.TO-IB-rtk-1.the-capture-tool-complete-lifecycle-observer-and-sticky-refusal.proof_of_spec.json")
IB_RTL_1_PROOF = os.path.join(HERE, "IRPT_BCKEND.TO-IB-rtl-1.the-capture-tool-invariant-guard-at-the-write-boundary.proof_of_spec.json")
IB_RTL_1_RESULT = os.path.join(HERE, "the-capture-tool-invariant-guard-at-the-write-boundary.result.md")

# IB-rto-1 (C-S196): the commit at which the IB-rtk-1 fourth-pass repair introduced the
# capture-session.cjs bytes C-S174's citation is about -- NEVER HEAD (the file has moved on
# since). Recomputation always targets THIS commit's blob, never a hardcoded hash VALUE.
HISTORICAL_COMMIT = "0d0c8cdc4d"

# The exact wrong (two-hex-character-transposed) substring this chain's own C-S174 fix wrote
# into the CRLF value. Built by concatenation, never as one contiguous literal in this file's own
# source text, so this detector's OWN presence never itself trips the zero-occurrences check it
# implements below. A DETECTOR for the defect class, never a correctness comparison target -- the
# correct value is never hardcoded anywhere in this file; it is recomputed fresh every run by
# recompute_crlf_value()/recompute_lf_value().
WRONG_TRANSPOSED_SUBSTRING = "03f" + "bb20"


def run_node(path, timeout=60, arg=None):
    argv = ["node", path] + ([arg] if arg else [])
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


def recompute_lf_value(commit=HISTORICAL_COMMIT, rel_path=CAP):
    """IB-rto-1 (R115-AC1) run-time recomputation, LF/git-object side. Reads the blob TWICE by
    two different git plumbing commands (never a raw fs read, never a hardcoded value) and
    requires them to agree byte-for-byte before trusting either. Returns (sha256_hex, raw_bytes)."""
    p1 = subprocess.run(["git", "-C", REPO, "cat-file", "-p", "%s:%s" % (commit, rel_path)], capture_output=True)
    if p1.returncode != 0:
        raise RuntimeError("git cat-file -p failed for %s:%s -- %s" % (commit, rel_path, p1.stderr.decode("utf-8", "replace")))
    p2 = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (commit, rel_path)], capture_output=True)
    if p2.returncode != 0:
        raise RuntimeError("git show failed for %s:%s -- %s" % (commit, rel_path, p2.stderr.decode("utf-8", "replace")))
    if p1.stdout != p2.stdout:
        raise RuntimeError("git cat-file -p and git show DISAGREE on blob bytes for %s:%s -- instrument fault" % (commit, rel_path))
    return hashlib.sha256(p1.stdout).hexdigest(), p1.stdout


def recompute_crlf_value(lf_bytes, commit=HISTORICAL_COMMIT, rel_path=CAP):
    """IB-rto-1 (R115-AC1) run-time recomputation, CRLF/checkout-grain side. An ACTUAL raw
    working-tree read on THIS box (never a hardcoded value, never a canned \\n->\\r\\n
    substitution passed off as a read): `git read-tree` + `git checkout-index` populate a
    throwaway scratch work-tree via a redirected GIT_WORK_TREE/GIT_INDEX_FILE, applying this
    box's real core.autocrlf filter on actual checkout -- this REPO's own index and working tree
    are never touched. Returns sha256_hex."""
    if b"\r" in lf_bytes:
        raise RuntimeError("blob at %s:%s already carries CR bytes -- this instrument assumes pure-LF git storage" % (commit, rel_path))
    with tempfile.TemporaryDirectory() as td:
        env = dict(os.environ)
        env["GIT_DIR"] = os.path.join(REPO, ".git")
        env["GIT_WORK_TREE"] = td
        env["GIT_INDEX_FILE"] = os.path.join(td, ".ib-rto-1-scratch-index")
        p1 = subprocess.run(["git", "read-tree", commit], env=env, cwd=REPO, capture_output=True, text=True)
        if p1.returncode != 0:
            raise RuntimeError("git read-tree %s failed: %s" % (commit, p1.stderr))
        p2 = subprocess.run(["git", "checkout-index", "-f", "--", rel_path], env=env, cwd=REPO, capture_output=True, text=True)
        if p2.returncode != 0:
            raise RuntimeError("git checkout-index for %s failed: %s" % (rel_path, p2.stderr))
        checked_out = os.path.join(td, rel_path.replace("/", os.sep))
        with open(checked_out, "rb") as f:
            raw = f.read()
    return hashlib.sha256(raw).hexdigest()


def scan_deliverables_for_substring(substring):
    """Enumerate EVERY file in this worker's own deliverables directory (HERE) and return
    (hit_count, files_scanned, hit_paths) for a literal substring search -- the denominator IS
    the file count, printed by the caller. Skips this battery script's own bytes (which must be
    free of transposed 8-char-run 'ARMED string' matches too; verified separately by construction
    -- WRONG_TRANSPOSED_SUBSTRING is never a contiguous literal in this file's own source)."""
    hit_paths = []
    files_scanned = 0
    for root, dirs, files in os.walk(HERE):
        # __pycache__ is a gitignored build byproduct of running/compiling THIS script, never a
        # deliverable -- a stale .pyc from an earlier (pre-fix) version of this same file would
        # otherwise self-trigger a false residual hit that has nothing to do with the correction.
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in files:
            path = os.path.join(root, name)
            files_scanned += 1
            try:
                with open(path, "rb") as f:
                    data = f.read()
            except OSError:
                continue
            if substring.encode("ascii") in data:
                hit_paths.append(os.path.relpath(path, HERE))
    return len(hit_paths), files_scanned, hit_paths


def run_diag(diag_rel_path, blob):
    rc, out, err = run_node(os.path.join(REPO, diag_rel_path), arg=blob)
    try:
        res = json.loads(out)
    except Exception:
        print("  RAW OUTPUT (json parse failed): %s" % out[:2000])
        raise
    return rc, res, err


def arm_classify():
    print("=== ARM classify (R113-AC1): typed error classification (C-S179) + truthful cleanup (C-S180) ===")
    ok = True

    blob = git_blob(CAP)
    print("current committed capture-session.cjs blob (git rev-parse HEAD:<path>): %s" % blob)

    print("--- R12 diagnostic (CVO~B, UNMODIFIED) against the CURRENT COMMITTED blob -- all 7 cases ---")
    rc12, res12, err12 = run_diag(R12_DIAG, blob)
    print("  blob echoed by diagnostic: %s  sourceSha256: %s" % (res12["blob"], res12["sourceSha256"][:16]))
    ok &= check("R12 diagnostic ran (blob passed matches)", res12["blob"] == blob)

    retries = {r["name"]: r for r in res12["retries"]}
    cleanups = {c["name"]: c for c in res12["cleanups"]}

    r_a = retries["non-timeout certificate error, ordinary URL text"]
    print("  case A 'non-timeout certificate error, ordinary URL text': writes=%d success=%s exitCode=%s" % (r_a["writes"], r_a["success"], r_a["exitCode"]))
    ok &= check("case A terminal (writes=0, success=False)", r_a["writes"] == 0 and r_a["success"] is False)

    r_b = retries["same non-timeout certificate error, timeout substring in URL text"]
    print("  case B (C-S179 counterexample) 'timeout substring in URL text': writes=%d success=%s verificationCalls=%d" % (r_b["writes"], r_b["success"], r_b["verificationCalls"]))
    ok &= check("case B (C-S179) now TERMINAL (writes=0, success=False, verificationCalls=1) -- closes C-S179",
                r_b["writes"] == 0 and r_b["success"] is False and r_b["verificationCalls"] == 1)

    r_c = retries["actual timeout positive control"]
    print("  case C 'actual timeout positive control': writes=%d success=%s verificationCalls=%d" % (r_c["writes"], r_c["success"], r_c["verificationCalls"]))
    ok &= check("case C actual-timeout positive STILL RECOVERS (writes=1, success=True, verificationCalls=2)",
                r_c["writes"] == 1 and r_c["success"] is True and r_c["verificationCalls"] == 2)

    r_d = retries["HTTP404 terminal control"]
    print("  case D 'HTTP404 terminal control': writes=%d success=%s" % (r_d["writes"], r_d["success"]))
    ok &= check("case D HTTP 404 stays terminal", r_d["writes"] == 0 and r_d["success"] is False)

    c_clean = cleanups["clean rename positive control"]
    print("  cleanup 1 'clean rename positive control': writes=%d unlinks=%d success=%s" % (c_clean["writes"], c_clean["unlinks"], c_clean["success"]))
    ok &= check("cleanup 1 clean positive control unaffected", c_clean["writes"] == 1 and c_clean["unlinks"] == 0 and c_clean["success"] is True)

    c_del_ok = cleanups["latched rename, deletion succeeds"]
    print("  cleanup 2 'latched rename, deletion succeeds': deleted=%s diskFinal=%s exitCode=%s" % (c_del_ok["deleted"], c_del_ok["diskFinal"], c_del_ok["exitCode"]))
    ok &= check("cleanup 2 (deletion succeeds) unaffected: deleted=True, diskFinal=False, exitCode=1 (old message)",
                c_del_ok["deleted"] is True and c_del_ok["diskFinal"] is False and c_del_ok["exitCode"] == 1
                and "was deleted" in c_del_ok["errors"])

    c_del_fail = cleanups["same latched rename, deletion fails EPERM"]
    print("  cleanup 3 (C-S180 counterexample) 'deletion fails EPERM': deleted=%s diskFinal=%s exitCode=%s" % (c_del_fail["deleted"], c_del_fail["diskFinal"], c_del_fail["exitCode"]))
    print("    errors: %s" % c_del_fail["errors"].strip())
    ok &= check("cleanup 3 (C-S180) now TRUTHFUL: deleted=False, diskFinal=True, exitCode=4, message names removal failure not deletion -- closes C-S180",
                c_del_fail["deleted"] is False and c_del_fail["diskFinal"] is True and c_del_fail["exitCode"] == 4
                and "could NOT be removed" in c_del_fail["errors"] and "was deleted" not in c_del_fail["errors"])

    print("--- R11/R10/R9/R8 diagnostics (CVO, UNMODIFIED) against the SAME blob -- no regression ---")
    have_baseline = all(os.path.isfile(p) for p in (BASELINE_R11, BASELINE_R10, BASELINE_R9, BASELINE_R8))
    ok &= check("baseline files present (r11, r10, r9, r8, captured at arm (c) before any edit)", have_baseline)

    rc11, res11, err11 = run_diag(R11_DIAG, blob)
    base11 = load(BASELINE_R11)
    verdict_fields = ("success", "writes", "exitCode", "verificationCalls", "prompts", "storageCalls")
    n_verdict_same = 0
    n_byte_identical = 0
    for a, b in zip(res11["results"], base11["results"]):
        verdict_same = all(a.get(k) == b.get(k) for k in verdict_fields)
        n_verdict_same += 1 if verdict_same else 0
        n_byte_identical += 1 if a == b else 0
    print("  R11: %d of %d cases externally-visible-verdict UNCHANGED; %d of %d byte-identical (incl. error text)"
          % (n_verdict_same, len(base11["results"]), n_byte_identical, len(base11["results"])))
    ok &= check("R11: ALL cases' externally-visible verdict unchanged (success/writes/exitCode/verificationCalls/prompts/storageCalls) -- zero behavioral regression",
                n_verdict_same == len(base11["results"]))
    if n_byte_identical != len(base11["results"]):
        print("  NOTE: the byte-level diff is COSMETIC ONLY -- an added '(error.name=...)' annotation")
        print("        on an already-terminal case's error message, per module docstring NOTE.")

    for diag_path, baseline_path, label in ((R10_DIAG, BASELINE_R10, "R10"), (R9_DIAG, BASELINE_R9, "R9"), (R8_DIAG, BASELINE_R8, "R8")):
        rc, res, err = run_diag(diag_path, blob)
        base = load(baseline_path)
        same = res["results"] == base["results"]
        print("  %s: results array BYTE-IDENTICAL to pre-repair baseline: %s" % (label, same))
        ok &= check("%s: zero drift (byte-identical results array)" % label, same)

    print("--- this worker's own single-difference pairs (harness_ib_rtm_1.cjs) ---")
    rc_h, out_h, err_h = run_node(HARNESS, arg=blob)
    pairs = json.loads(out_h)
    print("  pair (i) typed classification -- discriminating property: %s" % pairs["pairI"]["discriminatingProperty"])
    gi = pairs["pairI"]["good"]
    bi = pairs["pairI"]["bad"]
    print("    GOOD (genuine TimeoutError):  writes=%d success=%s exitCode=%s verificationCalls=%d" % (gi["writes"], gi["success"], gi["exitCode"], gi["verificationCalls"]))
    print("    BAD  (message-text twin):     writes=%d success=%s exitCode=%s verificationCalls=%d" % (bi["writes"], bi["success"], bi["exitCode"], bi["verificationCalls"]))
    ok &= check("pair (i): GOOD retries+recovers, BAD (same substring, wrong TYPE) terminally refuses", pairs["pairI"]["pairIOk"] is True)

    print("  pair (ii) truthful cleanup -- discriminating property: %s" % pairs["pairII"]["discriminatingProperty"])
    gii = pairs["pairII"]["good"]
    bii = pairs["pairII"]["bad"]
    print("    GOOD (unlink succeeds): deleted=%s diskFinal=%s exitCode=%s" % (gii["deleted"], gii["diskFinal"], gii["exitCode"]))
    print("    BAD  (unlink throws):   deleted=%s diskFinal=%s exitCode=%s" % (bii["deleted"], bii["diskFinal"], bii["exitCode"]))
    ok &= check("pair (ii): GOOD deletes+old message, BAD retains file+truthful message+distinct exit code", pairs["pairII"]["pairIIOk"] is True)

    if ok:
        print("IBR113-TYPED-CLASSIFICATION-BOTH-DEFECTS-REFUSE-TWINS-SUCCEED")
        return 0
    print("FAIL: classify arm")
    return 1


def arm_metadata():
    print("=== ARM metadata (R113-AC2 + IB-rto-1/R115-AC1): C-S174 + C-S187 corrected metadata, recomputed not copied ===")
    ok = True

    print("--- IB-rto-1 (R115-AC1) run-time recomputation control: FRESH, from actual bytes, at commit %s ---" % HISTORICAL_COMMIT)
    print("  cmd: git -C <repo> cat-file -p %s:%s | sha256sum" % (HISTORICAL_COMMIT, CAP))
    print("  cmd: git -C <repo> show %s:%s | sha256sum   (cross-check, must agree)" % (HISTORICAL_COMMIT, CAP))
    fresh_lf_hash, lf_bytes = recompute_lf_value()
    print("  freshly recomputed LF/git-object sha256:       %s" % fresh_lf_hash)
    print("  cmd: git read-tree %s ; git checkout-index -- %s   (into a throwaway scratch work-tree, this REPO's own index untouched)" % (HISTORICAL_COMMIT, CAP))
    fresh_crlf_hash = recompute_crlf_value(lf_bytes)
    print("  freshly recomputed CRLF/checkout-grain sha256: %s" % fresh_crlf_hash)
    print("  byte lengths: LF=%d CRLF=%d (delta=%d, one CR inserted per LF newline converted)" % (len(lf_bytes), len(lf_bytes) + lf_bytes.count(b"\n"), lf_bytes.count(b"\n")))
    ok &= check("LF and CRLF recomputed values DIFFER (two different byte sequences of the same logical file, not a duplicate)", fresh_lf_hash != fresh_crlf_hash)

    print("--- C-S174: controls.mutant.observed (IB-rtk-1's proof instance) -- checked against the FRESH recomputation above, never a hardcoded constant ---")
    rtk1 = load(IB_RTK_1_PROOF)
    observed = rtk1["controls"]["mutant"]["observed"]
    print("  observed text (first 200 chars): %s..." % observed[:200])
    # IB-rtn-1 (C-S194 -> arm (g)'s own C-S174 metadata correction): widened from a [:12] PREFIX
    # comparison to the FULL 64-hex-char hash string -- a 12-char prefix collision is not
    # cryptographically implausible enough to certify "this exact hash is present"; the full
    # string is the only comparison that actually does.
    # IB-rto-1 (C-S196): the comparison target is the value JUST recomputed above, fresh, this
    # run -- never a module-level constant copied from a prior reading of the proof text (that
    # exact pattern is how the transposition and misattribution survived undetected).
    has_crlf = fresh_crlf_hash in observed
    has_blob = fresh_lf_hash in observed
    # Never AFFIRMS either value is a typo/transcription-error -- a NEGATION of that claim
    # ("is NOT a transcription error", "neither is a typo") is exactly the required correction,
    # so this checks for the AFFIRMATIVE phrasing only, not bare substring presence.
    lower = observed.lower()
    affirms_typo = ("packet-only typo" in lower) or ("is a transcription error" in lower) or \
        ("was a transcription error" in lower) or ("an arbitrary typo" in lower and "not an arbitrary typo" not in lower)
    ok &= check("names the FRESHLY-RECOMPUTED CRLF hash %s as a value present in the text" % fresh_crlf_hash, has_crlf)
    ok &= check("names the FRESHLY-RECOMPUTED LF/git-object hash %s as a value present in the text" % fresh_lf_hash, has_blob)
    ok &= check("never AFFIRMS either value is a 'typo' or 'transcription error' (a negation of that claim is the required correction)", not affirms_typo)
    names_crlf_correctly = "CRLF" in observed and "checkout-grain" in observed
    names_blob_correctly = "git-object" in observed or "git blob" in observed.lower()
    ok &= check("text names the CRLF value as the CRLF/checkout-grain value", names_crlf_correctly)
    ok &= check("text names the corrected value as the git-object sha256", names_blob_correctly)

    print("--- IB-rto-1 (R115-AC1) arm (b): zero residual occurrences of the wrong transposed substring ---")
    hit_count, files_scanned, hit_paths = scan_deliverables_for_substring(WRONG_TRANSPOSED_SUBSTRING)
    print("  scanned %d files under this worker's own deliverables directory; %d hit(s)" % (files_scanned, hit_count))
    if hit_paths:
        for hp in hit_paths:
            print("    RESIDUAL HIT: %s" % hp)
    ok &= check("zero remaining occurrences of the wrong transposed substring, denominator=%d files scanned" % files_scanned, hit_count == 0)

    print("--- IB-rto-1 (R115-AC1) arm (c): LF/git-object attribution corrected -- names git cat-file -p / git show, never a worktree diagnostic ---")
    # The SPECIFIC wrong causal claim this cell corrected: crediting a worktree-mode diagnostic
    # read's "computed value on the repaired bytes" directly with "the git-object sha256 -- the
    # git BLOB's own LF bytes", with no git cat-file/git show mention at all. Checked for absence
    # by exact phrase (the literal wrong continuation), not by a keyword that could false-positive
    # on legitimate CRLF-side prose that also mentions "worktree" and "bytes".
    wrong_attribution_phrase = "and the git-object sha256 -- the git BLOB's own LF bytes)"
    ok &= check("observed text no longer carries the specific wrong LF-attribution phrasing", wrong_attribution_phrase not in observed)
    names_correct_lf_source = ("git cat-file" in observed) or ("git show" in observed)
    ok &= check("observed text names git cat-file -p / git show as an LF/git-object value's actual source", names_correct_lf_source)

    print("--- C-S187: result.md artifact row + declared_exclusions scoping (IB-rtl-1's proof instance) ---")
    rtl1 = load(IB_RTL_1_PROOF)
    result_row = None
    for a in rtl1["artifacts_produced"]:
        if a["path_or_key"].endswith("the-capture-tool-invariant-guard-at-the-write-boundary.result.md"):
            result_row = a
            break
    ok &= check("result.md artifact row found in IB-rtl-1's proof instance", result_row is not None)

    true_blob = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD:" + os.path.relpath(IB_RTL_1_RESULT, REPO).replace("\\", "/")],
                                capture_output=True, text=True).stdout.strip()
    print("  true HEAD blob for result.md: %s" % true_blob)
    print("  proof instance's pinned commit_or_etag: %s" % (result_row["commit_or_etag"] if result_row else "MISSING"))
    ok &= check("proof instance's commit_or_etag now equals the true HEAD blob (re-pinned to post-publish state)",
                result_row is not None and result_row["commit_or_etag"] == true_blob)

    addendum_commit = "d8bac06b89"
    ok &= check("deploy_evidence cites the addendum commit (%s) that landed the sixth-pass publish" % addendum_commit,
                result_row is not None and addendum_commit in result_row.get("deploy_evidence", ""))

    print("--- declared_exclusions: 'no real S3 action' scoped to the pass it actually applies to ---")
    exclusions_text = json.dumps(rtl1.get("declared_exclusions", []))
    blanket_s3_claim = ("any real host/SSM/S3 action" in exclusions_text) or ("or any real host/SSM/S3 action" in exclusions_text)
    ok &= check("no exclusion still blanket-claims 'no real S3 action' across the whole order (arm (f)'s sixth pass DID publish for real)",
                not blanket_s3_claim)
    scoped_language = ("S3 action" not in exclusions_text) or ("fifth-pass" in exclusions_text) or ("code-only" in exclusions_text)
    ok &= check("remaining exclusions are scoped to on-host verification / no-live-browser only, not to S3 broadly", scoped_language)

    if ok:
        print("IBR113-METADATA-C174-C187-CORRECTED")
        print("IBR115-C174-RECOMPUTED-NO-TRANSPOSITION-NO-MISATTRIBUTION")
        return 0
    print("FAIL: metadata arm")
    return 1


ARMS = {"classify": arm_classify, "metadata": arm_metadata}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "--arm" or sys.argv[2] not in ARMS:
        print("usage: battery_ib_rtm_1.py --arm {%s}" % "|".join(ARMS))
        sys.exit(2)
    sys.exit(ARMS[sys.argv[2]]())
