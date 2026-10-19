"""Summarise a qa_return_bodies response (no body printed): size, sha256, status, errors, a4_objects_built, body keys.
  python -I s6_response.py summary <response.json>
  python -I s6_response.py diff <ref.json> <new.json>   which bodies are byte-equal after stripping the pair's volatile paths
"""
from __future__ import annotations

import hashlib
import json
import sys

VOLATILE = {'process_time', 'trigger', 'source_vintage_age_hours', 'generated_at', 'last_updated'}


def load(p: str):
    raw = open(p, 'rb').read()
    return raw, json.loads(raw)


def find_payload(o):
    """The invoke response may wrap the result in a body string; return the dict that carries status/errors."""
    if isinstance(o, dict) and ('a4_objects_built' in o or 'errors' in o):
        return o
    if isinstance(o, dict):
        for v in o.values():
            if isinstance(v, str):
                try:
                    r = find_payload(json.loads(v))
                    if r is not None:
                        return r
                except ValueError:
                    pass
            else:
                r = find_payload(v)
                if r is not None:
                    return r
    return None


def bodies_of(p: dict) -> dict:
    for k in ('bodies', 'qa_bodies', 'objects', 'artifacts'):
        if isinstance(p.get(k), dict) and p[k]:
            return p[k]
        if isinstance(p.get(k), list) and p[k]:
            return {str(i): v for i, v in enumerate(p[k])}
    return {}


def decoded(e):
    """A returned body is {body: <verbatim utf-8 JSON text>, sha256: transport integrity}; compare the parsed JSON, never the wrapper."""
    if isinstance(e, dict) and isinstance(e.get('body'), str):
        try:
            return json.loads(e['body'])
        except ValueError:
            return e['body']
    return e


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def summary(path: str) -> int:
    raw, o = load(path)
    p = find_payload(o)
    print('file', path, 'bytes', len(raw), 'sha256', hashlib.sha256(raw).hexdigest())
    print('top keys', sorted(o)[:12] if isinstance(o, dict) else type(o).__name__)
    if p is None:
        print('NO payload with status/errors found')
        return 1
    print('payload keys', sorted(p)[:30])
    print('status', p.get('status'), '| errors', json.dumps(p.get('errors'))[:300], '| a4_objects_built', p.get('a4_objects_built'))
    b = bodies_of(p)
    print('bodies', len(b), sorted(b)[:20])
    return 0


def diff(a: str, b: str) -> int:
    pa, pb = find_payload(load(a)[1]), find_payload(load(b)[1])
    ba, bb = bodies_of(pa), bodies_of(pb)
    print('ref bodies', len(ba), 'new bodies', len(bb))
    for k in sorted(set(ba) | set(bb)):
        if k not in ba:
            print('  NEW-ONLY', k)
        elif k not in bb:
            print('  REF-ONLY', k)
        else:
            eq = json.dumps(strip(decoded(ba[k])), sort_keys=True) == json.dumps(strip(decoded(bb[k])), sort_keys=True)
            print('  %s %s' % ('EQUAL' if eq else 'DIFFER', k))
    return 0


if __name__ == '__main__':
    sys.exit(summary(sys.argv[2]) if sys.argv[1] == 'summary' else diff(sys.argv[2], sys.argv[3]))
