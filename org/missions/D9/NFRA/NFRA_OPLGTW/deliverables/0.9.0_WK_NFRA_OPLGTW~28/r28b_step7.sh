#!/usr/bin/env bash
# OG-rl-14 PHASE A step 7, RE-RUN on the r28b release sha (amendment A1; copy of r28_step7.sh, only names changed; rl14.AC1.sh as amended by the issuer, row S28) (R18, row Z-W15-S51): the PRE-GO exercise of rl14.AC1.sh and rl14.AC2.sh against the r28 release.
# Builds a SCRATCH worktree (branch x28, never merged, plumbing commit, no hook) from the wk head, with the POST-DEPLOY state standing in:
#   manifest deployed_commit = the release sha; a ledger entry file; no sentinel; RL14_READ.json = the host's own answer of the STAGED rehearsal, taken from the
#   `STEP7_STANDIN` lines that run printed (the same body with installed_code flipped to true, digest printed by the SAME real ssm invocation; a staged run is not the installed code,
#   so Phase B writes its own record from the installed-code run and never uses this).
# AC1's ssm md5 answer is STOOD IN by .scratch/fakeaws, which answers `md5sum <files>` with what the HOST prints after the deploy: the md5 line of each file the HOST HAS. The host has
# app/audit.py only (the release md5 list r28_release_md5.txt); deploy-to-ec2.sh and ops/bun_cache_precheck.py are laptop tools that the deploy's tar command does not ship, so the stand-in prints
# no line for them (exactly what `md5sum` prints to stdout for a missing file: nothing). Every other aws call (the floor's reads included) falls through to the real shim.
# AC2 verifies the digest against the REAL ssm invocation (get-command-invocation).
# usage: bash r28_step7.sh <release sha, 40 hex>     (run from the wk worktree root; writes r28b_rl14.* .out files beside this script)
set -u
REL="$1"
LIVE=510c8cfed2c852946e3e57fb4dd1c0467e2f3a52
W="$(git rev-parse --show-toplevel)"; D="$W/org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
C="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/r29/checks"
WD="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28"
S="$W/.scratch/x28b"; WKHEAD="$(git rev-parse HEAD)"
if [ ! -d "$S" ]; then
  git worktree add --no-checkout "$S" -b x28b HEAD >/dev/null 2>&1 || { echo "worktree add failed"; exit 9; }
  ( cd "$S" && git sparse-checkout init --cone >/dev/null 2>&1 && git sparse-checkout set .tools org infra/aws/ec2 lib >/dev/null 2>&1 && git read-tree -m -u HEAD )
fi
mkdir -p "$W/.scratch/fakeaws"
cat > "$W/.scratch/fakeaws/aws" <<'FAKE'
#!/usr/bin/env bash
# STAND-IN for `aws` in the step-7 exercise ONLY: answers the SSM calls rl14.AC1.sh's ssm_run makes with what the host prints AFTER the deploy for `md5sum <files>`: the md5 line of
# each file the HOST HAS (the release md5 list). A file the host does not have prints nothing to stdout. Every other aws call (the floor's reads included) falls through to the real shim.
case "$*" in
  *"ssm send-command"*"md5sum"*) echo "fake-command-id"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"--query Status"*) echo "Success"; exit 0 ;;
  *"get-command-invocation"*"fake-command-id"*"StandardOutputContent"*) for f in app/audit.py deploy-to-ec2.sh ops/bun_cache_precheck.py; do grep "  $f\$" "$FAKE_MD5_LIST"; done; exit 0 ;;
esac
FD="$(cd "$(dirname "$0")" && pwd)"; PATH="${PATH//$FD:/}"   # drop this fake from PATH, or the real shim finds it again and loops
exec "$(dirname "$0")/../../.tools/aws" "$@"
FAKE
chmod +x "$W/.scratch/fakeaws/aws"
# the stand-in record and the NEGATIVE-CONTROL records, parsed from the runs' own host output (body line + the ssm command id of that invocation)
python - "$D" "$W/.scratch/x28bjson" <<'PY'
import json, os, re, sys
d, out = sys.argv[1:3]
os.makedirs(out, exist_ok=True)
t = open(os.path.join(d, "r28b_after_stage_lake.out"), encoding="utf-8").read()
cid = re.search(r"^ssm (\S+) status=Success", t, re.M).group(1)
rec = lambda body, c=cid: json.dumps({"body": body, "instance_id": "i-07dccb1615503ac99", "ssm_command_id": c}, indent=1, sort_keys=True) + "\n"
stand = json.loads(re.search(r"^STEP7_STANDIN RL14_BODY (\{.*\})$", t, re.M).group(1))
reh = json.loads(re.search(r"^RL14_REHEARSAL_BODY (\{.*\})$", t, re.M).group(1))
tb = open(os.path.join(d, "r28_before.out"), encoding="utf-8").read()
cidb = re.search(r"^ssm (\S+) status=Success", tb, re.M).group(1)
bef = json.loads(re.search(r"^RL14_BEFORE_BODY (\{.*\})$", tb, re.M).group(1))
w = lambda fn, s: open(os.path.join(out, fn), "w", encoding="utf-8", newline="\n").write(s)
w("RL14_READ.json", rec(stand))                                                                  # the stand-in: installed_code flipped
w("RL14_READ.rehearsal.json", rec(reh))                                                          # control 2: the staged run's TRUE record (installed_code false)
w("RL14_READ.before.json", rec(bef, cidb))                                                       # control 3: the live r27 answer (time part empty), with its OWN ssm id
w("RL14_READ.changed.json", rec(dict(stand, records_changed_by_key_builder=1)))                  # control 4: the builder changed a record
w("RL14_READ.written.json", rec(dict(stand, lake_objects_written=1)))                            # control 5: an object was written to the lake
w("RL14_READ.dayoff.json", rec(dict(stand, lake_key_no_ts_day_matches_time=False)))              # control 6: the day does not match the time
print("stand-in and 5 control records written from r28b_after_stage_lake.out and r28_before.out")
PY
cd "$S" || exit 9
git read-tree --reset -u "$WKHEAD" || exit 9   # the scratch tree = the CURRENT worker head (an earlier exercise may have left it on an older base)
# the POST-DRAIN-BACK stand-in: overlay the release's gateway files (mode and blob from the release commit) into the INDEX only (plumbing; the commit-tree below reads the index), so
# `git diff <release> HEAD -- gateway` is the CLOUD-only runbook alone, exactly as after the drain-back.
G=infra/aws/ec2/opal-gateway
for f in $(git diff --name-only "$LIVE" "$REL" -- "$G"); do
  e=$(git ls-tree "$REL" -- "$f"); m=${e%% *}; b=$(echo "$e" | awk '{print $3}')
  git update-index --add --cacheinfo "$m,$b,$f" || exit 9
done
python - "$REL" "$W/.scratch/x28bjson" <<'PY'
import re, shutil, sys
rel, src = sys.argv[1], sys.argv[2]
p = "infra/aws/ec2/EC2_MANIFEST.json"
t = open(p, encoding="utf-8", newline="").read()
t2 = re.sub(r'("opal-gateway"[\s\S]*?"deployed_commit"\s*:\s*")[0-9a-f]{40}(")', lambda mm: mm.group(1) + rel + mm.group(2), t, count=1)
assert rel in t2
open(p, "w", encoding="utf-8", newline="").write(t2)
shutil.copyfile(src + "/RL14_READ.json", "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL14_READ.json")
PY
echo "exercise ledger entry (scratch only)" > org/critical_paths/change_management/20261007T0000Z_nfra-oplgtw-gateway-release-r28_deploy_completion.md
git add -f infra/aws/ec2/EC2_MANIFEST.json "$WD/RL14_READ.json" org/critical_paths/change_management/20261007T0000Z_nfra-oplgtw-gateway-release-r28_deploy_completion.md
# the ledger is CLOSED in the post-deploy state this clone stands in for: no OPEN sentinel exists in the tree (none was opened at Phase A); make sure of it
git rm -q --cached -f --ignore-unmatch org/critical_paths/.open_deploys/nfra-oplgtw-gateway-release-r28.json
T=$(git write-tree); P="$WKHEAD"
N=$(echo "x28b scratch-clone exercise commit (never in the real repo): manifest = release sha, ledger entry present, no sentinel, RL14_READ = the staged rehearsal's host answer (installed_code flipped)" | GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@x GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@x git commit-tree "$T" -p "$P")
git update-ref refs/heads/x28b "$N"
echo "scratch HEAD $(git rev-parse --short HEAD) manifest deployed_commit $(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'][:10])" | tr -d '\r')"
export FAKE_MD5_LIST="$D/r28_release_md5.txt"
{
echo "### rl14.AC1.sh EXPECTED-PASS FORM (the issuer's script as written, via the order's literal invocation), scratch clone x28bb @ $(git rev-parse --short HEAD); fake aws as above (the host has app/audit.py only); floor reads the REAL host"
SECONDS=0; PATH="$(cygpath -u "$W")/.scratch/fakeaws:$PATH" timeout 600 bash "$C/rl14.AC1.sh"; echo "exit=$? (${SECONDS}s)"
} > "$D/r28b_rl14.AC1_expected_pass_form.out" 2>&1
{
echo "### rl14.AC1.sh NEGATIVE CONTROL 1: the same scratch clone against the REAL undeployed host (still serving live 510c8cfed2: app/audit.py differs from the release bytes; the two tools are not on the host)"
SECONDS=0; timeout 600 bash "$C/rl14.AC1.sh"; echo "exit=$? (${SECONDS}s)"
echo
echo "### rl14.AC1.sh NEGATIVE CONTROL 2: the real pre-act worktree (manifest = live 510c8cfed2; no ledger entry), real host"
( cd "$W" && SECONDS=0; timeout 600 bash "$C/rl14.AC1.sh"; echo "exit=$? (${SECONDS}s)" )
} > "$D/r28b_rl14.AC1_negative_controls.out" 2>&1
{
echo "### rl14.AC2.sh EXPECTED-PASS FORM: scratch clone x28bb (RL14_READ.json = the host's answer of the STAGED rehearsal with installed_code flipped; digest checked against that real ssm invocation)"
timeout 120 bash "$C/rl14.AC2.sh"; echo "exit=$?"
} > "$D/r28b_rl14.AC2_expected_pass_form.out" 2>&1
{
echo "### rl14.AC2.sh NEGATIVE CONTROL 1: the real pre-act worktree (RL14_READ.json absent)"
( cd "$W" && timeout 120 bash "$C/rl14.AC2.sh"; echo "exit=$?" )
echo
echo "### rl14.AC2.sh NEGATIVE CONTROL 2: the same scratch clone with RL14_READ.json = the STAGED rehearsal's true record (installed_code false: a staged run is never accepted as the installed gateway)"
cp "$W/.scratch/x28bjson/RL14_READ.rehearsal.json" "$S/$WD/RL14_READ.json"
timeout 120 bash "$C/rl14.AC2.sh"; echo "exit=$?"
echo
echo "### rl14.AC2.sh NEGATIVE CONTROL 3: the live r27 answer (the BEFORE run on the installed code: the no-ts key's time part is EMPTY and its day does not match), with its own ssm id"
cp "$W/.scratch/x28bjson/RL14_READ.before.json" "$S/$WD/RL14_READ.json"
timeout 120 bash "$C/rl14.AC2.sh"; echo "exit=$?"
echo
echo "### rl14.AC2.sh NEGATIVE CONTROL 4: the stand-in with records_changed_by_key_builder = 1 (the builder changed a record)"
cp "$W/.scratch/x28bjson/RL14_READ.changed.json" "$S/$WD/RL14_READ.json"
timeout 120 bash "$C/rl14.AC2.sh"; echo "exit=$?"
echo
echo "### rl14.AC2.sh NEGATIVE CONTROL 5: the stand-in with lake_objects_written = 1 (an object was written to the lake)"
cp "$W/.scratch/x28bjson/RL14_READ.written.json" "$S/$WD/RL14_READ.json"
timeout 120 bash "$C/rl14.AC2.sh"; echo "exit=$?"
echo
echo "### rl14.AC2.sh NEGATIVE CONTROL 6: the stand-in with lake_key_no_ts_day_matches_time = false"
cp "$W/.scratch/x28bjson/RL14_READ.dayoff.json" "$S/$WD/RL14_READ.json"
timeout 120 bash "$C/rl14.AC2.sh"; echo "exit=$?"
cp "$W/.scratch/x28bjson/RL14_READ.json" "$S/$WD/RL14_READ.json"
} > "$D/r28b_rl14.AC2_negative_controls.out" 2>&1
cd "$W" || exit 9
python - "$D" <<'PY'
import re, sys
D = sys.argv[1]
tos = open("org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-14.gateway-release-r28.md", encoding="utf-8").read()   # the order as issued (no amendment)
exp = dict(re.findall(r'<criterion id="(AC\d)"[^>]*>.*?<expect>(.*?)</expect>', tos, re.S))
rows = [("AC1", "r28b_rl14.AC1_expected_pass_form.out", True, "expected-PASS form"),
        ("AC1", "r28b_rl14.AC1_negative_controls.out", False, "negative controls 1 and 2"),
        ("AC2", "r28b_rl14.AC2_expected_pass_form.out", True, "expected-PASS form"),
        ("AC2", "r28b_rl14.AC2_negative_controls.out", False, "negative controls 1 to 6")]
out = []
for cid, fn, want, note in rows:
    txt = open(D + "/" + fn, encoding="utf-8").read()
    body = "\n".join(l for l in txt.split("\n") if not l.startswith("### "))
    if want:
        m = re.search(exp[cid], body) is not None
        out.append("%s %s (%s): re.search(<expect>) %s -> %s (the order wants MATCH)" % (cid, fn, note, "MATCH" if m else "NO MATCH", "OK" if m else "NOT MATCHABLE"))
    else:
        # each control is its own run: split the file on the '### ... NEGATIVE CONTROL n' headers and test every block separately
        blocks = [b for b in re.split(r"^### .*NEGATIVE CONTROL \d.*$", txt, flags=re.M)[1:]]
        for i, b in enumerate(blocks, 1):
            blk = "\n".join(l for l in b.split("\n") if not l.startswith("### "))
            m = re.search(exp[cid], blk) is not None
            out.append("%s %s (%s, control %d of %d): re.search(<expect>) %s -> %s (must NOT match)" % (cid, fn, note, i, len(blocks), "MATCH" if m else "NO MATCH", "WRONG" if m else "OK"))
open(D + "/r28b_expect_match.out", "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out))
PY
