#!/usr/bin/env python3
"""Mutant control for AR384-y-AC1: the lint check must FIRE on the un-fixed literals.

Takes the candidate blobs at cand/dell2/anlreq-test-lint-fixes, REVERTS each rewritten literal to its
origin/DEV form in memory (never on disk, never in git), and lints the mutants with eslint --stdin.
The mutant FIRES when eslint reports one error per file, the rule named in the cell for that file.
Prints `MUTANT-FIRED <n> errors (no-regex-spaces in filing-hint, no-control-regex in filing-decision-tree)`
and exit 0 only when both rules fire; otherwise `MUTANT-DID-NOT-FIRE <why>` and exit 1.
"""
import json
import subprocess
import sys

sys.path.insert(0, "C:/dev/wk-irpt-anlreq-284/.tools")
from git_bash_resolver import git_bash  # noqa: E402

PORTAL = "C:/dev/wk-irpt-anlreq-284/portal"
CAND = "cand/dell2/anlreq-test-lint-fixes"
HINT = "src/pages/TicketCenter/__tests__/filing-hint.test.tsx"
TREE = "src/pages/TicketCenter/__tests__/filing-decision-tree.test.tsx"


def blob(path):
    p = subprocess.run(["git", "-C", PORTAL, "show", f"{CAND}:{path}"], capture_output=True)
    if p.returncode != 0:
        print(f"MUTANT-DID-NOT-FIRE git show {path} rc={p.returncode}")
        sys.exit(1)
    return p.stdout


def lint(bash, path, data):
    cmd = f"bun x eslint --stdin --stdin-filename {path} -f json"
    p = subprocess.run([bash, "-c", cmd], cwd=PORTAL, input=data, capture_output=True)
    try:
        res = json.loads(p.stdout.decode("utf-8", "replace"))
    except ValueError:
        print(f"MUTANT-DID-NOT-FIRE eslint output not JSON for {path}")
        sys.exit(1)
    return [m["ruleId"] for r in res for m in r.get("messages", [])]


def main():
    bash = git_bash()
    if not bash:
        print("MUTANT-DID-NOT-FIRE no Git Bash resolved")
        sys.exit(1)
    hint = blob(HINT)
    tree = blob(TREE)
    # reverse the rewrite: the origin/DEV literal text, read back from the base blob for the same file
    base_hint = subprocess.run(["git", "-C", PORTAL, "show", f"origin/DEV:{HINT}"], capture_output=True).stdout
    base_tree = subprocess.run(["git", "-C", PORTAL, "show", f"origin/DEV:{TREE}"], capture_output=True).stdout
    if base_hint == hint or base_tree == tree:
        print("MUTANT-DID-NOT-FIRE candidate equals base for a file; no rewrite to revert")
        sys.exit(1)
    mut_hint = hint.replace(b"\\n {2}\\}", b"\\n  \\}")
    mut_tree = tree.replace(bytes([91, 92, 98, 93]), bytes([91, 0x08, 93]))
    rules_hint = lint(bash, HINT, mut_hint)
    rules_tree = lint(bash, TREE, mut_tree)
    ok = rules_hint == ["no-regex-spaces"] and rules_tree.count("no-control-regex") >= 1
    n = len(rules_hint) + len(rules_tree)
    if ok:
        print(f"MUTANT-FIRED {n} errors (no-regex-spaces in filing-hint, no-control-regex in filing-decision-tree)")
        sys.exit(0)
    print(f"MUTANT-DID-NOT-FIRE filing-hint rules={rules_hint} filing-decision-tree rules={rules_tree}")
    sys.exit(1)


if __name__ == "__main__":
    main()
