"""AR-y-354 criterion AR354-y-AC2: one mutant of the helper that builds the Keep pair must make the keep test file FAIL.

The helper file (analysisRequest.ts at the portal HEAD) is copied to a scratch folder OUTSIDE the product tree, with keptHint built
as a SWAP (the to_value is the symbol plus X, a different symbol). The copy is run with the keep test file. A positive control runs
the unmutated copy first and must pass (else MUTANT-HARNESS-BAD, exit 1). Prints MUTANT-FIRES only when the mutated run FAILS;
otherwise MUTANT-SURVIVES, exit 1. The product tree is never written. ASCII output only.
"""
import os
import re
import shutil
import subprocess
import sys
import tarfile
import io

WT = "C:/dev/wk-irpt-anlreq-154"
PORTAL = WT + "/portal"
SCRATCH = WT + "/.scratch/mutant_check"
SCRATCH_TC = SCRATCH + "/src/pages/TicketCenter"
LINK = SCRATCH + "/node_modules"
TARGET = PORTAL + "/node_modules"
KEEP_TEST = "src/pages/TicketCenter/__tests__/filing-hint-keep.test.tsx"
HELPER = "src/pages/TicketCenter/analysisRequest.ts"
OLD = "return { row: h.row, value: h.value, suggestion: h.value, description: h.description }"
MUTANT = "return { row: h.row, value: h.value, suggestion: h.value + 'X', description: h.description }"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def bun_path():
    found = shutil.which("bun")
    if found:
        return found
    fallback = ("C:/Users/Test/AppData/Local/Microsoft/WinGet/Packages/Oven-sh.Bun_Microsoft.Winget.Source_8wekyb3d8bbwe/"
                "bun-windows-x64/bun.exe")
    return fallback if os.path.exists(fallback) else None


def unlink_junction():
    """Remove the node_modules link only. rmdir without /S never enters the target."""
    if os.path.lexists(LINK):
        subprocess.run(["cmd", "/c", "rmdir", LINK.replace("/", "\\")], capture_output=True)


def cleanup():
    unlink_junction()
    if os.path.lexists(LINK):
        print("MUTANT-HARNESS-BAD scratch link could not be removed; left in place for inspection")
        sys.exit(1)
    shutil.rmtree(SCRATCH, ignore_errors=True)


def build_scratch():
    if os.path.lexists(SCRATCH):
        unlink_junction()
        shutil.rmtree(SCRATCH, ignore_errors=True)
    os.makedirs(SCRATCH_TC, exist_ok=True)
    archive = subprocess.run(["git", "-C", PORTAL, "archive", "HEAD", "src/pages/TicketCenter"], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
        for member in tf.getmembers():
            if member.name.startswith("src/pages/TicketCenter/") and member.isfile():
                target = os.path.join(SCRATCH, member.name)
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "wb") as out:
                    out.write(tf.extractfile(member).read())
    with open(SCRATCH + "/tsconfig.json", "w", encoding="utf-8") as fh:
        fh.write('{ "compilerOptions": { "baseUrl": ".", "paths": { "@/*": ["' + PORTAL + '/src/*"] } } }\n')
    proc = subprocess.run(["cmd", "/c", "mklink", "/J", LINK.replace("/", "\\"), TARGET.replace("/", "\\")], capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.lexists(LINK):
        print("MUTANT-HARNESS-BAD could not link node_modules into the scratch copy: " + proc.stdout + proc.stderr)
        sys.exit(1)


def run_keep(bun):
    proc = subprocess.run([bun, "test", KEEP_TEST], cwd=SCRATCH,
                          capture_output=True, text=True, timeout=300)
    text = ANSI.sub("", proc.stdout + proc.stderr)
    fails = re.findall(r"^\s*(\d+) fail\s*$", text, re.M)
    passes = re.findall(r"^\s*(\d+) pass\s*$", text, re.M)
    return proc.returncode, (int(passes[-1]) if passes else None), (int(fails[-1]) if fails else None)


def main():
    bun = bun_path()
    if bun is None:
        print("MUTANT-HARNESS-BAD bun not found")
        sys.exit(1)
    try:
        build_scratch()
        rc0, p0, f0 = run_keep(bun)
        if rc0 != 0 or f0 != 0 or p0 != 7:
            print("MUTANT-HARNESS-BAD positive control (unmutated copy) rc=%s pass=%s fail=%s" % (rc0, p0, f0))
            sys.exit(1)
        helper = os.path.join(SCRATCH_TC, "analysisRequest.ts")
        with open(helper, encoding="utf-8") as fh:
            body = fh.read()
        if body.count(OLD) != 1:
            print("MUTANT-HARNESS-BAD the keptHint return line occurs %d times, expected 1" % body.count(OLD))
            sys.exit(1)
        with open(helper, "w", encoding="utf-8") as fh:
            fh.write(body.replace(OLD, MUTANT))
        rc1, p1, f1 = run_keep(bun)
        if rc1 != 0:
            print("MUTANT-FIRES keep test file fails on the swap mutant: rc=%d pass=%s fail=%s (control: rc=0 pass=7 fail=0)" % (rc1, p1, f1))
            sys.exit(0)
        print("MUTANT-SURVIVES keep test file did not fail on the swap mutant: rc=%d pass=%s fail=%s" % (rc1, p1, f1))
        sys.exit(1)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
