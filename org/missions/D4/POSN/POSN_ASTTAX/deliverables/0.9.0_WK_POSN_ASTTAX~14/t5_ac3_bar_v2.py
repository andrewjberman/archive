"""T5-AC3/AC5 -- clause (b) and (d), THREE numbers per member, on TWO CODE ARMS.

ARM DEPLOYED : bytes running in AWS today (lambda get-function -> Code.Location),
               lambda_function.py md5 cc79aff7506f8c39e17453f386c69551, 94164 bytes.
ARM HEAD     : bytes committed at 3ce0c0e372 (AT3-s-1 terminal @425da33b79),
               lambda_function.py md5 96aedb53a9fcac4151517028c72ded42, 115411 bytes.

Per member, per code arm: BEFORE = the registry value served TODAY; AFTER = the ratified target.
Read-only; stubs only the registry read (the input under test) and load_aum_data (S3, no asset_class).
"""
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import types
import zipfile
from contextlib import redirect_stdout

import pandas as pd

GEN = ('infra/aws/lambda/v2_portal/yang_pipeline/positioning/'
       'yang-generate-positioning/lambda_function.py')
PIN = '3ce0c0e372'
MODEL = 'INT'

MEMBERS = [
    ("DBC", "hedge", "Commodities", 0.025), ("GLD", "hedge", "Commodities", 0.025),
    ("GSG", "hedge", "Commodities", 0.025), ("IAU", "hedge", "Commodities", 0.025),
    ("SLV", "hedge", "Commodities", 0.025), ("USO", "hedge", "Commodities", 0.025),
    ("VIXY", "hedge", "Structured", 0.025), ("VXX", "equity", "Structured", 0.015),
    ("UVXY", "equity", "Structured", 0.025), ("QBER", "fixed_income", "Structured", 0.025),
    ("PDBC", "equity", "Commodities", 0.025),
]


def materialise(which):
    if which == "HEAD":
        src = subprocess.check_output(['git', 'show', '%s:%s' % (PIN, GEN)])
    else:
        src = zipfile.ZipFile('.scratch/yang-generate-positioning.DEPLOYED.zip').read('lambda_function.py')
    h, p = tempfile.mkstemp(suffix='_%s_lambda_function.py' % which)
    os.fdopen(h, 'wb').write(src)
    return p


def make_registry(ticker, asset_class, sub):
    return {
        'IVV': {'ticker': 'IVV', 'name': 'iShares Core S&P 500 ETF', 'asset_class': 'equity',
                'sub_asset_class': 'Large', 'management_style': 'passive', 'sector': 'Broad'},
        'AGG': {'ticker': 'AGG', 'name': 'iShares Core US Aggregate Bond ETF', 'asset_class': 'fixed_income',
                'sub_asset_class': 'Intermediate', 'management_style': 'passive', 'sector': 'Aggregate'},
        'BIL': {'ticker': 'BIL', 'name': 'SPDR Bloomberg 1-3 Month T-Bill ETF', 'asset_class': 'cash',
                'sub_asset_class': 'Short Duration', 'management_style': 'passive', 'sector': 'Government'},
        ticker: {'ticker': ticker, 'name': ticker + ' Fund', 'asset_class': asset_class,
                 'sub_asset_class': sub, 'management_style': 'passive', 'sector': 'Other'},
    }


def load_generator(tag, path, registry):
    class StubClassifier(object):
        def __init__(self, *a, **k):
            pass

        def get_classification(self, ticker):
            return registry.get(ticker)

    stub = types.ModuleType('etf_classifications_dynamodb')
    stub.ETFClassifier = StubClassifier
    sys.modules['etf_classifications_dynamodb'] = stub
    spec = importlib.util.spec_from_file_location('gen_%s' % tag, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules['gen_%s' % tag] = m
    spec.loader.exec_module(m)
    m.etf_classifier = StubClassifier()
    m.load_aum_data = lambda *a, **k: None
    return m


def build_pkl(ticker, weight):
    latest, prior = pd.Timestamp('2026-09-10'), pd.Timestamp('2026-09-09')
    holdings = pd.DataFrame([
        {'date': prior, 'ticker': 'IVV', 'weight': 0.600, 'model': MODEL},
        {'date': prior, 'ticker': 'AGG', 'weight': 0.400, 'model': MODEL},
        {'date': latest, 'ticker': 'IVV', 'weight': 0.600, 'model': MODEL},
        {'date': latest, 'ticker': 'AGG', 'weight': 0.400 - weight, 'model': MODEL},
        {'date': latest, 'ticker': ticker, 'weight': weight, 'model': MODEL},
    ])
    bench = pd.DataFrame([{'ticker': 'AGG', 'weight': 0.40, 'model': MODEL},
                          {'ticker': 'IVV', 'weight': 0.60, 'model': MODEL}])
    chars = pd.DataFrame([
        {'ticker': 'IVV', 'name': 'A', 'fee': 0.0003, 'yield': 1.3, 'duration': None, 'beta': 1.0},
        {'ticker': 'AGG', 'name': 'B', 'fee': 0.0003, 'yield': 4.1, 'duration': 6.1, 'beta': None},
        {'ticker': 'BIL', 'name': 'C', 'fee': 0.0014, 'yield': 4.3, 'duration': 0.1, 'beta': None},
        {'ticker': ticker, 'name': ticker, 'fee': 0.004, 'yield': 0.0, 'duration': None, 'beta': None},
    ])
    return {'holdings': holdings, 'benchmark_holdings': bench, 'etf_characteristics': chars}


def run_arm(path, tag, ticker, raw, target, weight):
    """Returns a dict of readings, or {'RAISED': ...} -- a raise IS the reading."""
    try:
        buf = io.StringIO()
        with redirect_stdout(buf):
            m = load_generator(tag, path, make_registry(ticker, raw, 'Volatility' if target == 'Structured' else 'Gold'))
            payload = m.generate_positioning_data(build_pkl(ticker, weight), '20260910', None, '2026-09-10')
        pf = payload['portfolios'][MODEL]
        row = [h for h in pf['holdings'] if h['ticker'] == ticker][0]
        lg = round(sum(h['weight'] for h in pf['holdings'] if h.get('assetClass') == target), 6)
        key = str(target).strip().lower().replace('-', '_').replace(' ', '_')
        sub = {}
        for h in pf['holdings']:
            sub[h.get('assetClass')] = round(sub.get(h.get('assetClass'), 0.0) + h['weight'], 6)
        return {'label': row.get('assetClass'), 'lg': lg, 'alloc': pf['allocation'].get(key, '<ABSENT>'),
                'alloc_keys': list(pf['allocation']), 'sub': sub,
                'grand': round(sum(h['weight'] for h in pf['holdings']), 6),
                'two': round(sum(v for k, v in sub.items() if k in ('Fixed Income', 'Equity')), 6)}
    except Exception as e:
        return {'RAISED': '%s: %s' % (type(e).__name__, e)}


for which in ("DEPLOYED", "HEAD"):
    path = materialise(which)
    print("\n" + "#" * 118)
    print("# CODE ARM: %s   (%s)" % (which, path))
    print("#" * 118)
    print("%-6s %-13s %-12s | %-26s %-26s | %-24s" % ("MEM", "served_now", "target", "BEFORE (label / LBLGRP)", "AFTER (label / LBLGRP)", "alloc[key] BEFORE / AFTER"))
    print("-" * 118)
    for t, now, target, w in MEMBERS:
        b = run_arm(path, '%s_b_%s' % (which, t), t, now, target, w)
        a = run_arm(path, '%s_a_%s' % (which, t), t, target, target, w)

        def cell(r):
            if 'RAISED' in r:
                return "RAISED " + r['RAISED'][:19]
            return "%r / %.6f" % (r['label'], r['lg'])

        def ac(r):
            return "RAISED" if 'RAISED' in r else str(r['alloc'])
        print("%-6s %-13s %-12s | %-26s %-26s | %s / %s" % (t, now, target, cell(b), cell(a), ac(b), ac(a)))

    print("\n  CLAUSE (d) ARITHMETIC on VXX (the only live-held member), %s:" % which)
    for tag, raw in (("BEFORE", "equity"), ("AFTER", "Structured")):
        r = run_arm(path, '%s_d_%s' % (which, tag), 'VXX', raw, 'Structured', 0.015)
        if 'RAISED' in r:
            print("    %-7s NO PAYLOAD IS PRODUCED AT ALL -- %s" % (tag, r['RAISED'][:110]))
            continue
        print("    %-7s subtotals=%s" % (tag, r['sub']))
        print("    %-7s grand_total=%.6f | sum of the two groups the page RENDERS=%.6f | DIFFERENCE=%.6f"
              % (tag, r['grand'], r['two'], round(r['grand'] - r['two'], 6)))
        print("    %-7s allocation dict keys=%s" % (tag, r['alloc_keys']))
