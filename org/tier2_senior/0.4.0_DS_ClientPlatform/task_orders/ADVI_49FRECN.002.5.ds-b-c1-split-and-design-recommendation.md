<task_order>
  <metadata>
    <id>ADVI_49FRECN.002.5</id>
    <project>ADVI_49FRECN</project>
    <title>Phase 1.5 Sub-Investigation — Split C1 (60 accts/$55M) + Custodian Source-of-Truth + Track 2 Design Pick</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>complete</status>
    <priority>P0 — gates Track 2 fix design (the 77% AUA lever)</priority>
    <estimated_effort>1d (sub-investigation + design recommendation; no code changes)</estimated_effort>
  </metadata>

  <context>
    Phase 0 identified Bucket C1: 60 investment accounts, ~$55M AUA, created 2025-2026, missing
    from C_03 because the positions cube has no positions for them today. This is 77% of the
    $71.3M total AUA gap — the primary lever.

    Andrew's design ruling 2026-05-01:

      "The question then becomes the accounts that DO have transactions but we probably closed
       out via FIFO lots or whatever, that will require being more clever and we need to discuss
       exactly how we'd accomplish that."

    Before Track 2 fix design (Option A allocation-as-fallback / Option B parallel path / Option C
    time-window inclusion), CTO needs a data-driven split of C1 into two sub-buckets and answers
    to two business-rule questions. This TO is that sub-investigation.

    You (DS~B) own this — you have the C1 account-id list from .001B and the deepest context
    on the missing-account trace.
  </context>

  <objective>
    (1) Split the 60 C1 accounts into C1a (genuinely closed, fully liquidated) vs C1b (allocation
    AUA exists but no positions because rollover-in-flight or cash-only).
    (2) Investigate custodian source-of-truth: when an account is "fully sold off," does BD's
    bronze feed still report a balance? If yes, why isn't our positions cube capturing it?
    (3) Survey the data to inform Andrew's business-rule answer on what 49F means by "in book."
    (4) Recommend Track 2 fix design (Option A / B / C from CTO's discussion) with empirical justification.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Split C1 into C1a vs C1b</title>
      <detail>
        For each of the 60 C1 accounts, classify:
        - **C1a — Genuinely closed:** all positions sold, account zeroed out, custodian still
          listing it for X days post-close. Look for: zero positions today AND zero allocation
          AUA AND last transaction was a sell-off / liquidation.
        - **C1b — Allocation AUA exists but no positions:** allocation feed shows non-zero AUA
          but positions cube has zero positions. Cash-only or rollover-in-flight cases.

        Per-account table: account_id, advisor, account_type, allocation_aua, last_position_date,
        last_transaction_type, last_transaction_date, classification (C1a / C1b / UNCLEAR).

        Tabulate: how many of each? What's the AUA breakdown by sub-bucket?
      </detail>
    </ac>

    <ac id="2">
      <title>Custodian source-of-truth check</title>
      <detail>
        For a sample of 5 C1a (genuinely closed) and 5 C1b (allocation-only) accounts, trace upstream:
        - Does BD bronze (`s3://opal-data-bd/bronze/...`) carry a current balance for these accounts?
        - If yes — what's the balance and where is it stored (positions feed? cash feed? other)?
          And why isn't our silver positions cube picking it up?
        - If no — BD literally isn't reporting a balance, but 49F is showing AUA. Where is 49F
          getting their number from? (Allocation feed? Their own internal book-keeping? Custodian
          direct that doesn't flow through BD?)

        Output: a 10-account trace table that pinpoints WHERE the divergence between BD bronze
        and 49F's display lives.
      </detail>
    </ac>

    <ac id="3">
      <title>Survey data for Andrew's "in book" definition</title>
      <detail>
        Andrew owes an answer to the question "what does 49F mean by 6,611 accounts" — but our
        data can survey what's plausible:
        - How many accounts have non-zero balance today (any source)?
        - How many were active in the last 30/60/90/180/365 days?
        - How many are in the CRM-equivalent allocation feed regardless of activity?

        Tabulate and recommend which definition matches 6,611. This narrows Andrew's decision space.
      </detail>
    </ac>

    <ac id="4">
      <title>Track 2 fix design recommendation</title>
      <detail>
        Three design options on the table from CTO's discussion:

        - **Option A — Allocation-as-fallback in C_03:** when account has allocation_AUA but no
          positions, materialize a synthetic cash-equivalent position equal to the allocation AUA.
          Account flows through C_03 normally. Pro: simplest. Con: synthesizes data.
        - **Option B — Separate path for allocation-AUA accounts:** keep C_03 strict; add C_03b
          or D_04 extension that processes allocation-only accounts and emits performance metrics
          from allocation feed. Two streams converge in downstream merge. Pro: clean separation.
          Con: more pipeline surface.
        - **Option C — Time-window inclusion:** include accounts in C_03 if they had positions
          within last N days. Pro: matches 49F probable behavior. Con: arbitrary N; cliff edge.

        Based on findings from #1, #2, #3, recommend ONE option (or a hybrid) with empirical
        justification. If a 4th option emerges from your investigation, propose it.

        Specifically address: how does each option handle C1a vs C1b differently? Is one option
        better for one sub-bucket and another for the other?
      </detail>
    </ac>

    <ac id="5">
      <title>Open questions to escalate to Andrew</title>
      <detail>
        If your investigation surfaces business-rule questions Andrew needs to answer before
        the Track 2 fix can be authored, list them explicitly with the data context that makes
        the question concrete. (E.g., "Of the 12 C1a accounts, all have last sell within 30
        days — should accounts in this 0-30 day post-liquidation window be included? If so,
        Option C with N=30 is the cleanest; if not, Option B routes them out-of-scope.")
      </detail>
    </ac>

    <ac id="6">
      <title>Deliverable</title>
      <detail>
        Append a new section to `docs/architecture/49F_RECONCILIATION_2026-05-01.md`:
        `## Phase 1.5 Sub-Investigation — C1 Split + Track 2 Design (DS~B)`

        Include:
        - C1a / C1b classification table (60 accounts)
        - Custodian source-of-truth trace (10 accounts)
        - "In book" definition data survey
        - Track 2 design recommendation with empirical justification
        - Open questions to Andrew

        Doc lane = ANY_CTO; commit via CTO same pattern as Phase 0 (`21e65922d`).

        RAVC4 to CTO with executive summary + design recommendation. CTO authors the actual
        Track 2 fix TO based on your recommendation + Andrew's business-rule answers.
      </detail>
    </ac>
  </acceptance_criteria>

  <constraints>
    <constraint>Investigation only — no code changes, no pipeline reruns. Read-only S3 + parquet.</constraint>
    <constraint>49F-only scope.</constraint>
    <constraint>Compiler tools first: `comp-pipescript io <script>` + `comp-trace` for upstream tracing.</constraint>
    <constraint>Pre-commit gate (CLAUDE.md Rule 14) on any Python helper for analysis.</constraint>
  </constraints>

  <gates_and_dependencies>
    <gates>None — runs in parallel with .002 D_04 extension.</gates>
    <unblocks>Track 2 fix TO (CTO authors after this RAVC4 + Andrew's business-rule answers).</unblocks>
    <related>.002 (DS~A — Track 1 D_04 out-of-scope JSON for buckets A+B+C2/C3) runs in parallel.</related>
  </gates_and_dependencies>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 with: commit ref to recon doc append + executive summary copied into the message body + Track 2 design recommendation + open questions for Andrew.</on_complete>
  </ravc_target>

  <inputs>
    <input>docs/architecture/49F_RECONCILIATION_2026-05-01.md (Slice B — your own C1 bucket from .001B)</input>
    <input>Your .001B session log (account-id list for C1)</input>
    <input>CTO design discussion 2026-05-01 (Option A/B/C from conversation)</input>
    <input>Andrew design directive 2026-05-01 ("more clever and we need to discuss")</input>
  </inputs>
</task_order>
