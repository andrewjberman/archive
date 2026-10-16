#!/usr/bin/env bash
# OPLGTW OG-ap-23 AC1 (round-37 CODE-BATCH, PHASE A): the re-cut carries exactly the tools and files trunk@trunk_sha adds beyond the live ref, no Terraform.
#  - W/ap23_release.json {base_sha, release_sha, trunk_sha}; base_sha is the live ref BEFORE this release (EC2_MANIFEST deployed_commit at HEAD, or previous_deployed_commit once this release is the deployed one);
#  - base..release differs only in the allowed set; no Terraform;
#  - every tool function trunk_sha adds to app/tools.py beyond the base is registered in the release's app/tools.py, and the release adds none trunk_sha does not;
#  - each added tool is in the release's SAFE_TOOLS (destructive_ops.py) and NATIVE_TOOLS (data_entitlement.py);
#  - the release does NOT commit app/refs/partner_roster.json or app/refs/scopes.json (the gate grades a new data copy's firm tokens as new carriers); its deploy-to-ec2.sh stages lib/opal_naming.py, partner_roster.json and scopes.json into the bundle at build time from the repo sources, which exist at trunk_sha.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
REC="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/ap23_release.json"
[ -f "$REC" ] || { echo "ap23_release.json absent"; echo "RESULT: FAIL"; exit 1; }
read -r base rel trunk mcp <<<"$(python -c "import json,sys;d=json.load(open(sys.argv[1],encoding='utf-8'));print(d.get('base_sha',''),d.get('release_sha',''),d.get('trunk_sha',''),d.get('mcportal_sha',''))" "$(native "$REC")" | tr -d '\r')"
git cat-file -e "${rel}^{commit}" && git cat-file -e "${trunk}^{commit}" || { echo "release_sha ${rel:-EMPTY} or trunk_sha ${trunk:-EMPTY} is not a commit here"; echo "RESULT: FAIL"; exit 1; }
read -r dep prev <<<"$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway'];print(s.get('deployed_commit','NONE'),s.get('previous_deployed_commit','NONE'))" | tr -d '\r')"
live=$dep; [ "$dep" = "$rel" ] && live=$prev
ALLOW="^($GW/(app/(client_[a-z0-9_]+|etfs_rivals|etfs_rivals_flow|etfs_silver|portal_served|portal_json_served|mdpf_classification|tools|destructive_ops|data_entitlement|admin_gateway_breakdown|admin_people)\.py|app/integrations/portal_index/integration\.py|deploy-to-ec2\.sh|tests/test_[a-z0-9_]+\.py)|lib/opal_naming\.py|infra/aws/ec2/EC2_MANIFEST\.json)$"
files=$(git diff --name-only "$base" "$rel" | tr -d '\r'); outside=$(printf '%s\n' "$files" | grep -vE "$ALLOW" | grep -c .)
tf=$(git diff --name-only "$base" "$rel" | grep -c '\.tf$' | tr -d '\r')
read -r want have extra safe native <<<"$(python - "$base" "$rel" "$trunk" <<'PYEOF2'
import re, subprocess, sys
base, rel, trunk = sys.argv[1:4]
G = "infra/aws/ec2/opal-gateway/app/"
def show(ref, f):
    return subprocess.run(["git", "show", "%s:%s%s" % (ref, G, f)], capture_output=True).stdout.decode("utf-8", "replace")
def defs(ref):
    return set(re.findall(r"(?m)^(?:async )?def (\w+)\(", show(ref, "tools.py")))
added_trunk = defs(trunk) - defs(base)
added_rel = defs(rel) - defs(base)
safe, native = show(rel, "destructive_ops.py"), show(rel, "data_entitlement.py")
have = len(added_trunk & added_rel)
extra = len(added_rel - added_trunk)
sa = sum(1 for x in added_trunk if '"%s"' % x in safe or "'%s'" % x in safe)
na = sum(1 for x in added_trunk if '"%s"' % x in native or "'%s'" % x in native)
print(len(added_trunk), have, extra, sa, na)
PYEOF2
)"
stg=$(git show "$rel:$GW/deploy-to-ec2.sh" 2>/dev/null)
dep_on=$(printf '%s\n' "$stg" | grep -cE "opal_naming\.py"); dep_ro=$(printf '%s\n' "$stg" | grep -cE "partner_roster\.json"); dep_sc=$(printf '%s\n' "$stg" | grep -cE "scopes\.json")
src_ok=yes; for p in lib/opal_naming.py infra/logic/registry/scopes.json data/mdpf/config/partner_roster.json; do git cat-file -e "$trunk:$p" 2>/dev/null || src_ok=no; done
cm=$(git ls-tree -r --name-only "$rel" -- "$GW/app/refs/partner_roster.json" "$GW/app/refs/scopes.json" | grep -c .)
mcp_ok=no
if [ -n "$mcp" ] && git -C mcportal cat-file -e "${mcp}^{commit}" 2>/dev/null && git -C mcportal merge-base --is-ancestor 421f8fbe8446650881a178fbac82a6432bb5d6ca "$mcp" 2>/dev/null; then
  mcp_ok=$(python - "$base" "$rel" "$mcp" <<'PYEOF3'
import json, subprocess, sys
base, rel, mcp = sys.argv[1:4]
def man(ref):
    raw = subprocess.run(["git", "show", "%s:infra/aws/ec2/EC2_MANIFEST.json" % ref], capture_output=True).stdout.decode("utf-8", "replace")
    return json.loads(raw)["services"]["opal-gateway"]
b, r = man(base), man(rel)
same = {k: v for k, v in b.items() if k != "mcportal_commit"} == {k: v for k, v in r.items() if k != "mcportal_commit"}
print("yes" if r.get("mcportal_commit") == mcp and same else "no")
PYEOF3
)
  mcp_ok=$(printf '%s' "$mcp_ok" | tr -d '\r')
fi
echo "base ${base:0:10} is the live ref before this release: $([ "$base" = "$live" ] && echo yes || echo no) (manifest ${dep:0:10}/${prev:0:10}); release ${rel:0:10}; trunk ${trunk:0:10}"
echo "files differing $(printf '%s\n' "$files" | grep -c .); outside the batch set $outside (want 0); terraform files differing $tf (want 0)"
echo "tools added by trunk $want; registered in the release $have of $want; extra tools in the release $extra (want 0); SAFE $safe of $want; NATIVE $native of $want"
echo "mcportal bundle: manifest mcportal_commit equals the GO's, descends from 421f8fbe84, only that manifest field changed $mcp_ok"
cens=$(python - "$trunk" "$(native "$REC")" <<'PYEOF4'
import hashlib, json, os, subprocess, sys
trunk, rec = sys.argv[1], sys.argv[2]
cp = os.path.join(os.path.dirname(rec), "ap23_tar_census.json")
def blob_md5(path):
    b = subprocess.run(["git", "show", "%s:%s" % (trunk, path)], capture_output=True).stdout
    return hashlib.md5(b).hexdigest() if b else None
try:
    m = json.load(open(cp, encoding="utf-8")).get("members", {})
except Exception:
    m = {}
want = {"app/refs/partner_roster.json": blob_md5("data/mdpf/config/partner_roster.json"), "app/refs/scopes.json": blob_md5("infra/logic/registry/scopes.json")}
cnt = {k: (m.get(k) or {}).get("count") for k in want}
ok = all(want[k] and cnt[k] == 1 and (m.get(k) or {}).get("md5") == want[k] for k in want)
print("%s %s %s" % (cnt["app/refs/partner_roster.json"] or 0, cnt["app/refs/scopes.json"] or 0, "yes" if ok else "no"))
PYEOF4
)
read -r tr_ro tr_sc tr_ok <<<"$(printf '%s' "$cens" | tr -d '\r')"
echo "bundle staging: deploy script stages opal_naming $dep_on, partner_roster $dep_ro, scopes $dep_sc line(s) (want 1 or more each); sources exist at trunk $src_ok; data copies committed in the release $cm (want 0); tar census: roster ${tr_ro:-0} and registry copy ${tr_sc:-0} member(s) in the archive, md5 equal to trunk's blobs ${tr_ok:-no}"
[ "$base" = "$live" ] && [ "$outside" = 0 ] && [ "$tf" = 0 ] && [ "${want:-0}" -ge 20 ] && [ "$have" = "$want" ] && [ "$extra" = 0 ] && [ "$safe" = "$want" ] && [ "$native" = "$want" ] && [ "$dep_on" -ge 1 ] && [ "$dep_ro" -ge 1 ] && [ "$dep_sc" -ge 1 ] && [ "$src_ok" = yes ] && [ "$cm" = 0 ] && [ "${tr_ok:-no}" = yes ] && [ "$mcp_ok" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
