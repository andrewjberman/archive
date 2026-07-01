<to_id>ADVI_COTMVP.B-DS</to_id>
<project>ADVI_COTMVP</project>
<title>B-DS -- emit platinum/firm/client_directory.json on opal-data-cot (firm-level client roster) -- lights up the shipped-but-empty COTMVP-B Clients roster</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>0.4.0_DE_ClientPlatform (COO owner-confirm 2026-07-01T1425Z; DS lane freed + offered)</issued_by>
<consult>0.4.0_DE_ClientPlatform (FE consumer -- schema below is what CottonwoodClientsSection reads); 2.0.0_SA_COO (owner-confirm); 3.0.0_SA_CVO (served count-verify)</consult>
<issued_date>2026-07-01</issued_date>
<status>pending</status>
<priority>MEDIUM -- lower than ADVI_TAGATTR/49F, but the priority gap-work in the cot-DS lane per COO: it unblocks a SHIPPED-but-empty FE (CottonwoodClientsSection, DEV 07d5887f).</priority>

<context>
COTMVP-B FE is DONE + CTO-arch-approved (Andrew-direct 2026-06-30): CottonwoodClientsSection ships COT-ISOLATED with a graceful empty-state and renders EMPTY until the COT client directory is served. Ground-confirmed 2026-07-01: s3://opal-data-cot/platinum/firm/ has NO client_directory.json (only clients-tab-slim.json @529B). COT gold already aggregates 217 clients / 805 accounts (dashboard-level), so the data exists -- it just isn't emitted as the directory artifact. inf + 49F already serve this artifact shape; COT is the only gap.
</context>

<scope>
Emit s3://opal-data-cot/platinum/firm/client_directory.json -- a FIRM-LEVEL, advisor-INDEPENDENT client/household roster (no advisor tagging; COT has no segmentable advisor dimension). cot-tree ONLY, firm-separated (NEVER#1; 49F/bd ZERO-touch, IAM+gate enforced). Same artifact shape inf/49F serve.
</scope>

<exact_fe_schema>
The FE (portal .../cottonwood/CottonwoodClientsSection.tsx -> getClientDirectory) is DEFENSIVE on shape + field names, so this is the CANONICAL target (any of the accepted aliases also work):

{
  "households": [
    { "household_id": "<stable id>", "display_name": "<client/household name>", "aua": <number> },
    ...   // ~217 rows
  ]
}

Accepted by the FE (build the canonical, but for reference):
- households: ARRAY of objects (canonical) OR a RECORD keyed by household_id -> object. Either works.
- per row: name  = display_name (preferred) || advisor_name || household_id   -> emit `display_name` = the CLIENT/HOUSEHOLD name (NOT an advisor name; COT is advisor-independent).
                   key   = household_id (stable; used as React key + Record key).
                   aua   = OPTIONAL: aua (preferred) || total_aua || aum ; a finite number. If omitted, the roster still renders (names only, AUA column hidden). Emit it -- household AUA -- so the roster shows + sorts by $.
- account_count is NOT consumed by v1 (fine to include for the future per-client drill; do not block on it).
The FE sorts by aua desc then name, shows "<N> clients". So N must == the firm's real client/household count (~217).
</exact_fe_schema>

<compiler_tools_mandate>
  <phase id="1" when="before write"><step><run>comp-pipescript io &lt;the cot gold script that will emit it&gt;</run><expect>COLUMN GAPS + confirm the household+AUA aggregation source (COT gold already has 217 clients/805 accts).</expect></step></phase>
  <phase id="2" when="before commit"><step><run>.tools/ds-commit-gate.sh</run><expect>py_compile + ruff clean; from __future__ import annotations present.</expect></step></phase>
  <phase id="3" when="after commit / on the SCHEDULED nightly artifact"><step><run>comp-validate &lt;script&gt; --artifact &lt;served client_directory.json&gt;</run><expect>PASS/WAIVED; households present, count ~217, each row has display_name + finite aua.</expect><if_mismatch>STOP; do not signal DE/CVO safe.</if_mismatch></step></phase>
</compiler_tools_mandate>

<cross_domain_coordination>cot-tree only; no bd/inf cross-ref (firm separation gate + IAM). FE (CottonwoodClientsSection) is DE-owned + already shipped -- it lights up automatically on serve, ZERO FE change needed. Validate on the scheduled nightly (no ad-hoc gold run).</cross_domain_coordination>

<acceptance_criteria>
1. s3://opal-data-cot/platinum/firm/client_directory.json served on the scheduled nightly, shape { households: [...] } (or Record), ~217 rows, firm-separated (cot only).
2. Each row carries a client/household display_name + a finite household aua (roster renders names + $, sorts by $).
3. Count matches the firm's real client/household count (CVO served count-verify 217/805 class).
4. 49F + bd artifacts ZERO-touched (firm separation held).
5. Session-log Compiler Tools reproduces the mandate. RAVC2 to DE (CC COO + CVO). On serve, DE verifies the roster renders + CVO count-verifies.
</acceptance_criteria>

<nightly_validation_runbook note="COO-requested fresh-DS handoff -- run if the base session is not live at the cot nightly. Code = bb2d62ef8 (cot D_04 build_client_directory), deployed+sha256-verified on opal-data-cot/code/gold/.">
After the cot nightly regenerates s3://opal-data-cot/platinum/firm/client_directory.json (currently ABSENT -- do NOT verify before it exists):
1. comp-validate D_04.client_portal_summary --artifact &lt;served cot client_directory.json&gt; (or direct: households present, ~218).
2. Pull the served client_directory.json: shape {households:[{household_id,display_name,aua}]}; 218 rows (== cot clients_tab headline.client_count, NOT 217 -- 218 is faithful/correct); each display_name a CLIENT/household name (not advisor); all aua finite (one legit aua=0); sum(aua) reconciles to clients_tab headline.total_aua (~$433.84M, data_as_of advances).
3. firm-sep: bd/49F leaderboard.json + inf served NOT moved by this cot-only change (comp-pipescript deployed bd/inf MATCH).
4. PASS -> RAVC2 0.4.0_DE_ClientPlatform (CC 2.0.0_SA_COO + 3.0.0_SA_CVO); DE renders CottonwoodClientsSection (218 roster sorted by $), CVO count-verifies 218. MISMATCH -> STOP.
</nightly_validation_runbook>
<references><ref type="fe">portal/src/pages/AdvisorIntelligence/_partners/cottonwood/CottonwoodClientsSection.tsx (toRoster -- the exact consumed fields); _shared getClientDirectory -> platinum/firm/client_directory.json</ref><ref type="peer-artifact">inf + 49F platinum/firm/client_directory.json (same shape, reference implementation)</ref></references>
<lane_note>DS owns the cot-gold emit (rule 13). DE owns the FE (already shipped). Owner single-routed to base-DS by COO 2026-07-01 (off the 06-30 base-COO/MSTR routing). GATE: land on the scheduled nightly, never an ad-hoc gold run.</lane_note>
