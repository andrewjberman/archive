The specification of the gateway tool over the canonical security-classification table, and of the one grant it needs. Facts are from W/ETF_CLASS_CENSUS.json (measured 2026-10-16T04:41Z); the tool name and its proposed inputs are from the CRO's G4 spec section 3.3 (read at HEAD, not checked out in this worktree); the key forms are from org/standards/MDPF_SECCLASS_CONTRACT.json.

## Tool

The tool is `mdpf_get_security_classification`, the third proposed tool of the CRO's G4 spec. It answers one security's classification row from the DynamoDB table `etf-classifications` (us-east-1), by its ticker key.

Inputs: `ticker`, a string, the table's hash key as the contract writes it: an exchange ticker, a `CUSIP:<9 chars>` key, a `BBG:<ticker>:<exch>` key, or a `NAME::<slug>` key. The G4 inputs `firm`, `account_last4` and `platform` are `n/a` for this market-data table and are not accepted. `as_of` is accepted only as `latest`, the one value the table holds.

Read path: one `GetItem` by `Key = {ticker: <ticker>}`, no `Query`, no `Scan`, no index. The table key is the full hash key, so no index is needed.

Envelope: `as_of` is the row's own `last_updated` date (the object's own date, never the read time). `source_keys` names the table and the ticker key read. `denominator` is `{"rows": 1}` when the row is found and `{"rows": 0}` when it is not. `absent_reason` is set when no row exists for the ticker. The body carries the row fields the contract names: `asset_class`, `sub_asset_class`, `classified_by`, `classification_confidence`, `low_confidence`, `identifier_namespace`, `last_updated`. A row with no `classified_by` reads `legacy`; a row with no `identifier_namespace` reads `TICKER`; `classification_confidence` and `low_confidence` are present only on `model` rows and read null otherwise. No other attribute of the row is returned.

Principals: Opal principals only (the rows are opal-internal-only). The 50 KB projection of the common envelope applies unchanged. Freshness: the envelope states the row's `last_updated` and its lag in trading days behind T-1, by lib/trading_calendar.py, in the same form as the OG-sv-1 tools.

## Grant

The gateway role needs exactly one statement on its own role:

```json
{
  "Sid": "ReadEtfClassificationsByTicker",
  "Effect": "Allow",
  "Action": ["dynamodb:GetItem"],
  "Resource": "arn:aws:dynamodb:us-east-1:<account-elided>:table/etf-classifications"
}
```

Action is `dynamodb:GetItem` only. `dynamodb:Query` is not granted, because the lookup is by the full hash key `ticker` and needs no range or index. Resource is the table ARN the census measured (`table/etf-classifications` in us-east-1); the account segment is elided in this record and is resolved by the grant order from the caller identity, as the grant's own Terraform will do.

What it newly lets the gateway read: a single item at a time from the `etf-classifications` table, by ticker. It lets the gateway read no other table and no other index, and it writes nothing. It names no write action, no list or scan action, and no wildcard resource.

## Refused

The tool refuses these arms before any read, with zero DynamoDB calls, each recorded as one denied audit row:

1. No principal in the request: `principal_required`.
2. A principal that is not an Opal user: `typed_opal_only`.
3. A missing `ticker` (no argument, or an empty string) or a `ticker` that is not a string: `harvest_bad_argument`.
4. A `ticker` longer than 96 characters: `harvest_bad_argument`. The cap covers the longest contract key form, `NAME::` plus an 80-character slug.
5. A `ticker` containing whitespace or a `/`: `harvest_bad_argument`. The contract forbids whitespace in every key form.
6. A request for `as_of` other than `latest`: `harvest_bad_argument`.

One arm is an answer, not a refusal, and costs one read: a well-formed ticker with no row returns `absent_reason` with an empty body.
