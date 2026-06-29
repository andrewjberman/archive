# TASK ORDER — SCHWAB_SSOT.DERISK-1

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>HIGH — Andrew-GO'd Schwab-SSOT migration de-risk (validate-first; feeds the PRD). START after the off-cycle bd-49f-runner confirms the 49f silver unfreeze (AC#3).</priority>
<date>2026-06-29</date>

## Context

Andrew GO'd the Schwab-as-SSOT migration for 49F today. The custodial data path goes Schwab-native.
This is a REVERSIBLE feasibility spike (tear down after) — one of two validate-first de-risk groundings
CTO's migration PRD will cite (CTO briefing 20260629T142313Z). You're the fit: you just stood up the 49f
EC2 box + interactive auth + scheduler + S3 sync for the durable port — the Quartz pull is the same shape.

## Objective

Prove that an unattended Schwab SI2-Desktop pull can land in S3 from an EC2 Windows box.
**MILESTONE = ONE unattended pull lands in `s3://opal-data-schwab/01_raw`.**

## Scope (per CTO brief + docs/architecture/SCHWAB_SDD_DELIVERY_BRIEF.md — keep that brief LOCAL)

1. Stand up an EC2 **Windows** box.
2. Install **SI2 Desktop** (ClickOnce .NET app).
3. One-time **interactive login** (steady-state is OTP-FREE + durable via the x-refresh-token per the UA's
   feasibility — read SCHWAB_SDD_DELIVERY_BRIEF.md; UA 0.0.1 has the feasibility context to advise).
4. Let SI2's **built-in scheduler** run **AllNewFiles** unattended -> land locally.
5. **`aws s3 sync`** the landed files -> `s3://opal-data-schwab/01_raw`.

## Risks to VALIDATE (these are the de-risk deliverable, not just the happy path)

- **ClickOnce auto-update** — does an SI2 auto-update break the unattended box / require interactive re-consent?
- **RDP re-auth cadence** — how often does the Windows session / RDP need re-auth, and does it interrupt the unattended scheduler?
- **TOTP-seed-to-SecretsManager** as a re-enrollment contingency — can the TOTP seed be captured to Secrets Manager so the box can be re-enrolled without a fresh manual interactive step (the durability story)?

<compiler_tools_mandate>
- `comp-iam service` on the EC2 box role for the s3 sync (PutObject opal-data-schwab/01_raw) before relying on it.
- Ground the milestone against the LANDED S3 object (an actual file in opal-data-schwab/01_raw), not the box-side "it ran" — NEVER#7.
</compiler_tools_mandate>

<cross_domain_coordination>
REVERSIBLE spike — stand up + tear down. Writes only to opal-data-schwab/01_raw (the existing Schwab raw prefix; coordinate with the 49-schwab-conv AE-owned ingest if a live pull could collide with a manual delivery — this is a validation pull, keep it clearly marked/segregated so it doesn't pollute the production Schwab silver converters). No production cutover. UA 0.0.1 advises on the SDD feasibility.
</cross_domain_coordination>

<acceptance_criteria>
1. ONE unattended SI2 AllNewFiles pull lands a file in `s3://opal-data-schwab/01_raw` (S3-verified object, not box-side claim).
2. The 3 named risks each have a VALIDATED finding: ClickOnce-auto-update behavior, RDP re-auth cadence, TOTP-seed-to-SM re-enrollment feasibility — documented as a de-risk brief.
3. Reversibility confirmed — the box is torn down (or parked) after; no lingering cost/exposure.
4. RAVC to 2.0.0_SA_COO + CC 1.0.0_SA_CTO (PRD input) with the S3-landed evidence + the 3 risk findings.
</acceptance_criteria>

## Sequencing

STAGED — START after the off-cycle bd-49f-runner you're firing confirms the 49f silver unfreeze (AC#3)
+ comp-freshness bd PASS. The GATE-B lock build stays HELD (CTO thin-tether right-sizing), so this is
your next substantive task. UA 0.0.1 has the SDD feasibility context — consult before standing up the box.
