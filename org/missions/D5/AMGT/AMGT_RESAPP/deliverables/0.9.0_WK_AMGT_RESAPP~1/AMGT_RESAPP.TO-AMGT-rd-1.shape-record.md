# AMGT-rd-1 -- THE ARTICLE STORE: shape record

`0.9.0_WK_AMGT_RESAPP~1`, round 5, 2026-09-11.

## (c) THE SHAPE RECORD -- what was landed, and what it was measured against

`opal-news-articles` has NO declarative Terraform source in this repo (comp-find --corpus aws at the
round-5 cut: drift=LIVE-no-DECLARED). So "shaped like the proven `opal-news-articles`" cannot mean "copied
from a .tf file" -- there is none. It was re-measured directly against the LIVE table before this module
was written:

```
timeout 60 .tools/aws dynamodb describe-table --table-name opal-news-articles --output json
```

## opal-news-articles -- LIVE shape (measured 2026-09-11, this table exists but is undeclared in Terraform)

| | |
|---|---|
| TableName | opal-news-articles |
| BillingMode | PAY_PER_REQUEST |
| KeySchema | HASH `article_date` (S)  /  RANGE `url_hash` (N) |
| GSI | `source_date_index` -- HASH `source` (S) / RANGE `published_at` (S), Projection ALL |
| SSE | KMS enabled |
| DeletionProtectionEnabled | true |
| ItemCount (at measurement) | 344,211 |
| Declared item fields beyond the key schema (per the cell text: title / source / url / published_at / sentiment) | NOT in AttributeDefinitions -- DynamoDB only declares attributes that participate in a key schema or a GSI key; payload-only fields (title, sentiment, url) are written per-item with no schema entry. `source` and `published_at` ARE declared because they are the GSI's own hash/range keys. |

## opal-amgt-articles -- landed shape (this cell, `infra/aws/terraform/amgt-resapp/dynamodb.tf`)

| | |
|---|---|
| TableName | opal-amgt-articles |
| BillingMode | PAY_PER_REQUEST (matches opal-news-articles, per the cell's explicit instruction) |
| KeySchema | HASH `security_key` (S)  /  RANGE `published_at` (S) |
| GSI 1 | `platform_date_index` -- HASH `platform` (S) / RANGE `published_at` (S), Projection ALL |
| GSI 2 | `ticker_date_index` -- HASH `ticker` (S) / RANGE `published_at` (S), Projection ALL |
| PITR | enabled (house convention on every sibling DDB module measured in this estate -- `etfs-canon/dynamo.tf`, `imo-pipeline/dynamodb.tf` -- not itself asked for by the cell, so named here rather than left silent) |
| Payload-only item fields (declared nowhere, exactly as opal-news-articles does for its own payload fields) | `title`, `source`, `url`, `sentiment` |

## The mirroring, stated axis by axis (measured, not asserted)

- **Payload fields**: `title` / `source` / `url` / `published_at` / `sentiment` are carried exactly as
  `opal-news-articles` carries its own -- `published_at` promoted to a declared key attribute (it is the
  table's own range key AND both GSIs' range key, exactly mirroring how `opal-news-articles` promotes
  `published_at` to its GSI's range key); `title` / `source` / `url` / `sentiment` are payload-only,
  exactly as `title` and `sentiment` are payload-only on the live table (`source` here is payload for
  identifying which platform published, distinct from the new `platform` key attribute below).
- **`platform_date_index` mirrors `source_date_index` directly**: HASH+RANGE-by-date over the "who
  published this" axis. `opal-news-articles` uses `source` (a general-news wire/outlet); this table's
  per-platform axis is `platform` (Seeking Alpha / FT / Bloomberg / WSJ per AMGT-rd-4) -- same shape,
  same GSI role, different domain vocabulary because this is a genuinely different store.
- **`ticker` / `security_key` are FIRST-CLASS declared key attributes, never packed into a blob**: this is
  the one axis `opal-news-articles` has no analogue for (it is not per-ticker). `security_key` (the S12-
  resolved canonical identity) is the table's PRIMARY partition key -- the strongest possible "first-class"
  placement. `ticker` (the raw, human-facing symbol S12 resolves FROM) is a second first-class key via its
  own GSI, so a caller can look up by either the raw ticker or the resolved identity without touching a
  blob field.

## GENUINELY SEPARATE, stated against both bounded stores

- **Not `opal-news-articles` with a filter**: a wholly separate `aws_dynamodb_table` resource, its own
  name, its own key schema (`opal-news-articles` has no per-ticker axis at all -- there is no filter value
  of `article_date`/`url_hash` that turns that table into a per-ticker store). Different owner
  (AMGT_RESAPP), different consumers (the Lead Panel / Thesis-Peers-Coverage surface, AMGT-rd-8), different
  lifecycle.
- **Not `opal-data-research`**: that is an S3 bucket (S1's model-block home, S5's print-snapshot home,
  created by this project's own `AMGT-s-6`), a different AWS service entirely, untouched by this module --
  `infra/aws/terraform/amgt-resapp/*.tf` declares no `aws_s3_bucket` resource of any kind and no
  modification to any existing one.

## Terraform plan, for the record (1 resource, no second output path)

```
Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + amgt_articles_table_arn  = (known after apply)
  + amgt_articles_table_name = "opal-amgt-articles"
```
