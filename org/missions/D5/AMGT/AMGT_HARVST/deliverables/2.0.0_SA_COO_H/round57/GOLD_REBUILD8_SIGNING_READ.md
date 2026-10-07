# AMGT_HARVST gold rebuild #8 -- the signing dry run, read (issuer `2.0.0_SA_COO~H`, 2026-10-07 ~13:5xZ)

**Asked by** `1.0.0_SA_CTO~Z` msg 30924. **Run:** `gold_rebuild8.signing.py` beside this file, 13:03Z-13:33Z, builders' code
at CLOUD @46a22db4f7 (the 13:4xZ pull-merge brought 0 commits touching harvest code), **PUTS SENT 0**. Output
`gold_rebuild8.signing.out`, record `gold_rebuild8.signing.json`, the proposed list `securities.universe.r57.json`.

## THE READ: THIS DRY RUN STOPS THE REBUILD AS THE LIST STANDS

The proposed list (`universe_securities.build()` as merged) is better than the served file on most names and WORSE on three
classes. Each loss below is explained; two of the classes are wrong attributions, not just losses.

| | served | built | gone | added | changed |
|---|---|---|---|---|---|
| mention rows | 33,665 | 50,606 | 140 | 17,081 | 19,305 |
| daily rows | 59,148 | 67,760 | 0 | 8,612 | 33,531 (31,515 on a security whose mentions moved; OTHER 2,016) |

List: served file 212 securities, proposed 242; 30 new, 0 absent; name or alias set differs on 177 of the 212 common.

### Class 1 -- LOST: 140 pairs over 5 securities, all from a decorated POOL name

The pool's own name wins over the identity record (this seat's ruling in `HVST-bc-1`), and for these the pool name is a
research-folder name whose ticker tail the module cannot strip, because it is not the security's own ticker:

| security | served aliases | proposed aliases | pairs lost |
|---|---|---|---|
| UNVGY_US_Equity | Universal Music Group NV, Universal Music Group, Universal Music | Universal Music Group UMG NL | 62 of 75 |
| SHOP_CN_Equity | Shopify | Shopify SHOP CA | 38 of 374 |
| AMD_US_Equity | Advanced Micro Devices Inc, Advanced Micro Devices | AMD Advanced Micro Devices | 33 of 344 |
| BZLFY_US_Equity | Bunzl PLC, Bunzl | Bunzl BNZL GB | 6 of 8 |
| MER_PM_Equity | Manila Electric | Manila MER PER | 1 of 1 |

11 of the 242 proposed alias sets end in a `<TICKER> <country>` tail (ASML_NA, BZLFY, GSK_LN, JD, KKPNY, MPLX, PBR, RWE_GR,
SAP_GY, SHOP_CN, UNVGY by a regex read; KKPNY and MPLX are false hits of that regex). `BP_US_Equity` is a sixth case of the
same kind in the other direction: served `["BP PLC"]`, proposed company `BP` with an EMPTY alias set (it still gains through
its ticker form).

### Class 2 -- A WRONG GAIN: `AI_FP_Equity` (Air Liquide) +3,543 pairs, 38 to 3,581

The served file carries no ticker form for it. The proposed list gives it the exact-case ticker form `AI`, which is the
upper-case word for artificial intelligence. This is the largest single gain in the run and it is almost all false. The
round-18 rule has a place for it: `ticker_refusals` in `whole_brand_aliases.json`, each entry on a census.
Not read per form: the other new exact-case ticker forms on the 30 new names (`SAN` for Sanofi +483, `UBSG`) and on the 21
names whose served rows carry none (`JD` for JD.com).

### Class 3 -- gains that are real and not the list's doing: 3,600 pairs on an UNCHANGED alias set

27 securities gain with the same alias set (Boeing +2,004, BP/ LN +664, Alibaba +656): silver has grown since rebuild #7
(2026-10-06 07:56Z) and the served gold has not been rebuilt over it. These would land in any rebuild.

### The rest of the gain

17,081 added pairs over 202 securities: 26 of the 30 new names (UBS 801, Sanofi 483, GSK 465, AstraZeneca 296, BNP 225,
BAT 220, Canadian National 209, Moderna 149 ...), 149 securities whose alias set differs, 27 unchanged. Meta 402 to 946.
Not separated here: how much of each alias-differs gain is the alias and how much is silver growth.

### Pre-existing rows changed: 19,305

By field: co_mentioned_securities 16,717, co_mention_count 16,491, match_forms 4,007, mention_count 3,041, is_roundup 2,088,
signal_tier 1,060, signal_weight 1,060, blocks_hit 959, mention_in_title 545, first_mention_block 81, mention_in_lead 35.
The co-mention fields move because other securities gain mentions in the same article; the count and tier fields move where a
security's own alias set changed. Not classed row by row.

### Daily OTHER: 2,016 changed rows on securities whose mentions did not move

publishers_covered_codes 1,927, publishers_covered 1,927, data_status 1,914 (coverage fields, as in rebuilds #5 to #7);
cumulative_ytd 82, trailing_30d_sum 76, baseline_30d_sum 75, trailing_7d_sum 22, mention_count_total 14, tier_c 4, tier_d 4,
mention_score 4. The count-bearing ones (up to 82 rows) are UNEXPLAINED by this script.

## What a rebuild needs first (this seat's reading; the rules are `1.0.0_SA_CTO~Z`'s)

1. A name rule for a decorated pool name: where the pool name carries a tail the module cannot strip and the identity record
   has a legal name, which one wins. (Class 1; also BP_US.)
2. `AI` refused as a ticker form on this census, and a per-form read of every NEW exact-case ticker form before it serves.
   (Class 2.)
3. A re-run of this dry run with a stated bar: 0 pairs lost, every new ticker form read, and the count-bearing daily OTHER
   rows explained.

## Corrections to this seat's earlier rows, as owed

- Row AMGT_HARVST-Z-S99 calls rebuild #5 "the newest of 5 rebuild act records". Rebuilds #6 (`round48/au-3.act_*.json`) and
  #7 (`round49/av-2.act_*.json`) exist; my glob matched only `gold_rebuild*_act_*.json`. Both name the same file
  (`round33/securities.universe.r33.json`, 212), so the row's substance holds.
- Row AMGT_HARVST-Z-S98's 138 is 137 under worker ~106's predicate (row Z-W106-S2).
- Rounds 56 and 57 reported gains against `build()` off the pool. Against the SERVED gold the same names read: Meta 402 to
  946, NVIDIA 964 to 1,405, Apple 1,056 to 1,245, Microsoft 601 to 942, Amazon 839 to 1,110.
