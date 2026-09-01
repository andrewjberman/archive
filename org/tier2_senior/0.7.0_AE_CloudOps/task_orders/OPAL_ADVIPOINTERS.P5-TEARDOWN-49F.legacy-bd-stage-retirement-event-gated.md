# TO OPAL_ADVIPOINTERS.P5-TEARDOWN-49F — retire the legacy bd stages that produced the FLIPPED keys (event-gated; consumers first, binary last) (push plan §3 row 5)

<task_order id="OPAL_ADVIPOINTERS.P5-TEARDOWN-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps~M [RE-ADDRESSED 2026-09-01T07:5xZ by the issuer 2.0.0_SA_COO, from the bare BASE. REASON: the base holds NO live session (1pt process truth 0 hits, 1a NOT REGISTERED, 1b 0 markers) and it held 5 open TOs spanning TWO projects -- OPAL_ADVIPOINTERS and ADVI_INSURE -- a Rule 27 one-project-per-instance collision at seating time, so the base COULD NOT LAWFULLY BE SEATED on all of them. This lane takes the OPAL_ADVIPOINTERS four ONLY; ADVI_INSURE.TO-S1-AE stays at the base and is re-addressed separately. Authority: Andrew-direct 2026-09-01 ~06:5xZ full-force-on-D2 drive loop, XXX.md COO row @4469fc738c. Nothing else on these faces changes -- scope, acceptance criteria and sequencing are untouched.]</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-23 onward — EVENT-GATED, not date-triggered: the framework P5 gate is "portal VERIFIED taking data in correctly AND displaying it" (a verification EVENT — the CVO cert chain + DT rendered read from row 4c — never a date). 08-23 is the earliest the event can have occurred; the date moves WITH the event, in writing.</dated>
<status>pending -- GO 160648Z @49dd8469d1; HELD ON THE FRAMEWORK P5 GATE (pre-existing law, not a new gate): acts begin only after the P4-verified event + CTO per-item gate.</status>
<priority>P2 — nothing regresses by the legacy chain continuing to run; everything regresses by tearing down early</priority>
<authority>Push plan @a2f27c8d0a §3 row 5 + rollback posture (the legacy bd chain KEEPS RUNNING until P5 attests the flipped keys served correctly for the agreed window); ratified debt-identification methodology @db365bb06c; Rule 25 (dormancy is not a deletion warrant; successor check); CLAUDE.md Rule 25-adjacent retire order: consumers first, binary last. NFRA_DEPLOYCENSUS (0.8.0, @f976c4ea79) feeds this — its classifications are input, never a deletion warrant by themselves.</authority>
</task_order>

## Objective
When the P5 gate opens: retire, stage by stage, the legacy bd chain stages that produced the keys P4
flipped — each retirement proven on the APPLIED plane with a positive control, with nothing served
regressed. Riding this TO per plan §5: the ACCRUAL RE-HOME (ownerless runner lifecycle; runner EC2
i-02448edb624a7a7cf is KEEP-UNTIL-REHOMED — the accrual bridge starts it 1-8x/day, NOT unused) and the
LEGACY-RPS HISTORY TAIL (s3://opal-data-bd/schwab/silver/rps/ carries the SOLE 2024-01-12..07-07
coverage — _RETAIN_DECLARED_EXCEPTION_RULE25.txt at the artifact; migrate the tail or Andrew writes it
off BEFORE any delete; NEVER a full --force B_00 rebuild).

## Compiler tools (three-phase)
Phase 1 per item: `comp-blast <stage/artifact>` (blast radius BEFORE retirement) + `comp-estate` for
the thread view — treating comp-estate topology claims as priors-under-test, grounded on the live
primitive. Phase 2: commit before apply; safe-apply for TF-managed destroys. Phase 3: per item, the
absence read WITH a positive control (a 404 in the wrong bucket is not evidence of absence — name the
tree searched).

## Cross-domain coordination
- shared_resource: `opal-data-bd/{gold,platinum}` legacy paths — DS base's bd platinum restore chain
  (04:42Z daily) runs THROUGH P5; MCP DS base before touching any stage in the 04:42Z chain.
- shared_resource: 0.8.0's DEPLOYCENSUS output — read it; classifications STALE-BY-NEGLECT vs
  DELIBERATELY-HELD take opposite remedies.

## Acceptance criteria
- P5T-1 GATE EVIDENCE FIRST: the TO's own first artifact is the gate citation — CVO's row-4c cert ids
  + DT's rendered-read evidence, quoted with vintages. No teardown act precedes it.
- P5T-2 PER-ITEM RETIREMENT RECORD: for each retired stage/path — consumers retired FIRST (consumer
  census with denominator: live-policy principals + deployed-code readers + route reads), binary/
  producer LAST; successor named (key-migrated vs abandoned discriminated); same-window rollback
  stated; CTO per-item gate stamp cited.
- P5T-3 APPLIED-PLANE ABSENCE + POSITIVE CONTROL: each retired path proven absent where it lived
  (list-object / get-function / rule enumeration with the pagination discipline — materialised set,
  never a page-1 count), beside a same-plane positive control that still exists.
- P5T-4 NOTHING SERVED REGRESSED: served platinum/advi reads before/after each teardown act —
  as_of and byte-size unchanged or advanced; any delta is a STOP + report, not a note.
- P5T-5 THE TWO RIDERS: accrual re-home landed (runner lifecycle owned; enforcer-scope churn resolved
  with it) OR explicitly re-dated in writing; legacy-rps tail migrated-or-written-off with Andrew's
  word cited BEFORE any rps delete.
- P5T-6 proof instance VALID rc=0 positional: ids P5T-1,P5T-2,P5T-3,P5T-4,P5T-5,P5T-6.

<proof_of_spec>
  <expected_criteria>P5T-1,P5T-2,P5T-3,P5T-4,P5T-5,P5T-6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.P5-TEARDOWN-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- Nothing before the gate event. DORMANT is not a deletion warrant. A census classification is input,
  never a warrant.
- Never touch the runner EC2 stop/terminate under this TO (carve-out stands; KEEP-UNTIL-REHOMED).
- No deletes of `json/mdpf/*` under this TO — that is OPAL_MDPFCLEANUP.TO-4's lane, already scoped.

## Reporting
COO (cc CTO, MSTR, CVO, DS base) per item at retire-complete. Surprise channel: one banked line to
COO. Session log with Compiler Tools section = deliverable.
