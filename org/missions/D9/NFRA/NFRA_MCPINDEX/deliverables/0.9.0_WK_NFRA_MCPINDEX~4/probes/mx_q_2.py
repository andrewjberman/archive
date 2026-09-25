"""MX-q-2 probe -- two READ-ONLY live reads (R-2 (1) Black Diamond null cusip; R-3 Eclipse tenancy).

Worker 0.9.0_WK_NFRA_MCPINDEX~4. Verbs used: s3:ListObjectsV2 (paginated), s3:GetObject. No write verb.
Prints aggregate counts only: no client name, account number or balance.

Usage: python mx_q_2.py BD | ECL
"""
import io
import sys
from datetime import datetime, timezone

import boto3
import pyarrow.compute as pc
import pyarrow.parquet as pq

S3 = boto3.client('s3', region_name='us-east-1')
SINCE = '2026-04-14'
INFLECTION_REP_IDS_SOURCE = 'data/inf/scripts/silver/_orion_api_silver_lib.py'


def now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def keys(bucket, prefix):
    out = []
    for pg in S3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix):
        out.extend(pg.get('Contents', []))
    return out


def read_cols(bucket, key, cols):
    b = S3.get_object(Bucket=bucket, Key=key)['Body'].read()
    pf = pq.ParquetFile(io.BytesIO(b))
    have = [c for c in cols if c in pf.schema_arrow.names]
    return pf.read(columns=have), pf.schema_arrow.names


def null_or_blank(col):
    """Count of null, plus count of blank/'nan'/'None' strings, in an arrow column."""
    n_null = col.null_count
    s = pc.utf8_trim_whitespace(pc.cast(col, 'string'))
    blank = pc.sum(pc.cast(pc.is_in(s, value_set=__import__('pyarrow').array(['', 'nan', 'None', 'NaN'])), 'int64')).as_py() or 0
    return n_null, blank


def bd():
    bucket = 'opal-data-bd'
    t0 = now()
    objs = [o for o in keys(bucket, 'silver/transactions/') if o['Key'].endswith('.parquet')]
    part = sorted(o['Key'] for o in objs if o['Key'].rsplit('/', 1)[1][:10] >= SINCE)
    print(f'INSTRUMENT: ListObjectsV2 s3://{bucket}/silver/transactions/ -> {len(objs)} parquet partitions; '
          f'{len(part)} with filename date >= {SINCE} ({part[0]} .. {part[-1]})')
    rows = nul = blank = cash_null = 0
    for k in part:
        t, _ = read_cols(bucket, k, ['cusip', 'asset_id'])
        rows += t.num_rows
        if 'cusip' not in t.column_names:
            nul += t.num_rows
            continue
        a, b = null_or_blank(t['cusip'])
        nul += a
        blank += b
        if 'asset_id' in t.column_names:
            m = pc.and_(pc.is_null(t['cusip']), pc.equal(pc.cast(t['asset_id'], 'string'), '4'))
            cash_null += pc.sum(pc.cast(m, 'int64')).as_py() or 0
    t1 = now()
    print(f'DENOMINATOR: {len(part)} partitions, {rows} rows; null={nul} blank_string={blank} '
          f'(of the nulls, asset_id=4 cash rows={cash_null}); read {t0}..{t1}')
    print(f'BD-NULL-CUSIP rows={rows} null_cusip={nul + blank} since={SINCE} '
          f'source=s3://{bucket}/silver/transactions/ read_at={t1}')

    # Served figures that join on cusip AND emit a cusip column: latest partition of each.
    figs = [
        ('holdings_lots', 'data/black_diamond/scripts/gold/B_01.holdings_lots.py', 'gold/timeseries/holdings_lots/'),
        ('canonical_lots_unrealized', 'data/black_diamond/scripts/gold/B_02.canonical_lots.py', 'gold/canonical/lots_unrealized/'),
        ('canonical_lots_realized', 'data/black_diamond/scripts/gold/B_02.canonical_lots.py', 'gold/canonical/lots_realized/'),
    ]
    carrying = 0
    for name, producer, pre in figs:
        ks = sorted(o['Key'] for o in keys(bucket, pre)
                    if o['Key'].endswith('.parquet') and o['Key'].rsplit('/', 1)[1][:4].isdigit()
                    and not o['Key'].rsplit('/', 1)[1].startswith('backfill'))
        k = ks[-1]
        t, _ = read_cols(bucket, k, ['cusip'])
        a, b = null_or_blank(t['cusip'])
        carrying += 1 if (a + b) > 0 else 0
        print(f'FIGURE {name} producer={producer} key=s3://{bucket}/{k} (latest of {len(ks)}) '
              f'rows={t.num_rows} null={a} blank_string={b} read_at={now()}')
    print(f'BD-SERVED-CUSIP-JOINS served_figures_checked={len(figs)} carrying_null={carrying}')


def ecl():
    bucket = 'opal-data-inf'
    sys.path.insert(0, 'data/inf/scripts/silver')
    src = open(INFLECTION_REP_IDS_SOURCE, encoding='utf-8').read()
    line = [ln for ln in src.splitlines() if ln.startswith('INFLECTION_REP_IDS =')][0]
    allow = {str(x) for x in eval(line.split('=', 1)[1].split('#')[0])}
    print(f'ALLOWLIST: {INFLECTION_REP_IDS_SOURCE} INFLECTION_REP_IDS={sorted(allow)}')
    objs = keys(bucket, 'silver/eclipse/')
    dates = sorted({o['Key'].split('/')[2] for o in objs if o['Key'].endswith('portfolios_simple.parquet')})
    d = dates[-1]
    print(f'INSTRUMENT: ListObjectsV2 s3://{bucket}/silver/eclipse/ -> {len(objs)} objects, '
          f'{len(dates)} dated partitions; latest {d}')
    simple, snames = read_cols(bucket, f'silver/eclipse/{d}/portfolios_simple.parquet',
                               ['eclipse_account_id_int', 'is_deleted'])
    idcols = [c for c in snames if any(t in c.lower() for t in ('rep', 'firm', 'advisor', 'team'))]
    print(f'portfolios_simple rows={simple.num_rows}; columns naming rep/firm/advisor/team: {idcols}')
    full, fnames = read_cols(bucket, f'silver/eclipse/{d}/portfolios_full.parquet', ['team'])
    print(f'portfolios_full rows={full.num_rows}; columns naming rep/firm/advisor/team: '
          f'{[c for c in fnames if any(t in c.lower() for t in ("rep", "firm", "advisor", "team"))]}; '
          f'distinct team values={len(set(full["team"].to_pylist())) if "team" in full.column_names else "n/a"}')
    # Rep ids via the producer's own sanctioned join (INF_E_00: eclipse_account_id_int -> accounts_v2.account_id).
    av = sorted({o['Key'].split('/')[3] for o in keys(bucket, 'silver/api_dims/accounts_v2/')
                 if o['Key'].endswith('data.parquet')})
    ad = av[-1]
    acc, anames = read_cols(bucket, f'silver/api_dims/accounts_v2/{ad}/data.parquet', ['account_id', 'rep_id'])
    print(f'accounts_v2 {ad} rows={acc.num_rows}; has rep_id={"rep_id" in anames}')
    rep_of = {}
    for a, r in zip(acc['account_id'].to_pylist(), acc['rep_id'].to_pylist()):
        if a is not None:
            rep_of[str(a).split('.')[0]] = None if r in (None, '') else str(r).strip().split('.')[0]
    ids = simple['eclipse_account_id_int'].to_pylist()
    joined = [rep_of[str(i)] for i in ids if i is not None and str(i) in rep_of]
    no_acct = sum(1 for i in ids if i is None)
    unjoined = sum(1 for i in ids if i is not None and str(i) not in rep_of)
    reps = {r for r in joined if r is not None}
    null_rep = sum(1 for r in joined if r is None)
    outside = sorted(r for r in reps if r not in allow)
    rows_outside = sum(1 for r in joined if r is not None and r not in allow)
    t1 = now()
    print(f'DENOMINATOR: {simple.num_rows} portfolios_simple rows; null eclipse_account_id={no_acct}; '
          f'unjoined to accounts_v2={unjoined}; joined={len(joined)} (null rep_id={null_rep}); '
          f'distinct rep_ids={len(reps)}; outside allowlist={len(outside)} ids, {rows_outside} rows')
    print(f'ECLIPSE-SCOPE rows={simple.num_rows} distinct_ids={len(reps)} outside_allowlist={len(outside)} '
          f'allowlist={INFLECTION_REP_IDS_SOURCE} read_at={t1}')


if __name__ == '__main__':
    {'BD': bd, 'ECL': ecl}[sys.argv[1]]()
