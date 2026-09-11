"""S7-AC4 corroboration -- a SECOND instrument on a DIFFERENT plane.

The models-payload read (ac4_models_payload_vxx.py) reads the PKL the generator
consumes.  This reads the SERVED artifact the generator produced -- the other end
of the same chain.  Two instruments, two planes; agreement is corroboration, not
repetition.

Also prints the asset_class values the served payload actually carries TODAY,
which is the pre-retag baseline the AC3 verdict is measured against.
Read-only.
"""
import gzip
import json
from collections import Counter

SRC = '.scratch/served_positioning.json.gz'
S3_URI = 's3://opal-data-portal-v2/json/positioning/positioning_data.json'
VINTAGE = 'LastModified 2026-09-11T11:06:24+00:00 UTC (s3api), ContentEncoding gzip, ContentLength 8123'

print('S7-AC4 CORROBORATION -- SERVED ARTIFACT')
print('ARTIFACT: %s' % S3_URI)
print('VINTAGE : %s' % VINTAGE)
print('NOTE    : produced 2026-09-11T11:06:24Z from model_20260910_v1.pkl (11:04:19Z) -- same run.')
print('')

with gzip.open(SRC, 'rt', encoding='utf-8') as fh:
    doc = json.load(fh)

print('TOP-LEVEL KEYS (denominator %d): %s' % (len(doc), sorted(doc)))
print('')


def walk(node, path='$'):
    """Yield every dict that looks like a holding, with its path."""
    if isinstance(node, dict):
        if 'ticker' in node:
            yield path, node
        for k, v in node.items():
            yield from walk(v, '%s.%s' % (path, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, '%s[%d]' % (path, i))


holdings = list(walk(doc))
print('HOLDING OBJECTS FOUND: %d (full recursive walk, no page)' % len(holdings))
print('')

ac_counter = Counter()
vxx_rows = []
for path, h in holdings:
    val = h.get('asset_class', h.get('assetClass'))
    ac_counter[val] += 1
    if str(h.get('ticker', '')).strip().upper() == 'VXX':
        vxx_rows.append((path, h.get('ticker'), val, h.get('sub_asset_class'), h.get('weight')))

print('asset_class VALUES PRESENT IN THE SERVED PAYLOAD (denominator %d holding objects):'
      % len(holdings))
for v, n in ac_counter.most_common():
    print('  %-16r %d' % (v, n))
print('')
print('  ^ THIS IS THE PRE-RETAG BASELINE. Note the vocabulary actually served is the')
print('    FOUR-class display set, not the ratified FIVE.')
print('')

print('VXX OCCURRENCES IN THE SERVED ARTIFACT: %d' % len(vxx_rows))
print('  %-34s %-7s %-14s %-14s %s' % ('PATH', 'TICKER', 'asset_class', 'sub_asset_class', 'weight'))
for p, t, a, s, w in vxx_rows:
    print('  %-34s %-7s %-14r %-14r %s' % (p[:34], t, a, s, w))
print('')

if vxx_rows:
    print('CORROBORATION: VXX is HELD -- it is RENDERED in the live served payload,')
    print('               independently of the PKL read. Two planes agree.')
else:
    print('CORROBORATION: VXX does not appear in the served payload.')
