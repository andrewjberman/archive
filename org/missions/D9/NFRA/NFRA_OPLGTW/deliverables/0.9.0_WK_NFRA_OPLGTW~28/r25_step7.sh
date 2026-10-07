#!/usr/bin/env bash
# OG-rl-11 PHASE A step 7 (R18, row Z-W15-S51): the PRE-GO exercise of rl11.AC1.sh, rl11.AC2.sh and rl11.AC3.sh against the r25 release.
# Builds a SCRATCH worktree (branch x25, never merged, plumbing commit, no hook) from the wk head, with the POST-DEPLOY state standing in:
#   manifest deployed_commit = the release sha; a ledger entry file; no sentinel; RL11_SEND.json / RL11_SCOPES.json = the host's own answers of the STAGED rehearsals, taken from the
#   `STEP7_STANDIN` lines those runs printed (the same body with installed_code flipped to true, digest printed by the SAME real ssm invocation; a staged run is not the installed code, so
#   Phase B writes its own records from the installed-code run and never uses these).
# AC1's ssm md5 answer is STOOD IN by .scratch/fakeaws, which prints ONLY the md5 lines the real host prints after a deploy for the shipped files (the release md5 list);
# every other aws call (the floor's reads included) falls through to the real shim. AC2 and AC3 verify the digest against the REAL ssm invocation (get-command-invocation).
# usage: bash r25_step7.sh <release sha, 40 hex>     (run from the wk worktree root; writes r25_rl11.* .out files beside this script)
set -u
REL="$1"
W="$(git rev-parse --show-toplevel)"; D="$W/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r25/checks"
WD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
S="$W/.scratch/x25"; WKHEAD="$(git rev-parse HEAD)"
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x25 HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools org infra/aws/ec2 lib >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
mkdir -p "$W/.scratch/fakeaws"
cat > "$W/.scratch/fakeaws/aws" <<'FAKE'
#!/usr/bin/env bash
# STAND-IN for `aws` in the step-7 exercise ONLY: answers the SSM calls rl11.AC1.sh's ssm_run makes with what the host prints AFTER the deploy for `md5sum <files>`: the md5 line of
# each file the HOST HAS (the release md5 list). Every other aws call (the floor's reads included) falls through to the real shim.
case "$*" in
  *"ssm send-command"*"md5sum"*) echo "fake-command-id"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"--query Status"*) echo "Success"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"StandardOutputContent"*) for f in app/data_entitlement.py app/graph_scope_map.py app/identity_scope.py app/integrations/opal_portal/integration.py app/token_broker.py; do grep "  $f\$" "$FAKE_MD5_LIST"; done; exit 0 ;;
esac
FD="$(cd "$(dirname "$0")" && pwd)"; PATH="${PATH//$FD:/}"   # drop this fake from PATH, or the real shim finds it again and loops
exec "$(dirname "$0")/../../.tools/aws" "$@"
FAKE
chmod +x "$W/.scratch/fakeaws/aws"
# the two stand-in records, parsed from the staged rehearsals' own host output (body line + the ssm command id of that invocation)
python - "$D" "$W/.scratch/x25json" <<'PY'
import json, os, re, sys
d, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
for outfile, tag, fn in (("r25_after_stage_send.out", "RL11S", "RL11_SEND.json"), ("r25_after_stage_scopes.out", "RL11C", "RL11_SCOPES.json")):
    t = open(os.path.join(d, outfile), encoding="utf-8").read()
    cid = re.search(r"^ssm (\S+) status=Success", t, re.M).group(1)
    body = json.loads(re.search(r"^STEP7_STANDIN " + tag + r"_BODY (\{.*\})$", t, re.M).group(1))
    open(os.path.join(out, fn), "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body, "instance_id": "i-07dccb1615503ac99", "ssm_command_id": cid}, indent=1, sort_keys=True) + "\n")
    print("stand-in", fn, "from", outfile)
# the NEGATIVE-CONTROL records: the REHEARSAL body of the same invocations (installed_code false, its real digest is in the same output)
for outfile, tag, fn in (("r25_after_stage_send.out", "RL11S", "RL11_SEND.rehearsal.json"), ("r25_after_stage_scopes.out", "RL11C", "RL11_SCOPES.rehearsal.json")):
    t = open(os.path.join(d, outfile), encoding="utf-8").read()
    cid = re.search(r"^ssm (\S+) status=Success", t, re.M).group(1)
    body = json.loads(re.search(r"^" + tag + r"_REHEARSAL_BODY (\{.*\})$", t, re.M).group(1))
    # a record is attested by '<MARKER> <digest>' in the host output; the rehearsal digest line is RL11x_REHEARSAL_DIGEST, so the marker the checker greps for is absent: the control tests that too
    open(os.path.join(out, fn), "w", encoding="utf-8", newline="\n").write(json.dumps({"body": body, "instance_id": "i-07dccb1615503ac99", "ssm_command_id": cid}, indent=1, sort_keys=True) + "\n")
PY
cd "$S" || exit 9
git read-tree --reset -u "$WKHEAD" || exit 9   # the scratch tree = the CURRENT worker head (an earlier exercise may have left it on an older base)
python - "$REL" "$W/.scratch/x25json" "$D" <<'PY'
import re, shutil, sys
rel, src, d = sys.argv[1], sys.argv[2], sys.argv[3]
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
for f in ("RL11_SEND.json", "RL11_SCOPES.json"):
    shutil.copyfile(src + "/" + f, "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/" + f)
PY
echo "exercise ledger entry (scratch only)" > org/critical_paths/change_management/20261007T0000Z_nfra-oplgtw-gateway-release-r25_deploy_completion.md
git add -f infra/aws/ec2/EC2_MANIFEST.json "$WD/RL11_SEND.json" "$WD/RL11_SCOPES.json" org/critical_paths/change_management/20261007T0000Z_nfra-oplgtw-gateway-release-r25_deploy_completion.md
# the ledger is CLOSED in the post-deploy state this clone stands in for: no OPEN sentinel exists in the tree (none was opened at Phase A); make sure of it
git rm -q --cached -f --ignore-unmatch org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-r25.json
T=$(git write-tree); P="$WKHEAD"
N=$(echo "x25 scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, no sentinel, RL11_SEND/RL11_SCOPES = the staged rehearsals' host answers (installed_code flipped)" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x25 "$N"
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])" | tr -d '\r')"
export FAKE_MD5_LIST="$D/r25_release_md5.txt"
{
echo "### rl11.AC1.sh EXPECTED-PASS FORM (the issuer's script as written, via the order's literal invocation), scratch clone x25 @ $(git rev-parse --short HEAD); fake aws as above; floor reads the REAL host"
SECONDS=0; PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 600 bash "$C/rl11.AC1.sh"; echo "exit=$? (${SECONDS}s)"
} > "$D/r25_rl11.AC1_expected_pass_form.out" 2>&1
{
echo "### rl11.AC1.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live 7d65a28db0: the 5 shipped files differ from the release bytes)"
SECONDS=0; timeout 600 bash "$C/rl11.AC1.sh"; echo "exit=$? (${SECONDS}s)"
echo
echo "### rl11.AC1.sh NEGATIVE CONTROL 2: the real pre-act worktree (manifest = live 7d65a28db0; no ledger entry), real host"
( cd "$W" && SECONDS=0; timeout 600 bash "$C/rl11.AC1.sh"; echo "exit=$? (${SECONDS}s)" )
} > "$D/r25_rl11.AC1_negative_controls.out" 2>&1
{
echo "### rl11.AC2.sh EXPECTED-PASS FORM: scratch clone x25 (RL11_SEND.json = the host's answer of the STAGED rehearsal with installed_code flipped; digest checked against that real ssm invocation)"
timeout 120 bash "$C/rl11.AC2.sh"; echo "exit=$?"
} > "$D/r25_rl11.AC2_expected_pass_form.out" 2>&1
{
echo "### rl11.AC2.sh NEGATIVE CONTROL 1: the real pre-act worktree (RL11_SEND.json absent)"
( cd "$W" && timeout 120 bash "$C/rl11.AC2.sh"; echo "exit=$?" )
echo
echo "### rl11.AC2.sh NEGATIVE CONTROL 2: the same scratch clone with RL11_SEND.json = the STAGED rehearsal's true record (installed_code false: a staged run is never accepted as the installed gateway)"
cp "$W/.scratch/x25json/RL11_SEND.rehearsal.json" "$S/$WD/RL11_SEND.json"
timeout 120 bash "$C/rl11.AC2.sh"; echo "exit=$?"
cp "$W/.scratch/x25json/RL11_SEND.json" "$S/$WD/RL11_SEND.json"
} > "$D/r25_rl11.AC2_negative_controls.out" 2>&1
{
echo "### rl11.AC3.sh EXPECTED-PASS FORM: scratch clone x25 (RL11_SCOPES.json = the host's answer of the STAGED rehearsal with installed_code flipped; digest checked against that real ssm invocation)"
timeout 120 bash "$C/rl11.AC3.sh"; echo "exit=$?"
} > "$D/r25_rl11.AC3_expected_pass_form.out" 2>&1
{
echo "### rl11.AC3.sh NEGATIVE CONTROL 1: the real pre-act worktree (RL11_SCOPES.json absent)"
( cd "$W" && timeout 120 bash "$C/rl11.AC3.sh"; echo "exit=$?" )
echo
echo "### rl11.AC3.sh NEGATIVE CONTROL 2: the same scratch clone with RL11_SCOPES.json = the STAGED rehearsal's true record (installed_code false)"
cp "$W/.scratch/x25json/RL11_SCOPES.rehearsal.json" "$S/$WD/RL11_SCOPES.json"
timeout 120 bash "$C/rl11.AC3.sh"; echo "exit=$?"
echo
echo "### rl11.AC3.sh NEGATIVE CONTROL 3: the same scratch clone with the stand-in body edited so the scoped scope count is 17 (the unnarrowed state; digest no longer matches the host output either)"
python - "$S/$WD/RL11_SCOPES.json" "$W/.scratch/x25json/RL11_SCOPES.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[2], encoding="utf-8"))
d["body"]["scoped_scope_count"] = 17
open(sys.argv[1], "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, sort_keys=True) + "\n")
PY
timeout 120 bash "$C/rl11.AC3.sh"; echo "exit=$?"
cp "$W/.scratch/x25json/RL11_SCOPES.json" "$S/$WD/RL11_SCOPES.json"
} > "$D/r25_rl11.AC3_negative_controls.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
tos = open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-11.gateway-release-r25.md", encoding="utf-8").read()
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', tos, re.S))
rows = [("AC1", "r25_rl11.AC1_expected_pass_form.out", True, "expected-PASS form"),
        ("AC1", "r25_rl11.AC1_negative_controls.out", False, "negative controls 1 and 2"),
        ("AC2", "r25_rl11.AC2_expected_pass_form.out", True, "expected-PASS form"),
        ("AC2", "r25_rl11.AC2_negative_controls.out", False, "negative controls 1 and 2"),
        ("AC3", "r25_rl11.AC3_expected_pass_form.out", True, "expected-PASS form"),
        ("AC3", "r25_rl11.AC3_negative_controls.out", False, "negative controls 1, 2 and 3")]
out = []
for cid, fn, want, note in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("### "))
    m = re.search(exp[cid], body) is not None
    out.append("%s %s (%s): re.search(<expect>) %s -> %s (must %s)" % (cid, fn, note, "MATCH" if m else "NO MATCH", "OK" if m == want else "WRONG", "MATCH" if want else "NOT match"))
open(D + "/r25_expect_match.out", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
PY
