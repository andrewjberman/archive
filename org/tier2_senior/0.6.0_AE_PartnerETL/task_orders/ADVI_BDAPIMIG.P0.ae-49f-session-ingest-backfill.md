<to_id>ADVI_BDAPIMIG.P0</to_id>
<project>ADVI_BDAPIMIG</project>
<title>Phase 0 (P0 unblock): stand up the 49F BD DataMining-REST ingest (session secret + env + templates + ported cot_bronze_ingest run + backfill 06-19..today) -> un-freeze the 4 bd silver tables</title>
<assigned_to>0.6.0_AE_PartnerETL</assigned_to>
<issued_by>1.0.0_SA_CTO (PRD author/arch; CVO drives the GO + co-verify per the BD-lane division 2026-06-25)</issued_by>
<issued_date>2026-06-25</issued_date>
<status>staged</status>
<!-- STAGED: GO fires when ANDREW provides the post-MFA 49F cookie (.bd.identity + bd_DeviceRegistration). 3.0.0_SA_CVO holds the cookie-GO + drives dispatch + owns co-verification (the Andrew-BD lane per sovereign direction -- BD is OFF the COO plate this session). Do NOT self-start before CVO's GO. PRD: docs/architecture/ADVI_BDAPIMIG_PRD.md. -->

<context>
49F BD bronze dark since 2026-06-19: SS&C enabled email-OTP MFA on the AndrewBerman49F account, the
headless Playwright scrape can't pass it -> bd_silver_{allocations,transactions,realized,unrealized}
all frozen @06-19 (comp-freshness FAIL @135h+) -> gold lots run nightly on stale silver -> served 49F
AUA stale + degrading silently 6d. FIX (CTO ruling, PRD Section 3): migrate to the PROVEN cot DataMining
REST flow -- data pull is solved (Option D); the only hard problem is seeding a valid post-MFA
.bd.identity session (Phase-0 Option B = a manual cookie Andrew captures). The ported ingest lands at
the IDENTICAL forwardfill_v2/{table}/*.xlsx seam the scraper used, so silver + gold need ZERO change.
</context>

<objective>
Restore the 49F BD bronze ingest via the REST path + backfill the frozen window, so the 4 silver tables
un-freeze and served 49F AUA recovers -- a config + port of proven cot code, no new pipeline code.
</objective>

<the_work>
1. SESSION SECRET: create Secrets Manager `blackdiamond/49f/session` and inject the Andrew-captured
   cookie jar (the `.bd.identity` post-MFA cookie + `bd_DeviceRegistration`) in the field shape
   cot_bronze_ingest.py reads (bd_identity/cookie field -- see the script's _load_session, ~line 116-144).
   NEVER reuse cot's `blackdiamond/cot/session`.
2. ENV (the 4 Model-B vars -- ALL FOUR explicitly, see FIRM-SEPARATION AC below):
   BD_S3_BUCKET=opal-data-bd | BD_FIRM_ID=49f | BD_SESSION_SECRET_ID=blackdiamond/49f/session |
   BD_BASE=https://bd3.bdreporting.com.
3. TEMPLATES: capture the 49F DataMining query bodies (its account universe + selected dims differ from
   cot) -- via `cot_bronze_ingest.py --provision` against the live 49F session, OR DevTools "Copy as cURL"
   per table -> land `s3://opal-data-bd/code/bronze/templates/{allocations,transactions,realized,unrealized,holdings}.json`.
4. RUN + BACKFILL: run the ported ingest (firm-bound to bd) and `--backfill --start 2026-06-19 --end <last
   COMPLETE day>`. Use Custom date-window mode (TABLE_DATE_MODE) -- backfill COMPLETE days only; do NOT
   over-advance to an incomplete today (the COTETL over-advance/zero-AUA trap). Keep the holdings
   completeness floor ($0-MV reject) ON.
5. DEVICE-TRUST PROBE (steady-state fork -- CVO-requested AC): with bd_DeviceRegistration injected, test a
   HEADLESS 49F login (the ported cot_bd_session_fetch.py path) -> does it SKIP the OTP step-up? Record y/n
   + evidence. y => Phase-1 steady-state = Option B headless auto-refresh; n => Option-A primary/Option-C
   fallback. Report the result to CTO + CVO (it decides the Phase-1 durable design).
</the_work>

<compiler_tools_mandate>
- BEFORE write: `comp-blast cot_bronze_ingest` (and the session-fetch fn) for the blast radius; `comp-iam
  service` for any new runner role boto3 (Secrets Manager get + s3 put to opal-data-bd) before deploy.
- BEFORE run: `comp-pipescript deployed` to confirm the ingest artifact is current; `comp-pipescript
  postdeps` for required post-steps.
- AFTER: `comp-freshness chain bd` (the 4 silver tables) -- the un-freeze evidence for CVO co-verify.
</compiler_tools_mandate>

<cross_domain_coordination>
- SHARED CODE cot_bronze_ingest.py + cot_bd_session_fetch.py (cot lane) -- a Model-B firm-port, NOT a
  fork. Run the SAME code firm-bound to bd via env. FIRM-SEPARATION (CLAUDE.md NEVER#1, gate+IAM): the
  port must NOT introduce any bd->cot bucket cross-reference. CTO-VERIFIED 2026-06-25: the script is
  cleanly env-parameterized (all S3 ops use BD_S3_BUCKET), BUT its DEFAULTS are cot
  (opal-data-cot/cottonwood/blackdiamond/cot/session) -- so a MISSING env var silently defaults a 49F run
  to WRITING cot's bucket. See the FIRM-SEPARATION-ENV AC -- this is the load-bearing safety.
- S3 SEAM opal-data-bd/forwardfill_v2/{table} is SHARED with the existing scraper output during the
  parallel-run window. API + scraper must NOT double-write the same {table}/{date} partition -- per-table
  cutover; decommission scrape only post-parity (Phase 2). Coordinate the cutover order.
- DS (0.4.0): confirm the bd silver merge ingests the API-landed xlsx with zero change (same seam).
- CVO (3.0.0): owns the GO (on Andrew's cookie) + the co-verification close-gate.
</cross_domain_coordination>

<acceptance_criteria>
1. All 4 bd_silver_{allocations,transactions,realized,unrealized} show a fresh today-dated partition,
   `comp-freshness` = PASS (the un-freeze, grounded on SERVED state).
2. Restored rows sane vs the pre-06-19 baseline: row counts in band, AUA magnitude plausible, no all-$0,
   no schema drift, source_system correct.
3. Served 49F AUA reflects post-06-19 dates end-to-end (the freeze clears through gold, not just bronze).
4. FIRM-SEPARATION-ENV: the 49F runner sets ALL 4 env vars explicitly AND a guard refuses the run / fails
   loud if BD_S3_BUCKET resolves to the cot default while BD_FIRM_ID!=cottonwood (no silent default-to-cot
   write). Prove: a dry-run with BD_S3_BUCKET unset for a 49f firm FAILS closed (does not write opal-data-cot).
5. DEVICE-TRUST PROBE result recorded (headless login + bd_DeviceRegistration -> skips OTP y/n + evidence),
   reported to CTO+CVO as the Phase-1 steady-state decision input.
6. Session log w/ Compiler Tools section. RAVC2 to CTO (arch) + CVO (the verification close-gate). CVO's
   PRD-Section-6 bar is the close-gate; CVO certifies the un-freeze on the first restored run.
</acceptance_criteria>
