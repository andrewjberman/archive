<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-r20-sidecar-census</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>3.0.0_SA_CVO</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
  </metadata>

  <objective>
    Execute R-20 of the MDPF remediation register **up to but NOT including deletion**: a READER CENSUS
    of every sidecar-state and one-off-patch object, classified against the register's four-shape table,
    with a deletion PROPOSAL per object. **This TO closes at "census delivered + deletion proposed."
    It never closes at "deleted."**
  </objective>

  <context>
    PRD: `docs/architecture/MDPF_REMEDIATION_REGISTER.md` @e5e932caf6 §2g. Andrew took the register AS
    THE PRD 2026-08-07 ~1910Z.

    ANDREW-DIRECT 2026-08-07 ~0312Z, VERBATIM: *"one off weird patches and 'meta' tables, trash all of
    it"* — widening R-19 from the GATES to the ARTIFACTS THEY READ.

    >> **THE LINE IS ALREADY DRAWN AND BASE-CTO ADJUDICATED IT SOUND (191307Z). ADOPT IT VERBATIM.**
    The register's author flagged *"THE LINE THAT MUST BE DRAWN, or this ruling deletes something the
    contract requires"* as a RISK, not a gap — then drew it:

    | shape | verdict |
    |---|---|
    | **SIDECAR STATE OBJECT** — a separate file ASSERTING A CURRENT CONDITION about other files. Mutable, singular, READ AS A GATE. | ⛔ **TRASH** |
    | **ONE-OFF PATCH ARTIFACT** — a frozen or hand-made copy created to survive one migration | ⛔ **TRASH** |
    | **IN-BAND `meta` BLOCK** — inside the artifact, derived by the same computation | ✅ **KEEP** |
    | **IMMUTABLE RUN MANIFEST** — append-only, per-run, never read as a gate | ✅ **KEEP** |

    >> **THE DISCRIMINATOR, CARRIED VERBATIM BECAUSE THE FAILURE MODE IS CLASSIFYING BY FILENAME:**
    **"A MANIFEST RECORDS WHAT HAPPENED. A SENTINEL ASSERTS WHAT IS TRUE."**
    The first is HISTORY — append-only, nothing branches on it. The second is a LOCK — mutable,
    singular, and the pipeline's behaviour depends on it. Andrew's ruling **kills the lock, not the
    history.** ***"A manifest read as a gate has become a sentinel; THAT is the test, NOT THE FILENAME."***

    WHY THIS CLASS IS THE ROOT: a sidecar meta object is a DESCRIPTION of state living OUTSIDE the
    state. It can be false while the data is fine, or true while the data is broken, **and nothing
    reconciles them.** `pipeline-complete.json` said `run_date: 2026-07-31` for eight days while
    Schwab silver advanced to 08-06 — **a true reading of a stale description.** (COO re-verified the
    marker at 2026-07-31 today.)

    THE INVENTORY (register §2g):
      opal-data-inf/gold/meta/pipeline-complete.json                          <- see criterion 1
      opal-data-inf/gold/eclipse/_meta/dispatch_eclipse_status.json
      opal-data-assets/gold/mdpf_revamp/meta/cycle-complete.json
      opal-data-assets/gold/mdpf_revamp/_audit/legacy_account-distribution_pre-w6_20260723.json
      .../_audit/legacy_aum-timeseries_pre-a2_20260723.json
      .../global/non_model_assets_precutover_frozen.json
      .../cottonwood/aggregate_aua_timeseries_interpolated.json               <- SEE THE CARVE-OUT
      opal-data-mdpf/telemetry/mdpf-daily-runner/ (180 obj) · cache/ · bmkaud-evidence/
  </context>

  <compiler_tools_mandate>
    Phase 1: <run>comp-which "what reads &lt;object key&gt;"</run> then <run>comp-find "&lt;object basename&gt;"</run>
             <expect>PRINT THE DENOMINATOR on every scan. Use `--all` where a count is load-bearing —
             a paginated count is a page size wearing a total's clothes, and an ABSENCE verdict here
             authorizes a deletion proposal.</expect>
             <if_mismatch>An absence you cannot show the denominator for is NOT an absence. Say
             UNMEASURED.</if_mismatch>
    Phase 2/3: record every command, its denominator and its disposition in the log.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - >> ⛔ **BLOCKED ON `MDPF_REMED.W1-2` FOR `pipeline-complete.json` SPECIFICALLY.** That object is
      read by `_check_inf_spine`, which W1-2 (0.7.0_AE_CloudOps) is retiring. **RETIRE THE READER
      BEFORE PROPOSING THE OBJECT'S DELETION — never the reverse.** COO releases that one object when
      AE reports (a) retired. **Every OTHER object in the inventory is unblocked; start now.**
    - `opal-data-inf/*` is INF's tree, not MDPF's. A census is read-only and fine; a deletion proposal
      on another program's object is a PROPOSAL to its owner, never a plan.
  </cross_domain_coordination>

  <acceptance_criteria>

    1. EVERY OBJECT IN THE INVENTORY CARRIES: its four-shape classification, **the reason keyed to the
       DISCRIMINATOR rather than to its filename**, its reader census with a printed denominator, and a
       deletion proposal or a KEEP with cause.
       ⛔ *"It is called `meta`"* and *"it is called `manifest`"* are BOTH invalid reasons. The test is
       whether anything BRANCHES on it.

    2. >> **THE CARVE-OUT SURVIVES INTACT.** `aggregate_aua_timeseries_interpolated.json` is a
       **SANCTIONED, LABELLED backfill** — the register's author carved it out explicitly: it *"retires
       on its own terms, not as residue."* It is the one item on the TRASH list that is NOT residue.
       ⛔ Sweeping it in would be exactly the *"deletes something the contract requires"* harm this
       classification exists to prevent.

    3. >> **THIS TO CLOSES AT "CENSUS DELIVERED + DELETION PROPOSED." IT NEVER CLOSES AT "DELETED."**
       S3 object deletion is on the human-confirmation list. **`R-13`'s underscore twins are the
       precedent that RULED ≠ EXECUTED** — and note they have since BEEN executed @46d3bf3f32, so the
       register row describing them as outstanding is itself stale. Deletion happens only with
       Andrew's word attached to that specific object.

    4. A ZERO-READER FINDING IS SHOWN, NOT ASSERTED. For any object you propose deleting on
       "nothing reads it", print the denominator of the scan and name what you could NOT see
       (untracked files, deployed-but-uncommitted code, another device's tree). ⛔ An absence verdict
       from a truncated scan is indistinguishable from a real absence.

    5. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier1_exec/3.0.0_SA_CVO/deliverables/MDPF_R20_SIDECAR_CENSUS_20260807.md</file>
      <file action="reference">docs/architecture/MDPF_REMEDIATION_REGISTER.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Census every inventory object; classify by the discriminator, not the filename.</requirement>
    <requirement id="2">Hold `pipeline-complete.json` until COO releases it on W1-2's completion.</requirement>
    <requirement id="3">Preserve the interpolated-backfill carve-out.</requirement>
    <requirement id="4">Propose; do not delete.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">The census + per-object proposal.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>⛔ DO NOT DELETE ANY S3 OBJECT under this TO. Propose only.</rule>
    <rule>DO NOT classify by filename. A manifest read as a gate IS a sentinel.</rule>
    <rule>DO NOT sweep in `aggregate_aua_timeseries_interpolated.json` — sanctioned, retires on its
    own terms.</rule>
    <rule>DO NOT propose deletion of `pipeline-complete.json` before COO releases it.</rule>
    <rule>DO NOT report an absence without its denominator.</rule>
    <rule>DO NOT build any alert, alarm, checker or monitor.</rule>
  </do_not>
</task_order>
