"""CA-l-2 issuer check: the assistant's Lambda package carries ONLY the registry files the assistant reads.

Run from the checkout under test:   python <this file>          (the checkout is `git rev-parse --show-toplevel` of the CURRENT
working directory, never this file's location; a plain directory that is not a git repo is used as it is -- the cwd fallback, so a
scratch mirror can be graded)
Prints:  M2-BUILD ok=<True|False> arms=<k> of <n>      and one line  FAIL <arm>: <reason>  per failed arm  (plus NOTE lines).

It runs `bash infra/aws/lambda/teams-chat-assist/build.sh` of THAT checkout with OPAL_BUILD_REPO unset and OPAL_BUILD_DIST a fresh
temp folder outside the checkout, so it grades what a worker built, and reads the ZIP that build wrote (what ships).

DESIGN under test (the worker's contract): infra/aws/lambda/teams-chat-assist/registry_files.txt lists, one name per line ('#'
comments and blank lines ignored), the registry files the assistant reads; build.sh copies exactly those from infra/logic/registry/
and refuses a listed file that is absent. The manifest is a build input and is not packaged.

Arms (n = 7):
  manifest_list     the zip's registry files == the manifest's names, and are STRICTLY fewer than the checkout's full registry
  trace_equal       the zip's registry files == the files OPENED when the 17 probes and every packaged module import run against a
                    FULL-registry copy of the package (open()/io.open/os.open hooked; a listing of the registry directory is itself
                    a failure) UNION the registry files the packaged code names statically (opal_naming.REGISTRY_FILES and a
                    path built from "registry" + "<x>.json" in any other packaged module)
  probes_same       the 17 probes (check_l4_equiv.py PROBE: S3 addresses and the mail parties) print identical output from the
                    narrowed package and from the full-registry package
  no_unreferenced   no registry file in the zip is neither opened by the trace nor named statically
  reproducible      two builds give the same zip sha256
  foreign_absent    catalog_fork_keys.json is not in the zip (and the trace did not open it)
  other_bytes       every non-registry packaged file equals its source byte for byte (text read as LF), and the set is exactly
                    the expected one (the manifest is not packaged)
Hazard (stated, not graded): a registry file read lazily on a code path none of the probes or module imports reaches is invisible to
the trace; the static scan and opal_naming.REGISTRY_FILES narrow that gap but cannot close it.
"""
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

AGENT_REL = "infra/aws/lambda/teams-chat-assist"
MANIFEST_REL = AGENT_REL + "/registry_files.txt"
REG_REL = "infra/logic/registry"
FOREIGN = "catalog_fork_keys.json"
TEXT = (".py", ".json", ".md", ".txt")
ARMS = ("manifest_list", "trace_equal", "probes_same", "no_unreferenced", "reproducible", "foreign_absent", "other_bytes")

# The probe battery of check_l4_equiv.py (17 keys: BUCKET, firms, and state/silver/bronze for five chats), then the module imports.
TRACE = r'''
import builtins, importlib, io, json, os, sys
pkg = os.path.realpath(sys.argv[1])
sys.path.insert(0, pkg)
reg = os.path.normcase(os.path.join(pkg, "infra", "logic", "registry"))
opened, listed = set(), set()
_real_listdir, _real_scandir, _real_open, _real_osopen = os.listdir, os.scandir, builtins.open, os.open


def _split(p):
    try:
        if isinstance(p, int):
            return "", ""
        rp = os.path.realpath(os.fspath(p))
    except Exception:
        return "", ""
    return os.path.normcase(os.path.dirname(rp)), os.path.basename(rp)


def hopen(file, *a, **k):
    d, n = _split(file)
    if d == reg:
        opened.add(n)
    return _real_open(file, *a, **k)


def hosopen(path, *a, **k):
    d, n = _split(path)
    if d == reg:
        opened.add(n)
    return _real_osopen(path, *a, **k)


def hlistdir(path="."):
    d, n = _split(path)
    if os.path.normcase(os.path.join(d, n)) == reg:
        listed.add("listdir")
    return _real_listdir(path)


def hscandir(path="."):
    d, n = _split(path)
    if os.path.normcase(os.path.join(d, n)) == reg:
        listed.add("scandir")
    return _real_scandir(path)


builtins.open = hopen
io.open = hopen
os.open = hosopen
os.listdir = hlistdir
os.scandir = hscandir
out = {}
try:
    from data.transcripts.scripts.teams_chat import assist as a, mail_requests as mr
    out["BUCKET"] = a.BUCKET
    try:
        out["firms"] = json.dumps({k: sorted(v) if isinstance(v, (list, set, tuple)) else v for k, v in mr.firm_domains().items()}, sort_keys=True, default=str)
    except Exception as exc:
        out["firms"] = "ERR %s" % type(exc).__name__
    for i, cid in enumerate(["19:abc@unq.gbl.spaces", "19:meeting_XYZ@thread.v2", "eod:2026-10-13", "job:J290", "mail:owner"]):
        out["state_%d" % i] = a.state_key("x_%d.json" % i)
        out["silver_%d" % i] = a.silver_key(cid, "context.md")
        out["bronze_%d" % i] = a.bronze_key(cid, {"created": "2026-10-13T20:13:51Z", "id": "m%d" % i})
except Exception as exc:
    out = {"ERROR": "%s: %s" % (type(exc).__name__, str(exc)[:160])}
imp = {}
tc = os.path.join(pkg, "data", "transcripts", "scripts", "teams_chat")
names = ["handlers", "ldo"] + ["data.transcripts.scripts.teams_chat." + n[:-3] for n in sorted(_real_listdir(tc)) if n.endswith(".py") and n != "__init__.py"]
for name in names:
    try:
        importlib.import_module(name)
    except BaseException as exc:
        imp[name.rsplit(".", 1)[-1]] = type(exc).__name__
print(json.dumps({"probe": out, "opened": sorted(opened), "listed": sorted(listed), "imp": imp}, sort_keys=True))
sys.stdout.flush()
'''


def root():
    """The checkout under test: the git toplevel of the CURRENT directory; the current directory itself when it is not a git repo
    (or the toplevel holds no build.sh and the current directory does) -- never this file's location."""
    cwd = os.getcwd()
    top = ""
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, encoding="utf-8", cwd=cwd)
        top = r.stdout.strip() if r.returncode == 0 else ""
    except OSError:
        top = ""
    has = lambda d: os.path.isfile(os.path.join(d, *AGENT_REL.split("/"), "build.sh"))  # noqa: E731
    if top and has(top):
        return top
    return cwd if has(cwd) or not top else top


def find_bash(base):
    """Git Bash, never the System32 WSL stub (a bare 'bash' from python on this host)."""
    if os.name != "nt":
        return "bash"
    for c in (r"C:\Program Files\Git\usr\bin\bash.exe", r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files (x86)\Git\usr\bin\bash.exe"):
        if os.path.isfile(c):
            return c
    git = shutil.which("git")
    if git:
        p = os.path.realpath(git)
        while True:
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
            for rel in ("usr/bin/bash.exe", "bin/bash.exe"):
                b = os.path.join(p, *rel.split("/"))
                if os.path.isfile(b):
                    return b
    return None


def build(base, dist, bash):
    """Run the checkout's own build.sh with OPAL_BUILD_REPO unset and OPAL_BUILD_DIST=dist; return (zip path or None, message)."""
    env = dict(os.environ)
    env.pop("OPAL_BUILD_REPO", None)
    env["OPAL_BUILD_DIST"] = dist.replace(os.sep, "/")
    script = os.path.join(base, *AGENT_REL.split("/"), "build.sh").replace(os.sep, "/")
    r = subprocess.run([bash, script], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    z = os.path.join(dist, "teams-chat-assist.zip")
    if r.returncode != 0 or not os.path.isfile(z):
        return None, "build.sh rc=%d: %s" % (r.returncode, (r.stderr or r.stdout).strip()[-240:])
    return z, ""


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def lf(data, name):
    return data.replace(b"\r\n", b"\n") if name.endswith(TEXT) else data


def read_manifest(base):
    p = os.path.join(base, *MANIFEST_REL.split("/"))
    if not os.path.isfile(p):
        return None
    with open(p, "rb") as fh:
        lines = fh.read().decode("utf-8", "replace").replace("\r", "").split("\n")
    return [x.strip() for x in lines if x.strip() and not x.strip().startswith("#")]


def run_trace(pkg_dir):
    r = subprocess.run([sys.executable, "-c", TRACE, pkg_dir], capture_output=True, text=True, encoding="utf-8", errors="replace",
                       cwd=pkg_dir, timeout=180, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    lines = [x for x in r.stdout.strip().splitlines() if x.startswith("{")]
    if r.returncode != 0 or not lines:
        return {"probe": {"ERROR": (r.stderr or "no output")[-200:]}, "opened": [], "listed": [], "imp": {}}
    return json.loads(lines[-1])


def static_refs(pkg_dir):
    """Registry file names the packaged code names in code: opal_naming.REGISTRY_FILES, and in every other packaged .py a path built
    from "registry" + "<x>.json" or a literal 'infra/logic/registry/<x>.json'."""
    names = set()
    for base, dirs, files in os.walk(pkg_dir):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(base, fn)
            try:
                with open(p, "rb") as fh:
                    tree = ast.parse(fh.read().decode("utf-8"))
            except (SyntaxError, UnicodeDecodeError, OSError):
                continue
            is_naming = os.path.basename(p) == "opal_naming.py"
            for node in ast.walk(tree):
                if is_naming and isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "REGISTRY_FILES" for t in node.targets):
                    names.update(c.value for c in ast.walk(node.value) if isinstance(c, ast.Constant) and isinstance(c.value, str))
                if is_naming:
                    continue
                if isinstance(node, ast.Call):
                    args = [a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                    if node.args and isinstance(node.args[-1], ast.Constant) and "registry" in args and args[-1].endswith(".json"):
                        names.add(args[-1])
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.startswith(REG_REL + "/") and node.value.endswith(".json"):
                    names.add(node.value.rsplit("/", 1)[1])
    return names


def source_expected(base):
    """{zip name: source path} for every NON-registry file build.sh packages (the layout mirrors the repo)."""
    exp = {"handlers.py": os.path.join(base, *AGENT_REL.split("/"), "handlers.py"),
           "ldo.py": os.path.join(base, "infra", "aws", "terraform", "modules", "ldo", "runtime", "ldo.py"),
           "daily_reports/eod/post_format.py": os.path.join(base, "daily_reports", "eod", "post_format.py"),
           "daily_reports/eod/VOICE.md": os.path.join(base, "daily_reports", "eod", "VOICE.md"),
           "lib/opal_naming.py": os.path.join(base, "lib", "opal_naming.py"),
           "org/standards/NAMING_SCHEMA.json": os.path.join(base, "org", "standards", "NAMING_SCHEMA.json")}
    tc = os.path.join(base, "data", "transcripts", "scripts", "teams_chat")
    for b, dirs, files in os.walk(tc):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for fn in files:
            if not fn.endswith(".pyc"):
                p = os.path.join(b, fn)
                exp["data/transcripts/scripts/teams_chat/" + os.path.relpath(p, tc).replace(os.sep, "/")] = p
    return exp


def grade(base, tmp):
    res = dict.fromkeys(ARMS)   # arm -> None (ok) or a reason
    notes = []
    bash = find_bash(base)
    if not bash:
        return {a: "no Git Bash found" for a in ARMS}, notes
    z1, why = build(base, os.path.join(tmp, "dist1"), bash)
    if not z1:
        return {a: "no package: " + why for a in ARMS}, notes
    with zipfile.ZipFile(z1) as zf:
        names = zf.namelist()
        zf.extractall(os.path.join(tmp, "narrow"))
        zdata = {n: zf.read(n) for n in names}
    prefix = REG_REL + "/"
    pkg_reg = {n[len(prefix):] for n in names if n.startswith(prefix)}
    src_reg_dir = os.path.join(base, *REG_REL.split("/"))
    full_reg = {n for n in os.listdir(src_reg_dir) if n.endswith(".json")}

    # arm 1: the manifest
    man = read_manifest(base)
    if man is None:
        res["manifest_list"] = "%s is absent" % MANIFEST_REL
    elif len(set(man)) != len(man):
        res["manifest_list"] = "the manifest repeats a name"
    elif set(man) != pkg_reg:
        res["manifest_list"] = "zip registry files != manifest: only in zip %s, only in manifest %s" % (sorted(pkg_reg - set(man)), sorted(set(man) - pkg_reg))
    elif not pkg_reg < full_reg:
        res["manifest_list"] = "the package holds %d of the checkout's %d registry files: not strictly fewer" % (len(pkg_reg), len(full_reg))

    # the FULL-registry copy of the package, and the traces
    full_dir, narrow_dir = os.path.join(tmp, "full"), os.path.join(tmp, "narrow")
    shutil.copytree(narrow_dir, full_dir)
    for n in sorted(full_reg - pkg_reg):
        with open(os.path.join(src_reg_dir, n), "rb") as fh:
            data = fh.read().replace(b"\r\n", b"\n")
        with open(os.path.join(full_dir, *REG_REL.split("/"), n), "wb") as fh:
            fh.write(data)
    tf, tn = run_trace(full_dir), run_trace(narrow_dir)
    opened, static = set(tf["opened"]), static_refs(full_dir)
    notes.append("NOTE trace opened=%s static=%s listed=%s import_errors=%s" % (sorted(opened), sorted(static & full_reg), tf["listed"], tf["imp"]))

    # arm 2: package == opened U (statically named and present in the checkout's registry)
    required = opened | (static & full_reg)
    if tf["listed"]:
        res["trace_equal"] = "packaged code lists the registry directory (%s): a directory read is not a named read" % tf["listed"]
    elif "ERROR" in tf["probe"]:
        res["trace_equal"] = "the full-registry trace failed: %s" % tf["probe"]["ERROR"]
    elif pkg_reg != required:
        res["trace_equal"] = "zip registry files != files the assistant opens: in zip not read %s, read but not in zip %s" % (
            sorted(pkg_reg - required), sorted(required - pkg_reg))

    # arm 3: the 17 probes, narrowed vs full
    pn, pf = tn["probe"], tf["probe"]
    if "ERROR" in pn or "ERROR" in pf:
        res["probes_same"] = "probe failed: narrowed=%s full=%s" % (str(pn)[:100], str(pf)[:100])
    elif len(pn) != 17 or pn != pf:
        res["probes_same"] = "probes differ or are not 17 (narrowed %d, full %d): %s" % (len(pn), len(pf), sorted(k for k in set(pn) | set(pf) if pn.get(k) != pf.get(k))[:5])

    # arm 4: nothing in the zip that no code references
    unref = sorted(pkg_reg - opened - static)
    if unref:
        res["no_unreferenced"] = "registry file(s) in the zip that nothing opens or names: %s" % unref

    # arm 5: reproducible
    z2, why2 = build(base, os.path.join(tmp, "dist2"), bash)
    if not z2:
        res["reproducible"] = "second build failed: " + why2
    elif sha(z1) != sha(z2):
        res["reproducible"] = "two builds differ: %s vs %s" % (sha(z1)[:12], sha(z2)[:12])

    # arm 6: the large foreign file
    if FOREIGN in pkg_reg:
        res["foreign_absent"] = "%s is in the package" % FOREIGN
    elif FOREIGN in opened:
        res["foreign_absent"] = "%s is absent but the trace opened it" % FOREIGN

    # arm 7: every other file equals its source
    exp = source_expected(base)
    other = {n for n in names if not n.startswith(prefix)}
    bad = []
    if other != set(exp):
        bad.append("file set differs: extra %s missing %s" % (sorted(other - set(exp))[:4], sorted(set(exp) - other)[:4]))
    for n in sorted(other & set(exp)):
        with open(exp[n], "rb") as fh:
            if lf(fh.read(), n) != zdata[n]:
                bad.append("bytes differ: " + n)
                break
    if bad:
        res["other_bytes"] = "; ".join(bad)
    return res, notes


def main():
    base = root()
    tmp = tempfile.mkdtemp(prefix="m2_build_")
    try:
        res, notes = grade(base, tmp)
    except Exception as exc:  # noqa: BLE001 -- any failure reads as ok=False with its reason
        res, notes = {a: "check error %s: %s" % (type(exc).__name__, str(exc)[:160]) for a in ARMS}, []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for n in notes:
        print(n)
    for a in ARMS:
        if res.get(a):
            print("FAIL %s: %s" % (a, res[a]))
    k = sum(1 for a in ARMS if not res.get(a))
    print("M2-BUILD ok=%s arms=%d of %d" % (k == len(ARMS), k, len(ARMS)))


if __name__ == "__main__":
    sys.exit(main() or 0)
