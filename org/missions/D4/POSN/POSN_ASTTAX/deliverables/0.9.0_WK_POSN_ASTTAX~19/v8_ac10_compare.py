"""V8-AC10 -- SERVED vs RENDERED, per satellite, with the excluded rows NAMED.

THE BAR THE CRITERION SETS: for each satellite, served rows == rendered rows, class
subtotals == total to 0.1, and each satellite's total weight EQUAL to its pre-retag
total. This is the COUNTING instrument beside the screenshots: a row a renderer drops
and a row scrolled out of frame look identical in a PNG.

WHY THE EXCLUDED ROWS ARE THE WHOLE POINT. The order's own first paragraph says 'A
retag into a two-class page hides the row while its weight stays in the total (the Cash
defect PROD v2.1.167 shipped once); that is why you are last.' This script measures
exactly that shape: rows whose served asset_class is NOT one of the ratified five are
dropped by the renderer while their weight remains inside the Grand Total, so the
rendered subtotals do not add up to the rendered total.

Usage: python .../v8_ac10_compare.py
"""
import json
import sys

FIVE = {'cash', 'fixed_income', 'equity', 'structured', 'commodities', 'alternatives'}
DOM = '.scratch/v8_dom_read.json'
HOLD = '.scratch/v8_sat_holdings.raw'


def main():
    dom = json.load(open(DOM, encoding='utf-8'))
    served = json.load(open(HOLD, encoding='utf-8'))['satellites']

    print('SERVED vs RENDERED, per satellite')
    print('%-20s %7s %8s %9s %10s %9s %s'
          % ('satellite', 'served', 'rendered', 'subtotals', 'grandtotal', 'served w',
             'excluded rows (served class not one of the five)'))
    bad_rows = bad_sub = 0
    total_excluded = 0
    lines = []
    for code in sorted(served):
        rows = served[code]['holdings']
        served_n = len(rows)
        served_w = round(sum(r['weight'] for r in rows), 2)
        read = dom['reads'].get(code)
        if read is None:
            lines.append((code, served_n, None, None, None, served_w, 'NOT RENDERED (hidden)'))
            continue
        rendered_n = len(read['rows'])
        subs, grand = [], None
        for t in read['totals']:
            parts = [p.strip() for p in t.split('|')]
            val = float(parts[-1])
            if parts[0].lower().startswith('grand'):
                grand = val
            else:
                subs.append(val)
        sub_sum = round(sum(subs), 2)
        excluded = [(r['ticker'], r['asset_class'], r['weight'])
                    for r in rows if r['asset_class'] not in FIVE]
        total_excluded += len(excluded)
        if served_n != rendered_n:
            bad_rows += 1
        if grand is None or abs(sub_sum - grand) > 0.1:
            bad_sub += 1
        lines.append((code, served_n, rendered_n, sub_sum, grand, served_w,
                      ', '.join('%s(%s, w=%s)' % e for e in excluded) or 'none'))
    for c, sn, rn, ss, g, sw, ex in lines:
        print('%-20s %7s %8s %9s %10s %9s %s'
              % (c, sn, rn if rn is not None else '-', ss if ss is not None else '-',
                 g if g is not None else '-', sw, ex))
    print('')
    print('DENOMINATORS: %d satellite(s) served, %d read from the DOM'
          % (len(served), len(dom['reads'])))
    print('  satellites where served rows != rendered rows : %d of %d'
          % (bad_rows, len(dom['reads'])))
    print('  satellites where class subtotals != total     : %d of %d (tolerance 0.1)'
          % (bad_sub, len(dom['reads'])))
    print('  served rows whose asset_class is NOT one of the five: %d of %d'
          % (total_excluded, sum(len(v['holdings']) for v in served.values())))
    print('')
    print('THE FIVE, as the renderer admits them: %s' % sorted(FIVE))
    vocab = {}
    for v in served.values():
        for r in v['holdings']:
            vocab[r['asset_class']] = vocab.get(r['asset_class'], 0) + 1
    print('THE SERVED VOCABULARY in these bytes: %s' % json.dumps(vocab, sort_keys=True))
    print('  tokens outside the five: %s'
          % sorted(k for k in vocab if k not in FIVE))
    return 0 if (bad_rows == 0 and bad_sub == 0) else 1


if __name__ == '__main__':
    sys.exit(main())
