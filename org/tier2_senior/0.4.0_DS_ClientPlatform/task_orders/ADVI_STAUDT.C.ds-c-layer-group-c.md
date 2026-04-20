<task_order>
  <metadata>
    <id>ADVI_STAUDT.C</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-20</date>
    <status>staged</status><!-- CTO confirms shape before COO dispatches GO -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~C — Layer: Group C (canonical NNA / role_aua / fee_detail / account_performance / advisor_fee_efficiency)</lane>
    <model>LAYER × 4-checkpoint MATRIX. Lane owns one layer; lane walks through all 4 checkpoints to capture evolution. Andrew 2026-04-20: "layer scoped AND time scoped — at each of those times, watch how the layer evolved, cross-reference, comprehensive."</model>
    <priority>P0 — third-from-upstream. Findings-file write GATES on ~B findings MCP per §4.5. Findings-file write fires gate to ~D. **OWNS Class 1 NNA path producer C_01 — critical for ~D synthesis.**</priority>
    <checkpoints>T0=544877cc | T1=f177240b | T2=ae759bbb | T3=cd177553</checkpoints>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§3.0 (Two failure classes — lead-with), §3.4 (Group C subsection — secondary grounding), §4.0 (investigative discipline), §4.3 (lane ~C), §4.5 (sequencing), §5 (guardrails), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCPs 20260420T~12:14Z (§3.0) + 20260420T121431Z (§3.4) + 20260420T~12:30Z (§4 LAYER-scoped restructure)</ref>
    <ref type="andrew-clarification">2026-04-20: layer-scoped AND time-scoped, not either/or.</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="ADVI_STAUDT.A" status="staged" required="layer_a_findings.md committed (read for upstream rule-out)"/>
    <dependency agent="0.4.0_DS_ClientPlatform~B" task="ADVI_STAUDT.B" status="staged" required="layer_b_findings.md committed + MCP fired"/>
  </dependencies>

  <objective>
    Audit the Group C layer (C_00, C_01, C_01b, C_02, C_03, C_04, C_05, C_06, C_07, C_08 — canonical NNA, role_aua, fee_detail, account_performance, account_team, advisor_fee_efficiency, etc.) across all 4 checkpoints (T0/T1/T2/T3) and produce a definitive layer-findings file. ~C reads A + B output; **~C OWNS the Class 1 NNA path producer (C_01) and is the most critical upstream layer for ~D's synthesis.** Findings-file write gates ~D's findings + synthesis. Read-only audit only.
  </objective>

  <scope>
    <!-- VERBATIM from ADVI_STAUDT.md §3.0 (Two primary failure classes) per CTO MCP 20260420T~12:14Z. Lead-with framing — do not paraphrase. -->

    ### 3.0 Two primary failure classes (Andrew 2026-04-20 — lead every lane TO scope with this)

    **Class 1 — NNA definition change** (grain AND path) — see §3.0 in ~A TO. **~C OWNS C_01 — the path-sub-class producer.** CN-P1 `bf9651b8` Wed 13:14 ET introduced the `nna_atomic` shadow writer; CN-P1b `9e47830c` + `dc4980c3` Thu 09:48-10:02 ET backfilled 2,294 partitions / 9,245,944 rows. The schema diff between `nna/` and `nna_atomic/` is the upstream of the live D-group split that `cd177553` partially reverted. Your `c01_nna_schema_diff.md` is THE evidence document for this class.

    **Class 2 — Group D mapping ambiguity** (tagged_aua source + role-split + fee-split) — see §3.0 in ~A TO. ~C's relevance: C_03 (`85bb2daa` phantom outflow fix) and C_08 (`d9ab1719` RA-P5 role override + `9e537f9f` defensive backfill) are upstream propagators of role-split + fee-split bugs.

    **MANDATORY INVARIANT per checkpoint per advisor (Group D primarily; check at C-output level if observable, surface to ~D regardless):**
    - `sum(role_breakdown[*].aua) == tagged_aua`
    - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`

    <!-- VERBATIM from ADVI_STAUDT.md §4.3 (Lane ~C — Group C) per CTO PRD restructure. -->

    ### 4.3 Lane ~C — Group C (canonical + views + advisor_fee_efficiency)

    **Layer scope:** C_00, C_01, C_01b, C_02, C_03, C_04, C_05, C_06, C_07, C_08. Reads A + B output. Produces canonical/nna, canonical/nna_atomic, canonical/role_aua, canonical/advisor_fee_detail, account_performance, account_team, advisor_fee_efficiency, client_tax_liability, mix_daily_summary — the canonicals D-group reads.

    **Commits in window** per §3.4 (C-group subsection — verbatim below). Lane verifies + may discover more.

    **§3.4 Group C subsection (verbatim — each script gets a line):**
    - `C_00.canonical_performance.py` — `f177240b` (Thu 20:29 full Polars port — groupby+agg L222 + cumsum L263), `22736cf7` (Thu 20:18 batched cumsum), `4a6173db` (Thu 20:35 runner polars install). **Polars parity probe MANDATORY in ~C lane.** Diff polars-port output vs prior pandas baseline for 2026-04-15 partition. Row-level delta > $0.01 = finding.
    - `C_01.canonical_nna.py` — `bf9651b8` (Wed 13:14 CN-P1 nna_atomic shadow writer) · `9e47830c` (Thu 09:48 CN-P1b --backfill-nna-atomic-only) · `dc4980c3` (Thu 10:02 CN-P1b bulk historical emit 2,294 partitions / 9,245,944 rows). **NNA Class 1 path sub-class producer.** Audit: schema diff between `nna/` and `nna_atomic/` at each checkpoint · which partitions exist at T0/T1/T2/T3 · what columns (aua_current, growth, client_state, aua_residual, nna_clean) are present where. This is the upstream of the §3.0 Class 1 path split.
    - `C_01b` — search commits; if touched, audit.
    - `C_02 / C_04 / C_05 / C_06` — quieter scripts but must confirm they are quiet. Any commits = audit; else document "no material change in window".
    - `C_03.canonical_performance.py` — `85bb2daa` (Fri 09:42 phantom outflow pulse fix — recompute cum_inflows/cum_outflows on dense date grid post-merge cumsum). **Load-bearing for NNA.** `ACCOUNT_PERFORMANCE` is read by D_00c, D_02, D_04. Audit: cum_inflows/cum_outflows values at each checkpoint · advisor-level and firm-level daily NNA derived from C_03 output · does the phantom outflow pulse exist at T0/T1 but not T2/T3? · any downstream advisor whose NNA flipped sign between checkpoints.
    - `C_07.advisor_dimensions.py` — `f49aa9bd` (Wed 18:34 C07-T1 RCA — team_attribution bug is D_02 column-load, not C_07). Confirm C_07 output (`account_team.parquet`, `rel_architect_lookup.parquet`) is stable across checkpoints.
    - `C_08.advisor_fee_efficiency.py` — Group D-linked — already PRIMARY in §3.3. §3.4 adds: `f2ec98d1`/`d2dcae39`/`bb426933` (B9/B8b/B10 output), `3e497ab8` (canonical role order), `86e57e36` (WAR ROOM iterrows→to_dict), `49eac17d` (CN-P5 nna_atomic flip — REVERTED by cd177553), `d9ab1719` (RA-P5 role_breakdown canonical override), `9e537f9f` (Fri 15:56 defensive backfill aua_current/growth), `cd177553` (Fri 16:08 prefix revert to nna/).

    **Per-checkpoint audit** (same 4× pattern):
    - Scratch worktree + `comp-pipescript io` per script
    - Partition inventory:
      - `gold/canonical/nna/` — partition count per checkpoint
      - `gold/canonical/nna_atomic/` — partition count per checkpoint (does it exist at T0? CN-P1 `bf9651b8` Wed 13:14 ET — pre-T0 anchor 20:38 ET, so shadow writer present but backfill ABSENT until Thu)
      - `gold/canonical/role_aua/` — partition count per checkpoint
      - `gold/timeseries/account_performance.parquet` — C_03 output
      - `gold/artifacts/advisor_fee_efficiency.json` — C_08 output

    **Special scope — C_00 polars parity probe (MANDATORY, this lane):**
    Checkout `544877cc` (pre-polars) C_00 + `f177240b` (polars port) C_00 into two scratch worktrees. Run both against silver inputs for 2026-04-15 partition. Diff outputs (groupby+agg at L222, cumsum at L263). Any row-level delta > $0.01 is a finding.

    **Special scope — C_01 NNA schema diff (CRITICAL for Class 1 path):**
    Full column-level diff between `gold/canonical/nna/` and `gold/canonical/nna_atomic/` schemas per checkpoint. Enumerate every column in `nna/` not in `nna_atomic/` (known so far: `aua_current`, `growth`, `client_state`, `aua_residual`, `nna_clean`) and vice versa. Per (advisor, date, role) sample: do values agree where keys align?

    **Special scope — C_03 phantom outflow probe:**
    Per checkpoint, sample cum_inflows / cum_outflows for 3 advisors at 5 dates. Does the phantom outflow pulse exist at T0/T1 and not at T2/T3 (post `85bb2daa` Fri 09:42 ET)? Is cum_outflows monotonic non-decreasing at each checkpoint?

    **Rule-out check (mandatory conclusion per §4.0):**
    - Did any C-script introduce a definitional change to canonical fields D-group reads?
    - Is there a partition that does not exist at T0 but does at T3 (e.g., `nna_atomic/` before CN-P1b backfill)?

    **Upstream consistency (reference ~A + ~B findings):**
    If ~B flagged a B_01 output change, does it propagate through C_03 / C_08 to canonical outputs? If ~A flagged a silver schema change, does C_01 (which reads silver) absorb it?

    **Investigative discipline (§4.0):** layer × 4 checkpoints. Walk upstream-first. Andrew clarification: cross-reference layer × time comprehensively.
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="parallel data collection (no findings-file gate)">
      <step>
        <run>git worktree add /tmp/staudt_layerC_T0 544877cc &amp;&amp; git worktree add /tmp/staudt_layerC_T1 f177240b &amp;&amp; git worktree add /tmp/staudt_layerC_T2 ae759bbb &amp;&amp; git worktree add /tmp/staudt_layerC_T3 cd177553</run>
        <expect>Four scratch worktrees per PRD §5 #4.</expect>
        <if_mismatch>Force-remove + retry; MCP COO if blocked.</if_mismatch>
      </step>
      <step>
        <run>For each Tx in {T0, T1, T2, T3}: cd /tmp/staudt_layerC_Tx &amp;&amp; comp-pipescript io C_00 &amp;&amp; comp-pipescript io C_01 &amp;&amp; comp-pipescript io C_01b (if exists) &amp;&amp; comp-pipescript io C_02 &amp;&amp; comp-pipescript io C_03 &amp;&amp; comp-pipescript io C_04 &amp;&amp; comp-pipescript io C_05 &amp;&amp; comp-pipescript io C_06 &amp;&amp; comp-pipescript io C_07 &amp;&amp; comp-pipescript io C_08</run>
        <expect>READS + WRITES + COLUMN GAPS per script per checkpoint. Anchors layer-C inventory.</expect>
        <if_mismatch>Document COLUMN GAPS — do not fix.</if_mismatch>
      </step>
      <step>
        <run>For each Tx: cd /tmp/staudt_layerC_Tx &amp;&amp; comp-blast C_00 &amp;&amp; comp-blast C_01 &amp;&amp; comp-blast C_03 &amp;&amp; comp-blast C_08</run>
        <expect>Downstream propagation map per checkpoint.</expect>
        <if_mismatch>n/a — orientation only.</if_mismatch>
      </step>
      <step>
        <run>POLARS PARITY PROBE: cd /tmp/staudt_layerC_T0 &amp;&amp; python data/black_diamond/scripts/gold/C_00.canonical_performance.py --partition 2026-04-15 --out /tmp/staudt_C00_pandas.parquet ; cd /tmp/staudt_layerC_T1 &amp;&amp; python data/black_diamond/scripts/gold/C_00.canonical_performance.py --partition 2026-04-15 --out /tmp/staudt_C00_polars.parquet ; diff outputs at row level on shared keys; flag any delta > $0.01</run>
        <expect>Empty diff. Polars port `f177240b` should be byte-equivalent at row level. Any row-level delta > $0.01 = FINDING for ~D's bug_attribution.md.</expect>
        <if_mismatch>Document EVERY row with delta > $0.01: (advisor_id, account_id, snapshot_date, pandas_value, polars_value, delta_dollars).</if_mismatch>
      </step>
      <step>
        <run>NNA SCHEMA DIFF: For each Tx where both nna/ and nna_atomic/ partitions exist (T1+ probably; T0 may have nna_atomic/ shadow writer code present but backfill ABSENT), pull both 2026-04-15 partitions and diff column-set + dtypes + per-(advisor, date, role) value alignment</run>
        <expect>Per-checkpoint schema delta enumerated. nna/ has 14 cols (incl aua_current/growth/client_state/aua_residual/nna_clean); nna_atomic/ has 22 cols (no aua_current/growth, has 'state' not 'client_state'). Anchor for ~D's NNA-path-split synthesis.</expect>
        <if_mismatch>If atomic partitions ABSENT at a checkpoint, document — that's data not absence-of-data.</if_mismatch>
      </step>
      <step>
        <run>C_03 PHANTOM OUTFLOW PROBE: For each Tx, pull account_performance.parquet (or recompute from silver if not persisted at that point-in-time). Sample cum_inflows / cum_outflows for 3 advisors × 5 dates. Verify cum_outflows monotonic non-decreasing.</run>
        <expect>Phantom outflow pulse exists at T0/T1 (pre-`85bb2daa`) but NOT at T2/T3 (post-fix). cum_outflows should be monotonic non-decreasing at T2/T3.</expect>
        <if_mismatch>If phantom pulse absent at T0 OR present at T3, that's a finding.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="findings-file write — GATES ON ~B findings MCP">
      <step>
        <run>WAIT for ~B's MCP fire — check inbox + read layer_b_findings.md summary; ACK ~B via RAVC step 2 before proceeding</run>
        <expect>~B's MCP arrives carrying clean-bill-or-N-findings + links. ~C ACKs receipt before writing layer_c_findings.md.</expect>
        <if_mismatch>If ~B MCP not arrived after data collection, MCP ~B; escalate to COO if blocked.</if_mismatch>
      </step>
      <step>
        <run>Synthesize layer-C findings: did any C-script introduce a definitional change to canonical fields D-group reads? Did partition presence change between checkpoints? Polars parity findings? NNA schema diff findings? C_03 phantom outflow findings? Reference ~A + ~B findings for upstream propagation.</run>
        <expect>Clean-bill OR N-findings per §4.0 with downstream blast.</expect>
        <if_mismatch>If unable to conclude, document gap + MCP COO + CTO.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="post-findings-write — propagation handoff">
      <step>
        <run>MCP CTO + COO + ~D with one-paragraph summary + links to layer_c_findings.md + c00_polars_parity_probe.md + c01_nna_schema_diff.md + c03_phantom_outflow_probe.md + evidence_pack.json</run>
        <expect>~D's findings + synthesis writes gate here. ~D gets the most evidence packs to chew on; flag the C_01 NNA schema diff prominently — it's THE Class 1 path evidence.</expect>
        <if_mismatch>Direct file-write to inboxes if MCP fails.</if_mismatch>
      </step>
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run (per checkpoint × per script)</run>
        <expect>Auto-append fires if context set.</expect>
        <if_mismatch>Manual append.</if_mismatch>
      </step>
      <step>
        <run>git worktree remove /tmp/staudt_layerC_T0 &amp;&amp; git worktree remove /tmp/staudt_layerC_T1 &amp;&amp; git worktree remove /tmp/staudt_layerC_T2 &amp;&amp; git worktree remove /tmp/staudt_layerC_T3</run>
        <expect>Cleaned up.</expect>
        <if_mismatch>Force-remove.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    All under `data/black_diamond/diagnostics/STAUDT/layer_C/`:

    1. **`group_c_inventory.md`** — touched-script list + 4-checkpoint commit diff per script. Each C-script gets its own line. Quiet (C_02/C_04/C_05/C_06) explicitly noted "no material change in window" with grep evidence.
    2. **`layer_c_findings.md`** — definitive answer + evidence per claim + upstream-consistency reference to ~A + ~B findings.
    3. **`c00_polars_parity_probe.md`** — polars vs pandas C_00 parity probe per checkpoint. Either "no delta found" with hash equality OR delta table per (advisor_id, account_id, snapshot_date, pandas_value, polars_value, delta_dollars).
    4. **`c01_nna_schema_diff.md`** — full column-level diff between `gold/canonical/nna/` and `gold/canonical/nna_atomic/` schemas per checkpoint. Per (advisor, date, role) value-alignment sample. **THIS IS THE Class 1 path-sub-class evidence document — flag prominently in MCP handoff.**
    5. **`c03_phantom_outflow_probe.md`** — per-checkpoint cum_inflows/cum_outflows samples for 3 advisors × 5 dates. Monotonicity check.
    6. **`evidence_pack.json`** — hashes + row counts + column sets + partition presence matrix.
    7. **MCP handoff** to CTO + COO + ~D at findings-file commit.
    8. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_layer_c_group_c.md` with Compiler Tools section reproducing every `<run>` with observed output and pass/fail vs. `<expect>`.
    9. **`org/compiler-tools-log.md`** appended.
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6 + §4.5:
    - **Upstream gate:** ~C's findings-file write gates on ~B findings MCP. Phase 0 data collection runs in parallel; Phase 1 findings synthesis blocks on ~B.
    - **Downstream gate:** ~C's findings-file write fires the gate to ~D.
    - **Lane collision avoidance:** ~C writes ONLY under `STAUDT/layer_C/`. Never touch other lanes' dirs.
    - **Append-only after MCP.**
    - **RAVC:** ACK ~B's MCP before writing findings; MCP ~A or ~B for upstream validation if needed.
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7:

    1. `group_c_inventory.md` committed under `STAUDT/layer_C/` — script-line discipline.
    2. `layer_c_findings.md` committed — clean-bill OR N-findings; references ~A + ~B for upstream rule-out.
    3. `c00_polars_parity_probe.md` committed — delta table OR "no delta found" with hash. Missing = REWORK.
    4. `c01_nna_schema_diff.md` committed — per-checkpoint column-level diff. Missing = REWORK.
    5. `c03_phantom_outflow_probe.md` committed — per-checkpoint cum_inflows/cum_outflows samples + monotonicity check. Missing = REWORK.
    6. `evidence_pack.json` committed.
    7. **MCP handoff sent** to CTO + COO + ~D at commit. ~D's gate releases on this MCP.
    8. Session log includes Compiler Tools section reproducing every `<run>` with observed output and pass/fail vs. `<expect>`. Missing rows = REWORK.
    9. `org/compiler-tools-log.md` appended.
    10. Evidence-file-trace holds.
    11. Rule-out discipline (§4.0): grounded in C-layer evidence; references ~A + ~B for upstream rule-out.
    12. No scope creep — fifth-bug candidate or out-of-§3.4-Group-C finding triggers MCP CTO+COO.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5:

    1. **READ-ONLY.**
    2. **Evidence-file-trace mandatory.**
    3. **Lane collision avoidance — LAYER-SCOPED.** ~C writes ONLY under `STAUDT/layer_C/`.
    4. **Scratch worktree per checkpoint** — `/tmp/staudt_layerC_T0..T3`.
    5. **S3 point-in-time retrieval** — `gold/canonical/nna_atomic/` partitions ABSENT at T0 (CN-P1b backfill landed Thu); document.
    6. **Commit scope discipline** — `--only`, author = `0.4.0_DS_ClientPlatform~C`.
    7. **No upstream lane rewrites after downstream consumes.**
  </guardrails>

  <deadline>
    10 hours after ~B findings MCP (per PRD §4.5 — heavier scope: polars parity probe + NNA schema diff + phantom outflow probe).
  </deadline>

  <agent_context_setup>
    Before first comp-* run:
    ```bash
    mkdir -p .comp-graph && printf "SERIAL=0.4.0_DS_ClientPlatform~C\nTO_ID=ADVI_STAUDT.C\n" > .comp-graph/.agent_context
    ```
  </agent_context_setup>

  <sequencing_summary>
    Per PRD §4.5 — ~C is Phase 3: ~B MCP + 0 to +10hr. ~C findings MCP fires gate to ~D.
  </sequencing_summary>
</task_order>
