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

## Result (first spawn, ended in the 07:56Z reboot before this session_log/proof commit landed)

AC1 PASS, AC2 FAIL, AC3 FAIL, AC4 PASS on the amendment-2 criteria. `<status>` was NOT flipped to
`complete`. That slot's local commit `0a5064ded5` (positioning_chain.py, build_universe.py, the
universe object, and rows `AMGT_RESAPP-Z-W25-S1..S4`) landed and drained into SITEZ at `a8be8b7452`
before the device rebooted; no code or channel edit from that slot was lost.

## Respawn (`0.9.0_WK_AMGT_RESAPP~25`, second spawn, 2026-09-16 ~14:4xZ, worktree `/c/tmp/wk-amgt-12-25`
at `de77282136`, carrying ISSUER AMENDMENTS 1-5)

**Pre-flight.** `git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-12-25`; `org/`, `.tools/` present.
Of the 8 `<paths>` lines, 6 exist; `lib/research/universe/` and `lib/research/scores/` have never
existed in this repository (`git log --all -- <path>` returns nothing for either, at any commit) --
filed as `AMGT_RESAPP-Z-W25-S5` (OBSERVATION/INERT, not blocking: they are write-grant surfaces this
cell's DELIVER never needed, since the actual work lives under `lib/research/identity/` and
`lib/research/peers/`, both present).

**Re-ran ISSUER AMENDMENT 3's re-cut AC1/AC2/AC3 verbatim, plus the unchanged AC4, against the
already-landed code and the live S3 store -- no code was re-touched.**

- **AC1** (re-cut, pinned baseline `universe/v1/2026-09-15.json@Z1IOpX7ng4KboYu172Hks3Gn0IqkRVgV`
  vs latest `universe/v1/2026-09-16.json`): baseline MEASURED 33 / UNRESOLVED 223 /
  unresolved_holdings 167; latest MEASURED 191 / UNRESOLVED 59 / unresolved_holdings 3;
  `source_values` includes `holding`; `measured_without_security_key` 0. **PASS** -- every
  amendment-3 condition met on the corrected invocation itself (no field-name mismatch this time).
- **AC2** (re-cut, code-only regex count dropping comment lines): `positioning-input` 89,
  `bare-ticker-join` 0, `unresolved-preserved` 86. **PASS** -- the amendment-2 `guess`-substring
  instrument defect (`AMGT_RESAPP-Z-W25-S1`) is gone; the repaired count reads 0 as the amendment
  predicted.
- **AC3** (re-cut, empty-subject-with-a-classification-source count, per CTO ruling msg 23440(a)):
  `peer_objects` 33 of 33, `empty` 23, `identity_defect_live` 0, `identity_defect_mutant` 1 (on
  `BA_US_Equity`, which sits in both the model-block pool and the peers engine's block dir). **PASS**
  -- all 23 empty subjects trace to a genuinely missing model block (no classification source at
  all), exactly as `AMGT_RESAPP-Z-W25-S2` found; none is a repairable identity-join defect.
- **AC4** (unchanged): `W21-S3-mentions` 20, `disarm-rows` 22 (channel grew by the new W25-S5 row),
  `my-rows` 5. **PASS** -- the disarm row is `AMGT_RESAPP-Z-W25-S3`, a NEW row citing `W21-S3`;
  its own bytes are untouched.

## Result (this run)

AC1 PASS, AC2 PASS, AC3 PASS, AC4 PASS -- all four criteria as amendment 3 re-cut them are met.
`<status>` flips to `complete`.
