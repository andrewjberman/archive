<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-16-advi-rollup-b9b-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-16</date>
    <status>pending</status>
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3-addendum</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP_ADDENDUM_small_account_count.md</ref>
    <ref type="precedent">ADVI_ROLLUP.B9.ds-small-account-count-c08.md — COMPLETE (f2ec98d1 + 9cbfbde5). C_08 carries advisor-level small_account_count. This TO extends D_02 to carry per-client + per-role + summary counts in book.json.</ref>
  </references>

  <context>
    B9 (C_08) shipped advisor-level small_account_count in advisor_fee_efficiency.json.
    This TO extends D_02 (build_advisor_books) to carry small_account_count in three places
    inside gold/entities/advisors/{id}/book.json:
      1. summary.small_account_count    — advisor aggregate (unique accounts, any role)
      2. role_breakdown[role].small_account_count — per-role count (same-role mask)
      3. clients[].small_account_count  — per-client count (this advisor × this relationship)

    D_02 already has all required data in snap_latest:
      - total_aua column (per account)
      - role columns (architect, implementor, consultant, local_ops, additional_advisor)
      - relationship grouping (clients loop already exists)

    Use SMALL_ACCOUNT_AUA_THRESHOLD_USD = 40_000. Define module-level in D_02 (same value
    as C_08; do NOT import cross-script — two constants, one value, one grep).
  </context>

  <objective>
    In D_02.advisor_client_detail.py (build_advisor_books function), add small_account_count
    in three places:

    1. role_breakdown loop (already at lines ~1363-1376):
       For each role, add:
         role_small = int(snap_latest.loc[
           role_acct_mask & (snap_latest['total_aua'] < SMALL_ACCOUNT_AUA_THRESHOLD_USD),
           'account_id'
         ].nunique())
         role_breakdown[role]['small_account_count'] = role_small

    2. summary dict (book['summary']):
       Compute UNION small count (advisor attached in ANY role, unique accounts):
         any_role_mask = (
             (snap_latest['architect']          == advisor) |
             (snap_latest['implementor']        == advisor) |
             (snap_latest['consultant']         == advisor) |
             (snap_latest['local_ops']          == advisor) |
             (snap_latest['additional_advisor'] == advisor)
         )
         summary_small = int(snap_latest.loc[
             any_role_mask & (snap_latest['total_aua'] < SMALL_ACCOUNT_AUA_THRESHOLD_USD),
             'account_id'
         ].nunique())
         book['summary']['small_account_count'] = summary_small

    3. clients[] list (wherever AdvisorClient dicts are built in the clients iteration):
       For each relationship, within the per-advisor snap_latest subset filtered to
       that relationship_id:
         client_small = int(client_accts.loc[
             client_accts['total_aua'] < SMALL_ACCOUNT_AUA_THRESHOLD_USD,
             'account_id'
         ].nunique())
       Emit as 'small_account_count': client_small in the client dict.

    Edge-case rules (match C_08 B9 precedent):
    - NULL total_aua: excluded (NaN comparisons with less-than return False in pandas — correct by default).
    - Zero total_aua: INCLUDED (0 < 40_000 is True).
    - Negative total_aua: INCLUDED.
  </objective>

  <wire_contract>
    book.json shape additions:

    summary:
      { ..., "small_account_count": 12 }

    role_breakdown:
      { "architect": { "aua": ..., "account_count": ..., "pct_of_tagged": ..., "small_account_count": 3 }, ... }

    clients:
      [ { "client_key": ..., "client_name": ..., "aua": ..., "small_account_count": 2, ... }, ... ]

    All fields are required int, default 0. Never null.
  </wire_contract>

  <acceptance_criteria>
    1. book.json for at least one advisor carries small_account_count in summary, all role keys,
       and all client entries.
    2. summary.small_account_count == count of unique accounts across all roles where total_aua &lt; 40_000
       (verify: not a sum of role counts, which double-counts multi-role accounts).
    3. sum(role_breakdown[r].small_account_count for r in roles) >= summary.small_account_count
       (per-role can double-count; union cannot).
    4. sum(client.small_account_count for client in clients) may differ from summary.small_account_count
       (per-client sums across clients; summary is unique accounts regardless of client overlap — rare
       but possible if same account mapped to multiple relationships).
    5. Travis Penfield's book.json: at least one role shows small_account_count > 0.
    6. py_compile D_02 exit 0.
    7. comp-pipescript deployed D_02: MATCH before upload.
    8. comp-validate D_02 exit 0 after QA rerun.
    9. MCP COMPLETE to COO with commit hash + Travis small_account_count summary + sample role_breakdown.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_02</run>
        <expect>READS includes account_team, advisor_fee_detail. No new COLUMN GAPS introduced by this change (we read total_aua which is already in snap_latest).</expect>
        <if_mismatch>STOP. Surface to COO if new read required.</if_mismatch>
      </step>
      <step>
        <run>comp-blast D_02</run>
        <expect>No downstream consumers of book.json beyond D_04 and portal platinum/advisors/* path. No new blast risk.</expect>
        <if_mismatch>Document any new consumer before writing.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>comp-pipescript deployed D_02</run>
        <expect>MATCH.</expect>
        <if_mismatch>Coordinate with AE.</if_mismatch>
      </step>
      <step>
        <run>python -m py_compile D_02.advisor_client_detail.py</run>
        <expect>Exit 0.</expect>
      </step>
    </phase>
    <phase id="3" when="after QA rerun">
      <step>
        <run>comp-validate D_02 --artifact /tmp/book_sample.json</run>
        <expect>Exit 0. small_account_count fields present and non-null.</expect>
        <if_mismatch>STOP. Do not signal COO until clean.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. snap_latest already has total_aua. No new gold inputs required.
  </dependencies>

  <next>
    On MCP COMPLETE: DE B9b-1 (Clients panel) and DE B9b-2 (Role decomp) can both proceed.
    They depend on this artifact landing on DEV before FE type changes are tightened to required.
    Mark types optional (?) until this ships, then tighten.
  </next>
</task_order>
