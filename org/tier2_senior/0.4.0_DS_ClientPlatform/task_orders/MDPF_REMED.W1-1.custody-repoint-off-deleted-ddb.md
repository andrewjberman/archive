<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-07-custody-repoint</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-08-07</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
  </metadata>

  <objective>
    Repoint the 49F custody series off `opal-assets-daily-aua` (DELETED by Andrew 2026-08-07) onto the
    S3 silver path that already sits in the same file. **MEASURED AS A TRUE NO-OP ON SERVED VALUES** —
    this is not a basis change and needs no ruling. ⏰ The MDPF 09:00 ET schedule fires TOMORROW
    UNATTENDED with Andrew as its oracle, and the current code path scans a table that no longer exists.
  </objective>

  <context>
    Andrew deleted `opal-assets-daily-aua` and `opal-etfs-daily` 2026-08-07 ~1855Z. VERBATIM, on being
    shown a consumer: *"too late got rid of both and dont care."* Not re-litigated. This TO handles the
    consequence.

    THE FILE: `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`
      :73   SCHWAB_SILVER = "schwab/08242234/silver"
      :322  DDB_AUA_TABLE = "opal-assets-daily-aua"          <- DELETED
      :329  load_ddb_0824_custody_history()  -- `ddb.scan()`, BARE, no try/except
      :368  load_rps_custody_history()       -- reads {SCHWAB_SILVER}/fact_rps_s2, sums
                                                `net_mv_plus_cash`, NAMED gaps, NO interpolation

    >> THE MEASUREMENT THAT MAKES THIS A NO-OP — run at the COO seat on Andrew's own instruction
    (*"I would just manually check out the results post-7/23 and see if they align with simply adding
    net+cash or just net from the s3 silver"*):

      served truth = platinum/mdpf/49financial/aggregate-aua-timeseries.json (meta.basis "schwab-rps",
      439 dates, as_of_last 2026-08-05), partner_custody_total[] joined to dates[].
      candidates computed from all 9 post-7/23 fact_rps_s2 partitions (9 of 9 present).

      date          rows           SERVED         net+cash         net only   d(net+cash)      d(net)
      2026-07-24   7098  1,681,629,958.02  1,681,629,958.02  1,649,483,876.28      0.00  -32,146,081.74
      2026-07-29   7123  1,678,057,669.35  1,678,057,669.35  1,650,908,393.08      0.00  -27,149,276.27
      2026-08-05   7144  1,724,877,753.85  1,724,877,753.85  1,699,571,113.13      0.00  -25,306,640.72
      (all 9 rows in the COO record; the three above are representative)

      EXACT (<1 cent) of 9:   net_mv_plus_cash = 9      net_mv_positions = 0

    **`SUM(net_mv_plus_cash)` reproduces EVERY served point TO THE CENT.** Net-only misses by $25–32M
    every single day — a DISCRIMINATING negative, so the positive is not luck.

    ⛔ **THEREFORE THE DOCSTRING AT :329 IS FALSE AND YOU SHOULD DELETE IT, NOT PRESERVE IT.** It claims
    the DDB series *"SUPERSEDES the fact_rps_s2 envelope series (a different VALUATION of the same
    account)."* The served artifact the script itself produced contradicts that. Header `:12`
    (*"partner_custody_total[] = REAL full-envelope fact_rps_s2 daily snapshots"*) and the C2 definition
    at `:2595` (*"SUM(net_mv_plus_cash) ... positions + FULL cash leg"*) were right; the function
    docstring between them was wrong, and it was the load-bearing sentence in a hold I placed and have
    since withdrawn.

    HONEST BOUND, carried so you do not overclaim it: the tie covers the **9 post-7/23 dates** where
    both series exist. Earlier history is UNTESTED and may differ. The repoint only has to be right
    going forward and the served axis ends 2026-08-05 — but do not describe the tie as historical.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-pipescript io dim_mdpf_aggregate_aua_timeseries.py --pipeline mdpf</run>
      <expect>COLUMN GAPS + portal consumers. `--pipeline` REQUIRED — flagless is rc=2 REFUSED.</expect>
      <if_mismatch>Fix any COLUMN GAP before proceeding.</if_mismatch>
      <run>comp-blast load_ddb_0824_custody_history</run>
      <expect>Its callers. Confirm nothing else depends on the DDB shape.</expect>

    Phase 2 — before committing: <run>.tools/commit-gate.sh</run>

    Phase 3 — after committing:
      <run>comp-validate dim_mdpf_aggregate_aua_timeseries.py --artifact /tmp/&lt;artifact&gt;.json</run>
      <expect>PASS or WAIVED. ⛔ NO_CONFIG / ZERO_CHECKS = UNVALIDATED — never signal SAFE on it.</expect>
      <run>comp-pipescript deployed dim_mdpf_aggregate_aua_timeseries.py</run>
      <expect>MATCH after upload. ⚠ `data/mdpf/...` deploys under the S3-membership guard — a 404 is a
      LOUD SKIP, and a silent skip is not a deploy.</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` — you also hold
      MDPF_COTTONWOOD.FIX1 on `build_dim_model_portfolio.py` in the same tree.
    - required_action: **land both on ONE ad-hoc QA run** — Andrew asked for *"an ad hoc run to test the
      flow."* Ad-hoc runs are SANCTIONED for QA; the production path remains the SCHEDULE.
    - The script is packaged into `mdpf-gold-lambda` (`build_package.py:35`) and referenced by
      `mdpf-daily-dispatch.sh` as a LIBRARY, not an entry point. Deploy accordingly.
  </cross_domain_coordination>

  <acceptance_criteria>

    1. THE 49F CUSTODY SERIES IS SOURCED FROM `{SCHWAB_SILVER}/fact_rps_s2` VIA `net_mv_plus_cash`.
       No `boto3` DynamoDB client remains on this path; `DDB_AUA_TABLE` and
       `DDB_0824_CUSTODY_COHORT` are removed, not left dangling.

    2. >> THE TIE IS RE-DERIVED AT YOUR SEAT AND PUBLISHED — do not take the COO figures on report.
       Recompute the 9 post-7/23 dates and show `d = 0.00` on all 9, **plus the net-only column as the
       NEGATIVE CONTROL.** ⛔ A run that shows only the passing limb is not a control: the net-only
       miss ($25–32M/day) is what proves the match is discriminating rather than coincidental.

    3. THE `__missing__` / HONEST-ABSENT CONTRACT IS PRESERVED. The DDB path returned
       `out["__missing__"]` and never carried forward or interpolated. The S3 path has the same
       discipline (`_all_partition_dates` -> NAMED gaps). **A date with no `fact_rps_s2` partition must
       still come back ABSENT, never zero and never carried.** Zero is a VALUE; absent is a
       NON-MEASUREMENT, and the artifact asserts the difference to a client.

    4. THE FALSE DOCSTRING IS DELETED, not amended into a footnote. Replace it with what the
       measurement establishes, citing the tie's vintage and its 9-date bound.

    5. `comp-validate` PASS/WAIVED and `comp-pipescript deployed` MATCH.

    6. Session log with a Compiler Tools section and an archetype tag.

  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py</file>
      <file action="reference">s3://opal-data-assets/schwab/08242234/silver/fact_rps_s2/</file>
      <file action="reference">s3://opal-data-portal-v2/platinum/mdpf/49financial/aggregate-aua-timeseries.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Repoint the custody series to the existing S3 function; do not write a new reader.</requirement>
    <requirement id="2">Re-derive and publish the 9-date tie WITH its negative control.</requirement>
    <requirement id="3">Preserve honest-absent semantics exactly.</requirement>
    <requirement id="4">Ride the same ad-hoc QA run as MDPF_COTTONWOOD.FIX1.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">The repoint, gate-passed.</deliverable>
    <deliverable type="document">The re-derived tie table incl. the net-only negative control + vintage.</deliverable>
    <deliverable type="document">Session log with Compiler Tools section.</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT restore, recreate or re-provision the DynamoDB table. Andrew deleted it deliberately.</rule>
    <rule>DO NOT preserve the "different VALUATION" docstring. It is FALSE by measurement.</rule>
    <rule>DO NOT let an absent date become 0.00. Zero is a value; absent is a non-measurement.</rule>
    <rule>DO NOT publish the tie without the net-only negative control beside it.</rule>
    <rule>DO NOT claim the tie holds pre-7/23 — that window is UNTESTED.</rule>
    <rule>DO NOT touch the platinum publisher or serving projection. Gold producer only; D4 never
    patches shape.</rule>
    <rule>DO NOT build any alert, alarm, SNS topic, SES send, freshness checker or monitor.</rule>
  </do_not>
</task_order>
