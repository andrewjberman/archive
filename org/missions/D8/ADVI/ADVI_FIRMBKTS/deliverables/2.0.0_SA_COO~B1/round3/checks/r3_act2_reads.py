"""r3_act2_reads.py -- ADVI_FIRMBKTS FB-f-9 phase B (the mode move): the three read-only checks the act's criteria run.
Issuer 2.0.0_SA_COO~B1. Standard library + boto3. Prints counts and class prefixes only, never a key under an entity.

  deployed-equal [--base 96f3212d22]
      the 19 non-test .py files of data/black_diamond/scripts/gold changed since --base, and gold_dispatch.sh, each
      compared (sha256) with its object under s3://opal-data-bd/code/gold/ (the key by .tools/safe_deploy_core.py
      file_to_s3_target); the repository side is `git show HEAD:<path>`.
      prints: DEPLOY EQUAL: <n> of <N> objects equal the repository at HEAD
  new-home --since ISO
      for each of the 11 served classes (lib/platinum_dest_view.py PLATINUM_CLASSES): the newest LastModified under the
      class's destination prefix in its bucket; counts the classes whose newest is after ISO.
      prints: NEW HOME: <n> of 11 served classes written since <ISO>
  old-home --since ISO
      for each class: the keys under its legacy prefix in the legacy bucket modified after ISO.
      prints: OLD HOME QUIET: <n> keys of 11 classes modified since <ISO>
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import os
import subprocess
import sys

GOLD = 'data/black_diamond/scripts/gold'
LEGACY_BUCKET = 'opal-data-bd'


REF = 'HEAD'   # set from --ref in main(); the repository commit the deployed objects are compared with


def root():
    return subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()


def classes(rt):
    ns = {}
    src = subprocess.run(['git', 'show', '%s:%s/lib/platinum_dest_view.py' % (REF, GOLD)], capture_output=True, text=True,
                         cwd=rt).stdout
    exec(compile(src, 'view', 'exec'), ns)
    return [(p, b, t.replace('{tail}', '')) for p, b, t in ns['PLATINUM_CLASSES']]


def s3():
    import boto3
    return boto3.client('s3', region_name='us-east-1')


def iso(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)


def cmd_deployed(a):
    rt = root()
    sys.path.insert(0, os.path.join(rt, '.tools'))
    import safe_deploy_core as sdc
    names = subprocess.run(['git', 'diff', '--name-only', a.base, REF, '--', GOLD], capture_output=True, text=True,
                           cwd=rt).stdout.split()
    files = [n for n in names if n.endswith('.py') and '/tests/' not in n]
    todo = []
    for n in files:
        tgt = sdc.file_to_s3_target(n)
        if tgt is None:
            print('  UNMAPPED %s' % os.path.basename(n))
            continue
        todo.append((n, tgt[0], tgt[1]))
    todo.append((GOLD + '/gold_dispatch.sh', LEGACY_BUCKET, 'code/gold/gold_dispatch.sh'))
    client = s3()
    ok = 0
    for n, bucket, key in todo:
        want = hashlib.sha256(subprocess.run(['git', 'show', REF + ':' + n], capture_output=True, cwd=rt).stdout).hexdigest()
        try:
            body = client.get_object(Bucket=bucket, Key=key)['Body'].read()
            got = hashlib.sha256(body).hexdigest()
        except Exception as e:  # noqa: BLE001 -- an unreadable object is a difference, never a skip
            got = 'UNREADABLE:' + type(e).__name__
        if got == want:
            ok += 1
        else:
            print('  DIFFERS %s (%s)' % (os.path.basename(n), 'absent or unreadable' if got.startswith('UNREAD') else 'bytes'))
    print('DEPLOY EQUAL: %d of %d objects equal the repository at %s' % (ok, len(todo), REF if REF != 'HEAD' else 'HEAD'))
    return 0 if ok == len(todo) else 1


def _newest(client, bucket, prefix):
    newest = None
    n = 0
    for page in client.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get('Contents', []):
            n += 1
            if newest is None or o['LastModified'] > newest:
                newest = o['LastModified']
    return newest, n


def cmd_new(a):
    rt = root()
    cut = iso(a.since)
    client = s3()
    cl = classes(rt)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(lambda c: _newest(client, c[1], c[2]), cl))
    done = 0
    for (p, b, r), (newest, n) in zip(cl, res):
        written = newest is not None and newest > cut
        done += 1 if written else 0
        print('  %-26s objects=%-6d %s' % (p, n, 'written since' if written else 'NOT written since'))
    print('NEW HOME: %d of %d served classes written since %s' % (done, len(cl), a.since))
    return 0 if done == len(cl) else 1


def _count_after(client, bucket, prefix, cut):
    n = 0
    for page in client.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get('Contents', []):
            if o['LastModified'] > cut:
                n += 1
    return n


def cmd_old(a):
    rt = root()
    cut = iso(a.since)
    client = s3()
    cl = classes(rt)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(lambda c: _count_after(client, LEGACY_BUCKET, c[0], cut), cl))
    for (p, b, r), n in zip(cl, res):
        print('  %-26s modified since: %d' % (p, n))
    total = sum(res)
    print('OLD HOME QUIET: %d keys of %d classes modified since %s' % (total, len(cl), a.since))
    return 0 if total == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('deployed-equal')
    d.add_argument('--base', default='96f3212d22')
    d.add_argument('--ref', default='HEAD', help='the repository commit the objects are compared with (default HEAD; a pinned commit when other projects move HEAD)')
    n = sub.add_parser('new-home')
    n.add_argument('--since', required=True)
    o = sub.add_parser('old-home')
    o.add_argument('--since', required=True)
    a = ap.parse_args()
    global REF
    REF = getattr(a, 'ref', 'HEAD') or 'HEAD'
    return {'deployed-equal': cmd_deployed, 'new-home': cmd_new, 'old-home': cmd_old}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
