<to_id>DATA_PLATFORM.DC0</to_id>
<project>DATA_PLATFORM</project>
<title>Phase-1-DEEP DC0 -- reusable post-auth stealth crawl+catalog harness (ride-existing-session + HARD live-pipeline isolation)</title>
<assigned_to>0.7.0_AE_CloudOps (lead) + 2nd AE-CloudOps lane (MSTR-spawning) -- Playwright/EC2/exporter</assigned_to>
<consult>0.4.0_DS_ClientPlatform (catalog schema + the characterization handoff to DC-REV)</consult>
<verify>3.0.0_SA_CVO (verify the HARD live-pipeline isolation + fail-safe; reconcile the catalog per the D3 §14 basis taxonomy)</verify>
<arch_gate>1.0.0_SA_CTO -- the stealth/isolation/live-pipeline-protection design is arch-gated BEFORE any live crawl runs (MANDATORY; risk #1)</arch_gate>
<issued_by>2.0.0_SA_COO (Andrew-direct DATA_PLATFORM deep-expansion; CTO Phase-1-DEEP decomposition 141811Z; posture RIDE-EXISTING+HARD-ISOLATION Andrew-direct 2026-06-24)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<!-- The enabling infra for Phase-1-DEEP: built ONCE, parameterized per vendor; DC1-3 (per-vendor crawl) configure it. GATES on CTO's arch-gate of the isolation/stealth design before any live crawl. -->

<objective>
ONE reusable, per-vendor-parameterized post-auth crawl+catalog harness that COMPREHENSIVELY enumerates each vendor's endpoint surface by RIDING the existing authenticated exporter sessions -- with HARD isolation from the live-pull pipelines + fail-safe stealth. Enables the comprehensive enumeration (all 4 vendors) feeding DC-REV (reverse-ETL) + the SmartX leverage-map.
</objective>

<the_work>
- RIDE the EXISTING authenticated exporter sessions (cot/BD, inf/Orion+Eclipse, smartx-exporter) -- NO new logins (no MFA/detection trip). Playwright drives the REAL UI -> walk every screen/route/drill-down -> capture every XHR (method/path/params/response-shape) -> candidate-probe gaps (sibling resources/param variants, carefully) -> bronze(raw captures) -> silver(normalized endpoint catalog) -> gold(characterized: call-pattern + what-it-serves).
- STEALTH + HARD ISOLATION (Andrew posture = the LOAD-BEARING constraint): human-paced (randomized human-speed delays, no burst); rate-limited well under any ceiling (SmartX 20/min known -> <=17/min; BD/Orion unobserved -> conservative); NEVER concurrent with the live pull + OFF-PEAK + ISOLATED from the live-pull schedule; monitor 429/captcha/session-invalidation -> back off + alert; FAIL-SAFE = detect -> backoff -> NEVER burn the live session (the live ADVI/MDPF pipelines depend on it -- a burned session breaks LIVE serving).
- Parameterized per-vendor (the cot/inf shared-code pattern) so DC1-3 just supply config.
- S3-artifact deploy (Rule 12); rides the exporter EC2 infra (Rule 7-12); comp-graph coverage; ds-gate per .py.
</the_work>

<acceptance_criteria>
1. Reusable per-vendor harness: rides the existing session, walks the UI exhaustively, captures all XHRs -> bronze -> silver(catalog) -> gold(characterized).
2. HARD live-pipeline isolation PROVEN: the harness cannot run concurrent-with / contend-with / burn the live-pull session (CTO arch-gate + CVO verify the fail-safe + the schedule-isolation).
3. Stealth: human-paced + rate-limited + off-peak + 429/captcha/session-invalidation backoff.
4. CTO ARCH-GATES the isolation/stealth design BEFORE any live crawl runs (mandatory -- risk #1 live-pipeline-disruption + risk #2 session-lockout).
5. RAVC2 COO+CTO; CVO verifies the isolation + the catalog basis.
</acceptance_criteria>
