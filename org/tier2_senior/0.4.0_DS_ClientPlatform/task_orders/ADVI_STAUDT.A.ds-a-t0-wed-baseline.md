<task_order>
  <metadata>
    <id>ADVI_STAUDT.A</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>staged</status><!-- CTO confirms shape before COO dispatches GO -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~A — T0 Wednesday baseline</lane>
    <priority>P0 — gates fix-TO authoring on Friday breakage attribution</priority>
    <git_anchor>544877cc</git_anchor>
    <wall_clock>Wed 2026-04-15 ~20:40 ET</wall_clock>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§4.1 (lane scope), §3.2 (fields in scope), §3.3 (Group D PRIMARY focus), §5 (guardrails), §6 (cross-domain), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCP 20260420T120334Z — §3.3 amendment locking Group D tagged_aua / role-split / fee-split as PRIMARY scope</ref>
    <ref type="upstream">CTO MCP 20260417T213111Z — 4-bug audit ratification</ref>
    <ref type="cto-handoff">CTO MCP 20260420T~12:00Z — STAUDT PRD handoff with lane assignments + read-only guardrails</ref>
  </references>

  <objective>
    Deliver the T0 (Wed 2026-04-15 ~20:40 ET, git `544877cc`) checkpoint of ADVI gold + portal state. T0 is the "imperfect but accepted" baseline: pre-polars, pre-CN/RA cutover, pre-W4 structural convergence, FE post-19:35Z artifact set. ~D's 4-checkpoint synthesis depends on this evidence pack. Read-only audit only — no code writes, no S3 writes, no gold-runner triggers.
  </objective>

  <scope>
    <!-- VERBATIM from ADVI_STAUDT.md §3.3 (Group D PRIMARY FOCUS) per CTO MCP 20260420T120334Z. The primary-focus language must survive into the TO — no paraphrasing. -->

    ### 3.3 GROUP D PRIMARY FOCUS — tagged_aua / role-split / fee-split (PRIMARY SCOPE, non-negotiable)

    Per Andrew 2026-04-20: the Group D logic touching `tagged_aua`, role-split AUA, and fee-split AUA is the **primary** audit scope — not one of many fields. Every lane treats the following Group D production sites and consumer sites as the highest-priority targets. Evidence packs must lead with these, not bury them.

    **Canonical Group D production sites (enumerate formula + inputs + line range at EVERY checkpoint):**

    | Site | Script : line | Role | What to capture |
    |---|---|---|---|
    | **D_00c `_weighted_aua`** | `D_00c.portal_leaderboard.py:881` (or equivalent at checkpoint) | Role-split AUA producer (split-weighted sum across roles) | Function body, caller list, role-weight formula, advisor cohort where split-weight diverges from total. Was this present at T0? How did it evolve T1→T2→T3? |
    | **D_00c `tagged_aua` column** | `D_00c:528` (row.total_aua fallback) | Leaderboard `tagged_aua` source | Is this the fallback OR the primary? What feeds `row.total_aua`? Does D_00c read from D_02 at any checkpoint? |
    | **D_00c `no_fee_aua`** | `D_00c:565` (`max(0, tagged_aua - fee_aua)` silent-clip) | Fee-split no-fee producer | Clip behavior + per-advisor `no_fee.aua = 0` cohort size at each checkpoint. Travis drops off here because clip silently zeros. |
    | **D_00c `aua_growth_pct`** | `D_00c:580` | Growth rate numerator/denominator | What is numerator, what is denominator, do both trace to the same tagged_aua source? |
    | **D_00c `role_breakdown[role].aua`** | D_00c `_weighted_aua` output | Per-role AUA breakdown written to leaderboard | Is the sum across roles equal to `tagged_aua`? Where does it diverge? |
    | **D_02 `tagged_aua` / `summary.tagged_aua`** | `D_02.advisor_client_detail.py` `build_advisor_books` | Book.json per-advisor `tagged_aua` producer | Formula, inputs, does it fold per-role or per-account? |
    | **D_02 `_nna_since` / per-role NNA** | `D_02` `build_advisor_books._nna_since` (CN-P2 commit `b3f6b1ee` added canonical cum-sum lookup + period-diff; `ebd737e3` flipped paginator prefix) | Per-role NNA producer | Daily vs cumulative grain at each checkpoint. Summary site vs timeseries site. |
    | **D_02 `role_breakdown` / `canonical_role_aua`** | `D_02` writes `canonical_role_aua_key` (RA-P2b `94600ff6`) | Role-AUA canonical producer for downstream | Per-date per (advisor, role). Consumer: D_01. |
    | **D_02 `weighted_avg_fee_bps`** | `D_02` (denominator changed `5162fc1c`) | Fee-rate producer | Denominator: all accounts vs fee-paying-only. T1 flipped it. |
    | **D_04 OVERRIDE BLOCK — `aua_growth_pct` numerator** | `D_04:2325-2328` (commit `fe999416`, 2026-04-09) | Leaderboard `aua_growth_pct` numerator swap | What does it swap from/to? Does it use D_02's `tagged_aua` or D_00c's? |
    | **D_04 OVERRIDE BLOCK — `aua_growth_pct` denominator** | `D_04:2335-2340` (commit `6391b96c`, 2026-04-09) | Same for denominator | Same questions. Andrew: "Ratio = growth(pair A) displayed against pair B." |
    | **D_04 `fee_breakdown.no_fee.aua` top-level** | `D_04` leaderboard post-processing | Leaderboard top-level no-fee producer | B1.fix `5114984b` swept `role_breakdown[role].no_fee.aua` but NOT top-level — confirm. Travis drop-off originates here + D_00c:565 clip. |
    | **C_08 `role_breakdown.aua` canonical override** | `C_08.advisor_fee_efficiency.py` (RA-P5 `d9ab1719` latest-partition override) | C_08 role-breakdown source for fee_efficiency.json | Override behavior + mid-period-new-advisor fallback. |
    | **C_08 defensive backfill `aua_current` / `growth`** | `C_08:644` (quick-patch `9e537f9f`) | Silent zero-fill mask | T3 only. MUST be flagged as an audit concern — it masks the NNA-prefix-split schema mismatch. |

    <!-- Lane ~A specific scope (PRD §4.1 + §3.2) -->

    **Per-script audit at T0 `544877cc`:**
    - B_01 (T0 baseline pre-bond-100x, pre-cusip-rework, pre-tiered-cap)
    - C_00 (T0 baseline pre-polars port)
    - C_08 (T0 baseline pre-WAR-ROOM iterrows→to_dict, pre-defensive-backfill)
    - D_00b / D_00c / D_01 / D_02 / D_04 (T0 baseline pre-CN/RA cutover and pre-perf-rewrite)

    **Fields in scope (§3.2 — every script × T0):** `tagged_aua`, `row.total_aua` fallback, `fee_paying.aua` / `fee_aua`, `fee_breakdown.no_fee.aua` (top-level + per-role), `aua_growth_pct` (D_00c:580 + D_04 override L2325-2340), `nna` and `nna_canonical` (D_02 summary vs daily vs D_00c vs D_04), `role_breakdown[role].aua`, `small_account_count` (D_02 B9b), `fee_summary.window_revenue` (D_02 B3b), `growth.ttm_nna` (D_02 B3c). `market_value_uncapped` is T3-only — do not report at T0.

    **S3 platinum snapshots (PRD §4.1 input list):**
    - `s3://opal-data-bd/platinum/firm/leaderboard.json` at latest version ≤ 2026-04-16 00:00 UTC
    - `s3://opal-data-bd/platinum/firm/fee_efficiency.json` at same cutoff
    - `s3://opal-data-bd/platinum/advisors/{travis-penfield,kyle-sims,hunter-lloyd,alex-bright,tim-rodgers}/summary.json`
    - `s3://opal-data-bd/platinum/firm/header_metrics.json`
    - `s3://opal-data-bd/gold/canonical/nna/2026-04-15.parquet` AND `nna_atomic/2026-04-15.parquet` (if the latter exists at T0 — CN-P1b backfill landed Thu ~10:02 ET so atomic likely ABSENT at T0; document the absence)
    - `s3://opal-data-bd/gold/canonical/role_aua/2026-04-15.parquet` (if exists at T0 — likely ABSENT pre-RA-P1b)
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write — T0 reconstruction setup">
      <step>
        <run>git worktree add /tmp/staudt_T0 544877cc</run>
        <expect>Clean checkout of `544877cc` into scratch worktree per PRD §5 guardrail #4. Repo root remains on CLOUD tip — do NOT `git checkout` at repo root.</expect>
        <if_mismatch>STOP. If worktree creation fails (likely existing /tmp/staudt_T0 from another run), `git worktree remove --force /tmp/staudt_T0` then retry. If still failing, MCP COO before continuing.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T0 && comp-pipescript io B_01</run>
        <expect>READS + WRITES + COLUMN GAPS for B_01 at T0. Pre-bond-100x: cost_per_unit handling baseline. Pre-cusip-rework: name-keyed merges. No `market_value_uncapped` column write.</expect>
        <if_mismatch>If COLUMN GAPS surface, document — do not fix. Audit only.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T0 && comp-pipescript io D_00c &amp;&amp; comp-pipescript io D_02 &amp;&amp; comp-pipescript io D_04</run>
        <expect>D_00c reads CANONICAL_NNA_PREFIX (NOT atomic — pre-CN-P3). D_02 reads CANONICAL_NNA_PREFIX (NOT atomic — pre-CN-P2). D_04 reads CANONICAL_NNA_PREFIX. Confirm D_00c does NOT read from D_02 at T0 (anchors the COO 4-bug audit attribution).</expect>
        <if_mismatch>If any of the three reads atomic at T0, the git anchor is wrong — re-verify `544877cc` is pre-CN-P1. STOP and MCP COO.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T0 && comp-pipescript io C_08 &amp;&amp; comp-pipescript io D_00b &amp;&amp; comp-pipescript io D_01</run>
        <expect>All three read CANONICAL_NNA_PREFIX at T0. C_08 reads aua_current + growth from nna/ (NOT atomic). No defensive backfill `aua_current=0.0` / `growth=0.0` at C_08:644 — that landed at `9e537f9f` (T3).</expect>
        <if_mismatch>Document the actual prefix being read.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T0 && comp-blast D_00c &amp;&amp; comp-blast D_04 &amp;&amp; comp-blast C_08</run>
        <expect>Downstream blast at T0. Snapshot for delta vs T1/T2/T3.</expect>
        <if_mismatch>n/a — orientation only.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T0 && comp-blast D_00c._weighted_aua</run>
        <expect>Function-level blast for D_00c `_weighted_aua` per CTO §3.3 amendment. Per ADHC_ROUTER Phase 2 backlog item: function-level blast nodes may be MISSING for compiler-tool reasons.</expect>
        <if_mismatch>If function-level node is MISSING (per ADHC_ROUTER Phase 2 known gap), DO NOT skip — escalate via MCP to COO+CTO with the exact compiler error. Continue with script-level `comp-blast D_00c` as fallback.</if_mismatch>
      </step>
      <step>
        <run>comp-trace tagged_aua</run>
        <expect>Every reader of `tagged_aua` enumerated end-to-end. Used to validate per-5-advisor trace coverage.</expect>
        <if_mismatch>Document missing nodes.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse tagged_aua &amp;&amp; comp-platinum reverse fee_breakdown.no_fee.aua &amp;&amp; comp-platinum reverse aua_growth_pct</run>
        <expect>Producer + consumer paths for the three Group D primary fields. Anchors §3.3 deliverable.</expect>
        <if_mismatch>If any reverse-lookup returns empty, document — DO NOT fabricate.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before committing evidence pack">
      <step>
        <run>comp-build</run>
        <expect>Graph rebuilt fresh if stale. Required before comp-validate.</expect>
        <if_mismatch>If comp-build fails, MCP COO before proceeding.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/staudt_T0_artifacts/leaderboard.json &amp;&amp; comp-validate C_08 --artifact /tmp/staudt_T0_artifacts/fee_efficiency.json</run>
        <expect>Document validator output. Per AE 2026-04-17 finding: D_04 validator config has bug (windows[0] vs windows.{QTD,YTD,MAX} dict keys) — capture as gap, do NOT fix per §5 guardrail #1.</expect>
        <if_mismatch>Document gap. Continue.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after committing evidence pack">
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run above</run>
        <expect>One row per tool run with TO_ID=ADVI_STAUDT.A. Auto-append should fire if `.comp-graph/.agent_context` is set correctly to `SERIAL=0.4.0_DS_ClientPlatform~A` and `TO_ID=ADVI_STAUDT.A`.</expect>
        <if_mismatch>If rows missing, manually append per the log format in `org/compiler-tools-log.md`.</if_mismatch>
      </step>
      <step>
        <run>git worktree remove /tmp/staudt_T0</run>
        <expect>Scratch worktree cleaned up. Repo root remains on CLOUD tip.</expect>
        <if_mismatch>Force-remove via `git worktree remove --force /tmp/staudt_T0`.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    All under `data/black_diamond/diagnostics/STAUDT/T0_wednesday/`:

    1. **`state.md`** — Per PRD §4.1: one subsection per script in scope (B_01, C_00, C_08, D_00b, D_00c, D_01, D_02, D_04). For every field in §3.2, the formula text (code excerpt with line number) and a sample value from the pulled platinum JSON for each of the 5 top advisors (Travis Penfield, Kyle Sims, Hunter Lloyd, Alex Bright, Tim Rodgers) and firm-level. IO manifest snapshot for every script in scope. Validator config gaps documented (do not fix). Hash of the five platinum JSONs pulled.

    2. **`T0_evidence.json`** — Machine-readable field-value snapshot. Schema mirrors §3.2 field list. Used by ~D for delta-table population.

    3. **`group_d_tagged_aua_role_fee_decomposition.md`** — PRIMARY deliverable per §3.3 (NON-NEGOTIABLE):
       (a) Producer-sites table: one row per production site in §3.3 table, with function code excerpt + line range + formula in plain English at T0.
       (b) Per-5-advisor trace (Travis + Kyle + Hunter + Alex + Tim): at T0, sample `tagged_aua`, `fee_paying.aua`, `role_breakdown[role].aua` per-role, `no_fee.aua` top-level AND per-role, `aua_growth_pct`, `nna`. Firm-level aggregates same fields.
       (c) Divergence table: where does D_00c's `tagged_aua` disagree with D_02's for the same (advisor, role) key at T0? Does D_04's leaderboard override agree with either? What percentage of advisors have `sum(role_breakdown[*].aua) ≠ tagged_aua` at T0? Cite specific advisor IDs.
       (d) Definition vs source table: for every field in the production-site table, annotate whether the change at T0 vs prior was a definition change OR a source change. (At T0 this is the baseline — annotate "BASELINE" for every cell.)

    4. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_t0_wed_baseline.md` (or appropriate date if work spans days) citing the STAUDT deliverables + Compiler Tools section reproducing every `<run>` from `<compiler_tools_mandate>` with observed output and explicit pass/fail vs. `<expect>`.

    5. **compiler-tools-log.md** appended with one row per tool run (auto via `.comp-graph/.agent_context`).
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6: all four lanes read the same scripts (B_01, C_00, C_08, D_00c, D_00b, D_01, D_02, D_04, gold_validate_config.yaml, platinum/firm/leaderboard.json). **Write-collision is impossible** — read-only audit. **Directory collision** is prevented by lane-scoped evidence directory `STAUDT/T0_wednesday/` (~A only writes here; never to T1/T2/T3/SYNTHESIS). **Interpretation collision** is prevented by ~D owning all SYNTHESIS/* writes — if you have a synthesis-relevant observation that doesn't fit T0, MCP ~D rather than writing to SYNTHESIS/.
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7 (per-lane block):

    1. `state.md` committed under `STAUDT/T0_wednesday/` with: one subsection per script in scope, cited line ranges for every formula, sample values for 5 top advisors + firm, validator config gaps documented.
    2. `T0_evidence.json` committed: machine-readable field-value snapshot.
    3. `group_d_tagged_aua_role_fee_decomposition.md` committed per §3.3 — must contain ALL FOUR sub-tables (producer sites + per-5-advisor trace + divergence + definition-vs-source). Missing any sub-table = REWORK, not COMPLETE.
    4. `compiler-tools-log.md` appended with one row per tool run.
    5. Session log includes Compiler Tools section reproducing every `<run>` from `<compiler_tools_mandate>` with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK.
    6. Evidence-file-trace holds: every claim in `state.md` and `group_d_tagged_aua_role_fee_decomposition.md` traceable to a commit SHA + line range OR a pulled artifact hash. No "COO said" / "I remember" summaries.
    7. No scope creep — if you surface a fifth-bug candidate or a finding outside §3.2/§3.3, MCP CTO+COO rather than fixing or adding to deliverables silently.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5 (read verbatim before starting):

    1. **READ-ONLY.** No commits to `data/black_diamond/scripts/gold/`. No S3 writes. No gold-runner triggers. No `comp-validate` config edits (document gaps, do not fix).
    2. **Evidence-file-trace mandatory.** Every claim must cite file path + line range OR commit SHA + line range. No "COO said" summaries. No "I remember".
    3. **Lane collision avoidance.** ~A writes ONLY under `data/black_diamond/diagnostics/STAUDT/T0_wednesday/`. Never touch T1/T2/T3/SYNTHESIS/.
    4. **Scratch worktree for historical checkouts.** `git worktree add /tmp/staudt_T0 544877cc`. Never `git checkout 544877cc` at repo root.
    5. **S3 point-in-time retrieval.** Buckets are versioned for platinum/ artifacts but `gold/canonical/nna_atomic/` likely does NOT exist at T0 (CN-P1b backfill landed Thu ~10:02 ET). Document absences; do not fabricate.
    6. **Commit scope discipline.** Per-lane commits use `--only` with explicit path list, author = `0.4.0_DS_ClientPlatform~A`.
  </guardrails>

  <deadline>
    6 hours after COO GO message lands in your inbox.
  </deadline>

  <agent_context_setup>
    Before first comp-* run:
    ```bash
    mkdir -p .comp-graph && printf "SERIAL=0.4.0_DS_ClientPlatform~A\nTO_ID=ADVI_STAUDT.A\n" > .comp-graph/.agent_context
    ```
    This enables auto-append to `org/compiler-tools-log.md` for every comp-* tool call.
  </agent_context_setup>
</task_order>
