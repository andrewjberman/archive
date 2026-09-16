# SESSION LOG -- `0.9.0_WK_AMGT_RESAPP~25` on `AMGT_RESAPP.TO-AMGT-rk-4`

Worktree `C:/tmp/wk-amgt-12-25`, branch `wk-amgt_resapp-12-25`, cut from `SITEZ @6e4327f77f`.

## What was built

1. **`lib/research/identity/positioning_chain.py` (new, 450 lines).** The Positioning chain's
   compiled CUSIP/FIGI/SEDOL/Bloomberg-security identity, per the precedence measured in
   `org/missions/D5/AMGT/AMGT_RESAPP/ledger/L10_PREREAD.round11.md` addendum candidate 3 and
   Andrew's own terminal correction (2026-09-15 ~16:4x-17:0xZ): CUSIP (check-digit validated)
   first, else FIGI, else SEDOL+domicile, else the Bloomberg security + ETFClassifier name with
   the malformed raw value recorded. Reproduced the pre-read's exact measured numbers on the live
   gold/holding partition: 164 of 164 non-cash holdings resolved (161 CUSIP / 1 FIGI / 1 SEDOL /
   1 fallback), 47 of 47 ISIN cross-checks against `trade-security-identifiers` agreeing, 0
   disagreements.
2. **`lib/research/identity/build_universe.py` (edited).** `read_etf_plane()` now also captures
   `cusip`/`domicile`/`is_cash` from the SAME gold/holding read (no second S3 call).
   `build_union()` gained an optional `positioning_identities` parameter, tried AFTER the
   crosswalk (a holding's identifier is NEVER minted by appending a country code -- it is minted
   ONLY when BBG characteristics itself MEASURED that Bloomberg security for the exact ticker
   root). Backward compatible: both pre-existing unit arms that pass no positioning data are
   unaffected (34 of 34 tests still pass).
3. **Wrote `s3://opal-data-harvest/universe/v1/2026-09-16.json`.** MEASURED 33 -> 191, UNRESOLVED
   223 -> 59, both 3 -> 6, over a union of 250 names (89 coverage + 167 holdings - 6 both).
   Schema-valid; a guessed-key mutant fires the schema's own refusal; two dry-runs on unchanged
   inputs are byte-identical.

## What was attempted and reverted

Extended `lib/research/peers/engine.py`'s self-exclusion arm with a significant-token-overlap
check, aimed at `AMGT_RESAPP-Z-W21-S3`'s residual (a cross-listing under a different name string
ranking as its own peer). It correctly caught the named BABA/Alibaba case, but on the full
33-key population it ALSO excluded unrelated companies sharing only a generic corporate-suffix
word ("Corporation") absent from the boilerplate strip list -- e.g. Costco's peer set lost
CVS Health and Monster Beverage as members, replaced by two unrelated Canadian issuers. This is a
real regression on served output, not a bookkeeping change. Reverted byte-for-byte (confirmed
identical to the pre-edit snapshot; `git diff --stat` empty). Re-measured instead: across all 10
currently-populated peers/v1 objects, no live self-match instance exists today. Filed as
`AMGT_RESAPP-Z-W25-S3`, disarming `W21-S3` by its own named alternative.

## Two criteria refused, with grounds

- **AC2**: the literal invocation's `j.count("guess")` conflates the defect it forbids with the
  word inside "never guessed"/"NOT guessed" doctrine comments already in the pre-existing
  codebase (16 before this cell, 23 after -- more defensive language, not a new defect). Real
  construction count (`+ " US"` / `+ ' US'`) is 0, both before and after. Filed
  `AMGT_RESAPP-Z-W25-S1`.
- **AC3**: all 23 empty peer subjects trace to a missing `model_block_<key>.json` (CRO's case
  "missing subject header/classification"), not an identity-join defect this cell's crosswalk
  work can repair. Fixing them needs either a forbidden new Bloomberg call or a guessed
  ADR-to-home-line join the CTO's own L10 pre-read explicitly rules "stays open, not guessed".
  Filed `AMGT_RESAPP-Z-W25-S2`.

AC1's literal invocation also carries a field-name mismatch (`identity_status` vs the schema's
`resolution`) -- filed `AMGT_RESAPP-Z-W25-S4`, graded on the field-corrected read per this
project's own `AMGT_RESAPP-Z-W19-S1` precedent.

## Result

AC1 PASS, AC2 FAIL, AC3 FAIL, AC4 PASS. `<status>` is NOT flipped to `complete` -- the order
stays OPEN per the REFUSAL CLAUSE.
