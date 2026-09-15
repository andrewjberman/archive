"""FETCH_SERVED_V8 -- POSN_ASTTAX.TO-V8-1 V8-AC10: pull the SEVEN served keys the
Positioning page fetches, AFTER the driven refresh, and record each one's VersionId.

NEVER HAND-WRITTEN. Every byte the fixtures carry is downloaded here from the bucket
that serves it, and the manifest this writes names the bucket, the key, the VersionId,
the LastModified and an md5 of the raw bytes -- so the fixture a capture was taken
against is identifiable later BY CONTENT, not by filename. build_fixtures_v8.js reads
this manifest instead of carrying literals, which is the one change from slot ~22's
build_fixtures_v7.js: its VersionIds were typed into the source, and after a driven
refresh a typed VersionId is a stale claim.

WHAT 'AFTER THE DRIVEN REFRESH' MEANS TODAY, stated rather than implied: V8-AC14
refreshed positioning_data.json and allocation_summary.json; holdings_attribution_data.json
and the three satellites keys DID NOT REFRESH (rows W19-S15, W19-S16, W19-S17 -- one
recorded event names a deleted workbook, and both cot producers refuse on absent
upstream partitions). This script prints, per key, whether the bytes it fetched are
POST-RETAG or PRE-RETAG, so no reader of the capture can mistake one for the other.

Usage: python .../fetch_served_v8.py
"""
import datetime
import hashlib
import json
import os

import boto3

SCRATCH = '.scratch'
MANIFEST = os.path.join(SCRATCH, 'v8_fixture_manifest.json')

# (local raw file, gzip?, bucket, key, fixture URL substring the page fetches)
SRC = [
    ('v8_posn.raw', True, 'opal-data-portal-v2', 'json/positioning/positioning_data.json',
     '/api/general/positioning/positioning_data.json'),
    ('v8_etf.raw', False, 'opal-data-portal-v2', 'platinum/etfs/positioning_data.json',
     '/api/general/etfs/positioning_data.json'),
    ('v8_attr.raw', False, 'opal-data-portal-v2',
     'json/positioning/holdings_attribution_data.json',
     '/api/general/positioning/holdings_attribution_data.json'),
    ('v8_sat_registry.raw', False, 'opal-data-cot', 'platinum/satellites/registry.json',
     '/api/scoped/satellites/registry.json'),
    ('v8_sat_holdings.raw', False, 'opal-data-cot', 'platinum/satellites/holdings.json',
     '/api/scoped/satellites/holdings.json'),
    ('v8_sat_characteristics.raw', False, 'opal-data-cot',
     'platinum/satellites/characteristics.json',
     '/api/scoped/satellites/characteristics.json'),
]

# The pre-retag VersionIds, printed before the first update-item (r1_before_served_heads.txt)
PRE_RETAG = {
    'json/positioning/positioning_data.json': 'OuevyO7kCIJdEqzGlJWd.z.8S8pqiXJk',
    'json/positioning/allocation_summary.json': 'HfPxh0kkU6s5yCYCyKvv7SRP977Dhijp',
    'json/positioning/holdings_attribution_data.json': 'mOBBmXhjOyNPM2ue_.3C9G1eR79lUrlk',
    'platinum/satellites/registry.json': 'XaX6zaVWH7ybXnRBu2jeF2PNABUhezuM',
    'platinum/satellites/holdings.json': 'BRjqyqnB0pIdLUHOvDY3B_Sh9b0EXIPw',
    'platinum/satellites/characteristics.json': 'rt61ogajZQy79meUlsY1X_mIdPngxJTZ',
}


def main():
    s3 = boto3.client('s3', region_name='us-east-1')
    rows = []
    print('SERVED BYTES FOR THE FIXTURES -- fetched %s'
          % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    print('%-46s %-34s %-22s %-10s %s'
          % ('key', 'VersionId', 'LastModified', 'bytes', 'vintage'))
    for local, gz, bucket, key, urlkey in SRC:
        r = s3.get_object(Bucket=bucket, Key=key)
        raw = r['Body'].read()
        path = os.path.join(SCRATCH, local)
        with open(path, 'wb') as fh:
            fh.write(raw)
        ver = r.get('VersionId')
        lm = r['LastModified'].astimezone(datetime.timezone.utc).strftime(
            '%Y-%m-%dT%H:%M:%SZ')
        pre = PRE_RETAG.get(key)
        vintage = ('POST-RETAG (refreshed)' if pre and ver != pre
                   else 'PRE-RETAG (NOT refreshed)' if pre
                   else 'no pre-retag baseline recorded')
        rows.append({'local': path, 'gzip': gz, 'bucket': bucket, 'key': key,
                     'urlkey': urlkey, 'VersionId': ver, 'LastModified': lm,
                     'bytes': len(raw), 'md5': hashlib.md5(raw).hexdigest(),
                     'pre_retag_VersionId': pre, 'vintage': vintage})
        print('%-46s %-34s %-22s %-10d %s'
              % (key.split('/')[-1], ver, lm, len(raw), vintage))
    with open(MANIFEST, 'w', encoding='utf-8', newline='') as fh:
        json.dump(rows, fh, indent=2)
    n_post = sum(1 for r in rows if r['vintage'].startswith('POST'))
    print('')
    print('DENOMINATOR: %d key(s) fetched; POST-RETAG %d, PRE-RETAG %d'
          % (len(rows), n_post, len(rows) - n_post))
    print('manifest: %s' % MANIFEST)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
