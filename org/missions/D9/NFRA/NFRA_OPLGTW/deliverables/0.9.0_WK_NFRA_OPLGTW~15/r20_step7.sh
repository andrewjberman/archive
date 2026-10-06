#!/usr/bin/env bash
# OG-rl-8 PHASE A step 7 (R18, row Z-W15-S51): the PRE-GO exercise of rl8.AC1.sh and rl8.AC2.sh against the r20 release.
# Builds a SCRATCH worktree (branch x20, never merged, plumbing commit, no hook) from the wk head, with the POST-DEPLOY state standing in:
#   manifest deployed_commit = the release sha; RL8_LOGIN.json built from the staged exercise (r20_login_after_stage.out) and the admit set; a ledger entry file; no sentinel.
# AC1's ssm md5 answer is STOOD IN by .scratch/fakeaws (the release md5 of the shipped files, i.e. what the host prints after the deploy). AC2's floor reads the REAL host.
# usage: bash r20_step7.sh <release sha, 40 hex>     (run from the wk worktree root; writes r20_rl8.* .out files beside this script)
set -u
REL="$1"
W="$(git rev-parse --show-toplevel)"; D="$W/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15"
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r20/checks"
S="$W/.scratch/x20"
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x20 HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools org infra/aws/ec2 lib >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
cd "$S" || exit 9
python - "$REL" "$D/r20_login_after_stage.out" "$D/r20_admit_set.json" <<'PY'
import json, re, sys
rel, outf, adm = sys.argv[1], sys.argv[2], sys.argv[3]
m = [json.loads(l[len("LOGIN_JSON "):]) for l in open(outf, encoding="utf-8").read().split("\n") if l.startswith("LOGIN_JSON ")]
a = [d for d in m if d["expect"] == "after"][0]
ad = json.load(open(adm, encoding="utf-8"))
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
doc = {"served_release": rel, "files_shipped": ["app/server.py", "app/audit.py", "app/integrations/schwab/engine.py"],
       "admit_before": sorted(set(ad["admit_before"])), "admit_after": sorted(set(ad["admit_after"])), "lost_nonrestricted": ad["lost_nonrestricted"],
       "after": {"nonrestricted": a["nonrestricted"], "analyst_service_identity": a["analyst"], "restricted": a["restricted"], "server_held": a["server_held"],
                 "requests": a["requests"], "audit_records": a["audit_records"]}, "grants_written": 0}
open("org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL8_LOGIN.json", "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1, sort_keys=True) + "\n")
PY
echo "exercise ledger entry (scratch only)" > org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-release-r20_deploy_completion.md
git add -f infra/aws/ec2/EC2_MANIFEST.json org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~15/RL8_LOGIN.json org/critical_paths/change_management/20261006T0000Z_nfra-oplgtw-gateway-release-r20_deploy_completion.md
T=$(git write-tree); P=$(git rev-parse HEAD)
N=$(echo "x20 scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, RL8_LOGIN.json complete" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x20 "$N"
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])" | tr -d '\r')"
export FAKE_MD5_LIST="$D/r20_release_md5.txt"
{
echo "### rl8.AC1.sh EXPECTED-PASS FORM: scratch clone x20 @ $(git rev-parse --short HEAD) (manifest deployed_commit = release ${REL:0:10}; RL8_LOGIN.json complete: admit sets, lost_nonrestricted [], ADMITTED / ADMITTED / REFUSED / ADMITTED, 8 requests = 8 audit records, grants 0); the host's ssm md5 answer is STOOD IN by a fake aws returning the release md5 of the 3 shipped files (the state after a deploy)"
PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 120 bash "$C/rl8.AC1.sh"; echo "exit=$?"
} > "$D/r20_rl8.AC1_expected_pass_form.out" 2>&1
{
echo "### rl8.AC1.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live cf4b036e62: the 3 shipped files differ from the release bytes)"
timeout 120 bash "$C/rl8.AC1.sh"; echo "exit=$?"
echo
echo "### rl8.AC1.sh NEGATIVE CONTROL 2: the real pre-act worktree (manifest = live cf4b036e62; RL8_LOGIN.json absent), real host"
( cd "$W" && timeout 120 bash "$C/rl8.AC1.sh"; echo "exit=$?" )
} > "$D/r20_rl8.AC1_negative_controls.out" 2>&1
{
echo "### rl8.AC2.sh EXPECTED-PASS FORM: scratch clone x20 @ $(git rev-parse --short HEAD) (manifest deployed_commit = release ${REL:0:10}, ledger entry present, no sentinel, HEAD gateway tree = release); floor arms read the REAL host"
timeout 400 bash "$C/rl8.AC2.sh"; echo "exit=$?"
} > "$D/r20_rl8.AC2_expected_pass_form.out" 2>&1
{
echo "### rl8.AC2.sh NEGATIVE CONTROL: the real pre-act worktree (manifest deployed_commit = live cf4b036e62, no ledger entry, CLOUD still differs from live by the 5 files); floor reads the real host"
( cd "$W" && timeout 400 bash "$C/rl8.AC2.sh"; echo "exit=$?" )
} > "$D/r20_rl8.AC2_negative_control.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
tos = open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-8.gateway-release-r20.md", encoding="utf-8").read()
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', tos, re.S))
rows = [("AC1", "r20_rl8.AC1_expected_pass_form.out", True), ("AC1", "r20_rl8.AC1_negative_controls.out", False),
        ("AC2", "r20_rl8.AC2_expected_pass_form.out", True), ("AC2", "r20_rl8.AC2_negative_control.out", False)]
out = []
for cid, fn, want in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    # drop the '### ...' banner lines (they are exercise annotations, not criterion output)
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("### "))
    m = re.search(exp[cid], body) is not None
    out.append("%s %s: re.search(<expect>) %s -> %s (must %s)" % (cid, fn, "MATCH" if m else "NO MATCH", "OK" if m == want else "WRONG", "MATCH" if want else "NOT match"))
open(D + "/r20_expect_match.out", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
PY
