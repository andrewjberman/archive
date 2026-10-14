"""R18P1-AC2 -- the one mutant: the coordinator's Confirm sends the FIRST proposed time whatever was clicked.

A scratch copy of MeetingRequestParts.tsx with that change, and a scratch copy of the new test file that imports it, are made in a
folder under the workspace worktree's .scratch (OUTSIDE the portal product tree). Both live in one scratch folder, whose tsconfig maps
the @/ alias to the portal source so the copies resolve the same modules as the product. The new test file is run against the
unmutated copy first (a control: it must pass) and then against the mutant (it must fail).

Prints MUTANT-FIRES only when the mutant run FAILS; MUTANT-SURVIVES (exit 1) when it passes; MUTANT-CONTROL-BROKEN (exit 1) when the
unmutated control does not pass, which would make a FAIL meaningless.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

WORKTREE = "C:/dev/wk-tckt-vnext-42"
PORTAL = WORKTREE + "/portal"
PARTS = PORTAL + "/src/pages/TicketCenter/MeetingRequestParts.tsx"
TEST = PORTAL + "/src/pages/TicketCenter/__tests__/meeting-request.test.tsx"
CONFIRM_OLD = "await record(ticket.ticket_id, { action: 'confirm', time })"
CONFIRM_MUTANT = "await record(ticket.ticket_id, { action: 'confirm', time: times[0] })"
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def rewrite_parts(text):
    # The copy sits in the scratch folder: its sibling imports and the alias resolve to the portal source.
    return re.sub(r"from '\./", "from '@/pages/TicketCenter/", text)


def rewrite_test(text):
    text = text.replace("'../MeetingRequestParts'", "'./MeetingRequestParts'")
    text = text.replace("'../../", "'@/pages/")
    text = text.replace("'../", "'@/pages/TicketCenter/")
    return text


def link_modules(scratch):
    # A directory junction (no admin needed) so the copies resolve the portal's packages; bun does not read NODE_PATH.
    link = os.path.join(scratch, "node_modules")
    proc = subprocess.run(["cmd", "/c", "mklink", "/J", link, os.path.normpath(PORTAL + "/node_modules")],
                          capture_output=True, text=True)
    if proc.returncode != 0 or not os.path.isdir(link):
        print("MUTANT-CONTROL-BROKEN could not link node_modules into the scratch folder: %s" % proc.stderr.strip()[:200])
        sys.exit(1)
    return link


def run_test(scratch_test):
    bun = shutil.which("bun") or "bun"
    proc = subprocess.run([bun, "test", scratch_test], cwd=PORTAL, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=100)
    return proc.returncode, ANSI.sub("", (proc.stdout or "") + (proc.stderr or ""))


def main():
    with open(PARTS, encoding="utf-8") as fh:
        parts_src = fh.read()
    with open(TEST, encoding="utf-8") as fh:
        test_src = fh.read()
    if parts_src.count(CONFIRM_OLD) != 1:
        print("MUTANT-SURVIVES the confirm line was found %d times, not 1" % parts_src.count(CONFIRM_OLD))
        sys.exit(1)
    scratch_root = os.path.join(WORKTREE, ".scratch")
    os.makedirs(scratch_root, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="mutant_mt3_", dir=scratch_root)
    link = None
    try:
        link = link_modules(scratch)
        with open(os.path.join(scratch, "tsconfig.json"), "w", encoding="utf-8") as fh:
            json.dump({"compilerOptions": {"jsx": "react-jsx", "baseUrl": ".",
                                           "paths": {"@/*": [PORTAL + "/src/*"]}}}, fh)
        with open(os.path.join(scratch, "meeting-request.test.tsx"), "w", encoding="utf-8") as fh:
            fh.write(rewrite_test(test_src))
        scratch_test = os.path.join(scratch, "meeting-request.test.tsx")

        with open(os.path.join(scratch, "MeetingRequestParts.tsx"), "w", encoding="utf-8") as fh:
            fh.write(rewrite_parts(parts_src))
        rc_c, out_c = run_test(scratch_test)
        if rc_c != 0:
            print("MUTANT-CONTROL-BROKEN the unmutated copy fails (rc=%s) so the mutant run means nothing" % rc_c)
            sys.exit(1)

        with open(os.path.join(scratch, "MeetingRequestParts.tsx"), "w", encoding="utf-8") as fh:
            fh.write(rewrite_parts(parts_src.replace(CONFIRM_OLD, CONFIRM_MUTANT)))
        rc_m, out_m = run_test(scratch_test)
        failed = re.findall(r"^\s*(\d+) fail\s*$", out_m, re.M)
        summary = "rc=%s control-pass mutant-fail=%s" % (rc_m, failed[-1] if failed else "?")
        if rc_m != 0:
            print("MUTANT-FIRES " + summary)
            sys.exit(0)
        print("MUTANT-SURVIVES " + summary)
        sys.exit(1)
    finally:
        # Remove the junction as a link (os.rmdir never descends into it), then the scratch copies.
        if link is not None and os.path.isdir(link):
            os.rmdir(link)
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    main()
