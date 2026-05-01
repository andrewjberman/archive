<task_order>
  <metadata>
    <id>ADVI_49FRECN.002</id>
    <project>ADVI_49FRECN</project>
    <title>Phase 1 Track 1 — Extend D_04 to Emit out_of_scope_accounts.json (Buckets A + B + C2/C3)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-01</issued_date>
    <status>open</status>
    <priority>P0 — closes 530 of 590 missing accounts (88% by count, ~5% by $); structurally clean (no C_03 invariant change)</priority>
    <estimated_effort>1d (D_04 extension + emit JSON + verify)</estimated_effort>
  </metadata>

  <context>
    Phase 0 (`9088aa2f8` + `21e65922d`) confirmed: 590 accounts missing from gold; gap is 100% scope-driven (CASE_A). Andrew's design ruling 2026-05-01:

      "The accounts that are out of scope via not having transactions, those ones we simply
       need to be able to keep in a summary json somewhere, probably extend D_04 to create
       this out-of-scope json, and the front end can then call and manipulate that data
       however makes sense visually."

    This TO covers the simple track. Bucket C1 (60 large recently-created accounts WITH transactions, $55M, the 77% AUA lever) is handled separately under .002.5 sub-investigation + a follow-on Track 2 fix.

    Bucket scope for THIS TO:
    - Bucket A: 44 non-investment (CreditCard / Bank / Mortgage / LLC / Loans / Savings)
    - Bucket B: 11 brand-new (no transaction history — onboarding lag)
    - Bucket C2/C3: 475 dormant / near-zero (investment, no current positions)

    Total: 530 accounts. AUA: ~$3.3M (small dollar but large count).

    DS~B's bucket classification + account-id list lives in their .001B session log + their slice in `docs/architecture/49F_RECONCILIATION_2026-05-01.md` (commit `21e65922d`). Read the Slice B section to anchor the bucket mappings before extending D_04.
  </context>

  <objective>
    Extend `D_04` (or its appropriate canonical script in the BD gold chain) to emit
    a new side-write artifact at `gold/artifacts/49f/out_of_scope_accounts.json` per
    snapshot date. Front-end DE will consume this artifact to surface out-of-scope
    accounts in the UI (separate visual treatment, footnote on AUA totals, etc. — out
    of scope for THIS TO). C_03 stays untouched; positions-required invariant preserved.
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>Identify the correct emission script</title>
      <detail>
        Use `comp-pipescript io D_04` first to confirm D_04 is the right home for the side-write,
        OR identify a different script (D_00b, D_00c, D_07) if the data inputs make those
        a cleaner fit. Document the choice. Out-of-scope accounts originate from the silver
        allocations feed, not from positions — pick the script that already reads allocations.
      </detail>
    </ac>

    <ac id="2">
      <title>Out-of-scope detection logic</title>
      <detail>
        For each snapshot date, an account is "out-of-scope" if BOTH:
        - Account is present in silver/allocations (or equivalent BD silver feed of "all accounts")
        - Account is NOT present in C_03's account_performance gold output

        Classify each out-of-scope account into a bucket using the same logic DS~B used in .001B:
        - Bucket A: account_type in {CreditCard, Bank, Mortgage, LLC, Loans, Savings} (non-investment)
        - Bucket B: account exists < N days (onboarding lag — pick N based on data; suggest 30d but justify)
        - Bucket C1: investment, has transactions, but no positions today (created within last 12 months by default — but CHECK against DS~B's 60-account list; if mismatch, defer to that list)
        - Bucket C2/C3: investment, dormant or near-zero AUA (no transactions in last 12 months OR allocation < $X threshold)

        **Important:** Bucket C1 accounts are EXCLUDED from this JSON — they are handled by Track 2
        (separate TO; DS~B's .002.5 sub-investigation in progress). Emit only A + B + C2/C3.
      </detail>
    </ac>

    <ac id="3">
      <title>JSON schema</title>
      <detail>
        Path: `gold/artifacts/49f/out_of_scope_accounts.json` (versioned per snapshot date by directory or filename — match existing artifact convention).

        Per-account record schema:
        ```json
        {
          "account_id": "...",
          "advisor": "...",
          "account_type": "...",
          "custodian": "...",          // null if not derivable
          "allocation_aua": 12345.67,
          "classification_bucket": "A" | "B" | "C2" | "C3",
          "exclusion_reason": "non-investment-type" | "onboarding-lag" | "dormant-no-positions" | "near-zero-allocation"
        }
        ```

        Top-level aggregates (also emitted in the same JSON):
        - `total_count`: 530 (expected)
        - `total_allocation_aua`: ~$3.3M (expected)
        - `count_by_bucket`: {"A": 44, "B": 11, "C2": ..., "C3": ...}
        - `aua_by_bucket`: {"A": ..., "B": ..., "C2": ..., "C3": ...}
        - `count_by_advisor`: {"Advisor Name": count, ...}
        - `aua_by_advisor`: {"Advisor Name": aua, ...}
        - `snapshot_date`: "2026-04-29" (or whatever the run date is)
        - `script_version`: "D_04 v..." or whichever script generated it
      </detail>
    </ac>

    <ac id="4">
      <title>Verification against Phase 0 baseline</title>
      <detail>
        On a 2026-04-29 dry-run, the emission should produce ~530 accounts (44 A + 11 B + remaining C2/C3 after subtracting C1 from the original 590). Match DS~B's bucket classification within ±5 accounts; any larger drift means the bucketing logic in #2 disagrees with .001B and needs reconciliation before ship.
      </detail>
    </ac>

    <ac id="5">
      <title>Catalog + dispatch wiring</title>
      <detail>
        - Add the new artifact to `gold_validate_config.yaml` if applicable (check .001B / E_25 patterns for whether diagnostic side-writes go here).
        - Update CATALOG entry (`org/modules/graph/...`) so the new artifact is visible to comp-tools.
        - Confirm dispatch wires correctly: BD nightly chain runs D_04 → emits both existing outputs AND the new out_of_scope_accounts.json.
        - Run `comp-pipescript io D_04` post-edit to confirm the emission is indexed.
      </detail>
    </ac>

    <ac id="6">
      <title>Pre-commit gate + S3 upload + RAVC4</title>
      <detail>
        - Pre-commit gate per CLAUDE.md Rule 14 (py_compile + AST + ruff).
        - Per CLAUDE.md Rule 13: DS owns commit → S3 upload → MATCH cycle.
          1. `git commit` (your DS author identity) + push CLOUD
          2. `aws s3 cp data/black_diamond/scripts/gold/D_04....py s3://opal-data-bd/code/gold/`
          3. `comp-pipescript deployed D_04` → expect MATCH
        - QA dispatch on bd-gold-qa-runner: hand RAVC2 ACK to AE 0.7.0 (PROD trigger via bd-gold-trigger).
        - Verify output JSON exists on S3 + contents match #3 schema + counts match #4 baseline.
        - RAVC4 to CTO with: commit hashes, S3 ETag, run-id, sample of emitted JSON.
      </detail>
    </ac>
  </acceptance_criteria>

  <constraints>
    <constraint>NO change to C_03. Positions-required invariant stays.</constraint>
    <constraint>Bucket C1 accounts EXCLUDED from this JSON — handled separately under Track 2.</constraint>
    <constraint>49F-only scope. Side-write path under `gold/artifacts/49f/` is partner-prefixed for future expansion (Inflection, Cottonwood may want analogous artifacts later).</constraint>
    <constraint>Pre-commit gate + Rule 13 S3 upload mandatory.</constraint>
    <constraint>Coordinate with DS~B if bucket-membership classification produces drift vs .001B — DS~B is source of truth on the bucket assignments.</constraint>
  </constraints>

  <gates_and_dependencies>
    <gates>None — Phase 0 closed; ready to ship.</gates>
    <unblocks>Front-end DE work to surface out-of-scope accounts in the UI (separate follow-on, not in this TO).</unblocks>
    <related>.002.5 (DS~B sub-investigation on C1) runs in parallel; no dependency.</related>
  </gates_and_dependencies>

  <ravc_target>
    <to>1.0.0_SA_CTO</to>
    <on_complete>RAVC4 with commit refs + S3 ETag + run-id + sample JSON output + count reconciliation against DS~B's Phase 0 bucket numbers.</on_complete>
  </ravc_target>

  <inputs>
    <input>docs/architecture/49F_RECONCILIATION_2026-05-01.md (Slice B — bucket classifications + 590-account list)</input>
    <input>DS~B .001B session log</input>
    <input>Phase 0 commits: 9088aa2f8, 21e65922d</input>
    <input>Andrew design directive 2026-05-01 (D_04 extension approach)</input>
  </inputs>
</task_order>
