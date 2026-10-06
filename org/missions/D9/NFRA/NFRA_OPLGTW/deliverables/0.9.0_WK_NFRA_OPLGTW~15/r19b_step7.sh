#!/usr/bin/env bash
# OG-rl-7 r19b PHASE A2 step 7 (R18, row Z-W15-S51): the PRE-GO exercise of rl7.AC1b.sh and rl7.AC2.sh against the r19b release.
# Builds a SCRATCH worktree (branch x19c, never merged, plumbing commit, no hook) from the wk head, with the POST-DEPLOY state standing in:
#   manifest deployed_commit = the release sha; RL7_SENDER.json built from the staged exercise (r19b_refusals_after_stage.out); a ledger entry file; no sentinel.
# AC1b's ssm md5 answer is STOOD IN by .scratch/fakeaws (the release md5 of the shipped files, i.e. what the host prints after the deploy). AC2's floor reads the REAL host.
# usage: bash r19b_step7.sh <release sha, 40 hex>     (run from the wk worktree root; writes r19b_rl7.* .out files beside this script)
set -u
REL="$1"
W="$(git rev-parse --show-toplevel)"; D="$W/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15"
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r19/checks"
S="$W/.scratch/x19c"
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x19c HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools org infra/aws/ec2 lib >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
cd "$S" || exit 9
python - "$REL" "$D/r19b_refusals_after_stage.out" <<'PY'
import json, re, sys
rel, outf = sys.argv[1], sys.argv[2]
m = [json.loads(l[len("SENDER_JSON "):]) for l in open(outf, encoding="utf-8").read().split("\n") if l.startswith("SENDER_JSON ")]
a = [d for d in m if d["mode"] == "after"][0]
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
doc = {"served_release": rel, "after": {"with_sender_args": a["with_sender_args"], "without_sender_args": a["without_sender_args"]}, "grants_written": 0}
open("org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL7_SENDER.json", "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1, sort_keys=True) + "\n")
PY
echo "exercise ledger entry (scratch only)" > org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-release-r19_deploy_completion.md
git add -f infra/aws/ec2/EC2_MANIFEST.json org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL7_SENDER.json org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-release-r19_deploy_completion.md
T=$(git write-tree); P=$(git rev-parse HEAD)
N=$(echo "x19c scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, RL7_SENDER.json complete" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x19c "$N"
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])" | tr -d '\r')"
export FAKE_MD5_LIST="$D/r19b_release_md5.txt"
{
echo "### rl7.AC1b.sh EXPECTED-PASS FORM: scratch clone x19c @ $(git rev-parse --short HEAD) (manifest deployed_commit = release ${REL:0:10}; RL7_SENDER.json complete: AS_GIVEN / NULL / grants 0); the host's ssm md5 answer is STOOD IN by a fake aws returning the release md5 of the 3 files (the state after a deploy)"
PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 120 bash "$C/rl7.AC1b.sh"; echo "exit=$?"
} > "$D/r19b_rl7.AC1b_expected_pass_form.out" 2>&1
{
echo "### rl7.AC1b.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live 37be3485db: server.py equal, the two behaviour files not)"
timeout 120 bash "$C/rl7.AC1b.sh"; echo "exit=$?"
echo
echo "### rl7.AC1b.sh NEGATIVE CONTROL 2: the real pre-act worktree (manifest = live 37be3485db; RL7_SENDER.json absent), real host"
( cd "$W" && timeout 120 bash "$C/rl7.AC1b.sh"; echo "exit=$?" )
} > "$D/r19b_rl7.AC1b_negative_controls.out" 2>&1
{
echo "### rl7.AC2.sh EXPECTED-PASS FORM: scratch clone x19c @ $(git rev-parse --short HEAD) (manifest deployed_commit = release ${REL:0:10}, ledger entry present, no sentinel, HEAD gateway tree = release); floor arms read the REAL host"
timeout 400 bash "$C/rl7.AC2.sh"; echo "exit=$?"
} > "$D/r19b_rl7.AC2_expected_pass_form.out" 2>&1
{
echo "### rl7.AC2.sh NEGATIVE CONTROL: the real pre-act worktree (manifest deployed_commit = live 37be3485db, no ledger entry, CLOUD still differs from live by the 21 files); floor reads the real host"
( cd "$W" && timeout 400 bash "$C/rl7.AC2.sh"; echo "exit=$?" )
} > "$D/r19b_rl7.AC2_negative_control.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
tos = open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-7.gateway-release-r19.md", encoding="utf-8").read()
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', tos, re.S))
rows = [("AC1", "r19b_rl7.AC1b_expected_pass_form.out", True), ("AC1", "r19b_rl7.AC1b_negative_controls.out", False),
        ("AC2", "r19b_rl7.AC2_expected_pass_form.out", True), ("AC2", "r19b_rl7.AC2_negative_control.out", False)]
out = []
for cid, fn, want in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    # drop the '### ...' banner lines (they are exercise annotations, not criterion output)
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("### "))
    m = re.search(exp[cid], body) is not None
    out.append("%s %s: re.search(<expect>) %s -> %s (must %s)" % (cid, fn, "MATCH" if m else "NO MATCH", "OK" if m == want else "WRONG", "MATCH" if want else "NOT match"))
open(D + "/r19b_expect_match.out", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
PY
