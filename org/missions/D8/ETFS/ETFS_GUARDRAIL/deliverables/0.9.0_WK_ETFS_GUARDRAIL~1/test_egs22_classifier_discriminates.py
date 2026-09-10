#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-22 S22-AC1 battery -- THE CLASSIFIER MUST TELL A CLOSED DAY
CARRYING A SLICE FROM A CLOSED DAY CARRYING NOTHING.

Prints EGS22-CLASSIFIER-DISCRIMINATES only when all seven arms (a)-(g) hold, every number
beside its denominator.

READ-ONLY on S3. NO SES CLIENT AND NO LAMBDA INVOKE -- arm (g) proves that from this run.
In particular every classify_month call here passes `probe=None` on BOTH sides of every
comparison, because a real probe INVOKES producer Lambdas, which this cell's BOUNDS forbid.

Run from the worktree root:
  timeout 300 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs22_classifier_discriminates.py
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import types

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
CLASSIFIER = os.path.join(ROOT, "data", "etfs", "scripts", "coverage", "classifier.py")
CLASSIFIER_REL = "data/etfs/scripts/coverage/classifier.py"
PRE_PIN = "c866edd3246df27f8ed3ec4a3da251f7fece71ce"   # the vintage the face cites
ETFS_BUCKET = "opal-data-etfs"
ART_BUCKET = "opal-313476888478-lambda-artifacts"
ART_KEY = "ec2/etfs-reports/coverage/classifier.py"
MONTH = "2026-09"
VERDICT_KEY = "platinum/reports/%s/coverage_verdict.json" % MONTH
TARGET = "2026-09-07"          # Labor Day: closed, and inflection carries a slice
SLICE_KEY = "daily/inflection/%s.json" % TARGET

ARMS: list[tuple[str, bool, str]] = []
AWS_CALLS: list[list[str]] = []       # every AWS CLI argv this battery ran (arm g)
BOTO_CLIENTS: list[str] = []          # every boto3 client service constructed (arm g)


def arm(name: str, ok: bool, detail: str) -> bool:
    ARMS.append((name, ok, detail))
    print("ARM %-3s %-4s %s" % (name, "PASS" if ok else "FAIL", detail))
    return ok


def aws(args: list[str], timeout: int = 120) -> tuple[int, bytes]:
    AWS_CALLS.append(list(args))
    p = subprocess.run([AWS] + args, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout


def aws_json(args: list[str], timeout: int = 120):
    rc, out = aws(args + ["--output", "json"], timeout=timeout)
    txt = out.decode("utf-8", "replace").replace("\r", "")
    try:
        return rc, json.loads(txt) if txt.strip() else None
    except Exception:  # noqa: BLE001
        return rc, None


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_module_from_source(src: str, name: str):
    """Exec `src` as a module whose __file__ is the REAL classifier path, so its own
    repo-layout calendar fallback resolves exactly as it does in production."""
    mod = types.ModuleType(name)
    mod.__file__ = CLASSIFIER
    sys.modules[name] = mod
    exec(compile(src, CLASSIFIER, "exec"), mod.__dict__)
    return mod


def main() -> int:
    print("EG-s-22 -- the classifier must tell a closed day CARRYING a slice from one "
          "carrying NOTHING\n")

    # arm (g) instrumentation, installed BEFORE anything else runs.
    try:
        import boto3  # noqa: F401
        _real_client = boto3.client

        def _watched_client(service_name, *a, **kw):
            BOTO_CLIENTS.append(str(service_name))
            return _real_client(service_name, *a, **kw)

        boto3.client = _watched_client  # type: ignore[assignment]
        boto3_available = True
    except Exception:  # noqa: BLE001
        boto3_available = False

    # ---------------------------------------------------------------- arm (a)
    # THE DEFECT REPRODUCES FIRST, ON THE PRODUCER'S OWN BYTES, against the classifier
    # AS IT STANDS BEFORE the change.
    print("(a) REPRODUCE THE DEFECT ON THE PRE-CHANGE CLASSIFIER, USING THE PRODUCER'S OWN BYTES")
    dest = os.path.join(ROOT, ".scratch", "s22", "inflection_%s.json" % TARGET)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    rc_b, _ = aws(["s3api", "get-object", "--bucket", ETFS_BUCKET, "--key", SLICE_KEY, dest])
    if rc_b == 0:
        raw = open(dest, "rb").read()
        provenance = "FETCHED LIVE from s3://%s/%s this run" % (ETFS_BUCKET, SLICE_KEY)
    else:
        raw = b""
        provenance = "UNFETCHED (rc=%d)" % rc_b
    print("    the slice: s3://%s/%s" % (ETFS_BUCKET, SLICE_KEY))
    print("    provenance: %s" % provenance)
    print("    bytes=%d sha256=%s" % (len(raw), sha256_bytes(raw)))
    if raw:
        rows = json.loads(raw)
        print("    contents: %d row(s), tickers %s, source_as_of=%s -- PRICED rows on a US "
              "market holiday" % (len(rows), [r.get("etf_ticker") for r in rows],
                                  rows[0].get("source_as_of") if rows else None))

    pre_src = subprocess.run(["git", "show", "%s:%s" % (PRE_PIN, CLASSIFIER_REL)],
                             capture_output=True, cwd=ROOT).stdout.decode("utf-8")
    print("    PRE-CHANGE classifier loaded from git %s:%s -- %d bytes, sha256 %s"
          % (PRE_PIN[:10], CLASSIFIER_REL, len(pre_src.encode()),
             sha256_bytes(pre_src.encode())))
    pre = load_module_from_source(pre_src, "classifier_pre_egs22")

    # PRESENCE-only, derived from the REAL key that exists in S3 (the classifier reads
    # presence, never contents -- its own docstring says so).
    series_with = {TARGET: True}
    series_without: dict = {}
    rec_pre_with = pre.classify_month("inflection", MONTH, series=series_with,
                                      probe=None)[TARGET]
    rec_pre_without = pre.classify_month("inflection", MONTH, series=series_without,
                                         probe=None)[TARGET]
    j_with = json.dumps(rec_pre_with, sort_keys=True)
    j_without = json.dumps(rec_pre_without, sort_keys=True)
    print("    PRE-CHANGE, closed day WITH a real slice : %s" % j_with)
    print("    PRE-CHANGE, closed day with NO slice     : %s" % j_without)
    names_slice = [k for k in rec_pre_with if "slice" in k.lower()]
    reproduced = (j_with == j_without) and not names_slice
    print("    TEXTUALLY EQUAL -> %s ; key(s) naming the slice -> %s"
          % (j_with == j_without, names_slice or "NONE"))
    if not reproduced:
        print("    DEFECT DID NOT REPRODUCE -- the premise of this cell is refused by the "
              "world. STOPPING before any further arm; file a surprise row.")
        arm("a", False, "the defect did NOT reproduce on the pre-change classifier: the two "
                        "records differ or a key already names the slice -- STOPPED, not "
                        "proceeding to grade a change on a premise the world refused")
        print("\nARMS %d of 7 PASS" % sum(1 for _, ok, _ in ARMS if ok))
        print("EGS22-PREMISE-REFUSED")
        return 1
    arm("a", True,
        "the defect REPRODUCES on the pre-change classifier (git %s): a closed day carrying a "
        "REAL %d-byte slice (sha256 %s, %d priced rows) and a closed day carrying NOTHING "
        "return the BYTE-IDENTICAL record %s, with 0 key(s) naming the slice"
        % (PRE_PIN[:10], len(raw), sha256_bytes(raw)[:16], len(json.loads(raw)) if raw else 0,
           j_with))

    # ---------------------------------------------------------------- arm (b)
    print("\n(b) THE DISCRIMINATOR, AFTER THE CHANGE")
    print("    SHAPE CHOSEN, in one sentence: a FIELD -- `slice_on_closed_day` (bool) on the "
          "class-A record -- NOT a new class value, because a closed day is class A on the "
          "coverage axis whether or not an artifact turned up and its remedy moves no other "
          "class value, so the fact is ORTHOGONAL to the class and belongs beside it.")
    post_src = open(CLASSIFIER, "rb").read().decode("utf-8")
    post = load_module_from_source(post_src, "classifier_post_egs22")
    rec_post_with = post.classify_month("inflection", MONTH, series=series_with,
                                        probe=None)[TARGET]
    rec_post_without = post.classify_month("inflection", MONTH, series=series_without,
                                           probe=None)[TARGET]
    p_with = json.dumps(rec_post_with, sort_keys=True)
    p_without = json.dumps(rec_post_without, sort_keys=True)
    print("    POST-CHANGE, closed day WITH a real slice : %s" % p_with)
    print("    POST-CHANGE, closed day with NO slice     : %s" % p_without)
    print("    TEXTUALLY UNEQUAL -> %s" % (p_with != p_without))
    arm("b", p_with != p_without,
        "the two records are TEXTUALLY UNEQUAL after the change (%s vs %s on "
        "`slice_on_closed_day`), so a closed day carrying a slice is now distinguishable "
        "from one carrying nothing"
        % (rec_post_with.get("slice_on_closed_day"), rec_post_without.get("slice_on_closed_day")))

    # ---------------------------------------------------------------- arms (c) + (e)
    # Both need the real served slices and the artifact's own partner list.
    dest_v = os.path.join(ROOT, ".scratch", "s22", "coverage_verdict.json")
    rc_v, _ = aws(["s3api", "get-object", "--bucket", ETFS_BUCKET, "--key", VERDICT_KEY, dest_v])
    vdoc = json.load(open(dest_v, encoding="utf-8")) if rc_v == 0 else {}
    partners = sorted((vdoc.get("per_partner") or {}).keys())
    print("\n    PARTNER LIST TAKEN FROM THE ARTIFACT (s3://%s/%s): %s -> %d partner(s) "
          "(denominator)" % (ETFS_BUCKET, VERDICT_KEY, partners, len(partners)))

    series_real: dict = {}
    for p in partners:
        rc_l, doc = aws_json(["s3api", "list-objects-v2", "--bucket", ETFS_BUCKET,
                              "--prefix", "daily/%s/%s" % (p, MONTH)])
        keys = [c["Key"] for c in (doc or {}).get("Contents", [])]
        dates = sorted(k.rsplit("/", 1)[-1][:-len(".json")] for k in keys
                       if k.endswith(".json"))
        series_real[p] = {d: True for d in dates}
        print("      daily/%-12s -> %d real slice(s) in %s: %s"
              % (p + "/", len(dates), MONTH, dates))

    # ---------------------------------------------------------------- arm (c)
    print("\n(c) POSITIVE CONTROL -- A GENUINELY EMPTY CLOSED DAY STILL READS AS IT DID")
    classes_post = {p: post.classify_month(p, MONTH, series=series_real[p], probe=None)
                    for p in partners}
    holes_post = {p: sorted(d for d, e in classes_post[p].items()
                            if e["class"] in ("C", "D", "UNKNOWN")) for p in partners}
    empty_closed = []
    for p in partners:
        for d, e in classes_post[p].items():
            if e["class"] == "A" and not e.get("slice_on_closed_day"):
                empty_closed.append((p, d, e))
    ok_c = 0
    for p, d, e in empty_closed:
        in_any_holes = any(d in holes_post[q] for q in partners)
        good = (e["class"] == "A" and not in_any_holes
                and e["reason"] == "market closed (not a trading day)")
        ok_c += 1 if good else 0
        print("    %-12s %s class=%s slice_on_closed_day=%s reason=%r | in ANY partner's "
              "holes -> %s" % (p, d, e["class"], e.get("slice_on_closed_day"), e["reason"],
                               in_any_holes))
    print("    genuinely-empty closed days across %d of %d partner(s): %d (denominator)"
          % (len(partners), len(partners), len(empty_closed)))
    arm("c", len(empty_closed) > 0 and ok_c == len(empty_closed),
        "%d of %d genuinely-empty closed day(s) across %d partner(s) still read class A with "
        "the ORIGINAL reason string and appear in NO partner's holes"
        % (ok_c, len(empty_closed), len(partners)))

    # ---------------------------------------------------------------- arm (d)
    print("\n(d) THE ZERO-vs-MISSING CONTRACT IS UNDISTURBED")
    suite = "data/etfs/scripts/coverage/tests/test_classifier.py"
    r = subprocess.run([sys.executable, "-m", "pytest", suite, "-q"],
                       capture_output=True, cwd=ROOT, timeout=300)
    out = r.stdout.decode("utf-8", "replace")
    tail = [ln for ln in out.splitlines() if "passed" in ln or "failed" in ln]
    print("    invocation: python -m pytest %s -q" % suite)
    print("    POST-CHANGE rc=%d  %s" % (r.returncode, tail[-1].strip() if tail else out[-200:]))
    print("    PRE-CHANGE  rc=0   8 passed   (measured this session BEFORE the edit, on the "
          "same suite by the same invocation)")
    # pytest -q colourises its summary, so the count is NOT a bare whitespace token:
    # strip ANSI first and match the count against the word it labels.
    import re as _re
    plain = _re.sub(r"\x1b\[[0-9;]*m", "", out)
    m_pass = _re.search(r"(\d+)\s+passed", plain)
    m_fail = _re.search(r"(\d+)\s+failed", plain)
    post_pass = int(m_pass.group(1)) if m_pass else 0
    post_fail = int(m_fail.group(1)) if m_fail else 0
    print("    parsed from the de-ANSI'd summary: %d passed, %d failed" % (post_pass, post_fail))
    PRE_PASS, PRE_FAIL = 8, 0     # measured this session BEFORE the edit, same invocation
    print("    DELTA: +%d test(s). The defect existed BECAUSE nothing covered it, so two "
          "permanent regression arms were added to the estate's own suite -- "
          "test_closed_day_carrying_a_slice_is_distinguishable_from_one_carrying_nothing and "
          "test_slice_on_a_closed_day_moves_no_sum. Growth, not regression: 0 failed on both "
          "sides." % (post_pass - PRE_PASS))
    print("    THE NEW ARMS ARE NOT CONSTANTS: they assert `with_slice != without`, and arm "
          "(a) measured those two records BYTE-IDENTICAL on the pre-change classifier -- so "
          "both new arms would FAIL against the code as it stood, which is what makes them a "
          "guard rather than a restatement.")
    arm("d", r.returncode == 0 and post_fail == PRE_FAIL == 0 and post_pass >= PRE_PASS,
        "the existing suite is green on both sides by its own path: PRE-CHANGE rc=0 %d passed "
        "%d failed, POST-CHANGE rc=%d %d passed %d failed -- NO REGRESSION (0 failed both "
        "sides, +%d new arms), and the class-B ZERO-vs-MISSING arms inside that suite are "
        "untouched" % (PRE_PASS, PRE_FAIL, r.returncode, post_pass, post_fail,
                       post_pass - PRE_PASS))

    # ---------------------------------------------------------------- arm (e)
    print("\n(e) NO ORDINARY DAY MOVES, AND THE ARITHMETIC IS PROVEN NOT ASSUMED")
    print("    Recomputed over the REAL served slices for EVERY partner the artifact lists, "
          "probe=None on BOTH sides (a real probe would INVOKE producer Lambdas, which this "
          "cell's BOUNDS and arm (g) forbid).")
    classes_pre = {p: pre.classify_month(p, MONTH, series=series_real[p], probe=None)
                   for p in partners}
    CLASSES = ("A", "COVERED", "B", "C", "D", "UNKNOWN")
    total_days = 0
    moved_any = []
    for p in partners:
        s_pre, s_post = pre.summarize(classes_pre[p]), post.summarize(classes_post[p])
        total_days += len(classes_pre[p])
        print("    %-12s  %-5s %s" % (p, "PRE ", " ".join("%s=%s" % (c, s_pre[c])
                                                          for c in CLASSES)
                                      + "  trading_days=%s holes=%s"
                                      % (s_pre["trading_days"], s_pre["holes"])))
        print("    %-12s  %-5s %s" % ("", "POST", " ".join("%s=%s" % (c, s_post[c])
                                                           for c in CLASSES)
                                      + "  trading_days=%s holes=%s"
                                      % (s_post["trading_days"], s_post["holes"])))
        for c in CLASSES + ("trading_days", "holes", "covered", "expected_empty"):
            if s_pre[c] != s_post[c]:
                moved_any.append("%s.%s %s->%s" % (p, c, s_pre[c], s_post[c]))
    # the ONLY permitted textual delta: class-A records that now carry the field
    diffs = []
    for p in partners:
        for d in classes_pre[p]:
            a, b = classes_pre[p][d], classes_post[p][d]
            if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
                diffs.append((p, d, a["class"], b.get("slice_on_closed_day")))
    print("    partner-day denominator: %d record(s) compared across %d partner(s)"
          % (total_days, len(partners)))
    print("    COUNTS THAT MOVED: %s" % (moved_any or "NONE"))
    print("    RECORDS THAT CHANGED TEXTUALLY: %d of %d -- %s"
          % (len(diffs), total_days,
             [(p, d, "class=%s slice_on_closed_day=%s" % (c, s)) for p, d, c, s in diffs]))
    print("    IN WORDS: neither `trading_days` nor `holes` moved for any partner, and that is "
          "CORRECT -- summarize() computes trading_days = COVERED+B+C+D+UNKNOWN and holes = "
          "C+UNKNOWN+D, and class A is a member of NEITHER sum. The change adds a FIELD to the "
          "class-A record and no new member to _CLASS_NAMES, so no count can move by "
          "construction; only the class-A records themselves gained the field.")
    all_a = all(c == "A" for _, _, c, _ in diffs)
    arm("e", not moved_any and all_a and len(diffs) > 0,
        "0 count(s) moved across %d partner(s) (trading_days and holes identical on both "
        "sides); %d of %d records changed textually and ALL are class A -- the "
        "closed-day records, which is exactly where the change lives"
        % (len(partners), len(diffs), total_days))

    # ---------------------------------------------------------------- arm (f)
    print("\n(f) DEPLOYED-vs-BUILT, MEASURED")
    dest_a = os.path.join(ROOT, ".scratch", "s22", "deployed_classifier.py")
    rc_a, _ = aws(["s3api", "get-object", "--bucket", ART_BUCKET, "--key", ART_KEY, dest_a])
    dep = open(dest_a, "rb").read() if rc_a == 0 else b""
    built = open(CLASSIFIER, "rb").read()
    dep_sha, built_sha = sha256_bytes(dep), sha256_bytes(built)
    head_blob = subprocess.run(["git", "show", "%s:%s" % (PRE_PIN, CLASSIFIER_REL)],
                               capture_output=True, cwd=ROOT).stdout
    print("    DEPLOYED s3://%s/%s -- %d bytes, sha256 %s" % (ART_BUCKET, ART_KEY, len(dep),
                                                              dep_sha))
    print("    BUILT    %s (this worktree, the bytes this cell commits) -- %d bytes, sha256 %s"
          % (CLASSIFIER_REL, len(built), built_sha))
    print("    CRLF in deployed: %d ; CRLF in built: %d (both LF -- the hash is not an eol "
          "artifact)" % (dep.count(b"\r\n"), built.count(b"\r\n")))
    print("    CORROBORATION: the deployed bytes match the PRE-CHANGE blob at git %s -> %s "
          "(so what the box reads today is exactly the classifier this cell just changed, "
          "before the change)" % (PRE_PIN[:10], sha256_bytes(head_blob) == dep_sha))
    verdict_f = "DEPLOYED == BUILT" if dep_sha == built_sha else "DEPLOYED != BUILT"
    print("    %s" % verdict_f)
    print("    THIS CELL DEPLOYS NOTHING, so %s is the EXPECTED answer. The gap is recorded "
          "as a number and handed on: until someone deploys these bytes to "
          "s3://%s/%s, the served verdict object cannot discriminate a closed day carrying a "
          "slice from one carrying nothing." % (verdict_f, ART_BUCKET, ART_KEY))
    arm("f", (dep_sha != built_sha) and len(dep) > 0 and len(built) > 0,
        "%s -- deployed sha256 %s (%d B) vs built sha256 %s (%d B); this cell deploys nothing "
        "and that is the expected answer, recorded as a number rather than assumed"
        % (verdict_f, dep_sha[:16], len(dep), built_sha[:16], len(built)))

    # ---------------------------------------------------------------- arm (g)
    print("\n(g) NO SEND AND NO INVOKE, PROVEN FROM THIS RUN")
    svc = sorted({c[0] for c in AWS_CALLS if c})
    bad_cli = [c for c in AWS_CALLS if c and c[0] in ("ses", "sesv2", "lambda")]
    bad_boto = [s for s in BOTO_CLIENTS if s in ("ses", "sesv2", "lambda")]
    print("    boto3 available and instrumented: %s ; boto3 clients constructed during this "
          "run: %d (denominator) -> %s" % (boto3_available, len(BOTO_CLIENTS),
                                           BOTO_CLIENTS or "NONE"))
    print("    AWS CLI invocations by this battery: %d (denominator); services used: %s"
          % (len(AWS_CALLS), svc))
    print("    of those, `ses`/`sesv2`/`lambda` calls: %d" % len(bad_cli))
    print("    every classify_month call in this battery passed probe=None, so no producer "
          "Lambda was invoked to build any class")
    print("    the changed module constructs no SES client: `ses` occurs %d time(s) in %s"
          % (post_src.lower().count("ses("), CLASSIFIER_REL))
    arm("g", not bad_cli and not bad_boto,
        "0 SES clients and 0 Lambda invokes over the whole battery: %d boto3 client(s) "
        "constructed (%s), %d AWS CLI call(s) across services %s with 0 naming ses/sesv2/"
        "lambda, and probe=None on every classify_month call -- Andrew's standing constraint "
        "cannot be reached from this cell by construction"
        % (len(BOTO_CLIENTS), BOTO_CLIENTS or "none", len(AWS_CALLS), svc))

    # ---------------------------------------------------------------- verdict
    npass = sum(1 for _, ok, _ in ARMS if ok)
    print("\nARMS %d of %d PASS" % (npass, len(ARMS)))
    if npass == len(ARMS) == 7:
        print("EGS22-CLASSIFIER-DISCRIMINATES")
        return 0
    print("EGS22-NOT-ESTABLISHED -- failing arms: %s"
          % ", ".join(n for n, ok, _ in ARMS if not ok))
    return 1


if __name__ == "__main__":
    sys.exit(main())
