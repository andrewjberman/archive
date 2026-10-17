"""Which JSON paths differ between the D4-ref and D4-new bodies (path names and counts only; scalar values printed only for provenance paths).
  python -I s6_pathdiff.py <ref.json> <new.json>
"""
from __future__ import annotations

import collections
import re
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s6_response import bodies_of, decoded, find_payload, load  # noqa: E402


def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((path + '.' + k, 'KEY-ONLY-' + ('NEW' if k in b else 'REF'), None, None))
            else:
                walk(a[k], b[k], path + '.' + k, out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, 'LEN %d vs %d' % (len(a), len(b)), None, None))
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, path + '[]', out)
    elif a != b:
        out.append((path, 'VALUE', a, b))


pa, pb = find_payload(load(sys.argv[1])[1]), find_payload(load(sys.argv[2])[1])
ba, bb = bodies_of(pa), bodies_of(pb)
allpaths = collections.Counter()
examples = {}
for k in sorted(set(ba) & set(bb)):
    out = []
    walk(decoded(ba[k]), decoded(bb[k]), '$', out)
    for p, kind, x, y in out:
        norm = re.sub(r'\[\]', '[]', p)
        allpaths[(norm, kind)] += 1
        examples.setdefault((norm, kind), (x, y))
print('bodies compared', len(set(ba) & set(bb)), '| distinct differing paths', len(allpaths))
for (p, kind), n in sorted(allpaths.items()):
    x, y = examples[(p, kind)]
    show = ''
    if re.search(r'provenance|generated_at|last_updated|commit|vintage|process|trigger', p) and x is not None:
        show = ' | e.g. %r -> %r' % (str(x)[:60], str(y)[:60])
    print('  %4d  %-9s %s%s' % (n, kind, p, show))
