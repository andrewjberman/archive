"""T1-AC4 -- THE SILENT-ZERO PATH IS CLOSED AND SAYS SO OUT LOUD.

Feeds a value the ratified taxonomy does NOT contain ('Fine Wine Fund') through
every allocation chain in the generator and reads two things:

  (1) WHERE THE WEIGHT WENT. It must not vanish. A chain that neither raises nor
      buckets is the failure this cell exists to remove: the class line renders
      0.000 and a zero reads exactly like a real allocation.
  (2) WHAT WAS SAID. A carried-but-unnamed value is still an unaudited bucket,
      so every chain must emit a WARN NAMING THE VALUE AS THE REGISTRY HOLDS IT.

Four probes, then the TOTALS, then the two controls that stop this from being a
test that passes on anything:

  CONTROL-SENTINEL   the unknown sentinel must stay DISTINGUISHABLE from a
                     value outside the taxonomy -- `asset_class_recognized`
                     False vs True. AT2-s-1 owns that distinction and AT3-s-1
                     must not have collapsed it.
  CONTROL-RATIFIED   a ratified class must NOT trip any of these paths, or the
                     WARN means nothing.

Read-only. No AWS, no registry write, no deploy.
POSN_ASTTAX.TO-T1-1 / cell AT3-s-1 / 0.9.0_WK_POSN_ASTTAX~10
"""
import importlib.util
import io
import sys
import types
from contextlib import redirect_stdout

import pandas as pd

GEN = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
       'yang-generate-positioning/lambda_function.py')
GARBAGE = 'Fine Wine Fund'      # a real-looking value the taxonomy does not hold
MODEL = 'INT'
PROBE = 'PROBE'
PROBE_WEIGHT = 0.025


def load_generator(tag, asset_class_value):
    """Import the worktree generator with PROBE carrying `asset_class_value`."""
    registry = {
        'IVV': {'ticker': 'IVV', 'name': 'iShares Core S&P 500 ETF',
                'asset_class': 'equity', 'sub_asset_class': 'Large',
                'management_style': 'passive', 'sector': 'Broad'},
        'AGG': {'ticker': 'AGG', 'name': 'iShares Core US Aggregate Bond ETF',
                'asset_class': 'fixed_income', 'sub_asset_class': 'Intermediate',
                'management_style': 'passive', 'sector': 'Aggregate'},
        PROBE: {'ticker': PROBE, 'name': 'Probe Fund',
                'asset_class': asset_class_value, 'sub_asset_class': 'Other',
                'management_style': 'passive', 'sector': 'Other'},
    }

    class StubClassifier(object):
        def __init__(self, *args, **kwargs):
            pass

        def get_classification(self, ticker):
            return registry.get(ticker)

    stub = types.ModuleType('etf_classifications_dynamodb')
    stub.ETFClassifier = StubClassifier
    sys.modules['etf_classifications_dynamodb'] = stub
    name = 'ac4_gen_%s' % tag
    spec = importlib.util.spec_from_file_location(name, GEN)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    module.etf_classifier = StubClassifier()
    return module


def capture(func, *args):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


def warn_lines(log):
    return [line for line in log.splitlines() if line.startswith('WARN:')]


def probe_allocation_chain(module):
    """PROBE 1 -- calculate_allocations(): the portfolio allocation accumulator."""
    holdings = [{'ticker': 'IVV', 'weight': 0.600},
                {'ticker': 'AGG', 'weight': 0.375},
                {'ticker': PROBE, 'weight': PROBE_WEIGHT}]
    (allocations, _), log = capture(module.calculate_allocations, holdings)
    key = module.normalize_asset_class(GARBAGE)
    print('  allocation dict            : %s' % allocations)
    print('  weight under %-16r: %s' % (key, allocations.get(key, '<ABSENT>')))
    for line in warn_lines(log):
        print('  WARN VERBATIM              : %s' % line)
    carried = allocations.get(key)
    named = any(repr(GARBAGE) in line for line in warn_lines(log))
    print('  NOT silently zeroed        : %s   (weight %s, expected %s)'
          % (carried not in (None, 0, 0.0), carried, PROBE_WEIGHT * 100))
    print('  WARN names the value       : %s' % named)
    total = sum(value for value in allocations.values())
    ratified = sum(allocations.get(k, 0) for k in module.ASSET_CLASS_ORDER)
    print('  TOTALS: all keys sum to %.1f%%; the five ratified classes sum to %.1f%%;'
          % (total, ratified))
    print('          the %.1f%% difference is the unmatched value, PRESENT and NAMED,'
          % (total - ratified))
    print('          not missing from the payload and not folded into a real class.')
    return (carried == PROBE_WEIGHT * 100) and named and abs(total - 100.0) < 1e-9


def probe_benchmark_chain(module):
    """PROBE 2 -- calculate_benchmark_allocations_from_holdings(): the if/elif chain."""
    frame = pd.DataFrame([
        {'ticker': 'IVV', 'weight': 0.600, 'model': MODEL},
        {'ticker': 'AGG', 'weight': 0.375, 'model': MODEL},
        {'ticker': PROBE, 'weight': PROBE_WEIGHT, 'model': MODEL},
    ])
    allocations, log = capture(
        module.calculate_benchmark_allocations_from_holdings, frame)
    model_allocation = allocations[MODEL]
    key = module.normalize_asset_class(GARBAGE)
    print('  model %s allocation        : %s' % (MODEL, model_allocation))
    print('  weight under %-16r: %s' % (key, model_allocation.get(key, '<ABSENT>')))
    for line in warn_lines(log):
        print('  WARN VERBATIM              : %s' % line)
    carried = model_allocation.get(key)
    named = any(repr(GARBAGE) in line for line in warn_lines(log))
    total = sum(model_allocation.values())
    print('  NOT silently zeroed        : %s   (weight %s)'
          % (carried not in (None, 0, 0.0), carried))
    print('  WARN names the value       : %s' % named)
    print('  TOTALS: the model allocation sums to %.1f%% WITH the unmatched value'
          % total)
    print('          included. Dropping it would have summed to %.1f%% with nothing'
          % (total - (carried or 0)))
    print('          in the payload saying why.')
    return (carried == PROBE_WEIGHT * 100) and named and abs(total - 100.0) < 1e-9


def probe_display(module):
    """PROBE 3 -- asset_class_display_label(): the served label."""
    label, log = capture(module.asset_class_display_label, GARBAGE, 'AC4 probe')
    print('  served label               : %r' % label)
    for line in warn_lines(log):
        print('  WARN VERBATIM              : %s' % line)
    named = any(repr(GARBAGE) in line for line in warn_lines(log))
    print('  no sixth class minted      : %s   (label is the placeholder, not %r)'
          % (label == 'Unknown', GARBAGE))
    print('  WARN names the value       : %s' % named)
    return label == 'Unknown' and named


def probe_served_payload(module):
    """PROBE 4 -- the whole served payload: delta and spread rows too."""
    module.load_aum_data = lambda *args, **kwargs: None
    latest, prior = pd.Timestamp('2026-09-10'), pd.Timestamp('2026-09-09')
    pkl = {
        'holdings': pd.DataFrame([
            {'date': prior, 'ticker': 'IVV', 'weight': 0.600, 'model': MODEL},
            {'date': prior, 'ticker': 'AGG', 'weight': 0.400, 'model': MODEL},
            {'date': latest, 'ticker': 'IVV', 'weight': 0.600, 'model': MODEL},
            {'date': latest, 'ticker': 'AGG', 'weight': 0.375, 'model': MODEL},
            {'date': latest, 'ticker': PROBE, 'weight': PROBE_WEIGHT, 'model': MODEL},
        ]),
        'benchmark_holdings': pd.DataFrame([
            {'ticker': 'AGG', 'weight': 0.40, 'model': MODEL},
            {'ticker': 'IVV', 'weight': 0.60, 'model': MODEL},
        ]),
        'etf_characteristics': pd.DataFrame([
            {'ticker': 'IVV', 'name': 'iShares Core S&P 500 ETF', 'fee': 0.0003,
             'yield': 1.30, 'duration': None, 'beta': 1.00},
            {'ticker': 'AGG', 'name': 'iShares Core US Aggregate Bond ETF',
             'fee': 0.0003, 'yield': 4.10, 'duration': 6.10, 'beta': None},
            {'ticker': PROBE, 'name': 'Probe Fund', 'fee': 0.0040,
             'yield': 0.00, 'duration': None, 'beta': None},
        ]),
    }
    payload, log = capture(module.generate_positioning_data, pkl, '20260910',
                           None, '2026-09-10')
    portfolio = payload['portfolios'][MODEL]
    probe = [h for h in portfolio['holdings'] if h['ticker'] == PROBE][0]
    key = module.normalize_asset_class(GARBAGE)
    print('  served assetClass          : %r' % probe['assetClass'])
    print('  assetClassRecognized       : %r' % probe['assetClassRecognized'])
    print('  allocation[%r]  : %s' % (key, portfolio['allocation'].get(key, '<ABSENT>')))
    print('  delta[%r]       : %s' % (key, portfolio['delta'].get(key, '<ABSENT>')))
    print('  spread[%r]      : %s'
          % (key, portfolio['benchmark']['spread']['allocation'].get(key, '<ABSENT>')))
    for line in warn_lines(log):
        if PROBE in line or GARBAGE in line:
            print('  WARN VERBATIM              : %s' % line)
    return (portfolio['allocation'].get(key) == PROBE_WEIGHT * 100
            and portfolio['delta'].get(key) is not None
            and portfolio['benchmark']['spread']['allocation'].get(key) is not None)


def control_sentinel(module):
    """CONTROL -- the unknown sentinel stays distinguishable from a foreign value."""
    sentinel = module.UNCLASSIFIED_ASSET_CLASS
    label, log = capture(module.asset_class_display_label, sentinel, 'AC4 control')
    recognized = module.asset_class_is_recognized(sentinel)
    foreign_recognized = module.asset_class_is_recognized(GARBAGE)
    print('  sentinel %-14r label %r  recognized %r  WARNs %d'
          % (sentinel, label, recognized, len(warn_lines(log))))
    print('  foreign  %-14r label %r  recognized %r'
          % (GARBAGE, 'Unknown', foreign_recognized))
    print('  the two states are DISTINCT: %s' % (recognized != foreign_recognized))
    return (label == 'Unknown' and recognized is False
            and foreign_recognized is True and not warn_lines(log))


def control_ratified(module):
    """CONTROL -- a ratified class trips none of the loud paths."""
    holdings = [{'ticker': 'IVV', 'weight': 0.60}, {'ticker': 'AGG', 'weight': 0.40}]
    (allocations, _), log = capture(module.calculate_allocations, holdings)
    label, display_log = capture(module.asset_class_display_label,
                                 'commodities', 'AC4 control')
    print('  equity/FI allocations      : %s' % allocations)
    print('  WARNs on the clean path    : %d' % len(warn_lines(log)))
    print('  ratified %-14r label %r  WARNs %d'
          % ('commodities', label, len(warn_lines(display_log))))
    return (not warn_lines(log) and label == 'Commodities'
            and not warn_lines(display_log))


def main():
    print('=' * 94)
    print('T1-AC4  THE NO-ELSE PROBE -- an unmatched value must not silently zero')
    print('FILE    : %s' % GEN)
    print('VALUE   : %r  (not a ratified class; not the sentinel)' % GARBAGE)
    print('=' * 94)
    module = load_generator('garbage', GARBAGE)
    results = []
    for title, probe in (
            ('PROBE 1 -- calculate_allocations() (portfolio allocation chain)',
             probe_allocation_chain),
            ('PROBE 2 -- calculate_benchmark_allocations_from_holdings() (the if/elif chain)',
             probe_benchmark_chain),
            ('PROBE 3 -- asset_class_display_label() (the served label)',
             probe_display),
            ('PROBE 4 -- generate_positioning_data() (the whole served payload)',
             probe_served_payload),
            ('CONTROL-SENTINEL -- sentinel vs foreign value stay distinct',
             control_sentinel),
            ('CONTROL-RATIFIED -- a ratified class trips nothing',
             control_ratified)):
        print('')
        print('-' * 94)
        print(title)
        print('-' * 94)
        results.append((title.split(' -- ')[0], probe(module)))

    print('')
    print('=' * 94)
    print('T1-AC4 RESULT')
    print('=' * 94)
    for name, ok in results:
        print('  %-20s %s' % (name, 'HOLDS' if ok else 'FAIL'))
    verdict = all(ok for _, ok in results)
    print('  %d of %d hold' % (sum(1 for _, ok in results if ok), len(results)))
    print('T1-AC4        : %s' % ('PASS' if verdict else 'FAIL'))
    return 0 if verdict else 1


if __name__ == '__main__':
    sys.exit(main())
