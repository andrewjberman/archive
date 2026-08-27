<to_id>ADVI_BDAPIMIG.P1</to_id>
<project>ADVI_BDAPIMIG</project>
<title>Phase 1 (DURABLE): productionize the 49F BD DataMining-REST ingest -- scheduled bd-exporter runner + session-refresh + per-table absence alarm + (Phase 2) decommission the scrape boxes</title>
<assigned_to>0.6.0_AE_PartnerETL (staged for when the AE PartnerETL lane spins up; CVO/Andrew drive BD)</assigned_to>
<issued_by>1.0.0_SA_CTO (PRD author/arch; re-scoped 2026-06-25 from Phase-0 after CVO drove the P0 recovery manually)</issued_by>
<issued_date>2026-06-25 (re-scoped from the Phase-0 TO d09a612d4)</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_BDAPIMIG, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<!-- PHASE-0 P0 RECOVERY DONE 2026-06-25 by 3.0.0_SA_CVO (AE lane cold, BD on CVO per Andrew): auth proven
live, blackdiamond/49f/session created, 4 templates provisioned (Custom dateRangeType), cot_bronze_ingest.py
run firm-bound to bd (all 4 env vars explicit), 4 tables re-landed @06-24 to opal-data-bd/forwardfill_v2,
firm-sep verified (opal-data-cot negative-checked, no 49f leak). DS holds the silver-zero-change trigger;
CVO co-verifies the un-freeze (§6). THIS TO is now the DURABLE Phase-1 productionization, STAGED for an AE
lane. GO when an AE PartnerETL session is live + CVO/Andrew direct. PRD: docs/architecture/ADVI_BDAPIMIG_PRD.md. -->
<!-- PHASE-1 INTERIM BUILD DONE 2026-06-25 by 0.6.0_AE_PartnerETL (CVO GO + drive). All 3 components SHIPPED +
live-proven, build order A->C->B:
  (A) bd-49f-keepalive Lambda, EventBridge rate(15m), GET /auth/keepalive -> live invoke {ok:true,status:204}.
      401/403 -> direct SNS re-capture alert + KeepaliveOK=0 + absence alarm. READ-ONLY secret, zero cot.
      tag bd-v2.33.0. CVO: ALL-4-BARS PASS / ACCEPTED (email egress Andrew-confirmed delivery-proven).
  (C) bd-49f-freshness-probe Lambda, rate(1h): AuthTokenOK (401-specific, 5xx=no-page) + per-table
      SilverAgeHours{4 tables}. Alarm-driven paging (authtoken-dead/absence + 4x silver-stale) to
      opal-bd-49f-cookie-alerts. tag bd-v2.34.0. CVO: FULL PASS / ACCEPTED (alarms discriminate frozen-vs-
      fresh on live data). Egress: SMS sub DROPPED (no origination entity + sandbox = false coverage);
      EMAIL = single proven channel. {test_alert:true} hook on A+C for re-provable delivery.
  (B) bd-49f-runner Lambda, daily cron(0 2 UTC): pulls shared cot_bronze_ingest.py from opal-data-bd/code/
      bronze/ (Model-B, no fork), 4 env vars EXPLICIT, runs 4 REST tables -> forwardfill_v2. Retry/backoff
      401(no-storm)/5xx-Error(retry). tag bd-v2.35.0. FIRM-SEP HARD GATE (AC#4): _assert_firm_separation()
      added to the shared script (commit eb0ce40f6) -- PROVEN matrix (49f+unset=ABORT, 49f+cot=ABORT,
      49f+bd=PASS, cot-default=no-abort) + 3-layer defense (explicit env / script guard / IAM Deny cot).
      Live smoke: ingested transactions 76MB -> forwardfill_v2/transactions/TRANSACTIONS_DAILY_2026-06-25.xlsx,
      222s. CVO formal dry-run + full-4-table verify PENDING.
3 deploy-ledgers opened+CLOSED (bd-49f-p1a-keepalive / p1c-freshness / p1b-runner), no stranded legs.
REMAINING (this TO stays pending): (B) full-4-table run gated on CVO/Andrew silver-fire GO (realized/unrealized
still 138h-stale in SILVER -- B lands their bronze, DS-owned silver trigger re-lands); cron-timing vs bd-silver
precedence (DS confirm); (D) Andrew manual reseed when C alerts; PHASE 2 decommission of the 4 Playwright scrape
boxes (parity-verify + separate GO, destructive). Durable follow-up (non-blocking): SMS 2nd channel = SNS
origination identity + production access (account-owner). DEFERRED per Andrew hold: auto-login session-refresh. -->

<!-- ROOT-CAUSE FIX LANDED 2026-07-09 by 0.6.0_AE_PartnerETL (CTO GO 083650Z). The productionized runner
was itself the source of a SECOND client-facing freeze: it fires at 00:00Z off the session chain, so
run_date=_today_utc() asked BD for an as-of date that had not begun in ET. BD answers a point-in-time
SNAPSHOT query for a non-existent date with a header-only ~4.6KB xlsx -> allocations + unrealized landed
0-row stubs 07-05..07-09 while transactions + realized (PERIOD queries over a 14d window) kept flowing.
Stubs -> 0-row silver -> C_02 certified_aua<=0 -> D_00 held a frozen served AUA. Auth was REFUTED: same
invocation, same bearer, allocations=4,592B while realized=993,387B. Exercised: asOfDate 07-09 -> 0 rows,
07-08 -> 32,726 rows.
  FIX 1 (content-grounded guards; CTO calls it the freshness-integrity reference fix): 0-data-row SNAPSHOT
    exports REJECTED pre-write; the holdings-only completeness sidecar generalized to every table
    (has_data_rows); _already_landed + emit_bronze_sentinel now bind to that sidecar instead of
    head_object EXISTENCE (four existence proxies were masking the freeze, incl. a sentinel that fired
    bd-silver-merge on stubs). Legacy stubs now re-pull themselves.
  FIX 2 (empty-root): BD_SNAPSHOT_ASOF_LAG_BDAYS=1 on bd-49f-runner -- snapshot tables request the LAST
    COMPLETE BUSINESS DAY and land under that TRUE as-of date. Default 0 = OFF = byte-identical = zero cot
    regression (same firm-safety shape as BD_TXN_CHUNK_DAYS). cot's snapshot tables carry the same latent
    bug -- flagged to CTO+DS, deliberately NOT folded in.
  Self-caught pre-re-pull: the first row probe counted bare '<row ' but BD emits NAMESPACED '<x:row' --
    it would have REJECTED a small VALID export. Rebound to '<dimension ref>'. Tests 57/57 incl. the 22
    cot retry-net no-regression tests + 3 real-BD-artifact fixtures.
  Source repaired under CTO GO: as_of 07-08 re-pulled real -> silver/allocations/2026-07-08 = 6,870 rows /
    $1,840,781,732.39 (was a 46,277B 0-row stub); silver/unrealized/2026-07-08 = 103,490 rows.
  SERVED un-freeze is GOLD-GATED (~04:00Z; D_00 only runs inside the scheduled gold). Predicted cert
    @data_date 2026-07-08 = $1,844,022,461.17. NOTE: the "~$185M/11% overstated" premise is NOT supported --
    the served figure is $6.86M (0.372%) UNDERstated and the frozen cert is dated 07-02 (7d, not ~3wk).
  Commits 9d44d6af5 / 7a229eaaf / 463238356 / d37ae51b6. Ledger 20260709T0855Z_bd-49f-empty-stub-asof-lag-
  root-fix (L1-L4 CLOSED, L6 HELD-external on the gold gate). Findings: docs/briefs/{bd-unrealized-export-
  500k-row-cap-finding,comp-freshness-is-mtime-bound-greenlit-a-5day-client-facing-freeze}-20260709.md. -->

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

<durable_auto_auth_extension>
<!-- ADDED 2026-06-25 (Andrew-direct GO via CVO; brief docs/briefs/bd-49f-durable-auto-auth-cv-login-otp-relay-20260625.md).
EXTENDS this TO from the scheduled-runner interim to the DURABLE auto-RE-AUTHENTICATION layer that retires the
manual cookie reseed. WHY: measured today the .bd.identity ABSOLUTE SSO cap is SHORT (~hours) -- keepalive can't
beat it; only a fresh LOGIN resets the absolute clock. (The dead-cookie was caught live in the 2026-06-25 health verify.) -->

ARCH (CTO-ruled 2026-06-25): VISION = Kimi-VL (already wired, SM astn/kimi/api-key, model kimi-k2.6; reuse the
analyze.py:_chat OpenAI-compat call shape + the harvest_ft_session.js grid-localization pattern). COMPUTE = co-opt
the ASTN CV stack (EC2 astn-wsjft-scraper -- has residential-proxy + Chromium + Kimi-VL; a Lambda can't hold the
human-OTP wait). Same-box-scheduled-nonoverlap vs AMI-sibling = 0.7.0 coordination (proxy-zone 2nd-concurrent-session).

ANDREW-LOCKED: OTP return-channel = the m365 gateway (NOT SMS -- SNS-SMS dependency DROPPED). 0.5.0 grounded the
gateway = Andrew's OWN identity (not a bot) -> DESIGN FORK (CVO ruling pending, 0.5.0 confirming the channel):
  PATH A (target, if BD email-delivers the OTP): the automation runs AS Andrew -> reads the OTP from his EMAIL
    directly (search_email scoped to the SS&C/BD sender) -> FULLY AUTOMATED, no human-in-loop, no >15min wait.
  PATH B (fallback, if SMS-only): Andrew types the code once into a designated Teams chat -> poll_addressed_teams
    _messages + read_chat_messages reads it. Human-in-loop only on SMS-OTP.

ROE (CTO-ruled, CVO-verified, NON-NEGOTIABLE): observe-act-only; NEVER log/persist OTP or credential VALUES
(response/commit/log/S3); single-use OTP not stored; ONLY persisted artifact = fresh .bd.identity -> SM
blackdiamond/49f/session. Firm-sep NEVER#1 binds (49F never opal-data-cot).

LEGS:
  L1 CORE auto-login (channel-independent): extend cot_bd_session_fetch's OIDC login + MFA-fail branch into a
     49F bd_auto_login -- Playwright+Chromium on the residential proxy -> Kimi-VL perceive->act loop (screenshot
     -> classify login/modal/OTP/logged-in + grid-localize -> Playwright act) -> capture .bd.identity -> SM.
  L2 OTP-RELAY adapter (Path A read-email | Path B Teams-poll), channel-selected by 0.5.0's finding.
  L3 DEVICE-TRUST: capture bd_DeviceRegistration on success + inject on subsequent logins to SKIP OTP where BD
     allows (the OTP-minimizer; works WITH or WITHOUT it -- Andrew owes a capture to fully prove the quiet path).
  L4 FRESHNESS-GATE TRIGGER: extend bd-49f-freshness-probe to TRIGGER the refresh on 401 (not just alert).
  L5 COMPUTE wrapper: the ASTN-box deploy (S3->box->SSM) or AMI-sibling, 49F-scoped IAM/secrets.

STATUS 2026-06-25: launched. CTO arch ruled (vision+compute). 0.5.0 surfaced the Andrew-identity gateway ->
design fork out to CVO/0.5.0 (channel confirm) + 0.7.0 (box-arch). Kimi-VL call shape + cot login base grounded.
Core (L1) authorable channel-independent once 0.7.0 confirms same-box-vs-AMI-sibling (wrapper shape).
DELIVERY: standard cycle + deploy-ledger at first deploy-start. CVO verifies end-to-end (live-cookie refresh +
OTP-path + device-trust-skips + ROE + firm-sep + no runner/keepalive/alarm regression). Interim stays the bridge until this lands.
</durable_auto_auth_extension>
