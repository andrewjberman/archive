# FB-k-5 -- legacy operations the Inflection and Cottonwood moves make unnecessary (read-only)

Read 2026-10-13 21:56 UTC. Record: `PLANINV_LEGACY_OPERATIONS.json` (16 candidates). Nothing was changed in AWS or the repository. Class: RETIRE = no use once the firm buckets serve; REPOINT = needed, but its legacy bucket must move first.

| # | Candidate (live name) | Kind | Class | Replaced by | Replacement claim | Decision owner |
|---|---|---|---|---|---|---|
| 1 | FIRMSEP-s3-direct-access-bypass | EventBridge rule (ENABLED) | RETIRE | nothing (target SNS opal-infrastructure-alerts, 1 subscription) | inferred | CTO |
| 2 | inf-canonical-prices-daily | rule (DISABLED, held) | RETIRE | inf-silver-aggregator N/N gold fire | inferred | CTO |
| 3 | inf-gold-full-on-bronze-complete | rule (DISABLED) | RETIRE | inf-silver-aggregator N/N gold fire | inferred | CTO |
| 4 | mdpf-feeder-accelerator | rule (ENABLED, Door 6 key) | RETIRE | mdpf-feeder-backstop-daily (guarantee only) | measured | Andrew |
| 5 | opal-data-inf notification gold/meta/ pipeline-complete.json -> inf-portal-publisher | S3 notification | DECISION FIRST | nothing named | held | Andrew |
| 6 | router_iam.tf statement 3 (Door 6 deny) | IAM deny (TF text) | RETIRE | nothing | inferred | Andrew |
| 7 | opal-cot-value-parity | Lambda reader (ENABLED via rule 8) | REPOINT | reader on opal-data-cottonwood | inferred | CTO |
| 8 | opal-cot-value-parity-hourly | rule (ENABLED, rate 1 hour) | KEPT | unchanged target (7) | inferred | CTO |
| 9 | opal-cot-value-parity (role) | IAM role, CotServedAndSourceRead | REPOINT | same role, grant re-scoped | inferred | CTO |
| 10 | opal-data-cot#policy (and bd, inf) | bucket policy, OAI read | RETIRE WITH BUCKET | firm-bucket policies (PRD F4) | inferred | CTO |
| 11 | portal CloudFront distribution | edge, 3 legacy origins | REPOINT | same distribution, origins moved | inferred | CTO |
| 12 | opal-assets-ingest-mirror-cot-daily-et | schedule (ENABLED) | REPOINT | mirror sources moved | inferred | CTO |
| 13 | cot-bronze-complete | rule (ENABLED) | REPOINT | rule re-created on firm bucket | inferred | CTO |
| 14 | cot-silver-complete | rule (ENABLED) | REPOINT | rule re-created on firm bucket | inferred | CTO |
| 15 | opal-cot-served-guard-on-write | rule (ENABLED) | REPOINT (PRD DEC-7) | guard re-created on firm bucket | measured | CTO |
| 16 | opal-inf-value-parity | Lambda reader | REPOINT | reader on opal-data-inflection | inferred | CTO |

## The four named operations

- `FIRMSEP-s3-direct-access-bypass`: row 1. Watches GetObject on the two legacy buckets; cot is no longer in its pattern.
- `inf-canonical-prices-daily`: row 2. Disabled since 2026-07-13 under the INF gold dispatch hold; stays held.
- `mdpf-feeder-accelerator`: row 4. Andrew's DEC-13 ruling; the backstop schedule remains the only guarantee.
- `opal-cot-value-parity`: row 7, with its hourly rule (row 8) and role (row 9). A repoint, not a retirement.

## For Andrew

- **Door 6 has a second consumer (row 5).** The "no-other-consumer read" that the DEC-13 ruling assumes finds `inf-portal-publisher`, wired by ADVI_INFETL.005. Retiring the key stops that trigger. Surprise `ADVI_FIRMBKTS-D1-W80-S1`.
- The router deny (row 6) cites `mdpf-daily-refresh-trigger`, which is absent live. Surprise `ADVI_FIRMBKTS-D1-W80-S2`.

## Denominators

2926 AWS nodes scanned by the graph; 11 EventBridge rules name a legacy bucket (all read); 34 Scheduler schedules listed (3 read in full); 5 Lambda configurations read; 3 bucket notification configurations and 3 bucket policies read; 194 repo files under infra/ name a legacy bucket (counted, not classified).

Not read: see `not_read` in the JSON record.
