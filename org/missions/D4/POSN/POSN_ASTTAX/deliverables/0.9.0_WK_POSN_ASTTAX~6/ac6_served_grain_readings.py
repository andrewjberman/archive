#!/usr/bin/env python3
"""S1-AC6 READINGS for POSN_ASTTAX.TO-S1-1 / cell AT2-s-1. NO VERDICT.

S1-AC6 is a JUDGMENT criterion graded by 3.0.0_SA_CVO~Z at L9: is "not
recognised" now genuinely distinguishable from a real class AT THE SERVED GRAIN,
or only inside the generator? This script produces the readings that question
needs and stops there. It states no verdict and must not be read as one.

WHY IT EXISTS SEPARATELY FROM THE S1-AC3 CONTROL: the control compares an absent
ticker with two GENUINE holdings of classes this producer can carry. The open
question is the THIRD population -- a security the registry tags with a RATIFIED
class the producer's served display map cannot carry. The PRD ratifies FIVE
classes (POSN_ASTTAX_PRD.md s.3 @66ded3a0c5: Fixed Income/Cash, Equity,
Structured, Commodities, Alternatives); all three served display maps in this
generator map exactly FOUR values and render everything else, via
`.get(asset_class_raw, 'Unknown')`, as the literal string 'Unknown'. So after
AT2-s-2's retag lands, 'Unknown' at the served grain will have TWO producers.
This script measures what each of them actually emits.

Run from anywhere; paths resolve from this file's location. Registry stubbed --
no AWS, no network.
"""

import json
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]
REL_PATH = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
            'yang-generate-positioning/lambda_function.py')

# Four populations, one per row of the reading table.
POPULATIONS = [
    ('SPY', 'equity',
     'RATIFIED and CARRYABLE -- a class the served display map holds'),
    ('GLD', 'Commodities',
     'RATIFIED by PRD s.3 and NOT CARRYABLE -- outside the display map'),
    ('VXX', 'Structured',
     'RATIFIED by PRD s.3 and NOT CARRYABLE -- outside the display map'),
    ('ZZZZ', None,
     'NOT IN THE REGISTRY -- the population this cell is about'),
]

REGISTRY = {}
for _ticker, _cls, _why in POPULATIONS:
    if _cls is not None:
        REGISTRY[_ticker] = {
            'ticker': _ticker,
            'asset_class': _cls,
            'sub_asset_class': '',
            'management_style': 'passive',
            'name': 'Row tagged ' + _cls,
        }

CHARS = {
    'name': 'Security Under Test',
    'fee': 0.001,
    'aum': 1000.0,
    'active': 0,
    'yield': 0.02,
    'duration': 5.0,
    'credit': 'AA',
    'beta': 1.0,
}


class StubClassifier(object):
    """Stands in for ETFClassifier. Never touches DynamoDB."""

    def get_classification(self, ticker):
        return REGISTRY.get(ticker)


def load_new_module():
    src = (REPO_ROOT / REL_PATH).read_text(encoding='utf-8')
    if 'UNCLASSIFIED_ASSET_CLASS' not in src:
        raise RuntimeError('ERROR: worktree bytes carry no sentinel')
    stub_mod = types.ModuleType('etf_classifications_dynamodb')
    stub_mod.ETFClassifier = StubClassifier
    sys.modules['etf_classifications_dynamodb'] = stub_mod
    mod = types.ModuleType('positioning_after')
    mod.__file__ = 'positioning_after'
    exec(compile(src, 'positioning_after', 'exec'), mod.__dict__)
    return mod


def served_record(mod, ticker):
    holdings = mod.calculate_aggregated_holdings(
        {'ST': [{'ticker': ticker, 'weight': 1.0}]},
        {'ST': 1000000.0},
        {ticker: dict(CHARS)})
    return holdings[0]


def portfolio_buckets(mod, ticker):
    asset_alloc, _ = mod.calculate_allocations(
        [{'ticker': ticker, 'weight': 1.0}])
    return dict((k, v) for k, v in asset_alloc.items() if v)


def main():
    mod = load_new_module()
    print('=' * 78)
    print('S1-AC6 READINGS -- served grain vs generator grain. NO VERDICT.')
    print('bytes  : worktree %s' % REL_PATH)
    print('sentinel value: %r' % mod.UNCLASSIFIED_ASSET_CLASS)
    print('=' * 78)
    print('')

    print('READING 1 -- the SERVED asset_class string, per population')
    print('  (the field a portal consumer reads; display map has FOUR keys)')
    for ticker, cls, why in POPULATIONS:
        rec = served_record(mod, ticker)
        print('    %-5s registry=%-13s -> served asset_class=%-14r  %s'
              % (ticker, repr(cls), rec.get('asset_class'), why))
    print('')

    print('READING 2 -- the DISCRIMINATOR this cell adds, same populations')
    for ticker, cls, _why in POPULATIONS:
        rec = served_record(mod, ticker)
        print('    %-5s served asset_class=%-14r  asset_class_recognized=%r'
              % (ticker, rec.get('asset_class'), rec.get('asset_class_recognized')))
    print('')

    print('READING 3 -- collisions on the SERVED STRING ALONE')
    by_display = {}
    for ticker, _cls, _why in POPULATIONS:
        rec = served_record(mod, ticker)
        by_display.setdefault(rec.get('asset_class'), []).append(ticker)
    for display, tickers in sorted(by_display.items(), key=lambda kv: str(kv[0])):
        note = 'unique' if len(tickers) == 1 else 'COLLISION'
        print('    served %-14r <- %-18s (%s)'
              % (display, ','.join(tickers), note))
    print('')

    print('READING 4 -- the GENERATOR grain (raw value, never served)')
    for ticker, _cls, _why in POPULATIONS:
        print('    %-5s classify_etf=%-16r portfolio buckets=%s'
              % (ticker, mod.classify_etf(ticker),
                 json.dumps(portfolio_buckets(mod, ticker), sort_keys=True)))
    print('')

    print('READING 5 -- full served record for the two populations that share'
          ' a display string')
    for ticker in ('GLD', 'ZZZZ'):
        print('    %-5s %s' % (ticker, json.dumps(served_record(mod, ticker),
                                                  sort_keys=True, default=str)))
    print('')
    print('=' * 78)
    print('END OF READINGS. The grade is 3.0.0_SA_CVO~Z\'s at L9.')
    print('=' * 78)
    return 0


if __name__ == '__main__':
    sys.exit(main())
