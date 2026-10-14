"""AR336-y-AC3 checker (written by 0.9.0_WK_IRPT_ANLREQ~143). ASCII only.

Prints SCOPE-OK only when (1) `git diff --name-only <base> HEAD` lists only the builder, the re-pinned import test, the
new test file, and paths under org/missions/D9/IRPT/IRPT_ANLREQ/ (the base is the `base` field of the record JSON), AND
(2) the builder's diff adds only the two binding keys, their named constants and comments, and removes no line.
Otherwise prints SCOPE-BAD <why> and exits 1.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WT = next(p for p in HERE.parents if (p / ".tools").is_dir() and (p / "org").is_dir())
RECORD = HERE / "r41" / "RESIDENT_R31_PACKAGER_BINDINGS_RECORD.json"
BUILDER_REL = "infra/aws/lambda/investor-reporting/reports/build_resident_package.py"
IMPORTS_REL = "infra/aws/lambda/investor-reporting/reports/tests/test_resident_package_imports.py"
NEW_REL = "infra/aws/lambda/investor-reporting/reports/tests/test_resident_r31_packager_bindings.py"
ORDER_PREFIX = "org/missions/D9/IRPT/IRPT_ANLREQ/"
ALLOWED_ADDED = (
    re.compile(r"^\s*#"),                                                        # a comment
    re.compile(r'^[A-Z][A-Z0-9_]* = "[^"]*"$'),                                  # a named constant
    re.compile(r'^    "commentary_ready_queue_url": SQS_PREFIX \+ names\["commentary_ready_queue"\]\["name"\],$'),
    re.compile(r'^    "packager": \{"api_base": PACKAGER_API_BASE, "secret_name": PACKAGER_SECRET_NAME\},$'),
)


def git(*args):
    return subprocess.run(["git", "-C", str(WT)] + list(args), capture_output=True, text=True, check=True).stdout


def main():
    base = json.loads(RECORD.read_text(encoding="utf-8"))["base"]
    print("BASE " + base)
    names = [n for n in git("diff", "--name-only", base, "HEAD").splitlines() if n]
    print("PATHS " + str(len(names)) + " changed since base")
    for name in names:
        print("  " + name)
    allowed = {BUILDER_REL, IMPORTS_REL, NEW_REL}
    outside = [n for n in names if n not in allowed and not n.startswith(ORDER_PREFIX)]
    if outside:
        print("SCOPE-BAD paths outside the grant: " + ", ".join(outside))
        return 1
    for required in (BUILDER_REL, NEW_REL):
        if required not in names:
            print("SCOPE-BAD required path not in the diff: " + required)
            return 1
    diff = git("diff", "-U0", base, "HEAD", "--", BUILDER_REL).splitlines()
    added = [line[1:] for line in diff if line.startswith("+") and not line.startswith("+++")]
    removed = [line[1:] for line in diff if line.startswith("-") and not line.startswith("---")]
    if removed:
        print("SCOPE-BAD the builder diff removes %d line(s): %r" % (len(removed), removed[:3]))
        return 1
    stray = [line for line in added if not any(pattern.match(line) for pattern in ALLOWED_ADDED)]
    if stray:
        print("SCOPE-BAD the builder diff adds a line that is not a key, a named constant or a comment: %r" % stray[:3])
        return 1
    print("BUILDER ADDED %d line(s), all keys, named constants or comments" % len(added))
    print("SCOPE-OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
