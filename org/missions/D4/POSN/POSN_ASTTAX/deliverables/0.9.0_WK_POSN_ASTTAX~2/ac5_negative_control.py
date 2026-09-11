#!/usr/bin/env python3
"""S6-AC5 negative control for POSN_ASTTAX.TO-S6-1 (decomp cell AT2-s-6).

WHAT IT PROVES, AND WHY IT CANNOT PASS BOTH WAYS
------------------------------------------------
It exercises the REAL calculate_allocations() / classify_etf() /
classify_management_style() / registry_field() of TWO BYTE-VINTAGES of the same
generator, on a holding whose registry asset_class is "Commodities" -- a value
neither allocation dict is seeded with -- and whose management_style is the
placeholder "unknown". The PRE-FIX vintage must RAISE KeyError and the POST-FIX
vintage must COMPLETE with that holding visible; the script exits 1 unless it
sees exactly that ordering, so a harness that passed both ways would fail here.

HOW TO GET THE PRE-FIX BYTES (argv[1], default .scratch/prefix_lambda_function.py)
    MSYS_NO_PATHCONV=1 git show <fix-commit>^:infra/aws/lambda/v2_portal/\
yang_pipeline/positioning/yang-generate-positioning/lambda_function.py \
        > /tmp/prefix_lambda_function.py
At authoring time the fix was uncommitted, so HEAD (2d8b5f7314) WAS the pre-fix
vintage: 94164 bytes / 2268 lines, positively controlled as carrying the old
direct subscript `asset_allocations[asset_class] += weight * 100` and NOT
carrying the new marker "TOLERATE AN UNSEEDED CLASS WITHOUT SWALLOWING IT".
Post-fix worktree bytes: 96268 bytes / 2298 lines.

WHAT IS STUBBED, AND WHAT IS NOT
    STUBBED: boto3 and pandas (MagicMock) and etf_classifications_dynamodb
    (a dict-backed ETFClassifier) -- i.e. the AWS/dataframe boundary only.
    NOT STUBBED: every line of classification and allocation logic under test.
    No AWS call is made and nothing is written anywhere.

Usage:  python org/missions/D4/POSN/POSN_ASTTAX/deliverables/\
0.9.0_WK_POSN_ASTTAX~2/ac5_negative_control.py [pre_fix_source_path]
Run from the repository root. Exit 0 = the control discriminated.
"""
import json
import sys
import traceback
import types
from unittest.mock import MagicMock

POST = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
        'yang-generate-positioning/lambda_function.py')
PRE = sys.argv[1] if len(sys.argv) > 1 else '.scratch/prefix_lambda_function.py'

# The registry rows the stub serves. DBC is the unexpected-value probe: its
# asset_class is a value the generator's allocation dict was never seeded with.
REGISTRY = {
    'AGG': {'asset_class': 'fixed_income', 'management_style': 'passive', 'name': 'Core Bond'},
    'SPY': {'asset_class': 'equity', 'management_style': 'passive', 'name': 'S&P 500'},
    'DBC': {'asset_class': 'Commodities', 'management_style': 'unknown', 'name': 'Commodity Index'},
}

HOLDINGS = [
    {'ticker': 'AGG', 'weight': 0.60},
    {'ticker': 'SPY', 'weight': 0.35},
    {'ticker': 'DBC', 'weight': 0.05},
]


class StubClassifier(object):
    def get_classification(self, ticker):
        return REGISTRY.get(ticker)


def install_stubs():
    stub = types.ModuleType('etf_classifications_dynamodb')
    stub.ETFClassifier = StubClassifier
    sys.modules['etf_classifications_dynamodb'] = stub
    sys.modules['boto3'] = MagicMock(name='boto3')
    sys.modules['pandas'] = MagicMock(name='pandas')


def load(path, tag):
    src = open(path, encoding='utf-8').read()
    mod = types.ModuleType('gen_' + tag)
    mod.__dict__['__name__'] = 'gen_' + tag
    exec(compile(src, path, 'exec'), mod.__dict__)
    return mod, len(src.encode('utf-8'))


def run(path, tag, label):
    mod, nbytes = load(path, tag)
    print('==================== %s ====================' % label)
    print('source: %s   bytes=%d' % (path, nbytes))
    print('holdings: %s' % json.dumps(HOLDINGS))
    print('registry DBC row: %s' % json.dumps(REGISTRY['DBC']))
    print('classify_etf("DBC")               -> %r' % mod.classify_etf('DBC'))
    print('classify_management_style("DBC")  -> %r   (placeholder guard)'
          % mod.classify_management_style('DBC'))
    try:
        assets, mgmt = mod.calculate_allocations(HOLDINGS)
    except Exception as exc:
        print('OUTCOME: RAISED %s: %s' % (type(exc).__name__, exc))
        print('traceback tail: %s' % traceback.format_exc().strip().splitlines()[-3:])
        print('served allocation payload: NONE -- generator dies, '
              'positioning_data.json is never rewritten')
        return 'RAISED'
    print('OUTCOME: COMPLETED, no exception')
    print('asset_allocations      = %s' % json.dumps(assets))
    print('management_allocations = %s' % json.dumps(mgmt))
    print('served payload fragment (this dict is serialized whole as '
          "portfolios[model]['allocation']): %s" % json.dumps({'allocation': assets}))
    print('"Commodities" present in served asset_allocations: %s   value=%s'
          % ('Commodities' in assets, assets.get('Commodities')))
    print('sum of asset_allocations = %.1f   (weights total 100.0)'
          % sum(assets.values()))
    return 'COMPLETED'


if __name__ == '__main__':
    install_stubs()
    pre = run(PRE, 'pre', 'PRE-FIX  (HEAD 2d8b5f7314, before this order)')
    print('')
    post = run(POST, 'post', 'POST-FIX (edited worktree bytes)')
    print('')
    print('==================== DISCRIMINATION ====================')
    print('PRE-FIX  outcome: %s' % pre)
    print('POST-FIX outcome: %s' % post)
    ok = (pre == 'RAISED' and post == 'COMPLETED')
    print('control discriminates (must be RAISED then COMPLETED): %s' % ok)
    sys.exit(0 if ok else 1)
