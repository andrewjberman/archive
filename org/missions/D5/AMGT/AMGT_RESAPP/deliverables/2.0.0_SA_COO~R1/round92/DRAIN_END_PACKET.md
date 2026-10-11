# AMGT_RESAPP round 92 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~10:0xZ. Five orders, all complete: `qq-1`, `qq-2`, `qq-3` merged; `qq-5` (the ONE redeploy) APPLIED 09:26:42Z and
HELD (no rollback); `qq-4` (the stored-driver write) WRITTEN for two names, a third HELD; `qq-6` (the rendered read) DONE; `qq-7` STAGED with no
order (no DEMQUE answer); `AMGT-nn-6` parked at Andrew.** Round 92 implements the CTO~DELL1 round-91 analysis `ledger/ROUND_ANALYSIS.round91.md`
@f6eb45c478 (items 1-7; msg 3649); decomposition s.100; issuance @cbd398d50e. Amendments: qq-4 AMENDMENT 1 @35d5d641be (SAP held) and AMENDMENT 2
@b75fac17a3 (AC1 takes the write set); qq-5 COO ADDENDUM 1 @1c092a4540 and CTO ADDENDUM 1 @8171f3ee77 (three more members admitted by blob).
`round-close-check.py --round 92`: orders 5, proof_ok 5 of 5, judgment 0, verdict MAY-CLOSE.

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-qq-1` | 1, 2: a minor-unit currency is never served beside a scanner price; a served currency carries no stale reason | complete, merged @5b8736efac; SERVED by qq-5 | worker ~381 @482f9dd33d, instance VALID, AC1 4 of 4, AC2 86 passed |
| `AMGT-qq-2` | 3: the candidate universe's home follows the scanner vintage; a rebuild writes a NEW dated key | complete, merged @9d4236533c; producer-side, no store write by the cell | worker ~382 @1a71eaf845, instance VALID, AC1 6 of 6, AC2 146 passed |
| `AMGT-qq-3` | 5: a located period's block stops at another year's label | complete, merged @72f6ede5e0; producer-side | worker ~383 @38de57e4fd, instance VALID, AC1 5 of 5, AC2 13 of 13 + 322 passed |
| `AMGT-qq-4` | 4: the stored drivers re-verified and spliced (ASML, BABA; SAP held) | complete; SERVED (2 analysis + 2 drafting objects overwritten, VersionIds kept) | RA1 record @9ff87dc612, ledger `amgt-resapp-r92-qq4-stored-driver-dell1` CLOSED 8 of 8, proof VALID |
| `AMGT-qq-5` | 1: the ONE redeploy, identity (pp-1) and the unit-aware currency (qq-1) | complete, SERVED: CodeSha256 `l8egBo..` -> `SOzAz9/gfKE++UOSB8qWSDJvhOsDQMoE+DDPzaFbeSI=` | RA1 record @11da95c822, ledger `amgt-resapp-r92-qq5-scoped-api-dell1` CLOSED 11 of 11, proof VALID |
| `AMGT-qq-6` issuer act | 6: FWD-38's rendered-page read on ASML, BA, ROG | DONE | `round92_prep/QQ6_RENDERED_READ_20261011.md` @d448f91b32 |
| `AMGT-qq-7` | 7: the DEMQUE answer's reader (pp-4) | STAGED, no order | request has no quote and no answer; row `MDPF_DEMQUE-D1-S10` stands |
| `AMGT-nn-6` (round 89) | mm-2 to PROD | PARKED at Andrew | call `dell1-20261011T033643Z-e7f2` |

## 2. The issuer's ONE REAL RUN at close

- **qq-5 (WORLD): re-run by the issuer, not RA1's report.** Live CodeSha256 read fresh `SOzAz9..` (LastModified 09:26:42Z). `r92_member_table.py` live against the
  merged tree's handler: 243 subjects, 2,230 members, **0 changed** (the function IS the merged code). The 180-member change set was measured BEFORE the act
  (`MEMBER_TABLE_BASELINE_vs_MERGED_20261011.json`, four classes: 144 stale reason dropped with the code kept, 12 GBp rows refused, 11 identity gains with a
  currency EUR 6 SGD 3 CHF 2, 13 identity gains without) and RA1's after-act compare names exactly those 180, 0 outside `identity`, `security_key`,
  `price_currency`, `price_currency_reason`. `r92_minor_unit_census.py` deployed: M1 0 minor-unit labels (was 12), M2 0 rows with a currency beside a stale
  reason (was 156), M3 160 major-unit rows served (floor 149; USD 125, EUR 14, CHF 11, JPY 6, SGD 3, HKD 1), M4 every held-index record currency a plain major
  or a classified minor (the CTO's added arm); `R92 MINOR-UNIT CENSUS: YES`. `r91_name_match_deployed.py` 24 candidates, 24 served, 0 leaked.
  `r89_peers_deployed.sh` and `r89_deployed_close.sh --want amgt-corpus-dossier/11`: YES, YES.
- **qq-4 (WORLD): re-run by the issuer.** Live `/thesis` `thesis_driver.points`: ASML none (was the one false point, the digit 4 of `12.4`), BABA FY2025 =
  118,028 and FY2026 = 158,132 (RMB millions, one table row), SAP the stored 2024 = 18,078 only. VersionIds read for both keys of each name: ASML and BABA moved,
  SAP not; the drafting diff against the pre-act version is `thesis_driver` and `thesis_driver_provenance` and nothing else.
  `r92_driver_reverified.py --hold SAP_GY_Equity --write-set ASML_NA_Equity,BABA_US_Equity`: R1, R2, R4, R5 PASS, `R92 DRIVER REVERIFIED: YES`.
- **qq-1, qq-2, qq-3 (LOCAL): on the merged tree.** `r92_currency_guard.py` 4 of 4, `r92_universe_home.py` 6 of 6, `r92_block_bound.py` 5 of 5,
  `r91_locator.py` 13 of 13; drain checks 515 passed (peers, filings and the price-currency api test). The qq-3 regression read, a dry-run
  re-verification of all 12 stored analysis objects with the code before and after the bound, nothing written: 0 objects differ.

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **The qq-5 blast radius was measured over `lib/` only.** RA1 stopped before upload: the build's content diff named three members the COO half had not
   admitted (`universe.py`, via `engine.py`'s top-level import, which I had called outside the closure; and two registry files `opal_naming` loads). I read the
   request path (`scoped_amgt` calls only `engine._subject_from_model_block` and `subject_cap`; the `load_candidate_universe` callers are producer paths) and the CTO
   admitted all three by blob. Cost: the apply landed 4 minutes after the STOP (STOP 09:22Z, applied 09:26:42Z); nothing had been uploaded. The registry blobs are the ones round 91's pp-6 carried live for 13 minutes with R89 YES.
2. **qq-4's AC1 could not read YES after its own write** (its expected-changed class was computed from stored != expected). RA1 found it and held the order open
   rather than flipping it; fixed by AMENDMENT 2. The writes were correct.
3. **The re-read caught a harm before the write:** SAP's three re-verified points mix EUR millions (2023, 2024) with EUR billions (2025). The verifier asks
   whether a figure's digits are in its period's block, not whether a series shares a scale. SAP was held out of the write; rows below.

## 4. JUDGMENT for L9

No JUDGMENT criterion in an order. Offered for the CVO's own re-run: `r92_minor_unit_census.py` (deployed, a few minutes), `r92_member_table.py <out.json>`
(live against the checkout; expect 0 changed), `r92_driver_reverified.py --hold SAP_GY_Equity --write-set ASML_NA_Equity,BABA_US_Equity`, and
`QQ6_RENDERED_READ_20261011.md`.
**FWD-38**: the page prints the members' vintage (universe vintage October 2nd, equal to all 12 members' `cap_vintage` on each of ASML, BA, ROG) and the
subject's own cap date (October 10th); the cross-vintage caveat sentence is served and NOT rendered. The CTO's condition (neither the date nor the why)
is not met, so no engine date line was cut. The instrument was a server render of the real PeersTab over the live payloads, not a browser walk.

## 5. Rows filed this round

Workers: `D1-W381-S1` (OBSERVATION, ARMED as filed: the hashed account-id list is absent on this device so the client-data check did not run on the code
commit; the commit is a pure function and a test; ruled an instrument gap, stands), `D1-W382-S1` (the pooled payload drops `read_at` and machine-local
fields; stands), `D1-W382-S2` (the literal AC invocation answers for the base checkout when the shell cwd resets; stands), `D1-W383-S1` (a located period whose
key is not a four-digit year keeps its unbounded block; stands). RA1: none. Issuer: **`D1-S21`** (INERT: 7 subjects list their own company among their
peers live, 10 after pp-1; the engine's exclusion is the CTO's call) and **`D1-S22`** (ARMED as filed, disarmed same turn by qq-4 AMENDMENT 1: the verifier
does not check scale across a series' points). **Disarmed by this round:** `D1-W372-S3` (qq-3), `C-S55` (qq-1 and qq-5, the census).

## 6. For the next round (the ENRICHMENT LIST's inputs)

1. **A verifier rule for a mixed-scale series (D1-S22):** a point set whose unit renderings differ by a thousand, million or billion token in the sentence
   each figure sits in is held as a set unless the excerpt states the conversion; then SAP under its own never-widen pair (the check already takes `--hold`).
2. **Self-peer by identity (D1-S21):** a member whose served key equals the subject's own is excluded (an engine rule); a round-93 cell.
3. **Render the served `cross_vintage_caveat`** under the peers table (a portal cell, DEV landing under the push law): the date is on the page, the why is not.
4. **The candidate-universe rebuild itself** (a store write under its own pair): qq-2 made it safe to run; the pool object still reads `date=2026-08-06`.
5. **qq-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6` stays Andrew's.

checked 5 of 5 orders terminal, 5 of 5 proofs VALID
