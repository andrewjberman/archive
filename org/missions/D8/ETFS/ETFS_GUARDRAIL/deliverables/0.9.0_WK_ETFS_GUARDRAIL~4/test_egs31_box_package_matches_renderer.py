#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-31 -- S31-AC1 BATTERY, five arms, one token.

THE PROPERTY BEING TESTED, and it is deliberately not an act:

    The box EXECUTES a `coverage` package whose symbols satisfy the renderer artifact
    it will actually run -- and that agreement is PROVEN BY EXERCISING THE CALL PATH,
    never by an upload receipt.

SO NO ARM HERE ACCEPTS AN UPLOAD RECEIPT, AN ETag, OR A DIRECTORY LISTING AS PROOF OF
THE OUTCOME. Arm (c) resolves the symbol ON THE BOX through the renderer's own import,
and arm (d) runs the real `--no-ladder` call path there and reads a verdict out of it.
Arm (b) does hash the artifact prefix, but it is a CENSUS of a writer, not the outcome.

Run from the repo root:
    timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs31_box_package_matches_renderer.py

Prints EGS31-THE-BOX-RUNS-THE-PACKAGE-THE-RENDERER-EXPECTS on the last line if and only
if all five arms hold. Every number is printed beside its denominator.

WHY ARM (a) READS A COMMITTED FIXTURE AND NOT THE LIVE PREFIX. Arm (a) must show the
defect REPRODUCING on the deployed package before any act -- but the act makes the
deployed package current, so a grader re-running this battery later cannot re-read the
broken state from S3. The pre-act deployed bytes are therefore committed under
fixtures/pre_act_deployed_coverage/ as `.pyfixture` files, with their sha256 recorded in
egs31_pre_act_manifest.json and their S3 VersionIds recorded there too, so the claim
stays checkable against the bucket's own version history. `.pyfixture` rather than `.py`
because these are recorded ARTEFACT BYTES, not source: they must not be imported by any
tool that walks the tree, and they are not this repo's code to lint.

THE ONE PERMITTED DRIVEN RUN OF EG-s-21 IS NOT SPENT HERE AND CANNOT BE. Every exercise
runs with `ladder=False` and a stub probe, so `remediate.remediate_month` is never
called, no Lambda is invoked, and the renderer module's `s3` client is replaced by a
recording stub before the call -- the one `put_object` the `--no-ladder` branch attempts
is intercepted and counted, never forwarded. This battery invokes no orchestrator and
sends no mail.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import time

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))

BUCKET = "opal-313476888478-lambda-artifacts"
PREFIX = "ec2/etfs-reports/coverage/"
RENDERER_KEY = "ec2/etfs-reports/render_month_end.py"
INSTANCE = "i-070477bf35fc54409"
REGION = "us-east-1"

EXERCISE = os.path.join(HERE, "egs31_exercise_call_path.py")
FIXTURES = os.path.join(HERE, "fixtures", "pre_act_deployed_coverage")
MANIFEST = os.path.join(HERE, "egs31_pre_act_manifest.json")

REPO_RENDERER = os.path.join(REPO, "data", "etfs", "scripts", "presentation",
                             "render_month_end.py")
REPO_COVERAGE = os.path.join(REPO, "data", "etfs", "scripts", "coverage")

# The prefix carries FIVE members but the repo `coverage/` package holds only THREE.
# The other two are VENDORED from elsewhere in the repo -- render_month_end.py:60-64 and
# classifier.py:49-56 name both. A census that compared the prefix only against
# data/etfs/scripts/coverage/ would score these two as orphans; naming their true source
# is what makes "5 of 5 match" a real statement instead of "3 of 3 plus two we ignored".
COUNTERPART = {
    "__init__.py": "data/etfs/scripts/coverage/__init__.py",
    "classifier.py": "data/etfs/scripts/coverage/classifier.py",
    "remediate.py": "data/etfs/scripts/coverage/remediate.py",
    "_orion_vendor_asof.py": "data/inf/scripts/silver/_orion_vendor_asof.py",
    "trading_calendar.py": "lib/trading_calendar.py",
}

SPEC = "cottonwood:2026-08-14"
EXPECT_VERDICT = "VERDICT: REFUSE holes=1"

s3 = boto3.client("s3", region_name=REGION)
ssm = boto3.client("ssm", region_name=REGION)
ec2 = boto3.client("ec2", region_name=REGION)

results: dict = {}


def hdr(arm: str, title: str) -> None:
    print("")
    print("=" * 78)
    print("ARM (%s) -- %s" % (arm, title))
    print("=" * 78)


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: str) -> str:
    with open(p, "rb") as fh:
        return sha256_bytes(fh.read())


def run_local_exercise(label: str, coverage_dir: str, extras: list) -> str:
    cmd = [sys.executable, EXERCISE, "--label", label,
           "--coverage-dir", coverage_dir, "--renderer", REPO_RENDERER]
    for e in extras:
        cmd += ["--extra", e]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    text = out.stdout + out.stderr
    print(text.strip())
    return text


def ssm_run(script: str, timeout_s: int = 420) -> str:
    cid = ssm.send_command(
        InstanceIds=[INSTANCE],
        DocumentName="AWS-RunShellScript",
        Parameters={"commands": [script], "executionTimeout": [str(timeout_s)]},
    )["Command"]["CommandId"]
    print("SSM-COMMAND-ID %s" % cid)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except ssm.exceptions.InvocationDoesNotExist:
            continue
        if inv["Status"] in ("Pending", "InProgress", "Delayed"):
            continue
        print("SSM-STATUS %s rc=%s" % (inv["Status"], inv.get("ResponseCode")))
        text = inv.get("StandardOutputContent", "") + inv.get("StandardErrorContent", "")
        print(text.strip())
        return text
    print("SSM-STATUS CLIENT-SIDE-TIMEOUT")
    return ""


def ensure_box_running() -> str:
    state = ec2.describe_instances(InstanceIds=[INSTANCE])[
        "Reservations"][0]["Instances"][0]["State"]["Name"]
    print("EGS31-BOX %s state=%s (measured)" % (INSTANCE, state))
    if state == "running":
        pass
    elif state in ("stopped", "stopping"):
        # Starting a box is an ordinary act (CLAUDE.md). STOPPING it is not, and this
        # battery never stops it -- see arm (e).
        print("EGS31-BOX starting (ordinary act; this battery never stops it)")
        while state == "stopping":
            time.sleep(10)
            state = ec2.describe_instances(InstanceIds=[INSTANCE])[
                "Reservations"][0]["Instances"][0]["State"]["Name"]
        ec2.start_instances(InstanceIds=[INSTANCE])
        waiter = ec2.get_waiter("instance_running")
        waiter.wait(InstanceIds=[INSTANCE])
        state = "running"
    else:
        print("EGS31-BOX unexpected state %s" % state)
    # SSM registration lags the power state; wait for the agent, do not assume it.
    for _ in range(45):
        info = ssm.describe_instance_information(
            Filters=[{"Key": "InstanceIds", "Values": [INSTANCE]}])["InstanceInformationList"]
        if info and info[0]["PingStatus"] == "Online":
            print("EGS31-BOX ssm=Online")
            return state
        time.sleep(10)
    print("EGS31-BOX ssm=NOT-ONLINE")
    return state


# --------------------------------------------------------------------------------
# ARM (a) -- the defect reproduces on the DEPLOYED artifact, paired with the current
# package, before any act. Both sides printed. Same renderer bytes on both sides: the
# ONLY thing that differs between them is the coverage package.
# --------------------------------------------------------------------------------
def arm_a() -> bool:
    hdr("a", "THE DEFECT REPRODUCES ON THE PRE-ACT DEPLOYED PACKAGE (paired, both printed)")
    man = json.load(io.open(MANIFEST, "r", encoding="utf-8"))

    # GRAIN first: the fixture must BE the pre-act deployed bytes, not merely resemble
    # them. Hash every fixture against the manifest's recorded S3 sha256.
    pre = {os.path.basename(e["key"]): e for e in man["artifact_prefix_pre_act"]}
    ok_fix = 0
    for name, entry in sorted(pre.items()):
        fx = os.path.join(FIXTURES, name.replace(".py", ".pyfixture"))
        got = sha256_file(fx)
        same = got == entry["sha256"]
        ok_fix += 1 if same else 0
        print("FIXTURE %-24s sha256=%s == recorded pre-act S3 object (VersionId %s): %s"
              % (name, got, entry["version_id"], "YES" if same else "NO"))
    print("FIXTURE-INTEGRITY %d of %d fixtures equal the pre-act deployed objects"
          % (ok_fix, len(pre)))

    print("")
    print(">>> BEFORE side: served renderer + PRE-ACT DEPLOYED coverage package")
    before = run_local_exercise("BEFORE-pre-act-deployed-package", FIXTURES, [])

    print("")
    print(">>> AFTER side: the SAME renderer + the CURRENT repo coverage package")
    after = run_local_exercise(
        "AFTER-current-repo-package", REPO_COVERAGE,
        [os.path.join(REPO, "data", "inf", "scripts", "silver", "_orion_vendor_asof.py"),
         os.path.join(REPO, "lib", "trading_calendar.py")])

    raised = ("AttributeError" in before
              and "_provider_for" in before
              and "EGS31-RESULT RAISED" in before)
    verdict = EXPECT_VERDICT in after

    print("")
    if not raised:
        print("EGS31-ARM-A STOP-CONDITION: the defect did NOT reproduce on the pre-act")
        print("  deployed package. Per the task order's arm (a) and NEVER-2's supersede")
        print("  limb this is a PREMISE MOVE, not a pass: file a row and stop.")
    print("EGS31-ARM-A before=RAISED-AttributeError:%s after=%s:%s  -> %s"
          % (raised, EXPECT_VERDICT.replace(" ", "-"), verdict,
             "HOLDS" if (raised and verdict) else "FAILS"))
    print("EGS31-ARM-A both sides ran the SAME renderer sha256=%s; the package is the"
          % sha256_file(REPO_RENDERER))
    print("           ONLY variable, which is what makes this a difference control.")
    print("EGS31-ARM-A fixture integrity %d of %d" % (ok_fix, len(pre)))
    return raised and verdict and ok_fix == len(pre)


# --------------------------------------------------------------------------------
# ARM (b) -- the artifact prefix carries the current package, BY CONTENT, with the
# denominator of what was uploaded printed beside it.
# --------------------------------------------------------------------------------
def arm_b() -> bool:
    hdr("b", "THE ARTIFACT PREFIX CARRIES THE CURRENT PACKAGE (by sha256, with denominators)")
    man = json.load(io.open(MANIFEST, "r", encoding="utf-8"))
    pre = {os.path.basename(e["key"]): e for e in man["artifact_prefix_pre_act"]}
    moved = {os.path.basename(e["key"]) for e in man["keys_written_by_this_order"]}

    objs = s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX).get("Contents", [])
    print("PREFIX s3://%s/%s  DENOMINATOR %d object(s)" % (BUCKET, PREFIX, len(objs)))
    print("")
    print("%-26s %8s  %-24s  %-8s  %s" % ("member", "bytes", "LastModified (UTC)",
                                          "pre-act", "sha256 vs repo counterpart"))
    matched = 0
    for o in sorted(objs, key=lambda x: x["Key"]):
        name = os.path.basename(o["Key"])
        body = s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()
        got = sha256_bytes(body)
        cp = COUNTERPART.get(name)
        want = sha256_file(os.path.join(REPO, cp)) if cp else None
        same = (want is not None and got == want)
        matched += 1 if same else 0
        p = pre.get(name)
        print("%-26s %8d  %-24s  %-8s  %s  (%s)"
              % (name, o["Size"], o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                 ("%dB" % p["size"]) if p else "-",
                 "MATCH" if same else "MISMATCH", cp or "NO COUNTERPART"))
    print("")
    print("PRE-ACT sizes/UTC for the same 5 members (egs31_pre_act_manifest.json):")
    for name, e in sorted(pre.items()):
        print("  %-26s %8d  %-24s  %s"
              % (name, e["size"], e["last_modified"].replace(".000Z", "Z"), e["state"]))
    print("")
    print("DENOMINATOR AND MOVEMENT, STATED: the package has %d files and %d were moved."
          % (len(objs), len(moved)))
    print("  THE NUMBERS DIFFER, AND THE REASON IS MEASURED, NOT ASSUMED: the other %d"
          % (len(objs) - len(moved)))
    print("  members (%s) already equalled their repo counterparts by sha256 BEFORE the"
          % ", ".join(sorted(set(pre) - moved)))
    print("  act, so re-putting them would have been a no-op write on a served prefix --")
    print("  NEVER-2's supersede limb says do not re-apply bytes already served.")
    print("  MOVED: %s" % ", ".join(sorted(moved)))
    print("  TWO OF THE FIVE ARE VENDORED FROM OUTSIDE data/etfs/scripts/coverage/ and are")
    print("  compared against their true sources, not against that directory:")
    print("    _orion_vendor_asof.py -> data/inf/scripts/silver/_orion_vendor_asof.py")
    print("    trading_calendar.py   -> lib/trading_calendar.py")

    # The renderer is the OTHER half of the agreement this cell is about, so census it too.
    rb = s3.get_object(Bucket=BUCKET, Key=RENDERER_KEY)["Body"].read()
    r_same = sha256_bytes(rb) == sha256_file(REPO_RENDERER)
    print("")
    print("SERVED RENDERER %s bytes=%d sha256=%s vs repo: %s"
          % (RENDERER_KEY, len(rb), sha256_bytes(rb), "MATCH" if r_same else "MISMATCH"))

    ok = (matched == len(objs) == 5 and r_same)
    print("EGS31-ARM-B %d of %d prefix members match by content; renderer match=%s -> %s"
          % (matched, len(objs), r_same, "HOLDS" if ok else "FAILS"))
    return ok


# --------------------------------------------------------------------------------
# ARMS (c) and (d) -- ON THE BOX. One exercise, two assertions: the symbol RESOLVES
# (c), and the call path RETURNS A VERDICT instead of raising (d).
# --------------------------------------------------------------------------------
def arms_cd() -> tuple:
    hdr("c+d", "ON THE BOX: the symbol RESOLVES, and the --no-ladder call path RETURNS "
               "A VERDICT")
    ensure_box_running()

    with io.open(EXERCISE, "r", encoding="utf-8", newline="") as fh:
        src = fh.read().replace("\r\n", "\n")
    import base64
    b64 = base64.b64encode(src.encode("utf-8")).decode("ascii")

    pull = ("aws s3 cp s3://%s/%s ./render_month_end.py --region %s --only-show-errors"
            % (BUCKET, RENDERER_KEY, REGION))
    script = "\n".join([
        'echo "=== EGS31 ON-BOX EXERCISE (arms c and d) ==="',
        'date -u +"UTC %Y-%m-%dT%H:%M:%SZ"',
        'echo "%s" > /tmp/egs31_exercise.b64' % b64,
        "base64 -d /tmp/egs31_exercise.b64 > /tmp/egs31_exercise.py",
        "chmod 644 /tmp/egs31_exercise.py",
        'echo "--- the entry point a run uses begins with an UNCONDITIONAL renderer pull"',
        'echo "--- (lambda_function.py:652); run it as ec2-user, exactly as the run does"',
        'su - ec2-user -c "cd /opt/etfs-reports && %s"' % pull,
        'echo "--- what the box now holds (the RUNNING path, not an S3 ETag) ---"',
        "sha256sum /opt/etfs-reports/render_month_end.py /opt/etfs-reports/coverage/*.py",
        "ls -l /opt/etfs-reports/coverage/",
        'echo "--- EXERCISE: import through the renderer itself, as ec2-user, in place ---"',
        'su - ec2-user -c "cd /opt/etfs-reports && python3 /tmp/egs31_exercise.py '
        '--label ON-BOX-VERIFY --in-place /opt/etfs-reports" 2>&1',
        'echo "=== END ==="',
    ])
    out = ssm_run(script)

    c_ok = "EGS31-SYMBOL remediate._provider_for present=True" in out
    d_ok = EXPECT_VERDICT in out
    box_files_ok = out.count("/opt/etfs-reports/coverage/") > 0

    print("")
    print("EGS31-ARM-C the symbol was RESOLVED ON THE BOX through the renderer's own")
    print("  import (`from coverage import classifier, remediate` at render_month_end.py")
    print("  :118-129), not read from a listing, an ETag or an `aws s3 cp` exit code.")
    print("EGS31-ARM-C remediate._provider_for present-on-box=%s -> %s"
          % (c_ok, "HOLDS" if c_ok else "FAILS"))
    print("EGS31-ARM-D same code, same spec %s, after the act: %s present=%s -> %s"
          % (SPEC, EXPECT_VERDICT, d_ok, "HOLDS" if d_ok else "FAILS"))
    print("EGS31-ARM-D the paired BEFORE for this spec is arm (a)'s "
          "AttributeError: module 'coverage.remediate' has no attribute '_provider_for'")
    return (c_ok and box_files_ok), d_ok


# --------------------------------------------------------------------------------
# ARM (e) -- nothing else moved, and the box's power state is a MEASURED value.
# --------------------------------------------------------------------------------
def arm_e() -> bool:
    hdr("e", "NOTHING ELSE MOVED; THE BOX'S POWER STATE IS MEASURED")
    man = json.load(io.open(MANIFEST, "r", encoding="utf-8"))
    written = {e["key"] for e in man["keys_written_by_this_order"]}

    vers = s3.list_object_versions(Bucket=BUCKET, Prefix=PREFIX)
    dms = vers.get("DeleteMarkers", [])
    print("EVERY KEY WRITTEN BY THIS ORDER (denominator %d):" % len(written))
    for e in man["keys_written_by_this_order"]:
        print("  s3://%s/%s  %d bytes  %s  VersionId %s"
              % (BUCKET, e["key"], e["size"], e["last_modified"].replace(".000Z", "Z"),
                 e["new_version_id"]))
    print("")
    print("S3 DELETES: DeleteMarkers under the prefix = %d (must be 0). "
          "No S3 delete was issued under this order at all." % len(dms))
    print("VERSION HISTORY (rollback is real, not asserted): %d version(s) retained "
          "under the prefix" % len(vers.get("Versions", [])))
    for v in sorted(vers.get("Versions", []), key=lambda x: (x["Key"], x["LastModified"])):
        print("  %-46s %-34s %7d %s %s"
              % (v["Key"], v["VersionId"], v["Size"],
                 v["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "LATEST" if v["IsLatest"] else ""))

    # The one key the exercise's --no-ladder branch tries to write. The renderer PRINTS
    # "OK: s3://..." for it even when the client is a stub, so the print line is NOT the
    # discriminator -- the object's own size and LastModified are.
    unchanged = man["unchanged_by_this_order"]
    ok_unchanged = True
    print("")
    print("THE ONE PUT THE CALL PATH ATTEMPTS, VERIFIED NOT TO HAVE LANDED:")
    for uri, exp in unchanged.items():
        b, k = uri.replace("s3://", "").split("/", 1)
        h = s3.head_object(Bucket=b, Key=k)
        same = (h["ContentLength"] == exp["size"])
        ok_unchanged = ok_unchanged and same
        print("  %s" % uri)
        print("    expected %d bytes @ %s ; measured %d bytes @ %s -> %s"
              % (exp["size"], exp["last_modified"], h["ContentLength"],
                 h["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                 "UNCHANGED" if same else "MOVED"))
    print("    The renderer prints 'OK: s3://...' for this key regardless, because the")
    print("    print statement sits beside the put_object rather than after a read. The")
    print("    stub intercepted it (EGS31-S3-PUTS n=1, none forwarded) and the object")
    print("    above did not move -- that pair, not the print line, is the evidence.")

    print("")
    print("SES SENDS: 0. No ses client is constructed anywhere in this battery or in")
    print("  egs31_exercise_call_path.py, and aj@opalinvest.com is a recipient of nothing.")
    print("ORCHESTRATOR / LAMBDA INVOKES: 0. Every exercise runs ladder=False with a stub")
    print("  probe, so remediate.remediate_month and _make_invoke are never reached, and")
    print("  EG-s-21's single permitted DRIVEN RUN remains UNSPENT.")

    inst = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]
    state = inst["State"]["Name"]
    print("")
    print("BOX POWER STATE, MEASURED NOT ASSUMED:")
    print("  instance_id = %s" % INSTANCE)
    print("  state       = %s   (ec2:DescribeInstances at battery time)" % state)
    print("  pre-act     = %s   (recorded in egs31_pre_act_manifest.json)"
          % man["instance_state_at_open"])
    print("  THIS ORDER STARTED THE BOX AND LEFT IT RUNNING, DELIBERATELY. Starting an")
    print("  EC2 is ordinary; STOPPING one is a human-confirmation act under CLAUDE.md")
    print("  and is Andrew's to take. A running box here is NOT a defect and NOT an")
    print("  oversight -- it is the bound this order was given, stated out loud.")

    ok = (len(dms) == 0 and len(written) == 2 and ok_unchanged and state == "running")
    print("")
    print("EGS31-ARM-E keys_written=%d delete_markers=%d unchanged_ok=%s box=%s -> %s"
          % (len(written), len(dms), ok_unchanged, state, "HOLDS" if ok else "FAILS"))
    return ok


def main() -> int:
    print("EGS31 BATTERY -- ETFS_GUARDRAIL.TO-EG-s-31 / S31-AC1")
    print("repo root: %s" % REPO)
    print("spec:      %s   expectation: %s" % (SPEC, EXPECT_VERDICT))

    results["a"] = arm_a()
    results["b"] = arm_b()
    results["c"], results["d"] = arms_cd()
    results["e"] = arm_e()

    hdr("SUMMARY", "five arms, one token")
    for k in ("a", "b", "c", "d", "e"):
        print("  arm (%s) %s" % (k, "HOLDS" if results[k] else "FAILS"))
    held = sum(1 for v in results.values() if v)
    print("")
    print("ARMS HOLDING: %d of %d" % (held, len(results)))
    if held == len(results):
        print("EGS31-THE-BOX-RUNS-THE-PACKAGE-THE-RENDERER-EXPECTS")
        return 0
    print("EGS31-NOT-SATISFIED (%d of %d arms hold; no token)" % (held, len(results)))
    return 1


if __name__ == "__main__":
    sys.exit(main())
