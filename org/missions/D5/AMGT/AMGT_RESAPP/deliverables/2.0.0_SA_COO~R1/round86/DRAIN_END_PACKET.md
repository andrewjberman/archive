# AMGT_RESAPP round 86 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-09 ~18:2xZ. Five of five orders terminal, all complete; round-close-check MAY-CLOSE (5 of 5, proofs 5 ok).** Nothing below is a verdict. Round 86 implements the CTO~DELL1 round-85 analysis @2b173f8e66 (R1-R5);
decomposition s.94 (+94e); issuance in this round's issue commit. R2's check half (bare years) was a direct act @f36289abfa.

## 1. Orders (each line is the order's own last status, written at its drain)

- **`AMGT-kk-1`** (name list republished with research folders): complete -- run on the laptop by `0.7.0_AE_CloudOps~AMG`, drained
  @14191e0e45, proof @fe30d75c0d VALID, NEVER-2 entry CLOSED. Guard first (AC3, @f2dbac84a4: crosswalk.main refuses to publish
  research_universe ABSENT over a served count). Same-key versioned re-put of `crosswalk/v1/2026-10-09.json` 17:20:53Z (prior
  CHWQWAM0... kept, new d3y5Cbs6...): research_universe 102 folders, 243 of 243 records kept, 204 issuer.cik. AMENDMENT 3 (CTO fold of
  UB-4d77): the three client-data removal commits printed as ancestors before the put (rc=0 x3, control rc=0; it fired rc=1 at
  f2dbac84a4 and was cleared by merging CLOUD). AMENDMENT 4 (row S1, an ISSUER check defect): AC1 admits research_universe.source,
  the reading box's path. Guard exercised end to end against the live served count (rc 2, no put).
- **`AMGT-kk-2`** (company description from the business item only): complete -- merged @246654e7a6. `FilingsProducer.draft` keeps a
  company_description item only if every cited passage sits in the business item (20-F Item 4 / 4.B, 10-K Item 1). AC1 9 of 9; negative
  control (rule off) 4 of 9 fail; AC2 291 passed. Future drafts only.
- **`AMGT-kk-3`** (five stored drafts in place): complete -- merged @23a50926ad. Five versioned overwrites of `drafting/v1/<KEY>.json`
  (ASML, BABA, NU, PBR, SAP), priors kept; pair COO @1380a0f2cd + CTO (conditions 4-5); NEVER-2 entry
  `amgt-resapp-r86-kk3-five-drafting-description-dell1` CLOSED, 5 legs. Description sentences 25 -> 1 (NU's Item 4.B); NU's 11 and 19
  restored whole (6 restored, then dropped as Item 5). Issuer live re-read: r86_description YES; outside the description 0 of 98
  restated or glued, every name at its base (ASML 16, BABA 19, NU 28, PBR 22, SAP 13). Row D1-W343-S1 INERT.
- **`AMGT-kk-4`** (issuer ids in add_security and build_universe): complete -- merged @f2c0b8c3c0. AMENDMENT 1 ruled fail-CLOSED (row
  D1-W344-S1: the first build caught a source load failure and built without issuer); a load failure now refuses with a printed reason
  (rc 6). Re-run on the merged tree: 8 passed; identity 256 passed. Row D1-W344-S2 INERT.
- **`AMGT-kk-5`** (a fresh analysis serves the filing's own sentences): complete -- merged @2cb7806aa1. Drafting serves the cited
  passage's own sentence for an item whose text is a paraphrase (draw-independent). ONE offline NU run (2 model calls, USD 0.68, no store
  write): 35 drafted, 31 served, 31 of 31 wholly verbatim, 0 restated / 0 glued. AMENDMENT 1 (row D1-W345-S1, an ISSUER check defect):
  the Y1 floor 38 predated kk-2's rule; the like-for-like floor is the stored NU draft under that rule, measured 29; arms: base draw 22
  FAIL, this draw 31 PASS. Proof re-recorded @771f66d840, pinned @5d5402764c. Rows D1-W345-S2, -S3 INERT.

## 2. The issuer's ONE REAL RUN at close

`round86/ONE_REAL_RUN_20261009.txt` (18:20:10Z, script `round86_prep/checks/r86_real_run.sh --with-ac3`), live
`HZoC2x` (hash read before and after, equal; no deploy this round):
- `r86_description` deployed: **YES** -- every served description sentence cites the business item; NU serves 1 (Item 4.B); ASML,
  BABA, PBR, SAP, AMD, NVDA empty.
- `r85_sentences` deployed outside company_description: **YES** -- 0 of 98 restated or glued; every name at its r86 base.
- `r85_crosswalk` AC1 (AMENDMENT 4 admit list): **YES** -- C1-C5, folders 102.
- `r84_listing` deployed: **YES** 3 of 3.
- `r86_yield` on kk-5's offline NU draft: **YES** -- 31 served of floor 29, 31 of 31 verbatim.
- kk-4 writers: 8 passed; kk-1 AC3 guard: 10 passed.
- `r84_store` AC1 and AC2: **YES 5 of 5**; `r82`, `r81`, `r80` deployed: YES 3/3, 2/2, 1/1 -- no regression.

## 3. JUDGMENT for L9

The CVO's read of the served description card for NU (one Item 4.B sentence) and one of the four empty names (kk-3, CTO condition 4).

## 4. Rows filed this round

D1-W343-S1; D1-W344-S1 (ruled), -S2; D1-W345-S1 (ruled), -S2, -S3; S1 (laptop ~AMG, kk-1 AC1 --admit omitted
research_universe.source; resolved by AMENDMENT 4 and D1-S17), S2 (owned-paths has no route for a non-worker seat; MSTR's lane);
D1-S18 (the scoped watchlist route ignores selected_tenant -- 200 with the caller's own list, not a refusal; a candidate cell for
round 87).

## 5. For the next round

1. D1-S18: the scoped watchlist route refuses an off-list selected_tenant like the other scoped routes.
2. AMGT_CORPUS ask (2.0.0_SA_COO~C1 msg 2900): the next scoped-API redeploy carries `lib/research/corpus/dossier.py` at box/dell1 >=
   4fc60f6444 (METHOD amgt-corpus-dossier/8); it changes 27 dossier section values in 21 names. CORPUS's halves:
   `org/missions/D5/AMGT/AMGT_CORPUS/deliverables/2.0.0_SA_COO~C1/NEVER_WIDEN_ROUND41_AQ5_SERVED_ACT.md` and
   `ledger/NEVER_WIDEN_ROUND41_AQ5_CTO_HALF.md`. Reply owed to C1: the deploy hash and function LastModified.
3. Row AMGT_RESAPP-S3 (laptop ~AMG @76f6aa9189): `lib/research/corpus/library.py` silently skips a SET but nonexistent
   `OPAL_RESEARCH_LIBRARY_ROOT` and reads the next candidate (measured: a bogus path still read 102 folders from OneDrive) -- a typo
   publishes a different library instead of refusing; a set override that does not exist should refuse.
