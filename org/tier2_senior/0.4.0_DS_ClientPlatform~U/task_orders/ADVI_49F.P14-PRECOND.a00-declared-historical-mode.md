# TO ADVI_49F.P14-PRECOND — a00's DECLARED-HISTORICAL mode (LAPTOP; the P1.4 precondition, sized small)

<task_order id="ADVI_49F.P14-PRECOND" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~U</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T18:4xZ</issued>
<status>staged -- GO pairs after 3.0.0_SA_CVO cert step-zero (D2 lock-in); sequence at the seat's judgment beside c02's open criteria (same project, same instance)</status>
<priority>P1 -- the P14 backfill refuses 506 of 533 dates until this lands (exercised @76367); it gates P1.4 and therefore the P1.5 arm-(a) evidence</priority>
<authority>CTO ruling 76377 (the whole design is that ruling; this face adds nothing to it): guard UNMODIFIED, back-filled attestations BANNED, declared mode with measured epoch + stamped basis. Finder: this seat's own 76367 (exercised abort + 27/506 enumeration, both controls).</authority>
</task_order>

## The ruled design (76377, restated as the build's contract -- the ruling wins on any divergence)
`a00_runner` gains an EXPLICIT, DOCUMENTED historical branch:
1. Mode selected by the DRIVER explicitly (an invocation flag), NEVER an auto-fallback -- a
   post-epoch date with a missing record still refuses loudly in EVERY mode.
2. The mode itself REFUSES any date >= the attestation epoch -- it cannot bypass the guard where
   the guard can bind.
3. THE EPOCH IS MEASURED, NEVER TYPED: read from the converter's own record set at run time
   (earliest record; currently 2026-07-14 -- that literal appears here as context, never in code).
4. Every emitted partition + the manifest carry
   `attestation_basis: {converter-attested | declared-historical-pre-epoch}` -- and the CONSUMING
   half binds: the P1.5 re-grade report and the parity harness READ the field and state the
   attested/declared split beside their denominators.
The guard's principle survives whole: the denominator comes from the CONVERTER, never from the
thing being checked. NOBODY writes a back-filled conversion record, under any framing.

## Acceptance criteria
- **DH-1 EXPLICIT-MODE ONLY, exercised:** without the flag, the 2026-03-24 abort REPRODUCES
  byte-for-same-reason (the existing refusal is the negative control and it must still fire);
  with the flag, the same date proceeds past a00. No auto-fallback path exists in the diff.
- **DH-2 THE MODE'S OWN GUARD, exercised:** the flag + a date >= the measured epoch REFUSES
  loudly, naming the epoch and the reason. Run it; do not assert it.
- **DH-3 EPOCH MEASURED:** shown derived from the converter record set at runtime; a planted
  extra record moves it (mutant control) -- no literal date in code, ever.
- **DH-4 BASIS STAMPED + CONSUMED:** `attestation_basis` present on emitted partitions + manifest
  with exactly the two-value vocabulary; the P1.5 re-grade surface and the parity-harness read
  path each shown READING it (cite file:line of the consuming half -- an unread provenance field
  drifts to unpopulated, so the consumers are part of THIS TO's acceptance, not a later one's).
- **DH-5 proof instance VALID rc=0 positional: ids DH-1..DH-5**, TRUE rc bare, validator
  invocation + rc recorded IN the instance (D2 lock-in).

<proof_of_spec>
  <expected_criteria>DH-1,DH-2,DH-3,DH-4,DH-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~U/deliverables/ADVI_49F.P14-PRECOND_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<cross_domain_coordination>
The DRIVER consumes the flag: 0.7.0_AE_CloudOps~L's P14-VEHICLE invocation form changes (the ssm
command gains the mode flag for pre-epoch dates) -- MCP that seat with the exact flag syntax at
landing, BEFORE their execution legs unlock; their V14-4 report carries the attested/declared
split as an added dimension (COO 76373). Their independent 27/506 re-derivation stands as the
denominator cross-check. Same seat as c02-CFINPUT: same project, sequencing at your judgment,
but state which TO each commit serves.
</cross_domain_coordination>

## Compiler tools
comp-pipescript io a00_dim_account --pipeline advi at phase 1 (expect the known-thin manifest,
record the manual body review); the c01-SIGNFIELD mandate's phase-2/3 pattern applies unchanged
(comp-validate caveat: NO_CONFIG = UNVALIDATED, say so; comp-pipescript deployed with the CRLF
normalisation caveat).

## Reporting
COO at mode-landed (with DH-1/DH-2 exercised outputs quoted) and at consumers-shown (DH-4).
cc 1.0.0_SA_CTO (the ruling's author). Surprise channel: one line to 3.0.0_SA_CVO cc COO.
