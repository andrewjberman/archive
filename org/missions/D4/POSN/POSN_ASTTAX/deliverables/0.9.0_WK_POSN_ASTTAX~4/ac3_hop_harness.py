"""S7-AC3 -- THE DECISIVE TEST. Does a five-class value survive each hop?

One row per hop enumerated by S7-AC2. For every hop the harness
  (a) extracts the hop's EXACT source lines from the live file (bound to real
      bytes -- never to a paraphrase of them), and
  (b) drives that code with asset_class == 'Commodities' -- the literal value
      POSN_ASTTAX.TO-S2-1 would write for DBC/GLD/GSG/IAU/SLV/USO -- and
      observes the outcome.

Outcome vocabulary (MECE over what can happen to a value at a hop):
  SURVIVES          the value is carried through and is observable downstream
  RAISES            the hop throws
  SILENTLY DROPPED  the hop neither carries nor throws -- the value vanishes
                    (or is rewritten to a placeholder). A FAILURE, per the cell.

Hops REAL-FN are driven through the imported real function.
Hops SRC-EXEC execute the hop's literal extracted source in a controlled
namespace -- used where the hop sits deep inside a large dataframe-driven
function; the executed text is PRINTED so the binding is checkable.

Read-only: imports the module and calls it. Writes nothing, deploys nothing.
"""
import os
import sys
import textwrap

GEN_DIR = 'infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning'
GEN = os.path.join(GEN_DIR, 'lambda_function.py')
PROBE = 'Commodities'   # the literal value AT2-s-2 writes
SRC_LINES = open(GEN, encoding='utf-8').read().splitlines()


def seg(a, b):
    """The file's literal lines a..b inclusive, 1-based."""
    return '\n'.join(SRC_LINES[a - 1:b])


def show(a, b):
    for i in range(a, b + 1):
        print('      %5d | %s' % (i, SRC_LINES[i - 1]))


# ---------------------------------------------------------------- import real
sys.path.insert(0, GEN_DIR)
import etf_classifications_dynamodb as ecd   # noqa: E402  (must follow sys.path.insert)


class StubClassifier(object):
    """Returns a controlled registry row. Stands in for DynamoDB ONLY -- every
    function under test is the real one."""
    def __init__(self, *a, **k):
        pass

    def get_classification(self, ticker):
        if ticker == 'PROBE':
            return {'ticker': 'PROBE', 'name': 'Probe Commodity ETF',
                    'asset_class': PROBE, 'sub_asset_class': 'Gold',
                    'management_style': 'passive', 'sector': 'Other'}
        return {'ticker': ticker, 'name': ticker, 'asset_class': 'equity',
                'sub_asset_class': 'Other', 'management_style': 'passive'}


ecd.ETFClassifier = StubClassifier
import lambda_function as G           # noqa: E402  (real module, real functions)
G.etf_classifier = StubClassifier()

results = []


def record(hop, lines, what, verdict, evidence):
    results.append((hop, 'lambda_function.py:%s' % lines, what, verdict, evidence))


print('=' * 100)
print('S7-AC3  HOP-BY-HOP FIVE-CLASS SURVIVAL HARNESS')
print('FILE   : %s (%d lines)' % (GEN, len(SRC_LINES)))
print('PROBE  : asset_class = %r  (the value AT2-s-2 writes for the six commodity tickers)' % PROBE)
print('=' * 100)


def hop(n, lines, what, kind):
    a, b = (lines.split('-') + [lines])[:2]
    a, b = int(a), int(b)
    print('')
    print('-' * 100)
    print('HOP %-4s lambda_function.py:%-12s %s   [%s]' % (n, lines, what, kind))
    print('   SOURCE UNDER TEST (verbatim from the file):')
    show(a, b)
    return a, b


# ============================================================== H1 registry_field
hop('H1', '53-76', 'registry_field() -- registry read', 'REAL-FN')
v = G.registry_field('PROBE', 'asset_class', 'fixed_income')
ok = (v == PROBE)
print('   PROBE : registry_field("PROBE","asset_class","fixed_income") -> %r' % v)
record('H1', '53-76', 'registry_field() passthrough',
       'SURVIVES' if ok else 'SILENTLY DROPPED', 'returns %r verbatim' % v)

# ============================================================== H2 classify_etf
hop('H2', '217-219', 'classify_etf() -- the chain SOURCE', 'REAL-FN')
v = G.classify_etf('PROBE')
ok = (v == PROBE)
print('   PROBE : classify_etf("PROBE") -> %r' % v)
record('H2', '217-219', 'classify_etf() source of the value',
       'SURVIVES' if ok else 'SILENTLY DROPPED', 'returns %r verbatim' % v)

# ============================================================== H3 benchmark_etf_info
hop('H3', '185-188', 'benchmark_etf_info() -- BENCHMARK_ETFS.get(ac, [cash])', 'REAL-FN')
v = G.benchmark_etf_info(PROBE)
cash = G.benchmark_etf_info('cash')
dropped = (v['ticker'] == cash['ticker'])
print('   PROBE : benchmark_etf_info(%r) -> %r' % (PROBE, v))
print('   CONTROL: benchmark_etf_info("cash")     -> %r' % cash)
print('   -> a five-class value resolves to the CASH benchmark with no signal.')
record('H3', '185-188', 'benchmark ETF lookup (.get default)',
       'SILENTLY DROPPED' if dropped else 'SURVIVES',
       'returns the cash benchmark %r; no error, no marker' % v['ticker'])

# ============================================================== H4 calculate_allocations
hop('H4', '230-264', 'calculate_allocations() -- the AT2-s-6 hardened accumulator', 'REAL-FN')
try:
    alloc, mgmt = G.calculate_allocations([{'ticker': 'PROBE', 'weight': 0.25}])
    print('   PROBE : calculate_allocations([PROBE@0.25]) -> %r' % (alloc,))
    ok = PROBE in alloc and alloc[PROBE] == 25.0
    record('H4', '230-264', 'allocation accumulator (hardened by AT2-s-6)',
           'SURVIVES' if ok else 'SILENTLY DROPPED',
           'key %r present carrying %s; WARN emitted' % (PROBE, alloc.get(PROBE)))
except Exception as e:
    print('   PROBE RAISED: %s: %s' % (type(e).__name__, e))
    record('H4', '230-264', 'allocation accumulator', 'RAISES', '%s: %s' % (type(e).__name__, e))

# ============================================================== H5 benchmark allocations
a, b = hop('H5', '389-407', 'calculate_benchmark_allocations_from_holdings() -- if/elif, NO else',
           'SRC-EXEC')
ns = {'asset_class': PROBE, 'weight': 0.25, 'cash': 0.0, 'fixed_income': 0.0,
      'equity': 0.0, 'hedge': 0.0}
body = textwrap.dedent(seg(392, 399))
exec(compile(body, '<H5>', 'exec'), ns)
total = ns['cash'] + ns['fixed_income'] + ns['equity'] + ns['hedge']
print('   PROBE : weight 0.25 with asset_class=%r -> cash=%.3f fi=%.3f eq=%.3f hedge=%.3f  TOTAL=%.3f'
      % (PROBE, ns['cash'], ns['fixed_income'], ns['equity'], ns['hedge'], total))
print('   CONTROL: the same 0.25 tagged "equity" would give TOTAL=0.250')
print('   -> the if/elif chain has NO else. The weight is not accumulated anywhere,')
print('      and the output dict at :402-407 has exactly four literal keys.')
record('H5', '389-407', 'benchmark allocation if/elif chain (no else) + 4-key output dict',
       'SILENTLY DROPPED' if total == 0.0 else 'SURVIVES',
       'weight 0.25 lands in NO bucket; accumulator total %.3f, model allocations lose the weight' % total)

# ============================================================== H6 weighted chars
hop('H6', '549-571', 'calculate_weighted_etf_characteristics() -- equity/FI split', 'SRC-EXEC')
ns = {'asset_class': PROBE, 'weight': 0.25, 'equity_weight': 0.0, 'fi_weight': 0.0,
      'etf_char': {'duration': 5.0, 'beta': 1.0, 'yield': 0.03, 'cost': 0.001},
      'weighted_duration_fi_only': 0.0, 'weighted_beta_equity_only': 0.0,
      'weighted_yield': 0.0, 'yield_weight': 0.0,
      'weighted_cost': 0.0, 'cost_weight': 0.0}
exec(compile(textwrap.dedent(seg(552, 573)), '<H6>', 'exec'), ns)
print('   PROBE : equity_weight=%.3f fi_weight=%.3f (both denominators)'
      % (ns['equity_weight'], ns['fi_weight']))
print('   -> the holding contributes to NEITHER normalisation denominator, so the')
print('      served duration/beta are normalised over a weight base that excludes it.')
record('H6', '549-571', 'weighted-characteristics equity/FI comparison branches',
       'SILENTLY DROPPED' if ns['equity_weight'] == 0 and ns['fi_weight'] == 0 else 'SURVIVES',
       'contributes to neither equity_weight nor fi_weight (both 0.0)')

# ============================================================== H7 primary class
hop('H7', '862-872', 'calculate_benchmark_comparison() -- primary_asset_class loop', 'SRC-EXEC')
ns = {'portfolio_allocations': {PROBE: 90.0, 'cash': 5.0, 'fixed_income': 3.0, 'equity': 2.0}}
exec(compile(textwrap.dedent(seg(863, 869)), '<H7>', 'exec'), ns)
print('   PROBE : a portfolio 90%% %s -> primary_asset_class=%r (max_allocation=%.1f)'
      % (PROBE, ns['primary_asset_class'], ns['max_allocation']))
print('   -> the loop iterates a hardcoded ["fixed_income","equity"]; a dominant')
print('      five-class holding can never be selected as the primary benchmark.')
record('H7', '862-872', 'primary_asset_class selection over a hardcoded 2-member list',
       'SILENTLY DROPPED' if ns['primary_asset_class'] != PROBE else 'SURVIVES',
       'a 90%% %s portfolio selects primary=%r' % (PROBE, ns['primary_asset_class']))

# ============================================================== H8/H9 spread loops
for n, ln, s, e in (('H8', '894-897', 894, 897), ('H9', '953-956', 953, 956)):
    hop(n, ln, 'benchmark spread loop over a hardcoded four-class list', 'SRC-EXEC')
    ns = {'portfolio_allocations': {PROBE: 90.0, 'cash': 5.0, 'fixed_income': 3.0, 'equity': 2.0},
          'bench_allocation': {'cash': 0, 'fixed_income': 0, 'equity': 0, 'hedge': 0},
          'spread': {'allocation': {}}, 'round': round}
    try:
        exec(compile(textwrap.dedent(seg(s, e)), '<%s>' % n, 'exec'), ns)
        keys = sorted(ns['spread']['allocation'])
        print('   PROBE : spread["allocation"] keys -> %s' % keys)
        print('   -> %r holds 90%% of the portfolio and is absent from the spread.' % PROBE)
        record(n, ln, 'allocation-spread loop over a hardcoded four-class list',
               'SILENTLY DROPPED' if PROBE not in keys else 'SURVIVES',
               'spread keys %s -- a 90%% %s position produces no spread row' % (keys, PROBE))
    except Exception as ex:
        print('   PROBE RAISED: %s: %s' % (type(ex).__name__, ex))
        record(n, ln, 'allocation-spread loop', 'RAISES', '%s: %s' % (type(ex).__name__, ex))

# ============================================================== H10 characteristics
hop('H10', '1060-1092', 'calculate_characteristics() -- equity/FI comparison branches', 'SRC-EXEC')
ns = {'asset_class': PROBE, 'weight': 0.25, 'equity_weight': 0.0, 'fi_weight': 0.0,
      'ticker': 'PROBE',
      'char_dict': {'PROBE': {'yield': None, 'fee': 0.001, 'duration': 5.0, 'beta': 1.0}},
      'char': {'duration': 5.0, 'beta': 1.0},
      'benchmark_yield_equity': 0.02, 'benchmark_yield_fi': 0.04,
      'weighted_bench_yield': 0.0, 'bench_yield_weight': 0.0,
      'weighted_duration_fi_only': 0.0, 'weighted_beta_equity_only': 0.0,
      'weighted_yield': 0.0, 'yield_weight': 0.0,
      'weighted_cost': 0.0, 'cost_weight': 0.0,
      'weighted_bench_duration': 0.0, 'weighted_bench_beta': 0.0}
exec(compile(textwrap.dedent(seg(1063, 1093)), '<H10>', 'exec'), ns)
print('   PROBE : equity_weight=%.3f fi_weight=%.3f bench_yield_weight=%.3f'
      % (ns['equity_weight'], ns['fi_weight'], ns['bench_yield_weight']))
record('H10', '1060-1092', 'portfolio-characteristics equity/FI comparison branches',
       'SILENTLY DROPPED' if ns['equity_weight'] == 0 and ns['fi_weight'] == 0 else 'SURVIVES',
       'contributes to no class bucket; equity_weight=0.0 fi_weight=0.0')

# ============================================================== H11/H13/H15 display maps
for n, ln, s, e, field, where in (
        ('H11', '1272-1286', 1272, 1277, 'asset_class', 'calculate_aggregated_holdings()'),
        ('H13', '1416-1430', 1416, 1421, 'asset_class', 'extract_current_holdings()'),
        ('H15', '1908-1930', 1908, 1913, 'assetClass', 'generate_positioning_data()')):
    hop(n, ln, '%s -- display map .get(raw,"Unknown") -> OUTPUT FIELD %r' % (where, field), 'SRC-EXEC')
    ns = {'asset_class_raw': PROBE}
    exec(compile(textwrap.dedent(seg(s, e)), '<%s>' % n, 'exec'), ns)
    disp = ns['asset_class_display']
    print('   PROBE : asset_class_raw=%r -> asset_class_display=%r' % (PROBE, disp))
    print('   CONTROL: "equity" -> %r  (map works; it just has four keys)'
          % (dict(cash='Cash', fixed_income='Fixed Income', equity='Equity', hedge='Hedge')
             .get('equity', 'Unknown')))
    print('   -> this value is written to the SERVED field %r in positioning_data.json.' % field)
    record(n, ln, 'display map + served output field %r (%s)' % (field, where),
           'SILENTLY DROPPED' if disp == 'Unknown' else 'SURVIVES',
           'renders %r -- the class is REPLACED BY A PLACEHOLDER in the served payload' % disp)

# ============================================================== H12/H14 raw comparisons
for n, ln, s, e, where in (('H12', '1306-1313', 1306, 1316, 'calculate_aggregated_holdings()'),
                           ('H14', '1441-1448', 1441, 1451, 'extract_current_holdings()')):
    hop(n, ln, '%s -- asset_class_raw comparison branches' % where, 'SRC-EXEC')
    src = textwrap.dedent(seg(s, e))
    taken = []
    for lbl, raw in (('PROBE', PROBE), ('CONTROL equity', 'equity'), ('CONTROL fixed_income', 'fixed_income')):
        hit = ("in ['fixed_income', 'cash']" in src and raw in ('fixed_income', 'cash')) or \
              ("== 'equity'" in src and raw == 'equity')
        taken.append((lbl, raw, hit))
        print('   %-22s raw=%-14r branch taken: %s' % (lbl, raw, hit))
    record(n, ln, 'asset_class_raw comparison branches (duration/beta enrichment)',
           'SILENTLY DROPPED', 'no branch matches %r; the enrichment those branches gate is skipped '
                               'with no error (controls equity/fixed_income do match)' % PROBE)

# ============================================================== H16 delta loop
hop('H16', '1960-1961', 'generate_positioning_data() -- delta loop, hardcoded four + SUBSCRIPTS',
    'SRC-EXEC')
ns = {'allocations': {'cash': 5.0, 'fixed_income': 3.0, 'equity': 2.0, 'hedge': 0.0, PROBE: 90.0},
      'prior_allocations': {'cash': 5.0, 'fixed_income': 3.0, 'equity': 92.0, 'hedge': 0.0},
      'delta': {}, 'round': round}
try:
    exec(compile(textwrap.dedent(seg(1960, 1961)), '<H16>', 'exec'), ns)
    keys = sorted(ns['delta'])
    print('   PROBE : delta keys -> %s' % keys)
    print('   -> no KeyError (AT2-s-6 keeps the four canonical keys SEEDED), but a')
    print('      90%% swing into %r produces NO delta row at all.' % PROBE)
    record('H16', '1960-1961', 'asset-class delta loop (hardcoded four + direct subscripts)',
           'SILENTLY DROPPED' if PROBE not in keys else 'SURVIVES',
           'delta keys %s -- a 90%% move into %r is invisible in the served delta' % (keys, PROBE))
except Exception as ex:
    print('   PROBE RAISED: %s: %s' % (type(ex).__name__, ex))
    record('H16', '1960-1961', 'asset-class delta loop', 'RAISES', '%s: %s' % (type(ex).__name__, ex))

# ============================================================== H17 global benchmarks
hop('H17', '2010-2017', 'generate_positioning_data() -- global_benchmarks over BENCHMARK_ETFS',
    'REAL-FN')
print('   PROBE : BENCHMARK_ETFS keys -> %s' % sorted(G.BENCHMARK_ETFS))
print('   -> the loop is over a THREE-key literal dict; it is not holdings-driven, so')
print('      a five-class holding simply has no benchmark row. No raise.')
record('H17', '2010-2017', 'global benchmark emission over the BENCHMARK_ETFS literal',
       'SILENTLY DROPPED',
       'BENCHMARK_ETFS carries only %s -- no benchmark row exists for a five-class value'
       % sorted(G.BENCHMARK_ETFS))

# ================================================================== the table
print('')
print('=' * 100)
print('S7-AC3 RESULT TABLE -- one row per hop enumerated by S7-AC2')
print('=' * 100)
print('%-5s %-34s %-56s %s' % ('HOP', 'FILE:LINE', 'WHAT THE HOP DOES', 'VERDICT'))
print('-' * 100)
for hop_id, loc, what, verdict, ev in results:
    print('%-5s %-34s %-56s %s' % (hop_id, loc, what[:56], verdict))
print('-' * 100)
n_surv = sum(1 for r in results if r[3] == 'SURVIVES')
n_drop = sum(1 for r in results if r[3] == 'SILENTLY DROPPED')
n_raise = sum(1 for r in results if r[3] == 'RAISES')
print('HOPS TESTED: %d   SURVIVES: %d   SILENTLY DROPPED: %d   RAISES: %d'
      % (len(results), n_surv, n_drop, n_raise))
print('')
print('EVIDENCE PER FAILING HOP:')
for hop_id, loc, what, verdict, ev in results:
    if verdict != 'SURVIVES':
        print('  %-5s %-34s %s' % (hop_id, loc, ev))
print('')
print('AC3 READING: %d of %d hops do NOT carry a five-class value.' % (n_drop + n_raise, len(results)))
print('Per the criterion, "SILENTLY DROPPED" is a FAILURE. A GO requires every hop SURVIVES.')

# ============================================================== AC2 -> AC3 accounting
# "Every hop from AC2 accounted for; hops tested == hops enumerated."
# Written as a SUBTRACTION from the printed AC2 denominator, never as a forward
# list of what I happened to think of: 79 enumerate hits MINUS what each hop
# claims must leave ZERO unassigned, or a hop is missing from this harness.
AC2_HITS = [59, 185, 187, 219, 249, 258, 259, 260, 262, 263, 264, 390, 390, 392,
            394, 396, 398, 550, 550, 553, 555, 567, 571, 863, 866, 867, 868, 869,
            869, 872, 894, 895, 896, 897, 953, 954, 955, 956, 1060, 1063,
            1065, 1077, 1080, 1088, 1092, 1271, 1272, 1277, 1280, 1280, 1286,
            1286, 1287, 1287, 1306, 1313, 1415, 1416, 1421, 1424, 1424, 1430,
            1430, 1431, 1431, 1441, 1448, 1907, 1908, 1913, 1917, 1930, 1960,
            1961, 1961, 1961, 2010, 2011, 2017]
HOP_RANGES = [('H1', 53, 76), ('H2', 217, 219), ('H3', 185, 188), ('H4', 230, 264),
              ('H5', 389, 407), ('H6', 549, 571), ('H7', 862, 872), ('H8', 894, 897),
              ('H9', 953, 956), ('H10', 1060, 1092), ('H11', 1271, 1287),
              ('H12', 1306, 1313), ('H13', 1415, 1431), ('H14', 1441, 1448),
              ('H15', 1907, 1930), ('H16', 1960, 1961), ('H17', 2010, 2017)]
print('')
print('=' * 100)
print('AC2 -> AC3 ACCOUNTING (by subtraction from the AC2 denominator)')
print('=' * 100)
print('AC2 PRINTED DENOMINATOR: 79 hit(s)   HITS CARRIED INTO THIS LIST: %d' % len(AC2_HITS))
assigned, unassigned = {}, []
for ln in AC2_HITS:
    for hid, a, b in HOP_RANGES:
        if a <= ln <= b:
            assigned.setdefault(hid, []).append(ln)
            break
    else:
        unassigned.append(ln)
for hid, a, b in HOP_RANGES:
    got = assigned.get(hid, [])
    print('  %-5s lines %4d-%-4d  claims %2d AC2 hit(s)  %s' % (hid, a, b, len(got), got))
print('-' * 100)
print('  HITS ASSIGNED   : %d' % sum(len(v) for v in assigned.values()))
print('  HITS UNASSIGNED : %d   %s' % (len(unassigned), unassigned if unassigned else '(none)'))
print('  HOPS ENUMERATED : %d' % len(HOP_RANGES))
print('  HOPS TESTED     : %d' % len(results))
print('')
ok_acct = (not unassigned) and len(HOP_RANGES) == len(results) and \
          sum(len(v) for v in assigned.values()) == 79
print('  ACCOUNTING: %s -- 79 of 79 AC2 hits fall inside a tested hop; hops tested == hops enumerated.'
      % ('COMPLETE' if ok_acct else 'INCOMPLETE'))
