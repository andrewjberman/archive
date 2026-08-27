# TO ADVI_INSURE.TO-A2-AE — the advisor-carrier capture: `relationshipdetail` `financialTeam[]` on the 49F principal (LAPTOP)

<task_order id="ADVI_INSURE.TO-A2-AE" project="ADVI_INSURE">
<decomp_ref>workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md — cell INS-a-4 (issuer amendment 2026-08-27)</decomp_ref>
<decomp_context>ONE cell. The capture was ruled route-2 (COO 76246, CTO concur 76249) on 0.4.0_DS_ClientPlatform~R's measured advisor-spine gap (advisor_basis NOT-CAPTURED 106/106); the executing seat's surface-scoped egress reading (76291, contemporaneous receipt record) was concurred by COO. This face lands the machine-readable contract BEHIND an act already properly authorized on the wire — the artifact persists, the messages scroll.</decomp_context>
<certification>PENDING 3.0.0_SA_CVO cert step-zero on the INS-a-4 amendment + this face (alternate: base 1.0.0_SA_CTO, never CRO). The act in flight predates the cert by explicit issuer disclosure; the ACCEPTANCE waits on the cert even though the capture does not.</certification>
<issued_to>0.6.0_AE_PartnerETL</issued_to>
<executor_class>AE-class (partner ETL vehicle).</executor_class>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T18:0xZ</issued>
<status>pending -- the capture is already in flight per 76291/76292 (proceed stood); this face is its contract</status>
<priority>P1 -- the advisor spine hop is TO-R1-DS AC2's named exception; this capture is what flips advisor_basis to a derived value</priority>
<placement>LAPTOP (Rule 26).</placement>
<scope_guard>ONE cell. relationshipdetail on the 49F principal ONLY, read-only, quantity scoped to the advisor-carrier need. ⛔ /account-api/* stays carved out (OPAL_TAXSMA gate). Adjacent findings: one line to 3.0.0_SA_CVO cc 2.0.0_SA_COO, keep working.</scope_guard>
⛔ <distribution>NOT TO 4.0.0_SA_CRO, at every relay (ADVI_INSURE PRD s.3).</distribution>

## Acceptance criteria

| id | criterion | layer |
|---|---|---|
| **INSA2AE-AC1** | The capture EXERCISED on the 49F principal: a LANDING or a PER-SURFACE REFUSAL are both complete answers, denominator printed either way (INS-a-3 law: a refusal names the surface, never the absence; first exercise of S4 on this principal — do not generalise a zero). **RIDER (pre-registered 2026-08-27 ~18:1xZ, COO 76310 + CVO 76307 concurring, BEFORE any byte was captured): an EMPTY `financialTeam[]` is a THIRD complete answer — a Black Diamond CONFIGURATION finding (49F's sibling `teams[]` is affirmatively empty 77/77; the population expectation was Cottonwood's bytes). It closes AC1 as measured; the advisor-basis stamp moves to a vendor-config value; the ask routes to Andrew. NO retry, NO widening. PROBE-FIRST binds execution: ONE relationship id read before the cohort is spent.** | EXERCISED |
| **INSA2AE-AC2** | Any landed bytes are BRONZE RAW, byte-for-byte, under the deployed leg's landing tree (`blackdiamond/49financial/bronze/insurance_*`) — no parquet, no transform (Rule 17a) | APPLIED |
| **INSA2AE-AC3** | SCOPE HELD, shown not asserted: the session's calls enumerated — **relationshipdetail plus its structurally-required id source (relationshipaccountdetailsearch, the certified map's sanctioned S3) and the authority mints, no other surface**; 49F principal only, read-only; zero /account-api/* calls. *[CLAUSE AMENDED 2026-08-27 ~18:5xZ by issuer on the seat's 76383: the original "relationshipdetail only" was a FALSE clause — S4's path cannot be called without an id and S3 is the map's sanctioned id source. The seat scored FAIL against the false clause rather than silently retiring it (the correct form, sibling to the INSA1AE-AC1 FAIL); this amendment makes the clause true to the certified map, and the FAIL re-scores against the amended clause. Every actual-breach guard was always satisfied.]* | EXERCISED |
| **INSA2AE-AC4** | Proof instance VALID rc=0 positional, ids INSA2AE-AC1..AC4, TRUE rc bare, validator invocation + rc recorded IN the instance (D2 lock-in) | — |

<proof_of_spec>
  <criterion id="INSA2AE-AC1" cell_refs="INS-a-4"/>
  <criterion id="INSA2AE-AC2" cell_refs="INS-a-4"/>
  <criterion id="INSA2AE-AC3" cell_refs="INS-a-4"/>
  <criterion id="INSA2AE-AC4" cell_refs="INS-a-4"/>
  <expected_criteria>INSA2AE-AC1,INSA2AE-AC2,INSA2AE-AC3,INSA2AE-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/ADVI_INSURE.TO-A2-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 4; cells: 1; every criterion carries exactly 1 cell_ref; unmapped cells 0; untraceable criteria 0.</alignment_denominators>
</proof_of_spec>

## Compiler tools
One sentence per the mandate law: this is a vendor-capture act on an already-deployed leg — no code, infra, or schema change; the deploy-side compiler runs (comp-iam, manifest parity) were discharged at TO-A1-AE's ledger and are cited, not re-run. If the capture unexpectedly requires a code change, STOP and surface — that is scope, not mechanics.

## Reporting
COO at capture-complete (landing or refusal, per-surface, denominator). On a landing, 0.4.0_DS_ClientPlatform~R's bounded AC1-plane prep consumes it. cc CTO only on a refusal that blocks the advisor spine permanently.
