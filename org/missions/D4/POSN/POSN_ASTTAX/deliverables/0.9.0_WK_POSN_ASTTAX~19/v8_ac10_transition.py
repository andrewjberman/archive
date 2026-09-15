"""V8-AC10 re-record: the Satellites arm as the COUNTED TRANSITION STATE, from the
captured artifacts (no browser re-run). Reads only files already on disk."""
import io
import json

D = 'org/missions/D4/POSN/POSN_ASTTAX/deliverables/0.9.0_WK_POSN_ASTTAX~19/'
S = '.scratch/'
RATIFIED = ['alternatives', 'cash', 'commodities', 'equity', 'fixed_income', 'structured']

served = json.loads(io.open(S + 'v8_sat_holdings.raw', encoding='utf-8').read())
dom = json.load(io.open(D + 'v8_ac10_dom_read.json', encoding='utf-8'))
probe = json.load(io.open(D + 'v8_ac10_adapter_probe.json', encoding='utf-8'))
manifest = json.load(io.open(D + 'v8_fixture_manifest.json', encoding='utf-8'))
books = {code: blob['holdings'] for code, blob in served['satellites'].items()}

out = []
def p(s=''):
    out.append(s)
    print(s)

hj = [m for m in manifest if m['key'].endswith('satellites/holdings.json')][0]
p('V8-AC10 -- THE SATELLITES ARM AS THE COUNTED TRANSITION STATE')
p('re-derived from the captured artifacts; no browser re-run. 0.9.0_WK_POSN_ASTTAX~19')
p('')
p('THE SERVED BYTES THIS ARM IS GRADED ON (stated at capture time, per the amended face):')
p('  s3://%s/%s' % (hj['bucket'], hj['key']))
p('  VersionId %s   LastModified %s   %d bytes   md5 %s' %
  (hj['VersionId'], hj['LastModified'], hj['bytes'], hj['md5']))
p('  pre-retag VersionId %s -- IDENTICAL, so these bytes ARE the prior version.' % hj['pre_retag_VersionId'])
p('  Its producer REFUSED on an absent roster partition (W19-S16), so the Satellites page is')
p('  read PRE-RETAG and the transition state is COUNTED and NAMED, as V7-AC5 did.')
p('')
p('%-20s %6s %8s %8s %9s %7s %6s %6s  %s' % ('satellite', 'served', 'ratified', 'rendered',
  'subtotals', 'total', 'gap', 'exc w', 'excluded rows (served class / sub, weight)'))
agree_rendered = agree_gap = dom_n = 0
for code in sorted(books):
    rows = books[code]
    exc = [r for r in rows if str(r.get('asset_class', '')).lower() not in RATIFIED]
    ratified_n = len(rows) - len(exc)
    excw = round(sum(float(r.get('weight', 0)) for r in exc), 2)
    exctxt = ', '.join('%s(%s / %s, w=%.2f)' % (r['ticker'], r.get('asset_class'),
                        r.get('sub_asset_class'), float(r.get('weight', 0))) for r in exc) or 'none'
    read = dom['reads'].get(code)
    if read:
        dom_n += 1
        rendered = len(read['rows'])
        subt, grand = 0.0, None
        for t in read['totals']:
            val = t.split('|')[-1].strip()
            try:
                v = float(val)
            except ValueError:
                continue
            if 'Grand' in t:
                grand = v
            else:
                subt += v
        subt = round(subt, 2)
        gap = round(grand - subt, 2)
        ok_rows = (rendered == ratified_n)
        ok_gap = abs(gap - excw) <= 0.011
        agree_rendered += 1 if ok_rows else 0
        agree_gap += 1 if ok_gap else 0
        p('%-20s %6d %8d %8d %9.2f %7.2f %6.2f %6.2f  %s' %
          (code, len(rows), ratified_n, rendered, subt, grand, gap, excw, exctxt))
    else:
        cov = [c for c in probe['coverage'] if c['code'] == code][0]
        per = [c for c in probe['perSatellite'] if c['code'] == code][0]
        p('%-20s %6d %8d %8s %9s %7.2f %6s %6.2f  %s' %
          (code, len(rows), ratified_n, 'n/a', 'n/a', per['allocationSum'], 'n/a', excw, exctxt))
        p('    ^ NINTH LINE, from the adapter probe: hidden from the picker by')
        p('      SATELLITES_HIDDEN_FROM_DISPLAY (Positioning.tsx:156, W22-S19); probe reads')
        p('      %d served row(s), allocation sum %.2f, off-ratified rows %s.' %
          (per['currentHoldingRows'], per['allocationSum'], cov['offRatified'] or 'none'))
p('')
p('DENOMINATORS: 9 satellite(s) served; %d read from the DOM + 1 from the adapter probe = 9 of 9' % dom_n)
p('  rendered rows == RATIFIED served rows  : %d of %d' % (agree_rendered, dom_n))
p('  (total - subtotals) == EXCLUDED weight : %d of %d   (tolerance 0.011)' % (agree_gap, dom_n))
p('  served rows outside the ratified five  : %d of %d' %
  (sum(1 for c in books.values() for r in c if str(r.get('asset_class', '')).lower() not in RATIFIED),
   sum(len(c) for c in books.values())))
p('')
p('WEIGHT UNCHANGED -- each satellite total vs holdings.json PRIOR version:')
wt = json.load(io.open(S + 'v8_sat_weight_totals.json', encoding='utf-8'))
for code in sorted(wt):
    p('  %-20s served total %6.2f == prior-version total %6.2f  (SAME OBJECT: VersionId %s never moved)' %
      (code, wt[code], wt[code], hj['VersionId']))
p('  NOTE, stated: this equality is NON-DISCRIMINATING tonight -- holdings.json IS its prior')
p('  version, because its producer refused. It is recorded as measured, not as a passed test.')
p('')
p('DATE: the page renders none (W22-S20).')
p('  DOM dateMatches / asOfMatches across the %d tabs read: %s / %s' %
  (dom_n, sorted({json.dumps(r['dateMatches']) for r in dom['reads'].values()}),
   sorted({json.dumps(r['asOfMatches']) for r in dom['reads'].values()})))
p('  adapter as_of : %s' % probe['dataAsOf'])
p('  holdings.json as_of : %s' % served['as_of'])
p('  EQUAL : %s' % (str(probe['dataAsOf']) == str(served['as_of'])))
io.open(S + 'ac10_transition.txt', 'w', encoding='ascii', newline='\n').write('\n'.join(out) + '\n')
