<task_order>
  <metadata>
    <id>ADVI_STAUDT.D</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-20</date>
    <status>pending</status><!-- CTO conditional-approved 20260420T~12:49Z; comp-build rework + minor polish landed; COO dispatched GO to ~D inbox 20260420T~12:55Z. Phase 0 data collection may begin immediately; Phase 1 findings + 5 SYNTHESIS docs gate on ~C findings MCP (which transitively confirms ~A + ~B fired). -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~D — Layer: Group D audit + cross-layer SYNTHESIS (dual role)</lane>
    <model>LAYER × 4-checkpoint MATRIX. ~D owns Group D layer (D_00..D_04) across all 4 checkpoints AND owns the 5 SYNTHESIS deliverables that cite the upstream lane findings. Andrew 2026-04-20: "layer scoped AND time scoped — at each of those times, watch how the layer evolved, cross-reference, comprehensive."</model>
    <priority>P0 — most-downstream + synthesis owner. Findings + synthesis pack are THE deliverable COO uses to author every fix-TO.</priority>
    <checkpoints>T0=544877cc | T1=f177240b | T2=ae759bbb | T3=cd177553</checkpoints>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§3.0 (Two failure classes — lead-with), §3.3 (Group D PRIMARY focus — primary scope), §3.4 (Group B+C material-change — secondary grounding for synthesis), §4.0 (investigative discipline), §4.4 (lane ~D), §4.5 (sequencing), §5 (guardrails), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCPs 20260420T~12:14Z (§3.0) + 20260420T120334Z (§3.3) + 20260420T121431Z (§3.4) + 20260420T~12:30Z (§4 LAYER-scoped restructure)</ref>
    <ref type="andrew-clarification">2026-04-20: layer-scoped AND time-scoped, not either/or. Each lane watches its layer's evolution across all 4 timepoints; ~D synthesizes across all 4 lanes × 4 checkpoints.</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="ADVI_STAUDT.A" status="staged" required="layer_a_findings.md committed + evidence_pack.json"/>
    <dependency agent="0.4.0_DS_ClientPlatform~B" task="ADVI_STAUDT.B" status="staged" required="layer_b_findings.md + b01_evolution_trace.md + b01_cusip_coverage_probe.md + evidence_pack.json"/>
    <dependency agent="0.4.0_DS_ClientPlatform~C" task="ADVI_STAUDT.C" status="staged" required="layer_c_findings.md + c00_polars_parity_probe.md + c01_nna_schema_diff.md + c03_phantom_outflow_probe.md + evidence_pack.json + MCP fired"/>
  </dependencies>

  <objective>
    Two-part lane:
    Part 1 — Audit the Group D layer (D_00, D_00b, D_00c, D_01, D_02, D_03, D_04) across all 4 checkpoints; produce per-checkpoint Group D evidence per §3.3 PRIMARY focus.
    Part 2 — Synthesize ~A/~B/~C findings + your Group D evidence into 5 SYNTHESIS deliverables: master Group D decomposition table (2A), cross-layer propagation matrix (2B), 4-checkpoint delta table (2C), bug attribution pack (2D), COO handoff briefing (2E). 2E is THE deliverable COO uses to author every fix-TO. Read-only audit only.
  </objective>

  <scope>
    <!-- VERBATIM from ADVI_STAUDT.md §3.0 (Two primary failure classes) per CTO MCP 20260420T~12:14Z. Lead-with framing — do not paraphrase. -->

    ### 3.0 Two primary failure classes (Andrew 2026-04-20 — lead every lane TO scope with this)

    **Class 1 — NNA definition change** (grain AND path)
    - **Grain sub-class:** D_02 `_nna_since` flipped per-advisor cumulative → per-(date, advisor, role) daily-grain at CN-P2 (commits `b3f6b1ee` + `ebd737e3` Thu 2026-04-16 12:31–12:35 ET). COO audit bug #1 — currently hidden in the modal via `SHOW_NNA=false` (`AdvisorBookAccountModal.tsx:38`).
    - **Path sub-class:** Canonical prefix split — see §3.0 in ~A TO. ~D synthesizes the live schism into the Group D decomposition table (2A) and bug attribution (2D) using ~C's `c01_nna_schema_diff.md` as the upstream evidence.

    **Class 2 — Group D mapping ambiguity** (tagged_aua source + role-split + fee-split) — see §3.0 in ~A TO. **~D OWNS the per-checkpoint sum-invariant column for 5 top advisors in `group_d_tagged_aua_decomposition.md`.**

    **MANDATORY INVARIANT per checkpoint per advisor (~D's primary measurement responsibility):**
    - `sum(role_breakdown[*].aua) == tagged_aua`
    - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`

    Violations rolled into `bug_attribution.md` with advisor ID + checkpoint + delta magnitude + likely-source-layer (silver/A/B/C/D) per cross-layer propagation matrix.

    <!-- VERBATIM from ADVI_STAUDT.md §3.3 (Group D PRIMARY FOCUS) per CTO MCP 20260420T120334Z. The primary-focus language must survive into the TO — no paraphrasing. -->

    ### 3.3 GROUP D PRIMARY FOCUS — tagged_aua / role-split / fee-split (PRIMARY SCOPE, non-negotiable)

    Per Andrew 2026-04-20: the Group D logic touching `tagged_aua`, role-split AUA, and fee-split AUA is the **primary** audit scope. Every lane treats the following Group D production sites as the highest-priority targets. Evidence packs must lead with these.

    **Canonical Group D production sites (enumerate formula + inputs + line range at EVERY checkpoint):**

    | Site | Script : line | Role | What to capture |
    |---|---|---|---|
    | **D_00c `_weighted_aua`** | `D_00c.portal_leaderboard.py:881` | Role-split AUA producer | Function body, caller list, role-weight formula, advisor cohort where split-weight diverges from total. |
    | **D_00c `tagged_aua` column** | `D_00c:528` (row.total_aua fallback) | Leaderboard `tagged_aua` source | Fallback OR primary? What feeds `row.total_aua`? Does D_00c read from D_02? |
    | **D_00c `no_fee_aua`** | `D_00c:565` (`max(0, tagged_aua - fee_aua)` silent-clip) | Fee-split no-fee producer | Clip behavior + per-advisor `no_fee.aua = 0` cohort size at each checkpoint. Travis drops off here. |
    | **D_00c `aua_growth_pct`** | `D_00c:580` | Growth rate numerator/denominator | What is num, what is denom, do both trace to same tagged_aua source? |
    | **D_00c `role_breakdown[role].aua`** | D_00c `_weighted_aua` output | Per-role AUA breakdown | Is sum across roles equal to `tagged_aua`? Where does it diverge? |
    | **D_02 `tagged_aua` / `summary.tagged_aua`** | `D_02.advisor_client_detail.py` `build_advisor_books` | Book.json per-advisor `tagged_aua` producer | Formula, inputs, per-role or per-account fold? |
    | **D_02 `_nna_since` / per-role NNA** | CN-P2 `b3f6b1ee` + `ebd737e3` | Per-role NNA producer | Daily vs cumulative grain at each checkpoint. |
    | **D_02 `role_breakdown` / `canonical_role_aua`** | RA-P2b `94600ff6` | Role-AUA canonical producer | Per-date per (advisor, role). Consumer: D_01. |
    | **D_02 `weighted_avg_fee_bps`** | `5162fc1c` | Fee-rate producer | Denom: all accounts vs fee-paying-only. T1 flipped. |
    | **D_04 OVERRIDE `aua_growth_pct` numerator** | `D_04:2325-2328` (`fe999416` 2026-04-09) | Leaderboard override | What does it swap from/to? |
    | **D_04 OVERRIDE `aua_growth_pct` denominator** | `D_04:2335-2340` (`6391b96c` 2026-04-09) | Same | Andrew: "Ratio = growth(pair A) displayed against pair B." |
    | **D_04 `fee_breakdown.no_fee.aua` top-level** | `D_04` post-processing | Leaderboard top-level | B1.fix `5114984b` swept role-level NOT top-level. |
    | **C_08 `role_breakdown.aua` canonical override** | RA-P5 `d9ab1719` | C_08 role-breakdown source for fee_efficiency.json | Override + mid-period-new-advisor fallback. (~C lane primary; ~D incorporates into Group D decomposition.) |
    | **C_08 defensive backfill `aua_current` / `growth`** | `C_08:644` (`9e537f9f`) | Silent zero-fill mask | T3 only. MUST be flagged — it masks the NNA-prefix-split schema mismatch. |

    <!-- VERBATIM from ADVI_STAUDT.md §4.4 (Lane ~D — Group D audit + synthesis) per CTO PRD restructure. -->

    ### 4.4 Lane ~D — Group D audit + synthesis (dual role)

    **Layer scope:** D_00, D_00b, D_00c, D_01, D_02, D_03, D_04. Reads A/B/C output. Produces all platinum/*.json the portal consumes.

    **Per-checkpoint audit (Part 1 — Group D layer):**
    Same 4× pattern. For each checkpoint, produce the Group D primary-focus evidence mandated by §3.3:
    - Producer-site table per script per checkpoint
    - 5-advisor trace (Travis + Kyle + Hunter + Alex + Tim) at each checkpoint
    - Divergence table per checkpoint (D_00c vs D_02 tagged_aua disagreement; % advisors with sum-invariant violation)
    - Definition-change vs source-change annotation per field per checkpoint

    **Synthesis (Part 2 — cross-layer):**

    - **Deliverable 2A — Group D master decomposition table:** `STAUDT/SYNTHESIS/group_d_tagged_aua_decomposition.md` per §3.3. Master table, one row per (production-site × field), 4 checkpoint columns with formula text + 5-advisor sample values + divergence class. Primary artifact COO cites in fix-TO scope.
    - **Deliverable 2B — Cross-layer propagation matrix:** `STAUDT/SYNTHESIS/group_bc_propagation_matrix.md` per §3.4. One row per B/C material change (from ~B/~C findings), tracing: change → affected C artifacts → affected D artifacts → affected platinum JSONs → affected portal components. Any row where a B/C change lands at platinum without being captured in the Group D bug attribution is an extra finding class.
    - **Deliverable 2C — 4-checkpoint delta table:** `STAUDT/SYNTHESIS/delta_table.md` + `delta_table.json`. One row per (script, field, advisor-or-firm). Columns: formula@T0..T3 + sample-value@T0..T3 + delta-class (identity / cosmetic / numeric / definitional / structural / schema-path).
    - **Deliverable 2D — Bug attribution pack:** `STAUDT/SYNTHESIS/bug_attribution.md`. For each of COO's 4 bugs + NNA-path split (§2.3) + any layer-A/B/C-surfaced defect + any sum-invariant violation: one section with (a) symptom, (b) commit SHA, (c) lines changed, (d) layer of origin (silver/A/B/C/D), (e) downstream blast, (f) recommendation.
    - **Deliverable 2E — COO handoff briefing:** `STAUDT/SYNTHESIS/coo_handoff.md`. Plain English. Restore-to-T0 vs keep-T1/T2/T3 vs hybrid-with-rewrite — one call per field/bug. Per-call rationale citing specific rows of decomposition / propagation / delta tables. Per-call proposed fix-TO sketch (DS lane, scope, acceptance criteria machine-checkable).

    **Investigative discipline (§4.0):** layer × 4 checkpoints × cross-layer synthesis. Andrew clarification: cross-reference is the point. Every recommendation in coo_handoff.md cites a specific row of decomposition / propagation / delta tables AND a layer-of-origin (silver/A/B/C/D) per propagation matrix.

    **T0 pre-window-state note (CTO MCP 20260420T~12:49Z):** T0 anchor `544877cc` is "imperfect but accepted" per PRD §3.1 — already contains pre-window Group D regressions including the W6-005 split-weighted change (`0804b377` 2026-04-13) and DE allChecked removal (`9f6faf9` 2026-04-13). These predate the audit window. In `bug_attribution.md`, classify them as "pre-window inherited state at T0" with original commit SHA cited. They are NOT "introduced at T0" — but they ARE in scope for the restore/keep/rewrite decision in `coo_handoff.md` because the W6-005 split-weighted is the source of the Travis $82M-vs-$434M divergence Andrew flagged.
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="parallel data collection (no findings-file gate)">
      <step>
        <run>git worktree add /tmp/staudt_layerD_T0 544877cc &amp;&amp; git worktree add /tmp/staudt_layerD_T1 f177240b &amp;&amp; git worktree add /tmp/staudt_layerD_T2 ae759bbb &amp;&amp; git worktree add /tmp/staudt_layerD_T3 cd177553</run>
        <expect>Four scratch worktrees per PRD §5 #4.</expect>
        <if_mismatch>Force-remove + retry; MCP COO if blocked.</if_mismatch>
      </step>
      <step>
        <run>For each Tx in {T0, T1, T2, T3}: cd /tmp/staudt_layerD_Tx &amp;&amp; comp-build</run>
        <expect>1,162 ± 50 nodes / 940 ± 50 edges built per checkpoint. Node/edge count variance between checkpoints is itself a finding — document drift in `group_d_inventory.md` and roll into `delta_table.md`.</expect>
        <if_mismatch>If comp-build fails inside a worktree, investigate before falling back. Do NOT skip — skipping reads wrong-checkpoint state from the repo-root graph (CLOUD tip = T3) and invalidates the entire layer × 4-checkpoint matrix. Per CTO MCP 20260420T~12:49Z (shape-review rework).</if_mismatch>
      </step>
      <step>
        <run>For each Tx in {T0, T1, T2, T3}: cd /tmp/staudt_layerD_Tx &amp;&amp; comp-pipescript io D_00 &amp;&amp; comp-pipescript io D_00b &amp;&amp; comp-pipescript io D_00c &amp;&amp; comp-pipescript io D_01 &amp;&amp; comp-pipescript io D_02 &amp;&amp; comp-pipescript io D_03 &amp;&amp; comp-pipescript io D_04</run>
        <expect>READS + WRITES + COLUMN GAPS per script per checkpoint. At T3, D_04 reads CANONICAL_NNA_PREFIX (reverted); D_00c + D_02 read CANONICAL_NNA_ATOMIC_PREFIX (CN-P2/P3 terminal); C_08 reads CANONICAL_NNA_PREFIX with defensive backfill at L644.</expect>
        <if_mismatch>If T3 reads do not match expected, the NNA-path-split status changed since CTO PRD pass — re-anchor §2.3 of bug_attribution.md.</if_mismatch>
      </step>
      <step>
        <run>For each Tx: cd /tmp/staudt_layerD_Tx &amp;&amp; comp-blast D_00c &amp;&amp; comp-blast D_04 &amp;&amp; comp-blast C_08 &amp;&amp; comp-blast D_00c._weighted_aua</run>
        <expect>Per-checkpoint blast snapshot. Function-level _weighted_aua per CTO §3.3 amendment.</expect>
        <if_mismatch>Function-level node MISSING per ADHC_ROUTER Phase 2 backlog → MCP COO+CTO; do not skip.</if_mismatch>
      </step>
      <step>
        <run>For each Tx: comp-trace tagged_aua &amp;&amp; comp-platinum reverse tagged_aua &amp;&amp; comp-platinum reverse fee_breakdown.no_fee.aua &amp;&amp; comp-platinum reverse aua_growth_pct</run>
        <expect>Producer + consumer paths for the three Group D primary fields per checkpoint.</expect>
        <if_mismatch>Document missing nodes.</if_mismatch>
      </step>
      <step>
        <run>For each Tx: pull platinum/firm/leaderboard.json + platinum/advisors/{travis,kyle,hunter,alex,tim}/summary.json + platinum/firm/header_metrics.json at versioned cutoff per checkpoint. Compute sum-invariant per advisor per checkpoint.</run>
        <expect>4-checkpoint × 5-advisor × 2-invariant matrix populated. T2/T3 may show invariant violations (Travis $82M split vs $434M unsplit; no-fee silent clip).</expect>
        <if_mismatch>Cite specific advisor + checkpoint + delta in bug_attribution.md.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="layer_d_findings + synthesis writes — GATES ON ~A + ~B + ~C MCPs">
      <step>
        <run>WAIT for ~C's MCP fire (which transitively confirms ~A + ~B fired). Read all three findings files + all evidence packs + all probe documents. ACK ~C via RAVC step 2.</run>
        <expect>Three findings files committed + MCPs received. ~D ready to write Part 1 layer-D + Part 2 synthesis.</expect>
        <if_mismatch>If any upstream MCP missing, MCP that lane directly; escalate to COO if blocked.</if_mismatch>
      </step>
      <step>
        <run>Phase 2 schema-check pass at T3 (CLOUD tip): comp-cache collisions &amp;&amp; comp-transform schema-check AdvisorsTab &amp;&amp; comp-transform schema-check ClientsTab &amp;&amp; comp-transform schema-check AdvisorIntelligence</run>
        <expect>Per PRD §4.4 mandate — three leaderboard consumers. MISSING / UNUSED / NOTE captured. PartnerAnalytics MISSING `period` at L454 is pre-existing (not your scope).</expect>
        <if_mismatch>Any new MISSING/UNUSED mapping to Group D fields = FE-side rendering risk → bug_attribution.md.</if_mismatch>
      </step>
      <step>
        <run>Synthesize Part 1 (layer_d_findings.md) + 5 SYNTHESIS docs (2A/2B/2C/2D/2E)</run>
        <expect>All 6 deliverables committed. Every claim cites commit SHA + line range OR upstream evidence-pack row. Every recommendation in 2E cites a specific row of 2A/2B/2C/2D AND a layer-of-origin per 2B propagation matrix.</expect>
        <if_mismatch>If unable to ground a recommendation in evidence, mark "needs further investigation" rather than fabricating.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post-synthesis — final handoff">
      <step>
        <run>MCP CTO + COO + Andrew with one-paragraph executive summary + link to coo_handoff.md + count of recommendations + count of fix-TO candidates per layer-of-origin</run>
        <expect>Andrew receives review notice via the chain. COO begins fix-TO authoring on receipt.</expect>
        <if_mismatch>Direct file-write to inboxes if MCP fails.</if_mismatch>
      </step>
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run (per checkpoint × per script + Phase 1 schema-check pass)</run>
        <expect>Auto-append fires.</expect>
        <if_mismatch>Manual append.</if_mismatch>
      </step>
      <step>
        <run>git worktree remove /tmp/staudt_layerD_T0 &amp;&amp; git worktree remove /tmp/staudt_layerD_T1 &amp;&amp; git worktree remove /tmp/staudt_layerD_T2 &amp;&amp; git worktree remove /tmp/staudt_layerD_T3</run>
        <expect>Cleaned up.</expect>
        <if_mismatch>Force-remove.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    Per PRD §4.4:

    Part 1 — Group D layer evidence (under `data/black_diamond/diagnostics/STAUDT/layer_D/`):
    1. `group_d_inventory.md` — touched-script list + 4-checkpoint commit diff per D-script.
    2. `layer_d_findings.md` — definitive answer + evidence per claim + upstream-consistency reference to ~A + ~B + ~C findings + per-checkpoint sum-invariant violations.
    3. `evidence_pack.json` — hashes + row counts + per-checkpoint sample figures + 5-advisor invariant matrix.

    Part 2 — Cross-layer SYNTHESIS (under `data/black_diamond/diagnostics/STAUDT/SYNTHESIS/`):
    4. **`group_d_tagged_aua_decomposition.md` (2A)** — master table per §3.3. One row per (Group D production site × field), four checkpoint columns with formula text + 5-advisor sample values + divergence class. Per-checkpoint sum-invariant column populated.
    5. **`group_bc_propagation_matrix.md` (2B)** — one row per B/C material change (from ~B/~C findings) tracing C → D → platinum → portal. Extra-class findings (B/C change at platinum NOT in bug_attribution.md) flagged.
    6. **`delta_table.md` + `delta_table.json` (2C)** — 4-checkpoint field × checkpoint matrix populated for every field in §3.2 with delta-class tagged.
    7. **`bug_attribution.md` (2D)** — one section per COO-bug + NNA-path-split + every layer-A/B/C-surfaced defect + every sum-invariant violation + every FE schema-check / cache-collision finding. Each section: symptom + commit SHA + lines + layer of origin + downstream blast + recommendation.
    8. **`coo_handoff.md` (2E)** — PRIMARY COO INPUT. Plain English. Restore-to-T0 vs keep-T1/T2/T3 vs hybrid-with-rewrite per field/bug. Per-call rationale citing specific rows of 2A/2B/2C/2D. Per-call proposed fix-TO sketch (DS lane, scope, acceptance criteria machine-checkable). COO uses this directly to author the fix-PRD + fix-TOs without re-investigation.

    Plus:
    9. **MCP handoff** to CTO + COO + Andrew at synthesis-commit time.
    10. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_layer_d_and_synthesis.md` with Compiler Tools section reproducing every `<run>` with observed output and pass/fail vs. `<expect>`.
    11. **`org/compiler-tools-log.md`** appended.
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6 + §4.5:
    - **Upstream gate:** ~D blocks on ~C MCP (which transitively confirms ~A + ~B fired). Phase 0 data collection runs in parallel; Phase 1 findings + synthesis writes block on ~C.
    - **No downstream gate:** ~D is the last lane. Final MCP to CTO + COO + Andrew.
    - **Lane collision avoidance:** ~D writes ONLY under `STAUDT/layer_D/` AND `STAUDT/SYNTHESIS/`. ~D OWNS SYNTHESIS/ exclusively.
    - **No upstream rewrites after ~D consumes:** if ~D surfaces a suspect upstream cause not in ~A/~B/~C findings, MCP that lane for append-only validation rather than re-investigation.
    - **RAVC:** ACK ~C MCP before writing.
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7 ~D block:

    1. `group_d_inventory.md` + `layer_d_findings.md` + `evidence_pack.json` committed under `STAUDT/layer_D/`.
    2. **`group_d_tagged_aua_decomposition.md` (2A)** committed per §3.3 — master table + per-advisor sum-invariant column populated for all 5 top advisors per checkpoint.
    3. **`group_bc_propagation_matrix.md` (2B)** committed per §3.4 — every B/C change from ~B/~C findings has a row tracing C → D → platinum → portal.
    4. **`delta_table.md` + `delta_table.json` (2C)** committed — 4-checkpoint field × checkpoint matrix populated for every field in §3.2 with delta-class tagged.
    5. **`bug_attribution.md` (2D)** committed — one section per COO-bug + NNA-path-split + every layer-A/B/C-surfaced defect + every sum-invariant violation + every FE schema-check / cache-collision finding.
    6. **`coo_handoff.md` (2E)** committed — explicit per-bug recommendation + proposed fix-TO sketch (DS lane, scope, acceptance criteria machine-checkable). Every recommendation cites a specific row of 2A/2B/2C/2D AND a layer-of-origin per 2B.
    7. **MCP handoff sent** to CTO + COO + Andrew.
    8. Session log includes Compiler Tools section reproducing every `<run>` with observed output and pass/fail vs. `<expect>`. Missing rows = REWORK.
    9. `org/compiler-tools-log.md` appended.
    10. Evidence-file-trace holds — every claim traceable to commit SHA + line range OR pulled artifact hash OR specific row of an upstream evidence pack (~A/~B/~C).
    11. Recommendations are SPECIFIC (file + line + proposed change), not "we should think about". Fix-TO scope must be authorable by COO without re-investigation.
    12. Delta-class taxonomy self-consistent across delta_table — normalize across ~A/~B/~C input variations.
    13. Rule-out discipline (§4.0): grounded in D-layer evidence + cited upstream layer findings.
    14. No scope creep — fifth-bug candidate triggers MCP CTO+COO for inclusion decision.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5:

    1. **READ-ONLY.**
    2. **Evidence-file-trace mandatory.** Every claim cites file path + line range OR commit SHA + line range OR specific upstream evidence-pack row.
    3. **Lane collision avoidance.** ~D OWNS SYNTHESIS/* writes exclusively + writes layer_D/* under its own lane.
    4. **Scratch worktree per checkpoint** — `/tmp/staudt_layerD_T0..T3`.
    5. **S3 point-in-time retrieval** for current T3 platinum pulls + dated platinum versions per checkpoint.
    6. **Commit scope discipline** — `--only`, author = `0.4.0_DS_ClientPlatform~D`.
    7. **No parallel commits to synthesis doc.** ~D owns SYNTHESIS/* — others MCP if they have a finding to add.
    8. **Recommendation specificity bar:** every fix-TO sketch in coo_handoff.md must be authorable by COO into a real TO without re-investigation. If ~D cannot specify (file + line + proposed change + acceptance criterion), flag as "needs further investigation" rather than fabricating.
  </guardrails>

  <deadline>
    12 hours after ~C findings MCP (per PRD §4.5 — heaviest lane: layer-D audit + 5 SYNTHESIS docs).
  </deadline>

  <agent_context_setup>
    Before first comp-* run:
    ```bash
    mkdir -p .comp-graph && printf "SERIAL=0.4.0_DS_ClientPlatform~D\nTO_ID=ADVI_STAUDT.D\n" > .comp-graph/.agent_context
    ```
  </agent_context_setup>

  <sequencing_summary>
    Per PRD §4.5 — ~D is Phase 4: ~C MCP + 0 to +12hr. Final MCP to CTO + COO + Andrew. Total end-to-end: ~36h sequenced with overlap allowed in data collection.
  </sequencing_summary>
</task_order>
