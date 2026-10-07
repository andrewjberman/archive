#!/usr/bin/env bash
# OG-rl-9 PHASE A step 7 (R18, row Z-W15-S51): the PRE-GO exercise of rl9.AC1.sh, rl9.AC2.sh and rl9.AC3.sh against the r23 release.
# Builds a SCRATCH worktree (branch x23b, never merged, plumbing commit, no hook) from the wk head, with the POST-DEPLOY state standing in:
#   manifest deployed_commit = the release sha; a ledger entry file; no sentinel; GA1_DOWNLOAD.json / GA1_QUERY.json = the host's own answer of the STAGED release rehearsal (r23b_ssm.py real after_stage --json .scratch/x23bjson).
# AC1's ssm md5 answer is STOOD IN by .scratch/fakeaws, which prints ONLY the md5 lines the real host prints (a file the host does not have prints nothing: r23b_host_tests_absent.out). AC1's floor reads the REAL host.
# AC2 and AC3 verify the digest against the REAL ssm invocation of the staged rehearsal (get-command-invocation).
# usage: bash r23b_step7.sh <release sha, 40 hex>     (run from the wk worktree root; writes r23b_rl9.* .out files beside this script)
set -u
REL="$1"
W="$(git rev-parse --show-toplevel)"; D="$W/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r23/checks"
WD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
S="$W/.scratch/x23b"; WKHEAD="$(git rev-parse HEAD)"
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x23b HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools org infra/aws/ec2 lib >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
mkdir -p "$W/.scratch/fakeaws"
cat > "$W/.scratch/fakeaws/aws" <<'FAKE'
#!/usr/bin/env bash
# STAND-IN for `aws` in the step-7 exercise ONLY: answers the SSM calls rl9.AC1.sh's ssm_run makes with what the host prints AFTER the deploy for
# `md5sum <files>`: the md5 line of each file the HOST HAS (the release md5 of the 4 shipped files: integration.py, rivalfunds_view.py, server.py, app/tests/test_rivalfunds_view.py); a file the host does not have
# (tests/...) prints nothing on stdout. Every other aws call (the floor's reads included) falls through to the real shim.
case "$*" in
  *"ssm send-command"*"md5sum"*) echo "fake-command-id"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"--query Status"*) echo "Success"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"StandardOutputContent"*) for f in app/integrations/schwab/integration.py app/rivalfunds_view.py app/server.py app/tests/test_rivalfunds_view.py; do grep "  $f\$" "$FAKE_MD5_LIST"; done; exit 0 ;;
esac
FD="$(cd "$(dirname "$0")" && pwd)"; PATH="${PATH//$FD:/}"   # drop this fake from PATH, or the real shim finds it again and loops
exec "$(dirname "$0")/../../.tools/aws" "$@"
FAKE
chmod +x "$W/.scratch/fakeaws/aws"
cd "$S" || exit 9
git read-tree --reset -u "$WKHEAD" || exit 9   # the scratch tree = the CURRENT worker head (an earlier exercise may have left it on an older base)
python - "$REL" "$W/.scratch/x23bjson" "$D" <<'PY'
import re, shutil, sys
rel, src, d = sys.argv[1], sys.argv[2], sys.argv[3]
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
for f in ("GA1_DOWNLOAD.json", "GA1_QUERY.json"):
    shutil.copyfile(src + "/" + f, "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/" + f)
PY
echo "exercise ledger entry (scratch only)" > org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-release-r23_deploy_completion.md
git add -f infra/aws/ec2/EC2_MANIFEST.json "$WD/GA1_DOWNLOAD.json" "$WD/GA1_QUERY.json" org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-release-r23_deploy_completion.md
# the ledger is CLOSED in the post-deploy state this clone stands in for: the OPEN sentinel (committed at the worker head) is removed from the scratch index
git rm -q --cached -f org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-r23.json
T=$(git write-tree); P="$WKHEAD"
N=$(echo "x23b scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, sentinel removed (ledger closed), GA1_DOWNLOAD/GA1_QUERY = the staged rehearsal's host answers" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x23b "$N"
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])" | tr -d '\r')"
export FAKE_MD5_LIST="$D/r23b_release_md5.txt"
# rl9.AC1.sh is exercised AS THE ISSUER AMENDED IT (the shipped list already excludes the source-only ^tests/ files, per the order's A2): no corrected copy
{
echo "### rl9.AC1.sh EXPECTED-PASS FORM (the issuer's amended script as written), scratch clone x23b @ $(git rev-parse --short HEAD); fake aws as above; floor reads the REAL host"
SECONDS=0; PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 600 bash "$C/rl9.AC1.sh"; echo "exit=$? (${SECONDS}s)"
} > "$D/r23b_rl9.AC1_expected_pass_form.out" 2>&1
{
echo "### rl9.AC1.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live 9d3e2eb3fc: the 4 shipped files differ from the release bytes)"
SECONDS=0; timeout 600 bash "$C/rl9.AC1.sh"; echo "exit=$? (${SECONDS}s)"
echo
echo "### rl9.AC1.sh NEGATIVE CONTROL 2: the real pre-act worktree (manifest = live 9d3e2eb3fc; no ledger entry), real host"
( cd "$W" && SECONDS=0; timeout 600 bash "$C/rl9.AC1.sh"; echo "exit=$? (${SECONDS}s)" )
} > "$D/r23b_rl9.AC1_negative_controls.out" 2>&1
{
echo "### rl9.AC2.sh EXPECTED-PASS FORM: scratch clone x23b (GA1_DOWNLOAD.json = the host's answer of the STAGED release rehearsal; digest checked against that real ssm invocation)"
timeout 120 bash "$C/rl9.AC2.sh"; echo "exit=$?"
} > "$D/r23b_rl9.AC2_expected_pass_form.out" 2>&1
{
echo "### rl9.AC2.sh NEGATIVE CONTROL: the real pre-act worktree (GA1_DOWNLOAD.json = the r22 record: 23 unheld blank rows)"
( cd "$W" && timeout 120 bash "$C/rl9.AC2.sh"; echo "exit=$?" )
} > "$D/r23b_rl9.AC2_negative_control.out" 2>&1
{
echo "### rl9.AC3.sh EXPECTED-PASS FORM: scratch clone x23b (GA1_DOWNLOAD.json + GA1_QUERY.json = the host's answers of the STAGED release rehearsal; both digests are in that real ssm invocation's output)"
timeout 120 bash "$C/rl9.AC3.sh"; echo "exit=$?"
} > "$D/r23b_rl9.AC3_expected_pass_form.out" 2>&1
{
echo "### rl9.AC3.sh NEGATIVE CONTROL 1: the real pre-act worktree (GA1_QUERY.json absent)"
( cd "$W" && timeout 120 bash "$C/rl9.AC3.sh"; echo "exit=$?" )
echo
echo "### rl9.AC3.sh NEGATIVE CONTROL 2: the same scratch clone with GA1_DOWNLOAD.json / GA1_QUERY.json replaced by the BEFORE run's host answers on live code (23 blank rows; digests are in that real ssm invocation)"
python - "$D" <<'PY'
import json, re, sys
d = sys.argv[1]
t = open(d + "/r23b_before_real.out", encoding="utf-8").read()
cid = re.search(r"^ssm (\S+) status", t, re.M).group(1)
for tag, fn in (("GA1_BODY ", "GA1_DOWNLOAD.json"), ("GA1Q_BODY ", "GA1_QUERY.json")):
    b = json.loads(re.search(r"^" + tag + r"(\{.*\})$", t, re.M).group(1))
    open("org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/" + fn, "w", encoding="utf-8", newline="\n").write(
        json.dumps({"body": b, "instance_id": "i-07dccb1615503ac99", "ssm_command_id": cid}, indent=1, sort_keys=True) + "\n")
PY
timeout 120 bash "$C/rl9.AC3.sh"; echo "exit=$?"
} > "$D/r23b_rl9.AC3_negative_controls.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
tos = open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-9.gateway-release-r23.md", encoding="utf-8").read()
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', tos, re.S))
rows = [("AC1", "r23b_rl9.AC1_expected_pass_form.out", True, "expected-PASS form, the script as amended"),
        ("AC1", "r23b_rl9.AC1_negative_controls.out", False, "negative controls 1 and 2"),
        ("AC2", "r23b_rl9.AC2_expected_pass_form.out", True, "expected-PASS form"),
        ("AC2", "r23b_rl9.AC2_negative_control.out", False, "negative control"),
        ("AC3", "r23b_rl9.AC3_expected_pass_form.out", True, "expected-PASS form"),
        ("AC3", "r23b_rl9.AC3_negative_controls.out", False, "negative controls 1 and 2")]
out = []
for cid, fn, want, note in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("### "))
    m = re.search(exp[cid], body) is not None
    out.append("%s %s (%s): re.search(<expect>) %s -> %s (must %s)" % (cid, fn, note, "MATCH" if m else "NO MATCH", "OK" if m == want else "WRONG", "MATCH" if want else "NOT match"))
open(D + "/r23b_expect_match.out", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
PY
