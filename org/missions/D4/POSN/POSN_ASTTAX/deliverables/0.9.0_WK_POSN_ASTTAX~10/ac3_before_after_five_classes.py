"""T1-AC3 -- BEFORE/AFTER on the SAME input, through the REAL served path.

For each of Commodities, Structured and Alternatives this drives the generator's
own `generate_positioning_data()` -- the function whose return value IS
positioning_data.json -- twice on ONE synthetic model PKL:

  BEFORE  the file's bytes at the worktree base commit (git show <pin>:<path>)
  AFTER   the bytes in the worktree now

Nothing is stubbed except the two things that would reach AWS:
  * `etf_classifications_dynamodb.ETFClassifier` -> a controlled registry row.
    This is the INPUT under test (it is what a retag changes), not the code.
  * `load_aum_data` -> None, so the current-holdings extraction is skipped
    instead of calling S3. It reads no asset_class and is not a hop.
Every function that maps, buckets or renders an asset class is the real one.

THE TWO HALVES, MEASURED SEPARATELY (the weight half is the one that hides):
  served class   portfolios[M].holdings[PROBE].assetClass
  served weight  the weight the payload publishes FOR THAT CLASS at the
                 five-class grain = the summed weight of the holdings the
                 payload labels with it. A consumer asking "what is my
                 Commodities allocation" can only group by the label the
                 payload serves; when that label is 'Unknown' the Commodities
                 line has no holdings and reads 0.000.

DISCLOSED, because it softens nothing and hiding it would be the overclaim:
AT2-s-6 already made the raw-keyed accumulator carry an unseeded value under
its own key, so under the OLD bytes `allocation['commodities']` is NON-zero
while the served label is 'Unknown'. The served delta row and the benchmark
spread row for that class are ABSENT under the old bytes. All four readings are
printed per arm.

FALSIFY ARM: the identical comparison with the OLD bytes in BOTH positions. It
MUST fail, or the AFTER assertions are not discriminating.

Read-only: imports two module versions and calls them. Writes nothing, deploys
nothing, touches no registry row.
POSN_ASTTAX.TO-T1-1 / cell AT3-s-1 / 0.9.0_WK_POSN_ASTTAX~10
"""
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import types
from contextlib import redirect_stdout

import pandas as pd

GEN = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
       'yang-generate-positioning/lambda_function.py')
OLD_PIN = '651ffd4f16'          # the worktree base -- the bytes before this cell
MODEL = 'INT'
PROBE = 'PROBE'
PROBE_WEIGHT = 0.025            # 2.5% of the model
CASES = [('commodities', 'Commodities'),
         ('structured', 'Structured'),
         ('alternatives', 'Alternatives')]
SPELLINGS = ['commodities', 'Commodities', 'COMMODITIES', 'commodity',
             'Fixed Income', 'alternative']


def old_bytes_file():
    """The generator's source at OLD_PIN, materialised to a temp file."""
    src = subprocess.check_output(['git', 'show', '%s:%s' % (OLD_PIN, GEN)])
    handle, path = tempfile.mkstemp(suffix='_old_lambda_function.py')
    with os.fdopen(handle, 'wb') as out:
        out.write(src)
    return path


def make_registry(probe_asset_class):
    """The registry rows the generator will read. PROBE carries the class under test."""
    return {
        'IVV': {'ticker': 'IVV', 'name': 'iShares Core S&P 500 ETF',
                'asset_class': 'equity', 'sub_asset_class': 'Large',
                'management_style': 'passive', 'sector': 'Broad'},
        'AGG': {'ticker': 'AGG', 'name': 'iShares Core US Aggregate Bond ETF',
                'asset_class': 'fixed_income', 'sub_asset_class': 'Intermediate',
                'management_style': 'passive', 'sector': 'Aggregate'},
        'BIL': {'ticker': 'BIL', 'name': 'SPDR Bloomberg 1-3 Month T-Bill ETF',
                'asset_class': 'cash', 'sub_asset_class': 'Short Duration',
                'management_style': 'passive', 'sector': 'Government'},
        PROBE: {'ticker': PROBE, 'name': 'Probe Fund',
                'asset_class': probe_asset_class, 'sub_asset_class': 'Gold',
                'management_style': 'passive', 'sector': 'Other'},
    }


def load_generator(tag, path, registry):
    """Import one version of the generator with a controlled registry."""
    class StubClassifier(object):
        def __init__(self, *args, **kwargs):
            pass

        def get_classification(self, ticker):
            return registry.get(ticker)

    stub = types.ModuleType('etf_classifications_dynamodb')
    stub.ETFClassifier = StubClassifier
    sys.modules['etf_classifications_dynamodb'] = stub

    name = 'gen_%s' % tag
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    module.etf_classifier = StubClassifier()
    module.load_aum_data = lambda *args, **kwargs: None   # no S3, no AWS
    return module


def build_pkl():
    """One synthetic model PKL. IDENTICAL for every arm -- it is the SAME INPUT."""
    latest, prior = pd.Timestamp('2026-09-10'), pd.Timestamp('2026-09-09')
    holdings = pd.DataFrame([
        {'date': prior, 'ticker': 'IVV', 'weight': 0.600, 'model': MODEL},
        {'date': prior, 'ticker': 'AGG', 'weight': 0.400, 'model': MODEL},
        {'date': latest, 'ticker': 'IVV', 'weight': 0.600, 'model': MODEL},
        {'date': latest, 'ticker': 'AGG', 'weight': 0.375, 'model': MODEL},
        {'date': latest, 'ticker': PROBE, 'weight': PROBE_WEIGHT, 'model': MODEL},
    ])
    benchmark_holdings = pd.DataFrame([
        {'ticker': 'AGG', 'weight': 0.40, 'model': MODEL},
        {'ticker': 'IVV', 'weight': 0.60, 'model': MODEL},
    ])
    characteristics = pd.DataFrame([
        {'ticker': 'IVV', 'name': 'iShares Core S&P 500 ETF', 'fee': 0.0003,
         'yield': 1.30, 'duration': None, 'beta': 1.00},
        {'ticker': 'AGG', 'name': 'iShares Core US Aggregate Bond ETF', 'fee': 0.0003,
         'yield': 4.10, 'duration': 6.10, 'beta': None},
        {'ticker': 'BIL', 'name': 'SPDR Bloomberg 1-3 Month T-Bill ETF', 'fee': 0.0014,
         'yield': 4.30, 'duration': 0.10, 'beta': None},
        {'ticker': PROBE, 'name': 'Probe Fund', 'fee': 0.0040,
         'yield': 0.00, 'duration': None, 'beta': None},
    ])
    return {'holdings': holdings, 'benchmark_holdings': benchmark_holdings,
            'etf_characteristics': characteristics}


def serve(module):
    """Run the generator and return (payload, captured stdout)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        payload = module.generate_positioning_data(
            build_pkl(), '20260910', None, '2026-09-10')
    return payload, buffer.getvalue()


def readings(payload, raw_value, label):
    """The four served readings for the class under test."""
    portfolio = payload['portfolios'][MODEL]
    probe = [h for h in portfolio['holdings'] if h['ticker'] == PROBE][0]
    by_label = sum(h['weight'] for h in portfolio['holdings']
                   if h['assetClass'] == label)
    key = str(raw_value).strip().lower().replace('-', '_').replace(' ', '_')
    return {
        'served_class': probe['assetClass'],
        'recognized': probe['assetClassRecognized'],
        'five_class_weight': round(by_label, 6),
        'allocation_raw_key': portfolio['allocation'].get(key, '<ABSENT>'),
        'delta_row': portfolio['delta'].get(key, '<ABSENT>'),
        'spread_row': portfolio['benchmark']['spread']['allocation'].get(key, '<ABSENT>'),
        'allocation_keys': list(portfolio['allocation']),
    }


def show(arm, raw_value, label, reading):
    print('  %-6s served assetClass      : %r' % (arm, reading['served_class']))
    print('  %-6s assetClassRecognized   : %r' % (arm, reading['recognized']))
    print('  %-6s served weight for %-13s: %.3f   (input weight %.3f)'
          % (arm, label, reading['five_class_weight'], PROBE_WEIGHT))
    print('  %-6s allocation[%r] : %s' % (arm, label.lower().replace(' ', '_'),
                                          reading['allocation_raw_key']))
    print('  %-6s delta[%r]      : %s' % (arm, label.lower().replace(' ', '_'),
                                          reading['delta_row']))
    print('  %-6s spread[%r]     : %s' % (arm, label.lower().replace(' ', '_'),
                                          reading['spread_row']))
    print('  %-6s allocation keys        : %s' % (arm, reading['allocation_keys']))


def judge(before, after, label):
    """The criterion, split into its two halves, per arm."""
    before_ok = (before['served_class'] == 'Unknown'
                 and round(before['five_class_weight'], 3) == 0.000)
    after_ok = (after['served_class'] == label
                and after['five_class_weight'] != 0
                and abs(after['five_class_weight'] - PROBE_WEIGHT) < 1e-9)
    return before_ok, after_ok


def run_case(old_path, raw_value, label, after_path, arm_name):
    print('')
    print('=' * 94)
    print('CASE %s   registry asset_class = %r   PROBE weight %.3f   model %s   [%s]'
          % (label, raw_value, PROBE_WEIGHT, MODEL, arm_name))
    print('=' * 94)
    registry = make_registry(raw_value)
    before_mod = load_generator('before_%s_%s' % (label.lower(), arm_name),
                                old_path, registry)
    after_mod = load_generator('after_%s_%s' % (label.lower(), arm_name),
                               after_path, registry)
    before_payload, before_log = serve(before_mod)
    after_payload, after_log = serve(after_mod)
    before = readings(before_payload, raw_value, label)
    after = readings(after_payload, raw_value, label)
    show('BEFORE', raw_value, label, before)
    print('  ' + '-' * 90)
    show('AFTER', raw_value, label, after)
    before_ok, after_ok = judge(before, after, label)
    print('  BEFORE assertion (reads %r AND weight 0.000)        : %s'
          % ('Unknown', 'HOLDS' if before_ok else 'DOES NOT HOLD'))
    print('  AFTER  assertion (reads %r AND weight == input) : %s'
          % (label, 'HOLDS' if after_ok else 'DOES NOT HOLD'))
    for line in after_log.splitlines():
        if PROBE in line and (line.startswith('WARN:') or line.startswith('OK: c')):
            print('  AFTER  generator line: %s' % line)
    for line in before_log.splitlines():
        if PROBE in line and line.startswith('WARN:'):
            print('  BEFORE generator line: %s' % line)
    return before_ok, after_ok


def spelling_table(after_path):
    print('')
    print('=' * 94)
    print('SPELLING ROBUSTNESS (AFTER bytes only) -- the retag cell AT3-s-6 has not')
    print('fixed its raw spelling. What each spelling renders as, and its weight:')
    print('=' * 94)
    print('  %-16s %-16s %-8s %s' % ('REGISTRY VALUE', 'SERVED LABEL', 'WEIGHT', 'RECOGNIZED'))
    for index, spelling in enumerate(SPELLINGS):
        module = load_generator('spell_%d' % index, after_path, make_registry(spelling))
        payload, _ = serve(module)
        portfolio = payload['portfolios'][MODEL]
        probe = [h for h in portfolio['holdings'] if h['ticker'] == PROBE][0]
        weight = sum(h['weight'] for h in portfolio['holdings']
                     if h['assetClass'] == probe['assetClass'] and h['ticker'] == PROBE)
        print('  %-16r %-16r %-8.3f %r'
              % (spelling, probe['assetClass'], weight, probe['assetClassRecognized']))


def main():
    print('=' * 94)
    print('T1-AC3  BEFORE/AFTER -- five classes carried through the positioning generator')
    print('FILE   : %s' % GEN)
    print('BEFORE : git show %s:<file>   (worktree base, the bytes before AT3-s-1)' % OLD_PIN)
    print('AFTER  : the worktree bytes')
    print('=' * 94)
    old_path = old_bytes_file()
    results = []
    for raw_value, label in CASES:
        results.append((label,) + run_case(old_path, raw_value, label, GEN, 'REAL'))

    spelling_table(GEN)

    print('')
    print('=' * 94)
    print('FALSIFY ARM -- the OLD bytes in BOTH positions. The AFTER assertion MUST FAIL.')
    print('=' * 94)
    falsify = []
    for raw_value, label in CASES:
        falsify.append((label,) + run_case(old_path, raw_value, label, old_path, 'FALSIFY'))

    print('')
    print('=' * 94)
    print('T1-AC3 RESULT')
    print('=' * 94)
    print('%-16s %-22s %s' % ('CLASS', 'BEFORE reads Unknown/0', 'AFTER reads label/weight'))
    for label, before_ok, after_ok in results:
        print('%-16s %-22s %s' % (label, 'HOLDS' if before_ok else 'FAIL',
                                  'HOLDS' if after_ok else 'FAIL'))
    real_ok = all(before_ok and after_ok for _, before_ok, after_ok in results)
    falsify_failed = all(not after_ok for _, _, after_ok in falsify)
    print('')
    print('REAL ARM      : %d of %d classes satisfy BOTH halves' % (
        sum(1 for _, b, a in results if b and a), len(results)))
    print('FALSIFY ARM   : %d of %d AFTER assertions FAILED on the old bytes (must be %d)'
          % (sum(1 for _, _, a in falsify if not a), len(falsify), len(falsify)))
    verdict = real_ok and falsify_failed
    print('T1-AC3        : %s' % ('PASS' if verdict else 'FAIL'))
    os.unlink(old_path)
    return 0 if verdict else 1


if __name__ == '__main__':
    sys.exit(main())
