"""DELTA_HARNESS_RUN_GENERATOR -- POSN_ASTTAX.TO-V1-1 V1-AC4, one command.

THE BRANCH RULE the two never-widen halves bind this cell to: run the positioning
generator at 69b867c4eb and at HEAD against the SAME live input, diff the two
outputs per key, and classify every difference into the THREE permitted change
classes or OTHER. OTHER must be EMPTY.

WHAT MAKES THE TWO RUNS A CODE DELTA RATHER THAN A CODE-PLUS-INPUT DELTA: every
S3 get_object and every DynamoDB get_item is served from ONE shared on-disk cache
(run_generator.py), so the second arm provably reads the first arm's bytes; each
read logs LIVE or CACHE. No S3 write happens -- put_object is intercepted and its
gzip body is decompressed into a local file.

AWS_LAMBDA_FUNCTION_NAME is set for BOTH arms so load_aum_data takes the S3 branch
the deployed function takes. Without it the harness silently omits current_holdings
-- 3987 leaf keys become 1701 -- and 10 of the 52 base..HEAD code hunks live in
exactly that section.

Usage: timeout 900 python .scratch/delta_harness.py
"""
import json
import os
import shutil
import subprocess
import sys
import tarfile

BASE_PIN = '69b867c4eb'
PKG = 'infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning'
NEW_CLASSES = ('structured', 'commodities', 'alternatives')
ROOT = os.getcwd()
SCRATCH = os.path.join(ROOT, '.scratch')
CACHE = os.path.join(SCRATCH, 'cache')

INPUT_LINE = ('INPUT: s3://opal-data-portal-v2/benchmarks/model_20260911_v1.pkl '
              '(VersionId jcG67EudvJWQd0.cguenteFECbQNJMa1) + '
              's3://opal-data-portal-v2/json/portfolios/aum-metrics.json + the live '
              'etf-classifications table; event data_as_of_date 2026-09-11, '
              'model_pkl_key benchmarks/model_20260911_v1.pkl -- the exact input the last '
              'SUCCEEDED YangDataPipeline execution 20260911_v1-1c95bba7 handed '
              'yang-generate-positioning (LambdaFunctionScheduled event 83).')


def git(*args):
    # argv form, NO shell: subprocess shell=True lands in cmd.exe on this device, not bash,
    # and an MSYS tar cannot open a Windows-form -C argument either. So: git writes a tar,
    # python's own tarfile unpacks it, and no shell is involved at any step.
    r = subprocess.run(['git'] + list(args), capture_output=True, cwd=ROOT)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode('utf-8', 'replace'))
        raise SystemExit('REFUSED: git %s -> rc=%d' % (' '.join(args), r.returncode))
    return r.stdout


def extract(pin, rel_dest):
    dest = os.path.join(ROOT, rel_dest)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    tar_path = dest + '.tar'
    with open(tar_path, 'wb') as fh:
        fh.write(git('archive', pin, PKG))
    with tarfile.open(tar_path) as tf:
        tf.extractall(dest)
    os.remove(tar_path)
    return os.path.join(dest, PKG.replace('/', os.sep))


def run_arm(pkg_dir, out_json):
    env = dict(os.environ)
    env['AWS_LAMBDA_FUNCTION_NAME'] = 'yang-generate-positioning'
    r = subprocess.run([sys.executable, os.path.join(SCRATCH, 'run_generator.py'),
                        pkg_dir, out_json, CACHE],
                       capture_output=True, text=True, cwd=ROOT, env=env)
    if r.returncode != 0:
        sys.stderr.write(r.stdout[-4000:] + r.stderr[-4000:])
        raise SystemExit('REFUSED: generator arm failed rc=%d' % r.returncode)
    for line in (r.stdout + r.stderr).splitlines():
        if '[harness]' in line:
            print(line.rstrip())
    return json.load(open(out_json, encoding='utf-8'))


def flatten(obj, prefix=''):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, '%s.%s' % (prefix, k) if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, '%s[%d]' % (prefix, i)))
    else:
        out[prefix] = obj
    return out


def leaf(p):
    return p.split('.')[-1].split('[')[0]


def classify(path, old=None, new=None, kind='changed'):
    lf = leaf(path)
    if path == 'generated_at':
        return 'volatile-run-clock'
    # C-BENCHMARK, amendment (c) of the re-cut face (issuer ruling Z-S78 on row
    # W19-S6): the SERVED labelled-zero benchmark row. The emit adds the path
    # shape benchmarks.etf.<class>.* for EXACTLY the three ratified classes that
    # have no benchmark ETF -- admitted BY NAME, one class at a time, so any
    # fourth key appearing under benchmarks.etf stays OTHER and still stops the
    # apply. OTHER remains the discriminator.
    for _new_class in NEW_CLASSES:
        if path == 'benchmarks.etf.%s' % _new_class:
            return 'benchmark-row/allocation-key'
        if path.startswith('benchmarks.etf.%s.' % _new_class):
            return 'benchmark-row/allocation-key'
    if lf in NEW_CLASSES:
        return 'benchmark-row/allocation-key'
    sentinel = ('unclassified', 'Unclassified', 'Unknown', 'Not classified')
    if lf in ('assetClass', 'asset_class', 'assetClassLabel', 'asset_class_label',
              'assetClassRecognized', 'asset_class_recognized'):
        return 'unrecognised-security-label'
    if kind == 'changed' and (str(old) in sentinel or str(new) in sentinel):
        return 'unrecognised-security-label'
    if lf in ('name', 'benchmarkName', 'displayName'):
        if kind == 'changed' and isinstance(old, str) and isinstance(new, str):
            return 'display-name'
        if kind == 'added':
            return 'display-name'
    return 'OTHER'


print(INPUT_LINE)
print('')
head = git('rev-parse', '--short', 'HEAD').decode().strip()
print('ARM 1 -- BASE %s (the build the live CodeSha256 PRg64EGzQtLw7/HAhyN/jNP6rd01PrcLK4wKqCHAKfQ= was cut from)' % BASE_PIN)
base = run_arm(extract(BASE_PIN, '.scratch/base_pkg'),
               os.path.join(SCRATCH, 'out_base_full.json'))
print('ARM 2 -- HEAD %s' % head)
head_payload = run_arm(extract('HEAD', '.scratch/head_pkg'),
                       os.path.join(SCRATCH, 'out_head_full.json'))
print('')

fb, fh = flatten(base), flatten(head_payload)
added = sorted(set(fh) - set(fb))
removed = sorted(set(fb) - set(fh))
changed = sorted(k for k in set(fb) & set(fh) if fb[k] != fh[k])

buckets = {}
for p in added:
    buckets.setdefault(classify(p, new=fh[p], kind='added'), []).append(('ADDED', p, None, fh[p]))
for p in removed:
    buckets.setdefault(classify(p, old=fb[p], kind='removed'), []).append(('REMOVED', p, fb[p], None))
for p in changed:
    buckets.setdefault(classify(p, old=fb[p], new=fh[p], kind='changed'), []).append(
        ('CHANGED', p, fb[p], fh[p]))

print('BASE  : %s  leaf keys=%d' % (BASE_PIN, len(fb)))
print('HEAD  : %s  leaf keys=%d' % (head, len(fh)))
print('DIFF  : added=%d removed=%d changed=%d  (differing leaf keys=%d)'
      % (len(added), len(removed), len(changed), len(added) + len(removed) + len(changed)))
print('')
order = ['display-name', 'unrecognised-security-label', 'benchmark-row/allocation-key',
         'volatile-run-clock', 'OTHER']
for cls in order:
    print('CLASS %-32s count=%d' % (cls, len(buckets.get(cls, []))))
for cls in buckets:
    if cls not in order:
        print('CLASS %-32s count=%d  (UNEXPECTED CLASS)' % (cls, len(buckets[cls])))
print('')
other = buckets.get('OTHER', [])
print('OTHER count = %d  -> BRANCH %s' % (len(other), 'A (proceed)' if not other else 'B (STOP, row, no apply)'))
for row in other:
    print('  OTHER %s %s  base=%r head=%r' % row)
print('')

print('--- THE CHECKS THAT COULD FALSIFY THE CLASSIFICATION (V1-AC13 readings) ---')
nz = [r for r in buckets.get('benchmark-row/allocation-key', []) if r[3] not in (0, 0.0)]
print('  benchmark-row/allocation-key rows whose HEAD value is NOT zero: %d of %d'
      % (len(nz), len(buckets.get('benchmark-row/allocation-key', []))))
for r in nz:
    print('     NON-ZERO %s %s head=%r' % (r[0], r[1], r[3]))
shapes = sorted({p[1].replace('UST', '<M>').replace('ULT', '<M>').replace('INT', '<M>')
                 .replace('LT', '<M>').replace('ST', '<M>')
                 for p in buckets.get('benchmark-row/allocation-key', [])})
print('  distinct path shapes in that class: %d' % len(shapes))
for s in shapes:
    print('     %s' % s)
names = [k for k in set(fb) & set(fh) if leaf(k) == 'name']
print('  display-name negative control: %d name leaf keys present in BOTH, %d differing'
      % (len(names), len([k for k in names if fb[k] != fh[k]])))
print('  CHANGED rows in full (all classes): %d' % len(changed))
for k in changed:
    print('     CHANGED %s  base=%r head=%r' % (k, fb[k], fh[k]))
print('  membership per model (tickers, base vs head):')
for m in sorted(base.get('portfolios', {})):
    tb = [h['ticker'] for h in base['portfolios'][m]['holdings']]
    th = [h['ticker'] for h in head_payload['portfolios'][m]['holdings']]
    print('     %-4s %d vs %d  identical=%s | benchmark %r -> %r'
          % (m, len(tb), len(th), tb == th,
             base['portfolios'][m]['benchmark']['ticker'],
             head_payload['portfolios'][m]['benchmark']['ticker']))

raise SystemExit(0 if not other else 1)
