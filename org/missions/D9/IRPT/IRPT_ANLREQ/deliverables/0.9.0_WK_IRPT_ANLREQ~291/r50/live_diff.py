"""IRPT_ANLREQ release 36S live diff (cell AR-y-392, worker 0.9.0_WK_IRPT_ANLREQ~291). Stdlib only, ASCII only.

    python -I live_diff.py <record.json> <live-members.json> [--stage <folder>]
    python -I live_diff.py --selftest <record.json> <live-members.json> [--stage <folder>]

Diffs the member sha256 of the BUILT irpt-status package (the record written by r36s_build.py) against the LIVE package's members
(read earlier with a read-only get-function: names, sizes and sha256 only). For every member that is not SAME it prints the commits
that moved it since the live build pin 90b69dcb12, with the repository path taken from the function map at the record's pin. It then
opens the staged zip and checks that the packaged acceptance.py carries get_commentary_ref and hashes to 0c4acec6...513d.

Prints the LIVE-DIFF-OK line and exits 0 only when the only non-SAME member is acceptance.py (MOVED) and the text checks hold;
otherwise prints LIVE-DIFF-BAD with every reason and exits 1. Nothing is suppressed: an extra mover is named.

--selftest runs the same checks on a copy of the record in which a second member's hash is altered, and prints CONTROL-FIRES only
when that copy yields LIVE-DIFF-BAD (otherwise CONTROL-DID-NOT-FIRE and exit 1).
"""
import argparse
import copy
import hashlib
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

FUNCTION = "irpt-status"
MOVER = "acceptance.py"
ACCEPT_SHA = "0c4acec625b7da70da82efccf58cc967e9e5bf53c32e955d67079b711701513d"
ACCEPT_MARKER = b"def get_commentary_ref"
LIVE_BUILD_PIN = "90b69dcb12cdfedc786966ab33d034bf14229396"
MAP_PATH = "infra/aws/lambda/ci/function-map/irpt-status.json"
STAGE_DEFAULT = "C:/dev/irpt-release-r36s2"
STAGE_ZIP = "irpt-status.zip"


def git_run(args):
    out = subprocess.run(["git", *args], capture_output=True)
    return out.returncode, out.stdout.decode("utf-8", "replace"), out.stderr.decode("utf-8", "replace").strip()


def short(value):
    return value[:12] if value else "-"


def load_map(commit):
    rc, text, err = git_run(["show", commit + ":" + MAP_PATH])
    if rc != 0:
        return None, err[:200]
    return json.loads(text), ""


def resolve_repo_path(map_doc, name):
    for entry in map_doc.get("staged_from", []):
        if entry.get("packaged_as") == name:
            return entry.get("repo_path"), "function map staged_from"
    if name in map_doc.get("files", []):
        return map_doc.get("source_dir", "") + "/" + name, "inferred from function map files list"
    return None, "UNRESOLVED"


def staged_pin(map_doc, name):
    for entry in map_doc.get("staged_from", []):
        if entry.get("packaged_as") == name:
            return entry.get("pin")
    return None


def moved_commits(commit, repo_path):
    rc, text, err = git_run(["log", "--oneline", LIVE_BUILD_PIN + ".." + commit, "--", repo_path])
    if rc != 0:
        return ["GIT-ERR rc=%d %s" % (rc, err[:200])]
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return lines or ["NO-COMMIT-SINCE-90b69dcb12"]


def evaluate(record, live, stage):
    lines = []
    reasons = []
    built_fn = record["functions"][FUNCTION]
    built = built_fn["member_sha256"]
    live_map = {m["name"]: m["sha256"] for m in live["members"]}
    pin = record["pin"]
    lines.append("BUILT sha=%s members=%d" % (built_fn["code_sha256"], len(built)))
    lines.append("LIVE sha=%s members=%d" % (live["code_sha256"], len(live_map)))

    names = sorted(set(built) | set(live_map))
    kinds = {}
    for name in names:
        built_sha = built.get(name)
        live_sha = live_map.get(name)
        if built_sha is None:
            kind = "REMOVED"
        elif live_sha is None:
            kind = "ADDED"
        elif built_sha == live_sha:
            kind = "SAME"
        else:
            kind = "MOVED"
        kinds[name] = kind
        lines.append("%s %s built=%s live=%s" % (kind, name, short(built_sha), short(live_sha)))

    non_same = [n for n in names if kinds[n] != "SAME"]
    map_doc, map_err = load_map(pin)
    if map_doc is None:
        reasons.append("function map unreadable at pin %s: %s" % (pin[:12], map_err))
    for name in non_same:
        if map_doc is None:
            lines.append("COMMITS %s repo_path=UNRESOLVED (no map)" % name)
            continue
        repo_path, how = resolve_repo_path(map_doc, name)
        if repo_path is None:
            lines.append("COMMITS %s repo_path=UNRESOLVED" % name)
            continue
        lines.append("COMMITS %s repo_path=%s (%s)" % (name, repo_path, how))
        lines.append("GITLOG git log --oneline %s..%s -- %s" % (LIVE_BUILD_PIN, pin, repo_path))
        for entry in moved_commits(pin, repo_path):
            lines.append("  " + entry)
        # The staged blob is the one at the MAP's per-entry pin, not at the record's commit: the commits behind the mover are the
        # ones between the base map's pin for this member and the pin-commit map's pin for it.
        old_doc, _ = load_map(pin + "^")
        old_pin = staged_pin(old_doc, name) if old_doc is not None else None
        new_pin = staged_pin(map_doc, name)
        if old_pin is None or new_pin is None:
            lines.append("MAPPIN %s old=%s new=%s UNRESOLVED" % (name, old_pin, new_pin))
            continue
        lines.append("MAPPIN %s map-pin %s -> %s: git log --oneline %s..%s -- %s" % (
            name, old_pin[:12], new_pin[:12], old_pin, new_pin, repo_path))
        rc, text, err = git_run(["log", "--oneline", old_pin + ".." + new_pin, "--", repo_path])
        entries = [ln for ln in text.splitlines() if ln.strip()] if rc == 0 else ["GIT-ERR rc=%d %s" % (rc, err[:200])]
        for entry in entries or ["NO-COMMIT-IN-MAP-PIN-RANGE"]:
            lines.append("  " + entry)

    others = [n for n in non_same if not (n == MOVER and kinds[n] == "MOVED")]
    if others:
        reasons.append("non-SAME members other than %s MOVED: %s" % (
            MOVER, ", ".join("%s:%s" % (n, kinds[n]) for n in others)))
    if kinds.get(MOVER) != "MOVED":
        reasons.append("%s is not MOVED (%s)" % (MOVER, kinds.get(MOVER, "absent from both")))
    if built.get(MOVER) != ACCEPT_SHA:
        reasons.append("record %s sha256 is %s, not %s" % (MOVER, built.get(MOVER), ACCEPT_SHA))

    zip_path = Path(stage) / STAGE_ZIP
    if not zip_path.is_file():
        reasons.append("stage zip absent: %s" % zip_path)
    else:
        data = zip_path.read_bytes()
        zip_sha = hashlib.sha256(data).hexdigest()
        if zip_sha != built_fn["zip_sha256"]:
            reasons.append("stage zip sha256 %s differs from the record %s" % (zip_sha, built_fn["zip_sha256"]))
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            zip_members = {}
            for info in zf.infolist():
                if not info.is_dir():
                    zip_members[info.filename] = hashlib.sha256(zf.read(info.filename)).hexdigest()
            if MOVER not in zip_members:
                reasons.append("%s absent at the zip root" % MOVER)
                acc = b""
            else:
                acc = zf.read(MOVER)
        acc_sha = hashlib.sha256(acc).hexdigest()
        marker_ok = ACCEPT_MARKER in acc
        lines.append("CHECK zip=%s zip_sha256=%s members=%d" % (zip_path, zip_sha, len(zip_members)))
        lines.append("CHECK acceptance_sha256=%s equals_0c4acec=%s" % (acc_sha, "yes" if acc_sha == ACCEPT_SHA else "no"))
        lines.append("CHECK acceptance_has_get_commentary_ref=%s" % ("yes" if marker_ok else "no"))
        if acc_sha != ACCEPT_SHA:
            reasons.append("zip %s sha256 %s, not %s" % (MOVER, acc_sha, ACCEPT_SHA))
        if not marker_ok:
            reasons.append("zip %s has no def get_commentary_ref" % MOVER)

    if not reasons:
        counts = {k: sum(1 for n in names if kinds[n] == k) for k in ("MOVED", "ADDED", "REMOVED", "SAME")}
        lines.append("LIVE-DIFF-OK moved=%d added=%d removed=%d same=%d mover=%s acceptance_has_get_commentary_ref=yes" % (
            counts["MOVED"], counts["ADDED"], counts["REMOVED"], counts["SAME"], MOVER))
        return lines, True
    lines.append("LIVE-DIFF-BAD " + "; ".join(reasons))
    return lines, False


def selftest(record, live, stage):
    control = copy.deepcopy(record)
    built = control["functions"][FUNCTION]["member_sha256"]
    altered = sorted(n for n in built if n != MOVER)[0]
    built[altered] = "0" * 64
    lines, ok = evaluate(control, live, stage)
    verdict = lines[-1]
    print("CONTROL altered=%s" % altered)
    print(verdict)
    if ok or not verdict.startswith("LIVE-DIFF-BAD"):
        print("CONTROL-DID-NOT-FIRE")
        return 1
    print("CONTROL-FIRES")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("record")
    parser.add_argument("live")
    parser.add_argument("--stage", default=STAGE_DEFAULT)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    record = json.loads(Path(args.record).read_text(encoding="utf-8"))
    live = json.loads(Path(args.live).read_text(encoding="utf-8"))
    if args.selftest:
        return selftest(record, live, args.stage)
    lines, ok = evaluate(record, live, args.stage)
    for ln in lines:
        print(ln)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
