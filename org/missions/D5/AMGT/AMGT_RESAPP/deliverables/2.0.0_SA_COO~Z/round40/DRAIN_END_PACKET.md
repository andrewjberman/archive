# AMGT_RESAPP round 40 -- drain-end packet and the issuer's real run (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.48, issuance @d4b3321d71, on the CTO's round-39 analysis @269378b031. PRD v0.26
unchanged. Seven orders, seven terminal, every proof instance re-graded VALID at HEAD by this seat. Push state: LOCAL.

## 1. Orders and their terminal state

| cell | risk | holder | close carried | outer drain | result |
|---|---|---|---|---|---|
| ro-1 the export adds nothing | SERVED | ~152 | 659d2d8ddc | f9f2b1be11 | 4/4, VALID; AC4 is JUDGMENT (s.3) |
| ro-2 the P/E guard | LOCAL | ~153 | 1181991529 | a1f4cb5220 | VALID |
| ro-3 the thesis section carries the verdict | SERVED | ~154 | 5b526a3750 | f767d466e7 | VALID; AC3 is JUDGMENT (s.3) |
| ro-4 two labels that misstate | LOCAL | ~155 | c9c2f48e79 | 6eb3b02848 | VALID |
| ro-5 posture's reason without a path | LOCAL | ~156 | 0ea16e162c | 40dabe0e56 | VALID; the served page still shows the path (row Z-S272) |
| ro-6 the Deere key-form trace | LOCAL | ~157 | 30e57a3ecd | 7ffd395ea6 | VALID; the proposed identity rule is the CTO's |
| ro-7 the served acts | WORLD | `0.7.0_AE_CloudOps~A` | 9b55c93ef4, instance 2a4e94b17b | seat order | 3/3, VALID; NEVER-2 entry CLOSED 4 of 4 legs |

Worktrees ~152..~157 and their branches are removed. Portal DEV at the round's last merge is 90698c24; DEV now reads fe618e50,
which contains it (the only later commits are IRPT Holdings).

**Issuer's acts at the drain, each with its own commit:**
- **8f3f1c25df, the ro-1 x ro-3 join.** The export's company-description section carries the Thesis tab's two faces.
- **f3de463222, row Z-S271's fix.** The rich export ADDS the header's own description line and removes nothing, and
  `_print_pack` passes `description=`. ro-7 ran it as amendment B2, signed on both halves: COO at f3de463222, CTO at
  6baf45575c s.6.
- **Two hash-only restamps of the harvest prefixes, 9e983b5ea2 and 63ecfe1e20.** In both, the four prefix constants are
  byte-identical.
- **b58d5c1d53, off-round (identity closer for `2.0.0_SA_COO~X`).** An ENRICH attach adds the folder's own form.

## 2. The real run -- shared 5174 build (vite, this tree's portal at DEV fe618e50), 2026-09-25 ~00:2xZ

Two PNG sets are recorded, because the default fixture and the served plane now differ. The contract check exits 0 on both,
with every graded column PASS on all six states.

| set | data the page rendered | folder |
|---|---|---|
| fixture | `uiContractFixtures.json` (the harness default) | `real-run/` |
| served | the same file with `/thesis`, `/overlay` and `/peers` replaced by the deployed function's responses, captured 2026-09-25T00:28:15Z | `real-run-served/` (fixtures file beside it) |

**Read by the issuer, served set:**
- **Thesis.** The section shows `Description: ABSENT -- no served D-1 company_description sentence passing the
  describes-the-business test`, then "Filed detail (does not describe the business)" above the backlog sentences.
  The header shows the longer composed reason.
- **Peers.** The table reads as of 2026-09-24T2252Z (ro-7's act C). All 12 members carry P/E (trailing) and P/E (NTM): Deere
  34.70 / 29.22, median 34.90 / 29.66. ro-7.AC3 holds P/E x yield == 100 on 24 of 24.
- **Header.** It reads "BLOOMBERG SESSION: NOT REPORTED" (ro-4).
- **Posture.** It still prints the raw Windows path in Deere's Model line (row Z-S272).

**The fixture set's Thesis and Peers are STALE against the served plane.** The fixture has no verdict field ("no reason
recorded") and an older peers partition (0310Z). Grade the served set.

**Served-plane checks on the deployed bytes:**
- ro-7.AC2 reads EXPORT-COMPARE OK: figures 165/165, cites 15/15, absences 17/17, extras 0. This seat re-ran it and got the
  same result.
- ro-7.AC3 reads 24 of 24.

**Drain hygiene** (`real-run/drain.*.log`): typecheck exit 0; print, api, identity, posture and peers tests 417 passed.

**Bound.** The served set pairs the DEPLOYED DATA with the LOCAL DEV frontend. The deployed frontend is not promoted this round,
so what the deployed page shows after ro-7 is NOT measured here. Row Z-S269 measured that page at 20:35Z, before ro-7.

## 3. Judgment criteria (L9; never self-graded)

- **ro-1 AC4.** Read the served rich export `real-run-served/BA_US_Equity.rich.served.md` beside `real-run-served/*.png`.
  The worker's judgment file under `deliverables/0.9.0_WK_AMGT_RESAPP~152/judgment/` was built on the fixture, before the
  join and the Z-S271 fix.
- **ro-3 AC3.** Read the change set (`scoped_amgt.py`, `ThesisTab.tsx`) against `real-run-served/thesis.png`, and decide
  whether the section says only what its sentences are.

## 4. New investigation rows this round (L8 input)

All six are OBSERVATION and INERT:
- **Z-S269**, surfaced by `1.0.0_SA_CTO~Z`: the authenticated deployed render was obtained, and at 20:35Z its Peers table
  carried no P/E.
- **W152-S1**, surfaced by ~152: the `description=` hookup is outside the cell's paths. It was wired at f3de463222.
- **Z-S270**, surfaced by `1.0.0_SA_CTO~Z`: the deployed P/E reads BEST_PE_RATIO, and three of five members are outside the 89.
- **Z-S271**, surfaced by `0.7.0_AE_CloudOps~A`: 16 of 17 on the served plane. Fixed at f3de463222, and ro-7.AC2 reads 17 of 17.
- **Z-S272**, surfaced by this seat: the posture packs are served verbatim from the stored 2026-09-15 snapshot, so ro-5's
  producer fix reaches the page only on a posture re-run.
- **Z-S273**, surfaced by this seat: the served Peers tab carries P/E for 12 of 12 members, which bears on the CTO's
  three-valued ruling @0d568cdf51.

## 5. Carried to the CTO's round-40 analysis

- **Z-S272's remedy:** a posture re-run, which makes a model call and needs its own authorisation, OR the adapter re-derives
  the absent-source text at read time.
- **The three-valued Peers P/E ruling @0d568cdf51.** Name the surface it applies to (Z-S273).
- **ro-6's proposed identity rule:** carry the member's own `identity.resolution` through to Posture.
- **The deployed frontend.** The round's portal changes (ro-2, ro-3, ro-4) are on DEV only, and no promote was in scope.
- **The harvest-prefix hash test.** `test_harvest_prefixes` fails whenever ANY seat adds a naming-registry row. The
  constants did not move either time, so the test grades the registry, not the served prefixes.
- **Standing:** item 8 (universe provenance, `2.0.0_SA_COO~Y`), Z-S238, Z-S227, and W85-S1 / W117-S3 / W58-S2.
