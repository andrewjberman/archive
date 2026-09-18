#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtc-8 acceptance battery -- R38-AC1, four graded arms.

Prints IBR38-BUNDLE-REMINTED-49F-ABOARD only when arms (a)-(d) ALL hold.

The K5 mint (the sign-off packet's step 5): the investor_reporting bundle re-minted after IB-rtc-6's
Firm49F merged. BOUND TO IDENTITY for a later grader: the minted object by VersionId, the tree by the
commit the mint ran at, the distribution members' loose legs by the VersionIds IB-rtc-2 left.

WHAT THIS BATTERY IS NOT (bound 12): it wraps nothing it grades. The closure is derived from the real
runner; the served object and its version history are read from S3; the host arm is a read-only SSM
command that extracts the served bytes and imports the real runner from them.

Graded arms:
  (a) CLOSURE     8 of 8 declared by repo path, the diff against IB-rtc-2's list printed; IB-rtc-6's test
                  file is not a runtime member.
  (b) RE-MINT     the minted version's identity (ETag, VersionId, sha256 of downloaded bytes),
                  source-repo-paths 8 of 8, the NEGATIVE CONTROL against IB-rtc-2's object DIFFERS, and
                  directory_runner.py's bytes in the tarball equal the blob at the mint commit.
  (c) CONSISTENCY the three distribution legs consistent 3 of 3 on the minted version and the loose
                  VersionIds IB-rtc-2 left; 0 commits to them in this cell's range.
  (d) HOST        extract 8 of 8 at repo shape, IMPORT-OK 3 of 3; with the source-role variable UNSET the
                  K5 WARN appears on the host session with 0 calls to any service endpoint; with it SET to
                  a valid-shaped, non-existent ARN, construction makes 0 network events and no assumption.
"""
from __future__ import annotations

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
RUNNER = "data/assets/scripts/gold/investor_reporting/directory_runner.py"
INSTANCE = "i-02448edb624a7a7cf"
REGION = "us-east-1"
CUT = "437789944a"                                  # the order's cut
MINT_COMMIT = "a1f09a51dd"                          # the tree the guard packed (OPEN sentinel commit)
CLOSE_COMMIT = "84349a3a19"                         # the ledger close (the cell's tip before its deliverables)
CELL_RANGE = "%s..%s" % (CUT, CLOSE_COMMIT)            # this cell's commits up to the ledger close
MINTED = {"etag": "479af04c0a3a1eb6651707b340df9926", "version": "q8myxeHdNw48w1uDb7YTcBh8DHV9TzU2"}
PRE_CELL = {"etag": "0020e7afc760b827a6adb7c0ad538903", "version": "1jPgGCGLP.uGY5RpMlMJTrKvKzvyYf7O"}
LOOSE_LEFT_BY_IB_RTC_2 = {
    "data/assets/scripts/gold/runners_49f/runner_common.py": "jnnxQWbVT_lx6WlJu8HbVXNjQJpYK00w",
    "data/cot/scripts/gold/runners_cot/runner_common.py": "bobsNlnmKIjMyMW8PHxiQVeJCXPIJmOs",
    "data/inf/scripts/gold/runners_inf/runner_common.py": "z_WDDmx6004thBhXbT0uBvsDkNibZQF8",
}
IB_RTC_2_CLOSURE = sorted([
    RUNNER,
    "data/assets/scripts/gold/runners_49f/runner_common.py",
    "data/cot/scripts/gold/runners_cot/runner_common.py",
    "data/firm_registry.json",
    "data/inf/scripts/gold/runners_inf/runner_common.py",
    "infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json",
    "infra/aws/lambda/investor-reporting/_ids/ids.py",
    "lib/trading_calendar.py",
])
RTC6_TEST = "data/assets/scripts/gold/investor_reporting/tests/test_directory_runner_source_principal.py"
NONEXISTENT_ARN = "arn:aws:iam::000000000000:role/irpt-nonexistent-probe-role"

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


def record(arm, ok, detail):
    results.append((arm, ok is True))
    print("  %-5s %s" % ({True: "PASS", False: "FAIL", None: "N/E"}[ok], arm))
    for line in detail:
        print("        " + line)
    print()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


print("R38-AC1 battery -- IRPT_BCKEND.TO-IB-rtc-8, the K5 mint (the 49 Financial source set aboard)")
print("workspace: %s" % WS)
_, head = run(["git", "rev-parse", "--short=10", "HEAD"])
print("branch tip: %s   mint commit: %s   run at %s" % (head.strip(), MINT_COMMIT,
      dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
print()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

# ============================================================ (a) the closure
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
b = sdc.find_bundle(BUNDLE)[2]
by_path = {s["repo_path"]: n for n, s in b["members"].items()}
by_spec = {s["repo_path"]: s for s in b["members"].values()}
declared = [c for c in closure if c in by_path and by_path[c] == c]
det = ["dynamic open/import probe rc=%d: CLOSURE N = %d" % (drc, len(closure)),
       "diff vs IB-rtc-2's 8: added %s, removed %s" % (sorted(set(closure) - set(IB_RTC_2_CLOSURE)),
                                                      sorted(set(IB_RTC_2_CLOSURE) - set(closure))),
       "declared and named by repo path: %d of %d" % (len(declared), len(closure)),
       "IB-rtc-6's test file %s: present in the tree %s, in the closure %s, a bundle member %s "
       "(a test, not a runtime member; IB-rtc-6 edited directory_runner.py IN PLACE, so the list is unchanged)"
       % (RTC6_TEST, (WS / RTC6_TEST).is_file(), RTC6_TEST in closure, RTC6_TEST in by_path)]
ok_a = drc == 0 and len(closure) == 8 and len(declared) == 8 and closure == IB_RTC_2_CLOSURE \
    and (WS / RTC6_TEST).is_file() and RTC6_TEST not in closure and RTC6_TEST not in by_path
record("(a) CLOSURE", ok_a, det)

# ============================================================ (b) the re-mint
import boto3                                     # noqa: E402
s3 = boto3.client("s3", region_name=REGION)
cur = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=MINTED["version"])
body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=MINTED["version"])["Body"].read()
live = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"])
meta = cur.get("Metadata", {})
srp = [p for p in meta.get("source-repo-paths", "").split(";") if p]
with tarfile.open(fileobj=io.BytesIO(body), mode="r:gz") as tf:
    served = {m.name: tf.extractfile(m).read() for m in tf.getmembers()}
pre = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=PRE_CELL["version"])
pre_body = pre["Body"].read()
with tarfile.open(fileobj=io.BytesIO(pre_body), mode="r:gz") as tf:
    pre_runner = tf.extractfile(RUNNER).read()
blob = git_bytes(MINT_COMMIT, RUNNER)
_, blob_id = run(["git", "rev-parse", "%s:%s" % (MINT_COMMIT, RUNNER)])
_, close_id = run(["git", "rev-parse", "%s:%s" % (CLOSE_COMMIT, RUNNER)])
_, head_id = run(["git", "rev-parse", "HEAD:%s" % RUNNER])
with tempfile.TemporaryDirectory() as td:
    tmpf = pathlib.Path(td) / "runner_member.py"
    tmpf.write_bytes(served.get(RUNNER, b""))
    _, served_id = run(["git", "hash-object", "--no-filters", str(tmpf)])
member = served.get(RUNNER, b"")
det = ["THE MINTED VERSION (bound by id) s3://%s/%s ETag %s VersionId %s, %d bytes, LastModified %s"
       % (b["bucket"], b["s3_key"], cur["ETag"].strip('"'), cur.get("VersionId"), len(body),
          cur["LastModified"].isoformat()),
       "md5(downloaded) == ETag: %s   sha256(downloaded) = %s" % (hashlib.md5(body).hexdigest() == MINTED["etag"],
                                                                 sha256(body)),
       "INFO -- currently served: VersionId %s (%s)" % (live.get("VersionId"), "the minted version"
                                                       if live.get("VersionId") == MINTED["version"]
                                                       else "a LATER one; the grade stays on the minted one"),
       "source-repo-paths names %d of %d closure members; members served %d"
       % (len([c for c in closure if c in srp]), len(closure), len(served)),
       "stamp directory-runner-sha256 %s == sha256(member): %s"
       % (meta.get(by_spec[RUNNER]["sha_metadata_key"], ""), meta.get(by_spec[RUNNER]["sha_metadata_key"], "")
          == sha256(member)),
       "NEGATIVE CONTROL vs IB-rtc-2's object (ETag %s, v %s): ETag %s, VersionId %s, runner member sha256 %s -> %s"
       % (PRE_CELL["etag"], PRE_CELL["version"], "DIFFERS" if cur["ETag"].strip('"') != PRE_CELL["etag"] else "SAME",
          "DIFFERS" if cur.get("VersionId") != PRE_CELL["version"] else "SAME", sha256(pre_runner)[:12],
          sha256(member)[:12]),
       "directory_runner.py in the tarball: git hash-object %s sha256 %s" % (served_id.strip(), sha256(member)),
       "directory_runner.py at the mint commit %s: git blob %s sha256 %s"
       % (MINT_COMMIT, blob_id.strip(), sha256(blob) if blob else None),
       "directory_runner.py at the ledger close %s: git blob %s (the cell's tip before its deliverables)"
       % (CLOSE_COMMIT, close_id.strip()),
       "INFO -- directory_runner.py at HEAD: git blob %s (%s)" % (head_id.strip(), "the same"
                                                                  if head_id.strip() == blob_id.strip()
                                                                  else "MOVED after this cell")]
differs = cur["ETag"].strip('"') != PRE_CELL["etag"] and cur.get("VersionId") != PRE_CELL["version"]     and sha256(pre_runner) != sha256(member)
ok_b = (hashlib.md5(body).hexdigest() == MINTED["etag"] and cur.get("VersionId") == MINTED["version"]
        and all(c in srp for c in closure) and len(closure) == 8 and differs and blob is not None
        and member == blob and served_id.strip() == blob_id.strip() == close_id.strip()
        and meta.get(by_spec[RUNNER]["sha_metadata_key"], "") == sha256(member))
record("(b) RE-MINT", ok_b, det)

# ============================================================ (c) consistency, read-only
v, lines, rows = cons.check(MINT_COMMIT, version_id=MINTED["version"], loose_versions=LOOSE_LEFT_BY_IB_RTC_2)
_, commits = run(["git", "log", "--format=%h", CELL_RANGE, "--"] + sorted(LOOSE_LEFT_BY_IB_RTC_2))
commits = commits.split()
now_versions = {}
for rel in LOOSE_LEFT_BY_IB_RTC_2:
    t = sdc.file_to_s3_target(rel)
    now_versions[rel] = s3.head_object(Bucket=t[0], Key=t[1]).get("VersionId")
det = ["  " + ln for ln in lines]
det.append("commits to the three distribution members in %s: %d %s" % (CELL_RANGE, len(commits), commits))
det.append("INFO -- loose VersionIds now vs as IB-rtc-2 left them: %s"
           % {k.split("/")[1]: ("UNCHANGED" if now_versions[k] == vv else "MOVED") for k, vv in
              LOOSE_LEFT_BY_IB_RTC_2.items()})
ok_c = v == "CONSISTENT" and len(rows) == 3 and not commits
record("(c) CONSISTENCY", ok_c, det)

# ============================================================ (d) the host
ec2, ssm = boto3.client("ec2", region_name=REGION), boto3.client("ssm", region_name=REGION)
state = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]["State"]["Name"]
info = ssm.describe_instance_information(
    Filters=[{"Key": "InstanceIds", "Values": [INSTANCE]}])["InstanceInformationList"]
ping = info[0]["PingStatus"] if info else "(absent)"
base = "/tmp/irpt-rtc8-%s" % dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
CHECK_PY = r'''
import importlib.util, os, socket, sys
events = []
def hook(ev, args):
    if ev in ("socket.connect", "socket.getaddrinfo", "http.client.connect"):
        addr = args[0] if ev == "socket.getaddrinfo" else (args[1] if len(args) > 1 else None)
        events.append((ev, str(addr)))
sys.addaudithook(hook)
def imds(e):
    return "169.254.169.254" in e[1] or "fd00:ec2::254" in e[1]
def split(evs):
    return len([e for e in evs if not imds(e)]), len([e for e in evs if imds(e)])
root = sys.argv[1]
p = root + "/data/assets/scripts/gold/investor_reporting/directory_runner.py"
try:
    spec = importlib.util.spec_from_file_location("directory_runner", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
except BaseException as e:
    print("[rtc8] MODULE-IMPORT-FAIL %s: %s" % (type(e).__name__, e)); sys.exit(0)
print("[rtc8] MODULE-IMPORT-OK SOURCE_SETS=%r" % (sorted(m.SOURCE_SETS),))
for firm in sorted(m.SOURCE_SETS):
    try:
        m.SOURCE_SETS[firm](); print("[rtc8] IMPORT-OK %s" % firm)
    except BaseException as e:
        print("[rtc8] IMPORT-FAIL %s %s: %s" % (firm, type(e).__name__, e))
# UNSET: construct, then open the lazy seam WITHOUT a read.
os.environ.pop(m.SOURCE_ROLE_ENV, None)
n0 = len(events)
f = m.Firm49F()
c_con = split(events[n0:])
print("[rtc8] UNSET construct-warn=%s gold-client-none=%s" % (
    any(x.startswith("WARN:") and m.SOURCE_ROLE_ENV in x for x in f.notes), f._gold_client is None))
n1 = len(events)
client = f._gold()
c_seam = split(events[n1:])
warn = [x for x in f.notes if x.startswith("WARN:") and m.SOURCE_ROLE_ENV in x]
print("[rtc8] UNSET construct-events service=%d imds=%d" % c_con)
print("[rtc8] UNSET seam-events service=%d imds=%d" % c_seam)
print("[rtc8] UNSET warn=%s host-session=%s" % (bool(warn), client is f.rc.s3()))
print("[rtc8] UNSET note: %s" % (warn[0] if warn else "(none)"))
# SET to a valid-shaped, non-existent ARN: construct only; the assumption is lazy.
os.environ[m.SOURCE_ROLE_ENV] = sys.argv[2]
n2 = len(events)
g = m.Firm49F()
c_set = split(events[n2:])
print("[rtc8] SET construct-events service=%d imds=%d assumed=%s" % (c_set[0], c_set[1], g._gold_client is not None))
n3 = len(events)
try:
    socket.getaddrinfo("localhost", None)
except OSError:
    pass
print("[rtc8] NET-POSITIVE-CONTROL %s" % (len(events) > n3))
'''
closure_paths = closure or IB_RTC_2_CLOSURE
host_cmds = [
    "set -u", "B=%s" % base, "rm -rf $B && mkdir -p $B/W",
    # The host role has s3:GetObject on the key but no s3:GetObjectVersion (measured at IB-rtc-2): it fetches
    # the key as the dispatch does, and the arm binds it to the minted version by sha256.
    "aws s3 cp s3://%s/%s $B/bundle.tar.gz --only-show-errors || { echo '[rtc8] FETCH-FAIL'; exit 90; }"
    % (b["bucket"], b["s3_key"]),
    "echo \"[rtc8] bundle sha256 $(sha256sum $B/bundle.tar.gz | cut -d' ' -f1)\"",
    "tar -tzf $B/bundle.tar.gz | sed 's/^/[rtc8] member /'",
    "tar -xzf $B/bundle.tar.gz -C $B/W && echo '[rtc8] EXTRACT-OK' || echo '[rtc8] EXTRACT-FAIL'",
] + ["[ -f $B/W/%s ] && echo '[rtc8] placed %s' || echo '[rtc8] ABSENT %s'" % (c, c, c) for c in closure_paths] + [
    "cat > $B/check.py <<'PYEOF'", CHECK_PY.strip("\n"), "PYEOF",
    "cd /tmp && python3 $B/check.py $B/W '%s' 2>&1" % NONEXISTENT_ARN,
    "echo '[rtc8] END'",
]
det = ["host %s state=%s ssm=%s (this battery never starts or stops it)" % (INSTANCE, state, ping)]
out, cmd_id = "", None
if state == "running" and ping == "Online":
    r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                         Comment="IRPT IB-rtc-8 read-only K5 check (/tmp only)",
                         Parameters={"commands": host_cmds, "executionTimeout": ["600"]})
    cmd_id = r["Command"]["CommandId"]
    inv = {}
    for _ in range(90):
        time.sleep(5)
        try:
            inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=INSTANCE)
        except Exception:                          # noqa: BLE001
            continue
        if inv.get("Status") not in ("Pending", "InProgress", "Delayed"):
            break
    out = inv.get("StandardOutputContent", "")
    det.append("SSM command %s status=%s rc=%s" % (cmd_id, inv.get("Status"), inv.get("ResponseCode")))
else:
    det.append("NOT-EVALUATED: the host is not running+Online.")
g = lambda pat: re.findall(pat, out, re.M)   # noqa: E731
host_sha = g(r"^\[rtc8\] bundle sha256 ([0-9a-f]{64})$")
placed = g(r"^\[rtc8\] placed (.+)$")
oks = g(r"^\[rtc8\] IMPORT-OK (\S+)$")
un_con = g(r"^\[rtc8\] UNSET construct-events service=(\d+) imds=(\d+)$")
un_seam = g(r"^\[rtc8\] UNSET seam-events service=(\d+) imds=(\d+)$")
un_warn = g(r"^\[rtc8\] UNSET warn=(\S+) host-session=(\S+)$")
un_cwarn = g(r"^\[rtc8\] UNSET construct-warn=(\S+) gold-client-none=(\S+)$")
un_note = g(r"^\[rtc8\] UNSET note: (.+)$")
set_con = g(r"^\[rtc8\] SET construct-events service=(\d+) imds=(\d+) assumed=(\S+)$")
pc = g(r"^\[rtc8\] NET-POSITIVE-CONTROL (\S+)$")
det += ["host sha256(bundle) %s == the MINTED version's %s: %s" % (host_sha[0] if host_sha else None, sha256(body),
                                                                   bool(host_sha) and host_sha[0] == sha256(body)),
        "extracted at one /tmp root, each at its repo path: %d of %d" % (len(placed), len(closure_paths)),
        "IMPORT-OK %d of 3 %s" % (len(oks), oks),
        "UNSET: construction events (service, imds) %s; the lazy seam opened without a read %s; WARN %s; "
        "host session %s" % (un_con, un_seam, un_warn[0][0] if un_warn else None, un_warn[0][1] if un_warn else None),
        "UNSET at construction (WARN in notes, client unbuilt) %s -- the WARN is emitted by the lazy seam "
        "_gold(), not by __init__ (row IRPT_BCKEND-S70)" % un_cwarn,
        "UNSET note: %s" % (un_note[0] if un_note else None),
        "SET (non-existent ARN): construction events (service, imds, assumed) %s" % set_con,
        "network positive control fired: %s" % (pc[0] if pc else None)]
host_up = cmd_id is not None
ok_d = (host_up and bool(host_sha) and host_sha[0] == sha256(body) and len(placed) == len(closure_paths) == 8
        and len(oks) == 3 and un_con == [("0", "0")] and bool(un_seam) and un_seam[0][0] == "0"
        and un_warn == [("True", "True")] and un_cwarn == [("False", "True")]
        and set_con == [("0", "0", "False")] and pc == ["True"])
record("(d) HOST", ok_d if host_up else None, det)

print("R-40 identities:")
print("  minted bundle: ETag %s  VersionId %s  sha256 %s" % (MINTED["etag"], MINTED["version"], sha256(body)))
print("  directory_runner.py member: git blob %s  sha256 %s" % (served_id.strip(), sha256(served.get(RUNNER, b""))))
if cmd_id:
    print("  host command %s  host sha256 %s" % (cmd_id, host_sha[0] if host_sha else None))
print()
passed = sum(1 for _, ok in results if ok)
print("R38-AC1: %d of %d graded arms PASS" % (passed, len(results)))
if passed == len(results):
    print("IBR38-BUNDLE-REMINTED-49F-ABOARD")
    sys.exit(0)
print("BLOCKED: not every graded arm passed; the expect token is withheld")
sys.exit(1)
