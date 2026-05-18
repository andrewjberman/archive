<task_order>
  <metadata>
    <id>MDPF_ASSETS.005</id>
    <slug>dsb-wsd1-pfde-pfoe-netassets-holdings-ingestion</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-18 (COO) to DS~B -- the open lane (DS~B finished MDPF_ASSETS.003). WS-D.1 ingestion is self-contained -- it extends the existing ETFS_NETAST probe and writes the existing opal-data-etfs schema; it is NOT gated on the WS-A contract (only WS-D.2, the partner-attribution decomposition, conforms to WS-A). Start now.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF_ASSETS WS-D.1. DIVZ/IDVZ net-assets ship today via the ETFS_NETAST TrueShares probe; PFDE/PFOE do not. This TO closes the 2-of-4 ETF gap and lays down the day-over-day holdings record WS-D.2 needs.</priority>
    <sla>2-3d wall -- a probe-source extension (DS~A scoped the net-assets piece "small"; the day-over-day holdings-detail artifact is the added scope).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md (v0.3) -- section 3.3 (ETF ownership decomposition), section 4 WS-D.1 (extend ETF net-assets ingestion to PFDE+PFOE) + WS-D.2 (the ownership decomposition this TO's holdings artifact feeds), section 7-Q4.</prd>
    <phase0_brief>docs/briefs/mdpf-pfde-pfoe-etf-netassets-feasibility-20260518.md (MDPF_ASSETS.002, DS~A) -- the SHIP-feasible verdict + the confirmed source. READ THIS FIRST; it is the build spec. Key findings:
      - PFDE/PFOE are NOT TrueShares funds -- they are Pathfinder ETFs, and the Filepoint namespace `FilepointOpalCap` confirms they are Opal Capital's own funds.
      - The issuer publishes a public, no-auth, daily-post-close Filepoint CSV set at `https://pathfinderetfs.com/assets/data/FilepointOpalCap.40O6.O6_*`.
      - Third-party aggregators (Yahoo, Investing.com) carry PFDE/PFOE but are MATERIALLY STALE -- DS~A measured PFDE on Yahoo/web ~$102.9M vs the issuer's $131.63M (~22% error). Yahoo is NOT a viable source; do not use it.
    </phase0_brief>
    <built_pattern>etf_netassets_watch/etf_probe.py (committed da4931c85, ETFS_NETAST) -- the DIVZ/IDVZ net-assets probe. A per-fund tiered source ladder (Tier 1 TrueShares HTML scrape -> Tier 2 carry-forward -> Tier 3 MSN -> Tier 4 stale carry-forward -> Tier 5 null) writing `etf_history.csv` + per-day parquet + `silver/netassets_daily.parquet` + a JSON snapshot, all to `s3://opal-data-etfs/`. The row schema (`CSV_FIELDS` / `PARQUET_COLUMNS`) is source-neutral; the `FUNDS` config is per-fund.</built_pattern>
    <andrew_directive>Andrew direct 2026-05-18: source PFDE/PFOE from the issuer's "Download All Holdings" feed (the Filepoint `ETF_Holdings.csv`), NOT the topline `DailyNAV.csv` alone -- so the pipeline captures day-over-day LINE-ITEM holdings, not just a topline summary. The net-assets number is then an aggregation/read off the holdings record. Rationale: one source serves both WS-D.1 (the net-assets topline) and WS-D.2 (the ownership decomposition needs per-holding detail); keeping the detailed daily record from day one means a future holdings decomposition has history, not just a current snapshot.</andrew_directive>
  </references>

  <context>
    Three of the four Opal ETFs' net-assets story: DIVZ + IDVZ flow daily through the ETFS_NETAST TrueShares probe; PFDE + PFOE do not, because they are not TrueShares-administered. DS~A's MDPF_ASSETS.002 feasibility resolved the source -- the Pathfinder/Filepoint issuer CSV feed -- and confirmed it SHIP-feasible and structurally cleaner than the TrueShares scrape.

    Andrew has refined the source choice: rather than the topline `DailyNAV.csv`, ingest the "Download All Holdings" feed -- the Filepoint `ETF_Holdings.csv` -- which carries per-holding line items (name, ticker, CUSIP/identifier, shares held, market value, percentage of net assets) for both funds, plus per-row NetAssets + SharesOutstanding. Storing this line-item detail daily gives a day-over-day holdings record; the net-assets topline is derived from it. This makes WS-D.1 the ingestion of BOTH the net-assets topline AND the holdings detail -- the holdings detail is what WS-D.2 (the ETF ownership decomposition: held_49F / held_Inflection / public_residual, section 3.3) will later attribute to partners. WS-D.2 itself -- the decomposition logic conforming to the WS-A canonical contract -- is a separate, later TO; this TO captures the data it will need.

    DS~A's brief lists the exact Filepoint paths and four carry-forward gaps; this TO is the build off that brief, with the holdings-detail capture added per Andrew's directive.
  </context>

  <scope>
    <step>Phase 0 -- study + source confirmation. Read DS~A's MDPF_ASSETS.002 brief end to end and study `etf_netassets_watch/etf_probe.py` (the `FUNDS` config, the source ladder, `CSV_FIELDS` / `PARQUET_COLUMNS`, the S3 write path). Verify the live Filepoint `ETF_Holdings.csv` (`https://pathfinderetfs.com/assets/data/FilepointOpalCap.40O6.O6_ETF_Holdings.csv`): its column set, that it carries both PFDE + PFOE, its refresh cadence (daily / T-1 -- the screenshot shows "Data as of 05/18/2026"), and its per-row NetAssets + SharesOutstanding fields. Settle the file mix: `ETF_Holdings.csv` is the holdings + net-assets source; decide whether `DailyNAV.csv` is still pulled for the `nav` / `market_price` / premium-discount fields the probe schema records (the holdings file is line items -- it likely lacks fund-level NAV/market-price). Settle the net-assets method: the holdings file carries a NetAssets field -- use it as the topline of record, with the sum of per-holding market value as a reconciliation cross-check (note: sum-of-holdings excludes the fund's cash/receivables, so it will not equal NetAssets exactly -- surface the gap, do not silently pick one). Record the decisions.</step>
    <step>Phase 1 -- build. Extend `etf_netassets_watch/etf_probe.py`:
      - Add `pfde` / `pfoe` entries to `FUNDS` with a per-fund `source_kind` key; DIVZ/IDVZ keep `source_kind` = TrueShares so the existing tier is untouched.
      - Add a Filepoint Tier-1 source function (`fetch_filepoint` or similar): GET the `ETF_Holdings.csv`, parse the line items + the NetAssets/SharesOutstanding fields, for both funds in one call. Per-fund `source_kind` branches Tier 1; the MSN Tier-3 fallback + the carry-forward tiers stay source-neutral as-is.
      - Add a day-over-day holdings-detail artifact: persist the full per-holding line-item set per fund per day (name, ticker, identifier/CUSIP, shares held, market value, pct of net assets, the data-as-of date) -- a new parquet under `s3://opal-data-etfs/` (e.g. `silver/holdings/{date}.parquet` -- DS~B's call on the exact layout, keep it parallel to the existing `silver/netassets/` convention). This is the durable record WS-D.2 consumes.
      - The net-assets topline for PFDE/PFOE flows into the existing `etf_history.csv` / `silver/netassets_daily.parquet` / snapshot schema unchanged -- the row schema is already source-neutral; `source` just gains a `filepoint` value.
      Carry DS~A's brief gaps 1-4 into the build: (1) historical backfill is NAV-only -- start the true net-assets + holdings series from the first probe run, flag inferred history; (2) the Filepoint URL embeds a client code (`40O6.O6`) -- treat a non-200 / header-schema-mismatch as a Tier-1 failure that falls through to MSN, and assert the expected header; (3) net-assets differs slightly between the Filepoint files -- holdings-file NetAssets is the SoR; (4) the probe is now two-issuer -- keep the ladder per-fund.
      ds-commit-gate (`.tools/ds-commit-gate.sh`) exit 0 on the `.py` edit before commit.</step>
    <step>Phase 2 -- verify. Run the probe for PFDE/PFOE end to end. Net-assets must land within ~1% of both the 2026-05-15 reference values (PFDE ~$131.52M, PFOE ~$111.33M -- the coworker tracking sheet) and DS~A's 2026-05-15 issuer-CSV pull (PFDE $131.63M, PFOE $110.40M). Confirm: the holdings-detail artifact captures the full line-item set for both funds; the holdings-sum vs NetAssets reconciliation is surfaced (not silently absorbed); DIVZ/IDVZ are unaffected (the TrueShares tier still runs). Record the verified numbers in the session log.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>No comp-* graph tool applies -- WS-D.1 extends a local off-the-books probe (etf_netassets_watch/), not a pipeline-graph node. State N/A in one line. The Phase-0 verification is the direct HTTPS GET of the live ETF_Holdings.csv (per DS~A's MDPF_ASSETS.002 method).</run>
        <expect>N/A -- documented.</expect>
        <if_mismatch>n/a</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>The extended probe end-to-end: `python etf_netassets_watch/etf_probe.py` for the PFDE/PFOE funds (the gate's own mechanism).</run>
        <expect>PFDE/PFOE net-assets rows + the holdings-detail artifact materialize; DIVZ/IDVZ rows still produced via the TrueShares tier.</expect>
        <if_mismatch>Debug the Filepoint source function / the per-fund source_kind branch.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>WS-D.1 ADDS two funds to a daily forward-looking probe + a new holdings artifact; it does not modify or reprocess any existing pipeline producer. DIVZ/IDVZ history is untouched. PFDE/PFOE net-assets history is NAV-only pre-existing (DS~A gap 1) -- the true net-assets + holdings series starts from the first probe run; no backfill of fabricated history.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    `etf_netassets_watch/etf_probe.py` is co-owned with ETFS_NETAST (the DIVZ/IDVZ probe + the opal-data-etfs Terraform adoption). Coordinate:
    - ETFS_NETAST.001 (AE 0.7.0) is Terraform-adopting the `opal-data-etfs` bucket (import-to-0-diff of the existing bucket resource). Adding PFDE/PFOE objects + a new `silver/holdings/` prefix does NOT affect the bucket-resource import (Terraform manages the bucket, not its objects) -- but notify AE 0.7.0 so the adoption's object census is not surprised by new prefixes.
    - `.owned-paths.yaml` has NO path rule for `etf_netassets_watch/**` (a known ETFS_NETAST open item -- DS~A's original probe commit da4931c85 used an audited GIT_COMMIT_AUTHOR_OVERRIDE). DS~B will hit the same on the etf_probe.py commit -- use `.tools/safe-commit.sh` and, if owned-paths blocks the commit, the audited `--force` path (FORCE-BYPASS audit entry) per the OWNPTH precedent, and flag it to COO. The permanent fix (a path rule, CTO-owned) is tracked under ETFS_NETAST -- do not author it here.
    - WS-D.2 (the ownership decomposition: attributing ETF holdings to partners, conforming to the WS-A canonical contract) is a separate later TO. This TO produces the holdings-detail artifact WS-D.2 consumes; it does NOT build the decomposition.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">`etf_probe.py` is extended: `pfde` / `pfoe` `FUNDS` entries + a Filepoint Tier-1 source function reading the `ETF_Holdings.csv`; a per-fund `source_kind` branch leaves DIVZ/IDVZ on the TrueShares tier untouched.</ac>
    <ac id="AC2">PFDE/PFOE net-assets flow into the existing `etf_history.csv` / `silver/netassets_daily.parquet` / snapshot schema (source-neutral schema, `source` = `filepoint`). Verified within ~1% of both the 2026-05-15 reference set ($131.52M / $111.33M) and DS~A's issuer-CSV pull ($131.63M / $110.40M).</ac>
    <ac id="AC3">A day-over-day holdings-detail artifact ships: the full per-holding line-item set (name, ticker, identifier, shares held, market value, pct of net assets, data-as-of) per fund per day, persisted to opal-data-etfs. The holdings-sum vs NetAssets reconciliation is computed + surfaced, not silently absorbed.</ac>
    <ac id="AC4">DS~A's gaps 1-4 are handled: NAV-only history flagged inferred; the Filepoint URL non-200 / schema-mismatch falls through to the MSN tier; holdings-file NetAssets is the net-assets SoR; the probe ladder stays per-fund (two-issuer).</ac>
    <ac id="AC5">No emoji; ds-commit-gate exit 0 on the `.py` edit; Rule 16 (any new local-runtime bash relies only on Git-Bash-3.6.7 utilities); session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The extended `etf_probe.py` -- Filepoint Tier-1 source + PFDE/PFOE `FUNDS` entries.
    - The day-over-day ETF holdings-detail artifact (opal-data-etfs).
    - The Phase-0 file-mix + net-assets-method decision record.
    - Session log with the Compiler Tools section + the verified PFDE/PFOE numbers. RAVC2 to COO.
  </deliverables>
</task_order>
