#!/usr/bin/env python3
"""Negative control for POSN_ASTTAX.TO-S1-1 / cell AT2-s-1 (criterion S1-AC3).

THE QUESTION: given only what the positioning generator produces, can a consumer
tell that a security was NEVER CLASSIFIED apart from one a human deliberately
tagged with a real asset class?

THE METHOD: load the SAME module twice -- BEFORE from `git show HEAD:<path>`
(the bytes as committed, which already carry AT2-s-6's hardening) and AFTER from
the worktree file -- against ONE stubbed registry, and run four arms of the real
generator functions on both. No AWS, no network: the DynamoDB client is replaced
before the module body executes.

THE COMPARATORS: an ABSENT ticker (`ZZZZ`, not in the registry) is compared with
two GENUINE holdings -- a deliberately-tagged equity and a deliberately-tagged
fixed income -- whose `sub_asset_class` is also unset. That is a real population
(cell AT2-s-4 owns those rows), and choosing it isolates the ASSET CLASS field,
which is the only field this cell changes. The projection compared is therefore
the CLASS-BEARING fields only; identity fields (ticker, name) are excluded by
construction and the full served dict is printed beside it so nothing is hidden.

THE BAR: on the BEFORE bytes the absent ticker must be INDISTINGUISHABLE from at
least one genuine holding in every arm (that is the defect); on the AFTER bytes
it must be DISTINGUISHABLE from both, with the distinguishing field NAMED. Exit
0 only if both halves hold -- so this control FAILS on the old bytes, which is
what makes it a control rather than a restatement of the status quo.
`--falsify` loads the OLD bytes into BOTH arms and must exit 1.
"""

import json
import subprocess
import sys
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[7]
REL_PATH = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
            'yang-generate-positioning/lambda_function.py')

ABSENT_TICKER = 'ZZZZ'
GENUINE_EQUITY = 'SPY'
GENUINE_FI = 'AGG'

# The stub registry. ZZZZ is deliberately NOT a key: get_classification returns
# None for it, exactly as the live client does for a ticker the table lacks.
# Both genuine rows carry an unset sub_asset_class so that field cannot do the
# discriminating work the asset_class field is supposed to do.
REGISTRY = {
    GENUINE_EQUITY: {
        'ticker': GENUINE_EQUITY,
        'asset_class': 'equity',
        'sub_asset_class': '',
        'management_style': 'passive',
        'name': 'Genuine Equity Holding',
    },
    GENUINE_FI: {
        'ticker': GENUINE_FI,
        'asset_class': 'fixed_income',
        'sub_asset_class': '',
        'management_style': 'passive',
        'name': 'Genuine Fixed Income Holding',
    },
}

# Identical characteristics for all three tickers, so nothing except the asset
# class can make their served records differ.
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

TICKERS = [ABSENT_TICKER, GENUINE_EQUITY, GENUINE_FI]

# Fields excluded from the compared projection because they identify the
# security rather than classify it.
IDENTITY_FIELDS = ('ticker', 'name')


class StubClassifier(object):
    """Stands in for ETFClassifier. Never touches DynamoDB."""

    def get_classification(self, ticker):
        return REGISTRY.get(ticker)

    def get_asset_class(self, ticker):
        return (REGISTRY.get(ticker) or {}).get('asset_class')


def read_old_source():
    """The committed bytes, with a positive control on what came back."""
    result = subprocess.run(
        ['git', 'show', 'HEAD:' + REL_PATH],
        cwd=str(REPO_ROOT), capture_output=True)
    if result.returncode != 0:
        raise RuntimeError('ERROR: git show failed rc=%d: %s'
                           % (result.returncode, result.stderr[:400]))
    src = result.stdout.decode('utf-8')
    # POSITIVE CONTROL: these two literals are the OLD defaults. If the
    # retrieval silently returned the wrong object, they are absent and this
    # raises instead of quietly comparing the file with itself.
    for literal in ("registry_field(ticker, 'asset_class', 'fixed_income')",
                    "registry_field(ticker, 'asset_class', 'equity')"):
        if literal not in src:
            raise RuntimeError('ERROR: retrieved BEFORE bytes lack %r -- not the'
                               ' pre-fix source' % literal)
    return src


def read_new_source():
    """The worktree bytes, with a positive control that the fix is in them."""
    src = (REPO_ROOT / REL_PATH).read_text(encoding='utf-8')
    if 'UNCLASSIFIED_ASSET_CLASS' not in src:
        raise RuntimeError('ERROR: worktree bytes carry no sentinel -- nothing'
                           ' to test')
    return src


def load_module(src, label):
    """Execute the generator source with the registry stubbed out."""
    stub_mod = types.ModuleType('etf_classifications_dynamodb')
    stub_mod.ETFClassifier = StubClassifier
    sys.modules['etf_classifications_dynamodb'] = stub_mod
    mod = types.ModuleType(label)
    mod.__file__ = label
    exec(compile(src, label, 'exec'), mod.__dict__)
    return mod


def arm_raw_class(mod, ticker):
    """ARM 1 -- the generator's own asset-class string."""
    return {'classify_etf': mod.classify_etf(ticker)}


def arm_portfolio_allocation(mod, ticker):
    """ARM 2 -- the portfolio allocation buckets (calculate_allocations)."""
    asset_alloc, _ = mod.calculate_allocations(
        [{'ticker': ticker, 'weight': 1.0}])
    return {key: value for key, value in asset_alloc.items() if value}


def arm_served_holding(mod, ticker):
    """ARM 3 -- the SERVED holding dict (calculate_aggregated_holdings)."""
    holdings = mod.calculate_aggregated_holdings(
        {'ST': [{'ticker': ticker, 'weight': 1.0}]},
        {'ST': 1000000.0},
        {ticker: dict(CHARS)})
    return holdings[0]


def arm_benchmark_allocation(mod, ticker):
    """ARM 4 -- the benchmark allocations (the second old `equity` default)."""
    import pandas as pd
    frame = pd.DataFrame([{'ticker': ticker, 'weight': 1.0, 'model': 'ST'}])
    return mod.calculate_benchmark_allocations_from_holdings(frame).get('ST')


ARMS = [
    ('ARM 1  generator raw class      classify_etf()', arm_raw_class),
    ('ARM 2  portfolio allocation     calculate_allocations()',
     arm_portfolio_allocation),
    ('ARM 3  SERVED holding           calculate_aggregated_holdings()',
     arm_served_holding),
    ('ARM 4  benchmark allocation     calculate_benchmark_allocations_from_holdings()',
     arm_benchmark_allocation),
]


def project(record):
    """Drop identity fields; keep everything that classifies."""
    if not isinstance(record, dict):
        return record
    return {key: value for key, value in record.items()
            if key not in IDENTITY_FIELDS}


def name_difference(absent_rec, genuine_rec):
    """Name the field(s) on which the two records differ."""
    left = project(absent_rec)
    right = project(genuine_rec)
    if not isinstance(left, dict) or not isinstance(right, dict):
        return ['<whole record>'] if left != right else []
    fields = []
    for key in sorted(set(list(left.keys()) + list(right.keys()))):
        if left.get(key, '<absent>') != right.get(key, '<absent>'):
            fields.append('%s (%r vs %r)'
                          % (key, left.get(key, '<absent>'),
                             right.get(key, '<absent>')))
    return fields


def run_arm(mod, arm_fn):
    return dict((ticker, arm_fn(mod, ticker)) for ticker in TICKERS)


def report_arm(label, results):
    """Print one arm's three records and say whether the absent one is hidden."""
    print('  %s' % label)
    for ticker in TICKERS:
        tag = 'ABSENT ' if ticker == ABSENT_TICKER else 'genuine'
        print('    %s %-5s : %s'
              % (tag, ticker, json.dumps(results[ticker], sort_keys=True,
                                         default=str)))
    absorbed_into = []
    for genuine in (GENUINE_EQUITY, GENUINE_FI):
        diff = name_difference(results[ABSENT_TICKER], results[genuine])
        if diff:
            print('    DISTINGUISHABLE from %s by: %s'
                  % (genuine, '; '.join(diff)))
        else:
            print('    INDISTINGUISHABLE from %s -- every class-bearing field is'
                  ' identical' % genuine)
            absorbed_into.append(genuine)
    return absorbed_into


def evaluate(mod, heading):
    print(heading)
    absorbed_any = False
    distinguishable_all = True
    for label, arm_fn in ARMS:
        results = run_arm(mod, arm_fn)
        absorbed = report_arm(label, results)
        if absorbed:
            absorbed_any = True
            distinguishable_all = False
        print('')
    return absorbed_any, distinguishable_all


def main(argv):
    falsify = '--falsify' in argv
    old_src = read_old_source()
    new_src = new_src_for(falsify, old_src)

    print('=' * 78)
    print('NEGATIVE CONTROL  POSN_ASTTAX.TO-S1-1 / cell AT2-s-1 / S1-AC3')
    print('file   : %s' % REL_PATH)
    print('BEFORE : git show HEAD:<file>  (%d lines)' % len(old_src.splitlines()))
    print('AFTER  : worktree <file>       (%d lines)%s'
          % (len(new_src.splitlines()),
             '   [--falsify: OLD bytes in BOTH arms]' if falsify else ''))
    print('absent ticker %r is not a registry key; %r and %r are genuine rows'
          % (ABSENT_TICKER, GENUINE_EQUITY, GENUINE_FI))
    print('compared projection excludes identity fields %s' % (IDENTITY_FIELDS,))
    print('=' * 78)
    print('')

    old_mod = load_module(old_src, 'positioning_before')
    before_absorbed, _ = evaluate(
        old_mod, '---------------- BEFORE (HEAD bytes) ----------------')

    new_mod = load_module(new_src, 'positioning_after')
    _, after_distinguishable = evaluate(
        new_mod, '---------------- AFTER (worktree bytes) ----------------')

    print('=' * 78)
    print('BEFORE: absent ticker indistinguishable from a genuine holding'
          ' somewhere : %s' % ('YES -- THE DEFECT' if before_absorbed else 'NO'))
    print('AFTER : absent ticker distinguishable from BOTH genuine holdings in'
          ' every arm : %s' % ('YES' if after_distinguishable else 'NO'))
    ok = before_absorbed and after_distinguishable
    print('CONTROL: %s' % ('OK: the fix changed the world in the asserted'
                           ' direction' if ok else
                           'ERROR: the control does not hold'))
    print('=' * 78)
    return 0 if ok else 1


def new_src_for(falsify, old_src):
    """The AFTER arm's bytes -- or the OLD bytes again when falsifying."""
    if falsify:
        return old_src
    return read_new_source()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
