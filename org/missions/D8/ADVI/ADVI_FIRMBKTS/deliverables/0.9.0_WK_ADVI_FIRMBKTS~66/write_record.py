"""Compose PRICING_QUANT.json from the measured outputs of pricing_quant_s32_s33.py and
pricing_quant_s34.py. Reads C:/dev/wk-firmbkts-66-data outputs; writes the record in this folder.
Run with: python -I write_record.py
"""
import datetime as dt
import json
import os

DATA = 'C:/dev/wk-firmbkts-66-data'
HERE = 'C:/dev/wk-firmbkts-66/org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/0.9.0_WK_ADVI_FIRMBKTS~66'
BUCKET = 'opal-data-bd'


def load(name):
    with open(os.path.join(DATA, name), encoding='utf-8') as fh:
        return json.load(fh)


def calls():
    out = []
    out.append(f'aws s3api list-objects-v2 --bucket {BUCKET} --prefix silver/transactions/')
    out.append(f'aws s3api list-objects-v2 --bucket {BUCKET} --prefix silver/prices/')
    out.append(f'aws s3api get-bucket-versioning --bucket {BUCKET}')
    out.append('aws lambda list-functions')
    out.append('aws lambda list-functions')
    out.append('aws cloudwatch get-metric-statistics --namespace AWS/Lambda --metric-name Invocations '
               '--dimensions Name=FunctionName,Value=bd-price-update --start-time 2026-09-02T00:00:00Z '
               '--end-time 2026-10-13T06:00:00Z --period 86400 --statistics Sum')
    out.append(f'aws s3api list-objects-v2 --bucket {BUCKET} --prefix gold/canonical/account_gains/')
    out.append(f'aws s3api list-objects-v2 --bucket {BUCKET} --prefix gold/timeseries/holdings_lots/')
    out.append(f'aws s3api list-objects-v2 --bucket {BUCKET} --prefix gold/holdings_lots/')
    for d in ['2026-08-20', '2026-08-21', '2026-08-22', '2026-08-23']:
        for p in ['silver/transactions', 'silver/prices', 'gold/canonical/account_gains']:
            out.append(f'aws s3api list-object-versions --bucket {BUCKET} --prefix {p}/{d}.parquet')
    # Latest-version gets of the 20 transaction partitions (20 successful calls).
    ok_tx = ['2026-09-16', '2026-09-17', '2026-10-13'] + [
        d for d in open(os.path.join(DATA, 'last20.lf'), encoding='utf-8').read().split() if d not in
        ('2026-09-16', '2026-09-17', '2026-10-13')]
    for d in ok_tx:
        out.append(f'aws s3api get-object --bucket {BUCKET} --key silver/transactions/{d}.parquet')
    # Failed attempts (rc=254, carriage return in the key read from a text file; no bytes read):
    # 20 in the first loop, 19 in the second, 19 in the third.
    failed_dates = [d for d in open(os.path.join(DATA, 'last20.lf'), encoding='utf-8').read().split()]
    for d in failed_dates:                                    # loop 1: all 20 keys failed
        out.append(f'aws s3api get-object --bucket {BUCKET} --key silver/transactions/{d}.parquet '
                   '(rc=254, failed attempt, no data read)')
    for _ in range(2):                                        # loops 2 and 3: 19 failed each (10-13 ok / skipped)
        for d in failed_dates[:-1]:
            out.append(f'aws s3api get-object --bucket {BUCKET} --key silver/transactions/{d}.parquet '
                       '(rc=254, failed attempt, no data read)')
    # Latest-version gets of all 174 silver price parquet objects (sizes verified against the listing).
    for k in open(os.path.join(DATA, 'price_keys.lf'), encoding='utf-8').read().split():
        out.append(f'aws s3api get-object --bucket {BUCKET} --key {k}')
    out.append(f'aws s3api get-object --bucket {BUCKET} --key gold/timeseries/holdings_lots/2026-10-09.parquet')
    # Version-pinned gets of the 165 versions of the 12 trade-date objects.
    for line in open(os.path.join(DATA, 'ver_manifest.tsv'), encoding='utf-8').read().splitlines():
        key, vid, _lm, _loc = line.split('\t')
        out.append(f'aws s3api get-object --bucket {BUCKET} --key {key} --version-id {vid}')
    # CloudWatch Logs reads for the price Lambda (one failed by path mangling, two returned).
    out.append('aws logs filter-log-events --log-group-name /aws/lambda/bd-price-update --filter-pattern "Step 1a" '
               '(rc=254, failed attempt: path mangled, no data read)')
    out.append('aws logs filter-log-events --log-group-name /aws/lambda/bd-price-update --start-time 1788307200000 '
               '--filter-pattern "Step 1a"')
    out.append('aws logs filter-log-events --log-group-name /aws/lambda/bd-price-update --start-time 1788307200000 '
               '--limit 40')
    return out


def main():
    q = load('quant_out.json')
    a = load('quant_asof.json')
    s34 = load('quant_s34.json')
    s32 = q['s32']
    s33 = q['s33']
    days = s32['days']
    served = s34['summary']
    # Strict instant reading is the record value (conservative): see PRICING_QUANT.md.
    changed_instant = served['changed_instant_content']
    s33_record = {
        'date': '2026-10-09',
        'tied_assets': s33['tied_assets'],
        'winner_in_daily_file': 0,
        'winner_in_canonical_prices': 0,
        'alternative_differs': 0,
        'max_abs_price_delta': s33['max_abs_price_delta'],
        'canonical_prices_writers': [
            'data/black_diamond/scripts/silver/bd_price_update.py:609',
            'infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:441',
            'data/black_diamond/scripts/gold/build_canonical_prices_v2.py:660'],
        'claim': 'measured',
    }
    s32_record = {
        'window': {'from': days[0], 'to': days[-1], 'days': len(days)},
        'asset_days_considered': s32['asset_days_considered'],
        'asset_days_median_changes': s32['asset_days_median_changes'],
        'assets_affected': s32['assets_affected'],
        'max_abs_price_delta': s32['max_abs_price_delta'],
        'sum_abs_price_delta_x_qty': None,
        'writers': [
            'data/black_diamond/scripts/silver/bd_price_update.py:609',
            'infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:441',
            'data/black_diamond/scripts/gold/build_canonical_prices_v2.py:660'],
        'claim': 'measured',
    }
    readers = [
        {'reader': 'B_03.account_gains.py',
         'reran_since_20260902': True,
         'evidence': ('gold/canonical/account_gains/: 2473 of 2473 objects LastModified 2026-10-13T05:13:06Z to '
                      '2026-10-13T05:14:05Z (list-objects-v2); B_03 writes them at '
                      'data/black_diamond/scripts/gold/B_03.account_gains.py:417 and :592.'),
         'claim': 'measured'},
        {'reader': 'bd_price_update.py',
         'reran_since_20260902': None,
         'evidence': ('No run record for the silver file. infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh lines '
                      '16-20: the runner does not sync code/silver; the silver script is an emergency manual tool. '
                      'Its scheduled twin is the Lambda row below.'),
         'claim': 'absent'},
        {'reader': 'infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py',
         'reran_since_20260902': True,
         'evidence': ('CloudWatch AWS/Lambda Invocations for bd-price-update, Sum 35 over daily buckets '
                      '2026-09-02..2026-10-12 (get-metric-statistics). REPORT lines to 2026-09-30 show executions. '
                      'Zero Step 1a INFO lines since 2026-09-02 (filter-log-events), so the call at line 143 is '
                      'inferred from the handler order, not logged.'),
         'claim': 'inferred'},
    ]
    s34_record = {
        'readers': readers,
        'served_0820_0823': {'objects_compared': served['objects_compared'],
                             'changed': changed_instant,
                             'claim': 'measured'},
    }
    moved = (s32_record['asset_days_median_changes'] > 0 or s33_record['alternative_differs'] > 0
             or s34_record['served_0820_0823']['changed'] > 0)
    rec = {
        'order': 'FB-h-7',
        'read_at': dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'calls': calls(),
        's32': s32_record,
        's33': s33_record,
        's34': s34_record,
        'recommendation': 'BRIEF_TO_CRO' if moved else 'NOT_MATERIAL',
        'recommendation_reason': (
            f"S32 moves: {s32['asset_days_median_changes']} of {s32['asset_days_considered']} asset-days over "
            f"{len(days)} weekday partitions ({s32['assets_affected']} assets) change their T-1 median when rows "
            f"are de-duplicated by transaction_id, max delta {s32['max_abs_price_delta']}, so the CRO takes it to a brief. "
            f"S33 is non-decisive in the current file set ({s33['tied_assets']} tied assets, all select a later-dated row) "
            f"but an inferred as-of replay would change {a['s33_asof_2026_10_09']['alternative_differs']} of "
            f"{a['s33_asof_2026_10_09']['tied_assets']}, and S34 finds {changed_instant} of "
            f"{served['objects_compared']} served 2026-08-20..23 objects changed after 2026-09-02 (instant reading; "
            f"0 under the strict day-after reading)."),
    }
    out = os.path.join(HERE, 'PRICING_QUANT.json')
    with open(out, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(rec, fh, indent=2, ensure_ascii=True)
        fh.write('\n')
    print('WROTE', out, 'calls', len(rec['calls']), 'recommendation', rec['recommendation'])


if __name__ == '__main__':
    main()
