# TO ADVI_BDPARITY.P2-CENSUS — the full-population BD parity census, inheriting the probe's design (plan §7 P2)

<task_order id="ADVI_BDPARITY.P2-CENSUS" project="ADVI_BDPARITY">
<issued_to>0.4.0_DS_ClientPlatform~C (continuity: the seat that built the probe harness, the pull vehicle read-back and BP1-6; same project, Rule 27)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-30T05:2xZ</issued>
<decomp_ref>docs/architecture/ADVI_BDPARITY plan §7 P2 (the census the probe's BP1-4 design deliverable specifies) -- <owned_cells>P2-DESIGN,P2-PULL,P2-TABLE,P2-MECH,P2-PROOF</owned_cells>; the P1-PROBE face @b462717dcc is HISTORY, not restated</decomp_ref>
<proof_of_spec>
  <expected_criteria>P2-1,P2-2,P2-3,P2-4,P2-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~C/deliverables/ADVI_BDPARITY.P2-CENSUS.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form: python .tools/proof-of-spec-check.py <instance>.json P2-1,P2-2,P2-3,P2-4,P2-5 ; print the checker's commit-ish beside the verdict -->
</proof_of_spec>
<status>staged -- P2-1 (the request-side design + manifest, NO vendor call) is GO on delivery of this face; P2-2 (the population PULL) is GATED ON ANDREW'S EXPLICIT PER-USE WORD -- availability is not authorization; the probe's 21:23Z word covered ONE pull of five accounts and is SPENT. Nothing after P2-1 starts until that word is on the record.</status>
<priority>P1 -- Andrew's own words (plan §7): "we need to 'check our work' ... at account level ... We need to get to a point where our logic is EXACT." The probe proved the instrument; the census is the product.</priority>
<authority>P1-PROBE graded COMPLETE 5 of 5 (CVO 85965); the frozen methodology @f11fb765ad + ANNOTATIONS 1-3 (CVO); the classification thresholds @9f894ec5d9 + A1 (CRO, CTO ACCEPTED frozen 85565, CVO CONFORMANCE PASS 85569); the period convention (CTO 85238, BP1-6); the fee-calendar premise A7; the parity record pinned at 03:22:17Z (issuer 85938). Nothing PERFRP-subject. Not to 4.0.0_SA_CRO unless re-spawned for a CRO-class act.</authority>
</task_order>

## Objective
Run the account-level parity census over the FULL 49F population against BD's own per-account performance outputs, per the design the probe produced (BP1-4), classifying every cell with the frozen thresholds and carrying every non-EXACT cell's mechanism -- **on ONE pull authorised by Andrew for the population**, never on the probe's spent word.

## Acceptance criteria
- **P2-1 THE DESIGN + THE REQUEST-SIDE MANIFEST (no vendor call):** population (the account universe at the census vintage, denominator printed; the 13 nine-digit keys EXCLUDED and named -- their scope is at Andrew, D3-T73-R3), the endpoints (the three the probe pulled), the periods (the ruled set; SI requested AT the anchor via a prior anchor read per account -- ANNOTATION 3's cost fact: the anchor comes from `combinedLevels[].startDate`, so SI parity per account costs a prior read or a second call; the design states which and its call count), the request window (`q_end` = the measured last trading day), the request-side hole manifest (every date in OUR gold with no partition, incl. the five 08-11..08-17 until C02-g-7 backfills them, and 2026-08-18's status), the runtime estimate at the probe's measured per-call cost, the classification thresholds frozen with the CRO's file + A1, the outcome vocabulary (COMPUTED / UNAVAILABLE-NO-COVERAGE / UNAVAILABLE-SI-WINDOW-NOT-AT-ANCHOR / VACUOUS-NO-LINKED-DAYS / UNAVAILABLE-RANGE-MISMATCH), the Dlog print with BOTH units and the per-window day columns. **Delivered to the issuer as the census plan Andrew's word is asked ON.**
- **P2-2 THE PULL (GATED on Andrew's per-use word, relayed verbatim by the issuer):** ONE pull of the population on the deployed puller (read on the running artifact first), `pull_date` its own partition, the 07-17 and 08-30 snapshots untouched (negative control), landed count vs requested printed, every account's returned ranges vs requested (range_match), bronze-raw per Rule 17a.
- **P2-3 THE TABLE:** every account x period x figure classified on the frozen thresholds, signed deltas, both units, the outcome vocabulary, days_expected / days_linked / in-window status census per cell, ONE gold vintage stated (the post-C02-g-6 "1.2" baseline unless C02-g-7 lands first -- state which); the C2 gross-leg cell read on this vintage (the exclusion lifted here, per the issuer's 85938 ruling).
- **P2-4 MECHANISMS:** every non-EXACT cell carries a named candidate (the hole, OUR-REFUSAL-DAYS n d, fee timing on the gross leg per A7's two-batch premise, the SI anchor, or UNATTRIBUTED stated); a mechanism is CONFIRMED only when its mirror brings the cell to the bar, else PARTIAL with the residual classified on its own; DAY-COUNT RESIDUAL FIRST (rule d), on differenced windows too (A1); **the population-level distribution of classes per period and per leg is the census's headline** -- printed with denominators, never a single rate.
- **P2-5** proof instance VALID rc=0 positional P2-1..P2-5 with the checker vintage printed; graded by `3.0.0_SA_CVO`.

## Do not
- ⛔ **No vendor call before Andrew's per-use word for THIS pull is on the record** (the probe's word is spent; NEVER-law on vendor egress). The issuer relays the word verbatim; the face records it.
- ⛔ No convention change under this TO (P3 is the drive-to-EXACT, CTO-gated per cell); the census measures and names.
- ⛔ No re-run of the pinned P1 table; a P2 table is a NEW artifact with its own vintage stamp.
- ⛔ Nothing PERFRP-subject; nothing to `4.0.0_SA_CRO` unless re-spawned; the 13 nine-digit keys are OUT of the population until Andrew rules their scope.

## Rule-24 note carried from P1 (CVO 85965)
`VACUOUS-NO-LINKED-DAYS` exists in the harness and NOT in `parity_period_returns.py`'s declared outcome set (whose docstring claims MECE over "the result of attempting one (account, period) cell"). At the next linker touch under this TO, the member JOINS the declared set with its four-postulate record (domain: a differenced window with zero linked days on BOTH sides; what no remedy moves: loading history does not create an account that did not exist) -- or the harness maps it onto an existing member and says so. Not a deadline; a drift to close before P2-3 prints it.

## Reporting
P2-1 to the issuer (+ CTO, CVO) as the census plan; the issuer asks Andrew for the pull word on it. P2-2 landed-count line immediately after the pull; P2-3/P2-4 at completion; surprise channel one line to `3.0.0_SA_CVO` cc issuer. Session log with Compiler Tools section = deliverable.
