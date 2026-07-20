# Task Order: ADVI_COTPPLADVFIX TO-1 -- inject single "Cottonwood Capital Advisors" synthetic advisor in cot A_01

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-advi-cotppladvfix-to1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <completed>2026-07-08</completed>
    <reconcile_note>Status-reconciled 2026-07-20 by 2.0.0_SA_COO (Andrew-direct backlog review). SHIPPED + served-verified: synthetic single-advisor injection @0bb589a29 (2026-07-07) + 6 cot-clone 49F-safety fixes; DS ship-log @1dbc13e66 (full advisor-drill chain served-verified, live-call fast-track); the paired TO-2 Books/advisor-drill tab is LIVE on portal PROD (portal-v2.1.133, @27f543ade 2026-07-08). The Cottonwood synthetic single-advisor IS the intended state; native advisor keying is deferred to the Sept-2026 Cottonwood-BD phase (GCONTR disposition @a2a0a8c2f). The TO+JSON simply were never reconciled after the 07-07/08 ship.</reconcile_note>
    <dispatch_state>DISPATCHED + GO 2026-07-07 (Andrew-direct P0 via CTO 192953Z re-confirm; paired MCP GO to 0.4.0_DS_ClientPlatform). This is the SEPARATE cot gold/advisor-dimension workstream -- NOT the held cot DATEMODE/holdings-freshness thread (Andrew's PRD in flight); no file overlap (A_01 gold vs cot_bronze_ingest bronze), so the DATEMODE hold does NOT block this. DS lane note: DS was not broker-live at dispatch (post-reboot Tier-1-only); respawn-requested to MSTR same cycle -- the GO drains on respawn. PRD docs/architecture/ADVI_COTPPLADVFIX_PRD.md (commit 11f6bd3c2). TO-1 of 3.</dispatch_state>
    <gate_note>Gates: none upstream. Validate on the SCHEDULED nightly's served artifact (CLAUDE.md NEVER #4 -- no ad-hoc gold run). Gates TO-2 (DE) downstream: TO-2 cannot render until this TO's served advisor entity lands.</gate_note>
  </metadata>

  <objective>For the cot pipeline ONLY, inject a single synthetic advisor "Cottonwood Capital Advisors" into the cot advisor-assignment producer so every account maps to it uniformly across the full SCD, giving the already-built D_02->D_04->shared BooksTab stack exactly one real (non-Unassigned) advisor to nest every client under -- turning Cottonwood's flat/empty advisor surface into a properly-nested advisor-drill Books tab. Root cause (source+served grounded, PRD S1/S2): cot gold runner cloned from 49F/bd keys its advisor layer 100% on 49F team-role columns (architect/implementor/consultant/local_ops/additional_advisor) that cot_silver_merge produces NONE of -> A_01 yields all-Unassigned -> served opal-data-cot/gold/entities/advisors/ + platinum/advisors/ are BOTH EMPTY.</objective>

  <requirements>
    <requirement id="1">Modify the cot advisor-assignment producer so that WHEN the real role dimension is absent (0 of ROLE_COLS populated, or all-Unassigned), assign a single firm advisor "Cottonwood Capital Advisors" to EVERY account across EVERY SCD record (uniform, not time-varying). Result: exactly one distinct advisor across the whole book, for all dates. Leave the other 4 roles Unassigned (D_02/D_04 already skip Unassigned -- must NOT create a spurious second "Unassigned" advisor book).</requirement>
    <requirement id="2">Injection-site latitude (PRD S7 Q2): PRD names data/cot/scripts/gold/A_01.advisor_assignments.py as the natural home, but you may pick the cleanest non-override site (e.g. C_07/account_team, which D_02 uses as a name override) if the Phase-1 comp-blast shows A_01 would be silently re-overridden to Unassigned downstream. The CONTRACT is fixed (one advisor, all clients, all dates, survives the full D_02 PIT-join); the site is your call. cot-only file(s) under data/cot/ -- NEVER touch bd/49F/inf files (firm separation, gate+IAM enforced).</requirement>
    <requirement id="3">GUARD (mandatory): the injection MUST be gated on "real role dimension absent" so it self-DISABLES the moment real advisor matching (rep-code/team) lands -- the evolution path (TO-3) REPLACES, not layers on, this bridge.</requirement>
    <requirement id="4">Idempotent across full + incremental runs. Must NOT partially assign (every account gets the firm advisor, or the injection is a clean no-op -- no half-populated book).</requirement>
    <requirement id="5">Deploy per Rule 13 (DS owns the cot gold commit->deploy cycle incl. aws s3 cp to opal-data-cot/code/gold/). Do NOT trigger an ad-hoc gold run to validate -- validate on the scheduled 02:00 UTC nightly's served artifact.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase name="before_write">comp-pipescript io A_01.advisor_assignments.py (confirm consumers C_08/D_00c/D_02 survive a single-advisor input, unchanged) + comp-blast on the role-assignment path -- surface EVERY site that reads the role columns / account_team / rel_architect_lookup, so the single-advisor mapping is NOT silently re-overridden downstream (esp. C_07's account_team). Patch-or-justify each per the multi-call-site rule. This blast DECIDES the injection site (req 2).</phase>
    <phase name="before_commit">.tools/commit-gate.sh on the changed cot gold script(s); comp-pipescript io again (no blast expansion) to confirm the IO contract is unchanged.</phase>
    <phase name="after_commit">after the SCHEDULED nightly: comp-pipescript deployed A_01... (MATCH) + verify served gold/entities/advisors/ now has exactly one cottonwood_capital_advisors/ book. comp-validate if the script carries a validate config.</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>Shares data/cot/scripts/gold/A_01.advisor_assignments.py + the cot gold chain with ADVI_COTETL (base cot pipeline) and the in-flight cot DATEMODE regression (Andrew's PRD). DATEMODE = bronze/holdings-freshness; THIS = gold/advisor-dimension -- NO file overlap (A_01 gold vs cot_bronze_ingest bronze). Neither blocks the other. NOTE: the cot nightly gold chain is currently running exit-0-but-degraded (holdings_lots empty, allocations 0-rows -- the DATEMODE blast radius); your served-verify must confirm the advisor entity lands DESPITE that, and flag to COO if the empty-allocations state prevents the advisor book from populating.</item>
    <item>GATES ADVI_COTPPLADVFIX.TO-2 (DE, cottonwood/layout.ts flag-flip + BooksTab render). Notify COO the moment the served advisor entity lands (nightly-verified) so TO-2's GO can fire.</item>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion>SERVED artifact (s3://opal-data-cot/gold/entities/advisors/): contains EXACTLY ONE advisor dir -- cottonwood_capital_advisors/book.json -- and NO unassigned/ book.</criterion>
    <criterion>That book's summary.total_aua == the firm headline clients_tab.headline.total_aua (+/- rounding). Every client relationship appears nested under it.</criterion>
    <criterion>platinum/advisors/cottonwood_capital_advisors/summary.json exists on served state.</criterion>
    <criterion>Verified on the SCHEDULED nightly's served artifact, not an ad-hoc run; comp-pipescript deployed = MATCH.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="prd">docs/architecture/ADVI_COTPPLADVFIX_PRD.md S4.1 / S6 TO-1 (CTO-authored, Andrew-direct; commit 11f6bd3c2)</ref>
    <ref type="project">org/projects/ADVI_COTPPLADVFIX.json</ref>
  </references>
</task_order>
```
