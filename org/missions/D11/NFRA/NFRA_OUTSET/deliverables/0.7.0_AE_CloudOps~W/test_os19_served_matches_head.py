#!/usr/bin/env python3
"""NFRA_OUTSET.TO-OS-s-19 battery (O19-AC1): the SERVED bytes match the graded commit's.

Run at both required file grains (path per the face AMENDED @cb43d05200, remedy (c) on row
NFRA_OUTSET-S18 -- this file cannot be committed under `.tools/tests/` by this seat, because a
`<paths>` block grants only a `0.9.0_WK_*` serial and `.tools/tests/**` is lane TOOL_BATTERIES):
  python org/missions/D11/NFRA/NFRA_OUTSET/deliverables/0.7.0_AE_CloudOps~W/test_os19_served_matches_head.py
  python -m pytest -q org/missions/D11/NFRA/NFRA_OUTSET/deliverables/0.7.0_AE_CloudOps~W/test_os19_served_matches_head.py

WHY A CONTENT DIFF AND NOT A VINTAGE. CLAUDE.md Rule 22a's CODE trap: deployed bytes are diffed
against the BUILD INPUT, never by filename, and running-bytes-older-than-built passes every other
rung. `head-object` is read here for the vintage and the ETag, but the VERDICT rests on a sha256 of
the actual downloaded object against `git show HEAD:<path>` -- because a timestamp says when
something was written and says nothing about what.

⛔ EVERY TOKEN IN A PRESENCE/ABSENCE CENSUS NEEDS ITS OWN POSITIVE CONTROL -- A CENSUS OF FOUR
TOKENS IS FOUR DETECTORS, NOT ONE (NFRA_OUTSET-W1-S27). Row `S14` measured the cost: `W1-S25` cited
`rerun_recipe` and `tool_invocation` as evidence the served producer lacked this project's work, and
both are ZERO AT HEAD TOO, so their zeros measured that row's own spelling rather than the world. So
ARM D classifies every token before counting it: a token absent from HEAD is INERT and is REFUSED as
evidence rather than silently contributing a meaningless zero. `rerun_recipe` is carried in the
census ON PURPOSE, as a sealed control, and the arm asserts it is classified INERT.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-19). 2026-09-09.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path


def _repo_root() -> Path:
    """DERIVED, never counted -- the same lesson NFRA_OUTSET-S19 records for the OS-s-18 battery:
    a hardcoded `parents[N]` is the one line that cannot survive its own relocation, and it fails
    as a WRONG ROOT with every derived path missing rather than as an obvious move error."""
    here = Path(__file__).resolve()
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(here.parent),
                             capture_output=True, text=True, timeout=30)
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip()).resolve()
    except Exception:                                                       # noqa: BLE001
        pass
    for cand in here.parents:
        if (cand / ".owned-paths.yaml").is_file() and (cand / "CLAUDE.md").is_file():
            return cand
    raise RuntimeError("cannot derive the workspace root from %s -- refusing to guess" % here)


ROOT = _repo_root()
REPO_PATH = "infra/aws/ec2/estate-report-runner/estate_report_runner.py"
REGION = "us-east-1"
BUCKET = "opal-estate-report"
KEY = "code/estate_report_runner.py"

# ARM D's census. Each entry is (token, why it should discriminate). The battery does NOT trust this
# list: it computes each token's HEAD count first and refuses any token that is absent there.
CENSUS_TOKENS = [
    ("_outset_read", "the OS-s-10 consumer function itself"),
    ("OUTSET_ANSWER_STATE_TO_STATUS", "the seam's answer-state mapping"),
    ("ESTATE_OUTSET_SEAM_PREFIX", "the seam source the consumer reads"),
    ("_outset_trace", "OS-s-11's seam-fed re-run recipe"),
    ("render_trace", "OS-s-11's traceability renderer"),
    # SEALED CONTROL, carried deliberately: row S14 measured this at ZERO on BOTH sides, so it
    # discriminates nothing. ARM D must classify it INERT and exclude it, not count its zero.
    ("rerun_recipe", "SEALED INERT CONTROL -- S14 measured 0 at HEAD and 0 served"),
]
# The positive control for "same program, older vintage" rather than "a different file entirely".
SAME_PROGRAM_TOKEN = "_stratum("

RESULTS = []
NOT_EVALUATED = []


def _record(arm, ok, detail):
    RESULTS.append((arm, bool(ok), str(detail).replace("\n", " ")[:400]))


def _skip(arm, reason):
    NOT_EVALUATED.append((arm, str(reason).replace("\n", " ")[:300]))


def _head_bytes() -> bytes:
    out = subprocess.run(["git", "show", "HEAD:" + REPO_PATH], cwd=str(ROOT),
                         capture_output=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("git show HEAD:%s rc=%d" % (REPO_PATH, out.returncode))
    if not out.stdout:
        # Never let a mangled ref read as a clean empty (CLAUDE.md: never 2>/dev/null a git show).
        raise RuntimeError("git show returned ZERO bytes -- refusing to treat that as an answer")
    return out.stdout


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def arm_a_vintage(s3):
    """head-object: the vintage and the ETag. READ, never the verdict."""
    h = s3.head_object(Bucket=BUCKET, Key=KEY)
    head = _head_bytes()
    etag = h["ETag"].strip('"')
    md5 = hashlib.md5(head).hexdigest()
    ok = h["ContentLength"] == len(head) and etag == md5
    _record("A-head-object-vintage-and-etag", ok,
            "served ContentLength=%d vs HEAD %d | ETag=%s vs HEAD md5=%s | LastModified=%s | "
            "VersionId=%s"
            % (h["ContentLength"], len(head), etag, md5,
               h["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"), h.get("VersionId")))
    return h


def arm_b_content(s3):
    """THE VERDICT ARM. A sha256 of the DOWNLOADED OBJECT against git show HEAD:<path>."""
    served = s3.get_object(Bucket=BUCKET, Key=KEY)["Body"].read()
    head = _head_bytes()
    ok = _sha(served) == _sha(head)
    _record("B-CONTENT-diff-served-vs-HEAD", ok,
            "served sha256=%s (%d B) | HEAD sha256=%s (%d B) | identical=%s"
            % (_sha(served)[:16], len(served), _sha(head)[:16], len(head), ok))
    return served, head


def arm_c_negative_control(served: bytes, head: bytes):
    """A comparison that cannot fail is not a comparison. Mutate ONE byte of a COPY and prove the
    same comparator reports a mismatch -- otherwise ARM B's pass is unattributable."""
    if not served:
        _skip("C-NEGATIVE-CONTROL-comparator-can-fail", "needs ARM B's download")
        return
    mutated = served[:100] + bytes([served[100] ^ 0x01]) + served[101:]
    same_len = len(mutated) == len(served)
    detected = _sha(mutated) != _sha(head)
    _record("C-NEGATIVE-CONTROL-comparator-can-fail", detected and same_len,
            "flipped ONE bit at offset 100, length unchanged (%s); comparator reports mismatch=%s "
            "-- so ARM B's match is a measurement and not a constant" % (same_len, detected))


def arm_d_token_census(served: bytes, head: bytes):
    """The census, with a POSITIVE CONTROL PER TOKEN. A token absent from HEAD is INERT: its zero
    in the served bytes measures the speller, not the world (S14 / W1-S27)."""
    if not served or not head:
        _skip("D-token-census-each-token-its-own-control", "needs ARM B's bytes")
        return
    st, ht = served.decode("utf-8", "replace"), head.decode("utf-8", "replace")
    live, inert = [], []
    for tok, why in CENSUS_TOKENS:
        h_n = len(re.findall(re.escape(tok), ht))
        s_n = len(re.findall(re.escape(tok), st))
        (live if h_n > 0 else inert).append((tok, h_n, s_n, why))
    # Every LIVE token must now agree with the served bytes, because served IS head.
    disagreeing = [(t, h, s) for t, h, s, _ in live if h != s]
    inert_names = [t for t, _, _, _ in inert]
    ok = (len(live) >= 4 and not disagreeing and inert_names == ["rerun_recipe"])
    _record("D-token-census-each-token-its-own-control", ok,
            "%d LIVE token(s) (non-zero at HEAD, so their counts carry information): %s | "
            "%d INERT token(s) REFUSED as evidence: %s | disagreeing served-vs-HEAD: %s"
            % (len(live), "; ".join("%s H=%d S=%d" % (t, h, s) for t, h, s, _ in live),
               len(inert), inert_names or "none", disagreeing or "none"))


def arm_e_same_program(served: bytes, head: bytes):
    """The positive control that separates 'same program, newer vintage' from 'a different file'."""
    if not served or not head:
        _skip("E-same-program-positive-control", "needs ARM B's bytes")
        return
    st, ht = served.decode("utf-8", "replace"), head.decode("utf-8", "replace")
    h_n = len(re.findall(re.escape(SAME_PROGRAM_TOKEN), ht))
    s_n = len(re.findall(re.escape(SAME_PROGRAM_TOKEN), st))
    _record("E-same-program-positive-control", h_n > 0 and s_n == h_n,
            "%r HEAD=%d SERVED=%d -- non-zero on both sides is what makes this the SAME program "
            "rather than an unrelated file, and equal counts are what make it the same VINTAGE"
            % (SAME_PROGRAM_TOKEN, h_n, s_n))


def arm_f_worktree_is_head():
    """The bytes uploaded were git show HEAD:<path>. A worktree hash on an autocrlf box hashes the
    CHECKOUT, not the record -- so the claim 'the worktree is what landed' is asserted only if the
    two are measured equal."""
    head = _head_bytes()
    wt = (ROOT / REPO_PATH).read_bytes()
    ok = _sha(wt) == _sha(head)
    _record("F-worktree-equals-HEAD-no-crlf-drift", ok,
            "worktree sha256=%s (%d B, CRLF=%d) | HEAD sha256=%s (%d B, CRLF=%d)"
            % (_sha(wt)[:16], len(wt), wt.count(b"\r\n"),
               _sha(head)[:16], len(head), head.count(b"\r\n")))


def main():
    print("=" * 92)
    print("NFRA_OUTSET.TO-OS-s-19  O19-AC1 -- do the SERVED bytes match the graded commit's?")
    print("  s3://%s/%s   vs   git show HEAD:%s" % (BUCKET, KEY, REPO_PATH))
    print("=" * 92)
    try:
        import boto3
    except Exception as e:                                                  # noqa: BLE001
        print("BLOCKED: boto3 unavailable (%s)." % e)
        return 2
    s3 = boto3.client("s3", region_name=REGION)
    try:
        arm_a_vintage(s3)
        served, head = arm_b_content(s3)
    except Exception as e:                                                  # noqa: BLE001
        _record("B-CONTENT-diff-served-vs-HEAD", False,
                "%s: %s" % (type(e).__name__, str(e)[:200]))
        served, head = b"", b""
    arm_c_negative_control(served, head)
    arm_d_token_census(served, head)
    arm_e_same_program(served, head)
    arm_f_worktree_is_head()

    print("")
    passed = sum(1 for _, ok, _ in RESULTS if ok)
    total = len(RESULTS)
    for arm, ok, detail in RESULTS:
        print("  [%s] %-46s %s" % ("PASS" if ok else "FAIL", arm, detail))
    for arm, reason in NOT_EVALUATED:
        print("  [NOT-EVALUATED] %-36s %s" % (arm, reason))
    print("")
    print("  DENOMINATOR: %d of %d evaluated arm(s) PASSED; %d NOT-EVALUATED (never a pass)."
          % (passed, total, len(NOT_EVALUATED)))
    print("")
    if passed == total and total > 0:
        print("SERVED MATCHES HEAD")
        return 0
    print("SERVED DOES NOT MATCH HEAD: %d arm(s) failed" % (total - passed))
    return 1


def test_os19_served_matches_head():
    rc = main()
    failures = [(a, d) for a, ok, d in RESULTS if not ok]
    assert not failures, "OS-s-19 arms failed: %s" % failures
    assert rc == 0


if __name__ == "__main__":
    raise SystemExit(main())
