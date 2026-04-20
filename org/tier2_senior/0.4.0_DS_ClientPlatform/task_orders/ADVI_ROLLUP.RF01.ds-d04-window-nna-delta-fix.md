<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-rf01</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- COMPLETE 2026-04-15. Commit 21c0637f (DS ~A). QA run SSM 08f103c1 PASS. Spot-checks ±$0.01: Travis Penfield rfs.decomposition_max.nna $13,445,180.97 (+$0.00), Sydney Cobb $1,353,309.44 (+$0.01), Kyle Sims $2,457,322.57 (-$0.00). CF NOT invalidated (awaiting Andrew). ACCEPTANCE-FLEX (Rule 7 locked 2026-04-15): (1) mg/sc kept as row-sums — (a) reinterpreted from "sum-on-cumulative paths removed" (b) B_03 daily-delta semantic for growth+aua_residual means summing daily deltas IS the intended math (c) original expect: criterion #1 "sum-on-cumulative paths removed"; substituted: "removed for nna only; mg/sc remain row-sums per B_03 daily-delta contract". (2) QTD #4 reinterpreted — (a) from "within $1 for 3 spot-check books" to "document magnitude not pass/fail" (b) pre-quarter rows are NOT ~0 for mature books so QTD shifts legitimately (c) original expect: "`rfs.decomposition_qtd.nna` unchanged within $1"; substituted: "full QTD census in DS session log with pre/post delta distribution; sign-flips flagged". Pre-flagged to CTO in 20260415T163030Z_2.0.0_SA_COO_ACK msg; CTO ACK'd 20260415T163352Z. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W5</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 5 — Standalone point fix)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_geo_three_way_schism_and_rfs_nna_window.md (Bug 2)</ref>
    <ref type="brief">org/tier2_senior/0.4.0_DS_ClientPlatform/briefs/2026-04-15_post_presentation_master_summary.md (§3)</ref>
  </references>

  <objective>
    Fix D_04 window-NNA sum-of-cumulative bug emitting `rfs.decomposition_{ytd,max}.nna`
    as area-under-curve of a cumulative series instead of `last - pre_cutoff` delta.

    Two callsites in `data/black_diamond/scripts/gold/D_04.client_portal_summary.py`:
      - `_compute_window_decomposition` (L696): `sum(r.nna for r in slice_rows)` on cumulative col
      - `_compute_window_flows` nna branch (L747): same pattern

    Replace nna-sum with `_window_nna_delta()` helper using `last - pre_cutoff` math —
    identical pattern to `cum_inflows` / `cum_outflows` in the same functions (already correct).

    Spot-check evidence (DS brief): z0820265531 emits `rfs.nna_max = $563.6M`, true ITD NNA = $24.98M.
    Travis book: `decomposition_max.nna = $4.82B` on ~$428M book (11x inflation).

    ALSO verify whether `market_growth` and `synthetic_correction` branches in the same
    two functions carry the same bug pattern; if yes, fix both in the same commit.

    No wire-contract change. No FE edit required. Artifact shape identical.
  </objective>

  <wire_contract>
    Unchanged. Same keys, same types:
      platinum/accounts/{id}/summary.json:  rfs.decomposition_{qtd,ytd,max}.{nna,inflows,outflows,market_growth,synthetic_correction}
      platinum/advisors/{id}/summary.json:  rfs.decomposition_{qtd,ytd,max}.{same fields}
    Only the numeric value of the `nna` (and possibly `market_growth`/`synthetic_correction`)
    field changes. QTD coincidentally correct (pre-quarter rows ~0) -- scope should still
    pass a QTD regression test.
  </wire_contract>

  <acceptance_criteria>
    1. `_compute_window_decomposition` + `_compute_window_flows` both emit nna via
       `last - pre_cutoff` delta; sum-on-cumulative paths removed.
    2. Spot-check z0820265531: `rfs.decomposition_max.nna` matches ITD NNA ($24.98M) within $0.01.
    3. Spot-check Travis book (advisor): `rfs.decomposition_max.nna` matches advisor ITD NNA within $0.01.
    4. QTD regression: `rfs.decomposition_qtd.nna` unchanged to within $1 for 3 spot-check books.
    5. Decision + evidence recorded in commit message on whether `market_growth` / `synthetic_correction`
       carry the same bug (fix both if yes).
    6. `comp-validate D_04 --artifact /tmp/platinum_accounts_sample.json` exits 0.
    7. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement locked 2026-04-15).
    8. MCP COMPLETE to COO with commit hash + spot-check table.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_04</run>
        <expect>READS + WRITES manifest includes platinum/{accounts,advisors}/{*}/summary.json as hardcoded writes; confirms portal consumers AdvisorBookView / AdvisorPublicProfile.</expect>
        <if_mismatch>Stop and escalate to COO — script identity changed.</if_mismatch>
      </step>
      <step>
        <run>grep -n '_compute_window_decomposition\|_compute_window_flows\|_window_nna_delta' data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>Exactly the two callsite bodies (L696, L747) plus any existing `_window_nna_delta` helper (none expected — you are creating it).</expect>
        <if_mismatch>Scope has drifted since DS brief; report and pause.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse rfs.decomposition_max.nna; comp-platinum reverse rfs.decomposition_ytd.nna</run>
        <expect>Returns empty (nested-key, not indexed by tool). Manually grep portal for `rfs.decomposition` consumers; record the consumer list in the commit message so DT can spot-check post-deploy.</expect>
        <if_mismatch>If tool returns unexpected consumers, enumerate and coordinate with DT before ship.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript deployed D_04</run>
        <expect>MATCH status (runner has latest source).</expect>
        <if_mismatch>Coordinate with AE before upload.</if_mismatch>
      </step>
      <step>
        <run>comp-validate D_04 --artifact /tmp/platinum_accounts_sample.json</run>
        <expect>Exit 0 after dry-run build.</expect>
        <if_mismatch>Iterate on math until validator is clean.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast platinum/accounts/{*}/summary.json</run>
        <expect>Consumer set unchanged — no surprise downstream reader.</expect>
        <if_mismatch>Flag to COO before signaling DE/DT.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Independent of every other wave; ships immediately.
  </dependencies>

  <next>
    Post-commit: push to S3 + trigger bd-gold-qa-runner dry-run. On validator clean, signal COO;
    COO signals DT for post-nightly spot-check of the affected advisor/account surfaces via
    `/frontend-dev` Skill (AdvisorPublicProfile rfs tiles + AdvisorBookView rfs cards).
  </next>
</task_order>
