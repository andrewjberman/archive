"""AR-y-363 criterion AR363-y-AC2: the Replace button is removed in a scratch copy OUTSIDE the product tree, and the decision-tree
test file runs against that copy.

The file holding the Replace button is src/pages/TicketCenter/AnalysisRequestParts.tsx (the ReplaceTicker element inside the
tree). The scratch copy carries the whole TicketCenter folder from the portal worktree, the new test file, a tsconfig whose
"@/*" alias points at the portal's src, and a link to the portal's node_modules. A control copy (unmutated) runs first and must pass.

Prints MUTANT-FIRES only when the mutant run FAILS (and the control passes). Otherwise prints MUTANT-SURVIVES <why>, exit 1.
ASCII output only.
"""
import os
import re
import shutil
import subprocess
import sys

PORTAL = "C:/dev/wk-irpt-anlreq-160/portal"
SCRATCH = "C:/dev/wk-irpt-anlreq-160/.scratch/mutant_check"
FOLDER_REL = "src/pages/TicketCenter"
TEST_REL = "src/pages/TicketCenter/__tests__/filing-decision-tree.test.tsx"
HOLDER = "AnalysisRequestParts.tsx"
REPLACE_ELEMENT = re.compile(r"[ \t]*<ReplaceTicker h=\{h\} busy=\{busy\} onChoose=\{onChoose\} />[ \t]*\n")
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def bun_path():
    found = shutil.which("bun")
    if found:
        return found
    fallback = ("C:/Users/Test/AppData/Local/Microsoft/WinGet/Packages/Oven-sh.Bun_Microsoft.Winget.Source_8wekyb3d8bbwe/"
                "bun-windows-x64/bun.exe")
    return fallback if os.path.exists(fallback) else None


def build_copy(dest, mutate):
    """A scratch copy of the folder, its test file, the alias config and the modules link; mutate=True removes the Replace element."""
    if os.path.lexists(dest):
        # the modules link is removed first as a LINK (os.rmdir on a symlink or junction removes only the link), so no
        # rmtree can reach the portal's own node_modules through it
        link_old = os.path.join(dest, "node_modules")
        if os.path.lexists(link_old):
            os.rmdir(link_old)
        shutil.rmtree(dest)
    src_dir = os.path.join(dest, FOLDER_REL)
    os.makedirs(os.path.join(src_dir, "__tests__"))
    for name in os.listdir(os.path.join(PORTAL, FOLDER_REL)):
        full = os.path.join(PORTAL, FOLDER_REL, name)
        if os.path.isfile(full):
            shutil.copyfile(full, os.path.join(src_dir, name))
    shutil.copyfile(os.path.join(PORTAL, TEST_REL), os.path.join(src_dir, "__tests__", os.path.basename(TEST_REL)))
    holder = os.path.join(src_dir, HOLDER)
    text = open(holder, encoding="utf-8").read()
    if mutate:
        found = REPLACE_ELEMENT.findall(text)
        if len(found) != 1:
            return "the Replace element matched %d times, expected 1" % len(found)
        text = REPLACE_ELEMENT.sub("", text)
        with open(holder, "w", encoding="utf-8") as fh:
            fh.write(text)
    with open(os.path.join(dest, "tsconfig.json"), "w", encoding="utf-8") as fh:
        fh.write('{ "compilerOptions": { "baseUrl": ".", "paths": { "@/*": ["%s/src/*"] } } }\n' % PORTAL)
    link = os.path.join(dest, "node_modules")
    try:
        os.symlink(os.path.join(PORTAL, "node_modules"), link, target_is_directory=True)
    except OSError:
        subprocess.run(["cmd", "/c", "mklink", "/J", link.replace("/", "\\"), os.path.join(PORTAL, "node_modules").replace("/", "\\")],
                       capture_output=True, text=True, timeout=60)
    return None


def run_test(bun, dest):
    proc = subprocess.run([bun, "test", os.path.join(FOLDER_REL, "__tests__", os.path.basename(TEST_REL))], cwd=dest,
                          capture_output=True, text=True, timeout=120)
    text = ANSI.sub("", proc.stdout + proc.stderr)
    passed = [int(m) for m in re.findall(r"^\s*(\d+) pass\s*$", text, re.M)]
    failed = [int(m) for m in re.findall(r"^\s*(\d+) fail\s*$", text, re.M)]
    return proc.returncode, (passed[-1] if passed else None), (failed[-1] if failed else None)


def main():
    bun = bun_path()
    if bun is None:
        print("MUTANT-SURVIVES bun not found on PATH or at the WinGet path")
        sys.exit(1)
    control = SCRATCH + "_control"
    err = build_copy(control, mutate=False)
    if err:
        print("MUTANT-SURVIVES control copy: " + err)
        sys.exit(1)
    c_rc, c_pass, c_fail = run_test(bun, control)
    if c_rc != 0 or c_fail != 0 or c_pass is None:
        print("MUTANT-SURVIVES control run did not pass: rc=%d pass=%s fail=%s" % (c_rc, c_pass, c_fail))
        sys.exit(1)
    err = build_copy(SCRATCH, mutate=True)
    if err:
        print("MUTANT-SURVIVES mutant copy: " + err)
        sys.exit(1)
    m_rc, m_pass, m_fail = run_test(bun, SCRATCH)
    if m_rc != 0 and (m_fail or 0) > 0:
        print("MUTANT-FIRES the Replace button removed: mutant rc=%d pass=%s fail=%s; control rc=0 pass=%s fail=0"
              % (m_rc, m_pass, m_fail, c_pass))
        sys.exit(0)
    print("MUTANT-SURVIVES the Replace button removed still passes: mutant rc=%d pass=%s fail=%s" % (m_rc, m_pass, m_fail))
    sys.exit(1)


if __name__ == "__main__":
    main()
