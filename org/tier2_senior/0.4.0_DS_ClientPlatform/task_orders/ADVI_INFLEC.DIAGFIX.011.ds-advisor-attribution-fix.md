<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFLEC.DIAGFIX.011</id>
    <project>ADVI_INFLEC</project>
    <title>Advisor attribution fix — populate rep_id + servicing rep name in silver/api_dims/accounts_v2 from /Portfolio/Representatives + /Portfolio/Clients?representativeId</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-29</issued_date>
    <status>pending</status>
    <priority>high</priority>
    <estimated_effort>2-3h</estimated_effort>
  </metadata>

  <references>
    <ref type="andrew_directive">Andrew 2026-04-29 (post DIAGFIX.010 Phase 5 RAVC): "we are back up to 198.87m which is more reasonable of a number" + "I think he has his own advisor number and we need to figure it out" — confirming Joe Brandenburg is the missing advisor</ref>
    <ref type="discovery">Joe Brandenburg = rep_id=6 in Orion (`TAN Inflection Brandenburg`, 21 households, 67 accounts, $16.22M). Confirmed via GET /api/v1/Portfolio/Representatives + GET /api/v1/Portfolio/Clients?representativeId=6.</ref>
    <ref type="root_cause">data/orion/scripts/silver/convert_orion_api_to_silver.py:410 build_accounts_v2() explicitly sets `out['rep_id'] = None`. NewPortfolio API response carries only `representativeName` field showing 3 firm-level rep names (Inflection Wealth Management 818 / Peter Lee 29 / Patrick Scanlan 3). Brandenburg's 67 accounts roll up as 'Inflection Wealth Management' because that's NewPortfolio's primary rep field. Servicing rep is captured in a separate Orion endpoint.</ref>
    <ref type="orion_endpoints">
      GET /api/v1/Portfolio/Representatives (no params) — returns all 18 reps with id/repNo/fullName/firstName/lastName/isActive/status/brokerDealer/riaName/etc. Sync, ~1s, ~19KB
      GET /api/v1/Portfolio/Clients?representativeId={N} — returns full household-level detail for a given rep. Sync, varies by rep. For rep 6: 21 households.
    </ref>
    <ref type="related">DIAGFIX.010 (Orion-native classification) shipped — INF_I_D03 already routes by representative_name slugified to advisor_key. Once accounts_v2 surfaces Brandenburg as a distinct rep_name, gold scripts pick him up automatically as a first-class advisor with no code changes.</ref>
  </references>

  <context>
    DIAGFIX.010 confirmed Orion's rep master list has 18 reps, 7 of which are Inflection-relevant
    (3 IWM/Lee/Scanlan currently in our data + 4 missing: Brandenburg rep 6, Brandenburg/IWM rep 7,
    Brandenburg/Lee rep 8, Soderblom rep 10). Reps 7/8/10 are 0-household joint placeholders today.

    Brandenburg's 21 households + 67 accounts ARE present in our current bronze + silver pulls
    (his $16.22M is included in the $197.86M total). The gap is ATTRIBUTION ONLY — they all roll
    up under "Inflection Wealth Management" instead of "Joe Brandenburg".

    Once accounts_v2.rep_id and accounts_v2.representative_name are correctly populated, downstream
    gold scripts (INF_I_D03, INF_D_00c leaderboard, INF_D_02 advisor_client_detail, etc.) will
    automatically generate per-Brandenburg artifacts (composition.json, leaderboard rows, drilldown
    pages) because they all slugify representative_name to advisor_key.

    Bonus: this same fix makes the rep master list available as a silver dim
    (silver/api_dims/representatives) so future advisor-related features (ADV reports, fee splits,
    custody attribution, etc.) have a clean source of truth for advisor metadata.
  </context>

  <scope>
    PHASE 1 — bronze pull (representatives + household mapping):
    Create data/orion/manual_api/pull_inflection_representatives.py.
      - GET /api/v1/Portfolio/Representatives — capture all 18 rep records as bronze JSON.
      - For each Inflection-relevant rep_id [3, 6, 7, 8, 10, 11, 12]: GET /api/v1/Portfolio/Clients?representativeId={N}.
        Capture (household_id, rep_id, rep_name) tuples. Concatenate all into one bronze artifact.
      - Output:
          s3://opal-data-inf/bronze/orion-api-v2/{date}/representatives.json (18 rows)
          s3://opal-data-inf/bronze/orion-api-v2/{date}/household_rep_mapping.json (~270 rows)
      - Local mirror under data/orion/manual_api/pulls/.

    PHASE 2 — silver dims:
    Add 2 new dim builders to data/orion/scripts/silver/convert_orion_api_to_silver.py:
      - build_representatives() -> silver/api_dims/representatives/snapshot_date={date}/data.parquet
        Schema: rep_id (Int64), rep_no (string), full_name (string), first_name, last_name,
        is_active (bool), status, broker_dealer, ria_name, households (int — count from rep master),
        snapshot_date, source_system='orion-api'.
      - build_household_rep_mapping() -> silver/views/household_rep_mapping/snapshot_date={date}/data.parquet
        Schema: household_id (string), rep_id (Int64), rep_name (string), snapshot_date,
        source_system='orion-api'.
        Treat as Inflection-scoped (only the 7 reps pulled in Phase 1).

    PHASE 3 — augment build_accounts_v2():
    In data/orion/scripts/silver/convert_orion_api_to_silver.py build_accounts_v2():
      - REMOVE line 410: `out['rep_id'] = None`
      - LOAD silver/views/household_rep_mapping for the same snapshot_date
      - JOIN on household_id, populating rep_id + override representative_name with the
        mapping's rep_name (servicing rep). Keep representative_name fallback to the original
        NewPortfolio value if mapping is absent.
      - Add advisor_firm_rep_name fallback chain: mapping.rep_name -> NewPortfolio.representativeName -> 'inflection_wealth_management' (existing default).

    PHASE 4 — re-run silver + verify:
    Run the silver pipeline:
      python3 data/orion/scripts/silver/convert_orion_api_to_silver.py --dim representatives --upload
      python3 data/orion/scripts/silver/convert_orion_api_to_silver.py --dim household_rep_mapping --upload  
      python3 data/orion/scripts/silver/convert_orion_api_to_silver.py --dim accounts_v2 --upload
    (or whatever the existing CLI shape is)
    Verify:
      - silver/api_dims/representatives/.../data.parquet contains 18 rows with Brandenburg at rep_id=6
      - silver/views/household_rep_mapping has 21 Brandenburg households
      - silver/api_dims/accounts_v2 rep_id non-null on Brandenburg's 67 accounts
      - accounts_v2.representative_name shows "Joe Brandenburg" on those 67 accounts

    PHASE 5 — re-run gold chain:
    Run INF_I_D03 to regenerate firm + per-advisor compositions:
      python3 data/orion/scripts/gold/INF_I_D03.composition_artifacts.py --upload
    Verify:
      - platinum/advisors/joe_brandenburg/composition.json exists on S3
      - Brandenburg's $16.22M shows in the new advisor composition
      - firm_composition.json totals unchanged (his data was already in firm view)
      - INF_I_D02d composer auto-republishes with no metadata change (orion_native_v1 propagation works)

    PHASE 6 — RAVC to COO:
    - Brandenburg's composition.json on S3 (size, asset_class breakdown)
    - Updated rep counts in firm view (4 advisors: IWM-residual, Lee, Scanlan, Brandenburg)
    - Confirm $198.87M total (matches Andrew's UI-with-Brandenburg figure)
    - Document any other reps that surfaced (Soderblom rep 10 likely 0 households still)

    Pre-commit gate + S3 upload + chain registration:
    - .tools/ds-commit-gate.sh on all modified scripts
    - aws s3 cp each script to s3://opal-data-inf/code/{manual_api,silver,gold}/
    - MD5 MATCH verification
    - AE 0.6.1 to register pull_inflection_representatives.py in orion-gold-dispatch.sh CHAIN_FULL.
      Daily cadence, FIRST in the chain (no upstream deps).
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_I_D03 (already built; no changes here)</run>
        <expect>SKIPPED — Orion scripts not in BD-pipeline graph (documented gap)</expect>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh on each modified .py file</run>
        <expect>Exit 0 — py_compile + AST + ruff all pass</expect>
        <if_mismatch>STOP. Fix gate failures first.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after S3 upload">
      <step>
        <run>MD5 MATCH verification on each uploaded script (registry gap precedent)</run>
        <expect>Local md5 == S3 ETag for each.</expect>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <criterion id="1">
      bronze/orion-api-v2/{date}/representatives.json + household_rep_mapping.json exist on S3.
      18 reps + ~270 household-rep tuples.
    </criterion>
    <criterion id="2">
      silver/api_dims/representatives/snapshot_date={date}/data.parquet exists with 18 rows.
      Joe Brandenburg present at rep_id=6 with households=21.
    </criterion>
    <criterion id="3">
      silver/views/household_rep_mapping/snapshot_date={date}/data.parquet exists.
      21 Brandenburg households present (cids 24, 32, 51, 63, 126, 141, 161, 190, 219, 221, 223,
      284, 334, 394, 403, 449, 481, 497, 515, 540, 550).
    </criterion>
    <criterion id="4">
      silver/api_dims/accounts_v2.rep_id non-null on Brandenburg's 67 accounts. representative_name
      = 'Joe Brandenburg' on those 67 rows.
    </criterion>
    <criterion id="5">
      platinum/advisors/joe_brandenburg/composition.json exists on S3 with $16.22M ± rounding
      and Orion-native classification (orion_native_v1 metadata).
    </criterion>
    <criterion id="6">
      ds-commit-gate.sh exit 0 on all modified scripts. S3 deploy MATCH for each.
    </criterion>
    <criterion id="7">
      RAVC to 2.0.0_SA_COO: commit hash, S3 deploy MATCH, advisor count before/after,
      Brandenburg composition verification, total firm AUA confirmation.
    </criterion>
  </acceptance_criteria>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" status="complete">DIAGFIX.010 Phase 1+2 — silver/api_dims/assets_v2 + INF_I_D03 Orion-native classifier already shipped</dependency>
    <dependency agent="0.6.1_AE_PartnerETL" status="will_engage">
      AE 0.6.1 chain registration of pull_inflection_representatives.py in orion-gold-dispatch.sh
      after Phase 1 commit lands. Pattern same as DIAGFIX.010 registrations.
    </dependency>
    Independent of AE 0.6.1's new DIAGFIX.009 (holdings pricing strategy).
  </dependencies>

  <cross_domain_coordination>
    <coordination>
      AE 0.6.1: register new bronze pull script in CHAIN_FULL CATALOG. New silver dim
      (representatives) and silver view (household_rep_mapping) consumed by augmented
      build_accounts_v2(); make sure CHAIN ordering reflects the dependency.
    </coordination>
    <coordination>
      DE 0.4.0: no immediate action. Once Brandenburg's composition.json lands, advisor drilldown
      pages will auto-render him as a first-class advisor (slug: joe_brandenburg). DE may want
      to verify the page renders correctly and add him to any hardcoded advisor lists.
    </coordination>
  </cross_domain_coordination>

  <commit_identity>
    Phase 1 (bronze pull):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
      -m "feat(ADVI_INFLEC.DIAGFIX.011 Phase 1): pull_inflection_representatives.py — reps + household-rep mapping bronze pull" \
      -- data/orion/manual_api/pull_inflection_representatives.py

    Phase 2+3 (silver dims + accounts_v2 augment):
    .tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
      -m "feat(ADVI_INFLEC.DIAGFIX.011 Phase 2+3): silver representatives + household_rep_mapping dims + accounts_v2 rep_id population" \
      -- data/orion/scripts/silver/convert_orion_api_to_silver.py
  </commit_identity>
</task_order>
