# TO D5_ALTRESEARCH.TO-D5.1 — standing corpus ingest (LAPTOP, CRO lane, STANDING)

<task_order id="D5_ALTRESEARCH.TO-D5.1" project="D5_ALT_RESEARCH">
<issued_to>4.0.0_SA_CRO</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:50Z</issued>
<dated>STANDING -- per batch, as Andrew provides transcripts</dated>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "D5_ALTRESEARCH" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged -- GO paired; STANDING (this TO does not close on a single batch)</status>
<priority>P3 -- behind the ontology lock-down tranche, which is the fabric's critical path</priority>
<authority>D5_ALT_RESEARCH_PRD.md §6 item 1 at dispatch vintage @9ad40bc0e8 (CVO verdict @715fe724d8, ACCEPT 0 P0). Placement: LAPTOP (CTO placement ruling FINAL 193804Z -- LAPTOP = D0/D1/D2/D3/D4/D5).</authority>
</task_order>

## Objective
Ingest new research transcripts as Andrew provides them; rebuild index/analysis per batch.

## Acceptance criteria (per batch)
- **D5.1-1 RAW BYTE-FIDELITY RE-HASH** — the stored raw matches the delivered bytes. Bronze law:
  raw and untouched, whatever the source delivered, byte-for-byte.
- **D5.1-2 STRUCTURED COUNT ADVANCES** — with the before/after denominators printed.
- **D5.1-3 QUEUE REBUILT** — the materiality-ranked build queue re-derived, not hand-edited.
- **D5.1-4 proof instance VALID rc=0 positional per batch: ids D5.1-1..D5.1-4.**

<proof_of_spec>
  <expected_criteria>D5.1-1,D5.1-2,D5.1-3,D5.1-4</expected_criteria>
  <instance_path>org/tier1_exec/4.0.0_SA_CRO/deliverables/D5_ALTRESEARCH.TO-D5.1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## ⚠ CROSS-PACKAGE NOTE YOU OWN THE ANSWER TO (CVO synthesis item 2a, 193954Z)
`research_transcripts/analysis/source_{divz,idvz}_holdings_20260731.csv` are **D5's materiality
basis AND D4's holdings source** — two PRDs, one source, and until tonight neither knew the other
depended on it. D4's TO-D4b is now provenance-FIRST because of this. **When you touch those files,
the provenance finding reports to BOTH D4 and D5** under the feed-lander-owns rule. Do not re-source
or move them without saying so on both threads.

## Do not
- **NO VENDOR EGRESS.** D5's ingest is operator-provided transcripts. Any external fetch needs
  Andrew's explicit per-use word (arxiv is lifted for CRO cloud-Lambda only; that is not a general
  lift). Availability in the toolset is not authorization.

## Reporting
COO per batch. Session log w/ Compiler Tools section.
