<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-28-infship-b4-9dim-spec-doc</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-28</date>
    <status>complete</status><!-- DS~A 2026-04-28: shipped 8fb09338 (INFLEC_DIMS_AND_TRANSACTIONS.md v0.1, 9-dim operational catalog) + 0629d129 (v0.2 patch per DS~B peer-review); session log 40de48e6. Reconciled 2026-04-29 startup. -->
    <project_code>ADVI_INFSHIP</project_code>
    <to_serial>B4</to_serial>
    <priority>HIGH</priority>
    <prd>docs/architecture/ADVI_INFSHIP.md (Phase 1.5 Infrastructure formalization sub-wave)</prd>
  </metadata>

  <objective>
    Author the single source-of-truth specification document for the
    Inflection bronze/silver dimension catalog at
    `docs/architecture/INFLEC_DIMS_AND_TRANSACTIONS.md`. The doc enumerates
    the 9 dims + transactions identified during INFSHIP Phase 1, with API
    contract, refresh cadence, downstream gold/platinum dependencies, and
    lane ownership per dim. This doc gates the AE-side bronze/silver
    runner TF + boot scripts (B1, B2) — without it, AE has to reverse-
    engineer the dim list from scattered DS pull scripts.
  </objective>

  <context>
    Andrew direct (~06:15Z, 2026-04-28, via COO MCP):

      "Probably relevant for you and CTO to check in with 0.6.1_AE and
       make sure they have TOs regarding putting together the actual
       infrastructure to manage all this. We probably want bronze/silver
       runners that use the manual_api to pull daily data and merge to
       silver parquets just like how bd-pipeline does it. Probably need to
       figure out what all dims and transactions we need and start setting
       up bronze/silver vms for inf-pipeline... The benefit to our scenario
       is we don't even need to scrape CSVs we can just have them use the
       manual api approach"

    9 dims have been identified during INFSHIP Phase 1 across DS lanes:

    SHIPPED (silver/api_dims/* live in S3):
    1. household — DS~A
    2. performance — DS~A
    3. activity — DS~A (canonical AUA $199.4M)
    4. billing — DS~B
    5. tax_unrealized — DS~B (costBasisOptionId=0)
    6. tax_realized — DS~B (costBasisOptionId=1)
    7. assets — DS~D Path C (canonical-sourced; Path A vendor-blocked per
       INFSHIP.A2)

    IN-FLIGHT or PLANNED:
    8. accounts_v2 — DS~A planning (NewPortfolio endpoint, HAR(5))
    9. transactions — DS~A probe v0.2 (Custom Reports endpoint, HAR(4))

    All 9 are API-pullable; no CSV scraping required. This is the
    foundation simplification Andrew called out.

    Path X architecture (CTO ratified): single inf-bronze-runner EC2 runs
    all 9 dim pulls in sequence on daily schedule; sequenced silver chain
    follows. B4 enumerates the 9; B1 builds the runner; B2 builds silver
    chain; B3 formalizes QA runner.

    Existing DS pull scripts that B4 catalogs:
    - data/orion/scripts/pull_inflection_household.py (DS~A)
    - data/orion/scripts/pull_inflection_performance.py (DS~A)
    - data/orion/scripts/pull_inflection_activity.py (DS~A)
    - data/orion/scripts/pull_inflection_billing.py (DS~B)
    - data/orion/scripts/pull_inflection_tax_unrealized.py (DS~B)
    - data/orion/scripts/pull_inflection_tax_realized.py (DS~B)
    - data/orion/scripts/pull_inflection_assets.py (DS~D)
    - data/orion/scripts/pull_inflection_accounts.py (DS~A; NewPortfolio)
    - data/orion/scripts/pull_inflection_transactions.py (DS~A; Custom Reports)

    (Adjust paths per actual filenames — DS~A holds canonical list)

    Existing silver builders:
    - data/orion/scripts/silver/build_household_dim.py (DS~A)
    - data/orion/scripts/silver/build_performance_dim.py (DS~A)
    - data/orion/scripts/silver/build_activity_dim.py (DS~A)
    - data/orion/scripts/silver/build_billing_dim.py (DS~B)
    - data/orion/scripts/silver/build_tax_unrealized_dim.py (DS~B)
    - data/orion/scripts/silver/build_tax_realized_dim.py (DS~B)
    - data/orion/scripts/silver/build_assets_dim.py (DS~D Path C)
    - data/orion/scripts/silver/build_accounts_v2_dim.py (DS~A; planned)
    - data/orion/scripts/silver/build_transactions_dim.py (DS~A; planned)

    The shared envelope library: `data/orion/scripts/silver/_orion_api_silver_lib.py` (DS~A).

    Existing API endpoint catalog: `docs/architecture/INFLEC_API_ENDPOINTS_CATALOG.md` (DS~A 31c72a47, updated by DS~D for Path C). B4 doc cross-references but does not duplicate; B4 is the OPERATIONAL view (cadence, dependencies, ownership), the existing catalog is the API CONTRACT view (paths, payloads, response shapes).
  </context>

  <files_to_modify>
    <file action="create">docs/architecture/INFLEC_DIMS_AND_TRANSACTIONS.md</file>
  </files_to_modify>

  <spec_summary>
    Doc structure:

    **§1 — Overview** (1-2 paragraphs)
    Purpose of doc, relationship to INFLEC_API_ENDPOINTS_CATALOG.md, scope
    (Inflection only; future tenants get analogous docs).

    **§2 — Dim catalog table** (one row per dim)
    Columns:
    - Dim name (household / performance / activity / billing / tax_unrealized
      / tax_realized / assets / accounts_v2 / transactions)
    - Bronze script path
    - Silver script path
    - Silver S3 prefix (silver/api_dims/{dim}/snapshot_date=YYYY-MM-DD/)
    - API endpoint (cross-ref to INFLEC_API_ENDPOINTS_CATALOG.md section)
    - Refresh cadence (daily / weekly / monthly per business need)
    - Lane owner (DS~A / DS~B / DS~D)
    - Dependencies (does the silver builder depend on other silvers? e.g.,
      assets silver depends on canonical/holdings — Path C)
    - Status (LIVE / IN-FLIGHT / PLANNED)
    - Notes (e.g., "Path C canonical-sourced pending INFSHIP.A2 vendor
      investigation"; "$140M-vs-$200M reconciliation: $199.4M canonical
      cross-confirmed via Tax Guard B")

    **§3 — Refresh cadence rationale** (per dim)
    Why each dim refreshes at its chosen cadence. E.g., household = daily
    (low cost, need fresh state); billing = weekly (Orion bills cycle
    monthly + daily incremental for late posts); tax = daily (intra-day
    realization activity).

    **§4 — Downstream consumers** (gold + platinum)
    Per-dim, list which gold script(s) consume the silver. E.g., billing
    silver consumed by INF_D_04 (header_metrics fee_earning) + INF_D_02
    (book.json + detail.json summary.billing). This is the dependency
    graph that B1's bronze runner needs to honor (dim X must land before
    gold script Y runs).

    **§5 — Sequence requirements** (for B1 runner orchestration)
    Order in which dims must be pulled if any have inter-dim dependencies
    in silver. E.g., household → performance (performance silver may join
    on household_id from household silver). Identify any dim that can
    parallelize within sequence.

    **§6 — Future onboarding template**
    1-paragraph placeholder noting that this doc structure is the template
    for any future small-firm tenant onboarding (Fideles, etc). Not full
    template; just the placeholder.

    **§7 — Open questions / out-of-scope**
    - Path C source-of-truth for assets pending A2 vendor investigation
    - INFGRD.004 chain rerun on Andrew hold (affects assets silver freshness)
    - Future: per-account batching for Asset grouping if A2 unblocks (Track 2)

    Estimated final doc length: 200-400 lines (data-heavy table format,
    minimal prose).
  </spec_summary>

  <acceptance_criteria>
    <ac>1. Doc lands at `docs/architecture/INFLEC_DIMS_AND_TRANSACTIONS.md`
        and is committed via safe-commit.sh + pushed to origin/CLOUD.</ac>
    <ac>2. All 9 dims enumerated with all columns populated. Cadence /
        owner / dependencies fields are AUTHORITATIVE — AE will dispatch
        B1/B2 runner orchestration based on this doc.</ac>
    <ac>3. Cross-references to existing artifacts:
        - INFLEC_API_ENDPOINTS_CATALOG.md (API contract)
        - INFGRD .json (silver scope filters)
        - INFSHIP PRD (Phase 1 ship arc)
        - INFSHIP.A2 backlog TO (assets API deferral)</ac>
    <ac>4. Sequence requirements (§5) are unambiguous. AE B1 boot script
        author must be able to translate §5 directly into bash/python
        sequencing without further DS clarification.</ac>
    <ac>5. RAVC4 to CTO with commit ref + a 3-bullet summary of any
        decisions you made on cadence (default to your judgment if no
        Andrew direction; flag for ratification at session-end).</ac>
  </acceptance_criteria>

  <gates_and_dependencies>
    <gates>None — runs anytime DS~A has bandwidth. Can run in parallel
        with publisher refactors.</gates>
    <unblocks>INFSHIP.B1 (AE bronze runner TF + boot script — needs the
        dim list + sequence) and INFSHIP.B2 (AE silver chain Lambda —
        needs the silver builder paths + sequence).</unblocks>
  </gates_and_dependencies>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 with commit ref + cadence summary + any open
        questions for Andrew ratification.</on_complete>
  </ravc_target>

  <estimated_effort>1-2 hours (data-heavy doc; minimal prose; mostly
      table-filling from your own session knowledge + co-lane work).</estimated_effort>
</task_order>
