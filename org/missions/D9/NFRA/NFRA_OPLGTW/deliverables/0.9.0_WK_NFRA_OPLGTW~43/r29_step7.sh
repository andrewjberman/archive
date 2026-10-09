#!/usr/bin/env bash
# OG-rl-15 PHASE A step 7 (R18, row Z-W15-S51), on the RELEASE sha: the PRE-GO exercise of rl15.AC1.sh (the issuer's, as amended at A7 @4ad91ce013), with a negative control.
# Builds a SCRATCH worktree (branch x29, never merged, plumbing commit, no hook) from the worker head with the POST-DEPLOY, POST-DRAIN-BACK state standing in:
#   manifest deployed_commit = the release sha; a ledger entry file; no sentinel; the release's gateway files overlaid into the INDEX (server.py is kept at box/sitez: the drain-back is a
#   merge, and CT-i-11's three Route lines are CLOUD-only), so `git diff <release> HEAD -- gateway` is exactly the seven A7-listed CLOUD-only paths and the runbook.
# AC1's ssm md5 answer is STOOD IN by .scratch/fakeaws: it prints what the HOST prints after the deploy for `md5sum <files>` (the md5 line of each host file of the release list).
# The floor scripts (rl4.AC1, ht.AC2) read the live host, which still has 51 keys: in the stand-in tree they are replaced by two stubs that print PASS, so AC1's OWN logic is what is exercised;
# the real floor scripts are run separately, in the real tree, against the real host (51-key arm yes, 52-key arm no).
# usage: bash r29_step7.sh <release sha, 40 hex>   (from the worker worktree root)
set -u
REL="$1"
LIVE=aa75078e1b72a28219e6148d3ec8e9bf705ea111
W="$(git rev-parse --show-toplevel)"
WD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~43"
D="$W/$WD"
CD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O"
C="$CD/r32/checks"
S="$W/.scratch/x29"; WKHEAD="$(git rev-parse HEAD)"
G=infra/aws/ec2/opal-gateway
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x29 HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools lib infra/aws/ec2 org/missions/D9/NFRA/NFRA_OPLGTW org/critical_paths/change_management org/critical_paths/.open_deploys >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
mkdir -p "$W/.scratch/fakeaws"
cat > "$W/.scratch/fakeaws/aws" <<'FAKE'
#!/usr/bin/env bash
# STAND-IN for `aws` in the step-7 exercise ONLY: answers the SSM calls rl15.AC1.sh's ssm_run makes with what the host prints AFTER the deploy for `md5sum <files>`.
case "$*" in
  *"ssm send-command"*"md5sum"*) echo "fake-command-id"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"--query Status"*) echo "Success"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"StandardOutputContent"*) cat "$FAKE_MD5_LINES"; exit 0 ;;
esac
FD="$(cd "$(dirname "$0")" && pwd)"; PATH="${PATH//$FD:/}"
exec "$(dirname "$0")/../../.tools/aws" "$@"
FAKE
chmod +x "$W/.scratch/fakeaws/aws"
overlay_checks() {   # after EVERY read-tree: the issuer's amended checks (A7 @4ad91ce013) over the scratch working copies (not committed anywhere by this worker) + the two floor stubs
  git -C "$W" archive 4ad91ce013 "$CD/r32/checks" | tar -x -C "$S" || exit 9
  printf '#!/usr/bin/env bash
echo "stub rl4.AC1: PASS (step-7 stand-in)"; exit 0
' > "$CD/r14/checks/rl4.AC1.sh"
  printf '#!/usr/bin/env bash
echo "stub ht.AC2: PASS (step-7 stand-in)"; exit 0
' > "$CD/hxteams/checks/ht.AC2.sh"
}
cd "$S" || exit 9
git read-tree --reset -u "$WKHEAD" || exit 9
# the issuer's amended checks (A7 @4ad91ce013) overwrite the scratch working copies; they are not committed anywhere by this worker
for f in $(git diff --name-only "$LIVE" "$REL" -- "$G"); do
  case "$f" in "$G/app/server.py") continue ;; esac
  e=$(git ls-tree "$REL" -- "$f"); m=${e%% *}; b=$(echo "$e" | awk '{print $3}')
  git update-index --add --cacheinfo "$m,$b,$f" || exit 9
done
python - "$REL" <<'PY'
import re, sys
rel = sys.argv[1]
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
PY
LEDGER=org/critical_paths/change_management/20261009T0000Z_nfra-oplgtw-gateway-release-r29_deploy_completion.md
echo "exercise ledger entry (scratch only)" > "$LEDGER"
git add -f infra/aws/ec2/EC2_MANIFEST.json "$LEDGER"
git rm -q --cached -f --ignore-unmatch org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-r29.json
T=$(git write-tree); P="$WKHEAD"
N=$(echo "x29 scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, no sentinel, release gateway files overlaid" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x29 "$N"
git read-tree --reset -u "$N"
overlay_checks   # the amended checks and the two floor stubs (scratch copies only)
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])")"
python - "$LIVE" "$REL" "$G" "$D/r29_release_md5.txt" "$W/.scratch/md5_lines.txt" <<'PY'
import subprocess, sys
live, rel, g, lst, out = sys.argv[1:6]
names = subprocess.run(["git", "diff", "--name-only", live, rel, "--", g], capture_output=True, text=True).stdout.split()
host = [n[len(g) + 1:] for n in names]
host = [h for h in host if not h.startswith(("runbooks/", "tests/", "ops/")) and h != "deploy-to-ec2.sh"]
rows = [ln for ln in open(lst, encoding="utf-8") if ln.strip().split("  ", 1)[1] in host]
open(out, "w", encoding="utf-8", newline=chr(10)).writelines(rows)
PY
export FAKE_MD5_LINES="$W/.scratch/md5_lines.txt"
echo "stand-in md5 lines for the host files: $(wc -l < "$FAKE_MD5_LINES")"
{
echo "### rl15.AC1.sh EXPECTED-PASS FORM (the issuer's script as amended at A7, the order's literal invocation), scratch clone x29 @ $(git rev-parse --short HEAD); fake aws as above; floor stubs"
SECONDS=0; PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 600 bash "$C/rl15.AC1.sh"; echo "exit=$? (${SECONDS}s)"
} > "$D/r29_rl15.AC1_expected_pass_form.out" 2>&1
{
echo "### rl15.AC1.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live aa75078e1b: the 11 host files differ from the release bytes), floor stubs"
SECONDS=0; timeout 600 bash "$C/rl15.AC1.sh"; echo "exit=$? (${SECONDS}s)"
} > "$D/r29_rl15.AC1_negative_controls.out" 2>&1
{
echo "### rl15.AC1.sh NEGATIVE CONTROL 2: the stand-in with ONE CLOUD-only path restored to live (a gateway file differing beyond the listed seven): app/mail_route.py reverted to live in the scratch index"
e=$(git ls-tree "$LIVE" -- "$G/app/mail_route.py"); m=${e%% *}; b=$(echo "$e" | awk '{print $3}')
git update-index --add --cacheinfo "$m,$b,$G/app/mail_route.py"
T=$(git write-tree); N2=$(echo "x29 control" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$N"); git update-ref refs/heads/x29 "$N2"
PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 600 bash "$C/rl15.AC1.sh"; echo "exit=$?"
git update-ref refs/heads/x29 "$N"; git read-tree --reset -u "$N"; overlay_checks
} >> "$D/r29_rl15.AC1_negative_controls.out" 2>&1
cd "$W" || exit 9
{
echo "### the REAL floor scripts against the REAL host (still 51 keys), in the real worktree"
echo "-- rl4.AC1 against the 51-name r17b baseline (the host today):"; RL4_ENV_KEYS_BASELINE="$CD/r17/ENV_KEYS_R17B.txt" timeout 300 bash "$CD/r14/checks/rl4.AC1.sh" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"
echo "-- ht.AC2 at 51 keys (the host today):"; HT_ENV_KEYS_COUNT=51 timeout 300 bash "$CD/hxteams/checks/ht.AC2.sh" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"
echo "-- rl4.AC1 against the 52-name r29 baseline (reads NO before the deploy):"; RL4_ENV_KEYS_BASELINE="$CD/r32/ENV_KEYS_R29.txt" timeout 300 bash "$CD/r14/checks/rl4.AC1.sh" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"
echo "-- ht.AC2 at 52 keys (reads NO before the deploy):"; HT_ENV_KEYS_COUNT=52 timeout 300 bash "$CD/hxteams/checks/ht.AC2.sh" 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"
} > "$D/r29_floor_scripts_real.out" 2>&1
echo done
