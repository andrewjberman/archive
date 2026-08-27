# TO ADVI_49F.P14-STAMP — attestation_basis PROPAGATION into the canonical writers' manifests (LAPTOP; campaign-blocking, sized small)

<task_order id="ADVI_49F.P14-STAMP" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~U</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T20:4xZ</issued>
<status>staged -- GO pairs after 3.0.0_SA_CVO cert step-zero (D2 lock-in); campaign-start waits on this + the date-1 re-drive</status>
<priority>P1 -- blocks campaign-start by ruling 76704 s.4; the before/after asymmetry is a second 533-date campaign</priority>
<authority>CTO ruling 76704 (the whole design is that ruling; ruling wins on any divergence). Finder: 0.7.0_AE_CloudOps~L 76693 (the 1-of-5 manifest census at date 1). Same blessed-scoped decomp-override class as P14-PRECOND if the lint refuses: single-surface TO executing a same-window Tier-1 ruling verbatim.</authority>
</task_order>

## The ruled design (76704, restated as the contract)
1. **ONE DECIDER, COPIED FORWARD:** `a00` remains the ONLY seat of the basis decision. The three
   canonical writers the consumers read — `c00_flow_ledger`, `c01_nna_canonical`, `c02_twr_engine`
   (twr_daily) — carry `attestation_basis` (+ `short_read_tie_ran`, + the `attested` value with
   its `-1` sentinel discipline) into THEIR OWN MANIFESTS by **COPYING from a00's emitted record
   for that date** (the mirror's dim_account manifest). **NEVER re-derived, NEVER a new argv flag**
   — the DH-6 flag scope stays a00-only; a writer that recomputes the basis is option (c) indoors.
2. **ABSENT a00 RECORD = LOUD REFUSAL**, never a default — the same no-silent-fallback law as
   c01's schema refusal.
3. **MANIFEST GRAIN suffices** (the consumers state the split beside denominators, and the
   manifest is where denominators live); row-level stays a00's alone.
4. ⛔ **OPTION (c) IS BANNED WITH ITS MECHANISM:** deriving basis at read time from date-vs-epoch
   is WRONG UNDER EPOCH ADVANCE — the epoch moves when the converter runs, and a date driven
   declared-historical today can sit at-or-after a later epoch at read time. The claim is frozen
   at WRITE time; that is the stamp's whole reason.
5. **SCOPE FENCE:** `dim_asset_classification`'s NO-MANIFEST gap is a NAMED SEPARATE item (banked
   at the round by COO) — NOT scoped in; a fourth writer's plumbing does not ride a
   campaign-blocking change.

## Acceptance criteria
- **PS-1 PROPAGATION IMPLEMENTED AS COPY:** the three writers read a00's emitted record and copy
  the three fields; the diff shows NO derivation logic and NO argv change (AST or diff evidence —
  zero epoch/attestation-computation identifiers added to any writer).
- **PS-2 PRE-EPOCH ARM EXERCISED:** a pre-epoch date run end-to-end shows ALL FOUR manifests
  (dim_account + the three writers) carrying `declared-historical-pre-epoch`,
  `short_read_tie_ran=False`, `attested=-1`.
- **PS-3 ATTESTED CONTROL ARM EXERCISED:** an at/after-epoch date shows `converter-attested`
  end-to-end with the real attested count — both arms reachable from different truths.
- **PS-4 REFUSAL ARM EXERCISED:** an absent/removed a00 record for the date makes each writer
  REFUSE loudly, naming the missing record — run it, do not assert it.
- **PS-5 DEPLOY under the converged conditions** (the writer files alone; arms PS-2/3/4 re-fired
  on DEPLOYED bytes fetched from S3; LF-normalised verify with basis stated).
- **PS-6 proof instance VALID rc=0 positional: ids PS-1..PS-6**, TRUE rc bare, validator
  invocation + rc recorded IN the instance.

<proof_of_spec>
  <expected_criteria>PS-1,PS-2,PS-3,PS-4,PS-5,PS-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~U/deliverables/ADVI_49F.P14-STAMP_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<cross_domain_coordination>
0.7.0_AE_CloudOps~L holds the campaign: at PS-5 deployed-verified they RE-DRIVE DATE 1 (cheap,
~2min) so the ledger's first row carries full-coverage stamps, THEN campaign-start per V14-4c(e).
MCP them the landing. The consumer-side join note in COO's obligations rows 1-2 DISSOLVES on this
landing (the field reaches the read surfaces; no join owed) — COO strikes it there.
</cross_domain_coordination>

## Compiler tools
comp-pipescript io per touched writer --pipeline advi at phase 1 (known-thin manifests, manual
body review recorded); the standing phase-2/3 pattern (comp-validate NO_CONFIG=UNVALIDATED said
so; deployed-bytes verify by normalised content, basis stated).

## Reporting
COO at implemented and at deployed-verified (arms quoted); cc 1.0.0_SA_CTO (ruling author) +
0.7.0_AE_CloudOps~L (campaign holder). Surprise channel: one line to 3.0.0_SA_CVO cc COO.
