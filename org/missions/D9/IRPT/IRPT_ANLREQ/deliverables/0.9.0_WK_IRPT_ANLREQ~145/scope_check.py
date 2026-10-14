"""AR339-y-AC3 -- scope check for TO-AR-y-339 (worker 0.9.0_WK_IRPT_ANLREQ~145).

The cell is BUILD ONLY: a build that touched the repository or the cloud is a release nobody signed.
Prints SCOPE-OK only when: every path this order changed lies under org/missions/D9/IRPT/IRPT_ANLREQ/;
the product tree shows nothing untracked or modified under infra/; every AWS call the worker declares in the
record is a read; and any staged artifact lies under C:/dev/irpt-release-r31/. Otherwise SCOPE-BAD <why>, exit 1.
The AWS check reads the calls the worker declared in r41/IRPT_STATUS_R31_BUILD.json (aws_calls); it does not read
the shell history.
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
RELEASE_DIR = "C:/dev/irpt-release-r31/"
WRITE_VERBS = re.compile(
    r"\b(put-|update-|create-|delete-|publish|invoke|upload|apply|deploy|tag-|add-|remove-|set-|"
    r"start-|stop-|run-instances|cp\b|mv\b|rm\b|sync\b|copy-object|send)")


def bad(why):
    print("SCOPE-BAD " + why)
    sys.exit(1)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True, check=True).stdout


def main():
    rec = json.load(open(REC_PATH, encoding="utf-8"))

    # 1. the base is the parent of the first commit this order made
    issue = git("rev-parse", ISSUE_COMMIT).strip()
    first = git("rev-list", "--reverse", issue + "..HEAD").split()
    if not first:
        bad("no commit of this order on the branch yet")
    base = git("rev-parse", first[0] + "^").strip()
    changed = [p for p in git("diff", "--name-only", base, "HEAD").split("\n") if p]
    outside = [p for p in changed if not p.startswith(ORDER_PREFIX)]
    if outside:
        bad("paths changed outside the order's tree: " + ", ".join(outside[:5]))

    # 2. the product tree is clean under infra/
    infra = git("status", "--porcelain", "--", "infra").strip()
    if infra:
        bad("product tree under infra/ is not clean: " + infra.split("\n")[0])

    # 3. the declared AWS calls are reads
    calls = rec.get("aws_calls", [])
    writes = [c for c in calls if WRITE_VERBS.search(c)]
    if writes:
        bad("write-class AWS call declared: " + writes[0])

    # 4. staged artifacts live under the release directory (none staged when the build is blocked)
    art = rec.get("artifact", {}).get("path")
    if art and not art.startswith(RELEASE_DIR):
        bad("staged artifact outside " + RELEASE_DIR + ": " + art)

    print("SCOPE-OK base=%s changed=%d (all under %s) infra-clean aws-calls-read-only=%d staged-under-release-dir=%d"
          % (base[:10], len(changed), ORDER_PREFIX, len(calls), 1 if art else 0))


if __name__ == "__main__":
    main()
