#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtc-9 acceptance battery -- R39-AC1, four graded arms.

Prints IBR39-RUNNERS-VALIDATE-UNDER-HOST-JSONSCHEMA only when arms (a)-(d) ALL hold.

The defect (row W2-S56): directory_runner.py and holdings_snapshot.py called jsonschema 4.x-only API
(`Draft202012Validator`, `ValidationError.json_path`); the MDPF host runs 3.2.0. The fix is committed at
de4e176cc3 and the bundle re-minted under change-management entry irpt-bckend-rtc9-jsonschema-mint
(opened 163c3bf7b0, closed dfdd58a2a6). BOUND TO IDENTITY for a later grader: the minted and pre-cell
objects by VersionId, the tree by the commits that carried it.

WHAT THIS BATTERY IS NOT (bound 12): it wraps nothing it grades. The AST walk reads the SERVED tarball's
members; the suite is the directory's own tests, run as written; the host arm imports the real served
members and calls the real validators on the host's own interpreter. What the host arm SUPPLIES is named
and hash-bound: the four fixtures, the HoldingsSnapshot contract the bundle does not carry (row S71), and
the pre-cell tarball, shipped through SSM because the host role has no s3:GetObjectVersion.

Graded arms:
  (a) AST WALK   the served tarball's .py members: 0 attribute references to the three 4.x-only names,
                 denominator printed; the 2020-12 name appears only as a string in the tolerant lookup.
  (b) SUITE      the directory's whole test suite N of N, collected == passed; the fallback branch run under
                 the mutant environment; the hard-coded mutant FAILING it.
  (c) RE-MINT    the minted identity; the closure re-derived with the diff against IB-rtc-8's 8; the negative
                 control against 479af04c DIFFERS; both edited members' tarball bytes == the blobs; the other
                 stamps unchanged; the distribution legs consistent 3 of 3 with 0 commits to them.
  (d) HOST       jsonschema version printed; IMPORT-OK for every member; valid fixtures accepted 2 of 2,
                 invalid refused 2 of 2 with paths; the pre-cell members raise AttributeError on both calls
                 (the positive control of the defect), same interpreter, same command; 0 network events.
"""
from __future__ import annotations

import ast
import base64
import datetime as dt
import hashlib
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import tarfile
import tempfile
import time

WS = pathlib.Path(__file__).resolve().parents[7]
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(WS / ".tools"))
sys.path.insert(0, str(HERE))
import safe_deploy_core as sdc          # noqa: E402  the guard's declaration
import consistency_ib_rtc_2 as cons     # noqa: E402  the R-45 two-leg check

BUNDLE = "investor_reporting"
PKG = "data/assets/scripts/gold/investor_reporting"
RUNNER = PKG + "/directory_runner.py"
HOLDINGS = PKG + "/holdings_snapshot.py"
EDITED = [RUNNER, HOLDINGS]
TEST_FILE = PKG + "/tests/test_runner_jsonschema_tolerance.py"
HS_CONTRACT = "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json"
FIXTURE_DIR = "infra/aws/lambda/investor-reporting/_contracts/fixtures"
FIXTURES = ["DirectoryEntry.valid", "DirectoryEntry.invalid", "HoldingsSnapshot.valid", "HoldingsSnapshot.invalid"]
FOUR_X_ONLY = ("Draft202012Validator", "Draft201909Validator", "json_path")
INSTANCE = "i-02448edb624a7a7cf"
REGION = "us-east-1"
CUT = "ea3fa54c2b"                    # the order's cut
CODE_COMMIT = "de4e176cc3"            # the two runner edits + the test
MINT_COMMIT = "163c3bf7b0"            # the tree the guard packed (the ledger OPEN commit)
CLOSE_COMMIT = "dfdd58a2a6"           # the ledger close
CELL_RANGE = "%s..%s" % (CUT, CLOSE_COMMIT)
MINTED = {"etag": "4c942a76f990874838e33e37f24ed69a", "version": "0XLkiPt4wljdniLnF2fkPKN4qAIkjUbc"}
PRE_CELL = {"etag": "479af04c0a3a1eb6651707b340df9926", "version": "q8myxeHdNw48w1uDb7YTcBh8DHV9TzU2"}
LOOSE_LEFT_BY_IB_RTC_2 = {
    "data/assets/scripts/gold/runners_49f/runner_common.py": "jnnxQWbVT_lx6WlJu8HbVXNjQJpYK00w",
    "data/cot/scripts/gold/runners_cot/runner_common.py": "bobsNlnmKIjMyMW8PHxiQVeJCXPIJmOs",
    "data/inf/scripts/gold/runners_inf/runner_common.py": "z_WDDmx6004thBhXbT0uBvsDkNibZQF8",
}
IB_RTC_8_CLOSURE = sorted([
    RUNNER,
    "data/assets/scripts/gold/runners_49f/runner_common.py",
    "data/cot/scripts/gold/runners_cot/runner_common.py",
    "data/firm_registry.json",
    "data/inf/scripts/gold/runners_inf/runner_common.py",
    "infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json",
    "infra/aws/lambda/investor-reporting/_ids/ids.py",
    "lib/trading_calendar.py",
])

results = []


def run(cmd, timeout=300, cwd=None, env=None):
    try:
        p = subprocess.run(cmd, cwd=str(cwd or WS), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout, env=env)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ss" % timeout


def git_bytes(ref, rel):
    p = subprocess.run(["git", "show", "%s:%s" % (ref, rel)], capture_output=True, cwd=str(WS), timeout=30)
    return p.stdout if p.returncode == 0 else None


def blob_id(ref, rel):
    _, out = run(["git", "rev-parse", "%s:%s" % (ref, rel)])
    return out.strip()


def hash_object(data):
    with tempfile.TemporaryDirectory() as td:
        f = pathlib.Path(td) / "member"
        f.write_bytes(data)
        _, out = run(["git", "hash-object", "--no-filters", str(f)])
    return out.strip()


def record(arm, ok, detail):
    results.append((arm, ok is True))
    print("  %-5s %s" % ({True: "PASS", False: "FAIL", None: "N/E"}[ok], arm))
    for line in detail:
        print("        " + line)
    print()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def untar(body):
    with tarfile.open(fileobj=io.BytesIO(body), mode="r:gz") as tf:
        return {m.name: tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}


print("R39-AC1 battery -- IRPT_BCKEND.TO-IB-rtc-9, the runners validate under the host's jsonschema")
print("workspace: %s" % WS)
_, head = run(["git", "rev-parse", "--short=10", "HEAD"])
print("branch tip: %s   code: %s   mint commit: %s   run at %s" % (
    head.strip(), CODE_COMMIT, MINT_COMMIT, dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
print()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

import boto3                                     # noqa: E402
s3 = boto3.client("s3", region_name=REGION)
b = sdc.find_bundle(BUNDLE)[2]
by_path = {s["repo_path"]: n for n, s in b["members"].items()}
by_spec = {s["repo_path"]: s for s in b["members"].values()}
cur = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=MINTED["version"])
body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=MINTED["version"])["Body"].read()
served = untar(body)
pre_head = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=PRE_CELL["version"])
pre_body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=PRE_CELL["version"])["Body"].read()
pre_served = untar(pre_body)

# ============================================================ (a) the AST walk, over the SERVED bytes
py_members = sorted(n for n in served if n.endswith(".py"))
attr_hits, string_hits = [], []
for name in py_members:
    tree = ast.parse(served[name].decode("utf-8"))
    owner = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for sub in ast.walk(fn):
                owner[id(sub)] = fn.name
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in FOUR_X_ONLY:
            attr_hits.append("%s:%d .%s" % (name, node.lineno, node.attr))
        if isinstance(node, ast.Constant) and node.value in FOUR_X_ONLY:
            string_hits.append((name, node.lineno, owner.get(id(node))))
pre_attr = []
for name in sorted(n for n in pre_served if n.endswith(".py")):
    for node in ast.walk(ast.parse(pre_served[name].decode("utf-8"))):
        if isinstance(node, ast.Attribute) and node.attr in FOUR_X_ONLY:
            pre_attr.append("%s:%d .%s" % (name.rsplit("/", 1)[-1], node.lineno, node.attr))
det = ["the MINTED tarball (v %s): %d members, %d of them .py -- all %d walked; the %d JSON members are data, "
       "not walked" % (MINTED["version"], len(served), len(py_members), len(py_members),
                       len(served) - len(py_members)),
       "attribute references to %s: %d %s" % (list(FOUR_X_ONLY), len(attr_hits), attr_hits),
       "string references: %d %s (the tolerant lookup's vars(jsonschema).get key)" % (len(string_hits), string_hits),
       "DIFFERENCE CONTROL -- the same walk over the PRE-CELL tarball (v %s) finds %d: %s"
       % (PRE_CELL["version"], len(pre_attr), pre_attr)]
ok_a = (len(py_members) == 7 and attr_hits == [] and len(string_hits) == 2
        and all(fn == "contract_validator_class" for _, _, fn in string_hits)
        and sorted(n for n, _, _ in string_hits) == sorted(EDITED) and len(pre_attr) >= 3)
record("(a) AST WALK", ok_a, det)

# ============================================================ (b) the suite
tests_dir = PKG + "/tests"
code_blobs = {p: (blob_id(CODE_COMMIT, p), blob_id("HEAD", p)) for p in EDITED + [TEST_FILE]}
rc_s, out_s = run([sys.executable, "-m", "pytest", tests_dir, "-q", "-p", "no:cacheprovider",
                   "-W", "ignore::DeprecationWarning"], timeout=600, env=env)
rc_c, out_c = run([sys.executable, "-m", "pytest", tests_dir, "--collect-only", "-q", "-p", "no:cacheprovider"],
                  timeout=600, env=env)
rc_t, out_t = run([sys.executable, "-m", "pytest", TEST_FILE, "-q", "-s", "-p", "no:cacheprovider",
                   "-W", "ignore::DeprecationWarning"], timeout=600, env=env)
strip = lambda s: re.sub(r"\x1b\[[0-9;]*m", "", s)   # noqa: E731
out_s, out_c, out_t = strip(out_s), strip(out_c), strip(out_t)
m_pass = re.search(r"(\d+) passed", out_s)
m_fail = re.search(r"(\d+) (failed|error)", out_s)
m_coll = re.search(r"(\d+) tests? collected", out_c)
n_pass = int(m_pass.group(1)) if m_pass else 0
n_coll = int(m_coll.group(1)) if m_coll else -1
fb = re.search(r"fallback class: (\S+); grades identical to native: (\S+)$", out_t, re.M)   # after pytest's dot
mut = re.search(r"^.*MUTANT FAILS as it must: (.*)$", out_t, re.M)
walk_line = re.search(r"^AST walk: .*$", out_t, re.M)
det = ["the code the suite grades is the cell's: %s" % {p.rsplit("/", 1)[-1]: ("SAME as %s" % CODE_COMMIT
                                                                            if a == h else "MOVED")
                                                     for p, (a, h) in code_blobs.items()},
       "pytest %s rc=%d: %s" % (tests_dir, rc_s, (m_pass.group(0) if m_pass else "(no pass count)")
                                + ("; " + m_fail.group(0) if m_fail else "")),
       "collected %d; passed %d -> %d of %d" % (n_coll, n_pass, n_pass, n_coll),
       "tolerance file rc=%d: %s" % (rc_t, (walk_line.group(0) if walk_line else "(no AST walk line)")),
       "FALLBACK BRANCH (Draft202012Validator deleted from the module): class %s, grades identical to native %s"
       % ((fb.group(1), fb.group(2)) if fb else (None, None)),
       "MUTANT (the 2020-12 class hard-coded) under the same environment: %s"
       % (mut.group(1) if mut else "(no mutant line)")]
ok_b = (rc_s == 0 and not m_fail and n_pass == n_coll and n_coll > 0 and rc_t == 0
        and fb is not None and fb.group(1) == "Draft7Validator" and fb.group(2) == "True"
        and mut is not None and all(a == h for a, h in code_blobs.values()))
record("(b) SUITE", ok_b, det)

# ============================================================ (c) the re-mint
DYNAMIC_PROBE = r'''
import importlib.util, json, os, sys
WS = os.path.abspath(sys.argv[1]); RUNNER = sys.argv[2]
opened = set()
def hook(ev, args):
    if ev == "open" and args and isinstance(args[0], str):
        p = os.path.abspath(args[0])
        if p.startswith(WS) and "__pycache__" not in p:
            opened.add(os.path.relpath(p, WS).replace(os.sep, "/"))
sys.addaudithook(hook)
spec = importlib.util.spec_from_file_location("directory_runner", os.path.join(WS, RUNNER))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for firm in sorted(m.SOURCE_SETS):
    m.SOURCE_SETS[firm]()
fids = [f["firm_id"] for f in m.client_firms()]
m.firm_bucket_map(); m.load_contract(); m.tcal.calendar_source()
for fid in fids:
    m.opaque_id("firm", fid, fid)
mods = set()
for mod in list(sys.modules.values()):
    f = getattr(mod, "__file__", None)
    if f and os.path.abspath(f).startswith(WS) and "__pycache__" not in f:
        mods.add(os.path.relpath(os.path.abspath(f), WS).replace(os.sep, "/"))
print("DYNAMIC-JSON " + json.dumps(sorted(opened | mods)))
'''
with tempfile.TemporaryDirectory() as td:
    probe = pathlib.Path(td) / "probe.py"
    probe.write_text(DYNAMIC_PROBE, encoding="utf-8")
    drc, dout = run([sys.executable, str(probe), str(WS), RUNNER], cwd=td, env=env)
dm = re.search(r"^DYNAMIC-JSON (.*)$", dout, re.M)
closure = sorted(set(json.loads(dm.group(1))) | {RUNNER}) if dm else []
meta, pre_meta = cur.get("Metadata", {}), pre_head.get("Metadata", {})
srp = [p for p in meta.get("source-repo-paths", "").split(";") if p]
det = ["THE MINTED VERSION (bound by id) s3://%s/%s ETag %s VersionId %s, %d bytes, LastModified %s"
       % (b["bucket"], b["s3_key"], cur["ETag"].strip('"'), cur.get("VersionId"), len(body),
          cur["LastModified"].isoformat()),
       "md5(downloaded) == ETag: %s   sha256(downloaded) = %s" % (hashlib.md5(body).hexdigest() == MINTED["etag"],
                                                                 sha256(body)),
       "closure (directory_runner's dynamic probe, rc=%d): N = %d; diff vs IB-rtc-8's 8: added %s, removed %s; "
       "the new test file is a member: %s (a test, not a runtime member)"
       % (drc, len(closure), sorted(set(closure) - set(IB_RTC_8_CLOSURE)),
          sorted(set(IB_RTC_8_CLOSURE) - set(closure)), TEST_FILE in by_path),
       "source-repo-paths names %d of %d closure members; members served %d" % (
           len([c for c in closure if c in srp]), len(closure), len(served))]
edited_ok = True
for rel in EDITED:
    mem = served.get(rel, b"")
    stamp = meta.get(by_spec[rel]["sha_metadata_key"], "")
    ho = hash_object(mem)
    blobs = {c: blob_id(c, rel) for c in (CODE_COMMIT, MINT_COMMIT, CLOSE_COMMIT)}
    git_b = git_bytes(MINT_COMMIT, rel)
    moved = sha256(pre_served.get(rel, b"")) != sha256(mem)
    ok = (git_b is not None and mem == git_b and len(set(blobs.values())) == 1 and ho == blobs[MINT_COMMIT]
          and stamp == sha256(mem) and moved)
    edited_ok = edited_ok and ok
    det.append("%s: tarball git hash-object %s sha256 %s; blob at %s/%s/%s: %s; stamp == sha256 %s; "
               "moved off the pre-cell bytes (%s) %s"
               % (rel.rsplit("/", 1)[-1], ho, sha256(mem), CODE_COMMIT, MINT_COMMIT, CLOSE_COMMIT,
                  sorted(set(blobs.values())), stamp == sha256(mem), sha256(pre_served.get(rel, b""))[:12], moved))
unchanged = [s["sha_metadata_key"] for p, s in sorted(by_spec.items()) if p not in EDITED]
same = [k for k in unchanged if meta.get(k) and meta.get(k) == pre_meta.get(k)]
det.append("the other stamps equal the pre-cell object's: %d of %d" % (len(same), len(unchanged)))
differs = (cur["ETag"].strip('"') != PRE_CELL["etag"] and cur.get("VersionId") != PRE_CELL["version"]
           and pre_head["ETag"].strip('"') == PRE_CELL["etag"])
det.append("NEGATIVE CONTROL vs the pre-cell object (ETag %s, v %s, read back: ETag %s): ETag %s, VersionId %s"
           % (PRE_CELL["etag"], PRE_CELL["version"], pre_head["ETag"].strip('"'),
              "DIFFERS" if cur["ETag"].strip('"') != PRE_CELL["etag"] else "SAME",
              "DIFFERS" if cur.get("VersionId") != PRE_CELL["version"] else "SAME"))
v, lines, rows = cons.check(MINT_COMMIT, version_id=MINTED["version"], loose_versions=LOOSE_LEFT_BY_IB_RTC_2)
_, commits = run(["git", "log", "--format=%h", CELL_RANGE, "--"] + sorted(LOOSE_LEFT_BY_IB_RTC_2))
commits = commits.split()
det += ["  " + ln for ln in lines]
det.append("commits to the three distribution members in %s: %d %s" % (CELL_RANGE, len(commits), commits))
ok_c = (hashlib.md5(body).hexdigest() == MINTED["etag"] and cur.get("VersionId") == MINTED["version"]
        and drc == 0 and closure == IB_RTC_8_CLOSURE and all(c in srp for c in closure)
        and TEST_FILE not in by_path and edited_ok and len(same) == len(unchanged) == 7 and differs
        and v == "CONSISTENT" and len(rows) == 3 and not commits)
record("(c) RE-MINT", ok_c, det)

# ============================================================ (d) the host
ec2, ssm = boto3.client("ec2", region_name=REGION), boto3.client("ssm", region_name=REGION)
state = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]["State"]["Name"]
info = ssm.describe_instance_information(
    Filters=[{"Key": "InstanceIds", "Values": [INSTANCE]}])["InstanceInformationList"]
ping = info[0]["PingStatus"] if info else "(absent)"
base = "/tmp/irpt-rtc9-%s" % dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
# WHAT THE HOST ARM SUPPLIES, each hash-bound: the pre-cell tarball (the host role has no
# s3:GetObjectVersion), the four fixtures (not bundle members), and the HoldingsSnapshot contract the
# bundle does not carry (row IRPT_BCKEND-S71). All read from git at the code commit or from S3 by VersionId.
extras = {"pre.tar.gz": pre_body, "tree/" + HS_CONTRACT: git_bytes(CODE_COMMIT, HS_CONTRACT)}
for fx in FIXTURES:
    extras["fix/%s.json" % fx] = git_bytes(CODE_COMMIT, "%s/%s.json" % (FIXTURE_DIR, fx))
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as tf:
    for name, data in sorted(extras.items()):
        ti = tarfile.TarInfo(name)
        ti.size = len(data)
        tf.addfile(ti, io.BytesIO(data))
payload = base64.b64encode(buf.getvalue()).decode("ascii")
CHUNK = 16000
chunks = [payload[i:i + CHUNK] for i in range(0, len(payload), CHUNK)]
CHECK_PY = r'''
import importlib.util, json, os, socket, sys
events = []
def hook(ev, args):
    if ev in ("socket.connect", "socket.getaddrinfo", "http.client.connect"):
        events.append(ev)
sys.addaudithook(hook)
root, tag, fix = sys.argv[1], sys.argv[2], sys.argv[3]
import jsonschema
try:
    from importlib.metadata import version as _v
    jv = _v("jsonschema")
except Exception:
    jv = getattr(jsonschema, "__version__", "?")
print("[rtc9] %s jsonschema %s has-2020-12-class %s" % (tag, jv, "Draft202012Validator" in vars(jsonschema)))
PY = sys.argv[4].split(",")
JS = sys.argv[5].split(",")
def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(root, rel))
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); return m
try:
    dr = load("data/assets/scripts/gold/investor_reporting/directory_runner.py", "directory_runner")
    hs = load("data/assets/scripts/gold/investor_reporting/holdings_snapshot.py", "holdings_snapshot")
    for firm in sorted(dr.SOURCE_SETS):
        dr.SOURCE_SETS[firm]()
except BaseException as e:
    print("[rtc9] %s MODULE-IMPORT-FAIL %s: %s" % (tag, type(e).__name__, e)); sys.exit(0)
loaded = set(os.path.realpath(getattr(m, "__file__", None) or "") for m in list(sys.modules.values()))
for rel in PY:
    ok = os.path.realpath(os.path.join(root, rel)) in loaded
    print("[rtc9] %s %s %s" % (tag, "IMPORT-OK" if ok else "IMPORT-MISSING", rel))
for rel in JS:
    try:
        json.load(open(os.path.join(root, rel), encoding="utf-8")); print("[rtc9] %s LOAD-OK %s" % (tag, rel))
    except Exception as e:
        print("[rtc9] %s LOAD-FAIL %s %s" % (tag, rel, type(e).__name__))
F = lambda n: json.load(open(os.path.join(fix, n + ".json"), encoding="utf-8"))["instance"]
calls = [("DE.valid", lambda: dr.validate_entries([F("DirectoryEntry.valid")])),
         ("DE.invalid", lambda: dr.validate_entries([F("DirectoryEntry.invalid")])),
         ("HS.valid", lambda: hs.validate_snapshot(F("HoldingsSnapshot.valid"))),
         ("HS.invalid", lambda: hs.validate_snapshot(F("HoldingsSnapshot.invalid")))]
for name, fn in calls:
    try:
        print("[rtc9] %s RESULT %s %s" % (tag, name, json.dumps(fn())))
    except BaseException as e:
        print("[rtc9] %s RAISED %s %s: %s" % (tag, name, type(e).__name__, e))
print("[rtc9] %s NET-EVENTS %d" % (tag, len(events)))
n0 = len(events)
try:
    socket.getaddrinfo("localhost", None)
except OSError:
    pass
print("[rtc9] %s NET-POSITIVE-CONTROL %s" % (tag, len(events) > n0))
'''
py_list = ",".join(sorted(n for n in served if n.endswith(".py")))
js_list = ",".join(sorted(n for n in served if n.endswith(".json")))
det = ["host %s state=%s ssm=%s (this battery never starts or stops it)" % (INSTANCE, state, ping),
       "SUPPLIED to the host (not in the served bundle), each sha256-bound: %s"
       % ", ".join("%s %s" % (k, sha256(v)[:12]) for k, v in sorted(extras.items())),
       "shipped as %d base64 chunk(s) of <= %d chars over SSM (the host role has no s3:GetObjectVersion)"
       % (len(chunks), CHUNK)]


def ssm_run(commands, comment):
    r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript", Comment=comment,
                         Parameters={"commands": commands, "executionTimeout": ["600"]})
    cid = r["Command"]["CommandId"]
    inv = {}
    for _ in range(120):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=INSTANCE)
        except Exception:                          # noqa: BLE001
            continue
        if inv.get("Status") not in ("Pending", "InProgress", "Delayed"):
            break
    return cid, inv


out, cmd_id, ship_ok = "", None, True
if state == "running" and ping == "Online":
    for i, ch in enumerate(chunks):
        cmds = ["set -eu", "mkdir -p %s" % base] + (["rm -f %s/extras.b64" % base] if i == 0 else []) + [
            "printf '%%s' '%s' >> %s/extras.b64" % (ch, base), "echo '[rtc9] chunk %d ok'" % i]
        cid, inv = ssm_run(cmds, "IRPT IB-rtc-9 read-only check: ship chunk %d (/tmp only)" % i)
        ship_ok = ship_ok and inv.get("Status") == "Success"
    det.append("chunks shipped: %s" % ("all Success" if ship_ok else "a chunk FAILED"))
    names = sorted(extras)
    host_cmds = [
        "set -u", "B=%s" % base, "cd $B && rm -rf NEW OLD X && mkdir -p NEW OLD X",
        "base64 -d extras.b64 > extras.tar.gz && tar -xzf extras.tar.gz -C X && echo '[rtc9] EXTRAS-OK'",
    ] + ["echo \"[rtc9] supplied %s $(sha256sum X/%s | cut -d' ' -f1)\"" % (n, n) for n in names] + [
        # The host role may GetObject the key but not GetObjectVersion: fetch it as the dispatch does, and
        # bind it to the minted version by sha256 below.
        "aws s3 cp s3://%s/%s new.tar.gz --only-show-errors || echo '[rtc9] FETCH-FAIL'" % (b["bucket"], b["s3_key"]),
        "echo \"[rtc9] new sha256 $(sha256sum new.tar.gz | cut -d' ' -f1)\"",
        "tar -xzf new.tar.gz -C NEW && tar -xzf X/pre.tar.gz -C OLD && echo '[rtc9] EXTRACT-OK'",
        "for T in NEW OLD; do mkdir -p $T/$(dirname %s) && cp X/tree/%s $T/%s; done" % (HS_CONTRACT, HS_CONTRACT,
                                                                                    HS_CONTRACT),
    ] + ["[ -f NEW/%s ] && echo '[rtc9] placed %s' || echo '[rtc9] ABSENT %s'" % (n, n, n) for n in sorted(served)] + [
        "cat > check.py <<'PYEOF'", CHECK_PY.strip("\n"), "PYEOF",
        "cd /tmp && python3 $B/check.py $B/NEW NEW $B/X/fix '%s' '%s' 2>&1" % (py_list, js_list),
        "cd /tmp && python3 $B/check.py $B/OLD OLD $B/X/fix '%s' '%s' 2>&1" % (py_list, js_list),
        "echo '[rtc9] END'",
    ]
    cmd_id, inv = ssm_run(host_cmds, "IRPT IB-rtc-9 read-only validator check on NEW and pre-cell members (/tmp only)")
    out = inv.get("StandardOutputContent", "")
    det.append("SSM command %s status=%s rc=%s" % (cmd_id, inv.get("Status"), inv.get("ResponseCode")))
    if inv.get("StandardErrorContent"):
        det.append("stderr (first 300): " + inv["StandardErrorContent"][:300].replace("\n", " | "))
else:
    det.append("NOT-EVALUATED: the host is not running+Online.")
g = lambda pat: re.findall(pat, out, re.M)   # noqa: E731
supplied = dict(g(r"^\[rtc9\] supplied (\S+) ([0-9a-f]{64})$"))
sup_ok = len(supplied) == len(extras) and all(supplied.get(k) == sha256(v) for k, v in extras.items())
host_sha = g(r"^\[rtc9\] new sha256 ([0-9a-f]{64})$")
placed = g(r"^\[rtc9\] placed (.+)$")
res = {}
for tag in ("NEW", "OLD"):
    res[tag] = {
        "jv": g(r"^\[rtc9\] %s jsonschema (\S+) has-2020-12-class (\S+)$" % tag),
        "imp": g(r"^\[rtc9\] %s IMPORT-OK (\S+)$" % tag),
        "load": g(r"^\[rtc9\] %s LOAD-OK (\S+)$" % tag),
        "result": dict(g(r"^\[rtc9\] %s RESULT (\S+) (.*)$" % tag)),
        "raised": {k: (t, msg) for k, t, msg in g(r"^\[rtc9\] %s RAISED (\S+) (\w+): (.*)$" % tag)},
        "net": g(r"^\[rtc9\] %s NET-EVENTS (\d+)$" % tag),
        "pc": g(r"^\[rtc9\] %s NET-POSITIVE-CONTROL (\S+)$" % tag),
    }
new, old = res["NEW"], res["OLD"]
jv = new["jv"][0] if new["jv"] else (None, None)
det += ["supplied files arrived intact (host sha256 == local): %s (%d of %d)"
        % (sup_ok, len([k for k, v in extras.items() if supplied.get(k) == sha256(v)]), len(extras)),
        "host sha256(new) %s == the MINTED version's %s: %s" % (host_sha[0] if host_sha else None, sha256(body),
                                                                bool(host_sha) and host_sha[0] == sha256(body)),
        "HOST jsonschema.__version__ %s; has a 2020-12 class: %s (expected 3.2.0 / False)" % jv,
        "NEW extracted at repo shape: %d of %d members placed" % (len(placed), len(served)),
        "NEW: IMPORT-OK %d of %d .py, LOAD-OK %d of %d .json" % (len(new["imp"]), len(py_list.split(",")),
                                                               len(new["load"]), len(js_list.split(",")))]
for k in ("DE.valid", "DE.invalid", "HS.valid", "HS.invalid"):
    det.append("  NEW %-10s %s" % (k, new["result"].get(k) or ("RAISED %s: %s" % new["raised"][k]
                                                               if k in new["raised"] else None)))
for k in ("DE.valid", "DE.invalid", "HS.valid", "HS.invalid"):
    det.append("  OLD %-10s %s" % (k, ("RAISED %s: %s" % old["raised"][k]) if k in old["raised"]
                                   else old["result"].get(k)))
det.append("network events NEW %s OLD %s; positive control fired NEW %s OLD %s"
           % (new["net"], old["net"], new["pc"], old["pc"]))


def parsed(k):
    try:
        return json.loads(new["result"][k])
    except (KeyError, ValueError):
        return None


de_v, de_i, hs_v, hs_i = parsed("DE.valid"), parsed("DE.invalid"), parsed("HS.valid"), parsed("HS.invalid")
accepted = [de_v == [1, []], hs_v == [True, []]]
refused = [bool(de_i) and de_i[0] == 0 and len(de_i[1]) == 1 and de_i[1][0].startswith("entry[0] $."),
           bool(hs_i) and hs_i[0] is False and bool(hs_i[1]) and hs_i[1][0].startswith("$.")]
old_raises = [k for k, (t, msg) in old["raised"].items() if t == "AttributeError" and "Draft202012Validator" in msg]
det.append("valid accepted %d of 2; invalid refused with a path %d of 2; pre-cell calls raising AttributeError "
           "naming Draft202012Validator %d of 4 (validate_entries %d of 2, validate_snapshot %d of 2)"
           % (sum(accepted), sum(refused), len(old_raises), len([k for k in old_raises if k.startswith("DE")]),
              len([k for k in old_raises if k.startswith("HS")])))
host_up = cmd_id is not None
ok_d = (host_up and ship_ok and sup_ok and bool(host_sha) and host_sha[0] == sha256(body)
        and len(placed) == len(served) == 9
        and len(new["imp"]) == 7 and len(new["load"]) == 2
        and all(accepted) and all(refused) and len(old_raises) == 4
        and new["net"] == ["0"] and old["net"] == ["0"] and new["pc"] == ["True"] and old["pc"] == ["True"]
        and jv[1] == "False")
record("(d) HOST", ok_d if host_up else None, det)

print("R-40 identities:")
print("  minted bundle: ETag %s  VersionId %s  sha256 %s" % (MINTED["etag"], MINTED["version"], sha256(body)))
print("  pre-cell bundle: ETag %s  VersionId %s  sha256 %s" % (PRE_CELL["etag"], PRE_CELL["version"],
                                                               sha256(pre_body)))
for rel in EDITED:
    print("  %s member: git blob %s  sha256 %s" % (rel.rsplit("/", 1)[-1], blob_id(MINT_COMMIT, rel),
                                                  sha256(served.get(rel, b""))))
print("  test file: git blob %s" % blob_id(CODE_COMMIT, TEST_FILE))
if cmd_id:
    print("  host command %s  host sha256 %s" % (cmd_id, host_sha[0] if host_sha else None))
print()
passed = sum(1 for _, ok in results if ok)
print("R39-AC1: %d of %d graded arms PASS" % (passed, len(results)))
if passed == len(results):
    print("IBR39-RUNNERS-VALIDATE-UNDER-HOST-JSONSCHEMA")
    sys.exit(0)
print("BLOCKED: not every graded arm passed; the expect token is withheld")
sys.exit(1)
