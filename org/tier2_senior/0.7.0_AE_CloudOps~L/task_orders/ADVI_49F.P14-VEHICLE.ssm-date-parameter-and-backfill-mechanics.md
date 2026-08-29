# TO ADVI_49F.P14-VEHICLE — the backfill VEHICLE (SSM `--date`) + host mechanics for the ruled 531-partition pass (LAPTOP; P1.4)

<task_order id="ADVI_49F.P14-VEHICLE" project="ADVI_49F">
<issued_to>0.7.0_AE_CloudOps~L</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-27T15:2xZ</issued>
<status>complete -- 534 of 534 dates ARTIFACT-COMPLETE, campaign ledger pin 9dd522c50d, final row 2026-08-27T09:59:16Z; zero unsuperseded; three-bucket reconciliation 0 unexplained on BOTH planes. Flipped by the issuer 2026-08-29T14:4xZ on evidence read at this seat (send-plane half independently corroborated here: 587 unique, same 7 ids, same 1 remainder, 0 post-pin, 0 unexplained) AND 3.0.0_SA_CVO acceptance at the same pin; register drift surfaced by 1.0.0_SA_CTO 82878. GO was 2026-08-27T160935Z (COO msg 76134).</status>
<priority>P1 -- the ruled backfill (brief @e4f7ecbfdc P1.4) has NO vehicle today; vehicle work is ungated, execution is gated</priority>
<authority>The ruled 08-26 remediation design (@69b2b7678c); the assignee's own measurements @4da71d969b (--date vehicle gap) + @f62e93b9bb (no stage-scoping) + 74209 (dispatcher-halt trap, safe-default parameter); 74218 (the named ad-hoc/backfill boundary, ~U concurrence). Andrew-direct seat word 2026-08-27 ~15:0xZ @1d761ded1f.</authority>
</task_order>

## Context — this is YOUR plane, re-seated
This seat re-instantiates the 0.7.0_AE_CloudOps~L publisher/backfill context. Every hazard this TO
names was measured by this lane before the drawdown; the TO exists so the ruled loop has a vehicle
and the hazards cannot be re-discovered the hard way mid-loop.

## Scope
1. **THE VEHICLE (ungated, first act):** `advi-49f-chain-dispatch` today hardcodes
   `python3 chain_49f_entrypoint.py --production` and can express no historical date. Parameterize
   it (or mint a date-taking variant per the Build Ladder — minimum change that works): rendered
   command for a historical run is **`--date {{Date}} --upload`**. `--production` is PROHIBITED for
   historical runs — it derives T-1 and would run the SAME date 531 times, every iteration green.
<!-- THE VEHICLE IS NOT YET COMPLETE FOR ALL 533 DATES -- banked 2026-08-27 ~19:4xZ by
       0.7.0_AE_CloudOps~L (assignee) on its own 76525 finding, CTO ARCHITECTURE CONCUR 76528.
       On the face because messages scroll, and a successor of this seat would otherwise
       rediscover this by 506 refusals on date 1 of the pass.

       THE GAP (measured at HEAD, not predicted): ADVI_49F.P14-PRECOND landed
       `--declared-historical` on a00_runner.py:131 -- but this TO's ruled vehicle drives
       chain_49f_entrypoint.py, which BUILDS a00's argv itself at :148,
           ("a00_dim_account", [sys.executable, "a00_runner.py", "--date", date] + u)
       where `u` (:131) is only ["--upload"] or ["--dry-run"]. grep for declared.historical in
       chain_49f_entrypoint.py at HEAD: ZERO hits; @bc585df628 did not touch that file. The flag
       has a SLOT at a00 and NO PATH from this vehicle, so all 506 pre-epoch dates would still hit
       the ORIGINAL refusal. A value needs a whole PATH, not a slot.

       SEQUENCE, ruled (CTO 76528):
         1. DS plane adds the entrypoint pass-through -- three touches, no logic: main() argparse
            store_true; _stage_list appends the flag to the a00 stage argv ONLY; :450 passes it.
            AUTO-DERIVING the flag from the epoch is BANNED AT EVERY LEVEL -- in the entrypoint it
            is the auto-fallback one level up, where a00 cannot see it. The DRIVER decides; the
            entrypoint only carries.
         2. THEN this seat adds the SSM document's SECOND PARAMETER, shape mirroring
            StartedByDispatcher (allowedValues ["true","false"], default "false"), rendering
            --declared-historical only when true, with V14-1-style live get-document acceptance.
            NOT BEFORE: a rendered flag that argparse rejects fails every pre-epoch send on argv
            rather than at the guard, which wears a vehicle defect's face.

       THE RULED DRIVER DISCIPLINE (0.4.0_DS_ClientPlatform~U 76503, adopted verbatim CTO 76528):
       set the flag ONLY for dates this seat's own enumeration says are pre-epoch; treat EITHER
       refusal (flag on a post-epoch date, or flag absent on a pre-epoch date) as a HARD STOP for
       that date. NEVER auto-retry with the flag toggled -- that re-creates the banned auto-fallback
       from the driver side, where a00 cannot see it either.

       V14-4 READS attestation_basis {converter-attested | declared-historical-pre-epoch} from the
       emitted rows + manifest -- NEVER a replay of this seat's pre-run census (the inherited-claim
       trap). The vocabulary is CLOSED in code, so an unrecognised value is a defect, never a silent
       new state. Under the declared branch the manifest's `attested` field is the SENTINEL -1, not
       a count: guard for -1 rather than summing it as a magnitude. -->

2. **DRIVER MECHANICS:** the driver ensures the host running ONCE, sends `ssm send-command`
   DIRECTLY with `StartedByDispatcher` omitted (defaults `"false"`, the safe path), and halts the
   host ITSELF once at the end. **NEVER route through `advi-49f-gold-dispatch`** — the Lambda sets
   the parameter itself and would halt the host after date 1 of 531.
3. **THE EXECUTION (gated on `ADVI_49F.c01-SIGNFIELD` + `ADVI_49F.c02-CFINPUT` landing):** ONE
   full-chain entrypoint-driven pass per affected date over the ruled set
   {c00 -> c01 -> c02 -> c04 dependents} + `nna_canonical` — full chain per date because **no
   stage-scoping exists** (@f62e93b9bb); do not build stage-scoping to avoid it (Build Ladder /
   YAGNI — the full chain is the ruled form).
   <!-- BANKED 2026-08-27 by 0.7.0_AE_CloudOps~L on 0.4.0_DS_ClientPlatform~U 76340, relayed by
        2.0.0_SA_COO 76342 ("bank it beside the D-1-pull rationale"). A SECOND, INDEPENDENT reason
        the full-chain form is load-bearing, measured on a DIFFERENT instrument than the first:
          reason 1 (D-1 pull): _pull_prev_valuation_into_mirror lives in main(), not _stage_list, so a
            stage-scoped driver would write 531 all-refused partitions GREEN.
          reason 2 (input availability, ~U's partition census): the A/B-plane inputs DO NOT EXIST over
            history -- fact_trn 538, canonical_valuation 533, flow_ledger 533, twr_daily 532, but
            ref_txn_classification 7, canonical_positions 7, dim_boundary 8, dim_calendar 8. A
            stage-scoped backfill would FAIL OUTRIGHT on historical dates, not merely emit refusals.
            The full chain re-mints those planes via a00-a07 and b00-b03 before c00 runs.
        CONSEQUENCE FOR ANY FUTURE READER: the 531 denominator is unaffected and WHICH scripts the pass
        runs is unchanged -- but the a0x/b0x re-mint is LOAD-BEARING, not incidental. Trimming stages
        off this loop trims the thing that makes the loop possible. Two independent instruments now
        agree, so this is corroboration rather than repetition. -->
4. **STANDING OF THE WRITES (74218, state it in every report):** the backfill's OWN writes take the
   named ad-hoc/backfill boundary — they repair history the scheduled path produced wrongly and
   BECOME production history. The step-(4) verification fire stays a QA instrument and is NEVER
   production evidence. Two `--date` invocations, different standing; conflating them is the
   named failure.

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-iam service advi-49f-chain-dispatch</run>
      <expect>Action-level grants for the SSM path enumerated. NECESSARY, NOT SUFFICIENT (action-grain only): for any NEW resource ARN touched, verify on the live primitive with aws iam simulate-principal-policy, ONE --resource-arns per call, positive control as a SEPARATE invocation.</expect>
      <if_mismatch>STOP. A missing grant surfaces to COO before any document edit.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript postdeps chain_49f_entrypoint --firm bd</run>
      <expect>Downstream consumer set of the chain's writes enumerated (flagless silently defaults bd -- the flag is stated deliberately). No consumer outside the ruled backfill set's read plane.</expect>
      <if_mismatch>STOP. An unlisted consumer inherits re-emitted history -- surface to COO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-iam gaps</run>
      <expect>Run ONLY if iam.tf changed: no new permission gaps. If iam.tf unchanged, record that fact -- the run is then N/A by its own trigger rule.</expect>
      <if_mismatch>STOP. Do not commit an IAM change with open gaps.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>aws ssm get-document --name advi-49f-chain-dispatch (or the variant) # rail-checked: live-document APPLIED-state read, no comp-tool reads live SSM document content</run>
      <expect>The LIVE document carries the date parameter with its allowedPattern and the rendered --date {{Date}} --upload form. DESIRED (tf/source) is not APPLIED -- this read is the acceptance substrate, not the tf diff.</expect>
      <if_mismatch>STOP. The vehicle does not exist until the live document says so.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

## Acceptance criteria
- **V14-1 VEHICLE LIVE:** the LIVE SSM document (get-document read, APPLIED state) accepts a date
  parameter and renders `--date {{Date}} --upload`; `--production` absent from the historical path.
- **V14-2 HALT TRAP RULED OUT BY EXERCISE:** >=2 consecutive direct sends on a control date with the
  parameter omitted; host stays up across both (read from instance state, not send rc).
- **V14-3 GATE HONORED:** zero backfill execution before c01-SIGNFIELD + c02-CFINPUT land — the
  dependency block below is the record.
- **V14-4 EXECUTION COVERAGE:** every affected date driven; DENOMINATOR PRINTED (n of 531 at the
  ruled count — re-derive the affected set at execution time, never copy 531 as a constant);
  per-date completion read from produced artifacts, never rc; failures enumerated by date.
- **V14-4c THE CAMPAIGN CLAUSE (issuer amendment 2026-08-27 ~20:3xZ on AE~L 76664 — the pass is a
  MULTI-DAY CAMPAIGN, not a sitting; the execution stays under THIS TO, no re-cut):**
  (a) **MEASURE ONE REAL DATE FIRST** (concurred — a pre-epoch date with the flag, a genuine
  backfill write inside the clear gate) for true per-date wall time + a real artifact-completion
  signal BEFORE committing to the shape for the rest.
  (b) **DURABLE CHECKPOINT LEDGER**, committed (org-side, this seat's folder): per-date row
  {date, basis, outcome, artifact-evidence}, written as driven — a SUCCESSOR SEAT RESUMES FROM THE
  LEDGER, never from a session's memory; restart never redoes a date whose row shows
  artifact-complete. Strictly sequential (the entrypoint mutex's refusal is a feature).
  (c) **REPORTING CADENCE:** at date-1-measured (with the projected campaign span), then per 100
  dates or per session boundary, whichever first; immediately on any refusal outside the
  enumerated expectation.
  (d) ⛔ **THE TWO SCHEDULED-FIRE SEAMS, NAMED BEFORE THEY BITE** (CTO 76669 sharpened form,
  converged): (i) **THE BLACKOUT WINDOW, a criterion not a habit** — the nightly production fire
  takes the SAME entrypoint mutex (the V14-2 exercise proved release-between-runs, NOT
  coexistence). NO campaign date STARTS within [measured per-date wall time + margin] before the
  scheduled 12:45Z fire, and the campaign RESUMES only after the nightly's completion is READ
  FROM ITS PRODUCED ARTIFACTS (the driver's own completion instrument, pointed at the production
  run). A nightly refused on the campaign's mutex is a MISSED PRODUCTION RUN wearing a defect's
  face; a campaign date refused on the nightly's is a spurious failure — NEITHER may be
  discovered live. The date-1 wall-time measurement sizes the blackout, not just the campaign.
  <!-- IMPLEMENTED + CORRECTED 2026-08-27 ~22:3xZ by 0.7.0_AE_CloudOps~L (assignee), banked here
       because the clause as written is READ as one window and it is TWO, and the permissive half
       is the one that is silent.

       WHAT BIT ME, in my own driver, 30 minutes after I committed it: the sentence a reader acts
       on is "no date STARTS within [wall + margin] BEFORE the fire", so that is what I built. But
       seconds-to-next-anchor jumps from ~0 to ~24h THE INSTANT THE ANCHOR PASSES. At 12:47Z, with
       the nightly holding the entrypoint mutex, that test reads 23.97h and says CLEAR. The guard
       is structurally blind for exactly the span of the run it exists to avoid.

       THE FIX IS ALREADY IN THIS CLAUSE -- "RESUMES only after the nightly's completion is READ
       FROM ITS PRODUCED ARTIFACTS". I had even written the artifact-reading function, then called
       it only to PRINT inside the pause branch and never to GATE resumption. A check that is
       computed and not consumed reads as rigour and enforces nothing; it is the same class as a
       declared-but-unrun falsifier, and CLAUDE.md s.4's consuming-half law at its smallest grain.

       SO THE CRITERION, STATED AS THE TWO WINDOWS AN IMPLEMENTER MUST BUILD:
         PRE-FIRE   held when [wall + margin] does not fit before the anchor.
         POST-FIRE  held FROM the anchor UNTIL the nightly's own artifact is read. The schedule
                    having FIRED is not evidence; only the artifact is.
         OVERDUE    past a bounded grace (2h as built) it STOPS and asks a human -- "not finished
                    yet" and "never ran" are indistinguishable from here, and only one is safe to
                    drive through.
         DISABLED   nightly not ENABLED on the applied plane -> no contender, campaign runs.
                    UNREADABLE is treated as ENABLED: an unreadable schedule is exactly when an
                    assumption is least affordable.
       Exercised at 7 clock positions + the disabled arm, all correct. One of MY controls was wrong
       before the code was (I expected 12:20Z HELD; it is correctly CLEAR, 25 min > the 16.9 min
       budget) -- recorded because an expectation that was wrong is data about the instrument.

       MEASURED, and it sizes the blackout's other half: the nightly's OWN wall time is ~2.6 min
       (twr_daily date=2026-08-26 written 12:47:36Z against the 12:45:00Z anchor).

       BLAST RADIUS, measured on BOTH trigger planes so the single-window design is justified
       rather than assumed: only advi-49f-gold-floor cron(45 12) UTC contends (advi-49f-publisher
       cron(15 13) is DISABLED -- a latent SECOND window if anyone enables it).
       bd-49f-session-complete keys on document-name `opal-bd-49f-session-fetch`, NOT
       advi-49f-chain-dispatch, so the campaign's sends CANNOT fire {mode: runner-run};
       opal-49f-served-guard-on-write keys on a different bucket+key. -->
  (ii) the nightly's
  DISPATCHER sets StartedByDispatcher=true and HALTS THE HOST after its run — mid-campaign, the
  driver EXPECTS that halt, restarts the host, and resumes from the ledger; a halted host is a
  scheduled event, never a campaign failure.
  (e) Campaign-start = when the seat judges the date-1 measurement supports the shape; no further
  word needed. Delta-cert of this clause: `3.0.0_SA_CVO`, the standing form.
  <!-- (e) AMENDED BY THE JOINT MATERIALITY DECISION, banked 2026-08-27 ~22:1xZ by
       0.7.0_AE_CloudOps~L on 2.0.0_SA_COO 76783 + 1.0.0_SA_CTO 76746, semantics pinned by COO
       76863. Campaign-start now reads THREE inputs, all at the FACES:
         (1) ADVI_49F.P14-STAMP  TERMINAL ON ITS FACE -- and 76863 pins that this means the
             COMPLETION FLIP, *not* the deploy leg's report. The deploy is verified @9644276a3a
             while the face still reads pending; the FACE is the operative read.
         (2) ADVI_49F.c00-SIGNING TERMINAL -- deployed-verified for the FC sub-class OR
             closed-as-impossible with the TR disposition recorded. Either is terminal.
             (SG-2b already answered NEGATIVE at n=49 @c46d26a059: TR does not late-join.)
         (3) THE DATE-1 RE-DRIVE, run AFTER (1) and (2) so the ledger's first row carries
             full-coverage stamps. Running it before is discarded work.
       All three, then this seat's (e) judgment. Nothing else about the driver, ledger or blackout
       changes. -->

- **THE CAMPAIGN VEHICLE, BUILT 2026-08-27 ~22:2xZ (V14-4c(b) discharged as artifacts, not design):**
  - `org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.P14-VEHICLE_CAMPAIGN_DRIVER.py`
    @6914a73fd1 (+ blackout fix @42ce31beec). `--plan` is the DEFAULT; `--run` REFUSES without
    `--confirm-campaign-start` because these writes take the 74218 boundary and BECOME production
    history. `--status` reads the ledger without touching AWS.
  - LEDGER `ADVI_49F.P14-VEHICLE_CAMPAIGN_LEDGER.jsonl` (same dir) -- append-only, one row per date
    {date, basis, outcome, artifact-evidence, command_id, wall}; last row wins; a torn line WARNs
    rather than vanishing. A successor RESUMES FROM THIS FILE. Dates whose row reads
    ARTIFACT-COMPLETE are never redone.
  - ⛔ THE COMPLETION ORACLE IS THE ARTIFACTS, and it REFUSES TODAY'S STATE BY CONSTRUCTION. Three
    discriminators, each exercised with today's wrong state as the firing negative: basis-presence
    (3 of 4 manifests carry no `attestation_basis` until P14-STAMP lands), freshness (LastModified
    strictly after this run's send -- the control date also had 2 objects, so PRESENCE IS NOT
    REPAIR and COUNT IS NOT AN ORACLE), and branch-agreement (the stamp must equal the branch the
    driver drove). `attested` is guarded as the -1 SENTINEL, never summed. CONSEQUENCE: the driver
    CANNOT mark a date complete before P14-STAMP -- the gate lives in the instrument, not only in
    this seat's judgment.
  - The flag is decided from `ADVI_49F.P14-VEHICLE_A00_ATTESTATION_REDERIVATION.py::derive()` and
    NO other predicate -- a second transcription of a00's gate is how two artifacts drift while
    both look right.
- **APPLIED-ENTRYPOINT RE-VERIFICATION (this seat's named step, CTO 76738) PASSED @a52a2224ce** on
  DEPLOYED bytes (`s3://opal-data-49financial/_code/`, LastModified 22:08:00Z): a00-only argv scope
  (1 of 15 stages carries the flag), mirror membership (a00 joins the mirror per ruling (i)), no
  auto-derive (AST-only), and ARGV SURFACE AGREEMENT (deployed a00 accepts all 5 options the
  entrypoint sends -- without this, `--local-out` would have killed all 533 dates on argv rather
  than at the guard). Every check carries a negative control that FIRES. Re-runnable:
  `ADVI_49F.P14-VEHICLE_APPLIED_ENTRYPOINT_VERIFY.py`, rc=0 read bare.
  LIMIT STATED: this verifies what the deployed bytes DO. It does NOT claim they match a committed
  source vintage -- that identity is the DS lane's deploy leg (COO 76863 confirmed the division).
- ⛔ **SUBSTRATE CARD ROW 6 -- KEY/IDENTITY SPACE. THE HOST, NAMED, because it was the one thing
  never carded and it refused date 1 on the first live send** (added 2026-08-28 ~00:3xZ by
  0.7.0_AE_CloudOps~L per `1.0.0_SA_CTO` 77108 item 5 + `2.0.0_SA_COO` 77114 item 4(ii);
  `3.0.0_SA_CVO` delta-certs in the standing form):

  | field | value |
  |---|---|
  | HOST | `i-01003b035d2988dfb` = **bd-gold-layer-runner** (P2D-4 host ruling, `infra/aws/terraform/opal-assets/advi_49f_floor.tf:52`) |
  | ROLE | `bd-exporter-ec2-role` via `bd-exporter-profile`; grant is inline policy **advi-49f-chain-access** |
  | GRANT | `s3:GetObject`+`s3:PutObject` on `opal-data-49financial/gold/advi/*`; `s3:GetObject` on `_code/*`; `s3:ListBucket` on the bucket |
  | DOCUMENT | `advi-49f-chain-dispatch` DocumentVersion 3 |
  | OWNER | the host + role are the 49F floor's, NOT this TO's -- this vehicle BORROWS a proven identity and must never widen it |

  **WHAT THIS ROW COST BEFORE IT EXISTED:** the driver's `INSTANCE_ID` read
  `i-0fa1846f04ed7e337  # bd-49f-auto-login` -- and **the comment was TRUE**. That id really is
  the BD auto-login box; the constant was correct about what it NAMED and wrong about what it
  should have NAMED, so every reading of the line confirmed it. Date 1 refused rc=2 on
  `s3:ListBucket` AccessDenied: the login box's role is firm-separated least-privilege and has
  never held `opal-data-49financial` (`infra/aws/terraform/bd-49f-auto-login/iam.tf:8-11`), so
  the `aws s3 sync` of `_code/` returned nothing and `chain_49f_entrypoint.py` was not on the box.
  ⛔ **THE FIX IS THE RE-POINT AND NOTHING ELSE. NO IAM CHANGE ANYWHERE** -- widening the login
  box to a firm bucket is refused outright, and the runner needs nothing added. A seat that
  "fixes" an AccessDenied by granting the denied permission would have handed a session-login box
  permanent read/write on the whole 49F data estate.
  ⛔ **EVERY EARLIER PROBE MEASURED THE DOCUMENT; NONE MEASURED THE HOST.** V14-1 (get-document)
  and V14-2 (halt trap) are both sound about the DOCUMENT and both were exercised against the
  WRONG BOX. A document-plane instrument cannot see an identity-plane defect, and the two planes
  were never distinguished until a live send crossed both.
  ✅ **V14-2 RE-EXERCISED AND RESTORED 2026-08-28 00:42:50-00:47Z on `i-01003b035d2988dfb`**, in
  the order `2.0.0_SA_COO` 77146 sequenced (date-1 oracle read -> V14-2 -> then (e), so (e) is
  FINAL and not provisional). rc=0 read bare. SUBJECT CONTROL first, because the whole defect was
  a wrong subject: `describe-instances` returns `Name=bd-gold-layer-runner` before any send.
  Two consecutive sends with `StartedByDispatcher` OMITTED -- Success rc=0 at 121.2s and 105.6s --
  and the host read `running` from **ec2 instance state, never from send rc**, across all THREE
  reads (before / after 1 / after 2; denominator printed). CONDITIONAL-HALT ARM, new with the
  re-point: `_DRIVER_STARTED_HOST=False`, so `halt_host()` REFUSED to stop the shared runner and
  it read `running` afterwards. The old V14-2 evidence is superseded, not deleted.
  ⚠ **CONSEQUENCE OF THE RE-POINT, not a separate finding: the new host is SHARED.**
  `bd-exporter-ec2-role` also carries schwab, `opal-data-bd`, `opal-data-inf`, `opal-data-assets`
  and the platinum publisher, so other lanes run on this box. The driver's `halt_host()` is now
  CONDITIONAL -- it halts only a host it started itself, and leaves a host found running alone,
  because stopping it could kill another lane's in-flight run that this driver cannot see. That
  is CTO 77108 item 3(b)'s own "only when the driver started it" applied to the STOP, which is the
  destructive half. `StartedByDispatcher` stays OMITTED on every send: sending it true would
  self-halt after EVERY date, which is the 74209 dispatcher-halt trap this TO already forbids.

- **V14-5 ACCEPTANCE RE-READS GREEN (joint with 0.4.0_DS_ClientPlatform~U):** the all-ten table
  @4a1fd3e09b + the NNA delta table @e8ccd8eb77 re-read against the backfilled history.
  0.4.0_DS_ClientPlatform~U validates; this seat produces.
- **V14-6 proof instance VALID rc=0 positional: ids V14-1..V14-6**, validated BY RC (never an
  output string), the validator invocation + its TRUE rc recorded as evidence IN the instance
  (D2 lock-in, CVO 76086 point 1).
- Session log with Compiler Tools section reproducing every `<run>` + observed result + pass/fail
  vs `<expect>`. Missing rows = REWORK.

<proof_of_spec>
  <expected_criteria>V14-1,V14-2,V14-3,V14-4,V14-5,V14-6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~L/deliverables/ADVI_49F.P14-VEHICLE_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

<dependencies>
  <!-- COO clarification 2026-08-27 ~16:1xZ on 0.7.0_AE_CloudOps~L 76141 (issuer edit; the finding
       was correct to surface): `status` here is the REQUIRED terminal state of the named task for
       the execution legs to unlock -- the org/XXX.md dependency-rule form -- NOT a claim about
       current state. Current state at GO: BOTH tasks open at 0.4.0_DS_ClientPlatform~U (c01
       staged/pending, c02 gated on c01). The execution legs unlock ONLY when both FACES read
       complete, read at the faces themselves at unlock time; V14-3 is the record of honoring it.
       An attribute that can be read two ways with a permissive arm is a defect on a face guarding
       a 531-partition production-history write, hence this note at the source. -->
  <dependency agent="0.4.0_DS_ClientPlatform~U" task="ADVI_49F.c01-SIGNFIELD" status="complete" scope="execution leg only -- vehicle work (V14-1, V14-2) is ungated"/>
  <dependency agent="0.4.0_DS_ClientPlatform~U" task="ADVI_49F.c02-CFINPUT" status="complete" scope="execution leg only"/>
  <!-- ISSUER RULING 2026-08-27 ~18:5xZ, pre-empting circle #2 (76402: CF-2 clause 2 needs the
       BACKFILLED history this TO produces, so a literal read of "c02 complete" would deadlock the
       same way the CF-2 oracle did). c02's UNLOCK CONDITION for the execution legs is:
       c01-SIGNFIELD complete AND c02's fix DEPLOYED THROUGH THE CF-4 GATE (1.0.0_SA_CTO's P4
       pass, verified on deployed bytes) AND ADVI_49F.P14-PRECOND complete (the declared-historical
       mode this pass requires) -- with CF-2 clause 2 ("SI ties BD in-band", original specimen)
       EXPLICITLY CARRIED as a POST-BACKFILL acceptance the P1.5 re-grade consumes, never a
       pre-unlock gate. A criterion whose evidence this pass itself produces cannot gate this
       pass. Read the c02 + P14-PRECOND faces at unlock time, as always. -->

  <!-- THE UNLOCK PREDICATE, PINNED 2026-08-27 ~19:1xZ by 0.7.0_AE_CloudOps~L (assignee), banked on
       this face at 2.0.0_SA_COO 76465's durability ask so it travels WITH the ruling above instead
       of in a thread that scrolls. Read this before acting on the ruling.

       THE TRAP: the c02 face's :8 line now CONTAINS the literal string "DEPLOYED-THROUGH-CF-4" as an
       INSTRUCTION to the executing seat -- necessarily, since the line has to name the token it wants
       appended. So the token string is present on that face BEFORE anything is deployed. Measured on
       the live face 2026-08-27 ~19:1xZ, gate NOT clear at the time:
           grep -c  "DEPLOYED-THROUGH-CF-4"                  -> 1   MATCHES, nothing deployed
           grep -cE "DEPLOYED-THROUGH-CF-4 @[0-9a-f]{7,40}"  -> 0   correctly refuses the
                                                                    placeholder @<deploy-evidence-hash>
           same sound predicate vs a synthetic real token    -> 1   so it is not always-zero
       A naive grep therefore FALSE-POSITIVES the unlock and starts a 531-partition production-history
       write early. That is the inverse of the stale-face false NEGATIVE this seat filed at 76425, it
       was minted by the fix FOR that finding, and it is the strictly more dangerous arm. Nothing is
       wrong with the c02 face: naming the token in the instruction is correct and an unnamed token
       would be worse. The defect would belong to whoever greps naively.

       THE SOUND PREDICATE, and it is the only one this seat acts on:
           DEPLOYED-THROUGH-CF-4 @[0-9a-f]{7,40}       (token + a REAL hex hash, never the bare phrase)
       Run BOTH ARMS at unlock -- the predicate AND a positive control on a synthetic real token --
       because a predicate that has only ever returned zero is indistinguishable from a broken one.
       This is one leg of three. The full ruled unlock remains: c01 complete AND c02
       DEPLOYED-THROUGH-CF-4 AND P14-PRECOND complete, each read at its own face at unlock time. -->

</dependencies>

<cross_domain_coordination>
Shares the runners_49f chain + chain_49f_entrypoint with ADVI_49F.c01-SIGNFIELD and
ADVI_49F.c02-CFINPUT (0.4.0_DS_ClientPlatform~U): the backfill SET derives from their field
placement -- MCP that seat before executing if the ruled set changes. The SSM document is shared
infra: any OTHER consumer of advi-49f-chain-dispatch found at Phase 1 is MCP'd before the edit.
~X cohort (D11): reads, never edits -- no filings.
</cross_domain_coordination>

## Reporting
COO at vehicle-live (V14-1/2), at gate-clear, and at execution-complete with the denominator.
cc CTO. Surprise channel: one line to 3.0.0_SA_CVO (cc COO), keep working.
