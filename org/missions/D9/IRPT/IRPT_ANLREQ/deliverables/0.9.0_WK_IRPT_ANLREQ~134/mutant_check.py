"""AR327-y-AC2 (IRPT_ANLREQ AR-y-327): the one mutant that must fail. A copy of the investor-reporting tree and lib is made in a
scratch folder under the worktree's .scratch (outside the product tree); in the copy's opal_packager.py the commentary call is
changed back to opal_producer.produce_package (the combined shape). The new test file runs against the copy. Prints
MUTANT-FIRES only when that run FAILS; otherwise MUTANT-SURVIVES and exit 1."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

NEW = "test_commentary_standalone_pdf.py"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
SITE = 'ports.get("produce_commentary") or opal_producer.produce_commentary_pdf'
MUTANT = 'ports.get("produce_commentary") or opal_producer.produce_package'


def root():
    here = Path(__file__).resolve()
    for p in [here] + list(here.parents):
        if (p / ".tools").is_dir() and (p / "org").is_dir():
            return p
    print("MUTANT-SURVIVES root with .tools and org not found above " + str(here))
    sys.exit(1)


def main():
    r = root()
    scratch = r / ".scratch" / "mutant_ar327"
    if scratch.exists():
        shutil.rmtree(str(scratch))
    ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(str(r / "infra/aws/lambda/investor-reporting"), str(scratch / "infra/aws/lambda/investor-reporting"),
                    ignore=ignore)
    shutil.copytree(str(r / "lib"), str(scratch / "lib"), ignore=ignore)
    shutil.copytree(str(r / "infra/logic"), str(scratch / "infra/logic"), ignore=ignore)  # the naming registry, read by lib
    shutil.copytree(str(r / "org/standards"), str(scratch / "org/standards"), ignore=ignore)  # NAMING_SCHEMA.json, read by lib
    packager =scratch / "infra/aws/lambda/investor-reporting/ycharts/research/opal_packager.py"
    text = packager.read_text(encoding="utf-8")
    sites = text.count(SITE)
    if sites != 1:
        print("MUTANT-SURVIVES the mutation site was found %d times, expected 1" % sites)
        shutil.rmtree(str(scratch), ignore_errors=True)
        return 1
    packager.write_text(text.replace(SITE, MUTANT), encoding="utf-8")
    tests = scratch / "infra/aws/lambda/investor-reporting/ycharts/research/tests"
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "--color=no", "-p", "no:cacheprovider", NEW],
                          cwd=str(tests), capture_output=True, text=True, timeout=110)
    out = ANSI.sub("", proc.stdout + proc.stderr)
    summary = [ln for ln in out.splitlines() if " in " in ln and ("passed" in ln or "failed" in ln or "error" in ln)]
    failed = re.findall(r"^FAILED (\S+)", out, flags=re.MULTILINE)
    print("MUTANT-RUN mutation=produce_package rc=%d %s" % (proc.returncode, summary[-1].strip() if summary else "NO-SUMMARY"))
    for name in failed:
        print("MUTANT-FAILED " + name)
    shutil.rmtree(str(scratch), ignore_errors=True)
    if proc.returncode != 0 and failed:
        print("MUTANT-FIRES")
        return 0
    print("MUTANT-SURVIVES the new file passed against the combined-shape copy")
    return 1


if __name__ == "__main__":
    sys.exit(main())
