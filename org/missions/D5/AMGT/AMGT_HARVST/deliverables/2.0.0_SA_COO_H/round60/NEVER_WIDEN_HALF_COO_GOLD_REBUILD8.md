# NEVER-WIDEN -- COO HALF: HARVST served gold rebuild #8 -- the served gold moves from the hand-carried 212-name list to the list the code builds (242 names)

**Signer:** `2.0.0_SA_COO~H`, 2026-10-07 ~20:3xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Why:** `1.0.0_SA_CTO~Z` msgs 30864 item 3 (ONE rebuild, under its own pair), 30924, 31008, 31173, 31209, 31222, 31329.
Every served build through #7 took `round33/securities.universe.r33.json` (212 names, hand-carried). Rounds 56 to 60 made
`universe_securities.build()` yield a list fit to serve: legal names from the collector's identity record (`HVST-bc-1`,
`HVST-be-1`), `Meta` as a gold brand and `Lilly` anchored (`HVST-bd-1`), and eight ticker forms refused on a graded census
(`AI` in `be-1`; `BATS`, `JD`, `ICT`, `ML`, `BE`, `SAN`, `MSCI` in `HVST-bg-1`). The rebuild-#7 pair is spent; this is a NEW
pair.

## THE RULE (`round60/gold_rebuild8_rule.py`, ONE function; read by the gate `gold_rebuild8.signing4.py` before the write and by `gold_rebuild8.act.py` VERIFY after it)

List passed to the builders: `round60/securities.universe.r60.json`, 242 securities; the gate checks it equals
`universe_securities.build()` at HEAD (True at signing).

**Mention** (key = article, security):
- **LOST: 0.** A served pair that goes is class **(h) REFUSED-FORM REMOVAL** only when every form it matched is on
  `ticker_refusals`, the list no longer gives the security that form, AND the pair is one of the 17 named in
  `round60/ICT_US_SERVED_PAIRS.json`. Any other gone pair is LOST and breaks the rule.
- A served row that CHANGES is exactly one of: **(c)** hash-only (the rebuild-#7 class); **(g)** own-alias (a counting field
  moves on a security whose name or alias set differs between the two lists); **(f)** co-mention (only the co-mention
  fields move, and every security entering or leaving the set has an added, (g)-changed or (h)-removed row in that article).
  Anything else is UNEXPLAINED and breaks the rule.
- A `mention_count` that goes DOWN is allowed only on a security that lost a served alias.

**Daily** (key = security, day): gone 0; a changed row is (a) on a security with an added, changed or (h)-removed mention
row, or (b)/(d) coverage-only by the rebuild-#5 bounds; OTHER breaks the rule.

## MEASURED AT SIGNING

Gate run 19:40Z-20:18Z, builders' own code at CLOUD HEAD through the capturing client, **PUTS SENT 0**; record
`round60/gold_rebuild8.signing4.json`, out `round60/gold_rebuild8.signing4.out`. (The first gate run, before class (h) was
ruled, is kept as `signing4.run1.*` and read BROKEN on the same 17 pairs.)

| | served | built | gone | added | changed |
|---|---|---|---|---|---|
| mention | 33,665 | 47,992 | 17, all class (h); **LOST 0** | 14,344 | 12,032: (g) 3,257, (f) 8,775, **UNEXPLAINED 0** |
| daily | 59,148 | 67,760 | 0 | 8,612 | 38,996: (a) 38,438, (d) 558, **OTHER 0** |

- **Added 14,344** = on an unchanged alias set 7,828 + on a new security 3,888 + on a security whose alias set differs 2,628.
  Dry run 3 on the same list (`gold_rebuild8.signing3.out`, 17:33Z-19:3xZ) splits the gain by CAUSE: silver growth 10,034
  (pairs the SERVED list itself builds over today's silver) + new security 3,884 + new alias 367. The two runs are 30 to 60
  minutes of silver apart; their totals differ by that growth.
- **Removed (h) 17 of 17 named, one security:** every served pair of `ICT_US_Equity`, each resting on the form `ICT` alone.
  `3.0.0_SA_CVO~Z` read all 17 (@160f1c9602): 17 of 17 are NOT about the security (Foxconn 14, Huawei 1, NTT and SAP 1,
  Luxshare ICT 1). **After the rebuild `ICT_US_Equity` holds 0 pairs.** Following those 17: 45 co-mention rows and 275 daily
  rows, all inside classes (f) and (a).
- **Mention count down: 2 rows**, both `ASML_US_Equity` (its text brand `ASML` is now refused by limb (a); it keeps the
  exact-case form). A lost-alias security; allowed.
- **Alias set differs on 41 of the 212 common securities;** 17 of them lost a served alias (9 slash tails, the decorated
  forms, the ASML brand).
- **RULE (rebuild #8): HOLDS.**

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold` (`write_gold`, never-overwrite conditional
put plus read-back), through its `build-mention` / `build-daily` CLI. No scheduled producer runs it (as every pair since #5
states; not re-measured today).

## WHAT THE GRADES COVER, AND WHAT THEY DO NOT

- Graded by `3.0.0_SA_CVO~Z`: the gain sample 29 of 30 (@399fcf7d0a); seven ticker forms refused on 0 to 2 of 10; `CAT` kept
  10 of 10 (Caterpillar, by `lib/research/identity/registrations.json`); `CSL` kept on all 42 pairs, 39 of 42 (@f6e370e6cc);
  `Meta` on gold 30 of 30 and `Lilly` anchored (@8289c4e3ed).
- **NOT sampled, stated as such:** 9 new ticker forms no sampled row reached, 20 pairs in dry run 3 (BNP 5, HEI 3, SNPS 3,
  DG 2, ED 2, GPN 2, ADBE 1, NKE 1, SHOP 1).
- **Known wrong pairs that land:** 3 of CSL's 42 are Carlisle Companies on its New York ticker.
- **Not graded:** the silver-growth pairs (the served list already attributes them); pairs resting on a lower-case hit of a
  name through the matcher's empty-alias fallback to the company name (GSK, RWE, SAP, BP_US, Nokia).
- Three securities carry only their key as a name (`CAT_US_Equity`, `CSL_AU_Equity`, `6861_JP_Equity`); the first two match
  through their ticker form, the third matches nothing.

## BLAST RADIUS

- **Written:** exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` and
  `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet`. Nothing is deleted or overwritten.
- **Readers of the newest parts** (AMGT_RESAPP's routes and pages, on every device that serves or reads them) see: 30 new
  securities with rows; about 14,300 more article pairs; `ICT_US_Equity` with none; co-mention counts and tiers moved on
  12,032 served rows; 8,612 new day rows and 38,996 changed ones. **This moves served chatter that another project reads;
  `1.0.0_SA_CTO~Z` is asked to tell `2.0.0_SA_COO~Z` and the laptop before the act (Andrew-direct ~19:0xZ, relay 31356).**
- **Scope in time:** ONE act (rebuild #8), at most 24 h after the pair is complete. NEVER-2: a ledger entry is opened at the
  start and closed at completion. The act re-runs the gate first; silver grows between signing and the act, so the act's
  counts will be larger, and the RULE, not the counts, is what must hold.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done. `round60/gold_rebuild8.act_<stamp>.json` records it, and
  `2.0.0_SA_COO~Z` is told the stamp.
- **The rule fails BEFORE the write** (the act's own gate run): STOP; nothing is written.
- **The rule fails on the WRITTEN parts:** ROLLBACK. The BEFORE rows are written back as a newer part of each table
  (`pg.write_gold`, never-overwrite), so readers see BEFORE again. Nothing is deleted.
- **A builder CLI fails between the two tables** (mention written, daily not): the act stops and says so; the issuer verifies
  and rolls the mention table back by the same write-back, in session.

## EXCLUDED

No other table; no bronze or silver write; no publisher host contacted; no collector change; no deploy, Lambda, Terraform or
portal change; no change to `ticker_refusals`, the brand list or the identity record inside this act.

## VERDICT: SIGNED (COO), pending the CTO half
