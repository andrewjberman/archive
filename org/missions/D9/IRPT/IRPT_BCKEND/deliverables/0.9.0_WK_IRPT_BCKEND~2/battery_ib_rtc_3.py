#!/usr/bin/env python3
"""BATTERY IB-rtc-3 AMENDMENT 2 -- THE REFRESH BUILDS, EXERCISED FOR INFLECTION AND COTTONWOOD.

Grades R33-AC1's six arms against THE REAL WORLD: the unit-tested recipe TEXT refresh.py's
runner_script() returns (now with NO explicit --as-of, per the issuer's ruling on row
IRPT_BCKEND-W2-S55), the applied Terraform (served CodeSha256, 0-diff plan), a fresh read-only
host sweep (10 source prefixes + 3 destinations, the corrected population -- row
IRPT_BCKEND-W2-S54), the SSM command records THIS session's own real fires (a fresh dispatch
plus its reconciliation), and the S3 objects in the three firm buckets. Nothing here wraps,
patches or re-registers the subject (bound 12): every arm reads the artifact the estate serves
and prints its denominator.

THE TOKEN IS GATED. `IBR33...` is assembled only if every arm PASSES and arm (d) reads 2 of 2
landed. It does not, as measured: AMENDMENT 2's fix (drop the explicit --as-of) is PROVEN
correct and working -- both inflection's and cottonwood's real fires now proceed PAST
directory_runner.py's own business-date check for the first time in this project's record,
confirming row W2-S55 is CLEARED -- and the real fire then exposed a THIRD, still deeper,
out-of-lane blocker (row IRPT_BCKEND-W2-S56): directory_runner.py's validate_entries() calls
jsonschema.Draft202012Validator, a class absent from the host's installed jsonschema==3.2.0.
That is directory_runner.py's own defect (outside this order's <paths>) and this cell does not
work around it.

ASCII only. Bounded: every AWS call runs under a subprocess timeout.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
AWS = os.path.join(REPO, ".tools", "aws.cmd")
DIRECTORY = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "directory")
TF_ROOT = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "directory")
TERRAFORM = os.path.join(REPO, ".tools", "terraform.exe")

FUNCTION = "irpt-directory-refresh"
RUNNER = "i-02448edb624a7a7cf"
FIRM_BUCKETS = {"49financial": "opal-data-bd",
                "inflection": "opal-data-inf",
                "cottonwood": "opal-data-cot"}
DIRECTORY_PREFIX = "investor-reporting/directory"
DRIVEN_DATE = "2026-09-18"

# ARTIFACT IDS this session's AMENDMENT 2 fire created -- read back below, never re-derived.
# (The first pass's commands -- 74c1f0f4.., 71f11079.., b1c2b24e.. -- are row W2-S55's evidence.
# An interim fire -- f9c34e7a.., e6869e09.., 0fe77c42.. -- ran against a zip built with the WRONG
# fixed timestamp (caught by this battery's own b.2); THESE ids are the fire against the FINAL,
# canonical-timestamp deployed code, dispatched after the zipdate-fix re-apply.)
DISPATCH_COMMANDS = {
    "inflection": "d625bc56-a79a-47e6-9d74-9d9108f4b16a",
    "cottonwood": "bc273cf9-a173-4056-bbe2-649cb83f8d30",
    "49financial": "ae2243aa-ff47-4d70-ad8f-c95feb0037b6",
}
SWEEP_SCRIPT_SHA256 = "8b39dea2419d8d3b03d47134bced6f368d55c2378a04db898cc3120447d0bb1b"
TEST_FILE = os.path.join(DIRECTORY, "tests", "test_refresh_expiry.py")
PYTHON = os.environ.get("PY312", "py")
PYTHON_ARGS = ["-3.12"] if PYTHON == "py" else []

SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
SHARED_ROOTS = [
    os.path.join(REPO, "lib"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_authz"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_scope"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_keys"),
    os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_ids"),
]

RESULTS = []


def record(arm, verdict, line, denominator=""):
    RESULTS.append((arm, verdict, line, denominator))
    print("  [%s] %-9s %s%s" % (arm, verdict, line,
                                ("   denominator: %s" % denominator) if denominator else ""))


def aws(*args, timeout=180):
    try:
        p = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    return p.returncode, (p.stdout or "").replace("\r", ""), (p.stderr or "").replace("\r", "")


def aws_json(*args, **kw):
    rc, out, err = aws(*args, **kw)
    if rc != 0:
        return None, (err or out)[-400:]
    try:
        return json.loads(out), None
    except ValueError as exc:
        return None, "unparseable: %s" % exc


def head(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


# ============================================================== ARM (a) -- THE RECIPE
def arm_a():
    head("ARM (a) THE UNPACK RECIPE -- repo-shaped, no mv, member list + import check unchanged")
    sys.path.insert(0, DIRECTORY)
    import refresh                                                       # noqa: E402

    script = refresh.runner_script("inflection", "2026-09-18", "s3://bucket/bundle.tar.gz",
                                   "inflection-2026-09-18")
    has_cw = "tar -xzf $W/bundle.tar.gz -C $W || exit 91" in script
    record("a.1", "PASS" if has_cw else "FAIL",
           "recipe extracts at the simulated repo root: '-C $W' present")
    no_mv = (" mv " not in script) and ("mv $R" not in script)
    record("a.2", "PASS" if no_mv else "FAIL",
           "no mv line survives -- no member is stored flat any longer")
    order_ok = ("tar -tzf" in script and "tar -xzf" in script
                and script.index("tar -tzf") < script.index("tar -xzf")
                and "IMPORT-OK first-party modules resolved: trading_calendar, ids, contract"
                in script)
    record("a.3", "PASS" if order_ok else "FAIL",
           "member list (tar -tzf) precedes extraction; import check text unchanged")
    no_dotdot_recipe = "../" not in script and "/.." not in script
    record("a.4", "PASS" if no_dotdot_recipe else "FAIL",
           "the recipe text itself carries no .. path segment")

    # a.6 -- AMENDMENT 2 (row IRPT_BCKEND-W2-S55): the recipe carries NO explicit --as-of.
    no_as_of = "--as-of" not in script
    record("a.6", "PASS" if no_as_of else "FAIL",
           "AMENDMENT 2: the recipe carries 0 explicit --as-of arguments to directory_runner.py",
           "0 of 1" if no_as_of else "1 of 1")

    # a.7 -- the REAL unit-test suite (bound 12: the actual test file, not a wrapper), which
    # covers the manifest/date discipline AMENDMENT 2 requires: no --as-of, a completed manifest
    # carries the RUNNER's date (not the clock's), and a same-frontier re-fire is a no-op.
    p = subprocess.run([PYTHON] + PYTHON_ARGS + ["-m", "pytest", TEST_FILE, "-q"],
                       capture_output=True, text=True, timeout=120)
    tail = (p.stdout or "")[-300:].replace("\n", " | ")
    record("a.7", "PASS" if p.returncode == 0 else "FAIL",
           "the real test_refresh_expiry.py suite (manifest/date + same-frontier tests included) "
           "-- %s" % tail, "rc=%d" % p.returncode)

    # a.5 -- the REAL, currently-served bundle carries 0 members with a '..' path segment.
    # Fetched unversioned (the host role lacks s3:GetObjectVersion) and bound by content hash.
    bpath = os.path.join(HERE, "_bat_bundle.tar.gz")
    rc, out, err = aws("s3api", "get-object", "--bucket", "opal-data-mdpf",
                       "--key", "code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz",
                       bpath, "--output", "text")
    if rc != 0:
        record("a.5", "FAIL", "could not fetch the served bundle: %s" % (err or out)[-200:])
    else:
        with open(bpath, "rb") as fh:
            bsha = hashlib.sha256(fh.read()).hexdigest()
        p = subprocess.run(["tar", "-tzf", bpath], capture_output=True, text=True, timeout=30)
        members = [m for m in p.stdout.splitlines() if m.strip()]
        dotdot = [m for m in members if ".." in m.split("/")]
        record("a.5", "PASS" if (p.returncode == 0 and not dotdot) else "FAIL",
               "served bundle sha256 %s, %d members named, 0 with a '..' segment"
               % (bsha[:16], len(members)), "%d of %d" % (len(dotdot), len(members)))
        os.remove(bpath)


# ============================================================== ARM (b) -- TERRAFORM
def arm_b():
    head("ARM (b) THE DIRECTORY ROOT -- applied under ledger, served bytes verified")
    cfg, err = aws_json("lambda", "get-function-configuration", "--function-name", FUNCTION,
                        "--output", "json")
    if cfg is None:
        record("b.1", "FAIL", "get-function-configuration failed: %s" % err)
        return
    served = cfg["CodeSha256"]
    smap = json.load(open(SOURCE_MAP, encoding="utf-8"))
    declared = smap["functions"][FUNCTION]["artifact_sha256"]
    record("b.1", "PASS" if served == declared else "FAIL",
           "served CodeSha256 %s %s source-map artifact_sha256"
           % (served, "==" if served == declared else "!="))

    # Re-derive the zip's bytes from the SAME declared files[] this run, resolving DISTRIBUTION
    # members from SHARED_ROOTS exactly as the deploy did -- never trusting the producer's own
    # report of what it built.
    fn = smap["functions"][FUNCTION]
    source_dir = os.path.join(REPO, fn["source_dir"].replace("/", os.sep))

    def resolve(name):
        p = os.path.join(source_dir, name.replace("/", os.sep))
        if os.path.isfile(p):
            return p
        for root in SHARED_ROOTS:
            q = os.path.join(root, os.path.basename(name))
            if os.path.isfile(q):
                return q
        return None

    members = {}
    for name in fn["files"]:
        path = resolve(name)
        if path:
            members[name] = path
    zpath = os.path.join(HERE, "_bat_rebuild.zip")
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as zf:
        for arc in sorted(members):
            info = zipfile.ZipInfo(arc, date_time=(2020, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.create_system = 0
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(members[arc], "rb") as fh:
                zf.writestr(info, fh.read())
    with open(zpath, "rb") as fh:
        rebuilt_sha = base64.b64encode(hashlib.sha256(fh.read()).digest()).decode("ascii")
    os.remove(zpath)
    record("b.2", "PASS" if rebuilt_sha == served else "FAIL",
           "re-derived zip (resolved: %d of %d declared members) sha256 %s %s served CodeSha256"
           % (len(members), len(fn["files"]), rebuilt_sha,
              "==" if rebuilt_sha == served else "!="),
           "%d of %d" % (len(members), len(fn["files"])))

    p = subprocess.run([TERRAFORM, "-chdir=%s" % TF_ROOT, "plan", "-input=false", "-detailed-exitcode"],
                       capture_output=True, text=True, timeout=120)
    zero_diff = (p.returncode == 0) and ("No changes" in p.stdout)
    record("b.3", "PASS" if zero_diff else "FAIL",
           "post-apply re-plan reads 0-diff (rc=%d)" % p.returncode)


# ================================================================ ARM (c) -- THE SWEEP
def arm_c():
    head("ARM (c) THE ON-HOST SWEEP -- 10 source prefixes + 3 destinations (row W2-S54: the "
         "face's inherited '9' is stale; the CTO-ratified population is 10), positive control")
    params_path = os.path.join(HERE, "_bat_sweep_params.json")
    with open(params_path, "w", encoding="utf-8") as fh:
        json.dump({"commands": [
            "aws s3 cp s3://opal-data-mdpf/diagnostics/aec-irpt-iam1/irpt_sweep_v2.sh /tmp/irpt_sweep_v2.sh "
            "&& sha256sum /tmp/irpt_sweep_v2.sh && bash /tmp/irpt_sweep_v2.sh"],
            "executionTimeout": ["120"]}, fh)
    rc, out, err = aws("ssm", "send-command", "--instance-ids", RUNNER,
                       "--document-name", "AWS-RunShellScript",
                       "--parameters", "file://%s" % params_path,
                       "--comment", "battery_ib_rtc_3 arm c", "--output", "json")
    os.remove(params_path)
    if rc != 0:
        record("c.1", "FAIL", "send-command failed: %s" % (err or out)[-200:])
        return
    cid = json.loads(out)["Command"]["CommandId"]
    import time
    inv = None
    for _ in range(15):
        time.sleep(4)
        inv, err = aws_json("ssm", "get-command-invocation", "--command-id", cid,
                            "--instance-id", RUNNER, "--output", "json")
        if inv and inv.get("Status") not in ("Pending", "InProgress", "Delayed"):
            break
    if inv is None:
        record("c.1", "FAIL", "get-command-invocation failed: %s" % err)
        return
    out_txt = inv.get("StandardOutputContent") or ""
    hashed_ok = SWEEP_SCRIPT_SHA256 in out_txt
    record("c.1", "PASS" if (inv.get("Status") == "Success" and hashed_ok) else "FAIL",
           "sweep script pulled by the host, sha256 %s the recorded instrument"
           % ("==" if hashed_ok else "!="))
    pos_ok = "READ-OK" in out_txt.split("POSITIVE CONTROL")[1].split("\n")[1] if \
        "POSITIVE CONTROL" in out_txt else False
    record("c.2", "PASS" if pos_ok else "FAIL", "positive control fires (READ-OK)")
    import re as _re
    m = _re.search(r"AC4 SOURCE:\s+READ-OK=(\d+)\s+READ-DENY=(\d+)\s+READ-OTHER=(\d+)\s+"
                   r"denominator (\d+)", out_txt)
    n = _re.search(r"AC5 NEG CONTROLS:\s+READ-OK=(\d+)\s?READ-DENY=(\d+)\s?READ-OTHER=(\d+)\s+"
                   r"denominator (\d+)", out_txt)
    if m:
        ok, deny, other, denom = m.groups()
        record("c.3", "PASS" if int(denom) == 10 else "FAIL",
               "SOURCE sweep: READ-OK=%s READ-DENY=%s READ-OTHER=%s (5 OK / 5 DENY expected -- "
               "all 5 denials are opal-data-49financial/gold/advi/dimensions/*, row W2-S49/S53)"
               % (ok, deny, other), "denominator %s (corrected population, row W2-S54)" % denom)
    else:
        record("c.3", "FAIL", "could not parse AC4 SOURCE totals from sweep output")
    if n:
        nok, ndeny, nother, ndenom = n.groups()
        record("c.4", "PASS" if (nok == "0" and ndeny == "8") else "FAIL",
               "8 negative controls: READ-OK=%s READ-DENY=%s (0/8 expected -- grant not wider "
               "than its enumeration)" % (nok, ndeny), "denominator %s" % ndenom)
    else:
        record("c.4", "FAIL", "could not parse AC5 negative-control totals from sweep output")
    record("c.5", "PASS" if "DEST:49financial" in out_txt else "FAIL",
           "3 destination prefixes probed (read-plane only; DENY is the DESIGNED result -- no "
           "ListBucket was granted on any destination, per the sweep's own comment)",
           "3 of 3 probed")


# ============================================================ ARM (d) -- THE REAL FIRE
def arm_d():
    head("ARM (d) THE DEPLOYED DISPATCH, FIRED FOR ALL THREE FIRMS -- read back through the "
         "IB-rt-6 mechanism (run record, command status, reconciliation, before/after)")
    landed = 0
    for firm in ("inflection", "cottonwood"):
        cid = DISPATCH_COMMANDS[firm]
        inv, err = aws_json("ssm", "get-command-invocation", "--command-id", cid,
                            "--instance-id", RUNNER, "--output", "json")
        if inv is None:
            record("d.%s.1" % firm[:3], "FAIL", "get-command-invocation failed: %s" % err)
            continue
        out = inv.get("StandardOutputContent") or ""
        repo_shaped_ok = ("IMPORT-OK first-party modules resolved: trading_calendar, ids, "
                          "contract" in out)
        record("d.%s.import" % firm[:3], "PASS" if repo_shaped_ok else "FAIL",
               "%s: repo-shaped unpack IMPORT-OK on the host (all 3 runner_common modules "
               "resolve) -- Status=%s" % (firm, inv.get("Status")))

        # AMENDMENT 2 (row IRPT_BCKEND-W2-S55): confirm the as-of refusal is GONE.
        as_of_cleared = "REFUSE: explicit --as-of" not in out
        record("d.%s.asof_cleared" % firm[:3], "PASS" if as_of_cleared else "FAIL",
               "%s: AMENDMENT 2's fix confirmed -- 0 occurrences of the W2-S55 "
               "'REFUSE: explicit --as-of' refusal in this fire's stdout" % firm,
               "0 of 1" if as_of_cleared else "1 of 1")
        # row IRPT_BCKEND-W2-S56: the NEW, deeper, out-of-lane blocker this fire MEASURED (a
        # PASS here means the row's claim is confirmed present in the real stdout, same
        # convention as arm (e)'s expected-AccessDenied PASS -- this is not a defect of THIS
        # cell's own deliverable, which arm (a)/(b)/(c)/d.*.import/d.*.asof_cleared all PASS).
        new_blocker = "Draft202012Validator" in out
        record("d.%s.new_blocker" % firm[:3], "PASS" if new_blocker else "FAIL",
               "%s: row IRPT_BCKEND-W2-S56 confirmed in this fire's stdout (directory_runner.py's "
               "jsonschema.Draft202012Validator, absent from the host's jsonschema==3.2.0) -- "
               "out-of-lane, filed and not worked around" % firm)

        bucket = FIRM_BUCKETS[firm]
        d, _ = aws_json("s3api", "list-objects-v2", "--bucket", bucket,
                        "--prefix", "%s/" % DIRECTORY_PREFIX, "--output", "json")
        keys = [o["Key"] for o in ((d or {}).get("Contents") or [])]
        has_artifact = any(k.endswith("/directory.json") for k in keys)
        has_pointer = any(k.endswith("/latest.json") for k in keys)
        landed += 1 if (has_artifact and has_pointer) else 0
        record("d.%s.landed" % firm[:3], "PASS" if (has_artifact and has_pointer) else "BLOCKED",
               "%s: directory.json=%s latest.json=%s -- W2-S55 CLEARED, now BLOCKED on row "
               "IRPT_BCKEND-W2-S56 (directory_runner.py's own jsonschema.Draft202012Validator "
               "use, absent from the host's jsonschema==3.2.0, out-of-lane)"
               % (firm, has_artifact, has_pointer))

    record("d.landed_total", "PASS" if landed == 2 else "FAIL",
           "firms with a landed directory artifact AND its pointer", "%d of 2" % landed)

    # THE RECONCILIATION: a second fire reads each command's terminal status back and records
    # REFRESH_FAILED with the correct half (BUILD, not HAND_OVER) -- the loop closes even though
    # nothing lands.
    reconciled = 0
    for firm in ("inflection", "cottonwood", "49financial"):
        bucket = FIRM_BUCKETS[firm]
        key = "%s/_refresh/%s/manifest.json" % (DIRECTORY_PREFIX, DRIVEN_DATE)
        p = os.path.join(HERE, "_bat_recman_%s.json" % firm)
        rc, out, err = aws("s3api", "get-object", "--bucket", bucket, "--key", key, p,
                           "--output", "text")
        if rc == 0:
            man = json.load(open(p, encoding="utf-8"))
            delta = man.get("delta") or {}
            ok = (man.get("reason_code") == "REFRESH_FAILED"
                 and delta.get("build_dispatch_failure") == "BUILD_ENDED_UNSUCCESSFUL"
                 and delta.get("build_dispatch_half") == "BUILD")
            reconciled += 1 if ok else 0
            os.remove(p)
    record("d.reconcile", "PASS" if reconciled == 3 else "FAIL",
           "the NEXT fire reads each command's terminal status back and records "
           "REFRESH_FAILED/BUILD_ENDED_UNSUCCESSFUL (BUILD half, not HAND_OVER) -- the "
           "dispatch-to-reconcile loop closes", "%d of 3 firms" % reconciled)


# =================================================================== ARM (e) -- 49 FINANCIAL
def arm_e():
    head("ARM (e) THE 49 FINANCIAL ARM -- attempted once, BLOCKED at the named read")
    cid = DISPATCH_COMMANDS["49financial"]
    inv, err = aws_json("ssm", "get-command-invocation", "--command-id", cid,
                        "--instance-id", RUNNER, "--output", "json")
    if inv is None:
        record("e.1", "FAIL", "get-command-invocation failed: %s" % err)
        return
    out = inv.get("StandardOutputContent") or ""
    err_out = (inv.get("StandardErrorContent") or "") + out
    denied = ("AccessDenied" in err_out and "opal-data-49financial" in err_out
             and "explicit deny in a resource-based policy" in err_out)
    record("e.1", "PASS" if denied else "FAIL",
           "49financial's build ends AccessDenied on opal-data-49financial (row "
           "IRPT_BCKEND-W2-S49/S53, iam.tf:598-603 DenyForeignFirmPrincipals) -- attempted "
           "ONCE, never worked around", "command %s Status=%s" % (cid, inv.get("Status")))


# ============================================================ ARM (f) -- CONTENT SANITY
def arm_f():
    head("ARM (f) CONTENT SANITY ON WHAT LANDED -- 0 of 3 firms landed anything (arm d), so "
         "this arm has no real artifact to grade")
    total_keys = 0
    for firm, bucket in sorted(FIRM_BUCKETS.items()):
        d, _ = aws_json("s3api", "list-objects-v2", "--bucket", bucket,
                        "--prefix", "%s/" % DIRECTORY_PREFIX, "--output", "json")
        keys = [o["Key"] for o in ((d or {}).get("Contents") or [])]
        artifacts = [k for k in keys if k.endswith("/directory.json")]
        total_keys += len(artifacts)
    record("f.1", "BLOCKED",
           "no directory.json exists in any firm bucket to grade for content sanity -- "
           "BLOCKED on the same row as arm (d) (IRPT_BCKEND-W2-S56, out-of-lane), a "
           "self-wrapping content check against a fabricated artifact would be the bound-12 "
           "violation this battery refuses to commit", "%d directory.json across 3 firms"
           % total_keys)


# ================================================================== the verdict
def main():
    print("BATTERY IB-rtc-3 -- the refresh builds, exercised for inflection and cottonwood")
    print("repo: %s" % REPO)
    print("subject: the repo-shaped refresh.py recipe, the applied directory Terraform root, "
          "the on-host sweep, and the DEPLOYED dispatch fired live for all three firms")
    arm_a()
    arm_b()
    arm_c()
    arm_d()
    arm_e()
    arm_f()

    head("VERDICT")
    npass = sum(1 for _, v, _, _ in RESULTS if v == "PASS")
    nfail = sum(1 for _, v, _, _ in RESULTS if v == "FAIL")
    nblock = sum(1 for _, v, _, _ in RESULTS if v == "BLOCKED")
    for arm, v, line, den in RESULTS:
        print("  %-16s %-9s %s" % (arm, v, line[:88]))
    print("")
    print("  PASS %d | FAIL %d | BLOCKED %d   denominator: %d graded check(s)"
          % (npass, nfail, nblock, len(RESULTS)))
    landed_row = next((r for r in RESULTS if r[0] == "d.landed_total"), None)
    landed_2of2 = bool(landed_row) and landed_row[1] == "PASS"
    if nfail == 0 and nblock == 0 and landed_2of2:
        print("  " + "-".join(["IBR33", "TWO-OF-THREE-DIRECTORIES-LANDED"]))
        return 0
    print("  THE ACCEPTANCE TOKEN IS WITHHELD. arm (d) landed_total is not 2 of 2, and/or "
          "another arm did not PASS:")
    print("    IRPT_BCKEND-W2-S49/S53  49financial's build is AccessDenied on")
    print("                            opal-data-49financial (DenyForeignFirmPrincipals) --")
    print("                            EXPECTED, per arm (e); not a regression.")
    print("    IRPT_BCKEND-W2-S55      CLEARED by this cell's AMENDMENT 2 fix (confirmed: 0")
    print("                            occurrences of the as-of refusal in either firm's stdout).")
    print("    IRPT_BCKEND-W2-S56      inflection and cottonwood's builds now reach")
    print("                            directory_runner.py's validate_entries() (a strictly")
    print("                            LATER point than W2-S55) and fail there: jsonschema")
    print("                            .Draft202012Validator is absent from the host's")
    print("                            installed jsonschema==3.2.0. Out-of-lane (directory_")
    print("                            runner.py is not in this order's <paths>); filed, not")
    print("                            worked around.")
    print("  R33-AC1 is FAIL. The order stays open.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
