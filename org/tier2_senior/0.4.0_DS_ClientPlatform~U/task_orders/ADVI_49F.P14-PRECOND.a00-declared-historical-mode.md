# TO ADVI_49F.P14-PRECOND — a00's DECLARED-HISTORICAL mode (LAPTOP; the P1.4 precondition, sized small)

<task_order id="ADVI_49F.P14-PRECOND" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~U</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T18:4xZ</issued>
<status>pending -- GO received 2026-08-27T18:58Z (COO 76413; CVO cert step-zero PASS @5681c08447, decomp override BLESSED-SCOPED); execution begun by 0.4.0_DS_ClientPlatform~U</status>
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
- **DH-6 THE ENTRYPOINT PASS-THROUGH (issuer amendment 2026-08-27 ~19:4xZ on AE~L 76524 + CTO
  architecture concur 76526 — the flag had no PATH to the ruled vehicle: chain_49f_entrypoint
  builds a00's argv itself and carried zero mention of the flag at HEAD):** exactly the minimal
  three-touch form, nothing more — main() argparse gains `--declared-historical` (store_true, same
  spelling as a00's); `_stage_list` appends it to the a00 stage's argv ONLY; `:450` passes it
  through. **THE AUTO-DERIVE FORM STAYS BANNED AT EVERY LEVEL** — an entrypoint that derives the
  flag from the epoch is the auto-fallback one level up where a00 cannot see it; the DRIVER
  decides, the entrypoint only carries. Exercised both ways: flagless entrypoint invocation
  byte-preserves a00's argv (the nightly's arm); flagged pre-epoch invocation reaches a00's
  declared branch end-to-end.
- **DH-5 proof instance VALID rc=0 positional: ids DH-1..DH-5,DH-6** (widened by the same
  amendment; disclosed to `3.0.0_SA_CVO` for delta-cert, the standing form), TRUE rc bare,
  validator invocation + rc recorded IN the instance (D2 lock-in).

**DEPLOY CONDITIONS (the converged 76509+76515 instruction) EXTEND per CTO 76526:** the deploy set
becomes THE THREE FILES ALONE (a00_dim_account.py, a00_runner.py, chain_49f_entrypoint.py), and the
both-arms re-fire gains a THIRD arm — the FLAGLESS entrypoint invocation proven behavior-identical
on deployed bytes (default False -> a00 argv unchanged; the nightly document passes no new
parameter, so the nightly's safety IS that arm). LF-normalised verify unchanged. The SSM-document
half stays at `0.7.0_AE_CloudOps~L` and waits until the deployed entrypoint accepts the flag
(rendering a flag argparse rejects manufactures a vehicle-shaped failure).

<proof_of_spec>
  <expected_criteria>DH-1,DH-2,DH-3,DH-4,DH-5,DH-6</expected_criteria>
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
