<task_order>
  <metadata>
    <id>ADVI_INFFIN.014</id>
    <slug>dsc-nna-histogram-emit-parity</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-14</date>
    <status>complete</status>
    <shipped_commit>a731e8461</shipped_commit>
    <shipped_s3_etag>c5758d28a534fd387704a5e6a023c7f0</shipped_s3_etag>
    <shipped_at>2026-05-14T14:10:47Z</shipped_at>
    <ravc4_accept>1.0.0_SA_CTO 2026-05-14T14:13Z; 2.0.0_SA_COO RAVC1 ACCEPTED + AE chain-fire on RAVC2 receipt</ravc4_accept>
    <session_log>org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-14/DS_C_session1_inffin014_nna_histogram_emit.md</session_log>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Andrew-flagged partner-visible defect; INF NNA bell curve cannot render (no histogram data); 49F parity exists; smallest possible delta on INF gold emit side</priority>
    <sla>~2-3h wall (RD estimate "hours"; pattern matches existing 49F NNA histogram emit logic)</sla>
  </metadata>

  <references>
    <ref type="brief">RD 0.4.2 MCP 2026-05-14 ~13:55Z (Issue 2 routing) + empirical S3 inspection (49F vs INF parquet/json shape diff)</ref>
    <ref type="project_json">org/projects/ADVI_INFFIN.json</ref>
    <ref type="authority">Andrew direct flag mid-session: "make sure we are displaying canonical distribution bell curve for snapshot-NNA as well." Screenshot evidence: Snapshot/ADV/NNA/Quarter L0 right partition empty (placeholder "Select a advisor to view per-relationship NNA flow distribution"); should render firm-level NNA bell curve like 49F.</ref>
    <ref type="cross_link">Companion to RD .013 FE-side fix `1574ba7d` (Issue 1 percentile-chip synthesis; already shipped; auto-populates p10-p90 chips once .014 histogram lands). 11/12 prior INFFIN TOs all CLOSED; this is Issue 2 addendum surfaced post-CTO RAVC4 on 12/12.</ref>
    <ref type="prior_dissolved">ADVI_INFFIN.013 (v1.7.57 inf-client-detail Lambda mirror) DISSOLVED 2026-05-13 per AE 0.7 pre-ship empirical investigation (`dfcc60c42`). .014 is the next clean slot.</ref>
  </references>

  <context>
    Andrew flagged 2 INF Distribution-tab defects mid-session 2026-05-14. RD 0.4.2 routing:

    - **Issue 1 (FE-side)**: Snapshot/GEO/AUA percentile chips showing "N/A" — INF emits `percentiles: null` while 49F emits the full p10-p90 block. RD shipped `1574ba7d` portal DEV: `withSynthesizedPercentiles()` helper synthesizes chips client-side from histogram bin counts. Auto-no-ops on 49F (already populated). DONE.

    - **Issue 2 (DS-side; THIS TO)**: Snapshot-NNA canonical bell curve absent on Inflection. Right partition shows empty placeholder; 49F partner_analytics_quarterly.json has populated histogram + percentiles for `views.nna.current.{geo,adv}.distribution.total`; INF has `histogram.bins=0, counts=[]` and `percentiles: null`. FE cannot synthesize without underlying histogram data.

    **Empirical data-side gap (per RD S3 inspection):**

    | Surface | 49F `views.nna.current.geo.distribution.total` | INF `views.nna.current.geo.distribution.total` |
    |---|---|---|
    | `histogram.bins / counts` | bins=23, counts_sum=781 ✓ | empty (bins=0, counts=[]) |
    | `percentiles` block | `{p10, p25, p50, p75, p90}` populated ✓ | null |
    | Flat aggregate stats | not emitted | `count=218, p25/p50/p75/min/max/mean/sum` |

    Same gap on `views.nna.current.adv.distribution.total`.

    **Smallest-delta fix:** INF gold script that produces `partner_analytics_quarterly.json` (likely INF_09 partner_analytics aggregator OR upstream INF_D_00 portal_aggregates path) — add `views.nna.current.{geo,adv}.distribution.total.histogram.{bins,counts}` + `percentiles.{p10,p25,p50,p75,p90}` to match 49F shape exactly. RD's `withSynthesizedPercentiles` helper auto-populates the chip strip once the histogram bins land; no additional FE work needed.

    **Bin structure:** match 49F semantics — per-relationship NNA values across the firm, signed-binned (NNA can be negative outflows). Reference 49F's BD-pipeline equivalent script for canonical bin-edges + count semantics.
  </context>

  <objective>
    Emit `views.nna.current.{geo,adv}.distribution.total.histogram.{bins,counts}` + `percentiles.{p10,p25,p50,p75,p90}` blocks on INF `partner_analytics_quarterly.json` matching 49F shape exactly. Smallest possible delta; reuse existing 49F NNA histogram logic if possible.
  </objective>

  <scope>
    <surfaces>
      <surface id="2-issue-2">INF Snapshot-NNA bell curve histogram emit parity with 49F (GEO + ADV cohorts)</surface>
    </surfaces>
    <files>
      <file action="investigate">Locate which INF gold script writes `partner_analytics_quarterly.json#views.nna` — likely INF_09 (partner_analytics aggregator) OR INF_D_00 (portal_aggregates). `comp-pipescript io <script>` to confirm.</file>
      <file action="readonly_reference">49F BD-pipeline equivalent — `data/black_diamond/scripts/gold/...` that produces 49F `partner_analytics_quarterly.json#views.nna.current.{geo,adv}.distribution.total.histogram` — reuse bin-edge logic + count semantics</file>
      <file action="modify">INF gold script — add NNA histogram + percentiles emit for GEO + ADV cohorts under `views.nna.current.*.distribution.total`</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript io INF_09 + comp-pipescript io INF_D_00 (or whichever script you identify as the partner_analytics_quarterly.json writer)</run>
      <expect>READS includes the upstream NNA timeseries source(s) + accounts_v2 / advisor_attribution dims. WRITES includes partner_analytics_quarterly.json with views.nna structure.</expect>
      <if_mismatch>If writer isn't obvious from io scan, fork to manual S3 lineage trace + grep for "views.nna" emit sites. Surface to COO if you can't identify the writer in ~15min.</if_mismatch>
    </step>
    <step>
      <run>grep -rn "views.nna.current" data/orion/scripts/gold/ + grep -rn "views.nna.current" data/black_diamond/scripts/gold/ to find 49F's equivalent emit logic</run>
      <expect>49F writer enumerated; copy bin-edge + count logic verbatim if symmetric, OR adapt to INF schema if 49F path uses BD-specific source.</expect>
      <if_mismatch>If 49F path is structurally different (e.g., uses BD per-account transaction granularity vs INF per-HH NNA aggregates), document the adaptation rationale in session log.</if_mismatch>
    </step>
    <step>
      <run>aws s3 cp s3://opal-data-bd/platinum/firm/partner_analytics_quarterly.json - | jq '.views.nna.current.geo.distribution.total | {histogram, percentiles}' | head -30</run>
      <expect>49F empirical shape: histogram.bins ~23 entries, counts ~ same length, sum matches firm-level NNA count; percentiles object with all 5 keys.</expect>
      <if_mismatch>Document 49F empirical baseline; reproduce shape exactly on INF emit side.</if_mismatch>
    </step>
  </phase>

  <phase id="2" when="before commit">
    <step>
      <run>ds-commit-gate.sh on the modified gold script (py_compile + ds-precommit-check.py + ruff py39 0.15.11)</run>
      <expect>Three gates pass.</expect>
      <if_mismatch>STOP. Per CLAUDE.md Rule 14.</if_mismatch>
    </step>
    <step>
      <run>Local dry-run: invoke the modified gold script against today's silver inputs (or staged test fixture) + jq the output to confirm `views.nna.current.geo.distribution.total.histogram.bins` + `counts` + `percentiles` are populated</run>
      <expect>Empirical histogram emit non-empty; percentiles object has all 5 keys.</expect>
      <if_mismatch>Fix emit logic; do not commit + safe-deploy without empirical verification.</if_mismatch>
    </step>
    <step>
      <run>comp-validate (if validate config exists for this script) OR manual jq spot-check matching 49F shape</run>
      <expect>Exit 0 OR manual spot-check confirms shape parity.</expect>
    </step>
  </phase>

  <phase id="3" when="after commit">
    <step>
      <run>safe-deploy.sh + comp-pipescript deployed gate on the modified script</run>
      <expect>MATCH (S3 ETag = committed-ref SHA).</expect>
    </step>
    <step>
      <run>AE 0.6.1 chain fire (gold-d OR full per AE's call) → empirical check `s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json#views.nna.current.geo.distribution.total.histogram.bins` post-chain</run>
      <expect>Histogram + percentiles populated on INF artifact; FE chip strip auto-renders via RD's `withSynthesizedPercentiles` helper from `1574ba7d`.</expect>
      <if_mismatch>Surface to COO; chain wiring or Lambda overwrite may be in play.</if_mismatch>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `views.nna.current.geo.distribution.total.histogram.{bins,counts}` populated on INF `partner_analytics_quarterly.json` post-chain.
    AC2: `views.nna.current.geo.distribution.total.percentiles.{p10,p25,p50,p75,p90}` populated.
    AC3: Same emit on `views.nna.current.adv.distribution.total` (ADV cohort parity).
    AC4: Shape parity verified against 49F via jq diff.
    AC5: ds-commit-gate.sh PASS (py_compile + ds-precommit-check.py + ruff py39).
    AC6: safe-deploy.sh + comp-pipescript deployed MATCH.
    AC7: Andrew visual smoke on INF Snapshot/ADV/NNA bell curve renders post-chain (signal-bounded: gate on AE chain fire + RD visual confirm or Andrew direct).
    AC8: Session log Compiler Tools section reproduces every Phase 1/2/3 run.
    AC9: MCP RAVC2 to COO with commit hash + S3 ETag + empirical artifact shape evidence.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phases above. Auto-rule 1 trigger: new platinum field — `comp-platinum reverse views.nna.current.geo.distribution.total.histogram` at Phase 1 to enumerate consumers BEFORE emit lands. (Single consumer expected: DistributionTab.tsx chip-strip + bell-curve render path; RD's helper auto-routes once data present.)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: none — additive INF emit; existing 49F path is the reference.

    DOWNSTREAM CONSUMERS: DistributionTab.tsx `withSynthesizedPercentiles` helper (RD ship `1574ba7d`) auto-populates chip strip on histogram presence. Bell-curve render path already wired (currently no-ops on empty histogram).

    COORD: AE 0.6.1 — chain fire post-ship (gold-d OR full; AE call). RD 0.4.2 — visual confirm post-chain.

    PORTAL SUBMODULE: DT 0.4 push (RD's `1574ba7d` portal commit is part of the existing 6-commit DT push queue; nothing additional from this TO).
  </cross_domain_coordination>

  <data_reprocess_scope>
    <reprocess_required>
      Single gold-script patch on INF partner_analytics aggregator. Phase 3 chain fire materializes new histogram emit on `partner_analytics_quarterly.json`. No silver/bronze touch; no historical re-walk; net new fields on existing artifact path.

      Affected S3 prefix: `s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json` — overwritten on every chain. Post-chain mtime > commit-time + jq spot-check on new fields = freshness gate satisfied.
    </reprocess_required>
  </data_reprocess_scope>

  <deliverables>
    1. INF gold script patch (likely INF_09 OR INF_D_00; identify in Phase 1)
    2. Single commit under 0.4.0_DS_ClientPlatform~C author
    3. safe-deploy.sh + S3 MATCH evidence
    4. AE chain fire RAVC2 (parallel routing)
    5. Session log + RAVC2 MCP to COO
  </deliverables>

  <ravc>
    DS~C RAVC2 to COO post-AC1-9 PASS. COO ratifies + signals AE 0.6.1 for chain fire post-deploy (gold-d sufficient; full chain not required for this single platinum aggregator). Post-chain: RD visual confirm; Andrew direct sign-off on bell-curve render.
  </ravc>

  <notes>
    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"` per protocol.

    **Compiler context update:**
    ```
    SERIAL=0.4.0_DS_ClientPlatform~C
    TO_ID=ADVI_INFFIN.014
    ```

    **Light coord with INFINC.001:** DS~D is starting INFINC.001 skip-gate lib (~3d) on a different code surface (`data/orion/scripts/gold/lib/`). Your INFFIN.014 work on `data/orion/scripts/gold/INF_*.py` shouldn't conflict.

    **Open Item carry-forward (per RD's prior INFFIN.012 RAVC2 + .011 ship):** per-window NNA flows fee-split would require DS-side scope (per-HH per-period flow stream OR per-fee parallel emit). NOT in .014 scope; track as follow-on if Andrew wants post-demo (see prior open-item documentation).
  </notes>
</task_order>
