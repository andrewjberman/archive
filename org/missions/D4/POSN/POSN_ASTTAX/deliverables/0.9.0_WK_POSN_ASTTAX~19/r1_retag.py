"""R1_RETAG -- POSN_ASTTAX.TO-V8-1 (cell AT5-s-8), the thirteen writes, LEVEL-EXPLICIT
and CONDITIONED ON THE PRIOR VALUE.

WHAT THIS ACT IS. Store 1 is the served DynamoDB table etf-classifications (C-ONE-SOURCE).
This script moves exactly thirteen rows at TWO levels each -- asset_class AND
sub_asset_class -- in one update-item per row, and nothing else. VNQ's management_style
is NOT written here: criterion V8-AC4 sets it FIRST, on its own conditioned call, so
C-RETAG-SAFETY's guard is never armed mid-retag.

EVERY WRITE NAMES ITS LEVEL. UpdateExpression is literally
    SET asset_class = :a, sub_asset_class = :s
so neither level can be moved by accident and neither can be left behind.

CONDITIONED ON THE NOW VALUE -- THE CONTROL IS THE CONDITION, NOT A PRIOR READ.
    ConditionExpression: asset_class = :oa AND sub_asset_class = :os
A row that somebody moved between the V8-AC2 scan and this call is REFUSED by DynamoDB,
not overwritten; the script prints the row's actual value and exits non-zero. That is
Branch B: STOP, run r1_rollback.py for the rows already written, file the row. A
conditional write is also the reason a second run of this script writes NOTHING -- every
row is then at its TARGET, so all thirteen conditions fail. That re-run is a genuine
NEGATIVE CONTROL and is offered as one (--recheck prints it without writing).

THE TARGET VOCABULARY IS THE GENERATOR'S, NOT THE DISPLAY LABEL. The stored top-level
values come from yang-generate-positioning/lambda_function.py (ASSET_CLASS_ORDER and
ASSET_CLASS_LABELS, :296-303): lowercase 'commodities', 'structured', 'alternatives'.
sub_asset_class keeps the store's Title Case ('Commodities', 'Metals', 'Oil', 'Hedge',
'Options Income', 'Real Estate'). 'Hedge' is a sub_asset_class under 'structured'; the
TOP-level 'hedge' dissolves -- 7 rows before, 0 rows after, and V8-AC6 measures it.

THE SIGN-OFF. Both never-widen halves carry this same thirteen-row table and co-sign
this act:
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_COO_HALF.md
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_CTO_HALF.md
THE RESTORE EXISTS ALREADY: r1_rollback.py, written and committed before this file ran
(V8-AC3).

Usage:
  python .../r1_retag.py             # the thirteen conditioned writes
  python .../r1_retag.py --recheck   # read-only: where the thirteen rows stand now
Exit codes: 0 = 13 written / 0 refused; 1 = any refusal or failure (Branch B).
"""
import argparse
import json
import os
import sys

import boto3
from botocore.exceptions import ClientError

REGION = 'us-east-1'
TABLE = 'etf-classifications'
HERE = os.path.dirname(os.path.abspath(__file__))
BEFORE = os.path.join(HERE, 'r1_before.json')

# ticker -> (NOW asset_class, NOW sub_asset_class, TARGET asset_class, TARGET sub_asset_class)
RETAG = [
    ('DBC',  'hedge',        'Commodities',  'commodities',  'Commodities'),
    ('GLD',  'hedge',        'Gold',         'commodities',  'Metals'),
    ('GSG',  'hedge',        'Commodities',  'commodities',  'Commodities'),
    ('IAU',  'hedge',        'Gold',         'commodities',  'Metals'),
    ('SLV',  'hedge',        'Silver',       'commodities',  'Metals'),
    ('USO',  'hedge',        'Oil',          'commodities',  'Oil'),
    ('PDBC', 'equity',       'Commodities',  'commodities',  'Commodities'),
    ('VXX',  'equity',       'Volatility',   'structured',   'Hedge'),
    ('VIXY', 'hedge',        'Volatility',   'structured',   'Hedge'),
    ('UVXY', 'equity',       'Volatility',   'structured',   'Hedge'),
    ('QBER', 'fixed_income', 'Volatility',   'structured',   'Hedge'),
    ('JEPI', 'equity',       'US Large Cap', 'structured',   'Options Income'),
    ('VNQ',  'equity',       'US Large Cap', 'alternatives', 'Real Estate'),
]


def load_before():
    with open(BEFORE, encoding='utf-8') as fh:
        doc = json.load(fh)
    out = {}
    for item in doc['Items']:
        out[item.get('ticker', {}).get('S')] = (
            item.get('asset_class', {}).get('S'),
            item.get('sub_asset_class', {}).get('S'))
    return doc, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recheck', action='store_true',
                    help='read-only: print where the thirteen rows stand, write nothing')
    args = ap.parse_args()

    print('R1 RETAG -- table %s, region %s, %d rows, TWO levels each'
          % (TABLE, REGION, len(RETAG)))
    doc, before = load_before()
    print('premise: r1_before.json Count %s == ScannedCount %s (V8-AC2)'
          % (doc.get('Count'), doc.get('ScannedCount')))
    bad = [t for (t, na, ns, _, _) in RETAG if before.get(t) != (na, ns)]
    if bad:
        print('BLOCKED: the NOW values in this script disagree with the V8-AC2 scan for '
              '%s -- refusing before the first write' % bad)
        return 1
    print('premise: 13 of 13 NOW pairs EQUAL the V8-AC2 scan -- proceeding')
    print('')

    ddb = boto3.client('dynamodb', region_name=REGION)

    if args.recheck:
        for (t, na, ns, ta, ts) in RETAG:
            cur = ddb.get_item(TableName=TABLE, Key={'ticker': {'S': t}},
                               ConsistentRead=True).get('Item', {})
            cac = cur.get('asset_class', {}).get('S')
            csac = cur.get('sub_asset_class', {}).get('S')
            state = ('AT TARGET' if (cac, csac) == (ta, ts)
                     else 'AT NOW' if (cac, csac) == (na, ns) else 'THIRD VALUE')
            print('%-5s %-12s asset_class=%-14s sub_asset_class=%s'
                  % (t, state, cac, csac))
        return 0

    written = refused = failed = 0
    for (t, na, ns, ta, ts) in RETAG:
        upd = 'SET asset_class = :a, sub_asset_class = :s'
        cond = 'asset_class = :oa AND sub_asset_class = :os'
        vals = {':a': {'S': ta}, ':s': {'S': ts},
                ':oa': {'S': na}, ':os': {'S': ns}}
        print('%-5s update-item --update-expression "%s" --condition-expression "%s"'
              % (t, upd, cond))
        print('      LEVEL asset_class      %-14s -> %-14s' % (na, ta))
        print('      LEVEL sub_asset_class  %-14s -> %-14s' % (ns, ts))
        try:
            r = ddb.update_item(TableName=TABLE, Key={'ticker': {'S': t}},
                                UpdateExpression=upd,
                                ConditionExpression=cond,
                                ExpressionAttributeValues=vals,
                                ReturnValues='ALL_NEW')
            a = r['Attributes']
            gac = a.get('asset_class', {}).get('S')
            gsac = a.get('sub_asset_class', {}).get('S')
            gms = a.get('management_style', {}).get('S')
            ok = (gac, gsac) == (ta, ts)
            print('      WRITTEN (ALL_NEW): asset_class=%s sub_asset_class=%s '
                  'management_style=%s  %s'
                  % (gac, gsac, gms, 'MATCHES TARGET' if ok else 'DOES NOT MATCH TARGET'))
            if ok:
                written += 1
            else:
                failed += 1
        except ClientError as exc:
            code = exc.response.get('Error', {}).get('Code')
            if code == 'ConditionalCheckFailedException':
                cur = ddb.get_item(TableName=TABLE, Key={'ticker': {'S': t}},
                                   ConsistentRead=True).get('Item', {})
                print('      REFUSED (ConditionalCheckFailed): row holds %s / %s -- '
                      'NOT overwritten. BRANCH B.'
                      % (cur.get('asset_class', {}).get('S'),
                         cur.get('sub_asset_class', {}).get('S')))
                refused += 1
            else:
                print('      FAILED: %s -- %s' % (code, exc))
                failed += 1
        print('')

    print('RETAG SUMMARY: %d written / %d refused / %d failed, of %d'
          % (written, refused, failed, len(RETAG)))
    if refused or failed:
        print('BRANCH B: run r1_rollback.py for the rows already written, file the row.')
        return 1
    print('13 written / 0 refused.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
