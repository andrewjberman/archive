#!/usr/bin/env python
"""EG-s-26 / S26-AC1 -- THE ARTIFACT MUST RECORD WHAT WAS *SKIPPED*, NOT ONLY WHAT WAS FORCED.

Six arms, each one clause of the task order's acceptance. Every number is printed
beside its denominator. The token EGS26-SKIP-DISCLOSED-IN-ONE-READ is emitted ONLY
when all six arms hold; any arm failing prints its own FAIL line and the battery
exits 1 with no token.

  (a) THE ABSENCE REPRODUCES FIRST, ON THE DEPLOYED BYTES.
  (b) A LADDER-SKIPPED RUN SAYS SO, AND NAMES WHAT THE SKIP COST.
  (c) A LADDER-RAN RUN SAYS SO TOO, AND THE TWO ARE TEXTUALLY DIFFERENT.
  (d) ONE READ, NOT TWO.
  (e) THE VERDICT DID NOT MOVE.
  (f) THE DEPLOY IS REAL AND REVERSIBLE, AND NOTHING ELSE FIRED.

VINTAGES, because a citation without one is not a citation. This battery reads
THREE different renderer objects and never conflates them:

  PRE  = the bytes that WERE served at s3://opal-313476888478-lambda-artifacts/
         ec2/etfs-reports/render_month_end.py as object VersionId
         V1i.w8DNP2iqwsiiRYC7k40Neh90w3DH (66756 B, LastModified 2026-09-10T05:19:37Z).
         Byte-equal to git blob 32ae4ede66:data/etfs/scripts/presentation/render_month_end.py.
         THIS is the object arm (a)'s absence census runs against and arm (e)'s
         "before" runs against. It is fetched from S3 BY VERSION ID, not from git,
         so the arm reads the DEPLOYED bytes the task order names.
  POST = the bytes served at that key NOW, VersionId TkhI7NPt_hpJUaXYAlBnjZggJQDz.wBG
         (69879 B, LastModified 2026-09-10T06:40:10Z). Byte-equal to git blob
         5b15b09834:data/etfs/scripts/presentation/render_month_end.py.
  WORK = data/etfs/scripts/presentation/render_month_end.py in this worktree, which
         is what arms (b), (c), (d) and (e)-after exercise as an imported module.

NOTE: WHY ARM (a) DOES NOT RUN AGAINST "CURRENTLY SERVED", AND SAYS SO PLAINLY. The
task order's arm (a) reads "against the renderer as currently served". At the time
the task order was cut that phrase and "the bytes without the skip record" named the
same object. They no longer do: the deploy this cell owns landed at 2026-09-10T06:40:10Z,
3m25s before the device that was executing it rebooted, so by the time this battery
could be written the CURRENTLY-served object is already the POST object. Running the
reproduce-the-absence arm against POST would be a vacuously FAILING census of a
premise that was true and has been closed by this very cell. Arm (a) therefore runs
its premise census against PRE -- still a DEPLOYED object, fetched from the same key
by version id -- and reports the POST census separately as the LANDING half, which is
a different claim. Filed as surprise row ETFS_GUARDRAIL-W5-S9.

HERMETIC. Zero producer invokes, zero SES calls, zero writes anywhere. Every S3 write
in arms (b)-(e) goes to a recording stub; the only real AWS calls in the whole battery
are READS (s3 head/get/list, cloudwatch get-metric-statistics) in arms (a) and (f).
subprocess.run is poisoned before the PRE module is loaded so that the renderer's own
box-bootstrap fallback (an `aws s3 cp`) cannot fire silently from a temp directory.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile

# --------------------------------------------------------------------------------
# Locate the repo and put the renderer's own import roots on sys.path FIRST, so that
# `from coverage import classifier, remediate` and `from _orion_vendor_asof import ...`
# resolve from the repo checkout and NEVER from the renderer's box-bootstrap fallback.
# --------------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
# SEVEN levels: deliverables/<serial> -> deliverables -> ETFS_GUARDRAIL -> ETFS -> D8
# -> missions -> org -> repo root. Asserted below rather than trusted, because an
# off-by-one here resolves to a REAL directory and every later path silently misses.
REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..", "..", "..", ".."))
if not (os.path.isdir(os.path.join(REPO, ".tools")) and os.path.isdir(os.path.join(REPO, "org"))):
    raise SystemExit("REPO does not resolve to the worktree root: %s" % REPO)
PRESENTATION = os.path.join(REPO, "data", "etfs", "scripts", "presentation")
ETFS_SCRIPTS = os.path.join(REPO, "data", "etfs", "scripts")
SILVER = os.path.join(REPO, "data", "inf", "scripts", "silver")
for _p in (SILVER, ETFS_SCRIPTS, PRESENTATION, REPO):
    if _p not in sys.path:
        sys.path.insert(0, _p)

BUCKET = "opal-313476888478-lambda-artifacts"
KEY = "ec2/etfs-reports/render_month_end.py"
PREFIX = "ec2/etfs-reports/"
# NOTE: A DIFFERENT BUCKET FROM THE ARTIFACT PREFIX, and the two are easy to conflate
# because the prefixes read alike. The served reports live in the ETFS DATA bucket;
# the renderer CODE lives in the lambda-artifacts bucket. Taken from the verbatim argv
# of the act's own step 1 (`--bucket opal-data-etfs --prefix platinum/reports/`) in
# egs26_deploy_evidence.json, so the battery reads the SAME population the act listed
# rather than a bucket this file happened to name. An earlier draft of this battery
# had the artifacts bucket here and the listing returned 0 keys -- which would have
# read as "nothing to move" instead of "wrong object". See the ZERO GUARD below.
REPORTS_BUCKET = "opal-data-etfs"
REPORTS_PREFIX = "platinum/reports/"
PRIOR_VERSION_ID = "V1i.w8DNP2iqwsiiRYC7k40Neh90w3DH"
POST_VERSION_ID = "TkhI7NPt_hpJUaXYAlBnjZggJQDz.wBG"
COMMITTED_BLOB_REF = "5b15b09834:data/etfs/scripts/presentation/render_month_end.py"
PRECHANGE_BLOB_REF = "32ae4ede66:data/etfs/scripts/presentation/render_month_end.py"
EVIDENCE = os.path.join(_HERE, "egs26_deploy_evidence.json")

ARMS: dict = {}
FAILURES: list = []


def hdr(title: str) -> None:
    print("")
    print("=" * 96)
    print(title)
    print("=" * 96)


def check(arm: str, label: str, ok: bool, detail: str = "") -> bool:
    line = "  [%s] %-58s %s" % (arm, label[:58], "OK" if ok else "FAIL")
    if detail:
        line += "   " + detail
    print(line)
    if not ok:
        FAILURES.append("%s: %s %s" % (arm, label, detail))
    return ok


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob(ref: str) -> bytes:
    """Read a blob at a VINTAGE from the object DB -- never the worktree checkout,
    which on this autocrlf box hashes the CHECKOUT and not the record."""
    out = subprocess.run(["git", "-C", REPO, "show", ref],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out.returncode != 0:
        raise RuntimeError("git show %s failed rc=%d: %s"
                           % (ref, out.returncode, out.stderr.decode("utf-8", "replace")[:300]))
    return out.stdout


# ================================================================================
# ARM (a) -- THE ABSENCE REPRODUCES FIRST, ON THE DEPLOYED BYTES
# ================================================================================
# The 8 skip-disclosure tokens. Written as the record's OWN key set plus the two
# reader-facing strings the task order names by hand ("RUNG 3 DID NOT RUN so
# coverage_egress_ask.json IS ABSENT BY CONSTRUCTION"), so the census cannot pass by
# checking only machine keys a human never reads.
SKIP_TOKENS = [
    "ladder_ran",
    "ladder_skip_mechanism",
    "rung3_stop_and_ask_reachable",
    "coverage_egress_ask_possible",
    "skip_note",
    "run_shape",
    "LADDER SKIPPED",
    "ABSENT BY CONSTRUCTION",
]
# POSITIVE CONTROLS. Deliberately the EG-s-25 forcing fields and the verdict itself:
# if these read zero too, the census instrument is dead and the skip zeros mean
# nothing. A zero that cannot be distinguished from a dead read is not a measurement.
POS_CONTROLS = ["forced", "mechanism", "forcing", "run_id", "verdict"]


def census(text: str, tokens: list) -> dict:
    """TWO counting methods over one text, because one method's blind spot is the
    other's ordinary case: (i) raw substring count, (ii) word-boundary regex count.
    A token present only as a fragment of a longer identifier scores on (i) and not
    on (ii); the pair is what makes a ZERO trustworthy."""
    out = {}
    for t in tokens:
        sub = text.count(t)
        wb = len(re.findall(r"(?<![A-Za-z0-9_])" + re.escape(t) + r"(?![A-Za-z0-9_])", text))
        out[t] = {"substring": sub, "word_boundary": wb}
    return out


def arm_a(s3c) -> bool:
    hdr("ARM (a)  THE ABSENCE REPRODUCES FIRST, ON THE DEPLOYED BYTES")
    ok = True

    # --- fetch PRE: the DEPLOYED object that carried the absence, BY VERSION ID ---
    r = s3c.get_object(Bucket=BUCKET, Key=KEY, VersionId=PRIOR_VERSION_ID)
    pre = r["Body"].read()
    pre_sha = sha256_bytes(pre)
    print("  PRE  object  s3://%s/%s?versionId=%s" % (BUCKET, KEY, PRIOR_VERSION_ID))
    print("               %d B   LastModified %s   sha256 %s"
          % (len(pre), r["LastModified"].astimezone(_dt.timezone.utc).isoformat(), pre_sha))
    blob_pre = git_blob(PRECHANGE_BLOB_REF)
    print("  PRE  git blob %s" % PRECHANGE_BLOB_REF)
    print("               %d B   sha256 %s" % (len(blob_pre), sha256_bytes(blob_pre)))
    ok &= check("a", "PRE served object byte-equal to the pre-change git blob",
                sha256_bytes(blob_pre) == pre_sha and len(blob_pre) == len(pre),
                "(two independent sources of one vintage agree)")

    # --- fetch POST: what is served NOW ---
    r2 = s3c.get_object(Bucket=BUCKET, Key=KEY)
    post = r2["Body"].read()
    post_sha = sha256_bytes(post)
    print("  POST object  s3://%s/%s   VersionId %s" % (BUCKET, KEY, r2["VersionId"]))
    print("               %d B   LastModified %s   sha256 %s"
          % (len(post), r2["LastModified"].astimezone(_dt.timezone.utc).isoformat(), post_sha))
    ok &= check("a", "PRE and POST are DIFFERENT objects (negative control)",
                post_sha != pre_sha,
                "(so an equality anywhere below discriminates rather than passing vacuously)")

    pre_t = pre.decode("utf-8", "replace")
    post_t = post.decode("utf-8", "replace")
    pre_lines = pre_t.count("\n") + 1
    post_lines = post_t.count("\n") + 1

    # --- THE PREMISE CENSUS, on PRE ---
    print("")
    print("  PREMISE CENSUS on the PRE object -- DENOMINATOR: %d line(s) / %d byte(s) scanned,"
          % (pre_lines, len(pre)))
    print("  %d skip token(s) x 2 counting methods = %d reads; %d positive control(s) x 2 = %d reads."
          % (len(SKIP_TOKENS), 2 * len(SKIP_TOKENS), len(POS_CONTROLS), 2 * len(POS_CONTROLS)))
    pre_skip = census(pre_t, SKIP_TOKENS)
    pre_pos = census(pre_t, POS_CONTROLS)
    print("    SKIP-DISCLOSURE TOKENS (expected ZERO on both methods):")
    zero_n = 0
    for t in SKIP_TOKENS:
        c = pre_skip[t]
        z = (c["substring"] == 0 and c["word_boundary"] == 0)
        zero_n += 1 if z else 0
        print("      %-34s substring=%-4d word_boundary=%-4d  %s"
              % (t, c["substring"], c["word_boundary"], "ZERO" if z else "*** PRESENT ***"))
    print("    POSITIVE CONTROLS (expected NON-ZERO -- proves the census can see):")
    nonzero_n = 0
    for t in POS_CONTROLS:
        c = pre_pos[t]
        nz = (c["substring"] > 0)
        nonzero_n += 1 if nz else 0
        print("      %-34s substring=%-4d word_boundary=%-4d  %s"
              % (t, c["substring"], c["word_boundary"], "NON-ZERO" if nz else "*** ZERO ***"))
    print("    RESULT: %d of %d skip tokens ZERO; %d of %d positive controls NON-ZERO."
          % (zero_n, len(SKIP_TOKENS), nonzero_n, len(POS_CONTROLS)))

    # THE TASK ORDER'S STOP CLAUSE, honoured explicitly.
    if zero_n != len(SKIP_TOKENS):
        print("")
        print("  *** PREMISE WRONG: a skip record ALREADY EXISTS on the PRE object. ***")
        print("  Per the task order's arm (a): file a row, print it, and STOP.")
        FAILURES.append("a: PREMISE WRONG -- skip record already present on the PRE object")
        return False
    ok &= check("a", "all %d skip tokens ZERO on the deployed PRE object" % len(SKIP_TOKENS),
                zero_n == len(SKIP_TOKENS), "(%d of %d)" % (zero_n, len(SKIP_TOKENS)))
    ok &= check("a", "all %d positive controls NON-ZERO on the same read" % len(POS_CONTROLS),
                nonzero_n == len(POS_CONTROLS), "(%d of %d -- the zeros are not a dead read)"
                % (nonzero_n, len(POS_CONTROLS)))

    # --- THE LANDING HALF, on POST. A DIFFERENT CLAIM, reported separately. ---
    print("")
    print("  LANDING CENSUS on the POST object (NOT the premise check -- the premise is")
    print("  what PRE carried; this is whether the change reached the world).")
    print("  DENOMINATOR: %d line(s) / %d byte(s) scanned, %d token(s) x 2 methods."
          % (post_lines, len(post), len(SKIP_TOKENS)))
    post_skip = census(post_t, SKIP_TOKENS)
    land_n = 0
    for t in SKIP_TOKENS:
        c = post_skip[t]
        nz = c["substring"] > 0
        land_n += 1 if nz else 0
        print("      %-34s substring=%-4d word_boundary=%-4d  %s"
              % (t, c["substring"], c["word_boundary"], "PRESENT" if nz else "*** ABSENT ***"))
    print("    RESULT: %d of %d skip tokens PRESENT on the currently-served object."
          % (land_n, len(SKIP_TOKENS)))
    ok &= check("a", "all %d skip tokens PRESENT on the POST object" % len(SKIP_TOKENS),
                land_n == len(SKIP_TOKENS), "(%d of %d)" % (land_n, len(SKIP_TOKENS)))

    globals()["_PRE_BYTES"] = pre
    globals()["_POST_BYTES"] = post
    globals()["_PRE_SHA"] = pre_sha
    globals()["_POST_SHA"] = post_sha
    return ok


# ================================================================================
# Hermetic harness for arms (b)-(e): stubs, module loading, and a main() driver.
# ================================================================================
class ExplodingLam:
    """Fails the battery LOUDLY if .invoke() is ever reached. A 'no invoke' arm that
    merely happens not to raise proves nothing; this makes the absence a measurement."""

    def __init__(self):
        self.calls = []

    def invoke(self, **kw):
        self.calls.append(kw)
        raise AssertionError("lam.invoke() must never be called in this battery: %r" % (kw,))


class FailingLam:
    """Rung 1's producer invoke, made to fail deterministically and IDENTICALLY for
    the PRE and the POST module, so arm (e) compares two runs that took the same path
    through the ladder rather than two runs that diverged in the stub."""

    def __init__(self):
        self.calls = []

    def invoke(self, **kw):
        self.calls.append(kw)
        raise RuntimeError("upstream partition absent (deterministic stub)")


class StubS3:
    """Serves classifier._load_series (list_objects_v2 paginator) and
    remediate._slice_exists (head_object) from a FIXED caller-supplied key set, and
    RECORDS every put_object instead of performing one. Nothing this battery does can
    reach real S3 through this object."""

    def __init__(self, existing: dict):
        self.existing = {k: set(v) for k, v in (existing or {}).items()}
        self.put_calls: list = []
        self.head_calls = 0
        self.list_calls = 0

    def get_paginator(self, name):
        assert name == "list_objects_v2", name
        return self

    def paginate(self, Bucket, Prefix):
        self.list_calls += 1
        partner = Prefix.split("/")[1]
        yield {"Contents": [{"Key": "daily/%s/%s.json" % (partner, d)}
                            for d in sorted(self.existing.get(partner, set()))]}

    def head_object(self, Bucket, Key):
        self.head_calls += 1
        partner = Key.split("/")[1]
        d = Key.rsplit("/", 1)[-1][:-len(".json")]
        if d in self.existing.get(partner, set()):
            return {}
        raise Exception("404 Not Found")

    def put_object(self, Bucket, Key, Body, ContentType=None, **kw):
        self.put_calls.append((Bucket, Key, Body))
        return {}


def load_module(name: str, source: bytes):
    """Import a renderer's BYTES as a module without letting its box-bootstrap
    fallback fire. The renderer resolves `coverage` and `_orion_vendor_asof` relative
    to its own file location and, on ImportError, shells out to `aws s3 cp`. Loading
    the PRE bytes from a temp directory is exactly the shape that triggers it -- so
    the two modules are pre-seeded into sys.modules and subprocess.run is POISONED
    across the load. If the fallback ever fires this raises instead of quietly making
    a network call."""
    import coverage as _cov            # noqa: F401  -- seeds sys.modules
    from coverage import classifier, remediate   # noqa: F401
    import _orion_vendor_asof          # noqa: F401
    tmpd = tempfile.mkdtemp(prefix="egs26_")
    path = os.path.join(tmpd, name + ".py")
    with open(path, "wb") as f:
        f.write(source)
    real_run = subprocess.run

    def poisoned(*a, **kw):
        raise AssertionError("subprocess.run reached during module load -- the box "
                             "bootstrap fallback fired: %r" % (a,))
    subprocess.run = poisoned
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    finally:
        subprocess.run = real_run
    return mod


def trading_days(month: str) -> list:
    from lib import trading_calendar as tcal
    y, m = int(month[:4]), int(month[5:7])
    import calendar as _cal
    last = _cal.monthrange(y, m)[1]
    return [d.isoformat() for d in tcal.trading_days_between(
        _dt.date(y, m, 1), _dt.date(y, m, last))]


def slice_(v: float, as_of: str) -> dict:
    return {"DIVZ": {"v": v, "n": 1, "as_of": as_of}}


def drive_main(mod, month, fixture, present, ladder: bool, fixture_remove_spec: str = ""):
    """Drive the REAL main() end to end through --gate [--no-ladder] --s3-out and
    return the EXACT coverage_verdict.json BODY BYTES it wrote. This is the ARTIFACT,
    not a re-serialisation of the gate's return value: the battery reads what the
    renderer's own writer put, so a defect between the record and the artifact cannot
    hide behind a transcribed json.dumps."""
    saved = {}
    for attr, val in (("load_universe", lambda: ["DIVZ"]),
                      ("load_monthly_avg", lambda month_: {}),
                      ("load_all_daily", lambda p: dict(fixture.get(p, {}))),
                      ("opal_logo_svg", lambda: ""),
                      ("_make_probe", lambda lam_client=None:
                       (lambda partner, date_str: {"partition": True, "priced": 999}))):
        saved[attr] = getattr(mod, attr)
        setattr(mod, attr, val)
    lam = ExplodingLam() if not ladder else FailingLam()
    rec = StubS3({p: set(present) for p in fixture})
    saved["lam"], saved["s3"] = mod.lam, mod.s3
    mod.lam, mod.s3 = lam, rec
    tmpd = tempfile.mkdtemp(prefix="egs26_out_")
    argv = [os.path.join(PRESENTATION, "render_month_end.py"), "--month", month,
            "--out", os.path.join(tmpd, "out.html"), "--gate",
            "--s3-out", "s3://test-bucket/platinum/reports/"]
    if not ladder:
        argv.append("--no-ladder")
    if fixture_remove_spec:
        argv += ["--fixture-remove", fixture_remove_spec]
    saved_argv, saved_stdout = sys.argv, sys.stdout
    sys.argv = argv
    cap = io.StringIO()
    sys.stdout = cap
    try:
        try:
            rc = mod.main()
        except SystemExit as exc:
            rc = exc.code
    finally:
        sys.argv, sys.stdout = saved_argv, saved_stdout
        for attr in ("load_universe", "load_monthly_avg", "load_all_daily",
                     "opal_logo_svg", "_make_probe", "lam", "s3"):
            setattr(mod, attr, saved[attr])
    body = None
    for _b, k, bb in rec.put_calls:
        if k.endswith("coverage_verdict.json"):
            body = bb
    return {"rc": rc, "body": body, "stdout": cap.getvalue(),
            "put_keys": [k for _b, k, _bb in rec.put_calls],
            "invokes": len(lam.calls), "s3": rec}


MONTH = "2026-08"


def arm_b(rme) -> bool:
    hdr("ARM (b)  A LADDER-SKIPPED RUN SAYS SO, AND NAMES WHAT THE SKIP COST")
    days = trading_days(MONTH)
    present = days[:16]
    missing = days[16:]
    fixture = {"cottonwood": {d: slice_(100.0, d) for d in present}}
    spec = "cottonwood:" + ",".join(missing)
    run = drive_main(rme, MONTH, fixture, present, ladder=False, fixture_remove_spec=spec)
    print("  DRIVEN THROUGH main(): --month %s --gate --no-ladder --fixture-remove %s"
          % (MONTH, spec))
    print("  DENOMINATOR: %d trading day(s) in %s; %d present, %d removed. rc=%s. "
          "producer invokes=%d of a permitted 0. put_object keys written=%d."
          % (len(days), MONTH, len(present), len(missing), run["rc"], run["invokes"],
             len(run["put_keys"])))
    for k in run["put_keys"]:
        print("      wrote (to the recording stub, NOT to S3): %s" % k)
    ok = check("b", "the artifact was written at all", run["body"] is not None)
    if not ok:
        return False
    art = json.loads(run["body"])
    print("")
    print("  THE WRITTEN coverage_verdict.json, PRINTED WHOLE (%d B as written):"
          % len(run["body"]))
    print("  " + "-" * 92)
    for ln in json.dumps(art, indent=2).splitlines():
        print("  | " + ln)
    print("  " + "-" * 92)
    f = art.get("forcing", {})
    ok &= check("b", "records THAT the ladder was skipped", f.get("ladder_ran") is False,
                "ladder_ran=%r" % f.get("ladder_ran"))
    ok &= check("b", "records WHY / by what mechanism",
                f.get("ladder_skip_mechanism") == "--no-ladder",
                "ladder_skip_mechanism=%r" % f.get("ladder_skip_mechanism"))
    ok &= check("b", "records that RUNG 3 DID NOT RUN",
                f.get("rung3_stop_and_ask_reachable") is False,
                "rung3_stop_and_ask_reachable=%r" % f.get("rung3_stop_and_ask_reachable"))
    ok &= check("b", "records that the ask artifact is not possible",
                f.get("coverage_egress_ask_possible") is False,
                "coverage_egress_ask_possible=%r" % f.get("coverage_egress_ask_possible"))
    note = f.get("skip_note", "")
    ok &= check("b", "NAMES coverage_egress_ask.json by name in prose",
                "coverage_egress_ask.json" in note)
    ok &= check("b", "says ABSENT BY CONSTRUCTION in prose",
                "ABSENT BY CONSTRUCTION" in note)
    ok &= check("b", "a reader need not know the flag implies the missing artifact",
                "coverage_egress_ask.json" in note and "ABSENT BY CONSTRUCTION" in note
                and "--no-ladder" in note,
                "(the note carries flag + artifact + consequence in ONE string)")
    ok &= check("b", "no coverage_egress_ask.json was written by this run",
                not any(k.endswith("coverage_egress_ask.json") for k in run["put_keys"]),
                "(0 of %d keys)" % len(run["put_keys"]))
    ok &= check("b", "zero producer invokes", run["invokes"] == 0,
                "(%d of a permitted 0)" % run["invokes"])
    ok &= check("b", "the run's own stdout warns too, not only the artifact",
                "LADDER SKIPPED" in run["stdout"]
                and "ABSENT BY CONSTRUCTION" in run["stdout"])
    globals()["_ART_SKIPPED"] = art
    return ok


def arm_c(rme) -> bool:
    hdr("ARM (c)  A LADDER-RAN RUN SAYS SO TOO, AND THE TWO ARE TEXTUALLY DIFFERENT")
    days = trading_days(MONTH)
    fixture = {"cottonwood": {d: slice_(100.0, d) for d in days}}
    ran = drive_main(rme, MONTH, fixture, days, ladder=True)
    skipped = drive_main(rme, MONTH, fixture, days, ladder=False)
    print("  BOTH runs driven through the SAME main() writer over the SAME fixture")
    print("  (%d of %d trading days present in %s), the ONLY difference being --no-ladder."
          % (len(days), len(days), MONTH))
    print("  DIFFERENCE CONTROL, not a positive control: what changes is the flag, so what")
    print("  differs in the output is attributable to the flag and to nothing else.")
    ok = check("c", "both artifacts written", ran["body"] is not None and skipped["body"] is not None)
    if not ok:
        return False
    a_ran = json.loads(ran["body"])["forcing"]
    a_skip = json.loads(skipped["body"])["forcing"]
    keys = sorted(set(a_ran) | set(a_skip))
    print("")
    print("  SIDE BY SIDE -- the `forcing` object of each artifact. DENOMINATOR: %d key(s)"
          % len(keys))
    print("  present in the union of the two records; %d in ran, %d in skipped."
          % (len(a_ran), len(a_skip)))
    print("  %-32s | %-26s | %s" % ("key", "LADDER RAN", "LADDER SKIPPED"))
    print("  " + "-" * 92)
    diff_n = 0
    for k in keys:
        v1 = a_ran.get(k, "<ABSENT>")
        v2 = a_skip.get(k, "<ABSENT>")
        d = "" if v1 == v2 else "  <-- DIFFERS"
        if v1 != v2:
            diff_n += 1
        print("  %-32s | %-26s | %s%s" % (k, repr(v1)[:26], repr(v2)[:40], d))
    print("  " + "-" * 92)
    print("  %d of %d key(s) differ between the two records." % (diff_n, len(keys)))
    print("")
    print("  FULL skip_note, LADDER RAN branch:")
    print("    %s" % a_ran.get("skip_note"))
    print("  FULL skip_note, LADDER SKIPPED branch:")
    print("    %s" % a_skip.get("skip_note"))

    # A FIELD PRESENT ONLY IN THE SKIPPED CASE IS NOT A DISCLOSURE.
    only_in_skipped = sorted(set(a_skip) - set(a_ran))
    ok &= check("c", "no disclosure key exists ONLY in the skipped record",
                not only_in_skipped, "(%d such key(s): %r)" % (len(only_in_skipped), only_in_skipped))
    ok &= check("c", "ladder_ran carries an explicit RAN-value on the ran branch",
                a_ran.get("ladder_ran") is True, "ladder_ran=%r" % a_ran.get("ladder_ran"))
    ok &= check("c", "ladder_skip_mechanism reads the literal 'none', not omitted",
                a_ran.get("ladder_skip_mechanism") == "none",
                "=%r" % a_ran.get("ladder_skip_mechanism"))
    ok &= check("c", "rung3 reachable is explicitly TRUE on the ran branch",
                a_ran.get("rung3_stop_and_ask_reachable") is True)
    ok &= check("c", "coverage_egress_ask_possible explicitly TRUE on the ran branch",
                a_ran.get("coverage_egress_ask_possible") is True)
    ok &= check("c", "the ran branch does NOT overclaim (reachable != written)",
                "may or may not have been written" in (a_ran.get("skip_note") or ""))
    ok &= check("c", "the two records are TEXTUALLY different",
                json.dumps(a_ran, sort_keys=True) != json.dumps(a_skip, sort_keys=True),
                "(%d of %d keys differ)" % (diff_n, len(keys)))
    ok &= check("c", "run_shape distinguishes them for a prose reader",
                "LADDER RAN" in (a_ran.get("run_shape") or "")
                and "LADDER SKIPPED" in (a_skip.get("run_shape") or ""))
    globals()["_ART_RAN"] = json.loads(ran["body"])
    return ok


def arm_d(rme) -> bool:
    hdr("ARM (d)  ONE READ, NOT TWO")
    days = trading_days(MONTH)
    present = days[:16]
    fixture = {"cottonwood": {d: slice_(100.0, d) for d in present}}
    spec = "cottonwood:" + ",".join(days[16:])
    run = drive_main(rme, MONTH, fixture, present, ladder=False, fixture_remove_spec=spec)
    art = json.loads(run["body"])
    top = sorted(art.keys())
    f = art["forcing"]
    fam = sorted(f.keys())
    forced_half = ["forced", "mechanism", "fixture_remove_spec", "fixture_remove",
                   "removed_slice_count"]
    skip_half = ["ladder_ran", "ladder_skip_mechanism", "rung3_stop_and_ask_reachable",
                 "coverage_egress_ask_possible", "skip_note"]
    print("  THIS RUN IS BOTH: --fixture-remove (forced) AND --no-ladder (skipped), so the")
    print("  two halves are live at the same time and a reader needs both from one place.")
    print("  DENOMINATOR: %d top-level key(s) in the artifact; %d key(s) in `forcing`."
          % (len(top), len(fam)))
    print("  top-level keys : %s" % ", ".join(top))
    print("  forcing keys   : %s" % ", ".join(fam))
    print("  FORCED half (%d of %d forcing keys): %s" % (len(forced_half), len(fam),
                                                          ", ".join(forced_half)))
    print("  SKIPPED half (%d of %d forcing keys): %s" % (len(skip_half), len(fam),
                                                           ", ".join(skip_half)))
    print("  SHARED summary (1 of %d): run_shape = %r" % (len(fam), f.get("run_shape")))
    ok = check("d", "every FORCED-half key lives in `forcing`",
               all(k in f for k in forced_half),
               "(%d of %d)" % (sum(1 for k in forced_half if k in f), len(forced_half)))
    ok &= check("d", "every SKIPPED-half key lives in the SAME `forcing` object",
                all(k in f for k in skip_half),
                "(%d of %d)" % (sum(1 for k in skip_half if k in f), len(skip_half)))
    # BY SUBTRACTION, never by recall: no OTHER top-level key carries either half.
    others = [k for k in top if k != "forcing"]
    leaked = []
    for k in others:
        blob = json.dumps(art[k], sort_keys=True, default=str)
        for tok in forced_half + skip_half:
            if tok in blob:
                leaked.append((k, tok))
    print("  SUBTRACTION CHECK: %d top-level key(s) MINUS `forcing` = %d other key(s)"
          % (len(top), len(others)))
    print("  scanned for ANY of the %d half-keys; %d leak(s) found."
          % (len(forced_half) + len(skip_half), len(leaked)))
    ok &= check("d", "no second place holds either half", not leaked, repr(leaked[:4]))
    ok &= check("d", "both halves read TRUE-ly on this one run",
                f.get("forced") is True and f.get("ladder_ran") is False,
                "forced=%r ladder_ran=%r" % (f.get("forced"), f.get("ladder_ran")))
    ok &= check("d", "run_shape restates both in one line for a prose reader",
                "FORCED" in (f.get("run_shape") or "") and "LADDER SKIPPED" in (f.get("run_shape") or ""))
    print("")
    print("  THE CTO'S CONDITION (i), IN ONE SENTENCE: a reader opens")
    print("  coverage_verdict.json, reads the single key `forcing`, and has BOTH facts --")
    print("  what this run FORCED into its input (`forced`/`mechanism`/`fixture_remove`) and")
    print("  what it SKIPPED in its processing (`ladder_ran`/`ladder_skip_mechanism`/")
    print("  `rung3_stop_and_ask_reachable`/`coverage_egress_ask_possible`/`skip_note`),")
    print("  plus `run_shape` restating both in one line -- with no second key to find, no")
    print("  join to perform, and nothing to know in advance.")
    return ok


def _classes(mod, month, partners, daily, ladder, lam, s3stub):
    saved_lam, saved_s3 = mod.lam, mod.s3
    saved_probe = mod._make_probe
    mod.lam, mod.s3 = lam, s3stub
    mod._make_probe = lambda lam_client=None: (lambda p, d: {"partition": True, "priced": 999})
    cap, saved_stdout = io.StringIO(), sys.stdout
    sys.stdout = cap
    try:
        return mod.coverage_gate(month, partners, daily, ["DIVZ"], ladder=ladder,
                                 probe=(lambda p, d: {"partition": True, "priced": 999}))
    finally:
        sys.stdout = saved_stdout
        mod.lam, mod.s3, mod._make_probe = saved_lam, saved_s3, saved_probe


def arm_e(rme, rme_pre) -> bool:
    hdr("ARM (e)  THE VERDICT DID NOT MOVE")
    days = trading_days(MONTH)
    scenarios = [
        ("COMPLETE  (%d of %d days present)" % (len(days), len(days)), days),
        ("5 REMOVED (%d of %d days present)" % (len(days) - 5, len(days)), days[:-5]),
    ]
    quantities = ["verdict", "holes", "A", "B", "C", "D", "UNKNOWN"]
    print("  BEFORE = the DEPLOYED PRE bytes (VersionId %s), loaded as a module." % PRIOR_VERSION_ID)
    print("  AFTER  = data/etfs/scripts/presentation/render_month_end.py in this worktree.")
    print("  DENOMINATOR: %d scenario(s) x %d ladder branch(es) x %d quantity(ies) = %d"
          % (len(scenarios), 2, len(quantities), len(scenarios) * 2 * len(quantities)))
    print("  compared quantities, plus %d producer-invoke count(s)." % (len(scenarios) * 2))
    print("")
    print("  %-40s %-7s %-24s %-24s %s"
          % ("scenario", "ladder", "BEFORE (PRE bytes)", "AFTER (worktree)", "match"))
    print("  " + "-" * 118)
    same, total, inv_same, inv_total = 0, 0, 0, 0
    ok = True
    for label, present in scenarios:
        daily = {"cottonwood": {d: slice_(100.0, d) for d in present}}
        for ladder in (True, False):
            lam_a, lam_b = FailingLam(), FailingLam()
            r_pre = _classes(rme_pre, MONTH, ["cottonwood"], daily, ladder,
                             lam_a, StubS3({"cottonwood": set(present)}))
            r_post = _classes(rme, MONTH, ["cottonwood"], daily, ladder,
                              lam_b, StubS3({"cottonwood": set(present)}))
            s_pre = r_pre["per_partner"]["cottonwood"]["summary"]
            s_post = r_post["per_partner"]["cottonwood"]["summary"]
            for q in quantities:
                v1 = r_pre[q] if q in ("verdict", "holes") else s_pre.get(q)
                v2 = r_post[q] if q in ("verdict", "holes") else s_post.get(q)
                total += 1
                same += 1 if v1 == v2 else 0
                if v1 != v2:
                    ok = False
                print("  %-40s %-7s %-24s %-24s %s"
                      % (label if q == "verdict" else "", "ladder=%s" % ladder if q == "verdict" else "",
                         "%s=%r" % (q, v1), "%s=%r" % (q, v2), "SAME" if v1 == v2 else "*** MOVED ***"))
            inv_total += 1
            inv_same += 1 if len(lam_a.calls) == len(lam_b.calls) else 0
            print("  %-40s %-7s %-24s %-24s %s"
                  % ("", "", "invokes=%d" % len(lam_a.calls), "invokes=%d" % len(lam_b.calls),
                     "SAME" if len(lam_a.calls) == len(lam_b.calls) else "*** MOVED ***"))
            print("  " + "-" * 118)
    print("  RESULT: %d of %d compared quantities IDENTICAL; %d of %d invoke counts identical."
          % (same, total, inv_same, inv_total))
    ok &= check("e", "every class count and verdict identical, BOTH ladder branches",
                same == total, "(%d of %d)" % (same, total))
    ok &= check("e", "the ladder took the same path in both modules",
                inv_same == inv_total, "(%d of %d)" % (inv_same, inv_total))
    # A NEGATIVE CONTROL ON THE COMPARISON ITSELF: the two scenarios must NOT agree
    # with each other, or the 'identical' above would pass on a dead comparator.
    d1 = {"cottonwood": {d: slice_(100.0, d) for d in scenarios[0][1]}}
    d2 = {"cottonwood": {d: slice_(100.0, d) for d in scenarios[1][1]}}
    v1 = _classes(rme, MONTH, ["cottonwood"], d1, False, ExplodingLam(), StubS3({}))["verdict"]
    v2 = _classes(rme, MONTH, ["cottonwood"], d2, False, ExplodingLam(), StubS3({}))["verdict"]
    print("  NEGATIVE CONTROL on the comparator: complete month -> %s, 5 removed -> %s."
          % (v1, v2))
    ok &= check("e", "the comparator CAN report a difference", v1 != v2,
                "(%s vs %s -- so 'identical' above is a measurement, not a constant)" % (v1, v2))
    return ok


def arm_f(s3c, cw) -> bool:
    hdr("ARM (f)  THE DEPLOY IS REAL AND REVERSIBLE, AND NOTHING ELSE FIRED")
    ok = True
    ev = json.load(open(EVIDENCE, encoding="utf-8"))

    print("  STANDING: this deploy is WORLD-DONE and is CLOSED SUPERSEDED, NOT RE-EXECUTED.")
    print("  The copy landed 2026-09-10T06:40:10Z; the device rebooted 06:43:35Z, killing the")
    print("  session between the act and its record. CLAUDE.md NEVER-2: measure the ARTIFACT,")
    print("  and a re-execute of an overtaken promote is a REWIND. This battery makes READS")
    print("  ONLY -- head_object, get_object, list_objects_v2, get_metric_statistics -- and")
    print("  issues NO put, NO copy and NO invoke.")
    print("")

    # ---- (f.1) the served object IS the committed bytes -------------------------
    h = s3c.head_object(Bucket=BUCKET, Key=KEY)
    body = s3c.get_object(Bucket=BUCKET, Key=KEY)["Body"].read()
    served_sha = sha256_bytes(body)
    committed = git_blob(COMMITTED_BLOB_REF)
    committed_sha = sha256_bytes(committed)
    print("  SERVED    s3://%s/%s" % (BUCKET, KEY))
    print("            VersionId %s  %d B  LastModified %s"
          % (h["VersionId"], h["ContentLength"],
             h["LastModified"].astimezone(_dt.timezone.utc).isoformat()))
    print("            sha256 %s" % served_sha)
    print("  COMMITTED %s" % COMMITTED_BLOB_REF)
    print("            %d B  sha256 %s" % (len(committed), committed_sha))
    ok &= check("f", "served bytes sha256 EQUAL committed bytes sha256",
                served_sha == committed_sha and len(body) == len(committed),
                "(both sides printed above)")
    ok &= check("f", "served object is the version the act created",
                h["VersionId"] == POST_VERSION_ID, "VersionId=%s" % h["VersionId"])

    # ---- (f.2) the rollback, exact, cross-verified from two sources --------------
    pr = s3c.get_object(Bucket=BUCKET, Key=KEY, VersionId=PRIOR_VERSION_ID)
    prior = pr["Body"].read()
    prior_sha = sha256_bytes(prior)
    prior_blob = git_blob(PRECHANGE_BLOB_REF)
    print("")
    print("  PRIOR OBJECT (the rollback target), recorded in the entry BEFORE the copy:")
    print("            VersionId %s  %d B  sha256 %s" % (PRIOR_VERSION_ID, len(prior), prior_sha))
    print("  INDEPENDENT SOURCE: git blob %s" % PRECHANGE_BLOB_REF)
    print("            %d B  sha256 %s" % (len(prior_blob), sha256_bytes(prior_blob)))
    ok &= check("f", "entry's recorded prior sha256 matches the live prior version",
                ev.get("prior_sha256") == prior_sha,
                "entry=%s live=%s" % (str(ev.get("prior_sha256"))[:16], prior_sha[:16]))
    ok &= check("f", "entry's recorded prior VersionId matches",
                ev.get("prior_version_id") == PRIOR_VERSION_ID)
    ok &= check("f", "rollback target cross-verified from TWO independent sources",
                sha256_bytes(prior_blob) == prior_sha,
                "(S3 version + git blob -- different instruments, not one twice)")
    ok &= check("f", "the rollback is a REAL restore, not a no-op",
                prior_sha != served_sha, "(prior != served)")
    print("  ROLLBACK, EXACT RESTORE, one command, no rebuild:")
    print("    .tools/aws s3api copy-object --bucket %s --key %s \\" % (BUCKET, KEY))
    print("      --copy-source '%s/%s?versionId=%s'" % (BUCKET, KEY, PRIOR_VERSION_ID))
    print("    restores %d B / sha256 %s. Equivalent second source: re-upload git blob %s."
          % (len(prior), prior_sha, PRECHANGE_BLOB_REF))

    # ---- (f.3) nothing else moved in the artifact prefix -------------------------
    def listing(bucket, prefix):
        # AUTO-PAGINATED then counted client-side: a `list-*` that is not paginated
        # returns the PAGE, and a page is not an answer.
        out = {}
        p = s3c.get_paginator("list_objects_v2")
        for page in p.paginate(Bucket=bucket, Prefix=prefix):
            for o in page.get("Contents", []):
                out[o["Key"]] = {"Size": o["Size"], "ETag": o["ETag"],
                                 "LastModified": o["LastModified"].astimezone(
                                     _dt.timezone.utc).isoformat()}
        return out

    now_art = listing(BUCKET, PREFIX)
    ev_before = ev["artifact_before"]
    ev_after = ev["artifact_after"]
    print("")
    print("  ARTIFACT PREFIX s3://%s/%s" % (BUCKET, PREFIX))
    print("    DENOMINATOR: %d key(s) listed before the act, %d after, %d NOW (this read)."
          % (len(ev_before), len(ev_after), len(now_art)))
    delta_act = ev["artifact_delta"]
    print("    DURING THE ACT: %d of %d key(s) changed." % (len(delta_act), len(ev_after)))
    for d in delta_act:
        print("      %s  %s  %s B -> %s B" % (d["change"], d["key"],
                                              d["before"]["Size"], d["after"]["Size"]))
    ok &= check("f", "exactly ONE key changed during the act",
                len(delta_act) == 1 and delta_act[0]["key"] == KEY,
                "(1 of %d)" % len(ev_after))
    # SINCE the act, across the crash window, to now.
    since = []
    for k in sorted(set(now_art) | set(ev_after)):
        a, b = ev_after.get(k), now_art.get(k)
        if a is None:
            since.append(("ADDED", k))
        elif b is None:
            since.append(("REMOVED", k))
        elif a["ETag"] != b["ETag"] or a["Size"] != b["Size"]:
            since.append(("CHANGED", k))
    print("    SINCE THE ACT (spanning the 06:43:35Z crash to this read): %d of %d key(s) moved."
          % (len(since), len(now_art)))
    for c, k in since[:10]:
        print("      %s %s" % (c, k))
    ok &= check("f", "nothing in the artifact prefix moved after the act",
                not since, "(%d of %d)" % (len(since), len(now_art)))

    # ---- (f.4) no write under platinum/reports/ ---------------------------------
    now_rep = listing(REPORTS_BUCKET, REPORTS_PREFIX)
    ev_rep_before = ev["reports_before"]
    # ZERO GUARD. An empty listing and a listing of an untouched population are the
    # same value here, and only one of them is evidence. A wrong bucket, a wrong
    # prefix or a lost credential all return {} with rc=0, and the delta computed
    # from {} reads as "everything REMOVED" or, if the baseline were also empty, as
    # a clean pass. So the battery refuses to grade a zero-length population at all.
    ok &= check("f", "the reports listing is NON-EMPTY (a zero is out-of-corpus, not absence)",
                len(now_rep) > 0 and len(ev_rep_before) > 0,
                "(now=%d key(s), baseline=%d key(s) in s3://%s/%s)"
                % (len(now_rep), len(ev_rep_before), REPORTS_BUCKET, REPORTS_PREFIX))
    ok &= check("f", "the artifact-prefix listing is NON-EMPTY for the same reason",
                len(now_art) > 0 and len(ev_after) > 0,
                "(now=%d key(s), baseline=%d key(s))" % (len(now_art), len(ev_after)))
    rep_since = []
    for k in sorted(set(now_rep) | set(ev_rep_before)):
        a, b = ev_rep_before.get(k), now_rep.get(k)
        if a is None:
            rep_since.append(("ADDED", k))
        elif b is None:
            rep_since.append(("REMOVED", k))
        elif a["ETag"] != b["ETag"] or a["Size"] != b["Size"]:
            rep_since.append(("CHANGED", k))
    print("")
    print("  SERVED REPORTS PREFIX s3://%s/%s" % (REPORTS_BUCKET, REPORTS_PREFIX))
    print("    DENOMINATOR: %d key(s) listed at 2026-09-10T06:40:03Z (before the act), %d NOW."
          % (len(ev_rep_before), len(now_rep)))
    print("    DELTA recorded across the act itself: %d key(s)." % len(ev["reports_delta"]))
    print("    DELTA before-the-act -> NOW (spans the act AND the crash window): %d of %d key(s)."
          % (len(rep_since), len(now_rep)))
    for c, k in rep_since[:10]:
        print("      %s %s" % (c, k))
    ok &= check("f", "ZERO writes under platinum/reports/ across the whole window",
                not rep_since and not ev["reports_delta"],
                "(%d of %d keys moved)" % (len(rep_since), len(now_rep)))

    # ---- (f.5) no SES send ------------------------------------------------------
    act_start = _dt.datetime(2026, 9, 10, 6, 39, 0, tzinfo=_dt.timezone.utc)
    act_end = _dt.datetime(2026, 9, 10, 6, 41, 0, tzinfo=_dt.timezone.utc)
    now = _dt.datetime.now(_dt.timezone.utc)
    print("")
    print("  SES, namespace AWS/SES, Period=300.")
    print("  NOTE: THE CLAIM IS SCOPED TO THE ACT, AND THE SCOPE IS STATED BEFORE THE NUMBER.")
    print("  A whole-day zero is NOT the claim and would be a false one: this estate sends")
    print("  legitimate mail from other cells on other seats, and grading my act on their")
    print("  traffic would convict me of their sends -- or, worse, would have quietly")
    print("  passed on a day nobody else happened to send. So the discriminator is")
    print("  TIME OVERLAP: every SES datapoint of the whole UTC day is enumerated with its")
    print("  bucket timestamp, and the claim is that NONE of them overlaps the act window")
    print("  06:39:20Z-06:40:19Z. That is falsifiable in both directions.")
    day0 = _dt.datetime(2026, 9, 10, 0, 0, 0, tzinfo=_dt.timezone.utc)
    ses_ok, day_total, overlapping = True, 0.0, []
    for metric in ("Send", "Delivery", "Reputation.BounceRate"):
        r = cw.get_metric_statistics(Namespace="AWS/SES", MetricName=metric,
                                     StartTime=day0, EndTime=now, Period=300,
                                     Statistics=["Sum"])
        dp = sorted(r.get("Datapoints", []), key=lambda d: d["Timestamp"])
        tot = sum(d.get("Sum", 0.0) for d in dp)
        print("    %-22s WHOLE DAY %s -> now: datapoints=%-3d sum=%s"
              % (metric, day0.strftime("%H:%MZ"), len(dp), tot))
        for d in dp:
            b0 = d["Timestamp"].astimezone(_dt.timezone.utc)
            b1 = b0 + _dt.timedelta(seconds=300)
            hit = (b0 < act_end) and (b1 > act_start)
            print("        bucket %s -> %s  sum=%-6s  %s"
                  % (b0.strftime("%H:%M:%SZ"), b1.strftime("%H:%M:%SZ"), d.get("Sum"),
                     "*** OVERLAPS THE ACT ***" if hit else "outside the act window"))
            if hit and d.get("Sum", 0.0) != 0:
                overlapping.append((metric, b0.isoformat(), d.get("Sum")))
                ses_ok = False
        if metric == "Send":
            day_total = tot
    # AND the narrow query on its own, as a SECOND read of the same claim at a
    # different grain -- a whole-day enumeration filtered in this process, versus
    # CloudWatch itself filtering server-side. They can disagree; if they do, say so.
    narrow = cw.get_metric_statistics(Namespace="AWS/SES", MetricName="Send",
                                      StartTime=act_start, EndTime=act_end,
                                      Period=300, Statistics=["Sum"])
    ndp = narrow.get("Datapoints", [])
    ntot = sum(d.get("Sum", 0.0) for d in ndp)
    print("    SERVER-SIDE NARROW READ  Send, StartTime=06:39:00Z EndTime=06:41:00Z:")
    print("        datapoints=%d  sum=%s" % (len(ndp), ntot))
    ok &= check("f", "no SES Send datapoint overlaps the act window", ses_ok,
                "(%d overlapping of a whole-day Send total of %s)" % (len(overlapping), day_total))
    ok &= check("f", "the server-side narrow read agrees", ntot == 0,
                "(sum=%s -- two reads of one claim at different grains)" % ntot)
    print("  DISCLOSED, NOT GRADED: the day's %s Send(s) sit in buckets outside the act"
          % day_total)
    print("  window and are NOT this cell's. This cell issues no SES call at all -- see the")
    print("  argv census below, which is what actually bounds the claim.")

    # ---- (f.6) no Lambda invoke -------------------------------------------------
    all_fns = ev.get("_fn_denominator") or globals().get("_FN_NAMES") or []
    print("")
    print("  LAMBDA, namespace AWS/Lambda, MetricName Invocations, window 06:39:00Z-06:41:00Z")
    print("  (the act ran 06:39:20Z -> 06:40:19Z; a 2-minute window brackets it).")
    print("  DENOMINATOR BY SUBTRACTION, never by recall: %d function(s) exist in this account;"
          % len(all_fns))
    sel = [f for f in all_fns if ("etf" in f.lower() or "report" in f.lower())]
    print("  the checked set is those %d MINUS the %d whose name carries neither the token"
          % (len(all_fns), len(all_fns) - len(sel)))
    print("  'etf' nor 'report' = %d function(s) checked." % len(sel))
    inv_ok, checked = True, 0
    for fn in sorted(sel):
        r = cw.get_metric_statistics(Namespace="AWS/Lambda", MetricName="Invocations",
                                     Dimensions=[{"Name": "FunctionName", "Value": fn}],
                                     StartTime=act_start, EndTime=act_end,
                                     Period=300, Statistics=["Sum"])
        dp = r.get("Datapoints", [])
        tot = sum(d.get("Sum", 0.0) for d in dp)
        checked += 1
        print("    %-40s datapoints=%-3d sum=%s" % (fn, len(dp), tot))
        if tot != 0:
            inv_ok = False
    ok &= check("f", "zero Lambda invocations in the act window",
                inv_ok, "(%d of %d function(s) checked, all sum=0)" % (checked, len(sel)))

    # SECOND, DIFFERENT INSTRUMENT on the same claim -- not the same command twice.
    steps = ev.get("steps", [])
    services = sorted({(s["argv"][1] if len(s.get("argv", [])) > 1 else "?") for s in steps})
    bad = [s["label"] for s in steps
           if len(s.get("argv", [])) > 1 and s["argv"][1] not in ("s3api", "cloudwatch")]
    print("")
    print("  SECOND INSTRUMENT, DIFFERENT AXIS: a census of what the act ACTUALLY CALLED,")
    print("  from the verbatim argv of every step in the entry's evidence -- CloudWatch")
    print("  measures what FIRED, this measures what was ISSUED, and they can disagree.")
    print("    DENOMINATOR: %d step(s) recorded, AWS services invoked: %s"
          % (len(steps), ", ".join(services)))
    print("    step(s) touching any service other than s3api/cloudwatch: %d of %d"
          % (len(bad), len(steps)))
    ok &= check("f", "no `lambda`, no `ses` and no `ssm` call in the act's argv census",
                not bad and len(steps) > 0, "(%d of %d)" % (len(bad), len(steps)))

    # ---- (f.7) the entry itself --------------------------------------------------
    print("")
    print("  RESIDUAL, STATED RATHER THAN IMPLIED: the invoke check is scoped to function")
    print("  names carrying 'etf' or 'report'. A function named with neither token could in")
    print("  principle have fired in that window; the argv census above is what bounds that,")
    print("  because a step that never called `aws lambda` cannot have invoked anything.")
    return ok


def main() -> int:
    print("EG-s-26 / S26-AC1 BATTERY -- THE ARTIFACT MUST RECORD WHAT WAS SKIPPED")
    print("serial  0.9.0_WK_ETFS_GUARDRAIL~5")
    print("to      ETFS_GUARDRAIL.TO-EG-s-26")
    print("repo    %s" % REPO)
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"],
                          stdout=subprocess.PIPE).stdout.decode().strip()
    branch = subprocess.run(["git", "-C", REPO, "rev-parse", "--abbrev-ref", "HEAD"],
                            stdout=subprocess.PIPE).stdout.decode().strip()
    print("branch  %s   HEAD %s" % (branch, head))
    print("run at  %s" % _dt.datetime.now(_dt.timezone.utc).isoformat())

    import boto3
    s3c = boto3.client("s3", region_name="us-east-1")
    cw = boto3.client("cloudwatch", region_name="us-east-1")
    lam_c = boto3.client("lambda", region_name="us-east-1")
    names = []
    p = lam_c.get_paginator("list_functions")
    for page in p.paginate():
        names.extend(f["FunctionName"] for f in page.get("Functions", []))
    globals()["_FN_NAMES"] = names

    ARMS["a"] = arm_a(s3c)
    if not ARMS["a"] and any("PREMISE WRONG" in f for f in FAILURES):
        print("")
        print("STOPPED at arm (a) per the task order's own instruction.")
        return 1

    import render_month_end as rme
    rme_pre = load_module("render_month_end_PRE", globals()["_PRE_BYTES"])
    print("")
    print("  MODULES LOADED: AFTER = %s" % rme.__file__)
    print("                  BEFORE = the PRE object's bytes (%d B, sha256 %s),"
          % (len(globals()["_PRE_BYTES"]), globals()["_PRE_SHA"]))
    print("                  loaded from a temp path with subprocess.run poisoned across")
    print("                  the load, so the renderer's `aws s3 cp` box-bootstrap could")
    print("                  not fire silently. It did not fire.")

    ARMS["b"] = arm_b(rme)
    ARMS["c"] = arm_c(rme)
    ARMS["d"] = arm_d(rme)
    ARMS["e"] = arm_e(rme, rme_pre)
    ARMS["f"] = arm_f(s3c, cw)

    hdr("RESULT")
    held = 0
    for a in ("a", "b", "c", "d", "e", "f"):
        print("  ARM (%s)  %s" % (a, "HOLDS" if ARMS.get(a) else "FAILS"))
        held += 1 if ARMS.get(a) else 0
    print("")
    print("  %d of 6 arms hold.  %d failure line(s)." % (held, len(FAILURES)))
    for f in FAILURES:
        print("    FAILURE: %s" % f)
    if held == 6 and not FAILURES:
        print("")
        print("EGS26-SKIP-DISCLOSED-IN-ONE-READ")
        return 0
    print("")
    print("NO TOKEN -- the battery emits EGS26-SKIP-DISCLOSED-IN-ONE-READ only when all")
    print("six arms hold and no arm recorded a failure line.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
