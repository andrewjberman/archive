#!/usr/bin/env python3
"""S6-AC7 instrument readings for POSN_ASTTAX.TO-S6-1 (decomp cell AT2-s-6).

S6-AC7 IS A JUDGMENT CRITERION GRADED BY 3.0.0_SA_CVO~Z AT L9. This script
offers NO verdict; it only reads instruments and prints what they say about
whether an unexpected classification value is now both NON-FATAL and VISIBLE
rather than non-fatal by being silently discarded.

Three arms beyond S6-AC5, same two byte-vintages (see ac5_negative_control.py
for how the pre-fix bytes are obtained and what is stubbed):
  ARM 1  the PLACEHOLDER path in isolation -- asset_class canonical, only
         management_style is "unknown" (the 187-of-285 registry population).
  ARM 2  VISIBILITY -- is the unexpected value present, NAMED and COUNTABLE in
         the dict that is serialized whole into the served payload?
  ARM 3  the FIXED-LIST CONSUMERS inside the same file, replayed against a dict
         that now carries an extra key (the delta loop's direct subscript over
         the four canonical asset classes, the management delta over the two
         styles, and the benchmark spread's .get() loop).

Usage:  python org/missions/D4/POSN/POSN_ASTTAX/deliverables/\
0.9.0_WK_POSN_ASTTAX~2/ac7_visibility_instruments.py [pre_fix_source_path]
Run from the repository root.
"""
import json
import sys
import types
from unittest.mock import MagicMock

POST = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
        'yang-generate-positioning/lambda_function.py')
PRE = sys.argv[1] if len(sys.argv) > 1 else '.scratch/prefix_lambda_function.py'

REGISTRY = {
    'AGG': {'asset_class': 'fixed_income', 'management_style': 'passive'},
    'XYZ': {'asset_class': 'equity', 'management_style': 'unknown'},
}
PLACEHOLDER_ONLY = [{'ticker': 'AGG', 'weight': 0.5}, {'ticker': 'XYZ', 'weight': 0.5}]


class StubClassifier(object):
    def get_classification(self, ticker):
        return REGISTRY.get(ticker)


def load(path, tag):
    stub = types.ModuleType('etf_classifications_dynamodb')
    stub.ETFClassifier = StubClassifier
    sys.modules['etf_classifications_dynamodb'] = stub
    sys.modules['boto3'] = MagicMock(name='boto3')
    sys.modules['pandas'] = MagicMock(name='pandas')
    src = open(path, encoding='utf-8').read()
    mod = types.ModuleType('gen_' + tag)
    mod.__dict__['__name__'] = 'gen_' + tag
    exec(compile(src, path, 'exec'), mod.__dict__)
    return mod


print('---------- ARM 1: the placeholder path alone (management_style "unknown") ----------')
for path, tag, label in ((PRE, 'pre', 'PRE-FIX '), (POST, 'post', 'POST-FIX')):
    mod = load(path, tag)
    try:
        assets, mgmt = mod.calculate_allocations(PLACEHOLDER_ONLY)
        print('%s registry_field -> %r | calculate_allocations COMPLETED | mgmt=%s'
              % (label, mod.classify_management_style('XYZ'), json.dumps(mgmt)))
    except Exception as exc:
        print('%s registry_field -> %r | calculate_allocations RAISED %s: %s'
              % (label, mod.classify_management_style('XYZ'), type(exc).__name__, exc))

print('')
print('---------- ARM 2: visibility of the unexpected value (POST-FIX only) ----------')
REGISTRY['DBC'] = {'asset_class': 'Commodities', 'management_style': 'Overlay'}
mod = load(POST, 'post2')
assets, mgmt = mod.calculate_allocations(
    [{'ticker': 'AGG', 'weight': 0.8}, {'ticker': 'DBC', 'weight': 0.2}])
print('asset_allocations keys      = %s' % list(assets.keys()))
print('management_allocations keys = %s' % list(mgmt.keys()))
print('unexpected asset value named+counted:      Commodities=%s' % assets.get('Commodities'))
print('unexpected mgmt  value named+counted:      Overlay=%s' % mgmt.get('Overlay'))
print('asset total=%.1f  mgmt total=%.1f  (nothing discarded into a void)'
      % (sum(assets.values()), sum(mgmt.values())))
print('serialized as the payload does it: %s'
      % json.dumps({'allocation': assets, 'management': mgmt}))

print('')
print('---------- ARM 3: the fixed-list consumers, replayed on a 5-key dict ----------')
prior = {'cash': 0, 'fixed_income': 100.0, 'equity': 0, 'hedge': 0}
try:
    delta = {}
    for asset_class in ['cash', 'fixed_income', 'equity', 'hedge']:
        delta[asset_class] = round(assets[asset_class] - prior[asset_class], 1)
    print('delta loop (direct subscript, 4 canonical keys) OK: %s' % json.dumps(delta))
except Exception as exc:
    print('delta loop RAISED %s: %s' % (type(exc).__name__, exc))
try:
    mgmt_delta = {}
    for style in ['active', 'passive']:
        mgmt_delta[style] = round(mgmt[style] - 0, 1)
    print('management delta loop OK: %s' % json.dumps(mgmt_delta))
except Exception as exc:
    print('management delta loop RAISED %s: %s' % (type(exc).__name__, exc))
spread = {}
for asset_class in ['cash', 'fixed_income', 'equity', 'hedge']:
    spread[asset_class] = round(assets.get(asset_class, 0) - 0, 1)
print('benchmark spread loop (.get over 4 canonical keys) OK: %s' % json.dumps(spread))
print('NOTE: those consumers iterate a LITERAL four/two-key list, so the extra key is')
print('      carried in "allocation" but does NOT appear in "delta" or the spreads.')
