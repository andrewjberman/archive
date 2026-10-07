#!/usr/bin/env bash
# OG-rl-12 PHASE A step 7 (R18, row Z-W15-S51): the PRE-GO exercise of rl12.AC1.sh and rl12.AC2.sh against the r26 release.
# Builds a SCRATCH worktree (branch x26, never merged, plumbing commit, no hook) from the wk head, with the POST-DEPLOY state standing in:
#   manifest deployed_commit = the release sha; a ledger entry file; no sentinel; RL12_ALLOW.json = the host's own answer of the STAGED rehearsal, taken from the
#   `STEP7_STANDIN` lines that run printed (the same body with installed_code flipped to true, digest printed by the SAME real ssm invocation; a staged run is not the installed code,
#   so Phase B writes its own record from the installed-code run and never uses this).
# AC1's ssm md5 answer is STOOD IN by .scratch/fakeaws, which prints ONLY the md5 lines the real host prints after a deploy for the two shipped files (the release md5 list);
# every other aws call (the floor's reads included) falls through to the real shim. AC2 verifies the digest against the REAL ssm invocation (get-command-invocation).
# usage: bash r26_step7.sh <release sha, 40 hex>     (run from the wk worktree root; writes r26_rl12.* .out files beside this script)
set -u
REL="$1"
W="$(git rev-parse --show-toplevel)"; D="$W/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r26/checks"
WD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
S="$W/.scratch/x26"; WKHEAD="$(git rev-parse HEAD)"
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x26 HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools org infra/aws/ec2 lib >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
mkdir -p "$W/.scratch/fakeaws"
cat > "$W/.scratch/fakeaws/aws" <<'FAKE'
#!/usr/bin/env bash
# STAND-IN for `aws` in the step-7 exercise ONLY: answers the SSM calls rl12.AC1.sh's ssm_run makes with what the host prints AFTER the deploy for `md5sum <files>`: the md5 line of
# each file the HOST HAS (the release md5 list: the FIVE shipped files, A3). Every other aws call (the floor's reads included) falls through to the real shim.
case "$*" in
  *"ssm send-command"*"md5sum"*) echo "fake-command-id"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"--query Status"*) echo "Success"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"StandardOutputContent"*) for f in app/integrations/opal_portal/integration.py app/rivalfunds_view.py app/server.py app/tests/test_rivalfunds_view.py identity_tool_allowlist.txt; do grep "  $f\$" "$FAKE_MD5_LIST"; done; exit 0 ;;
esac
FD="$(cd "$(dirname "$0")" && pwd)"; PATH="${PATH//$FD:/}"   # drop this fake from PATH, or the real shim finds it again and loops
exec "$(dirname "$0")/../../.tools/aws" "$@"
FAKE
chmod +x "$W/.scratch/fakeaws/aws"
# the stand-in record and the NEGATIVE-CONTROL records, parsed from the staged rehearsal's own host output (body line + the ssm command id of that invocation)
python - "$D" "$W/.scratch/x26json" <<'PY'
import json, os, re, sys
d, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
t = open(os.path.join(d, "r26_after_stage_allow.out"), encoding="utf-8").read()
cid = re.search(r"^ssm (\S+) status=Success", t, re.M).group(1)
rec = lambda body: json.dumps({"body": body, "instance_id": "i-07dccb1615503ac99", "ssm_command_id": cid}, indent=1, sort_keys=True) + "\n"
stand = json.loads(re.search(r"^STEP7_STANDIN RL12_BODY (\{.*\})$", t, re.M).group(1))
reh = json.loads(re.search(r"^RL12_REHEARSAL_BODY (\{.*\})$", t, re.M).group(1))
w = lambda fn, s: open(os.path.join(out, fn), "w", encoding="utf-8", newline="\n").write(s)
w("RL12_ALLOW.json", rec(stand))                                   # the stand-in: installed_code flipped
w("RL12_ALLOW.rehearsal.json", rec(reh))                           # control 2: the staged run's TRUE record (installed_code false)
w("RL12_ALLOW.denied.json", rec(dict(stand, status_tool_allowed_for_scoped=False)))   # control 3: the status tool NOT admitted
w("RL12_ALLOW.unnamed.json", rec(dict(stand, unnamed_tool_allowed_for_scoped=True)))  # control 4: an unnamed tool admitted
print("stand-in and 3 control records written from r26_after_stage_allow.out")
PY
cd "$S" || exit 9
git read-tree --reset -u "$WKHEAD" || exit 9   # the scratch tree = the CURRENT worker head (an earlier exercise may have left it on an older base)
# A3: the POST-DRAIN-BACK stand-in. The worker head predates the RIV-rt-1 merge, so its gateway tree lacks the route's 4 files; after the real drain-back CLOUD carries every release file.
# Overlay the release's gateway files (mode and blob from the release commit) into the INDEX only (plumbing; the commit-tree below reads the index), so `git diff <release> HEAD -- gateway`
# is the CLOUD-only runbook alone, exactly as after the drain-back.
G=infra/aws/ec2/opal-gateway
for f in $(git diff --name-only 240ac2fe5abde944f15358ab563cb4b2ab63f09f "$REL" -- "$G"); do
  e=$(git ls-tree "$REL" -- "$f"); m=${e%% *}; b=$(echo "$e" | awk '{print $3}')
  git update-index --add --cacheinfo "$m,$b,$f" || exit 9
done
python - "$REL" "$W/.scratch/x26json" <<'PY'
import re, shutil, sys
rel, src = sys.argv[1], sys.argv[2]
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
shutil.copyfile(src + "/RL12_ALLOW.json", "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL12_ALLOW.json")
PY
echo "exercise ledger entry (scratch only)" > org/critical_paths/change_management/20261007T0000Z_nfra-oplgtw-gateway-release-r26_deploy_completion.md
git add -f infra/aws/ec2/EC2_MANIFEST.json "$WD/RL12_ALLOW.json" org/critical_paths/change_management/20261007T0000Z_nfra-oplgtw-gateway-release-r26_deploy_completion.md
# the ledger is CLOSED in the post-deploy state this clone stands in for: no OPEN sentinel exists in the tree (none was opened at Phase A); make sure of it
git rm -q --cached -f --ignore-unmatch org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-r26.json
T=$(git write-tree); P="$WKHEAD"
N=$(echo "x26 scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, no sentinel, RL12_ALLOW = the staged rehearsal's host answer (installed_code flipped)" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x26 "$N"
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])" | tr -d '\r')"
export FAKE_MD5_LIST="$D/r26_release_md5.txt"
{
echo "### rl12.AC1.sh EXPECTED-PASS FORM (the issuer's script as written, via the order's literal invocation), scratch clone x26 @ $(git rev-parse --short HEAD); fake aws as above; floor reads the REAL host"
SECONDS=0; PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 600 bash "$C/rl12.AC1.sh"; echo "exit=$? (${SECONDS}s)"
} > "$D/r26_rl12.AC1_expected_pass_form.out" 2>&1
{
echo "### rl12.AC1.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live 240ac2fe5a: the 5 shipped files differ from the release bytes)"
SECONDS=0; timeout 600 bash "$C/rl12.AC1.sh"; echo "exit=$? (${SECONDS}s)"
echo
echo "### rl12.AC1.sh NEGATIVE CONTROL 2: the real pre-act worktree (manifest = live 240ac2fe5a; no ledger entry), real host"
( cd "$W" && SECONDS=0; timeout 600 bash "$C/rl12.AC1.sh"; echo "exit=$? (${SECONDS}s)" )
} > "$D/r26_rl12.AC1_negative_controls.out" 2>&1
{
echo "### rl12.AC2.sh EXPECTED-PASS FORM: scratch clone x26 (RL12_ALLOW.json = the host's answer of the STAGED rehearsal with installed_code flipped; digest checked against that real ssm invocation)"
timeout 120 bash "$C/rl12.AC2.sh"; echo "exit=$?"
} > "$D/r26_rl12.AC2_expected_pass_form.out" 2>&1
{
echo "### rl12.AC2.sh NEGATIVE CONTROL 1: the real pre-act worktree (RL12_ALLOW.json absent)"
( cd "$W" && timeout 120 bash "$C/rl12.AC2.sh"; echo "exit=$?" )
echo
echo "### rl12.AC2.sh NEGATIVE CONTROL 2: the same scratch clone with RL12_ALLOW.json = the STAGED rehearsal's true record (installed_code false: a staged run is never accepted as the installed gateway)"
cp "$W/.scratch/x26json/RL12_ALLOW.rehearsal.json" "$S/$WD/RL12_ALLOW.json"
timeout 120 bash "$C/rl12.AC2.sh"; echo "exit=$?"
echo
echo "### rl12.AC2.sh NEGATIVE CONTROL 3: the stand-in with status_tool_allowed_for_scoped false (the status tool NOT admitted; digest no longer matches the host output either)"
cp "$W/.scratch/x26json/RL12_ALLOW.denied.json" "$S/$WD/RL12_ALLOW.json"
timeout 120 bash "$C/rl12.AC2.sh"; echo "exit=$?"
echo
echo "### rl12.AC2.sh NEGATIVE CONTROL 4: the stand-in with unnamed_tool_allowed_for_scoped true (a tool nothing names admitted)"
cp "$W/.scratch/x26json/RL12_ALLOW.unnamed.json" "$S/$WD/RL12_ALLOW.json"
timeout 120 bash "$C/rl12.AC2.sh"; echo "exit=$?"
cp "$W/.scratch/x26json/RL12_ALLOW.json" "$S/$WD/RL12_ALLOW.json"
} > "$D/r26_rl12.AC2_negative_controls.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
import subprocess   # the order's text at the amendment commit c38d69aa3d (A3 binds; the worktree copy is the OLD text)
tos = subprocess.run(["git", "show", "c38d69aa3d:org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-12.gateway-release-r26.md"], capture_output=True, text=True, encoding="utf-8").stdout
assert "AMENDMENT 3" in tos or "AMENDED A3" in tos
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', tos, re.S))
rows = [("AC1", "r26_rl12.AC1_expected_pass_form.out", True, "expected-PASS form"),
        ("AC1", "r26_rl12.AC1_negative_controls.out", False, "negative controls 1 and 2"),
        ("AC2", "r26_rl12.AC2_expected_pass_form.out", True, "expected-PASS form"),
        ("AC2", "r26_rl12.AC2_negative_controls.out", False, "negative controls 1, 2, 3 and 4")]
out = []
for cid, fn, want, note in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("### "))
    if want:
        m = re.search(exp[cid], body) is not None
        out.append("%s %s (%s): re.search(<expect>) %s -> %s (must MATCH)" % (cid, fn, note, "MATCH" if m else "NO MATCH", "OK" if m else "WRONG"))
    else:
        # each control is its own run: split the file on the '### ... NEGATIVE CONTROL n' headers and test every block separately
        blocks = [b for b in re.split(r"^### .*NEGATIVE CONTROL \d.*$", txt, flags=re.M)[1:]]
        for i, b in enumerate(blocks, 1):
            blk = "\n".join(l for l in b.split("\n") if not l.startswith("### "))
            m = re.search(exp[cid], blk) is not None
            out.append("%s %s (%s, control %d of %d): re.search(<expect>) %s -> %s (must NOT match)" % (cid, fn, note, i, len(blocks), "MATCH" if m else "NO MATCH", "WRONG" if m else "OK"))
open(D + "/r26_expect_match.out", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
PY
