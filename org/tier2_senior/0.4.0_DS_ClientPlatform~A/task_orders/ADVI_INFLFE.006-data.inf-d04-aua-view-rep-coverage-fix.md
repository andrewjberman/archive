<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLFE.006-data</id>
    <project>ADVI_INFLFE</project>
    <title>INF_D_04 _build_aua_view + _build_geo_view: apply AUDIT-003 rep-coverage gate (aum_snapshot partial-rep override causing $182.5M in partner_analytics granularity files + NMNC/NMEC collapse)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>pending</status><!-- GO issued same session. Priority: HIGH — blocks all correct portal AUA display for Inflection. -->
    <priority>high</priority>
    <estimated_effort>~45min (surgical fix + rerun + comp-validate)</estimated_effort>
  </metadata>

  <references>
    <ref type="root_cause_audit">COO session 60 S3 investigation 20260506T~1530Z: partner_analytics_quarterly.json views.aua.donut.total = $182,552,380.96; canonical dashboard.json headline.total_aua = $199,649,186.31. Same run (10:42Z). Discrepancy = aum_snapshot partial-rep override not gated.</ref>
    <ref type="audit_003_precedent">AUDIT-003 (commit 28dcb8b56): applied INFLECTION_REP_IDS.issubset(snapshot_rep_ids) full-rep coverage gate to build_dashboard(). Rep 6 (joe_brandenbrug) is missing from aum_snapshot (rep_ids in snapshot: ['3','11','12'] only). Gate correctly falls back to holdings ($199.6M). SAME gate was NOT applied to _build_aua_view or _build_geo_view.</ref>
    <ref type="aum_snapshot_state">silver/aum_snapshot/2026-04-29.parquet: rep_ids = ['3','11','12'], total managed_value = $182,552,380.96. Rep 6 absent → partial-rep snapshot. INFLECTION_REP_IDS = {'3','6','11','12'} (INF_D_04:102).</ref>
    <ref type="nmnc_collapse">_build_aua_view:1918-1926: when use_aum=True, NMNC segment AUA is summed from hh_managed.index (aum_snapshot household_ids). Lifecycle classification uses accounts_dim household_ids. ID mismatch → nmnc_ids not found in hh_managed.index → nmnc_aua=0, nmec_aua=0, all clients collapse to "existing". NMNC should be $174M (201 accounts per nmec_nmnc_nna.json).</ref>
    <ref type="affected_files">platinum/firm/partner_analytics_quarterly.json (views.aua.donut.total=$182.5M), platinum/firm/partner_analytics_monthly.json (same), platinum/firm/partner_analytics_annual.json. Also possible: timeseries_overview.json 2026Q2=$189.2M (investigate separately — may have different AUA source path).</ref>
    <ref type="gold_script">data/orion/scripts/gold/INF_D_04.client_portal_summary.py — functions _build_aua_view (line 1878) and _build_geo_view (line 1681).</ref>
  </references>

  <context>
    AUDIT-003 (commit 28dcb8b56) fixed INF_D_04.build_dashboard() by adding a full-rep
    coverage gate: aum_snapshot override is only applied when INFLECTION_REP_IDS is a
    subset of the snapshot's rep_ids. Since rep 6 is absent from the latest aum_snapshot,
    the gate correctly falls back to holdings.market_value.sum() = $199,649,186.31.

    AUDIT-003 did NOT update _build_aua_view or _build_geo_view. Both functions use a
    weaker gate (column presence only) and unconditionally apply the aum_snapshot override.
    Result: partner_analytics_quarterly/monthly/annual.json all contain $182.5M (missing
    rep 6's $17M portfolio) instead of the canonical $199.6M.

    Secondary consequence: NMNC/NMEC segments are zero. When use_aum=True, segment AUA
    is keyed against hh_managed.index (aum_snapshot household_ids). If lifecycle-classified
    NMNC household_ids (from accounts_dim) don't match aum_snapshot household_ids, all
    clients collapse to "existing". The use_aum=False path (holdings) does NOT have this
    issue — it uses hh['aua'].sum() directly from _compute_hh_lifecycle, which correctly
    produces NMNC/NMEC splits.

    Portal impact: Distribution tab + Mix view show $182-187M instead of $199.6M.
    AUA toggle shows no NMNC/NMEC breakdown. Andrew requirement: "All AUA numbers have to
    agree, no matter how we get there."
  </context>

  <steps>
    <step id="1">
      <objective>Read and understand the existing _build_aua_view and _build_geo_view functions.</objective>
      <run>
        Read data/orion/scripts/gold/INF_D_04.client_portal_summary.py.
        Locate:
        - _build_aua_view (line ~1878): current use_aum gate (column-only check)
        - _build_geo_view (line ~1681): similar use_aum gate
        - build_dashboard (line ~715): the AUDIT-003 override_safe pattern to replicate
        - INFLECTION_REP_IDS constant (line 102)
      </run>
    </step>

    <step id="2">
      <objective>Apply AUDIT-003 rep-coverage gate to _build_aua_view.</objective>
      <run>
        In _build_aua_view, replace the current use_aum gate:
          use_aum = aum_snapshot is not None and not aum_snapshot.empty \
              and 'managed_value' in aum_snapshot.columns \
              and 'household_id' in aum_snapshot.columns

        With the AUDIT-003 rep-coverage pattern:
          override_safe = False
          if (aum_snapshot is not None and not aum_snapshot.empty
                  and 'managed_value' in aum_snapshot.columns
                  and 'rep_id' in aum_snapshot.columns):
              snapshot_rep_ids = set(aum_snapshot['rep_id'].astype(str).unique())
              if INFLECTION_REP_IDS.issubset(snapshot_rep_ids):
                  override_safe = True
              else:
                  missing = INFLECTION_REP_IDS - snapshot_rep_ids
                  log(f'WARN [_build_aua_view]: aum_snapshot SKIPPED: missing rep_ids {missing} -- using canonical holdings')
          use_aum = override_safe and 'household_id' in (aum_snapshot.columns if aum_snapshot is not None else [])

        Also update the DIAGFIX.002a docstring to note AUDIT-003 parity fix:
        Remove or update the comment that says "$182.6M per-HH managed_value" -- that
        comment is now stale (AUDIT-003 confirmed holdings is canonical).
      </run>
      <expect>
        With current aum_snapshot (rep_ids=['3','11','12'], rep 6 missing):
        override_safe = False → use_aum = False → total_aua = holdings.market_value.sum() = $199.6M.
        NMNC/NMEC segments computed from holdings-based lifecycle path.
      </expect>
    </step>

    <step id="3">
      <objective>Apply same fix to _build_geo_view.</objective>
      <run>
        In _build_geo_view (line ~1706), current gate:
          use_aum = (aum_snapshot is not None and not aum_snapshot.empty
                     and 'managed_value' in aum_snapshot.columns
                     and 'household_id' in aum_snapshot.columns)

        Apply the same override_safe pattern as step 2.
        _build_geo_view uses aum_snapshot for geo AUA totals (states/cities).
        Without the gate, geo view also reads partial-rep $182.5M.
      </run>
    </step>

    <step id="4">
      <objective>Pre-commit gate.</objective>
      <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_04.client_portal_summary.py</run>
      <expect>py_compile + ds-precommit-check.py + ruff all exit 0. from __future__ import annotations already present (Rule 15 — verify).</expect>
    </step>

    <step id="5">
      <objective>Commit.</objective>
      <run>
        .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~A &lt;0.4.0_DS_ClientPlatform~A@opal.agent&gt;" \
          -m "fix(ADVI_INFLFE.006-data): _build_aua_view + _build_geo_view rep-coverage gate parity with AUDIT-003" \
          -- data/orion/scripts/gold/INF_D_04.client_portal_summary.py
        git push
      </run>
    </step>

    <step id="6">
      <objective>Rerun INF_D_04 + INF_09 on inf-gold-qa-runner.</objective>
      <run>
        Upload fixed script to S3:
          aws s3 cp data/orion/scripts/gold/INF_D_04.client_portal_summary.py \
            s3://opal-data-inf/code/gold/INF_D_04.client_portal_summary.py

        Dispatch via SSM (inf-gold-qa-runner):
          export OUTPUT_PREFIX=platinum/  (mandatory -- non-login shell; see feedback memory)
          Run INF_D_04 --upload, then INF_09 --upload --skip-sub-scripts
          (--skip-sub-scripts skips re-running INF_D_00c/INF_D_02; only need INF_D_04 rerun)

        Verify S3 writes:
          aws s3 cp s3://opal-data-inf/platinum/firm/partner_analytics_quarterly.json - \
            | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['views']['aua']['donut']['total'], [s['key'] for s in d['views']['aua']['donut']['segments']])"

        Expected: total ~$199.6M, segments = ['nmnc', 'existing'] (nmec likely $0 → omitted per line 1945 guard).
      </run>
      <expect>
        partner_analytics_quarterly.json views.aua.donut.total ≈ $199,649,186.31.
        NMNC segment present with aua ≈ $174M.
        partner_analytics_monthly.json and _annual.json similarly updated.
      </expect>
    </step>

    <step id="7">
      <objective>comp-validate.</objective>
      <run>
        comp-validate INF_D_04.client_portal_summary.py --artifact /tmp/partner_analytics_quarterly.json
        (download the updated file from S3 first for local validate artifact)
      </run>
      <expect>Exit 0 all-pass or ADVISORY (no ERROR-class). Per COMP_VALIDATE_PROTOCOL.</expect>
    </step>

    <step id="8">
      <objective>RAVC to COO.</objective>
      <run>
        Send RAVC to 2.0.0_SA_COO:
        - Commit hash
        - partner_analytics_quarterly.json views.aua.donut.total (must be ~$199.6M)
        - NMNC segment aua value
        - NMEC segment aua value (likely $0 → omitted)
        - Existing segment aua value
        - partner_analytics_monthly.json views.aua.donut.total
        - comp-validate exit code
        - Note on timeseries_overview.json 2026Q2 value (was $189.2M before fix — check if it also updated)
      </run>
    </step>
  </steps>

  <acceptance_criteria>
    <criterion id="AC1">partner_analytics_quarterly.json views.aua.donut.total = $199,649,186.31 (±$1K for rounding).</criterion>
    <criterion id="AC2">NMNC segment present in views.aua.donut.segments with aua ≈ $174M (per nmec_nmnc_nna.json nmnc_aua=$174,184,477.25).</criterion>
    <criterion id="AC3">partner_analytics_monthly.json views.aua.donut.total = $199,649,186.31 (same run).</criterion>
    <criterion id="AC4">Pre-commit gate PASS: py_compile + ds-precommit-check.py + ruff all exit 0.</criterion>
    <criterion id="AC5">comp-validate exit 0 (all-pass or ADVISORY only; no ERROR-class).</criterion>
    <criterion id="AC6">RAVC to COO includes all evidence fields from step 8.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="before_edit">Read INF_D_04.client_portal_summary.py. Locate _build_aua_view, _build_geo_view, build_dashboard (AUDIT-003 pattern), INFLECTION_REP_IDS.</phase>
    <phase id="before_commit">.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_D_04.client_portal_summary.py</phase>
    <phase id="after_rerun">comp-validate INF_D_04.client_portal_summary.py --artifact (downloaded partner_analytics_quarterly.json)</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>RAVC to COO only. DT INFLFE.006 frontend TO gates on this data fix landing (correct data in platinum before frontend debugging).</item>
    <item>Do NOT edit DT/AE files. DS~A scope = INF_D_04.client_portal_summary.py only.</item>
    <item>gold_freshness_config.yaml silver/transactions path fix (separate FLAG from COO) may be done in the same session if convenient, but is not blocking this TO.</item>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT rerun INF_D_00c or INF_D_02 as part of this fix (use --skip-sub-scripts on INF_09). Those are unchanged.</rule>
    <rule>Do NOT modify the aum_snapshot logic in build_dashboard — that function already has the correct AUDIT-003 gate.</rule>
    <rule>Do NOT remove aum_snapshot loading from main() — it is still needed (as a fallback source when all reps are present, or for future use).</rule>
  </do_not>

  <go_signal>
    <issued_at>20260506T~1535Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Root cause confirmed via S3 investigation: aum_snapshot rep_ids=['3','11','12'] (rep 6 missing), use_aum=True in _build_aua_view bypasses full-rep gate. Same fix as AUDIT-003 applied to build_dashboard. Execute steps 1-8. RAVC to COO on complete.</message>
  </go_signal>
</task_order>
