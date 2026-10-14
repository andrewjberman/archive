#!/usr/bin/env python3
"""BP-c-2 -- verify every silver/transactions partition against S3 metadata before relying on it. READ-ONLY.

Inputs:
  --listing  <json>  `aws s3api list-objects-v2 --prefix silver/transactions/` (Key, Size, ETag), read verb
  --heads    <tsv>   `aws s3api head-object` per key: key TAB ContentLength TAB ETag TAB rc=N, read verb
  --cache    <dir>   round 2's scratch cache tx_back/ (pre-2026) and tx/ (2026); READ only, never modified
  --fetched  <dir>   this worker's data folder for partitions fetched here (outside the checkout)
Output:
  --out      <csv>   one line per dated partition with the verdict

A local copy is VERIFIED when its byte count equals head-object ContentLength and its MD5 equals the head-object
ETag (single-part uploads). A multipart ETag (a '-' in it) cannot be checked by MD5; it is VERIFIED_SIZE only and
named as such. Anything else is MISMATCH or MISSING and is fetched again by the caller (get-object into --fetched).

Run with python -I at this file's own path. ASCII only.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import sys

KEY_RE = re.compile(r'^silver/transactions/(\d{4}-\d{2}-\d{2})\.parquet$')


def md5_and_size(path):
    h = hashlib.md5()
    n = 0
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


def local_candidates(day, cache, fetched):
    """Where a copy may already sit: round 2's cache first (read), then this worker's fetched folder."""
    sub = 'tx_back' if day < '2026-01-01' else 'tx'
    out = [os.path.join(cache, sub, day + '.parquet')]
    out.append(os.path.join(fetched, 'tx', day + '.parquet'))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--listing', required=True)
    ap.add_argument('--heads', required=True)
    ap.add_argument('--cache', required=True)
    ap.add_argument('--fetched', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    with open(a.listing, encoding='utf-8') as fh:
        listing = {x['K']: x for x in json.load(fh)}
    heads = {}
    with open(a.heads, encoding='utf-8') as fh:
        for line in fh:
            parts = line.rstrip('\n').split('\t')
            if len(parts) != 3:
                raise SystemExit('ERROR: malformed heads line: %r' % line[:120])
            key, meta, rc = parts
            vals = meta.split(' ', 1)
            heads[key] = {'rc': rc, 'len': vals[0] if vals and vals[0] else '', 'etag': vals[1].strip('"') if len(vals) > 1 else ''}

    keys = sorted(k for k in listing if KEY_RE.match(k))
    rows = []
    counts = {}
    for key in keys:
        day = KEY_RE.match(key).group(1)
        h = heads.get(key)
        if h is None or h['rc'] != 'rc=0' or not h['len']:
            verdict, src, lb, lm = 'HEAD_FAILED', '', '', ''
            hl, he = '', ''
            if h:
                hl, he = h['len'], h['etag']
        else:
            hl, he = int(h['len']), h['etag']
            verdict, src, lb, lm = 'MISSING', '', '', ''
            # the first candidate that VERIFIES is used; otherwise the first existing one is reported as the mismatch
            fallback = None
            for cand in local_candidates(day, a.cache, a.fetched):
                if not os.path.isfile(cand):
                    continue
                m, n = md5_and_size(cand)
                if n != hl:
                    v = 'MISMATCH_SIZE'
                elif '-' in he:
                    v = 'VERIFIED_SIZE_MULTIPART'
                elif m == he:
                    v = 'VERIFIED_MD5'
                else:
                    v = 'MISMATCH_MD5'
                if v.startswith('VERIFIED'):
                    verdict, src, lb, lm = v, cand, n, m
                    fallback = None
                    break
                if fallback is None:
                    fallback = (v, cand, n, m)
            if fallback is not None:
                verdict, src, lb, lm = fallback
        counts[verdict] = counts.get(verdict, 0) + 1
        rows.append({'key': key, 'date': day, 'source_path': src.replace('\\', '/'), 'local_bytes': lb,
                     'head_content_length': hl, 'local_md5': lm, 'head_etag': he, 'verdict': verdict,
                     'listing_size': listing[key]['S']})

    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print('PARTITIONS listed=%d dated=%d verdicts=%s' % (len(listing), len(keys), json.dumps(counts, sort_keys=True)))
    bad = [r['key'] for r in rows if r['verdict'] not in ('VERIFIED_MD5', 'VERIFIED_SIZE_MULTIPART')]
    print('PARTITIONS needing fetch or review=%d' % len(bad))
    for k in bad[:20]:
        print('  ' + k)
    return 0


if __name__ == '__main__':
    sys.exit(main())
