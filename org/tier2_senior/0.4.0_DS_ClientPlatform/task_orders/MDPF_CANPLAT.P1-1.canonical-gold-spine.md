<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-canplat-p1-1</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~Z</issued_to>
    <date>2026-08-06</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
    <supersedes>MDPF_CANRTE.P1-1 (adopted @a6ae64326, deltas below) · MDPF_CANRTE.A / P0-4 / W2R (superseded; outputs adopted as inputs)</supersedes>
    <governing>PRD docs/architecture/MDPF_CANONICAL_PLATINUM_PRD.md @24d3eb2f8 · CONTRACT docs/architecture/MDPF_CANONICAL_PLATINUM_DELIVERABLE_CONTRACT.md @a3106d585</governing>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0, VERBATIM — THE OPERATING INSTRUCTION FOR THIS ENTIRE PROGRAM:

    > **ANDREW-DIRECT, 2026-08-06, VERBATIM:**
    > *"This is exactly correct. I need you to persist this exactly as laid out here as a PRD and issue that
    > to COO for decomposition. I just terminated every fabric agent's session on this device aside from you
    > and mstr~z because I want them respawned with this being fresh context and instruction. **I do not want
    > them to go off the rails on hunting down errors, just do what is described here.**"*

    **THE LAST SENTENCE IS THE OPERATING INSTRUCTION FOR THIS ENTIRE PROGRAM. It is why your session is new.**

    **BUILD WHAT §2 DESCRIBES. DO NOT HUNT ERRORS.**

    - **A number that surprises you is NOT a finding.** The business logic is **correct and live** — it
      renders properly in Portal PROD today. This is a **SHAPE** project.
    - **The only defects in scope are SHAPE divergences**: a field present on one scope and absent on a
      sibling, or a value a producer never emits. **Everything else is out of scope**, however interesting.
    - **If you find something that looks wrong: REPORT IT, DO NOT CHANGE IT.** One line to COO~Z. Then
      continue the work in §2. Do not open an investigation. Do not widen a task order.
    - **Prior context is deliberately not being restored.** The predecessor sessions found real defects for
      three days and became primed to read every surprising number as a bug. **You are fresh so that you are
      not.** Do not go looking for the previous session's threads.

    > **The measured reason this clause exists:** `1.0.0_SA_CTO~Z` surfaced Global's non-model excluding
    > Inflection and Cottonwood (~$409mm) as "a consequence worth seeing." **It is Andrew's own ruled,
    > correct, intended semantic**, enforced in code by leg pins, rendering correctly in PROD.
    > **TREATING A CORRECT NUMBER AS A FINDING IS HOW A WORKING PIPELINE GETS "FIXED."**

    SURPRISE CHANNEL: anything that looks wrong = ONE LINE to 2.0.0_SA_COO~Z, subject beginning
    `SURPRISE:`, then keep building. No investigation, no change, no widening. COO triages.
  </standing_instruction>

  <objective>
    Build the gold consolidator per CONTRACT §A — ONE firm-parameterized `mdpf-gold-lambda` (firms are
    config rows, global is a fold) — emitting the CONTRACT §B canonical shape for all 3 artifact types x
    4 scopes, in the A4 grammar
    `s3://opal-data-assets/portal/gold/mdpf/{scope}/{artifact-type}/{data-as-of}.json` (dated,
    hyphenated), DIRECTLY — **together with the Cottonwood producer family (§C), one atomic unit.**
    The platinum daily contract this feeds is 12 objects, every single day (PRD §2).
  </objective>

  <adoption>
    **The corrected body of `MDPF_CANRTE.P1-1.firm-parameterized-gold-spine-atomic.md` AS COMMITTED
    @a6ae64326 IS ADOPTED AS THIS TO's CONTENT** — its &lt;context&gt; (rulings, banked measurements,
    packaging decision, roster/calendar rulings), &lt;compiler_tools_mandate&gt;,
    &lt;cross_domain_coordination&gt;, &lt;acceptance_criteria&gt; 1–10 (including 9c's five-limb
    regression form, 9d's consolidation-only fee_scope ruling, 9e's ternary correction, 9f's second-oracle
    rule), &lt;scope&gt;, &lt;requirements&gt;, and &lt;do_not&gt; — **subject to the DELTAS below, which
    win on any conflict.** Read that file at that pin as part of this TO. Do not chase any other
    predecessor thread (§0).

    **DELTAS (authoritative):**
    - **Δ1 · THE COUNT IS 12.** PRD §2. Anywhere the adopted body says "14 canonical artifacts," read the
      canonical 12 + the two extras folding in (W-5/W-6) + the dated `_aggregate_aua` (A7). The two
      standalone extras retire only per R12, and never by you.
    - **Δ2 · THE EXEMPTION DENOMINATOR IS CONTRACT §B.** Everywhere the adopted body says "the §3 list" /
      "spec §3," the closed field-path list the comparator consumes is **CONTRACT §B @a3106d585**. The
      comparator itself is CVO~Z's (`MDPF_CANPLAT.G2`); you supply the declared canonicalisation and the
      mutation fixture jointly with CVO~Z.
    - **Δ3 · A3/A4 GRAMMAR IS YOURS TO EMIT DIRECTLY.** Gold writes
      `portal/gold/mdpf/{scope}/{artifact-type}/{data-as-of}.json` — dated, HYPHENATED type — directly.
      Today's `gold/mdpf_revamp/{firm}/aggregate_aua_timeseries.json` (undated, underscored) is the
      grammar the 09:40 bridge exists to correct; **gold writing A4 directly is what makes the bridge
      deletable (R3). You do NOT retire the bridge** — it retires second, on R11 evidence, by AE~Z under a
      later GO. Until then it idles into a no-op.
    - **Δ4 · A7 VERBATIM:** the dated `_aggregate_aua` producer contract
      (`gold/mdpf_revamp/_aggregate_aua/{date}.json`) is **preserved** until `opal-assets-daily-emitter`
      is atomically re-pointed with equivalence proved. It is **NOT per-scoped** — multi-partner BY
      COMPUTATION. DEPLOY BEFORE ENV (adopted cross-domain row binds).
      ⛔ **THE `mdpf_revamp` NAME IS DELIBERATE AND CURRENT — Andrew SEQUESTERED its retirement**
      (CTO~Z 234938Z, A7 anti-widening line @76d4ba532; brief pocketed at
      `docs/briefs/mdpf-revamp-name-retirement-POCKETED-20260806.md`, NOT authorized, NOT scheduled).
      Do not scope the rename in; when A4 lands, the scoped `mdpf_revamp` objects simply stop being
      written and go inert. If you wonder why we still write a prefix Andrew dislikes: sequestered by
      his ruling, A7 stands — that is the one-line answer, already given.
    - **Δ5 · §B3's FIVE GLOBAL-ONLY FIELDS ARE YOUR CLASSIFICATION CALL.** `count_as_of`, `count_basis`,
      `account_count_total_raw`, `point_class`, `opal_aggregate_aua`: DECIDE per L-1 — canonical-for-all
      (honest absence at firm scope) or non-canonical — and RECORD the decision + reasoning in your
      deliverable. ⛔ Classification only, NOT a deletion decision; a field ruled non-canonical still
      serves until Andrew rules its retirement. `inflection_non_model_aua` is already ruled NOT canonical
      (firm-named field at global scope); its data is canonically inflection's own `non_model_aua`.
    - **Δ6 · CONFIRM THE ⟨confirm⟩ ROWS.** §C's four role-inferences (`mdpf_revamp_model_crosswalk`,
      `stage_mdpf_revamp_trio`, `cottonwood_aua`, `build_dim_model_portfolio`) are the only unmeasured
      cells in the contract — confirm or correct each in your deliverable.
    - **Δ7 · fee_scope: COLLAPSE 2→1, SOURCE-SIDE, CHANGING NO VALUES** (W-7,
      `dim_mdpf_aggregate_aua_timeseries.py:2378` + `dim_mdpf_aum_metrics.py:191-195`). Migration to
      declared data is P2-1's config axis, **not this build's**; nobody populates
      `data/firm_registry.json` on this program's authority (PRD §6). State plainly in the deliverable
      that the surviving map is still builder-authored.
  </adoption>

  <guard_3>
    ⛔ GUARD 3 — VERBATIM, AND IT IS YOURS TO HOLD: **W-2's acceptance is COVERAGE, never "non_model is
    non-null."** The honest-None guard is **the derivation itself** (`build_cottonwood_mdpf_slice.py:853`,
    `:1131-1132`, `:782`). **There is no gate object to delete — so a non-null criterion is satisfiable by
    changing `else None` to `else 0`: a ONE-TOKEN EDIT THAT READS AS NULL-SAFETY HARDENING AND LEAVES NO
    SCAR.** The both-operand form (`:1131`) wins at the converged path; record it as a CHOSEN SEMANTIC.
    Coverage is reported as a **ratio with its denominator printed** (cottonwood non_model N of 446-class),
    never a boolean. §B array invariants bind: every parallel array `len == n_dates == len(dates)`;
    `non_model_aua`, `account_count_total` carry `null` for unreached dates — **never `0`**.
  </guard_3>

  <acceptance_criteria>
    The adopted criteria 1–10 @a6ae64326 stand under the deltas. The COMPLETION oracle is CONTRACT §E —
    these rows, quoted, are what your build must make PASS on the scheduled path (final adjudication runs
    on one unattended scheduled cycle, program-level):

    - **A1** "ONE Lambda, ONE firm-parameterized code path. Firms are config rows, not branches. Global is
      a fold, not a fourth builder." Oracle: zero `if firm ==` in the spine.
    - **A2** "Fires on the 09:00 ET scheduled floor. The INF completion marker may accelerate; it is never
      the only trigger." Oracle: `ScheduleExpression` present + non-null. (Infra half lands with AE~Z;
      your handler must be schedule-first by design.)
    - **A3/A4** "Writes the canonical dated grammar DIRECTLY … hyphenated type, dated." Oracle: key listing.
    - **A5** per-scope exceptions — fixture: fail each firm in turn, other two still succeed (R8).
    - **A6** immutable run manifest, all fields, data-as-of and process time distinguishable (R10).
    - **A7** `_aggregate_aua` contract preserved until atomic emitter re-point.
    - **A8** idempotent; same hash → `unchanged`; different bytes same date → `conflict`, recorded, never
      silently overwritten (R9: double-fire → identical business bytes).
    - **A9** trading-day frontiers per feed from committed config, never wall-clock;
      `calendar_source()` asserts the pmc backend.
    - **R2** "Key set identical across all four scopes, per artifact type. PASS iff set-diff = ∅ for each
      of the 3 types" — §B shapes, honest absence (`null`) where a scope lacks data, never omission,
      never zero.
    - **R4** "I-1 global non-model = 49F only, both artifacts — asserted vs `fee_basis_components`, never
      a literal firm name" (the adopted 9d honesty clause binds: the surviving source map is still
      builder-authored; say so).
    - **R5** "I-2 each firm carries its own non-model — coverage ratio with denominator printed, never
      'non-null'."
    - **R6** "I-3 global counts = total model holdings ex-unfunded — value tie."
  </acceptance_criteria>

  <cross_domain_coordination>
    The adopted three rows @a6ae64326 bind (cottonwood private-symbol atomicity; Lambda package/
    BUILD_MANIFEST with AE~Z — runtime python3.11, x86_64, flat; `_aggregate_aua` + daily-emitter
    DEPLOY-BEFORE-ENV). Plus, this generation:
    <shared_resource>A4 gold keys `portal/gold/mdpf/{scope}/{artifact-type}/{data-as-of}.json`</shared_resource>
    <also_in_to>MDPF_CANPLAT.P3-1 (publisher D2 reads these exact keys)</also_in_to>
    <required_action>MCP 0.7.0_AE_CloudOps~Z before ANY grammar shift; the publisher consumes the exact
    keys you write.</required_action>
    <shared_resource>Served platinum baseline (CVO~Z G2 pins VersionIds)</shared_resource>
    <also_in_to>MDPF_CANPLAT.G2</also_in_to>
    <required_action>Gold writes portal/gold ONLY. Nothing in this TO writes a platinum key — the
    publisher is platinum's only writer. Supply CVO~Z the declared canonicalisation + a mutation fixture
    on request.</required_action>
  </cross_domain_coordination>

  <deliverables>
    <deliverable type="commit">The atomic build across both trees, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">§B3 five-field classification decision + reasoning (Δ5); §C ⟨confirm⟩ confirmations (Δ6); coverage ratios with denominators; equivalence/channel-independence/calendar tie-outs with denominators (adopted)</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>Everything in the adopted &lt;do_not&gt; @a6ae64326 — verbatim force.</rule>
    <rule>DO NOT retire the 09:40 bridge, the EC2 chain, OWNTS, or any old route — R11 is AE~Z's, later,
    on evidence. DO NOT touch the two standalone extras (R12). DO NOT delete or move any served key
    (R14, NEVER#3).</rule>
    <rule>DO NOT change any §3-invariant number: a builder that changes a §3 number has FAILED, not fixed
    (PRD §6).</rule>
    <rule>DO NOT populate data/firm_registry.json or migrate fee_scope to declared data (PRD §6).</rule>
    <rule>NO error-hunting (§0). SURPRISE: line to COO~Z, then keep building.</rule>
  </do_not>
</task_order>
