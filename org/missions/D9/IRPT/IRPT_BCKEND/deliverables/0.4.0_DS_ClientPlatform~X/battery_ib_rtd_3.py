#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtd-3 acceptance battery -- R43-AC1, four graded arms.

Prints IBR43-HOLDINGS-CONTRACT-ABOARD-AND-TRIGGER-GUARDED only when arms (a)-(d) ALL hold.

Row S71: holdings_snapshot.py reads docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json, which
the investor_reporting bundle did not carry. The member is declared at 28bc06907f, the trigger test committed at
024033d9d9, and the bundle re-minted under change-management entry irpt-bckend-rtd3-holdings-contract-mint
(opened 3ac01a96ae, closed 8f460875a1). BOUND TO IDENTITY for a later grader: the minted and pre-cell objects by
VersionId, the tree by the commits that carried it. Every count is RE-DERIVED from the real world on each run;
nothing is read from this battery's own earlier output.

WHAT THIS BATTERY IS NOT (bound 12): it wraps nothing it grades. The declaration is the guard's own; the diff reads
both schemas as git blobs; the served object is read by VersionId; the host arm imports the served runner and calls
its real load_contract(); the trigger arm runs the committed test file as written. What the host arm SUPPLIES is
named and hash-bound: the pre-cell tarball, shipped over SSM because the host role has no s3:GetObjectVersion.

Graded arms:
  (a) MEMBER     the guard declares the v1 schema by repo path, bundle-only (no distribution flag, no loose leg);
                 neither schema edited and the runner's CONTRACT_PATH line untouched in the cell's range; the diff
                 of the two schemas printed with its denominators.
  (b) RE-MINT    the minted identity; closure 10 of 10 with the diff against IB-rtc-9's 9; the negative control
                 against the pre-cell object DIFFERS (both 0XLkiPt4 and 00PXLyYm, byte-identical, row S74); the new
                 member's tarball bytes == blob 9ec70af2 and == its stamp; the other 9 members unchanged; the
                 distribution legs consistent 3 of 3 at the pre-mint VersionIds, 0 commits to them.
  (c) HOST       IMPORT-OK all .py members; holdings_snapshot.load_contract() returns the v1 schema 1 of 1 on the
                 new tree; the pre-cell tree raises FileNotFoundError naming the v1 path 1 of 1; same interpreter,
                 same command; 0 network events.
  (d) TRIGGER    the committed trigger test: LIVE verdict PASS (read now), the mutant FAILING under a simulated
                 ENABLED read and PASSING the same list DISABLED; 0 skipped; the directory suite N of N.
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
import schema_diff_ib_rtd_3 as sdiff    # noqa: E402  arm (a)'s recorded diff, re-derived here

BUNDLE = "investor_reporting"
PKG = "data/assets/scripts/gold/investor_reporting"
HOLDINGS = PKG + "/holdings_snapshot.py"
MEMBER = "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json"
MEMBER_BLOB = "9ec70af2ba0c71ea589dab48bd14407e111694a8"
CTR_SCHEMA = "infra/aws/lambda/investor-reporting/_contracts/HoldingsSnapshot.schema.json"
TRIGGER_TEST = PKG + "/tests/test_holdings_rearm_trigger.py"
INSTANCE = "i-02448edb624a7a7cf"
REGION = "us-east-1"
CUT = "e4623a5872"                    # the order's cut
DECL_COMMIT = "28bc06907f"            # the member declared in the guard
TRIGGER_COMMIT = "024033d9d9"         # the trigger test + rows S74/S75
MINT_COMMIT = "3ac01a96ae"            # the tree the guard packed (the ledger OPEN commit)
CLOSE_COMMIT = "8f460875a1"           # the ledger close
CELL_RANGE = "%s..%s" % (CUT, CLOSE_COMMIT)
MINTED = {"etag": "a8e1a036b4e26cd2fca45f3a295a4c71", "version": ".v.aG6Rbk5wXOjGgb4vnQIeGPzrabMKo"}
PRE_CELL = {"etag": "4c942a76f990874838e33e37f24ed69a", "version": "00PXLyYmM0vJavlwdpUHBKRi3pza0_nS"}
FACE_PRE = "0XLkiPt4wljdniLnF2fkPKN4qAIkjUbc"   # the version the face names; byte-identical (row S74)
LOOSE_PRE_MINT = {                              # read at 12:1xZ, before the mint (row S74)
    "data/assets/scripts/gold/runners_49f/runner_common.py": "jnnxQWbVT_lx6WlJu8HbVXNjQJpYK00w",
    "data/cot/scripts/gold/runners_cot/runner_common.py": "81mlcZFSpRyiH_OeK0OlWFvEHKYUelj_",
    "data/inf/scripts/gold/runners_inf/runner_common.py": "z_WDDmx6004thBhXbT0uBvsDkNibZQF8",
}
IB_RTC_9_MEMBERS = sorted([
    PKG + "/directory_runner.py", HOLDINGS,
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


print("R43-AC1 battery -- IRPT_BCKEND.TO-IB-rtd-3, the holdings contract aboard and the re-arm trigger guarded")
print("workspace: %s" % WS)
_, head = run(["git", "rev-parse", "--short=10", "HEAD"])
print("branch tip: %s   declared: %s   mint commit: %s   run at %s" % (
    head.strip(), DECL_COMMIT, MINT_COMMIT, dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
print()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

import boto3                                     # noqa: E402
s3 = boto3.client("s3", region_name=REGION)
b = sdc.find_bundle(BUNDLE)[2]
by_spec = {s["repo_path"]: s for s in b["members"].values()}
cur = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=MINTED["version"])
body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=MINTED["version"])["Body"].read()
served = untar(body)
pre_head = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=PRE_CELL["version"])
pre_body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=PRE_CELL["version"])["Body"].read()
pre_served = untar(pre_body)
face_body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=FACE_PRE)["Body"].read()

# ============================================================ (a) the member + the recorded diff
spec = by_spec.get(MEMBER)
decl_ok = (spec is not None and spec["repo_path"] == MEMBER and not sdc.is_distribution_spec(spec)
           and sdc.file_to_s3_target(MEMBER) is None)
_, schema_commits = run(["git", "log", "--format=%h", CELL_RANGE, "--", MEMBER, CTR_SCHEMA])
schema_commits = schema_commits.split()
runner_same = blob_id(CUT, HOLDINGS) == blob_id(CLOSE_COMMIT, HOLDINGS)
_hs_src = (git_bytes(CLOSE_COMMIT, HOLDINGS) or b"").decode("utf-8")
contract_line = ["%s:%d-%d @%s %s" % (HOLDINGS, n.lineno, n.end_lineno, CLOSE_COMMIT,
                                      " ".join(ast.get_source_segment(_hs_src, n).split()))
                 for n in ast.parse(_hs_src).body
                 if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CONTRACT_PATH"
                                                      for t in n.targets)]
d = sdiff.diff(CUT)
det = ["the guard declares %s: %s; bundle-only (distribution flag %s; per-file S3 target %s); sha key %s"
       % (MEMBER, spec is not None, sdc.is_distribution_spec(spec) if spec else None,
          sdc.file_to_s3_target(MEMBER), spec["sha_metadata_key"] if spec else None),
       "commits to either HoldingsSnapshot schema in %s: %d %s" % (CELL_RANGE, len(schema_commits), schema_commits),
       "holdings_snapshot.py blob at %s == at %s: %s; its CONTRACT_PATH assignment (AST): %s"
       % (CUT, CLOSE_COMMIT, runner_same, contract_line)]
det += ["DIFF " + ln for ln in sdiff.render(d)]
ok_a = (decl_ok and not schema_commits and runner_same and len(contract_line) == 1
        and all(tok in contract_line[0] for tok in ('"docs"', '"contracts"', '"investor-reporting"', '"v1"',
                                                     '"HoldingsSnapshot.schema.json"'))
        and d["V1"]["blob"] == MEMBER_BLOB
        and d["properties"]["paths_union"] > 0 and d["leaves"]["union"] > 0)
record("(a) MEMBER + DIFF", ok_a, det)

# ============================================================ (b) the re-mint
meta, pre_meta = cur.get("Metadata", {}), pre_head.get("Metadata", {})
srp = [p for p in meta.get("source-repo-paths", "").split(";") if p]
declared = sorted(by_spec)
mem = served.get(MEMBER, b"")
ho = hash_object(mem)
blob_b = git_bytes(MINT_COMMIT, MEMBER)
others = [p for p in declared if p != MEMBER]
unchanged = [p for p in others if served.get(p) is not None and served.get(p) == pre_served.get(p)]
stamps_same = [p for p in others if meta.get(by_spec[p]["sha_metadata_key"])
               and meta.get(by_spec[p]["sha_metadata_key"]) == pre_meta.get(by_spec[p]["sha_metadata_key"])]
v, lines, rows = cons.check(MINT_COMMIT, version_id=MINTED["version"], loose_versions=LOOSE_PRE_MINT)
_, commits = run(["git", "log", "--format=%h", CELL_RANGE, "--"] + sorted(LOOSE_PRE_MINT))
commits = commits.split()
differs = (cur["ETag"].strip('"') != PRE_CELL["etag"] and cur.get("VersionId") != PRE_CELL["version"]
           and cur.get("VersionId") != FACE_PRE and pre_head["ETag"].strip('"') == PRE_CELL["etag"])
det = ["THE MINTED VERSION (bound by id) s3://%s/%s ETag %s VersionId %s, %d bytes, LastModified %s"
       % (b["bucket"], b["s3_key"], cur["ETag"].strip('"'), cur.get("VersionId"), len(body),
          cur["LastModified"].isoformat()),
       "md5(downloaded) == ETag: %s   sha256(downloaded) = %s" % (hashlib.md5(body).hexdigest() == MINTED["etag"],
                                                                 sha256(body)),
       "closure: the guard declares %d of %d; diff vs IB-rtc-9's 9: added %s, removed %s"
       % (len(declared), len(declared), sorted(set(declared) - set(IB_RTC_9_MEMBERS)),
          sorted(set(IB_RTC_9_MEMBERS) - set(declared))),
       "source-repo-paths names %d of %d declared; members served %d" % (len([p for p in declared if p in srp]),
                                                                       len(declared), len(served)),
       "the new member in the tarball: git hash-object %s sha256 %s (%d bytes, %d CR); blob at %s %s; stamp %s"
       % (ho, sha256(mem), len(mem), mem.count(b"\r"), MINT_COMMIT, blob_id(MINT_COMMIT, MEMBER),
          meta.get(by_spec[MEMBER]["sha_metadata_key"]) if MEMBER in by_spec else None),
       "the other %d members' bytes equal the pre-cell tarball's: %d of %d; their stamps equal: %d of %d"
       % (len(others), len(unchanged), len(others), len(stamps_same), len(others)),
       "PRE-CELL: the key's predecessor %s and the face's %s are byte-identical (sha256 %s == %s: %s; row S74)"
       % (PRE_CELL["version"], FACE_PRE, sha256(pre_body)[:12], sha256(face_body)[:12],
          sha256(pre_body) == sha256(face_body)),
       "NEGATIVE CONTROL vs the pre-cell object (ETag %s): ETag %s, VersionId %s"
       % (PRE_CELL["etag"], "DIFFERS" if cur["ETag"].strip('"') != PRE_CELL["etag"] else "SAME",
          "DIFFERS" if cur.get("VersionId") not in (PRE_CELL["version"], FACE_PRE) else "SAME")]
det += ["  " + ln for ln in lines]
det.append("commits to the three distribution members in %s: %d %s" % (CELL_RANGE, len(commits), commits))
ok_b = (hashlib.md5(body).hexdigest() == MINTED["etag"] and cur.get("VersionId") == MINTED["version"]
        and len(declared) == 10 and sorted(set(declared) - set(IB_RTC_9_MEMBERS)) == [MEMBER]
        and not (set(IB_RTC_9_MEMBERS) - set(declared)) and all(p in srp for p in declared) and len(served) == 10
        and blob_b is not None and mem == blob_b and ho == MEMBER_BLOB
        and meta.get(by_spec[MEMBER]["sha_metadata_key"]) == sha256(mem)
        and len(unchanged) == len(stamps_same) == len(others) == 9
        and sha256(pre_body) == sha256(face_body) and differs
        and v == "CONSISTENT" and len(rows) == 3 and not commits)
record("(b) RE-MINT", ok_b, det)

# ============================================================ (c) the host
ec2, ssm = boto3.client("ec2", region_name=REGION), boto3.client("ssm", region_name=REGION)
state = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]["State"]["Name"]
info = ssm.describe_instance_information(
    Filters=[{"Key": "InstanceIds", "Values": [INSTANCE]}])["InstanceInformationList"]
ping = info[0]["PingStatus"] if info else "(absent)"
base = "/tmp/irpt-rtd3-%s" % dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
payload = base64.b64encode(pre_body).decode("ascii")
CHUNK = 16000
chunks = [payload[i:i + CHUNK] for i in range(0, len(payload), CHUNK)]
v1_id = json.loads(blob_b.decode("utf-8")).get("$id") if blob_b else None
CHECK_PY = r'''
import hashlib, importlib.util, json, os, socket, sys
events = []
def hook(ev, args):
    if ev in ("socket.connect", "socket.getaddrinfo", "http.client.connect"):
        events.append(ev)
sys.addaudithook(hook)
root, tag = sys.argv[1], sys.argv[2]
PY = sys.argv[3].split(",")
def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(root, rel))
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m; spec.loader.exec_module(m); return m
try:
    dr = load("data/assets/scripts/gold/investor_reporting/directory_runner.py", "directory_runner")
    hs = load("data/assets/scripts/gold/investor_reporting/holdings_snapshot.py", "holdings_snapshot")
    for firm in sorted(dr.SOURCE_SETS):
        dr.SOURCE_SETS[firm]()
except BaseException as e:
    print("[rtd3] %s MODULE-IMPORT-FAIL %s: %s" % (tag, type(e).__name__, e)); sys.exit(0)
loaded = set(os.path.realpath(getattr(m, "__file__", None) or "") for m in list(sys.modules.values()))
for rel in PY:
    ok = os.path.realpath(os.path.join(root, rel)) in loaded
    print("[rtd3] %s %s %s" % (tag, "IMPORT-OK" if ok else "IMPORT-MISSING", rel))
print("[rtd3] %s CONTRACT_PATH %s" % (tag, os.path.relpath(str(hs.CONTRACT_PATH), root).replace(os.sep, "/")))
try:
    c = hs.load_contract()
    raw = open(str(hs.CONTRACT_PATH), "rb").read()
    print("[rtd3] %s LOAD-CONTRACT RETURNED id=%s title=%s sha256=%s" % (tag, c.get("$id"), c.get("title"),
                                                                         hashlib.sha256(raw).hexdigest()))
except BaseException as e:
    print("[rtd3] %s LOAD-CONTRACT RAISED %s: %s" % (tag, type(e).__name__, e))
print("[rtd3] %s NET-EVENTS %d" % (tag, len(events)))
n0 = len(events)
try:
    socket.getaddrinfo("localhost", None)
except OSError:
    pass
print("[rtd3] %s NET-POSITIVE-CONTROL %s" % (tag, len(events) > n0))
'''
py_list = ",".join(sorted(n for n in served if n.endswith(".py")))
det = ["host %s state=%s ssm=%s (this battery never starts or stops it)" % (INSTANCE, state, ping),
       "SUPPLIED to the host: the pre-cell tarball %s (sha256 %s), %d base64 chunk(s) over SSM (no GetObjectVersion)"
       % (PRE_CELL["version"], sha256(pre_body)[:12], len(chunks))]


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
        cmds = ["set -eu", "mkdir -p %s" % base] + (["rm -f %s/pre.b64" % base] if i == 0 else []) + [
            "printf '%%s' '%s' >> %s/pre.b64" % (ch, base), "echo '[rtd3] chunk %d ok'" % i]
        _, inv = ssm_run(cmds, "IRPT IB-rtd-3 read-only check: ship chunk %d (/tmp only)" % i)
        ship_ok = ship_ok and inv.get("Status") == "Success"
    det.append("chunks shipped: %s" % ("all Success" if ship_ok else "a chunk FAILED"))
    host_cmds = [
        "set -u", "B=%s" % base, "cd $B && rm -rf NEW OLD && mkdir -p NEW OLD",
        "base64 -d pre.b64 > pre.tar.gz && echo \"[rtd3] pre sha256 $(sha256sum pre.tar.gz | cut -d' ' -f1)\"",
        "aws s3 cp s3://%s/%s new.tar.gz --only-show-errors || echo '[rtd3] FETCH-FAIL'" % (b["bucket"], b["s3_key"]),
        "echo \"[rtd3] new sha256 $(sha256sum new.tar.gz | cut -d' ' -f1)\"",
        "tar -xzf new.tar.gz -C NEW && tar -xzf pre.tar.gz -C OLD && echo '[rtd3] EXTRACT-OK'",
    ] + ["[ -f NEW/%s ] && echo '[rtd3] placed %s' || echo '[rtd3] ABSENT %s'" % (n, n, n) for n in sorted(served)] + [
        "[ -f OLD/%s ] && echo '[rtd3] OLD-HAS-MEMBER' || echo '[rtd3] OLD-LACKS-MEMBER'" % MEMBER,
        "cat > check.py <<'PYEOF'", CHECK_PY.strip("\n"), "PYEOF",
        "cd /tmp && python3 $B/check.py $B/NEW NEW '%s' 2>&1" % py_list,
        "cd /tmp && python3 $B/check.py $B/OLD OLD '%s' 2>&1" % py_list,
        "echo '[rtd3] END'",
    ]
    cmd_id, inv = ssm_run(host_cmds, "IRPT IB-rtd-3 read-only load_contract check, NEW and pre-cell (/tmp only)")
    out = inv.get("StandardOutputContent", "")
    det.append("SSM command %s status=%s rc=%s" % (cmd_id, inv.get("Status"), inv.get("ResponseCode")))
    if inv.get("StandardErrorContent"):
        det.append("stderr (first 300): " + inv["StandardErrorContent"][:300].replace("\n", " | "))
else:
    det.append("NOT-EVALUATED: the host is not running+Online.")
g = lambda pat: re.findall(pat, out, re.M)   # noqa: E731
host_new = g(r"^\[rtd3\] new sha256 ([0-9a-f]{64})$")
host_pre = g(r"^\[rtd3\] pre sha256 ([0-9a-f]{64})$")
placed = g(r"^\[rtd3\] placed (.+)$")
old_lacks = g(r"^\[rtd3\] (OLD-HAS-MEMBER|OLD-LACKS-MEMBER)$")
res = {}
for tag in ("NEW", "OLD"):
    res[tag] = {
        "imp": g(r"^\[rtd3\] %s IMPORT-OK (\S+)$" % tag),
        "cpath": g(r"^\[rtd3\] %s CONTRACT_PATH (\S+)$" % tag),
        "ret": g(r"^\[rtd3\] %s LOAD-CONTRACT RETURNED id=(\S+) title=(.*) sha256=([0-9a-f]{64})$" % tag),
        "raised": g(r"^\[rtd3\] %s LOAD-CONTRACT RAISED (\w+): (.*)$" % tag),
        "net": g(r"^\[rtd3\] %s NET-EVENTS (\d+)$" % tag),
        "pc": g(r"^\[rtd3\] %s NET-POSITIVE-CONTROL (\S+)$" % tag),
    }
new, old = res["NEW"], res["OLD"]
det += ["host sha256(new) == the MINTED version's: %s; host sha256(pre) == the pre-cell version's: %s"
        % (bool(host_new) and host_new[0] == sha256(body), bool(host_pre) and host_pre[0] == sha256(pre_body)),
        "NEW extracted at repo shape: %d of %d placed; the pre-cell tree %s" % (len(placed), len(served),
                                                                                old_lacks[0] if old_lacks else None),
        "IMPORT-OK NEW %d of %d .py, OLD %d of %d .py" % (len(new["imp"]), len(py_list.split(",")), len(old["imp"]),
                                                        len(py_list.split(","))),
        "CONTRACT_PATH (both trees): NEW %s OLD %s" % (new["cpath"], old["cpath"]),
        "NEW load_contract() RETURNED: %s" % (new["ret"] or ("RAISED %s" % new["raised"])),
        "OLD load_contract(): %s" % (("RAISED %s: %s" % old["raised"][0]) if old["raised"] else old["ret"]),
        "network events NEW %s OLD %s; positive control fired NEW %s OLD %s" % (new["net"], old["net"], new["pc"],
                                                                                 old["pc"])]
ret_ok = (len(new["ret"]) == 1 and new["ret"][0][0] == v1_id and new["ret"][0][2] == sha256(blob_b or b""))
raise_ok = (len(old["raised"]) == 1 and old["raised"][0][0] == "FileNotFoundError" and MEMBER in old["raised"][0][1])
det.append("load_contract returned the v1 schema (id %s, sha256 == blob): %d of 1; the pre-cell raised "
           "FileNotFoundError naming the v1 path: %d of 1" % (v1_id, int(ret_ok), int(raise_ok)))
host_up = cmd_id is not None
ok_c = (host_up and ship_ok and bool(host_new) and host_new[0] == sha256(body) and bool(host_pre)
        and host_pre[0] == sha256(pre_body) and len(placed) == len(served) == 10 and old_lacks == ["OLD-LACKS-MEMBER"]
        and len(new["imp"]) == 7 and new["cpath"] == [MEMBER] and old["cpath"] == [MEMBER] and ret_ok and raise_ok
        and new["net"] == ["0"] and old["net"] == ["0"] and new["pc"] == ["True"] and old["pc"] == ["True"])
record("(c) HOST", ok_c if host_up else None, det)

# ============================================================ (d) the trigger, run as committed
strip = lambda s: re.sub(r"\x1b\[[0-9;]*m", "", s)   # noqa: E731
trig_same = blob_id(TRIGGER_COMMIT, TRIGGER_TEST) == blob_id("HEAD", TRIGGER_TEST)
rc_t, out_t = run([sys.executable, "-m", "pytest", TRIGGER_TEST, "-q", "-s", "-rs", "-p", "no:cacheprovider",
                   "-W", "ignore::DeprecationWarning"], timeout=900, env=env)
rc_s, out_s = run([sys.executable, "-m", "pytest", PKG + "/tests", "-q", "-rs", "-p", "no:cacheprovider",
                   "-W", "ignore::DeprecationWarning"], timeout=900, env=env)
rc_c, out_c = run([sys.executable, "-m", "pytest", PKG + "/tests", "--collect-only", "-q", "-p", "no:cacheprovider"],
                  timeout=600, env=env)
out_t, out_s, out_c = strip(out_t), strip(out_s), strip(out_c)
live = re.search(r"REARM-TRIGGER LIVE: (.*) -> (PASS|FAIL)$", out_t, re.M)
ifen = re.search(r"IF-ENABLED-NOW: (PASS|FAIL)", out_t)
mut = re.search(r"MUTANT: (.*)$", out_t, re.M)
t_pass = re.search(r"(\d+) passed", out_t)
t_skip = re.search(r"(\d+) skipped", out_t)
s_pass = re.search(r"(\d+) passed", out_s)
s_bad = re.search(r"(\d+) (failed|error|skipped)", out_s)
s_coll = re.search(r"(\d+) tests? collected", out_c)
det = ["the trigger test at HEAD is the committed one (%s): %s" % (TRIGGER_COMMIT, trig_same),
       "trigger test rc=%d: %s%s" % (rc_t, t_pass.group(0) if t_pass else "(no pass count)",
                                    ("; " + t_skip.group(0) + " -- NOT-EVALUATED") if t_skip else ""),
       "LIVE: %s -> %s" % ((live.group(1), live.group(2)) if live else (None, None)),
       "IF-ENABLED-NOW (informational, after the mint): %s" % (ifen.group(1) if ifen else None),
       "MUTANT: %s" % (mut.group(1) if mut else None),
       "directory suite rc=%d: %s of %s collected%s" % (rc_s, s_pass.group(1) if s_pass else 0,
                                                       s_coll.group(1) if s_coll else "?",
                                                       ("; " + s_bad.group(0)) if s_bad else "")]
ok_d = (trig_same and rc_t == 0 and t_pass is not None and t_pass.group(1) == "3" and not t_skip
        and live is not None and live.group(2) == "PASS" and ifen is not None and ifen.group(1) == "PASS"
        and mut is not None and "FAILS as it must" in mut.group(1) and "DISABLED -> PASS (inert)" in mut.group(1)
        and rc_s == 0 and s_pass is not None and s_coll is not None and s_pass.group(1) == s_coll.group(1)
        and not s_bad)
record("(d) TRIGGER", ok_d, det)

print("R-40 identities:")
print("  minted bundle: ETag %s  VersionId %s  sha256 %s" % (MINTED["etag"], MINTED["version"], sha256(body)))
print("  pre-cell bundle: ETag %s  VersionId %s (== %s)  sha256 %s" % (PRE_CELL["etag"], PRE_CELL["version"],
                                                                       FACE_PRE, sha256(pre_body)))
print("  new member %s: git blob %s  sha256 %s" % (MEMBER, ho, sha256(mem)))
print("  trigger test: git blob %s   guard: git blob %s" % (blob_id(TRIGGER_COMMIT, TRIGGER_TEST),
                                                          blob_id(DECL_COMMIT, ".tools/safe_deploy_core.py")))
if cmd_id:
    print("  host command %s  host sha256 new %s" % (cmd_id, host_new[0] if host_new else None))
print()
passed = sum(1 for _, ok in results if ok)
print("R43-AC1: %d of %d graded arms PASS" % (passed, len(results)))
if passed == len(results):
    print("IBR43-HOLDINGS-CONTRACT-ABOARD-AND-TRIGGER-GUARDED")
    sys.exit(0)
print("BLOCKED: not every graded arm passed; the expect token is withheld")
sys.exit(1)
