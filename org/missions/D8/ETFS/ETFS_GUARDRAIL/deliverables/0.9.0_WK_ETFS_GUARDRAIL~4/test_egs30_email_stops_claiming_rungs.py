"""ETFS_GUARDRAIL.TO-EG-s-30 -- S30-AC1. THE EMAIL STOPS CLAIMING RUNGS THAT NEVER RAN.

SIX ARMS. Every number prints beside its denominator, and the token prints only when
all six hold. NO SEND AND NO ORCHESTRATOR INVOKE: every module this battery loads is
imported with `boto3.client` replaced by a stub that RAISES on any call, so no SES,
EC2 or SSM call is reachable through the code under test; the only AWS this file
touches is arm (f)'s READS through the `.tools/aws` shim.

TWO DEFECTS, KEPT APART THROUGHOUT, because they have different remedies and
different evidence: (1) a POSITIVE FALSE CLAIM -- the message asserted the repair
ladder was exhausted on a run that never entered it; (2) a MISSING DISCLOSURE --
nothing said the condition was FORCED. Fixing only (2) would leave (1) standing.
"""
import ast
import base64
import datetime
import hashlib
import importlib
import io
import json
import os
import subprocess
import sys
import tempfile
from unittest import mock

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "..", "..", "..", "..", "..", ".."))
REL = "infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py"
LAMBDA_DIR = os.path.join(REPO_ROOT, "infra", "aws", "lambda",
                          "etfs-reports-orchestrator")
DELIVERABLES = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(DELIVERABLES, "fixtures")
# The .cmd plane, not the bash shim: CreateProcess cannot exec a shebang script, and
# CLAUDE.md ships both halves of this shim ("both or neither"). Absolute, because a
# relative name is not resolved against cwd by CreateProcess.
AWS = os.path.join(REPO_ROOT, ".tools", "aws.cmd")

# ---------------------------------------------------------------------------
# THE PRE-FIX BYTES, AND WHY THEY ARE PINNED AS A CONSTANT WITH A VINTAGE.
# Arm (a) must reproduce both defects "against the deployed bytes". This battery
# runs AFTER the apply, so the function's served bytes are by then the FIXED ones
# and the pre-fix state is no longer live-readable. The pre-fix blob is therefore
# pinned by commit, and the fact that it WAS the served member is pinned as the
# sha256 measured from the function's OWN presigned Code.Location at 13:16Z, before
# any apply. Arm (f) closes the loop from the other side: it re-reads the live
# member and confirms the NEW bytes are served and that this same pre-fix blob is a
# negative control that does NOT match.
PRE_FIX_COMMIT = "a6cbb6f3c3"
PRE_FIX_SERVED_MEMBER_SHA256 = (
    "3266c6cced4940f01314652e6d3cf41bcc2f021fdba8d276a2cfe445dc3ebb3c")
PRE_FIX_SERVED_CODE_SHA256 = "5qPTUpaxx+NUvTN6hmXdNfe2pT2xwkHF9Y3Q3fFJVSw="
PRE_FIX_SERVED_READ_AT = "2026-09-10T13:16Z (lambda:GetFunction -> presigned Code.Location)"
CM_ENTRY = os.path.join(REPO_ROOT, "org", "critical_paths", "change_management",
                        "20260910T1730Z_etfs-guardrail-eg-s-30-email-run-shape-disclosure"
                        "_deploy_completion.md")
SES_BEFORE = os.path.join(FIXTURES, "EG-s-30_ses_send_stats_BEFORE.json")

# ---------------------------------------------------------------------------
# ONE INPUT SET, USED BY EVERY ARM, so a difference between two printed messages is
# a difference in the RUN SHAPE and never in the rows.
MONTH = "2026-08"
UNRESOLVED = [
    {"date": "2026-08-04", "partner": "cottonwood", "class": "C",
     "reason": "no ownership rows for the date"},
]
TO_HEADER = "andrew@opalinvest.com"


def _verdict(forced, ladder_ran):
    """coverage_verdict.json's `forcing` block, EXACTLY the shape
    render_month_end._forcing_record emits at disclosure_version 2. The two axes are
    set independently here so a caller can build the coupled pair OR either
    off-diagonal."""
    spec = "cottonwood:2026-08-04" if forced else ""
    return {
        "month": MONTH, "verdict": "REFUSE",
        "forcing": {
            "forced": forced, "mechanism": "--fixture-remove" if forced else "none",
            "fixture_remove_spec": spec,
            "fixture_remove": {"cottonwood": ["2026-08-04"]} if forced else {},
            "removed_slice_count": 1 if forced else 0,
            "ladder_ran": ladder_ran,
            "ladder_skip_mechanism": "none" if ladder_ran else "--no-ladder",
            "rung3_stop_and_ask_reachable": ladder_ran,
            "coverage_egress_ask_possible": ladder_ran,
            "skip_note": "(see render_month_end._forcing_record)",
            "run_shape": "%s and %s" % ("FORCED" if forced else "NOT FORCED",
                                        "LADDER RAN" if ladder_ran else "LADDER SKIPPED"),
            "run_id": "5b1f0c9d84a24e7fa0d3e6712c8b4419",
            "run_id_source": "uuid4 minted by this run; printed to stdout as 'RUN-ID: <id>'",
            "disclosure_version": "2",
        },
    }


# The orchestrator COUPLES the two axes (EG-s-27: --no-ladder rides the forcing), so
# these two are the pair a real driven run and its organic twin actually produce.
FORCED_VERDICT = _verdict(True, False)
ORGANIC_VERDICT = _verdict(False, True)


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _git_show(ref_path):
    r = subprocess.run(["git", "show", ref_path], capture_output=True, cwd=REPO_ROOT)
    # NEVER 2>/dev/null a git show -- a mangled ref returns clean-empty and reads as
    # an honest absence. rc and length are both asserted.
    assert r.returncode == 0 and r.stdout, (
        "git show %r -> rc=%d, %d bytes, stderr=%r"
        % (ref_path, r.returncode, len(r.stdout), r.stderr[:300]))
    return r.stdout


def _load(source_bytes, tag):
    """Import a copy of the module from raw bytes with EVERY boto3 client stubbed to
    RAISE. Structurally send-free: no AWS call is reachable from the code under test."""
    d = tempfile.mkdtemp(prefix="egs30_%s_" % tag)
    p = os.path.join(d, "lambda_function.py")
    io.open(p, "wb").write(source_bytes)
    os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
    os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub")

    class _Raiser(object):
        def __init__(self, service):
            self._s = service

        def __getattr__(self, name):
            def _call(**kw):
                raise AssertionError(
                    "BATTERY VIOLATION: %s.%s reached from the code under test" % (self._s, name))
            return _call

    sys.path.insert(0, d)
    try:
        with mock.patch("boto3.client", lambda service, **kw: _Raiser(service)):
            if "lambda_function" in sys.modules:
                del sys.modules["lambda_function"]
            mod = importlib.import_module("lambda_function")
            mod.__egs30_tag = tag
            del sys.modules["lambda_function"]
            return mod
    finally:
        sys.path.remove(d)


def _msg(mod, verdict, pre_fix):
    """Build the terminal message. The pre-fix signature has no `verdict` parameter,
    which is itself the shape of defect (2): the builder could not see the record."""
    if pre_fix:
        m = mod._build_terminal_email(MONTH, UNRESOLVED, None, TO_HEADER)
    else:
        m = mod._build_terminal_email(MONTH, UNRESOLVED, None, TO_HEADER, verdict)
    return m["Subject"], m.get_payload()[0].get_payload()


def _dump(tag, subject, body):
    print("-" * 78)
    print("[%s] SUBJECT: %s" % (tag, subject))
    print("-" * 78)
    print(body)
    print("-" * 78)


# ---------------------------------------------------------------------------
# THE DISCLOSURE TOKEN SET AND ITS POSITIVE CONTROL.
# The token set is what a reader would have to see, ANYWHERE in the message, to
# learn the condition was manufactured. The control set is fields that DO exist in
# the same message, censused by the SAME instrument over the SAME text -- so a zero
# on the first set is a measured absence and not a broken counter.
DISCLOSURE_TOKENS = ["forced", "forcing", "--fixture-remove", "--no-ladder", "driven",
                     "test run", "manufactured", "run id", "run_id", "run shape",
                     "not a real", "skipped"]
CONTROL_TOKENS = ["unresolved", "cottonwood", "2026-08-04", "Opal Capital",
                  "coverage ladder"]


def _census(subject, body, tokens):
    text = (subject + "\n" + body).lower()
    hits = {t: text.count(t.lower()) for t in tokens}
    return hits, sum(1 for t in tokens if hits[t]), sum(hits.values())


def arm_a(pre):
    print("\n=== ARM (a) BOTH DEFECTS REPRODUCE FIRST, SEPARATELY, ON THE PRE-FIX "
          "SERVED BYTES ===")
    blob = _git_show("%s:%s" % (PRE_FIX_COMMIT, REL))
    print("GRAIN: git show %s:%s -> %d bytes sha256 %s" % (PRE_FIX_COMMIT, REL,
                                                           len(blob), _sha(blob)))
    print("       served zip member sha256 at %s = %s" % (PRE_FIX_SERVED_READ_AT,
                                                          PRE_FIX_SERVED_MEMBER_SHA256))
    same = _sha(blob) == PRE_FIX_SERVED_MEMBER_SHA256
    print("       BLOB IS THE BYTES THAT WERE SERVED: %s" % same)
    if not same:
        return False, "pre-fix blob is not the served member"
    subject, body = _msg(pre, FORCED_VERDICT, pre_fix=True)
    print("\nTHE MESSAGE THE DEPLOYED BYTES BUILD FOR A LADDER-SKIPPED RUN, WHOLE:")
    _dump("PRE-FIX / ladder SKIPPED, input FORCED", subject, body)

    print("FINDING 1 of 2 -- A POSITIVE FALSE CLAIM (the artifact asserts a repair "
          "attempt that did not happen).")
    claim = "after every rung ran (probe, re-run the producer, re-check)"
    body_hits = body.count(claim)
    subj_hits = subject.count("after remediation")
    print("  body   occurrences of %r: %d  (denominator: 1 message built from a run "
          "on which remediate_month was NEVER called and ZERO rungs ran)" % (claim, body_hits))
    print("  subject occurrences of 'after remediation': %d  (denominator: 1 subject)"
          % subj_hits)
    d1 = body_hits == 1 and subj_hits == 1
    print("  FINDING 1 PRESENT: %s" % d1)

    print("\nFINDING 2 of 2 -- A MISSING DISCLOSURE (nothing tells a reader the "
          "condition was manufactured). SEPARATE MEASUREMENT, SEPARATE EVIDENCE.")
    hits, n_tok, n_occ = _census(subject, body, DISCLOSURE_TOKENS)
    print("  forcing-disclosure token census over subject+body, case-insensitive:")
    print("    %d of %d tokens hit; %d total occurrences" % (n_tok, len(DISCLOSURE_TOKENS), n_occ))
    print("    per token: %s" % json.dumps(hits))
    chits, cn_tok, cn_occ = _census(subject, body, CONTROL_TOKENS)
    print("  POSITIVE CONTROL -- the SAME instrument over the SAME text, on fields "
          "that DO exist in this message:")
    print("    %d of %d tokens hit; %d total occurrences" % (cn_tok, len(CONTROL_TOKENS), cn_occ))
    print("    per token: %s" % json.dumps(chits))
    d2 = n_tok == 0 and cn_tok == len(CONTROL_TOKENS)
    print("  FINDING 2 PRESENT (zero disclosure, non-zero control): %s" % d2)
    ok = d1 and d2
    print("ARM (a): %s -- both defects reproduce, measured apart" % ("HOLDS" if ok else "FAILS"))
    return ok, None


def arm_b(new):
    print("\n=== ARM (b) THE FALSE CLAIM IS GONE ON THE SKIPPED BRANCH -- AND THE "
          "ARM SAYS WHAT REPLACED IT ===")
    subject, body = _msg(new, FORCED_VERDICT, pre_fix=False)
    _dump("FIXED / ladder SKIPPED, input FORCED", subject, body)
    gone = body.count("after every rung ran") == 0 and "after remediation" not in subject
    print("occurrences of 'after every rung ran' in the body: %d of 1 message (was 1)"
          % body.count("after every rung ran"))
    print("occurrences of 'after remediation' in the subject: %d of 1 subject (was 1)"
          % subject.count("after remediation"))
    lines = body.split("\n")
    claim = [ln for ln in lines if ln.startswith("The ETF ownership coverage ladder")]
    print("\nTHE NEW WORDING, VERBATIM (%d claim line(s) of %d body lines):" % (len(claim), len(lines)))
    for ln in claim:
        print("  >> %s" % ln)
    print("  >> SUBJECT: %s" % subject)
    # NOT A SILENT DELETION: the replacement must STATE what happened. Four
    # independent facts, each named in the text rather than implied by its absence.
    said = {
        "names the mechanism (--no-ladder)": "--no-ladder" in body,
        "names the function that was not called (remediate_month)":
            "remediate_month was not called" in body,
        "states the rung count that ran (ZERO)": "ZERO of probe / re-run the producer / re-check ran" in body,
        "distinguishes first-classified from post-repair":
            "unresolved as first classified, not unresolved after repair" in body,
    }
    for k, v in said.items():
        print("  REPLACEMENT %s: %s" % (k, v))
    stated = all(said.values()) and len(claim) == 1
    ok = gone and stated
    print("ARM (b): %s -- claim removed AND replaced by a statement of what happened "
          "(%d of %d replacement facts present)"
          % ("HOLDS" if ok else "FAILS", sum(1 for v in said.values() if v), len(said)))
    return ok, None


def arm_c(pre, new):
    print("\n=== ARM (c) THE ORGANIC BRANCH -- THE INVARIANCE ARM ===")
    old_subject, old_body = _msg(pre, None, pre_fix=True)
    new_subject, new_body = _msg(new, ORGANIC_VERDICT, pre_fix=False)
    _dump("PRE-FIX / organic", old_subject, old_body)
    _dump("FIXED / organic (nothing forced, full ladder ran)", new_subject, new_body)

    subj_same = old_subject.encode("utf-8") == new_subject.encode("utf-8")
    body_same = old_body.encode("utf-8") == new_body.encode("utf-8")
    print("SUBJECT byte-identity (compared as bytes): %s" % subj_same)
    print("BODY LITERAL whole-message byte-identity: %s" % body_same)

    old_lines, new_lines = old_body.split("\n"), new_body.split("\n")
    tail = new_lines[len(new_lines) - len(old_lines):]
    preserved = tail == old_lines
    added = len(new_lines) - len(old_lines)
    removed = sum(1 for ln in old_lines if ln not in new_lines)
    altered = 0 if preserved else -1
    print("REPORTING INVARIANCE: every pre-fix body line present, in order, "
          "byte-identical: %s" % preserved)
    print("  pre-fix body lines: %d   fixed body lines: %d   added: %d   removed: %d"
          "   altered: %s" % (len(old_lines), len(new_lines), added, removed,
                              altered if altered >= 0 else "UNKNOWN (order broken)"))
    print("  THE DELTA, WHOLE (every line the fixed body adds):")
    for i, ln in enumerate(new_lines[:added]):
        print("    +[%d] %s" % (i, ln))
    print("  THE PRE-FIX CLAIM SENTENCE, byte-identical on this branch: %s"
          % (old_lines[0] in new_lines))
    print("    >> %s" % old_lines[0])

    print("\n  ARM (c) DEVIATION -- READ THIS BEFORE GRADING, ROW ETFS_GUARDRAIL-W4-S13.")
    print("  The face's arm (c) as WRITTEN asks for whole-message byte-identity on the")
    print("  organic branch. The face's own BOUND and arm (d) require the disclosure to")
    print("  carry an EXPLICIT VALUE ON BOTH BRANCHES ('a field present only on the")
    print("  forced run is not a disclosure'). Under the orchestrator's coupling")
    print("  (EG-s-27: --no-ladder rides the forcing) the UNFORCED run IS the organic")
    print("  run, so the two requirements name the same message and are JOINTLY")
    print("  UNSATISFIABLE: any always-present field is a line the pre-fix bytes did not")
    print("  emit. The BOUND was taken as governing and arm (d) is the arm the face")
    print("  itself calls 'the arm that carries the outcome'. Arm (c) is therefore")
    print("  executed as the STRONGEST FORM THAT SURVIVES: subject byte-identical, and")
    print("  every pre-fix body line preserved byte-identical and in order, with ZERO")
    print("  removed and ZERO altered, the sole delta being the additive disclosure")
    print("  block. What arm (c) exists to stop -- the fix breaking the real case -- is")
    print("  fully measured; whole-message byte-identity is NOT claimed and reads FALSE")
    print("  above. Judgment on the trade is the CVO's, not this seat's.")
    ok = subj_same and preserved and removed == 0
    print("ARM (c): %s (as executed: reporting invariance; LITERAL whole-body "
          "byte-identity = %s)" % ("HOLDS" if ok else "FAILS", body_same))
    return ok, None


def arm_d(new):
    print("\n=== ARM (d) THE DISCLOSURE ON BOTH BRANCHES WITH AN EXPLICIT VALUE -- "
          "THE DIFFERENCE CONTROL, AND THE ARM THAT CARRIES THE OUTCOME ===")
    print("SAME INPUTS ON BOTH SIDES: month=%s, %d unresolved row(s) %r, ask=None, "
          "to=%s. THE ONLY THING THAT MOVES IS THE FORCING." % (MONTH, len(UNRESOLVED),
                                                                [u["date"] for u in UNRESOLVED],
                                                                TO_HEADER))
    f_subject, f_body = _msg(new, FORCED_VERDICT, pre_fix=False)
    u_subject, u_body = _msg(new, ORGANIC_VERDICT, pre_fix=False)
    _dump("ENGAGED  -- forcing ON", f_subject, f_body)
    _dump("DISENGAGED -- the same run with the forcing OFF", u_subject, u_body)

    labels = ["  forced:", "  ladder ran:", "  run id:", "  read from:"]
    f_present = [lb for lb in labels if lb in f_body]
    u_present = [lb for lb in labels if lb in u_body]
    print("SAME FIELD, BOTH BRANCHES: engaged %d of %d labels, disengaged %d of %d "
          "labels; identical set: %s" % (len(f_present), len(labels), len(u_present),
                                         len(labels), f_present == u_present == labels))

    def _val(body, label):
        for ln in body.split("\n"):
            if ln.startswith(label):
                return ln[len(label):].strip()
        return None

    print("VALUES, side by side:")
    moved = 0
    for lb in labels:
        a, b = _val(f_body, lb), _val(u_body, lb)
        differs = a != b
        moved += 1 if differs else 0
        print("  %-13s ENGAGED    : %s" % (lb.strip(), a))
        print("  %-13s DISENGAGED : %s" % (lb.strip(), b))
        print("  %-13s MOVES      : %s" % (lb.strip(), differs))
    run_id = FORCED_VERDICT["forcing"]["run_id"]
    spec = FORCED_VERDICT["forcing"]["fixture_remove_spec"]
    names_forcing = spec in f_body and "--fixture-remove" in f_body
    names_run_id = run_id in f_body and run_id in u_body
    not_forced_explicit = ("forced:     NO" in u_body
                           and "no --fixture-remove" in u_body)
    print("ENGAGED names the forcing (%r) and its mechanism: %s" % (spec, names_forcing))
    print("ENGAGED names its run id (%s): %s  | DISENGAGED carries the same run id "
          "field: %s" % (run_id, run_id in f_body, run_id in u_body))
    print("DISENGAGED carries the SAME field with its NOT-FORCED value (never absent, "
          "never blank): %s" % not_forced_explicit)
    print("SUBJECT, engaged   : %s" % f_subject)
    print("SUBJECT, disengaged: %s" % u_subject)
    ok = (f_present == u_present == labels and names_forcing and names_run_id
          and not_forced_explicit and moved >= 2)
    print("ARM (d): %s -- %d of %d fields move between engaged and disengaged; the "
          "field exists on both" % ("HOLDS" if ok else "FAILS", moved, len(labels)))
    return ok, None


def arm_e(new):
    print("\n=== ARM (e) A PERSON CAN TELL, AND THE ARM SAYS HOW ===")
    f_subject, f_body = _msg(new, FORCED_VERDICT, pre_fix=False)
    o_subject, o_body = _msg(new, ORGANIC_VERDICT, pre_fix=False)
    f_lines, o_lines = f_body.split("\n"), o_body.split("\n")
    table_ix = [i for i, ln in enumerate(f_lines) if ln.startswith("date       | partner")]
    print("PLACEMENT, MEASURED (a disclosure buried below the per-date table is not one):")
    print("  disclosure headline line index: %d of %d body lines" % (0, len(f_lines)))
    print("  character offset of the headline in the body: %d" % f_body.index("RUN SHAPE:"))
    print("  per-date table header line index: %s of %d" % (table_ix, len(f_lines)))
    print("  lines between the headline and the table: %d" % (table_ix[0] - 1 if table_ix else -1))
    print("  the headline is ABOVE the table: %s" % (bool(table_ix) and table_ix[0] > 0))
    print("  the subject carries the marker too: %s" % f_subject.startswith(
        "[DRIVEN TEST -- NOT A REAL ALERT]"))
    print("\nWHAT A READER SEES, IN ONE SENTENCE:")
    print("  The reader sees, in the subject line and again as the very first line of")
    print("  the body -- before the count, before the per-date table, and inside the")
    print("  first two lines every mail client previews -- the words '[DRIVEN TEST --")
    print("  NOT A REAL ALERT]' and 'RUN SHAPE: DRIVEN TEST RUN -- THIS ALERT WAS")
    print("  MANUFACTURED ON PURPOSE AND IS NOT A REAL COVERAGE EMERGENCY.', where a")
    print("  real emergency instead reads 'RUN SHAPE: ORGANIC -- nothing was forced and")
    print("  the full repair ladder ran. This is a real coverage failure.'")
    print("\nTHE LINE THEY WOULD READ, QUOTED, ON EACH BRANCH:")
    print("  DRIVEN : %s" % f_lines[0])
    print("  ORGANIC: %s" % o_lines[0])
    print("  DRIVEN  SUBJECT: %s" % f_subject)
    print("  ORGANIC SUBJECT: %s" % o_subject)
    ok = (f_lines[0].startswith("RUN SHAPE: DRIVEN TEST RUN")
          and o_lines[0].startswith("RUN SHAPE: ORGANIC")
          and f_body.index("RUN SHAPE:") == 0
          and bool(table_ix) and table_ix[0] > 0
          and f_subject.startswith("[DRIVEN TEST -- NOT A REAL ALERT]")
          and not o_subject.startswith("["))
    print("ARM (e): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, None


def _aws(args):
    r = subprocess.run([AWS] + args, capture_output=True, text=True, cwd=REPO_ROOT)
    return r.returncode, r.stdout.replace("\r", ""), r.stderr.replace("\r", "")


def arm_f():
    print("\n=== ARM (f) THE DEPLOY IS REAL AND NOTHING ELSE FIRED ===")
    ok = True
    rc, out, err = _aws(["lambda", "get-function-configuration", "--function-name",
                         "etfs-reports-orchestrator", "--region", "us-east-1",
                         "--query", "[CodeSha256,LastModified,CodeSize]",
                         "--output", "text"])
    assert rc == 0, (rc, err[:400])
    served_sha, last_mod, code_size = out.strip().split("\t")
    print("READ 1 -- served CodeSha256 (lambda:GetFunctionConfiguration): %s "
          "(LastModified %s, CodeSize %s)" % (served_sha, last_mod, code_size))

    zip_path = os.path.join(REPO_ROOT, "infra", "aws", "terraform", "etfs-reports",
                            ".build", "etfs-reports-orchestrator.zip")
    built = io.open(zip_path, "rb").read()
    built_sha = base64.b64encode(hashlib.sha256(built).digest()).decode()
    print("READ 2 -- base64 sha256 of the zip Terraform BUILT (%s, %d B): %s"
          % (os.path.relpath(zip_path, REPO_ROOT), len(built), built_sha))

    plan_txt = io.open(os.path.join(DELIVERABLES,
                                    "EG-s-30_preapply_plan_transcript.txt"),
                       encoding="utf-8").read()
    predicted = [ln.split("->")[-1].strip().strip('"')
                 for ln in plan_txt.split("\n") if "source_code_hash" in ln]
    print("READ 3 -- the value the REVIEWED plan PREDICTED: %r" % predicted)
    three = (served_sha == built_sha and predicted and predicted[0] == served_sha)
    print("THREE READS EQUAL: %s" % bool(three))
    ok = ok and bool(three)

    # GRAIN DEEPER THAN THE ZIP (Rule 22a): the build INPUT, not the filename.
    rc, loc, err = _aws(["lambda", "get-function", "--function-name",
                         "etfs-reports-orchestrator", "--region", "us-east-1",
                         "--query", "Code.Location", "--output", "text"])
    assert rc == 0, (rc, err[:400])
    import urllib.request
    with urllib.request.urlopen(loc.strip(), timeout=120) as fh:
        blob = fh.read()
    import zipfile
    zf = zipfile.ZipFile(io.BytesIO(blob))
    member = zf.read("lambda_function.py")
    head_blob = _git_show("HEAD:%s" % REL)
    print("SERVED zip member lambda_function.py: %d B sha256 %s"
          % (len(member), _sha(member)))
    print("git show HEAD:%s                    : %d B sha256 %s"
          % (REL, len(head_blob), _sha(head_blob)))
    member_ok = member == head_blob
    print("MEMBER BYTE-EQUAL TO THE COMMITTED BLOB: %s" % member_ok)
    ok = ok and member_ok

    pre_blob = _git_show("%s:%s" % (PRE_FIX_COMMIT, REL))
    neg = _sha(pre_blob) != _sha(member)
    print("NEGATIVE CONTROL -- the pre-fix blob %s is retrievable (%d B sha256 %s) "
          "and does NOT match: %s" % (PRE_FIX_COMMIT, len(pre_blob), _sha(pre_blob), neg))
    print("  (and its pre-apply served CodeSha256 was %s, which the served value above "
          "is not)" % PRE_FIX_SERVED_CODE_SHA256)
    ok = ok and neg and served_sha != PRE_FIX_SERVED_CODE_SHA256

    entry = io.open(CM_ENTRY, encoding="utf-8").read()
    opened = [ln for ln in entry.split("\n") if ln.startswith("**Date opened:**")]
    status = [ln for ln in entry.split("\n") if ln.startswith("**Status:**")]
    print("NEVER-2 ENTRY: %s" % os.path.relpath(CM_ENTRY, REPO_ROOT))
    print("  %s" % (opened[0] if opened else "(no opened line)"))
    print("  %s" % (status[0] if status else "(no status line)"))
    o_dt = datetime.datetime.fromisoformat(
        opened[0].split("**Date opened:**")[1].strip()).replace(tzinfo=None)
    a_dt = datetime.datetime.strptime(last_mod.split(".")[0], "%Y-%m-%dT%H:%M:%S")
    print("  OPENED %sZ  <  APPLY %sZ : %s" % (o_dt.isoformat(), a_dt.isoformat(),
                                               o_dt < a_dt))
    closed = "CLOSED" in (status[0] if status else "")
    print("  CLOSED before this grading read: %s" % closed)
    ok = ok and o_dt < a_dt and closed

    # 0 ORCHESTRATOR INVOKES, WITH A NON-ZERO POSITIVE CONTROL so the zero is a
    # measured absence and not a vacuous pass on an empty set.
    print("\nNOTHING ELSE FIRED -- 0 ORCHESTRATOR INVOKES, 0 SES SENDS, WITH "
          "DENOMINATORS AND A CONTROL.")
    now = datetime.datetime.now(datetime.timezone.utc)
    start = int((now - datetime.timedelta(hours=6)).timestamp() * 1000)
    end = int((now + datetime.timedelta(minutes=5)).timestamp() * 1000)
    rc, out, err = _aws(["logs", "filter-log-events", "--log-group-name",
                         "/aws/lambda/etfs-reports-orchestrator", "--region", "us-east-1",
                         "--start-time", str(start), "--end-time", str(end),
                         "--output", "json"])
    events = json.loads(out)["events"] if rc == 0 else None
    starts = [e for e in (events or []) if e["message"].startswith("START RequestId")]
    print("  logs:FilterLogEvents /aws/lambda/etfs-reports-orchestrator over the 6 h "
          "window %s -> %s (SPANS the apply at %sZ): %s events, %s START RequestId"
          % (datetime.datetime.utcfromtimestamp(start / 1000).isoformat(),
             datetime.datetime.utcfromtimestamp(end / 1000).isoformat(),
             a_dt.isoformat(), len(events or []), len(starts)))
    # POSITIVE CONTROL: the window containing EG-s-15's known driven run.
    c_start = int(datetime.datetime(2026, 9, 10, 1, 0,
                                    tzinfo=datetime.timezone.utc).timestamp() * 1000)
    c_end = int(datetime.datetime(2026, 9, 10, 1, 30,
                                  tzinfo=datetime.timezone.utc).timestamp() * 1000)
    rc2, out2, err2 = _aws(["logs", "filter-log-events", "--log-group-name",
                            "/aws/lambda/etfs-reports-orchestrator", "--region", "us-east-1",
                            "--start-time", str(c_start), "--end-time", str(c_end),
                            "--output", "json"])
    cev = json.loads(out2)["events"] if rc2 == 0 else []
    cstarts = [e for e in cev if e["message"].startswith("START RequestId")]
    print("  POSITIVE CONTROL 2026-09-10T01:00Z-01:30Z (EG-s-15's known driven run): "
          "%d events, %d START RequestId -- NON-ZERO, so the zero above discriminates"
          % (len(cev), len(cstarts)))
    invokes_ok = len(starts) == 0 and len(cstarts) > 0
    print("  0 ORCHESTRATOR INVOKES UNDER THIS ORDER: %s" % invokes_ok)
    ok = ok and invokes_ok

    # SECOND INSTRUMENT, DIFFERENT PLANE: SES's own account-wide send counters.
    before = json.load(io.open(SES_BEFORE, encoding="utf-8"))["SendDataPoints"]
    rc3, out3, err3 = _aws(["ses", "get-send-statistics", "--region", "us-east-1",
                            "--output", "json"])
    after = json.loads(out3)["SendDataPoints"] if rc3 == 0 else []
    b_tot = sum(x["DeliveryAttempts"] for x in before)
    a_tot = sum(x["DeliveryAttempts"] for x in after)
    b_max = max(x["Timestamp"] for x in before) if before else "(none)"
    a_max = max(x["Timestamp"] for x in after) if after else "(none)"
    print("  ses:GetSendStatistics, a DIFFERENT plane from the log read: BEFORE "
          "(captured %s) %d bucket(s), %d DeliveryAttempts, latest bucket %s"
          % ("2026-09-10T17:24Z", len(before), b_tot, b_max))
    print("    AFTER %d bucket(s), %d DeliveryAttempts, latest bucket %s"
          % (len(after), a_tot, a_max))
    print("    DELTA DeliveryAttempts across the whole order: %d" % (a_tot - b_tot))
    print("    HONEST LIMIT: this counter is ACCOUNT-WIDE and 15-minute-bucketed, so a "
          "non-zero delta would not by itself be mine; a ZERO delta bounds MY sends at 0.")
    ses_ok = (a_tot - b_tot) == 0
    print("  0 SES SENDS: %s" % ses_ok)
    ok = ok and ses_ok

    print("\n  DENOMINATOR OF WHAT WAS CHECKED: 2 planes (CloudWatch Logs for the "
          "function's own invocations; SES account send counters), 1 log group, 1 "
          "6 h window spanning the apply, 1 non-zero control window, 62 -> %d SES "
          "buckets. AWS CALLS MADE BY THIS ORDER, 6 KINDS, ALL READS: "
          "lambda:GetFunctionConfiguration, lambda:GetFunction, an HTTPS GET of the "
          "presigned Code.Location, logs:FilterLogEvents, ses:GetSendStatistics -- "
          "plus the ONE Terraform apply, which writes only the function's code."
          % len(after))
    print("ARM (f): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, None


def main():
    print("=" * 78)
    print("ETFS_GUARDRAIL.TO-EG-s-30 -- S30-AC1 BATTERY")
    print("repo root: %s" % REPO_ROOT)
    print("started:   %s" % datetime.datetime.now(datetime.timezone.utc).isoformat())
    print("=" * 78)
    pre = _load(_git_show("%s:%s" % (PRE_FIX_COMMIT, REL)), "prefix")
    new = _load(io.open(os.path.join(REPO_ROOT, REL), "rb").read(), "fixed")
    print("MODULES LOADED: pre-fix (%s) and fixed (worktree), both with every boto3 "
          "client stubbed to RAISE -- structurally send-free." % PRE_FIX_COMMIT)
    # A pre-fix signature that ALREADY took a verdict would mean the premise is wrong.
    pre_tree = ast.parse(_git_show("%s:%s" % (PRE_FIX_COMMIT, REL)).decode("utf-8"))
    pre_fn = [f for f in ast.walk(pre_tree) if isinstance(f, ast.FunctionDef)
              and f.name == "_build_terminal_email"]
    pre_args = [a.arg for a in pre_fn[0].args.args]
    print("PREMISE: pre-fix _build_terminal_email takes %d parameter(s) %r -- "
          "'verdict' among them: %s. The builder could not see the forcing record."
          % (len(pre_args), pre_args, "verdict" in pre_args))
    assert "verdict" not in pre_args

    results = []
    results.append(("a", arm_a(pre)[0]))
    if not results[0][1]:
        print("\nPREMISE WRONG: a defect arm (a) expects is already absent. STOPPING. "
              "File a row.")
        print("EGS30-PREMISE-WRONG")
        return 2
    results.append(("b", arm_b(new)[0]))
    results.append(("c", arm_c(pre, new)[0]))
    results.append(("d", arm_d(new)[0]))
    results.append(("e", arm_e(new)[0]))
    results.append(("f", arm_f()[0]))

    print("\n" + "=" * 78)
    for tag, held in results:
        print("ARM (%s): %s" % (tag, "HOLDS" if held else "FAILS"))
    held = sum(1 for _, h in results if h)
    print("arms: %d of %d HOLD" % (held, len(results)))
    print("v3.13 CONFORMANCE, STATED: 1 of 6 arms carries a DIFFERENCE control -- arm "
          "(d), the arm that carries the outcome. Arm (c) is an INVARIANCE proof, arm "
          "(a) is a paired census with a positive control, arms (b), (e) and (f) are "
          "single-state reads and censuses.")
    print("ARM (c) IS RECORDED AS EXECUTED IN A NARROWER FORM THAN WRITTEN -- see the "
          "deviation banner in arm (c) and row ETFS_GUARDRAIL-W4-S13.")
    if held == len(results):
        print("EGS30-EMAIL-TELLS-THE-TRUTH-ON-BOTH-BRANCHES")
        return 0
    print("TOKEN WITHHELD -- not every arm holds.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
