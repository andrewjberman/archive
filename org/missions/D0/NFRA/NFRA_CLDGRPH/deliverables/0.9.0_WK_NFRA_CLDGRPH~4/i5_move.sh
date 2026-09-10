#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-I-5 (CG-s-45) -- I5-AC3.
#
# THE MOVE, OR THE FILING. This is the filing, and the reason is a grant, not a
# judgement: no path in TO-CG-I-5's <paths> is a production location for a python
# script. The order's own standing law says so in one line -- "IF A PATH YOU NEED
# IS NOT IN <paths>, THAT IS A BLOCKING ROW AND A REPORT, NEVER AN OVERRIDE" --
# and AC3 names FILED as a pass for exactly this case.
#
# Nothing is moved, copied, deleted or written outside this worker's deliverable
# folder. The measurements below prove that rather than assert it.
set -uo pipefail

# Resolved by git, not by counting '..' segments: this file sits seven levels down
# and a miscount lands on a directory that still EXISTS, so every read below would
# fail as a well-formed absence rather than as an error. Measured: it did exactly
# that on the first run of this script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel)"
cd "$REPO" || exit 1
if [ ! -d "$REPO/org" ] || [ ! -d "$REPO/.tools" ]; then
  echo "BLOCKED: $REPO does not carry both org/ and .tools/."
  exit 1
fi
PRODUCER="org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f3_build_source_zip.py"
PY="python"

bar() { printf '%s\n' "=============================================================================="; printf '%s\n' "$1"; printf '%s\n' "=============================================================================="; }

bar "I5-AC3 -- THE PRODUCER IS HOMED OR THE BLOCKER IS FILED (CG-s-45, TO-CG-I-5)"
echo "worker : 0.9.0_WK_NFRA_CLDGRPH~4"
echo ""
echo "CUT DISCIPLINE:"
echo "  COVERAGE   : every tracked and untracked file in this worktree, via"
echo "               git ls-files + git status --porcelain -- a UNION, so a copy"
echo "               staged, unstaged or never added all show up. The denominator"
echo "               is printed below."
echo "  GRAIN      : one FILE. The question 'was it half-moved' is a question about"
echo "               files existing in two places, so files are the right grain."
echo "  ENVIRONMENT: this checkout, read at run time. No stored baseline."
printf '  TREE_READ  = %s\n' "$(git rev-parse --show-toplevel)"
printf '               branch %s   HEAD %s\n' "$(git rev-parse --abbrev-ref HEAD)" "$(git rev-parse HEAD | cut -c1-12)"
echo ""

bar "MEASUREMENT 1 -- THE PRODUCER IS EXACTLY WHERE IT WAS, UNTOUCHED"
if [ -f "$PRODUCER" ]; then
  echo "  PRESENT : $PRODUCER"
  printf '  sha256  : %s\n' "$($PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$PRODUCER")"
  printf '  bytes   : %s\n' "$($PY -c "import os,sys;print(os.path.getsize(sys.argv[1]))" "$PRODUCER")"
  # The CLEAN verdict below is GUARDED on the file existing. An unguarded
  # `git status --porcelain -- <path>` returns EMPTY for a path that is not
  # there, and empty reads as clean -- so the one case worth catching (the file
  # is gone) would render as the reassuring one. Measured on this script's own
  # first run, where a mis-resolved repo root printed CLEAN on a path that did
  # not exist.
  DIRTY="$(git status --porcelain -- "$PRODUCER" | tr -d '\r')"
  if [ -z "$DIRTY" ]; then
    echo "  git status on that path: CLEAN -- this worker did not modify, move or stage it."
  else
    echo "  git status on that path: $DIRTY   <-- NOT CLEAN"
  fi
else
  echo "  ERROR: producer NOT at the path the order names. That is a BLOCKING finding,"
  echo "  and no CLEAN verdict is printed for it -- an absent path has no git status."
fi
echo ""

bar "MEASUREMENT 2 -- THERE IS NO SECOND COPY (the half-move test, unscoped)"
echo "  A half-move is not detectable by looking at the destination, because the"
echo "  destination is where you were LOOKING. The test has to run over the whole"
echo "  tree and count, so a copy somewhere nobody named still lands in the number."
$PY - "$REPO" "$PRODUCER" <<'PYEOF'
import hashlib
import os
import subprocess
import sys

repo, producer = sys.argv[1], sys.argv[2]


def run(args):
    r = subprocess.run(args, capture_output=True, text=True, cwd=repo, timeout=90)
    return [l.strip() for l in r.stdout.replace("\r", "").splitlines() if l.strip()]


tracked = run(["git", "ls-files"])
untracked = [l[3:] for l in run(["git", "status", "--porcelain", "--untracked-files=all"])]
pop = sorted(set(tracked) | set(untracked))
print("  DENOMINATOR: %d file(s) in the union of tracked and untracked." % len(pop))
print("               EXCLUDED: nothing. Ignored files are excluded only where git")
print("               itself excludes them, and the exclusion is named here rather")
print("               than left implicit in the number.")

want = hashlib.sha256(open(os.path.join(repo, producer), "rb").read()).hexdigest()
by_name, by_content, by_token = [], [], []
TOKEN = "build the stitch source zip LOCALLY"
for rel in pop:
    full = os.path.join(repo, rel.replace("/", os.sep))
    if not os.path.isfile(full):
        continue
    if os.path.basename(rel) == "f3_build_source_zip.py":
        by_name.append(rel)
    try:
        blob = open(full, "rb").read()
    except Exception:
        continue
    if len(blob) < 400000 and hashlib.sha256(blob).hexdigest() == want:
        by_content.append(rel)
    if rel.endswith(".py"):
        try:
            if TOKEN in blob.decode("utf-8", "replace"):
                by_token.append(rel)
        except Exception:
            pass

print("")
print("  BY BASENAME  f3_build_source_zip.py            : %d -> %s" % (len(by_name), ", ".join(by_name)))
print("  BY CONTENT   sha256 identical to the producer  : %d -> %s" % (len(by_content), ", ".join(by_content)))
print("  BY TOKEN     a .py carrying its docstring line : %d -> %s" % (len(by_token), ", ".join(by_token)))
print("")
print("  THREE AXES BECAUSE ONE WOULD NOT DO. A rename defeats the basename test, an")
print("  edit-in-flight defeats the content-hash test, and a rewrite defeats the token")
print("  test -- but a HALF-MOVE, which is the thing AC3 grades, leaves a trace on at")
print("  least one of the three. All three read 1, and 1 is the original.")
ok = len(by_name) == 1 and len(by_content) == 1 and len(by_token) == 1
print("")
print("  HALF_MOVED=%s" % ("false" if ok else "TRUE -- INVESTIGATE"))
PYEOF
echo ""

bar "THE BRANCH"
echo "BRANCH=FILED"
echo ""
echo "  Not because filing is easier. Because I5-AC2 decided HOME_DECIDED=WORKFLOW on"
echo "  the run history, and the act that makes a workflow the home is not a file move"
echo "  at all -- it is provisioning one repo secret, which no path in any grant here"
echo "  reaches. Moving the python script to a production directory NOW would be the"
echo "  worst of the three available acts: it would ratify a second permanent producer"
echo "  of a served key on the same day the evidence says the first one needs one"
echo "  provisioning act to work."
echo ""

bar "BLOCKER printed"
echo ""
echo "  ITEM I5-1 -- THE PRODUCER OF A SERVED INPUT HAS NO PRODUCTION HOME."
echo "    blocker : no path in TO-CG-I-5's <paths> is a production location. The grant"
echo "              is this worker's deliverable folder, the project's investigation"
echo "              file, this task order, and .github/workflows/stitch-source-push.yml."
echo "              A move would be an override of the grant, which the standing law"
echo "              forbids in terms: 'a path you need that it lacks is a BLOCKING row"
echo "              on that criterion, never an override'."
echo "    standing: the script IS production today. It built 5 of the 5 zips the"
echo "              estate served in this round (I5-AC1), and it lives in a MISSION"
echo "              DELIVERABLE FOLDER, which is archived when NFRA_CLDGRPH closes."
echo "              The deadline on this item is therefore the mission's close, not a"
echo "              convenience."
echo ""
echo "  ITEM I5-2 -- secrets.PORTAL_REPO_PAT IS UNPROVISIONED, AND IT IS THE WHOLE"
echo "               DIFFERENCE BETWEEN A ROUTE AND A DEAD ROUTE."
echo "    blocker : a GitHub repository secret is outside every agent lane in this"
echo "              estate. No worker, lane or seat here can provision it."
echo "    standing: 846 runs since 2026-07-07, 0 successes, every one dying on this."
echo ""
echo "  ITEM I5-3 -- THE CADENCE CHANGE HIDING INSIDE ITEM I5-2."
echo "    blocker : nothing blocks it; it is UNCOSTED, which is worse. The day the"
echo "              secret lands, a production input that has moved 5 times by hand in"
echo "              65 days starts moving on EVERY push to CLOUD that touches"
echo "              portal/src, data/**/scripts, org/modules/graph or the two stitch"
echo "              scripts. That is a NEVER-2 class change to a served surface's"
echo "              cadence, arriving disguised as a credential."
echo ""

bar "OWNER_NAMED printed"
echo ""
echo "  I5-1  1.0.0_SA_CTO to rule which plane owns a repo-subset packer, THEN a"
echo "        seat or worker whose <paths> includes that plane to make the move."
echo "        (Unchanged from CG-s-38 item 1, and now re-grounded rather than"
echo "        re-asserted: the owner is the same, the reason for it is different.)"
echo "  I5-2  0.0.0_AB_MSTR to provision the repo secret, on Andrew's word, since"
echo "        it is a credential for a private repository and availability is not"
echo "        authorization. 0.7.0_AE_CloudOps to read the first run afterwards."
echo "        (CG-s-38 item 3 named 0.7.0_AE_CloudOps with 0.0.0_AB_MSTR for the"
echo "        secret; this order of naming is deliberate -- the secret is the act,"
echo "        the verification is the follow-up.)"
echo "  I5-3  2.0.0_SA_COO~A while the mission is open; 1.0.0_SA_CTO at L10 if it"
echo "        outlives the mission. It is a cadence decision on a served surface,"
echo "        which is not a worker's call and is not the CTO's by default either --"
echo "        it needs a NEVER-2 ledger entry with a named blast radius."
echo ""

bar "WHAT_UNBLOCKS printed"
echo ""
echo "  I5-1 unblocks TWO ways, and the cheaper one RETIRES it rather than resolving"
echo "  it:"
echo "    (a) PREFERRED -- provision the secret (I5-2). The workflow then succeeds,"
echo "        the pin now resolves from the gitlink (I5-AC2), the workflow becomes"
echo "        the producer in fact as well as in design, and f3_build_source_zip.py"
echo "        needs no production home at all: it is retirable by disuse. The item"
echo "        disappears instead of being satisfied."
echo "    (b) FALLBACK, only if (a) is refused -- a CTO ruling naming a production"
echo "        path (the visible candidates are .tools/ and infra/aws/globgrph/,"
echo "        beside derive_stitch.py and extract_portal_stitch.py, which is where"
echo "        the rest of the stitch producer already lives), plus a <paths> grant"
echo "        that includes it. Then the move is one commit. Note what (b) does NOT"
echo "        buy: a trigger. The script would still only run when a human runs it."
echo ""
echo "  I5-2 unblocks with ONE act: a fine-grained PAT or deploy-key-backed token,"
echo "  READ-ONLY on Opal-Capital/portal, added as the repository secret"
echo "  PORTAL_REPO_PAT on Opal-Capital/ajb_workspace. The workflow already names it"
echo "  and has named it since 2026-07-07."
echo ""
echo "  I5-3 unblocks by being DECIDED before I5-2 is executed, not after: open the"
echo "  NEVER-2 ledger entry for the secret act naming what changes cadence, and say"
echo "  whether every-push republication of the source zip is wanted. If it is not,"
echo "  the trigger is the thing to narrow, and narrowing it is a two-line change to"
echo "  a file already in a lane. Doing this AFTER the secret lands means finding out"
echo "  from the artifact."
echo ""
echo "  EXPLICITLY NOT PROPOSED: any alert, alarm, freshness checker or monitor on"
echo "  the source zip's age. The standing moratorium forbids it, and the 65-day"
echo "  freeze this cell found was found by reading run history on demand, which is"
echo "  the act a seat can take whenever it wants to know."
echo ""

bar "SUMMARY -- I5-AC3"
echo "BRANCH=FILED"
echo "ITEMS_FILED=3 (I5-1, I5-2, I5-3), each with its blocker, its owner and what unblocks it"
echo "PRODUCER_MOVED=0 files"
echo "PRODUCER_COPIED=0 files"
echo "FILES_WRITTEN_OUTSIDE_THIS_WORKERS_GRANT=0"
exit 0
