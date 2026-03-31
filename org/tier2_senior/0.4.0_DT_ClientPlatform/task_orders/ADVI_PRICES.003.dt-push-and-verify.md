<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-24-prices-003-dt</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <date>2026-03-24</date>
    <status>complete</status><!-- subsumed: all PRICES commits on CLOUD, AE verified gold rerun + scheduler fix, project closed 2026-03-25 -->
    <project_code>ADVI_PRICES</project_code>
  </metadata>

  <objective>
    QA gate and push for ALL accumulated ADVI_PRICES commits (.001 + .002 + .003).
    After AE completes the price rebuild + gold rerun + reconciliation, review
    final numbers and pass/fail.
  </objective>

  <scope>
    <files>
      <file action="review">data/black_diamond/scripts/silver/bd_price_update.py</file>
      <file action="review">data/black_diamond/scripts/silver/build_canonical_prices_v2.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Review DS .003 commits:
      - 08b6d557: diagnostic script (read-only, low risk)
      - 61b34f77: hierarchy fix + 8 ticker corrections in BOTH pricing scripts
        - Verify: scoped_override at -2 (highest), yahoo_finance at -1
        - Verify: _TICKER_CORRECTIONS map applied last in load_ticker_lookup()
        - Verify: BNP PARIBAS SA and SONY FINL GROUP have ticker set to None
        - Verify: FNDA->FNX, GLDM->GLTR, IJH->IJK, VBR->VSIAX, VEA->VTMGX, VO->VMCPX
      - 7d5c6c92: session log (no code changes)
      Also review AE's IYF correction commit if present.
    </requirement>

    <requirement id="2">
      Push ALL accumulated ADVI_PRICES commits to CLOUD remote after QA.
      This includes .001 (12 commits), .002 (2 commits), .003 (3+ commits).
    </requirement>

    <requirement id="3">
      After AE .003 completes:
      - Review reconciliation numbers
      - Pass: net gap within 1.5% of BD AUA (structural gaps accepted)
      - Fail: flag remaining causes to COO
      - Update ADVI_PRICES project status accordingly
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">All ADVI_PRICES commits reviewed and pushed</criterion>
    <criterion id="2">Final reconciliation pass/fail documented</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT push until AE .001 gold rerun complete (MVPLVL.009 shared gate)</constraint>
    <constraint>Do NOT push until DS .003 commits verified</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_PRICES.003" status="complete">
      DS committed 08b6d557, 61b34f77, 7d5c6c92.
    </dependency>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_PRICES.003" status="pending">
      AE must complete price rebuild + gold rerun + recon before DT final review.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Push all ADVI_PRICES commits to remote</deliverable>
    <deliverable type="document">Pass/fail assessment in session log</deliverable>
  </deliverables>
</task_order>
