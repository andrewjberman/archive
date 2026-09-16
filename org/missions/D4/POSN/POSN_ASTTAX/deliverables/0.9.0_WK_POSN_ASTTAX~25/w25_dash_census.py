"""W25_DASH_CENSUS -- POSN_ASTTAX.TO-W2-1 / W2-AC9 reading 2 (slot ~25).

One glyph, two silences: the table renders '-' BOTH for "no source carries this measure for
this holding" AND for "this column does not apply to this class" (Duration on Equity at
HoldingsTab.tsx:1576, Beta on Fixed Income at :1590). This counts them apart on the rendered
rows, so the judgment reading carries a number instead of an impression.

A dash is attributed to the CLASS RULE only where the rule alone would produce it -- i.e. a
Duration cell on an Equity row, or a Beta cell on a Fixed Income row. Where the class rule
and a served null BOTH hold, the cell is counted under BOTH and reported as OVERDETERMINED,
because saying "the class rule caused it" would be a claim the evidence cannot separate.

Usage (from the workspace root):
  PYTHONUTF8=1 python3 <this> <dom-dump.json> [<dom-dump.json> ...] --served <raw> --holdings <raw>
"""
import json
import sys

SERVED_CLASS_DISPLAY = {
    'cash': 'Cash', 'fixed_income': 'Fixed Income', 'equity': 'Equity',
    'structured': 'Structured', 'commodities': 'Commodities',
    'alternatives': 'Alternatives', 'hedge': 'Hedge',
}
CHAR_COLS = ['FEE', 'MC', 'ACTIVE', 'YIELD', 'DURATION', 'CREDIT', 'BETA']
SERVED_FIELD = {'FEE': 'fee', 'MC': 'aum', 'ACTIVE': 'management_style', 'YIELD': 'yield',
                'DURATION': 'duration', 'CREDIT': 'credit', 'BETA': 'beta'}


def main():
    argv = sys.argv[1:]
    served_path = '.scratch/w25_sat_characteristics.raw'
    holdings_path = '.scratch/w25_sat_holdings.raw'
    dumps = []
    i = 0
    while i < len(argv):
        if argv[i] == '--served':
            served_path = argv[i + 1]
            i += 2
        elif argv[i] == '--holdings':
            holdings_path = argv[i + 1]
            i += 2
        else:
            dumps.append(argv[i])
            i += 1
    served = json.load(open(served_path, encoding='utf-8'))
    holdings = json.load(open(holdings_path, encoding='utf-8'))
    tickers = served.get('tickers') or {}

    for dump_path in dumps:
        dump = json.load(open(dump_path, encoding='utf-8'))
        book = dump.get('book')
        rows_served = {r['ticker']: r for r in
                       (holdings.get('satellites', {}).get(book, {}) or {}).get('holdings', [])}
        t = dump['characteristics']['tables'][-1]
        header = t['headRows'][-1]
        idx = {n: k for k, n in enumerate(header)}
        rows = [r for r in t['rows'] if len(r) == len(header)]
        class_rule = 0
        absent = 0
        overdetermined = 0
        total_dashes = 0
        total_cells = 0
        for r in rows:
            ticker = r[idx['TICKER']]
            token = (rows_served.get(ticker) or {}).get('asset_class')
            display = SERVED_CLASS_DISPLAY.get(token, token)
            entry = tickers.get(ticker) or {}
            for col in CHAR_COLS:
                total_cells += 1
                if r[idx[col]] != '-':
                    continue
                total_dashes += 1
                value = entry.get(SERVED_FIELD[col])
                if col == 'ACTIVE':
                    served_null = value not in ('active', 'passive')
                else:
                    served_null = not isinstance(value, (int, float)) or isinstance(value, bool)
                rule = (col == 'DURATION' and display == 'Equity') or \
                       (col == 'BETA' and display == 'Fixed Income')
                if rule and served_null:
                    overdetermined += 1
                elif rule:
                    class_rule += 1
                else:
                    absent += 1
        print('%s: %d dash cells of %d characteristic cells (%d rows x %d columns)'
              % (book, total_dashes, total_cells, len(rows), len(CHAR_COLS)))
        print('   CLASS RULE ONLY (the column does not apply to this class): %d' % class_rule)
        print('   ABSENT MEASURE ONLY (no source carries it):               %d' % absent)
        print('   BOTH, INSEPARABLE ON SCREEN (rule AND served null):       %d' % overdetermined)
        # The performance plane's own null glyph, counted beside it.
        p = dump['performance']['tables'][-1]
        pidx = {n: k for k, n in enumerate(p['headRows'][-1])}
        prows = [r for r in p['rows'] if len(r) == len(p['headRows'][-1])]
        windows = ['1D', 'WTD', 'MTD', '1M', 'QTD', '1Q', 'YTD', '1Y']
        em = sum(1 for r in prows for w in windows if r[pidx[w]] == '\u2014')
        print('   PERFORMANCE em dashes (a FOURTH glyph for a null, same table): %d of %d cells'
              % (em, len(prows) * len(windows)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
