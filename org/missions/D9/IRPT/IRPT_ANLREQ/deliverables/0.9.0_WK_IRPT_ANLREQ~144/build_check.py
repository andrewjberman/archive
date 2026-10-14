"""TO-AR-y-338 criterion AR338-y-AC1 (amended by AMENDMENT 1): the release-31 build check. Offline: no AWS, no network,
nothing uploaded, installed or run on a host. The only subprocess is the AR-y-331 route test file, run from a copy of the
EXTRACTED tarball (its bytes are read from the tarball, never from the build folders), one pytest process, under timeout 280.

Prints one line `BUILD-OK ...` only when every condition holds; otherwise `BUILD-BAD <why>` and exit 1.
Conditions:
 (1) the sha256 of the release-31 tarball equals the record's;
 (2) build_a and build_b agree member by member (name and sha256);
 (3) the tarball and the release-29 base, read member by member, reproduce the record's delta lists exactly;
 (4) the differing set EQUALS the expected names (the order's step-3 list, plus reports/build_resident_package.py and
     ycharts/generate/acceptance.py per AMENDMENT 1, plus any member the record explains by a surprise row whose id is in
     the channel). "differing 0" in the success line counts differing members outside that set; "unexplained 0" counts
     differing members with no reason;
 (5) the extracted bindings carry the keys analysis_ready_queue_url, commentary_ready_queue_url, packager (exactly api_base
     and secret_name) and opal_map; OPAL_PRODUCER_PRINCIPALS in resident_worker.py is the two-entry tuple;
 (6) no JWT-shaped string and no "token" JSON member in any DIFFERING member or in any host script (untouched members are
     compared by equality, not scanned);
 (7) the AR-y-331 route tests (ops/tests/test_commentary_pdf_route.py) pass 6 of 6 against the extracted package tree.
ASCII only.
"""
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile

DL = os.path.dirname(os.path.abspath(__file__))
STAGE = "C:/dev/irpt-release-r31"
TAR = STAGE + "/irpt-resident-0485393f3a-r31.tar.gz"
BUILD_A = STAGE + "/build_a"
BUILD_B = STAGE + "/build_b"
R29_TAR = "C:/dev/irpt-release-r29/irpt-resident-0485393f3a-r29.tar.gz"
R29_SHA = "2de2adce622f8bb9bbd5ebc071e862446b056303c0d9ffd7d41b050bd17f51a4"
PIN = "c4c2afe89639071f41242fc9f663cadaffa0ffd8"
WT = STAGE + "/wt-release-c4c2afe896"
ROUTE_ROOT = STAGE + "/route-check-p2"
CHANNEL = os.path.join(DL, "..", "..", "surprise-channel", "investigations", "INVESTIGATION_v1.md")
RECORD = os.path.join(DL, "r41", "RESIDENT_R31_BUILD.json")
SCRIPTS = ["pre_read_r31.sh", "install_r31.sh", "rollback_r31.sh", "resident_host_install_0485393f3a-r31.sh"]
STEP3 = {
    "SHA256SUMS", "reports/resident_bindings.json", "ycharts/generate/resident_worker.py",
    "ycharts/generate/composition_admission.py", "_scope/interactive_access.py", "intake/uploads.py",
    "ycharts/research/layout_overview.py", "ycharts/research/opal_producer.py", "ycharts/research/opal_packager.py",
    "ops/entry.py", "ops/owned_report.py", "ops/pdf_link.py", "reports/status_installed.py",
}
AMENDMENT1 = {"reports/build_resident_package.py", "ycharts/generate/acceptance.py"}
PRINCIPALS = ("andrew@opalinvest.com", "fwd1-staff-r41a@opal.invalid")
PKG_PATH = "infra/aws/lambda/investor-reporting"
TEST_DIRS = ["intake/tests", "ops/tests", "reports/tests", "ycharts/session/tests", "ycharts/generate/tests",
             "ycharts/research/tests", "_authz/tests", "_scope/tests"]
PYPATH_DIRS = ["", "_scope", "_ids", "_keys", "_authz", "_contracts", "intake", "ops", "reports", "ycharts/generate",
               "ycharts/session", "ycharts/extract", "lib", "intake/tests", "ops/tests", "reports/tests",
               "ycharts/session/tests", "ycharts/generate/tests", "ycharts/research/tests", "_authz/tests", "_scope/tests"]
JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")
TOKEN_MEMBER = re.compile(r'"token"\s*:')


def bad(why):
    print("BUILD-BAD " + why)
    sys.exit(1)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha_file(path):
    with open(path, "rb") as fh:
        return sha_bytes(fh.read())


def folder_members(root):
    out = {}
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            out[os.path.relpath(p, root).replace(os.sep, "/")] = sha_file(p)
    return out


def tar_members(path):
    """name -> bytes, the './' prefix removed; read in memory (the bytes an extraction would write)."""
    out = {}
    with tarfile.open(path, "r:gz") as tar:
        for m in tar.getmembers():
            if not m.isfile():
                bad("non-file member in %s: %s" % (path, m.name))
            name = m.name[2:] if m.name.startswith("./") else m.name
            out[name] = tar.extractfile(m).read()
    return out


def route_tests(members):
    """Copy the tarball's bytes to ROUTE_ROOT (repository depth), add the pin's test folders and docs contract, run one
    pytest process on the route test file under timeout 280. Returns the summary line."""
    if os.path.isdir(ROUTE_ROOT):
        shutil.rmtree(ROUTE_ROOT)
    pkg = os.path.join(ROUTE_ROOT, *PKG_PATH.split("/"))
    for name, data in members.items():
        dst = os.path.join(pkg, *name.split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(data)
    wt_pkg = os.path.join(WT, *PKG_PATH.split("/"))
    for d in TEST_DIRS:
        src = os.path.join(wt_pkg, *d.split("/"))
        dst = os.path.join(pkg, *d.split("/"))
        os.makedirs(dst, exist_ok=True)
        shutil.copytree(src, dst, dirs_exist_ok=True)
    docs_src = WT + "/docs/contracts/investor-reporting/v1"
    docs_dst = ROUTE_ROOT + "/docs/contracts/investor-reporting/v1"
    shutil.copytree(docs_src, docs_dst)
    pp = ";".join(os.path.normpath(os.path.join(pkg, *d.split("/"))) if d else pkg for d in PYPATH_DIRS)
    pp = ";".join(p for p in pp.split(";") if os.path.isdir(p))
    env = dict(os.environ, PYTHONPATH=pp, PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                               "ops/tests/test_commentary_pdf_route.py"],
                              cwd=pkg, env=env, capture_output=True, timeout=280)
    except subprocess.TimeoutExpired:
        bad("route test timeout 280s (ops/tests/test_commentary_pdf_route.py)")
    text = re.sub(r"\x1b\[[0-9;]*m", "", (proc.stdout + proc.stderr).decode("utf-8", "replace"))
    last = text.strip().splitlines()[-1] if text.strip() else ""
    m = re.search(r"(\d+) passed", last)
    passed = int(m.group(1)) if m else 0
    failed = re.search(r"(\d+) failed", last)
    return proc.returncode, passed, (int(failed.group(1)) if failed else 0), last


# (1) the tarball sha256 equals the record's
record = json.load(open(RECORD, encoding="utf-8"))
tar_sha = sha_file(TAR)
if tar_sha != record["artifact"]["sha256"]:
    bad("tarball sha256 %s is not the record's %s" % (tar_sha, record["artifact"]["sha256"]))

# the worktree used for the route test copies must be the pin, clean
head = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=120).stdout.strip()
if head != PIN:
    bad("release worktree HEAD %s is not the pin %s" % (head, PIN))

# (2) the two builds agree member by member
a = folder_members(BUILD_A)
b = folder_members(BUILD_B)
if set(a) != set(b):
    bad("build names differ: only_a=%s only_b=%s" % (sorted(set(a) - set(b))[:3], sorted(set(b) - set(a))[:3]))
differ_builds = [n for n in a if a[n] != b[n]]
if differ_builds:
    bad("builds differ on %s" % differ_builds[:3])
members_n = len(a)
identical = sum(1 for n in a if a[n] == b.get(n))

# (3) the tarball and the release-29 base, member by member, reproduce the record's delta lists exactly
r29_sha = sha_file(R29_TAR)
if r29_sha != R29_SHA:
    bad("release-29 base sha256 %s is not %s" % (r29_sha, R29_SHA))
t31 = tar_members(TAR)
t29 = tar_members(R29_TAR)
if len(t31) != 299 or len(t29) != 299:
    bad("member counts %d and %d, want 299 each" % (len(t31), len(t29)))
h31 = {n: sha_bytes(d) for n, d in t31.items()}
h29 = {n: sha_bytes(d) for n, d in t29.items()}
differing = sorted(n for n in h31 if n in h29 and h31[n] != h29[n])
only_rel = sorted(n for n in h31 if n not in h29)
only_live = sorted(n for n in h29 if n not in h31)
unchanged = sum(1 for n in h31 if n in h29 and h31[n] == h29[n])
rec = record["delta_vs_live"]
if differing != sorted(rec["differing"]) or only_rel != sorted(rec["only_in_release"]) or only_live != sorted(rec["only_in_live"]):
    bad("the delta lists do not reproduce the record's")
if unchanged != rec["counts"]["unchanged"]:
    bad("unchanged count %d, record %d" % (unchanged, rec["counts"]["unchanged"]))

# (4) the differing set equals the expected names plus the names a surprise row explains
explained = rec["explained_by_surprise_row"]
channel = open(CHANNEL, encoding="utf-8").read()
for name, row_id in explained.items():
    if '"id": "%s"' % row_id not in channel:
        bad("explained member %s cites %s, which is not in the channel" % (name, row_id))
expected = STEP3 | AMENDMENT1 | set(explained)
outside = sorted(n for n in differing if n not in expected)
unexplained = sorted(n for n in differing if n not in STEP3 | AMENDMENT1 and n not in explained)
missing = sorted(n for n in expected if n not in differing)
if outside or unexplained:
    bad("differing members outside the expected set: %s; unexplained: %s" % (outside, unexplained))
if missing:
    bad("expected members that do not differ from release 29: %s" % missing)
if only_rel or only_live:
    bad("members only in one side: only_in_release=%s only_in_live=%s" % (only_rel, only_live))

# (5) the extracted bindings carry the four keys; the producer list is the two-entry tuple
bindings = json.loads(t31["reports/resident_bindings.json"].decode("utf-8"))
for key in ("analysis_ready_queue_url", "commentary_ready_queue_url", "packager", "opal_map"):
    if key not in bindings:
        bad("bindings lack %s" % key)
if sorted(bindings["packager"]) != ["api_base", "secret_name"]:
    bad("packager keys are %s, want exactly api_base and secret_name" % sorted(bindings["packager"]))
worker = t31["ycharts/generate/resident_worker.py"].decode("utf-8")
match = re.search(r"^OPAL_PRODUCER_PRINCIPALS = (\(.*?\))\s*$", worker, re.M)
if not match:
    bad("OPAL_PRODUCER_PRINCIPALS line not found in resident_worker.py")
if tuple(ast.literal_eval(match.group(1))) != PRINCIPALS:
    bad("OPAL_PRODUCER_PRINCIPALS is %s" % match.group(1))

# (6) no JWT-shaped string and no "token" JSON member in any differing member or host script
scan = [(n, t31[n]) for n in differing] + [(s, open(os.path.join(DL, s), "rb").read()) for s in SCRIPTS]
jwt_hits, token_hits = [], []
for name, data in scan:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        bad("differing member or script is not UTF-8: %s" % name)
    if JWT.search(text):
        jwt_hits.append(name)
    if TOKEN_MEMBER.search(text):
        token_hits.append("%s (%d)" % (name, len(TOKEN_MEMBER.findall(text))))
if jwt_hits:
    bad("JWT-shaped string in %s" % jwt_hits)
if token_hits:
    bad('"token" JSON member in %s' % token_hits)

# (7) the AR-y-331 route tests pass 6 of 6 against the extracted package tree
rc, passed, failed, last = route_tests(t31)
if rc != 0 or passed != 6 or failed != 0:
    bad("route tests rc=%d passed=%d failed=%d: %s" % (rc, passed, failed, last[:200]))

print("BUILD-OK %d members, builds identical %d of %d, delta %d differing 0 unexplained 0 only_in_live %d "
      "(expected names %d, explained by surprise rows %d); route tests %d of 6 passed, rc %d"
      % (members_n, identical, members_n, len(differing), len(only_live), len(set(differing) & (STEP3 | AMENDMENT1)),
         len(explained), passed, rc))
