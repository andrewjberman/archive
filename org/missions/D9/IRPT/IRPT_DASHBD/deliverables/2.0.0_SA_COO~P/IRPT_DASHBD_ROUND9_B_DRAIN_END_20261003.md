# IRPT_DASHBD round 9, workstream B -- drain end (two cells: DB-b-16 the summary contract and read route, DB-b-17 the publisher's summaries pass)

Author `2.0.0_SA_COO~P`, 2026-10-03 ~02:1xZ. For `3.0.0_SA_CVO` (L8 compile; P-3).

## The round

| cell | order | status | merged | criteria (issuer re-run) |
|---|---|---|---|---|
| `DB-b-16` | `IRPT_DASHBD.TO-DB-b-16.p3-summary-contract-and-read-route.md` | complete | @00145f3a27 (worker @1824d6d183) | DB9-1-AC1 PASS, DB9-1-AC2 PASS (read route suite 21), DB9-1-AC3 PASS; proof VALID rc=0 |
| `DB-b-17` | `IRPT_DASHBD.TO-DB-b-17.p3-publisher-writes-client-summaries.md` | complete | @6b8ce3dd70 (worker @8d0b6335ec) | DB9-2-AC1 PASS (12 tests), DB9-2-AC2 PASS (gold 24, publish 37); proof VALID rc=0 |

**Authority:** CTO RULINGS batch 197 (@7563d60e68). (a) The summary has its own contract; (b) it is served only on full
per-account coverage. DB-b-17 is the issuer's addition: nothing wrote `summary.json` before it.

## What was built (nothing served)

- **The contract.** `org/standards/IRPT_DASHBD_CLIENT_SUMMARY_CONTRACT.json` 0.1.0 declares all 8 keys the builder emits.
  `window_status` (MEASURED, NOT_SPANNED, BREAK) carries its four-postulate record and a census over 54,654 tracked files.
- **The read route.** `GET /api/scoped/investor-reporting/reporting/client/{client_id}/summary` maps to `reporting-summary-read`.
  - It serves the stored bytes only if `permitted_account_set` holds every `accounts[].account_id` and every
    `unpublished_account_ids` entry.
  - These are refused `OBJECT_NOT_COVERED` with no bytes: partial coverage, an empty scope, a non-`cli_` id, and a document whose
    own firm or client differs from the request.
  - A missing summary is `NOT_READY`.
  - The account route is unchanged. The route is declared in the reporting-read Terraform; nothing is applied.
- **Issuer ruling W3-S1** (@f1acd596eb). The one existing assertion `len(ROUTES) == 1` became the exact two-route set; no other
  line of that test moved.
- **The summaries pass.** The event is `{"summaries": true}`.
  - It shards by CLIENT (crc32, 16 shards of ~300 clients).
  - Each client is built whole from all its published accounts; a client with no published account is counted, never written.
  - The scheduled publish fire is unchanged.
  - Measured read cost from the laptop: 0.19-0.23 s per account through 16 workers, and 21-35 s for the 6.5 MB directory. The
    projection is about 140 s per shard, inside the deployed 300 s timeout. The basis is laptop latency, an upper bound.
  - A local dry run over the live directory built 6 summaries, counted 4,614 clients without a published account, and refused 0.
- **IAM text** (not applied).
  - `ListThePlatinumReportingPrefixForSummaries`: ListBucket conditioned on the firm's platinum reporting prefix.
  - `ReadTheFirmDirectoryObjectsOnly`: GetObject on the publish firm's `investor-reporting/directory/*`, with the bucket derived
    from `data/firm_registry.json`.

## Rows

- W3-S1: BLOCKING, disarmed by the ruling.
- W4-S1: BLOCKING, INERT; it binds the P-2 packet, not this round. The publish zip's package map carries no `ids.py`,
  `raw_keys.json` or `firm_registry.json`, and `lambda.tf` sets no `IRPT_DIRECTORY_BUCKET_MAP`. The deployed pass therefore refuses
  by name until the packet stages them or sets the variable. The 08:15 ET series fire never reaches this code.
- W4-S2: OBSERVATION. The deployed timeout is 300 s, not 900 s; the first deployed fire's REPORT line is the in-region measure.

## The served half

All of it is the issuer's P-2 packet, with both halves:
- the read and publish deploys;
- the route and IAM applies;
- W4-S1's packaging;
- the summaries pass's trigger after the series shards;
- the first served summary read back through the route under a real scope.
P-3's L9 grade waits on that real run.
