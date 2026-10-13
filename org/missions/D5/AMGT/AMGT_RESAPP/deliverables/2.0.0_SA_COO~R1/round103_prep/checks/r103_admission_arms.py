"""AMGT_RESAPP round-103 PREP -- the arms of the admission-table tool (`AMGT-bj-4`): it lists the registry files the BUILD packages, read from the build script, and only those.

  python r103_admission_arms.py [--instrument <path to r94_admission_table.py>]

The tool prints, for a pin and a ref, every package member whose bytes differ. Round 102's pair missed `infra/logic/registry/exemptions.json` because the tool diffed two registry files; the
CTO asked (ADDENDUM 1, msg 4929) that it diff EVERY registry file the build packages, with these arms. This script builds throwaway git repositories in a temp directory, each holding a
copy of `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh`'s `NAMING_REGISTRY_FILES` rule and a registry folder, and runs the instrument on them:
  A1  a ref that changes `exemptions.json` (packaged): the table LISTS `infra/logic/registry/exemptions.json`
  A2  a ref that changes ONLY `firm_pages.json` (in the folder, NOT packaged): the table lists NO registry file
  A3  a ref that changes no registry file: the table lists NO registry file ("a build that packages none lists none")
  A4  the rule is READ FROM THE BUILD SCRIPT: a repository whose script adds `feeds.json` to `NAMING_REGISTRY_FILES` lists a changed `feeds.json`
  A5  a ref that changes a `lib/` module: the table still lists it (the lib arm is unchanged)
Verdict `R103 ADMISSION ARMS: YES|NO` (5 of 5), exit 0 on YES. Writes only inside its temp directory.
"""
import os
import subprocess
import sys
import tempfile

SCRIPT = "infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh"
REG = "infra/logic/registry/"


def run(cwd, *cmd, check=True):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check, env=dict(os.environ, GIT_AUTHOR_NAME="x", GIT_AUTHOR_EMAIL="x@x",
                                                                                          GIT_COMMITTER_NAME="x", GIT_COMMITTER_EMAIL="x@x"))


def write(root, rel, text):
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def script_text(files):
    names = ", ".join('"%s"' % f for f in files)
    return ("# the packaging rule, as the real build script states it\nNAMING_REGISTRY_FILES = (%s)\n"
            'DATA_MEMBERS.append(("org/standards/NAMING_SCHEMA.json", "x", "org/standards/NAMING_SCHEMA.json"))\n') % names


def make_repo(extra_script_files=()):
    root = tempfile.mkdtemp(prefix="r103adm_")
    run(root, "git", "init", "-q")
    files = ["systems.json", "scopes.json", "tiers.json", "exemptions.json", "remediations.json", "resources.json", "reporting_policies.json"] + list(extra_script_files)
    write(root, SCRIPT, script_text(files))
    for n in files + ["firm_pages.json", "feeds.json"]:
        write(root, REG + n, '{"n": "%s", "v": 1}\n' % n)
    write(root, "org/standards/NAMING_SCHEMA.json", '{"v": 1}\n')
    write(root, "lib/opal_naming.py", "V = 1\n")
    run(root, "git", "add", "-A")
    run(root, "git", "commit", "-q", "-m", "pin")
    return root, run(root, "git", "rev-parse", "HEAD").stdout.strip()


def commit_change(root, rel, text):
    write(root, rel, text)
    run(root, "git", "add", "-A")
    run(root, "git", "commit", "-q", "-m", "ref: " + rel)
    return run(root, "git", "rev-parse", "HEAD").stdout.strip()


def table(instrument, root, ref, pin):
    out = run(root, sys.executable, instrument, ref, "--pin", pin, check=False)
    return out.stdout + out.stderr


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    default = os.path.normpath(os.path.join(here, "..", "..", "round94_prep", "checks", "r94_admission_table.py"))
    instrument = argv[argv.index("--instrument") + 1] if "--instrument" in argv else default
    instrument = os.path.abspath(instrument)
    arms = []

    def arm(name, ok, detail=""):
        arms.append((name, ok))
        print("   %s %s %s" % ("PASS" if ok else "FAIL", name, detail))

    root, pin = make_repo()
    ref = commit_change(root, REG + "exemptions.json", '{"n": "exemptions.json", "v": 2}\n')
    t = table(instrument, root, ref, pin)
    arm("A1 exemptions.json changed: listed", REG + "exemptions.json" in t, "")

    root, pin = make_repo()
    ref = commit_change(root, REG + "firm_pages.json", '{"n": "firm_pages.json", "v": 2}\n')
    t = table(instrument, root, ref, pin)
    arm("A2 only a NON-packaged registry file changed: none listed", (REG not in t.split("members whose bytes differ")[-1]), t.strip().splitlines()[0][:100] if t.strip() else "")

    root, pin = make_repo()
    ref = commit_change(root, "docs/note.md", "unrelated\n")
    t = table(instrument, root, ref, pin)
    arm("A3 no registry file changed: none listed", REG not in t.split("members whose bytes differ")[-1], t.strip().splitlines()[0][:100] if t.strip() else "")

    root, pin = make_repo(extra_script_files=("feeds.json",))
    ref = commit_change(root, REG + "feeds.json", '{"n": "feeds.json", "v": 2}\n')
    t = table(instrument, root, ref, pin)
    arm("A4 the rule is read from the build script: feeds.json listed once the script packages it", REG + "feeds.json" in t, "")

    root, pin = make_repo()
    ref = commit_change(root, "lib/opal_naming.py", "V = 2\n")
    t = table(instrument, root, ref, pin)
    arm("A5 a lib module change is still listed", "lib/opal_naming.py" in t, "")

    passed = sum(1 for _, ok in arms if ok)
    print("   arms passed %d of %d" % (passed, len(arms)))
    verdict = "YES" if passed == len(arms) else "NO"
    print("R103 ADMISSION ARMS: %s" % verdict)
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
