#!/usr/bin/env bash
# MX-a-1 AC1: the BD run-shape comparison record exists and answers each of Andrew's questions with evidence
# (Andrew-direct 2026-10-06 ~19:4xZ). Structure check only; whether the answers are right is AC2, graded at L9.
. "$(dirname "$0")/_root.sh"
R=org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.7.0_AE_CloudOps~MI/BD_RUN_SHAPE_COMPARISON.json
python - "$R" <<'PY'
import json, sys
p = sys.argv[1]
try:
    d = json.load(open(p, encoding='utf-8'))
except Exception as e:
    print(f"record unreadable: {p}: {e}"); print("RESULT: FAIL"); sys.exit(1)
bad = []
m, e = d.get('morning') or {}, d.get('evening') or {}
for k in ('transport', 'entry_point', 'schedule'):
    if not m.get(k): bad.append(f'morning.{k}')
tables = m.get('tables') or []
need = {'transactions', 'realized', 'unrealized', 'allocations'}
got = {t.get('table') for t in tables}
if not need <= got: bad.append(f'morning.tables missing {sorted(need - got)}')
for t in tables:
    if not t.get('fields'): bad.append(f"morning.tables[{t.get('table')}].fields empty")
    if not t.get('evidence'): bad.append(f"morning.tables[{t.get('table')}].evidence empty")
prov = m.get('as_of_provenance') or {}
if prov.get('bd_side_present') not in (True, False): bad.append('morning.as_of_provenance.bd_side_present not a bool')
if not prov.get('evidence'): bad.append('morning.as_of_provenance.evidence empty')
for k in ('transport', 'data_source', 'schedule'):
    if not e.get(k): bad.append(f'evening.{k}')
if e.get('fetches_from_bd') not in (True, False): bad.append('evening.fetches_from_bd not a bool')
v = d.get('verdict') or {}
if v.get('evening_extraneous') not in (True, False): bad.append('verdict.evening_extraneous not a bool')
if not v.get('preconditions_to_decommission') and v.get('evening_extraneous') is True:
    bad.append('verdict.preconditions_to_decommission empty')
print(f"morning tables: {len(tables)} ({', '.join(sorted(x for x in got if x))})")
print(f"evening fetches_from_bd={e.get('fetches_from_bd')}; verdict evening_extraneous={v.get('evening_extraneous')}")
for b in bad: print(f"MISSING: {b}")
print("RESULT: PASS" if not bad else "RESULT: FAIL"); sys.exit(0 if not bad else 1)
PY
