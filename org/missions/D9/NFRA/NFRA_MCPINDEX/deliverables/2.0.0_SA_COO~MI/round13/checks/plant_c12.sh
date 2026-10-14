#!/usr/bin/env bash
# plant_c12.sh -- the ISSUER's cut-time planted arms for c12.AC1-AC3 (standing battery clause 1). Not a criterion.
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/_root.sh"
C="$(native "$D/c12_check.py")"
export PLANT_REGISTRY_DIR="$(python -c "import sys; sys.path.insert(0, r'$(native "$D")'); import g1lib; print(g1lib.plant_registry_dir())" | tr -d '\r\n')"

G="$(native "$D/plant_gen.py")"
T="$(mktemp -d)"
python -c "
import sys; sys.path.insert(0, r'$(native "$D")'); import g1lib
open(r'$(native "$T")/g1.md','w',encoding='utf-8',newline='').write(g1lib.g1_text())"
echo '[]' > "$T/none.json"
BASE="$(python -c "import sys; sys.path.insert(0, r'$(native "$D")'); import g1lib; print(g1lib.base_rows_dir())" | tr -d '\r\n')"
python "$G" --g1 "$(native "$T/g1.md")" --out "$(native "$T/good")" --deployed-tools "$(native "$T/none.json")" --existing "$BASE" | tr -d '\r'
pass=0; fail=0
arm() { # arm <name> <expect PASS|FAIL> <mode> <rows dir>
  python "$C" "$3" --rows "$(native "$4")" >"$T/o.txt" 2>&1; rc=$?
  want=0; [ "$2" = FAIL ] && want=1
  if [ "$rc" = "$want" ]; then pass=$((pass+1)); echo "ARM ok:   $1 -> expected $2, got rc=$rc"; else fail=$((fail+1)); echo "ARM WRONG: $1 -> expected $2, got rc=$rc"; tail -5 "$T/o.txt" | cut -c1-200; fi
}
arm "good rows, ac1" PASS ac1 "$T/good"
arm "good rows, ac2" PASS ac2 "$T/good"
# mutations of the good set, each one defect
mut() { # mut <name> <mode> <python edit applied to a copied dir>
  rm -rf "$T/m"; cp -r "$T/good" "$T/m"
  python - "$(native "$T/m")" <<EOF
import sys,glob,os,yaml
d=sys.argv[1]
def rows(): return {p:yaml.safe_load(open(p,encoding='utf-8')) for p in sorted(glob.glob(os.path.join(d,'harvest_*.yaml')))}
def save(p,r): yaml.safe_dump(r,open(p,'w',encoding='utf-8',newline='\n'),sort_keys=False)
$3
EOF
  arm "$1" FAIL "$2" "$T/m"
}
mut "drop one row (ac1)" ac1 "os.remove(sorted(glob.glob(os.path.join(d,'harvest_*.yaml')))[7])"
mut "wrong contract.id on one row (ac1)" ac1 "p,r=list(rows().items())[3]; r['contract']['id']='x'; save(p,r)"
mut "legacy table typed as literal prefix (ac1)" ac1 "p=os.path.join(d,'harvest_research-dossier.yaml'); r=yaml.safe_load(open(p,encoding='utf-8')); r.pop('prefix_key'); r['prefix']='amgt/harvest/gold/research-dossier/'; save(p,r)"
mut "one object count off by one (ac2)" ac2 "p,r=list(rows().items())[5]; r['contract']['size']['objects']+=1; save(p,r)"
mut "producer claim inferred but text silent (ac2)" ac2 "p,r=list(rows().items())[9]; r['producer']='plain claim'; save(p,r)"
mut "nl_tags emptied on a tagged row (ac2)" ac2 "
for p,r in rows().items():
    if r['nl_tags']: r['nl_tags']=[]; save(p,r); break"
mut "publications/v1 not retired (ac2)" ac2 "p=os.path.join(d,'harvest_publications_v1.yaml'); r=yaml.safe_load(open(p,encoding='utf-8')); r['retired']=False; r.pop('retired_reason',None); save(p,r)"
mut "research-dossier retired with no evidence file (ac2)" ac2 "p=os.path.join(d,'harvest_research-dossier.yaml'); r=yaml.safe_load(open(p,encoding='utf-8')); r['retired']=True; r['retired_reason']='superseded'; save(p,r)"
mut "a round-12 example question dropped (ac2)" ac2 "p=os.path.join(d,'harvest_packs.yaml'); r=yaml.safe_load(open(p,encoding='utf-8')); r['example_questions']=r['example_questions'][1:]; save(p,r)"
mut "freshness_field loses derived_from (ac2)" ac2 "p,r=list(rows().items())[11]; r['freshness_field']='NONE -- unknown'; save(p,r)"
# ac3: the reference generator passes; a generator that names an undeployed tool fails
C12_GEN="$G" python "$C" ac3 >"$T/o.txt" 2>&1; rc=$?
if [ "$rc" = 0 ]; then pass=$((pass+1)); echo "ARM ok:   reference generator, ac3 -> PASS"; else fail=$((fail+1)); echo "ARM WRONG: reference generator, ac3 rc=$rc"; tail -6 "$T/o.txt" | cut -c1-200; fi
cat > "$T/badgen.py" <<'EOF'
import sys, runpy
# a generator that ALWAYS names harvest_read, deployed or not (the defect the policy forbids)
sys.argv = [a for a in sys.argv]
import json
i = sys.argv.index("--deployed-tools"); path = sys.argv[i + 1]
json.dump(["harvest_list", "harvest_read"], open(path, "w"))
runpy.run_path(r"PLANTGEN", run_name="__main__")
EOF
sed -i "s#PLANTGEN#$(native "$D/plant_gen.py" | sed 's#\\#/#g')#" "$T/badgen.py"
C12_GEN="$(native "$T/badgen.py")" python "$C" ac3 >"$T/o.txt" 2>&1; rc=$?
if [ "$rc" = 1 ]; then pass=$((pass+1)); echo "ARM ok:   always-harvest_read generator, ac3 -> FAIL"; else fail=$((fail+1)); echo "ARM WRONG: bad generator, ac3 rc=$rc"; tail -6 "$T/o.txt" | cut -c1-200; fi
echo "PLANTED ARMS: ok $pass, wrong $fail"
rm -rf "$T"
[ "$fail" = 0 ]
