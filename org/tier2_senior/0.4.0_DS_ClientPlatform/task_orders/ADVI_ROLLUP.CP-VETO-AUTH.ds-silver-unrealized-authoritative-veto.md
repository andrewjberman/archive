<task_order>
  <metadata>
    <id>ADVI_ROLLUP.CP-VETO-AUTH</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-17</date>
    <status>staged</status><!-- ON-CALL: Activate only if first clean CP-DS1 run shows >2% firm divergence vs silver/allocations. CTO adjudication 20260417T051141Z. -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P1 ON-CALL — ship if CP-DS1 first clean run firm AUA diverges >2%; otherwise deferred to hardening phase</priority>
  </metadata>

  <context>
    After CP-DS1 ships, ~472 accounts remain with zeroed positions in the gold output.
    These are Population A chronic accounts: BD-mapped, zero RPS rows (PCRA sleeve /
    SWTC / sub-master pattern), but WITH open positions in silver/unrealized.

    silver/unrealized is BD's own internal source of truth for currently-held open positions.
    If an account appears in silver/unrealized with open lots, those lots represent real positions
    that should flow through to the gold chain output.

    Currently dryrun_mode=True at B_01 L1832 correctly exempts these accounts from the force-close
    cohort (they don't trigger the halt). But their positions are NOT being emitted to the gold
    output because no RPS confirmation exists for them. Gap: ~472 accounts with open lots in
    silver/unrealized whose MV is absent from gold/holdings_lots.

    cec02a29 implemented an unrealized-authoritative veto "in theory" — this TO verifies it is
    complete, correct, and active for the 472 chronic-open-lots accounts.
  </context>

  <objective>
    Promote silver/unrealized as the authoritative open-positions source for accounts with
    ZERO RPS rows. For these accounts: if silver/unrealized shows open lots, emit them to
    gold/holdings_lots with is_open=True. Do not force-close them.

    Scope:
      1. Audit cec02a29 (unrealized-authoritative veto commit) — confirm it is active PROD code
         and correctly handles the 472 chronic-with-open-lots cohort.
      2. If incomplete or gated by a dryrun flag: promote to unconditional PROD path.
      3. Verify with single QA run: the 472 accounts' positions appear in gold output at their
         silver/unrealized MV (no longer zeroed).
      4. Verify Gate 2: (non-cash gold MV) + (cash MV from CP-WP5) within 2% of
         silver/allocations/2026-04-15 headline $1,694,648,746.
  </objective>

  <acceptance_criteria>
    1. 472 chronic-with-open-lots accounts emit open lot rows in gold/holdings_lots output.
    2. Their aggregate MV in gold output matches silver/unrealized MV for those accounts within 2%.
    3. No new force-closes triggered for these accounts on QA run.
    4. Gate 2: combined non-cash + cash gold MV within $1,660,755,771 – $1,728,541,721.
    5. comp-validate exits 0 on gold output.
    6. comp-pipescript deployed MATCH.
    7. MCP COMPLETE to COO with: 472-account MV recovered, Gate 2 recon figure, commit hash.
  </acceptance_criteria>

  <risk>
    If silver/unrealized is incomplete for sub-master accounts (missing some lots), promoted veto
    would under-report vs actual held positions. Validate silver/unrealized completeness for the
    472-account cohort before promoting. Flag to COO if coverage < 95%.
    Long-term structural fix: CP-MASTERFEED (AE, P2) — expand Schwab mapping so these accounts
    get their own RPS rows via proper sub-master feed. CP-VETO-AUTH is the bridge solution.
  </risk>

  <compiler_tools_mandate>
    Phase 1 (before write):
      comp-pipescript io B_01.holdings_lots.py — confirm silver/unrealized read path.
      comp-blast B_01 — confirm no new downstream breakage from veto path change.
    Phase 2 (before commit):
      python -m py_compile B_01.holdings_lots.py.
    Phase 3 (after QA run):
      comp-validate B_01 --artifact /tmp/holdings_lots_{date}.parquet — exit 0 required.
      comp-pipescript deployed B_01 — MATCH required.
  </compiler_tools_mandate>

  <dependencies>
    <dependency task="ADVI_ROLLUP.CP-DS1" status="staged"
      description="Gate 1 must be confirmed (halt clears) before promoting the veto path.
      CP-VETO-AUTH adds MV to accounts that previously had zeroed positions — must verify the halt
      is resolved first so we're not adding MV to accounts that would then trigger a re-halt."/>
  </dependencies>

  <next>
    CP-VETO-AUTH COMPLETE + CP-WP5 COMPLETE = Gate 2 achieved.
    Firm total_aua gold output matches silver/allocations within 2%.
    Andrew's "everything mapped" completion target satisfied.
    File ADVI_GLDOPS.CHRONIC-COHORT-AUDIT (P2) for long-term CP-MASTERFEED planning.
  </next>
</task_order>
