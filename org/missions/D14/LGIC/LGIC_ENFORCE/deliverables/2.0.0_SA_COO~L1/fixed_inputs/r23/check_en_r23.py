"""LGIC_ENFORCE round 23 -- the issuer's fixed checks, one subcommand per criterion (2.0.0_SA_COO~L1).

Run from the root of the worktree under test:  python <this file> <arm>
Each arm prints exactly one PASS-* or FAIL-* verdict line last, and exits 0 only on PASS.

Every arm builds a PRACTICE COPY (a sparse detached worktree of the committed HEAD of the worktree under test, carrying
.tools/, lib/, infra/, org/standards/, org/missions/D14/LGIC/ and the two enforce switches), stages a change in it, makes
the diff exactly as .tools/safe-commit.sh does (`git diff --cached --no-color --no-ext-diff -- <paths>`), and runs the
practice copy's own `.tools/naming-gate.py --diff F --post-from-index` with its enforce switches present.

  rename    EN-ac-1  (FWD-8 arm 1) a tracked file holding an OUT-OF-PATTERN name is renamed with its bytes unchanged:
                     the gate prints a NAMING line for the name that is not REFUSE, grades at least one literal, and
                     exits 0. DIFFERENCE CONTROL, same run: the same bytes staged as a COPY (source kept) are REFUSED.
  adopt     EN-ac-1  (FWD-8 arms 2 and 3) a declaration of a name the census LIVE plane holds, OUT-OF-PATTERN and with
                     the firm spelling `bd`: exit 0, no REFUSE, and the verdict text names the plane's vintage and the
                     node type matched. DIFFERENCE CONTROL, same run: a name the plane does not hold is REFUSED as today.
  closed    EN-ac-1  (FWD-8 arm 4) the same adoption with the live read made unreadable, and again with a read that
                     prints no vintage: each is REFUSED as today and the text says LIVE-READ-FAILED.
  selftest  EN-ac-1  `--self-test` prints a rename arm and an adopt arm, each `ok`, and ends NAMING-GATE-SELF-TEST: PASS.
"""
import contextlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
SPARSE = ["/lib/", "/infra/", "/.tools/", "/org/standards/", "/org/missions/D14/LGIC/",
          "/org/missions/*.yaml", "/org/mcp/naming-gate.enforce", "/org/mcp/naming-place.enforce"]
SRC_REL = "infra/aws/terraform/zz-r23-probe/zz_probe.tf.proposed"
DST_REL = "infra/aws/terraform/zz-r23-probe/zz_probe.tf"
COPY_REL = "infra/aws/terraform/zz-r23-probe/zz_probe_copy.tf"
ADOPT_REL = "infra/aws/terraform/zz-r23-probe/zz_adopt.tf"
RENAME_NAME = "bd-zz-r23-probe-role"
ABSENT_NAME = "bd-zz-r23-notrunning-policy"
RUNNING_TYPES = {"IAM_POLICY": "aws_iam_policy", "IAM_ROLE": "aws_iam_role"}
LIVE_TOKEN = "RUNNING-LIVE"
FAILED_TOKEN = "LIVE-READ-FAILED"


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def run(args, cwd=ROOT, timeout=900, env=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout, env=env)
    out = (p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace")
    return p.returncode, out.replace("\r\n", "\n")


@contextlib.contextmanager
def practice():
    tmp = tempfile.mkdtemp(prefix="r23-practice-")
    wt = os.path.join(tmp, "wt")
    try:
        rc, out = run(["git", "worktree", "add", "--no-checkout", "--detach", wt, "HEAD"])
        need(rc == 0, "could not add the practice copy: %s" % out[-300:])
        rc, out = run(["git", "sparse-checkout", "set", "--no-cone"] + SPARSE, cwd=wt)
        need(rc == 0, "sparse-checkout set failed: %s" % out[-300:])
        rc, out = run(["git", "checkout"], cwd=wt, timeout=1200)
        need(rc == 0, "practice checkout failed: %s" % out[-300:])
        need(os.path.isfile(os.path.join(wt, ".tools", "naming-gate.py")), "the practice copy lacks .tools/naming-gate.py")
        need(os.path.isfile(os.path.join(wt, "org", "mcp", "naming-gate.enforce")), "the practice copy lacks the enforce switch")
        yield wt
    finally:
        run(["git", "worktree", "remove", "--force", wt])
        shutil.rmtree(tmp, ignore_errors=True)


def git(wt, *args):
    # hooks off in the THROWAWAY practice copy only: the instrument under test is the naming gate, not the commit hooks
    hooks = os.path.join(os.path.dirname(wt), "nohooks")
    os.makedirs(hooks, exist_ok=True)
    rc, out = run(["git", "-c", "core.hooksPath=" + hooks, "-c", "user.name=r23-practice", "-c", "user.email=r23@practice.invalid",
                   "-c", "core.autocrlf=false"] + list(args), cwd=wt)
    need(rc == 0, "git %s failed in the practice copy: %s" % (" ".join(args[:3]), out[-300:]))
    return out


def write(wt, rel, text):
    path = os.path.join(wt, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def tf_role(name):
    return 'resource "aws_iam_role" "probe" {\n  name = "%s"\n}\n' % name


def tf_policy(res_type, name):
    return 'resource "%s" "probe" {\n  name = "%s"\n}\n' % (res_type, name)


def gate(wt, paths):
    """The save check on the staged change, as safe-commit.sh runs it: (rc, output, summary-count)."""
    diff = git(wt, "diff", "--cached", "--no-color", "--no-ext-diff", "--", *paths)
    need(diff.strip(), "the staged diff for %s is empty" % paths)
    fh = tempfile.NamedTemporaryFile("w", suffix=".diff", delete=False, encoding="utf-8", newline="\n")
    fh.write(diff)
    fh.close()
    try:
        env = dict(os.environ)
        env.pop("NAMING_PLACE_OVERRIDE", None)
        rc, out = run([sys.executable, ".tools/naming-gate.py", "--diff", fh.name, "--post-from-index"], cwd=wt, timeout=1500, env=env)
    finally:
        os.unlink(fh.name)
    return rc, out


def verdict_lines(out, name):
    return [ln for ln in out.split("\n") if ln.startswith("NAMING ") and name in ln]


def why_after(out, name):
    """The verdict line for `name` and the `  why:` line under it, joined."""
    lines = out.split("\n")
    got = []
    for i, ln in enumerate(lines):
        if ln.startswith("NAMING ") and name in ln:
            got.append(ln + " | " + (lines[i + 1] if i + 1 < len(lines) else ""))
    return got


def summary(out):
    m = re.search(r"^NAMING-GATE: (PASS|WARN|REFUSE) (\d+) graded", out, re.M)
    need(m is not None, "no NAMING-GATE summary line: %s" % out[-300:])
    return m.group(1), int(m.group(2))


def load_live():
    """(the live running name to adopt, its type, the plane's vintage) read through lib/opal_naming.py of THIS worktree."""
    sys.path.insert(0, os.path.join(ROOT, "lib"))
    import importlib.machinery
    import importlib.util
    loader = importlib.machinery.SourceFileLoader("opal_naming_r23", os.path.join(ROOT, "lib", "opal_naming.py"))
    spec = importlib.util.spec_from_loader("opal_naming_r23", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    nodes, vintage, _shown = mod.census_live(budget=600)
    held = set(n["name"] for n in nodes)
    need(ABSENT_NAME not in held, "the control name %r is running in the live plane: pick another" % ABSENT_NAME)
    picks = []
    for n in nodes:
        if n["type"] not in RUNNING_TYPES or "bd" not in re.split(r"[-_.]", n["name"]):
            continue
        try:
            res = mod.grade(n["name"], n["type"])
        except Exception:
            continue
        if res and res[0] == "OUT-OF-PATTERN":
            picks.append((n["name"], n["type"]))
    need(picks, "no running IAM_POLICY/IAM_ROLE name with the firm spelling `bd` reads OUT-OF-PATTERN in the live plane (%d nodes)" % len(nodes))
    picks.sort()
    return picks[0][0], picks[0][1], vintage


def arm_rename():
    with practice() as wt:
        write(wt, SRC_REL, tf_role(RENAME_NAME))
        git(wt, "add", "--", SRC_REL)
        git(wt, "commit", "-q", "-m", "r23 practice: the source file at HEAD")
        git(wt, "mv", SRC_REL, DST_REL)
        git(wt, "add", "-A")
        rc, out = gate(wt, [DST_REL])
        lines = verdict_lines(out, RENAME_NAME)
        summ, graded = summary(out)
        print("rename: rc=%d %s %d graded | %s" % (rc, summ, graded, lines[:1]))
        need(lines, "the gate printed no NAMING line for the renamed file's name %r: %s" % (RENAME_NAME, out[-300:]))
        need(not any(ln.startswith("NAMING REFUSE") for ln in lines), "the renamed file's name was REFUSED: %s" % lines)
        need(graded >= 1, "the gate graded 0 literals on the rename: a vacuous pass")
        need(rc == 0 and summ != "REFUSE", "the gate refused the rename (rc=%d, %s)" % (rc, summ))
        # the difference control: the SAME bytes as a COPY (the source stays) are a new name and are refused
        git(wt, "reset", "-q", "--hard", "HEAD")
        write(wt, COPY_REL, tf_role(RENAME_NAME))
        git(wt, "add", "--", COPY_REL)
        rc2, out2 = gate(wt, [COPY_REL])
        lines2 = verdict_lines(out2, RENAME_NAME)
        summ2, _g2 = summary(out2)
        print("copy:   rc=%d %s | %s" % (rc2, summ2, lines2[:1]))
        need(any(ln.startswith("NAMING REFUSE") for ln in lines2) and rc2 != 0,
             "the control (the same bytes as a copy) was not refused (rc=%d): the rename limb admits too much" % rc2)
    return "PASS-R23-RENAME"


def adoption_text(wt, name, typ, rel=ADOPT_REL):
    write(wt, rel, tf_policy(RUNNING_TYPES[typ], name))
    git(wt, "add", "--", rel)
    return gate(wt, [rel])


def arm_adopt():
    name, typ, vintage = load_live()
    asof = re.search(r"as of (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC)", vintage)
    need(asof is not None, "cannot read the vintage date out of %r" % vintage)
    print("live pick: %s (%s); vintage %s" % (name, typ, asof.group(1)))
    with practice() as wt:
        rc, out = adoption_text(wt, name, typ)
        lines = why_after(out, name)
        summ, graded = summary(out)
        print("adopt:  rc=%d %s %d graded | %s" % (rc, summ, graded, lines[:1]))
        need(lines, "the gate printed no NAMING line for the running name %r: %s" % (name, out[-300:]))
        need(not any(ln.startswith("NAMING REFUSE") for ln in lines), "the running name was REFUSED: %s" % lines)
        need(rc == 0 and summ != "REFUSE" and graded >= 1, "the gate did not admit the adoption (rc=%d, %s, %d graded)" % (rc, summ, graded))
        text = " ".join(lines)
        need(FAILED_TOKEN not in text, "the admitted adoption carries %s although the live read worked: %s" % (FAILED_TOKEN, text[:300]))
        need(LIVE_TOKEN in text and typ in text and asof.group(1) in text,
             "the verdict text lacks %s, the node type %s or the vintage date %s: %s" % (LIVE_TOKEN, typ, asof.group(1), text[:400]))
        # the difference control: a name the plane does not hold is refused exactly as today
        git(wt, "reset", "-q", "--hard", "HEAD")
        git(wt, "clean", "-fdq")
        rc2, out2 = adoption_text(wt, ABSENT_NAME, typ)
        lines2 = why_after(out2, ABSENT_NAME)
        print("absent: rc=%d | %s" % (rc2, lines2[:1]))
        need(any(ln.startswith("NAMING REFUSE") for ln in lines2) and rc2 != 0, "the name running nowhere was not refused (rc=%d)" % rc2)
        need("NEW and" in " ".join(lines2) and FAILED_TOKEN not in " ".join(lines2),
             "the refusal of the absent name does not read as today's NEW refusal: %s" % lines2[:1])
    return "PASS-R23-ADOPT"


STUBS = {
    "unreadable": "import sys\nsys.stderr.write('r23 stub: the live read cannot run\\n')\nsys.exit(3)\n",
    "undated": ("print('comp-find [aws name] .')\nprint('  WITHIN BUDGET: scanned 1 of 1 pull')\nprint('  DEFERRED: 0 of 1 pull(s) did not return')\n"
                "print('  VINTAGE: UNREAD')\nprint('  DENOMINATOR: 0 hit(s) across 0 aws node(s) scanned [corpus=aws]')\n"),
}


def arm_closed():
    name, typ, _vintage = load_live()
    seen = []
    for label, stub in sorted(STUBS.items()):
        with practice() as wt:
            write(wt, ".tools/comp-find", stub)
            rc, out = adoption_text(wt, name, typ)
            lines = why_after(out, name)
            print("%s: rc=%d | %s" % (label, rc, lines[:1]))
            need(lines, "[%s] the gate printed no NAMING line for %r: %s" % (label, name, out[-300:]))
            need(any(ln.startswith("NAMING REFUSE") for ln in lines) and rc != 0,
                 "[%s] a failed live read did not leave the name REFUSED (rc=%d): the gate fails OPEN" % (label, rc))
            need(FAILED_TOKEN in " ".join(lines), "[%s] the refusal does not say %s: %s" % (label, FAILED_TOKEN, lines[:1]))
            need(LIVE_TOKEN not in " ".join(lines), "[%s] the failed read printed %s" % (label, LIVE_TOKEN))
            seen.append(label)
    need(seen == sorted(STUBS), "an arm did not run: %s" % seen)
    return "PASS-R23-CLOSED"


def arm_selftest():
    rc, out = run([sys.executable, ".tools/naming-gate.py", "--self-test"], timeout=900)
    arms = [ln for ln in out.split("\n") if ln.startswith("SELF-TEST ")]
    ren = [ln for ln in arms if re.search(r"\brename\b", ln, re.I)]
    ado = [ln for ln in arms if re.search(r"\badopt", ln, re.I)]
    print("self-test: rc=%d arms=%d rename=%d adopt=%d" % (rc, len(arms), len(ren), len(ado)))
    need(ren and all(ln.rstrip().endswith(": ok") for ln in ren), "no rename arm, or one is not ok: %s" % ren)
    need(ado and all(ln.rstrip().endswith(": ok") for ln in ado), "no adopt arm, or one is not ok: %s" % ado)
    need(rc == 0 and "NAMING-GATE-SELF-TEST: PASS" in out, "the self-test did not end PASS (rc=%d)" % rc)
    return "PASS-R23-SELFTEST"


ARMS = {"rename": arm_rename, "adopt": arm_adopt, "closed": arm_closed, "selftest": arm_selftest}


def main(argv):
    if len(argv) != 2 or argv[1] not in ARMS:
        print("usage: check_en_r23.py {%s}" % "|".join(sorted(ARMS)))
        print("FAIL-R23-USAGE")
        return 2
    try:
        verdict = ARMS[argv[1]]()
    except Fail as exc:
        print("FAIL-R23-%s: %s" % (argv[1].upper(), exc))
        return 1
    except Exception as exc:  # an instrument error is a FAIL with its reason, never a silent pass
        print("FAIL-R23-%s: instrument error %s: %s" % (argv[1].upper(), type(exc).__name__, exc))
        return 1
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
