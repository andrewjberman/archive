"""r3_dispatch.py -- FB-f-9 phase A4: the two edits to gold_dispatch.sh, read by running them.

The file carries two marked blocks (the markers are the contract; the blocks are plain bash):

  # >>> PLATINUM-MODE (ADVI_FIRMBKTS FB-f-9) >>>        ... sets BD_PLATINUM_MODE=canonical on a scheduled production
  # <<< PLATINUM-MODE (ADVI_FIRMBKTS FB-f-9) <<<            chain run only, from the shell variables MODE, DRY_RUN,
                                                            GOLD_KEEP_ALIVE and the marker file ${GOLD_QA_MARKER:-/tmp/GOLD_QA_REBUILD}
  # >>> GATE-READ-LOCATION (ADVI_FIRMBKTS FB-f-9) >>>   ... sets gold_hm_loc, the s3 URI the freshness gate reads
  # <<< GATE-READ-LOCATION (ADVI_FIRMBKTS FB-f-9) <<<       (header_metrics.json) through lib/platinum_dest.py source(),
                                                            with SCRIPTS naming the directory that holds lib/

  python r3_dispatch.py --arm export|gate [--root CHECKOUT] [--file PATH]

Arm export runs the block in bash under eight environments and prints each result; arm gate runs the block with the
mode unset and with BD_PLATINUM_MODE=canonical and compares the printed location to the module's own answer. Exit 0
only when every case passes. Plain ASCII.
"""
import argparse
import os
import re
import subprocess
import sys

GOLD = 'data/black_diamond/scripts/gold'
KEY = 'gold/artifacts/summary/header_metrics.json'


def block(text, name):
    m = re.search(r'# >>> %s \(ADVI_FIRMBKTS FB-f-9\) >>>\n(.*?)\n# <<< %s \(ADVI_FIRMBKTS FB-f-9\) <<<' % (name, name),
                  text, re.S)
    return m.group(1) if m else None


def run_bash(script, env_extra):
    env = {'PATH': os.environ.get('PATH', ''), 'HOME': os.environ.get('HOME', ''),
           'SYSTEMROOT': os.environ.get('SYSTEMROOT', '')}
    env.update(env_extra)
    r = subprocess.run(['bash', '-c', script], env=env, capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def arm_export(text):
    b = block(text, 'PLATINUM-MODE')
    if b is None:
        print('  FAIL the PLATINUM-MODE block is absent')
        return False
    import tempfile
    marker = os.path.join(tempfile.gettempdir(), 'r3_dispatch_marker_%d' % os.getpid()).replace(chr(92), '/')
    cases = [  # (label, shell variables, extra env, marker present, expected)
        ('scheduled chain, no overrides', 'MODE=chain; DRY_RUN=0', {}, False, 'canonical'),
        ('single', 'MODE=single; DRY_RUN=0', {}, False, 'UNSET'),
        ('group', 'MODE=group; DRY_RUN=0', {}, False, 'UNSET'),
        ('chain dry-run', 'MODE=chain; DRY_RUN=1', {}, False, 'UNSET'),
        ('QA keep-alive', 'MODE=chain; DRY_RUN=0', {'GOLD_KEEP_ALIVE': '1'}, False, 'UNSET'),
        ('QA rebuild marker', 'MODE=chain; DRY_RUN=0', {}, True, 'UNSET'),
        ('mode already set to legacy', 'MODE=chain; DRY_RUN=0', {'BD_PLATINUM_MODE': 'legacy'}, False, 'legacy'),
        ('mode already set to canonical', 'MODE=chain; DRY_RUN=0', {'BD_PLATINUM_MODE': 'canonical'}, False, 'canonical'),
    ]
    ok = 0
    for label, svars, extra, mk, want in cases:
        if mk:
            open(marker, 'w').close()
        elif os.path.exists(marker):
            os.remove(marker)
        env = dict(extra)
        env['GOLD_QA_MARKER'] = marker
        script = "%s\n%s\nprintf '%%s' \"${BD_PLATINUM_MODE-UNSET}\"" % (svars, b)
        rc, out, err = run_bash(script, env)
        good = rc == 0 and out == want
        print('  %s %-32s -> %r (want %r)%s' % ('PASS' if good else 'FAIL', label, out, want, '' if rc == 0 else ' rc=%d' % rc))
        ok += 1 if good else 0
    if os.path.exists(marker):
        os.remove(marker)
    print('  export cases: %d of %d' % (ok, len(cases)))
    return ok == len(cases)


def arm_gate(text, root):
    b = block(text, 'GATE-READ-LOCATION')
    if b is None:
        print('  FAIL the GATE-READ-LOCATION block is absent')
        return False
    gold = os.path.join(root, GOLD)
    sys.path.insert(0, gold)
    try:
        from lib import platinum_dest as pd
        from lib.config import S3_BUCKET
    finally:
        sys.path.pop(0)
    legacy_want = 's3://%s/%s' % (S3_BUCKET, KEY)
    cb, ck = pd.source(KEY, 'canonical')
    canon_want = 's3://%s/%s' % (cb, ck)
    ok = 0
    for label, env_extra, want in (('mode unset (legacy)', {}, legacy_want),
                                   ('mode canonical', {'BD_PLATINUM_MODE': 'canonical'}, canon_want),
                                   ('lib absent (fallback)', {'R3_NO_LIB': '1'}, 's3://${BD_S3_BUCKET}/' + KEY)):
        scripts = gold if 'R3_NO_LIB' not in env_extra else os.path.join(root, 'no_such_dir_r3')
        pre = "BD_S3_BUCKET=%s; SCRIPTS=%s\n" % (S3_BUCKET, scripts.replace('\\', '/'))
        rc, out, err = run_bash(pre + b + "\nprintf '%s' \"$gold_hm_loc\"", dict(env_extra, BD_S3_BUCKET=S3_BUCKET, GOLD_PYTHON=sys.executable.replace(chr(92), '/')))
        want_x = want.replace('${BD_S3_BUCKET}', S3_BUCKET)
        good = rc == 0 and out == want_x
        print('  %s %-24s -> %r (want %r)' % ('PASS' if good else 'FAIL', label, out, want_x))
        ok += 1 if good else 0
    print('  gate cases: %d of 3' % ok)
    return ok == 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', required=True, choices=('export', 'gate'))
    ap.add_argument('--root', default=os.getcwd())
    ap.add_argument('--file', default=None)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    path = a.file or os.path.join(root, GOLD, 'gold_dispatch.sh')
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    good = arm_export(text) if a.arm == 'export' else arm_gate(text, root)
    print('ROUND 3 DISPATCH %s: %s' % (a.arm.upper(), 'ALL CASES PASS' if good else 'CASES FAIL'))
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
