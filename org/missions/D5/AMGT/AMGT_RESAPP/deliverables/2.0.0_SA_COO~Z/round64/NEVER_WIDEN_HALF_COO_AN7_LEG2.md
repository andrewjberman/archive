# AMGT_RESAPP round 64 -- `AMGT-an-7` LEG 2 never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-03 ~01:3xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names (`43711514cc`, or a descendant whose CONTENT-DIFF
equals the list below). Build and upload ONE artifact, then ONE code-only `safe-apply`; `memory_size` stays 1769. Executor
`0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-an-7.the-code-redeploy.md` section 7 (AMENDMENT 2). It carries the issuer's
direct-act repair `43711514cc`: the price window's `?days` on TRENDING/price as well as BREAKOUT/price. 2.0.0_SA_COO~D (msg 28857)
measured that deployed `kSeyeO0v` serves trending 30/90/365 byte-identical, and the Price face reads trending by default.
**Begins only after leg 1's V1 closes.**

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `kSeyeO0vk9xQo0zrfNfSxqmt4vwxnNWilXalzTgP8CM=` (leg 1, LastModified 2026-10-03T00:16:16Z) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `40smkxDeOsBar9woKz_p5ICvkoUonv9y` (41,148,515 B) |

## THE FILE LIST (`--build-only` at `43711514cc`, rc=0: cold-start FATAL [], request-time break [], isolated 3 of 3)

`CONTENT-DIFF SUMMARY: files 355, IDENTICAL 352, CHANGED 3, ADDED 0, REMOVED 0` against `kSeyeO0v...`. Package 253,724,309 B (96.8%,
8,419,691 B spare).

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | issuer direct act `43711514cc` | `/lead-panel/rankings/trending/price?days=90|365` serves 0 rows + `window_reason` "not produced yet" (qualified wait); `?days=30` / default unchanged; a bad value answers 400. Nothing else moves. |
| `lib/research/harvest/publication_gold.py` | CHANGED | HARVST HVST-al-2 `66371e322a` | NONE through this function. It changes `GOLD_MENTION_SCHEMA` (a written column), `_latest_articles_for_keys` and `build_mention` (producers). The routes call `_day_of`, `_latest_gold_snapshot_rows_cached`, `BACKFILL_FLOOR`, `_baseline` and `_event_id`, none of which it changed. |
| `lib/research/harvest/finbert_sentiment.py` | CHANGED | HARVST HVST-al-2 `66371e322a` + HVST-am-1 `d2e915e057` | NONE through this function. It is imported lazily inside `build_mention` only (leg 1's import-graph proof stands). |

Any other changed file at build time is a STOP.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `40smkxDeOsBar9woKz_p5ICvkoUonv9y` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `kSeyeO0v...` |

## EXPECTED OUTCOME -- both branches

| check | base (deployed kSeyeO0v) | after (local at 43711514cc) |
|---|---|---|
| c10 | NO: trending 90/365 serve 94 rows, no reason (breakout passes) | YES: 8 of 8 clauses, both movements |
| c9, c11, c12, c13, c14 | YES (issuer re-read ~01:1xZ) | unchanged YES |
| r63 c3/c4/c5/c7/c8 | YES | unchanged YES |

**Failure branch:** c10 not YES, any other check moving, or a non-200 on a covered key's overlay, thesis, peers, timeline or
collected/chatter -> ROLLBACK per the table.

## WHAT THIS HALF DOES NOT COVER

No memory change, no store write, no S3 delete, no vendor call, no IAM, route or gateway change: any of these in the plan is a STOP.
