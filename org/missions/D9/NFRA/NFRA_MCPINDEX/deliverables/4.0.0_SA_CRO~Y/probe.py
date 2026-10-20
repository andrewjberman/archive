"""Read-only value probes for the advisor-table brief. Prints one labelled line per probe."""
import json
import sys
from collections import Counter
import boto3
import pyarrow.parquet as pq
import pyarrow.fs as pafs

S = sys.argv[1]
t = json.load(open(S + '/census.json', encoding='utf-8'))
by = {(r['bucket'], r['prefix']): r for r in t}
s3 = boto3.client('s3')
fs = pafs.S3FileSystem(region='us-east-1')
CAP = 64 * 1024 * 1024
A, B = 'opal-data-assets', 'opal-data-bd'

READ = [(A, 'orion/inflection/silver/fact_positions/'), (A, 'orion/inflection/silver/fact_transactions/'),
        (A, 'eclipse/inflection/silver/fact_models/'), (A, 'eclipse/inflection/silver/fact_model_composition/'),
        (A, 'smartx/platform/silver/fact_model_allocation_roster/'), (A, 'smartx/platform/silver/fact_allocation_account_map/'),
        (A, 'smartx/platform/silver/fact_allocation_positions/'), (A, 'smartx/platform/silver/fact_allocation_valuation/'),
        (A, 'smartx/platform/silver/fact_model_holdings/'),
        (A, 'schwab/08242234/silver/dim_position/'), (A, 'schwab/08335338/silver/dim_position/'),
        (A, 'schwab/08242234/silver/dim_balance/'), (A, 'schwab/08242234/silver/dim_transaction/'),
        (A, 'blackdiamond/49f/silver/dim_account_xref/'), (B, 'silver/unrealized/'), (B, 'silver/transactions/'),
        (B, 'silver/fees/'), (B, 'silver/allocations/'), (A, 'blackdiamond/49f/silver/fact_bd_allocation/'),
        (A, 'blackdiamond/cottonwood/silver/fact_allocations/'), (A, 'blackdiamond/cottonwood/silver/fact_holdings/'),
        (A, 'blackdiamond/cottonwood/silver/fact_transactions/'), (A, 'blackdiamond/cottonwood/silver/fact_model_assignment/'),
        (A, 'commonwealth/cottonwood/silver/crosswalk/'), (A, 'commonwealth/cottonwood/silver/positions/'),
        (A, 'commonwealth/cottonwood/silver/account_day_value/'), (A, 'commonwealth/cottonwood/silver/transactions/')]
print('== SIZE vs 64 MiB object cap (newest partition key)')
for b, p in READ:
    k = by[(b, p)]['schema_key']
    n = s3.head_object(Bucket=b, Key=k)['ContentLength']
    print('%-8s %10.1f MiB  %s/%s' % ('OVER-CAP' if n > CAP else 'ok', n / 1048576, b, k))


def read(b, key, cols=None):
    with fs.open_input_file('%s/%s' % (b, key)) as f:
        return pq.read_table(f, columns=cols).to_pylist()


def key(b, p):
    return by[(b, p)]['schema_key']

# SmartX: the by-name firm fence against the gateway roster
roster_doc = json.load(open(sys.argv[2], encoding='utf-8'))
names = {}
for pt in roster_doc.get('partners', []):
    for nm in (pt.get('aliases') or {}).get('advisor_name') or []:
        names[nm] = pt.get('firm_id')
rows = read(A, key(A, 'smartx/platform/silver/fact_model_allocation_roster/'), ['advisor_id', 'advisor_name', 'allocation_id'])
c = Counter(names.get(r['advisor_name'], '<not in roster>') for r in rows)
print('== SMARTX roster rows by mapped firm (denominator %d rows, %d distinct advisor_name; roster map %d names):' % (
    len(rows), len({r['advisor_name'] for r in rows}), len(names)), dict(c.most_common(8)))

# BD 49F: resolve bridge (dim_account_xref) coverage of the live unrealized account ids
xr = read(A, key(A, 'blackdiamond/49f/silver/dim_account_xref/'), ['bd_account_id'])
xids = {str(r['bd_account_id']) for r in xr}
un = read(B, key(B, 'silver/unrealized/'), ['account_id'])
uids = Counter(str(r['account_id'])[:3] for r in un)
live = {str(r['account_id']) for r in un if str(r['account_id']).startswith('z08')}
print('== BD49F live unrealized account-id prefixes (rows %d):' % len(un), dict(uids.most_common(5)))
print('== BD49F z08 accounts in live unrealized: %d; present in xref %s: %d; absent: %d' % (
    len(live), by[(A, 'blackdiamond/49f/silver/dim_account_xref/')]['newest_partition'], len(live & xids), len(live - xids)))

# BD Cottonwood: model assignment join (account_number) against fact_allocations Account Number
al = read(A, key(A, 'blackdiamond/cottonwood/silver/fact_allocations/'), ['AccountID', 'Account Number'])
nums = {str(r['Account Number']) for r in al if r['Account Number'] not in (None, '')}
ma = read(A, key(A, 'blackdiamond/cottonwood/silver/fact_model_assignment/'), ['account_number', 'strategy_name'])
man = {str(r['account_number']) for r in ma}
print('== BDCW alloc accounts %d; assignment accounts %d; joined %d' % (len(nums), len(man), len(nums & man)))
mr = read(A, key(A, 'blackdiamond/cottonwood/silver/fact_model_roster/'), ['model_name'])
rn = {r['model_name'] for r in mr}
strat = Counter(r['strategy_name'] in rn for r in ma if r['strategy_name'])
print('== BDCW assignment strategy_name found in roster model_name: %s (of %d with a strategy)' % (dict(strat), sum(strat.values())))

# Orion: transaction status values, fee-description rows, custodianName
tx = read(A, key(A, 'orion/inflection/silver/fact_transactions/'), ['status', 'transactionDescription', 'custodianName'])
print('== ORION tx rows %d; status:' % len(tx), dict(Counter(r['status'] for r in tx).most_common(6)))
fee = Counter(r['transactionDescription'] for r in tx if 'fee' in str(r['transactionDescription'] or '').lower())
print('== ORION tx descriptions containing fee:', dict(fee.most_common(10)))
print('== ORION tx custodianName:', dict(Counter(r['custodianName'] for r in tx).most_common(6)))
pos = read(A, key(A, 'orion/inflection/silver/fact_positions/'), ['custodian'])
print('== ORION positions custodian:', dict(Counter(r['custodian'] for r in pos).most_common(6)))

# Commonwealth: any fee-like transaction types
cw = read(A, key(A, 'commonwealth/cottonwood/silver/transactions/'), ['Transaction_Type', 'Transaction_Description'])
print('== CW tx types (rows %d):' % len(cw), dict(Counter(r['Transaction_Type'] for r in cw).most_common(12)))
print('== CW fee-like descriptions:', dict(Counter(r['Transaction_Description'] for r in cw if 'fee' in str(r['Transaction_Description'] or '').lower()).most_common(6)))

# Schwab: fee-like transaction categories in dim_transaction (one partition, 08242234)
st = read(A, key(A, 'schwab/08242234/silver/dim_transaction/'), ['tr_cd', 'transaction_category'])
print('== SCHWAB dim_transaction categories (rows %d):' % len(st), dict(Counter(r['transaction_category'] for r in st).most_common(10)))

# Eclipse: the account-to-model bridge in fact_portfolios_simple
ps = by[(A, 'eclipse/inflection/silver/fact_portfolios_simple/')]['columns']
print('== ECLIPSE fact_portfolios_simple columns:', [c.split(':')[0] for c in ps])
