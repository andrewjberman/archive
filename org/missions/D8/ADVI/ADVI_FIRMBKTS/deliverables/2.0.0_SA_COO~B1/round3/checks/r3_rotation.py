"""r3_rotation.py -- FB-f-9 phase A2: the two canonical-mode reads that follow a platinum write (rows D1-W16-S7, S8).

Arms (each PASS or FAIL, with its denominator):
  R1  D_04.client_portal_summary.py: the prior-week rotation's copy_object CopySource is the DESTINATION of
      'platinum/firm/leaderboard.json' (Bucket and Key both names bound from platinum_destination(...) of that literal)
  R2  D_00f.advisor_nna_canonical.py: the write-success sentinel's head_object reads the DESTINATION of OUTPUT_KEY
      (Bucket and Key both names bound from platinum_destination(OUTPUT_KEY))
  R3  platinum_dest.destination() in 'legacy' mode returns (S3_BUCKET, key) for both keys: the dormant build names
      today's bucket and key

Also prints, informationally, every head_object/copy_object/get_object call in the 14 census writers whose Key text
carries 'platinum' and whose Bucket is S3_BUCKET or BUCKET (the read-after-write candidates), with the count.
Exit 0 only when all three arms pass.   usage: python r3_rotation.py [--root <checkout>]
"""
import argparse
import ast
import os
import sys

GOLD = 'data/black_diamond/scripts/gold'
D04 = GOLD + '/D_04.client_portal_summary.py'
D00F = GOLD + '/D_00f.advisor_nna_canonical.py'
LEADER = "'platinum/firm/leaderboard.json'"


def parse(root, rel):
    with open(os.path.join(root, rel), encoding='utf-8') as fh:
        src = fh.read()
    return src, ast.parse(src)


def bindings(tree):
    """(bucket_name, key_name, arg_source) for every `a, b = platinum_destination(<one arg>)`."""
    out = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Assign) and isinstance(n.value, ast.Call)):
            continue
        f = n.value.func
        if not (isinstance(f, ast.Name) and f.id == 'platinum_destination' and len(n.value.args) == 1):
            continue
        if len(n.targets) != 1 or not isinstance(n.targets[0], ast.Tuple):
            continue
        elts = n.targets[0].elts
        if len(elts) == 2 and all(isinstance(e, ast.Name) for e in elts):
            out.append((elts[0].id, elts[1].id, ast.unparse(n.value.args[0])))
    return out


def calls(tree, attr):
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == attr]


def kw(call, name):
    for k in call.keywords:
        if k.arg == name:
            return k.value
    return None


def name_of(node):
    return node.id if isinstance(node, ast.Name) else None


def arm_r1(root):
    _, tree = parse(root, D04)
    bound = bindings(tree)
    cs_calls = calls(tree, 'copy_object')
    hits = 0
    for c in cs_calls:
        src = kw(c, 'CopySource')
        if not isinstance(src, ast.Dict):
            continue
        d = {ast.literal_eval(k): v for k, v in zip(src.keys, src.values) if isinstance(k, ast.Constant)}
        b, k = name_of(d.get('Bucket')), name_of(d.get('Key'))
        if b and k and (b, k, LEADER) in bound:
            hits += 1
    print('  D_04: copy_object calls=%d, bindings of platinum_destination=%d, CopySource from the leaderboard destination=%d'
          % (len(cs_calls), len(bound), hits))
    return hits >= 1 and hits == len(cs_calls)


def arm_r2(root):
    _, tree = parse(root, D00F)
    bound = bindings(tree)
    heads = calls(tree, 'head_object')
    hits = 0
    for c in heads:
        b, k = name_of(kw(c, 'Bucket')), name_of(kw(c, 'Key'))
        if b and k and (b, k, 'OUTPUT_KEY') in bound:
            hits += 1
    print('  D_00f: head_object calls=%d, bindings of platinum_destination=%d, head of the OUTPUT_KEY destination=%d'
          % (len(heads), len(bound), hits))
    return hits >= 1 and hits == len(heads)


def arm_r3(root):
    gold = os.path.join(root, GOLD)
    sys.path.insert(0, gold)
    os.environ.pop('BD_PLATINUM_MODE', None)
    try:
        from lib import config, platinum_dest
    finally:
        sys.path.pop(0)
    keys = ('platinum/firm/leaderboard.json', 'platinum/firm/leaderboard.prior_week.json',
            'platinum/firm/advisor_nna_canonical.json')
    got = [platinum_dest.destination(k, 'legacy') == (config.S3_BUCKET, k) for k in keys]
    print('  legacy identity: %d of %d keys name (S3_BUCKET, key)' % (sum(got), len(keys)))
    return all(got)


def candidates(root):
    import json
    cen = json.load(open(os.path.join(root, 'org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/'
                                            '0.9.0_WK_ADVI_FIRMBKTS~16/PRODUCER_CENSUS.json'), encoding='utf-8'))
    files = sorted({w['script'] for c in cen['classes'] for w in c['writers']})
    print('  census writer scripts read: %d' % len(files))
    rows = []
    for rel in files:
        try:
            src, tree = parse(root, rel)
        except (OSError, SyntaxError):
            continue
        for attr in ('head_object', 'copy_object', 'get_object'):
            for c in calls(tree, attr):
                seg = ast.get_source_segment(src, c) or ''
                b = ast.unparse(kw(c, 'Bucket')) if kw(c, 'Bucket') is not None else ''
                if 'platinum' in seg and b in ('S3_BUCKET', 'BUCKET'):
                    rows.append('%s:%d %s Bucket=%s' % (os.path.basename(rel), c.lineno, attr, b))
    print('  read-after-write candidates (informational, not graded): %d' % len(rows))
    for r in rows[:40]:
        print('    ' + r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.getcwd())
    a = ap.parse_args()
    arms = [('R1', 'the prior-week rotation copies from the leaderboard destination', arm_r1),
            ('R2', "D_00f's write-success sentinel heads the OUTPUT_KEY destination", arm_r2),
            ('R3', 'the destination in legacy mode is (S3_BUCKET, key) for the three keys', arm_r3)]
    ok = 0
    for rid, text, fn in arms:
        try:
            good = fn(a.root)
        except Exception as exc:  # a read that cannot run is a FAIL, never a skip
            print('  %s raised %s: %s' % (rid, type(exc).__name__, exc))
            good = False
        print('%s %s %s' % ('PASS' if good else 'FAIL', rid, text))
        ok += 1 if good else 0
    try:
        candidates(a.root)
    except Exception as exc:
        print('  candidates arm could not run: %s: %s' % (type(exc).__name__, exc))
    print('ROUND 3 ROTATION AND SENTINEL: %d of %d arms' % (ok, len(arms)))
    return 0 if ok == len(arms) else 1


if __name__ == '__main__':
    sys.exit(main())
