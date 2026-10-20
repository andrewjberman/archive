"""IRPT_ANLREQ release 37 version 2 acceptance checker (cell AR-y-441, worker 0.9.0_WK_IRPT_ANLREQ~319). Stdlib only, ASCII only.

    python -I check_r37.py diff <record.json> <live-members.json>
    python -I check_r37.py identity <record.json> <smoke.txt>
    python -I check_r37.py map
    python -I check_r37.py --selftest <record.json> <live-members.json>

diff: compares the member sha256 map of the BUILT irpt-ycharts-generate package (the record written by r37_build.py) with the
LIVE members file (names, sizes and sha256 only, read earlier with a read-only get-function). Prints R37V2-DIFF-OK only when the
non-SAME set is exactly the two movers, both MOVED, and the built served.py and ticket_confirmation.py hash to the values of this
release; otherwise R37V2-DIFF-BAD naming every other mover, exit 1. An extra mover is named, never suppressed.

identity: prints R37V2-IDENTITY-OK only when the record shows the two builds byte-identical and the smoke file holds exactly one
line each of import_served=ok, import_generate_installed=ok, confirm_created_by=true and other=false.

map: finds the commit whose subject begins 'pin(IRPT_ANLREQ TO-AR-y-441,' and prints R37V2-MAP-OK only when that commit's diff
touches exactly one file, the function map, with 2 insertions and 2 deletions, and the ticket_confirmation.py staged_from entry of
that map at the commit carries the pin and sha256 of this release; otherwise R37V2-MAP-BAD, exit 1.

--selftest runs the diff mode on an in-memory copy of the record in which a third non-mover member's hash is altered, and prints
CONTROL-FIRES only when that copy yields R37V2-DIFF-BAD (otherwise CONTROL-DID-NOT-FIRE and exit 1).
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

FUNCTION = "irpt-ycharts-generate"
MAP_PATH = "infra/aws/lambda/ci/function-map/irpt-ycharts-generate.json"
MAP_GREP = "^pin(IRPT_ANLREQ TO-AR-y-441,"
MOVERS = ("served.py", "ticket_confirmation.py")
SHA = {
    "served.py": "600a934c4b34da1e14ec8b7d4de4a3f69cc55c331257dd90abb525def9929fcd",
    "ticket_confirmation.py": "e76593c7951a2949a42ba78dba85aa45a8eaa4a5633fe58f0e636291b2c5dc6d",
}
TC_PIN = "752e87d46b73b8d92dc638a1040a17ad359dcfd8"
SMOKE_EXPECT = {"import_served": "ok", "import_generate_installed": "ok", "confirm_created_by": "true", "other": "false"}


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
    others = [n for n in kinds if kinds[n] != "SAME" and not (n in MOVERS and kinds[n] == "MOVED")]
    if others:
        reasons.append("other movers present: " + ", ".join("%s:%s" % (n, kinds[n]) for n in others))
    for mover in MOVERS:
        if kinds.get(mover) != "MOVED":
            reasons.append("%s is %s, not MOVED" % (mover, kinds.get(mover, "absent from both")))
        if built.get(mover) != SHA[mover]:
            reasons.append("built %s sha256=%s, not %s" % (mover, built.get(mover), SHA[mover]))
    if not reasons:
        lines.append("R37V2-DIFF-OK moved=%d added=%d removed=%d same=%d movers=%s" % (
            counts["MOVED"], counts["ADDED"], counts["REMOVED"], counts["SAME"], ",".join(MOVERS)))
        return lines, True
    lines.append("R37V2-DIFF-BAD " + "; ".join(reasons))
    return lines, False


def smoke_pairs(path):
    pairs = []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            pairs.append((key, value))
    return pairs


def identity_verdict(record, smoke_path):
    identical = record["functions"][FUNCTION].get("builds_identical") is True
    pairs = smoke_pairs(smoke_path)
    smoke_ok = all([v for k, v in pairs if k == key] == [want] for key, want in SMOKE_EXPECT.items())
    if identical and smoke_ok:
        return "R37V2-IDENTITY-OK builds_identical=yes import_served=ok import_generate_installed=ok confirm_created_by=true other=false", True
    seen = " ".join("%s=%s" % (k, v) for k, v in pairs)
    return "R37V2-IDENTITY-BAD builds_identical=%s smoke=[%s]" % ("yes" if identical else "no", seen), False


def map_verdict():
    rc, out, err = run_git(["log", "--format=%H", "--grep=" + MAP_GREP, "-1"])
    commits = out.split()
    if rc != 0 or not commits:
        return "R37V2-MAP-BAD no commit has a subject beginning %s (rc=%d %s)" % (MAP_GREP, rc, err[:200]), False
    commit = commits[0]
    rc, out, err = run_git(["diff", "--numstat", commit + "~1", commit])
    if rc != 0:
        return "R37V2-MAP-BAD git diff --numstat failed rc=%d %s" % (rc, err[:200]), False
    rows = [line.split("\t") for line in out.splitlines() if line.strip()]
    if len(rows) != 1:
        return "R37V2-MAP-BAD numstat lists %d files, want exactly 1" % len(rows), False
    added, deleted, path = rows[0]
    if path != MAP_PATH:
        return "R37V2-MAP-BAD numstat file is %s, want %s" % (path, MAP_PATH), False
    if (added, deleted) != ("2", "2"):
        return "R37V2-MAP-BAD numstat=%s/%s, want 2/2" % (added, deleted), False
    rc, text, err = run_git(["show", commit + ":" + MAP_PATH])
    if rc != 0:
        return "R37V2-MAP-BAD git show failed rc=%d %s" % (rc, err[:200]), False
    entries = [e for e in json.loads(text).get("staged_from", []) if e.get("packaged_as") == "ticket_confirmation.py"]
    if len(entries) != 1:
        return "R37V2-MAP-BAD %d staged_from entries packaged as ticket_confirmation.py, want 1" % len(entries), False
    entry = entries[0]
    if entry.get("pin") != TC_PIN or entry.get("sha256") != SHA["ticket_confirmation.py"]:
        return "R37V2-MAP-BAD pin=%s sha256=%s on the ticket_confirmation.py entry, want pin=%s sha256=%s" % (
            entry.get("pin"), entry.get("sha256"), TC_PIN, SHA["ticket_confirmation.py"]), False
    return "R37V2-MAP-OK numstat=2/2 pin=%s sha256=%s" % (TC_PIN[:12], SHA["ticket_confirmation.py"][:12]), True


def selftest(record, live_doc):
    control = copy.deepcopy(record)
    built = control["functions"][FUNCTION]["member_sha256"]
    altered = sorted(n for n in built if n not in MOVERS)[2]
    built[altered] = "0" * 64
    lines, ok = diff_verdict(control, live_doc)
    print("CONTROL altered=%s" % altered)
    verdict = lines[-1]
    print(verdict)
    if ok or not verdict.startswith("R37V2-DIFF-BAD"):
        print("CONTROL-DID-NOT-FIRE")
        return 1
    print("CONTROL-FIRES")
    return 0


def main(argv):
    if not argv:
        print("R37V2-USAGE diff|identity|map|--selftest")
        return 2
    mode, rest = argv[0], argv[1:]
    if mode == "--selftest" and len(rest) == 2:
        return selftest(load_json(rest[0]), load_json(rest[1]))
    if mode == "diff" and len(rest) == 2:
        lines, ok = diff_verdict(load_json(rest[0]), load_json(rest[1]))
    elif mode == "identity" and len(rest) == 2:
        line, ok = identity_verdict(load_json(rest[0]), rest[1])
        lines = [line]
    elif mode == "map" and not rest:
        line, ok = map_verdict()
        lines = [line]
    else:
        print("R37V2-USAGE diff|identity|map|--selftest")
        return 2
    for line in lines:
        print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
