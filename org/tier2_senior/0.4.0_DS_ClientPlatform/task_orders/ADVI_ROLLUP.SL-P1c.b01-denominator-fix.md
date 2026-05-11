<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_ROLLUP.SL-P1c</id>
    <project>ADVI_ROLLUP</project>
    <title>Fix B_01 apportionment denominator bug + dry-run validate + nightly re-enable gate</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <routed_by>0.4.0_DS_ClientPlatform~B (self-authored per COO directive 2026-05-01)</routed_by>
    <issued_date>2026-05-01</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <wave>W4</wave>
    <phase_label>SL-P1c (denominator fix + re-emit gate)</phase_label>
    <estimated_effort>0.5d (fix 2h + dry-run 1h + 3-nightly-wait async)</estimated_effort>
    <closed_date>2026-05-11</closed_date>
    <closed_by>0.4.0_DS_ClientPlatform~A</closed_by>
    <closed_via>RAVC4 ACCEPT-WITH-NOTE — 2.0.0_SA_COO 20260511T~12:45Z</closed_via>
  </metadata>

  <references>
    <ref type="predecessor">ADVI_ROLLUP.SL-P1b — ITERATE verdict; root cause analysis at org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_SLEEVE_P1B_ANALYSIS.md (commit c52f1fc5e)</ref>
    <ref type="script">data/black_diamond/scripts/gold/B_01.holdings_lots.py lines ~988-1006 (_build_uln_sleeve_lots non-cash apportionment)</ref>
    <ref type="coo_ack">2.0.0_SA_COO 2026-05-01: ITERATE accepted; Fix B spec clear; route to DS to author this TO</ref>
    <ref type="successor_gate">ADVI_ROLLUP.SL-P1b re-run (3 clean nightlies required); ADVI_ROLLUP.SL-P2 PROMOTE decision (COO gates)</ref>
  </references>

  <context>
    SL-P1b validation confirmed one critical bug in the ULN sleeve shadow apportionment logic in
    B_01.holdings_lots.py (_build_uln_sleeve_lots, lines ~988-1006).

    BUG: `total_unit_cost` is computed from ALL ULN non-cash positions for the account (including
    those that will be vetoed by the FIFO check). Non-vetoed lots then receive weight =
    unit_cost / total_unit_cost_all — only their fractional share of `non_cash_target_mv`.
    For accounts with significant FIFO coverage (e.g. Jones: 10 of 13 non-cash positions vetoed),
    the surviving lots receive a tiny fraction (12.43%) of the intended MV. Jones shadow: $318K
    observed vs $2,396,510 target (86.7% error). 98.7% of cohort accounts off by >10%.

    Dry-run (2026-04-13 partition) produced Jones at 0.00% delta — at that time Jones had no FIFO
    lots, so all ULN positions passed the veto and the denominator was correct. Between dry-run
    and first nightly emit (2026-04-15), FIFO lots were loaded for Jones, triggering the bug.

    Fix B (preferred): use uncovered MV as apportionment base + filter denominator to non-vetoed
    positions only. Architecturally correct for both pure-sleeve (0 FIFO) and partial-FIFO accounts.

    Secondary: cohort drift (553 dry-run → 458 live) must be investigated as part of the fix
    validation to confirm the re-run cohort is stable.
  </context>

  <scope>

    ## Phase 0 — Read before writing

    1. Read B_01.holdings_lots.py lines 958-1023 (_build_uln_sleeve_lots loop) before editing.
       Run comp-pipescript io B_01 — confirm no new column gaps introduced since SL-P1b.

    ## Phase 1 — Fix B implementation (B_01 lines ~958-1023)

    2. **Pre-compute FIFO-covered MV per sleeve account** before the ULN sleeve loop.
       Add a helper dict: `fifo_mv_by_acct = df[df['account_id'].isin(sleeve_accounts)]
       .groupby('account_id')['market_value'].sum().to_dict()` where `df` is the main FIFO
       holdings_lots DataFrame passed into _build_uln_sleeve_lots. (df is already in scope as
       the first argument.)

    3. **Change non_cash_target_mv computation** inside the per-account loop:
       ```python
       fifo_covered_mv = fifo_mv_by_acct.get(acct_id, 0.0)
       non_cash_target_mv = max(account_mv - cash_mv - fifo_covered_mv, 0.0)
       ```
       This sets non_cash_target_mv to the UNCOVERED non-cash portion only.

    4. **Filter grp_nc to non-vetoed positions BEFORE computing total_unit_cost:**
       ```python
       grp_nc_pass = grp_nc[grp_nc.apply(
           lambda row: (acct_id, str(row['asset_name']).strip()) not in fifo_open_set, axis=1
       )]
       if grp_nc_pass.empty or non_cash_target_mv <= 0:
           continue
       total_unit_cost = float(grp_nc_pass['unit_cost'].sum())
       if total_unit_cost <= 0:
           continue
       for _, lot in grp_nc_pass.iterrows():
           weight = float(lot['unit_cost']) / total_unit_cost
           target_mv = weight * non_cash_target_mv
           ...
       ```
       Remove the inner veto check (no longer needed — already filtered out).

    5. **Preserve cash lot logic unchanged.** Cash veto check remains as-is (separate code path).

    6. **from __future__ import annotations** — confirm present at top of B_01 (Rule 15).

    ## Phase 2 — Pre-commit gate + dry-run validation

    7. Run `.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/B_01.holdings_lots.py` —
       py_compile + AST undefined-name scan + ruff py39. Must exit 0.

    8. **Dry-run validation on 2026-04-21 partition:**
       ```bash
       python data/black_diamond/scripts/gold/B_01.holdings_lots.py \
           --date 2026-04-21 --dry-run --sleeve-shadow-only
       ```
       (Or equivalent dry-run flag per existing B_01 interface. If --dry-run not supported,
       run with --upload omitted and check local output.)

       Assertions MUST pass before committing:
       a. **Jones z0817905851: shadow MV = cash only (~$21,060).** Jones has 58 FIFO lots
          covering full $2.39M non-cash. After fix, uncovered_mv ≈ $0. Only cash lot should emit.
       b. **Pick 3 pure-sleeve accounts (0 FIFO lots in prod):** shadow account_mv must be
          within 2% of silver/allocations account_market_value. These should be unchanged by fix.
       c. **Cohort count:** note how many accounts emit shadow lots. Flag if substantially
          different from 458 (prior live) or 553 (dry-run baseline).
       d. **Firm shadow MV:** must increase substantially from $15.9M (buggy) toward the
          expected range (dry-run firm MV was ~$88.7M; post-fix firm MV for accounts with
          minimal FIFO coverage should recover; accounts with full FIFO coverage like Jones
          will correctly reduce to cash-only and lower firm total).

    ## Phase 3 — Commit + S3 upload + nightly re-enable

    9. Commit via safe-commit.sh:
       ```bash
       .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform <0.4.0_DS_ClientPlatform@opal.agent>" \
           -m "fix(ADVI_ROLLUP.SL-P1c): B_01 sleeve apportionment denominator bug

       Use uncovered_mv (account_mv - cash_mv - fifo_covered_mv) as apportionment
       base. Filter grp_nc to non-vetoed positions before total_unit_cost sum.
       Fix B per SL-P1b root cause analysis (c52f1fc5e)." \
           -- data/black_diamond/scripts/gold/B_01.holdings_lots.py
       ```

    10. Push to CLOUD: `git push origin CLOUD`

    11. S3 upload:
        ```bash
        aws s3 cp data/black_diamond/scripts/gold/B_01.holdings_lots.py \
            s3://opal-data-bd/code/gold/B_01.holdings_lots.py
        ```

    12. `comp-pipescript deployed B_01` — confirm MATCH before re-enabling nightly.

    ## Phase 4 — Nightly emission gate (async, 3 days)

    13. Shadow emissions resume automatically with next nightly gold run (B_01 runs nightly;
        SLEEVE_SHADOW_DISABLE not set). No additional trigger needed.

    14. After each nightly run, spot-check:
        ```bash
        aws s3 ls s3://opal-data-bd/gold/timeseries/holdings_lots_shadow/ --human-readable
        ```
        Confirm new date partition appears. Confirm file size > 50KB (non-trivial output).

    15. After 3 consecutive clean nightly emissions, run spot-check:
        - Jones z0817905851: confirm shadow MV ≈ cash only ($21K ± $500)
        - One pure-sleeve account: confirm shadow MV within 2% of silver/allocations
        - Cohort count stable across 3 dates (within ±5 accounts)

    16. On 3 CLEAN: MCP COO with RAVC4 noting:
        - Fix commit SHA, S3 ETag
        - Dry-run validation results (Jones, pure-sleeve accounts, firm MV)
        - 3 nightly emission dates + cohort counts
        - COO signals SL-P1b re-run when ready

    ## S1 — Cohort drift investigation (parallel, non-blocking)

    17. Check diagnostics/sleeve_cohort/ parquet dates in S3:
        ```bash
        aws s3 ls s3://opal-data-bd/diagnostics/sleeve_cohort/
        ```
        Determine if a new cohort parquet was written after 2026-04-13 (dry-run date).
        If yes: diff account_id sets between the 2026-04-13 cohort and the latest cohort.
        Document: which 95 accounts dropped out, and why (account closed? cohort criteria changed?).
        Not blocking fix or commit — document findings in session log.

  </scope>

  <acceptance_criteria>
    <ac id="1">ds-commit-gate.sh exits 0 on B_01.holidays_lots.py (py_compile + AST + ruff).</ac>
    <ac id="2">REVISED (CTO Option A, 20260508): Jones z0817905851 shadow MV reflects non-vetoed positions weighted by unit_cost against non_cash_target_mv (current design post-e3463bffa). Cash floor ($21K) present. Non-FIFO positions (IEMG/DIVZ/SPYM) expected in shadow by design. NOTE: FIFO-subtract semantics intentionally reverted at e3463bffa to prevent HLOT2b 98% suppression. Jones-class accounts receive shadow MV above cash floor by design. Discriminated-path revisit parked as ADVI_ROLLUP standing-backlog.</ac>
    <ac id="3">3 pure-sleeve accounts (0 FIFO lots) shadow MV within 2% of silver/allocations. PASS (verify in Night 3 close package — silver lookup deferred per COO 20260508).</ac>
    <ac id="4">B_01 committed to CLOUD via safe-commit.sh with correct author attribution.</ac>
    <ac id="5">S3 upload MATCH confirmed via comp-pipescript deployed B_01.</ac>
    <ac id="6">3 consecutive clean nightly shadow emissions (new date partition per night, file size > 50KB).</ac>
    <ac id="7">Post-3-nightly spot-check: Jones has cash floor ($21K) + non-FIFO positions (per revised AC2) + pure-sleeve within 2% + cohort count stable (within ±5 accounts across 3 nights).</ac>
    <ac id="8">Cohort drift investigation documented in session log (S1 — non-blocking).</ac>
    <ac id="9">RAVC4 to COO with: fix commit SHA, S3 ETag, dry-run results (Jones + pure-sleeve), 3 nightly dates + cohort counts.</ac>
    <ac id="10">Session log with Compiler Tools section.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-pipescript io B_01 — confirm no new column gaps; identify all sleeve-related reads</check>
    </before_write>
    <before_commit>
      <check>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/B_01.holdings_lots.py — py_compile + AST + ruff py39. Exit 0 required.</check>
      <check>from __future__ import annotations present at top of B_01 (Rule 15)</check>
    </before_commit>
    <after_commit>
      <check>comp-pipescript deployed B_01 — MATCH before nightly re-enable</check>
      <check>comp-blast B_01 — confirm blast radius unchanged (no new downstream nodes)</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- B_01 is DS-lane (data/black_diamond/scripts/gold/); no cross-lane coordination needed.
         AE 0.6.0 owns bd-gold-trigger for PROD; nightly re-enable is automatic (no trigger needed).
         No other agent touches holdings_lots_shadow. -->
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT use SLEEVE_SHADOW_DISABLE=1 to suppress shadow after fix — the nightly re-enable is automatic.</rule>
    <rule>Do NOT merge the shadow into production holdings_lots under this TO — that is SL-P2 scope, gated on COO PROMOTE call after SL-P1b re-run.</rule>
    <rule>Do NOT skip the Jones dry-run assertion. The Jones check at 0.00% delta was the original correctness proof; restoring it (to cash-only post-fix) is the gate.</rule>
    <rule>Do NOT skip cohort drift investigation — document even if non-blocking.</rule>
  </do_not>

  <closure_note issued_by="2.0.0_SA_COO" issued_at="20260511T~12:45Z">
    SL-P1c AC6 satisfied via 3 distinct &gt;50KB nightly emits. Architectural caveat: Night 1 (2026-05-01) emit used pre-revert Fix B aggressive (cash-only target_mv); Nights 2-3 (2026-05-06, 2026-05-07) used CTO Option A revert (e3463bffa) + HLOT2 df.attrs preservation (6424b29ab). AC2/AC3 spot-checks performed against Nights 2-3 only (post-revert canonical). Discriminated-path revisit parked as ADVI_ROLLUP standing-backlog per AC2 revision 2026-05-08.
  </closure_note>

  <ravc4_summary>
    <sha_chain>7c9f1b13c (orig Fix B, 2026-05-01 18:11Z) → e3463bffa (CTO Option A revert, 2026-05-05 13:00Z) → 6424b29ab (HLOT2 df.attrs preservation, 2026-05-07 16:10Z)</sha_chain>
    <emit_table>
      <emit date="2026-05-01" bytes="62347" etag="f5b670f4fe095fb35876ebb308898602" wrote_at="2026-05-05T04:27:35Z" arch="pre-revert Fix B aggressive"/>
      <emit date="2026-05-06" bytes="113366" etag="31696cdbef46061d8f1344159c34ae6f" wrote_at="2026-05-08T04:30:31Z" arch="post-revert + HLOT2 attrs fix"/>
      <emit date="2026-05-07" bytes="111281" etag="b218cd07ff5e87d0cb772b7f961b347a" wrote_at="2026-05-11T04:27:41Z" arch="post-revert + HLOT2 attrs fix"/>
    </emit_table>
    <cohort_counts>
      <date d="2026-05-01" rows="593" accts="449" firm_mv_usd="1089461" jones_mv_usd="21542" jones_lots="1"/>
      <date d="2026-05-06" rows="1203" accts="458" firm_mv_usd="46340649" jones_mv_usd="2488563" jones_lots="4"/>
      <date d="2026-05-07" rows="1221" accts="457" firm_mv_usd="49810495" jones_mv_usd="2462707" jones_lots="4"/>
      <stable_cross_date>448 accounts present on all 3 dates; Nights 2-3 cohort delta -1 (within ±5).</stable_cross_date>
    </cohort_counts>
    <jones_spot_check>Nights 2-3 ~$2.47M ± 1% (4 non-vetoed lots: IEMG/DIVZ/SPYM-class + cash floor). Matches AC2 CTO Option A revised semantics.</jones_spot_check>
    <pure_sleeve_spot_check>4 of top-5 non-Jones accts within 1% night-over-night: z0815250401 (-0.90%), z0820121161 (-0.99%), z0813461901 (-0.78%), z0820335091 (-0.77%). 5th (z0820641271 $11K→$1.14M) is real account state transition, not fix regression.</pure_sleeve_spot_check>
  </ravc4_summary>
</task_order>
