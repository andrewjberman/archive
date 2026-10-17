"""Member-by-member sha256 compare of two package zips, plus the pin's blob for each differing member.
  python -I s6_zipcmp.py <old.zip> <new.zip> <new_pin_sha>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile


def members(p: str) -> dict:
    with zipfile.ZipFile(p) as z:
        return {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if not n.endswith('/')}


old, new, pin = members(sys.argv[1]), members(sys.argv[2]), sys.argv[3]
print('members old %d new %d | only-old %s only-new %s' % (len(old), len(new), sorted(set(old) - set(new)), sorted(set(new) - set(old))))
diff = sorted(n for n in set(old) & set(new) if old[n] != new[n])
print('DIFFERING members (%d): %s' % (len(diff), diff))
with zipfile.ZipFile(sys.argv[2]) as z:
    bm = json.loads(z.read('BUILD_MANIFEST.json'))
print('new BUILD_MANIFEST source_vintage.commit =', (bm.get('source_vintage') or {}).get('commit'))
for n in diff:
    if n == 'BUILD_MANIFEST.json':
        continue
    r = subprocess.run(['git', 'ls-tree', '-r', pin, '--name-only'], capture_output=True, text=True)
    cand = [p for p in r.stdout.split() if p.endswith('/' + n) or p == n]
    for c in cand:
        blob = subprocess.run(['git', 'show', '%s:%s' % (pin, c)], capture_output=True).stdout
        h = hashlib.sha256(blob).hexdigest()
        print('  %s vs pin blob %s: %s' % (n, c, 'EQUAL' if h == new[n] else 'DIFF'))
