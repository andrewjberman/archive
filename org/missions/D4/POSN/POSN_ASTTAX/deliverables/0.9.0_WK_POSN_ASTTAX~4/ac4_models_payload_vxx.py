"""S7-AC4 -- is VXX a CURRENT HOLDING, read from the MODELS PAYLOAD itself.

Instrument: the model PKL the positioning generator actually loads
(yang-generate-positioning/lambda_function.py:2069 s3_key_model, :2088 get_object,
:1816 model_pkl_data.get('holdings')).  NOT the DT brief, NOT the DynamoDB registry.

Prints the artifact, its vintage, the denominator it drew from, and the verdict.
Read-only.
"""
import pickle
import sys

ARTIFACT = '.scratch/model_20260910_v1.pkl'
S3_URI = 's3://opal-data-portal-v2/benchmarks/model_20260910_v1.pkl'
VINTAGE = 'LastModified 2026-09-11T11:04:19+00:00 UTC (s3api), ContentLength 17682489, ETag aa2e619e77d85ffa5a1a8fc9f56112ee'
TARGET = 'VXX'
# The seven served `hedge` tickers AT2-s-2 would retag, plus VXX.
RETAG_SET = ['DBC', 'GLD', 'GSG', 'IAU', 'SLV', 'USO', 'VIXY', 'VXX']

print('S7-AC4 -- MODELS PAYLOAD READ')
print('ARTIFACT   : %s' % S3_URI)
print('LOCAL COPY : %s' % ARTIFACT)
print('VINTAGE    : %s' % VINTAGE)
print('SELECTED   : newest of 87 objects under benchmarks/model_ (client-side count,')
print('             auto-paginated list-objects-v2, sorted by LastModified)')
print('')

with open(ARTIFACT, 'rb') as fh:
    payload = pickle.load(fh)

print('PAYLOAD TOP-LEVEL KEYS (denominator %d):' % len(payload))
for k in sorted(payload):
    v = payload[k]
    shape = getattr(v, 'shape', None)
    print('  %-28s %-22s %s' % (k, type(v).__name__, shape if shape is not None else ''))
print('')

holdings = payload.get('holdings')
if holdings is None:
    print('ERROR: no holdings frame in the payload -- AC4 cannot be answered from it')
    sys.exit(1)

print('HOLDINGS FRAME  : %d row(s) x %d column(s)' % holdings.shape)
print('HOLDINGS COLUMNS: %s' % list(holdings.columns))
print('')

# --- the model axis -------------------------------------------------------
model_col = 'model' if 'model' in holdings.columns else None
if model_col:
    models = sorted(str(m) for m in holdings[model_col].dropna().unique())
    print('MODEL CODES PRESENT IN THE PAYLOAD (denominator %d): %s' % (len(models), models))
print('')

# --- the ticker denominator ----------------------------------------------
tick_col = 'ticker' if 'ticker' in holdings.columns else holdings.columns[0]
tickers_raw = [str(t) for t in holdings[tick_col].dropna().tolist()]
uniq = sorted(set(tickers_raw))
print('TICKER DENOMINATOR: %d holding row(s), %d UNIQUE ticker(s) in column %r'
      % (len(tickers_raw), len(uniq), tick_col))
print('')
print('FULL UNIQUE TICKER LIST (all %d, not a page):' % len(uniq))
for i in range(0, len(uniq), 10):
    print('  ' + ' '.join('%-6s' % t for t in uniq[i:i + 10]))
print('')

# --- the verdict ----------------------------------------------------------
# Case-insensitive + whitespace-stripped: a case-sensitive census misses the
# emphatic spellings, and an absence verdict must survive that.
norm = {}
for t in tickers_raw:
    norm.setdefault(t.strip().upper(), 0)
    norm[t.strip().upper()] += 1

print('RETAG-SET HELD STATUS (AT2-s-2 would move each of these):')
print('  %-8s %-10s %s' % ('TICKER', 'HELD?', 'ROWS IN THE MODELS PAYLOAD'))
for t in RETAG_SET:
    n = norm.get(t, 0)
    print('  %-8s %-10s %d' % (t, 'HELD' if n else 'NOT-HELD', n))
print('')

n_vxx = norm.get(TARGET, 0)
print('POSITIVE CONTROL: an unambiguously held ticker must read HELD --')
for ctrl in uniq[:1]:
    print('  %-8s rows=%d  (drawn from the same frame; if this read 0 the instrument is broken)'
          % (ctrl, norm.get(ctrl.strip().upper(), 0)))
print('NEGATIVE CONTROL: a ticker that cannot be held --')
print('  %-8s rows=%d  (must read 0)' % ('ZZZZNOPE', norm.get('ZZZZNOPE', 0)))
print('')

if n_vxx:
    rows = holdings[holdings[tick_col].astype(str).str.strip().str.upper() == TARGET]
    print('VERDICT: %s IS A CURRENT HOLDING -- %d row(s) in the models payload' % (TARGET, n_vxx))
    print(rows.to_string())
else:
    print('VERDICT: %s IS *NOT* A CURRENT HOLDING in this models payload.' % TARGET)
    print('         %d unique tickers scanned, case-insensitive, whole-value. Not a page.' % len(uniq))
print('')
# --- THE DECISIVE SLICE ---------------------------------------------------
# "current holding" is not "appears anywhere in the frame". The generator takes
# the LATEST DATE PER MODEL (extract_current_holdings, lambda_function.py:1396-1401:
#   model_dates = sorted(model_df['date'].unique()); model_latest_date = model_dates[-1]
# ). Mirrored here exactly -- that slice IS what reaches positioning_data.json.
MODEL_CODES = ['UST', 'ST', 'INT', 'LT', 'ULT']
print('CURRENT-SLICE READ (mirrors extract_current_holdings: latest date PER MODEL)')
print('  %-6s %-12s %-9s %-10s %s' % ('MODEL', 'LATEST DATE', 'HOLDINGS', 'VXX?', 'VXX WEIGHT'))
held_models = []
current_tickers = set()
for mc in MODEL_CODES:
    mdf = holdings[holdings['model'] == mc]
    if mdf.empty:
        print('  %-6s %-12s %-9s %-10s %s' % (mc, 'NO DATA', '-', '-', '-'))
        continue
    latest = sorted(mdf['date'].unique())[-1]
    slice_ = mdf[mdf['date'] == latest]
    slice_ticks = set(str(t).strip().upper() for t in slice_['ticker'])
    current_tickers |= slice_ticks
    hit = slice_[slice_['ticker'].astype(str).str.strip().str.upper() == TARGET]
    has = len(hit) > 0
    if has:
        held_models.append(mc)
    print('  %-6s %-12s %-9d %-10s %s' % (
        mc, str(latest)[:10], len(slice_), 'YES' if has else 'no',
        ('%.4f' % float(hit['weight'].iloc[0])) if has else '-'))
print('')
print('CURRENT-SLICE TICKER DENOMINATOR: %d unique ticker(s) across the 5 model slices'
      % len(current_tickers))
print('CURRENT-SLICE TICKERS (all, not a page):')
cl = sorted(current_tickers)
for i in range(0, len(cl), 10):
    print('  ' + ' '.join('%-6s' % t for t in cl[i:i + 10]))
print('')
print('RETAG-SET STATUS IN THE CURRENT SLICE (this is the live-impact set):')
for t in RETAG_SET:
    print('  %-8s %s' % (t, 'HELD NOW' if t in current_tickers else 'not in current slice'))
print('')
if held_models:
    print('AC4 VERDICT: %s IS A CURRENT HOLDING -- present in the CURRENT slice of model(s) %s.'
          % (TARGET, ', '.join(held_models)))
    print('             Retagging %s equity -> Structured is LIVE-IMPACTING on the next generator run.'
          % TARGET)
else:
    print('AC4 VERDICT: %s appears in the frame historically but is NOT in any current' % TARGET)
    print('             per-model slice -- the exposure is LATENT, not live.')
print('')
print('SCOPE QUALIFIER: this payload carries the FIVE CORE models the positioning')
print('generator iterates (MODEL_CODES = UST, ST, INT, LT, ULT at lambda_function.py:197).')
print('The DT brief asserts VXX flows into SATELLITES 70/80/90/98 -- a DIFFERENT model')
print('axis. Whether the satellite payload holds VXX is stated separately below from')
print('what THIS artifact can and cannot see.')
