"""W25_CELL_COMPARE -- POSN_ASTTAX.TO-W2-1 / W2-AC5 (slot ~25).

THE BAR IS THE SERVED BYTES AGAINST THE RENDERED CELLS, and this script is the join: for
every Holdings Breakdown row of the satellites named on the command line it prints, cell by
cell, the SERVED value formatted the way the table formats it beside the value the DOM
actually carries, and ends with `mismatches 0 of N` with N printed.

INPUTS
  argv[1..]  the DOM dumps produced by w25_dom_read.mjs (JSON; one per satellite)
  --served   the served characteristics.json raw bytes (default .scratch/w25_sat_characteristics.raw)
  --holdings the served holdings.json raw bytes    (default .scratch/w25_sat_holdings.raw)

THE RENDERER'S OWN RULES, re-implemented here from HoldingsTab.tsx rather than imported --
a second implementation on the same declared rule, so agreement is evidence rather than a
tautology:
  Fee       (fee * 100).toFixed(0)          else '-'
  MC        (aum / 1000).toFixed(1)         else '-'
  Active    management_style active -> YES, passive -> NO, unknown/null -> '-'
            (the LABEL, per PRD v0.11 C-HOLDING-IDENTITY; not the served `active` measure)
  Yield     yield.toFixed(2)                else '-'
  Duration  '-' when the row's display class is Equity, else duration.toFixed(2) else '-'
  Credit    credit.toFixed(0)               else '-'
  Beta      '-' when the row's display class is Fixed Income, else beta.toFixed(2) else '-'
            AFTER the HoldingsTab ticker overrides (UVXY -3.2, PFDE 1.05, PFOE 1.22), which
            are Yang's specification in every mode and which this TO leaves in place. The
            comparison is ALSO run without them and both counts are printed, so the
            override can never hide a disagreement.
  Name      the served `name` when non-null and non-empty, else the ticker
  Returns   formatPercentageReturn: (value >= 0 ? '+' : '') + value.toFixed(2) + '%',
            an EM DASH when the window is null or absent

`toFixed` IS RE-IMPLEMENTED EXACTLY, not approximated: ECMA-262 takes the sign off first
and then picks the nearer integer, larger on a tie, so it is ROUND-HALF-AWAY-FROM-ZERO over
the EXACT binary value of the double. Python's own round() is half-to-EVEN and its float
formatting rounds the decimal shortest-repr, so either would disagree with the browser on a
tie. Decimal(float) carries the exact binary value, which is what the spec rounds.

ASCII ONLY: a rendered em dash is printed as the token <EMDASH>, and any other non-ASCII
character as its \\uXXXX escape.
"""
import json
import sys
from decimal import Decimal, ROUND_HALF_UP

EM_DASH = '\u2014'  # the glyph the performance cell renders for a null; escaped, never typed

SERVED_CLASS_DISPLAY = {
    'cash': 'Cash',
    'fixed_income': 'Fixed Income',
    'equity': 'Equity',
    'structured': 'Structured',
    'commodities': 'Commodities',
    'alternatives': 'Alternatives',
    'hedge': 'Hedge',
}
BETA_OVERRIDES = {'UVXY': -3.2, 'PFDE': 1.05, 'PFOE': 1.22}
PERFORMANCE_WINDOWS = ['1D', 'WTD', 'MTD', '1M', 'QTD', '1Q', 'YTD', '1Y']


def to_fixed(value, digits):
    """ECMA-262 Number.prototype.toFixed, over the exact binary value of the double."""
    d = Decimal(value)
    # NEGATIVE ZERO IS NOT NEGATIVE HERE. A served -0.0 satisfies `x < 0` nowhere, so the
    # spec prepends no sign and the browser prints '0.00'; Decimal(-0.0) keeps the sign
    # bit and would format '-0.00'. Measured: VNLA's MTD is a served -0.0 and this was
    # the ONE disagreement in 512 cells -- in the INSTRUMENT, not in the render.
    if d == 0:
        d = Decimal(0)
    sign = '-' if d < 0 else ''
    q = Decimal(1).scaleb(-digits)
    out = (-d if d < 0 else d).quantize(q, rounding=ROUND_HALF_UP)
    # The sign is PREPENDED AFTER rounding, per the spec's own order: (-0.1467).toFixed(0)
    # is '-0' in the browser, not '0'. Dropping the sign here would have invented an
    # agreement on VGSH's credit cell.
    return sign + format(out, 'f')


def ascii_safe(text):
    out = []
    for ch in text:
        if ch == EM_DASH:
            out.append('<EMDASH>')
        elif ord(ch) < 128:
            out.append(ch)
        else:
            out.append('\\u%04x' % ord(ch))
    return ''.join(out)


def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def expect_char_cells(ticker, entry, display_class, apply_overrides=True):
    """The 7 characteristic cells, as the table formats them."""
    fee = entry.get('fee') if entry else None
    aum = entry.get('aum') if entry else None
    style = entry.get('management_style') if entry else None
    yld = entry.get('yield') if entry else None
    dur = entry.get('duration') if entry else None
    credit = entry.get('credit') if entry else None
    beta = entry.get('beta') if entry else None
    if apply_overrides and ticker in BETA_OVERRIDES:
        beta = BETA_OVERRIDES[ticker]
    cells = {}
    cells['FEE'] = to_fixed(fee * 100, 0) if is_number(fee) else '-'
    cells['MC'] = to_fixed(aum / 1000, 1) if is_number(aum) else '-'
    cells['ACTIVE'] = 'YES' if style == 'active' else ('NO' if style == 'passive' else '-')
    cells['YIELD'] = to_fixed(yld, 2) if is_number(yld) else '-'
    if display_class == 'Equity':
        cells['DURATION'] = '-'
    else:
        cells['DURATION'] = to_fixed(dur, 2) if is_number(dur) else '-'
    cells['CREDIT'] = to_fixed(credit, 0) if is_number(credit) else '-'
    if display_class == 'Fixed Income':
        cells['BETA'] = '-'
    else:
        cells['BETA'] = to_fixed(beta, 2) if is_number(beta) else '-'
    return cells


def expect_perf_cells(entry):
    """The 8 performance cells, as formatPercentageReturn formats them."""
    returns = (entry or {}).get('returns') or {}
    cells = {}
    for w in PERFORMANCE_WINDOWS:
        v = returns.get(w)
        if not is_number(v):
            cells[w] = '<EMDASH>'
        else:
            cells[w] = ('+' if v >= 0 else '') + to_fixed(v, 2) + '%'
    return cells


def expect_name(ticker, entry):
    name = (entry or {}).get('name')
    return name if isinstance(name, str) and name != '' else ticker


def table_rows(state):
    """The last table on the page (the Holdings Breakdown) as header + holding rows."""
    tables = state.get('tables') or []
    if not tables:
        return [], []
    t = tables[-1]
    header = t['headRows'][-1] if t.get('headRows') else []
    rows = [r for r in t.get('rows', []) if len(r) == len(header)]
    return header, rows


def main():
    argv = sys.argv[1:]
    # DEFAULTS ARE RELATIVE TO portal/, because W2-AC5's invocation runs the compare
    # from there (`cd portal && ... python3 <CELL_COMPARE> .scratch/w2_sat15.txt ...`)
    # and passes no path for the served bytes.
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

    with open(served_path, encoding='utf-8') as fh:
        served = json.load(fh)
    with open(holdings_path, encoding='utf-8') as fh:
        holdings = json.load(fh)
    tickers = served.get('tickers') or {}
    print('SERVED characteristics.json: as_of=%s  tickers=%d' % (served.get('as_of'), len(tickers)))
    print('SERVED holdings.json:        as_of=%s  satellites=%d'
          % (holdings.get('as_of'), len(holdings.get('satellites') or {})))
    print('COMPARING %d dump(s): %s' % (len(dumps), ', '.join(dumps)))

    grand_cells = 0
    grand_mismatch = 0
    grand_rows = 0
    name_from_served = 0
    name_from_ticker = 0
    override_diff = 0

    for dump_path in dumps:
        with open(dump_path, encoding='utf-8') as fh:
            dump = json.load(fh)
        book = dump.get('book')
        served_rows = {r['ticker']: r
                       for r in (holdings.get('satellites', {}).get(book, {}) or {}).get('holdings', [])}
        print('')
        print('=' * 108)
        print('%s  (dump %s)' % (dump.get('label'), dump_path))
        print('  served rows for this satellite: %d' % len(served_rows))
        c_header, c_rows = table_rows(dump['characteristics'])
        p_header, p_rows = table_rows(dump['performance'])
        print('  CHARACTERISTICS view: header=%s  holding rows=%d' % (c_header, len(c_rows)))
        print('  PERFORMANCE view:     header=%s  holding rows=%d' % (p_header, len(p_rows)))
        if not c_header or not p_header:
            print('  BLOCKED: no table found in the dump')
            continue
        ci = {name: idx for idx, name in enumerate(c_header)}
        pi = {name: idx for idx, name in enumerate(p_header)}
        perf_by_ticker = {r[pi['TICKER']]: r for r in p_rows}

        book_cells = 0
        book_mismatch = 0
        for row in c_rows:
            ticker = row[ci['TICKER']]
            grand_rows += 1
            entry = tickers.get(ticker)
            sr = served_rows.get(ticker)
            token = (sr or {}).get('asset_class')
            display_class = SERVED_CLASS_DISPLAY.get(token, token) if token else 'Unlabelled'
            exp = expect_char_cells(ticker, entry, display_class)
            exp_no_ovr = expect_char_cells(ticker, entry, display_class, apply_overrides=False)
            if exp['BETA'] != exp_no_ovr['BETA']:
                override_diff += 1
            exp_name = expect_name(ticker, entry)
            if entry and isinstance(entry.get('name'), str) and entry['name'] != '':
                name_from_served += 1
            else:
                name_from_ticker += 1
            perf_row = perf_by_ticker.get(ticker)
            exp_perf = expect_perf_cells(entry)

            print('  ROW %-6s served-class=%-13s in-tickers-block=%s'
                  % (ticker, display_class, 'YES' if entry else 'NO'))
            pairs = [('NAME', exp_name, row[ci['NAME']])]
            for col in ['FEE', 'MC', 'ACTIVE', 'YIELD', 'DURATION', 'CREDIT', 'BETA']:
                pairs.append((col, exp[col], row[ci[col]]))
            for w in PERFORMANCE_WINDOWS:
                got = ascii_safe(perf_row[pi[w]]) if perf_row else '(row absent)'
                pairs.append((w, exp_perf[w], got))
            for col, want, got in pairs:
                want_s = ascii_safe(str(want))
                got_s = ascii_safe(str(got))
                ok = want_s == got_s
                book_cells += 1
                if not ok:
                    book_mismatch += 1
                print('      %-9s served=%-28s rendered=%-28s %s'
                      % (col, want_s, got_s, 'OK' if ok else 'MISMATCH'))
        print('  %s: mismatches %d of %d cells across %d rows'
              % (book, book_mismatch, book_cells, len(c_rows)))
        grand_cells += book_cells
        grand_mismatch += book_mismatch

    print('')
    print('=' * 108)
    print('TOTAL: mismatches %d of %d cells across %d rows in %d satellite(s)'
          % (grand_mismatch, grand_cells, grand_rows, len(dumps)))
    print('NAME CELL: %d of %d rows took the SERVED name; %d fell back to the ticker '
          '(the served name was null)' % (name_from_served, grand_rows, name_from_ticker))
    print('BETA OVERRIDE: %d of %d rows would render a DIFFERENT beta without the '
          'HoldingsTab ticker overrides (UVXY/PFDE/PFOE)' % (override_diff, grand_rows))
    return 0 if grand_mismatch == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
