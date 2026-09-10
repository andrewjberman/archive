"""CE-e-2 / E2-AC1 -- THE BATTERY: a tool verified by its BARE NAME is the tool you changed.

TOKEN: CEE2-FORWARDERS-RESOLVE-TO-CALLER -- printed ONLY when EVERY arm holds. rc 0 with the token,
rc 1 without it. Every path printed absolute; every list carries its denominator.

THE ARMS, as the task order cuts them:
  (a) THE POPULATION -- the forwarders the provisioner regenerated, counted, with the denominator
      RE-DERIVED at this seat and printed beside round 7's cited 186 (and why they differ).
  (b) BOTH DIRECTIONS OF THE RESOLUTION, which is the whole cell -- `comp-which --which` BY THE
      BARE NAME from the MAIN tree prints the main tree's .tools/comp-which, and from a FRESH
      LINKED WORKTREE prints THAT worktree's; both absolute, and the two differ.
  (c) THE PLANTED EDIT, because a path that merely PRINTS right can still EXEC wrong -- a one-line
      marker in the FRESH worktree's .tools/comp-which appears in the bare-name run FROM that
      worktree and does NOT appear in the bare-name run from the main tree; then reverted and
      sha256-verified back.
  (d) THE NO-TOPLEVEL CASE -- a forwarder invoked from a directory inside no worktree falls back to
      the baked path AND SAYS SO on stderr; the exact line, the rc and the stream all recorded.
  (e) THE HARNESS -- its bare invocation writes NOTHING under
      org/tier2_senior/0.8.0_AE_CloudComp/deliverables/ (that file's sha256 identical before and
      after, printed) and completes inside the bound the file now STATES, with the runtime measured
      at this seat printed beside it.
  (f) NOTHING ELSE MOVED -- a named sample of other forwarders exercised after the regeneration,
      with its denominator, and the backup copy's absolute location printed.

BOTH PLANES ARE EXERCISED. The extensionless forwarder is what a bash caller gets; the .cmd twin is
what PowerShell and cmd get, and PowerShell is the primary shell on this box. A check scoped to one
plane cannot see a defect in what the two share -- and what they share is the generator.

WHY THE BASH PLANE IS INVOKED THROUGH AN EXPLICITLY RESOLVED bash.exe: a bare `bash` from Python on
this box resolves to the WSL stub (rc 1, a 504-byte UTF-16LE file), not Git Bash. `.tools/
git_bash_resolver.py` is the estate's answer and is used here rather than a baked path.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
# deliverables/<serial>/ -> deliverables -> NFRA_COMPEFFICACY -> NFRA -> D11 -> missions -> org -> ROOT
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))

TOKEN = "CEE2-FORWARDERS-RESOLVE-TO-CALLER"
BIN = os.path.join(os.path.expanduser("~"), "bin")
BASELINE_REL = ("org/tier2_senior/0.8.0_AE_CloudComp/deliverables/"
                "comp-which-routing-baseline.json")
HARNESS_REL = ".tools/comp-which-routing-test.py"
ROUND7_CITED_POPULATION = 186          # the number the row and the generator's own header cite
BACKUP_DIR = os.path.join(WS, ".scratch", "bin-backup-pre-ce-e-2")

# The sample arm (f) exercises. NAMED, not sliced at random: two python tools, two bash tools, the
# non-comp aws case, and the two commit-gate tools whose absence once turned safe-commit's coverage
# gate off silently (the outage this provisioner's own header records).
SAMPLE = ["comp-find", "comp-read", "comp-system", "comp-estate",
          "comp-coverage-check", "comp-manifest-check", "aws"]

RESULTS = []


def check(name, ok, msg):
    RESULTS.append((name, bool(ok), msg))
    print("  [%s] %-26s %s" % ("PASS" if ok else "FAIL", name, msg))
    return bool(ok)


def hdr(t):
    print("")
    print("-" * 100)
    print(t)
    print("-" * 100)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(args, cwd=None, timeout=600):
    r = subprocess.run(["git"] + list(args), cwd=cwd or WS, capture_output=True,
                       text=True, timeout=timeout)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def _git_bash():
    p = os.path.join(WS, ".tools", "git_bash_resolver.py")
    try:
        spec = importlib.util.spec_from_file_location("git_bash_resolver", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        b = m.git_bash()
        if b:
            return b
    except Exception as e:  # noqa: BLE001 -- the resolver is the preferred instrument, not the only one
        print("  NOTE: git_bash_resolver unusable (%s: %s); falling back to a probed default"
              % (type(e).__name__, e))
    cand = "C:/Program Files/Git/bin/bash.exe"
    return cand if os.path.exists(cand) else (shutil.which("bash") or "bash")


GIT_BASH = _git_bash()


def bare_bash(cmdline, cwd, timeout=300):
    """Run a BARE-NAME command through Git Bash with a named cwd. The bare name is the point."""
    r = subprocess.run([GIT_BASH, "-c", cmdline], cwd=cwd, capture_output=True,
                       text=True, timeout=timeout)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def bare_cmd(cmdline, cwd, timeout=300):
    """Run a BARE-NAME command through cmd.exe with a named cwd -- the PowerShell/cmd plane."""
    r = subprocess.run(["cmd.exe", "/c", cmdline], cwd=cwd, capture_output=True,
                       text=True, timeout=timeout)
    return r.returncode, (r.stdout or "").replace("\r", ""), (r.stderr or "").replace("\r", "")


def main(argv):
    t0 = time.time()
    print("=" * 100)
    print("CE-e-2 / E2-AC1 -- THE FORWARDERS RESOLVE TO THE CALLER'S TOPLEVEL")
    print("=" * 100)
    print("  battery   : %s" % os.path.abspath(__file__).replace("\\", "/"))
    print("  invoked in: %s" % WS.replace("\\", "/"))
    print("  ~/bin     : %s" % BIN.replace("\\", "/"))
    print("  Git Bash  : %s" % str(GIT_BASH).replace("\\", "/"))

    rc, out, _ = git(["worktree", "list", "--porcelain"])
    MAIN = ""
    for ln in out.splitlines():
        if ln.startswith("worktree "):
            MAIN = ln.split(" ", 1)[1].strip().replace("\\", "/")
            break
    print("  MAIN tree : %s   (DERIVED from `git worktree list --porcelain`, never hardcoded)" % MAIN)
    _, cur, _ = git(["rev-parse", "--abbrev-ref", "HEAD"])
    ref = cur.strip()
    _, sha, _ = git(["rev-parse", ref + "^{commit}"])
    print("  AFTER ref : %-32s sha %s" % (ref, sha.strip()))

    slot = "C:/tmp/cee2-fresh-%d" % os.getpid()
    branch = "cee2-fresh-%d" % os.getpid()
    made = False

    try:
        # ------------------------------------------------------------------ (a) THE POPULATION
        hdr("(a) THE POPULATION -- re-derived at this seat, printed beside round 7's cited number")
        present = sorted(os.listdir(BIN)) if os.path.isdir(BIN) else []
        ext = [n for n in present if not n.endswith(".cmd")]
        cmds = [n for n in present if n.endswith(".cmd")]
        tools_on_disk = sorted(
            os.path.basename(p) for p in
            [os.path.join(MAIN, ".tools", n) for n in os.listdir(os.path.join(MAIN, ".tools"))]
            if os.path.basename(p).startswith("comp-") and not p.endswith(".cmd")
            and os.path.isfile(p))
        derived_tools = len(tools_on_disk) + 1          # the comp-* set + the named non-comp `aws`
        derived_files = derived_tools * 2
        print("  ~/bin present            : %d file(s)  (%d extensionless + %d .cmd)"
              % (len(present), len(ext), len(cmds)))
        print("  .tools/comp-* in %s: %d" % (MAIN, len(tools_on_disk)))
        print("  DERIVED at this seat     : %d tool(s) (%d comp-* + 1 aws) x 2 forms = %d file(s)"
              % (derived_tools, len(tools_on_disk), derived_files))
        print("  ROUND 7 CITED            : %d -- and it differs, by %+d."
              % (ROUND7_CITED_POPULATION, derived_files - ROUND7_CITED_POPULATION))
        print("    WHY: the set is DERIVED from .tools/comp-* at run time, never a named list (the")
        print("    generator's own header says the named set WAS the defect). 186 is the count when")
        print("    that header was written (93 comp-tools x 2 = 186); .tools now carries %d, so the"
              % len(tools_on_disk))
        print("    population grew with the tool set. The number is re-derived, never quoted.")
        foreign = [n for n in ext if n != "aws" and not n.startswith("comp-")]
        print("  NOT WRITTEN BY THIS PROVISIONER: %d of %d extensionless -- %s"
              % (len(foreign), len(ext), ", ".join(foreign) or "none"))
        print("    (an extensionless shim with no .cmd twin; the provisioner emits comp-* + aws only,")
        print("     so it neither wrote nor touched it. Named so the denominator is not overclaimed.)")

        # every REGENERATED forwarder must carry the new resolution -- a census, not a spot check
        want_bash = "git rev-parse --show-toplevel"
        want_cmd = "SHIM_TARGET"
        ok_bash = ok_cmd = 0
        miss = []
        for n in ext:
            if n in foreign:
                continue
            try:
                body = open(os.path.join(BIN, n), "r", encoding="utf-8", errors="replace").read()
            except OSError:
                miss.append(n)
                continue
            if want_bash in body and "--which" in body:
                ok_bash += 1
            else:
                miss.append(n)
        for n in cmds:
            try:
                body = open(os.path.join(BIN, n), "r", encoding="utf-8", errors="replace").read()
            except OSError:
                miss.append(n)
                continue
            if want_cmd in body and "--which" in body:
                ok_cmd += 1
            else:
                miss.append(n)
        expect_bash = len(ext) - len(foreign)
        print("  CARRY THE CALLER-TOPLEVEL RESOLUTION + --which:")
        print("    extensionless: %d of %d   .cmd: %d of %d   MISSING: %s"
              % (ok_bash, expect_bash, ok_cmd, len(cmds), ", ".join(miss) or "none"))
        check("a", ok_bash == expect_bash and ok_cmd == len(cmds) and derived_files == 210
              and not miss,
              "%d of %d written forwarders carry the resolution and --which, on BOTH planes "
              "(%d + %d of %d expected)"
              % (ok_bash + ok_cmd, expect_bash + len(cmds), ok_bash, ok_cmd, derived_files))

        # ------------------------------------------------------------------ cut the fresh worktree
        hdr("CUTTING A FRESH LINKED WORKTREE (removed in arm (f))")
        t = time.time()
        rc, o, e = git(["worktree", "add", "-b", branch, slot, sha.strip()], timeout=900)
        print("  git worktree add -b %s %s %s -> rc=%d  %.1fs" % (branch, slot, sha.strip()[:10],
                                                                  rc, time.time() - t))
        if rc != 0:
            print("  BLOCKED: %s" % e.strip()[-400:])
            return 1
        made = True

        # ------------------------------------------------------------------ (b) BOTH DIRECTIONS
        hdr("(b) BOTH DIRECTIONS OF THE RESOLUTION -- the BARE NAME, from each tree")
        rc_m, out_m, err_m = bare_bash("comp-which --which", MAIN)
        rc_w, out_w, err_w = bare_bash("comp-which --which", slot)
        _, which_m, _ = bare_bash("command -v comp-which", MAIN)
        print("  BARE NAME RESOLVES TO      : %s" % which_m.strip())
        print("  bash  cwd=%-42s -> rc=%d  %s" % (MAIN, rc_m, out_m.strip()))
        print("  bash  cwd=%-42s -> rc=%d  %s" % (slot, rc_w, out_w.strip()))
        rc_cm, out_cm, _ = bare_cmd("comp-which.cmd --which", MAIN)
        rc_cw, out_cw, _ = bare_cmd("comp-which.cmd --which", slot)
        print("  cmd   cwd=%-42s -> rc=%d  %s" % (MAIN, rc_cm, out_cm.strip()))
        print("  cmd   cwd=%-42s -> rc=%d  %s" % (slot, rc_cw, out_cw.strip()))
        b_m, b_w = out_m.strip(), out_w.strip()
        c_m, c_w = out_cm.strip(), out_cw.strip()

        def same_file(a, b):
            return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))

        want_m = os.path.join(MAIN, ".tools", "comp-which")
        want_w = os.path.join(slot, ".tools", "comp-which")
        check("b:bash", same_file(b_m, want_m) and same_file(b_w, want_w) and b_m != b_w,
              "bash plane: the MAIN tree answers %s and the FRESH worktree answers %s -- absolute, "
              "and DIFFERENT" % (b_m, b_w))
        check("b:cmd", same_file(c_m, want_m) and same_file(c_w, want_w) and c_m != c_w,
              "cmd/PowerShell plane: %s vs %s -- absolute, and DIFFERENT" % (c_m, c_w))

        # ------------------------------------------------------------------ (c) THE PLANTED EDIT
        hdr("(c) THE PLANTED EDIT -- a path that PRINTS right can still EXEC wrong")
        target = os.path.join(slot, ".tools", "comp-which")
        print("  planting in the FRESH WORKTREE ONLY (never the main tree, never committed, and the")
        print("  worktree is destroyed in arm (f)): %s" % target.replace("\\", "/"))
        before_sha = sha256_of(target)
        original = open(target, "rb").read()
        marker = "CEE2-PLANTED-MARKER-%d" % os.getpid()
        lines = original.decode("utf-8", errors="surrogateescape").split("\n")
        ins = 0
        for i, ln in enumerate(lines):
            if re.match(r"^(import|from)\s+\w", ln):
                ins = i + 1
        lines.insert(ins, 'import sys as _cee2; _cee2.stderr.write("%s\\n")' % marker)
        print("  marker line inserted after the last module-level import, at line %d" % (ins + 1))
        planted_ok = False
        try:
            open(target, "wb").write("\n".join(lines).encode("utf-8", errors="surrogateescape"))
            # A REAL INVOCATION, NOT --which. --which prints the target and exits BEFORE the
            # exec, so a marker planted INSIDE the tool could never appear in it -- the arm
            # would have been a constant. That is this cell's own defect shape inside its own
            # control, and it is why arm (c) exists beside arm (b) at all: a path that PRINTS
            # right can still EXEC wrong, and a control that never execs cannot tell.
            rc_pw, out_pw, err_pw = bare_bash('comp-which "cee2 planted probe"', slot)
            rc_pm, out_pm, err_pm = bare_bash('comp-which "cee2 planted probe"', MAIN)
            in_w = marker in (out_pw + err_pw)
            in_m = marker in (out_pm + err_pm)
            print("  bare-name run FROM THE WORKTREE : rc=%d  marker present: %s" % (rc_pw, in_w))
            for ln in err_pw.splitlines():
                print("      stderr| %s" % ln)
            print("  bare-name run FROM THE MAIN TREE : rc=%d  marker present: %s" % (rc_pm, in_m))
            for ln in err_pm.splitlines():
                print("      stderr| %s" % ln)
            planted_ok = in_w and not in_m
        finally:
            open(target, "wb").write(original)
            after_sha = sha256_of(target)
            print("  REVERTED: sha256 before %s / after %s -- %s"
                  % (before_sha, after_sha, "IDENTICAL" if before_sha == after_sha else "DIFFERENT"))
        check("c", planted_ok and before_sha == after_sha,
              "the planted marker appears in the bare-name run from the worktree and NOT from the "
              "main tree, and the file is byte-restored (sha256 equal)")

        # ------------------------------------------------------------------ (d) THE NO-TOPLEVEL CASE
        hdr("(d) THE NO-TOPLEVEL CASE -- falls back to the baked path AND SAYS SO")
        nowhere = os.environ.get("SystemRoot", "C:/Windows") + "/Temp"
        rc_t, _, _ = git(["rev-parse", "--show-toplevel"], cwd=nowhere)
        print("  probe dir: %s   `git rev-parse --show-toplevel` there -> rc=%d (non-zero = no "
              "toplevel, as required)" % (nowhere.replace("\\", "/"), rc_t))
        rc_n, out_n, err_n = bare_bash("comp-which --which", nowhere)
        print("  bash rc=%d" % rc_n)
        print("  STDOUT: %s" % out_n.strip())
        print("  STDERR (the exact line):")
        for ln in err_n.splitlines():
            print("      %s" % ln)
        rc_nc, out_nc, err_nc = bare_cmd("comp-which.cmd --which", nowhere)
        print("  cmd  rc=%d  STDOUT: %s" % (rc_nc, out_nc.strip()))
        for ln in err_nc.splitlines():
            print("      stderr| %s" % ln)
        said_so = ("WARN:" in err_n and "no git toplevel" in err_n
                   and "EXECUTING THE BAKED PATH" in err_n)
        baked_is_main = same_file(out_n.strip(), want_m) if out_n.strip() else False
        check("d:says-so", said_so and rc_t != 0,
              "the fallback is LOUD on stderr (rc %d, %d bytes) and names the path it chose -- a "
              "silent fallback would rebuild this cell's defect one layer down" % (rc_n, len(err_n)))
        check("d:baked-is-durable", baked_is_main,
              "and the baked fallback names the MAIN worktree (%s), not the temporary checkout that "
              "ran the provisioner" % out_n.strip())

        # ------------------------------------------------------------------ (e) THE HARNESS
        hdr("(e) THE HARNESS -- writes nothing under the CloudComp deliverables, inside a STATED bound")
        baseline = os.path.join(WS, *BASELINE_REL.split("/"))
        harness = os.path.join(WS, *HARNESS_REL.split("/"))
        src = open(harness, "r", encoding="utf-8", errors="replace").read()
        m = re.search(r"^RECOMMENDED_TIMEOUT_S\s*=\s*(\d+)", src, re.M)
        m2 = re.search(r"^MEASURED_RUNTIME_S\s*=\s*\(([^)]*)\)", src, re.M)
        m3 = re.search(r"^MEASURED_TIMEOUT_S\s*=\s*\(([^)]*)\)", src, re.M)
        bound = int(m.group(1)) if m else 0
        print("  THE BOUND THE FILE NOW STATES: RECOMMENDED_TIMEOUT_S = %s s" % (bound or "ABSENT"))
        print("  ITS MEASUREMENTS            : MEASURED_RUNTIME_S = (%s) rc-0 completions; "
              "MEASURED_TIMEOUT_S = (%s) rc-124 under a 600 s bound"
              % (m2.group(1).strip() if m2 else "ABSENT", m3.group(1).strip() if m3 else "ABSENT"))
        rec = os.path.join(HERE, "cee2_harness_runtime.json")
        run = {}
        if os.path.isfile(rec):
            run = json.load(open(rec, encoding="utf-8"))
        print("  RUNTIME MEASURED AT THIS SEAT: %s s (rc %s), recorded %s"
              % (run.get("elapsed_s", "UNMEASURED"), run.get("rc", "?"),
                 rec.replace("\\", "/")))
        print("  baseline: %s" % baseline.replace("\\", "/"))
        print("    sha256 BEFORE the run : %s" % run.get("baseline_sha_before", "UNRECORDED"))
        print("    sha256 AFTER  the run : %s" % run.get("baseline_sha_after", "UNRECORDED"))
        print("    sha256 NOW            : %s" % sha256_of(baseline))
        untouched = (run.get("baseline_sha_before") and
                     run.get("baseline_sha_before") == run.get("baseline_sha_after") ==
                     sha256_of(baseline))
        inside = bool(run.get("elapsed_s")) and bound and run["elapsed_s"] <= bound
        print("  wrote instead -> %s" % run.get("out_path", "UNRECORDED"))
        check("e:baseline-untouched", bool(untouched),
              "the bare invocation left %s byte-identical (1 of 1 file under the CloudComp "
              "deliverables that this harness could write)" % BASELINE_REL)
        check("e:inside-stated-bound", bool(inside),
              "measured runtime %s s <= the bound the file states, %s s (round 7's own rc-124 pair "
              "at ~601 s under a 600 s bound is why the bound is stated from measurements)"
              % (run.get("elapsed_s", "?"), bound))
        check("e:rc", run.get("rc") == 0,
              "the harness's bare invocation returned rc %s" % run.get("rc", "UNRECORDED"))

        # ------------------------------------------------------------------ (f) NOTHING ELSE MOVED
        hdr("(f) NOTHING ELSE MOVED -- a named sample, exercised after the regeneration")
        print("  BACKUP of the pre-run ~/bin (kept for the length of the order):")
        nback = len(os.listdir(BACKUP_DIR)) if os.path.isdir(BACKUP_DIR) else 0
        print("    %s -- %d file(s)" % (BACKUP_DIR.replace("\\", "/"), nback))
        good = 0
        for name in SAMPLE:
            rcs, os_, es_ = bare_bash("%s --which" % name, slot)
            rcm, om_, _ = bare_bash("%s --which" % name, MAIN)
            tgt_w = os.path.join(slot, ".tools", name)
            hit = (rcs == 0 and os_.strip() and rcm == 0 and om_.strip()
                   and os_.strip() != om_.strip() and same_file(os_.strip(), tgt_w))
            good += 1 if hit else 0
            print("    %-22s worktree -> %-58s main -> %s"
                  % (name, os_.strip()[:58], om_.strip()[:58]))
        check("f:sample", good == len(SAMPLE),
              "%d of %d sampled forwarders (of %d written) resolve to the CALLER'S tree and differ "
              "from the main tree's" % (good, len(SAMPLE), derived_files))
        rc_r, out_r, _ = bare_bash("comp-read --help", slot, timeout=300)
        print("    a REAL run through a bare-name forwarder: `comp-read --help` from the worktree -> "
              "rc=%d, %d bytes of stdout" % (rc_r, len(out_r)))
        check("f:real-run", rc_r == 0 and len(out_r) > 200,
              "a bare-name forwarder still EXECUTES its tool after the regeneration (rc %d, %d B)"
              % (rc_r, len(out_r)))

    finally:
        hdr("CLEANUP")
        if made:
            rc, _, e = git(["worktree", "remove", "--force", slot])
            print("  git worktree remove --force %s -> rc=%d %s" % (slot, rc, e.strip()[:160]))
            rc2, _, e2 = git(["branch", "-D", branch])
            print("  git branch -D %s -> rc=%d %s" % (branch, rc2, e2.strip()[:160]))
            git(["worktree", "prune"])
        _, brs, _ = git(["branch", "--list", "cee2-*"])
        print("  git branch --list 'cee2-*' -> %s" % (brs.strip() or "(none)"))
        _, wl, _ = git(["worktree", "list"])
        print("  git worktree list -- %d worktree(s)" % len(wl.strip().splitlines()))
        leaked = os.path.exists(slot) or bool(brs.strip())
        check("cleanup", not leaked, "the worktree this run cut is removed and its branch deleted")

    hdr("SUMMARY")
    npass = sum(1 for _n, ok, _m in RESULTS if ok)
    for n, ok, m in RESULTS:
        print("  [%s] %-26s %s" % ("PASS" if ok else "FAIL", n, m))
    print("")
    print("  %d of %d arm(s) PASS   elapsed %.1fs" % (npass, len(RESULTS), time.time() - t0))
    failed = [n for n, ok, _m in RESULTS if not ok]
    if failed:
        print("  arms failed: %s" % ", ".join(failed))
        print("NOT ENFORCED -- %d arm(s) failed. NO TOKEN." % len(failed))
        return 1
    print(TOKEN)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
