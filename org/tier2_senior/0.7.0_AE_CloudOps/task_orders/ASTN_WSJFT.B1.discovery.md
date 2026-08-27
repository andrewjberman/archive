<to_id>ASTN_WSJFT.B1</to_id>
<project>ASTN_WSJFT</project>
<title>ASTN_WSJFT B1 (discovery, FIRST) -- WSJ/FT section-URLs + Bright-Data PAYWALL access-method + integration prereqs (one-shot, not a crawler)</title>
<assigned_to>0.7.0_AE_CloudOps (AE/cloud-ops lead; PACED behind the DC2-Eclipse recon + hot priorities)</assigned_to>
<arch_gate>1.0.0_SA_CTO (arch-gates the B2 verbatim-fidelity gate + the legal-posture framing)</arch_gate>
<verify>3.0.0_SA_CVO</verify>
<issued_by>2.0.0_SA_COO (Andrew-direct via CTO 184909Z; PRD docs/architecture/ASTN_WSJFT_PRD.md; new ASTN macro)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ASTN_WSJFT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<!-- PACED: contained scheduled product, behind the hot recon (DC2-Eclipse) + nightly priorities. B1 is the load-bearing FIRST open item (the paywall-access-method shapes everything downstream + the ToS posture). -->
<!-- DISCOVERY-RESULT (CTO ran it live 2026-06-24): WSJ one-shotter = FULL article text (citable-bullets feasible) -> WSJ-path GO. FT one-shotter = paywall-wall (body=subscription-page, headline-only). ANDREW DECISION: hold BOTH subs -> FT IN via the authenticated-session-ride (Bright-Data Scraping-Browser login -> session-cookies parked-in-SM -> 3am one-shotter rides -> refresh; MFA via inf-otp-relay/device-cookie -- the established parked-auth pattern, 4th instance). Bright-Data key ROTATED + ISOLATED (4 other BD consumers on distinct keys). FT GATED on Andrew handing WSJ/FT login-creds -> CTO SM-store + authed-full-body-test. BOTH-in (NOT WSJ-only-v1). -->

<objective>
The load-bearing discovery for the CEO daily WSJ/FT digest (3am-ET one-shot: Bright-Data pull top ~15-20 WSJ+FT stories -> GPT-5.4 cited-bullet summary -> SES email to the CEO, grouped by section). Surface the section-URLs + the Bright-Data ACCESS-METHOD options (the PAYWALL path) + confirm the integration prereqs, so Andrew can decide the access-method + ToS-posture (Andrew-owned).
</objective>

<the_work>
- WSJ/FT key SECTION-URLs (the top-sections to digest for the ~15-20 stories).
- the Bright-Data ACCESS-METHOD for the PAYWALL (WSJ/FT are paywalled/anti-bot): subscription-entitled [preferred -- our own subscription creds] vs Web-Unlocker. SURFACE both + the ToS-implication of each -> Andrew decides.
- integration PREREQS: Bright-Data account/key (NEW integration? -- confirm exists or needs-provisioning), the GPT-5.4 key, the SES verified-from-address (+ Austin opted-in).
- confirm ONE-SHOT (a scheduled 3am-ET pull, NOT a crawler -- bounded fetch of the named sections).
</the_work>

<acceptance_criteria>
1. Discovery deliverable: section-URLs + access-method-options (each with its ToS-implication) + prereq-status (have/need per integration).
2. ANDREW-OWNED decision surfaced (NOT decided by the lane): the paywall-access-method + the ToS/copyright posture -- routed through SCTY's external-content/vendor-diligence framing (consistency w/ the recon-ROE). B1 surfaces the options; Andrew rules; CTO arch-gates the legal-posture framing.
3. Feeds B2 (extract + GPT-summarize + the VERBATIM-FIDELITY machine-gate: each cited bullet = an exact normalized substring of the fetched article, non-verbatim rejected/regenerated -- CTO arch-gate) / B3 (email+SES) / B4 (3am-ET cron + one-shot Lambda + fail-loud).
4. RAVC2 COO + CTO.
</acceptance_criteria>
