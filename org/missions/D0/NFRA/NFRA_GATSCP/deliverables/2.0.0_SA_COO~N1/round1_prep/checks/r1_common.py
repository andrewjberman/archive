"""NFRA_GATSCP round 1 check helpers (issuer 2.0.0_SA_COO~N1).

Every check plants its defect in a PRIVATE COPY of this checkout's git index (GIT_INDEX_FILE), never in the
working tree and never in a ref: the shared tree and every branch are left exactly as found. A planted blob is
written to the object store as an unreferenced object, which gc removes.

ASCII only. Python 3.9.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))


def _root() -> str:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ERROR: not in a git checkout")
    return r.stdout.strip()


ROOT = _root()

# The bystander project (owns the planted defect) and the act's project.
BYSTANDER = "LGIC_BLANKFIX"
BYSTANDER_DOC = "org/missions/D14/LGIC/LGIC_BLANKFIX/surprise-channel/investigations/INVESTIGATION_v1.md"
BYSTANDER_ROW = "org/missions/D14/LGIC/LGIC_BLANKFIX/project.json"
ACT_DOC = "org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md"
ACT_ROW = "org/missions/D0/NFRA/NFRA_GATSCP/project.json"
BASELINE = "org/surprise_channel/.corpus-baseline.json"


def git(args, env=None, data=None):
    return subprocess.run(["git"] + list(args), cwd=ROOT, env=env, input=data, capture_output=True,
                          encoding="utf-8", errors="replace")


def temp_index():
    """Return (tmpdir, env) where env carries GIT_INDEX_FILE = a copy of this checkout's index."""
    src = git(["rev-parse", "--path-format=absolute", "--git-path", "index"]).stdout.strip()
    d = tempfile.mkdtemp(prefix="gatscp-r1-")
    dst = os.path.join(d, "index")
    shutil.copy2(src, dst)
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = dst
    return d, env


def index_text(rel, env=None) -> str:
    """The index blob's exact bytes, decoded utf-8 (no newline translation)."""
    r = subprocess.run(["git", "show", ":" + rel], cwd=ROOT, env=env, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ERROR: %s is not in the index: %s" % (rel, r.stderr.decode("utf-8", "replace").strip()))
    return r.stdout.decode("utf-8")


def plant(env, rel, new_text):
    """Stage new_text as rel in the private index only (bytes written exactly)."""
    mode = git(["ls-files", "-s", "--", rel], env=env).stdout.split(" ")[0] or "100644"
    h = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=ROOT, input=new_text.encode("utf-8"),
                       capture_output=True)
    oid = h.stdout.decode("ascii").strip()
    r = git(["update-index", "--add", "--cacheinfo", "%s,%s,%s" % (mode, oid, rel)], env=env)
    if r.returncode != 0:
        raise SystemExit("ERROR: update-index failed for %s: %s" % (rel, r.stderr.strip()))
    return oid


def plant_channel_failure(env):
    """A NEW schema failure in the bystander's channel: the first surfaced_at made non-UTC."""
    text = index_text(BYSTANDER_DOC)
    new, n = re.subn(r'("surfaced_at"\s*:\s*")[^"]*(")', r"\1not-a-utc-time\2", text, count=1)
    if n != 1:
        raise SystemExit("ERROR: no surfaced_at in %s" % BYSTANDER_DOC)
    plant(env, BYSTANDER_DOC, new)


def plant_row_drift(env):
    """The bystander's tree row moved without its generated index: dep_stage changed in the row only."""
    text = index_text(BYSTANDER_ROW)
    m = re.search(r'"dep_stage"\s*:\s*"([^"]*)"', text)
    if not m:
        raise SystemExit("ERROR: no dep_stage in %s" % BYSTANDER_ROW)
    target = "DECOMP" if m.group(1) != "DECOMP" else "EXECUTING"
    plant(env, BYSTANDER_ROW, text[:m.start(1)] + target + text[m.end(1):])


def git_bash() -> str:
    sys.path.insert(0, os.path.join(ROOT, ".tools"))
    import git_bash_resolver  # noqa: E402
    b = git_bash_resolver.git_bash()
    if not b:
        raise SystemExit("ERROR: no Git Bash")
    return b


def run(argv, env, timeout=100):
    try:
        r = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, encoding="utf-8", errors="replace",
                           timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT after %ss" % timeout


def standing(out, code=BYSTANDER) -> bool:
    return re.search(r"(?m)^\s*STANDING\s+%s\b" % re.escape(code), out) is not None


def finish(tag, arms):
    """arms: list of (name, ok, detail). Prints one line per arm, then ONE last line."""
    for name, ok, detail in arms:
        print("  %s %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    ok = all(a[1] for a in arms)
    print("%s ok=%s arms=%d failed=%d" % (tag, ok, len(arms), sum(1 for a in arms if not a[1])))
    return 0 if ok else 1


def tail(out, n=6) -> str:
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return " | ".join(lines[-n:])[:600]
