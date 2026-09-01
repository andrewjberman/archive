# TO ADVI_49F.c01-SIGNFIELD — the NEW signed in-kind field + c01's defect-3 sign fix (LAPTOP; P1.2-first-half)

<task_order id="ADVI_49F.c01-SIGNFIELD" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~U</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T15:2xZ</issued>
<status>COMPLETE -- ACCEPTED 2026-08-27T17:57:44Z by 2.0.0_SA_COO (msg 76286). ⛔ WRITTEN BACK TO THIS FACE ONLY ON 2026-09-01T10:5xZ, FIVE DAYS LATE, BY THE SAME ISSUER SEAT THAT ACCEPTED IT. THE WORK WAS NEVER UNFINISHED. The acceptance existed solely as an MCP inbox message and never reached any durable carrier. || EVIDENCE, delivered by 0.4.0_DS_ClientPlatform~U on its first act after re-seating (91409) and RE-VERIFIED INDEPENDENTLY BY THE ISSUER: GIT -- this face has exactly TWO commits, fea672efd5 (the cut, 2.0.0_SA_COO) and 0412a8d6d8 (the executing seat's own fix). NO ISSUER FLIP COMMIT EXISTS. Work commits 0412a8d6d8 and bb48c4ee4c are BOTH on origin/CLOUD by merge-base --is-ancestor, run with a positive control (26be6e4161) so a broken instrument could not read as a false ON. Working tree carries no stranded predecessor edits. SOURCE AT HEAD, field-level rather than schema prose -- c00_flow_ledger.py:401-407 sets in_kind_signed_value + in_kind_direction_unresolved while :392 leaves in_kind_value UNSIGNED and untouched (SCHEMA_VERSION 1.3); c01_nna_canonical.py:50 REQUIRED_LEDGER_FIELD = in_kind_signed_value and :127 REFUSES rather than falling back to the unsigned field (SCHEMA_VERSION 1.1). The CTO 74187 contract -- unsigned stays unsigned, signed is NEW and selectable -- holds at HEAD. SERVED PLANE -- c00_flow_ledger.py s3 sha256 46ca96edded3172c == HEAD, 33,825 B both, raw-byte equal, with the PRE-FIX PARENT as negative control (7a89bc699552261f, DIFFERS). || ⛔ THIRD VARIANT OF A CARRIER DEFECT THIS ISSUER CLOSED TWICE THIS MORNING, AND IT IS THE WORST OF THE THREE: @26be6e4161 recorded variant one -- a status block FALSE at close. @69a15bf90e recorded variant two -- TRUE and NEVER TERMINAL, which keeps a TO open as effectively as false. THIS IS NEITHER: THE VERDICT WAS NEVER WRITTEN AT ALL. An MCP message is not a carrier. DISCRIMINATION, so this is not read as a lane that never writes faces back: the other three TOs in this same directory each carry a rich three-instrument complete block (P14-PRECOND COO FLIP + RAVC-4 76629 + CVO PASS @d091ce16c6; P14-STAMP DEPLOYED-VERIFIED @0b76eeaec2; c00-SIGNING DEPLOYED-VERIFIED). 3 of 4 written back. THE MISS IS SPECIFIC, NOT SYSTEMIC. ⚠ INFERRED AND NOT MEASURED, offered by the executing seat as a hypothesis and carried as one: c01-SIGNFIELD was accepted at 17:57Z as the FIRST of the launch set, and every explicit FLIPPED-COMPLETE message in that seat's archive starts at 20:01Z with c02 -- the flip-commit practice appears to POSTDATE this acceptance by two hours. Nobody has verified that. || THE COST, MEASURED AND ALREADY PAID: this issuer's tick-11 drive log @e75e79ba2f (10:41Z 2026-09-01) reads 'ADVI_49F was 3 of 3 TOs with no live owner; two lanes seated.' ONE OF THOSE TWO SEATS WAS STOOD UP TO FINISH WORK ACCEPTED FIVE DAYS EARLIER. ⭐ The stale face misled NOTHING DOWNSTREAM -- 76286 itself released the gate ('P14-VEHICLE's V14-3 gate now waits on c02-CFINPUT ALONE') and the backfill campaign started 2026-08-28T00:52Z on that release. IT MISLED THE DISPATCH. THAT IS THE HARM SHAPE WORTH RECORDING: A NEVER-WRITTEN FACE COSTS A WHOLE SEAT-INSTANTIATION, NOT A WRONG NUMBER. || PRIOR STATUS, VERBATIM: pending -- GO received 2026-08-27T16:09Z (COO 76133; Andrew released ~16:05Z @fb79e6a4cd); execution begun by 0.4.0_DS_ClientPlatform~U</status>
<priority>P1 -- critical path (D2 brief @e4f7ecbfdc phase P1); client-facing NNA sign defect live today</priority>
<authority>The ruled 08-26 remediation design: root cause @ea7c227a24; CTO 74187 (no re-sign-in-place); defect-3 record @07bcdafb2b; the assignee's own corrected end-to-end design @69b2b7678c. Andrew-direct seat word 2026-08-27 ~15:0xZ @1d761ded1f.</authority>
</task_order>

## Context — this is YOUR chain, re-seated
This seat re-instantiates the 0.4.0_DS_ClientPlatform~U remediation-author context. The design you
are executing is the one this lane authored and corrected at @69b2b7678c. Nothing here is new
architecture; this TO is the c00/c01-plane half of that ruled design, cut so the face and the
ruling cannot drift apart again.

## Scope (two acts, one plane)
1. **THE NEW SIGNED FIELD.** `flow_ledger` (producer: `data/assets/scripts/gold/runners_49f/c00_flow_ledger.py`
   / the c01 plane per your ruled design) emits a NEW field carrying the SIGNED in-kind value.
   **`in_kind_value` KEEPS its unsigned contract untouched** — CTO 74187 ruled OUT re-signing in
   place, in your own words quoted back: "that is how a change nobody scoped reaches a client
   figure." Field name + exact producer placement are yours to fix per @69b2b7678c; the contract
   (unsigned stays unsigned, signed is NEW and selectable) is not.
2. **DEFECT-3 FIX in `c01_nna_canonical.py`:** it currently spends the UNSIGNED `in_kind_value` as
   a SIGNED one — in-kind OUTFLOWS emit POSITIVE into a client-facing NNA field (@07bcdafb2b).
   Consume the new signed field.

## Explicitly NOT in this TO
- **c02 is NOT edited here.** `ADVI_49F.c02-CFINPUT` (re-based face, at this seat) is the successor
  and consumes the new signed field via the grain-parameterized filter. Gated on this TO.
- **NO history re-valuation here.** The backfill is `ADVI_49F.P14-VEHICLE` (AE lane, gated on this
  TO + c02-CFINPUT).
- **NO emitter threshold.** Brief P1.1 cites @3b2982e290, which CTO 74069 declared STRUCK on
  Andrew's ~23:4xZ no-filter word — COO is converging that conflict with CTO; it enters a TO only
  on a converged, cited word. Do not build any filter under this TO.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io c01_nna_canonical --pipeline advi</run>
      <expect>Manifest returns Group C / Order 200. KNOWN-THIN: dynamic keys mean READS/WRITES print (none detected) with the manual-review WARN -- that WARN is the expected output, not a failure. Record the manual body-review of reads/writes in the session log as the substitute the tool itself mandates.</expect>
      <if_mismatch>If the tool ERRORS (vs prints thin), STOP and surface to COO before writing.</if_mismatch>
    </step>
    <step>
      <run>comp-blast fact_trn</run>
      <expect>Consumer set for the monolith silver read feeding c00_flow_ledger enumerated; no NEW consumer of flow_ledger outside the ruled set {c01, c02, c04 dependents, nna_canonical}.</expect>
      <if_mismatch>STOP. A consumer outside the ruled set widens the backfill set -- surface to COO before writing.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-validate c01_nna_canonical --artifact &lt;produced test partition&gt;</run>
      <expect>PASS or WAIVED. NO_CONFIG/ZERO_CHECKS = UNVALIDATED -- never signal SAFE on it; say so in the report instead.</expect>
      <if_mismatch>STOP. Do not commit until ERROR-clean or the UNVALIDATED state is reported as such.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-pipescript deployed c01_nna_canonical</run>
      <expect>MATCH on the deployed artifact. KNOWN TRAP: STALE on a CRLF working-tree file vs LF S3 object is an instrument signature, not deploy evidence -- a STALE verdict is resolved by content-hash at matching normalisation, never accepted or dismissed bare.</expect>
      <if_mismatch>Resolve by normalised content compare; report which way it resolved.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

## Acceptance criteria
- **C01-1 NEW FIELD LIVE, OLD CONTRACT INTACT:** the signed field present on IC legs in a produced
  `flow_ledger` partition; `in_kind_value` byte-identical semantics (unsigned) on the same rows.
  Field-level read cited, not schema prose.
- **C01-2 SIGN CORRECT AT THE CONSUMER:** an in-kind OUTFLOW specimen emits NEGATIVE in NNA; the
  NNA delta table @e8ccd8eb77 re-read is the acceptance instrument.
- **C01-3 NEGATIVE CONTROL (non-IC plane):** non-IC rows in the same partition bit-identical
  pre/post. Movement there = unauthorized widening.
- **C01-4 NEGATIVE CONTROL (c02 plane):** `twr_daily` bit-identical after THIS TO alone — same
  instrument as c00-FIX's final-form control; movement means this TO touched the engine it is
  fenced from.
- **C01-5 DEPLOY VERIFIED** on deployed bytes resolved through the build input (Rule 22a CODE),
  never rc=0 or filename.
- **C01-6 proof instance VALID rc=0 positional: ids C01-1..C01-6.** MEASURED/RULED rows only;
  validated BY RC (never an output string), the validator invocation + its TRUE rc recorded as
  evidence IN the instance (D2 lock-in, CVO 76086 point 1).
- Session log with Compiler Tools section reproducing every `<run>` + observed result + pass/fail
  vs `<expect>`. Missing rows = REWORK.

<proof_of_spec>
  <expected_criteria>C01-1,C01-2,C01-3,C01-4,C01-5,C01-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~U/deliverables/ADVI_49F.c01-SIGNFIELD_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<cross_domain_coordination>
Shares the runners_49f chain with ADVI_49F.c02-CFINPUT (same seat, successor) and
ADVI_49F.P14-VEHICLE (0.7.0_AE_CloudOps~L -- the backfill vehicle). The backfill SET is derived
from this TO's field placement: MCP 0.7.0_AE_CloudOps~L before committing anything that changes
which scripts the full-chain pass must re-run. The ~X cohort's D11 carding reads these scripts but
edits nothing -- no coordination needed, no filings there.
</cross_domain_coordination>

<data_reprocess_scope>
Reprocess required -- BY DESIGN, and it is NOT this TO: the ruled ONE full-chain backfill over the
531 partitions {c00 -> c01 -> c02 -> c04 dependents} + nna_canonical is ADVI_49F.P14-VEHICLE,
gated on this TO + c02-CFINPUT. Until it runs, historical partitions carry the old sign -- that gap
is the declared state, not a silent one.
</data_reprocess_scope>

## Reporting
COO at field-landed, at defect-3-fixed, and at both negative controls read. cc CTO (gate). The
harness/TWR movement belongs to c02-CFINPUT, not here -- invariance HERE is the expected result.
