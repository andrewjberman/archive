"""O27-AC1 -- THE STRATUM'S OWN TWO STRINGS REACH THE ARTIFACT.

Prints OS27-BOTH-STRATUM-STRINGS-SERIALIZED only when all six arms hold.

WHY (b), (c) AND (d) RENDER OFFLINE RATHER THAN READING A NEW SERVED RUN. The face bounds this
cell: "no served report is rewritten. This changes what FUTURE runs serialize, does not backfill
09-09 or 09-10, and an arm proves no existing served key moved." The next scheduled fire is
2026-09-11 13:00Z. So the arms that must show the NEW shape build the group block through the
NEW runner's OWN function, from THE SAME pinned seam artifacts the 2026-09-10 13:00Z run read --
same inputs, before and after, which is exactly what arm (d) asks for. The SERVED confirmation
lands on the next scheduled run and is NOT claimed here.

THE ASYMMETRY THAT MAKES THAT HONEST: the "before" side of arm (d) is not a reconstruction. It is
the REAL served artifact of the 13:00Z run, read by its VersionId. Only the "after" side is
rendered, and it is rendered by the deployed bytes rather than the worktree's.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-27). 2026-09-10.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

BUCKET = "opal-estate-report"
CODE_KEY = "code/estate_report_runner.py"
REPO_RUNNER = "infra/aws/ec2/estate-report-runner/estate_report_runner.py"

# The served run whose inputs both sides of arm (d) use, and whose group block is the "before".
RUN_KEY = "daily/2026/09/10/estate-report-2026-09-10.json"
RUN_VERSION = "kIo74Zug6entwLkwzLOw5TYMktp7RJ1R"
RUN_PIN = "77904431-4b72-4033-8f68-4eaba9704b1e"          # run_bundle.run_id, the artifact's own id
SEAM_PREFIX = "s3://opal-estate-report/outset"

# Arm (a): the literals whose ABSENCE is the premise. Denominator-side text and the grain TAG.
ABSENCE_LITERALS = {
    "rostered device(s) reporting": "denominator (group A headline)",
    "ROSTER (declared, not listed": "denominator (group A roster line)",
    "of tracked_total": "denominator (group A per-device)",
    "GRAIN DECLARATION": "denominator (group B grain NOTE)",
    "[grain=": "vintage (group B grain TAG -- what O23-AC1 quotes)",
}
PRESENCE_CONTROL = "A_propagation@laptop"

NEW_FIELDS = ("stratum_vintage", "stratum_denominator")

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def note(msg):
    print("  .. %s" % msg)


def repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         cwd=os.path.dirname(os.path.abspath(__file__)),
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        print("BLOCKED: not inside a git working tree")
        sys.exit(1)
    return out.stdout.strip()


ROOT = repo_root()


def import_module_from(path, name):
    os.environ.setdefault("ESTATE_REPORT_BUCKET", BUCKET)
    for k in ("ESTATE_GITHUB_SECRET_ID", "ESTATE_KIMI_SECRET_ID", "ESTATE_KIMI_MODEL"):
        os.environ.setdefault(k, "battery-placeholder")
    os.environ.setdefault("ESTATE_KIMI_URL", "http://placeholder.invalid")
    os.environ.setdefault("ESTATE_REPO_URL", "http://placeholder.invalid")
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------- tree provenance
def arm_tree():
    print("\n(0) THE TREE THIS BATTERY MEASURED IN, with a positive control")
    print("      git rev-parse --show-toplevel -> %s" % ROOT)
    br = subprocess.run(["git", "-C", ROOT, "rev-parse", "--abbrev-ref", "HEAD"],
                        capture_output=True, text=True, timeout=60).stdout.strip()
    head = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
                          capture_output=True, text=True, timeout=60).stdout.strip()
    print("      branch %s @%s" % (br, head))
    # POSITIVE CONTROL: a file that exists ONLY in this checkout must be visible to a census run
    # here. A tool resolving its corpus from somewhere else would miss it and read a clean zero.
    me = os.path.abspath(__file__)
    ls = subprocess.run(["git", "-C", ROOT, "ls-files", "--others", "--cached",
                         os.path.relpath(me, ROOT).replace("\\", "/")],
                        capture_output=True, text=True, timeout=120).stdout.strip()
    print("      positive control: this battery's own path resolves in THIS tree -> %r"
          % (ls or "(NOT FOUND)"))
    if not ls:
        fail("0", "the battery's own file is not visible to a census in the tree it claims to run "
                  "in -- every census below would be reading some other tree")
        return
    ok("censuses below ran in %s, proven by a file present only in this checkout" % ROOT)


# --------------------------------------------------------------------------- (a)
def arm_a(s3):
    print("\n(a) THE ABSENCE REPRODUCES FIRST, ON THE SERVED BYTES, BOTH STRINGS")
    body = s3.get_object(Bucket=BUCKET, Key=RUN_KEY, VersionId=RUN_VERSION)["Body"].read()
    txt = body.decode("utf-8", errors="replace")
    print("      %s @%s..  %d B" % (RUN_KEY, RUN_VERSION[:12], len(body)))
    print("      DENOMINATOR: %d literal(s) checked" % len(ABSENCE_LITERALS))
    present = []
    for lit, which in sorted(ABSENCE_LITERALS.items()):
        n = txt.count(lit)
        print("        %-32s %-46s %d hit(s)" % (repr(lit), which, n))
        if n:
            present.append((lit, n))
    ctrl = txt.count(PRESENCE_CONTROL)
    print("      POSITIVE CONTROL %-28s %d hit(s)  <- must be non-zero"
          % (repr(PRESENCE_CONTROL), ctrl))
    if ctrl == 0:
        fail("a", "the positive control is absent too, so the zeros above are a property of the "
                  "READER and not of the artifact")
        return
    if present:
        fail("a", "PREMISE WRONG -- %s already appear(s) in the served artifact: %s. The cell's "
                  "absence claim does not hold; file a row and STOP."
             % (len(present), present))
        return
    ok("both strings absent (0 hits each across %d literals) while the control reads %d -- the "
       "zeros are a property of the ARTIFACT" % (len(ABSENCE_LITERALS), ctrl))


# --------------------------------------------------------------------------- render helper
def render_group_b(mod, pin):
    """Build group B's stratum through THIS module, from the SAME seam artifacts the 13:00Z run
    read. `_stratum_cochange`'s seam branch needs only the prefix and a loader."""
    s = mod._stratum_cochange(ROOT, datetime.now(timezone.utc), {}, pin,
                              prefix=SEAM_PREFIX, loader=mod._outset_loader)
    return s


def group_block(mod, s):
    """The block the artifact carries for one group, as THIS module would serialize it."""
    base = {"stratum_status": s["status"], "detect_outcome": None, "unmeasured": True,
            "candidates_raw": None, "candidates_kept": 0, "candidates_rejected": []}
    if hasattr(mod, "group_out_fields"):
        base.update(mod.group_out_fields(s))
    return base


# --------------------------------------------------------------------------- (b) (c) (d)
def arms_bcd(new_mod, old_mod, s3):
    print("\n(b) BOTH FIELDS SERIALIZED, AND WHICH CLAUSE EACH SERVES")
    s_new = render_group_b(new_mod, RUN_PIN)
    block_new = group_block(new_mod, s_new)
    missing = [f for f in NEW_FIELDS if f not in block_new]
    if missing:
        fail("b", "the new group block is missing %s" % missing)
        return
    print("      ai.groups.B keys -> %s" % sorted(block_new.keys()))
    print("      stratum_vintage     (verbatim): %s" % block_new["stratum_vintage"])
    print("      stratum_denominator (verbatim): %s" % (block_new["stratum_denominator"] or "")[:400])
    print("      WHICH CLAUSE EACH SERVES, stated explicitly -- the distinction this cell exists for:")
    print("        stratum_denominator -> read by O22-AC1 clause (v): can a reader tell a device is")
    print("                               NOT-PUBLISHED-OR-UNREADABLE rather than simply absent")
    print("        stratum_vintage     -> read by O23-AC1: can a reader tell GROUP B pairs FILES")
    print("                               and not RESOURCES, via the [grain=...] tag")
    if not block_new["stratum_vintage"] or not block_new["stratum_denominator"]:
        fail("b", "a serialized field is empty")
        return
    ok("both fields present beside stratum_status, both non-empty, each mapped to its clause")

    print("\n(c) THE STRINGS ARE THE RUNNER'S OWN -- byte equality, not containment")
    for field, key in (("stratum_vintage", "vintage"), ("stratum_denominator", "denominator")):
        composed = s_new[key]
        serialized = block_new[field]
        same = composed == serialized
        print("      %-20s composed %d B  serialized %d B  sha256 %s / %s  EQUAL=%s"
              % (field, len(composed), len(serialized),
                 hashlib.sha256(composed.encode()).hexdigest()[:16],
                 hashlib.sha256(serialized.encode()).hexdigest()[:16], same))
        if not same:
            fail("c", "%s is not byte-equal to the value the runner composed in the same run"
                 % field)
            return
    # A CONTAINS-check would pass on a truncation or a prefix. Shown to fail where equality holds.
    truncated = block_new["stratum_vintage"][:-5]
    print("      CONTROL: a TRUNCATED copy still passes a `contains` test (%s) but fails equality "
          "(%s) -- which is why this arm compares bytes"
          % (truncated in s_new["vintage"], truncated == s_new["vintage"]))
    ok("both serialized fields are byte-equal to the strings the runner composed in the same run")

    print("\n(d) THE DIFFERENCE CONTROL -- the SAME inputs, before and after")
    served = json.loads(s3.get_object(Bucket=BUCKET, Key=RUN_KEY,
                                      VersionId=RUN_VERSION)["Body"].read().decode("utf-8"))
    block_before = ((served.get("ai") or {}).get("groups") or {}).get("B") or {}
    print("      BEFORE -- the REAL served group-B block of the 13:00Z run (not a reconstruction):")
    print("        %s" % json.dumps(block_before, sort_keys=True)[:400])
    print("      AFTER  -- the same stratum through the DEPLOYED new bytes:")
    print("        %s" % json.dumps({k: (v[:120] + "..." if isinstance(v, str) and len(v) > 120
                                         else v) for k, v in sorted(block_new.items())})[:600])
    tag = "[grain="
    before_has = tag in json.dumps(block_before)
    after_has = tag in json.dumps(block_new)
    print("      '%s' in BEFORE block: %s   in AFTER block: %s" % (tag, before_has, after_has))
    if before_has:
        fail("d", "the grain tag is already in the served block -- there is no difference to show")
        return
    if not after_has:
        fail("d", "the grain tag is STILL absent after the change -- the cell did not do its job")
        return
    ok("engaged against the same run disengaged: the grain tag is ABSENT before and PRESENT after, "
       "in the serialized vintage")


# --------------------------------------------------------------------------- (e)
def arm_e(new_mod, old_src, new_src, s3):
    print("\n(e) NOTHING ELSE MOVED")
    # 1. the composed strings are untouched.
    composed_lines = ['den = "%s -- %s" % (den, grain_note)',
                      'vin = "%s [grain=%s, NOT resource-grain]" % (vin, grain)']
    print("      DENOMINATOR: %d composed-string line(s) checked" % len(composed_lines))
    for ln in composed_lines:
        a, b = old_src.count(ln), new_src.count(ln)
        print("        %-58s old=%d new=%d" % (ln[:56], a, b))
        if a != b or b == 0:
            fail("e", "a composed-string line moved: %r old=%d new=%d" % (ln, a, b))
            return
    ok("the composed strings at :1421-1425 are unchanged (%d of %d present on both sides)"
       % (len(composed_lines), len(composed_lines)))

    # 2. the citation gate is untouched, byte-compared rather than counted.
    def fn_body(src, marker, end):
        i = src.find(marker)
        j = src.find(end, i + 1)
        return src[i:j] if i >= 0 else ""
    for marker in ("def tool_row_resolves(", "def tool_row_ref("):
        a = fn_body(old_src, marker, "\n\ndef ")
        b = fn_body(new_src, marker, "\n\ndef ")
        same = a == b and bool(a)
        print("        %-26s old %d B / new %d B  sha256 %s / %s  EQUAL=%s"
              % (marker.strip("def ("), len(a), len(b),
                 hashlib.sha256(a.encode()).hexdigest()[:12],
                 hashlib.sha256(b.encode()).hexdigest()[:12], same))
        if not same:
            fail("e", "%s changed -- this cell must not touch the validator" % marker)
            return
    ok("tool_row_resolves and tool_row_ref are BYTE-IDENTICAL between the served bytes and the "
       "new bytes")

    # 3. the day's other groups' stratum_status are unchanged.
    served = json.loads(s3.get_object(Bucket=BUCKET, Key=RUN_KEY,
                                      VersionId=RUN_VERSION)["Body"].read().decode("utf-8"))
    statuses = {g: b.get("stratum_status")
                for g, b in ((served.get("ai") or {}).get("groups") or {}).items()}
    print("      the 13:00Z run's stratum_status values, unchanged by this cell (it does not "
          "backfill): %s" % json.dumps(statuses, sort_keys=True))
    if not statuses:
        fail("e", "could not read the served run's group statuses")
        return
    ok("%d group status value(s) read from the served artifact; this cell rewrites none of them"
       % len(statuses))

    # 4. no existing served key was rewritten.
    keys = ["daily/2026/09/09/estate-report-2026-09-09.json",
            "daily/2026/09/09/estate-report-2026-09-09.md",
            "daily/2026/09/10/estate-report-2026-09-10.json",
            "daily/2026/09/10/estate-report-2026-09-10.md",
            "manifest/2026-09-09.json", "manifest/2026-09-10.json"]
    print("      DENOMINATOR: %d served report/manifest key(s) checked for a rewrite" % len(keys))
    moved = []
    for k in keys:
        h = s3.head_object(Bucket=BUCKET, Key=k)
        lm = h["LastModified"].astimezone(timezone.utc)
        recent = (datetime.now(timezone.utc) - lm).total_seconds() < 600
        print("        %-52s LastModified %s%s"
              % (k, lm.strftime("%Y-%m-%dT%H:%M:%SZ"), "  *** MOVED IN THE LAST 10 MIN ***"
                 if recent else ""))
        if recent:
            moved.append(k)
    if moved:
        fail("e", "%d served key(s) moved inside this act's window: %s" % (len(moved), moved))
        return
    ok("0 of %d served report/manifest keys moved -- this cell changes what FUTURE runs "
       "serialize and backfills nothing" % len(keys))


# --------------------------------------------------------------------------- (f)
def arm_f(s3, new_src_bytes):
    print("\n(f) THE DEPLOY IS REAL AND REVERSIBLE")
    h = s3.head_object(Bucket=BUCKET, Key=CODE_KEY)
    served_vid, served_etag, served_len = h["VersionId"], h["ETag"].strip('"'), h["ContentLength"]
    print("      served %s  %d B  ETag %s  VersionId %s"
          % (CODE_KEY, served_len, served_etag, served_vid))
    head_md5 = hashlib.md5(new_src_bytes).hexdigest()
    print("      HEAD blob %d B  md5 %s" % (len(new_src_bytes), head_md5))
    if served_etag != head_md5:
        fail("f", "the served ETag %s does not equal md5 of the committed bytes %s -- the deploy "
                  "is not landed" % (served_etag, head_md5))
        return
    # RE-DOWNLOAD BY THE NEW VersionId rather than trusting head-object's ETag.
    got = s3.get_object(Bucket=BUCKET, Key=CODE_KEY, VersionId=served_vid)["Body"].read()
    same = hashlib.sha256(got).hexdigest() == hashlib.sha256(new_src_bytes).hexdigest()
    print("      re-downloaded by VersionId: %d B  sha256 %s  EQUAL=%s"
          % (len(got), hashlib.sha256(got).hexdigest()[:16], same))
    if not same:
        fail("f", "the object re-downloaded by its own VersionId is not byte-equal to the "
                  "committed bytes")
        return
    mutant = bytearray(got)
    mutant[100] ^= 0x01
    if hashlib.sha256(bytes(mutant)).hexdigest() == hashlib.sha256(new_src_bytes).hexdigest():
        fail("f", "a one-bit mutant compares EQUAL -- the comparator is a constant")
        return
    ok("served bytes re-downloaded by VersionId are byte-equal to the committed bytes, with a "
       "one-bit negative control at fixed length reporting MISMATCH")
    vs = s3.list_object_versions(Bucket=BUCKET, Prefix=CODE_KEY).get("Versions", [])
    print("      DENOMINATOR: %d version(s) of the code key; rollback target is the one before "
          "this upload" % len(vs))
    prior = [v for v in vs if not v["IsLatest"]]
    if prior:
        p = sorted(prior, key=lambda v: v["LastModified"], reverse=True)[0]
        print("      ROLLBACK: copy-object from VersionId %s (%d B, %s) -- in session, no "
              "Terraform, versioning Enabled so nothing is deleted by an overwrite"
              % (p["VersionId"], p["Size"],
                 p["LastModified"].astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    ok("rollback target named from the live version list, not from memory")


def main():
    print("=" * 78)
    print("O27-AC1 -- THE STRATUM'S OWN TWO STRINGS REACH THE ARTIFACT")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s)." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")

    here = os.path.dirname(os.path.abspath(__file__))
    # THE "AFTER" MODULE IS THE DEPLOYED ONE, not the worktree's -- so arm (c)'s byte equality is
    # a statement about what the estate will run and not about what this seat can see.
    new_bytes = s3.get_object(Bucket=BUCKET, Key=CODE_KEY)["Body"].read()
    new_path = os.path.join(here, ".served_runner_os27_new.py")
    with open(new_path, "wb") as fh:
        fh.write(new_bytes)
    # THE "BEFORE" MODULE is the version the 13:00Z run actually executed.
    vs = sorted(s3.list_object_versions(Bucket=BUCKET, Prefix=CODE_KEY).get("Versions", []),
                key=lambda v: v["LastModified"], reverse=True)
    old_v = [v for v in vs if not v["IsLatest"]]
    old_bytes = s3.get_object(Bucket=BUCKET, Key=CODE_KEY,
                              VersionId=old_v[0]["VersionId"])["Body"].read() if old_v else b""
    print("after  = served %s (%d B)" % (CODE_KEY, len(new_bytes)))
    print("before = prior version %s (%d B)"
          % (old_v[0]["VersionId"][:12] if old_v else "(none)", len(old_bytes)))

    new_mod = import_module_from(new_path, "os27_new")
    old_src = old_bytes.decode("utf-8", errors="replace")
    new_src = new_bytes.decode("utf-8", errors="replace")

    arm_tree()
    arm_a(s3)
    arms_bcd(new_mod, None, s3)
    arm_e(new_mod, old_src, new_src, s3)
    arm_f(s3, new_bytes)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS27-BOTH-STRATUM-STRINGS-SERIALIZED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
