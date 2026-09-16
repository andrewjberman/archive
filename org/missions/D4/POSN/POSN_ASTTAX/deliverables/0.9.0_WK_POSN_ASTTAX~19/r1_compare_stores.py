"""R1_COMPARE_STORES -- POSN_ASTTAX.TO-V8-1 V8-AC6: each ticker against ITS TARGET per
level, and the negative control that nothing else moved.

THE BAR IS A STORE ENUMERATION, NOT A MEMBERSHIP TEST. 'is the row one of the five'
passes on WRONG rows (bd-securities already carries ratified 'alternatives' on ten of
the thirteen), so it is refused as a bar. Here the denominator is EVERY row of the
table and each of the thirteen is compared to ITS OWN target, per level, giving
13 x 2 = 26 independent PASS/FAIL cells.

THE NEGATIVE CONTROL IS THE OTHER 272 ROWS. Every row NOT in the thirteen is compared
field by field against r1_before.json -- the pre-write scan. A retag that leaked would
show here and nowhere else, because the per-member arm above cannot see a defect in
what the members share (a scoped check cannot see past its own scope).

Usage: python .../r1_compare_stores.py
Exit: 0 = 26 of 26 PASS, hedge 0, 272 of 272 unrelated rows identical; 1 otherwise.
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BEFORE = os.path.join(HERE, 'r1_before.json')
AFTER = os.path.join(HERE, 'r1_after.json')

# ticker -> (TARGET asset_class, TARGET sub_asset_class)
TARGET = {
    'DBC':  ('commodities',  'Commodities'),
    'GLD':  ('commodities',  'Metals'),
    'GSG':  ('commodities',  'Commodities'),
    'IAU':  ('commodities',  'Metals'),
    'SLV':  ('commodities',  'Metals'),
    'USO':  ('commodities',  'Oil'),
    'PDBC': ('commodities',  'Commodities'),
    'VXX':  ('structured',   'Hedge'),
    'VIXY': ('structured',   'Hedge'),
    'UVXY': ('structured',   'Hedge'),
    'QBER': ('structured',   'Hedge'),
    'JEPI': ('structured',   'Options Income'),
    'VNQ':  ('alternatives', 'Real Estate'),
}
ORDER = ['DBC', 'GLD', 'GSG', 'IAU', 'SLV', 'USO', 'PDBC',
         'VXX', 'VIXY', 'UVXY', 'QBER', 'JEPI', 'VNQ']
# The ONE management_style this order moves, by V8-AC4 (VNQ, unknown -> passive).
STYLE_MOVED = {'VNQ': ('unknown', 'passive')}


def load(path):
    with open(path, encoding='utf-8') as fh:
        doc = json.load(fh)
    rows = {}
    for item in doc['Items']:
        rows[item.get('ticker', {}).get('S')] = item
    return doc, rows


def flat(item):
    return (item.get('asset_class', {}).get('S'),
            item.get('sub_asset_class', {}).get('S'),
            item.get('management_style', {}).get('S'))


def main():
    bdoc, before = load(BEFORE)
    adoc, after = load(AFTER)

    print('DENOMINATOR -- the store enumeration, both vintages')
    print('  before : Count %s / ScannedCount %s / LastEvaluatedKey %s / items %d'
          % (bdoc.get('Count'), bdoc.get('ScannedCount'),
             'LastEvaluatedKey' in bdoc, len(before)))
    print('  after  : Count %s / ScannedCount %s / LastEvaluatedKey %s / items %d'
          % (adoc.get('Count'), adoc.get('ScannedCount'),
             'LastEvaluatedKey' in adoc, len(after)))
    same_n = (bdoc.get('Count') == adoc.get('Count') == bdoc.get('ScannedCount')
              == adoc.get('ScannedCount'))
    print('  Count == ScannedCount, unchanged across the write: %s' % same_n)
    print('')

    print('EACH TICKER AGAINST ITS TARGET, PER LEVEL (13 rows x 2 levels = 26 cells)')
    print('%-6s %-16s %-16s %-16s %s' % ('ticker', 'level', 'target', 'served', 'verdict'))
    cells = 0
    passed = 0
    for t in ORDER:
        item = after.get(t)
        tgt = TARGET[t]
        if item is None:
            print('%-6s %-16s %-16s %-16s FAIL (row ABSENT)' % (t, 'asset_class', tgt[0], '-'))
            print('%-6s %-16s %-16s %-16s FAIL (row ABSENT)' % (t, 'sub_asset_class', tgt[1], '-'))
            cells += 2
            continue
        got = flat(item)
        for i, level in enumerate(('asset_class', 'sub_asset_class')):
            cells += 1
            ok = got[i] == tgt[i]
            passed += 1 if ok else 0
            print('%-6s %-16s %-16s %-16s %s'
                  % (t, level, tgt[i], got[i], 'PASS' if ok else 'FAIL'))
    print('')
    print('PER-LEVEL RESULT: %d of %d PASS' % (passed, cells))
    print('')

    ac_after = collections.Counter(flat(i)[0] for i in after.values())
    ac_before = collections.Counter(flat(i)[0] for i in before.values())
    print('TOP-LEVEL asset_class CENSUS (denominator %d rows)' % len(after))
    keys = sorted(set(ac_before) | set(ac_after))
    for k in keys:
        print('   %-16s before %3d   after %3d' % (k, ac_before.get(k, 0), ac_after.get(k, 0)))
    hedge_after = ac_after.get('hedge', 0)
    print("   top-level 'hedge' AFTER: %d (was %d) -- the bucket dissolves"
          % (hedge_after, ac_before.get('hedge', 0)))
    print('')

    sub_after = collections.Counter(flat(i)[1] for i in after.values())
    print('NEW sub_asset_class VALUES, counted after the write:')
    for k in ('Metals', 'Hedge', 'Options Income', 'Real Estate', 'Commodities', 'Oil'):
        print('   %-16s %d' % (k, sub_after.get(k, 0)))
    print('')

    print('NEGATIVE CONTROL -- every row NOT in the thirteen, compared to r1_before.json')
    others_b = set(before) - set(TARGET)
    others_a = set(after) - set(TARGET)
    print('   rows outside the thirteen: before %d, after %d' % (len(others_b), len(others_a)))
    drift = []
    for t in sorted(others_b | others_a):
        b = before.get(t)
        a = after.get(t)
        if b is None or a is None:
            drift.append((t, 'PRESENT-BEFORE' if b else 'ABSENT-BEFORE',
                          'PRESENT-AFTER' if a else 'ABSENT-AFTER'))
        elif json.dumps(b, sort_keys=True) != json.dumps(a, sort_keys=True):
            drift.append((t, flat(b), flat(a)))
    print('   rows whose projected attributes are IDENTICAL: %d of %d'
          % (len(others_b | others_a) - len(drift), len(others_b | others_a)))
    for row in drift:
        print('   LEAK: %s' % (row,))
    print('')

    print('CONTROL ON THE CONTROL -- the thirteen MUST differ, or the comparator is blind')
    moved = 0
    for t in ORDER:
        if json.dumps(before.get(t), sort_keys=True) != json.dumps(after.get(t), sort_keys=True):
            moved += 1
    print('   of the thirteen, rows the SAME comparator reports as CHANGED: %d of 13' % moved)
    print('')

    print('management_style: the only row this order moves is VNQ (V8-AC4)')
    ms_moved = []
    for t in sorted(set(before) & set(after)):
        if flat(before[t])[2] != flat(after[t])[2]:
            ms_moved.append((t, flat(before[t])[2], flat(after[t])[2]))
    for t, b, a in ms_moved:
        print('   %s %s -> %s' % (t, b, a))
    print('   rows whose management_style moved: %d (expected 1: VNQ unknown -> passive)'
          % len(ms_moved))

    ok = (passed == cells == 26 and hedge_after == 0 and not drift and same_n
          and moved == 13 and ms_moved == [('VNQ',) + STYLE_MOVED['VNQ']])
    print('')
    print('V8-AC6 RESULT: %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
