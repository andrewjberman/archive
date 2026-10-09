# IRPT_DASHBD round 1 (workstream B) -- the issuer's drain-end record (spine L8 input; the CVO's channel compile is its own artifact)

**Issuer:** `2.0.0_SA_COO~P`, 2026-10-02 ~04:4xZ. **Issuance:** @51c05d1530 (decomposition `decompositions/IRPT_DASHBD_DECOMP.md`
section 1, four cells). **PRD at the drain:** v0.6 @aabc054e89 (both halves current). **Merge of the last chain:** @9000ce5a08.

## The four cells, terminal

| cell | order | terminal state | evidence |
|---|---|---|---|
| `DB-b-1` | TO-DB-b-1 (`0.4.0_DS_ClientPlatform~S`) | COMPLETE @c1c399af74 | gold `account_return_daily` + `dim_return_method` served under contracts 0.2.0; 3 of 3 criteria PASS; 559 partitions 2024-07-08..2026-09-28 |
| `DB-b-3` | TO-DB-b-3 (`0.4.0_DS_ClientPlatform~S`) | COMPLETE @38f828d708 | tie-out record `deliverables/0.4.0_DS_ClientPlatform~S/tieout/TIEOUT_49F_BLACKDIAMOND_R1.md`, 0 vendor calls; rows S10/S11, ruled in PRD v0.6 (22-25) |
| `DB-b-2` | TO-DB-b-2 (`0.9.0_WK_IRPT_DASHBD~1`) | COMPLETE @f27f5be63a, merged @9000ce5a08 | DB-2-AC1/AC2/AC3 PASS; proof VALID rc=0 (issuer re-run); ledger `irpt-dashbd-reporting-publish-49f-r1-20260930` CLOSED |
| `DB-b-4` | TO-DB-b-4 (`0.9.0_WK_IRPT_DASHBD~1`) | COMPLETE @e14bf52a37, merged @9000ce5a08 | DB-4-AC1 PASS; proof VALID rc=0 (issuer re-run); amendment 1 @4b45d5d089 |

Post-merge hygiene on CLOUD @9000ce5a08: 24 unit tests pass (`reporting-publish/tests`, `reporting/tests`); `py_compile` OK on the
three modules; `lib.opal_naming.load_registry()` loads with the new policy row.

## The one real run of each outcome

- **FWD-1 hop 1 (gold):** DB-b-1's served gold, read by both later cells (DB-b-2's AC2 links three 20-day windows from the gold rows).
- **FWD-1 hop 2 (platinum file):** the publisher ran for real once (the local `--upload` run under the closed ledger): six accounts'
  `series.json.gz` + `manifest.json` under `s3://opal-data-49financial/irpt/49financial/platinum/reporting/account=<id>/` (every
  account in the newest partition, 2026-09-28; the face said five). Thread account acct#08137b81: 559 days, 17,665 bytes gz; the served
  object's sha256 equals a fresh rebuild.
- **FWD-1 hop 3 (read route):** exercised LOCALLY against the real S3 objects: `serve_series` returned the series (17,665 B) and the
  manifest (385 B) byte-equal for the thread account and refused an uncovered account before any read. **Not served:** neither root is
  applied. Route for workstream F: `GET /api/scoped/investor-reporting/reporting/{account_id}/{which}`, `which` in `{series, manifest}`;
  success `Content-Type: application/json`, `Cache-Control: private, no-cache`, the object's `ETag`, `Content-Encoding: gzip` on the
  series; refusal `OBJECT_NOT_COVERED` and missing object `NOT_READY` as the public envelope, never a 500.
- **FWD-8 (tie-out):** 0 of 5 pairs on like day sets (PRD v0.6 ruling 23): not graded on agreement in round 1.
- **Thread live:** `n`. The two roots are planned, not applied, and the page is workstream F's.

Plans saved verbatim: `deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-publish.plan.txt` (`Plan: 7 to add, 0 to change, 0 to destroy`:
the Lambda, execution role + policy, scheduler role + policy, schedule `irpt-49f-reporting-publish-daily` 08:15 America/New_York
Mon-Fri, log group) and `reporting-read.plan.txt` (`Plan: 8 to add, 0 to change, 0 to destroy`; role reads only
`arn:aws:s3:::opal-data-49financial/irpt/49financial/platinum/reporting/*`). Artifacts in the artifacts bucket:
`investor-reporting/irpt-reporting-publish-lambda.zip` (108,492 B) and `investor-reporting/irpt-reporting-read-lambda.zip` (261,917 B,
head-object sha equals the source map).

## Rows (13 in the channel; 0 ARMED)

| row | standing | disposition |
|---|---|---|
| S1 | BLOCKING, INERT | answered by PRD v0.3 ruling 16 (@c812be9885): round-1 policy rows are for the platinum served files only |
| S2 | BLOCKING, INERT | answered by amendment @b116670d7c: contract files under `org/standards/` are written by the issuer |
| S3-S8 | BLOCKING / OBSERVATION, INERT | answered by PRD v0.4 rulings 17-19 and DB-b-1 amendments 5 and 6 (@f4f57b6fe4, @34ae583549) |
| S9 | BLOCKING, INERT | ruled at PRD v0.5 |
| S10, S11 | BLOCKING / OBSERVATION, INERT | ruled at PRD v0.6 (22-25) |
| W1-S1 | OBSERVATION, INERT | ACCEPTED (@4b45d5d089): `series.json.gz` has no X10 family (the validator admits csv/json/pdf, one family per table) |
| W1-S2 | OBSERVATION, INERT | ACCEPTED (@4b45d5d089): the naming gate refuses a new `49f` token; the source-map key is the scope-less builder name |

The channel's `disposition` fields still read UNDER_INVESTIGATION on all 13: no CVO compile has run on this channel (no
`adjudications/`; watermark 0 of 13).

## Enrichment the issuer proposes for round 2 (workstream B), for the CTO's analysis

1. **The thread's served leg:** apply both roots under ONE packet with both never-widen halves (WORLD: a new scheduled function and a
   new served route on the IRPT API), then the signed-in page's one fetch (workstream F) as the real run of FWD-1.
2. **A retention family for `series.json.gz`** (W1-S1): the registry admits gzip JSON or a second table; the registry owner's call.
3. **The 1,498.38 USD flow residual on acct#89d0916a** (PRD v0.6 ruling 25; the fee matches to the cent).
4. **Carried, not a cell:** like-day tie-out windows need Andrew's per-use vendor word (ruling 23); FWD-8's tolerance stays his.
5. **Hygiene:** untracked empty directories `data/`, `infra/`, `lib/`, `org/` sit inside `infra/aws/lambda/investor-reporting/reporting/`
   in the worker's worktree (a stopped build's staging); the build packages its source directory, so a rebuild there ships them empty.

## Not done here

- The worker worktree DIR `C:\Users\AndrewBerman\Desktop\wk-irpt-dashbd-1` and branch `wk-IRPT_DASHBD-1` are NOT yet removed (a
  recursive delete; held for Andrew's word under CLAUDE.md Agent Autonomy).
