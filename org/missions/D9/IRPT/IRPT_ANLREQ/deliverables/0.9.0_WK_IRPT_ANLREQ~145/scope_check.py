"""AR339-y-AC3 -- scope check for TO-AR-y-339 (worker 0.9.0_WK_IRPT_ANLREQ~145), AMENDED by AMENDMENT 1.

The cell is BUILD ONLY plus ONE map edit: a build that touched the cloud, or a map edit wider than the three staged_from
rows of functions.irpt-status, is a release nobody signed. Prints SCOPE-OK only when:
  1. every path changed from <base> to HEAD lies under org/missions/D9/IRPT/IRPT_ANLREQ/ or is the source map;
  2. the parsed source map differs from its base ONLY by the removal of exactly the three staged_from rows of
     functions.irpt-status (ops/entry.py, ops/owned_report.py, reports/status_installed.py), nothing else;
  3. the product tree shows nothing untracked or modified under infra/ (the map edit is committed);
  4. no write-class AWS call is declared in the record (the calls are reads);
  5. the release input and any staged artifact lie under C:/dev/irpt-release-r31s/.
Otherwise prints SCOPE-BAD <why> and exits 1. <base> is the parent of the first commit this order made.
"""
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
REMOVED = {
    "infra/aws/lambda/investor-reporting/ops/entry.py",
    "infra/aws/lambda/investor-reporting/ops/owned_report.py",
    "infra/aws/lambda/investor-reporting/reports/status_installed.py",
}
WRITE_VERBS = re.compile(
    r"\b(put-|update-|create-|delete-|publish|invoke|upload|apply|deploy|tag-|add-|remove-|set-|"
    r"start-|stop-|run-instances|cp\b|mv\b|rm\b|sync\b|copy-object|send)")


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True, check=True).stdout


def git_show(ref, path):
    return subprocess.run(["git", "-C", REPO, "show", ref + ":" + path], capture_output=True, text=True,
                          check=True).stdout


def main():
    rec = json.load(open(REC_PATH, encoding="utf-8"))

    # 1. the base is the parent of the first commit this order made; changed paths stay in the order's tree or the map
    issue = git("rev-parse", ISSUE_COMMIT).strip()
    first = git("rev-list", "--reverse", issue + "..HEAD").split()
    if not first:
        bad("no commit of this order on the branch yet")
    base = git("rev-parse", first[0] + "^").strip()
    changed = [p for p in git("diff", "--name-only", base, "HEAD").split("\n") if p]
    outside = [p for p in changed if not (p.startswith(ORDER_PREFIX) or p == MAP_PATH)]
    if outside:
        bad("paths changed outside the order's tree and the source map: " + ", ".join(outside[:5]))

    # 2. the map edit: parsed JSON, only the three staged_from rows of irpt-status removed
    before = json.loads(git_show(base, MAP_PATH))
    after = json.loads(open(os.path.join(REPO, MAP_PATH), encoding="utf-8").read())
    rows_b = before["functions"][FN]["staged_from"]
    rows_a = after["functions"][FN]["staged_from"]
    removed = [r["repo_path"] for r in rows_b if r not in rows_a]
    added = [r["repo_path"] for r in rows_a if r not in rows_b]
    if set(removed) != REMOVED or len(removed) != 3:
        bad("removed staged_from rows are %s, not the three named members" % sorted(removed))
    if added:
        bad("staged_from rows added: " + ", ".join(added))
    if len(rows_a) != len(rows_b) - 3:
        bad("staged_from row count changed beyond the three removals")
    b2 = json.loads(json.dumps(before))
    a2 = json.loads(json.dumps(after))
    b2["functions"][FN]["staged_from"] = []
    a2["functions"][FN]["staged_from"] = []
    if b2 != a2:
        bad("the source map differs outside the irpt-status staged_from rows")

    # 3. the product tree is clean under infra/ (the one map edit is committed, nothing else)
    infra = git("status", "--porcelain", "--", "infra").strip()
    if infra:
        bad("product tree under infra/ is not clean: " + infra.split("\n")[0])

    # 4. the declared AWS calls are reads
    calls = rec.get("aws_calls", [])
    writes = [c for c in calls if WRITE_VERBS.search(c)]
    if writes:
        bad("write-class AWS call declared: " + writes[0])

    # 5. the release input and any staged artifact lie under the release directory
    rel_wt = rec.get("release_input", {}).get("release_worktree", "")
    if not rel_wt.startswith(RELEASE_DIR):
        bad("release worktree outside " + RELEASE_DIR + ": " + rel_wt)
    art = rec.get("artifact", {}).get("path")
    if art and not art.startswith(RELEASE_DIR):
        bad("staged artifact outside " + RELEASE_DIR + ": " + art)

    print("SCOPE-OK base=%s changed=%d (all under %s or the map) map-rows-removed=3 map-other-changes=0 "
          "infra-clean aws-calls-read-only=%d staged-under-release-dir=%d"
          % (base[:10], len(changed), ORDER_PREFIX, len(calls), 1 if art else 0))


if __name__ == "__main__":
    main()
