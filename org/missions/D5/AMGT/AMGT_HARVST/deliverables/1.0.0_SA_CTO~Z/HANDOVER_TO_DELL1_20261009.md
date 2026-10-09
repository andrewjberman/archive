# AMGT_HARVST -- HAND-OVER to DELL1 (`1.0.0_SA_CTO~Z` to `1.0.0_SA_CTO~DELL1`), 2026-10-09 ~00:1xZ

**Order:** Andrew-direct ~22:5xZ 2026-10-08, record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261008_225xZ_AMGT_DSGN_RIVALS_TO_DELL1_AFTER_ROUND_CLOSE_AND_BBG_CENSUS.md`
@b7361ceb2a. **Census:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_DELL1_MOVE_BBG_AND_LOCAL_DEPENDENCY_CENSUS_20261008.md`
@6a308cd424. Written to `1.0.0_SA_CTO~DELL1`'s term (1).

## State at hand-over

| item | value |
|---|---|
| tree row | `org/missions/D5/AMGT/AMGT_HARVST/project.json`: `active`, `EXECUTING`, `fabric: site-z`, `coo_lane: 2.0.0_SA_COO~H`; CVO `3.0.0_SA_CVO~Z`, CRO `4.0.0_SA_CRO~Z`. DELL1 re-places it at L3 |
| PRD | `prd/AMGT_HARVST_PRD.md` v0.22 @e30fb3e610: ADMITTED; ratified-text half SIGNED by `3.0.0_SA_CVO~Z`, current |
| last rounds | **73 and 74 CLOSED**, 5 of 5 terminal, drain-end packet `deliverables/2.0.0_SA_COO_H/round74/DRAIN_END_ROUNDS_73_74.md` @e25bf67559 (`2.0.0_SA_COO~H` msg 32112). No round 75 is cut |
| served gold | **rebuild #10 SERVED** (act 3, rc 0, 23:40:30Z): mention `part-20261008T225527Z` (8,290,713 B), daily `part-20261008T232700Z` (453,573 B); VERIFY holds (gone 3, lost 0, unexplained 0); C2 read: `bbg:TLG1WZKGZAIP00` absent from both BP feeds (msg 32139). Ledger `harvst-gold-rebuild10-act2-m-20261008` CLOSED |
| analysis | `ledger/ROUND_ANALYSIS.round60.md` through ADDENDUM 4 (R18 to R30). R30 graded (`3.0.0_SA_CVO~Z` msg 32050: 30 of 30 wrong, bar met) |
| open orders | `to-check --all --project AMGT_HARVST` reads **39 ACTIVE**, all with status `issued`, from round 50 onward. The issuer reports every round closed, so this is likely the first-tag parse of orders that append their flips. **DELL1's COO reconciles it as its first act**, from each order's LAST `<status>` |
| open deploy ledgers | none (read 00:0xZ) |

## Held branches (on origin as branches, never merged; each needs its own pair)

| branch | content | pair state |
|---|---|---|
| `wk-AMGT_HARVST-122-r70` 419dc9b1fc | bo-1 | this seat's half on it is SPENT WITHOUT AN ACT (`CTO_HALF_AMGT_HARVST_BO1_QUERY_OVERRIDE_MERGE_20261008.md`) |
| `wk-AMGT_HARVST-123-r71` 537ac56e9b | bo-1 + bp-1 (R23/R24, AIG query override) | **CTO half SIGNED, UNSPENT**: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_AMGT_HARVST_QUERY_OVERRIDE_BRANCH_MERGE_20261008.md` @86f57d43fa, "not before the Seeking Alpha leg has ended" |
| `wk-AMGT_HARVST-125-r73` 09642610bd | bq-2 (R25/R27 acceptance; contains 122 and 123) | no pair asked; held per section 86 |
| `wk-AMGT_HARVST-126-r74` c868d27d87 | br-1 (R30) | no pair asked; serves after rebuild #11 (R28) |

**Every merge above lands in `lib/opal_data_harvest`, a site-Z producer path.** Under `1.0.0_SA_CTO~DELL1`'s own ruling (msg 1267),
each is a site-Z deploy under a never-widen pair with `1.0.0_SA_CTO~Z`'s half signed before the merge.

## Site-Z producers (census; they stay on site Z)

- The publication collector: `backfill_driver` and `lib.opal_data_harvest run`. Its sessions are DPAPI files bound to this box's
  Windows user, alongside Chrome profiles, the captcha extension, and the progress DB and checkpoint under `.runtime/`. PRD `:1108`:
  "Each publisher has ONE persistent browser profile on the site Z box, and it is the only source of that publisher's session."
  The Seeking Alpha r47 backfill leg is running now from the shared tree, unsigned.
- FWD-18's continuous cycle and its at-log-on installer (br-2 and br-3 drained; activation not done, per the drain packet), and the
  disabled task `Opal Data Harvest - Local Publications`. These are site-Z acts.
- `publication_gold build-mention` reads a repo JSON file and S3, so it can run on DELL1 (INFERRED).

## Next work (the enrichment, unchanged by the move)

R30's merge under its pair; R27's acceptance change (bq-2) under its pair after gold; rebuild #11 under its own pair (R28: the
AIG/OMAB list move, a dry run printing the pairs moved per security, ten titles each graded). The collector pointer and any
re-collection wait on Andrew's per-use word (R22).

## Acts only Andrew can do (cited)

- Any re-collection, or moving the collector pointer (R22; his 2026-10-03 word on data operations).
- A Barron's sign-in, on site Z (his, "any time").

-- 1.0.0_SA_CTO~Z
