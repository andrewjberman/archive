"""T1-AC1 -- the hop set RE-MEASURED at this cell's own vintage, accounted for.

The criterion's invocation is the comp-read census; this script is the
ACCOUNTING for its output. It carries the 98 hits that census printed at the
worktree base (651ffd4f16) -- line and band, transcribed from all three pages --
reads each line's literal text from those exact bytes, and assigns every hit to

  (a) ONE classification, and
  (b) ONE hop (the function whose behaviour the hit is part of),

then subtracts: 98 minus what is assigned must leave ZERO. A forward list of
"the hops I thought of" cannot fail that way, which is why it is not used here.

DECLARED DOMAIN AND ITS UNCOVERED MEMBERS. The criterion names five
classifications -- dict-key construction, subscript, comparison branch, output
field, mention. Hits fit none of them, so more are DECLARED rather than forced
into a neighbour: SIGNATURE (the token IS a parameter name), VALUE-SOURCE (the
token is bound from the registry read), LOG (the token is an argument to a
print), LOOP-VARIABLE (the token is the iteration variable over a class list)
and SELECTION-BINDING (`primary_asset_class = ...` -- the benchmark selection
records WHICH class won; it neither compares nor renders). SELECTION-BINDING was
found by running the subtraction and reading the three hits it left
UNCLASSIFIED, not by recall; widening "mention" to swallow them would have
produced a clean-looking 98 of 98 over a class that was never looked at.

THE CENSUS'S OWN BLIND SPOT IS PRINTED TOO. A token census over 'asset_class'
cannot see a hop that names the class VALUES instead -- a four-key literal dict,
a hardcoded subscript. Those hops are real and they are invisible to the AC1
invocation; the second census ('hedge', 31 hits at the same vintage) finds them
and they are listed at the end. A denominator certifies the SWEEP, never the SET.

Read-only.
POSN_ASTTAX.TO-T1-1 / cell AT3-s-1 / 0.9.0_WK_POSN_ASTTAX~10
"""
import subprocess
import sys

GEN = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
       'yang-generate-positioning/lambda_function.py')
PIN = '651ffd4f16'
DENOMINATOR = 98

# (line, band) for all 98 hits, transcribed in order from comp-read pages 1-3.
HITS = [
    (59, 'DOCSTRING'), (185, 'DEF'), (187, 'CODE'), (219, 'COMMENT'),
    (234, 'DEF'), (234, 'DEF'), (246, 'CODE'), (252, 'DOCSTRING'),
    (258, 'CODE'), (288, 'COMMENT'), (297, 'CODE'), (298, 'CODE'),
    (299, 'CODE'), (301, 'CODE'), (302, 'CODE'), (303, 'CODE'),
    (430, 'CODE'), (432, 'CODE'), (434, 'CODE'), (436, 'CODE'),
    (438, 'CODE'), (447, 'CODE'), (447, 'CODE'), (449, 'CODE'),
    (451, 'CODE'), (607, 'CODE'), (610, 'CODE'), (612, 'CODE'),
    (621, 'CODE'), (624, 'CODE'), (635, 'CODE'), (639, 'CODE'),
    (931, 'CODE'), (934, 'CODE'), (935, 'CODE'), (936, 'CODE'),
    (937, 'CODE'), (937, 'CODE'), (940, 'CODE'), (962, 'CODE'),
    (963, 'CODE'), (964, 'CODE'), (965, 'CODE'), (1021, 'CODE'),
    (1022, 'CODE'), (1023, 'CODE'), (1024, 'CODE'), (1128, 'CODE'),
    (1131, 'CODE'), (1133, 'CODE'), (1143, 'CODE'), (1146, 'CODE'),
    (1157, 'CODE'), (1160, 'CODE'), (1168, 'CODE'), (1172, 'CODE'),
    (1351, 'CODE'), (1352, 'CODE'), (1357, 'CODE'), (1360, 'CODE'),
    (1360, 'CODE'), (1366, 'CODE'), (1366, 'CODE'), (1371, 'CODE'),
    (1371, 'CODE'), (1371, 'CODE'), (1372, 'CODE'), (1372, 'CODE'),
    (1391, 'CODE'), (1398, 'CODE'), (1500, 'CODE'), (1501, 'CODE'),
    (1506, 'CODE'), (1509, 'CODE'), (1509, 'CODE'), (1515, 'CODE'),
    (1515, 'CODE'), (1519, 'CODE'), (1519, 'CODE'), (1519, 'CODE'),
    (1520, 'CODE'), (1520, 'CODE'), (1530, 'CODE'), (1537, 'CODE'),
    (1996, 'CODE'), (1997, 'CODE'), (2002, 'CODE'), (2006, 'CODE'),
    (2019, 'CODE'), (2023, 'CODE'), (2023, 'CODE'), (2053, 'CODE'),
    (2054, 'CODE'), (2054, 'CODE'), (2054, 'CODE'), (2103, 'CODE'),
    (2104, 'CODE'), (2110, 'CODE'),
]

# hop id, first line, last line, what it is, does its value reach the served JSON
HOPS = [
    ('A', 53, 76, 'registry_field() -- the registry read', 'SERVED (source)'),
    ('B', 185, 188, 'benchmark_etf_info() -- BENCHMARK_ETFS.get(ac, cash)',
     'SERVED (benchmark.ticker/name)'),
    ('P', 189, 233, 'module prose between the helpers', 'NOT SERVED (prose)'),
    ('C', 234, 246, 'asset_class_is_recognized() -- the sentinel discriminator',
     'SERVED (asset_class_recognized)'),
    ('D', 249, 258, 'classify_etf() -- THE one default site', 'SERVED (source)'),
    ('E', 260, 320, 'calculate_allocations() -- portfolio allocation accumulator',
     'SERVED (portfolios[M].allocation)'),
    ('F', 397, 466, 'calculate_benchmark_allocations_from_holdings() -- if/elif chain',
     'SERVED (benchmark.allocation)'),
    ('G', 529, 652, 'calculate_weighted_etf_characteristics() -- equity/FI split',
     'SERVED (benchmark.characteristics)'),
    ('H', 913, 1071, 'calculate_benchmark_comparison() -- primary + 2 spread loops',
     'SERVED (benchmark.spread.allocation)'),
    ('I', 1073, 1184, 'calculate_characteristics() -- equity/FI split + yield sub',
     'SERVED (portfolios[M].characteristics)'),
    ('J', 1290, 1414, 'calculate_aggregated_holdings() -- display map, fields, enrichment',
     'SERVED (AGG holdings[].asset_class)'),
    ('K', 1417, 1586, 'extract_current_holdings() -- display map, fields, enrichment',
     'SERVED (current_holdings[].asset_class)'),
    ('L', 1887, 2147, 'generate_positioning_data() -- display map, fields, delta, globals',
     'SERVED (holdings[].assetClass, delta)'),
    ('M', 2149, 2270, 'main() -- console summary', 'NOT SERVED (console only)'),
]

# Classification rules, in priority order. Each names the test that fired, so a
# reader can disagree with a specific rule rather than with a verdict.
RULES = [
    ('MENTION', lambda text, band: band in ('DOCSTRING', 'COMMENT')),
    ('SIGNATURE', lambda text, band: band == 'DEF'),
    ('OUTPUT-FIELD', lambda text, band: ("'asset_class':" in text
                                         or "'assetClass':" in text
                                         or "'asset_class_recognized':" in text
                                         or "'assetClassRecognized':" in text
                                         or "'sub_asset_class':" in text)),
    ('DICT-KEY-CONSTRUCTION', lambda text, band: ('asset_class_display = {' in text
                                                  or text.strip().startswith('}.get(')
                                                  or "global_benchmarks['etf'][" in text
                                                  or 'spread[' in text
                                                  or 'delta[' in text
                                                  or 'unallocated[' in text
                                                  or 'asset_allocations[' in text)),
    ('LOG', lambda text, band: (text.strip().startswith('print(')
                                or text.strip().startswith('%')
                                or text.strip().startswith('"'))),
    ('COMPARISON-BRANCH', lambda text, band: (' == ' in text or ' != ' in text
                                              or ' in [' in text
                                              or ' not in ' in text
                                              or ' > ' in text)),
    ('LOOP-VARIABLE', lambda text, band: text.strip().startswith('for asset_class in')),
    ('SELECTION-BINDING', lambda text, band: text.strip().startswith('primary_asset_class =')),
    ('VALUE-SOURCE', lambda text, band: ('= classify_etf(' in text
                                         or 'registry_field(' in text
                                         or 'benchmark_etf_info(' in text)),
    ('SUBSCRIPT', lambda text, band: ('.get(' in text or '[asset_class' in text
                                      or '[ticker]' in text)),
]

# Hops the AC1 census CANNOT see: they name the class VALUES, never the token.
# Found by the second census (comp-read --enumerate 'hedge', 31 hits at PIN).
VALUE_KEYED_HOPS = [
    ('N', '360-369', 'get_benchmark_allocation() -- four 4-key literal dicts + a '
     '4-key default', 'SERVED (fallback benchmark.allocation)'),
    ('O', '670-680', 'get_index_benchmark_data() -- 5 hardcoded 4-key allocations',
     'SERVED (index benchmark fallback)'),
    ('H*', '949-951, 1002-1004', 'calculate_benchmark_comparison() -- two 4-key '
     'bench_allocation defaults', 'SERVED (benchmark.allocation)'),
    ('M*', '2224-2227', 'main() -- four hardcoded allocation subscripts',
     'NOT SERVED (console only)'),
]


def source_lines():
    blob = subprocess.check_output(['git', 'show', '%s:%s' % (PIN, GEN)])
    return blob.decode('utf-8').splitlines()


def classify(text, band):
    for name, test in RULES:
        if test(text, band):
            return name
    return 'UNCLASSIFIED'


def hop_of(line):
    for hop_id, start, end, _, _ in HOPS:
        if start <= line <= end:
            return hop_id
    return None


def main():
    lines = source_lines()
    print('=' * 108)
    print('T1-AC1  HOP ACCOUNTING at THIS vintage -- %s @ %s' % (GEN, PIN))
    print('=' * 108)
    print('CENSUS DENOMINATOR (comp-read --enumerate asset_class): %d hit(s) across'
          ' 2391 lines / 31 sections' % DENOMINATOR)
    print('HITS TRANSCRIBED INTO THIS SCRIPT                     : %d' % len(HITS))
    print('BANDS: DOCSTRING=%d COMMENT=%d DEF=%d CODE=%d'
          % (sum(1 for _, b in HITS if b == 'DOCSTRING'),
             sum(1 for _, b in HITS if b == 'COMMENT'),
             sum(1 for _, b in HITS if b == 'DEF'),
             sum(1 for _, b in HITS if b == 'CODE')))
    print('')
    print('%-5s %-6s %-11s %-23s %s' % ('#', 'LINE', 'BAND', 'CLASS', 'HOP / TEXT'))
    print('-' * 108)
    by_class, by_hop, unassigned = {}, {}, []
    for index, (line, band) in enumerate(HITS, start=1):
        text = lines[line - 1]
        kind = classify(text, band)
        hop = hop_of(line)
        by_class[kind] = by_class.get(kind, 0) + 1
        if hop is None:
            unassigned.append((line, text))
        else:
            by_hop[hop] = by_hop.get(hop, 0) + 1
        print('%-5d %-6d %-11s %-23s %-3s %s'
              % (index, line, band, kind, hop or '???', text.strip()[:58]))

    print('-' * 108)
    print('')
    print('BY CLASSIFICATION (subtraction from the printed denominator):')
    for kind in sorted(by_class, key=lambda k: -by_class[k]):
        print('  %-23s %3d' % (kind, by_class[kind]))
    print('  %-23s %3d' % ('SUM', sum(by_class.values())))
    print('  %-23s %3d' % ('DENOMINATOR MINUS SUM', DENOMINATOR - sum(by_class.values())))
    print('')
    print('BY HOP -- the SERVED-PATH subset is every row not marked NOT SERVED:')
    print('  %-4s %-13s %-4s %-62s %s' % ('HOP', 'LINES', 'HITS', 'WHAT', 'REACHES'))
    for hop_id, start, end, what, served in HOPS:
        print('  %-4s %-13s %-4d %-62s %s'
              % (hop_id, '%d-%d' % (start, end), by_hop.get(hop_id, 0), what, served))
    print('  %-4s %-13s %-4d' % ('', 'TOTAL', sum(by_hop.values())))
    print('')
    print('HOPS THE AC1 CENSUS CANNOT SEE (they name the class VALUES, not the token;')
    print('found by the second census, comp-read --enumerate hedge = 31 hits at %s):' % PIN)
    print('  %-4s %-22s %-62s %s' % ('HOP', 'LINES', 'WHAT', 'REACHES'))
    for hop_id, span, what, served in VALUE_KEYED_HOPS:
        print('  %-4s %-22s %-62s %s' % (hop_id, span, what, served))
    print('')
    served_hops = [h for h in HOPS if not h[4].startswith('NOT SERVED')]
    print('ACCOUNTING: %d of %d hits assigned to a hop, %d unassigned'
          % (sum(by_hop.values()), DENOMINATOR, len(unassigned)))
    print('HOP DENOMINATOR: %d hops carry at least one hit; %d of %d are SERVED-PATH;'
          % (len([h for h in HOPS if by_hop.get(h[0])]), len(served_hops), len(HOPS)))
    print('                 %d further SERVED-PATH hops are invisible to this census.'
          % len([h for h in VALUE_KEYED_HOPS if not h[3].startswith('NOT SERVED')]))
    ok = (len(HITS) == DENOMINATOR and not unassigned
          and by_class.get('UNCLASSIFIED', 0) == 0
          and sum(by_hop.values()) + len(unassigned) == DENOMINATOR)
    print('T1-AC1 ACCOUNTING: %s' % ('COMPLETE' if ok else 'INCOMPLETE'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
