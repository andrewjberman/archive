<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-cottonwood-opal-child-attribution</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
  </metadata>

  <objective>
    Fix Cottonwood Opal attribution in `build_dim_model_portfolio.py`: Opal constituents held inside
    a NON-Opal-named parent strategy are currently dropped before decomposition, so they never
    attribute. The live gold dim UNDERSTATES real Opal AUA on a CLIENT-FACING number. The semantics
    are SETTLED by Andrew — you implement, you do not have to guess.
  </objective>

  <context>
    >> THE SEMANTIC QUESTION IS ANSWERED. Andrew-direct 2026-08-07 ~1645Z, base CTO terminal,
    VERBATIM: *"All your recs are approved, proceed"* — approving, as item 2:
    **Opal children of non-Opal-named parent strategies SHOULD attribute. A constituent that IS an
    Opal model is Opal exposure regardless of what its parent wrapper is named; current behaviour
    UNDERSTATES real Opal AUA.**
    This was the one input the fix could not derive. It is now settled and you implement against it.

    ROOT CAUSE, PINNED AND RE-DERIVED AT THE COO SEAT (not carried on report):
    `data/assets/scripts/gold/build_dim_model_portfolio.py:272-277` @HEAD —

        :272  assigned = assignment[assignment.strategy_name != "--"].copy()
        :273  # STRICT OPAL FILTER -- gold's job, applied to the ASSIGNED STRATEGY.
        :274  assigned["model_id"] = assigned.strategy_name.map(name_to_id)
        :275  unresolved = int(assigned.model_id.isna().sum())
        :276  assigned = assigned[assigned.model_id.notna()]
        :277  opal_assigned = assigned[assigned.model_id.isin(opal_ids)]
        :287  for _, acct in opal_assigned.iterrows():        <- DECOMPOSITION STARTS HERE

    **The Opal test is applied to the PARENT strategy at :277, BEFORE the decomposition loop at
    :287.** So a parent strategy whose NAME is not Opal is removed from the frame entirely, and its
    Opal children are never reached — they cannot attribute because they were never decomposed.

    ⚠ THE DATA TO DO IT RIGHT IS ALREADY COMPUTED. `:266` already sets a CHILD-level flag:
        "is_opal": rs.is_opal_name(e.child_model_name)
    So the child-grain Opal determination exists in `dim` today. This is a question of WHERE the test
    is applied, not of new information needing to be derived.

    MEASURED CONSEQUENCES (AE~Z brief @924c3b669): Opal Fixed Income ABSENT from the live gold dim;
    Conservative Growth ties 96+2=98. Read the brief before starting; do not re-derive what it
    already measured, and do not inherit its figures as your own measurement either.

    PRIOR ART / GRAIN WARNING: cot BD `fact_holdings` is RELATIONSHIP-grain (row = Relationship x
    Account x Asset). Naive sums DOUBLE-COUNT. If your verification touches that table, collapse via
    `collapse_relationship_grain()`.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-pipescript io build_dim_model_portfolio.py --pipeline mdpf</run>
      <expect>COLUMN GAPS + portal consumers. `--pipeline` is REQUIRED — flagless is rc=2 REFUSED
      and will not guess.</expect>
      <if_mismatch>Any COLUMN GAP is fixed before proceeding — silent column omissions have produced
      zero-valued output in prod.</if_mismatch>

      <run>comp-blast [the decomposition function you are changing]</run>
      <expect>Downstream consumers of the dim. This is a CLIENT-FACING serving path — know every
      consumer before you change what the number means.</expect>

    Phase 2 — before committing:
      <run>.tools/commit-gate.sh</run>
      <expect>py_compile + ds-precommit-check + ruff py39 all pass.</expect>

    Phase 3 — after committing / before signalling:
      <run>comp-validate build_dim_model_portfolio.py --artifact /tmp/[artifact].json</run>
      <expect>PASS or WAIVED. ⛔ `NO_CONFIG` / `ZERO_CHECKS` = UNVALIDATED — never signal SAFE on it.</expect>
      <run>comp-pipescript deployed build_dim_model_portfolio.py</run>
      <expect>MATCH after upload.</expect>
      ⚠ `data/assets/scripts/gold` is a SHARED repo home: it deploys under the S3-membership guard
      (key-exists=update enforced, 404=loud skip, first-mints explicit). A silent skip is not a deploy.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: `data/assets/scripts/gold/build_dim_model_portfolio.py` + the served MDPF gold
      dim + its platinum projection
    - also_in_to: MDPF_CANPLAT wave-1 work ran on site Z (DS~Z gold spine, AE~Z publisher). SITE Z IS
      DOWN and is invisible to this broker — do NOT infer its state from `get_live_agents` here.
    - required_action: the MDPF platinum cutover completed 2026-08-06 and the 09:00 ET schedule's
      FIRST UNATTENDED FIRE is Andrew's own oracle. If your fix changes what that fire emits, say so
      explicitly in your report — do not let a corrected number arrive at his screen unannounced.
  </cross_domain_coordination>

  <acceptance_criteria>

    >> 1. THE TEST MOVES FROM PARENT TO CHILD. IT IS NOT DELETED.
       ⛔ FORBIDDEN SHORTCUT, NAMED SO IT CANNOT BE TAKEN BY ACCIDENT: the cheapest way to make Opal
       children attribute is to drop the `:277` filter. **That would attribute EVERYTHING, including
       genuinely non-Opal exposure, and would OVERSTATE Opal AUA — replacing an understatement with
       an overstatement on the same client-facing number, in the direction nobody would question.**
       The strict Opal test must still be applied — at CHILD grain, after decomposition, using the
       determination `:266` already computes.

    2. THE THIRD STATE SURVIVES. `:275` currently counts `unresolved` (strategy names that map to no
       model id). After the change, unresolved constituents MUST STILL BE COUNTED AND REPORTED, and
       must NOT be silently folded into either the Opal or the non-Opal bucket.
       ⛔ An unresolved child is NOT a non-Opal child. Reporting zero unresolved is a finding against
       the change, not a clean result.

    >> 3. PUBLISH THE BEFORE/AFTER DELTA WITH ITS DENOMINATOR — THIS IS NOT OPTIONAL AND IT IS THE
       CRITERION MOST LIKELY TO BE SKIPPED. **The whole point of this fix is that a client-facing
       AUA number GOES UP.** A number that moves on a client-facing product with no stated delta is
       how a CORRECT FIX gets reported as a DEFECT. Publish: Opal AUA before, Opal AUA after, the
       delta, the count of newly-attributing constituents, the count of parent strategies newly
       reached, and a measurement vintage.

    4. THE TWO MEASURED CASES RESOLVE, and they are the sharpest test available because AE~Z already
       measured them: **Opal Fixed Income must APPEAR in the gold dim** (currently ABSENT), and
       **Conservative Growth's 96+2=98 tie must hold** after the change. State both explicitly.

    5. `comp-validate` PASS or WAIVED (never signal safe on NO_CONFIG/ZERO_CHECKS), and
       `comp-pipescript deployed` shows MATCH.

    6. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/assets/scripts/gold/build_dim_model_portfolio.py</file>
      <file action="reference">org/tier2_senior/0.7.0_AE_CloudOps/deliverables/[AE~Z Cottonwood brief @924c3b669]</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Move the Opal determination to child grain, post-decomposition, reusing the
    `:266` flag rather than deriving a second one.</requirement>
    <requirement id="2">Preserve `unresolved` as a reported third state.</requirement>
    <requirement id="3">Publish the before/after delta per criterion 3.</requirement>
    <requirement id="4">Rule 13: you own the full commit -> QA-deploy cycle for this file, including
    the `aws s3 cp`. Rule 15: `from __future__ import annotations` stays at the top.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">The fix, gate-passed.</deliverable>
    <deliverable type="document">The before/after delta report (criterion 3) with vintage.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT delete the strict Opal filter. Move it to child grain. See criterion 1 — deleting it
    swaps an understatement for an overstatement.</rule>
    <rule>DO NOT fold unresolved constituents into either bucket.</rule>
    <rule>DO NOT ship the fix without the before/after delta. The number moving IS the deliverable.</rule>
    <rule>DO NOT touch the platinum publisher or the serving projection. This TO is the GOLD producer
    only; D4 NEVER PATCHES SHAPE.</rule>
    <rule>DO NOT naive-sum cot BD `fact_holdings` — it is RELATIONSHIP-grain and will double-count.</rule>
    <rule>DO NOT build any alert, alarm, SNS topic, SES send, freshness checker or monitor. DO NOT
    call any external vendor API.</rule>
    <rule>DO NOT infer site-Z state from this device's broker — site Z is DOWN and invisible here.</rule>
  </do_not>
</task_order>
