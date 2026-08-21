# TO MDPF_PROVENANCE.T-A — reader precedence: `point_class[i]` FIRST at every grain; `carried` as a known member (R-1)

<task_order id="MDPF_PROVENANCE.T-A" project="MDPF_CANPLAT">
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T13:35Z</issued>
<dated>2026-08-19 — DATED + OWNED, awaiting spawn (MSTR spawns on the date; allocation call 132245Z: spawn nothing until bd platinum closes + K3 GOs, whichever later). A dated TO with a named owner is a live item; staged-undated is rot.</dated>
<status>complete 2026-08-21 -- LANDED @edcc503e and PROMOTED TO PROD in portal v2.1.163 (commit verified on BOTH origin/DEV and origin/PROD). Proof instance VALID rc=0 unpiped over PA-1..PA-7. VALIDATED AT ISSUER: COO 180336Z ("your T-A close stands as validated") + CTO 170535Z confirming the absent-flat point_class-first reading STANDS, no overrule. Status was stale-at-staged for 3 days after the work closed; corrected by the owning seat.</status>
<priority>P2 — first of three; kills BOTH live warn classes (inflection/49f "malformed channel", Global ~3,178/load); no pixel change</priority>
<authority>CTO RULING @fc74f8f6b4 `docs/architecture/MDPF_PROVENANCE_CANONICAL_FORM_RULING_20260818.md` §2 R-1 (binding on reader); routed to COO for decomposition (§4). One two-lane contract correction under CANPLAT/CONTRACT §B3 — NOT a new project. Andrew's 08-15 presentation ruling (LD-0417) untouched: nothing here changes a pixel.</authority>
<supersedes>Amends the FE-2 AC-8 fail-safe order (@e8b1fb07): that order was correct consumer-side hardening and is now GENERALISED by the ruling — `point_class[i]` is the FIRST read at every grain, not the fallback. FE-2's post_close_correction (49F falsification) rides this TO's startup read.</supersedes>
</task_order>

## The spec is the ruling — read §0-§2 of the ruling doc before touching the file

`portal/src/lib/pairedProvenanceRead.ts`. Amend the schema SoT (`:12-14`) and the per-firm precedence
(`:163-173`) so that at EVERY grain the class read is:
1. **`point_class[i]`** when present and length-aligned to `dates[]` — the CANONICAL class carrier
   (aggregator-derived, W-7 one law).
2. A present, **well-formed class-enum** cohort slot REFINES the cohort-specific series (model slot for
   `by_model`, custody slot for the firm aggregate) and MUST derive to `point_class[i]` under the
   any-cohort rule — **a contradiction WARNS and `point_class[i]` WINS.**
3. Predates-contract `measured` ONLY when `point_class[]` is absent.
A MISSING slot = "no refinement", NOT "invalid" (no warn). An UNKNOWN STRING in `point_class[]` or a
present slot keeps the LOUD degrade (the FE-2 mutant still binds). Name-tolerant Global read:
`partner_provenance ?? cohort_provenance` (T-B renames the producer key; T-C drops the tolerance).
**`carried` becomes a KNOWN member** of the render enum (one-law vocabulary is 5-valued:
`absent | interpolated_estimate | reconstructed | carried | measured`); pixels for `carried` follow the
LD-0417 pattern (own member, measured-identical) — **RULED, no longer flagged: Andrew-direct 2026-08-18
~1500Z at the CTO terminal ("All recs approved" over the /open-calls card; record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260818_ALL_RECS_APPROVED_49F_END_TO_END_PUSH_AND_MDPF_UNUSED_DELETE.md`)
ruled `carried` renders as ORDINARY points per the LD-0417 pattern.** Amended by COO 2026-08-18 ~16:00Z
per the push-plan decomposition (handoff DO-FIRST 2).

## Acceptance criteria (each with its own instrument — a screenshot cannot see a relabel)

- PA-1: on the LIVE served inflection artifact the "malformed channel" warn count 0 (before/after
  printed; before = 1/load).
- PA-2: on the LIVE served Global artifact the `invalid point_class 'undefined' at <date>.model` warn
  count 0 (before/after printed; before ≈ 3,178/load).
- PA-3: `carried` at Global derives as `carried` (5 dates today), not `interpolated_estimate`; no warn.
- PA-4: **INVERSE MUTANT (CTO amendment 2):** a hand-crafted per-firm artifact whose well-formed class
  slot CONTRADICTS `point_class[i]` MUST produce the warn AND `point_class[i]` MUST win — shown
  able-to-fail (a reader that ignores slots entirely passes PA-1..3 and fails this).
- PA-5: the FE-2 unknown-string mutant still fires (loud degrade intact) on both `point_class[]` and slot
  paths.
- PA-6: value-affecting consumer census (FE-2 AC-7 method): zero served/rendered NUMBERS move on the live
  artifacts; band-extent set unchanged; `/frontend-dev` screenshot control pixel-identical on
  inflection + Global (charts).
- PA-7: `reconstructed` still labelled `reconstructed` at exactly the 7 inflection dates (FE-2 AC-8
  regression).

<proof_of_spec>
  <expected_criteria>PA-1,PA-2,PA-3,PA-4,PA-5,PA-6,PA-7</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/MDPF_PROVENANCE.T-A_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
Positional-id validation, check the rc: `python .tools/proof-of-spec-check.py <instance> PA-1,PA-2,PA-3,PA-4,PA-5,PA-6,PA-7`

## Portal discipline + tools
Main tree stays DEV; `comp-transform schema-check ModelPortfolios` + `ternary-audit` before commit
(new enum member = the new-mode case); extend `portal/scripts/paired-provenance-read-exercise.mjs` (the
FE-2 instrument) rather than building a second one; commit under your author line, explicit pathspecs,
unpushed (MSTR integrates). CTO reads PA-1/PA-2 before/after on the live artifacts themselves.

## reporting
COO (cc CTO, MSTR) at completion or immediately if a consumer cannot carry the precedence without a
wider refactor. Surprise channel: one line, no action.
