<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-13-reborn-w6-003</id>
    <issued_by>Andrew / 0.4.0_DS_ClientPlatform (self-authored per directive)</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-13</date>
    <status>pending</status>
    <project_code>ADVI_REBORN</project_code>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_REBORN_LEADERBOARD_FEES_ROLES_FIX.md</ref>
    <ref type="prior_work">W6-001 (D_04 fee bucket passthrough), W6-002 (frontend fallback removal)</ref>
  </references>

  <objective>
    Add `role_combination_breakdown` to each advisor entry in
    `gold/artifacts/employee_leaderboard.json`. This partitions each advisor's accounts
    into non-overlapping groups by full role-set membership (e.g. "architect",
    "architect|implementor", "consultant|implementor"), then for each group emits
    fee_paying / no_fee AUA correctly deduplicated. The frontend can then sum
    any role subset exactly: include a combination if it intersects the selected
    role set. Each account counted once. `sum(all combos.fee_paying.aua)` =
    `fee_breakdown.fee_paying.aua` (canonical firm deduplicated total).
  </objective>

  <context>
    Root cause of W6-002 residual bug (discovered by Andrew):

    The existing per-role `role_breakdown[role].fee_paying.aua` uses split weights
    (1/n_roles_per_account) to make `sum(role.total_aua) == total_aua`. But it does
    NOT make `sum(role.fee_paying.aua) == fee_breakdown.fee_paying.aua`. A billable
    account where Travis is both architect AND implementor contributes split-weighted
    AUA to BOTH `architect.fee_paying` and `implementor.fee_paying` -- double-counting
    it in the fee sum.

    Travis Penfield QTD ground truth (from account_team parquet):
      architect only:        96 rels   $310.4M
      architect+consultant:   6 rels    $57.8M
      implementor only:       8 rels    $32.6M
      architect+implementor:  2 rels    $19.6M
      additional_advisor:     2 rels     $0.9M
      consultant only:        3 rels     $0.7M
      consultant+implementor: 2 rels     $0.4M
      Total (deduped):                 ~$422M

    With role_combination_breakdown, "no implementor + fee-paying" correctly includes
    the architect+implementor and consultant+implementor accounts (because architect /
    consultant is still selected) and excludes only the implementor-only accounts.
    "All roles + fee-paying" = sum(all combos.fee_paying) = fee_breakdown.fee_paying.aua
    = $340.5M (canonical).

    The additive invariant is restored: selecting implementor on top of
    "no implementor + fee-paying" adds exactly the implementor-only combo's
    fee_paying.aua -- it cannot decrease the total.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing code):
    - `comp-pipescript io D_00c` -- confirm reads/writes unchanged.
    - Read `_build_at_role_slice` (D_00c ~line 651) to understand split-weight mechanics.

    Phase 2 (before committing):
    - Dry-run `build_employee_leaderboard` locally; verify Travis Penfield:
      - `sum(all combo.fee_paying.aua)` == `fee_breakdown.fee_paying.aua` within $0.02
      - `sum(all combo.no_fee.aua)` == `fee_breakdown.no_fee.aua` within $0.02
      - `sum(all combo.aua)` == `total_aua` within $0.02
      - Selecting implementor only increases or equals "no implementor + fee-paying"
        total (additive invariant).
    - Check all 162 advisors: log any whose combo sum deviates from fee_breakdown totals.

    Phase 3 (after commit + S3 + trigger):
    - Verify `gold/artifacts/employee_leaderboard.json` Travis QTD entry has
      `role_combination_breakdown` with at least 3 distinct combination keys.
    - Append to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>gold/artifacts/employee_leaderboard.json</shared_resource>
    <shared_resource>data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</shared_resource>
    <also_in_to>ADVI_REBORN.W6-004 (DE -- frontend consumes role_combination_breakdown)</also_in_to>
    <required_action>
      DS ships D_00c + regenerated artifact. DE (W6-004) then updates AdvisorsTab.tsx
      to use role_combination_breakdown for fee-filtered role-subset sums. D_04 trim
      (W6-001) already passes through role_breakdown; new field is additive to artifact.
      D_04 must also pass through role_combination_breakdown -- check and update
      _LEADERBOARD_ROLE_FIELDS logic if needed (it's a top-level entry field, not a
      nested role_breakdown sub-field, so D_04 trim may pass it through automatically
      via the top-level entry copy).
    </required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `gold/artifacts/employee_leaderboard.json` contains `role_combination_breakdown`
       on each advisor entry with at least one combination key.
    2. For every advisor in QTD window:
       `sum(combo.fee_paying.aua for all combos)` == `fee_breakdown.fee_paying.aua` within $0.02.
    3. For every advisor in QTD window:
       `sum(combo.no_fee.aua for all combos)` == `fee_breakdown.no_fee.aua` within $0.02.
    4. Travis Penfield QTD: at least the combinations
       "architect", "implementor", "architect|implementor" present with nonzero AUA.
    5. Travis QTD: additive invariant holds -- sum(combos not containing implementor).fee_paying
       + combos(implementor_only).fee_paying == fee_breakdown.fee_paying.aua.
    6. D_04 passes `role_combination_breakdown` through to `platinum/firm/leaderboard.json`
       (either automatically or via explicit field addition).
    7. DS session log records validation table + Travis sample JSON excerpt.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py</file>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py</file>
    </files>
    <out_of_scope>
      Frontend (DE W6-004). NNA/inflows/outflows per combination (AUA only for now --
      NNA per combination requires canonical_nna join at combination grain, deferred).
    </out_of_scope>
  </scope>

  <schema>
    New field added to each entry in `windows[*].entries[*]`:

    "role_combination_breakdown": {
      "architect": {
        "fee_paying": { "aua": 310400000.00, "account_count": 96, "client_count": 96 },
        "no_fee":     { "aua": 0.00,          "account_count": 0,  "client_count": 0  }
      },
      "architect|consultant": {
        "fee_paying": { "aua": 57800000.00, "account_count": 6, "client_count": 6 },
        "no_fee":     { "aua": 0.00,         "account_count": 0, "client_count": 0 }
      },
      "architect|implementor": {
        "fee_paying": { "aua": 19600000.00, "account_count": 2, "client_count": 2 },
        "no_fee":     { "aua": 0.00,         "account_count": 0, "client_count": 0 }
      },
      ...
    }

    Combination key: "|".join(sorted(roles)), e.g. "architect|implementor".
    Single-role combo: just the role name, e.g. "architect".
    Sorted alphabetically so keys are deterministic.

    Frontend aggregation rule (for DE W6-004):
      For selected roles S and feeView F:
        total = sum(
          combo[F].aua
          for combo_key, combo in role_combination_breakdown.items()
          if any(role in selected_roles for role in combo_key.split("|"))
        )
  </schema>

  <deliverables>
    - Commit to CLOUD with DS author.
    - S3 upload D_00c + D_04 to opal-data-bd/code/gold/.
    - Trigger D_00c + D_04 single-script run (two SSM commands via gold_dispatch.sh).
    - Verify regenerated employee_leaderboard.json + leaderboard.json.
    - MCP message DE when artifact live.
    - Session log with compiler tools section.
  </deliverables>
</task_order>
