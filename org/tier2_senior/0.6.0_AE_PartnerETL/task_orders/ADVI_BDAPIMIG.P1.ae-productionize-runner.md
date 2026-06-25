<to_id>ADVI_BDAPIMIG.P1</to_id>
<project>ADVI_BDAPIMIG</project>
<title>Phase 1 (DURABLE): productionize the 49F BD DataMining-REST ingest -- scheduled bd-exporter runner + session-refresh + per-table absence alarm + (Phase 2) decommission the scrape boxes</title>
<assigned_to>0.6.0_AE_PartnerETL (staged for when the AE PartnerETL lane spins up; CVO/Andrew drive BD)</assigned_to>
<issued_by>1.0.0_SA_CTO (PRD author/arch; re-scoped 2026-06-25 from Phase-0 after CVO drove the P0 recovery manually)</issued_by>
<issued_date>2026-06-25 (re-scoped from the Phase-0 TO d09a612d4)</issued_date>
<status>staged</status>
<!-- PHASE-0 P0 RECOVERY DONE 2026-06-25 by 3.0.0_SA_CVO (AE lane cold, BD on CVO per Andrew): auth proven
live, blackdiamond/49f/session created, 4 templates provisioned (Custom dateRangeType), cot_bronze_ingest.py
run firm-bound to bd (all 4 env vars explicit), 4 tables re-landed @06-24 to opal-data-bd/forwardfill_v2,
firm-sep verified (opal-data-cot negative-checked, no 49f leak). DS holds the silver-zero-change trigger;
CVO co-verifies the un-freeze (§6). THIS TO is now the DURABLE Phase-1 productionization, STAGED for an AE
lane. GO when an AE PartnerETL session is live + CVO/Andrew direct. PRD: docs/architecture/ADVI_BDAPIMIG_PRD.md. -->

<context>
Phase 0 (the P0 unblock) is DONE -- CVO recovered the 4 frozen bd silver tables manually via the proven
cot DataMining REST flow (4 tables re-landed @06-24, firm-separation held). But that recovery is a MANUAL
session-driven run on a hand-injected cookie. Phase 1 makes it DURABLE: a scheduled runner + an automated
session-refresh so 49F BD ingest runs nightly without a human, + the per-table absence alarm that was
missing (the 6-day silent-fail gap), then Phase 2 decommissions the dead Playwright scrape fleet.
</context>

<objective>
Make the 49F BD REST ingest run autonomously + monitored, then retire the scrape boxes -- so the P0 stays
fixed without manual cookie/run intervention.
</objective>

<the_work>
INTERIM ARCHITECTURE (CTO arch-gated 2026-06-25, off CVO brief 65f83dc7b; password/auto-login ON HOLD per
Andrew -> this keepalive-extended-manual-cookie interim keeps 49F flowing). It IS PRD Phase-1 (B runner + C
alarm = permanent) MINUS auto-login PLUS the keepalive cron (A); only (D) gets automated when password resumes.

(B) SCHEDULED REST PULL RUNNER: the `bd-exporter` API runner -- one light HTTP/xlsx-passthrough box or Lambda
   (NO browser for the data pull) on the cot-exporter EventBridge->SSM model -- running cot_bronze_ingest.py
   firm-bound to bd (the 4 env vars; secret blackdiamond/49f/session). Daily, ahead of the bd silver stage.
   RETRY/BACKOFF that DISTINGUISHES 401 (auth -> route to C's alert, do NOT retry-storm) from 5xx (transient
   -> retry; CVO hit a transient allocations Error 2026-06-25 that cleared on retry). *** FIRM-SEP (AC#4) is
   the load-bearing gate -- see cross-domain. ***
(A) KEEPALIVE CRON (interim-specific): a tiny Lambda, EventBridge at cot's keepalive cadence (MATCH it, not an
   arbitrary aggressive interval -- stealth baseline-match), reads .bd.identity from SM (GetSecretValue,
   READ-ONLY -- keepalive extends server-side, mints no new cookie) -> GET /datamining/auth/keepalive (=204
   proven). Stretches the cookie to BD's absolute cap (>=24h expected; the cap is the one empirical unknown,
   determined by running A) -> minimizes manual re-capture. FAIL-LOUD on 401 (cookie dead -> feed C's alert).
(C) FRESHNESS-PROBE + PER-TABLE ABSENCE ALARM (NON-OPTIONAL -- closes the 6-day silent gap): (i) auth probe
   GET /auth/token, 401-SPECIFIC (not any non-200; a 5xx is transient, don't cry wolf) -> SNS to Andrew
   "re-capture .bd.identity", run AHEAD of B's window + periodically so a dead cookie alerts with lead time;
   (ii) per-table silver freshness/absence check. BOTH EGRESS-VERIFIED (SNS-confirmed != delivers -- prove
   delivery). ASTN 4am-absence-check is the reference.
(D) MANUAL RESEED (stays manual until password resumes): Andrew pastes a fresh .bd.identity -> SM
   put-secret-value (30-sec) when C alerts. The secret maintains ONLY .bd.identity (DROP __cf_bm -- CVO proved
   .bd.identity-alone auths, __cf_bm-alone=401, it's a 30-min CF cookie = stale-confound).
DEFERRED: the headless SESSION-REFRESH / auto-login (ported cot_bd_session_fetch.py) + the DEVICE-TRUST PROBE
   are DEFERRED until Andrew's password/login-automation hold lifts -- the keepalive cron (A) replaces them for
   the interim (no headless login needed). Do NOT build the auto-login now.
(PHASE 2) PARITY + DECOMMISSION: parity-verify API vs the last good scrape, then decommission the 4
   Playwright scrape boxes (bd-allocations/bd-transactions/bd-fees/bd-assets) -- cost + reliability win.
   Per-table cutover; do NOT double-write the opal-data-bd/forwardfill_v2/{table} partition during the
   parallel-run window.
</the_work>

<compiler_tools_mandate>
- BEFORE write: `comp-blast cot_bronze_ingest` (+ the session-fetch fn); `comp-iam service` for the new
  runner role boto3 (Secrets Manager get + s3 put to opal-data-bd) before deploy; `comp-blast` on the scrape
  boxes before any decommission.
- BEFORE run/deploy: `comp-pipescript deployed`; `comp-iam gaps` after any iam.tf change.
- AFTER: `comp-freshness chain bd` (the 4 tables) as the standing nightly-health evidence.
</compiler_tools_mandate>

<cross_domain_coordination>
- SHARED CODE cot_bronze_ingest.py + cot_bd_session_fetch.py (cot lane) -- Model-B firm-port via env, NOT a
  fork. FIRM-SEPARATION (CLAUDE.md NEVER#1): all 4 env vars EXPLICIT in the runner + a fail-closed guard (a
  49f run with BD_S3_BUCKET unset must FAIL, not silently default-write opal-data-cot -- the script's
  defaults are cot). CVO confirmed firm-sep clean on the manual run; the SCHEDULED runner must encode it.
- S3 forwardfill_v2/{table} parallel-run window with the scraper -- no double-write; per-table cutover.
- DS (0.4.0): the silver merge ingests the API xlsx zero-change (confirmed-pending on the manual run).
- CVO (3.0.0): owns BD + the §6 co-verification close-gate + drives AE on this build. Andrew (interim): the
  manual .bd.identity reseed (D) when C alerts; (deferred until the password hold lifts) the device-trust
  capture + the Option-A SS&C MFA-exempt ask.
</cross_domain_coordination>

<acceptance_criteria>
1. The bd-exporter runner runs cot_bronze_ingest.py firm-bound to bd on a nightly schedule, lands all
   tables to opal-data-bd/forwardfill_v2, with retry/backoff on transient DataMining errors. comp-freshness
   chain bd = PASS on the scheduled run (not just the manual one).
2. (A) KEEPALIVE: the keepalive cron measurably EXTENDS the .bd.identity life (GET /auth/keepalive=204 on
   schedule; the achieved absolute cap recorded, >=24h target) -> the manual re-capture cadence is set by
   that cap, NOT by an un-extended ~session TTL. Read-only on the secret (no PutSecretValue).
3. (C) AUTH-STALENESS ALERT: a 401 on the /auth/token probe (or a runner 401) DELIVERS an SNS alert to Andrew
   "re-capture .bd.identity" -- EGRESS-VERIFIED (prove it delivers, not just publishes), 401-specific (a 5xx
   does NOT alert). The secret maintains ONLY .bd.identity (__cf_bm dropped). [DEFERRED, not an AC for this
   interim: the headless auto-login session-refresh + the DEVICE-TRUST PROBE -- both wait on Andrew's
   password/login-automation hold lifting; the keepalive cron replaces them for now.]
4. FIRM-SEPARATION fail-closed guard in the runner (49f run with BD_S3_BUCKET unset FAILS, no opal-data-cot
   write). Proven via a dry-run.
5. Per-table absence alarm EGRESS-verified (fires + DELIVERS on a missing table).
6. (Phase 2) the 4 scrape boxes decommissioned without regression; EC2_MANIFEST.json updated.
7. Session log w/ Compiler Tools. RAVC2 to CTO (arch) + CVO (the §6 close-gate).
</acceptance_criteria>
