#!/usr/bin/env python3
"""AR-y-387 checker for r47/AUDIT_a.json (stdlib only, ASCII only).

Usage:
  python audit_check.py              checks AUDIT_a.json beside this file
  python audit_check.py --selftest   control: a temporary copy with one CLOSED row whose only code
                                     ref is dead must be rejected

Checks (step 3 of TO-AR-y-387):
  (i)   the ids are exactly the 21 listed rows, each once;
  (ii)  every verdict is in the enum;
  (iii) every CLOSED row has a code item, and a record item when deployed is not n/a;
  (iv)  every ref resolves at HEAD:
          code   "path:line"  path exists at HEAD and has at least that many lines;
                 "portal/<sub>:line" resolves in the portal submodule at the HEAD gitlink;
          record "path"       exists on disk or at HEAD;
          commit "sha"        resolves as a commit.
  plus the shape of each item (kind enum, says <= 200 chars, reason <= 400 chars, deployed enum).

Prints AUDIT-OK <n> rows <c> CLOSED <s> STANDS <l> NEEDS-LIVE-READ, or AUDIT-BAD <why> and exits 1.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AUDIT = os.path.join(HERE, "AUDIT_a.json")
IDS = [
    "IRPT_ANLREQ-D2-S26", "IRPT_ANLREQ-D2-W52-S24", "IRPT_ANLREQ-D2-W52-S29", "IRPT_ANLREQ-D2-W52-S31",
    "IRPT_ANLREQ-D2-W52-S33", "IRPT_ANLREQ-D2-W52-S35", "IRPT_ANLREQ-D2-W52-S36", "IRPT_ANLREQ-D2-W61-S2",
    "IRPT_ANLREQ-D2-W75-S1", "IRPT_ANLREQ-D2-W77-S3", "IRPT_ANLREQ-D2-W90-S3", "IRPT_ANLREQ-D2-W104-S1",
    "IRPT_ANLREQ-D2-W96-S3", "IRPT_ANLREQ-D2-W107-S4", "IRPT_ANLREQ-D2-W103-S3", "IRPT_ANLREQ-D2-W103-S4",
    "IRPT_ANLREQ-D2-W109-S2", "IRPT_ANLREQ-D2-W111-S5", "IRPT_ANLREQ-D2-W113-S2", "IRPT_ANLREQ-D2-W113-S3",
    "IRPT_ANLREQ-D2-W114-S1",
]
VERDICTS = ("CLOSED", "STANDS", "NEEDS-LIVE-READ")
KINDS = ("code", "record", "commit")
DEPLOYED = ("yes", "no", "n/a", "unread")
REQUIRED = ("id", "verdict", "hazard", "evidence", "deployed", "reason")


def git(args, cwd, gitdir=None):
    cmd = ["git"] + (["--git-dir", gitdir] if gitdir else []) + args
    proc = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout


def repo_root():
    rc, out = git(["rev-parse", "--show-toplevel"], HERE)
    if rc != 0:
        raise SystemExit("AUDIT-BAD not inside a git worktree")
    return out.decode("utf-8").strip()


def portal_ctx(root):
    """The portal submodule's git dir and its gitlink commit at HEAD (the pinned DEV commit)."""
    rc, out = git(["rev-parse", "--git-common-dir"], root)
    common = out.decode("utf-8").strip()
    if not os.path.isabs(common):
        common = os.path.normpath(os.path.join(root, common))
    gitdir = os.path.join(common, "modules", "portal")
    rc, out = git(["ls-tree", "HEAD", "portal"], root)
    parts = out.decode("utf-8").split()
    gitlink = parts[2] if len(parts) >= 3 and parts[1] == "commit" else None
    return gitdir, gitlink


def line_count(rev, path, root, gitdir=None):
    """Number of lines of rev:path, or None when the path does not exist at that revision."""
    rc, data = git(["show", "%s:%s" % (rev, path)], root, gitdir)
    if rc != 0:
        return None
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def check_code(ref, root, pgd, plink):
    path, sep, line = ref.rpartition(":")
    if not sep or not line.isdigit() or int(line) < 1:
        return "code ref lacks a :line suffix: %r" % ref
    if path.startswith("portal/"):
        if not plink:
            return "no portal gitlink at HEAD for %r" % ref
        n = line_count(plink, path[len("portal/"):], root, pgd)
        where = "portal@%s" % plink[:10]
    else:
        n = line_count("HEAD", path, root)
        where = "HEAD"
    if n is None:
        return "code path does not resolve at %s: %s" % (where, path)
    if int(line) > n:
        return "line %s is beyond the %d lines of %s at %s" % (line, n, path, where)
    return None


def check_record(ref, root):
    if os.path.exists(os.path.join(root, ref)):
        return None
    rc, _ = git(["cat-file", "-e", "HEAD:" + ref], root)
    if rc == 0:
        return None
    return "record path absent on disk and at HEAD: %s" % ref


def check_commit(sha, root):
    rc, _ = git(["cat-file", "-e", sha + "^{commit}"], root)
    return None if rc == 0 else "commit does not resolve: %s" % sha


def validate(path):
    """Return (None, counts) when the audit passes, else (why, None)."""
    try:
        with open(path, encoding="utf-8") as handle:
            doc = json.load(handle)
    except (OSError, ValueError) as exc:
        return "audit unreadable: %s" % exc, None
    if not isinstance(doc, list):
        return "audit must be a JSON list of row objects", None
    seen = {}
    for row in doc:
        if not isinstance(row, dict):
            return "a row is not an object", None
        rid = row.get("id")
        seen[rid] = seen.get(rid, 0) + 1
    if sorted(seen) != sorted(IDS) or any(count != 1 for count in seen.values()):
        missing = sorted(set(IDS) - set(seen))
        extra = sorted(set(seen) - set(IDS))
        dup = sorted(k for k, v in seen.items() if v != 1)
        return "ids differ from the 21 listed: missing %s extra %s duplicated %s" % (missing, extra, dup), None
    root = repo_root()
    pgd, plink = portal_ctx(root)
    counts = {v: 0 for v in VERDICTS}
    for row in doc:
        rid = row["id"]
        for key in REQUIRED:
            if key not in row:
                return "%s lacks %s" % (rid, key), None
        if row["verdict"] not in VERDICTS:
            return "%s verdict %r not in enum" % (rid, row["verdict"]), None
        if row["deployed"] not in DEPLOYED:
            return "%s deployed %r not in enum" % (rid, row["deployed"]), None
        if not isinstance(row["reason"], str) or not row["reason"] or len(row["reason"]) > 400:
            return "%s reason empty or longer than 400 chars" % rid, None
        if not isinstance(row["evidence"], list) or not row["evidence"]:
            return "%s has no evidence list" % rid, None
        kinds = [item.get("kind") for item in row["evidence"] if isinstance(item, dict)]
        for item in row["evidence"]:
            if not isinstance(item, dict) or set(item) != {"kind", "ref", "says"}:
                return "%s has an evidence item without exactly kind, ref, says" % rid, None
            if item["kind"] not in KINDS:
                return "%s evidence kind %r not in enum" % (rid, item["kind"]), None
            if not isinstance(item["says"], str) or len(item["says"]) > 200:
                return "%s evidence says missing or longer than 200 chars" % rid, None
            if item["kind"] == "code":
                why = check_code(item["ref"], root, pgd, plink)
            elif item["kind"] == "record":
                why = check_record(item["ref"], root)
            else:
                why = check_commit(item["ref"], root)
            if why:
                return "%s: %s" % (rid, why), None
        if row["verdict"] == "CLOSED":
            if "code" not in kinds:
                return "%s is CLOSED with no code evidence" % rid, None
            if row["deployed"] != "n/a" and "record" not in kinds:
                return "%s is CLOSED on a deployed hazard with no record evidence" % rid, None
        counts[row["verdict"]] += 1
    return None, counts


def selftest():
    with open(AUDIT, encoding="utf-8") as handle:
        doc = json.load(handle)
    target = next(row for row in doc if row["verdict"] == "CLOSED")
    target["evidence"] = [{"kind": "code", "ref": "infra/control/does_not_exist.py:1",
                           "says": "CONTROL: the only code ref of this CLOSED row is dead"}] + \
        [item for item in target["evidence"] if item["kind"] != "code"]
    tmp = os.path.join(HERE, "_selftest_copy_AUDIT.json")
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(doc, handle, indent=1)
        why, _counts = validate(tmp)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    if why:
        print("CONTROL-FIRES: copy with a dead CLOSED ref rejected (%s)" % why)
        return 0
    print("CONTROL-MISSED: a copy with a dead CLOSED ref was accepted")
    return 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    why, counts = validate(AUDIT)
    if why:
        print("AUDIT-BAD %s" % why)
        return 1
    print("AUDIT-OK %d rows %d CLOSED %d STANDS %d NEEDS-LIVE-READ" % (
        len(IDS), counts["CLOSED"], counts["STANDS"], counts["NEEDS-LIVE-READ"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
