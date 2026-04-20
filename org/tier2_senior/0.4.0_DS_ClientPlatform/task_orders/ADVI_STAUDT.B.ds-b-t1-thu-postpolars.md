<task_order>
  <metadata>
    <id>ADVI_STAUDT.B</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-20</date>
    <status>staged</status><!-- CTO confirms shape before COO dispatches GO -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~B — T1 Thursday post-polars + post-perf-war-room</lane>
    <priority>P0 — gates fix-TO authoring on Friday breakage attribution</priority>
    <git_anchor>f177240b</git_anchor>
    <wall_clock>Thu 2026-04-16 ~22:30 ET</wall_clock>
    <scope_weight>HEAVY — includes polars parity probe + iterrows-to-dict parity probe</scope_weight>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§4.2 (lane scope), §3.2 (fields in scope), §3.3 (Group D PRIMARY focus), §5 (guardrails), §6 (cross-domain), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCP 20260420T120334Z — §3.3 amendment locking Group D tagged_aua / role-split / fee-split as PRIMARY scope</ref>
    <ref type="upstream">CTO MCP 20260417T213111Z — 4-bug audit ratification</ref>
    <ref type="cto-handoff">CTO MCP 20260420T~12:00Z — STAUDT PRD handoff</ref>
  </references>

  <objective>
    Deliver the T1 (Thu 2026-04-16 ~22:30 ET, git `f177240b`) checkpoint of ADVI gold + portal state. T1 captures the post-W4-CN/RA-cutover + post-polars-port + post-perf-war-room state. Includes two parity probes (polars vs pandas C_00; iterrows→to_dict rewrites on D_02/D_00b/D_00c/D_01/C_08) — a row-level delta > $0.01 in either probe is an audit finding for ~D's bug-attribution pack. Read-only audit only.
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

    <!-- Lane ~B specific scope (PRD §4.2 + §3.2) -->

    **Per-script audit at T1 `f177240b`:**
    - All scripts post-W4 CN/RA cutover (D_00c reads atomic per CN-P3 `d96da39d`; D_02 reads atomic per CN-P2 `ebd737e3` + `b3f6b1ee`; D_01 + D_00b + D_04 + C_08 reads atomic per CN-P4 `4e63038e` + CN-P5 `49eac17d`)
    - D_00c reads role_aua per RA-P3 `e53f0afa`; D_02 writes canonical_role_aua per RA-P2b `94600ff6`; D_01 reads role_aua per RA-P4 `4e63038e`; D_00b + C_08 read role_aua per RA-P5 `d9ab1719`
    - C_00 ported to polars (`f177240b`)
    - WAR-ROOM iterrows→to_dict rewrites: B_01 + B_00 (`22736cf7`), C_08 (`86e57e36`), D_02 (`e031d1f5`), D_00b (`a822e34d`), D_00c (`c7a7a5a9`), D_01 (`a7f1ee76`), D_03 (`1aef359b`)
    - B-series additions: D_02 weighted_avg_fee_bps denom (`5162fc1c`), canonical role order (`3e497ab8`), D_02 B3b (`1f91954c`), D_02 B3c (`4fbe26dd`), D_02 B9b (`be14c1f9`), C_08 B10 (`bb426933`)

    **Special scope — polars parity probe (PRD §4.2):**
    Checkout `544877cc` pandas-baseline C_00 + `f177240b` polars C_00 into two scratch worktrees. Run both against silver inputs for 2026-04-15 partition. Diff outputs (groupby+agg at L222, cumsum at L263). Any row-level delta > $0.01 is a finding for ~D's bug-attribution pack.

    **Special scope — iterrows→to_dict parity probe (PRD §4.2):**
    Same pattern for D_02 (`e031d1f5`), D_00b (`a822e34d`), D_00c (`c7a7a5a9`), D_01 (`a7f1ee76`), C_08 (`86e57e36`). For each, diff output JSON against pre-WAR-ROOM tip `bbb66f8f`-or-equivalent baseline. Reported field list MUST include `role_breakdown`, `fee_breakdown`, `tagged_aua`, `aua_growth_pct`. Document any row-level delta > $0.01.

    **Fields in scope (§3.2):** same as ~A — `tagged_aua`, `row.total_aua` fallback, `fee_paying.aua` / `fee_aua`, `fee_breakdown.no_fee.aua` (top-level + per-role), `aua_growth_pct` (D_00c:580 + D_04 override L2325-2340), `nna` and `nna_canonical` (D_02 summary vs daily vs D_00c vs D_04), `role_breakdown[role].aua`, `small_account_count` (D_02 B9b), `fee_summary.window_revenue` (D_02 B3b), `growth.ttm_nna` (D_02 B3c), `weighted_avg_fee_bps` (T1 denominator flip).

    **S3 platinum snapshots (T1 cutoff = 2026-04-17 00:00 UTC):**
    - `s3://opal-data-bd/platinum/firm/leaderboard.json` at latest version ≤ 2026-04-17 00:00 UTC
    - `s3://opal-data-bd/platinum/firm/fee_efficiency.json` same cutoff
    - `s3://opal-data-bd/platinum/advisors/{travis,kyle,hunter,alex,tim}/summary.json`
    - `s3://opal-data-bd/platinum/firm/header_metrics.json`
    - `s3://opal-data-bd/gold/canonical/nna_atomic/2026-04-15.parquet` (PRESENT at T1 — CN-P1b backfill complete)
    - `s3://opal-data-bd/gold/canonical/role_aua/2026-04-15.parquet` (PRESENT at T1 — RA-P1b backfill complete)
    - `s3://opal-data-bd/gold/canonical/nna/2026-04-15.parquet` (still present — pre-revert)
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write — T1 reconstruction setup">
      <step>
        <run>git worktree add /tmp/staudt_T1 f177240b</run>
        <expect>Clean checkout of `f177240b` into scratch worktree per PRD §5 guardrail #4.</expect>
        <if_mismatch>STOP. Force-remove + retry; if still failing, MCP COO.</if_mismatch>
      </step>
      <step>
        <run>git worktree add /tmp/staudt_T0 54477cc</run>
        <expect>Pandas-baseline C_00 + pre-WAR-ROOM tips for parity probes. (Note: this worktree may collide with ~A's — coordinate via MCP if both lanes run concurrently. Per PRD §6, prefer per-lane worktree paths e.g. `/tmp/staudt_T1B_baseline`.)</expect>
        <if_mismatch>If collision with ~A active worktree, use `/tmp/staudt_T1B_baseline` instead.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T1 && comp-pipescript io D_00c &amp;&amp; comp-pipescript io D_02 &amp;&amp; comp-pipescript io D_04</run>
        <expect>D_00c reads CANONICAL_NNA_ATOMIC_PREFIX (CN-P3 terminal). D_02 reads CANONICAL_NNA_ATOMIC_PREFIX (CN-P2 terminal). D_04 reads CANONICAL_NNA_ATOMIC_PREFIX (CN-P5 not-yet-reverted).</expect>
        <if_mismatch>If D_04 reads non-atomic at T1, the git anchor is wrong — re-verify `f177240b`. STOP and MCP COO.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T1 && comp-pipescript io C_08 &amp;&amp; comp-pipescript io D_00b &amp;&amp; comp-pipescript io D_01</run>
        <expect>All three read CANONICAL_NNA_ATOMIC_PREFIX at T1 (CN-P5). Schema delta vs T0 nna/ — atomic has 22 cols, nna/ has 14. C_08 SHOULD crash on aua_current/growth at T1 reading atomic — confirm whether T1 was actually run end-to-end or whether the gold chain stalled here.</expect>
        <if_mismatch>If reads do not match expectation, document deviation. C_08 crash absence at T1 is itself a finding — was the chain ever run end-to-end at T1?</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T1 && comp-blast D_00c &amp;&amp; comp-blast D_04 &amp;&amp; comp-blast C_08 &amp;&amp; comp-blast D_00c._weighted_aua</run>
        <expect>Blast snapshot at T1. Function-level _weighted_aua per CTO §3.3.</expect>
        <if_mismatch>Function-level node MISSING per ADHC_ROUTER Phase 2 backlog → MCP COO+CTO; do not skip.</if_mismatch>
      </step>
      <step>
        <run>comp-trace tagged_aua &amp;&amp; comp-platinum reverse tagged_aua &amp;&amp; comp-platinum reverse fee_breakdown.no_fee.aua &amp;&amp; comp-platinum reverse aua_growth_pct</run>
        <expect>Producer + consumer paths for the three Group D primary fields at T1 (post-CN/RA cutover state).</expect>
        <if_mismatch>Document missing nodes.</if_mismatch>
      </step>
      <step>
        <run>POLARS PARITY PROBE: cd /tmp/staudt_T0 && python data/black_diamond/scripts/gold/C_00.canonical_performance.py --partition 2026-04-15 --out /tmp/staudt_C00_pandas.parquet ; cd /tmp/staudt_T1 && python data/black_diamond/scripts/gold/C_00.canonical_performance.py --partition 2026-04-15 --out /tmp/staudt_C00_polars.parquet ; python -c "import pandas as pd; a=pd.read_parquet('/tmp/staudt_C00_pandas.parquet'); b=pd.read_parquet('/tmp/staudt_C00_polars.parquet'); print((a.merge(b, on=KEYS, suffixes=('_pd','_pl')).assign(delta=lambda d: (d.value_pd - d.value_pl).abs()).query('delta > 0.01')))"</run>
        <expect>Empty diff (zero rows with delta > $0.01). Polars port `f177240b` should be byte-equivalent at row level. Any row-level delta > $0.01 = FINDING for ~D's bug_attribution.md.</expect>
        <if_mismatch>Document EVERY row with delta > $0.01 in the parity table. Annotate (advisor_id, account_id, snapshot_date, pandas_value, polars_value, delta_dollars). Surface to ~D MCP.</if_mismatch>
      </step>
      <step>
        <run>ITERROWS→TO_DICT PARITY PROBE: same pattern for D_02 (e031d1f5 vs pre), D_00b (a822e34d vs pre), D_00c (c7a7a5a9 vs pre), D_01 (a7f1ee76 vs pre), C_08 (86e57e36 vs pre). Diff output JSON keys: role_breakdown, fee_breakdown, tagged_aua, aua_growth_pct.</run>
        <expect>Empty diff. WAR-ROOM rewrites should be byte-equivalent at field level on the four required keys. Any delta = FINDING.</expect>
        <if_mismatch>Document every (script, advisor_id, field, before_value, after_value, delta) tuple. This becomes a primary input to ~D's bug attribution.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before committing evidence pack">
      <step>
        <run>comp-build && comp-validate D_04 --artifact /tmp/staudt_T1_artifacts/leaderboard.json && comp-validate C_08 --artifact /tmp/staudt_T1_artifacts/fee_efficiency.json && comp-validate D_02 --artifact /tmp/staudt_T1_artifacts/advisor_book_sample.json</run>
        <expect>Document validator output. Capture validator config gaps (D_04 windows[0] vs windows.{QTD,YTD,MAX} bug per AE 2026-04-17 — DO NOT FIX). B_01 will SKIP per session-32 finding — capture the SKIP.</expect>
        <if_mismatch>Document gap. Continue.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after committing evidence pack">
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run above</run>
        <expect>One row per tool run with TO_ID=ADVI_STAUDT.B. Auto-append should fire if `.comp-graph/.agent_context` is set to `SERIAL=0.4.0_DS_ClientPlatform~B` and `TO_ID=ADVI_STAUDT.B`.</expect>
        <if_mismatch>Manually append per the log format.</if_mismatch>
      </step>
      <step>
        <run>git worktree remove /tmp/staudt_T1 &amp;&amp; git worktree remove /tmp/staudt_T0 (or /tmp/staudt_T1B_baseline)</run>
        <expect>Scratch worktrees cleaned up.</expect>
        <if_mismatch>Force-remove.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    All under `data/black_diamond/diagnostics/STAUDT/T1_thursday/`:

    1. **`state.md`** — Per PRD §4.2: per-script subsections + §3.2 field list with line range + sample value per 5 top advisors + firm. IO manifest. Validator config gaps.

    2. **`T1_evidence.json`** — Machine-readable field-value snapshot.

    3. **`group_d_tagged_aua_role_fee_decomposition.md`** — PRIMARY deliverable per §3.3 (NON-NEGOTIABLE):
       (a) Producer-sites table at T1.
       (b) Per-5-advisor trace (Travis + Kyle + Hunter + Alex + Tim) at T1.
       (c) Divergence table at T1 — cite specific advisor IDs where sum(role_breakdown[*].aua) ≠ tagged_aua.
       (d) Definition vs source table T0→T1 deltas annotated.

    4. **`polars_parity_C00.md`** — Polars vs pandas C_00 parity probe results. Either "no delta found" with hash equality evidence, OR a delta table listing every (advisor_id, account_id, snapshot_date, pandas_value, polars_value, delta_dollars) row with delta > $0.01.

    5. **`war_room_iterrows_parity.md`** — One sub-section per script (D_02, D_00b, D_00c, D_01, C_08). Each subsection: either "no delta found" + hash, OR delta table for the four required keys (role_breakdown, fee_breakdown, tagged_aua, aua_growth_pct).

    6. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_t1_thu_postpolars.md` (or appropriate date) citing STAUDT deliverables + Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`.

    7. **compiler-tools-log.md** appended.
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6: read-only across all scripts. Write-collision impossible. Lane-scoped evidence dir `STAUDT/T1_thursday/` (~B only). If parity-probe surfaces a finding that ~D will need verbatim in bug_attribution.md, MCP ~D directly with the (script, advisor_id, field, delta) tuple — do not write to SYNTHESIS/.

    **Worktree-path coordination with ~A:** if both lanes run concurrently and both need T0 baseline (~A for primary, ~B for parity-probe baseline), use distinct paths: `/tmp/staudt_T0` (~A) vs `/tmp/staudt_T1B_baseline` (~B).
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7 (per-lane block):

    1. `state.md` committed under `STAUDT/T1_thursday/` with all required sub-content.
    2. `T1_evidence.json` committed.
    3. `group_d_tagged_aua_role_fee_decomposition.md` committed per §3.3 — must contain ALL FOUR sub-tables. Missing any sub-table = REWORK.
    4. **`polars_parity_C00.md` committed** — either delta table OR "no delta found" with hash equality evidence. Missing = REWORK.
    5. **`war_room_iterrows_parity.md` committed** — five script subsections (D_02, D_00b, D_00c, D_01, C_08). Missing any subsection = REWORK.
    6. `compiler-tools-log.md` appended with one row per tool run.
    7. Session log includes Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK.
    8. Evidence-file-trace holds: every claim traceable to commit SHA + line range OR pulled artifact hash.
    9. No scope creep — fifth-bug candidate or out-of-§3.2/§3.3 finding triggers MCP CTO+COO, not silent inclusion.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5 (read verbatim before starting):

    1. **READ-ONLY.** No commits to `data/black_diamond/scripts/gold/`. No S3 writes. No gold-runner triggers. No `comp-validate` config edits.
    2. **Evidence-file-trace mandatory.**
    3. **Lane collision avoidance.** ~B writes ONLY under `STAUDT/T1_thursday/`.
    4. **Scratch worktree for historical checkouts.** Never `git checkout` at repo root.
    5. **S3 point-in-time retrieval.** At T1 cutoff (2026-04-17 00:00 UTC) all three NNA partitions exist (`nna_atomic/`, `nna/`, `role_aua/`). Document if a snapshot version is missing.
    6. **Commit scope discipline.** `--only` with explicit path list, author = `0.4.0_DS_ClientPlatform~B`.
    7. **Parity-probe execution time budget:** if either probe pulls > 4 hours of compute, MCP COO with the wall-clock and the partial diff so we can decide truncation vs continuation. Do not silently kill.
  </guardrails>

  <deadline>
    8 hours after COO GO message lands in your inbox (heavier scope than ~A per PRD §4.2).
  </deadline>

  <agent_context_setup>
    Before first comp-* run:
    ```bash
    mkdir -p .comp-graph && printf "SERIAL=0.4.0_DS_ClientPlatform~B\nTO_ID=ADVI_STAUDT.B\n" > .comp-graph/.agent_context
    ```
  </agent_context_setup>
</task_order>
