# Never-widen sign-off packet -- P-2's window: every 49 Financial account served on method_version 2, the per-client summaries, print and export on PATH B, and PATH A retired for 49 Financial (P-6)

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-03 ~08:4xZ | **Orders:**
- `1.0.0_SA_CTO` RULINGS batches 201, 203 and 205 (P-6: one window, one rollback; the export freezes the series it renders;
  the export reads through the reporting route).
- `CTO_ROUND_ANALYSIS_IRPT_DASHBD_ROUNDS_2_9_20261003.md`, enrichment item E1.
- Andrew's card 2 (@fec2dc7266): every 49 Financial account, then ONE Black Diamond population pull.

**Rows carried** (section 2 of the analysis): W1-S12, W1-S13, W1-S14, W1-S18, W1-S19 with W2-S3, W4-S1, W4-S2, W5-S2.

Nothing in this packet has been applied or written. The artifacts are built and uploaded (@66a931244a), and every root is
planned.

## Why

FWD-1 is live today for 6 accounts. P-2 widens it to the declared 49 Financial population on method_version 2 (FWD-8: ACCEPT met
on the method, @a108c6bd93). P-3's per-client summaries ride the same publisher.

Batch 201 rules that PATH A stops serving 49 Financial in the same window. Otherwise two paths would serve one firm's
performance, and a printed or exported report could disagree with the tab.

## Inputs, measured 2026-10-03 ~08:0xZ-08:4xZ

### The artifacts

Every artifact below is verified three ways:
- map `artifact_sha256` = S3 object bytes = S3 `content-sha256`;
- the zip's members equal the build input (source_dir at HEAD, staged files at their pins), with 0 mismatches;
- the members are diffed against the live function's zip, read from `get-function` Code.Location.

| function (live name) | live CodeSha256 -> new | members changed vs live |
|---|---|---|
| `irpt-49f-reporting-gold-lambda` | RLOFPe0l -> Mex71Y5g | 3: `account_return_daily.py` (method v2, C-VALUE, the short DIV debit), `sources.json`, `handler.py` (population, backfill mode) |
| `irpt-49f-reporting-publish-lambda` | gZM/pgyL -> AH5r60vp | 4 changed (`handler.py`, `publisher.py`, `sources.json`, `NAMING_SCHEMA.json`) + 4 added (`ids.py`, `raw_keys.json`, `custodian_key_seam.json`, `firm_registry.json`: row W4-S1) |
| `irpt-49f-reporting-read-lambda` | dKMqVbKW -> Wzf2qS5P | 6 changed (`entry.py`, `served.py`, `enforce.py`, `maintained_sources.py`, `sources.json`, `NAMING_SCHEMA.json`) + 2 added (`grant.py`, `report_owner.py`) |
| `irpt-export-render` | BIYEQ3PK (live since 10-01) -> WDAv+kWK | 24 changed + 2 added: the rounds 37-40 export changes, plus naming and registry pins already in the map |
| `irpt-performance-adapter` | U+miRkw3 -> NU6YVERL | exactly 1: `retained.py` (the P-6 retirement, IB-pr-306) |
| `auth-validator-edge` (Lambda@Edge) | :21 Mfo4c4PG -> built IN the window | `render_auth.mjs`: one pattern added, `/api/scoped/investor-reporting/reporting/{id}/series`, inside the render-token branch only (IB-pr-304) |

Notes on the artifacts:
- **Pins** (@7f80b51429) moved only the six members P-2 and P-6 need. Four pins are deliberately left behind:
  - `lib/opal_naming.py` + `reporting_policies.json` (b77e2af4d5): no code consumer, and the old validator refuses the new row,
    so the two move together or not at all.
  - `_scope/maintained_sources.py` for the export and the adapter (~Y's Y-3).
  - The adapter's other registry and `_authz` members.
  - `rebalancer_schemas.py`: under `0.0.0_AB_MSTR`'s DEPLOY-SERVE-HELD.
- **The read artifact also carries ~Y's `maintained_sources.py`** (Y-3, bb255c4cb2), already pinned in the map by its owner. It is
  named here because it moves with this apply.
- **The edge is built and uploaded inside the window, not now.** Its S3 key is fixed and `portal-auth` is a shared root, so any
  apply of that root would publish whatever the key holds.

### The plans

Each plan is read on the main tree, @66a931244a, with the same terraform binary each time.

| root | plan | resources |
|---|---|---|
| `investor-reporting/reporting-gold` | 0/1/0 | the Lambda: `s3_object_version` + `source_code_hash` only |
| `investor-reporting/reporting-publish` | 1/2/0 | the Lambda; `irpt_reporting_publish` policy (+ ListBucket `irpt/49financial/platinum/reporting/*`, the summaries pass); CREATE `irpt-49f-reporting-publish-summaries-daily`, cron(45 8 ? * MON-FRI *) America/New_York, input `{summaries:true}` |
| `investor-reporting/reporting-read` | 2/2/0 | the Lambda (+ env `IRPT_EVIDENCE_BUCKET`); `irpt_reporting_read` policy (+ GetObject / GetObjectVersion, platinum reporting prefix, batch 205); CREATE `irpt-reporting-read-render-grant-read-policy` (one prefix, `firms/*/generations/exr_*/render_grant.json`, KMS via S3 only); CREATE route `GET /api/scoped/investor-reporting/reporting/client/{client_id}/summary` (CUSTOM authorizer, existing integration) |
| `investor-reporting/export` | 0/1/0 | the Lambda only. The root needed `init -reconfigure`: the cached backend is the same bucket, key and region as declared, so no state moved |
| `investor-reporting/performance` | 0/1/0 | the Lambda only |
| `portal-auth` | planned in the window | 09-25's precedent: the edge Lambda + the distribution + the recurring benign WAF row (S133). Anything else halts the leg |

### The data

All reads are from `opal-data-49financial` (versioning **Enabled**).

| table | today | after the window |
|---|---|---|
| `gold/account_return_daily` | 562 partitions, `date=2024-07-08`..`2026-10-01`, 6 rows each | the same 562 keys rewritten as supersets over the declared population (+ any day landed before the window) |
| declared population | `holdings_performance_daily` `date=2026-10-01`: 7,570 rows, 7,570 distinct accounts | |
| `gold/dim_return_method` | `method_version=1/` (data.parquet + manifest.json), `tieout_tolerance_proposed` 0.037 double | + `method_version=2/`: NEW keys |
| `platinum/reporting` | 6 `account=` prefixes | every account of the gold union (~7,570): 6 overwritten, the rest NEW |
| `client=<cid>/summary.json` | 0 | one per directory client with at least one published account: NEW keys |

## The acts -- ONE ledger entry, `irpt-p2-window-<date>`, opened before leg A1

### Group A: the backend

Every step here is additive or is P-2's own data. None waits on the portal.

| leg | act | proof that closes it |
|---|---|---|
| A1 | targeted safe-apply, `reporting-gold` (the Lambda) | live CodeSha256 = Mex71Y5g; re-plan 0 |
| A2 | **Backfill**: 23 chunks, oldest first, `2024-07-08`..the newest landed day. Each chunk is a gold Lambda invoke with `{"backfill":{"start","end"},"accounts":"population"}`, at most 25 trading days (`MAX_BACKFILL_DAYS`) | before A2, every pre-window VersionId of the 562 x 2 keys is recorded to the ledger. After each chunk, every day's rows equal the producer's emitted count; the 6 served accounts are present every day they were before |
| A3 | **Method row**: `account_return_daily.py --method-row-only --upload --tieout 0.037` (DB-b-3's proposal, as version 1 carried it; row W5-S2) | `method_version=2/data.parquet` read back: the 22 `name:type` lines hash to `73e80ef7...` (contract 0.3.0), or the difference is a contract bump, never an in-place edit |
| A4 | targeted safe-apply, `reporting-publish`: the Lambda + its policy, **not** the schedule | CodeSha256 = AH5r60vp; the policy reads back |
| A5 | **Publish fan-out**: one invoke `{}`. Above `SHARD_ACCOUNTS` it self-invokes 8 shards (row W1-S13) | `account=` prefixes = the distinct accounts across every gold partition (printed); each has series.json.gz + manifest.json; the 6 served manifests' `method_version` = 2 |
| A6 | targeted safe-apply, `reporting-read`: all 4 resources | CodeSha256 = Wzf2qS5P; the summary route listed; the series route answers 200 for an account outside the 6, through CloudFront with a human token |
| A7 | **Edge**: `build-nodejs-lambda.sh portal-auth auth-validator-edge`, upload, then targeted safe-apply (the edge Lambda + the distribution) | the new version's CodeSha256 = the built artifact. The LIVE distribution associates it on every behavior that carried :21, by count (the post-apply check is the association, not the re-plan). Negative arm before and after: a no-token and a bogus-bearer GET answer 401. Human Auth OK continues in the edge log, with 0 runtime errors |
| A8 | targeted safe-apply, `export` | CodeSha256 = WDAv+kWK. A PATH A export still answers as before (IB-pr-301: "PATH A exports are unchanged", 168 tests) |
| A9 | **Summaries pass**: one publish invoke `{"summaries":true}` | summaries written = directory clients with at least one published account (printed, with the no-account count) |
| A10 | targeted safe-apply, `reporting-publish`: the summaries schedule | the schedule reads back ENABLED at 08:45 America/New_York |

### Group B: P-6, the readers move, then PATH A retires

| leg | act | proof |
|---|---|---|
| B1 | `2.0.0_SA_COO~D` lands the held P-6 page (c16a31e9: print and export on PATH B, the frozen `as_of`), the P-3 client summary branch and Download on portal DEV | the three readers on DEV read PATH B; a DEV walk exports an account outside the 6 |
| B2 | **PROD carries the three readers.** This is `0.0.0_AB_MSTR`'s push, on Andrew's word | `origin/PROD` contains B1's commits (`git merge-base --is-ancestor`, with a positive control) |
| B3 | targeted safe-apply, `performance` (the adapter) | CodeSha256 = NU6YVERL. Negative arm: a 49F PATH A request answers `OBJECT_NOT_COVERED`, with `PathARetiredForFirm` named in the phases line. Positive control: an Inflection PATH A request still composes |

### V: the real run

- **P-1 walk on PROD:** a signed-in 49 Financial account outside the original 6 shows the tab, a print and an export, end to end.
  The export's receipt names the frozen `as_of`.
- `3.0.0_SA_CVO` reads one served FWD-8 pair with `method_version` 2 on the rows.

### After the window

- At the drain: S15 (`routes.json` names both reporting routes) and S19 (DB-7-AC1 counts kept landings, with a floor of 10).
- E3, the ONE Black Diamond population pull, is cut after A5 is read back.

## THE CALL THIS PACKET ASKS FOR: the window's opening condition

The PROD portal (6169edd9) already reads the tab from PATH B (`dashboard/reportingRead.ts`). Its print and export still call
PATH A (`src/api/endpoints/investor-reporting.ts:195`, `/performance/{accountSetId}`). This creates two constraints:
- **B3 before B2** would make PROD's 49F print and export answer `OBJECT_NOT_COVERED`. So B3 lands only after B2 is measured.
- **Between A5 and B3**, PROD's tab serves method_version 2 while its print and export serve PATH A's composition. That is the
  disagreement batch 201 exists to prevent, so the gap must be short.

**Recommendation:** open the window only when Andrew's word for B2 is in hand for the same session. Run A1-A10, then B1, B2 and B3
back to back. A weekend window has no scheduled fire inside it: the gold, publish and summaries fires run on trading days only.

If Andrew's word does not come the same session, the window does not open. Group A alone is never served ahead of it.

## Blast radius, by each writer's own rule

Writers of each property are counted before the rules are read, because N writers means N rules.

**`account_return_daily` (3 writers):** the scheduled fire (`handler.run`), the backfill (`handler` backfill mode) and the
producer's local `--upload` (`main`).
- A2 uses the backfill mode only. By its rule it rewrites exactly the trading days in `[start, end]`. It refuses by name:
  - when the range is over 25 days;
  - when `end` is after the newest landed day (a backfill never extends the gold);
  - when the accounts are neither `population` nor a list;
  - when any requested day yields no row (nothing written, so a day is never half-rewritten).
- **The manual path off the clock:** the backfill event is the reachable new state, and the refusals above bound it. The scheduled
  fire's path is unchanged.
- **Every row moves to method_version 2.** Both branches, read from the producer's rule (equity = `net_mv_plus_cash +
  margin_balance`, batch 193, plus the short DIV debit, DB-b-19):
  - **MOVES:** an account-day with a margin balance, or a short DIV debit. Measured on the served accounts' tie-out record
    (`TIEOUT_49F_BLACKDIAMOND_R4.json` vs `_R8.json`, 14 pairs on 3 of the 6): 13 of 14 pairs move, by -0.74 pp to +0.73 pp.
    For example, acct#89d0916a 2026-06-25..07-06 moves from +3.4935% to +2.7544%.
  - **UNCHANGED:** an account-day with neither. Measured: 1 of 14 (0076459710 2026-07-09..08-04, delta 0.000000).
  - DB-b-19's income move is NOT in R8 (claim: inferred). Its rows are the 38 short-account DIV debits, 822.51 absolute (W1-S17).
- **The new accounts:** rows only where the producer emits, meaning a positive value on the day.

**`dim_return_method` (1 writer, `main`):** A3 writes `method_version=2/` only, as NEW keys. The `method_version=1/` keys do not
move.

**`platinum/reporting/account=*` (1 function, scheduled + shard + manual):**
- The account set is the union of `account_id` across every gold partition.
- The series is written before the manifest, so a manifest never points at missing bytes.
- 6 keys x 2 are overwritten and the rest are NEW.
- A refused self-invoke raises, so the fan-out never half-lands silently.

**`client=*/summary.json` (1 function, the summaries pass):** a client with no published account gets no summary and is counted.

**Code and IAM:**
- read: + GetObject / GetObjectVersion on the platinum reporting prefix, and the one render-grant prefix.
- publish: + ListBucket on the platinum reporting prefix.
- No firm fence is edited (batch 205). The export role gains nothing: its platinum policy was removed before any apply.

**The edge:** one regex inside the render-token branch. The human-token path is unchanged.

**The adapter:**
- A 49F request through PATH A, fresh or a retained reopen, answers `OBJECT_NOT_COVERED`.
- Inflection and Cottonwood are byte-unchanged in composition.

## Rollback, per key

The whole window rolls back as one, per batch 201: 49F returns to `COMPOSED_FIRMS`, the portal reverts, and the prior artifacts
are re-promoted.

| what | rollback | needs |
|---|---|---|
| 5 Lambdas' code | copy the prior S3 object version back over its key as a new version, then targeted safe-apply. The prior versions are below; the live zips are also saved by CodeSha256 in the issuer's scratch | nothing new |
| edge | re-promote `GhdNkNEz...` (Mfo4c4PG) the same way, apply, then confirm the live association | nothing new |
| 2 policies, the render-grant policy, the summary route, the schedule | revert the blocks, then a targeted apply whose plan shows exactly those resources | nothing new |
| 562 x 2 gold keys, 6 x 2 platinum keys | copy each recorded pre-window VersionId back over its key, as a new version, never a delete | nothing new |
| NEW keys: `method_version=2/`, ~7,564 x 2 platinum, the summaries | a delete marker per key (versioned, recoverable) | **an S3 delete: human confirmation at that moment**, asked through `0.0.0_AB_MSTR` (Agent Autonomy) |
| portal | ~D reverts DEV; `0.0.0_AB_MSTR` reverts PROD on Andrew's word | Andrew |

Prior artifact versions:

| key | prior version |
|---|---|
| read | `_3yEGejQDTc6ja6HJuOTScuzuc12LbIb` |
| gold | `Q49yaWRJgeu02g5mceWkxH3If81hxAEG` |
| publish | `qnGujQo2HF4N3sAKb.wbB5mIYO9DtCOo` |
| export | `6boiI8tkz.DWBdrBY6VYx.NYRE8arRwr` |
| adapter | `iw5pK0BhA.pa.gPg2vhISL19hxhgGyWT` |

## COO half -- 2.0.0_SA_COO~P

**SIGNED** on this packet's blob at its commit, for Group A + Group B + V. This seat measured:
- the artifacts;
- the plans;
- the data counts;
- both branches of the method move.

The act may touch exactly the resources and keys named above. A plan or a write outside them halts the leg.

B3 is conditional on B2 being measured. The window opens only with Andrew's B2 word in hand for the same session, unless the
CTO half rules otherwise.

## CTO half

Owed by `1.0.0_SA_CTO`, as a file on this packet's blob. Two items:
1. the blast radius and the rollback;
2. the opening condition above.
