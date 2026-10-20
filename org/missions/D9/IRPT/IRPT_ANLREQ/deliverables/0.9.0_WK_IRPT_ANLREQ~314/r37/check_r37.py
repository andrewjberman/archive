"""IRPT_ANLREQ release 37 acceptance checker (cell AR-y-426, worker 0.9.0_WK_IRPT_ANLREQ~314). Stdlib only, ASCII only.

    python -I check_r37.py diff <record.json> <live-members.json>
    python -I check_r37.py identity <record.json> <smoke.txt>
    python -I check_r37.py map <commit>
    python -I check_r37.py --selftest <record.json> <live-members.json>

diff: compares the member sha256 map of the BUILT irpt-ycharts-generate package (the record written by r37_build.py) with the
LIVE members file (names, sizes and sha256 only, read earlier with a read-only get-function). Prints R37-DIFF-OK only when the
non-SAME set is exactly {served.py: MOVED} and the built served.py hashes to 600a934c4b34...; otherwise R37-DIFF-BAD naming every
other mover, exit 1. An extra mover is named, never suppressed.

identity: prints R37-IDENTITY-OK only when the record shows the two builds byte-identical and the smoke file shows both imports ok.

map: prints R37-MAP-OK only when the commit's diff touches exactly one file, the function map, with 2 insertions and 2 deletions,
and the served.py staged_from entry of that map at the commit carries the scratch pin and the sha256 of this release.

--selftest runs the diff mode on an in-memory copy of the record in which a second member's hash is altered, and prints
CONTROL-FIRES only when that copy yields R37-DIFF-BAD (otherwise CONTROL-DID-NOT-FIRE and exit 1).
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

FUNCTION = "irpt-ycharts-generate"
MOVER = "served.py"
MAP_PATH = "infra/aws/lambda/ci/function-map/irpt-ycharts-generate.json"
PIN = "720e125d31469ed60b6e698812c7be731bd6d8e8"
SHA = "600a934c4b34da1e14ec8b7d4de4a3f69cc55c331257dd90abb525def9929fcd"
SHA_SHORT = "600a934c4b34"


def run_git(args):
    out = subprocess.run(["git", *args], capture_output=True)
    return out.returncode, out.stdout.decode("utf-8", "replace"), out.stderr.decode("utf-8", "replace").strip()


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def classify(built, live):
    kinds = {}
    for name in sorted(set(built) | set(live)):
        if name not in built:
            kinds[name] = "ADDED"
        elif name not in live:
            kinds[name] = "REMOVED"
        elif built[name] == live[name]:
            kinds[name] = "SAME"
        else:
            kinds[name] = "MOVED"
    return kinds


def diff_verdict(record, live_doc):
    built = record["functions"][FUNCTION]["member_sha256"]
    live = {m["name"]: m["sha256"] for m in live_doc["members"]}
    kinds = classify(built, live)
    lines = ["NON-SAME %s %s built=%s live=%s" % (kinds[n], n, built.get(n, "-"), live.get(n, "-"))
             for n in kinds if kinds[n] != "SAME"]
    counts = {k: sum(1 for v in kinds.values() if v == k) for k in ("MOVED", "ADDED", "REMOVED", "SAME")}
    reasons = []
    others = [n for n in kinds if kinds[n] != "SAME" and not (n == MOVER and kinds[n] == "MOVED")]
    if others:
        reasons.append("other movers present: " + ", ".join("%s:%s" % (n, kinds[n]) for n in others))
    if kinds.get(MOVER) != "MOVED":
        reasons.append("%s is %s, not MOVED" % (MOVER, kinds.get(MOVER, "absent from both")))
    if built.get(MOVER) != SHA:
        reasons.append("built %s sha256=%s, not %s" % (MOVER, built.get(MOVER), SHA))
    if not reasons:
        lines.append("R37-DIFF-OK moved=%d added=%d removed=%d same=%d mover=%s served_sha256=%s" % (
            counts["MOVED"], counts["ADDED"], counts["REMOVED"], counts["SAME"], MOVER, SHA_SHORT))
        return lines, True
    lines.append("R37-DIFF-BAD " + "; ".join(reasons))
    return lines, False


def identity_verdict(record, smoke_path):
    identical = record["functions"][FUNCTION].get("builds_identical") is True
    smoke = set(line.strip() for line in Path(smoke_path).read_text(encoding="utf-8").splitlines())
    served_ok = "import_served=ok" in smoke
    generate_ok = "import_generate_installed=ok" in smoke
    if identical and served_ok and generate_ok:
        return "R37-IDENTITY-OK builds_identical=yes import_served=ok import_generate_installed=ok", True
    return "R37-IDENTITY-BAD builds_identical=%s import_served=%s import_generate_installed=%s" % (
        "yes" if identical else "no", "ok" if served_ok else "not-ok", "ok" if generate_ok else "not-ok"), False


def map_verdict(commit):
    rc, out, err = run_git(["diff", "--numstat", commit + "~1", commit])
    if rc != 0:
        return "R37-MAP-BAD git diff --numstat failed rc=%d %s" % (rc, err[:200]), False
    rows = [line.split("\t") for line in out.splitlines() if line.strip()]
    if len(rows) != 1:
        return "R37-MAP-BAD numstat lists %d files, want exactly 1" % len(rows), False
    added, deleted, path = rows[0]
    if path != MAP_PATH:
        return "R37-MAP-BAD numstat file is %s, want %s" % (path, MAP_PATH), False
    if (added, deleted) != ("2", "2"):
        return "R37-MAP-BAD numstat=%s/%s, want 2/2" % (added, deleted), False
    rc, text, err = run_git(["show", commit + ":" + MAP_PATH])
    if rc != 0:
        return "R37-MAP-BAD git show failed rc=%d %s" % (rc, err[:200]), False
    entries = [e for e in json.loads(text).get("staged_from", []) if e.get("packaged_as") == MOVER]
    if len(entries) != 1:
        return "R37-MAP-BAD %d staged_from entries packaged as %s, want 1" % (len(entries), MOVER), False
    entry = entries[0]
    if entry.get("pin") != PIN or entry.get("sha256") != SHA:
        return "R37-MAP-BAD pin=%s sha256=%s on the %s entry, want pin=%s sha256=%s" % (
            entry.get("pin"), entry.get("sha256"), MOVER, PIN, SHA), False
    return "R37-MAP-OK numstat=2/2 pin=%s sha256=%s" % (PIN, SHA_SHORT), True


def selftest(record, live_doc):
    control = copy.deepcopy(record)
    built = control["functions"][FUNCTION]["member_sha256"]
    altered = sorted(n for n in built if n != MOVER)[1]
    built[altered] = "0" * 64
    lines, ok = diff_verdict(control, live_doc)
    print("CONTROL altered=%s" % altered)
    verdict = lines[-1]
    print(verdict)
    if ok or not verdict.startswith("R37-DIFF-BAD"):
        print("CONTROL-DID-NOT-FIRE")
        return 1
    print("CONTROL-FIRES")
    return 0


def main(argv):
    if not argv:
        print("R37-USAGE diff|identity|map|--selftest")
        return 2
    mode, rest = argv[0], argv[1:]
    if mode == "--selftest" and len(rest) == 2:
        return selftest(load_json(rest[0]), load_json(rest[1]))
    if mode == "diff" and len(rest) == 2:
        lines, ok = diff_verdict(load_json(rest[0]), load_json(rest[1]))
    elif mode == "identity" and len(rest) == 2:
        line, ok = identity_verdict(load_json(rest[0]), rest[1])
        lines = [line]
    elif mode == "map" and len(rest) == 1:
        line, ok = map_verdict(rest[0])
        lines = [line]
    else:
        print("R37-USAGE diff|identity|map|--selftest")
        return 2
    for line in lines:
        print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
