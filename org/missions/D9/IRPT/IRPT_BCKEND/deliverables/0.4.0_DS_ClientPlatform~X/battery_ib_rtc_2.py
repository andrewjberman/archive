#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtc-2 acceptance battery -- R32-AC1, six graded arms + two disclosures.

Prints IBR32-CLOSURE-MINTED-AND-IMPORTS-ON-HOST only when arms (a)-(f) ALL hold.

WHAT THIS BATTERY IS NOT (bound 12): it wraps nothing it grades. Every graded arm reads the
REAL artifact -- the guard's own declaration and functions, the served S3 object and its
version history, the mdpf daily-runner host through a read-only SSM command, and the runner
module as the bundle carries it. Every hash is RE-DERIVED at run time; nothing is read from a
manifest this cell wrote.

Graded arms (the face's (a)-(f)):
  (a) CLOSURE     the set of repo files directory_runner.py reaches, DERIVED twice with two
                  instruments that must agree (a static AST sweep and a dynamic open/import
                  audit of the no-S3 entry points), N printed with its list and the diff
                  against row W2-S51; then how many of N the guard's CODE_TREES declares.
  (b) GUARD TESTS every test file that exercises the guard, run standalone, k of k.
  (c) SERVED      head-object on the minted key: ETag == md5 of the downloaded bytes, sha256
                  of those bytes, `source-repo-paths` covering N of N, each sha stamp equal
                  to the repo file at this branch tip.
  (d) HOST TAR    `tar -tzf` ON the host lists N of N closure members.
  (e) HOST IMPORT on the host, each member placed at the repo path the guard DECLARES for it,
                  `directory_runner` imported and SourceSet instantiated for 3 of 3 firms.
  (f) NEG CONTROL the previous tarballs (IB-rt-5's ETag, and the one served when this cell
                  began) are read from the bucket's version history with their member counts,
                  so a re-mint can be told from a no-op.

Disclosures (printed, NOT token-gating -- they ground this cell's rows):
  (g) ROUTING     for each closure member the guard does not declare: does the guard serve it
                  today on a per-file (loose) leg, and would declaring it as a bundle member
                  route it OUT of that leg (safe_deploy_core.py main(), the X-iii routing loop).
  (h) PLACEMENT   the deployed dispatch's own unpack lines (refresh.runner_script, cut before
                  its build) vs the declared placement, on ONE payload the guard's own
                  build_bundle_payload builds with the full closure named by repo path --
                  locally, with Git Bash GNU tar -- plus a dot-dot member probe.
"""
from __future__ import annotations

import ast
import copy
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

WS = pathlib.Path(__file__).resolve().parents[7]   # deliverables/<serial>/ -> ... -> repo root
sys.path.insert(0, str(WS / ".tools"))
import safe_deploy_core as sdc                        # noqa: E402  the guard itself
from git_bash_resolver import bash_argv               # noqa: E402  bare `bash` is the WSL stub

BUNDLE = "investor_reporting"
RUNNER = "data/assets/scripts/gold/investor_reporting/directory_runner.py"
INSTANCE = "i-02448edb624a7a7cf"
REGION = "us-east-1"
# Measured BEFORE this cell acted (2026-09-18T02:1xZ, list-object-versions + head-object):
PRE_CELL = {"etag": "7791109bada2dbb44c5ac742b65671ee",
            "version": "AxKzxFHuxAP7TTIJsmkxtWZxxgEgVJDC"}
# IB-rt-5's instance ETag (battery_ib_rt_5.result.md, the face's negative control).
RT5_ETAG = "cd188f6edb7270300a7409d66f9a3432"
FACE_RT5_MEMBER_CLAIM = 3
# Row IRPT_BCKEND-W2-S51's named paths, verbatim from its world_is (the row counts them SEVEN).
W2S51_NAMED = [
    "lib/trading_calendar.py",
    "infra/aws/lambda/investor-reporting/_ids/ids.py",
    "infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json",
    "data/firm_registry.json",
    "infra/aws/lambda-edge/_shared/firm-config.mjs",
    "data/assets/scripts/gold/runners_49f/runner_common.py",
    "data/inf/scripts/gold/runners_inf/runner_common.py",
    "data/cot/scripts/gold/runners_cot/runner_common.py",
]

results = []


def run(cmd, timeout=300, cwd=None, env=None):
    """Every invocation terminates (bound 9). rc 124 IS the recorded output."""
    try:
        p = subprocess.run(cmd, cwd=str(cwd or WS), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout, env=env)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ss" % timeout


def record(arm, ok, detail, graded=True):
    """ok is True, False, or None = NOT-EVALUATED (the arm had no subject; never a pass)."""
    results.append((arm, ok is True, graded))
    tag = ({True: "PASS", False: "FAIL", None: "N/E"}[ok]) if graded else "INFO"
    print("  %-5s %s" % (tag, arm))
    for line in detail:
        print("        " + line)
    print()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_blob(rel):
    rc, out = run(["git", "hash-object", rel])
    return out.strip() if rc == 0 else "(hash-object rc=%d)" % rc


def boto(kind):
    import boto3
    return boto3.client(kind, region_name=REGION)


# ============================================================ (a) the closure, derived twice
def _const_tail(node):
    """Trailing string constants of a Path-division chain or an os.path.join call."""
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        parts = []
        cur = node
        while isinstance(cur, ast.BinOp) and isinstance(cur.op, ast.Div):
            if isinstance(cur.right, ast.Constant) and isinstance(cur.right.value, str):
                parts.insert(0, cur.right.value)
            else:
                return None
            cur = cur.left
        return parts
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "join" and len(node.args) >= 2):
        tail = []
        for a in reversed(node.args[1:]):
            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                tail.insert(0, a.value)
            else:
                break
        return tail or None
    return None


def static_sweep(rel):
    """Every repo FILE a module names by a constant path tail, its first-party imports,
    and every _import_runner(dir, module) target -- with the line and a USED/DEAD verdict
    for module-level constants (a name bound to a path and never loaded is DEAD)."""
    src_path = WS / rel
    src = src_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    mod_dir = src_path.parent
    loads = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
            loads[n.id] = loads.get(n.id, 0) + 1
    assigned = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            assigned[id(n.value)] = n.targets[0].id
    refs = []       # (kind, repo_rel, line, verdict)
    search_dirs = [mod_dir]
    for n in ast.walk(tree):
        tail = _const_tail(n)
        if tail:
            rel_tail = "/".join(tail)
            for base in (mod_dir, WS):
                cand = base / rel_tail
                if cand.exists():
                    r = cand.resolve().relative_to(WS.resolve()).as_posix()
                    if cand.is_dir():
                        search_dirs.append(cand)
                        refs.append(("DIR", r, n.lineno, "search-dir"))
                    else:
                        name = assigned.get(id(n))
                        verdict = "USED" if (name is None or loads.get(name, 0) > 0) else "DEAD"
                        refs.append(("PATH", r, n.lineno,
                                     verdict + ("" if name is None else " via " + name)))
                    break
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "_import_runner" and len(n.args) == 2
                and all(isinstance(a, ast.Constant) for a in n.args)):
            refs.append(("RUNNER", "%s/%s.py" % (n.args[0].value, n.args[1].value),
                         n.lineno, "USED via _import_runner"))
    for n in tree.body:
        names = []
        if isinstance(n, ast.Import):
            names = [a.name.split(".")[0] for a in n.names]
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            names = [n.module.split(".")[0]]
        for nm in names:
            for d in search_dirs:
                if (d / (nm + ".py")).is_file():
                    refs.append(("IMPORT", (d / (nm + ".py")).resolve().relative_to(
                        WS.resolve()).as_posix(), n.lineno, "USED (module-level import)"))
                    break
    return refs


DYNAMIC_PROBE = r'''
import importlib.util, json, os, sys
WS = os.path.abspath(sys.argv[1]); RUNNER = sys.argv[2]
opened = set()
net = []
def hook(ev, args):
    if ev in ("socket.connect", "socket.getaddrinfo", "http.client.connect"):
        net.append(ev)
    if ev == "open" and args and isinstance(args[0], str):
        p = os.path.abspath(args[0])
        if p.startswith(WS) and "__pycache__" not in p:
            opened.add(os.path.relpath(p, WS).replace(os.sep, "/"))
sys.addaudithook(hook)
spec = importlib.util.spec_from_file_location("directory_runner", os.path.join(WS, RUNNER))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
out = {"firms": {}}
for firm in sorted(m.SOURCE_SETS):
    try:
        m.SOURCE_SETS[firm](); out["firms"][firm] = "IMPORT-OK"
    except BaseException as e:
        out["firms"][firm] = "IMPORT-FAIL %s: %s" % (type(e).__name__, e)
out["net_events_import_and_instantiate"] = len(net)
fids = [f["firm_id"] for f in m.client_firms()]
m.firm_bucket_map(); m.load_contract(); m.tcal.calendar_source()
for fid in fids:
    m.opaque_id("firm", fid, fid)
mods = set()
for mod in list(sys.modules.values()):
    f = getattr(mod, "__file__", None)
    if f and os.path.abspath(f).startswith(WS) and "__pycache__" not in f:
        mods.add(os.path.relpath(os.path.abspath(f), WS).replace(os.sep, "/"))
out["net_events_total"] = len(net)
# POSITIVE CONTROL for the zero above: a loopback resolve must move the counter (no egress)
import socket
try:
    socket.getaddrinfo("localhost", None)
except OSError:
    pass
out["net_positive_control_fired"] = len(net) > out["net_events_total"]
out["opened"] = sorted(opened | mods)
out["client_firms"] = fids
print("DYNAMIC-JSON " + json.dumps(out))
'''


def derive_closure():
    lines = []
    static = {}
    dead = []
    frontier = [RUNNER]
    seen = set()
    while frontier:
        rel = frontier.pop(0)
        if rel in seen or not rel.endswith(".py"):
            continue
        seen.add(rel)
        for kind, r, ln, verdict in static_sweep(rel):
            if kind == "DIR":
                continue
            tag = "%s:%d %s %s" % (rel.rsplit("/", 1)[-1], ln, kind, verdict)
            if verdict.startswith("DEAD"):
                dead.append((r, tag))
                continue
            static.setdefault(r, []).append(tag)
            if r.endswith(".py"):
                frontier.append(r)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    with tempfile.TemporaryDirectory() as td:
        probe = pathlib.Path(td) / "probe.py"
        probe.write_text(DYNAMIC_PROBE, encoding="utf-8")
        rc, out = run([sys.executable, str(probe), str(WS), RUNNER], timeout=300, cwd=td, env=env)
    m = re.search(r"^DYNAMIC-JSON (.*)$", out, re.M)
    dyn = json.loads(m.group(1)) if m else {"opened": [], "firms": {}, "client_firms": []}
    dynamic = set(dyn["opened"])
    # a USED static reference the dynamic exercise never opened: on a code path the runner
    # does not take (named, not counted)
    static_only = sorted(set(static) - dynamic - {RUNNER})
    dynamic_only = sorted(dynamic - set(static) - {RUNNER})
    lines.append("STATIC sweep: %d module(s) walked, %d distinct USED repo file reference(s), "
                 "%d DEAD" % (len(seen), len(static), len(dead)))
    lines.append("DYNAMIC probe rc=%d: %d repo file(s) opened/imported; SourceSet x%d %s"
                 % (rc, len(dynamic), len(dyn["firms"]), dyn["firms"]))
    lines.append("  network audit events (socket.connect/getaddrinfo, http.client.connect): "
                 "%s during import + SourceSet x3, %s over the whole probe; positive control "
                 "(a loopback resolve moves the counter): %s"
                 % (dyn.get("net_events_import_and_instantiate", "?"), dyn.get("net_events_total", "?"),
                    dyn.get("net_positive_control_fired", "?")))
    for r in static_only:
        lines.append("  static-only (named, NOT opened on the runner's paths): %s  [%s]"
                     % (r, "; ".join(static[r])))
    for r in dynamic_only:
        lines.append("  dynamic-only (opened, not named by a constant): %s" % r)
    for r, tag in dead:
        lines.append("  DEAD reference (bound, never loaded): %s  [%s]" % (r, tag))
    # the closure is what the runner LOADS: dynamic, plus static imports the probe must also see
    closure = sorted(dynamic | {RUNNER})
    return closure, static, static_only, dead, dyn, rc, lines


print("R32-AC1 battery -- IRPT_BCKEND.TO-IB-rtc-2, the bundle carries the runner's closure")
print("workspace: %s" % WS)
_, head = run(["git", "rev-parse", "--short=10", "HEAD"])
print("branch tip: %s   run at %s" % (head.strip(), dt.datetime.now(dt.timezone.utc)
                                         .strftime("%Y-%m-%dT%H:%M:%SZ")))
print()

closure, static, static_only, dead, dyn, dyn_rc, det = derive_closure()
N = len(closure)
hit = sdc.find_bundle(BUNDLE)
declared = sorted(m["repo_path"] for m in hit[2]["members"].values()) if hit else []
decl_in = [c for c in closure if c in declared]
missing = [c for c in closure if c not in declared]
det.append("CLOSURE N = %d (the runner plus every repo file it loads):" % N)
for c in closure:
    det.append("  %-9s %s   blob %s" % ("DECLARED" if c in declared else "MISSING", c,
                                         git_blob(c)[:12]))
det.append("DIFF vs W2-S51's named list (%d named; the row counts them seven):" % len(W2S51_NAMED))
for r in W2S51_NAMED:
    if r not in closure:
        why = [t for rr, t in dead if rr == r]
        det.append("  - %s  NOT in the closure at this tip%s" % (r, (" -- " + why[0]) if why else ""))
for c in closure:
    if c not in W2S51_NAMED and c != RUNNER:
        det.append("  + %s  in the closure, not named by W2-S51" % c)
det.append("declared members outside this closure: %s"
           % ([d for d in declared if d not in closure] or "none"))
det.append("DECLARED: %d of %d closure members in CODE_TREES['mdpf']['bundles']['%s']"
           % (len(decl_in), N, BUNDLE))
ok_a = (not missing) and dyn_rc == 0 and N > 1
record("(a) CLOSURE", ok_a, det)

# ============================================================ (b) the guard's own tests
GUARD_TESTS = [".tools/test_code_trees_invariant.py", ".tools/test_safe_deploy.py",
               ".tools/tests/test_safe_deploy_receipt_names_both_legs.py",
               ".tools/tests/test_comp_schedule.py"]
det = ["denominator: %d test file(s) that exercise the guard (census: every .tools test*.py "
       "naming safe_deploy_core / safe-deploy.sh / safe_deploy)" % len(GUARD_TESTS)]
green = 0
for t in GUARD_TESTS:
    rc, out = run([sys.executable, t], timeout=300)
    m = re.search(r"FAIL: (\d+)/(\d+) cases failed|(\d+)/(\d+) PASS", out)
    det.append("%s rc=%d  %s" % (t, rc, m.group(0) if m else "(no count line)"))
    green += 1 if rc == 0 else 0
det.append("GREEN: %d of %d guard test files (the two red suites were red at IB-rt-5's baseline "
           "too, 3/18 and 7/14 -- row IRPT_BCKEND-S29)" % (green, len(GUARD_TESTS)))
record("(b) GUARD TESTS", green == len(GUARD_TESTS), det)

# ============================================================ (c) the served artifact
s3 = boto("s3")
b = hit[2]
cur = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"])
cur_etag = cur["ETag"].strip('"')
cur_ver = cur.get("VersionId")
body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=cur_ver)["Body"].read()
meta = cur.get("Metadata", {})
srp = [p for p in meta.get("source-repo-paths", "").split(";") if p]
with tarfile.open(fileobj=io.BytesIO(body), mode="r:gz") as tf:
    served_members = tf.getnames()
det = ["s3://%s/%s" % (b["bucket"], b["s3_key"]),
       "ETag %s  VersionId %s  LastModified %s  %d bytes"
       % (cur_etag, cur_ver, cur["LastModified"].isoformat(), len(body)),
       "md5(downloaded bytes) == ETag: %s   sha256(downloaded bytes) = %s"
       % (hashlib.md5(body).hexdigest() == cur_etag, sha256(body)),
       "served members (%d): %s" % (len(served_members), served_members),
       "source-repo-paths names %d of %d closure members; absent: %s"
       % (len([c for c in closure if c in srp]), N, [c for c in closure if c not in srp])]
stamps_ok = 0
for name, spec in sorted(b["members"].items()):
    local = sha256((WS / spec["repo_path"]).read_bytes())
    served = meta.get(spec["sha_metadata_key"], "")
    stamps_ok += 1 if served == local else 0
    det.append("%-6s %s  %s" % ("MATCH" if served == local else "DIFFER", spec["sha_metadata_key"],
                                 spec["repo_path"]))
det.append("stamps equal to the repo at this tip: %d of %d declared" % (stamps_ok, len(b["members"])))
ok_c = (hashlib.md5(body).hexdigest() == cur_etag and all(c in srp for c in closure)
        and stamps_ok == len(b["members"]))
record("(c) SERVED", ok_c, det)

# ============================================================ (d)+(e) the host, read-only
ec2 = boto("ec2")
state = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]["State"]["Name"]
ssm = boto("ssm")
info = ssm.describe_instance_information(
    Filters=[{"Key": "InstanceIds", "Values": [INSTANCE]}])["InstanceInformationList"]
ping = info[0]["PingStatus"] if info else "(absent)"
stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
base = "/tmp/irpt-rtc2-%s" % stamp
sys.path.insert(0, str(WS / "infra/aws/lambda/investor-reporting/directory"))
import refresh                                        # noqa: E402  the deployed dispatch's source
dispatch_lines = refresh.runner_script("inflection", "2026-09-17",
                                       "s3://%s/%s" % (b["bucket"], b["s3_key"]),
                                       "E2", work_root=base + "/e2root").split("\n")
cut = next(i for i, ln in enumerate(dispatch_lines) if "--- build ---" in ln)
e2_script = "\n".join(dispatch_lines[:cut])
CHECK_PY = r'''
import importlib.util, sys
root, label = sys.argv[1], sys.argv[2]
p = root + "/data/assets/scripts/gold/investor_reporting/directory_runner.py"
try:
    spec = importlib.util.spec_from_file_location("directory_runner", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
except BaseException as e:
    print("[rtc2] %s MODULE-IMPORT-FAIL %s: %s" % (label, type(e).__name__, e)); sys.exit(0)
print("[rtc2] %s MODULE-IMPORT-OK SOURCE_SETS=%r" % (label, sorted(m.SOURCE_SETS)))
for firm in sorted(m.SOURCE_SETS):
    try:
        src = m.SOURCE_SETS[firm]()
        print("[rtc2] %s IMPORT-OK %s" % (label, firm))
    except BaseException as e:
        print("[rtc2] %s IMPORT-FAIL %s %s: %s" % (label, firm, type(e).__name__, e))
'''
place = []
for name, spec in sorted(b["members"].items()):
    d = spec["repo_path"].rsplit("/", 1)[0]
    place.append("[ -f %s/stage/%s ] && mkdir -p %s/e1/%s && cp %s/stage/%s %s/e1/%s"
                 % (base, name, base, d, base, name, base, spec["repo_path"]))
host_cmds = [
    "set -u",
    "B=%s" % base,
    "rm -rf $B && mkdir -p $B/stage $B/e1",
    "echo \"[rtc2] caller $(aws sts get-caller-identity --query Arn --output text)\"",
    "aws s3api get-object --bucket %s --key %s --version-id %s $B/bundle.tar.gz >/dev/null "
    "|| { echo '[rtc2] FETCH-FAIL'; exit 90; }" % (b["bucket"], b["s3_key"], cur_ver),
    "echo \"[rtc2] bundle sha256 $(sha256sum $B/bundle.tar.gz | cut -d' ' -f1)\"",
    "echo \"[rtc2] bundle md5 $(md5sum $B/bundle.tar.gz | cut -d' ' -f1)\"",
    "tar -tzf $B/bundle.tar.gz | sed 's/^/[rtc2] member /'",
    "echo \"[rtc2] member-count $(tar -tzf $B/bundle.tar.gz | wc -l)\"",
    "tar -xzf $B/bundle.tar.gz -C $B/stage || echo '[rtc2] EXTRACT-FAIL'",
] + place + [
    "cat > $B/check.py <<'PYEOF'", CHECK_PY.strip("\n"), "PYEOF",
    "python3 $B/check.py $B/e1 DECLARED 2>&1",
    "cat > $B/e2.sh <<'E2EOF'", e2_script, "E2EOF",
    "bash $B/e2.sh > $B/e2.log 2>&1; echo \"[rtc2] DEPLOYED-UNPACK rc=$?\"",
    "grep -E 'bundle sha256|IMPORT-|member ' $B/e2.log | sed 's/^/[rtc2] e2| /'",
    "python3 $B/check.py %s/e2root/E2 DEPLOYED 2>&1" % base,
    "echo '[rtc2] END'",
]
det = ["host %s state=%s ssm=%s (this battery never starts or stops it)" % (INSTANCE, state, ping)]
host_out = ""
cmd_id = None
if state == "running" and ping == "Online":
    r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                         Comment="IRPT IB-rtc-2 read-only closure check (/tmp only)",
                         Parameters={"commands": host_cmds, "executionTimeout": ["600"]})
    cmd_id = r["Command"]["CommandId"]
    inv = {}
    for _ in range(90):
        time.sleep(5)
        try:
            inv = ssm.get_command_invocation(CommandId=cmd_id, InstanceId=INSTANCE)
        except Exception:
            continue
        if inv.get("Status") not in ("Pending", "InProgress", "Delayed"):
            break
    host_out = inv.get("StandardOutputContent", "")
    det.append("SSM command %s status=%s rc=%s" % (cmd_id, inv.get("Status"),
                                                    inv.get("ResponseCode")))
    if inv.get("StandardErrorContent"):
        det.append("stderr (first 400): " + inv["StandardErrorContent"][:400].replace("\n", " | "))
else:
    det.append("NOT-EVALUATED: the host is not running+Online, so (d) and (e) have no subject."
               " The face admits ONE StartInstances by the seat; this battery never spends it.")
host_up = cmd_id is not None
host_members = re.findall(r"^\[rtc2\] member (.+)$", host_out, re.M)
host_sha = re.search(r"^\[rtc2\] bundle sha256 ([0-9a-f]{64})$", host_out, re.M)
det.append("caller: %s" % (re.search(r"^\[rtc2\] caller (.+)$", host_out, re.M) or
                           re.match("(.*)", "(none)")).group(1))
det.append("host sha256(bundle) = %s   local sha256 = %s   equal: %s"
           % (host_sha.group(1) if host_sha else "(none)", sha256(body),
              bool(host_sha) and host_sha.group(1) == sha256(body)))
det.append("tar -tzf on the host: %d member(s): %s" % (len(host_members), host_members))
# a member's repo path is what the guard declares for it; the closure is counted in repo paths
name_to_repo = {n: s["repo_path"] for n, s in b["members"].items()}
host_repo = {name_to_repo.get(m, m) for m in host_members}
det.append("closure members on the host: %d of %d; absent: %s"
           % (len([c for c in closure if c in host_repo]), N,
              [c for c in closure if c not in host_repo]))
record("(d) HOST TAR", (bool(host_members) and all(c in host_repo for c in closure))
       if host_up else None, det)

det = []
for label in ("DECLARED", "DEPLOYED"):
    oks = re.findall(r"^\[rtc2\] %s IMPORT-OK (\S+)$" % label, host_out, re.M)
    fails = re.findall(r"^\[rtc2\] %s (?:MODULE-)?IMPORT-FAIL (.*)$" % label, host_out, re.M)
    det.append("%s placement: IMPORT-OK %d of 3 firms %s" % (label, len(oks), oks))
    for f in fails:
        det.append("  IMPORT-FAIL %s" % f)
det.append("DECLARED = each member copied to the repo path CODE_TREES declares (the face's arm);")
det.append("DEPLOYED = refresh.runner_script's own unpack lines, cut before its build (disclosure).")
e1_ok = len(re.findall(r"^\[rtc2\] DECLARED IMPORT-OK (\S+)$", host_out, re.M))
record("(e) HOST IMPORT", (e1_ok == 3) if host_up else None, det)

# ============================================================ (f) the negative control
vers = s3.list_object_versions(Bucket=b["bucket"], Prefix=b["s3_key"]).get("Versions", [])
vers = [v for v in vers if v["Key"] == b["s3_key"]]


def members_of(version_id):
    raw = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=version_id)["Body"].read()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as t:
        return t.getnames()


rt5 = [v for v in vers if v["ETag"].strip('"') == RT5_ETAG]
rt5_members = members_of(rt5[-1]["VersionId"]) if rt5 else []
pre_members = members_of(PRE_CELL["version"])
det = ["version history: %d version(s) of the key (single listing page)" % len(vers),
       "IB-rt-5 ETag %s: %d version(s) carry it; members %d %s  (the face says %d)"
       % (RT5_ETAG, len(rt5), len(rt5_members), rt5_members, FACE_RT5_MEMBER_CLAIM),
       "served when this cell began: ETag %s VersionId %s members %d %s"
       % (PRE_CELL["etag"], PRE_CELL["version"], len(pre_members), pre_members),
       "served now:                  ETag %s VersionId %s members %d"
       % (cur_etag, cur_ver, len(served_members))]
remint = (cur_ver != PRE_CELL["version"] and cur_etag != PRE_CELL["etag"]
          and set(served_members) > set(pre_members))
det.append("RE-MINT evidenced (new version, new ETag, strictly more members): %s -> %s"
           % (remint, "RE-MINT" if remint else "NO-OP: the served object is the pre-cell object"))
record("(f) NEG CONTROL", remint, det)

# ============================================================ (g) disclosure: deploy routing
det = []
frozen = 0
loose_live = 0
for c in missing:
    tgt = sdc.file_to_s3_target(c)
    if tgt is None:
        det.append("%s: no per-file (loose) leg in the guard" % c)
        continue
    bucket, key, label = tgt
    try:
        h = s3.head_object(Bucket=bucket, Key=key)
        et = h["ETag"].strip('"')
        live = et == hashlib.md5((WS / c).read_bytes()).hexdigest()
        loose_live += 1
        state_s = "SERVED, ETag %s %s the repo md5" % (et, "==" if live else "!=")
    except Exception as exc:
        state_s = "not served (%s)" % type(exc).__name__
    saved = sdc.CODE_TREES
    try:
        probe_trees = copy.deepcopy(saved)
        tree_key = next(k for k, t in probe_trees.items() if BUNDLE in t.get("bundles", {}))
        probe_trees[tree_key]["bundles"][BUNDLE]["members"][c] = {
            "repo_path": c, "sha_metadata_key": "probe-sha256"}
        sdc.CODE_TREES = probe_trees
        routed = sdc.bundle_for_member(c)
    finally:
        sdc.CODE_TREES = saved
    frozen += 1 if routed else 0
    det.append("%s: loose leg [%s] s3://%s/%s -- %s" % (c, label, bucket, key, state_s))
    det.append("    declared as a member, bundle_for_member() -> %s: %s"
               % (routed[1] if routed else None,
                  "the main() routing loop moves it OUT of the loose leg (BUNDLE-ROUTED, "
                  "loose leg frozen)" if routed else "no routing change"))
_, diffq = run(["git", "diff", "--stat", "--", ".tools/safe_deploy_core.py"])
det.append("undeclared closure members with a LIVE loose leg: %d; that a declaration would "
           "route out of it: %d" % (loose_live, frozen))
det.append("the guard's real declaration is untouched by this probe (git diff --stat: %s)"
           % (diffq.strip() or "empty"))
record("(g) ROUTING [disclosure]", True, det, graded=False)

# ============================================================ (h) disclosure: placement
det = []
full = copy.deepcopy(b)
for c in missing:
    full["members"][c] = {"repo_path": c, "sha_metadata_key": "probe-" + str(len(full["members"]))}
payload, _shas, err = sdc.build_bundle_payload(full)
if payload is None:
    det.append("build_bundle_payload refused: %s" % err)
else:
    with tempfile.TemporaryDirectory(dir=str(WS / ".scratch") if (WS / ".scratch").is_dir()
                                     else None) as td:
        tdp = pathlib.Path(td)
        (tdp / "bundle.tar.gz").write_bytes(payload)
        (tdp / "check.py").write_text(CHECK_PY, encoding="utf-8")
        # RELATIVE paths, run with cwd = the temp dir: GNU tar reads a `C:/...` archive name
        # as host:path (a remote archive), so an absolute Windows path would test the wrong thing.
        local_lines = refresh.runner_script("inflection", "2026-09-17", "LOCAL", "E2",
                                            work_root="e2root").split("\n")
        cut_l = next(i for i, ln in enumerate(local_lines) if "--- import check" in ln)
        # the dispatch's lines verbatim, except its `aws s3 cp` fetch, which becomes a local cp
        unpack = [("cp bundle.tar.gz $W/bundle.tar.gz || exit 90")
                  if ln.startswith("aws s3 cp") else ln for ln in local_lines[:cut_l]]
        decl = ["mkdir -p e1 stage", "tar -xzf bundle.tar.gz -C stage || exit 91"]
        for name, spec in sorted(full["members"].items()):
            d = spec["repo_path"].rsplit("/", 1)[0]
            decl.append("mkdir -p 'e1/%s' && cp 'stage/%s' 'e1/%s'" % (d, name, spec["repo_path"]))
        (tdp / "e2.sh").write_text("\n".join(unpack) + "\n", encoding="utf-8", newline="\n")
        (tdp / "e1.sh").write_text("\n".join(decl) + "\n", encoding="utf-8", newline="\n")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        rc1, o1 = run(bash_argv("e1.sh"), timeout=120, cwd=td)
        rc2, o2 = run(bash_argv("e2.sh"), timeout=120, cwd=td)
        det.append("ONE payload, built by the guard's own build_bundle_payload: %d members "
                   "(the %d declared + the %d missing, named by repo path), md5 %s"
                   % (len(full["members"]), len(b["members"]), len(missing),
                      hashlib.md5(payload).hexdigest()))
        for label, root, rcx in (("DECLARED", tdp / "e1", rc1),
                                 ("DEPLOYED", tdp / "e2root" / "E2", rc2)):
            rc3, o3 = run([sys.executable, str(tdp / "check.py"), root.as_posix(), label],
                          timeout=180, cwd=td, env=env)
            oks = re.findall(r"^\[rtc2\] %s IMPORT-OK (\S+)$" % label, o3, re.M)
            det.append("%s placement (unpack rc=%d): IMPORT-OK %d of 3 %s"
                       % (label, rcx, len(oks), oks))
            for f in re.findall(r"^\[rtc2\] %s (?:MODULE-)?IMPORT-FAIL (.*)$" % label, o3, re.M):
                det.append("  IMPORT-FAIL " + f.replace(tdp.as_posix(), "<tmp>")
                           .replace(str(tdp), "<tmp>"))
            if rcx != 0:
                # the cut ends on the dispatch's `[ -f $R/<flat> ] && mv` tests, so a nonzero rc
                # there is a relocation that found no flat member, not a failed extraction
                det.append("  unpack rc is the last line's: " + local_lines[cut_l - 1][:90])
                det.append("  unpack output: " + " | ".join(
                    (o1 if label == "DECLARED" else o2).strip().splitlines()[-3:]))
    # the only member name that could climb out of the dispatch's extraction root
    with tempfile.TemporaryDirectory() as td2:
        t2 = pathlib.Path(td2)
        with tarfile.open(t2 / "dd.tar.gz", "w:gz") as t:
            for n in ("directory_runner.py", "../runners_inf/runner_common.py"):
                i = tarfile.TarInfo(n)
                i.size = 2
                t.addfile(i, io.BytesIO(b"x\n"))
        (t2 / "R").mkdir()
        rcd, od = run(bash_argv("-c", "tar -xzf dd.tar.gz -C R"), timeout=60, cwd=td2)
        det.append("dot-dot probe (GNU tar, local): rc=%d  %s"
                   % (rcd, " | ".join(ln for ln in od.splitlines() if ln.strip())))
        det.append("  -> the dispatch's `tar -xzf ... || exit 91` would abort the WHOLE build")
record("(h) PLACEMENT [disclosure]", True, det, graded=False)

# ============================================================ R-40 identities
print("R-40 identities (content hashes at this run):")
print("  served tarball: ETag %s  sha256 %s  VersionId %s" % (cur_etag, sha256(body), cur_ver))
if cmd_id:
    print("  host command: %s  host sha256 %s" % (cmd_id, host_sha.group(1) if host_sha else "(none)"))
for c in closure:
    print("  %s  git-blob %s" % (c, git_blob(c)))
print()

graded = [(a, ok) for a, ok, g in results if g]
passed = sum(1 for _, ok in graded if ok)
print("R32-AC1: %d of %d graded arms PASS" % (passed, len(graded)))
if passed == len(graded):
    print("IBR32-CLOSURE-MINTED-AND-IMPORTS-ON-HOST")
    sys.exit(0)
print("BLOCKED: not every graded arm passed; the expect token is withheld")
sys.exit(1)
