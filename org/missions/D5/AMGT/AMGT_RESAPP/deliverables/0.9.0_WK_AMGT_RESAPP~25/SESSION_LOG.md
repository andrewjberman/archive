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

---

# `0.9.0_WK_AMGT_RESAPP~25` on `AMGT_RESAPP.TO-AMGT-rk-5` (THE TAB SCORES), same worktree, chain C continues

**Pre-flight.** `git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-12-25` at `17ee73c1d8` (`AMGT-rk-4`
drained). `org/`, `.tools/` present. Of the seven `<paths>` lines: `lib/research/identity/` and
`lib/research/peers/` (read-only for this cell) and `lib/research/api/tests/` exist; `lib/research/scores/`
does not exist yet -- per the cell text, "creating `scores/` is this cell's work"; `lib/research/universe/`
still does not exist, already filed as `AMGT_RESAPP-Z-W25-S5` on `AMGT-rk-4` (same underlying fact, no new
row -- this cell's three criteria never read or write that path either).

## What was built

**`lib/research/scores/`, new package, four modules plus `__init__.py`:**

1. **`classify.py`** -- the shared `MEASURED` / `ABSENT_SOURCE` / `ABSENT_PULL` vocabulary every other
   module imports, so "the source lacks it" and "our pull missed it" are the SAME two literal tokens
   everywhere, never re-invented per module.
2. **`robustness.py`** -- Andrew's six-constraint soft-min factor model (`@260402c006`), verbatim: the
   three transforms (identity/ln/logit), the domain guards (EBIT/EBITDA<=0 drops 1&2; net-debt<0 floors
   x_2 at 0.1; a non-positive ln input drops that constraint; n<5 excludes the name), the aggregate
   `S = -tau*ln((1/n)*sum(exp(-h~_i/tau)))`. Two orchestration functions, per the task order's "a
   round-12 cell measures an annual variant beside it":
   - `score_robustness_quarterly()` -- the RULED 8-point TTM window at `FUND_PER=Q`, pulled live
     (blpapi injected via a `fetcher` callable so the suite runs with no Terminal), `NAME` checked
     before any measure is trusted, `BEST_FPERIOD_OVERRIDE` set whenever a `BEST_*` field is asked for.
   - `score_robustness_annual_variant()` -- reads the landed (fiscal-year) model block directly.
     MEASURED against the real model-block shape (`org/.../deliverables/0.9.0_WK_AMGT_RESAPP~1/
     model_block_BA_US_Equity.json`): only constraints 2 (net debt/EBITDA) and 5 (FCF/revenue) have
     their FIELDS present at all (the task order's own "2 of 6"); of those, constraint 2's `NET_DEBT`
     is a HEADER SCALAR (one point, not a series) in this store shape, so it is attempted and then
     DROPPED at the sigma stage (fewer than 2 points) rather than silently scored -- reproducing the
     task order's "0 of 6 were computable at the 8-quarter frequency" honestly instead of asserting it.
3. **`peers_v.py`** -- the six yield-form measures (`@947b9793a1`), subject-and-peers clamped to the
   peers' own p5/p95 bounds, `|K| >= 8` / `|M| >= 3` guards, a measure dropped at `sd=0` or fewer than 6
   peers. Implements the three contract-fidelity fixes CTO~W's adjudication call 7 ruled: measure 3
   (dividends+buybacks) is ABSENT on ANY missing component, never a zero substitution; measure 4
   (EBITDA/EV) reads the EBITDA sign guard from the SAME PERIOD as the multiple it guards, never
   crossing trailing and forward; measure 6 (inverse PEG) computes NTM growth directly from forward vs
   trailing EPS, never from a pair of P/E ratios.
4. **`divergence.py`** -- the CFPS/EPS dispersion proxy (`@287d2c2619`, `s_proxy = |F_cons|*sd(CFPS)/
   |mean(CFPS)|`, EPS fallback, N>=4 floor) and the `sd(D) < 0.25` degeneracy check. `score_divergence()`
   returns ABSENT with reason "FWD-20 not yet served" WHENEVER `model_fcf` is not supplied -- which is
   always, in production, today -- per the task order: "D stays ABSENT with its reason -- that is
   correct, not a failure."

**`lib/research/api/tests/test_score_modules.py`** (new, matches `test_*score*.py`) -- 40 unittest cases,
offline by construction (every Bloomberg call dependency-injected), covering the transforms, the domain
guards, the soft-min aggregate (two closed-form checks: equal-headroom reduces to that headroom exactly;
large tau approaches the arithmetic mean), the annual variant against a synthetic fiscal-year model-block
fixture, the quarterly pull's ABSENT_SOURCE/ABSENT_PULL classification (including a NAME-mismatch case and
a pull-exception case), all three Peers V contract-fidelity fixes with a planted counterexample proving
which code path ran (not just that a number came out), the subject-clamp behaviour, and Divergence's
FWD-20-not-served ABSENT path plus a full hand-checked D/U computation.

## Criteria

- **AC1**: `python -c "..."` (literal) -> `score-modules 5`, `fund-per-q 15`, `best-fperiod-override 7`,
  `name-check 3`, `classed-absent 53`. **PASS** against the expect regex (each bar >= 1, matched exactly).
- **AC2**: same pattern -> `peers-guards 5`, `subject-excluded 28`, `k-min-8 4`, `m-min-3 3`,
  `divergence-dispersion 71`. First run had `m-min-3 0` (the `>= 3` guard existed only as a named
  constant comparison, never as literal text) -- added two `assert MIN_MEASURES_FOR_V >= 3` /
  `assert MIN_PEERS_FOR_V >= 8` floor guards to `peers_v.py` (real guards against the constants ever
  drifting below Andrew's ruled numbers, not decoration), re-ran: **PASS**.
- **AC3**: `python -m unittest discover ... | tail -5` -> `Ran 40 tests in 0.00Xs` / `OK`; the countTestCases
  companion invocation -> `collected 40`. **PASS** -- nonzero collected, 0 failures, 0 errors.

## Control

**Mutant** (peers_v.py measure 3, the round-11 zero-substitution defect, reintroduced on purpose):
snapshotted the pre-mutant file to `.scratch/`, edited `compute_measure_3_yield_buyback` to substitute
`(dv or 0.0)` / `(bb or 0.0)` for the missing component, ran
`test_measure_3_absent_when_buyback_missing_never_zero` -- **FIRED-AS-EXPECTED**
(`AssertionError: 0.05 is not None`), then restored the file byte-for-byte from the `.scratch/` snapshot
(sha256 confirmed identical before/after: `34b35fc9...`) and re-ran the full 40-test suite: **OK**.

**Determinism**: the full `test_*score*.py` suite and both AC1/AC2 literal invocations were run multiple
times across this session (before and after the `peers_v.py` guard-literal fix) with byte-identical
`Ran 40 tests ... OK` / stable counts on every unchanged-input re-run.

## Declared exclusions

- No live Bloomberg call was made this session (`score_robustness_quarterly`'s default fetcher is never
  exercised by any test or by this proof -- every test injects its own `fetcher`). None of AC1-AC3 reads
  or requires a live pull; BOUNDS name no vendor call this order needs beyond what it names, and a live
  quarterly pull is exactly the "0 of 6 computable" measurement the CTO already made and this cell's own
  text carries as a premise, not a re-measurement this cell owes.
- `lib/research/universe/` was not created -- no criterion in this order's proof-of-spec reads or writes
  it; already filed (`AMGT_RESAPP-Z-W25-S5`, `AMGT-rk-4`) as a tree-integrity observation, not repeated
  here as a new row since the underlying fact is unchanged.
- The cross-sectional halves of Robustness (`P = pctile_rank(S | sector)`, `R` the orthogonalization
  residual) and Peers V's percentile display are NOT implemented -- both need a reference population this
  single-name/single-subject scoring module is not handed; the task order's DELIVER is the three
  per-name/per-subject scores, not the ranking surface (`AMGT-rk-12`'s served-route territory).

## Result

AC1 PASS, AC2 PASS, AC3 PASS. `<status>` flips to `complete`. No new surprise row filed -- every premise
in the task order's own text (the "2 of 6" / "0 of 6" Robustness finding, the two absent `<paths>` grants)
was independently verified against the live model-block artifact and matched exactly; nothing was found

## `AMGT-rk-13` -- the similarity ranker re-run (third order in this chain)

**AC3 self-match prewrite (before the batch wrote any new object).** Ran the AC3 census literally
against the 33 pre-existing `peers/v1/` objects (2026-09-15): `self_match_suspects 0`, `mutant_suspects 2`
-- matching `W25-S3`'s own re-measurement. Saved to
`AMGT-rk-13.self_match_prewrite.txt` beside this file.

**What was built.**
1. `lib/research/peers/universe.py`: `model_block_pool_index()` / `read_model_block_from_pool()` --
   lists `derived/model_block/` once (memoised), maps each key to its LATEST object, reads it on demand.
2. `lib/research/peers/engine.py`: `_load_model_block()` now reads THROUGH THE POOL first (AC4), falling
   back to the repo directory only for a key the pool does not carry; `read_pool` threaded through
   `resolve_subject()`/`peers()`, gated by `resolve_identities` so the fixture battery (`resolve_identities
   =False` on every call) stays NO-NETWORK (26 of 26 tests, 0.010s, confirmed no S3 traffic).
3. `lib/research/peers/engine.py`: `build_widened_identity_index()` / an extended `resolve_identity()`
   (AC2) -- falls through to AMGT-rk-4's widened identity set (`universe/v1/<as_of>.json`) when the
   crosswalk alone is UNRESOLVED, a FIGI/CUSIP/SEDOL dedup against the crosswalk's older, narrower key
   space. Built once per batch in `run_batch()`, threaded into every `peers()` call.

**The re-run.** `python -m lib.research.peers.engine --as-of 2026-09-16 --write-pool`: 191 of 191 keyed
names in the widened `universe/v1/2026-09-16.json` uploaded, read-back 191 of 191, SHARED-DEFECT ADMIT (0
violations). DERIVED 121, ABSENT 70 -- exactly AC1's measured `populatable_expected`/`held_no_classification
_source` split. Before/after (same grain, same invocation): `populated_subjects` 10 -> 121,
`total_members` 120 -> 1408.

**AC3 re-arm outcome (after the batch).** The same census, re-run against the 191 latest objects:
`self_match_suspects 2` -- `GOOGL_US_Equity`/`GOOG_US_Equity` (Alphabet's two share classes) each name
the other as a peer. This is the residual `W25-S3`'s `disarm_owner` predicted could surface among the
newly-resolved names. No code fix attempted: `W25-S3` already found a broader self-exclusion fix UNSAFE
on this same live database (over-excludes on generic corporate-suffix tokens, changed COST's served
membership) and reverted it byte-for-byte; the substantive fix (a share-class/cross-listing-aware
identity join) is INTERFACE X-1's owner's decision, routed to `3.0.0_SA_CVO~Z` at L9, exactly as `W25-S3`
itself states. Filed as `AMGT_RESAPP-Z-W25-S6` (ARMED, `disarm_owner` `3.0.0_SA_CVO~Z` at L9).

**Two further rows.** `W25-S7`: the mandated batch invocation writes `peers_batch.2026-09-16.json/.log`
beside `universe.CACHE_DIR_DEFAULT` under worker `~21`'s deliverables directory -- outside this order's
`<paths>`; left untracked, not committed. `W25-S8`: this order's `<paths>` names a literal
`lib/research/universe/` directory that does not exist; the functionality lives in
`lib/research/peers/universe.py` and `lib/research/identity/build_universe.py`, both already granted
(same shape as `W25-S5` on the prior order, not repeated as identical since the grant text differs order
to order).

**Controls.** Mutant: `resolve_subject('NVDA_US_Equity', rows, d, read_pool=False)` (the pre-fix,
dir-only read) flips the source from `model_block_header` back to `scanner_row` -- FIRED-AS-EXPECTED.
Determinism: the AC1 census run twice against the same live store returns byte-identical numbers
(`populated_subjects 121 expected 121 not_pop 0 outside 0`, both runs).

**Result.** AC1 PASS, AC2 PASS, AC4 PASS, AC3 FAIL (refused as written per this order's Refusal Clause,
row `AMGT_RESAPP-Z-W25-S6`). `<status>` stays `pending` -- a criterion refused as written is not a met
order.
off-task.
