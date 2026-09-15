"""W3-AC5 CONTROL (the RE-CUT run) -- the views this act must NOT have moved, compared
section by section against the dump taken at refs/drains/posn-6-portal (= 10a2799c, this
worker's PRIOR commit, which is what the ref now points at).

THE CONTROL IS THE UNCHANGED VIEWS, not the changed one. A re-cut that quietly re-rendered
Models or ETFs would pass every presence check and still be wrong, so the discriminating
question is whether EXACTLY ONE view moved. Each dump is split on its own section banners
and the sections are compared line for line; the Models LABELS line is printed from both
sides whatever the verdict, because that is the byte-identity W3-AC5 names.

Usage: PYTHONUTF8=1 python3 <this> <before.txt> <after.txt>
"""
import io
import re
import sys


def sections(path):
    with io.open(path, encoding='utf-8', errors='replace') as fh:
        t = fh.read()
    parts = re.split(r'^=+ (.+?) =+$', t, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        out[parts[i].strip()] = parts[i + 1]
    return out


def line(block, prefix):
    for ln in block.splitlines():
        if ln.startswith(prefix):
            return ln
    return '(no ' + prefix + ' line)'


def main():
    before_path, after_path = sys.argv[1], sys.argv[2]
    before, after = sections(before_path), sections(after_path)
    print('BEFORE: %s  (%d sections)' % (before_path, len(before)))
    print('AFTER : %s  (%d sections)' % (after_path, len(after)))
    print('')
    shared = [k for k in after if k in before]
    only_after = [k for k in after if k not in before]
    only_before = [k for k in before if k not in after]
    same = 0
    for k in shared:
        identical = before[k] == after[k]
        same += 1 if identical else 0
        print('%-46s %s' % (k, 'IDENTICAL' if identical else 'CHANGED'))
        if not identical:
            b = before[k].splitlines()
            a = after[k].splitlines()
            for i in range(max(len(a), len(b))):
                lb = b[i] if i < len(b) else '(absent)'
                la = a[i] if i < len(a) else '(absent)'
                if lb != la and (lb.startswith(('LEGEND', 'PRESENCE', 'COUNTS', 'ROWS', 'LABELS'))
                                 or la.startswith(('LEGEND', 'PRESENCE', 'COUNTS', 'ROWS', 'LABELS'))):
                    print('    BEFORE  ' + lb[:220])
                    print('    AFTER   ' + la[:220])
    print('')
    print('SECTIONS COMPARED: %d; IDENTICAL %d of %d; CHANGED %d of %d'
          % (len(shared), same, len(shared), len(shared) - same, len(shared)))
    print('SECTIONS ONLY IN THE AFTER DUMP (added by this run): %s' % (only_after or 'none'))
    print('SECTIONS ONLY IN THE BEFORE DUMP: %s' % (only_before or 'none'))
    print('')
    print('THE MODELS LABEL CONTROL, printed whatever the verdict:')
    for k in ('MODELS / Portfolio view (Expand Details open)', 'ETFS / Portfolio view',
              'SATELLITES / Portfolio view'):
        if k in before and k in after:
            lb, la = line(before[k], 'LABELS('), line(after[k], 'LABELS(')
            print('  ' + k)
            print('    BEFORE ' + lb[:200])
            print('    AFTER  ' + la[:200])
            print('    %s' % ('BYTE-IDENTICAL' if lb == la else 'DIFFERENT'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
