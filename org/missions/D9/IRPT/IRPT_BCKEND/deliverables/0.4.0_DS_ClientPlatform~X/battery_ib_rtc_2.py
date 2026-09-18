#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtc-2 acceptance battery -- R32-AC1 under AMENDMENT 1 (R-45), five graded arms.

Prints IBR32-CLOSURE-MINTED-AND-IMPORTS-ON-HOST only when arms (a)-(e) ALL hold.

The first pass of this cell (0 of 6, a FAIL as a measurement, rows S58/S59/S60/S62) is committed at
802cee5eab / 39caa17744 and drained at f2fc496c3d; its output is in git history. This re-cut grades
the amended face.

WHAT THIS BATTERY IS NOT (bound 12): it wraps nothing it grades. The flag's tests are the guard's own
test files run as written; the closure is DERIVED at this tip by two instruments; both deploy legs are
read on the REAL served objects; the mutant is a REAL bundle version in the key's history, minted from
a stale tree through the guard and re-graded here without minting anything; the host arm is a
read-only SSM command on the mdpf daily-runner. Every hash is re-derived at run time.

Graded arms:
  (a) FLAG TESTS   the DISTRIBUTION flag's own battery k of k; the guard's four test files with their
                   failing cases compared BY NAME to the pre-edit baseline (no prior pass regressed);
                   the whole .tools suite's before/after logs (RECORDED, committed beside this file,
                   each with its tip) compared -- 0 regressions.
  (b) DECLARED     the closure re-derived at this tip, N printed with the diff against the first
                   pass's 8; N of N declared by repo path; exactly 3 flagged DISTRIBUTION.
  (c) CONSISTENCY  after the REAL commit to one distribution member: both legs agree with the blob
                   for 3 of 3 members, the committed member's legs both moved off the pre-commit
                   bytes; the MUTANT version (bundle minted from the pre-commit tree) reads DIVERGED
                   on exactly that member's bundle leg, and the loose key gained no version in the
                   mutant's window -- one leg advanced, the plane named.
  (d) RE-MINT      the MINTED version's identity, bound by VersionId (ETag, sha256 of downloaded bytes),
                   source-repo-paths naming N of N, every stamp equal to its member's bytes, and
                   the negative control against the pre-cell object 7791109b DIFFERS.
  (e) HOST         on i-02448edb624a7a7cf, read-only: the minted version (by VersionId) to /tmp,
                   N of N closure members listed and extracted REPO-SHAPED at one /tmp root,
                   directory_runner imported and SourceSet instantiated IMPORT-OK 3 of 3, 0
                   network events with a positive control that fires.
"""
from __future__ import annotations

import ast
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
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(WS / ".tools"))
sys.path.insert(0, str(HERE))
import safe_deploy_core as sdc                        # noqa: E402  the guard itself
import consistency_ib_rtc_2 as cons                   # noqa: E402  the two-leg check (one instrument)

BUNDLE = "investor_reporting"
RUNNER = "data/assets/scripts/gold/investor_reporting/directory_runner.py"
INSTANCE = "i-02448edb624a7a7cf"
REGION = "us-east-1"
BASE = "65a95ae8db"   # the amendment's cut: the pre-edit tree
PRE_CELL = {"etag": "7791109bada2dbb44c5ac742b65671ee", "version": "AxKzxFHuxAP7TTIJsmkxtWZxxgEgVJDC",
            "members": 4}
FIRST_PASS_CLOSURE = sorted([
    RUNNER,
    "data/assets/scripts/gold/runners_49f/runner_common.py",
    "data/cot/scripts/gold/runners_cot/runner_common.py",
    "data/firm_registry.json",
    "data/inf/scripts/gold/runners_inf/runner_common.py",
    "infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json",
    "infra/aws/lambda/investor-reporting/_ids/ids.py",
    "lib/trading_calendar.py",
])
FLAGGED_EXPECTED = sorted([
    "data/assets/scripts/gold/runners_49f/runner_common.py",
    "data/inf/scripts/gold/runners_inf/runner_common.py",
    "data/cot/scripts/gold/runners_cot/runner_common.py",
])
# Measured at BASE, before the guard edit (the named baseline the face asks for).
BASELINE_FAILS = {
    ".tools/test_code_trees_invariant.py": (18, [
        "PIPELINE_MAP key set == frozen",
        "PIPELINE_MAP values == frozen (ordering-independent)",
        "state restored after mutation"]),
    ".tools/test_safe_deploy.py": (14, [
        "PASS gold deploy + ETag match",
        "FAIL-NODEPLOY stale ETag detected",
        "FAIL-PARTIAL second upload fails",
        "FAIL-MISMATCH corrupt ETag SHA guard",
        "SERVE-RELEASE removal w/ range ACK proceeds+audits",
        "AUTHOR enumeration notice shows author",
        "NO-REGRESSION clean deploy unchanged"]),
    ".tools/tests/test_safe_deploy_receipt_names_both_legs.py": (4, []),
    ".tools/tests/test_comp_schedule.py": (9, []),
}
DIST_TEST = ".tools/tests/test_safe_deploy_distribution_member.py"
SUITE_BEFORE = HERE / "IB-rtc-2_tools_tests_before.txt"
SUITE_AFTER = HERE / "IB-rtc-2_tools_tests_after.txt"
REAL_MEMBER = "data/cot/scripts/gold/runners_cot/runner_common.py"
# THE ACT'S IDENTITIES, recorded at the act (change-management entry irpt-bckend-rtc2-distribution-mint,
# closed at 68e3b02bcb). BOUND TO IDENTITY, NEVER POSITION: a commit by hash and every served object by
# VersionId, so a grader running this AFTER the drain -- on the shared tree, with later commits and later
# mints on top -- re-grades exactly these objects. Each is RE-GRADED below against the live store;
# none is trusted as a verdict.
ACT = {
    "real_commit": "d3508ff7143066f64c3e03070e6e6d7cb943bb59",   # L3
    "guard_commit": "0f8608947180437b02e977b997069ef5406d0414",  # L1a
    "bundle_after_deploy": "DVjQwk752KtYZFHYEZMsE36.T84hAumm",   # L4's mint (both legs)
    "mutant_version": "MpTRS5v.gk_0rrd7fkGz8Fp7z281noBB",        # L6: minted from the pre-L3 tree
    "bundle_final": "1jPgGCGLP.uGY5RpMlMJTrKvKzvyYf7O",          # L6 restore: the served result
    "loose_after_deploy": {                                       # each member's loose VersionId after L4
        "data/assets/scripts/gold/runners_49f/runner_common.py": "jnnxQWbVT_lx6WlJu8HbVXNjQJpYK00w",
        "data/cot/scripts/gold/runners_cot/runner_common.py": "bobsNlnmKIjMyMW8PHxiQVeJCXPIJmOs",
        "data/inf/scripts/gold/runners_inf/runner_common.py": "z_WDDmx6004thBhXbT0uBvsDkNibZQF8",
    },
    "loose_before": ("vrG96E7lhDeuxXs0IZigxHF0arWLhu_L", "384920cf9eb601ea7a344493d1a09d6a"),
    "mutant_window": ("2026-09-18T04:05:30Z", "2026-09-18T04:08:05Z"),
}

results = []


def run(cmd, timeout=300, cwd=None, env=None):
    """Every invocation terminates (bound 9). rc 124 IS the recorded output."""
    try:
        p = subprocess.run(cmd, cwd=str(cwd or WS), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout, env=env)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ss" % timeout


def record(arm, ok, detail):
    """ok is True, False, or None = NOT-EVALUATED (the arm had no subject; never a pass)."""
    results.append((arm, ok is True))
    print("  %-5s %s" % ({True: "PASS", False: "FAIL", None: "N/E"}[ok], arm))
    for line in detail:
        print("        " + line)
    print()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def md5(b):
    return hashlib.md5(b).hexdigest()


def git_bytes(ref, rel):
    p = subprocess.run(["git", "show", "%s:%s" % (ref, rel)], capture_output=True, cwd=str(WS), timeout=30)
    return p.stdout if p.returncode == 0 else None


def boto(kind):
    import boto3
    return boto3.client(kind, region_name=REGION)


print("R32-AC1 battery (AMENDMENT 1, R-45) -- IRPT_BCKEND.TO-IB-rtc-2")
print("workspace: %s" % WS)
_, head = run(["git", "rev-parse", "--short=10", "HEAD"])
print("branch tip: %s   base: %s   run at %s" % (head.strip(), BASE, dt.datetime.now(dt.timezone.utc)
                                                 .strftime("%Y-%m-%dT%H:%M:%SZ")))
print()

# ============================================================ (a) the flag's tests
det = []
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
rc, out = run([sys.executable, DIST_TEST], timeout=300, env=env)
m = re.search(r"DISTRIBUTION-MEMBER BATTERY: (\d+)/(\d+) PASS", out)
k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
det.append("%s rc=%d: %d of %d arms PASS" % (DIST_TEST, rc, k, n))
for ln in out.splitlines():
    if ln.strip().startswith("[FAIL]"):
        det.append("  " + ln.strip())
ok_dist = rc == 0 and n > 0 and k == n
regress = []
for t, (total, fails) in sorted(BASELINE_FAILS.items()):
    rc, out = run([sys.executable, t], timeout=300, env=env)
    now_fail = [ln.strip()[len("FAIL"):].strip() for ln in out.splitlines()
                if re.match(r"^\s+FAIL\s", ln)]
    mm = re.search(r"FAIL: (\d+)/(\d+) cases failed|(\d+)/(\d+) PASS", out)
    new = [f for f in now_fail if f not in fails]
    gone = [f for f in fails if f not in now_fail]
    regress += new
    det.append("%s rc=%d %s -- failing now %d (baseline %d of %d, named); NEW failures %d%s; "
               "baseline failures that now pass %d"
               % (t, rc, mm.group(0) if mm else "(no count line)", len(now_fail), len(fails), total,
                  len(new), (" " + str(new)) if new else "", len(gone)))
before, after = {}, {}
for path, dst in ((SUITE_BEFORE, before), (SUITE_AFTER, after)):
    if path.exists():
        for ln in path.read_text(encoding="utf-8").splitlines():
            mm = re.match(r"^rc=(\d+) (\S+)$", ln)
            if mm:
                dst[mm.group(2)] = int(mm.group(1))
passed_before = {t for t, r in before.items() if r == 0}
suite_regress = sorted(t for t in passed_before if after.get(t, -1) != 0)
heads = [p.read_text(encoding="utf-8").splitlines()[0] if p.exists() else "(absent)"
         for p in (SUITE_BEFORE, SUITE_AFTER)]
det.append("whole .tools suite, RECORDED (not re-run here; each log carries its tip): before %d files "
           "[%s], after %d files [%s]" % (len(before), heads[0], len(after), heads[1]))
det.append("  passed before: %d; of those failing after: %d %s; new files after: %s"
           % (len(passed_before), len(suite_regress), suite_regress,
              sorted(set(after) - set(before))))
det.append("  failing both before and after (pre-existing, named): %s"
           % sorted(t for t, r in before.items() if r != 0))
ok_a = ok_dist and not regress and not suite_regress and len(before) > 0 and len(after) > 0
record("(a) FLAG TESTS", ok_a, det)


# ============================================================ (b) the closure, derived twice
def _const_tail(node):
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
    src_path = WS / rel
    src = src_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    mod_dir = src_path.parent
    loads = {}
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Name) and isinstance(nd.ctx, ast.Load):
            loads[nd.id] = loads.get(nd.id, 0) + 1
    assigned = {}
    for nd in tree.body:
        if isinstance(nd, ast.Assign) and len(nd.targets) == 1 and isinstance(nd.targets[0], ast.Name):
            assigned[id(nd.value)] = nd.targets[0].id
    refs = []
    search_dirs = [mod_dir]
    for nd in ast.walk(tree):
        tail = _const_tail(nd)
        if tail:
            rel_tail = "/".join(tail)
            for base in (mod_dir, WS):
                cand = base / rel_tail
                if cand.exists():
                    r = cand.resolve().relative_to(WS.resolve()).as_posix()
                    if cand.is_dir():
                        search_dirs.append(cand)
                    else:
                        name = assigned.get(id(nd))
                        verdict = "USED" if (name is None or loads.get(name, 0) > 0) else "DEAD"
                        refs.append((r, nd.lineno, verdict))
                    break
        if (isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name)
                and nd.func.id == "_import_runner" and len(nd.args) == 2
                and all(isinstance(a, ast.Constant) for a in nd.args)):
            refs.append(("%s/%s.py" % (nd.args[0].value, nd.args[1].value), nd.lineno, "USED"))
    for nd in tree.body:
        names = []
        if isinstance(nd, ast.Import):
            names = [a.name.split(".")[0] for a in nd.names]
        elif isinstance(nd, ast.ImportFrom) and nd.module and nd.level == 0:
            names = [nd.module.split(".")[0]]
        for nm in names:
            for d in search_dirs:
                if (d / (nm + ".py")).is_file():
                    refs.append(((d / (nm + ".py")).resolve().relative_to(WS.resolve()).as_posix(),
                                 nd.lineno, "USED"))
                    break
    return refs


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

def derive_static(root):
    """The transitive static sweep from `root`: {repo file: [module:line, ...]} and the modules walked."""
    found, frontier, walked = {}, [root], set()
    while frontier:
        mod = frontier.pop(0)
        if mod in walked or not mod.endswith(".py"):
            continue
        walked.add(mod)
        for ref, lineno, verdict in static_sweep(mod):
            if verdict == "USED":
                found.setdefault(ref, []).append("%s:%d" % (mod.rsplit("/", 1)[-1], lineno))
                if ref.endswith(".py"):
                    frontier.append(ref)
    return found, walked


static, seen = derive_static(RUNNER)
with tempfile.TemporaryDirectory() as td:
    probe = pathlib.Path(td) / "probe.py"
    probe.write_text(DYNAMIC_PROBE, encoding="utf-8")
    drc, dout = run([sys.executable, str(probe), str(WS), RUNNER], timeout=300, cwd=td, env=env)
dm = re.search(r"^DYNAMIC-JSON (.*)$", dout, re.M)
dynamic = set(json.loads(dm.group(1))) if dm else set()
closure = sorted(dynamic | {RUNNER})
hit = sdc.find_bundle(BUNDLE)
b = hit[2]
by_path = {s["repo_path"]: (name, s) for name, s in b["members"].items()}
declared_in = [c for c in closure if c in by_path]
named_by_path = [c for c in closure if c in by_path and by_path[c][0] == c]
flagged = sorted(s["repo_path"] for s in b["members"].values() if sdc.is_distribution_spec(s))
det = ["STATIC sweep over %d module(s): %d USED repo file references; DYNAMIC probe rc=%d: %d opened"
       % (len(seen), len(static), drc, len(dynamic)),
       "static-only (named, not opened on the runner's paths): %s" % sorted(set(static) - dynamic - {RUNNER}),
       "CLOSURE N = %d; diff vs the first pass's 8: added %s, removed %s"
       % (len(closure), sorted(set(closure) - set(FIRST_PASS_CLOSURE)),
          sorted(set(FIRST_PASS_CLOSURE) - set(closure)))]
for c in closure:
    det.append("  %-8s %-9s %s" % ("DECLARED" if c in by_path else "MISSING",
                                   "by-path" if c in named_by_path else "FLAT-NAME", c))
det.append("declared members outside the closure: %s"
           % sorted(p for p in by_path if p not in closure))
det.append("DECLARED %d of %d, named by repo path %d of %d; DISTRIBUTION-flagged %d: %s"
           % (len(declared_in), len(closure), len(named_by_path), len(closure), len(flagged), flagged))
ok_b = (drc == 0 and len(closure) == len(declared_in) == len(named_by_path) and len(closure) > 1
        and flagged == FLAGGED_EXPECTED)
record("(b) DECLARED", ok_b, det)

# ============================================================ (c) two-leg consistency + the mutant
s3 = boto("s3")
det = []
real = ACT["real_commit"]
rc, touched = run(["git", "show", "--name-only", "--format=%an", real])
touched = [ln for ln in touched.splitlines() if ln.strip()]
det.append("REAL commit %s by %s touches %s" % (real[:10], touched[0] if touched else None, touched[1:]))
ok_moved = False
if touched[1:] == [REAL_MEMBER]:
    pre, post = git_bytes(real + "~1", REAL_MEMBER), git_bytes(real, REAL_MEMBER)
    ok_moved = pre is not None and post is not None and md5(pre) != md5(post)
    det.append("  pre-commit md5 %s  post-commit md5 %s  (differ: %s)"
               % (md5(pre) if pre else None, md5(post) if post else None, ok_moved))
v_now, lines_now, rows_now = cons.check(real, version_id=ACT["bundle_final"],
                                         loose_versions=ACT["loose_after_deploy"])
det.append("THE ACT'S RESULT (the loose versions L4 wrote + the final bundle version), graded against "
           "the real commit's tree:")
det += ["  " + ln for ln in lines_now]
v_dep, _, rows_dep = cons.check(real, version_id=ACT["bundle_after_deploy"],
                                loose_versions=ACT["loose_after_deploy"])
det.append("the deploy's OWN mint (L4, v %s) on the same grade: %s" % (ACT["bundle_after_deploy"], v_dep))
v_live, _, _ = cons.check(real)
det.append("INFO -- the LIVING state now (current versions of every leg) against the same tree: %s "
           "(a later commit or mint by anyone moves this; the verdict above does not)" % v_live)
committed_row = [r for r in rows_now if r["member"] == REAL_MEMBER]
both_advanced = (bool(committed_row) and committed_row[0]["loose_ok"] and committed_row[0]["bundle_ok"]
                 and ok_moved and committed_row[0]["repo_md5"] != ACT["loose_before"][1])
det.append("the committed member's BOTH legs carry the post-commit bytes: %s" % both_advanced)
mv = ACT["mutant_version"]
v_mut, lines_mut, rows_mut = ("NOT-EVALUATED", ["no mutant version recorded"], [])
if not mv.startswith("__"):
    v_mut, lines_mut, rows_mut = cons.check(real, version_id=mv, loose_versions=ACT["loose_after_deploy"])
det.append("MUTANT (the bundle version minted from the PRE-COMMIT tree through the guard's own "
           "--mint-bundle; plane: the production bundle key's version history), graded against the "
           "real commit's tree:")
det += ["  " + ln for ln in lines_mut]
diverged = [r["member"] for r in rows_mut if not (r["loose_ok"] and r["bundle_ok"])]
only_bundle_leg = [r["member"] for r in rows_mut if r["loose_ok"] and not r["bundle_ok"]]
det.append("mutant verdict %s; diverged members %s; of them loose-leg-still-OK/bundle-leg-stale %s"
           % (v_mut, diverged, only_bundle_leg))
t0, t1 = ACT["mutant_window"]
loose_versions_in_window = None
if not t0.startswith("__"):
    tgt = sdc.file_to_s3_target(REAL_MEMBER)
    vs = s3.list_object_versions(Bucket=tgt[0], Prefix=tgt[1]).get("Versions", [])
    vs = [v for v in vs if v["Key"] == tgt[1]]
    lo, hi = dt.datetime.fromisoformat(t0.replace("Z", "+00:00")), dt.datetime.fromisoformat(t1.replace("Z", "+00:00"))
    loose_versions_in_window = [v["VersionId"] for v in vs if lo <= v["LastModified"] <= hi]
    det.append("loose key s3://%s/%s: %d version(s) in history; written inside the mutant window "
               "[%s, %s]: %d -> the mutant advanced ONE leg"
               % (tgt[0], tgt[1], len(vs), t0, t1, len(loose_versions_in_window)))
ok_c = (v_now == "CONSISTENT" and v_dep == "CONSISTENT" and len(rows_now) == 3 and both_advanced
        and v_mut == "DIVERGED"
        and diverged == [REAL_MEMBER] and only_bundle_leg == [REAL_MEMBER]
        and loose_versions_in_window == [])
record("(c) CONSISTENCY", ok_c, det)

# ============================================================ (d) the re-mint
cur = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=ACT["bundle_final"])
cur_etag, cur_ver = cur["ETag"].strip('"'), cur.get("VersionId")
live = s3.head_object(Bucket=b["bucket"], Key=b["s3_key"])
body = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=cur_ver)["Body"].read()
meta = cur.get("Metadata", {})
srp = [p for p in meta.get("source-repo-paths", "").split(";") if p]
with tarfile.open(fileobj=io.BytesIO(body), mode="r:gz") as tf:
    served = {mm.name: tf.extractfile(mm).read() for mm in tf.getmembers()}
det = ["THE MINTED VERSION (bound by id) s3://%s/%s  ETag %s  VersionId %s  %d bytes  LastModified %s"
       % (b["bucket"], b["s3_key"], cur_etag, cur_ver, len(body), cur["LastModified"].isoformat()),
       "INFO -- currently served: VersionId %s (%s)" % (live.get("VersionId"),
                                                       "the minted version" if live.get("VersionId") == cur_ver
                                                       else "a LATER version; the grade stays on the minted one"),
       "md5(downloaded) == ETag: %s   sha256(downloaded) = %s" % (md5(body) == cur_etag, sha256(body)),
       "source-repo-paths names %d of %d closure members; members served %d"
       % (len([c for c in closure if c in srp]), len(closure), len(served))]
stamps_ok = 0
for name, spec in sorted(b["members"].items()):
    got = served.get(name)
    stamp = meta.get(spec["sha_metadata_key"], "")
    selfok = got is not None and sha256(got) == stamp
    blob = git_bytes(real, spec["repo_path"])
    blobeq = got is not None and blob is not None and sha256(got) == sha256(blob)
    stamps_ok += 1 if selfok else 0
    det.append("%-5s stamp==member  %-5s member==git blob  %s%s"
               % ("OK" if selfok else "DIFF", "EQUAL" if blobeq else "DIFF", name,
                  "" if blobeq else "  (CR bytes in member: %d; row IRPT_BCKEND-S63: the packer reads the worktree)"
                  % (got.count(b"\r") if got else -1)))
pre_members = None
try:
    raw = s3.get_object(Bucket=b["bucket"], Key=b["s3_key"], VersionId=PRE_CELL["version"])["Body"].read()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
        pre_members = len(tf.getnames())
except Exception as exc:
    det.append("pre-cell version unreadable: %s" % type(exc).__name__)
differs = cur_ver != PRE_CELL["version"] and cur_etag != PRE_CELL["etag"] and (pre_members or 0) < len(served)
det.append("NEGATIVE CONTROL vs the pre-cell object: ETag %s (%s members) -> %s (%d members): %s"
           % (PRE_CELL["etag"], pre_members, cur_etag, len(served), "DIFFERS" if differs else "SAME"))
ok_d = (md5(body) == cur_etag and all(c in srp for c in closure) and stamps_ok == len(b["members"])
        and differs)
record("(d) RE-MINT", ok_d, det)

# ============================================================ (e) the host, read-only
ec2, ssm = boto("ec2"), boto("ssm")
state = ec2.describe_instances(InstanceIds=[INSTANCE])["Reservations"][0]["Instances"][0]["State"]["Name"]
info = ssm.describe_instance_information(
    Filters=[{"Key": "InstanceIds", "Values": [INSTANCE]}])["InstanceInformationList"]
ping = info[0]["PingStatus"] if info else "(absent)"
stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
base = "/tmp/irpt-rtc2b-%s" % stamp
CHECK_PY = r'''
import importlib.util, socket, sys
net = []
def hook(ev, args):
    if ev in ("socket.connect", "socket.getaddrinfo", "http.client.connect"):
        net.append(ev)
sys.addaudithook(hook)
root = sys.argv[1]
p = root + "/data/assets/scripts/gold/investor_reporting/directory_runner.py"
try:
    spec = importlib.util.spec_from_file_location("directory_runner", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
except BaseException as e:
    print("[rtc2] MODULE-IMPORT-FAIL %s: %s" % (type(e).__name__, e)); sys.exit(0)
print("[rtc2] MODULE-IMPORT-OK SOURCE_SETS=%r" % (sorted(m.SOURCE_SETS),))
for firm in sorted(m.SOURCE_SETS):
    try:
        src = m.SOURCE_SETS[firm]()
        print("[rtc2] IMPORT-OK %s %s" % (firm, getattr(src.rc, "__file__", "?")))
    except BaseException as e:
        print("[rtc2] IMPORT-FAIL %s %s: %s" % (firm, type(e).__name__, e))
print("[rtc2] NET-EVENTS %d" % len(net))
n0 = len(net)
try:
    socket.getaddrinfo("localhost", None)
except OSError:
    pass
print("[rtc2] NET-POSITIVE-CONTROL %s" % (len(net) > n0))
'''
host_cmds = [
    "set -u",
    "B=%s" % base,
    "rm -rf $B && mkdir -p $B/W",
    "echo \"[rtc2] caller $(aws sts get-caller-identity --query Arn --output text)\"",
    # THE HOST ROLE MAY GetObject THE KEY BUT NOT GetObjectVersion (measured: a --version-id fetch is
    # AccessDenied for mdpf-daily-runner-ec2-role), so the host fetches the key the way the dispatch
    # does, unversioned, and the object is bound to the MINTED version by CONTENT: its sha256 must equal
    # the minted version's, or the arm refuses to call what it graded the minted object.
    "aws s3 cp s3://%s/%s $B/bundle.tar.gz --only-show-errors "
    "|| { echo '[rtc2] FETCH-FAIL'; exit 90; }" % (b["bucket"], b["s3_key"]),
    "echo \"[rtc2] bundle sha256 $(sha256sum $B/bundle.tar.gz | cut -d' ' -f1)\"",
    "tar -tzf $B/bundle.tar.gz | sed 's/^/[rtc2] member /'",
    "tar -xzf $B/bundle.tar.gz -C $B/W && echo '[rtc2] EXTRACT-OK at one root' || echo '[rtc2] EXTRACT-FAIL'",
] + ["[ -f $B/W/%s ] && echo '[rtc2] placed %s' || echo '[rtc2] ABSENT %s'" % (c, c, c) for c in closure] + [
    "cat > $B/check.py <<'PYEOF'", CHECK_PY.strip("\n"), "PYEOF",
    "cd /tmp && python3 $B/check.py $B/W 2>&1",
    "echo '[rtc2] END'",
]
det = ["host %s state=%s ssm=%s (this battery never starts or stops it)" % (INSTANCE, state, ping)]
host_out, cmd_id = "", None
if state == "running" and ping == "Online":
    r = ssm.send_command(InstanceIds=[INSTANCE], DocumentName="AWS-RunShellScript",
                         Comment="IRPT IB-rtc-2 read-only repo-shaped closure check (/tmp only)",
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
    det.append("SSM command %s status=%s rc=%s" % (cmd_id, inv.get("Status"), inv.get("ResponseCode")))
    if inv.get("StandardErrorContent"):
        det.append("stderr (first 300): " + inv["StandardErrorContent"][:300].replace("\n", " | "))
else:
    det.append("NOT-EVALUATED: the host is not running+Online.")
g = lambda pat: re.findall(pat, host_out, re.M)   # noqa: E731
host_sha = g(r"^\[rtc2\] bundle sha256 ([0-9a-f]{64})$")
members = g(r"^\[rtc2\] member (.+)$")
placed = g(r"^\[rtc2\] placed (.+)$")
oks = g(r"^\[rtc2\] IMPORT-OK (\S+) ")
fails = g(r"^\[rtc2\] (?:MODULE-)?IMPORT-FAIL (.*)$")
net_n = g(r"^\[rtc2\] NET-EVENTS (\d+)$")
net_pc = g(r"^\[rtc2\] NET-POSITIVE-CONTROL (\S+)$")
det += ["caller: %s" % (g(r"^\[rtc2\] caller (.+)$") or ["(none)"])[0],
        "host sha256(bundle) %s == the MINTED version's sha256 %s: %s -- identity by content (the host "
        "role holds no s3:GetObjectVersion, so it fetches the key unversioned, as the dispatch does)"
        % (host_sha[0] if host_sha else None, sha256(body), bool(host_sha) and host_sha[0] == sha256(body)),
        "tar -tzf on the host: %d member(s); closure members listed %d of %d"
        % (len(members), len([c for c in closure if c in members]), len(closure)),
        "extracted at ONE /tmp root, each at its repo path: %d of %d closure files placed"
        % (len(placed), len(closure)),
        "IMPORT-OK %d of 3 %s" % (len(oks), oks)] + ["  IMPORT-FAIL " + f for f in fails] + [
        "network events during import + SourceSet x3: %s; positive control fired: %s"
        % (net_n[0] if net_n else None, net_pc[0] if net_pc else None)]
host_up = cmd_id is not None
ok_e = (host_up and bool(host_sha) and host_sha[0] == sha256(body)
        and all(c in members for c in closure) and len(placed) == len(closure)
        and len(oks) == 3 and net_n == ["0"] and net_pc == ["True"])
record("(e) HOST", ok_e if host_up else None, det)

# ============================================================ R-40 identities
print("R-40 identities (content hashes at this run):")
print("  served bundle: ETag %s  sha256 %s  VersionId %s" % (cur_etag, sha256(body), cur_ver))
print("  mutant bundle version: %s" % mv)
if cmd_id:
    print("  host command %s  host sha256 %s" % (cmd_id, host_sha[0] if host_sha else None))
for r in rows_now:
    print("  %s  loose ETag %s  bundle-member sha256 %s" % (r["member"], r["loose_etag"],
                                                             r["bundle_member_sha256"]))
for c in closure:
    _, bl = run(["git", "rev-parse", "HEAD:" + c])
    print("  %s  git-blob %s" % (c, bl.strip()))
print()

passed = sum(1 for _, ok in results if ok)
print("R32-AC1: %d of %d graded arms PASS" % (passed, len(results)))
if passed == len(results):
    print("IBR32-CLOSURE-MINTED-AND-IMPORTS-ON-HOST")
    sys.exit(0)
print("BLOCKED: not every graded arm passed; the expect token is withheld")
sys.exit(1)
