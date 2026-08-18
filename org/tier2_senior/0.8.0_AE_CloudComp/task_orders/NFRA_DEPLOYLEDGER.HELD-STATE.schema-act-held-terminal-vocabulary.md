# TO NFRA_DEPLOYLEDGER.HELD-STATE — the deploy-ledger HELD state: vocabulary + predicate + re-classification (Andrew-approved ~1537Z)

<task_order id="NFRA_DEPLOYLEDGER.HELD-STATE" project="NFRA_DEPLOYLEDGER">
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:55Z</issued>
<dated>2026-08-20 — behind your PREFIX-READS (08-19); off the 49F push's critical path.</dated>
<status>staged -- GO paired; start after PREFIX-READS</status>
<priority>P2 — closes the "deliberate hold reads as abandoned-open" instrument gap (the interim never-close-a-live-hold rule stops being load-bearing)</priority>
<authority>Andrew-direct 2026-08-18 ~1537Z at the CTO terminal (verbatim: fourth section of org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260818_ALL_RECS_APPROVED_49F_END_TO_END_PUSH_AND_MDPF_UNUSED_DELETE.md): the COO/MSTR 145912Z schema proposal APPROVED — hold-reason + re-read condition required; scanner treats HELD as NOT-RED with its own age-based re-surface. CTO routing shape 164931Z (owner = comp lane; CTO gates the schema act). Rule 24 binds the vocabulary.</authority>
</task_order>

## Objective
Add HELD as a first-class state to `.tools/deploy_ledger.py`: a ledger may declare a deliberate hold
with a REQUIRED hold-reason and a REQUIRED re-read condition; `check --red` treats a well-formed HELD
as NOT-RED; a HELD past its stated re-read date surfaces as its OWN finding class (HELD-STALE-kind),
distinct from an aged OPEN — a detector that cannot tell a hold from neglect manufactures the wrong
reflex (Rule 22a's own words). Then re-classify the 4 existing HELD-STALE sentinel rows and MSTR's
LD-0420 #4 specimen under the new value, each citing its own gate/owner.

## Context
The tool took reader fixes today @0ae9d71ef5 (segment-aware close marker; bold-span-parity split) —
build on that vintage. The 4 current HELD-STALE rows: freshguard-leg4 (external/L4) ·
freshguard-leg5-v2 (sovereign PAT) · mdpf-canrte-w1a (external scheduled-run) · scty-premcp-p1
(sovereign MS token). Rule-24 statement REQUIRED in the deliverable: one axis (lifecycle), intent
stated, OPEN / HELD / terminal named as moving under different remedies (state-coherence declared).

## Compiler tools (three-phase)
Phase 1: read the existing `check --red` predicate + `_status_segments` machinery; no new instrument
where a projection serves. Phase 2: commit-gate (py_compile/ruff automatic). Phase 3: run
`check --red` before/after — the mutant discipline below IS phase 3.

## Cross-domain coordination
- shared_resource: `.tools/deploy_ledger.py` — COO landed reader fixes today; MCP COO before commit
  if your change touches `_status_segments`/`_split_fields` (last_write_owner: you for this act).
- shared_resource: the 4 sentinel ledger files + MSTR's LD-0420 specimen — re-classification edits;
  MCP MSTR (their #4 disposition text references the interim rule).

## Acceptance criteria
- HS-1 SCHEMA: HELD declared in the vocabulary with REQUIRED `hold-reason` + REQUIRED re-read
  condition (a date or a named event); a HELD missing either is NOT a valid HELD and stays RED —
  the easiest-pass route (labeling neglect HELD with no reason) is refused by construction.
- HS-2 PREDICATE: well-formed HELD = NOT-RED; HELD past its re-read date = its own finding class
  with its own line vocabulary (never merged into aged-OPEN); age-based re-surface cadence stated.
- HS-3 RULE-24 STATEMENT: axis intent + grain + state-coherence declared in the deliverable.
- HS-4 RE-CLASSIFICATION: the 4 sentinel rows + the LD-0420 #4 specimen re-expressed as valid HELD
  (reason + re-read condition quoted from each file's own gate), and `check --red` after shows them
  under the HELD class — with the mutant BOTH directions: (a) a hand-mutated HELD with its re-read
  date in the past FIRES the new class; (b) a hand-mutated reason-less HELD stays RED.
- HS-5 NOTHING ELSE MOVES: BYPASS count unchanged (0) before/after on the untouched corpus; true rc
  taken without a pipe.
- HS-6 proof instance VALID rc=0 positional: ids HS-1,HS-2,HS-3,HS-4,HS-5,HS-6.

<proof_of_spec>
  <expected_criteria>HS-1,HS-2,HS-3,HS-4,HS-5,HS-6</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_DEPLOYLEDGER.HELD-STATE_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No notification/alert machinery on the re-surface (moratorium) — the finding class prints in the
  existing check output, nothing more.
- Do not close or re-open any ledger's substance — this act re-EXPRESSES states, it never adjudicates
  them (the gates/owners in the 4 rows stand).

## Reporting
COO (cc CTO for the schema gate, MSTR for the LD row) at landed with the before/after + mutants.
Surprise channel: one banked line to COO. Session log with Compiler Tools section = deliverable.
