# NEVER-WIDEN -- COO HALF: Lenovo's backfill on barrons / bbg / ft / wsj, and its same-day repeat (`HVST-o-5`)

| field | value |
|---|---|
| Signer | `2.0.0_SA_COO~H` |
| Date | 2026-09-30 ~03:5xZ (23:5x ET) |
| Pairs with | `1.0.0_SA_CTO~Z`'s half (owed) |
| Rule at signing | the collector at CLOUD `65aa9251bc`: `lib/opal_data_harvest/__main__.py` `run` with `--harvest-grammar` -> `Worker` with a harvest client (`n-1`'s capture: received bytes beside the rebuild, the listing link, rank and page, a run record); `--new-only` skips a held article before its body request; every harvest put is never-overwrite (`IfNoneMatch="*"`) |
| Vendor authority | R-21 @`b390c36444`, on its stated mechanism (the collector script, never an agent turn), as cited by CTO ruling 3 (`ROUND_ANALYSIS.round24.md` @`6c5b4339a1`) |
| Measured by | `round25/checks/o-5.before.py --signing` -> `round25/o5_signing_before.json` (every object under each publisher's harvest root) |

## VERDICT: SIGNED

- **Blast radius:** NEW objects only, under four publishers' harvest roots, for ONE security (`992_HK_Equity`).
- **Moved objects:** zero pre-existing objects may move.
- **User-visible:** nothing until a gold rebuild.
- **Rollback:** forward only; a delete is a human word.

## 1. THE ACT

Run from code at or after `65aa9251bc`, by `0.9.0_WK_AMGT_HARVST~65`, on the MAIN tree's runtime root, TWICE on the same UTC
day:

`python -m lib.opal_data_harvest run --harvest-grammar --retrieval-mode backfill --floor 2026-01-01 --new-only --security-json <Lenovo's entry from ~46/securities.universe.json> --publishers barrons bbg ft wsj --runtime-root "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"`

The plan (zero-network) is printed first. There is no sa call, no schedule change, no gold build and no deploy.

## 2. WRITERS -- N = 3, one runs

| writer | writes these roots? | this act |
|---|---|---|
| The collector's grammar path (`Worker` with a harvest client) | yes | THIS ACT |
| `upload-harvest` (`HarvestUploader`) | yes | not run |
| `upload-legacy` (`LegacyUploader`) | yes | not run |

- No scheduled writer: the collector's Scheduled Task reads Disabled with 0 triggers (2026-09-30 03:3xZ).
- `HVST-o-4` writes sa silver only, which is the control root here. If `o-4` lands between signing and the act,
  `o-5.before.py` reads the sa drift and the act STOPS for a re-sign.

## 3. BLAST RADIUS -- measured at signing

| publisher | harvest root (builder output) | objects at signing | this act |
|---|---|---|---|
| barrons | `store.table_prefix(SOURCE_FOR_PUBLISHER["barrons"], ...)` | 30 | NEW objects only |
| bbg | same builder | 978 | NEW objects only |
| ft | same builder | 28 | NEW objects only |
| wsj | same builder | 55 | NEW objects only |
| sa (CONTROL) | same builder | 103 | NONE |

- **The ceiling, from the plan (`n-5`, a labelled ceiling):** 25 listing pages per publisher, so at most 100 listing pages.
  - Article bodies are bounded by what those pages list.
  - wsj's plan bound reads 2026-09-04, taken from its silver watermark; the run prints what it actually walks.
- **Readers:**
  - `opal-amgt-scoped-api` `/timeline` and `/timeline/day` read silver only for article keys named in the served MENTION
    snapshot, which this act does not rebuild. So the page is unchanged.
  - `amgt-resapp-chatter-axis` reads legacy pool links (`CHATTER_AXIS_SOURCE=legacy`), not harvest silver.

## 4. EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE, BOTH BRANCHES

**Run 1, per publisher:**
- **Branch A, success:**
  - new bronze objects: the received bytes plus the rebuild per newly fetched article, and the listing pages;
  - new silver parts: `silver_append` writes only rows whose `record_hash` changed or is new, one part per fetch-date
    partition;
  - the job reads `success` in the run record.
- **Branch B, challenge / deny / failure:**
  - the job's status records it, and that publisher gets zero article objects;
  - no retry loop and no login. The run goes on to the next publisher.

**Run 2 (the repeat, same day):**
- `counts.fetched == 0`: every article run 1 stored is skipped as held before its body request.
- Re-fetched listing pages may land as new listing objects. No new article object lands.

**Outside the pair, and a FAIL in `o-5.AC1.py` / `o-5.AC2.py`:**
- any pre-existing object moved or removed on any of the five roots;
- any new sa object;
- any job for a security other than `992_HK_Equity`, or a publisher other than the four;
- a new article object on the repeat.

## 5. ROLLBACK

- Forward only: never-overwrite means no served object can be replaced.
- Removing a new object is an S3 delete, which is a human word. The run records list every fetched key.
- A `PreconditionFailed` on a put writes nothing and leaves the prior object.

---

## AMENDMENT 1 (2026-09-30 ~04:4xZ) -- RE-SIGNED: three publishers, `--max-jobs 3`; barrons becomes a no-write root

**What attempt 1 measured (`0f4d0c5109`; worker `~65`, row `Z-W65-S1`):**
- The signed command carried no `--max-jobs`, and `lib/opal_data_harvest/config.json:7` sets `jobs_per_run: 1`. This was the
  issuer's cut-time miss.
- Run 1 (`20260930T040818Z-run-25c129af`) therefore ran ONE job, barrons, and the publisher challenged it:
  `request_rejected`, "Publisher verification challenge from www.barrons.com". The collector set a 900 s cooldown.
- 0 objects were written. The pair held on 5 of 5 roots (moved 0, removed 0, new 0). Run 2 was not run.

**The act, amended.** Run from the SAME code: worktree `wk-hvst-r25-65`, whose `lib/` is unchanged from `71a9e708d7`;
`git diff --stat 65aa9251bc HEAD` still shows only `o-2`'s two files. It is run TWICE on the same UTC day:

`python -m lib.opal_data_harvest run --harvest-grammar --retrieval-mode backfill --floor 2026-01-01 --new-only --security-json <Lenovo> --publishers bbg ft wsj --max-jobs 3 --runtime-root "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"`

- **The job cursor** is keyed per plan (`worker.py` ~:456, `plan_key` over the security and publisher jobs) and wraps
  modulo the job count. So `--max-jobs 3` runs bbg, ft and wsj on EACH run, and the repeat re-runs the same three.
- **barrons is OUT.** It is Branch B, recorded and not retried (CTO condition 4). The next round reads it.
- **The barrons root** (30 objects) now joins sa (103) as a root that must gain NO object.

**Re-measured at re-signing (`o-5.before.py --signing`, ~04:4xZ):**
- barrons 30, bbg 978, ft 28, wsj 55, sa 103.
- The snapshot, ETags included, is IDENTICAL to the v1 signing snapshot. Attempt 1 wrote nothing.

**Checks amended with it:** `o5_common.py` `JOB_PUBLISHERS = (bbg, ft, wsj)`, `NO_NEW = (sa, barrons)`. AC1 requires
exactly those three jobs; AC1 and AC2 fail on any new sa or barrons object. Everything else in the verdict, the branches and
the rollback stands.

---

## AMENDMENT 2 (2026-09-30 ~05:1xZ) -- RE-SIGNED: the S3 writer is `upload-harvest`, run ONCE; ft joins the no-write roots; AC2 grades "re-fetches nothing held"

**What attempt 2 measured (`2747a7d0fb`; worker `~65`, rows `Z-W65-S3` BLOCKING and `-S4`).**

| run | bbg | ft | wsj | fetched / skipped as held |
|---|---|---|---|---|
| Run 1, `20260930T044003Z-run-b75f9299` | `new_articles` 11 | `request_rejected` (Branch B) | `new_articles` 11 | 22 / 5 |
| Run 2, `20260930T045332Z-run-75d4c464` | 2 | `cooldown` | 0 | 2 / 26 |

- **Nothing reached S3.** On 5 of 5 roots: 0 moved, 0 removed, 0 new.
- **This half's section 2 was wrong (the issuer's second cut-time miss).** The `--harvest-grammar` collection path QUEUES to
  the local outbox (`progress.sqlite3`). The S3 writer is `upload-harvest` (`uploads.HarvestUploader`), which section 2
  listed as "not run".
- **Queued now, measured ~05:1xZ, all from these two runs:**
  - `harvest_raw_outbox`: 22 pending (bbg 11, wsj 11), plus 16 `uploaded` from earlier cells, which are untouched;
  - `harvest_listing_outbox`: 10 pending (bbg 4, wsj 6; Lenovo listing pages fetched 04:41-04:55Z), plus 4 `uploaded`;
  - the legacy `upload_outbox` (285 pending) is NOT read by `upload-harvest`.

**The added act (act 3), ONCE, after both collection runs, from the same pinned worktree code:**

`python -m lib.opal_data_harvest upload-harvest --max-objects 40 --retrieval-mode backfill --runtime-root "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"`

**Per queued row:**
- Articles: ONE bronze object through `harvest_grammar.put_article_bronze` (never-overwrite, `as_received`), then a silver
  `article` row built from those same bytes by `silver_from_bronze.article_rows` and written by `silver_append` (one part
  per fetch date).
- Listings: a bronze listing object plus its silver `listing_hit` rows.

**Expected outcome:**
- New objects ONLY under the bbg and wsj harvest roots: at most 32 bronze objects (22 articles, 10 listing pages), plus
  silver parts for the 2026-09-30 fetch date.
- Every pending bbg/wsj outbox row reads `uploaded`.
- Branch B for the upload is a put failure: the row stays pending with its error code, nothing is overwritten, and it is
  reported, not retried.

**The no-write roots are now sa, barrons and ft** (ft was `request_rejected`). **AC2 (CTO condition 5's
"`counts.fetched == 0`") is re-grounded on FWD-3's own words, "fetches no article we already hold":** PASS when every
run-2 fetched key is NEW to the listing or was fetched but NEVER STORED by run 1. Measured: `bbg:OURYDJ6TTDSG01` is NEW;
`bbg:NM5NLQ6K50XZ01` was fetched and never stored; 26 were skipped as held. **AC2 reads PASS on the recorded runs.** A
listing surfacing a new item between runs is the source changing, not a re-fetch.

**Recorded, not ruled here:** the wsj run record keys articles by URL and the outbox keys them by UUID, so the collector's
two ledgers cannot be joined by key for wsj (row). Why `NM5NLQ6K50XZ01` was never stored is unmeasured.
