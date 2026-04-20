<task_order>
  <metadata>
    <id>ADVI_STAUDT.INV1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-04-20</date>
    <status>draft</status>
    <project_code>ADVI_STAUDT</project_code>
    <priority>P1 — unblocks FIX-TO 4 scope decision. Pure diagnostic, no fixes. Target ~2-4 hour turnaround.</priority>
    <kind>INVESTIGATION — S3 reconstruction + integrity check. NO fixes authored under this TO.</kind>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_STAUDT.md §3.0 (Class 1 NNA definition change)</ref>
    <ref type="handoff">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md</ref>
    <ref type="attribution">data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md (c2e723f7 — Step 2 RETRACTED; see CORRECTION NOTICE)</ref>
    <ref type="ds-retraction-mcp">~D to COO 20260420T140305Z — "Step 2 of historical NNA causal stack has been retracted and corrected at c2e723f7"</ref>
    <ref type="cto-routing">CTO to COO 20260420T140816Z — INV1 authorization + query spec</ref>
    <ref type="andrew-observation">Historical NNA explosion: portal shows $100M+ NNA for advisors over 2020-2022 when AUA stock was only $50-100M. Stock/flow violation — cumulative net flows cannot sustainably exceed the asset base.</ref>
  </references>

  <background>
    ~D originally attributed the historical-NNA inflation to phantom-outflow resets baked into `gold/canonical/nna_atomic/` via the CN-P1b backfill (Step 2 of the causal stack). Upon CTO source review and ~D re-verification, Step 2 was RETRACTED at commit `c2e723f7`: `nna_atomic/` is built by C_01's shadow writer from `silver/transactions` daily values, NOT from `account_performance.parquet`. The phantom-outflow-in-account_performance bug therefore does NOT propagate into `nna_atomic/` via that path.

    Three open candidates remain for the historical-NNA inflation mechanism (per ~D's CORRECTION NOTICE):
    - **(a) silver/transactions inflation:** the raw transactions ledger itself contains inflated or duplicate flows in 2020-2022 (ETL artifact, double-classification, synthetic fills)
    - **(b) apples-to-oranges comparison:** the portal figure Andrew observed is being compared to the wrong AUA denominator; the "$50-100M AUA" stock is e.g. a single-advisor slice while the "$100M+ NNA" is a multi-advisor aggregate; no actual inflation
    - **(c) already-resolved at T3:** the inflation existed historically (via the retracted pre-c2e723f7 path) but has already been corrected by the C_03 phantom fix (85bb2daa) + CN-P1b re-runs + the Apr-17 hotfixes; T3 production figures are clean; Andrew observed pre-T3 state

    Without S3 data reconstruction, no further progress. AE has SSM + production S3 access; ~D does not.

    FIX-TO 4 (role_aua/ refresh) is BLOCKED on this investigation — its scope depends on which candidate is true.
  </background>

  <objective>
    Run three targeted S3 + silver reconstructions to determine which of (a)/(b)/(c) is actually responsible for the 2020-2022 portal NNA reading of $100M+ against $50-100M AUA stock. Deliver a single decision document telling CTO + COO which candidate is ruled in and which are ruled out. No code changes, no fix attempts under this TO — pure diagnostic.
  </objective>

  <scope>

    ### Query 1 — nna_atomic/ daily sum reconstruction

    For a primary target advisor (start with **Travis Penfield** — the advisor cited in ~D's Bug 1 + Bug 2 evidence with concrete figures) and 2-3 cross-check advisors (suggest: one with confirmed mid-2020s AUA of $50-100M, one with AUA in $200-500M range, one smaller):

    1. Enumerate the advisor's account set from `gold/dimensions/advisor_assignments_history.parquet` for the 2020-2022 window
    2. For each account in the set, sum `daily_inflow - daily_outflow` (or equivalent NNA-forming fields in `nna_atomic/`) across all `gold/canonical/nna_atomic/YYYY-MM-DD.parquet` partitions in 2020-01-01 through 2022-12-31
    3. Report the cumulative sum per advisor (the "historical NNA total" per the production figure)
    4. Report the same advisor's end-2022 `tagged_aua` stock (from `gold/dimensions/client_dimension.parquet` or the relevant 2022-12-31 gold partition)
    5. Delta = reproduction of Andrew's original observation (or not). If the sum is $100M+ against $50-100M AUA, the inflation IS present in the canonical data at T3. If the sum is reasonable, the issue is elsewhere (candidate b or c).

    **Output format (per advisor):**
    ```
    advisor: Travis Penfield
    account_count: <N>
    2020-2022 cumulative NNA from nna_atomic/ daily sum: $<X>M
    2022-12-31 tagged_aua stock: $<Y>M
    ratio (NNA / AUA): <r>
    violation (NNA >> AUA stock?): YES / NO
    ```

    ### Query 2 — silver/transactions integrity check

    For the same primary target advisor (Travis Penfield) across 2020-01-01 through 2022-12-31:

    1. Pull all silver/transactions rows for the advisor's account set for the window
    2. Aggregate transaction count per month (36 months)
    3. Identify anomaly months: transaction count > 2× the median month OR transaction count > 2× the prior/following month
    4. For any anomaly month found, dump the raw transaction rows for that month and characterize:
       - Are there duplicate transactions (same account, date, amount, classification appearing multiple times)?
       - Are there suspicious classifications (e.g., a single month with huge synthetic "inflow" or "outflow" rows matching an ETL backfill pattern)?
       - Are there transactions with null or wrong source fields (indicating synthetic fill)?
    5. Report: per-month count table + per-anomaly-month raw dump + characterization paragraph

    **Confirms candidate (a) — silver/transactions inflation — if anomaly months contain duplicate/synthetic rows.**

    ### Query 3 — T3 re-verification against production book.json

    1. Pull the current-T3 production `book.json` (or equivalent D_02 output) for Travis Penfield
    2. Extract the NNA values reported for any 2020-2022 window currently visible in the portal
    3. Confirm or deny: does the T3 production artifact still show the $100M+ historical NNA that Andrew originally observed? Or has it since self-corrected (via 85bb2daa phantom fix + any subsequent re-runs)?

    **Confirms candidate (c) — already-resolved-at-T3 — if the T3 artifact no longer shows inflation.**

    ### Synthesis

    Write a single `historical_nna_mechanism.md` decision document that:
    - Reports each query's raw numeric output
    - Rules in exactly one candidate ((a), (b), or (c)) OR reports that none of the three fits and additional investigation is needed
    - If candidate (a): characterize the silver/transactions inflation pattern sufficient for CTO + COO to scope the fix (is it a specific month? a classification? an ingestion run?)
    - If candidate (b): identify the apples-to-oranges mismatch in the portal rendering or Andrew's observation source
    - If candidate (c): confirm T3 is clean and no production fix is needed for the historical NNA (role_aua/ hygiene under FIX-TO 4 still stands, but reframes as data-hygiene not production-blocker)

    **OUT OF SCOPE:**
    - No code changes (no scripts, no Terraform, no S3 writes)
    - No fix attempts under this TO
    - No investigation beyond the three named queries — if a fourth candidate emerges, document it in the decision doc and escalate, but do not pursue it under INV1
    - No changes to `gold/canonical/nna_atomic/` partitions, no re-backfills
    - NNA universe Option B scoping (the 376-account shadow-writer asymmetry) is a separate follow-up — flag if you notice related anomalies but do not investigate here
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="pre-query diligence">
      <step>
        <run>comp-pipescript io C_01.canonical_nna</run>
        <expect>Column-load manifest for C_01 — confirms which silver/transactions columns feed nna_atomic/. Use this to write Query 1 + Query 2 correctly.</expect>
        <if_mismatch>Any unexpected column gap = flag to COO before running queries.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://&lt;gold-bucket&gt;/gold/canonical/nna_atomic/ | head -5 ; aws s3 ls s3://&lt;gold-bucket&gt;/gold/canonical/nna_atomic/ | tail -5</run>
        <expect>Confirm nna_atomic/ partitions actually span 2020-2022 (not just 2023+). If partitions only start from 2023, the historical window isn't in nna_atomic/ — reshape Query 1 against whichever partition carries the 2020-2022 window.</expect>
        <if_mismatch>If 2020-2022 partitions are missing in nna_atomic/, MCP COO — this changes Query 1's premise.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="per-query execution">
      <step>
        <run>Query 1 execution on bd-gold-qa-runner (NOT bd-gold-layer-runner per `feedback_prod_runner_eventbridge_only.md`)</run>
        <expect>Pandas/pyarrow script pulls partitions via s3fs or boto3, aggregates, writes output to local tmp + uploads artifact to diagnostics/STAUDT/INV1/.</expect>
        <if_mismatch>Any partition read failure = document + proceed with partial coverage; note gaps in decision doc.</if_mismatch>
      </step>
      <step>
        <run>Query 2 execution on same runner</run>
        <expect>Per-month transaction count + anomaly-month raw dumps.</expect>
        <if_mismatch>If silver/transactions is missing for 2020-2022 window entirely, that itself is a finding — document and raise.</if_mismatch>
      </step>
      <step>
        <run>Query 3: pull T3 book.json from `gold/portal/books/` (or wherever D_02 writes)</run>
        <expect>Current production book.json for Travis Penfield. Extract 2020-2022 NNA fields.</expect>
        <if_mismatch>If book.json doesn't contain 2020-2022 windows, reshape against the leaderboard or another D-script output that does.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="synthesis + handoff">
      <step>
        <run>Write historical_nna_mechanism.md with raw query outputs + candidate ruling</run>
        <expect>Single file, ~2-3 pages, concludes with a one-paragraph ruling: candidate (a), (b), (c), or "none of the above, further investigation required".</expect>
        <if_mismatch>If the three queries together don't rule in any candidate, document what additional query would be needed and MCP CTO + COO for scope expansion.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <deliverables>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/INV1/historical_nna_mechanism.md</path>
      <description>Decision document. Must include: query outputs, candidate ruling, recommendations to CTO + COO for FIX-TO 4 scoping.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/INV1/query1_nna_reconstruction.json</path>
      <description>Per-advisor cumulative NNA + tagged_aua stock + ratio, for Travis Penfield + 2-3 cross-check advisors.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/INV1/query2_silver_tx_anomaly.json</path>
      <description>Per-month transaction count table + per-anomaly-month raw row dumps.</description>
    </deliverable>
    <deliverable>
      <path>data/black_diamond/diagnostics/STAUDT/INV1/query3_t3_book_nna.json</path>
      <description>Current T3 production book.json NNA values for 2020-2022 windows for primary target advisor.</description>
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    - [ ] All three queries run against live production S3 (not local samples)
    - [ ] Query 1 covers Travis Penfield + ≥2 cross-check advisors with varying AUA magnitudes
    - [ ] Query 2 anomaly detection uses explicit threshold (2× median OR 2× neighbors) and documents any anomaly months with raw-row characterization
    - [ ] Query 3 uses a T3-current production artifact (not stale)
    - [ ] Decision document rules in exactly one candidate (or reports "further investigation needed" with specific next query)
    - [ ] Decision document recommends FIX-TO 4 scoping implication (does role_aua/ refresh alone close the historical-NNA gap, or is additional work needed?)
    - [ ] No S3 writes to gold/canonical/ (pure read)
    - [ ] No silver/ modifications
    - [ ] No code deployed
  </acceptance_criteria>

  <guardrails>
    - **Pure diagnostic:** zero S3 writes to canonical paths, zero silver/ modifications, zero deployed code. Any hypothesis → document, do NOT patch.
    - **QA runner only:** `feedback_prod_runner_eventbridge_only.md` — bd-gold-layer-runner is EventBridge-only PROD; use bd-gold-qa-runner (i-0090b823a4a0997e3) for all INV1 queries.
    - **Single command discipline:** per `feedback_ec2_single_command.md`, no overlapping SSM commands.
    - **S3 code deployment standard:** per `feedback_no_direct_ds_messages.md`'s deployment analogs, if you need to run diagnostic scripts on EC2, follow `docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md` — write locally → upload to S3 → EC2 pulls → execute. No inlined SSM Python.
    - **No emojis in code** (CLAUDE.md #13).
    - **No scope creep:** three named queries + synthesis. If a fourth candidate emerges during Query 1 or 2, document and escalate — do not pursue.
    - **Agent commit identity:** `git commit --only --author="0.6.0_AE_PartnerETL &lt;0.6.0_AE_PartnerETL@opal.agent&gt;" -- &lt;paths&gt;`
  </guardrails>

  <agent_context_setup>
    1. Register with MCP: `register_agent 0.6.0_AE_PartnerETL`
    2. Launch `bash org/mcp/inbox-watch.sh 0.6.0_AE_PartnerETL` in background
    3. Read in order:
       - docs/architecture/ADVI_STAUDT.md §3.0
       - data/black_diamond/diagnostics/STAUDT/SYNTHESIS/bug_attribution.md (specifically the CORRECTION NOTICE in the HEADLINE section)
       - data/black_diamond/diagnostics/STAUDT/SYNTHESIS/coo_handoff.md §FIX-TO 4 (the role_aua/ context)
       - data/black_diamond/scripts/gold/C_01.canonical_nna.py (understand how nna_atomic/ is built, particularly the shadow writer path)
       - data/black_diamond/scripts/gold/lib/s3_layout.py (canonical paths)
       - docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md (S3 artifact model for any scripts you deploy)
    4. Heartbeat every 60s during active work
  </agent_context_setup>

  <completion_protocol>
    - RAVC step 1 (Acknowledge): within 5 min of receipt, MCP COO with "ACK STAUDT.INV1 — starting Phase 0 diligence"
    - Phase 0 gate: MCP COO with comp-pipescript + S3 partition-span findings before running Query 1
    - Mid-flight: MCP COO after each query completes with the numeric headline (don't wait for full synthesis)
    - RAVC step 4 (Close): MCP COO with commit SHA of historical_nna_mechanism.md + the candidate ruling (a/b/c/none)
  </completion_protocol>
</task_order>
