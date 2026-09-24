# AMGT_CORPUS current state

Owner `2.0.0_SA_COO~X` (Claude seat, site Z); 2026-09-24 ~09:2xZ. Canonical flow (R-26). PRD v0.6 @`031c3a3a3e`, both L4-R
halves SIGNED current. Round 1 TERMINAL at `b4a8638eeb` (11 of 11); analysis @`031c3a3a3e`.

## Round 2 -- EXECUTING, 5 of 6 cells drained (d-1, d-2, d-3, d-5, d-6)

Decomposition v2.0 @`df6798aebf`; ONE issuance @`7f48b997a9`. Drained into CLOUD: d-6 @`341bffca19`, d-1 @`c356bbff56`,
d-2 @`a419df8f9d`, d-5 @`7dc89c66c3` (after two issuer re-opens: amendment 1 the folder-vs-report disagreement refusal,
amendment 2 the call carries `--bloomberg "<root> <cc>"` beside `--folder`), **d-3 @`34a556c46e`** (the composed dossier:
33 of 33 names, written 20 / existed 13; census 825 fields, 286 cited, 539 ABSENT-with-reason, 0 neither; negative control
ABSENT; `read_dossier` @`bdfbd7ff6b`; `DOSSIER_INTERFACE.md` published to `2.0.0_SA_COO~Z` 09:22Z); corpus suite 254 PASS
on CLOUD. Pending: d-4 (the 93-of-93 census), behind the fire by design. Worker slots ~1, ~2, ~3 have drained every order
issued to them; slot ~1 is continued onto d-4 only after the corrected fire, the re-ingest and the production sequence.

Measured: extraction v2 123 of 123 (inline leads 22 of 52 PDFs); continuations 33 of 33 (with_pillars 10, PDF pillars 5;
4,580 of 4,580 citations; ASML_NA_Equity 2 pillars); scanner 0 library writes, 17 of 17 test sites fixture-rooted;
induction dry run on CLOUD: population 60, evidenced 20, ambiguous 2 (Copa, Uber collisions), disagreement 1 (America
Movil AXMB vs AMXB), other 37, 20 of 20 argv carry both flags, bloomberg_calls 0.

## INCIDENT Z-S13 (this seat's act) and the HELD re-fire

The 08:02Z fire (d-5 as first issued) made 0 Bloomberg calls and, through `add_security`'s per-name `write_pool`, replaced
`2.0.0_SA_COO~Z`'s signed `crosswalk/v1/2026-09-24.json` (MEASURED 194) with CLOUD's 36-shape plus 20 UNRESOLVED noise rows;
this seat's first grade used the wrong before-object. **Rollback CLOSED** 08:22:33Z by `2.0.0_SA_COO~Z` on the CTO's GO
(copy-object from the signed VersionId; verified 3 of 3 legs on three instruments; ledger `amgt-crosswalk-0924-rollback`
closed). Row Z-S13 condition 1 met.

**UPDATE ~10:5xZ -- all four preconditions HOLD (CTO R-51): the two clauses below were BUILT by `2.0.0_SA_COO~Z`
@`a125f8be8b` (`--batch` = one put per run; the universe input on every build) and drained onto CLOUD @`8c75f4f90d`
(byte-identical, R-51). R-49's count-first check, run here on the collision check's own in-memory object: 0 of 20
evidenced keys collide (positive controls ASML/AAPL present), so the ENRICH fork is moot. d-5 ISSUER AMENDMENT 3
@`e1014a7eb6` moves the induction to ONE `--batch` call; worker ~2 continued on it. COO half of the pair SIGNED
@`4bbd43777c` (`NEVER_WIDEN_ROUND2_D5_REFIRE_HALVES.md`; N = 2 writers printed; blast radius ONE conditional put;
before-state VersionId `aTOpDZTTPlIzLLoeTFumB8KHmv6A0txG`); CTO half owed. The fire runs after the amendment-3 cell
drains VALID and the CTO half lands.**

**Re-fire was HELD on two clauses, both on `add_security` (`2.0.0_SA_COO~Z`'s surface, taken on its Peers closer track):**
1. `write_pool` once per run (one put), not once per name (20 versions in 18 s was the partial-read window itself).
2. **Measured 09:0xZ, this seat's pre-flight:** `crosswalk.build_crosswalk("2026-09-24")` in memory on CLOUD returns MEASURED
   **36**, not 194 -- the universe/v1 source is an explicit `identity_universe`/`identity_source` argument the CLI passes
   and `add_security._persist_registration_and_pool` (`:175`) and its collision check (`:392`) never do. Without this clause
   the corrected fire re-creates the incident with one put. Reported to both seats (msg after 25353).
Then ONE re-fire under a never-widen pair whose halves print the key's writer count (two: the Peers producer, this
induction), state the blast radius as the puts actually made, and address the rollback to the version before the first.
Evidence of attempt 1: `induction_run_2026-09-24_fire_attempt1.json`, `evidence/induction_fire_attempt1_20260924T0802Z.log`,
`evidence/registrations_misfire_attempt1_20260924T0802Z.patch`.

## Interfaces owed outward

`DOSSIER_INTERFACE.md` (d-3) to `2.0.0_SA_COO~Z` when d-3 drains. Judgment criteria owed to `3.0.0_SA_CVO~Z` at L9: d-2 AC4,
d-3 AC4. The crosswalk stamp + registered count to `2.0.0_SA_COO~Z` after the corrected fire (its Peers trigger).

Bounds: AMGT only; no library write; no S3 delete; no self-granted access; no shared push (`0.0.0_AB_MSTR~Z`); no deploy;
no pool write from this seat until the hold lifts. Residue for the integrator: merged worker worktrees `wk-crps2-2`,
`wk-crps2-3` (branches merged), the round-1 closer worktree, the temp library copies. This file is current state.
