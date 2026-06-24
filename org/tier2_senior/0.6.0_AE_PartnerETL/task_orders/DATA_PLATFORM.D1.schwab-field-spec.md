<to_id>DATA_PLATFORM.D1</to_id>
<project>DATA_PLATFORM</project>
<title>D1 Schwab field spec -- full SI2 feed field/grain/join-key audit + ingest-automation scoping</title>
<assigned_to>0.6.0_AE_PartnerETL (AE-lead -- SI2 feed/RPS ingest expertise + ingest-automation; DS-consult for field-modeling)</assigned_to>
<!-- RE-ASSIGNED 0.7.0->0.6.0 2026-06-24 (COO offloaded D1/D4 to the 2nd AE lane to keep base-AE on .07/.05/D2-pull). DS-consult = 0.4.0. -->

<consult>0.4.0_DS_ClientPlatform (field-modeling)</consult>
<verify>3.0.0_SA_CVO (reconcile-verify spec vs live Schwab data / DATA_DICTIONARY)</verify>
<issued_by>2.0.0_SA_COO (DATA_PLATFORM Phase-1 decomposition; Andrew-direct via CTO 2026-06-23; PRD S6/S11; LD-0209)</issued_by>
<issued_date>2026-06-24</issued_date>
<status>active</status>
<!-- This is a SPEC/AUDIT (Phase-1), NOT a build (Phase 2/3 build against it). SmartX/Schwab partnership-terms parallel, no external gate (Andrew-confirmed). -->

<objective>
Produce the complete Schwab field spec -- the audit of every field the SI2 feed carries, so we know exactly what custodian data exists + what a proprietary platform would have to own. SPEC-OF-RECORD: PRD S6 row D1 (docs/architecture/DATA_PLATFORM_PRD.md).
</objective>

<the_work>
Every field across the FULL SI2 feed (RPS/BDRECPOS, ACC, TRN, ULN, RLD, SEC, TCF, + the rest) -- name / type / grain / join-keys; what we currently CAPTURE vs what's AVAILABLE; the API/SFTP-vs-desktop-pull reality + the automation options. Seeds: data/schwab/DATA_DICTIONARY.md + the unbuilt data/schwab/ warehouse design.
KEY DEFICIENCY to scope (PRD insight #1): Schwab ingest is manual / single-firm / monthly / desktop-client file-pull, and the canonical silver/RPS positions table is EMPTY -- scope the path to programmatic/automated multi-firm ingest (API/SFTP or scheduled SI2 auto-sync).
</the_work>

<acceptance_criteria>
1. Complete field-spec doc: every SI2 feed-type, every field at field-grain (name/type/grain/join-keys).
2. Capture-vs-available gap mapped (what we ingest today vs the full feed).
3. Ingest-automation path scoped (the manual-desktop-pull -> programmatic/multi-firm options + tradeoffs).
4. CVO reconcile-verifies the spec vs live Schwab data + the DATA_DICTIONARY.
5. SPEC only -- no build. RAVC2 COO + CTO.
</acceptance_criteria>
