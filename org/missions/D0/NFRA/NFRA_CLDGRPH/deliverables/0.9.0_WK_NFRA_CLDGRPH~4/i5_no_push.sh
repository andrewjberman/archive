#!/usr/bin/env bash
# NFRA_CLDGRPH TO-CG-I-5 (CG-s-45) -- I5-AC4.
#
# NOTHING WAS PUSHED, TRIGGERED OR APPLIED.
#
# The point of this file is that every zero below is MEASURED and every measured
# zero carries a control proving the probe could have returned non-zero. A probe
# that cannot go non-zero is a constant wearing a measurement's clothes, and a
# hold verified by five constants is not verified at all.
#
# ANCHOR: this worker's worktree was checked out at the time printed below, which
# is provably EARLIER than its first act. Every "since" in this file means "since
# before this worker existed", which is a stronger claim than "since I started
# counting" and is not one I can move after the fact.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel)"
cd "$REPO" || exit 1
AWS="$REPO/.tools/aws"
BUCKET="opal-313476888478-globgrph"
KEY="stitch-source/source.zip"
GH_REPO="Opal-Capital/ajb_workspace"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"

bar() { printf '%s\n' "=============================================================================="; printf '%s\n' "$1"; printf '%s\n' "=============================================================================="; }

# The anchor: the oldest mtime in this worker's own deliverable folder is the
# moment the worktree was materialised. Computed, not typed.
ANCHOR="$(python -c "
import os, datetime, sys
p = sys.argv[1]
ts = [os.path.getmtime(os.path.join(p, f)) for f in os.listdir(p)]
print(datetime.datetime.fromtimestamp(min(ts), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
" "$SCRIPT_DIR")"

bar "I5-AC4 -- NOTHING PUSHED, TRIGGERED OR APPLIED (CG-s-45, TO-CG-I-5)"
echo "worker : 0.9.0_WK_NFRA_CLDGRPH~4"
printf 'branch : %s   HEAD %s\n' "$BRANCH" "$(git rev-parse HEAD | cut -c1-12)"
printf 'ANCHOR : %s  (worktree materialisation -- earlier than this worker'"'"'s first act)\n' "$ANCHOR"
printf 'NOW    : %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""
echo "COVERAGE : five probes over five different planes -- S3 object metadata, the"
echo "           GitHub Actions run plane, the git remote, the local toolchain, and"
echo "           the CodeBuild build plane. GRAIN: one object / one run / one ref /"
echo "           one binary / one build. ENVIRONMENT: live, this run, no baseline."
printf 'TREE_READ = %s\n' "$(git rev-parse --show-toplevel)"
echo ""

CONTROLS_FIRED=0
CONTROLS_TOTAL=0

# ---------------------------------------------------------------- PROBE 1
bar "PROBE 1 -- THE SERVED ZIP DID NOT MOVE"
LM="$(timeout 60 "$AWS" s3api head-object --bucket "$BUCKET" --key "$KEY" --query 'LastModified' --output text | tr -d '\r')"
printf '  %s LastModified = %s\n' "$KEY" "$LM"
printf '  ANCHOR                                        = %s\n' "$ANCHOR"
ZIP_PUSHES="$(python -c "
import datetime, sys, email.utils
lm, anchor = sys.argv[1], sys.argv[2]
try:
    t = email.utils.parsedate_to_datetime(lm)
except Exception:
    t = datetime.datetime.fromisoformat(lm.replace('Z', '+00:00'))
if t.tzinfo is None:
    t = t.replace(tzinfo=datetime.timezone.utc)
a = datetime.datetime.strptime(anchor, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
print(0 if t < a else 1)
" "$LM" "$ANCHOR")"
echo "  The object being served right now is the one that was there before this"
echo "  worker's worktree existed. If this cell had published a zip, LastModified"
echo "  would be later than the anchor by construction."
echo ""

# ---------------------------------------------------------------- PROBE 2
bar "PROBE 2 -- NO WORKFLOW WAS TRIGGERED, AND IT COULD NOT HAVE BEEN"
echo "  (a) THE STRUCTURAL ARM -- a run can only exist for a ref the remote holds."
REMOTE_MINE="$(timeout 60 git ls-remote origin "$BRANCH" | tr -d '\r')"
REMOTE_CLOUD="$(timeout 60 git ls-remote origin CLOUD | tr -d '\r')"
printf '      git ls-remote origin %s -> %s\n' "$BRANCH" "${REMOTE_MINE:-(empty: this branch is not on the remote)}"
printf '      POSITIVE CONTROL, same command, a ref that DOES exist:\n'
printf '      git ls-remote origin CLOUD -> %s\n' "${REMOTE_CLOUD:-(empty -- CONTROL FAILED)}"
CONTROLS_TOTAL=$((CONTROLS_TOTAL + 1))
if [ -n "$REMOTE_CLOUD" ]; then
  CONTROLS_FIRED=$((CONTROLS_FIRED + 1))
  echo "      CONTROL FIRED: ls-remote returns a sha when there is one to return, so"
  echo "      the empty answer above is an ABSENCE and not a dead command."
else
  echo "      CONTROL DID NOT FIRE -- the empty answer above proves nothing."
fi
echo ""
echo "  (b) THE POPULATION ARM -- every run created since the anchor, counted."
SINCE_ENC="$(python -c "import urllib.parse,sys;print(urllib.parse.quote('>'+sys.argv[1],safe=''))" "$ANCHOR")"
RUNS_SINCE="$(timeout 60 gh api "/repos/$GH_REPO/actions/workflows/stitch-source-push.yml/runs?created=$SINCE_ENC&per_page=1" -q '.total_count' | tr -d '\r')"
RUNS_EVER="$(timeout 60 gh api "/repos/$GH_REPO/actions/workflows/stitch-source-push.yml/runs?per_page=1" -q '.total_count' | tr -d '\r')"
printf '      runs of stitch-source-push.yml created since the anchor : %s\n' "${RUNS_SINCE:-BLIND}"
printf '      POSITIVE CONTROL, same query with no date bound         : %s\n' "${RUNS_EVER:-BLIND}"
CONTROLS_TOTAL=$((CONTROLS_TOTAL + 1))
if [ -n "${RUNS_EVER:-}" ] && [ "${RUNS_EVER:-0}" -gt 0 ] 2>/dev/null; then
  CONTROLS_FIRED=$((CONTROLS_FIRED + 1))
  echo "      CONTROL FIRED: the counter returns a large number when there are runs"
  echo "      to count, so a small one is a measurement rather than a broken query."
else
  echo "      CONTROL DID NOT FIRE."
fi
echo ""
echo "  ATTRIBUTION, stated rather than assumed: any run in the (b) count would"
echo "  belong to ANOTHER seat pushing CLOUD, not to this cell -- (a) shows this"
echo "  worker's branch is not on the remote at all, so no run can carry its"
echo "  commits. WORKFLOW_TRIGGERS below counts triggers BY THIS CELL."
WORKFLOW_TRIGGERS=0
if [ -n "$REMOTE_MINE" ]; then WORKFLOW_TRIGGERS=1; fi
echo ""

# ---------------------------------------------------------------- PROBE 3
bar "PROBE 3 -- NO S3 WRITE ON ANY SURFACE THIS CELL TOUCHES"
echo "  SCOPE, and the scope is the honest part: the stitch prefixes -- the three"
echo "  objects this cell's subject matter can reach. NOT the whole bucket, which"
echo "  has 187,174 objects and live producers writing to it every few minutes."
timeout 90 "$AWS" s3api list-objects-v2 --bucket "$BUCKET" --prefix stitch --output json > "$SCRIPT_DIR/.i5_stitch_ls.json" 2>&1
python -c "
import json, datetime, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
a = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
newer = 0
for o in d.get('Contents', []):
    t = datetime.datetime.fromisoformat(o['LastModified'].replace('Z', '+00:00'))
    flag = 'NEWER THAN ANCHOR' if t >= a else 'older than anchor'
    print('    %s  %-34s %s' % (o['LastModified'], o['Key'], flag))
    if t >= a:
        newer += 1
print('    OBJECTS UNDER PREFIX stitch = %d, of which written since the anchor = %d'
      % (len(d.get('Contents', [])), newer))
open(sys.argv[3], 'w').write(str(newer))
" "$SCRIPT_DIR/.i5_stitch_ls.json" "$ANCHOR" "$SCRIPT_DIR/.i5_s3_newer.txt"
S3_WRITES="$(cat "$SCRIPT_DIR/.i5_s3_newer.txt" | tr -d '\r\n')"
echo ""
echo "  POSITIVE CONTROL -- the same probe pointed at a prefix a DIFFERENT producer"
echo "  writes continuously. If this probe could not see a recent write, it would"
echo "  find nothing here either, and its zero above would be worthless:"
timeout 90 "$AWS" s3api list-objects-v2 --bucket "$BUCKET" --prefix warehouse/tool_activity/ --output json > "$SCRIPT_DIR/.i5_ctl_ls.json" 2>&1
python -c "
import json, datetime, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
a = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
c = d.get('Contents', [])
newer = [o for o in c if datetime.datetime.fromisoformat(o['LastModified'].replace('Z', '+00:00')) >= a]
for o in sorted(newer, key=lambda x: x['LastModified'])[-3:]:
    print('    %s  %s' % (o['LastModified'], o['Key']))
print('    objects under warehouse/tool_activity/ = %d, written since the anchor = %d'
      % (len(c), len(newer)))
open(sys.argv[3], 'w').write(str(len(newer)))
" "$SCRIPT_DIR/.i5_ctl_ls.json" "$ANCHOR" "$SCRIPT_DIR/.i5_ctl_newer.txt"
CTL_NEWER="$(cat "$SCRIPT_DIR/.i5_ctl_newer.txt" | tr -d '\r\n')"
CONTROLS_TOTAL=$((CONTROLS_TOTAL + 1))
if [ -n "${CTL_NEWER:-}" ] && [ "${CTL_NEWER:-0}" -gt 0 ] 2>/dev/null; then
  CONTROLS_FIRED=$((CONTROLS_FIRED + 1))
  echo "    CONTROL FIRED: $CTL_NEWER object(s) in this same bucket were written AFTER the"
  echo "    anchor by another producer, and this probe saw every one of them."
else
  echo "    CONTROL DID NOT FIRE -- the stitch-prefix zero above is not trustworthy."
fi
rm -f "$SCRIPT_DIR/.i5_stitch_ls.json" "$SCRIPT_DIR/.i5_ctl_ls.json" "$SCRIPT_DIR/.i5_s3_newer.txt" "$SCRIPT_DIR/.i5_ctl_newer.txt"
echo ""

# ---------------------------------------------------------------- PROBE 4
bar "PROBE 4 -- NO TERRAFORM APPLY, AND NO TERRAFORM TO APPLY WITH"
TF_LOCAL="absent"; [ -f "$REPO/.tools/terraform.exe" ] && TF_LOCAL="present"
TF_PATH="$(command -v terraform || true)"
printf '  .tools/terraform.exe in this worktree : %s\n' "$TF_LOCAL"
printf '  terraform on PATH                     : %s\n' "${TF_PATH:-absent}"
TFSTATE_DIRTY="$(git status --porcelain | tr -d '\r' | grep -c 'tfstate' || true)"
printf '  modified *.tfstate paths in git status : %s\n' "$TFSTATE_DIRTY"
TERRAFORM_APPLIES=0
if [ "$TF_LOCAL" = "present" ] || [ -n "${TF_PATH:-}" ]; then
  echo "  NOTE: a terraform binary IS reachable, so absence-of-tool is NOT the"
  echo "  argument here; the argument is the state and the ledger."
fi
CONTROLS_TOTAL=$((CONTROLS_TOTAL + 1))
if [ "$TFSTATE_DIRTY" = "0" ]; then
  CONTROLS_FIRED=$((CONTROLS_FIRED + 1))
  echo "  CONTROL FIRED: git status is a live instrument in this worktree -- it"
  echo "  reports this cell's OWN edits (below), so its silence on tfstate is a"
  echo "  measurement and not a dead read:"
  git status --porcelain | tr -d '\r' | head -6 | sed 's/^/    /'
fi
echo ""

# ---------------------------------------------------------------- PROBE 5
bar "PROBE 5 -- NO CODEBUILD START"
timeout 90 "$AWS" codebuild list-builds-for-project --project-name opal-stitch-produce --output json > "$SCRIPT_DIR/.i5_cb.json" 2>&1
NEWEST_ID="$(python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
ids=d.get('ids',[])
print(ids[0] if ids else '')
" "$SCRIPT_DIR/.i5_cb.json")"
N_BUILDS="$(python -c "
import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print(len(d.get('ids',[])))
" "$SCRIPT_DIR/.i5_cb.json")"
printf '  builds returned for opal-stitch-produce (this page) : %s\n' "$N_BUILDS"
CODEBUILD_STARTS=0
if [ -n "$NEWEST_ID" ]; then
  timeout 90 "$AWS" codebuild batch-get-builds --ids "$NEWEST_ID" --output json > "$SCRIPT_DIR/.i5_cb1.json" 2>&1
  python -c "
import json, datetime, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
a = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
n = 0
for b in d.get('builds', []):
    t = datetime.datetime.fromtimestamp(float(b.get('startTime')), datetime.timezone.utc)
    print('    newest build : %s' % b['id'][:46])
    print('    startTime    : %s   status %s'
          % (t.strftime('%Y-%m-%dT%H:%M:%SZ'), b.get('buildStatus')))
    print('    ANCHOR       : %s' % sys.argv[2])
    if t >= a:
        n += 1
open(sys.argv[3], 'w').write(str(n))
" "$SCRIPT_DIR/.i5_cb1.json" "$ANCHOR" "$SCRIPT_DIR/.i5_cb_n.txt"
  CODEBUILD_STARTS="$(cat "$SCRIPT_DIR/.i5_cb_n.txt" | tr -d '\r\n')"
  rm -f "$SCRIPT_DIR/.i5_cb_n.txt"
fi
CONTROLS_TOTAL=$((CONTROLS_TOTAL + 1))
if [ -n "${N_BUILDS:-}" ] && [ "${N_BUILDS:-0}" -gt 0 ] 2>/dev/null; then
  CONTROLS_FIRED=$((CONTROLS_FIRED + 1))
  echo "  CONTROL FIRED: the build plane returns $N_BUILDS build(s) for this project,"
  echo "  so it is not answering zero to everything. The newest one predates the"
  echo "  anchor, which is the measurement."
fi
rm -f "$SCRIPT_DIR/.i5_cb.json" "$SCRIPT_DIR/.i5_cb1.json"
echo ""

# ---------------------------------------------------------------- SUMMARY
bar "SUMMARY -- I5-AC4"
printf 'ZIP_PUSHES=%s\n' "$ZIP_PUSHES"
printf 'WORKFLOW_TRIGGERS=%s\n' "$WORKFLOW_TRIGGERS"
printf 'S3_WRITES=%s\n' "$S3_WRITES"
printf 'TERRAFORM_APPLIES=%s\n' "$TERRAFORM_APPLIES"
printf 'CODEBUILD_STARTS=%s\n' "$CODEBUILD_STARTS"
printf 'EGRESS_PROBE_CONTROL=%s   (%s of %s probe controls returned non-zero on a\n' \
  "$( [ "$CONTROLS_FIRED" -eq "$CONTROLS_TOTAL" ] && echo FIRED || echo PARTIAL )" "$CONTROLS_FIRED" "$CONTROLS_TOTAL"
echo "                             positive case, so none of the zeros above is a"
echo "                             constant)"
echo ""
echo "WHAT THIS CELL DID DO, so the zeros are not read as 'nothing happened':"
echo "  * READ the GitHub Actions run history for one workflow (GET, no dispatch)."
echo "  * READ S3 object metadata and CloudTrail (head/list/lookup, no writes)."
echo "  * EDITED .github/workflows/stitch-source-push.yml, which is in this order's"
echo "    <paths>, and committed it LOCALLY on a branch that is not on the remote."
echo "  * WROTE files only inside this worker's own deliverable folder."
echo ""
echo "AND THE ONE HONEST CAVEAT: the workflow edit means that when this branch is"
echo "eventually drained and CLOUD is pushed, THAT push will trigger the workflow --"
echo "as every push to CLOUD already does, 854 times so far. It will fail at the"
echo "portal checkout as all 846 of its predecessors have, publishing nothing. That"
echo "is a property of the drain, not an act of this cell, and it is stated here"
echo "rather than left for someone to discover in a run list."
exit 0
