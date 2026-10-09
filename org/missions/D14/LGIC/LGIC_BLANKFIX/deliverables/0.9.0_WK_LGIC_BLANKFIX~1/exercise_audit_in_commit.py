#!/usr/bin/env python3
"""exercise_audit_in_commit -- the placement override's audit row is committed in the commit it permits (LGIC_BLANKFIX BF-y-1).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/exercise_audit_in_commit.py

ADJUSTED BY BF-y-2 (the arms the binding legitimately changes): C2 now expects msg_sha256 = the sha256 of the message file the arm
wrote (was empty); C9 and C10 hand the gate the message (--message-file) and their hand-written row carries that message's hash
(the control is unchanged: row on disk only -> IGNORED; the same row staged -> OVERRIDDEN). Every other arm is unchanged.

WHAT RUNS. The way exercise_override.py (BF-x-4) runs, and nothing in the repository is written. Each arm builds its own temporary
git repository (outside the repository) from byte copies of .tools/naming-gate.py, .tools/naming-apply-gate.py, lib/*.py
(lib/opal_naming_rootcheck.py replaced by the BF-x-3 recorder: FIX for the hand-built name "irpt-directory-newjob", RIGHT for any
other), the registry json, and a baseline commit that already holds one earlier override row in
org/audit/naming-place-override-audit.jsonl. The REAL naming stage of .tools/safe-commit.sh (from its `if [ -n "$IN_SCOPE" ]` line to
the line before the LAYER 2 banner, which holds the override reader and the audit writer) is cut out and run in bash under
`set -euo pipefail` with SCRIPT_DIR pointed at the temporary tree; it is followed by the LANDING line, the same call safe-commit.sh
makes last: `git commit --only <the -F args> -- "${PATHSPEC[@]}"` -- so the pathspec the cut leaves behind (which the override
block extends with the audit file) is what lands. The exercise asserts that the real script still carries that landing line. The
placement switch exists in the temporary trees only; the repository's own switch file is read (hash) before and after, never
touched. The commits are READ BACK: `git show --stat` and the blob at the landed commit.

ARMS (placement switch PRESENT in the temporary tree, the older switch ABSENT):
  C1  override line, a name the canon cannot place       -> lands; `git show --stat` of the landed commit lists the audit file AND
                                                           the .tf; the committed file = the seed row + exactly one new row
  C2  the row's shape as built                           -> keys utc, author, id, reason, names, msg_sha256 (sha256 of the message); names holds the name
  C3  C1's id against the gate's OVERRIDDEN line         -> the output carries `NAMING OVERRIDDEN` and `OVERRIDDEN (audited, id <the row's id>)`
  C4  C1's tree afterwards                               -> the audit file on disk = the committed blob (clean); no .log file written
  C5  the SAME name, NO override line (difference control) -> refused (rc=1), nothing lands, the audit file's disk, index and HEAD bytes
                                                           are those of the seed (untouched)
  C6  override line, a name the older limb REFUSES too (older switch ON) -> refused, and the attempt leaves no row behind (disk, index)
  C7  a commit with no override line and nothing refused -> lands; its `git show --stat` does NOT list the audit file; file unchanged
  C8  override line, but nothing refused                 -> lands without an audit row (nothing was refused, nothing is audited)
  C9  the gate run directly, row on disk but NOT staged  -> rc=1, IGNORED (the index copy holds the seed only: the row honoured is the one that will land)
  C10 the same row once staged (control of C9)           -> rc=0, OVERRIDDEN
  C11 the repository afterwards                          -> its switch file and its audit file hold the bytes they held before;
                                                           no .log; no scratch tree
One line per arm: expected and got. Last line, printed once: AUDIT-IN-COMMIT ok=<bool> arms=<n> held=<n>
Python 3.9; ASCII only; standard library only.
"""
import datetime
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "0.9.0_WK_LGIC_BLANKFIX~2"))
import exercise_switch_on as sw  # noqa: E402  (the BF-x-3 harness: tree builder, cutter, switch setter)

ROOT = sw.ROOT
SAFE_COMMIT = sw.SAFE_COMMIT
TF_REL = sw.TF_REL
BAD_NAME = sw.BAD_NAME
OLD_REFUSE_NAME = sw.OLD_REFUSE_NAME
BASE_TF = sw.BASE_TF
BLOCK = sw.BLOCK
GOOD_NAME = "irpt-directory-fine-daily"  # the recorder answers RIGHT
AUTHOR = "0.9.0_WK_LGIC_BLANKFIX~1"
REASON = "the canon has no row for this creator yet"
AUDIT_REL = "org/audit/naming-place-override-audit.jsonl"
LOG_REL = "org/naming-place-override-audit.log"
LANDING = 'git -c user.name=ex -c user.email=ex@example.invalid commit --only "${COMMIT_ARGS[@]}" -- "${PATHSPEC[@]}"'
KEYS = ["utc", "author", "id", "reason", "names", "msg_sha256"]
REPO_SWITCH = os.path.join(ROOT, "org", "mcp", "naming-place.enforce")
REPO_AUDIT = os.path.join(ROOT, *AUDIT_REL.split("/"))
REPO_LOG = os.path.join(ROOT, *LOG_REL.split("/"))


def sha_of(path):
    if not os.path.exists(path):
        return "absent"
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def gitq(t, *args):
    """git in tree t; (rc, text) -- never raises."""
    p = subprocess.run(["git"] + list(args), cwd=t, capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def seed_row():
    return json.dumps({"utc": "2026-10-01T00:00:00Z", "author": "seed <seed@opal.agent>", "id": "seed-id", "reason": "an earlier override",
                       "names": ["irpt-seed-name"], "msg_sha256": ""}, separators=(",", ":")) + "\n"


def seeded_tree(td, name):
    """A tree whose baseline commit holds the repo plus one earlier audit row (a second commit on the sw baseline)."""
    t = sw.build_tree(td, name)
    sw.write(os.path.join(t, *AUDIT_REL.split("/")), seed_row())
    gitq(t, "add", "-f", "--", AUDIT_REL)
    rc, out = gitq(t, "-c", "user.name=ex", "-c", "user.email=ex@example.invalid", "commit", "-q", "-m", "seed", "--", AUDIT_REL)
    if rc != 0:
        raise RuntimeError("seed commit failed: " + out[:200])
    return t


def commit_limb(t, names, message, older_on, place_on=True):
    """Stage a .tf that adds a resource per name in `names`, run safe-commit.sh's real naming stage, then the landing line.
    (rc, text); 'LANDED' in text when the commit landed."""
    sw.set_switch(t, "naming-gate.enforce", older_on)
    sw.set_switch(t, "naming-place.enforce", place_on)
    sw.write(os.path.join(t, TF_REL), BASE_TF + "".join(BLOCK % n for n in names))
    gitq(t, "add", "--", TF_REL)  # safe-commit.sh stages the declared pathspec before its naming stage
    msgfile = os.path.join(t, "msg.txt")
    sw.write(msgfile, message)
    body = sw.cut(SAFE_COMMIT, 'if [ -n "$IN_SCOPE" ] && [ -f "$SCRIPT_DIR/naming-gate.py" ]; then',
                  "# LAYER 2 of the CANONICAL FABRIC WORKFLOW")
    script = ('set -euo pipefail\nSCRIPT_DIR="%s"\nIN_SCOPE="%s"\nPATHSPEC=("%s")\nCOMMIT_ARGS=(--author "%s <%s@opal.agent>" -F "%s")\n'
              'AGENT="%s"\nISO_TS="$(date -u +%%Y-%%m-%%dT%%H:%%M:%%SZ)"\n%s\n%s\necho LANDED\n') % (
        sw.fwd(os.path.join(t, ".tools")), TF_REL, TF_REL, AUTHOR, AUTHOR, sw.fwd(msgfile), AUTHOR, body, LANDING)
    rc, out = sw.run_bash(script, t)
    return rc, out


def gate_direct(t, name, env, message=None):
    """Run the gate itself over the staged .tf addition (no safe-commit). `message` (BF-y-2): the text handed as --message-file.
    (rc, text)."""
    sw.set_switch(t, "naming-gate.enforce", False)
    sw.set_switch(t, "naming-place.enforce", True)
    sw.write(os.path.join(t, TF_REL), BASE_TF + BLOCK % name)
    gitq(t, "add", "--", TF_REL)
    rc, diff = gitq(t, "diff", "--cached", "--no-color", "--no-ext-diff", "--", TF_REL)
    dfile = os.path.join(t, "gate.diff")
    sw.write(dfile, diff + "\n")
    e = dict(os.environ)
    for k in ("NAMING_GATE_ENFORCE", "NAMING_PLACE_PREVIEW", "NAMING_PLACE_OVERRIDE"):
        e.pop(k, None)
    e["OPAL_AGENT_SERIAL"] = AUTHOR
    e["STUB_REC"] = os.path.join(t, "stub.rec")
    e.update(env)
    cmd = [sys.executable, os.path.join(t, ".tools", "naming-gate.py"), "--diff", dfile, "--post-from-index"]
    if message is not None:
        mfile = os.path.join(t, "gate.msg")
        with open(mfile, "wb") as fh:
            fh.write(message.encode("utf-8"))
        cmd += ["--message-file", mfile]
    p = subprocess.run(cmd, cwd=t, env=e, capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def landed_stat(t):
    return gitq(t, "show", "--stat", "--format=%H", "-1", "HEAD")[1]


def head_of(t):
    return gitq(t, "rev-parse", "HEAD")[1].strip()


def audit_blob(t, rev):
    rc, out = gitq(t, "show", "%s:%s" % (rev, AUDIT_REL))
    return out if rc == 0 else None


def index_blob(t):
    rc, out = gitq(t, "show", ":" + AUDIT_REL)
    return out if rc == 0 else None


def parse_rows(text):
    rows = []
    for ln in (text or "").splitlines():
        try:
            rows.append(json.loads(ln))
        except ValueError:
            rows.append(None)
    return rows


def main():
    arms = []

    def arm(label, expected, got, held):
        arms.append((label, expected, got, bool(held)))

    pre = {"switch": sha_of(REPO_SWITCH), "audit": sha_of(REPO_AUDIT), "log": sha_of(REPO_LOG)}
    pre_tmp = set(n for n in os.listdir(tempfile.gettempdir()) if n.startswith("bfy1_audit_"))
    td = tempfile.mkdtemp(prefix="bfy1_audit_")
    line = "# naming-place-override: %s\n" % REASON
    base_msg = "build(x): a creator\n\nbody\n"
    try:
        with open(SAFE_COMMIT, "r", encoding="utf-8", errors="replace") as fh:
            sc_text = fh.read()
        landing_real = "git commit --only \"${COMMIT_ARGS[@]}\" -- \"${PATHSPEC[@]}\"" in sc_text

        # ---- C1..C4: the overridden commit
        t = seeded_tree(td, "t1")
        seed_sha = sha_of(os.path.join(t, *AUDIT_REL.split("/")))
        head0 = head_of(t)
        rc, out = commit_limb(t, [BAD_NAME], base_msg + line, False)
        head1 = head_of(t)
        stat1 = landed_stat(t)
        blob1 = audit_blob(t, "HEAD")
        rows1 = parse_rows(blob1)
        arm("C1 override line, a name the canon cannot place",
            "rc=0 landed, the commit's --stat lists the audit file and the .tf, file = seed row + one new row",
            "rc=%d %s, new commit=%s, stat lists audit=%s tf=%s, rows in committed file=%d" % (
                rc, "landed" if "LANDED" in out else "not landed", head1 != head0, AUDIT_REL in stat1, TF_REL in stat1, len(rows1)),
            landing_real and rc == 0 and "LANDED" in out and head1 != head0 and AUDIT_REL in stat1 and TF_REL in stat1
            and len(rows1) == 2 and rows1[0] is not None and rows1[0].get("id") == "seed-id" and rows1[1] is not None)
        row = rows1[1] if len(rows1) == 2 and rows1[1] else {}
        want_sha = hashlib.sha256((base_msg + line).encode("utf-8")).hexdigest()
        arm("C2 the row's shape as built (BF-y-2: msg_sha256 = sha256 of the message file)",
            "keys %s in that order; msg_sha256 = %s; names holds %s; author %s" % (KEYS, want_sha, BAD_NAME, AUTHOR),
            "keys %s; msg_sha256=%r; names=%r; author=%r" % (list(row.keys()), row.get("msg_sha256"), row.get("names"), row.get("author")),
            list(row.keys()) == KEYS and row.get("msg_sha256") == want_sha and row.get("names") == [BAD_NAME]
            and row.get("author") == AUTHOR and row.get("reason") == REASON and str(row.get("utc", "")).endswith("Z"))
        rid = row.get("id", "")
        arm("C3 the row's id against the gate's OVERRIDDEN line",
            "the output carries `NAMING OVERRIDDEN` and `OVERRIDDEN (audited, id <the row's id>)`",
            "NAMING OVERRIDDEN %s; id %r in the WARN line: %s" % ("printed" if "NAMING OVERRIDDEN " in out else "absent", rid,
                                                                 "yes" if rid and ("OVERRIDDEN (audited, id %s)" % rid) in out else "no"),
            "NAMING OVERRIDDEN " in out and bool(rid) and ("OVERRIDDEN (audited, id %s)" % rid) in out)
        disk = sha_of(os.path.join(t, *AUDIT_REL.split("/")))
        st_rc, st = gitq(t, "status", "--porcelain", "--", AUDIT_REL)
        arm("C4 the overridden commit's tree afterwards", "the audit file on disk = the committed blob, status clean, no .log file",
            "disk=%s blob=%s, status=%r, log file %s" % ("same" if disk == hashlib.sha256((blob1 or "").encode("utf-8")).hexdigest()
                                                          else "differs", "read" if blob1 else "none", st.strip(),
                                                          "present" if os.path.exists(os.path.join(t, LOG_REL)) else "absent"),
            disk == hashlib.sha256((blob1 or "").encode("utf-8")).hexdigest() and st.strip() == ""
            and not os.path.exists(os.path.join(t, LOG_REL)))

        # ---- C5: the difference control, same name, no line
        t = seeded_tree(td, "t2")
        head0 = head_of(t)
        rc, out = commit_limb(t, [BAD_NAME], base_msg, False)
        a_disk = sha_of(os.path.join(t, *AUDIT_REL.split("/")))
        a_idx = index_blob(t)
        arm("C5 the SAME name, no override line (difference control of C1)",
            "rc=1 refused, nothing lands, audit file bytes (disk, index, HEAD) = the seed",
            "rc=%d %s, new commit=%s, audit disk %s, index %s, HEAD %s" % (
                rc, "landed" if "LANDED" in out else "refused", head_of(t) != head0, "= seed" if a_disk == seed_sha else "CHANGED",
                "= seed" if a_idx == seed_row() else "CHANGED", "= seed" if audit_blob(t, "HEAD") == seed_row() else "CHANGED"),
            rc == 1 and "LANDED" not in out and "NAMING-PLACE: REFUSE" in out and head_of(t) == head0 and a_disk == seed_sha
            and a_idx == seed_row() and audit_blob(t, "HEAD") == seed_row())

        # ---- C6: an override that cannot carry the commit (older limb refuses too) leaves no row
        t = seeded_tree(td, "t3")
        head0 = head_of(t)
        rc, out = commit_limb(t, [BAD_NAME, OLD_REFUSE_NAME], base_msg + line, True)
        a_disk = sha_of(os.path.join(t, *AUDIT_REL.split("/")))
        a_idx = index_blob(t)
        arm("C6 override line, the older limb refuses a second name (older switch ON)",
            "rc=1 refused, nothing lands, no row left behind (disk, index = the seed)",
            "rc=%d %s, new commit=%s, audit disk %s, index %s" % (rc, "landed" if "LANDED" in out else "refused", head_of(t) != head0,
                                                                  "= seed" if a_disk == seed_sha else "CHANGED",
                                                                  "= seed" if a_idx == seed_row() else "CHANGED"),
            rc == 1 and "LANDED" not in out and head_of(t) == head0 and a_disk == seed_sha and a_idx == seed_row())

        # ---- C7 / C8: nothing refused
        t = seeded_tree(td, "t4")
        head0 = head_of(t)
        rc, out = commit_limb(t, [GOOD_NAME], base_msg, False)
        st7 = landed_stat(t)
        arm("C7 no override line, nothing refused", "rc=0 landed, --stat does not list the audit file, file = the seed",
            "rc=%d %s, stat lists audit=%s, audit disk %s" % (rc, "landed" if "LANDED" in out else "not landed", AUDIT_REL in st7,
                                                              "= seed" if sha_of(os.path.join(t, *AUDIT_REL.split("/"))) == seed_sha
                                                              else "CHANGED"),
            rc == 0 and "LANDED" in out and head_of(t) != head0 and AUDIT_REL not in st7 and TF_REL in st7
            and sha_of(os.path.join(t, *AUDIT_REL.split("/"))) == seed_sha)
        t = seeded_tree(td, "t5")
        head0 = head_of(t)
        rc, out = commit_limb(t, [GOOD_NAME], base_msg + line, False)
        st8 = landed_stat(t)
        arm("C8 override line, nothing refused", "rc=0 landed, no audit row (nothing was refused), file = the seed",
            "rc=%d %s, stat lists audit=%s, audit disk %s" % (rc, "landed" if "LANDED" in out else "not landed", AUDIT_REL in st8,
                                                              "= seed" if sha_of(os.path.join(t, *AUDIT_REL.split("/"))) == seed_sha
                                                              else "CHANGED"),
            rc == 0 and "LANDED" in out and head_of(t) != head0 and AUDIT_REL not in st8
            and sha_of(os.path.join(t, *AUDIT_REL.split("/"))) == seed_sha)

        # ---- C9 / C10: the gate reads the index
        t = seeded_tree(td, "t6")
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        hand_msg = base_msg + line
        hand = json.dumps({"utc": now, "author": AUTHOR, "id": "hand-row", "reason": REASON, "names": [BAD_NAME],
                           "msg_sha256": hashlib.sha256(hand_msg.encode("utf-8")).hexdigest()},
                          separators=(",", ":")) + "\n"
        p = os.path.join(t, *AUDIT_REL.split("/"))
        with open(p, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(hand)
        rc9, out9 = gate_direct(t, BAD_NAME, {"NAMING_PLACE_OVERRIDE": "hand-row"}, hand_msg)
        arm("C9 the gate directly: the row is on disk and not staged", "rc=1, IGNORED 'no audit row has id' (the index copy holds the seed only), NAMING-PLACE line",
            "rc=%d, IGNORED %s, no-row-in-index %s, NAMING-PLACE %s" % (
                rc9, "printed" if "NAMING-PLACE-OVERRIDE: IGNORED" in out9 else "absent",
                "yes" if "no audit row has id hand-row" in out9 else "no",
                "printed" if "NAMING-PLACE: REFUSE" in out9 else "absent"),
            rc9 == 1 and "NAMING-PLACE-OVERRIDE: IGNORED" in out9 and "no audit row has id hand-row" in out9 and "NAMING-PLACE: REFUSE" in out9)
        # stage the file: the hand row now rides the index copy the gate reads
        gitq(t, "add", "-f", "--", AUDIT_REL)
        rc10, out10 = gate_direct(t, BAD_NAME, {"NAMING_PLACE_OVERRIDE": "hand-row"}, hand_msg)
        arm("C10 the same row once staged (control of C9)", "rc=0, OVERRIDDEN printed",
            "rc=%d, OVERRIDDEN %s" % (rc10, "printed" if "NAMING OVERRIDDEN " in out10 else "absent"),
            rc10 == 0 and "NAMING OVERRIDDEN " in out10)
    finally:
        def _onerr(func, path, _exc):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except OSError:
                pass
        shutil.rmtree(td, onerror=_onerr)
    post_tmp = set(n for n in os.listdir(tempfile.gettempdir()) if n.startswith("bfy1_audit_"))
    post = {"switch": sha_of(REPO_SWITCH), "audit": sha_of(REPO_AUDIT), "log": sha_of(REPO_LOG)}
    arm("C11 the repository afterwards", "switch file, audit file and .log file hold the bytes they held before; no scratch tree left",
        "switch %s, audit %s, log %s, scratch trees left=%d" % ("same" if post["switch"] == pre["switch"] else "CHANGED",
                                                              "same" if post["audit"] == pre["audit"] else "CHANGED",
                                                              "same" if post["log"] == pre["log"] else "CHANGED", len(post_tmp - pre_tmp)),
        post == pre and post_tmp == pre_tmp)
    held = 0
    for label, expected, got, ok in arms:
        held += 1 if ok else 0
        print("ARM %s | expected: %s | got: %s | %s" % (label, expected, got, "ok" if ok else "FAIL"))
    print("AUDIT-IN-COMMIT ok=%s arms=%d held=%d" % (held == len(arms), len(arms), held))
    return 0 if held == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
