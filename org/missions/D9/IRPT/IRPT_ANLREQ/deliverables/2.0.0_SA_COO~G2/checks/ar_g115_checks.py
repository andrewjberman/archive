"""IRPT_ANLREQ AR-g-115 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python -I ar_g115_checks.py verify <stage folder> <record json> [<status CodeSha256>]   re-derives the release-35 irpt-status BUILD from the zips and the git objects,
                                                                    trusting nothing in the record: each zip's sha256 and CodeSha256, its
                                                                    members against the census build at the pin, the delta against the
                                                                    census build at the r33 build pin (exactly durable_job.py, owned_status.py
                                                                    and status.py), no live read claimed
    python -I ar_g115_checks.py scope <base ref> <worker folder> <order path>   the branch changed only the worker's folder, its order and
                                                                    the issuer's own files (merge-base diff)

Prints one RESULT line: AR-G115-OK / AR-G115-FAIL or AR-G115-SCOPE-OK / AR-G115-SCOPE-FAIL; rc 0 only on OK. ASCII only.
"""
import base64
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

CENSUS = "infra/aws/lambda/ci/release-census.py"
STATUS = "irpt-status"
# The live irpt-status package is the release-33 build (AQ2 msg 8976), built from the pin of AR-g-102's merge.
STATUS_BASELINE = "927337a741f40a83e7daa9e09154436a813b05dd"
EXPECT = {STATUS: ["durable_job.py", "owned_status.py", "status.py"]}
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")


def fail(why):
    print("AR-G115-FAIL " + why)
    sys.exit(1)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load_census():
    spec = importlib.util.spec_from_file_location("release_census", CENSUS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify(stage, record_path, expect=None):
    stage = Path(stage)
    rec = json.loads(Path(record_path).read_text(encoding="utf-8"))
    if rec.get("schema") != "irpt-r35l-build.v1" or rec.get("live_read") is not False:
        fail("the record is not an irpt-r33-build.v1 record, or claims a live read")
    pin = rec["pin"]
    if not re.fullmatch(r"[0-9a-f]{40}", pin) or subprocess.run(["git", "cat-file", "-e", pin + "^{commit}"]).returncode != 0:
        fail("the pin is not a commit: " + pin[:10])
    if set(rec["functions"]) != {STATUS}:
        fail("the record does not hold exactly irpt-status")
    census = load_census()
    root = Path.cwd()
    summary = []
    for function in (STATUS,):
        item = rec["functions"][function]
        data = (stage / item["zip"]).read_bytes()
        if sha(data) != item["zip_sha256"] or base64.b64encode(hashlib.sha256(data).digest()).decode() != item["code_sha256"]:
            fail("%s: the zip's hashes differ from the record" % function)
        if item.get("builds_identical") is not True:
            fail("%s: the record does not say the two builds were identical" % function)
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            built = {i.filename: sha(zf.read(i.filename)) for i in zf.infolist() if not i.is_dir()}
        if built != item["member_sha256"] or len(built) != item["members"]:
            fail("%s: the record's member table differs from the zip" % function)
        want_pin = {k: sha(v) for k, v in census.build_members(root, function, pin).items()}
        if built != want_pin:
            fail("%s: the zip's members differ from the census build at the pin: %s" % (function, sorted(set(built) ^ set(want_pin))[:6]))
        deployed = STATUS_BASELINE
        if item.get("deployed_commit") != deployed or subprocess.run(["git", "merge-base", "--is-ancestor", deployed, pin]).returncode != 0:
            fail("%s: the record's deployed commit is not the named baseline, or is not an ancestor of the pin" % function)
        want_base = {k: sha(v) for k, v in census.build_members(root, function, deployed).items()}
        delta = sorted(k for k in set(built) | set(want_base) if built.get(k) != want_base.get(k))
        if delta != EXPECT[function] or delta != item["delta_vs_deployed_commit"]:
            fail("%s: the delta against the last deployed commit is %s, expected %s" % (function, delta, EXPECT[function]))
        if expect is not None and item["code_sha256"] != expect[function]:
            fail("%s: the CodeSha256 %s is not the issuer's trial build's %s (a second build of the same pin must be identical)" % (function, item["code_sha256"], expect[function]))
        summary.append("%s members=%d delta=%d code_sha256=%s" % (function, len(built), len(delta), item["code_sha256"]))
    print("AR-G115-OK " + "; ".join(summary))
    return 0


def scope(base_ref, folder, order):
    out = subprocess.run(["git", "diff", "--name-only", base_ref + "...HEAD"], capture_output=True, text=True)
    diff = out.stdout.split()
    stray = [p for p in diff if not p.startswith(folder.rstrip("/") + "/") and p != order and not p.startswith(ISSUER)
             and p != "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md"]
    if out.returncode != 0 or stray:
        print("AR-G115-SCOPE-FAIL rc=%d stray=%s" % (out.returncode, str(stray[:5])))
        return 1
    print("AR-G115-SCOPE-OK %d changed paths, none outside the grant" % len(diff))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "verify":
        sys.exit(verify(sys.argv[2], sys.argv[3]))
    if len(sys.argv) == 5 and sys.argv[1] == "verify":
        sys.exit(verify(sys.argv[2], sys.argv[3], {STATUS: sys.argv[4]}))
    if len(sys.argv) == 5 and sys.argv[1] == "scope":
        sys.exit(scope(sys.argv[2], sys.argv[3], sys.argv[4]))
    print("usage: ar_g115_checks.py verify <stage> <record> [<expected status CodeSha256>] | scope <base ref> <worker folder> <order path>")
    sys.exit(2)
