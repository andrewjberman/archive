# NEVER-WIDEN -- COO HALF: rebuild `chatter_daily` with the publisher codes (`HVST-i-3`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~21:2xZ (17:2x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rule at signing:** `lib/research/harvest/publication_gold.py` at CLOUD `8f2a0bf027` (the `HVST-i-2` drain). The
harvest suite passes 202 of 202 on the merged trunk. The change appends ONE column, `publishers_covered_codes`
(`list<string>`), LAST in `GOLD_DAILY_SCHEMA`; its value is `list(covered)`, the list the rule already built for
`publishers_covered`. **Securities input:** `deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json` (`i-1`; it
equals the round-18 file on 191 of 191). **Measured by:** `i-2`'s AC2 script re-run on the trunk at signing, saved
beside this file as `i3_signing_i2_ac2_rerun.txt`. It is BYTE-IDENTICAL to `i-2`'s committed `i2_ac2_output.txt`
(silver unmoved: 120 articles, 60 listing rows). **That file IS the expected diff.**

## VERDICT: SIGNED -- blast radius ONE new S3 object (chatter_daily), user-visible only after `HVST-i-4`; rollback forward-only

## 1. THE ACT

Run `python -m lib.research.harvest.publication_gold build-daily --securities-json <the file above> --as-of <run date
UTC>` ONCE, by `0.9.0_WK_AMGT_HARVST~46`, from CLOUD code at or after `8f2a0bf027`. No mention put, no event put, no
code change, no delete, no vendor call.

## 2. WRITERS -- N = 3 (unchanged), READERS measured at signing

- **Writers:** `build_daily` (chatter_daily, the only one this act runs), `build_mention` and `build_event`, all in
  `publication_gold.py`. No scheduled producer writes the prefix.
- **Reader 1, the deployed scoped API** `opal-amgt-scoped-api`: CodeSha256 `lg6NJ2JLYbTc9ZtlDaA9nckuNSOaZZmsYKzDjRPbB3s=`,
  LastModified 2026-09-29T19:18:58Z (AMGT_RESAPP ww-1). It serves the newest daily part as the `/timeline` `series`.
  **That code predates `i-2`:** it reads named fields with `row.get` and ignores the new column. So after this put the
  served series is UNCHANGED on every field it serves today, and the codes reach users only through `HVST-i-4`.
- **Reader 2, LATENT:** `amgt-resapp-chatter-axis`, `CHATTER_AXIS_SOURCE=legacy` (LastModified 2026-09-24T05:09:00Z). It
  does not read chatter_daily today.

## 3. BLAST RADIUS -- measured at signing

| table | parts | newest (served) | ETag | rows | this act |
|---|---|---|---|---|---|
| article_security_mention | 6 | `date=2026-09-29/part-20260929T192610Z` | `831c5669591b247c5ebf2d081a91b249` | 304 | NONE |
| chatter_daily | 7 | `date=2026-09-29/part-20260929T192649Z` | `7bce5e68cf4fad06d227d4e41ff36dbd` | 51,952 | ONE put |
| chatter_event | 8 | `date=2026-09-29/part-20260929T192706Z` | `c146a325c98963f965b8b1bd69ca3393` | 8 | NONE |

The put is conditional (`IfNoneMatch="*"`) at `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<run_stamp>.parquet`.
Every prior part stays with its ETag unchanged.

## 4. EXPECTED OUTCOME, READ FROM THE MERGED RULE AT SIGNING -- both branches

### 4.1 chatter_daily: 51,952 -> 51,952 rows; the 21 pre-existing columns unmoved on EVERY row; ONE new column

- **Pre-existing columns:** 0 of 51,952 rows differ on any of the 21, with DRIFT 0 (rerun section (a)).
- **New column `publishers_covered_codes`, by class** (the codes are in `ENABLED_PUBLISHERS` order and
  `len == publishers_covered` on every row):

  | data_status | rows | codes |
  |---|---|---|
  | DENIED | 51,803 | `[]` |
  | PARTIAL | 149 | as below |
  | COMPLETE | 0 | none |

  | security | PARTIAL days | codes |
  |---|---|---|
  | `ASML_NA_Equity` | 74 | `['sa']` |
  | `ASML_US_Equity` | 74 | `['sa']` |
  | `992_HK_Equity` | 1 | `['wsj']` |

- **Any non-empty code list on a row outside those 149 is OUTSIDE THE PAIR.** So is any pre-existing cell that moves.

**The `--as-of` branch:**
- **At 2026-09-29:** the served daily part already ends on 09-29, so there are 0 extension rows.
- **At 2026-09-30:** exactly 191 extension rows are added (one day x 191 securities). They are DRIFT rows, and their
  codes follow the same rule. This is the only permitted DRIFT.
- Any other as-of is outside this half.

### 4.2 The failure branches

- **KEY COLLISION:** `PreconditionFailed`; nothing is written and the prior part stays newest.
- **READ-BACK MISMATCH:** `HarvestStoreError`; the object stays distrusted. Recovery is a further rebuild, never a
  delete.
- **The BEFORE state differs from section 3** (any of the three newest keys or ETags, or reader 1's CodeSha256): STOP
  before the put (`i-3` clause 1.5). A silver move surfaces as DRIFT, and in AC1(b) as OUTSIDE THE PAIR, which FAILS
  the run.

## 5. ROLLBACK -- forward-only

Revert `HVST-i-2`'s column (the `8f2a0bf027` drain) and rebuild daily. A later part without the column restores the
round-18 shape by addition. The section-3 part survives by construction and is the reference. Reader 1 at section 2's
code does not read the column, so the rollback has no user-visible leg until `i-4` lands.

## 6. FOR THE CO-SIGNER

1. **992_HK_Equity's single wsj day is new to this round's reading.** The analysis named ASML's 74 days. The merged rule
   also names the one 992_HK day on which the wsj listing rows cover Lenovo. Both are the same rule, the one ruled
   correct in round 18 (the identifier rule mirrors the writer), and this half covers the 992_HK day by name.
2. **COMPLETE is proved only by a unit test:** there are 0 COMPLETE rows at the cut.
3. **The user-visible change is `HVST-i-4`'s act, not this one.** This put changes no field reader 1 serves.

## 7. WHAT THIS HALF DOES NOT COVER

- No S3 delete; no mention or event put; no code change; no deploy.
- No change to `CHATTER_AXIS_SOURCE`.
- No as-of other than 2026-09-29 or 2026-09-30.
- No code on any row outside the 149 PARTIAL rows named above.
