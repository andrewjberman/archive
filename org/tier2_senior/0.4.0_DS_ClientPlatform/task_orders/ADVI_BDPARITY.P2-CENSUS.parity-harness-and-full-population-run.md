# TO ADVI_BDPARITY.P2-CENSUS — parity classification harness (4a) + full-population run (LAPTOP)

<task_order id="ADVI_BDPARITY.P2-CENSUS" project="ADVI_BDPARITY">
<issued_to>0.4.0_DS_ClientPlatform~C (build + run); 3.0.0_SA_CVO grades; 4.0.0_SA_CRO methodology [RE-ADDRESSED 2026-08-29T16:0xZ by the issuer 2.0.0_SA_COO: DS limb moves base -> 0.4.0_DS_ClientPlatform~C. REASON: /mstr-spawn step 1d refused seating the BASE -- it holds open TOs on TWO projects -- ADVI_BDPARITY and D3_MODELOVERLAY (TO-D3.1/1b/2, bare-base assignee verified at source) -- a Rule-27 collision at seating time. [CORRECTED same turn: my first note said THREE and named ADVI_COTSNP. FALSE -- those 3 rows carry NO base assignee; they rendered under a base query because to-check --assignee is a SUBSTRING match and they name a class with no instance. The refusal stands on the D3 rows alone.] ~C measured free: 0 open TOs, 0 process-truth hits, 0 spawn markers, and POD4-enumerated so it can commit data/*/scripts/gold/*.py. Remedy named by CTO ledger row 10. Nothing else on these faces changes.]</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T20:05Z</issued>
<dated>MON-TUE 2026-08-24/25 (SS7)</dated>
<status>staged -- GO paired; follows the P1 probe</status>
<priority>P1-program</priority>
<authority>D2_ADVI_49F_E2E_PRD.md §4a + §6 row 2 at dispatch vintage @c379cb6521. PLACEMENT RE-HOMED TO LAPTOP: Andrew-direct ~19:3xZ superseded the @a02f9ff5a4 D2-analytics-sitez workstream, VERBATIM "D2 is certainly laptop fabric"; CTO's 193804Z ruling confirms D2 whole-item laptop.</authority>
</task_order>

## Objective
Build the parity classification harness per §4a and run it over the full population.

## §6 EXISTENCE CHECK — THE HARNESS IS GENUINELY NEW
No prior harness file claims exist; the classifier is a **declared-NEW build.** Phase 1 includes
`git log` on the target path — run it and report, rather than inheriting the claim.

## THE DENOMINATOR IS THE DELIVERABLE
- **Report accounts covered / total.** A census without its denominator is a count with no frame.
- **Q1 IS AT ANDREW AND DOES NOT BLOCK YOU** (decision useful by this census; the probe is
  unaffected). Proposed parity universe = accounts BD serves calculated outputs for (the
  6,145-account BD export set intersected with performance-endpoint coverage). **The ~1,925 fam-only
  accounts have NO BD ORACLE to compare against — they are listed OUT-OF-ORACLE, never counted as
  EXACT.** Build to that reading and make the universe a parameter, so Andrew's answer is a config
  change and not a re-run of the harness design.
- **OUT-OF-ORACLE IS NOT A PASS AND NOT A FAILURE.** Counting an un-comparable account as EXACT
  would inflate parity with accounts that were never measured — the single most misleading number
  this census could produce.

## ⚠ A KNOWN INPUT DEFECT IS LIVE IN THIS WINDOW
`c00` emits IC (in-kind) legs with `in_kind_value=0.0` AND `in_kind_unvalued=False`, making
per-account TWR unreliable on in-kind-funded accounts (202/202 IC legs across 4 sampled days, 42
accounts — **a 4-day FLOOR, not the universe**). `ADVI_49F.c00-FIX` is staged at DS~A. **If this
census runs before that fix lands, in-kind-funded accounts must be SEGREGATED and reported as
known-defect-affected, never folded into a parity class** — otherwise the census measures the known
break instead of parity. Coordinate with DS~A on the full-history census result before you fix your
denominator.

## Acceptance criteria
- **P2-1 CENSUS REPORT WITH DENOMINATOR** (accounts covered / total, both printed).
- **P2-2 PER-CLASS COUNTS** across C1-C4 + any NEW-named class.
- **P2-3 ZERO UNEXPLAINED NON-EXACT** — every non-EXACT account lands in a named class or a named
  new one. "Unexplained" is the failure condition.
- **P2-4 OUT-OF-ORACLE SET LISTED SEPARATELY** with its own count.
- **P2-5 IN-KIND-AFFECTED ACCOUNTS SEGREGATED** if the c00 fix has not landed (see above).
- **P2-6 proof instance VALID rc=0 positional: ids P2-1..P2-6.** MEASURED/RULED-class run rows only;
  INFERRED-class expected values are mechanically ineligible.

<proof_of_spec>
  <expected_criteria>P2-1,P2-2,P2-3,P2-4,P2-5,P2-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_BDPARITY.P2-CENSUS_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at harness-built and at census-run; CVO grades the census; CRO holds methodology. Session log
w/ Compiler Tools section = deliverable.

---
## ⚖ TWO RULINGS LANDED — 2026-08-19 ~20:12Z (Andrew; records @1e0ec3b079 + @3c8c3f1035)
1. **PARITY DENOMINATOR CONFIRMED as proposed:** universe = accounts Black Diamond serves calculated
   outputs for. The **~1,925 fam-only accounts are OUT-OF-ORACLE** and are **NEVER counted as EXACT**
   (with subclasses per CTO's record). Q1 is CLOSED — build to it, not around it.
2. **COMPARISON PERIODS RULED: QTD / YTD / 1Y / SI.** That is the census spec; do not substitute a
   different period set.
