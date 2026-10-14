#!/usr/bin/env bash
# plant_c14.sh -- the ISSUER's cut-time planted arms for c14.AC1-AC3 (standing battery clause 1). Not a criterion.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
C="$(native "$D/c14_check.py")"
G="$(native "$D/plant_gen14.py")"
T="$(mktemp -d)"
for g in G2 G4 G5 G6; do
  python -c "
import sys; sys.path.insert(0, r'$(native "$D")'); import glib
open(r'$(native "$T")/$g.md','w',encoding='utf-8',newline='').write(glib.group_text('$g'))"
done
echo '[]' > "$T/none.json"
export PLANT_REGISTRY_DIR="$(python -c "
import sys; sys.path.insert(0, r'$(native "$D")'); import glib
print(glib.plant_registry_dir14(glib.load_all()))" | tr -d '\r\n')"
python "$G" --g2 "$(native "$T/G2.md")" --g4 "$(native "$T/G4.md")" --g5 "$(native "$T/G5.md")" --g6 "$(native "$T/G6.md")" --g2f "$(native "$T/G6.md")" --out "$(native "$T/good")" --deployed-tools "$(native "$T/none.json")" | tr -d '\r'
pass=0; fail=0
arm() { # arm <name> <expect PASS|FAIL> <mode> <rows dir>
  python "$C" "$3" --rows "$(native "$4")" >"$T/o.txt" 2>&1; rc=$?
  want=0; [ "$2" = FAIL ] && want=1
  if [ "$rc" = "$want" ]; then pass=$((pass+1)); echo "ARM ok:   $1 -> expected $2, got rc=$rc"; else fail=$((fail+1)); echo "ARM WRONG: $1 -> expected $2, got rc=$rc"; tail -5 "$T/o.txt" | cut -c1-200; fi
}
arm "good rows, ac1" PASS ac1 "$T/good"
arm "good rows, ac2" PASS ac2 "$T/good"
# a registry copy that lacks one catalog row: the registry limb of ac1 FAILs
python - "$PLANT_REGISTRY_DIR" "$T/badreg" <<PYEOF
import json, os, shutil, sys
shutil.copytree(sys.argv[1], sys.argv[2], dirs_exist_ok=True)
p = os.path.join(sys.argv[2], 'legacy_addresses.json'); d = json.load(open(p, encoding='utf-8'))
d['legacy_addresses'] = [r for r in d['legacy_addresses'] if r['key'] != [x['key'] for x in d['legacy_addresses'] if x['key'].startswith('catalog-')][5]]
json.dump(d, open(p, 'w', encoding='utf-8'), indent=1)
PYEOF
GOODREG="$PLANT_REGISTRY_DIR"; export PLANT_REGISTRY_DIR="$(native "$T/badreg")"
arm "a registry row missing (ac1)" FAIL ac1 "$T/good"
export PLANT_REGISTRY_DIR="$GOODREG"
python - "$GOODREG" "$T/badfork" <<PYEOF
import json, os, shutil, sys
shutil.copytree(sys.argv[1], sys.argv[2], dirs_exist_ok=True)
p = os.path.join(sys.argv[2], 'catalog_fork_keys.json'); d = json.load(open(p, encoding='utf-8'))
k = sorted(d['rows'])[3]; d['rows'][k]['key_template'] = 'changed'
json.dump(d, open(p, 'w', encoding='utf-8'), indent=1)
PYEOF
export PLANT_REGISTRY_DIR="$(native "$T/badfork")"
arm "a fork registry row altered (ac1)" FAIL ac1 "$T/good"
export PLANT_REGISTRY_DIR="$GOODREG"
mut() { # mut <name> <mode> <python edit applied to a copied dir>
  rm -rf "$T/m"; cp -r "$T/good" "$T/m"
  python - "$(native "$T/m")" <<EOF
import sys,glob,os,yaml
d=sys.argv[1]
def rows(): return {p:yaml.safe_load(open(p,encoding='utf-8')) for p in sorted(glob.glob(os.path.join(d,'*.yaml')))}
def save(p,r): yaml.safe_dump(r,open(p,'w',encoding='utf-8',newline='\n'),sort_keys=False)
$3
EOF
  arm "$1" FAIL "$2" "$T/m"
}
mut "drop one row (ac1)" ac1 "os.remove(sorted(glob.glob(os.path.join(d,'*.yaml')))[11])"
mut "an extra table row (ac1)" ac1 "p=sorted(glob.glob(os.path.join(d,'*.yaml')))[0]; r=yaml.safe_load(open(p,encoding='utf-8')); save(os.path.join(d,'zz_extra.yaml'),r)"
mut "wrong contract.id (ac1)" ac1 "p,r=list(rows().items())[4]; r['contract']['id']='x'; save(p,r)"
mut "a fork_keys block emptied (ac2)" ac2 "p,r=list(rows().items())[7]; r['fork_keys']={}; save(p,r)"
mut "a firm token left in a row (ac2)" ac2 "p,r=list(rows().items())[8]; r['nl_tags']=list(r['nl_tags'])+['cottonwood']; save(p,r)"
mut "a row prefix carrying a firm segment (ac2)" ac2 "p,r=list(rows().items())[10]; r['prefix']='silver/cottonwood/'; save(p,r)"
mut "firm_scope_rule flipped on a client table (ac2)" ac2 "
for p,r in rows().items():
    if r['firm_scope_rule']=='firm-scoped': r['firm_scope_rule']='opal-internal-only'; save(p,r); break"
mut "a common_query dropped (ac2)" ac2 "
for p,r in rows().items():
    if len(r['example_questions'])>0 and r['bucket']=='opal-data-assets': r['example_questions']=[]; save(p,r); break"
mut "open_items cleared (ac2)" ac2 "
for p,r in rows().items():
    if r['open_items']: r['open_items']=[]; save(p,r); break"
mut "an inferred producer text silent (ac2)" ac2 "
for p,r in rows().items():
    if 'inferred' in str((r['contract']['producer'] or {}).get('claim')): r['producer']='plain'; save(p,r); break"
mut "freshness_field wrong (ac2)" ac2 "p,r=list(rows().items())[9]; r['freshness_field']='FIELD:nope'; save(p,r)"
mut "tools disagree with read_tool (ac2)" ac2 "p,r=list(rows().items())[13]; r['tools']=['client_get_holdings']; save(p,r)"
mut "a frozen table not marked NOT CURRENT (ac2)" ac2 "
import re
for p,r in rows().items():
    if 'NOT CURRENT' in r['business_meaning']: r['business_meaning']=re.sub(r' NOT CURRENT[^.]*\.','',r['business_meaning']); save(p,r); break"
mut "a current table marked NOT CURRENT (ac2)" ac2 "
for p,r in rows().items():
    if 'NOT CURRENT' not in r['business_meaning']: r['business_meaning']+=' NOT CURRENT: 9 trading days behind.'; save(p,r); break"
mut "a not_served feed not retired (ac2)" ac2 "p=os.path.join(d,'opal_data_mdpf_feeds_model_aua_positions_inflection.yaml'); r=yaml.safe_load(open(p,encoding='utf-8')); r['retired']=False; r.pop('retired_reason',None); save(p,r)"
mut "a not_served reason that cites no record (ac2)" ac2 "p=os.path.join(d,'opal_data_mdpf_feeds_model_aua_positions_inflection.yaml'); r=yaml.safe_load(open(p,encoding='utf-8')); r['retired_reason']='not_served'; save(p,r)"
mut "a do-not-serve row not retired (ac2)" ac2 "p=os.path.join(d,'opal_data_mdpf_feeds_non_model_aua.yaml'); r=yaml.safe_load(open(p,encoding='utf-8')); r['retired']=False; r.pop('retired_reason',None); save(p,r)"
mut "a table row retired (ac2)" ac2 "p,r=list(rows().items())[2]; r['retired']=True; save(p,r)"
C14_GEN="$G" python "$C" ac3 >"$T/o.txt" 2>&1; rc=$?
if [ "$rc" = 0 ]; then pass=$((pass+1)); echo "ARM ok:   reference generator, ac3 -> PASS"; else fail=$((fail+1)); echo "ARM WRONG: reference generator, ac3 rc=$rc"; tail -6 "$T/o.txt" | cut -c1-200; fi
cat > "$T/badgen.py" <<'EOF'
import json, runpy, sys
# a generator that deploys client_get_holdings in its own head whatever the deployed set says (names an undeployed tool)
i = sys.argv.index("--deployed-tools"); path = sys.argv[i + 1]
d = json.load(open(path)); d.append("client_get_holdings"); json.dump(d, open(path, "w"))
runpy.run_path(r"PLANTGEN", run_name="__main__")
EOF
sed -i "s#PLANTGEN#$(native "$D/plant_gen14.py" | sed 's#\\#/#g')#" "$T/badgen.py"
C14_GEN="$(native "$T/badgen.py")" python "$C" ac3 >"$T/o.txt" 2>&1; rc=$?
if [ "$rc" = 1 ]; then pass=$((pass+1)); echo "ARM ok:   a generator that names an undeployed tool, ac3 -> FAIL"; else fail=$((fail+1)); echo "ARM WRONG: bad generator, ac3 rc=$rc"; tail -6 "$T/o.txt" | cut -c1-200; fi
echo "PLANTED ARMS: ok $pass, wrong $fail"
rm -rf "$T"
[ "$fail" = 0 ]
