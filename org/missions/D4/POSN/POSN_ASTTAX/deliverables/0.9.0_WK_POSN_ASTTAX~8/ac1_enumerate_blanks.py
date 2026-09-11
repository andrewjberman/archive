import json
d = json.load(open('.scratch/ac1_scan.json'))
items = d['Items']
print('Count field      :', d.get('Count'))
print('ScannedCount     :', d.get('ScannedCount'))
print('len(Items)       :', len(items))
print('LastEvaluatedKey :', json.dumps(d.get('LastEvaluatedKey')) if 'LastEvaluatedKey' in d else 'ABSENT (single page, no pagination needed)')
print('top-level keys   :', sorted(d.keys()))
missing = []
empty = []
nonblank = []
other = []
for it in items:
    t = it['ticker']['S']
    if 'sub_asset_class' not in it:
        missing.append(t)
        continue
    v = it['sub_asset_class']
    if 'S' in v:
        s = v['S']
        if s == '':
            empty.append((t, 'EMPTY_STRING'))
        elif s.strip() == '':
            empty.append((t, 'WHITESPACE_ONLY:' + repr(s)))
        else:
            nonblank.append((t, s))
    elif 'NULL' in v:
        other.append((t, 'NULL-type attribute'))
    else:
        other.append((t, 'non-S type: ' + json.dumps(v)))
print()
print('DENOMINATOR (items in table, client-side count) :', len(items))
print('MISSING attribute (no sub_asset_class key)      :', len(missing), sorted(missing))
print('EMPTY STRING / whitespace-only                  :', len(empty), sorted(empty))
print('NULL-type or non-string                         :', len(other), sorted(other))
print('POPULATED                                       :', len(nonblank))
print('CHECK sum:', len(missing)+len(empty)+len(other)+len(nonblank), '==', len(items))
vals = sorted(set(v for _, v in nonblank))
print()
print('DISTINCT sub_asset_class VALUES IN USE:', len(vals))
for v in vals:
    n = sum(1 for _, x in nonblank if x == v)
    print('   %-40s %d' % (v, n))
RETAG = ['DBC','GLD','GSG','IAU','SLV','USO','VIXY']
blank_tickers = set(missing) | set(t for t, _ in empty) | set(t for t, _ in other)
hit = sorted(blank_tickers & set(RETAG))
print()
print('RETAG SET                :', RETAG)
print('BLANK tickers (all shapes):', sorted(blank_tickers))
print('INTERSECTION             :', hit if hit else 'NONE -- no blank ticker is among DBC/GLD/GSG/IAU/SLV/USO/VIXY')
print()
print('Retag-set rows as served today:')
for it in items:
    t = it['ticker']['S']
    if t in RETAG:
        print('   %-6s sub_asset_class=%s' % (t, json.dumps(it.get('sub_asset_class', 'MISSING'))))
