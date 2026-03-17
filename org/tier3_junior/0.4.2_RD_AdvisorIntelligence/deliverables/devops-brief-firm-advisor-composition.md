# DevOps Brief: Firm & Advisor Composition Endpoints

**From:** 0.4.2_RD_AdvisorIntelligence
**To:** 0.4.0_DS_ClientPlatform (Lambda code), 0.4.0_DT_ClientPlatform (deploy)
**Date:** 2026-03-17
**Priority:** High -- frontend is wired and falling back to synthesized data until these endpoints go live

---

## What the Frontend Expects

The Books Tab canonical view calls composition at every drill level. L3 (relationship) and L4 (account) already work. N1 (firm) and L2 (advisor) currently fall back to synthesized portfolio data that has **no real top holdings concentration** and uses buy-activity-derived allocation instead of live position data.

The frontend calls these endpoints via `fetchComposition()` in `ClientsTab.tsx`:

| Level | Endpoint | Status |
|-------|----------|--------|
| N1 (Firm) | `GET /api/scoped/partners/books/firm/all/composition?firmId=49financial` | **PENDING** |
| L2 (Advisor) | `GET /api/scoped/partners/books/advisor/{advisor_id}/composition?firmId=49financial` | **PENDING** |
| L3 (Relationship) | `GET /api/scoped/partners/books/relationship/{id}/composition?firmId=49financial` | Live (partners-api-v1.1.0) |
| L4 (Account) | `GET /api/scoped/partners/books/account/{id}/composition?firmId=49financial` | Live (partners-api-v1.1.0) |

The frontend returns the same `BooksCompositionResponse` shape at every level:
```json
{
  "generated_at": "...",
  "data_as_of": "2026-03-16",
  "scope": { "firm_id": "49financial" },
  "mix": [
    { "asset_class": "equity", "label": "Equities", "market_value": 1234567.89, "pct": 45.2 }
  ],
  "concentration": {
    "top_n": 10,
    "items": [
      { "key": "AAPL", "label": "AAPL", "asset_class": "equity", "market_value": 500000, "pct": 12.3 }
    ],
    "other": { "market_value": 200000, "pct": 5.1 }
  },
  "unclassified": { "count": 3, "market_value": 15000 }
}
```

When the endpoint returns non-200, the frontend silently falls back to synthesized data. **No portal changes needed once the Lambda is deployed.**

---

## Lambda Changes Required

**File:** `infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py`

### Change 1: Router — accept `firm` and `advisor` entity types (line ~1122)

```python
# BEFORE:
if entity_type not in ('relationship', 'account'):
    return cors_response(400, {'error': f'Invalid entity type: {entity_type}'})

# AFTER:
if entity_type not in ('relationship', 'account', 'firm', 'advisor'):
    return cors_response(400, {'error': f'Invalid entity type: {entity_type}'})
```

### Change 2: `handle_books_composition` — firm scope (line ~841)

The function already reads `holdings_lots/{date}.parquet` and classifies every holding. For firm scope, just skip the entity filter — all data in the bucket belongs to that firm.

```python
# BEFORE:
filter_col = 'relationship_id' if entity_type == 'relationship' else 'account_id'
...
df = df[(df[filter_col] == entity_id) & (df['is_open'].fillna(False) == True)]

# AFTER:
if entity_type == 'firm':
    # Firm scope: aggregate ALL open holdings in this firm's bucket
    df = df[df['is_open'].fillna(False) == True]
else:
    filter_col = {
        'relationship': 'relationship_id',
        'account': 'account_id',
    }.get(entity_type)
    if filter_col:
        df = df[(df[filter_col] == entity_id) & (df['is_open'].fillna(False) == True)]
```

The rest of `handle_books_composition` (AP gate, classify, mix aggregation, concentration top-10) works unchanged.

### Change 3: `handle_books_composition` — advisor scope (line ~841)

Advisor scope requires joining with `accounts_dimension` to get the architect mapping. The `holdings_lots` parquet has `relationship_id` but not `architect`.

```python
elif entity_type == 'advisor':
    # Join with accounts_dimension to get architect -> relationship mapping
    dim_key = 'gold/accounts_dimension_latest.parquet'
    dim_df = wr.s3.read_parquet(
        path=f's3://{bucket}/{dim_key}',
        columns=['relationship_id', 'architect'],
        dtype_backend='numpy',
    )
    # Map advisor_id back to architect name (reverse of _advisor_id())
    advisor_relationships = dim_df[
        dim_df['architect'].str.lower().str.strip()
        .str.replace(r'[^a-z0-9_]+', '_', regex=True)
        .str.strip('_') == entity_id
    ]['relationship_id'].unique()
    df = df[
        (df['relationship_id'].isin(advisor_relationships)) &
        (df['is_open'].fillna(False) == True)
    ]
```

**Alternative (simpler):** If advisor scope is too complex for the first pass, skip it. The firm-level endpoint alone is high value — it gives real mix + real top-10 holdings for the N1 Firm Dashboard. L2 advisor can stay on synthesized data until a second pass.

### Change 4: Scope field in response (line ~940)

```python
'scope': {f'{entity_type}_id': entity_id},
# firm -> {"firm_id": "all"}, advisor -> {"advisor_id": "travis_penfield"}
```

Already works as-is with the existing string interpolation.

---

## Data Source

- **Parquet:** `s3://opal-data-bd/gold/holdings_lots/{YYYY-MM-DD}.parquet`
- **Produced by:** `03_build_holdings_lots.py` (runs nightly via bd-gold-layer-runner)
- **Columns used:** `account_id`, `relationship_id`, `ticker`, `asset_name`, `market_value`, `is_open`
- **For advisor scope:** `s3://opal-data-bd/gold/accounts_dimension_latest.parquet` (column: `architect`)

The holdings data is refreshed nightly by the gold layer runner. The latest snapshot is found by `_find_latest_holdings_lots()` which already exists in the Lambda.

---

## Deploy Sequence

1. DS: Modify `lambda_function.py` per changes 1-3 above
2. DS: Commit to CLOUD
3. DT: `build-and-upload.sh partners-api opal-partners-data`
4. DT: `terraform plan` -> `terraform apply` (partners-api module)
5. DT: Verify 0-diff, tag `partners-api-v1.2.0`
6. DT: Test: `aws lambda invoke --function-name opal-partners-data --payload '{"path":"/api/scoped/partners/books/firm/all/composition","queryStringParameters":{"firmId":"49financial"},"httpMethod":"GET"}'`
7. Verify in browser: Books Tab N1 should show real top-10 holdings in concentration pie

---

## Verification

After deploy, the frontend will automatically pick up real data (no portal changes needed):
- N1: Both mix pie AND concentration pie should populate with live position-based data
- L2: If advisor scope deployed, same behavior for advisor drill
- L3/L4: Unchanged (already working)

To confirm the fallback is no longer needed, check browser DevTools Network tab:
- `GET /api/scoped/partners/books/firm/all/composition?firmId=49financial` should return 200
- Response should have `concentration.items` with real tickers (AAPL, SPY, etc.), not empty
