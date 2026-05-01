<task_order>
  <metadata>
    <id>ADVI_49FRECN.001</id>
    <project>ADVI_49FRECN</project>
    <title>Phase 0 — 49F AUA + Account-Count Reconciliation Discovery</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>open</status>
    <priority>P1 — partner data accuracy regression vs 99.1% baseline (ADVI_AUAVAR closeout 2026-03-09)</priority>
    <estimated_effort>0.5–1d (discovery only — no code fixes)</estimated_effort>
  </metadata>

  <context>
    Andrew directive 2026-05-01:

      "Currently we are displaying a number 3.59% lower for AUA than they actually display,
       and we are displaying ~6025 accounts when we know there are actually 6611.
       We need to do another pass of investigation to see where we are inaccurate,
       where we overshoot, where we undershoot, what accounts we're not tracking, etc."

    Quantified gaps (vs 49F's actual):
    - **AUA**: Opal is 3.59% LOW (matches earlier Mar-09 99.1% baseline drift trajectory)
    - **Accounts**: Opal shows ~6025 vs 49F's 6611 → 586 missing, ~8.86% undercount

    The account-count gap is materially larger than the AUA gap, which means the
    missing accounts are below-average size on average (could be IRA rollovers in
    flight, micro-accounts, custodian-specific gaps, deceased/closed-but-still-listed
    cohorts, etc. — discovery should disambiguate).

    Prior reconciliation cycles (closed):
    - ADVI_AUAVAR 2026-03-09: full $73.6M gap attributed; BKF fix deployed; 99.1% accuracy
    - ADVI_NNAVAR 2026-03-09: NNA variance investigation (gap attributed to Holding MV withdrawn = correct behavior)
    - Schwab TRN NNA enrichment 2026-04-21: AE layers A+B shipped `bea387a9` (Schwab imputes novel gaps); DS Phase 6 C_01 merge pending

    You (DS~B) already hold the Schwab/49F NNA reconciliation context. This TO leverages that.
  </context>

  <objective>
    Produce a quantitative reconciliation matrix and per-gap root-cause writeup.
    NO code fixes in Phase 0. Phase 1+ remediation TOs will be authored based on
    your findings — file each remediation as a follow-on TO with clear scope.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Source-of-truth comparison numbers</title>
      <detail>
        From Andrew or 49F's reporting (he has direct partner access), capture the 49F-side reference snapshot:
        - Total AUA at a specific date (note the date)
        - Total account count at the same date
        - Per-advisor breakdown if available (49F has ~12 advisors per ROLEAUA closeout)
        - Per-account-type breakdown if available (taxable / IRA / Roth / 401k / SMA / etc.)
        - Per-custodian breakdown if available (Schwab / Fidelity / TD / Pershing / etc.)

        If 49F reference snapshot is incomplete, document what's available and proceed with what we have.
      </detail>
    </ac>

    <ac id="2">
      <title>Opal-side comparable snapshot at the same date</title>
      <detail>
        Pull the same dimensions from Opal's gold artifacts at the matching date:
        - `gold/d_00/...` (firm-level totals)
        - `gold/d_00b/...` (per-advisor)
        - `gold/d_02/...` (account-level if present)
        - `bd_assets_dim` joined with `bd_securities` for asset-class breakdown
        - Use `comp-pipescript io` first to confirm exact column availability per script.

        Document the artifact paths + run-date used so the comparison is reproducible.
      </detail>
    </ac>

    <ac id="3">
      <title>Reconciliation matrix — per-axis gap quantification</title>
      <detail>
        Produce a markdown table for each of: per-advisor, per-account-type, per-custodian. Columns: dimension value | 49F count + AUA | Opal count + AUA | account delta (count) | AUA delta ($ + %) | gap classification.

        Gap classifications to use:
        - **MISSING_FROM_OPAL** — account exists at 49F, absent from Opal
        - **MISSING_FROM_49F** — Opal-side account that 49F doesn't show (rare; possibly closed-still-listed)
        - **AUA_UNDERSHOOT** — same account both sides, Opal value lower
        - **AUA_OVERSHOOT** — same account both sides, Opal value higher
        - **CLASSIFICATION_DIFFERS** — same account both sides, but counted in different bucket
        - **UNKNOWN** — unable to match account-level
      </detail>
    </ac>

    <ac id="4">
      <title>Account-level missing-from-Opal investigation</title>
      <detail>
        Account count gap is the biggest quantified delta (586 missing). For these specifically:

        1. Pull Opal's account-id list at the reference date
        2. Compare to 49F's account list (if Andrew can provide; otherwise infer from totals)
        3. For each missing account or sample of representative ones, trace upstream:
           - Is the account in BD bronze ingestion at all? (`s3://opal-data-bd/bronze/...`)
           - If yes, is it filtered out at silver? Which step?
           - If no, why isn't BD producing it? (custodian feed gap? account-state filter? household linkage?)
        4. Hypothesized buckets to look for (based on the size-implied small-account hint):
           - In-flight IRA rollovers / pending account opens
           - Closed accounts within last X days that 49F still reports vs Opal already drops
           - Sub-accounts (sleeves, model-portfolio sub-positions) counted differently
           - Joint accounts represented as 1-on-49F-side, 2-on-Opal-side or vice versa
           - Specific custodian feeds that Opal is missing entirely
           - Trust/fiduciary accounts with linkage edge cases
      </detail>
    </ac>

    <ac id="5">
      <title>AUA gap — overshoot/undershoot allocation</title>
      <detail>
        For the 3.59% AUA gap, decompose:
        1. How much is attributable to the missing-account undercount (multiply count gap × avg account AUA)?
        2. After subtracting that, how much residual gap remains?
        3. Residual gap allocation by axis:
           - Per asset class (fixed income, equity, alternatives, cash) — which bucket undershoots/overshoots most?
           - Per custodian (price source differences, settled-vs-trade-date timing)
           - Per holding type (mutual fund NAV vs ETF NAV vs bond price vs SMA holdings)
        4. Cross-reference with prior reconciliation findings:
           - ADVI_AUAVAR BKF fix: still in place? Verify
           - Schwab TRN NNA enrichment: relevant to this gap?
           - ETFClassifier (ADVI_CLSPT2): any classification drift causing axis misallocation?
      </detail>
    </ac>

    <ac id="6">
      <title>Phase 1 remediation TO recommendations</title>
      <detail>
        Based on findings, propose follow-on Phase 1 TOs. For each:
        - Title
        - Lane (DS / AE / DT / RD)
        - Estimated effort
        - Acceptance criteria sketch (1–2 lines)
        - Priority (P0 → P3)

        Examples of what these might look like (do NOT prescribe — let findings drive):
        - "DS C_01 + bd-pipeline ingest filter relaxation for in-flight rollover accounts"
        - "AE silver-stage backfill of {custodian} feed gap from {date}"
        - "DT/DE Mix-tab classification drift fix — bond bucket migration"
        - "DS BD silver dedup logic — joint-account double-count"
      </detail>
    </ac>

    <ac id="7">
      <title>Deliverable</title>
      <detail>
        Single markdown report at `docs/architecture/49F_RECONCILIATION_2026-05-01.md`:
        - Executive summary (2 paragraphs: what we found, recommended next moves)
        - Reference snapshot details (date, source, what's complete vs partial)
        - Reconciliation matrix tables (AC #3)
        - Missing-account investigation findings (AC #4)
        - AUA gap decomposition (AC #5)
        - Phase 1 TO recommendations (AC #6)
        - Open questions for CTO / Andrew if anything is unresolvable from data alone
      </detail>
    </ac>
  </acceptance_criteria>

  <constraints>
    <constraint>Use compiler tools first: `comp-pipescript io <script>` before reading any gold script; `comp-trace` for upstream/downstream tracing on any column.</constraint>
    <constraint>NO code edits or pipeline reruns in Phase 0 — discovery only. Read-only S3 access + parquet inspection.</constraint>
    <constraint>If 49F reference snapshot is unobtainable, log the gap and proceed with what's available. Don't block on Andrew availability.</constraint>
    <constraint>Reference data lives at `s3://opal-data-bd/`. Do NOT cross-investigate into Inflection (`s3://opal-data-inf/`) — this is 49F-only scope.</constraint>
    <constraint>Standard pre-commit gate (CLAUDE.md Rule 14) applies if you author any Python helper scripts — though Phase 0 should not require any.</constraint>
  </constraints>

  <gates_and_dependencies>
    <gates>None.</gates>
    <unblocks>ADVI_49FRECN Phase 1+ remediation TOs (per finding).</unblocks>
    <coordination>If your findings overlap with Schwab TRN NNA enrichment Phase 6 C_01 (your in-flight scope), call out the overlap and propose merge vs. parallel.</coordination>
  </gates_and_dependencies>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>
      RAVC4 with: commit ref of the reconciliation report + 1-line per-AC PASS/findings + Phase 1 TO recommendations table.
    </on_complete>
  </ravc_target>

  <inputs>
    <input>Andrew directive 2026-05-01: 6025 vs 6611 accounts, 3.59% AUA undershoot</input>
    <input>ADVI_AUAVAR closeout 2026-03-09 (99.1% accuracy baseline)</input>
    <input>memory/project_schwab_trn_nna_enrichment.md</input>
    <input>org/projects/ADVI_49PUSH.json (closed 2026-04-11)</input>
    <input>compiler tool catalog: org/modules/graph/comp-tools.yaml</input>
  </inputs>
</task_order>
