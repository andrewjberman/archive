<to_id>ASTN_WSJFT.B</to_id>
<project>ASTN_WSJFT</project>
<title>ASTN_WSJFT B (AE infra-build, TOP PRIORITY) -- FT/WSJ headless fetch + S3 + SES + EC2/TF/3am-orchestration for the CEO daily digest</title>
<assigned_to>0.7.0_AE_CloudOps~C (dedicated ASTN-build lane, MSTR-spawning per COO request 203600Z; flip if MSTR assigns a different serial)</assigned_to>
<arch_gate>1.0.0_SA_CTO (per-infra arch-gate + the app-layer: URL-set, AI-analysis+verbatim-gate, email-template, Kimi-captcha-reflow)</arch_gate>
<verify>3.0.0_SA_CVO (co-verify)</verify>
<issued_by>2.0.0_SA_COO (Andrew-direct TOP PRIORITY via CTO 203152Z; PRD v0.2 docs/architecture/ASTN_WSJFT_PRD.md bf03e9bab)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>partial -- infra build COMPLETE and running (EC2 3am-ET orchestration live, verified 2026-08-05: astn-wsjft-scraper fired 07:00:35Z, ceo-daily-wsjft-digest delivering to Austin; Andrew ratified this vertical PERMANENT 2026-08-05). NOT closing as-written -- verify-only pass by 0.7.0_AE_CloudOps~C, 2026-08-05 ~2350Z: C1 corroborated, C2 PASS (2 flags: OpenAI-not-Claude drift from the LOCKED decision -- routed to CTO; s3:DeleteObject on raw/* read as legitimate scope growth), C3 CANNOT BE VERIFIED AS WRITTEN -- Andrew sovereign-reversed the verbatim-quote requirement TWICE (2026-06-24, 2026-06-29); disposition SUPERSEDED not failed, do NOT rebuild the verbatim gate. Separately: analyze.py:200 hardcodes "faithful_verified": True on every article (never computed, cannot be false) -- a real defect, routed to CTO as a ~5-line app-layer fix. C4 FAIL (no CVO co-verification found, 0/1115 files) -- and its subject (the removed gate) no longer exists to verify, so re-scoping is needed, not a retry. Held at CTO pending items 1-3 (OpenAI/Claude ruling, faithful_verified fix, C3/C4 re-scope) before this TO can close on updated criteria.</status>
<!-- TOP PRIORITY (Andrew-direct): AE BUILD-capacity to ASTN first (SCTY keeps moving, ASTN leads). Both fetch mechanisms + Kimi-captcha PROVEN; all secrets in SM (brightdata-api-key, astn/ft/credentials, astn/ft/session [49-cookie bundle], astn/kimi/api-key). LOCKED: storage=S3, AI=Claude(swappable, verbatim-gate de-risks), email=Opal-HTML, one EC2 scraper-host. -->

<the_work>
AE infra-build (each: design -> CTO arch-gate -> safe-apply + deploy-completion-ledger -> RAVC2 COO+CTO -> CVO co-verify):
1. FT HEADLESS FETCH on EC2: our Chromium + the parked astn/ft/session (49-cookie bundle from SM) + stealth (evaluate-free per the SCTY/crawl no-arbitrary-JS discipline); section-URLs -> top-N -> article-text. IP STRATEGY: test the EC2's OWN IP first (an authed session may pass Cloudflare); if Cloudflare/FT-roaming blocks -> a Bright Data RESIDENTIAL PROXY zone (Andrew provisioning if needed). Harvest + fetch from the SAME egress (session-IP consistency).
2. WSJ FETCH productionized: Web Unlocker (brightdata-api-key, proven; no auth).
3. S3 STORAGE: astn/raw/{date}/{source}/{id}.json + astn/digest/{date}/digest.json.
4. SES SEND: verified opal from-address -> Austin (opted-in). NEEDS the from-address (Andrew -- COO surfacing).
5. EC2 + TERRAFORM + ORCHESTRATION: EventBridge 3am-ET -> fetch -> store -> AI-analysis (CTO app-layer) -> compile -> SES; FAIL-LOUD (don't silently send garbage/skip); deploy-ledger; least-priv IAM (read astn/* secrets + S3 write).
CTO builds the APP-LAYER (not AE): WSJ/FT URL-set + the AI-analysis + the VERBATIM-FIDELITY gate (each cited bullet = exact normalized substring of the fetched article; non-verbatim rejected/regenerated -- Andrew's hard no-misquote machine-check) + the Opal-branded email template + the Kimi captcha re-login flow.
</the_work>

<acceptance_criteria>
1. FT + WSJ fetch live (full article text, IP-strategy resolved); S3 store; SES-send to Austin; 3am-ET EventBridge orchestration; fail-loud.
2. Per-infra CTO arch-gate + safe-apply + deploy-completion-ledger; least-priv IAM (astn/* read + S3 write only).
3. The verbatim-fidelity gate (CTO app-layer) enforced -- no misquote in the CEO brief.
4. RAVC2 COO+CTO; CVO co-verifies the end-to-end + the verbatim-gate. cc MSTR.
</acceptance_criteria>
