# TO NFRA_COMPTOOLS.PREFIX-READS — `comp-pipescript io` must see PAGINATED PREFIX reads (a coverage DEFECT, not an inconvenience)

<task_order id="NFRA_COMPTOOLS.PREFIX-READS" project="NFRA_COMPRAIL">
<issued_to>0.8.0_AE_CloudComp (comp-tool / graph lane; `.tools/**` = ANY)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T13:50Z</issued>
<dated>2026-08-19 — DATED + OWNED, awaiting spawn (MSTR). Not tonight; does not gate any live restore.</dated>
<status>complete -- DELIVERED 2026-08-25 @3b789c9d6f (ON origin/CLOUD, ancestry checked against a FETCHED ref with a firing positive control). Proof org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_COMPTOOLS.PREFIX-READS_PROOF_OF_SPEC.json = VALID rc=0 with COVERAGE CHECKED on the declared set CP-1..CP-5 (5/5 rows, 0 violations). CP-1 re-exercised live 2026-08-26 by 0.8.0_AE_CloudComp~F: 'comp-pipescript io B_00.canonical_holdings --pipeline bd' now lists SCHWAB_RPS_PREFIX as [PREFIX] [LOCAL-CONST] resolved to schwab/08335338/silver/fact_rps/. CP-4 denominator carried in the commit subject: the blindness was 150 of 356 gold scripts. STATUS-ONLY RESTAMP -- no code touched by this edit; the record was stale, the world was done. Prior status: staged -- DATED 2026-08-19, owner named, awaiting spawn</status>
<priority>P2 — Andrew: "the comp-tooling is not additive, it is foundational" (a coverage gap is a DEFECT). Found on the exact input of a client-facing restore.</priority>
<authority>CTO disposition 134609Z (spec below is CTO's; CTO arch-gates). Surfaced by 0.4.0_DS_ClientPlatform 134424Z during ADVI_BDPLAT_RESTORE.TO-1: `comp-pipescript io B_00.canonical_holdings --pipeline bd` does NOT list `SCHWAB_RPS_PREFIX` — the paginated prefix read that the whole restore turned on was INVISIBLE to the instrument.</authority>
</task_order>

## The defect
`comp-pipescript io`'s S3-read discovery enumerates KEY reads and is blind to PREFIX reads
(`list_objects_v2` / `get_paginator('list_objects_v2')` / `s3.Bucket().objects.filter(Prefix=...)`).
Same class as comp-iam's resource-style two-hop invisibility (Rule 22a): a correct exclusion of a
constructor token deletes the only textual tell. An instrument that cannot see a script's primary input
reads CLEAN on the exact question it exists to answer.

## The job (CTO spec, verbatim in substance)
Enumerate PREFIX reads as read-edges of kind `PREFIX` beside the existing KEY reads, resolving the
prefix constant through the same constant-tracing io already does for keys, and printing an
`UNRESOLVED-PREFIX` row (NEVER dropped) when the prefix is dynamic. Silence is the defect; the trace is
the bonus.

## Acceptance
- CP-1: `comp-pipescript io B_00.canonical_holdings --pipeline bd` lists `SCHWAB_RPS_PREFIX` as a PREFIX
  read-edge resolving to the constant's value.
- CP-2: positive control — a known KEY-read script's io output is UNCHANGED (diff = 0 lines).
- CP-3: MUTANT — rename the prefix constant to a dynamic expression; the row flips to `UNRESOLVED-PREFIX`
  (shown able-to-fail; never silently absent).
- CP-4: DENOMINATOR CENSUS — a one-shot count of how many gold scripts across all trees carry a paginated
  prefix read that io could NOT see before this change, printed in the proof ("N of M gold scripts") —
  so we know how blind the instrument WAS, not just that it is now less blind.
- CP-5: registry rows + `comp-manifest-check` clean; no new binary (extends the existing tool — build
  ladder rung 2).

<proof_of_spec>
  <expected_criteria>CP-1,CP-2,CP-3,CP-4,CP-5</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_COMPTOOLS.PREFIX-READS_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
Positional-id validation, check the rc.

## reporting
COO (cc CTO for the arch-gate, MSTR). Surprise channel: one line, no action.
