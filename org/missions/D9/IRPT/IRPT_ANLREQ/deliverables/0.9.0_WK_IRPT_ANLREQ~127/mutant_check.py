"""AR317-y-AC2 -- the one mutant that must fail (TO-AR-y-317, worker 0.9.0_WK_IRPT_ANLREQ~127).

Copies analysisRequest.ts OUTSIDE the product tree (into a scratch folder) with the commentary member made conditional on
answers.add_commentary === true (the held candidate's shape), runs the new test file against the copy, and prints
MUTANT-FIRES only when that run FAILS. Else MUTANT-SURVIVES, exit 1.

The scratch folder holds its own tsconfig.json whose '@/*' alias points at the portal src, so the copy's imports resolve
as they do in the product. The test file is copied beside the mutant with its one import of the module redirected to
the copy. A control run on the UNMUTATED copy must pass every case first, so a harness fault cannot read as a fire.
The product file is never written; its sha is printed before and after.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-127/portal"
PRODUCT_SRC = PORTAL + "/src/pages/TicketCenter/analysisRequest.ts"
PRODUCT_TEST = PORTAL + "/src/pages/TicketCenter/__tests__/analysis-commentary-always-requested.test.ts"
SCRATCH = "C:/dev/wk-irpt-anlreq-127/.scratch/ar317_mutant"
ANSI = re.compile(r"\x1b\[[0-9;]*m")
MEMBER = "commentary_requested: true,"
MUTANT_FIRST = "commentary_requested: a.add_commentary === true,"
MUTANT_SECOND = "commentary_requested: input.answers.add_commentary === true,"


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_tests(directory, filename):
    bun = shutil.which("bun")
    if bun is None:
        return None, "bun is not on PATH"
    try:
        proc = subprocess.run([bun, "test", filename], cwd=directory, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return None, "bun test timed out after 120 seconds"
    text = ANSI.sub("", (proc.stdout + proc.stderr).decode("utf-8", errors="replace"))
    p = re.findall(r"^\s*(\d+) pass\s*$", text, re.M)
    f = re.findall(r"^\s*(\d+) fail\s*$", text, re.M)
    if not p or not f:
        return None, "could not parse the summary (rc=%d)" % proc.returncode
    return {"rc": proc.returncode, "pass": int(p[-1]), "fail": int(f[-1])}, None


def main():
    before = sha(PRODUCT_SRC)
    with open(PRODUCT_SRC, encoding="utf-8") as fh:
        original = fh.read()
    if original.count(MEMBER) != 2:
        print("MUTANT-SURVIVES harness: expected 2 commentary_requested members in the product file, found %d"
              % original.count(MEMBER))
        return 1
    mutated = original.replace(MEMBER, MUTANT_FIRST, 1).replace(MEMBER, MUTANT_SECOND, 1)

    with open(PRODUCT_TEST, encoding="utf-8") as fh:
        test_src = fh.read()
    if test_src.count("'@/pages/TicketCenter/analysisRequest'") != 1:
        print("MUTANT-SURVIVES harness: the test file does not import the module exactly once")
        return 1
    test_src = test_src.replace("'@/pages/TicketCenter/analysisRequest'", "'./analysisRequest'")
    declared = len(re.findall(r"^\s*test\(", test_src, re.M))

    os.makedirs(SCRATCH, exist_ok=True)
    os.makedirs(os.path.join(SCRATCH, "control"), exist_ok=True)
    os.makedirs(os.path.join(SCRATCH, "mutant"), exist_ok=True)
    tsconfig = {"compilerOptions": {"baseUrl": PORTAL, "paths": {"@/*": ["./src/*"]}}}
    with open(os.path.join(SCRATCH, "tsconfig.json"), "w", encoding="utf-8") as fh:
        json.dump(tsconfig, fh, indent=2)

    results = {}
    for name, body in (("control", original), ("mutant", mutated)):
        folder = os.path.join(SCRATCH, name)
        with open(os.path.join(folder, "analysisRequest.ts"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        with open(os.path.join(folder, "analysis-commentary-always-requested.test.ts"), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(test_src)
        result, err = run_tests(folder, "analysis-commentary-always-requested.test.ts")
        if err:
            print("MUTANT-SURVIVES harness: %s run: %s" % (name, err))
            return 1
        results[name] = result

    after = sha(PRODUCT_SRC)
    if before != after:
        print("MUTANT-SURVIVES harness: the product file changed during the check")
        return 1

    control, mutant = results["control"], results["mutant"]
    print("control (unmutated copy): rc=%d pass=%d fail=%d of %d declared"
          % (control["rc"], control["pass"], control["fail"], declared))
    print("mutant (member conditional on add_commentary): rc=%d pass=%d fail=%d of %d declared"
          % (mutant["rc"], mutant["pass"], mutant["fail"], declared))
    print("product sha256 before=%s after=%s unchanged=%s" % (before[:16], after[:16], before == after))
    if control["fail"] != 0 or control["pass"] != declared:
        print("MUTANT-SURVIVES harness: the control run did not pass every case")
        return 1
    if mutant["fail"] >= 1:
        print("MUTANT-FIRES")
        return 0
    print("MUTANT-SURVIVES the mutant run had no failing case")
    return 1


if __name__ == "__main__":
    sys.exit(main())
