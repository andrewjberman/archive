#!/usr/bin/env python3
"""exercise_override -- the audited override for the placement step (LGIC_BLANKFIX BF-x-4, row W1-S21).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~2/exercise_override.py

WHAT RUNS. The same way exercise_switch_on.py (BF-x-3) runs: nothing in the repository is run in place and nothing is written in
it. One temporary tree (outside the repository) holds byte copies of .tools/naming-gate.py, .tools/naming-apply-gate.py, lib/*.py
(lib/opal_naming_rootcheck.py replaced by the same recorder: it answers FIX for the hand-built name "irpt-directory-newjob" and RIGHT
for any other), the registry's json, and a git repository with one baseline commit. The REAL naming stage of .tools/safe-commit.sh
(from its `if [ -n "$IN_SCOPE" ]` line to the line before the LAYER 2 banner, which holds the override reader) is cut out and run in
bash under `set -euo pipefail` with SCRIPT_DIR pointed at the temporary tree and a commit-message file, so the switch file, the
override audit log (org/naming-place-override-audit.log) and the gate are all the temporary tree's. The placement switch is created
in the temporary tree only. The last arm reads the repository back: no switch file, no audit file and no temp file was left there.

ARMS (placement switch PRESENT in the temporary tree, older switch ABSENT, unless the arm says so):
  O1  message carries `# naming-place-override: <reason>`        -> passes; one audit line (time, author, id, reason, the name)
  O2  the same staged name, no override line (control of O1)      -> blocked, rc=1, no audit line
  O3  an override line with an empty reason                       -> blocked, no audit line
  O4  NAMING_PLACE_OVERRIDE set by hand to an id with no row      -> blocked (the commit limb), no audit line
  O5  NAMING_PLACE_OVERRIDE set by hand to O1's REAL, fresh id    -> blocked (safe-commit unsets any inherited value; it is the only setter)
  O6  the gate run directly with a hand-set variable              -> rc=1, `NAMING-PLACE-OVERRIDE: IGNORED`, the refusal stands
  O7  the gate run directly with an audit row older than the window -> rc=1, IGNORED (control of O1's pass: same row, fresh)
  O8  the gate run directly with a fresh audit row that names a different name -> rc=1 (the row covers only what it lists)
  O9  override line, placement switch ABSENT                      -> passes, and NO audit line (nothing was refused)
  O10 override line, an older-limb REFUSE, older switch ON        -> blocked by the older limb (the override is not for it)
  O11 .tools/safe-merge.sh and .tools/safe-apply.sh               -> carry no reader of the override line and no setter of the variable
  O12 the repository afterwards                                   -> no naming-place.enforce, no override audit log, no scratch tree
One line per arm: expected and got. Last line, printed once: OVERRIDE-ARMS ok=<bool> arms=<n> held=<n>
Python 3.9; ASCII only; standard library only.
"""
import datetime
import os
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exercise_switch_on as sw  # noqa: E402  (the BF-x-3 harness: tree builder, cutter, switch setter)

ROOT = sw.ROOT
SAFE_COMMIT = sw.SAFE_COMMIT
TF_REL = sw.TF_REL
BAD_NAME = sw.BAD_NAME
OLD_REFUSE_NAME = sw.OLD_REFUSE_NAME
BASE_TF = sw.BASE_TF
BLOCK = sw.BLOCK
AUTHOR = "0.9.0_WK_LGIC_BLANKFIX~2"
REASON = "the canon has no row for this creator yet"
AUDIT_REL = "org/naming-place-override-audit.log"
REPO_SWITCH = os.path.join(ROOT, "org", "mcp", "naming-place.enforce")
REPO_AUDIT = os.path.join(ROOT, "org", "naming-place-override-audit.log")


def audit_lines(t):
    p = os.path.join(t, AUDIT_REL)
    if not os.path.exists(p):
        return []
    with open(p, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def reset_audit(t):
    p = os.path.join(t, AUDIT_REL)
    if os.path.exists(p):
        os.remove(p)


def stage(t, name):
    sw.write(os.path.join(t, TF_REL), BASE_TF + BLOCK % name)
    sw.git(t, "add", "--", TF_REL)


def unstage(t):
    sw.git(t, "reset", "-q", "HEAD", "--", TF_REL)
    sw.write(os.path.join(t, TF_REL), BASE_TF)


def commit_limb(t, name, message, older_on, place_on, extra_env=None):
    """Stage a one-resource addition named `name`, then run safe-commit.sh's real naming stage with `message` as the -F file."""
    sw.set_switch(t, "naming-gate.enforce", older_on)
    sw.set_switch(t, "naming-place.enforce", place_on)
    stage(t, name)
    msgfile = os.path.join(t, "msg.txt")
    sw.write(msgfile, message)
    body = sw.cut(SAFE_COMMIT, 'if [ -n "$IN_SCOPE" ] && [ -f "$SCRIPT_DIR/naming-gate.py" ]; then',
                  "# LAYER 2 of the CANONICAL FABRIC WORKFLOW")
    script = ('set -euo pipefail\nSCRIPT_DIR="%s"\nIN_SCOPE="%s"\nCOMMIT_ARGS=(-F "%s")\nAGENT="%s"\nISO_TS="$(date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ)"\n'
              '%s\necho REACHED-END\n') % (sw.fwd(os.path.join(t, ".tools")), TF_REL, sw.fwd(msgfile), AUTHOR, body)
    rc, out = sw.run_bash(script, t, extra_env)
    unstage(t)
    return rc, out


def gate_direct(t, name, env):
    """Run the gate itself over a staged addition (no safe-commit), with `env` added. (rc, text)."""
    sw.set_switch(t, "naming-gate.enforce", False)
    sw.set_switch(t, "naming-place.enforce", True)
    stage(t, name)
    diff = sw.git(t, "diff", "--cached", "--no-color", "--no-ext-diff", "--", TF_REL)
    dfile = os.path.join(t, "gate.diff")
    sw.write(dfile, diff + "\n")
    e = dict(os.environ)
    for k in ("NAMING_GATE_ENFORCE", "NAMING_PLACE_PREVIEW", "NAMING_PLACE_OVERRIDE"):
        e.pop(k, None)
    e["OPAL_AGENT_SERIAL"] = AUTHOR
    e["STUB_REC"] = os.path.join(t, "stub.rec")
    e.update(env)
    p = subprocess.run([sys.executable, os.path.join(t, ".tools", "naming-gate.py"), "--diff", dfile, "--post-from-index"],
                       cwd=t, env=e, capture_output=True)
    unstage(t)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def write_audit(t, ident, when, reason, names):
    line = "%s NAMING-PLACE-OVERRIDE  %s  id=%s  reason=%s  names=%s\n" % (when.strftime("%Y-%m-%dT%H:%M:%SZ"), AUTHOR, ident,
                                                                          reason, names)
    p = os.path.join(t, AUDIT_REL)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(line)


def main():
    arms = []

    def arm(label, expected, got, held):
        arms.append((label, expected, got, bool(held)))

    pre_switch, pre_audit = os.path.exists(REPO_SWITCH), os.path.exists(REPO_AUDIT)
    pre_tmp = set(n for n in os.listdir(tempfile.gettempdir()) if n.startswith("bfx4_override_"))
    td = tempfile.mkdtemp(prefix="bfx4_override_")
    line = "# naming-place-override: %s\n" % REASON
    base_msg = "build(x): a creator\n\nbody\n"
    try:
        t = sw.build_tree(td, "tree")
        # O1
        rc, out = commit_limb(t, BAD_NAME, base_msg + line, False, True)
        al = audit_lines(t)
        row = al[0] if al else ""
        arm("O1 override line, switch PRESENT", "rc=0 passed, OVERRIDDEN printed, one audit line with author, reason, name",
            "rc=%d %s, OVERRIDDEN %s, audit lines=%d%s" % (rc, "passed" if "REACHED-END" in out else "blocked",
                                                         "printed" if "NAMING OVERRIDDEN " in out else "absent", len(al),
                                                         (" [" + row + "]") if row else ""),
            rc == 0 and "REACHED-END" in out and "NAMING OVERRIDDEN " in out and len(al) == 1
            and ("NAMING-PLACE-OVERRIDE  " + AUTHOR + "  id=") in row and ("reason=" + REASON) in row
            and row.endswith("names=" + BAD_NAME) and "NAMING-PLACE: REFUSE" not in out)
        o1_id = ""
        if row and "id=" in row:
            o1_id = row.split("id=", 1)[1].split("  ", 1)[0]
        # O2
        reset_audit(t)
        rc, out = commit_limb(t, BAD_NAME, base_msg, False, True)
        arm("O2 same name, no override line (control of O1)", "rc=1 blocked, NAMING-PLACE line, no audit line",
            "rc=%d %s%s, audit lines=%d" % (rc, "passed" if "REACHED-END" in out else "blocked",
                                          ", NAMING-PLACE line" if "NAMING-PLACE: REFUSE" in out else ", no placement line",
                                          len(audit_lines(t))),
            rc == 1 and "REACHED-END" not in out and "NAMING-PLACE: REFUSE" in out and not audit_lines(t))
        # O3
        rc, out = commit_limb(t, BAD_NAME, base_msg + "# naming-place-override:   \n", False, True)
        arm("O3 override line with an empty reason", "rc=1 blocked, no audit line",
            "rc=%d %s, audit lines=%d" % (rc, "passed" if "REACHED-END" in out else "blocked", len(audit_lines(t))),
            rc == 1 and "REACHED-END" not in out and not audit_lines(t))
        # O4
        rc, out = commit_limb(t, BAD_NAME, base_msg, False, True, {"NAMING_PLACE_OVERRIDE": "forged-by-hand"})
        arm("O4 variable set by hand, no row for its id, no line", "rc=1 blocked, no audit line",
            "rc=%d %s, audit lines=%d" % (rc, "passed" if "REACHED-END" in out else "blocked", len(audit_lines(t))),
            rc == 1 and "REACHED-END" not in out and not audit_lines(t))
        # O5: a real, fresh id (from O1) set by hand
        write_audit(t, "real-fresh-id", datetime.datetime.now(datetime.timezone.utc), REASON, BAD_NAME)
        n_before = len(audit_lines(t))
        rc, out = commit_limb(t, BAD_NAME, base_msg, False, True, {"NAMING_PLACE_OVERRIDE": "real-fresh-id"})
        arm("O5 variable set by hand to a REAL fresh id (O1 produced %s), no line" % (o1_id or "none"),
            "rc=1 blocked (safe-commit unsets an inherited value), no new audit line",
            "rc=%d %s, new audit lines=%d" % (rc, "passed" if "REACHED-END" in out else "blocked", len(audit_lines(t)) - n_before),
            rc == 1 and "REACHED-END" not in out and len(audit_lines(t)) == n_before and bool(o1_id))
        # O6: gate direct, hand-set variable, no row
        reset_audit(t)
        rc, out = gate_direct(t, BAD_NAME, {"NAMING_PLACE_OVERRIDE": "forged-by-hand"})
        arm("O6 the gate directly, variable set by hand", "rc=1, IGNORED printed, NAMING-PLACE line",
            "rc=%d, IGNORED %s, NAMING-PLACE %s" % (rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent",
                                                  "printed" if "NAMING-PLACE: REFUSE" in out else "absent"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out and "NAMING-PLACE: REFUSE" in out)
        # O7: a fresh row passes the gate directly (the control), an old one does not
        now = datetime.datetime.now(datetime.timezone.utc)
        write_audit(t, "fresh", now, REASON, BAD_NAME)
        rc_f, out_f = gate_direct(t, BAD_NAME, {"NAMING_PLACE_OVERRIDE": "fresh"})
        write_audit(t, "old", now - datetime.timedelta(seconds=3600), REASON, BAD_NAME)
        rc, out = gate_direct(t, BAD_NAME, {"NAMING_PLACE_OVERRIDE": "old"})
        arm("O7 the gate directly: the same audit row fresh, then an hour old", "fresh rc=0 OVERRIDDEN; old rc=1 IGNORED",
            "fresh rc=%d %s; old rc=%d %s" % (rc_f, "OVERRIDDEN" if "NAMING OVERRIDDEN " in out_f else "no OVERRIDDEN", rc,
                                              "IGNORED" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "not ignored"),
            rc_f == 0 and "NAMING OVERRIDDEN " in out_f and rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out)
        # O8: fresh row for a different name
        write_audit(t, "other", now, REASON, "some-other-name")
        rc, out = gate_direct(t, BAD_NAME, {"NAMING_PLACE_OVERRIDE": "other"})
        arm("O8 the gate directly: a fresh row that lists a different name", "rc=1 blocked, NAMING-PLACE line",
            "rc=%d, NAMING-PLACE %s" % (rc, "printed" if "NAMING-PLACE: REFUSE" in out else "absent"),
            rc == 1 and "NAMING-PLACE: REFUSE" in out)
        # O9: switch absent, line present
        reset_audit(t)
        rc, out = commit_limb(t, BAD_NAME, base_msg + line, False, False)
        arm("O9 override line, placement switch ABSENT", "rc=0 passed, no audit line (nothing was refused)",
            "rc=%d %s, audit lines=%d" % (rc, "passed" if "REACHED-END" in out else "blocked", len(audit_lines(t))),
            rc == 0 and "REACHED-END" in out and not audit_lines(t))
        # O10: older-limb REFUSE, older ON, override line
        rc, out = commit_limb(t, OLD_REFUSE_NAME, base_msg + line, True, False)
        arm("O10 override line, an older-limb REFUSE name, older switch ON", "rc=1 blocked by the older limb, no audit line",
            "rc=%d %s%s, audit lines=%d" % (rc, "passed" if "REACHED-END" in out else "blocked",
                                          ", older-limb message" if "the naming limb refused (LGIC_ENFORCE" in out else "",
                                          len(audit_lines(t))),
            rc == 1 and "REACHED-END" not in out and "the naming limb refused (LGIC_ENFORCE" in out and not audit_lines(t))
        # O11: the other scripts
        hits = []
        for rel in (".tools/safe-merge.sh", ".tools/safe-apply.sh"):
            with open(os.path.join(ROOT, rel), "r", encoding="utf-8", errors="replace") as fh:
                txt = fh.read()
            for token in ("naming-place-override", "NAMING_PLACE_OVERRIDE"):
                if token in txt:
                    hits.append("%s:%s" % (rel, token))
        arm("O11 safe-merge.sh and safe-apply.sh", "no reader of the override line, no setter of the variable",
            "tokens found: %s" % (", ".join(hits) if hits else "none"), not hits)
    finally:
        def _onerr(func, path, _exc):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except OSError:
                pass
        shutil.rmtree(td, onerror=_onerr)
    post_tmp = set(n for n in os.listdir(tempfile.gettempdir()) if n.startswith("bfx4_override_"))
    clean = (os.path.exists(REPO_SWITCH) == pre_switch and os.path.exists(REPO_AUDIT) == pre_audit and not pre_switch
             and not pre_audit and post_tmp == pre_tmp)
    arm("O12 the repository afterwards", "naming-place.enforce absent, override audit log absent, no scratch tree left",
        "switch %s, audit log %s, scratch trees left=%d" % ("present" if os.path.exists(REPO_SWITCH) else "absent",
                                                           "present" if os.path.exists(REPO_AUDIT) else "absent",
                                                           len(post_tmp - pre_tmp)), clean)
    held = 0
    for label, expected, got, ok in arms:
        held += 1 if ok else 0
        print("ARM %s | expected: %s | got: %s | %s" % (label, expected, got, "ok" if ok else "FAIL"))
    print("OVERRIDE-ARMS ok=%s arms=%d held=%d" % (held == len(arms), len(arms), held))
    return 0 if held == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
