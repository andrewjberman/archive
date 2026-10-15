"""Branch 1 reads for leg Q' (MDPF_SECCLASS TO-SC-e102b, 0.7.0_AE_CloudOps~SC1). Read-only except `restore`.

  python -I e102_branch1.py read <pre_body.json> <before_snap.json> <after_snap.json> [<prev_run_etag>]
      the mix daily summary at its latest version: (1) parsed EQUAL to <pre_body.json> (canonical-JSON equality, XA-20261014T113939Z-a304);
      (2) md5(body) == md5(json.dumps(json.loads(body), sort_keys=True, separators=(',', ':')));
      (3) every OTHER key of the snapshot pair: same key set, every ETag equal (a new VersionId with an equal ETag is reported, not a delta);
      (4) optional: ETag equals <prev_run_etag> (byte determinism, run 2).
  python -I e102_branch1.py restore <VersionId>
      copy-object the mix daily summary's <VersionId> back onto the key (the same-session restore of branch (d)).
"""
from __future__ import annotations

import hashlib
import json
import sys

import boto3

B49 = 'opal-data-49financial'
KEY = 'advi/49financial/platinum/views/mix_daily_summary.json'
SNAPKEY = f'{B49}/{KEY}'


def canon(o) -> str:
    return json.dumps(o, sort_keys=True, separators=(',', ':'))


def read(pre_body: str, bsnap: str, asnap: str, prev_etag: str = '') -> int:
    s3 = boto3.client('s3')
    head = s3.head_object(Bucket=B49, Key=KEY)
    vid, etag = head['VersionId'], head['ETag'].strip('"')
    body = s3.get_object(Bucket=B49, Key=KEY, VersionId=vid)['Body'].read()
    pre = open(pre_body, 'rb').read()
    pj, nj = json.loads(pre), json.loads(body)
    parsed_equal = canon(pj) == canon(nj)
    top_pre = sorted(pj) if isinstance(pj, dict) else []
    top_new = sorted(nj) if isinstance(nj, dict) else []
    sorted_md5 = hashlib.md5(canon(nj).encode('utf-8')).hexdigest()
    body_md5 = hashlib.md5(body).hexdigest()
    sorted_bytes = sorted_md5 == body_md5
    print(f'mix daily summary now: VersionId={vid} ETag={etag} bytes={len(body)} (pre bytes={len(pre)} pre md5={hashlib.md5(pre).hexdigest()})')
    print(f'  PARSED-EQUAL to pre body: {parsed_equal}  (top-level keys pre={top_pre} now={top_new})')
    print(f'  SORTED-BYTES: body md5 {body_md5} vs sorted-dump md5 {sorted_md5} -> {sorted_bytes}')
    B = json.load(open(bsnap, encoding='utf-8'))['keys']
    A = json.load(open(asnap, encoding='utf-8'))['keys']
    only_b = sorted(set(B) - set(A))
    only_a = sorted(set(A) - set(B))
    both = sorted(set(A) & set(B))
    others = [k for k in both if k != SNAPKEY]
    etag_diff = [k for k in others if A[k]['ETag'] != B[k]['ETag']]
    newver = [k for k in others if A[k]['ETag'] == B[k]['ETag'] and A[k]['VersionId'] != B[k]['VersionId']]
    print(f'  OTHER KEYS: before={len(B)} after={len(A)} common={len(both)} only_before={len(only_b)} only_after={len(only_a)} '
          f'ETAG_DIFFERS(excluding the mix daily summary)={len(etag_diff)} NEW_VERSION_EQUAL_ETAG={len(newver)}')
    for k in newver[:10]:
        print('    NEWVER-SAME-ETAG', k.split('/')[-1] if '/entities/' in k else k)
    for k in etag_diff[:10]:
        print('    ETAG-DIFF', k)
    mds_in_snap_before = B.get(SNAPKEY, {}).get('ETag')
    mds_in_snap_after = A.get(SNAPKEY, {}).get('ETag')
    print(f'  mix daily summary ETag in snapshots: before={mds_in_snap_before} after={mds_in_snap_after}')
    if prev_etag:
        print(f'  DETERMINISM: ETag {etag} vs previous run {prev_etag} -> {etag == prev_etag}')
    ok_content = parsed_equal and not etag_diff and not only_b and not only_a
    print('BRANCH1-CONTENT ' + ('OK' if ok_content else 'STOP (restore the mix daily summary to the VersionId read before the run)')
          + f' sorted_bytes={sorted_bytes}' + (f' deterministic={etag == prev_etag}' if prev_etag else ''))
    return 0 if ok_content else 1


def restore(vid: str) -> int:
    s3 = boto3.client('s3')
    r = s3.copy_object(Bucket=B49, Key=KEY, CopySource={'Bucket': B49, 'Key': KEY, 'VersionId': vid}, MetadataDirective='COPY')
    print(f'restored {KEY} from {vid}: new VersionId={r.get("VersionId")} ETag={r["CopyObjectResult"]["ETag"]}')
    return 0


if __name__ == '__main__':
    if sys.argv[1] == 'read':
        sys.exit(read(*sys.argv[2:6]))
    sys.exit(restore(sys.argv[2]))
