<task_order>
  <metadata>
    <id>ADVI_ROLLUP.D02-T2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to><!-- self-authored + executed per COO 2026-04-15T22:18:47Z GO ("GO NOW: author + execute") -->
    <date>2026-04-16</date>
    <status>complete</status><!-- COMPLETE 2026-04-16 08:50 ET (~B). Path (b) — NO BUG. All 7 zero-current-activity advisors reconcile exactly at platinum/advisors/{slug}/summary.json: book.tagged_aua == sum(role_breakdown.*.aua) within $0.01, book.account_count == sum(role_breakdown.*.account_count) exactly. ~C's reported inconsistency (summary.tagged_aua=$0) was null-as-zero conflation — platinum has no top-level .summary key; only .book. Gold upstream D_02 book.json's .summary.tagged_aua populated correctly. Doc-only close; no D_02/D_04 code change. Session log: logs/2026-04-16/d02_t2_zero_activity_advisor_reconciliation.md. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>3 (Frontend correctness — D_02 producer triage)</wave>
    <priority>P3 (user-facing snapshot contradiction risk if real; no consumer breakage confirmed)</priority>
    <slug_note>Slug uses D02-T2 per COO's suggested convention (D_02 is the producer of `platinum/advisors/{id}/summary.json` via build_advisor_books). T2 follows T1 = D00c leaderboard count reconciliation (parallel triage pair, same 7 zero-current-activity advisor cohort).</slug_note>
  </metadata>

  <references>
    <ref type="trigger">~C D00c-T1 side finding (commit 7ea091cb, session log d00c_t1_leaderboard_advisor_count_reconciliation.md lines 57-64). ~C spot-checked andrew_rose / austin_bost / connor_haney summary.json and claimed `summary.tagged_aua=$0 + summary.account_count=0` but `role_breakdown.{role}.aua != $0`. Called "likely cause: snap_latest non-empty with $0-AUA accounts, or role_breakdown takes a different code path."</ref>
    <ref type="related">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ROLLUP.D00c-T1.ds-leaderboard-advisor-count-reconciliation.md (path b doc-only ship)</ref>
    <ref type="related">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_ROLLUP.D01-T1.ds-d01-geo-aua-snapshot-gap-triage.md (same shape — verify, decide path, ship)</ref>
    <ref type="cto-ack">org/mcp/inbox/0.4.0_DS_ClientPlatform/read/20260415T221412Z_1.0.0_SA_CTO_CLOSE___D00c-T1_ACCEPT__7ea091cb___austi.md — "austin_bost side finding surfaced to COO for a separate ADVI triage TO. Your diagnostic framing (snap_latest non-empty with $0 AUA OR role_breakdown takes different code path) is exactly the right starting hypothesis."</ref>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md</ref>
  </references>

  <objective>
    ~C's D00c-T1 side finding: 7 zero-current-activity advisors (andrew_rose, austin_bost, connor_haney, justin_jones, logan_tingley, nathan_grande, presley_lawson) allegedly show `summary.tagged_aua=$0 + summary.account_count=0` on `platinum/advisors/{slug}/summary.json` while their `role_breakdown.{role}.aua` is non-zero (e.g. austin_bost implementor.aua = $3,321,857.57 / 12 accounts).

    Verify whether this is:
    - **(a) Bug** — D_02 `build_advisor_books` emits inconsistent tagged_aua vs role_breakdown for zero-current-activity advisors; patch so `book.tagged_aua == sum(role_breakdown[*].aua)` holds universally.
    - **(b) Deliberate or false alarm** — producer is already consistent; the reported gap is a field-naming confusion, documentation artifact, or upstream stale artifact. Document the correct contract + close.
  </objective>

  <scope>
    <files>
      <file action="modify_or_document">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py (modify if path a) OR session log + inline contract note (path b)</file>
    </files>
  </scope>

  <wire_contract>
    Invariant: for every advisor_id in `platinum/advisors/{id}/summary.json`,
    `book.tagged_aua == sum(role_breakdown[role].aua for role in {architect, implementor, consultant, local_ops, additional_advisor})` within $0.01, AND
    `book.account_count == sum(role_breakdown[role].account_count)` exactly (or documented dedupe semantics — role_breakdown may count overlaps differently from book level).
  </wire_contract>

  <acceptance_criteria>
    1. Hypothesis verified or rejected against ALL 7 zero-current-activity advisors with a reconciliation table (book.tagged_aua vs sum-of-role-breakdown-aua; same for account_count).
    2. Path chosen (a bug vs b deliberate/false-alarm) in commit body / TO closeout with quantitative evidence.
    3. If (a): D_02 patched, S3 uploaded, post-nightly verification with reconciliation table rerun.
    4. If (b): inline contract note in session log + (if warranted) eligibility-criteria doc updated. FE (DE) notified if field-naming or structure contract needs clarification.
    5. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE to COO with chosen path + reconciliation table + outcome.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>READS visible (account_performance, account_team, advisor_fee_detail, role_aua post-RA-P1 shadow); WRITES platinum/advisors/{slug}/summary.json; confirm `book.tagged_aua` + `role_breakdown` emit sites.</expect>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-bd/platinum/advisors/{slug}/summary.json for all 7 candidates + current austin_bost control</run>
        <expect>Snapshot book.{total_aua, tagged_aua, account_count} + role_breakdown.*.{aua, account_count} for each. Reconcile.</expect>
      </step>
      <step>
        <run>grep -nE "tagged_aua|role_breakdown" D_02.advisor_client_detail.py</run>
        <expect>Identify emit sites; confirm single vs dual code path; verify snap_latest vs role_aua basis per ~C hypothesis.</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile D_02.advisor_client_detail.py (only if path a)</run>
        <expect>Exit 0.</expect>
      </step>
      <step>
        <run>Reconciliation table (book vs sum-role) — re-run after patch (path a) or once-final (path b)</run>
        <expect>Path (a): all 7 reconcile within $0.01. Path (b): table documents current reconciliation as-is.</expect>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>{path a only: post-nightly D_02 run + re-fetch 7 summary.json; sum role_breakdown vs book.tagged_aua}</run>
        <expect>All 7 within $0.01.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/><!-- D_02 is in flight with my own B3.fix (L358 loader + L2272 WARN-LOUD), ~D's CN-P2 (NNA atomic reader), and RA-P2 (role_aua shadow writer). If path a requires D_02 edit, coordinate with ~D before commit. Path b shouldn't require code edit. -->
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    If path (a), follow-up: verify FE consumer `AdvisorBookView` renders tagged_aua correctly from the post-fix artifact. If path (b), close with doc note; no follow-up expected.
  </next>
</task_order>
