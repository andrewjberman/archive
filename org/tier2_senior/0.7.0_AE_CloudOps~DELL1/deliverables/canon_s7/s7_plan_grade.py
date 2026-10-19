"""Grade a saved terraform plan json: which resources move, and which attributes of the one mover differ.
  python -I s6_plan_grade.py <plan.json>
"""
from __future__ import annotations

import json
import sys

p = json.load(open(sys.argv[1], encoding='utf-8'))
rc = p.get('resource_changes', [])
movers = [r for r in rc if r['change']['actions'] not in (['no-op'], ['read'])]
print('resource_changes', len(rc), 'movers', [(r['address'], r['change']['actions']) for r in movers])
for r in movers:
    b, a = r['change']['before'] or {}, r['change']['after'] or {}
    keys = sorted(set(b) | set(a))
    diff = [k for k in keys if b.get(k) != a.get(k)]
    print('changed attrs:', diff)
    be = ((b.get('environment') or [{}])[0].get('variables') or {}) if b.get('environment') else {}
    ae = ((a.get('environment') or [{}])[0].get('variables') or {}) if a.get('environment') else {}
    print('env keys differing:', sorted(k for k in set(be) | set(ae) if be.get(k) != ae.get(k)))
    same = [k for k in ('memory_size', 'timeout', 'runtime', 'handler', 'role', 'layers', 's3_bucket', 's3_key') if b.get(k) == a.get(k)]
    print('same:', same)
    print('planned hash', a.get('source_code_hash'), 'ver', a.get('s3_object_version'), 'commit', ae.get('MDPF_GOLD_COMMIT'))
    print('before hash', b.get('source_code_hash'), 'ver', b.get('s3_object_version'), 'commit', be.get('MDPF_GOLD_COMMIT'))
