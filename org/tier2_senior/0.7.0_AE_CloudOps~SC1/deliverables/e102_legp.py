"""Leg P enumerator (MDPF_SECCLASS TO-SC-e102b, 0.7.0_AE_CloudOps~SC1). Read-only.

  python -I e102_legp.py legp <out.json> <body_out.json>   IsLatest VersionIds of the four mix families + the live mix daily summary body
  python -I e102_legp.py version                            one line: the mix daily summary's latest VersionId + ETag (the Branch 1 restore target)

Every key is derived: lib/platinum_dest.py source()/list_target() in canonical mode, and lib/s3_layout.py
(MIX_DAILY_SUMMARY, FIRM_MIX_VIEWS_DAILY, LEGACY, advisor_mix_daily_key, legacy_advisor_mix_daily_key).
Pagination is counted client side; a key is read with list_object_versions(Prefix=key), IsLatest and exact key only.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

GOLD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..',
                                    'data', 'black_diamond', 'scripts', 'gold'))
sys.path.insert(0, GOLD)
os.environ['BD_PLATINUM_MODE'] = 'canonical'

import boto3  # noqa: E402

from lib import s3_layout as L  # noqa: E402
from lib.platinum_dest import destination, list_target, source  # noqa: E402

FIRM_SUMMARY_LEGACY = 'platinum/firm/mix_summary.json'
ADV_PREFIX = 'gold/entities/advisors/'


def _latest(s3, bucket: str, key: str):
    """(row or None, pages) for the exact key, IsLatest only."""
    pages = 0
    row = None
    for page in s3.get_paginator('list_object_versions').paginate(Bucket=bucket, Prefix=key):
        pages += 1
        for v in page.get('Versions', []):
            if v['Key'] == key and v['IsLatest']:
                row = {'ETag': v['ETag'].strip('"'), 'LastModified': v['LastModified'].isoformat(),
                       'Size': v['Size'], 'VersionId': v['VersionId']}
    return row, pages


def mix_summary_target():
    return source(L.MIX_DAILY_SUMMARY)


def legp(out: str, body_out: str) -> int:
    s3 = boto3.client('s3')
    families: dict = {}
    keys: dict = {}
    total_pages = 0

    def add(family: str, legacy_key: str, bucket: str, key: str) -> None:
        nonlocal total_pages
        k = f'{bucket}/{key}'
        if k in keys:
            return
        row, pages = _latest(s3, bucket, key)
        total_pages += pages
        keys[k] = dict(row or {'ETag': None, 'VersionId': None}, family=family, legacy_key=legacy_key, pages=pages,
                       present=row is not None)
        families.setdefault(family, []).append(k)

    # mix daily summary (C_06)
    b, k = source(L.MIX_DAILY_SUMMARY)
    add('mix_daily_summary', L.MIX_DAILY_SUMMARY, b, k)
    # firm_mix_views_daily (D_03) and its legacy alias
    b, k = destination(L.FIRM_MIX_VIEWS_DAILY)
    add('firm_mix_views_daily', L.FIRM_MIX_VIEWS_DAILY, b, k)
    alias = L.LEGACY.get(L.FIRM_MIX_VIEWS_DAILY)
    if alias and alias != L.FIRM_MIX_VIEWS_DAILY:
        b, k = destination(alias)
        add('firm_mix_views_daily_alias', alias, b, k)
    # platinum/firm/mix_summary.json (D_04)
    b, k = source(FIRM_SUMMARY_LEGACY)
    add('firm_mix_summary', FIRM_SUMMARY_LEGACY, b, k)

    # every advisor mix_daily.json: list the advisors prefix at its destination, keep the mix_daily.json members
    lb, lp, to_legacy = list_target(ADV_PREFIX)
    adv_ids = []
    list_pages = 0
    listed = 0
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=lb, Prefix=lp):
        list_pages += 1
        for o in page.get('Contents', []):
            listed += 1
            lk = to_legacy(o['Key'])
            parts = lk[len(ADV_PREFIX):].split('/')
            if len(parts) == 2 and parts[1] == 'mix_daily.json':
                adv_ids.append(parts[0])
    adv_ids = sorted(set(adv_ids))
    for aid in adv_ids:
        dk = L.advisor_mix_daily_key(aid)
        b, k = destination(dk)
        add('advisor_mix_daily', dk, b, k)
        lk = L.legacy_advisor_mix_daily_key(aid)
        if lk != dk:
            b, k = destination(lk)
            add('advisor_mix_daily_alias', lk, b, k)

    counts = {f: {'keys': len(v), 'present': sum(1 for x in v if keys[x]['present'])} for f, v in families.items()}
    no_vid = sum(1 for v in keys.values() if v['present'] and v['VersionId'] in (None, 'null'))
    doc = {'taken_utc': datetime.now(timezone.utc).isoformat(), 'mode': 'canonical',
           'advisor_prefix_listing': {'bucket': lb, 'prefix': lp, 'pages': list_pages, 'objects_listed': listed},
           'advisor_ids_with_mix_daily': len(adv_ids), 'counts': counts, 'total_keys': len(keys),
           'total_version_pages': total_pages, 'keys_absent': sum(1 for v in keys.values() if not v['present']),
           'keys_with_no_versionid': no_vid, 'keys': keys}
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=1, sort_keys=True)

    # the live body of the mix daily summary, read BY VersionId so body and record agree
    b, k = source(L.MIX_DAILY_SUMMARY)
    rec = keys[f'{b}/{k}']
    resp = s3.get_object(Bucket=b, Key=k, VersionId=rec['VersionId'])
    body = resp['Body'].read()
    with open(body_out, 'wb') as f:
        f.write(body)
    print(f'legp {out}: keys={len(keys)} version_pages={total_pages} absent={doc["keys_absent"]} no_versionid={no_vid}')
    print(f'  advisor listing: {lb}/{lp} pages={list_pages} objects={listed} advisor_ids_with_mix_daily={len(adv_ids)}')
    for fam, c in counts.items():
        print(f'  {fam}: keys={c["keys"]} present={c["present"]}')
    print(f'  mix_daily_summary body: {b}/{k} VersionId={rec["VersionId"]} ETag={rec["ETag"]} bytes={len(body)} '
          f'md5={hashlib.md5(body).hexdigest()} sha256={hashlib.sha256(body).hexdigest()}')
    return 0


def version() -> int:
    s3 = boto3.client('s3')
    b, k = source(L.MIX_DAILY_SUMMARY)
    row, pages = _latest(s3, b, k)
    print(f'{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")} {b}/{k} VersionId={row["VersionId"]} '
          f'ETag={row["ETag"]} LastModified={row["LastModified"]} Size={row["Size"]} pages={pages}')
    return 0


if __name__ == '__main__':
    if sys.argv[1] == 'legp':
        sys.exit(legp(sys.argv[2], sys.argv[3]))
    sys.exit(version())
