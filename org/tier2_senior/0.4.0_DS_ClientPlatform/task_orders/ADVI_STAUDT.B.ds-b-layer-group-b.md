<task_order>
  <metadata>
    <id>ADVI_STAUDT.B</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-20</date>
    <status>complete</status><!-- Completed 2026-04-20 ~13:20Z by 0.4.0_DS_ClientPlatform~B. All 5 deliverables shipped under STAUDT/layer_B/: group_b_inventory.md, layer_b_findings.md (7 material findings B-1..B-7), b01_evolution_trace.md (8 sub-behaviors × 4 checkpoints), b01_cusip_coverage_probe.md (98.30% at T3 measured), evidence_pack.json. MCP handoff to CTO+COO+~C+~D on commit. -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~B — Layer: Group B (holdings / canonical prices / transactions)</lane>
    <model>LAYER × 4-checkpoint MATRIX. Lane owns one layer; lane walks through all 4 checkpoints to capture evolution. Andrew 2026-04-20 reinforced: "layer scoped AND time scoped — at each of those times, watch how the layer evolved, cross-reference, comprehensive."</model>
    <priority>P0 — second-from-upstream. Findings-file write GATES on ~A findings MCP per §4.5 sequencing. Findings-file write fires gate to ~C.</priority>
    <checkpoints>T0=544877cc | T1=f177240b | T2=ae759bbb | T3=cd177553</checkpoints>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§3.0 (Two failure classes — lead-with), §3.4 (Group B subsection — secondary grounding), §4.0 (investigative discipline), §4.2 (lane ~B), §4.5 (sequencing), §5 (guardrails), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCPs 20260420T~12:14Z (§3.0) + 20260420T121431Z (§3.4) + 20260420T~12:30Z (§4 LAYER-scoped restructure)</ref>
    <ref type="andrew-clarification">2026-04-20: layer-scoped AND time-scoped, not either/or.</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="ADVI_STAUDT.A" status="staged" required="layer_a_findings.md committed + MCP fired"/>
  </dependencies>

  <objective>
    Audit the Group B layer (B_00, B_01, B_01b, B_02, B_03 — holdings, canonical prices, transactions) across all 4 checkpoints (T0/T1/T2/T3) and produce a definitive layer-findings file. ~B reads silver + A-group output (~A's domain); your findings reference ~A's clean-bill or N-findings before concluding. Findings-file write gates ~C's findings write. Read-only audit only.
  </objective>

  <scope>
    <!-- VERBATIM from ADVI_STAUDT.md §3.0 (Two primary failure classes) per CTO MCP 20260420T~12:14Z. Lead-with framing — do not paraphrase. -->

    ### 3.0 Two primary failure classes (Andrew 2026-04-20 — lead every lane TO scope with this)

    **Class 1 — NNA definition change** (grain AND path) — see §3.0 in ~A TO for full text. ~B's relevance: B_01 evolution may produce columns that change downstream NNA computation; B/C boundary scripts (B_01 → C_01 / C_03) are propagation paths.

    **Class 2 — Group D mapping ambiguity** (tagged_aua source + role-split + fee-split) — see §3.0 in ~A TO for full text. ~B's relevance: B_01 produces holdings_lots which feeds C_03 ACCOUNT_PERFORMANCE which feeds D_00c/D_02/D_04; any B_01 row-count or MV-total drift propagates to tagged_aua at the D layer.

    **MANDATORY INVARIANT per checkpoint per advisor (Group D primarily):**
    - `sum(role_breakdown[*].aua) == tagged_aua`
    - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`
    ~B documents if any B-script change at a checkpoint introduces a propagation path that COULD violate the invariant downstream — but the actual invariant check happens at ~D's Group D level.

    <!-- VERBATIM from ADVI_STAUDT.md §4.2 (Lane ~B — Group B) per CTO PRD restructure. -->

    ### 4.2 Lane ~B — Group B (holdings / prices / transactions)

    **Layer scope:** B_00, B_01, B_01b, B_02, B_03. Reads silver + A-group output. Produces holdings_lots, canonical_prices, bd_assets_dim input, etc. — the raw material D-group reads (via C-group).

    **Commits in window** per §3.4 (B-group subsection — verbatim below). Lane verifies + may discover more.

    **§3.4 Group B subsection (verbatim — each script gets a line):**
    - `B_00.canonical_fills.py` — `22736cf7` (Thu 20:18 perf: parallel forward-fill). Audit: Parity of parallel vs sequential forward-fill output; any partition drift.
    - `B_01.holdings_lots.py` — HEAVY (21+ commits). See §3.4 table for full enumeration. Audit: bond-convention logic at each checkpoint · cap compression firm total · `market_value_uncapped` column presence · cusip coverage ratio · silver-authority gate cohort size · PIVOT evolution · snapshot_date derivation path · stale-RPS behavior · `df.attrs` serialization path · Gate 3 silent-close cohort size.
    - `B_01b` — search commits in window; if touched, audit any parity probe or shadow output.
    - `B_02 / B_03` — `856855f3` (Thu 19:59 DAG race condition B_02‖B_03 identified + corrected). Audit: was there a window where B_02/B_03 raced producing a race? Did the correction land in the runner?

    **Per-checkpoint audit** (same 4× pattern — walk through T0/T1/T2/T3):
    - Scratch worktree per checkpoint
    - `comp-pipescript io` on every B-script at the checkpoint SHA
    - Pull B_01 output: `holdings_lots/2026-04-15.parquet` (sample latest partition). Compare row count, firm MV sum, per-account MV distribution, cusip coverage, bond-vs-equity split, `market_value_uncapped` presence.

    **Special scope — B_01 evolution trace:**
    Per-checkpoint state for:
    - Bond-100x heuristic: present at which checkpoints? Applied to how many lots?
    - Confidence-tiered cap (T3 only): compression magnitude + `market_value_uncapped` column
    - Cusip coverage ratio: target 98.3% at T3; what was it at T0/T1/T2?
    - Snapshot_date derivation: path at each checkpoint
    - Silver-authority Gate 3 silent-close cohort size
    - Stale-RPS auto-skip on/off status
    - DataFrame.attrs serialization behavior
    - Synth-inject PIVOT state (PIVOT 5 gate, PIVOT 6 MV cap 1.10 vs 1.00)

    **Special scope — B_02/B_03 DAG race:**
    `856855f3` identified a race condition. Confirm correction landed and is active at T1/T2/T3.

    **Rule-out check (mandatory conclusion per §4.0):**
    - Did any B-script introduce a definitional change to columns D-group reads (via C-group)?
    - Did row count or MV totals drift by more than the expected cap-compression magnitude between checkpoints?

    **Upstream consistency (reference ~A findings):**
    Lane reads `layer_a_findings.md` MCP summary BEFORE concluding. If ~A found silver schema changes affecting B_01 inputs (e.g., silver/transactions.cusip add `80917a1e` at T2), ~B's findings must trace the propagation — does B_01's cusip enrichment behavior change at T2 because of the silver upstream change?

    **Investigative discipline (§4.0):** layer-scoped × 4 checkpoints. Andrew: cross-reference layer × time. Walk upstream-first. Clean-bill or N-findings; no claim accepted without evidence.

    **T0 pre-window-state note (CTO MCP 20260420T~12:49Z):** T0 anchor `544877cc` is "imperfect but accepted" per PRD §3.1. It already contains pre-window regressions including the W6-005 split-weighted change (`0804b377` 2026-04-13) and DE allChecked removal (`9f6faf9` 2026-04-13). These PREDATE the audit window. Report any such pre-existing state as "pre-window state at T0" rather than "introduced at T0."
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="parallel data collection (no findings-file gate)">
      <step>
        <run>git worktree add /tmp/staudt_layerB_T0 544877cc &amp;&amp; git worktree add /tmp/staudt_layerB_T1 f177240b &amp;&amp; git worktree add /tmp/staudt_layerB_T2 ae759bbb &amp;&amp; git worktree add /tmp/staudt_layerB_T3 cd177553</run>
        <expect>Four scratch worktrees per PRD §5 #4.</expect>
        <if_mismatch>Force-remove + retry; MCP COO if blocked.</if_mismatch>
      </step>
      <step>
        <run>For each Tx in {T0, T1, T2, T3}: cd /tmp/staudt_layerB_Tx &amp;&amp; comp-build</run>
        <expect>1,162 ± 50 nodes / 940 ± 50 edges built per checkpoint. Node/edge count variance between checkpoints is itself a finding — document drift in `group_b_inventory.md`.</expect>
        <if_mismatch>If comp-build fails inside a worktree, investigate before falling back. Do NOT skip — skipping reads wrong-checkpoint state from the repo-root graph (CLOUD tip = T3) and invalidates the entire layer × 4-checkpoint matrix. Per CTO MCP 20260420T~12:49Z (shape-review rework).</if_mismatch>
      </step>
      <step>
        <run>For each Tx in {T0, T1, T2, T3}: cd /tmp/staudt_layerB_Tx &amp;&amp; comp-pipescript io B_00 &amp;&amp; comp-pipescript io B_01 &amp;&amp; comp-pipescript io B_01b (if exists) &amp;&amp; comp-pipescript io B_02 &amp;&amp; comp-pipescript io B_03</run>
        <expect>READS + WRITES + COLUMN GAPS per script per checkpoint. Anchors layer-B inventory.</expect>
        <if_mismatch>Document every COLUMN GAPS finding — do not fix.</if_mismatch>
      </step>
      <step>
        <run>For each Tx: cd /tmp/staudt_layerB_Tx &amp;&amp; comp-blast B_01</run>
        <expect>Downstream propagation map for B_01 (heaviest downstream node). What C/D scripts depend on B_01 outputs at each checkpoint?</expect>
        <if_mismatch>n/a — orientation only.</if_mismatch>
      </step>
      <step>
        <run>For each Tx: pull holdings_lots/2026-04-15.parquet (or latest partition available at that point-in-time). Compute: row count, firm MV sum, per-account MV distribution (top-10), cusip non-null ratio, bond-vs-equity split (cost_per_unit&lt;=2 cohort size), market_value_uncapped column presence (T3 only).</run>
        <expect>4-checkpoint sample matrix populated. cusip coverage at T3 should approach 98.3% (CP-DS1 1db831aa fix). market_value_uncapped present only at T3 (cb6d78e2).</expect>
        <if_mismatch>If observed sample contradicts expected, that's a finding.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="findings-file write — GATES ON ~A findings MCP">
      <step>
        <run>WAIT for ~A's MCP fire — check inbox + read layer_a_findings.md summary; ACK ~A via RAVC step 2 before proceeding</run>
        <expect>~A's MCP arrives carrying clean-bill-or-N-findings one-liner + link to findings + link to evidence pack. ~B ACKs receipt before writing layer_b_findings.md.</expect>
        <if_mismatch>If ~A MCP not yet arrived after data collection completes, MCP ~A directly to confirm status; if blocked, MCP COO to escalate.</if_mismatch>
      </step>
      <step>
        <run>Synthesize B_01 evolution trace across the 8 sub-behaviors per checkpoint (bond-100x, tiered cap, cusip coverage, snapshot_date, silver-auth Gate 3, stale-RPS, df.attrs, PIVOT state)</run>
        <expect>Per-checkpoint state table for each sub-behavior. Each sub-behavior gets a column per checkpoint. Used by ~D for cross-layer propagation.</expect>
        <if_mismatch>If a sub-behavior cannot be sampled at a checkpoint (e.g., script crashes), document the absence — that's data.</if_mismatch>
      </step>
      <step>
        <run>Synthesize layer-B findings: did any B-script introduce a definitional change to columns D-group reads (via C)? Did row counts or MV totals drift unexpectedly? Reference ~A's findings — does the propagation chain hold?</run>
        <expect>One of two conclusions per §4.0: clean-bill OR N-findings with downstream blast.</expect>
        <if_mismatch>If unable to conclude, document gap + MCP COO + CTO before writing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post-findings-write — propagation handoff">
      <step>
        <run>MCP CTO + COO + ~C + ~D with one-paragraph summary + link to layer_b_findings.md + link to evidence_pack.json</run>
        <expect>~C's findings-file write gates here.</expect>
        <if_mismatch>Direct file-write to inboxes if MCP fails.</if_mismatch>
      </step>
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run (per checkpoint × per script)</run>
        <expect>Auto-append fires if context set correctly.</expect>
        <if_mismatch>Manual append.</if_mismatch>
      </step>
      <step>
        <run>git worktree remove /tmp/staudt_layerB_T0 &amp;&amp; git worktree remove /tmp/staudt_layerB_T1 &amp;&amp; git worktree remove /tmp/staudt_layerB_T2 &amp;&amp; git worktree remove /tmp/staudt_layerB_T3</run>
        <expect>Worktrees cleaned up.</expect>
        <if_mismatch>Force-remove.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    All under `data/black_diamond/diagnostics/STAUDT/layer_B/`:

    1. **`group_b_inventory.md`** — touched-script list + 4-checkpoint commit diff per script. Each B-script gets its own line — no collapse. Quiet scripts noted "no material change in window" with grep evidence.
    2. **`layer_b_findings.md`** — definitive answer (clean-bill OR N-findings) + evidence per claim + upstream-consistency reference to ~A findings.
    3. **`b01_evolution_trace.md`** — per-checkpoint state of the 8 B_01 sub-behaviors enumerated above. Each sub-behavior × 4 checkpoint matrix populated.
    4. **`b01_cusip_coverage_probe.md`** — per-checkpoint cusip coverage ratio (per-lot AND per-row if they differ) compared to session-32 98.3% benchmark. Cohort breakdown by account-type if possible. **Note (CTO MCP 20260420T~12:49Z):** silver/transactions.cusip column doesn't land until `80917a1e` (Fri 05:59 ET, T2); B_01 runtime cusip enrichment via bd_assets_dim (`f5f19e77`) is also T2+. Expected cusip coverage at T0/T1 is legitimately low or N/A — document as expected, not as finding. Probe baselines start meaningfully at T2.
    5. **`evidence_pack.json`** — hashes + row counts + column sets + per-checkpoint sample figures.
    6. **MCP handoff** to CTO + COO + ~C + ~D at findings-file commit.
    7. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_layer_b_group_b.md` (or appropriate date) with Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`.
    8. **`org/compiler-tools-log.md`** appended.
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6 + §4.5:
    - **Upstream gate:** ~B's findings-file write gates on ~A findings MCP. Phase 0 data collection runs in parallel; Phase 1 findings synthesis blocks on ~A.
    - **Downstream gate:** ~B's findings-file write fires the gate to ~C.
    - **Lane collision avoidance:** ~B writes ONLY under `STAUDT/layer_B/`. Never touch layer_A/C/D/SYNTHESIS/.
    - **Append-only after MCP:** once `layer_b_findings.md` is committed and MCP'd, ~C reads as stable. If ~C/~D surfaces a suspect upstream cause in B, ~B APPENDS — does not rewrite.
    - **RAVC:** ACK ~A's MCP before writing findings. If suspect upstream (silver/A) cause, MCP ~A for validation rather than re-investigation.
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7:

    1. `group_b_inventory.md` committed under `STAUDT/layer_B/` — script-line discipline (no collapse).
    2. `layer_b_findings.md` committed — clean-bill OR N-findings per §4.0; every finding has commit SHA + file:line + downstream blast cited; references ~A findings file for upstream rule-out.
    3. `b01_evolution_trace.md` committed — 8 sub-behaviors × 4 checkpoint matrix populated. Missing sub-behavior column = REWORK.
    4. `b01_cusip_coverage_probe.md` committed — coverage % per checkpoint with per-lot/per-row distinction. Missing = REWORK.
    5. `evidence_pack.json` committed.
    6. **MCP handoff sent** to CTO + COO + ~C + ~D at commit time. ~C's findings-file write gate releases on this MCP.
    7. Session log includes Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK.
    8. `org/compiler-tools-log.md` appended.
    9. Evidence-file-trace holds.
    10. Rule-out discipline (§4.0): conclusion grounded in layer-specific evidence; upstream-consistency reference to ~A documented.
    11. No scope creep — fifth-bug candidate or out-of-§3.4-Group-B finding triggers MCP CTO+COO.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5:

    1. **READ-ONLY.** No code writes, no S3 writes, no gold-runner triggers, no comp-validate config edits.
    2. **Evidence-file-trace mandatory.**
    3. **Lane collision avoidance — LAYER-SCOPED.** ~B writes ONLY under `STAUDT/layer_B/`.
    4. **Scratch worktree per checkpoint** — `/tmp/staudt_layerB_T0..T3`.
    5. **S3 point-in-time retrieval.** Document any missing version.
    6. **Commit scope discipline.** `--only`, author = `0.4.0_DS_ClientPlatform~B`.
    7. **No upstream lane rewrites after downstream consumes.** Append-only.
  </guardrails>

  <deadline>
    8 hours after ~A findings MCP lands (per PRD §4.5). Parallel data collection in Phase 0 may begin immediately on COO GO; Phase 1 findings write gates on ~A.
  </deadline>

  <agent_context_setup>
    Before first comp-* run:
    ```bash
    mkdir -p .comp-graph && printf "SERIAL=0.4.0_DS_ClientPlatform~B\nTO_ID=ADVI_STAUDT.B\n" > .comp-graph/.agent_context
    ```
  </agent_context_setup>

  <sequencing_summary>
    Per PRD §4.5 — ~B is Phase 2: ~A MCP + 0 to +8hr. ~B findings MCP fires gate to ~C.
  </sequencing_summary>
</task_order>
