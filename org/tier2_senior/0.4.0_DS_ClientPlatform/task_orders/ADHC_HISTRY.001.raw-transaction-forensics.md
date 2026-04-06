<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-31-raw-transaction-forensics</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-31</date>
    <status>complete</status>
    <!-- Completed 2026-03-31. Commit 6e9715ca. 100% of $690M overshoot attributed: $513M missing sells, $177M vanished accounts. Dedup clean. Schwab crossref breakthrough (6,510 mappings). -->
  </metadata>

  <objective>
    Fundamental forensic investigation of the BD transaction data pipeline. The FIFO
    reconstruction produces $1.98B in holdings lots when BD reports $1.59B silver AUA --
    a $390M overshoot BEFORE any injection logic runs. Andrew suspects the foundation
    is broken: deduplication logic, transaction type classification, or ghost positions
    from corporate actions. This investigation must produce a root cause attribution
    before any further injection or overlay work proceeds.

    Preserve RC1 (NAME_ALIASES for DIVZ consolidation) -- it is committed and validated.
    Hold or revert all RC2-RC4 injection changes pending this investigation.
  </objective>

  <scope>
    <files>
      <file action="read">data/black_diamond/scripts/gold/02_build_positions_cube.py</file>
      <file action="read">data/black_diamond/scripts/gold/03_build_holdings_lots.py</file>
      <file action="read">data/black_diamond/scripts/bronze/</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      **Raw bronze audit.** Inventory all BD transaction files in S3. How many unique
      files? What date range? Are there gaps in the file delivery sequence? Do file counts
      match expected daily SFTP delivery cadence? Produce a timeline of file arrivals
      with row counts per file.
    </requirement>

    <requirement id="2">
      **Deduplication deep dive.** The 34% dedup rate (950K rows removed from 2.79M)
      needs full explanation. Document:
      - What columns are used as the dedup key in script 02?
      - What columns are used as the dedup key in script 03?
      - Do scripts 02 and 03 agree on dedup logic? If not, quantify the divergence.
      - Are there legitimate same-day same-asset transactions (e.g., multiple lot buys,
        partial fills, reinvested dividends) being incorrectly collapsed?
      - Sample 50 deduped rows and classify: true duplicate vs false positive.
    </requirement>

    <requirement id="3">
      **Transaction type classification audit.** How are corporate actions, transfers
      of assets, and passthroughs classified in the pipeline? Specifically:
      - Are transfers double-counted (both sides appearing as separate buy + sell)?
      - Are reinvested dividends inflating unit counts (counted as new buys without
        corresponding cash reduction)?
      - Are corporate actions (splits, mergers, spinoffs) correctly adjusting lot
        unit counts rather than creating new positions?
      - Produce a frequency table of all transaction_type values with row counts and
        total dollar impact.
    </requirement>

    <requirement id="4">
      **End-to-end trace for sample accounts.** Select 5-10 accounts spanning:
      - 2-3 Tier A (verified, healthy)
      - 2-3 Tier D (partial, moderate error)
      - 2-3 Tier F (suspect, large error)
      For each account, trace EVERY raw transaction record through dedup, classification,
      FIFO computation, and final position/lot. Identify the exact step where our
      reconstruction diverges from BD's unrealized report. Quantify the divergence per
      step (raw -> deduped -> classified -> FIFO -> final).
    </requirement>

    <requirement id="5">
      **Positions cube vs holdings lots reconciliation.** Script 02 and script 03 both
      read the same raw transactions. Why do they produce different AUA totals? The FIFO
      logic should yield identical unit counts. If they diverge, identify where and why.
    </requirement>

    <requirement id="6">
      **Root cause attribution.** Produce a table attributing the $390M overshoot to
      specific categories:
      - Dedup false positives (real transactions thrown out)
      - Dedup false negatives (duplicates kept, inflating units)
      - Transaction type misclassification (corporate actions counted as buys)
      - Transfer double-counting
      - Phantom positions (departed accounts, matured instruments)
      - Other
      Each category must have a dollar estimate and sample evidence.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Root cause attribution table with dollar estimates covering >= 80% of the $390M overshoot</criterion>
    <criterion id="2">Dedup logic fully documented with false positive rate estimated from 50-row sample</criterion>
    <criterion id="3">Transaction type frequency table with dollar impact per type</criterion>
    <criterion id="4">End-to-end trace for >= 5 accounts with per-step divergence quantified</criterion>
    <criterion id="5">02 vs 03 reconciliation showing where and why they diverge (if they do)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Preserve RC1 (NAME_ALIASES for DIVZ consolidation). Do not revert commit with DIVZ aliasing.</constraint>
    <constraint>Do NOT commit further injection changes (RC2-RC4) until this investigation completes.</constraint>
    <constraint>Work with 0.6.0_AE_PartnerETL for all EC2 execution and S3 data access. The c6i.16xlarge gold runner is available.</constraint>
    <constraint>This is an INVESTIGATION task order -- the deliverable is a diagnostic report with evidence, not code fixes. Code fixes come after root cause is understood.</constraint>
    <constraint>No emojis in any output per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="ec2-execution-support" status="complete">AE available for EC2/S3 support. c6i.16xlarge gold runner available.</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="document">Root cause attribution report covering >= 80% of $390M overshoot</deliverable>
    <deliverable type="document">Dedup logic documentation with false positive rate</deliverable>
    <deliverable type="document">Transaction type classification audit</deliverable>
    <deliverable type="document">End-to-end account trace (5-10 accounts)</deliverable>
    <deliverable type="document">02 vs 03 reconciliation analysis</deliverable>
  </deliverables>
</task_order>
