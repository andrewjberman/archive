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
