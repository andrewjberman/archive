"""W25_FETCH_MANIFEST -- POSN_ASTTAX.TO-W2-1 (slot ~25): record, by CONTENT, the served
bytes the ui-smoke fixtures are built from.

Modelled on slot ~26's w3_fetch_manifest.py (itself modelled on slot ~19's v8 builder).
The six keys were downloaded with the `.tools/aws s3api get-object` SHIM (never bare aws,
never hand-written) into portal/.scratch/. This script re-HEADS each key through the same
shim, prints the VersionId / LastModified / ContentLength the plane reports NOW, computes
an md5 over the local raw file, and refuses if the local byte count disagrees with the
object's ContentLength -- so a truncated download cannot become a fixture.

Every VersionId in the manifest is MEASURED at manifest time, never typed into a source
file: after a refresh a typed VersionId is a stale claim about bytes that have moved.

Usage (from the workspace worktree root): PYTHONUTF8=1 python3 <this> <out-manifest.json>
"""
import hashlib
import json
import os
import subprocess
import sys

AWS = os.path.join('.tools', 'aws.cmd' if sys.platform == 'win32' else 'aws')
SCRATCH = os.path.join('portal', '.scratch')

# (local raw file, gzip?, bucket, key, the URL substring ui-smoke matches on)
SRC = [
    ('w25_posn.raw', True, 'opal-data-portal-v2',
     'json/positioning/positioning_data.json',
     '/api/general/positioning/positioning_data.json'),
    ('w25_etf.raw', False, 'opal-data-portal-v2',
     'platinum/etfs/positioning_data.json',
     '/api/general/etfs/positioning_data.json'),
    ('w25_attr.raw', False, 'opal-data-portal-v2',
     'json/positioning/holdings_attribution_data.json',
     '/api/general/positioning/holdings_attribution_data.json'),
    ('w25_sat_registry.raw', False, 'opal-data-cot',
     'platinum/satellites/registry.json',
     '/api/scoped/satellites/registry.json'),
    ('w25_sat_holdings.raw', False, 'opal-data-cot',
     'platinum/satellites/holdings.json',
     '/api/scoped/satellites/holdings.json'),
    ('w25_sat_characteristics.raw', False, 'opal-data-cot',
     'platinum/satellites/characteristics.json',
     '/api/scoped/satellites/characteristics.json'),
]

# The floors the task order names. A VersionId is not orderable, so each is recorded as an
# EQUALITY witness with the LastModified beside it, never inferred from the string.
HOLDINGS_FLOOR = '67GP52SdV1rw6QFVNPytU6ec4TvhwJh3'
CHARACTERISTICS_FLOOR = '74d9.pGWF16Ox7cXKGax.zQw.lhwi5yI'


def head(bucket, key):
    out = subprocess.run(
        [AWS, 's3api', 'head-object', '--bucket', bucket, '--key', key,
         '--query', '{v:VersionId,lm:LastModified,len:ContentLength,ce:ContentEncoding}',
         '--output', 'json'],
        capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(out.stdout)


def main():
    out_path = sys.argv[1]
    rows = []
    print('%-46s %-34s %-26s %-9s %s'
          % ('key', 'VersionId', 'LastModified', 'bytes', 'local md5'))
    for local, gz, bucket, key, urlkey in SRC:
        meta = head(bucket, key)
        path = os.path.join(SCRATCH, local)
        with open(path, 'rb') as fh:
            raw = fh.read()
        md5 = hashlib.md5(raw).hexdigest()
        if len(raw) != meta['len']:
            print('BLOCKED: %s local %d bytes != ContentLength %d'
                  % (key, len(raw), meta['len']))
            return 1
        rows.append({'local': path.replace('\\', '/'), 'gzip': gz, 'bucket': bucket,
                     'key': key, 'urlkey': urlkey, 'VersionId': meta['v'],
                     'LastModified': meta['lm'], 'ContentEncoding': meta['ce'],
                     'bytes': len(raw), 'md5': md5})
        print('%-46s %-34s %-26s %-9d %s'
              % (key.split('/')[-1], meta['v'], meta['lm'], len(raw), md5))
    with open(out_path, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(rows, fh, indent=2)
        fh.write('\n')
    hold = [r for r in rows if r['key'].endswith('satellites/holdings.json')][0]
    char = [r for r in rows if r['key'].endswith('satellites/characteristics.json')][0]
    print('')
    print('HOLDINGS FLOOR CHECK: served VersionId=%s  floor=%s  %s'
          % (hold['VersionId'], HOLDINGS_FLOOR,
             'AT THE FLOOR' if hold['VersionId'] == HOLDINGS_FLOOR
             else 'DIFFERENT -- LastModified %s decides' % hold['LastModified']))
    print('CHARACTERISTICS (POST-B6) CHECK: served VersionId=%s  named=%s  %s'
          % (char['VersionId'], CHARACTERISTICS_FLOOR,
             'AT THE NAMED POST-B6 VERSION' if char['VersionId'] == CHARACTERISTICS_FLOOR
             else 'DIFFERENT -- LastModified %s decides' % char['LastModified']))
    print('DENOMINATOR: %d of %d keys fetched, headed and md5-ed' % (len(rows), len(SRC)))
    print('manifest: %s' % out_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
