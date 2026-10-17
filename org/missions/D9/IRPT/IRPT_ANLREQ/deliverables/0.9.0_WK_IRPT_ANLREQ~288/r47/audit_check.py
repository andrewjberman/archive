"""Checker for TO IRPT_ANLREQ.TO-AR-y-388 (cell AR-y-388): validates r47/AUDIT_b.json.

Stdlib only. Normal mode prints AUDIT-OK <n> rows <c> CLOSED <s> STANDS <l> NEEDS-LIVE-READ
only when every check passes; otherwise AUDIT-BAD <why> and exit 1.
--selftest writes a temporary copy in which every code reference of one CLOSED row points at a
path that does not exist, runs the same checks on it, prints CONTROL-FIRES only when the copy is
rejected, and removes the copy.

Reads committed bytes only: git cat-file / git show at HEAD of the repository that holds this file.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "AUDIT_b.json")

EXPECTED_IDS = [
    "IRPT_ANLREQ-D2-W128-S3", "IRPT_ANLREQ-D2-W129-S1", "IRPT_ANLREQ-D2-S100",
    "IRPT_ANLREQ-D2-W133-S1", "IRPT_ANLREQ-D2-W133-S4", "IRPT_ANLREQ-D2-W136-S2",
    "IRPT_ANLREQ-D2-W141-S1", "IRPT_ANLREQ-D2-W141-S2", "IRPT_ANLREQ-D2-W145-S1",
    "IRPT_ANLREQ-D2-W145-S5", "IRPT_ANLREQ-D2-W145-S6", "IRPT_ANLREQ-D2-W145-S8",
    "IRPT_ANLREQ-D2-W144-S1", "IRPT_ANLREQ-D2-W146-S4", "IRPT_ANLREQ-D2-W147-S2",
    "IRPT_ANLREQ-D2-W148-S1", "IRPT_ANLREQ-D2-S118", "IRPT_ANLREQ-D2-W150-S2",
    "IRPT_ANLREQ-D2-W150-S3", "IRPT_ANLREQ-D2-W155-S2", "IRPT_ANLREQ-D2-W166-S1",
]
VERDICTS = ("CLOSED", "STANDS", "NEEDS-LIVE-READ")
KINDS = ("code", "record", "commit")
DEPLOYED = ("yes", "no", "n/a", "unread")
ROW_KEYS = {"id", "verdict", "hazard", "evidence", "deployed", "reason"}
EV_KEYS = {"kind", "ref", "says"}
CODE_REF = re.compile(r"^(.+):([0-9]+)$")


def repo_root():
    r = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("AUDIT-BAD no git repository above " + HERE)
    return r.stdout.strip()


ROOT = repo_root()


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True)


def head_bytes(path):
    r = git("show", "HEAD:" + path)
    return r.stdout if r.returncode == 0 else None


def head_has(path):
    return git("cat-file", "-e", "HEAD:" + path).returncode == 0


def record_resolves(path):
    return os.path.isfile(os.path.join(ROOT, path)) or head_has(path)


def commit_resolves(sha):
    return git("cat-file", "-e", sha + "^{commit}").returncode == 0


def line_count(data):
    n = data.count(b"\n")
    if data and not data.endswith(b"\n"):
        n += 1
    return n


def check_evidence(row_id, idx, ev, errors):
    where = row_id + " evidence[" + str(idx) + "]"
    if not isinstance(ev, dict) or set(ev.keys()) != EV_KEYS:
        errors.append(where + " must carry exactly kind, ref, says")
        return None
    kind, ref, says = ev["kind"], ev["ref"], ev["says"]
    if kind not in KINDS:
        errors.append(where + " kind not in enum: " + str(kind))
        return None
    if not isinstance(says, str) or len(says) > 200 or not says:
        errors.append(where + " says must be a non-empty string of at most 200 characters")
    if not isinstance(ref, str) or not ref:
        errors.append(where + " ref must be a non-empty string")
        return kind
    if kind == "code":
        m = CODE_REF.match(ref)
        if not m:
            errors.append(where + " code ref must be path:line, got " + ref)
        else:
            path, line = m.group(1), int(m.group(2))
            data = head_bytes(path)
            if data is None:
                errors.append(where + " code path does not exist at HEAD: " + path)
            elif line < 1 or line > line_count(data):
                errors.append(where + " line " + str(line) + " beyond the " + str(line_count(data)) + " lines of " + path)
    elif kind == "record":
        if not record_resolves(ref):
            errors.append(where + " record path resolves neither on disk nor at HEAD: " + ref)
    elif kind == "commit":
        if not commit_resolves(ref):
            errors.append(where + " commit does not resolve: " + ref)
    return kind


def check(rows):
    """Return (errors, counts) for a parsed audit list."""
    errors = []
    if not isinstance(rows, list):
        return ["top level is not a list"], None
    ids = [r.get("id") if isinstance(r, dict) else None for r in rows]
    for i in sorted(set(EXPECTED_IDS) - set(ids)):
        errors.append("missing row " + i)
    for i in sorted(set(x for x in ids if x is not None) - set(EXPECTED_IDS)):
        errors.append("unexpected row " + str(i))
    for i in sorted(set(x for x in ids if x is not None and ids.count(x) > 1)):
        errors.append("row appears more than once " + i)
    counts = {v: 0 for v in VERDICTS}
    for row in rows:
        if not isinstance(row, dict):
            errors.append("row is not an object")
            continue
        rid = str(row.get("id"))
        if set(row.keys()) != ROW_KEYS:
            errors.append(rid + " keys must be exactly " + ", ".join(sorted(ROW_KEYS)))
            continue
        verdict = row["verdict"]
        if verdict not in VERDICTS:
            errors.append(rid + " verdict not in enum: " + str(verdict))
            continue
        counts[verdict] += 1
        if row["deployed"] not in DEPLOYED:
            errors.append(rid + " deployed not in enum: " + str(row["deployed"]))
        if not isinstance(row["hazard"], str) or not row["hazard"]:
            errors.append(rid + " hazard must be a non-empty string")
        if not isinstance(row["reason"], str) or len(row["reason"]) > 400 or not row["reason"]:
            errors.append(rid + " reason must be a non-empty string of at most 400 characters")
        ev_list = row["evidence"]
        if not isinstance(ev_list, list):
            errors.append(rid + " evidence must be a list")
            continue
        if verdict in ("CLOSED", "STANDS") and not ev_list:
            errors.append(rid + " " + verdict + " needs at least one evidence item")
        kinds = []
        for idx, ev in enumerate(ev_list):
            kinds.append(check_evidence(rid, idx, ev, errors))
        if verdict == "CLOSED":
            if "code" not in kinds:
                errors.append(rid + " CLOSED needs at least one code evidence item")
            if row["deployed"] != "n/a" and "record" not in kinds:
                errors.append(rid + " CLOSED with deployed=" + row["deployed"] + " needs at least one record evidence item")
    return errors, counts


def load_rows(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def selftest():
    rows = load_rows(AUDIT)
    target = next((r for r in rows if isinstance(r, dict) and r.get("verdict") == "CLOSED"), None)
    if target is None:
        print("CONTROL-MISSED: no CLOSED row to corrupt")
        return 1
    for ev in target["evidence"]:
        if ev.get("kind") == "code":
            ev["ref"] = "org/does/not/exist/dead_reference.py:1"
    fd, tmp = tempfile.mkstemp(prefix="audit_selftest_", suffix=".json")
    os.close(fd)
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=1)
        copy = load_rows(tmp)
        errors, _ = check(copy)
    finally:
        os.remove(tmp)
    if errors:
        print("CONTROL-FIRES " + target["id"] + ": " + errors[0])
        return 0
    print("CONTROL-MISSED: the dead-reference copy was accepted")
    return 1


def main():
    if "--selftest" in sys.argv[1:]:
        return selftest()
    try:
        rows = load_rows(AUDIT)
    except (OSError, ValueError) as exc:
        print("AUDIT-BAD cannot load AUDIT_b.json: " + str(exc))
        return 1
    errors, counts = check(rows)
    if errors:
        print("AUDIT-BAD " + "; ".join(errors[:8]) + ("; (" + str(len(errors)) + " errors in all)" if len(errors) > 8 else ""))
        return 1
    print("AUDIT-OK {} rows {} CLOSED {} STANDS {} NEEDS-LIVE-READ".format(
        len(rows), counts["CLOSED"], counts["STANDS"], counts["NEEDS-LIVE-READ"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
