<to_id>DATA_PLATFORM.DC-OSINT</to_id>
<project>DATA_PLATFORM</project>
<title>Phase-1-DEEP DC-OSINT -- passive public-source correlation of the 4 vendors (zero vendor traffic; Option-A)</title>
<assigned_to>0.6.0_AE_PartnerETL (research/leverage lane) -- flag if bottlenecked -> request the +1 characterization lane (MSTR headroom)</assigned_to>
<verify>3.0.0_SA_CVO (ROE-compliance + the evidence-schema grounding)</verify>
<arch_gate>1.0.0_SA_CTO (folds into PRD S6b; rejects any forbidden-tier drift)</arch_gate>
<issued_by>2.0.0_SA_COO (CTO methodology-expansion routing 145443Z; Andrew-ratified Recon ROE)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project DATA_PLATFORM, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: queued</status>
<!-- QUEUED behind the critical path (DC0 harness + DC-REV anchor). Zero-vendor-traffic = can run anytime/parallel; 0.6.0 picks up after the fast-follows or a +1 lane takes it. -->
<roe>MANDATORY: complies with docs/architecture/DATA_PLATFORM_RECON_ROE.md -- this is PURE OPTION-A (passive, zero vendor traffic). The forbidden tier (scanning/fuzzing/auth-testing/unauthorized-access) is HARD-EXCLUDED.</roe>

<objective>
Reconstruct each vendor's (BD/Orion/Eclipse/SmartX) tech-stack + service-architecture + endpoint surface from PUBLIC sources ONLY -- zero vendor traffic. Feeds the endpoint-enumeration (corroborates the crawl catalog) + the partner-scoring (security-posture + architecture-fit dimensions).
</objective>

<the_work>
Passive public-correlation (no vendor interaction): GitHub orgs/repos + npm/package-lockfiles, CT-logs (cert transparency -> subdomains/hosts), passive-DNS + public scan-datasets, job-postings (tech-stack tells), SOC2/security pages, public SDKs + mobile-app bundles. Cross-correlate -> per-vendor public-intel profile (stack/frameworks/service-names/hosts/disabled-routes/security-posture). Apply the RECON-RIGOR evidence-schema (Observation/Evidence/Inference/CONFIDENCE/ALTERNATIVE/Business-significance).
</the_work>

<acceptance_criteria>
1. Per-vendor public-intel profile (4 vendors), evidence-schema-grounded, confidence-tiered.
2. Corroborates/extends the crawl catalog (DC1-3) + feeds the 6-dim partner-scoring (security-posture + architecture).
3. ROE-compliant: 100% Option-A, zero vendor traffic (CVO verifies).
4. RAVC2 COO + CTO; folds into the DC-REV/DC-LEV synthesis.
</acceptance_criteria>
