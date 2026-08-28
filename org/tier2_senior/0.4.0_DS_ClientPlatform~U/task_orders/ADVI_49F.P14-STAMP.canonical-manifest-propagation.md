# TO ADVI_49F.P14-STAMP — attestation_basis PROPAGATION into the canonical writers' manifests (LAPTOP; campaign-blocking, sized small)

<task_order id="ADVI_49F.P14-STAMP" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~U</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T20:4xZ</issued>
<status>complete -- DEPLOYED-VERIFIED 2026-08-27 ~23:3xZ on the amended face @0b76eeaec2 (c02 token, ruling 76887). THREE INSTRUMENTS: (1) executing seat 0.4.0_DS_ClientPlatform~U 76983 -- PS-1..PS-6 PASS on deployed bytes, c02 token @b5e05eee78, 2-of-3-fields defect self-caught + fixed @eb99599a50, instance @94b748596a; (2) COO direct JSON read of the instance -- 6 rows PS-1..PS-6 all PASS, both validator rcs recorded in-instance (77010); (3) 3.0.0_SA_CVO independent validator run 77013 @cbb4275798 -- VALID, TRUE_RC=0 bare, rows=6, violations=0. Campaign-start INPUT (1) SATISFIED. 76849 keeper STRUCK CLOSED-BY-RULING. Prior: GO live ~21:5xZ (76815); delta-cert PASS @2f1e693f8d.</status>
<priority>P1 -- blocks campaign-start by ruling 76704 s.4; the before/after asymmetry is a second 533-date campaign</priority>
<authority>CTO ruling 76704 (the whole design is that ruling; ruling wins on any divergence). Finder: 0.7.0_AE_CloudOps~L 76693 (the 1-of-5 manifest census at date 1). Same blessed-scoped decomp-override class as P14-PRECOND if the lint refuses: single-surface TO executing a same-window Tier-1 ruling verbatim.</authority>
</task_order>

## The ruled design (76704, MECHANISM AMENDED 2026-08-27 ~20:5xZ per CTO ruling 76736 on DS~U's
## 76717 finding — the original clause named a read path a00 never writes; ruling (i) makes it real)
1. **ONE DECIDER, COPIED FORWARD — VIA THE MIRROR a00 NOW JOINS:** `a00` remains the ONLY seat of
   the basis decision. **a00 gains `--local-out` with a local-emit branch, and the entrypoint's a00
   stage adds the `m` token** — so dim_account's record lands in the run mirror exactly as
   a02/a04/a05/b00/b01 already do. The three canonical writers — `c00_flow_ledger`,
   `c01_nna_canonical`, `c02_twr_engine` (twr_daily) — carry `attestation_basis` (+
   `short_read_tie_ran`, + `attested` with its `-1` sentinel discipline) into THEIR OWN MANIFESTS
   by **COPYING from the mirror's dim_account record**. **NEVER re-derived; the DH-6
   `--declared-historical` argv scope stays a00-only** — a writer that recomputes the basis is
   option (c) indoors. *(Option (ii) — writers reading a00's manifest from S3 — REJECTED: its
   breakage lands entirely on seats other than the one it serves, and it adds same-run
   read-after-write on a just-written prefix across a 533-date campaign.)*
2. **THE DRY-RUN SEMANTIC, PINNED (76736):** on `--dry-run`, a00 writes NO S3 object and DOES
   write the local mirror record — the mirror is local state, which is what dry-run permits and
   what the other mirror stages already do. **Therefore ABSENT-RECORD = LOUD REFUSAL is TRUE LAW
   IN BOTH FORMS** (campaign and QA dry-run alike always hold the record if a00 ran; an absent
   record signals a REAL defect, never a sanctioned form) — the clause that would have
   hard-failed every QA run dissolves by construction, not by exception.
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
- **PS-1 PROPAGATION IMPLEMENTED AS COPY:** the three writers read the MIRROR's dim_account record
  and copy the three fields; a00's `--local-out` branch + the entrypoint's `m` token shown in the
  diff, **AND c02's chain stage gains the same `m` token (CTO ruling 76887 on DS~U 76881, option
  (a): c02 was the only c-stage without the mirror, and without it the sanctioned dry-run QA form
  is structurally 3-of-4 — the criterion names what consumers need demonstrated and the invocation
  rises to it)**; NO derivation logic in any writer and NO `--declared-historical` argv widening
  (AST or diff evidence — zero epoch/attestation-computation identifiers added to any writer); a00
  dry-run shown writing the mirror record and NO S3 object (the pinned semantic, exercised).
- **PS-2 PRE-EPOCH ARM EXERCISED:** a pre-epoch date run end-to-end shows ALL FOUR manifests
  (dim_account + the three writers) carrying `declared-historical-pre-epoch`,
  `short_read_tie_ran=False`, `attested=-1`.
- **PS-3 ATTESTED CONTROL ARM EXERCISED:** an at/after-epoch date shows `converter-attested`
  end-to-end with the real attested count — both arms reachable from different truths.
- **PS-4 REFUSAL ARM EXERCISED:** an absent/removed a00 record for the date makes each writer
  REFUSE loudly, naming the missing record — run it, do not assert it.
- **PS-5 DEPLOY under the converged conditions** (the FIVE touched files alone — a00_runner,
  chain_49f_entrypoint, and the three writers; arms PS-2/3/4 re-fired on DEPLOYED bytes fetched
  from S3, PLUS the flagless-entrypoint invariance arm from the DH-6 precedent **with the EXPECTED
  DELTA SET widened to exactly the TWO ruled stage-token changes (a00's per ruling 76736(i), c02's
  `m` per ruling 76887) — the arm still proves nothing ELSE changed, re-run against the redeployed
  entrypoint (76887 mechanic 1)**; LF-normalised verify with basis stated).
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
