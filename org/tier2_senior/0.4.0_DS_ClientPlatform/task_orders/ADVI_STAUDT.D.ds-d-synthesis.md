<task_order>
  <metadata>
    <id>ADVI_STAUDT.D</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-20</date>
    <status>staged</status><!-- CTO confirms shape before COO dispatches GO; ~D blocks on ~A/~B/~C evidence packs -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~D — synthesis + 4-checkpoint delta + bug attribution + COO handoff</lane>
    <priority>P0 — ~D is the deliverable COO uses to author all fix-TOs</priority>
    <git_anchor>cd177553 (CLOUD tip — T3)</git_anchor>
    <wall_clock>Mon 2026-04-20 current</wall_clock>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§4.4 (lane scope), §3.2 (fields in scope), §3.3 (Group D PRIMARY focus + master synthesis), §5 (guardrails), §6 (cross-domain), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCP 20260420T120334Z — §3.3 amendment locking Group D tagged_aua / role-split / fee-split as PRIMARY scope</ref>
    <ref type="upstream">CTO MCP 20260417T213111Z — 4-bug audit ratification (you incorporate this attribution directly)</ref>
    <ref type="cto-handoff">CTO MCP 20260420T~12:00Z — STAUDT PRD handoff</ref>
  </references>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform~A" task="ADVI_STAUDT.A" status="staged" required="evidence-pack-committed"/>
    <dependency agent="0.4.0_DS_ClientPlatform~B" task="ADVI_STAUDT.B" status="staged" required="evidence-pack-committed"/>
    <dependency agent="0.4.0_DS_ClientPlatform~C" task="ADVI_STAUDT.C" status="staged" required="evidence-pack-committed"/>
  </dependencies>

  <objective>
    Synthesize ~A/~B/~C evidence packs into the canonical 4-checkpoint delta table + bug attribution + COO hand-off briefing for fix-TO authoring. Pull T3 (current `cd177553`) state directly. Produce three SYNTHESIS/* files that COO uses to author every Group D fix-TO. Read-only audit only.

    **~D synthesis is the project's primary deliverable.** Without it, fix-TO authoring stalls. Quality bar: every recommendation in `coo_handoff.md` must cite a specific row of `group_d_tagged_aua_decomposition.md` AND a specific commit SHA + line range from one of the four checkpoints' evidence packs.
  </objective>

  <scope>
    <!-- VERBATIM from ADVI_STAUDT.md §3.0 (Two primary failure classes) per CTO MCP 20260420T~12:14Z. Lead-with framing — do not paraphrase, do not relabel. -->

    ### 3.0 Two primary failure classes (Andrew 2026-04-20 — lead every lane TO scope with this)

    Every lane TO must open its scope with these two classes named explicitly. These are THE primary audit subjects; everything else in §3.2/§3.3 is secondary evidence grounding.

    **Class 1 — NNA definition change** (grain AND path)
    - **Grain sub-class:** D_02 `_nna_since` flipped per-advisor cumulative → per-(date, advisor, role) daily-grain at CN-P2 (commits `b3f6b1ee` + `ebd737e3` Thu 2026-04-16 12:31–12:35 ET). Previously a single cumulative NNA value per advisor; now a daily-rolled sum decomposed across roles. COO audit bug #1 — currently hidden in the modal via `SHOW_NNA=false` (`AdvisorBookAccountModal.tsx:38`).
    - **Path sub-class:** Canonical prefix split — `CANONICAL_NNA_PREFIX` (`gold/canonical/nna/`, 14 cols, has `aua_current`/`growth`/`client_state`) vs `CANONICAL_NNA_ATOMIC_PREFIX` (`gold/canonical/nna_atomic/`, 22 cols, missing those). W4 CN-P2..P5 put all D-group consumers on atomic (Thu); session-32 `cd177553` (Fri 16:08 ET) reverted D_04+D_00b+D_01+C_08 to `nna/` but left D_00c+D_02 on `nna_atomic/`. Live schism. §2.3.

    **Class 2 — Group D mapping ambiguity** (tagged_aua source + role-split + fee-split)
    - **tagged_aua source sub-class:** Where does the canonical `tagged_aua` live? D_00c computes its own via `row.total_aua` fallback (`D_00c:528`) with a `_weighted_aua` split-weighted degradation (`D_00c:881`). D_02 produces `summary.tagged_aua` in `build_advisor_books`. D_04 overrides with its own block (`D_04:2325-2340`, commits `fe999416`/`6391b96c`, 2026-04-09). None of them reads from a shared module — D_00c does not read from D_02 (COO-verified: 9 reads, 0 from D_02). COO audit bugs #2 and #3.
    - **Role-split attribution sub-class:** How is a multi-role client's AUA distributed across roles? `D_00c._weighted_aua` (L881) applies a split-weight; DE removal of allChecked early return (`9f6faf9`) forced the leaderboard through the split-weighted sum, producing Travis $82M (split) vs $434M (non-split). C_08 role_breakdown canonical override (RA-P5 `d9ab1719`) adds a second role-split site.
    - **Fee-split attribution sub-class:** Fee-paying vs no-fee bucket boundaries. `D_00c:565` silent clip `no_fee_aua = max(0, tagged_aua - fee_aua)` zeros the no-fee bucket when tagged_aua under-computes (Travis `max(0, 82 - 346) = 0`, drops off leaderboard). B1.fix (`5114984b`) swept `role_breakdown[role].no_fee.aua` but NOT top-level `fee_breakdown.no_fee.aua`. COO audit bug #4.

    **MANDATORY INVARIANT per checkpoint per advisor (must check, every checkpoint, every advisor) — ~D rolls these into `group_d_tagged_aua_decomposition.md` as a per-checkpoint sum-invariant column:**
    - `sum(role_breakdown[*].aua) == tagged_aua`
    - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`

    Any checkpoint where these fail is a mapping-ambiguity finding — cite advisor ID + checkpoint + delta magnitude in `bug_attribution.md`.

    <!-- End §3.0 lead-in. The §3.3 Group D PRIMARY FOCUS table follows as second-level evidence detail. -->

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

    **~D master synthesis deliverable per §3.3 (dedicated):**
    ~D produces `STAUDT/SYNTHESIS/group_d_tagged_aua_decomposition.md` — ONE master table, one row per (site × field), four checkpoint columns with formula text + 5-advisor sample values + divergence class. This is the deliverable COO uses to decide fix-TO scope. Every recommendation in `coo_handoff.md` for Group D fixes must cite a specific row of this table.

    <!-- Lane ~D specific scope (PRD §4.4) -->

    **T3 direct pull (CLOUD tip `cd177553` at scope start):**
    - All scripts as currently checked out — no worktree needed for T3 (use repo root)
    - S3 platinum/* current pulls for the 5 top advisors + firm-level
    - **Critical:** D_04 + D_00b + D_01 + C_08 currently read CANONICAL_NNA_PREFIX (reverted per `cd177553`). D_00c + D_02 still read CANONICAL_NNA_ATOMIC_PREFIX. The NNA-path split (PRD §2.3) is LIVE — must be a top-line item in `bug_attribution.md`.

    **Synthesis scope:**
    - Cross-checkpoint delta table for every field in §3.2 + §3.3 across (T0, T1, T2, T3)
    - Bug attribution: COO's 4 bugs + the NNA-path split (§2.3) + any parity-probe finding from ~B + any cusip-coverage / revert-integrity finding from ~C + any sum-invariant violation from §3.3 sub-table (d)
    - COO handoff briefing with restore-to-T0 vs keep-T1/T2/T3 vs hybrid-with-rewrite calls per field/bug, each with proposed fix-TO sketch (DS lane, scope, acceptance criteria)
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write — synthesis prep at T3 + read upstream packs">
      <step>
        <run>Verify ~A/~B/~C evidence packs all committed: ls data/black_diamond/diagnostics/STAUDT/T0_wednesday/ data/black_diamond/diagnostics/STAUDT/T1_thursday/ data/black_diamond/diagnostics/STAUDT/T2_friday_earlyam/</run>
        <expect>All three checkpoint dirs contain `state.md` + `{Tx}_evidence.json` + `group_d_tagged_aua_role_fee_decomposition.md`. ~B additionally has `polars_parity_C00.md` + `war_room_iterrows_parity.md`. ~C additionally has `cusip_coverage_probe.md` + `revert_integrity_check.md`.</expect>
        <if_mismatch>STOP. ~D blocks on upstream evidence. MCP missing lane(s) directly + COO. Do not start synthesis with partial input.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io D_04 &amp;&amp; comp-pipescript io D_00c &amp;&amp; comp-pipescript io D_02 &amp;&amp; comp-pipescript io C_08 (at repo root, T3)</run>
        <expect>D_04 reads CANONICAL_NNA_PREFIX (reverted). D_00c + D_02 read CANONICAL_NNA_ATOMIC_PREFIX (CN-P2/P3 terminal). C_08 reads CANONICAL_NNA_PREFIX (reverted) WITH `aua_current` / `growth` defensive backfill at L644.</expect>
        <if_mismatch>If reads do not match, the NNA-path-split status changed since CTO PRD pass — re-anchor §2.3 of bug_attribution.md.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_00c &amp;&amp; comp-blast D_04 &amp;&amp; comp-blast C_08 &amp;&amp; comp-blast D_00c._weighted_aua</run>
        <expect>T3 blast snapshot for delta vs T0/T1/T2.</expect>
        <if_mismatch>Function-level node MISSING per ADHC_ROUTER Phase 2 → MCP COO+CTO; do not skip.</if_mismatch>
      </step>
      <step>
        <run>comp-trace tagged_aua &amp;&amp; comp-platinum reverse tagged_aua &amp;&amp; comp-platinum reverse fee_breakdown.no_fee.aua &amp;&amp; comp-platinum reverse aua_growth_pct</run>
        <expect>Producer + consumer paths for the three Group D primary fields at T3.</expect>
        <if_mismatch>Document missing nodes.</if_mismatch>
      </step>
      <step>
        <run>comp-trace each definitional-change node end-to-end: comp-trace `aua_growth_pct` --direction both ; comp-trace `_weighted_aua` --direction both ; comp-trace `no_fee_aua` --direction both</run>
        <expect>Per PRD §4.4 mandate. Full upstream + downstream chain for each definitional change.</expect>
        <if_mismatch>Document missing/broken edges.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before committing synthesis pack — schema-check pass on consumers">
      <step>
        <run>comp-cache collisions</run>
        <expect>Per PRD §4.4 mandate. Confirm no FE-side React Query key collision regression introduced by any 2026-04-15..2026-04-20 commit.</expect>
        <if_mismatch>Surface any collision in bug_attribution.md as a separate FE-side finding.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check AdvisorsTab &amp;&amp; comp-transform schema-check ClientsTab &amp;&amp; comp-transform schema-check AdvisorIntelligence</run>
        <expect>Per PRD §4.4 mandate — three leaderboard consumers. MISSING / UNUSED / NOTE captured. PartnerAnalytics MISSING `period` at L454 is pre-existing (not your scope).</expect>
        <if_mismatch>Any new MISSING / UNUSED that maps to Group D fields (tagged_aua, fee_breakdown, aua_growth_pct, role_breakdown) is a FE-side rendering risk — surface in bug_attribution.md as a separate finding.</if_mismatch>
      </step>
      <step>
        <run>comp-build (if graph stale)</run>
        <expect>Fresh graph for synthesis hygiene.</expect>
        <if_mismatch>If build fails, MCP COO before publishing synthesis.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after committing synthesis pack">
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run above</run>
        <expect>One row per tool run with TO_ID=ADVI_STAUDT.D.</expect>
        <if_mismatch>Manually append.</if_mismatch>
      </step>
      <step>
        <run>MCP COO + CTO with handoff: subject "STAUDT SYNTHESIS COMPLETE — coo_handoff.md ready for fix-TO authoring"; body cites the three SYNTHESIS/* file paths + a one-paragraph executive summary + count of recommendations.</run>
        <expect>Both execs notified within 5 minutes of synthesis commit. Andrew receives review notice via CTO/COO chain.</expect>
        <if_mismatch>If MCP send fails, escalate via direct file write to both inboxes.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    All under `data/black_diamond/diagnostics/STAUDT/SYNTHESIS/`:

    1. **`delta_table.md` + `delta_table.json`** (PRD §4.4 Deliverable 1):
       Canonical 4-checkpoint delta table. ONE row per (script, field, advisor-or-firm). Columns: formula@T0 | formula@T1 | formula@T2 | formula@T3 | sample-value@T0 | T1 | T2 | T3 | delta-class (identity / cosmetic / numeric / definitional / structural). Populate every field in §3.2.

    2. **`group_d_tagged_aua_decomposition.md`** — PRIMARY synthesis deliverable per §3.3 (NON-NEGOTIABLE):
       ONE master table, one row per (Group D production site × field), four checkpoint columns with formula text + 5-advisor sample values + divergence class. Per-advisor sum-invariant check per checkpoint: `sum(role_breakdown[*].aua) == tagged_aua` for Travis + Kyle + Hunter + Alex + Tim. Cite specific advisor IDs where violations occur.

    3. **`bug_attribution.md`** (PRD §4.4 Deliverable 2):
       For each of:
       - COO's 4 bugs (per CTO MCP 20260417T213111Z ratification)
       - The NNA-path split (PRD §2.3 — D_04/D_00b/D_01/C_08 reverted to nna/, D_00c/D_02 still on nna_atomic/)
       - Any parity finding from ~B (`polars_parity_C00.md` + `war_room_iterrows_parity.md`)
       - Any cusip-coverage / revert-integrity finding from ~C (`cusip_coverage_probe.md` + `revert_integrity_check.md`)
       - Any sum-invariant violation from the per-advisor §3.3 (d) decomposition above
       - Any FE-side schema-check / cache-collision finding from Phase 2 above
       
       One section per finding with: (a) symptom, (b) commit SHA that introduced it, (c) lines changed, (d) scope of downstream blast (cite comp-blast output), (e) recommendation (restore-to-T0 vs keep-T1/T2/T3 vs hybrid-with-rewrite, with one-line rationale).

    4. **`coo_handoff.md`** (PRD §4.4 Deliverable 3) — PRIMARY COO INPUT:
       Plain English. Restore-to-T0 vs keep-T1/T2/T3 vs hybrid-with-rewrite — one call per field/bug. Per-call rationale. Per-call proposed fix-TO sketch with: DS lane (~A/~B/~C/~D), scope (script + line range + change description), acceptance criteria (machine-checkable assertion). COO uses this directly to author the fix-PRD + fix-TOs without re-investigation. **Every Group D recommendation MUST cite a specific row of `group_d_tagged_aua_decomposition.md`.**

    5. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_d_synthesis.md` (or appropriate date) citing all four SYNTHESIS/* deliverables + Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`.

    6. **compiler-tools-log.md** appended.

    7. **MCP handoff** to COO + CTO at synthesis-commit time per Phase 3 above.
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6: read-only across all scripts. Write-collision impossible. **~D OWNS `STAUDT/SYNTHESIS/` directory exclusively** — no other lane writes here. ~A/~B/~C MCP ~D for inclusion of cross-checkpoint findings; do not write directly to SYNTHESIS/.

    **Sequencing:** ~D blocks on ~A/~B/~C evidence packs being committed. If ~A/~B/~C are still in flight when COO sends ~D's GO, ~D should ACK and start Phase 1 setup steps that don't require evidence input (T3 direct comp-* runs at repo root) while waiting; full synthesis writes wait until all three packs land.
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7 ~D block:

    1. `delta_table.md` + `delta_table.json` committed: 4-checkpoint field × checkpoint matrix populated for every field in §3.2 with delta-class tagged.
    2. **`group_d_tagged_aua_decomposition.md` — PRIMARY deliverable per §3.3:** master table, one row per (Group D production site × field), four checkpoint columns with formula + 5-advisor sample + divergence class. Per-advisor sum-invariant check populated for all 5 top advisors per checkpoint.
    3. `bug_attribution.md`: one section per COO-bug + NNA-path-split + every parity finding + every cusip-coverage / revert-integrity finding + every Group D sum-invariant violation + every FE schema-check / cache-collision finding. Each section has commit SHA + line range cited.
    4. `coo_handoff.md`: explicit per-bug recommendation + proposed fix-TO sketch (DS lane, scope, acceptance criteria machine-checkable). Every Group D recommendation cites a specific row of `group_d_tagged_aua_decomposition.md`.
    5. `compiler-tools-log.md` appended with one row per tool run.
    6. Session log includes Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK.
    7. MCP handoff sent to COO + CTO.
    8. Evidence-file-trace holds: every claim traceable to commit SHA + line range OR pulled artifact hash OR specific row of an upstream evidence pack (~A/~B/~C).
    9. Recommendations are SPECIFIC (file + line + proposed change), not "we should think about". Fix-TO scope must be authorable by COO without re-investigation.
    10. Delta-class taxonomy is self-consistent across the delta_table — normalize across ~A/~B/~C input variations.
    11. No scope creep — fifth-bug candidate triggers MCP CTO+COO for inclusion decision, not silent addition.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5 (read verbatim before starting):

    1. **READ-ONLY.** No commits to `data/black_diamond/scripts/gold/`. No S3 writes. No gold-runner triggers. No `comp-validate` config edits.
    2. **Evidence-file-trace mandatory.** Every claim cites file path + line range OR commit SHA + line range OR specific upstream evidence-pack row. No "I remember" / "COO said" summaries.
    3. **Lane collision avoidance.** ~D OWNS SYNTHESIS/* writes exclusively.
    4. **No scratch worktree needed for T3** (use repo root); T0/T1/T2 inputs come from upstream evidence packs, not direct re-checkout.
    5. **S3 point-in-time retrieval** only for current T3 platinum pulls.
    6. **Commit scope discipline.** `--only` with explicit path list, author = `0.4.0_DS_ClientPlatform~D`.
    7. **No parallel commits to synthesis doc.** ~D owns SYNTHESIS/* — others MCP if they have a finding to add.
    8. **Recommendation specificity bar:** every fix-TO sketch in coo_handoff.md must be authorable by COO into a real TO without re-investigation. If ~D cannot specify (file + line + proposed change + acceptance criterion), flag as "needs further investigation" rather than fabricating.
  </guardrails>

  <deadline>
    6 hours after ~A/~B/~C evidence packs are all in (per PRD §4.4).
  </deadline>

  <agent_context_setup>
    Before first comp-* run:
    ```bash
    mkdir -p .comp-graph && printf "SERIAL=0.4.0_DS_ClientPlatform~D\nTO_ID=ADVI_STAUDT.D\n" > .comp-graph/.agent_context
    ```
  </agent_context_setup>

  <amendment_2026_04_20_post_authoring>
    Per CTO MCPs 20260420T~12:14Z (§3.0 lead-with framing — already inserted at top of `<scope>` above) + 20260420T121431Z (§3.4 Group B+C material-change scope). This amendment ADDS scope, deliverable, mandate, and acceptance criteria; nothing above is superseded.

    ### 3.4 Group B + Group C material-change scope — ~D synthesis obligation (Andrew 2026-04-20)

    Group D is the most important, but every material Group B and Group C change in the window must be audited because those are the upstream producers whose output D-group reads. ~A/~B/~C produce per-checkpoint `group_bc_material_changes.md` evidence packs. ~D synthesizes them into a **propagation matrix** for COO fix-TO authoring.

    **~D synthesis obligation (NEW PRIMARY DELIVERABLE):**

    `data/black_diamond/diagnostics/STAUDT/SYNTHESIS/group_bc_propagation_matrix.md` — for every B/C material change identified by ~A/~B/~C, ONE row tracing the propagation chain:

    | B/C change | Commit SHA | File:line | C-artifact affected | D-artifact affected | platinum JSON affected | portal component affected | In Group D `bug_attribution.md`? |

    Any row where a B/C change lands at platinum WITHOUT being captured in `bug_attribution.md` is an EXTRA finding class — surface to COO as a fix-TO candidate ~D recommends but didn't classify under Group D originally.

    **Authoritative B/C scripts to track in the matrix** (verbatim from §3.4):

    **Group B:** B_00 (`22736cf7` parallel forward-fill), B_01 (21+ commits — see ~A/~B/~C inventories), B_01b (search), B_02/B_03 (`856855f3` DAG race fix).

    **Group C:** C_00 (`f177240b` Polars + `22736cf7` cumsum + `4a6173db` runner install), C_01 (`bf9651b8` CN-P1 + `9e47830c`/`dc4980c3` CN-P1b — NNA Class 1 path producer), C_01b (search), C_02/C_04/C_05/C_06 (quiet — confirm), C_03 (`85bb2daa` phantom outflow — load-bearing for NNA), C_07 (`f49aa9bd` C07-T1 RCA — confirm stable), C_08 (already PRIMARY §3.3; B9/B8b/B10 + canonical role order + WAR ROOM iterrows + CN-P5 + RA-P5 + defensive backfill + revert).

    ### Additional compiler mandate per §3.4 (Phase 1 deltas — augments the §3.3 mandate above):

    - At T3 (repo root): `comp-pipescript io B_00 && comp-pipescript io B_01 && comp-pipescript io B_02 && comp-pipescript io B_03 && comp-pipescript io C_00 && comp-pipescript io C_01 && comp-pipescript io C_03 && comp-pipescript io C_07` to anchor T3 baseline for matrix.
    - At T3: `comp-blast B_01 && comp-blast C_00 && comp-blast C_01 && comp-blast C_03 && comp-blast C_08` to anchor T3 propagation for matrix.

    ### Additional deliverable per §3.4:

    `data/black_diamond/diagnostics/STAUDT/SYNTHESIS/group_bc_propagation_matrix.md` per the row spec above. ~D OWNS this file exclusively. Cross-reference each row to the source ~A/~B/~C `group_bc_material_changes.md` row that surfaced it. Highlight rows that fall outside Group D `bug_attribution.md` as "extra-class findings" and include them in `coo_handoff.md` as additional fix-TO candidates.

    ### Additional acceptance criteria per §3.4 + §3.0:

    1. `STAUDT/SYNTHESIS/group_bc_propagation_matrix.md` committed. Every B/C material change from ~A/~B/~C inventories has a row tracing C → D → platinum → portal. Cross-reference back to source evidence file. Missing = REWORK.
    2. Every "extra-class finding" (B/C change at platinum NOT in `bug_attribution.md`) has a recommendation in `coo_handoff.md` per the same restore-to-T0 / keep / hybrid framework. Missing = REWORK.
    3. **MANDATORY INVARIANT per §3.0** — `group_d_tagged_aua_decomposition.md` (the master synthesis table) MUST include a per-checkpoint sum-invariant column for each of the 5 top advisors:
       - `sum(role_breakdown[*].aua) == tagged_aua`
       - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`
       Violations rolled into `bug_attribution.md` with advisor ID + checkpoint + delta. Missing = REWORK.
    4. Dependency unchanged — ~D blocks on ~A/~B/~C `group_bc_material_changes.md` packs being committed in addition to the existing Group D evidence packs.
  </amendment_2026_04_20_post_authoring>
</task_order>
