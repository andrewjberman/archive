#!/usr/bin/env bash
# OG-rl-10 PHASE A step 7 (R18, row Z-W15-S51): the PRE-GO exercise of rl10.AC1.sh and rl10.AC2.sh against the r24 release.
# Builds a SCRATCH worktree (branch x24, never merged, plumbing commit, no hook) from the wk head, with the POST-DEPLOY state standing in:
#   manifest deployed_commit = the release sha; a ledger entry file; no sentinel; RL10_LOGIN.json = the host's own answer of the STAGED release rehearsal
#   (run first: R24_STAGE_FROM=<release gateway dir> R24_JSON_DIR=.scratch/x24json python r24_ssm_prog.py r24_login_host.py.txt <out> "after <release sha>").
# AC1's ssm md5 answer is STOOD IN by .scratch/fakeaws, which prints the one md5 line the real host prints for the one shipped file. AC1's floor reads the REAL host.
# AC2 verifies the digest against the REAL ssm invocation of the staged rehearsal (get-command-invocation).
# usage: bash r24_step7.sh <release sha, 40 hex>     (run from the wk worktree root; writes r24_rl10.* .out files beside this script)
set -u
REL="$1"
W="$(git rev-parse --show-toplevel)"; D="$W/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r24/checks"
WD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
S="$W/.scratch/x24"; WKHEAD="$(git rev-parse HEAD)"
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x24 HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools org infra/aws/ec2 lib >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
mkdir -p "$W/.scratch/fakeaws"
cat > "$W/.scratch/fakeaws/aws" <<'FAKE'
#!/usr/bin/env bash
# STAND-IN for `aws` in the step-7 exercise ONLY: answers the SSM calls rl10.AC1.sh's ssm_run makes with what the host prints AFTER the deploy for
# `md5sum <files>`: the md5 line of the ONE shipped file (app/integrations/opal_portal/integration.py, the release md5). Every other aws call
# (the floor's reads included) falls through to the real shim.
case "$*" in
  *"ssm send-command"*"md5sum"*) echo "fake-command-id"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"--query Status"*) echo "Success"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"StandardOutputContent"*) grep "  app/integrations/opal_portal/integration.py\$" "$FAKE_MD5_LIST"; exit 0 ;;
esac
FD="$(cd "$(dirname "$0")" && pwd)"; PATH="${PATH//$FD:/}"   # drop this fake from PATH, or the real shim finds it again and loops
exec "$(dirname "$0")/../../.tools/aws" "$@"
FAKE
chmod +x "$W/.scratch/fakeaws/aws"
cd "$S" || exit 9
git read-tree --reset -u "$WKHEAD" || exit 9   # the scratch tree = the CURRENT worker head
python - "$REL" "$W/.scratch/x24json" "$D" <<'PY'
import re, shutil, sys
rel, src, d = sys.argv[1], sys.argv[2], sys.argv[3]
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
shutil.copyfile(src + "/RL10_LOGIN.json", "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL10_LOGIN.json")
PY
echo "exercise ledger entry (scratch only)" > org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-hotfix-r24_deploy_completion.md
git add -f infra/aws/ec2/EC2_MANIFEST.json "$WD/RL10_LOGIN.json" org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-hotfix-r24_deploy_completion.md
T=$(git write-tree); P="$WKHEAD"
N=$(echo "x24 scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, RL10_LOGIN.json = the staged rehearsal's host answer" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x24 "$N"
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])" | tr -d '\r')"
export FAKE_MD5_LIST="$D/r24_release_md5.txt"
{
echo "### rl10.AC1.sh EXPECTED-PASS FORM, scratch clone x24 @ $(git rev-parse --short HEAD) (manifest deployed_commit = release ${REL:0:10}; ledger entry present; no sentinel); the host's ssm md5 answer is STOOD IN by a fake aws that prints what the REAL host prints; floor reads the REAL host"
SECONDS=0; PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 600 bash "$C/rl10.AC1.sh"; echo "exit=$? (${SECONDS}s)"
} > "$D/r24_rl10.AC1_expected_pass_form.out" 2>&1
{
echo "### rl10.AC1.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live 2c27f3a795: the shipped file differs from the release bytes)"
SECONDS=0; timeout 600 bash "$C/rl10.AC1.sh"; echo "exit=$? (${SECONDS}s)"
echo
echo "### rl10.AC1.sh NEGATIVE CONTROL 2: the real pre-act worktree (manifest = live 2c27f3a795; no ledger entry), real host"
( cd "$W" && SECONDS=0; timeout 600 bash "$C/rl10.AC1.sh"; echo "exit=$? (${SECONDS}s)" )
} > "$D/r24_rl10.AC1_negative_controls.out" 2>&1
{
echo "### rl10.AC2.sh EXPECTED-PASS FORM: scratch clone x24 (RL10_LOGIN.json = the host's answer of the STAGED release rehearsal; digest checked against that real ssm invocation)"
timeout 120 bash "$C/rl10.AC2.sh"; echo "exit=$?"
} > "$D/r24_rl10.AC2_expected_pass_form.out" 2>&1
{
echo "### rl10.AC2.sh NEGATIVE CONTROL 1: the real pre-act worktree (RL10_LOGIN.json absent)"
( cd "$W" && timeout 120 bash "$C/rl10.AC2.sh"; echo "exit=$?" )
echo
echo "### rl10.AC2.sh NEGATIVE CONTROL 2: the same scratch clone with RL10_LOGIN.json replaced by the host's answer on the LIVE installed code (login 403, raw host; digest is in that real ssm invocation)"
cp "$W/.scratch/x24json_neg/RL10_LOGIN.json" "$S/$WD/RL10_LOGIN.json"
timeout 120 bash "$C/rl10.AC2.sh"; echo "exit=$?"
} > "$D/r24_rl10.AC2_negative_controls.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
tos = open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-10.gateway-hotfix-r24-portal-login.md", encoding="utf-8").read()
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', tos, re.S))
rows = [("AC1", "r24_rl10.AC1_expected_pass_form.out", True, "expected-PASS form"),
        ("AC1", "r24_rl10.AC1_negative_controls.out", False, "negative controls 1 and 2"),
        ("AC2", "r24_rl10.AC2_expected_pass_form.out", True, "expected-PASS form"),
        ("AC2", "r24_rl10.AC2_negative_controls.out", False, "negative controls 1 and 2")]
out = []
for cid, fn, want, note in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("### "))
    m = re.search(exp[cid], body) is not None
    out.append("%s %s (%s): re.search(<expect>) %s -> %s (must %s)" % (cid, fn, note, "MATCH" if m else "NO MATCH", "OK" if m == want else "WRONG", "MATCH" if want else "NOT match"))
open(D + "/r24_expect_match.out", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
PY
