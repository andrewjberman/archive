"""W3_REFETCH_PINNED -- POSN_ASTTAX.TO-W3-1 (slot ~26), the RE-CUT run.

The prior run's fixture bytes lived in portal/.scratch/, which is gitignored and did not
survive the session; the RE-CUT is required to be measured on THE SAME SERVED BYTES. So
each of the six keys is re-fetched BY ITS PINNED VersionId (never "latest") through the
`.tools/aws` shim, and the download is accepted only when its md5 equals the md5 the prior
manifest recorded for that VersionId.

THAT md5 COMPARISON IS THE POINT. A VersionId is an identity claim the plane makes; the
md5 is an identity claim about the bytes on this disk. Only the second one can tell a
truncated or re-encoded download from the object the earlier run actually rendered -- and
`aws s3 cp` returning rc=0 having written nothing is a measured failure mode on this
device, so rc is not the oracle here.

The LIVE head of each key is printed beside the pin, so a key that has MOVED since the
prior run is visible rather than silently assumed static.

Usage (from the workspace worktree root):
    PYTHONUTF8=1 python3 <this> <prior-manifest.json>
"""
import hashlib
import io
import json
import os
import subprocess
import sys

AWS = os.path.join('.tools', 'aws.cmd' if sys.platform == 'win32' else 'aws')


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8')


def main():
    manifest_path = sys.argv[1]
    with io.open(manifest_path, encoding='utf-8') as fh:
        rows = json.load(fh)

    os.makedirs(os.path.join('portal', '.scratch'), exist_ok=True)
    ok = 0
    print('%-34s %-34s %-9s %-34s %s'
          % ('key', 'PINNED VersionId', 'bytes', 'md5(downloaded)', 'vs manifest md5'))
    for r in rows:
        local = r['local']
        head = run([AWS, 's3api', 'head-object', '--bucket', r['bucket'], '--key', r['key'],
                    '--query', '{v:VersionId,lm:LastModified,len:ContentLength}',
                    '--output', 'json'])
        live = json.loads(head.stdout) if head.returncode == 0 else {'v': 'HEAD-FAILED', 'lm': '', 'len': -1}
        get = run([AWS, 's3api', 'get-object', '--bucket', r['bucket'], '--key', r['key'],
                   '--version-id', r['VersionId'], local])
        if get.returncode != 0:
            print('BLOCKED: get-object %s rc=%d %s' % (r['key'], get.returncode, get.stderr.strip()[:200]))
            return 1
        with open(local, 'rb') as fh:
            raw = fh.read()
        md5 = hashlib.md5(raw).hexdigest()
        same = md5 == r['md5']
        ok += 1 if same else 0
        print('%-34s %-34s %-9d %-34s %s'
              % (r['key'].split('/')[-1], r['VersionId'], len(raw), md5,
                 'SAME BYTES' if same else 'DIFFERENT -- manifest ' + r['md5']))
        print('    LIVE head of the same key now: VersionId=%s LastModified=%s bytes=%s  %s'
              % (live['v'], live['lm'], live['len'],
                 'UNMOVED since the prior run' if live['v'] == r['VersionId']
                 else 'MOVED -- the pinned version is still what is rendered'))
        if not same:
            print('BLOCKED: %s md5 %s != pinned %s' % (r['key'], md5, r['md5']))
            return 1
    print('')
    print('DENOMINATOR: %d of %d keys re-fetched BY PINNED VersionId and md5-IDENTICAL '
          'to the prior run' % (ok, len(rows)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
