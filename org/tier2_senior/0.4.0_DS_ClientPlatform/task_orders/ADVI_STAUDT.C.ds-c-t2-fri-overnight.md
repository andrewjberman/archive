<task_order>
  <metadata>
    <id>ADVI_STAUDT.C</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-20</date>
    <status>staged</status><!-- CTO confirms shape before COO dispatches GO -->
    <project_code>ADVI_STAUDT</project_code>
    <lane>~C — T2 Friday 00:00-07:00 ET (council + B_01 cusip rework)</lane>
    <priority>P0 — gates fix-TO authoring on Friday breakage attribution</priority>
    <git_anchor>ae759bbb</git_anchor>
    <wall_clock>Fri 2026-04-17 ~07:00 ET</wall_clock>
    <scope_weight>HEAVY — includes cusip-coverage probe + revert-integrity check</scope_weight>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md</ref>
    <ref type="prd-section">§4.3 (lane scope), §3.2 (fields in scope), §3.3 (Group D PRIMARY focus), §5 (guardrails), §6 (cross-domain), §7 (acceptance)</ref>
    <ref type="upstream">CTO MCP 20260420T120334Z — §3.3 amendment locking Group D tagged_aua / role-split / fee-split as PRIMARY scope</ref>
    <ref type="upstream">CTO MCP 20260417T213111Z — 4-bug audit ratification</ref>
    <ref type="cto-handoff">CTO MCP 20260420T~12:00Z — STAUDT PRD handoff</ref>
  </references>

  <objective>
    Deliver the T2 (Fri 2026-04-17 ~07:00 ET, git `ae759bbb`) checkpoint of ADVI gold + portal state. T2 captures the post-council, post-snapshot_date-revert-cycle, post-unrealized-rolling-key-revert-cycle, post-B_01-cusip-rework state — BEFORE the bond-100x fix and tiered cap. Includes a cusip-coverage probe (verify session-32 98.3% figure holds at T2) and a revert-integrity check (confirm `4317354a` revert vs `ec2c1efc` re-ship behavior matches intent). Read-only audit only.
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

    **MANDATORY INVARIANT per checkpoint per advisor (must check, every checkpoint, every advisor):**
    - `sum(role_breakdown[*].aua) == tagged_aua`
    - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`

    Any checkpoint where these fail is a mapping-ambiguity finding — cite advisor ID + checkpoint + delta magnitude in `group_d_tagged_aua_role_fee_decomposition.md`.

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

    <!-- Lane ~C specific scope (PRD §4.3 + §3.2) -->

    **Per-script audit at T2 `ae759bbb`:**
    - B_01 (T2 = post-cusip-rework: `1db831aa` re-key RPS sell-correction to (account_id, cusip), `f5f19e77` runtime CUSIP enrichment via bd_assets_dim, `c4ebde9a` cusip-keyed silver/unrealized veto, `ae759bbb` RPS absence != close signal). PRE bond-100x fix (`d45fc0dc`), PRE tiered cap (`cb6d78e2`), PRE `market_value_uncapped` column.
    - D_00c / D_02 / D_04 / D_00b / D_01 / C_08 — same as T1 (no D-group changes 2026-04-17 00:00-07:00 ET except as noted below).

    **Council session window (00:09–01:14 ET):** `ec2c1efc` GOLD-DATE-FIX, `9bb1094a` + `40a00bd0` + `67a0d0fb` + `7da58e60` + `95425624` + `d614b5ca` + `c8555120` + `b27299b0` — council ~A/~B/~C/~D deliverables; 8-35M actual-close baseline.

    **Silver-layer churn (overnight):**
    - `c270a9b2` (rolling-key refresh) → `32fbb0d6` (revert of rolling key) → `2a69b97e` (snapshot-date keying)
    - `80917a1e` cusip column added to silver/transactions (CP-AE1)
    - `6c80c5ed` Schwab ULN → silver/ULN/ (AE)

    **B_01 snapshot-date cycle:**
    - `59340b42` → `4317354a` (Andrew revert) → `ec2c1efc` (re-ship with silver/allocations anchor)

    **Special scope — reverted-path audit (PRD §4.3):**
    For every reverted commit, confirm the revert actually stuck. For `4317354a` vs `ec2c1efc`: diff the final B_01 snapshot_date derivation. Is the working behavior the same as intended? Same for `c270a9b2` vs `32fbb0d6` (rolling-key refresh attempt that was reverted).

    **Special scope — cusip coverage probe (PRD §4.3):**
    On the T2 state, enumerate the cohort of B_01 rows where cusip is populated vs null. Compare against the `cusip_non_null_ratio = 98.3%` figure from session-32 sanity check. Verify the figure holds at T2 (CP-DS1 `1db831aa` fix was intended as the mechanism). If figure differs by > 0.5 percentage points, FINDING for ~D's bug_attribution.md.

    **Fields in scope (§3.2):** same as ~A and ~B. Note: at T2 we are still pre-`market_value_uncapped` (that arrives with `cb6d78e2` at T3) — do not report at T2.

    **S3 platinum snapshots (T2 cutoff = 2026-04-17 12:00 UTC):**
    - `s3://opal-data-bd/platinum/firm/leaderboard.json` at latest version ≤ 2026-04-17 12:00 UTC
    - `s3://opal-data-bd/platinum/firm/fee_efficiency.json` same cutoff
    - `s3://opal-data-bd/platinum/advisors/{travis,kyle,hunter,alex,tim}/summary.json`
    - `s3://opal-data-bd/platinum/firm/header_metrics.json`
    - `s3://opal-data-bd/gold/canonical/nna_atomic/2026-04-15.parquet`
    - `s3://opal-data-bd/gold/canonical/role_aua/2026-04-15.parquet`
    - `s3://opal-data-bd/silver/transactions/2026-04-15.parquet` (post-CP-AE1 cusip column add — verify cusip column PRESENT)
    - `s3://opal-data-bd/silver/ULN/2026-04-15.parquet` (post-Schwab ULN ingest — verify path PRESENT)
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write — T2 reconstruction setup">
      <step>
        <run>git worktree add /tmp/staudt_T2 ae759bbb</run>
        <expect>Clean checkout per PRD §5 guardrail #4.</expect>
        <if_mismatch>Force-remove + retry; if still failing, MCP COO.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T2 && comp-pipescript io B_01</run>
        <expect>READS include silver/unrealized (cusip-keyed veto per `c4ebde9a`), bd_assets_dim (runtime CUSIP enrichment per `f5f19e77`). RPS sell-correction merge keys on (account_id, cusip) per `1db831aa`. NO `market_value_uncapped` write yet (that's T3). Snapshot_date derivation from silver/allocations per `ec2c1efc`.</expect>
        <if_mismatch>Document every read/write mismatch — these are direct evidence inputs for ~D's bug attribution.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T2 && comp-pipescript io D_00c &amp;&amp; comp-pipescript io D_02 &amp;&amp; comp-pipescript io D_04 &amp;&amp; comp-pipescript io D_00b &amp;&amp; comp-pipescript io D_01 &amp;&amp; comp-pipescript io C_08</run>
        <expect>D-group + C_08 unchanged from T1 (no D-group commits in the 00:00-07:00 ET window). All read CANONICAL_NNA_ATOMIC_PREFIX (still pre-`cd177553` revert).</expect>
        <if_mismatch>Document any unexpected change.</if_mismatch>
      </step>
      <step>
        <run>cd /tmp/staudt_T2 && comp-blast B_01 &amp;&amp; comp-blast D_00c &amp;&amp; comp-blast D_04 &amp;&amp; comp-blast C_08 &amp;&amp; comp-blast D_00c._weighted_aua</run>
        <expect>Blast snapshot at T2. Function-level _weighted_aua per CTO §3.3.</expect>
        <if_mismatch>Function-level node MISSING per ADHC_ROUTER Phase 2 backlog → MCP COO+CTO; do not skip.</if_mismatch>
      </step>
      <step>
        <run>comp-trace tagged_aua &amp;&amp; comp-platinum reverse tagged_aua &amp;&amp; comp-platinum reverse fee_breakdown.no_fee.aua &amp;&amp; comp-platinum reverse aua_growth_pct &amp;&amp; comp-platinum reverse cusip</run>
        <expect>Producer + consumer paths for the three Group D primary fields + cusip (since CP-DS1 cusip rework lands in this window).</expect>
        <if_mismatch>Document missing nodes.</if_mismatch>
      </step>
      <step>
        <run>REVERT INTEGRITY CHECK: cd /tmp/staudt_T2 && git show 4317354a -- 'data/black_diamond/scripts/gold/B_01*' &amp;&amp; git show ec2c1efc -- 'data/black_diamond/scripts/gold/B_01*' &amp;&amp; diff &lt;(git show 4317354a:data/black_diamond/scripts/gold/B_01.holdings_lots.py 2>/dev/null) &lt;(git show ec2c1efc:data/black_diamond/scripts/gold/B_01.holdings_lots.py 2>/dev/null)</run>
        <expect>Diff shows snapshot_date derivation difference between the revert and the re-ship. Document whether final T2 behavior matches intent. Same pattern for `c270a9b2` vs `32fbb0d6` rolling-key revert.</expect>
        <if_mismatch>If revert was incomplete (final tip behavior matches the reverted version), FINDING — surface to ~D.</if_mismatch>
      </step>
      <step>
        <run>CUSIP COVERAGE PROBE: pull silver/transactions/2026-04-15.parquet AND gold output of B_01 at T2 (whichever PROD/QA artifact represents T2). Compute count(cusip IS NOT NULL) / count(*) by lot_id. Compare to 98.3% benchmark from session-32.</run>
        <expect>≥ 97.8% (allow 0.5pp drift). Per-lot vs per-row distinction noted in evidence pack.</expect>
        <if_mismatch>If &lt; 97.8% or &gt; 98.8%, FINDING — surface delta + cohort breakdown to ~D.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before committing evidence pack">
      <step>
        <run>comp-build && comp-validate D_04 --artifact /tmp/staudt_T2_artifacts/leaderboard.json &amp;&amp; comp-validate C_08 --artifact /tmp/staudt_T2_artifacts/fee_efficiency.json &amp;&amp; comp-validate B_01 --artifact /tmp/staudt_T2_artifacts/holdings_lots.parquet</run>
        <expect>Document validator output + gaps. B_01 will SKIP per session-32 finding — capture. D_04 windows[0] vs windows.{QTD,YTD,MAX} bug capture.</expect>
        <if_mismatch>Document gap. Continue.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after committing evidence pack">
      <step>
        <run>Append rows to org/compiler-tools-log.md for every comp-* run above</run>
        <expect>One row per tool run with TO_ID=ADVI_STAUDT.C. Auto-append should fire if `.comp-graph/.agent_context` is set to `SERIAL=0.4.0_DS_ClientPlatform~C` and `TO_ID=ADVI_STAUDT.C`.</expect>
        <if_mismatch>Manually append per the log format.</if_mismatch>
      </step>
      <step>
        <run>git worktree remove /tmp/staudt_T2</run>
        <expect>Scratch worktree cleaned up.</expect>
        <if_mismatch>Force-remove.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    All under `data/black_diamond/diagnostics/STAUDT/T2_friday_earlyam/`:

    1. **`state.md`** — Per PRD §4.3: per-script subsections + §3.2 field list with line range + sample value per 5 top advisors + firm. IO manifest. Validator config gaps.

    2. **`T2_evidence.json`** — Machine-readable field-value snapshot.

    3. **`group_d_tagged_aua_role_fee_decomposition.md`** — PRIMARY deliverable per §3.3 (NON-NEGOTIABLE):
       (a) Producer-sites table at T2.
       (b) Per-5-advisor trace at T2.
       (c) Divergence table at T2 — cite advisor IDs.
       (d) Definition vs source table T1→T2 deltas annotated.

    4. **`cusip_coverage_probe.md`** — Coverage % at T2 + comparison to session-32 benchmark + per-account-type breakdown. Either "holds" with evidence OR "drift" with cohort.

    5. **`revert_integrity_check.md`** — One sub-section per reverted-then-re-shipped commit pair: (a) `4317354a` vs `ec2c1efc` (snapshot_date), (b) `c270a9b2` vs `32fbb0d6` (rolling-key). For each: diff text + "revert stuck Y/N" + behavioral implication.

    6. **Session log** at `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-20/staudt_t2_fri_overnight.md` (or appropriate date) citing STAUDT deliverables + Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`.

    7. **compiler-tools-log.md** appended.
  </deliverables>

  <cross_domain_coordination>
    Per PRD §6: read-only across all scripts. Write-collision impossible. Lane-scoped evidence dir `STAUDT/T2_friday_earlyam/` (~C only). Cusip-coverage probe and revert-integrity findings that ~D needs verbatim for bug_attribution.md → MCP ~D directly with the (commit, file, finding) tuple — do not write to SYNTHESIS/.
  </cross_domain_coordination>

  <acceptance_criteria>
    Per PRD §7 (per-lane block):

    1. `state.md` committed under `STAUDT/T2_friday_earlyam/` with all required sub-content.
    2. `T2_evidence.json` committed.
    3. `group_d_tagged_aua_role_fee_decomposition.md` committed per §3.3 — must contain ALL FOUR sub-tables. Missing any sub-table = REWORK.
    4. **`cusip_coverage_probe.md` committed** — coverage % with evidence (per-lot OR per-row clearly stated). Missing = REWORK.
    5. **`revert_integrity_check.md` committed** — both revert-pairs covered. Missing either = REWORK.
    6. `compiler-tools-log.md` appended with one row per tool run.
    7. Session log includes Compiler Tools section reproducing every `<run>` with observed output and explicit pass/fail vs. `<expect>`. Missing rows = REWORK.
    8. Evidence-file-trace holds: every claim traceable to commit SHA + line range OR pulled artifact hash.
    9. No scope creep — fifth-bug candidate or out-of-§3.2/§3.3 finding triggers MCP CTO+COO, not silent inclusion.
  </acceptance_criteria>

  <guardrails>
    Per PRD §5 (read verbatim before starting):

    1. **READ-ONLY.** No commits to `data/black_diamond/scripts/gold/`. No S3 writes. No gold-runner triggers. No `comp-validate` config edits.
    2. **Evidence-file-trace mandatory.**
    3. **Lane collision avoidance.** ~C writes ONLY under `STAUDT/T2_friday_earlyam/`.
    4. **Scratch worktree for historical checkouts.** Never `git checkout` at repo root.
    5. **S3 point-in-time retrieval.** Document any missing version. silver/ULN/ landed mid-window — verify path + first-version timestamp.
    6. **Commit scope discipline.** `--only` with explicit path list, author = `0.4.0_DS_ClientPlatform~C`.
    7. **Cusip-coverage probe distinction:** report per-lot AND per-row coverage if they differ — session-32 figure ambiguous on grain.
  </guardrails>

  <deadline>
    8 hours after COO GO message lands in your inbox (heavier scope than ~A per PRD §4.3).
  </deadline>

  <agent_context_setup>
    Before first comp-* run:
    ```bash
    mkdir -p .comp-graph && printf "SERIAL=0.4.0_DS_ClientPlatform~C\nTO_ID=ADVI_STAUDT.C\n" > .comp-graph/.agent_context
    ```
  </agent_context_setup>

  <amendment_2026_04_20_post_authoring>
    Per CTO MCPs 20260420T~12:14Z (§3.0 lead-with framing — already inserted at top of `<scope>` above) + 20260420T121431Z (§3.4 Group B+C material-change scope). This amendment ADDS scope, deliverable, mandate, and acceptance criteria; nothing above is superseded.

    ### 3.4 Group B + Group C material-change scope (Andrew 2026-04-20) — VERBATIM

    Group D is the most important, but every material Group B and Group C change in the window must be audited because those are the upstream producers whose output D-group reads. An upstream definitional change with a mild direct effect can cascade to a severe D-group effect.

    **Authoritative B/C scripts in scope at T2 `ae759bbb` (each gets a line in your `group_bc_material_changes.md` inventory — no collapse):**

    **Group B (Block-level: holdings, canonical prices, transactions):**
    - `B_00.canonical_fills.py` — at T2: same as T1 (no new commits in T1→T2 window). Confirm stability.
    - `B_01.holdings_lots.py` — HEAVY in T1→T2 window: `ec2c1efc` (Fri 00:09 GOLD-DATE-FIX), `59340b42`→`4317354a` (Thu 23:14-23:15 snapshot_date option-d + revert), `a9f42c3b`→`0e9ece2a` (Thu 22:38-23:08 stale-RPS auto-skip + removal), `52b78c0d`+`b320426b` (Thu 22:51-22:53 df.attrs strip), `5438de6e`+`cd00ff2c` (Fri 08:33-08:36 silver-authority gate PIVOT 2 + Gate 3 silent-close), `7e57576f`+`c693d5a3`+`d39c4dff` (Fri 09:00-09:49 PIVOT 5/6 synth-inject gate), `1db831aa`+`f5f19e77`+`c4ebde9a`+`ae759bbb` (Fri 06:11-07:40 cusip rework). Audit: snapshot_date derivation path (revert integrity covered in §4.3 probe) · stale-RPS behavior · `df.attrs` serialization path · silver-authority gate cohort size · PIVOT evolution · Gate 3 silent-close cohort size · cusip merge keying ((account_id, cusip) per `1db831aa`).
    - `B_01b` — search commits T1→T2; if touched, audit.
    - `B_02 / B_03` — at T2: same as T1 (DAG fix already landed). Confirm stability.

    **Group C (Canonical layer: performance, NNA, role_aua, fees, views, advisor_fee_efficiency):**
    - `C_00.canonical_performance.py` — at T2: same as T1 (Polars port already landed; no new commits). Confirm stability + cite hash equality if possible.
    - `C_01.canonical_nna.py` — at T2: same as T1 (CN-P1b backfill already landed; no new commits). Confirm `nna_atomic/` partition presence + schema unchanged.
    - `C_01b` — search commits T1→T2; if touched, audit.
    - `C_02 / C_04 / C_05 / C_06` — quieter scripts; grep T1→T2 commits. If quiet, document "no material change in T1→T2 window" with grep evidence.
    - `C_03.canonical_performance.py` — `85bb2daa` (Fri 09:42 phantom outflow pulse fix — IN T1→T2 WINDOW — recompute cum_inflows/cum_outflows on dense date grid post-merge cumsum). **Load-bearing for NNA.** `ACCOUNT_PERFORMANCE` is read by D_00c, D_02, D_04. Audit: cum_inflows/cum_outflows at T1 (pre-fix) vs T2 (post-fix) for sample advisors · advisor-level and firm-level daily NNA derived from C_03 output · does the phantom outflow pulse exist at T1 but not T2? · any downstream advisor whose NNA flipped sign between T1 and T2.
    - `C_07.advisor_dimensions.py` — at T2: same as T1 + T0 (no new commits). Confirm stability.
    - `C_08.advisor_fee_efficiency.py` — already PRIMARY in §3.3. §3.4 adds at T2: same as T1 (no new C_08 commits in T1→T2 window — defensive backfill `9e537f9f` and revert `cd177553` land Friday afternoon, AFTER T2 anchor `ae759bbb` 07:40 ET). Confirm C_08 still reads atomic at T2 (CN-P5 not-yet-reverted).

    **Silver-layer churn in T1→T2 window** (out of B/C strict scope but related):
    - `c270a9b2` (rolling-key refresh) → `32fbb0d6` (revert of rolling key) → `2a69b97e` (snapshot-date keying)
    - `80917a1e` cusip column added to silver/transactions (CP-AE1)
    - `6c80c5ed` Schwab ULN → silver/ULN/ (AE)
    Audit: revert integrity (covered in §4.3 + Phase 1 above), silver/transactions cusip column presence at T2, silver/ULN/ first-version timestamp.

    ### Additional compiler mandate per §3.4 (Phase 1 deltas — augments the §3.3 mandate above):

    - `cd /tmp/staudt_T2 && comp-pipescript io B_00 && comp-pipescript io B_01 && comp-pipescript io B_02 && comp-pipescript io B_03 && comp-pipescript io C_00 && comp-pipescript io C_01 && comp-pipescript io C_03 && comp-pipescript io C_07` (skip quiet scripts that have no commits in T1→T2 window; document the skip with grep evidence)
    - `cd /tmp/staudt_T2 && comp-blast B_01 && comp-blast C_00 && comp-blast C_01 && comp-blast C_03 && comp-blast C_08`
    - Cusip-coverage probe + revert-integrity check already in Phase 1 above per §4.3 — those satisfy the §3.4 Phase 2 mandate for ~C.

    ### Additional deliverable per §3.4:

    `data/black_diamond/diagnostics/STAUDT/T2_friday_earlyam/group_bc_material_changes.md` with the four required sections per §3.4: (1) touched-script inventory at T2, (2) per-change delta with formula/logic + commit SHA + file:line, (3) downstream propagation per `comp-blast`, (4) numeric signal at T2 — at least one sampled figure (firm total OR sample advisor OR sample account) for every touched B/C script that changed between T1 and T2. Quiet scripts get an explicit "no material change in T1→T2 window" line with grep evidence.

    ### Additional acceptance criteria per §3.4 + §3.0:

    1. `group_bc_material_changes.md` committed under `STAUDT/T2_friday_earlyam/`. Script-line discipline: each touched B/C script gets its own line — no collapse. Quiet scripts (C_02/C_04/C_05/C_06) explicitly noted "no material change in T1→T2 window" with grep evidence; silent omission = REWORK.
    2. **MANDATORY INVARIANT per §3.0** — for every advisor at T2 (5 top + firm-level), check both invariants:
       - `sum(role_breakdown[*].aua) == tagged_aua`
       - `fee_breakdown.fee_paying.aua + fee_breakdown.no_fee.aua == tagged_aua`
       Violations cited in `group_d_tagged_aua_role_fee_decomposition.md` with advisor ID + T2 + delta magnitude. Missing invariant evidence = REWORK.
  </amendment_2026_04_20_post_authoring>
</task_order>
