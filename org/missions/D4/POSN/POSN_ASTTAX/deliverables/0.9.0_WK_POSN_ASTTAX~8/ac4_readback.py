import json
d = json.load(open('.scratch/ac4_scan.json'))
items = d['Items']
print('Count field      :', d.get('Count'))
print('ScannedCount     :', d.get('ScannedCount'))
print('len(Items)       :', len(items))
print('LastEvaluatedKey :', 'ABSENT (single page)' if 'LastEvaluatedKey' not in d else json.dumps(d['LastEvaluatedKey']))
missing = []
empty = []
other = []
ok = []
for it in items:
    t = it['ticker']['S']
    if 'sub_asset_class' not in it:
        missing.append(t)
        continue
    v = it['sub_asset_class']
    if 'S' in v:
        s = v['S']
        if s.strip() == '':
            empty.append((t, repr(s)))
        else:
            ok.append((t, s))
    else:
        other.append((t, json.dumps(v)))
print()
print('DENOMINATOR (re-stated, client-side count):', len(items))
print('MISSING attribute                         :', len(missing), missing)
print('EMPTY STRING / whitespace-only            :', len(empty), empty)
print('NULL-type / non-string                    :', len(other), other)
print('POPULATED                                 :', len(ok))
print('CHECK sum:', len(missing)+len(empty)+len(other)+len(ok), '==', len(items))
print()
print('THE THREE FILLED ROWS AS SERVED:')
for t, s in sorted(ok):
    if t in ('2602335D','ICT','MER'):
        print('   %-10s %r' % (t, s))
vals = sorted(set(s for _, s in ok))
print()
print('DISTINCT VALUES IN USE AFTER THE FILL:', len(vals), '(was 31 pre-fill)')
print('NEW VALUES INTRODUCED               :', sorted(set(vals) - set([
 'Cash','Commodities','Communication Services','Consumer Discretionary','Consumer Staples','Developed','EM',
 'Energy','Financials','Global','Gold','Health Care','High Yield','Industrials','Information Technology',
 'Intermediate','International','Long Duration','Materials','Municipal','Oil','Short Duration','Silver',
 'Structured Credit','TIPS','US Large Cap','US Mid Cap','US Small Cap','Ultra Short Duration','Utilities',
 'Volatility'])) or 'NONE -- the fill used only values already in the pre-fill set')
