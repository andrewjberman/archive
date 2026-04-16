<task_order>
  <metadata>
    <id>ADVI_ROLLUP.T1d</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to><!-- self-authored + executed per COO 2026-04-16T12:54Z GO ("(c) Pull T1d ... Author a TO (self-assignment is fine; follow canonical triad format) OR emit a memo if you conclude it's a one-pass cleanup") -->
    <date>2026-04-16</date>
    <status>complete</status><!-- path (b) doc-only; classification memo ships, no D_02 code change -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>3 (Frontend correctness — producer hygiene adjacent to D00c-T1, D01-T1, D02-T2)</wave>
    <priority>P4 (no consumer breakage; hygiene classification)</priority>
    <slug_note>T1d = fourth triage branch off the D00c-T1 zero-current-activity cohort; parallel to D01-T1 and D02-T2 (which sibling ~B owns). T1d scope = the 20 advisor slug prefixes under `s3://opal-data-bd/gold/entities/advisors/` that have `timeseries.json` but NO `book.json` in the 2026-04-15 gold run. ~A witnessed these during the B4 `top_gain_positions` 166-advisor sweep (commit 80109df5).</slug_note>
  </metadata>

  <references>
    <ref type="trigger">~A B4 sweep finding (commit 80109df5, log `logs/2026-04-16/b4_top_gain_positions_sweep_closeout.md` — 20 slug prefixes with no book.json surfaced during 183-slug enumeration).</ref>
    <ref type="related">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ROLLUP.D00c-T1.ds-leaderboard-advisor-count-reconciliation.md (~C path b doc-only close 2026-04-15)</ref>
    <ref type="related">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ROLLUP.D01-T1.ds-d01-geo-aua-snapshot-gap-triage.md (~C path b close 2026-04-15)</ref>
    <ref type="related">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ROLLUP.D02-T2.ds-zero-activity-advisor-summary-vs-role-breakdown-inconsistency.md (~B lane — adjacent producer triage)</ref>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md</ref>
  </references>

  <objective>
    Audit the 20 advisor slug prefixes under `s3://opal-data-bd/gold/entities/advisors/` that have `timeseries.json` present but `book.json`, `mix.json`, `composition.json` absent in the 2026-04-15 gold run. Classify each as:
    - **(a) stale slug from rename** — source-data spelling drift, real advisor now at a different slug
    - **(b) pending producer gap** — advisor IS currently assigned but D_02 failed to emit the book
    - **(c) legitimate orphan / catch-all** — historical timeseries preserved but no current assignment (departed advisor, pseudo-advisor, inactive role)
  </objective>

  <acceptance_criteria>
    1. All 20 orphan slugs classified with quantitative evidence (timeseries first/last date, last-row AUA, name match against active slugs).
    2. If any (b) found: D_02 code path identified + patch authored (follow canonical commit-before-deploy triad).
    3. If only (a) + (c): memo-only close — inline classification table in session log + `docs/analysis/`, plus comp-platinum reverse evidence that no portal consumer resolves to the orphan slug.
    4. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    5. MCP COMPLETE to COO with classification table + chosen path + consumer-impact statement.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>Confirm `advisor_book_key` + `advisor_timeseries_key` are D_02 emits (not external). Identify writer code paths.</expect>
      </step>
      <step>
        <run>comp-platinum reverse gold/entities/advisors</run>
        <expect>Who consumes `gold/entities/advisors/{*}/book.json` and `.../timeseries.json` in portal dataflow — verify no orphan-slug consumer.</expect>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/entities/advisors/{orphan}/ for each of 20</run>
        <expect>Confirm only `timeseries.json` present (no book/mix/composition).</expect>
      </step>
      <step>
        <run>aws s3 cp timeseries.json + python analyze first/last date, last AUA, advisor_name</run>
        <expect>Classify each slug against the (a)/(b)/(c) taxonomy.</expect>
      </step>
      <step>
        <run>python token-match sweep orphan_slugs vs active_slugs</run>
        <expect>Surface rename candidates by shared name-like tokens.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Classification table reconciliation — every slug landed in exactly one bucket; evidence cited per slug</run>
        <expect>20/20 classified.</expect>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>{path (a) or (b) only: re-verify via one-shot orphan-prefix S3 ls after next gold run}</run>
        <expect>Not applicable for path (b) doc-only.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/><!-- Read-only audit. D_02 in flight with ~B B3.fix (L358 + L2272), ~D CN-P2 (NNA atomic reader), RA-P2 role_aua shadow writer. Path b doc-only → no D_02 edit → no commit collision. -->
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>

  <validation_result>
    Path (b) chosen — memo-only close. No D_02 code change.

    Classification: 2 (a) stale-rename, 0 (b) producer gap, 18 (c) legitimate orphan.

    Rename cases (a):
    - `david_ferrell` → active at `david_farrell` (ending AUA $111.77M vs orphan $0.36M; orphan last 2026-01-19)
    - `olivia_shin` → active at `liv_shin` (ending AUA $54.27M vs orphan $0.22M; orphan last 2026-01-19)

    Legitimate orphans (c) — 18 departed/inactive advisors, all with last AUA = $0 or small residual, last dates 2024-06 through 2026-03:
      49_solutions, 49f_house, alex_barnes, chad_crabill, connor_stiscak, ellie_shank, griffin_rea, jacob_villarreal, joshua_studebaker, kyle_kevorkian, luke_blackmon, maxwell_meyers, meredith_lipps, michael_wuest, mike_defrees, quinn_davis, ryan_fidler, ryan_witte

    Consumer impact: ZERO.
    - `comp-platinum reverse gold/entities/advisors` → no components found in dataflow index.
    - `platinum/firm/leaderboard.json` (2026-04-15 15:34): 157 unique advisor IDs, 0/20 orphan hits.
    - `platinum/advisors/{orphan}/*` mostly empty or stale pre-04-15.

    Producer note (informational — not a bug this TO patches):
    `build_advisor_books` (L1089, L1094-1099) scopes books to `latest_snap` advisor set only. `build_advisor_timeseries` (L1521) iterates full `acct` history (includes historical-only advisors). D_02's stale-cleanup step (L2745-2775) deletes orphan prefixes BEFORE Step 5 writes timeseries → timeseries.json re-creates orphan prefix. Result: timeseries.json without book.json. Not user-facing; parked for future D_02 hygiene pass (e.g. filter `build_advisor_timeseries` to latest-snap, OR move stale-cleanup to after Step 6).

    Deliverables:
    - Classification memo: `docs/analysis/2026-04-16_t1d_orphan_advisor_slug_classification.md`
    - Session log: `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-16/t1d_orphan_advisor_slug_classification.md`
  </validation_result>

  <next>
    Path (b) chosen — no follow-up. Next D_02 refactor (BDPL_CNPRCS or similar) can optionally incorporate the producer hygiene note to retire orphan timeseries writes. Flag to ~B / DE at their discretion; not this TO's scope.
  </next>
</task_order>
