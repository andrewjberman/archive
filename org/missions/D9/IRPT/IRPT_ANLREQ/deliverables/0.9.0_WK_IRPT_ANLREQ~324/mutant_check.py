"""AR-y-455 difference control: revert the guard edit in place for one bun run, then restore it.

The pre-edit guard is read from git (dd2b20ac58fe, the DEV base the branch was cut from). The committed guard
bytes are saved to a scratch file, the pre-edit bytes are written over the guard, the guard test file runs once,
and the saved bytes are written back with a sha256 check. Prints MUTANT-FIRES only when the run fails BOTH
named tests: (1) the real Ticket Center body and (5) the seam test. Otherwise MUTANT-SURVIVES, exit 1.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

PRE_EDIT = "dd2b20ac58fe"
GUARD = "src/pages/InvestorReporting/contracts/submission-request.ts"
TEST = "src/pages/InvestorReporting/__tests__/submission-request.test.ts"
NAMED = ("commentary_requested: the real Ticket Center body", "commentary_requested reaches transport")
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
# bun 1.4 marks a failed case with a cross mark (U+2717, built here so the source stays ASCII) and the duration in brackets
CROSS = re.escape(chr(0x2717))
FAIL_LINE = re.compile(r"^\s*" + CROSS + r"\s+(.*?)(?:\s+\[[0-9.]+ms\])?\s*$", re.M)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    repo = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    portal = os.path.join(repo, "portal")
    bun = shutil.which("bun")
    if bun is None:
        print("MUTANT-SURVIVES BLOCKED: bun not on PATH")
        return 1
    target = os.path.join(portal, GUARD)
    scratch = os.path.join(repo, ".scratch")
    os.makedirs(scratch, exist_ok=True)
    backup_path = os.path.join(scratch, "guard_committed.bak")
    with open(target, "rb") as fh:
        committed = fh.read()
    pre_edit = subprocess.check_output(["git", "-C", portal, "show", f"{PRE_EDIT}:{GUARD}"])
    # positive control: the pre-edit bytes are non-empty and carry no commentary_requested
    if not pre_edit or b"commentary_requested" in pre_edit:
        print("MUTANT-SURVIVES BLOCKED: the pre-edit guard read from git is not the expected base")
        return 1
    if b"commentary_requested" not in committed:
        print("MUTANT-SURVIVES BLOCKED: the committed guard does not carry the edit")
        return 1
    with open(backup_path, "wb") as fh:
        fh.write(committed)
    committed_sha = sha(committed)
    try:
        with open(target, "wb") as fh:
            fh.write(pre_edit)
        run = subprocess.run([bun, "test", TEST], cwd=portal, capture_output=True, timeout=300)
    finally:
        with open(backup_path, "rb") as fh:
            restored = fh.read()
        with open(target, "wb") as fh:
            fh.write(restored)
    with open(target, "rb") as fh:
        after = sha(fh.read())
    if after != committed_sha:
        print(f"RESTORE-BAD: sha256 {after} != {committed_sha}")
        return 2
    text = ANSI.sub("", (run.stdout + run.stderr).decode("utf-8", "replace"))
    with open(os.path.join(scratch, "mutant_bun_output.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    fails = [m.group(1).strip() for m in FAIL_LINE.finditer(text)]
    summary = [ln.strip() for ln in text.splitlines() if re.match(r"^\s*\d+ (pass|fail)$", ln)]
    print(f"mutant run rc={run.returncode} summary={' / '.join(summary)}")
    for name in fails:
        print(f"FAILING: {name}")
    print(f"restored sha256 {after} (matches committed: {after == committed_sha})")
    named_hit = all(any(name.startswith(prefix) for name in fails) for prefix in NAMED)
    if run.returncode != 0 and named_hit:
        print(f"MUTANT-FIRES tests (1) and (5) fail on the pre-edit guard; {len(fails)} failing in the file")
        return 0
    print("MUTANT-SURVIVES: a named test passed on the pre-edit guard")
    return 1


if __name__ == "__main__":
    sys.exit(main())
