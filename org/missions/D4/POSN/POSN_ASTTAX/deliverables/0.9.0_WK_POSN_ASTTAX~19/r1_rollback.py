"""R1_ROLLBACK -- POSN_ASTTAX.TO-V8-1 (cell AT5-s-8), the restore that exists BEFORE the act.

WHAT THIS IS. The retag of TO-V8-1 moves thirteen rows of the served DynamoDB table
etf-classifications at TWO levels (asset_class and sub_asset_class) plus VNQ's
management_style. This script puts those thirteen rows back exactly as V8-AC2
measured them, by update-item, one call per row. It is written and committed BEFORE
the first write (criterion V8-AC3) so Branch B is an act a seat can take on demand
and never a thing to be improvised after a refusal.

THE NOW VALUES ARE READ FROM THE MEASUREMENT, NOT TYPED. The restore targets are
loaded from r1_before.json -- the V8-AC2 scan of the whole table, Count == ScannedCount
== 285 -- and are then CROSS-CHECKED field by field against the literal table printed
in THE CELL of the task order. Two independent statements of the same thirteen rows
must agree or this script REFUSES before issuing anything: a rollback whose target is
a guess is worse than no rollback.

THE SIGN-OFF. Both never-widen halves carry this table and co-sign the retag and its
restore:
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_COO_HALF.md
  org/missions/D4/POSN/POSN_ASTTAX/ledger/NEVER_WIDEN_ROUND5_CTO_HALF.md

CONDITIONED, LIKE THE FORWARD WRITE. Each restore is conditioned on the row still
holding the TARGET (retagged) value. Three outcomes, all printed:
  RESTORED  -- the row held the retagged value and now holds the NOW value again;
  SKIP      -- the row already holds the NOW value (never written, or already rolled
               back); nothing is issued;
  REFUSED   -- the row holds a THIRD value, i.e. somebody else moved it. Nothing is
               overwritten and the script exits non-zero. A rollback that clobbers a
               stranger's write is a second incident, not a remedy.

Usage:
  python .../r1_rollback.py --dry-run             # prints the calls, writes NOTHING
  python .../r1_rollback.py                       # issues them (all thirteen)
  python .../r1_rollback.py --tickers GLD,IAU     # only the rows named (partial retag)
Exit codes: 0 = every named row at its NOW value; 1 = a refusal or a failure.
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

# THE CELL's literal table, transcribed: ticker -> (NOW asset_class, NOW sub_asset_class,
# NOW management_style, TARGET asset_class, TARGET sub_asset_class).
# The TARGET asset_class spelling is the GENERATOR's stored vocabulary
# (yang-generate-positioning/lambda_function.py ASSET_CLASS_ORDER / ASSET_CLASS_LABELS,
# :296-303): lowercase 'commodities' / 'structured' / 'alternatives' -- what the
# consumers read, never the display label. sub_asset_class keeps the store's Title Case.
CELL = {
    'DBC':  ('hedge',        'Commodities',  'passive', 'commodities',  'Commodities'),
    'GLD':  ('hedge',        'Gold',         'passive', 'commodities',  'Metals'),
    'GSG':  ('hedge',        'Commodities',  'passive', 'commodities',  'Commodities'),
    'IAU':  ('hedge',        'Gold',         'passive', 'commodities',  'Metals'),
    'SLV':  ('hedge',        'Silver',       'passive', 'commodities',  'Metals'),
    'USO':  ('hedge',        'Oil',          'passive', 'commodities',  'Oil'),
    'PDBC': ('equity',       'Commodities',  'active',  'commodities',  'Commodities'),
    'VXX':  ('equity',       'Volatility',   'passive', 'structured',   'Hedge'),
    'VIXY': ('hedge',        'Volatility',   'passive', 'structured',   'Hedge'),
    'UVXY': ('equity',       'Volatility',   'passive', 'structured',   'Hedge'),
    'QBER': ('fixed_income', 'Volatility',   'active',  'structured',   'Hedge'),
    'JEPI': ('equity',       'US Large Cap', 'active',  'structured',   'Options Income'),
    'VNQ':  ('equity',       'US Large Cap', 'unknown', 'alternatives', 'Real Estate'),
}
ORDER = ['DBC', 'GLD', 'GSG', 'IAU', 'SLV', 'USO', 'PDBC',
         'VXX', 'VIXY', 'UVXY', 'QBER', 'JEPI', 'VNQ']
# VNQ's management_style is the only style this order moves (V8-AC4, unknown -> passive).
STYLE_ROLLBACK = {'VNQ': 'unknown'}


def load_before():
    """The NOW values as MEASURED by V8-AC2, keyed by ticker."""
    with open(BEFORE, encoding='utf-8') as fh:
        doc = json.load(fh)
    if doc.get('Count') != doc.get('ScannedCount'):
        print('BLOCKED: r1_before.json Count %s != ScannedCount %s -- a partial scan is '
              'not a restore target' % (doc.get('Count'), doc.get('ScannedCount')))
        sys.exit(1)
    out = {}
    for item in doc['Items']:
        t = item.get('ticker', {}).get('S')
        out[t] = (item.get('asset_class', {}).get('S'),
                  item.get('sub_asset_class', {}).get('S'),
                  item.get('management_style', {}).get('S'))
    print('r1_before.json: %d rows, Count == ScannedCount == %s (the V8-AC2 enumeration)'
          % (len(out), doc.get('Count')))
    return out


def cross_check(before):
    """Two independent statements of the same thirteen rows, field by field."""
    bad = 0
    for t in ORDER:
        want = CELL[t][:3]
        got = before.get(t)
        if got != want:
            print('BLOCKED: %s -- THE CELL says %s, r1_before.json measured %s'
                  % (t, want, got))
            bad += 1
    print('cross-check THE CELL vs r1_before.json: %d of %d rows agree on all 3 fields'
          % (len(ORDER) - bad, len(ORDER)))
    if bad:
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true',
                    help='print the update-item calls and write nothing')
    ap.add_argument('--tickers', default='',
                    help='comma-separated subset (default: all thirteen)')
    args = ap.parse_args()

    print('R1 ROLLBACK -- table %s, region %s' % (TABLE, REGION))
    print('MODE: %s' % ('DRY RUN (writes nothing)' if args.dry_run
                        else 'LIVE (issues update-item)'))
    before = load_before()
    cross_check(before)

    names = [t.strip().upper() for t in args.tickers.split(',') if t.strip()] or list(ORDER)
    unknown = [t for t in names if t not in CELL]
    if unknown:
        print('BLOCKED: not members of the thirteen: %s' % unknown)
        sys.exit(1)
    print('rows in scope: %d of 13 -- %s' % (len(names), ','.join(names)))
    print('')

    ddb = boto3.client('dynamodb', region_name=REGION)
    restored = skipped = refused = failed = 0

    for t in names:
        now_ac, now_sac, now_ms, tgt_ac, tgt_sac = CELL[t]
        levels = 'asset_class + sub_asset_class'
        extra = ''
        style = STYLE_ROLLBACK.get(t)
        upd = 'SET asset_class = :a, sub_asset_class = :s'
        vals = {':a': {'S': now_ac}, ':s': {'S': now_sac},
                ':oa': {'S': tgt_ac}, ':os': {'S': tgt_sac}}
        cond = 'asset_class = :oa AND sub_asset_class = :os'
        if style is not None:
            upd = upd + ', management_style = :m'
            vals[':m'] = {'S': style}
            levels = levels + ' + management_style'
            extra = '      management_style -> %s (the V8-AC4 write, undone)' % style

        print('%-5s LEVELS %s' % (t, levels))
        print('      asset_class      %-14s -> %-14s (condition: currently %s)'
              % (tgt_ac, now_ac, tgt_ac))
        print('      sub_asset_class  %-14s -> %-14s (condition: currently %s)'
              % (tgt_sac, now_sac, tgt_sac))
        if extra:
            print(extra)
        print('      update-item --table-name %s --key ticker=%s '
              '--update-expression "%s" --condition-expression "%s"'
              % (TABLE, t, upd, cond))

        if args.dry_run:
            print('      DRY RUN: nothing issued')
            print('')
            continue

        try:
            r = ddb.update_item(TableName=TABLE, Key={'ticker': {'S': t}},
                                UpdateExpression=upd,
                                ConditionExpression=cond,
                                ExpressionAttributeValues=vals,
                                ReturnValues='ALL_NEW')
            a = r['Attributes']
            print('      RESTORED: asset_class=%s sub_asset_class=%s management_style=%s'
                  % (a.get('asset_class', {}).get('S'),
                     a.get('sub_asset_class', {}).get('S'),
                     a.get('management_style', {}).get('S')))
            restored += 1
        except ClientError as exc:
            code = exc.response.get('Error', {}).get('Code')
            if code == 'ConditionalCheckFailedException':
                cur = ddb.get_item(TableName=TABLE, Key={'ticker': {'S': t}},
                                   ConsistentRead=True).get('Item', {})
                cac = cur.get('asset_class', {}).get('S')
                csac = cur.get('sub_asset_class', {}).get('S')
                cms = cur.get('management_style', {}).get('S')
                if (cac, csac) == (now_ac, now_sac) and (style is None or cms == style):
                    print('      SKIP: already at the NOW value (%s / %s / %s) -- '
                          'never written, or already rolled back' % (cac, csac, cms))
                    skipped += 1
                else:
                    print('      REFUSED: row holds a THIRD value (%s / %s / %s) -- '
                          'NOT overwritten' % (cac, csac, cms))
                    refused += 1
            else:
                print('      FAILED: %s -- %s' % (code, exc))
                failed += 1
        print('')

    print('ROLLBACK SUMMARY: %d restored / %d already-at-NOW (skipped) / %d refused / '
          '%d failed, of %d in scope' % (restored, skipped, refused, failed, len(names)))
    if args.dry_run:
        print('DRY RUN COMPLETE: %d update-item calls WOULD be issued; 0 writes made.'
              % len(names))
        return 0
    return 1 if (refused or failed) else 0


if __name__ == '__main__':
    sys.exit(main())
