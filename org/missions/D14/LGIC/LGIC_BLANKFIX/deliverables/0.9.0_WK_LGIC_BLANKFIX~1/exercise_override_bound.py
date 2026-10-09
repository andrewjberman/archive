#!/usr/bin/env python3
"""exercise_override_bound -- the placement override is bound to the commit message (LGIC_BLANKFIX BF-y-2; forge hazard of BF-x-4).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/exercise_override_bound.py

THE BINDING UNDER TEST. .tools/safe-commit.sh writes the exact message it commits (the -F file's bytes, or the -m texts joined by a
blank line) to a temporary file, writes sha256 of that file as the audit row's msg_sha256, stages the row into the commit, and hands
the gate the same file by `--message-file`. .tools/naming-gate.py override_valid passes a refused name only when the STAGED row for
the exported id has a non-empty reason, its msg_sha256 equals the sha256 of the message file the gate is handed, and that message
carries a non-empty `# naming-place-override:` line. The 600 s age window is retired.

WHAT RUNS. The way exercise_audit_in_commit.py (BF-y-1) runs, and nothing in the repository is written: each arm builds its own
temporary git repository (outside the repository) from byte copies of .tools/naming-gate.py, .tools/naming-apply-gate.py, lib/*.py
(lib/opal_naming_rootcheck.py replaced by the BF-x-3 recorder: FIX for the hand-built name "irpt-directory-newjob"), the registry
json, and a baseline commit holding one earlier override row. The REAL naming stage of .tools/safe-commit.sh (from its
`if [ -n "$IN_SCOPE" ]` line to the line before the LAYER 2 banner) is cut out and run in bash under `set -euo pipefail` with
SCRIPT_DIR pointed at the temporary tree, followed by the LANDING line safe-commit.sh makes last. The gate arms run
.tools/naming-gate.py (the copy) directly over a staged .tf addition. The placement switch exists in the temporary trees only; the
repository's switch file and audit file are hashed before and after.

ARMS (placement switch PRESENT in the temporary tree, the older switch ABSENT):
  B1  a real override (-F message with the line)             -> lands; the committed row's msg_sha256 = sha256 of the message bytes
  B2  the -m form: two -m texts, the second with the line   -> lands; msg_sha256 = sha256 of the texts joined by a blank line
  B3  FORGED row (valid-looking: fresh, right id, right name, the hash of a DIFFERENT message), gate direct, message with the line
                                                              -> rc=1, IGNORED 'bound to a different message' (the negative arm)
  B4  the same row text with ONLY the hash corrected (difference control of B3) -> rc=0, OVERRIDDEN
  B5  right hash, message WITHOUT the override line          -> rc=1, IGNORED 'no non-empty' line
  B6  right hash, message with the line but an EMPTY reason  -> rc=1, IGNORED
  B7  right hash of M, message handed is M plus one byte     -> rc=1, IGNORED (the hash binds the exact bytes)
  B8  row with an EMPTY msg_sha256, message with the line    -> rc=1, IGNORED
  B9  right row, NO message handed to the gate               -> rc=1, IGNORED
  B10 a hand-set variable (no row for its id), a matching message handed -> rc=1, IGNORED 'no audit row'
  B11 the REAL row of B1, id set by hand on a later commit of the same name whose message differs and has NO line (replay)
                                                              -> refused (rc=1), nothing lands, no new row
  B12 a row written years ago with the right hash            -> rc=0, OVERRIDDEN (the 600 s window is retired; the binding is the check)
  B13 the commit message file safe-commit.sh makes           -> removed after the run (none left in TMPDIR beyond those present before)
  B14 the repository afterwards                              -> switch file and audit file hold the bytes they held before; no scratch tree
One line per arm: expected and got. Last line, printed once: OVERRIDE-BOUND ok=<bool> arms=<n> held=<n>
Python 3.9; ASCII only; standard library only.
"""
import datetime
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "0.9.0_WK_LGIC_BLANKFIX~2"))
import exercise_audit_in_commit as ac  # noqa: E402  (the BF-y-1 harness)
import exercise_switch_on as sw  # noqa: E402  (the BF-x-3 harness)

ROOT = sw.ROOT
SAFE_COMMIT = sw.SAFE_COMMIT
TF_REL = sw.TF_REL
BAD_NAME = sw.BAD_NAME
BASE_TF = sw.BASE_TF
BLOCK = sw.BLOCK
AUTHOR = "0.9.0_WK_LGIC_BLANKFIX~1"
REASON = "the canon has no row for this creator yet"
AUDIT_REL = ac.AUDIT_REL
LANDING = ac.LANDING
REPO_SWITCH = ac.REPO_SWITCH
REPO_AUDIT = ac.REPO_AUDIT
NL = chr(10)
TMPD = os.environ.get("TMPDIR") or tempfile.gettempdir()


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def msg_leftovers():
    try:
        return set(n for n in os.listdir(TMPD) if n.startswith("naming-place-msg."))
    except OSError:
        return set()


def limb(t, name, args_sh, files=(), scope=None, tf_text=None, env=None):
    """Stage a .tf adding `name`, write `files` ({path: text}), then run safe-commit.sh's real naming stage and the landing line with
    COMMIT_ARGS = `args_sh` (shell array text). (rc, text); 'LANDED' in text when it landed."""
    sw.set_switch(t, "naming-gate.enforce", False)
    sw.set_switch(t, "naming-place.enforce", True)
    scope = scope or TF_REL
    sw.write(os.path.join(t, *scope.split("/")), tf_text if tf_text is not None else BASE_TF + BLOCK % name)
    ac.gitq(t, "add", "--", scope)
    for path, text in files:
        sw.write(path, text)
    body = sw.cut(SAFE_COMMIT, 'if [ -n "$IN_SCOPE" ] && [ -f "$SCRIPT_DIR/naming-gate.py" ]; then',
                  "# LAYER 2 of the CANONICAL FABRIC WORKFLOW")
    script = ('set -euo pipefail\nSCRIPT_DIR="%s"\nIN_SCOPE="%s"\nPATHSPEC=("%s")\nCOMMIT_ARGS=(--author "%s <%s@opal.agent>" %s)\n'
              'AGENT="%s"\nISO_TS="$(date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ)"\n%s\n%s\necho LANDED\n') % (
        sw.fwd(os.path.join(t, ".tools")), scope, scope, AUTHOR, AUTHOR, args_sh, AUTHOR, body, LANDING)
    return sw.run_bash(script, t, env)


def put_row(t, ident, digest, when="2026-10-09T00:00:00Z", reason=REASON, names=(BAD_NAME,)):
    """Append one audit row to the tree's audit file (disk) and STAGE it: the gate reads the index copy."""
    row = json.dumps({"utc": when, "author": AUTHOR, "id": ident, "reason": reason, "names": list(names), "msg_sha256": digest},
                     separators=(",", ":")) + "\n"
    p = os.path.join(t, *AUDIT_REL.split("/"))
    with open(p, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(row)
    ac.gitq(t, "add", "-f", "--", AUDIT_REL)


def rows_of(text):
    return [r for r in ac.parse_rows(text) if r is not None]


def main():
    arms = []

    def arm(label, expected, got, held):
        arms.append((label, expected, got, bool(held)))

    pre = {"switch": ac.sha_of(REPO_SWITCH), "audit": ac.sha_of(REPO_AUDIT)}
    pre_tmp = set(n for n in os.listdir(tempfile.gettempdir()) if n.startswith("bfy2_bound_"))
    pre_msg = msg_leftovers()
    td = tempfile.mkdtemp(prefix="bfy2_bound_")
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = "# naming-place-override: %s\n" % REASON
    msg_m = "build(x): a creator\n\nbody\n" + line
    msg_other = "build(x): ANOTHER commit\n\nother body\n" + line
    try:
        # ---- B1: a real override through the real stage (-F)
        t = ac.seeded_tree(td, "t1")
        mf = os.path.join(t, "msg.txt")
        rc, out = limb(t, BAD_NAME, '-F "%s"' % sw.fwd(mf), [(mf, msg_m)])
        blob = ac.audit_blob(t, "HEAD")
        rows = rows_of(blob)
        real = rows[-1] if rows else {}
        arm("B1 a real override (-F message with the line)",
            "rc=0 landed, NAMING OVERRIDDEN, committed file = seed + one row, row msg_sha256 = %s" % sha(msg_m),
            "rc=%d %s, OVERRIDDEN %s, rows=%d, row msg_sha256=%s" % (rc, "landed" if "LANDED" in out else "not landed",
                                                                    "printed" if "NAMING OVERRIDDEN " in out else "absent",
                                                                    len(rows), real.get("msg_sha256")),
            rc == 0 and "LANDED" in out and "NAMING OVERRIDDEN " in out and len(rows) == 2 and real.get("msg_sha256") == sha(msg_m))
        real_id = real.get("id", "")

        # ---- B11 (same tree, after B1): replay the real row's id by hand on a later commit with another message and no line
        head_b1 = ac.head_of(t)
        rows_before = len(rows_of(ac.index_blob(t)))
        extra_rel = "infra/aws/terraform/zz-stub-root/second.tf"  # a second file in the stub root: the same unplaceable name, new here
        mf2 = os.path.join(t, "msg2.txt")
        later = "build(x): a later commit with a different message" + NL + NL + "no override line" + NL
        rc11, out11 = limb(t, BAD_NAME, '-F "%s"' % sw.fwd(mf2), [(mf2, later)], scope=extra_rel,
                           tf_text=BASE_TF.replace('"existing"', '"existing2"') + BLOCK % BAD_NAME, env={"NAMING_PLACE_OVERRIDE": real_id})
        rows_after = len(rows_of(ac.index_blob(t)))
        arm("B11 the REAL row of B1: its id set by hand on a later commit (another message, no line)",
            "rc=1 refused (NAMING-PLACE line), nothing lands, no new row",
            "rc=%d %s, NAMING-PLACE %s, new commit=%s, rows in index %d -> %d" % (
                rc11, "landed" if "LANDED" in out11 else "refused", "printed" if "NAMING-PLACE: REFUSE" in out11 else "absent",
                ac.head_of(t) != head_b1, rows_before, rows_after),
            bool(real_id) and rc11 == 1 and "LANDED" not in out11 and "NAMING-PLACE: REFUSE" in out11 and ac.head_of(t) == head_b1
            and rows_after == rows_before)

        # ---- B2: the -m form, two texts
        t = ac.seeded_tree(td, "t2")
        m_subject, m_body = "build(x): a creator", "body\n" + line.rstrip("\n")
        rc, out = limb(t, BAD_NAME, "-m %s -m %s" % (_q(m_subject), _q(m_body)))
        rows = rows_of(ac.audit_blob(t, "HEAD"))
        want = sha(m_subject + "\n\n" + m_body)
        arm("B2 the -m form: two -m texts, the second carries the line",
            "rc=0 landed, row msg_sha256 = sha256 of the texts joined by a blank line (%s)" % want,
            "rc=%d %s, rows=%d, row msg_sha256=%s" % (rc, "landed" if "LANDED" in out else "not landed", len(rows),
                                                     rows[-1].get("msg_sha256") if rows else None),
            rc == 0 and "LANDED" in out and len(rows) == 2 and rows[-1].get("msg_sha256") == want)

        # ---- B13: the message temp file is gone
        left = msg_leftovers() - pre_msg
        arm("B13 the message file safe-commit.sh makes", "removed after the run (no new naming-place-msg.* in %s)" % TMPD,
            "new files left=%d" % len(left), not left)

        # ---- gate-direct arms, one tree
        t = ac.seeded_tree(td, "t3")

        def gate(ident, message):
            """The gate directly: message text (None = none handed). (rc, text)."""
            return ac.gate_direct(t, BAD_NAME, {"NAMING_PLACE_OVERRIDE": ident}, message)

        put_row(t, "forged", sha(msg_other), when=now)
        rc, out = gate("forged", msg_m)
        arm("B3 a FORGED row (valid-looking, fresh, right id and name, the hash of another message); message with the line",
            "rc=1, IGNORED 'bound to a different message', NAMING-PLACE line",
            "rc=%d, IGNORED %s, different-message %s, NAMING-PLACE %s" % (
                rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent",
                "yes" if "bound to a different message" in out else "no", "printed" if "NAMING-PLACE: REFUSE" in out else "absent"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out and "bound to a different message" in out
            and "NAMING-PLACE: REFUSE" in out)
        put_row(t, "right", sha(msg_m), when=now)
        rc, out = gate("right", msg_m)
        arm("B4 the same row text with ONLY the hash corrected (control of B3)", "rc=0, NAMING OVERRIDDEN printed",
            "rc=%d, OVERRIDDEN %s" % (rc, "printed" if "NAMING OVERRIDDEN " in out else "absent"), rc == 0 and "NAMING OVERRIDDEN " in out)
        msg_noline = "build(x): a creator\n\nbody, no override line\n"
        put_row(t, "noline", sha(msg_noline), when=now)
        rc, out = gate("noline", msg_noline)
        arm("B5 right hash, the message has NO override line", "rc=1, IGNORED 'no non-empty' line",
            "rc=%d, IGNORED %s, no-non-empty %s" % (rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent",
                                                    "yes" if "no non-empty" in out else "no"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out and "no non-empty" in out)
        msg_empty = "build(x): a creator\n\n# naming-place-override:   \n"
        put_row(t, "emptyreason", sha(msg_empty), when=now)
        rc, out = gate("emptyreason", msg_empty)
        arm("B6 right hash, the message line has an EMPTY reason", "rc=1, IGNORED",
            "rc=%d, IGNORED %s" % (rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out)
        put_row(t, "onebyte", sha(msg_m), when=now)
        rc, out = gate("onebyte", msg_m + " ")
        arm("B7 right hash of M, the message handed is M plus one byte", "rc=1, IGNORED 'bound to a different message'",
            "rc=%d, IGNORED %s, different-message %s" % (rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent",
                                                         "yes" if "bound to a different message" in out else "no"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out and "bound to a different message" in out)
        put_row(t, "nohash", "", when=now)
        rc, out = gate("nohash", msg_m)
        arm("B8 a row with an EMPTY msg_sha256, message with the line", "rc=1, IGNORED",
            "rc=%d, IGNORED %s" % (rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out)
        rc, out = gate("right", None)
        arm("B9 the right row, NO message handed to the gate", "rc=1, IGNORED 'no commit message was handed'",
            "rc=%d, IGNORED %s, no-message %s" % (rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent",
                                                  "yes" if "no commit message was handed" in out else "no"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out and "no commit message was handed" in out)
        rc, out = gate("no-such-id", msg_m)
        arm("B10 a hand-set variable (no row for its id), a matching message handed", "rc=1, IGNORED 'no audit row has id'",
            "rc=%d, IGNORED %s, no-row %s" % (rc, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out else "absent",
                                              "yes" if "no audit row has id no-such-id" in out else "no"),
            rc == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out and "no audit row has id no-such-id" in out)
        put_row(t, "ancient", sha(msg_m), when="2020-01-01T00:00:00Z")
        rc, out = gate("ancient", msg_m)
        arm("B12 a row dated 2020-01-01 with the right hash (the 600 s window is retired)", "rc=0, NAMING OVERRIDDEN printed",
            "rc=%d, OVERRIDDEN %s" % (rc, "printed" if "NAMING OVERRIDDEN " in out else "absent"),
            rc == 0 and "NAMING OVERRIDDEN " in out)
    finally:
        def _onerr(func, path, _exc):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except OSError:
                pass
        shutil.rmtree(td, onerror=_onerr)
    post_tmp = set(n for n in os.listdir(tempfile.gettempdir()) if n.startswith("bfy2_bound_"))
    post = {"switch": ac.sha_of(REPO_SWITCH), "audit": ac.sha_of(REPO_AUDIT)}
    arm("B14 the repository afterwards", "switch file and audit file hold the bytes they held before; no scratch tree left",
        "switch %s, audit %s, scratch trees left=%d" % ("same" if post["switch"] == pre["switch"] else "CHANGED",
                                                       "same" if post["audit"] == pre["audit"] else "CHANGED",
                                                       len(post_tmp - pre_tmp)), post == pre and post_tmp == pre_tmp)
    arms.sort(key=lambda a: int(a[0].split()[0][1:]))
    held = 0
    for label, expected, got, ok in arms:
        held += 1 if ok else 0
        print("ARM %s | expected: %s | got: %s | %s" % (label, expected, got, "ok" if ok else "FAIL"))
    print("OVERRIDE-BOUND ok=%s arms=%d held=%d" % (held == len(arms), len(arms), held))
    return 0 if held == len(arms) else 1


def _q(text):
    """Shell single-quote `text` (it carries newlines and a leading #; no single quote in the texts used)."""
    return "'" + text.replace("'", "'\"'\"'") + "'"


if __name__ == "__main__":
    sys.exit(main())
