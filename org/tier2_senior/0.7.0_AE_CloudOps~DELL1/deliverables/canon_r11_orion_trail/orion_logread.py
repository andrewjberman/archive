"""Read S3 server access logs for opal-data-assets (TO ADHOC.canon-r11-orion-reader-trail, step 2). Read-only.

  python -I orion_logread.py list                 log objects delivered, per delivery hour (denominator) and the last object's time
  python -I orion_logread.py read <out.json>      REST.GET.OBJECT lines whose key begins orion/: requester, ip, user agent, per-hour counts,
                                                  bytes sent, key prefix to the SECOND level only. No deeper key, client name or account id is printed or saved.
"""
from __future__ import annotations

import collections
import json
import re
import sys
from datetime import datetime, timezone

import boto3

BUCKET = 'opal-data-security-access-logs'
PREFIX = 'opal-data-assets/'
START = datetime(2026, 10, 16, 18, 40, tzinfo=timezone.utc)
s3 = boto3.client('s3', region_name='us-east-1')

LINE = re.compile(r'^(\S+) (\S+) \[([^\]]+)\] (\S+) (\S+) (\S+) (\S+) (\S+) "([^"]*)" (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) "([^"]*)" "([^"]*)" (\S+)')


def objects() -> list:
    out = []
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=BUCKET, Prefix=PREFIX):
        out.extend(o for o in page.get('Contents', []) if o['LastModified'] >= START)
    return out


def second_level(key: str) -> str:
    parts = key.split('/')
    return '/'.join(parts[:2]) + ('/' if len(parts) > 2 else '')


def lst() -> int:
    objs = objects()
    per = collections.Counter(o['LastModified'].strftime('%Y-%m-%d %HZ') for o in objs)
    print('log objects since %s: %d (bucket %s prefix %s)' % (START.isoformat(), len(objs), BUCKET, PREFIX))
    for h, n in sorted(per.items()):
        print('  %s  %d' % (h, n))
    if objs:
        print('first object delivered', min(o['LastModified'] for o in objs).isoformat(), '| last', max(o['LastModified'] for o in objs).isoformat())
    return 0


def read(out: str) -> int:
    objs = objects()
    lines = parsed = 0
    gets = []
    ops = collections.Counter()
    def fetch(o):
        return s3.get_object(Bucket=BUCKET, Key=o['Key'])['Body'].read().decode('utf-8', 'replace')

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(24) as ex:
        bodies = list(ex.map(fetch, objs))
    for body in bodies:
        for ln in body.splitlines():
            lines += 1
            m = LINE.match(ln)
            if not m:
                continue
            parsed += 1
            g = m.groups()
            op, key = g[6], g[7]
            ops[op] += 1
            if op == 'REST.GET.OBJECT' and key.startswith('orion/'):
                ts = datetime.strptime(g[2].split(' ')[0], '%d/%b/%Y:%H:%M:%S').replace(tzinfo=timezone.utc)
                bytes_sent = 0 if g[11] == '-' else int(g[11])
                gets.append({'hour': ts.strftime('%Y-%m-%d %HZ'), 'requester': g[4], 'ip': g[3], 'ua': g[16][:90],
                             'status': g[9], 'bytes': bytes_sent, 'prefix2': second_level(key)})
    per_hour = collections.Counter(x['hour'] for x in gets)
    bytes_hour = collections.Counter()
    for x in gets:
        bytes_hour[x['hour']] += x['bytes']
    summary = {
        'claim': 'measured', 'bucket': BUCKET, 'prefix': PREFIX, 'log_objects_read': len(objs), 'lines': lines, 'lines_parsed': parsed,
        'ops_top': ops.most_common(6), 'orion_get_lines': len(gets), 'orion_get_bytes': sum(x['bytes'] for x in gets),
        'requesters': collections.Counter(x['requester'] for x in gets).most_common(10),
        'source_ips': collections.Counter(x['ip'] for x in gets).most_common(10),
        'user_agents': collections.Counter(x['ua'] for x in gets).most_common(10),
        'statuses': collections.Counter(x['status'] for x in gets).most_common(6),
        'prefix_second_level': collections.Counter(x['prefix2'] for x in gets).most_common(10),
        'size_stats': {'max_bytes': max((x['bytes'] for x in gets), default=0), 'gets_ge_10MB': sum(1 for x in gets if x['bytes'] >= 10_000_000),
                       'gets_ge_1MB': sum(1 for x in gets if x['bytes'] >= 1_000_000), 'mean_bytes': int(sum(x['bytes'] for x in gets) / max(len(gets), 1))},
        'requester_by_hour': sorted(collections.Counter((x['hour'], x['requester'].split('/')[-1] if 'assumed-role' in x['requester'] else x['requester'].split('/')[-1]) for x in gets).items()),
        'gets_per_hour': sorted(per_hour.items()), 'bytes_per_hour': sorted(bytes_hour.items()),
        'objects_per_hour': sorted(collections.Counter(o['LastModified'].strftime('%Y-%m-%d %HZ') for o in objs).items()),
        'last_object': max(o['LastModified'] for o in objs).isoformat() if objs else None,
    }
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=1, default=str)
    for k in ('log_objects_read', 'lines', 'lines_parsed', 'ops_top', 'orion_get_lines', 'orion_get_bytes', 'requesters', 'source_ips', 'user_agents',
              'statuses', 'prefix_second_level', 'size_stats', 'requester_by_hour', 'gets_per_hour', 'bytes_per_hour', 'last_object'):
        print(k, '=', summary[k])
    return 0


if __name__ == '__main__':
    sys.exit(lst() if sys.argv[1] == 'list' else read(sys.argv[2]))
