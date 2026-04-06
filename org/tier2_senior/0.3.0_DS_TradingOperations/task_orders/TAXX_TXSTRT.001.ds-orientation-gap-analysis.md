<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-06-taxx-001-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.3.0_DS_TradingOperations</issued_to>
    <date>2026-04-06</date>
    <status>complete</status>
    <project_code>TAXX_TXSTRT</project_code>
  </metadata>

  <objective>
    Review the existing Tax SMA trade allocation system, understand every component,
    and produce a gap analysis identifying what needs to be built, hardened, or
    automated to make this production-ready within the workspace.
  </objective>

  <context>
    Andrew has been running a Tax SMA trade allocation process using a prototype
    Python script (`trade_allocator.py`, 1,632 lines). The entire system has been
    aggregated into `models/tax_strategy/` in the workspace. You have NO prior
    logs on this — this is your first exposure.

    **What exists:**

    1. `models/tax_strategy/trade_allocator.py` — Core allocation engine
       - Reads Axioma optimizer output (Excel workbooks per account)
       - Reads account manifest (Tax SMA Accounts.xlsx)
       - Reads Schwab SSAVAIL2.ASC (borrow availability)
       - Applies constraint cascade: excluded securities -> HTB validation ->
         max weight caps (1% long, -1% short) -> sector bands (net + long cap) ->
         round lots -> EMH balance (long/short gross within 2%)
       - Produces per-account: Schwab upload CSVs, full ledger CSVs, mutation
         ledger CSVs, event ledger CSVs, run reports, audit JSON, exec summary MD

    2. `models/tax_strategy/Tax SMA Accounts (1).xlsx` — Account manifest
       - 3 accounts: Chiles (SMA 200, $1M, 1x), Nixon (SMA 200, $750K, 1x),
         Bump (SMA 145, $1.95M, 0.45x)
       - Each has: advisor, account number, strategy, leverage, AUM, divest list

    3. `models/tax_strategy/output/` — Latest run outputs (2026-04-02)
       - 3x Schwab upload CSVs (account_number, side B/SS, shares, ticker)
       - 3x full ledger CSVs (ticker, side, sector, alpha, optimizer/final shares/weight, constraint chain)
       - 3x mutation ledger CSVs (per-constraint audit trail)
       - 3x event ledger CSVs
       - 3x run report CSVs
       - 5x executive summary MDs (multiple runs on 04-02)
       - audit_log.json

    4. `models/tax_strategy/Trade/` — Source data
       - `Trade 20260330/Acct-1.xlsx`, `Acct-2.xlsx`, `Acct-3.xlsx` (Axioma output)
       - `Trade 20260330/SSAVAIL2.ASC` (Schwab short sell availability)
       - `schwab upload template.csv` (upload format reference)
       - `SOD Shortsale avail File Layout.pdf` (SSAVAIL2 format documentation)

    **Strategies:**
    - SMA 200: 200% long target, 100% short target, 1x leverage. ~216 longs, ~195 shorts.
    - SMA 145: 145% long target, 45% short target, 0.45x leverage. ~163 longs, ~146 shorts.

    **Constraint cascade (in order):**
    3a: excludedSecurities (HARD) — remove divested + optimizer-excluded
    3b: htbValidate (HARD) — shorts must have borrow availability in SSAVAIL2
    3c: maxWeight (HARD) — no long > +1%, no short > -1%
    3d: sectorBand (SOFT/HARD) — net sector active +/- band, long sector cap
    3e: roundLot (HARD) — whole shares only
    3X: emhBand (HARD) — long vs short gross within 2% of each other
  </context>

  <scope>
    <files>
      <file action="read">models/tax_strategy/trade_allocator.py</file>
      <file action="read">models/tax_strategy/Tax SMA Accounts (1).xlsx</file>
      <file action="read">models/tax_strategy/output/ (all files)</file>
      <file action="read">models/tax_strategy/Trade/ (all files)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read and understand the entire trade_allocator.py. Document the full
      constraint cascade flow, data contracts (input/output schemas), and
      edge cases handled.
    </requirement>

    <requirement id="2">
      Review the latest run outputs. Understand the exec summary format,
      the ledger structure, the Schwab upload format. Identify any issues
      or anomalies in the 04-02 run (the Nixon account had cascade-introduced
      sector violations flagged for human review).
    </requirement>

    <requirement id="3">
      Produce a gap analysis covering:
      - What manual steps are currently required (e.g., getting Axioma files,
        running the script, uploading to Schwab)
      - What could be automated (data retrieval, execution, upload)
      - Code quality issues (error handling, edge cases, hardcoded values)
      - Missing features (e.g., historical run tracking, position reconciliation,
        P&L attribution, risk monitoring)
      - What infrastructure would be needed (S3, Lambda, EC2, portal pages)
    </requirement>

    <requirement id="4">
      Produce recommendations for Phase 1 scope — what is the minimum viable
      automation that makes this safer and more efficient to run daily/weekly.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Full understanding of trade_allocator.py documented in session log</criterion>
    <criterion id="2">Gap analysis delivered as structured document</criterion>
    <criterion id="3">Phase 1 recommendations with priority ordering</criterion>
  </acceptance_criteria>

  <deliverables>
    <deliverable type="log">Session log with codebase review notes</deliverable>
    <deliverable type="document">Gap analysis + Phase 1 recommendations</deliverable>
  </deliverables>
</task_order>
