"""T1-AC6 -- READINGS ONLY. Graded by 3.0.0_SA_CVO~Z at L9. NO VERDICT HERE.

The question AC6 asks is whether the five classes are carried at the SERVED
grain END TO END, or only at the hops this cell happened to enumerate. So this
script deliberately drives the two served payloads the AC3 harness does NOT
reach -- `extract_current_holdings()` (hop K) and, inside it,
`calculate_aggregated_holdings()` (hop J). AC3 stubs `load_aum_data` to avoid
S3, and that stub is exactly what skips these two. Reporting AC3 alone would
have measured 3 of the 5 served payloads and called it end to end.

FIVE SERVED PAYLOADS in positioning_data.json, and where each is read here:
  1 portfolios[M].holdings[].assetClass        AC3 harness (hop L)
  2 portfolios[M].allocation / .delta          AC3 harness (hops E, L)
  3 portfolios[M].benchmark.allocation/.spread AC3 harness (hops F, H)
  4 current_holdings[M].holdings[].asset_class THIS script (hop K)
  5 current_holdings.AGG.holdings[].asset_class THIS script (hop J)

Every reading is printed for BOTH byte-sets on the SAME input. No pass, no fail,
no verdict -- the grade is the CVO's.

Read-only. No AWS: `load_aum_data` is replaced by a literal dict, which is the
same shape the real function returns.
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
OLD_PIN = '651ffd4f16'
MODEL = 'INT'
PROBE = 'PROBE'
PROBE_WEIGHT = 0.025
CASES = [('commodities', 'Commodities'),
         ('structured', 'Structured'),
         ('alternatives', 'Alternatives')]
AUM = {'UST': 1.0e7, 'ST': 1.0e7, 'INT': 1.0e7, 'LT': 1.0e7, 'ULT': 1.0e7}


def old_bytes_file():
    src = subprocess.check_output(['git', 'show', '%s:%s' % (OLD_PIN, GEN)])
    handle, path = tempfile.mkstemp(suffix='_old_lambda_function.py')
    with os.fdopen(handle, 'wb') as out:
        out.write(src)
    return path


def load_generator(tag, path, probe_class):
    registry = {
        'IVV': {'ticker': 'IVV', 'name': 'iShares Core S&P 500 ETF',
                'asset_class': 'equity', 'sub_asset_class': 'Large',
                'management_style': 'passive', 'sector': 'Broad'},
        'AGG': {'ticker': 'AGG', 'name': 'iShares Core US Aggregate Bond ETF',
                'asset_class': 'fixed_income', 'sub_asset_class': 'Intermediate',
                'management_style': 'passive', 'sector': 'Aggregate'},
        PROBE: {'ticker': PROBE, 'name': 'Probe Fund',
                'asset_class': probe_class, 'sub_asset_class': 'Gold',
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
    name = 'ac6_gen_%s' % tag
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    module.etf_classifier = StubClassifier()
    return module


def build_pkl():
    latest = pd.Timestamp('2026-09-10')
    holdings = pd.DataFrame(
        [{'date': latest, 'ticker': 'IVV', 'weight': 0.600, 'model': code}
         for code in AUM]
        + [{'date': latest, 'ticker': 'AGG', 'weight': 0.375, 'model': code}
           for code in AUM]
        + [{'date': latest, 'ticker': PROBE, 'weight': PROBE_WEIGHT, 'model': code}
           for code in AUM])
    characteristics = pd.DataFrame([
        {'ticker': 'IVV', 'name': 'iShares Core S&P 500 ETF', 'fee': 0.0003,
         'aum': 500000.0, 'yield': 1.30, 'duration': None, 'credit': None,
         'beta': 1.00, 'te': 0.02},
        {'ticker': 'AGG', 'name': 'iShares Core US Aggregate Bond ETF', 'fee': 0.0003,
         'aum': 120000.0, 'yield': 4.10, 'duration': 6.10, 'credit': 2.0,
         'beta': None, 'te': 0.03},
        {'ticker': PROBE, 'name': 'Probe Fund', 'fee': 0.0040,
         'aum': 900.0, 'yield': 0.00, 'duration': 4.40, 'credit': None,
         'beta': 0.35, 'te': 0.90},
    ])
    return {'holdings': holdings, 'etf_characteristics': characteristics}


def read_current(module):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        current = module.extract_current_holdings(build_pkl(), AUM, None)
    return current, buffer.getvalue()


def probe_row(portfolio):
    rows = [h for h in portfolio.get('holdings', []) if h['ticker'] == PROBE]
    return rows[0] if rows else None


def show(arm, current):
    for key in (MODEL, 'AGG'):
        portfolio = current.get(key)
        if portfolio is None:
            print('  %-6s %-4s payload ABSENT' % (arm, key))
            continue
        row = probe_row(portfolio)
        if row is None:
            print('  %-6s %-4s PROBE holding ABSENT' % (arm, key))
            continue
        print('  %-6s %-4s asset_class=%-14r asset_class_recognized=%-6r'
              ' weight=%-8s duration=%-6s beta=%s'
              % (arm, key, row.get('asset_class'), row.get('asset_class_recognized'),
                 row.get('weight'), row.get('duration'), row.get('beta')))


def main():
    print('=' * 100)
    print('T1-AC6  SERVED-GRAIN READINGS -- JUDGMENT CRITERION, NO VERDICT OFFERED')
    print('FILE   : %s' % GEN)
    print('BEFORE : git show %s:<file>      AFTER: the worktree bytes' % OLD_PIN)
    print('PAYLOADS READ HERE: current_holdings[%s] (hop K) and current_holdings.AGG'
          ' (hop J)' % MODEL)
    print('=' * 100)
    old_path = old_bytes_file()
    for raw_value, label in CASES:
        print('')
        print('CASE %s  (registry asset_class=%r, PROBE weight %.3f in all 5 models)'
              % (label, raw_value, PROBE_WEIGHT))
        print('-' * 100)
        before = load_generator('before_%s' % label.lower(), old_path, raw_value)
        after = load_generator('after_%s' % label.lower(), GEN, raw_value)
        before_current, _ = read_current(before)
        after_current, after_log = read_current(after)
        show('BEFORE', before_current)
        show('AFTER', after_current)
        for line in after_log.splitlines():
            if line.startswith('WARN:') and PROBE in line:
                print('  AFTER  generator line: %s' % line)

    print('')
    print('=' * 100)
    print('READINGS COMPLETE. 3 classes x 2 payloads x 2 byte-sets = 12 readings above.')
    print('T1-AC6 is JUDGMENT: whether this is "carried end to end at the served')
    print('grain" is graded by 3.0.0_SA_CVO~Z at L9. This script offers no verdict.')
    print('=' * 100)
    os.unlink(old_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
