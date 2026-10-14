"""AR339-y-AC3 -- scope check for TO-AR-y-339 (worker 0.9.0_WK_IRPT_ANLREQ~145), AMENDED by AMENDMENTS 1 and 3.

The cell is BUILD ONLY plus ONE map edit: a build that touched the cloud, or a map edit wider than the net change the
order names, is a release nobody signed. Prints SCOPE-OK only when:
  1. every path changed from <base> to HEAD lies under org/missions/D9/IRPT/IRPT_ANLREQ/ or is the source map;
  2. the NET diff of the source map against <base> (parsed JSON) is exactly: the staged_from rows of functions.irpt-status
     for ops/entry.py and ops/owned_report.py REMOVED, and the row for reports/status_installed.py KEPT with ONLY its
     pin (the full sha of c4c2afe896) and its sha256 (the sha256 of that blob at that pin) changed; every other row,
     key and top-level field (including _updated) identical, in the same order;
  3. the product tree shows nothing untracked or modified under infra/ (the map edit is committed);
  4. no write-class AWS call is declared in the record (the calls are reads);
  5. the release input and every staged artifact lie under C:/dev/irpt-release-r31s/.
Otherwise prints SCOPE-BAD <why> and exits 1. <base> is the parent of the first commit this order made.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REC_PATH = os.path.join(HERE, "r41", "IRPT_STATUS_R31_BUILD.json")
REPO = "C:/dev/wk-irpt-anlreq-145"
ISSUE_COMMIT = "69c3e39c2b"  # the issuance commit this order was cut on (worker HEAD at start)
ORDER_PREFIX = "org/missions/D9/IRPT/IRPT_ANLREQ/"
MAP_PATH = "infra/aws/lambda/ci/lambda-source-map.json"
RELEASE_DIR = "C:/dev/irpt-release-r31s/"
FN = "irpt-status"
STATUS_PATH = "infra/aws/lambda/investor-reporting/reports/status_installed.py"
STATUS_PIN = "c4c2afe89639071f41242fc9f663cadaffa0ffd8"
REMOVED = {
    "infra/aws/lambda/investor-reporting/ops/entry.py",
    "infra/aws/lambda/investor-reporting/ops/owned_report.py",
}
WRITE_VERBS = re.compile(
    r"\b(put-|update-|create-|delete-|publish|invoke|upload|apply|deploy|tag-|add-|remove-|set-|"
    r"start-|stop-|run-instances|cp\b|mv\b|rm\b|sync\b|copy-object|send)")


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True, check=True).stdout


def git_bytes(ref, path):
    return subprocess.run(["git", "-C", REPO, "show", ref + ":" + path], capture_output=True, check=True).stdout


def main():
    rec = json.load(open(REC_PATH, encoding="utf-8"))

    # 1. the base is the parent of the first commit this order made; changed paths stay in the order's tree or the map
    issue = git("rev-parse", ISSUE_COMMIT).strip()
    first = git("rev-list", "--reverse", issue + "..HEAD").split()
    if not first:
        bad("no commit of this order on the branch yet")
    base = git("rev-parse", first[0] + "^").strip()
    if base != issue:
        bad("base %s is not the issuance commit %s" % (base, issue))
    changed = [p for p in git("diff", "--name-only", base, "HEAD").split("\n") if p]
    outside = [p for p in changed if not (p.startswith(ORDER_PREFIX) or p == MAP_PATH)]
    if outside:
        bad("paths changed outside the order's tree and the source map: " + ", ".join(outside[:5]))

    # 2. the NET map diff against the base: parsed JSON, the exact named change and nothing else
    before = json.loads(git_bytes(base, MAP_PATH).decode("utf-8"))
    after = json.loads(open(os.path.join(REPO, MAP_PATH), encoding="utf-8").read())
    rows_b = before["functions"][FN]["staged_from"]
    rows_a = after["functions"][FN]["staged_from"]
    pin_sha = git("rev-parse", STATUS_PIN).strip()
    if pin_sha != STATUS_PIN:
        bad("STATUS_PIN does not resolve to itself: %s" % pin_sha)
    blob = git_bytes(STATUS_PIN, STATUS_PATH)
    blob_sha = hashlib.sha256(blob).hexdigest()
    if b"commentary-pdf" not in blob or b'"analysis-request-commentary-pdf"' not in blob:
        bad("the blob at the pin does not carry the commentary-pdf route key")
    expected = []
    seen_status = 0
    for r in rows_b:
        if r["repo_path"] in REMOVED:
            continue
        if r["repo_path"] == STATUS_PATH:
            seen_status += 1
            expected.append({"repo_path": STATUS_PATH, "pin": STATUS_PIN,
                             "packaged_as": r["packaged_as"], "sha256": blob_sha})
        else:
            expected.append(r)
    if seen_status != 1:
        bad("the status_installed.py row is not present exactly once at the base")
    if {r["repo_path"] for r in rows_b} - {r["repo_path"] for r in rows_a} != REMOVED:
        bad("removed staged_from rows are not exactly ops/entry.py and ops/owned_report.py")
    if rows_a != expected:
        bad("staged_from of %s differs from the named net change (the expected list is the base list with the two rows "
            "removed and the status_installed.py row re-pinned)" % FN)
    b2 = json.loads(json.dumps(before))
    a2 = json.loads(json.dumps(after))
    b2["functions"][FN]["staged_from"] = []
    a2["functions"][FN]["staged_from"] = []
    if b2 != a2:
        bad("the source map differs outside the irpt-status staged_from rows (top-level, _updated or another key)")

    # 3. the product tree is clean under infra/ (the map edit is committed, nothing else)
    infra = git("status", "--porcelain", "--", "infra").strip()
    if infra:
        bad("product tree under infra/ is not clean: " + infra.split("\n")[0])

    # 4. the declared AWS calls are reads
    calls = rec.get("aws_calls", [])
    writes = [c for c in calls if WRITE_VERBS.search(c)]
    if writes:
        bad("write-class AWS call declared: " + writes[0])

    # 5. the release input and every staged artifact lie under the release directory
    paths = [rec.get("release_input", {}).get("release_worktree", ""), rec.get("artifact", {}).get("path", "")]
    paths += rec.get("two_builds", {}).get("paths", [])
    paths += [rec.get("live_read", {}).get("download_path", "")]
    for p in paths:
        if not p or not p.startswith(RELEASE_DIR):
            bad("path outside " + RELEASE_DIR + ": %r" % p)

    print("SCOPE-OK base=%s changed=%d (all under %s or the map) map-rows-removed=2 status-row-repinned=1 "
          "map-other-changes=0 infra-clean aws-calls-read-only=%d staged-under-release-dir=%d"
          % (base[:10], len(changed), ORDER_PREFIX, len(calls), len(paths)))


if __name__ == "__main__":
    main()
