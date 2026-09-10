#!/usr/bin/env bash
# F8-AC2 -- the normaliser handles .sh: the regeneration's exclusion line reads 4 of N, every
# excluded name is a DECLARED retirement, and the suffix DOMAIN is censused before the stripped
# set is named.
#
# NFRA_CLDGRPH.TO-CG-F-8 / cell CG-s-28, 0.9.0_WK_NFRA_CLDGRPH~4.
#
# TWO INSTRUMENTS, ON PURPOSE. The EXCLUDED line comes from the generator's own stdout (the
# estate's instrument, run as the estate runs it). The "all declared retired" verdict is NOT
# taken from that same stdout: it is re-derived here by reading graph-call-manifest.yaml's
# retired_aliases directly, because a generator asserting its own exclusions are benign is the
# producer self-reporting.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1

OUT="$(timeout 120 python .tools/gen_tool_classification.py 2>&1)"
RC=$?
echo "=== gen_tool_classification.py stdout (rc=${RC}) ==="
echo "${OUT}"
echo "=== ==="
echo ""

EXLINE="$(printf '%s\n' "${OUT}" | grep -m1 '^EXCLUDED_NOT_IN_AUTHORITY=')"
echo "${EXLINE}"
echo ""

timeout 120 python - <<'PY'
import json
import os
import re
import sys

import yaml

sys.path.insert(0, '.tools')
import gen_tool_registry as reg  # noqa: E402  -- the SAME normaliser the generators use

MANIFEST = 'org/modules/graph/graph-call-manifest.yaml'
COVERAGE_MAP = 'org/modules/graph/comp-coverage-map.yaml'
PROFILE = 'org/tier1_exec/3.0.0_SA_CVO/deliverables/tool_profile.json'


def load_yaml(p):
    with open(p, encoding='utf-8', errors='replace') as fh:
        return yaml.safe_load(fh) or {}


cm = load_yaml(COVERAGE_MAP)
map_names = [str(r['tool']) for sec in ('tools', 'meta_tools')
             for r in (cm.get(sec) or []) if isinstance(r, dict) and r.get('tool')]
with open(PROFILE, encoding='utf-8') as fh:
    prof = json.load(fh)
prof_names = [str(r['tool']) for r in prof if r.get('tool')]

SUF = re.compile(r'(\.[A-Za-z0-9]+)$')


def census(names):
    out = {}
    for n in names:
        m = SUF.search(n.strip())
        k = m.group(1) if m else '(none)'
        out[k] = out.get(k, 0) + 1
    return out


mc, pc = census(map_names), census(prof_names)

# --- the exclusion set, RE-DERIVED here (not parsed out of the generator's prose) --------------
authority = reg.population_from_map()
excluded = sorted(n for n in prof_names if reg.norm_tool(n) not in authority)
mdoc = load_yaml(MANIFEST)
retired_names = set((mdoc.get('retired_aliases') or {}).keys())
undeclared = [n for n in excluded if reg.norm_tool(n) not in retired_names]

# entry-grain corroboration (R14 `status: retired` on a manifest ENTRY), a DIFFERENT surface
entry_status = {}
for e in (mdoc.get('entries') or []):
    if isinstance(e, dict) and str(e.get('status', '')).startswith('retired'):
        entry_status[str(e.get('id'))] = str(e.get('status'))

print('POPULATION_AUTHORITY_NAMES=%d  PROFILE_NAMES=%d' % (len(authority), len(prof_names)))
print('RE_DERIVED_EXCLUDED=%d of %d: %s' % (len(excluded), len(prof_names), ', '.join(excluded)))
for n in excluded:
    ra = (mdoc.get('retired_aliases') or {}).get(reg.norm_tool(n)) or {}
    print('    %-24s declared_retired=%s  retired: %s'
          % (n, reg.norm_tool(n) in retired_names, str(ra.get('retired'))[:90]))
print('UNDECLARED_EXCLUSIONS=%d: %s' % (len(undeclared), ', '.join(undeclared) or 'none'))
print('MANIFEST_ENTRIES_WITH_STATUS_RETIRED=%d: %s'
      % (len(entry_status), ', '.join(sorted(entry_status)) or 'none'))
print('EXCLUDED_ALL_DECLARED_RETIRED=%s' % ('true' if not undeclared else 'false'))
print('SUFFIXES_PRESENT=authority comp-coverage-map.yaml (%d names) %s | profile tool_profile.json '
      '(%d names) %s' % (len(map_names), mc, len(prof_names), pc))
print('SUFFIXES_STRIPPED=%s  (gen_tool_registry.SUFFIXES_STRIPPED, the single constant norm_tool '
      'iterates)' % (list(reg.SUFFIXES_STRIPPED),))
present = sorted(k for k in list(mc) + list(pc) if k != '(none)')
stripped = sorted(reg.SUFFIXES_STRIPPED)
print('SUFFIX_DOMAIN_MECE=%s  present=%s  stripped=%s  unstripped=%s'
      % ('true' if not [k for k in present if k not in stripped] else 'false',
         present, stripped, [k for k in present if k not in stripped] or 'none'))
print('NORM_CONTROL=%s' % ('FIRED' if reg.norm_tool('comp-v5-composite-test.sh')
                           == 'comp-v5-composite-test'
                           and reg.norm_tool('comp-whoread.py') == 'comp-whoread'
                           and reg.norm_tool('comp-find') == 'comp-find'
                           else 'DID-NOT-FIRE'))
sys.exit(0 if not undeclared else 1)
PY
PYRC=$?
echo "PY_RC=${PYRC}"
exit $(( RC != 0 || PYRC != 0 ))
