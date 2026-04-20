<task_order>
  <metadata>
    <id>ADVI_STAUDT.A</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-20</date>
    <status>pending</status><!-- CTO conditional-approved 20260420T~12:49Z; comp-build rework + minor polish landed; COO dispatched GO to ~A inbox 20260420T~12:55Z. ~A is upstream-most, no upstream gate, may begin immediately on registration. -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~A — Layer: SILVER + Group A (upstream-most)</lane>
    <model>LAYER × 4-checkpoint MATRIX. Lane owns one layer; lane walks through all 4 checkpoints to capture evolution. Andrew 2026-04-20 reinforced: "layer scoped AND time scoped — at each of those times, watch how the layer evolved, cross-reference, comprehensive."</model>
    <priority>P0 — upstream-most. Findings-file gates ~B's findings write per §4.5 sequencing.</priority>
    <checkpoints>T0=544877cc (Wed 2026-04-15 ~20:40 ET) | T1=f177240b (Thu 2026-04-16 ~22:30 ET) | T2=ae759bbb (Fri 2026-04-17 ~07:00 ET) | T3=cd177553 (Mon 2026-04-20 current)</checkpoints>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§3.0 (Two failure classes — lead-with), §3.1 (checkpoints), §4.0 (investigative discipline), §4.1 (lane ~A), §4.5 (sequencing), §5 (guardrails), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCPs 20260420T~12:14Z (§3.0) + 20260420T121431Z (§3.4) + 20260420T~12:30Z (§4 LAYER-scoped restructure)</ref>
    <ref type="andrew-clarification">2026-04-20: layer-scoped AND time-scoped, not either/or; each lane watches how its layer evolved across all 4 timepoints to cross-reference comprehensively.</ref>
  </references>

  <objective>
    Audit the SILVER + Group A layer across all 4 checkpoints (T0/T1/T2/T3) and produce a definitive layer-findings file: either clean-bill ("this layer introduced no material change in window affecting downstream portal figures") OR enumerated material changes with downstream blast. ~A is upstream-most; your findings unlock ~B's findings-file write. Per Andrew: walk upstream-first so each downstream lane gets a stable baseline. Read-only audit only.
  </objective>

  <scope>
    <!-- VERBATIM from ADVI_STAUDT.md §3.0 (Two primary failure classes) per CTO MCP 20260420T~12:14Z. Lead-with framing — do not paraphrase. -->

    ### 3.0 Two primary failure classes (Andrew 2026-04-20 — lead every lane TO scope with this)

    Every lane TO must open its scope with these two classes named explicitly. These are THE primary audit subjects.

    **Class 1 — NNA definition change** (grain AND path)
    - **Grain sub-class:** D_02 `_nna_since` flipped per-advisor cumulative → per-(date, advisor, role) daily-grain at CN-P2 (commits `b3f6b1ee` + `ebd737e3` Thu 2026-04-16 12:31–12:35 ET).
    - **Path sub-class:** Canonical prefix split — `CANONICAL_NNA_PREFIX` (`gold/canonical/nna/`, 14 cols, has `aua_current`/`growth`/`client_state`) vs `CANONICAL_NNA_ATOMIC_PREFIX` (`gold/canonical/nna_atomic/`, 22 cols, missing those). W4 CN-P2..P5 → atomic; `cd177553` reverted D_04+D_00b+D_01+C_08 to `nna/`. Live schism §2.3.

    **Class 2 — Group D mapping ambiguity** (tagged_aua source + role-split + fee-split)
    - **tagged_aua source:** D_00c via `row.total_aua` fallback (`D_00c:528`) + `_weighted_aua` (`D_00c:881`); D_02 `summary.tagged_aua` in `build_advisor_books`; D_04 override (`D_04:2325-2340`, `fe999416`/`6391b96c`).
    - **Role-split:** `D_00c._weighted_aua` L881 + DE allChecked early return removal (`9f6faf9`) + C_08 RA-P5 (`d9ab1719`).
    - **Fee-split:** `D_00c:565` silent clip + D_04 top-level `fee_breakdown.no_fee.aua` NOT swept by B1.fix `5114984b`.

    **MANDATORY INVARIANT per checkpoint per advisor (Group D primarily; ~A surfaces if upstream fields make this checkable at silver/A level — not expected, but document if observable):**
    - `sum(role_breakdown[*].aua) == tagged_aua`
    - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`

    <!-- ~A is upstream-most. Class 1 path producer (C_01) is owned by ~C, not here; but if a silver schema change FEEDS the C_01 schema split, ~A's findings must surface that propagation hint. ~A's primary deliverable is silver/A clean-bill or N-findings. -->

    <!-- VERBATIM from ADVI_STAUDT.md §4.1 (Lane ~A — SILVER + Group A) per CTO PRD restructure. -->

    ### 4.1 Lane ~A — SILVER + Group A (upstream-most)

    **Layer scope:** silver/* (ingestion + dimensional prep) + A-group (A_00, A_01, A_02, A_03, A_04). These are the most-upstream producers. Everything downstream reads their output. Any material change here cascades through B→C→D.

    **Known silver + A-group commits in window** (lane verifies + may discover more):
    - Silver: `80917a1e` (Fri 05:59 ET AE — add cusip column to silver/transactions via bd_assets_dim bridge, CP-AE1), `6c80c5ed` (Fri 14:50 ET AE — Schwab ULN → silver/ULN/ ingestion), `c270a9b2` (Fri 12:56 ET AE — silver/unrealized_gain_loss rolling-key refresh, REVERTED same day), `32fbb0d6` (Fri 13:23 ET Andrew — revert of rolling-key refresh), `33de8d08` (Thu 19:03 ET AE — sync code/silver/ so inject_scoped_overrides.py resolves in S_00)
    - Silver upstream write-back path: `2a69b97e` (Fri 12:56 ET — key silver/unrealized to snapshot date, retire stale rolling parquet)
    - A-group: lane runs `git log --all --since='2026-04-15' --until='2026-04-20' -- data/black_diamond/scripts/gold/A_*.py data/black_diamond/scripts/silver/*.py code/silver/*` to enumerate

    **Per-checkpoint audit** (lane runs this 4×, once per checkpoint):
    For each of T0=`544877cc` / T1=`f177240b` / T2=`ae759bbb` / T3=`cd177553`:
    - Checkout the anchor SHA into `/tmp/staudt_layerA_Tx/` via `git worktree add`
    - `comp-pipescript io` on every silver orchestrator + A-script that exists at that SHA
    - Pull dated S3 partitions: `silver/unrealized_gain_loss/`, `silver/transactions/`, `silver/allocations/`, `silver/ULN/` (T3 only), `gold/dimensions/client_dimension.parquet` (A_04), `gold/dimensions/advisor_assignments_history.parquet` (A_01), `gold/dimensions/fee_rate_history.parquet` (A_02)
    - Row counts + column set + schema hash per partition per checkpoint

    **Rule-out check (mandatory conclusion):**
    - Do silver partition schemas differ across T0/T1/T2/T3? Yes → which fields added/removed/reshaped?
    - Do A-dimension row counts drift materially?
    - Does `silver/unrealized_gain_loss` keying behavior (rolling vs dated) differ at T2 vs T0?
    - Does `silver/transactions.cusip` presence cohort change between T2 and T3?

    **Investigative discipline (§4.0 verbatim):** "the lane split is by LAYER, not by time" — but each lane owns the cross-product of layer × 4 checkpoints. Andrew clarification 2026-04-20: "layer scoped AND time scoped — at each of those times, watch how those layers have evolved, in an effort to cross-reference and be comprehensive." Walk upstream-first: silver+A first, then B, then C, then D+synthesis. If you find no material change, say so explicitly with evidence — neither "this layer is fine" nor "the bug is here" is accepted without layer-specific evidence.
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="parallel data collection (no findings-file dependency)">
      <step>
        <run>git worktree add /tmp/staudt_layerA_T0 544877cc &amp;&amp; git worktree add /tmp/staudt_layerA_T1 f177240b &amp;&amp; git worktree add /tmp/staudt_layerA_T2 ae759bbb &amp;&amp; git worktree add /tmp/staudt_layerA_T3 cd177553</run>
        <expect>Four scratch worktrees. Repo root remains on CLOUD tip. Per PRD §5 #4 + #3: lane writes ONLY under STAUDT/layer_A/.</expect>
        <if_mismatch>Force-remove + retry; if still failing, MCP COO.</if_mismatch>
      </step>
      <step>
        <run>For each Tx in {T0, T1, T2, T3}: cd /tmp/staudt_layerA_Tx &amp;&amp; comp-build</run>
        <expect>1,162 ± 50 nodes / 940 ± 50 edges built per checkpoint. Node/edge count variance between checkpoints is itself a finding — document drift in `silver_and_group_a_inventory.md`.</expect>
        <if_mismatch>If comp-build fails inside a worktree, investigate before falling back. Do NOT skip — skipping reads wrong-checkpoint state from the repo-root graph (CLOUD tip = T3) and invalidates the entire layer × 4-checkpoint matrix. Per CTO MCP 20260420T~12:49Z (shape-review rework).</if_mismatch>
      </step>
      <step>
        <run>git log --all --since='2026-04-15' --until='2026-04-20' -- data/black_diamond/scripts/gold/A_*.py data/black_diamond/scripts/silver/*.py code/silver/* > /tmp/staudt_layerA_commits.txt</run>
        <expect>Full enumeration of A-group + silver commits in window. Combine with the known silver commits in §4.1 to seed inventory. Quiet scripts (no commits) flagged "no material change in window".</expect>
        <if_mismatch>If grep returns empty, double-check date range and script-path globs. STOP if results look incomplete.</if_mismatch>
      </step>
      <step>
        <run>For each Tx in {T0, T1, T2, T3}: cd /tmp/staudt_layerA_Tx &amp;&amp; comp-pipescript io for every A-script + silver orchestrator that exists at that SHA</run>
        <expect>READS + WRITES + COLUMN GAPS per script per checkpoint. Anchors layer-A inventory.</expect>
        <if_mismatch>Document every COLUMN GAPS finding — do not fix. Audit only.</if_mismatch>
      </step>
      <step>
        <run>For each Tx: pull dated S3 partitions per §4.1 list. Compute row count + column set + schema hash per partition per Tx.</run>
        <expect>4-checkpoint matrix populated. silver/ULN/ ABSENT pre-T3 (lands `6c80c5ed` Fri 14:50 ET — verify via S3 first-version timestamp). silver/transactions.cusip ABSENT pre-T2 (lands `80917a1e` Fri 05:59 ET).</expect>
        <if_mismatch>If observed partition presence contradicts expected (e.g., silver/ULN/ exists at T2), document — that's a finding.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="findings-file write (no upstream dependency — ~A is upstream-most)">
      <step>
        <run>For each Tx: comp-blast on every script that writes into silver/ or gold/dimensions/ (A_00..A_04 + S_00 if it exists)</run>
        <expect>Downstream propagation map per checkpoint. What B/C/D scripts depend on each silver/A artifact?</expect>
        <if_mismatch>n/a — orientation only.</if_mismatch>
      </step>
      <step>
        <run>Synthesize findings: did silver schemas change? Did A-dimension behavior change? Did keying behavior change (rolling vs dated unrealized)? Did cusip cohort drift between T2 and T3?</run>
        <expect>One of two conclusions per §4.0 rule-out discipline: (a) "this layer introduced **no** material change in window affecting portal figures" (clean-bill), OR (b) "this layer introduced the following N material changes with downstream blast radius: ..." with per-claim evidence.</expect>
        <if_mismatch>If unable to conclude (insufficient evidence), document the gap and MCP COO before writing findings.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post-findings-write — propagation handoff">
      <step>
        <run>MCP CTO + COO + ~B + ~C + ~D with one-paragraph summary + link to layer_a_findings.md + link to evidence_pack.json</run>
        <expect>~B cannot write its findings file before seeing this MCP. ~B may do data collection in parallel BEFORE the MCP, but findings-file write gates here.</expect>
        <if_mismatch>If MCP send fails, escalate via direct file write to inboxes.</if_mismatch>
      </step>
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run (per checkpoint × per script)</run>
        <expect>Auto-append fires if `.comp-graph/.agent_context` is set to `SERIAL=0.4.0_DS_ClientPlatform~A` and `TO_ID=ADVI_STAUDT.A`.</expect>
        <if_mismatch>Manually append per the log format.</if_mismatch>
      </step>
      <step>
        <run>git worktree remove /tmp/staudt_layerA_T0 &amp;&amp; git worktree remove /tmp/staudt_layerA_T1 &amp;&amp; git worktree remove /tmp/staudt_layerA_T2 &amp;&amp; git worktree remove /tmp/staudt_layerA_T3</run>
        <expect>Scratch worktrees cleaned up.</expect>
        <if_mismatch>Force-remove.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    All under `data/black_diamond/diagnostics/STAUDT/layer_A/`:

    1. **`silver_and_group_a_inventory.md`** — touched-script list + 4-checkpoint commit diff per script. Each silver/A script gets its own line (no collapse). Quiet scripts explicitly noted "no material change in window" with grep evidence.

    2. **`layer_a_findings.md`** — definitive answer: "this layer introduced {no | N} material changes affecting downstream portal figures" + evidence per claim. Conclusion section MUST cite the rule-out discipline §4.0 ("either clean-bill OR N-findings; neither claim accepted without layer-specific evidence").

    3. **`silver_schema_diff.json`** — machine-readable schema delta per partition per checkpoint. Schema = ordered column list + dtypes + row count + schema hash.

    4. **`evidence_pack.json`** — hashes + row counts + column sets per partition per checkpoint. Used by ~B/~C/~D for upstream-rule-out reference.

    5. **MCP handoff** to CTO + COO + ~B + ~C + ~D at findings-file commit time.

    6. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_layer_a_silver_and_group_a.md` (or appropriate date) citing all deliverables + Compiler Tools section reproducing every `<run>` from `<compiler_tools_mandate>` with observed output and explicit pass/fail vs. `<expect>`.

    7. **`org/compiler-tools-log.md`** appended with one row per comp-* tool call.
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6 + §4.5 sequencing:
    - **~A is upstream-most.** No upstream dependency — Phase 0 + Phase 1 run as soon as COO GO lands.
    - **~A's findings-file write fires the gate to ~B.** ~B may do parallel data collection before this gate but cannot write `layer_b_findings.md` until ~A's MCP lands.
    - **Lane collision avoidance:** ~A writes ONLY under `STAUDT/layer_A/`. Never touch layer_B/C/D/SYNTHESIS/.
    - **No upstream lane rewrites after downstream consumes** (PRD §5 #8): once `layer_a_findings.md` is committed and MCP'd, ~B reads it as stable. If ~A needs to append (e.g., ~B/~C surfaces a suspect upstream cause), ~A APPENDS — does not rewrite existing claims.
    - **Cross-lane MCP protocol** (PRD §4.5): every layer-findings MCP carries (a) clean-bill-or-N-findings one-liner, (b) link to findings file, (c) link to evidence pack. Downstream RAVC ACK before proceeding with findings writing.
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7:

    1. `silver_and_group_a_inventory.md` committed under `STAUDT/layer_A/` — touched-script list + 4-checkpoint commit diff per script.
    2. `layer_a_findings.md` committed — definitive clean-bill OR N-findings conclusion per §4.0; every finding has commit SHA + file:line + downstream blast cited.
    3. `silver_schema_diff.json` committed — machine-readable schema delta per partition per checkpoint.
    4. `evidence_pack.json` committed — hashes + row counts + column sets.
    5. **MCP handoff sent** to CTO + COO + ~B + ~C + ~D at commit time. ~B's findings-file write gate releases on this MCP.
    6. Session log includes Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK.
    7. `org/compiler-tools-log.md` appended with one row per comp-* run per checkpoint per script.
    8. Evidence-file-trace holds: every claim traceable to commit SHA + line range OR pulled artifact hash.
    9. No scope creep — fifth-bug candidate or out-of-§3.2/§3.3/§4.1 finding triggers MCP CTO+COO, not silent inclusion.
    10. Rule-out discipline (PRD §4.0): conclusion cannot be "this layer is fine" without evidence; cannot be "the bug is here" without evidence. Both require layer-specific grounding.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5:

    1. **READ-ONLY.** No commits to `data/black_diamond/scripts/gold/`. No S3 writes. No gold-runner triggers. No `comp-validate` config edits.
    2. **Evidence-file-trace mandatory.** Every claim cites file path + line range OR commit SHA + line range OR pulled artifact hash.
    3. **Lane collision avoidance — LAYER-SCOPED.** ~A writes ONLY under `STAUDT/layer_A/`. No lane touches another's directory.
    4. **Scratch worktree per checkpoint.** `/tmp/staudt_layerA_T0`, `/tmp/staudt_layerA_T1`, `/tmp/staudt_layerA_T2`, `/tmp/staudt_layerA_T3`. Never `git checkout` at repo root.
    5. **S3 point-in-time retrieval.** silver/ULN/ ABSENT pre-T3 (Schwab ULN ingest lands `6c80c5ed` Fri 14:50 ET). silver/transactions.cusip ABSENT pre-T2 (lands `80917a1e` Fri 05:59 ET). Document absences; do not fabricate.
    6. **Commit scope discipline.** `--only` with explicit path list, author = `0.4.0_DS_ClientPlatform~A`.
    7. **No upstream lane rewrites after downstream consumes.** Append-only after first MCP fires gate.
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

  <sequencing_summary>
    Per PRD §4.5 — ~A is Phase 1: T+0 to T+6hr. ~A findings MCP fires gate to ~B (then ~B → ~C → ~D in cascading 8h/10h/12h windows). Total end-to-end: ~36h sequenced (data-collection overlap allowed; the gate is on findings-file write).
  </sequencing_summary>
</task_order>
