<task_order>
<id>MDPF_CHANNEL_INDEPENDENCE.CI-C1C2</id>
<title>Closure rows 1 + 2 — CONTRACT C1 (bronze → silver) and CONTRACT C2 (silver → gold DDB). Event-driven, per-feed/per-partner, idempotent, arbitrary-date safe. BUILD AND VERIFY; THE DEPLOY LEG IS BLOCKED.</title>
<project>MDPF_CHANNEL_INDEPENDENCE</project>
<workstream>P0 — MDPF closure. When rows 1–12 are true, MDPF CLOSES.</workstream>
<issued_to>0.6.2_AE_PartnerETL~C</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-24T17:21Z</issued_at>
<status>staged</status>
<authorization>**ANDREW-DIRECT ~1720Z: "Go now, this is P0."** PRD `docs/architecture/MDPF_CHANNEL_INDEPENDENCE_PRD.md` @eaa8433547 §2.2. Fleet narrowed by Andrew; you are one of two Tier-2 lanes KEPT — CTO's reasoning: **you ran the whole converter chain today and know which read paths are REAL versus DOCUMENTED.**</authorization>

<references>
  <ref type="prd">PRD §2.2 (the three event contracts), §3a rows 1 + 2</ref>
  <ref type="input">Your own GC-BF1 @1b7e133ed9 / @08e47e8638 — the seven-step cycle, 42/42 landed, and **the three stale records you corrected** including the TRN read-path our runbook had wrong</ref>
  <ref type="sovereign">Andrew ~1648Z: *"bronze must always write to silver through an event-based, deterministic process. Receipt of bronze needs to immediately roll to silver writes. Similarly, the silver write needs to catalyze the gold DDB write."*</ref>
</references>

<scope>
**ROW 1 — CONTRACT C1: fires on EVERY bronze landing, PER FEED, idempotent, arbitrary-date safe.**
*Verified by:* land a **historical** bronze partition → silver appears, **no manual step.**

**ROW 2 — CONTRACT C2: fires on EVERY silver landing, PER PARTNER, idempotent.**
*Verified by:* the same, one layer up; **re-deliver an event → the row is UNCHANGED.**

>> **WHY YOU HAVE BOTH, AND WHY C2 IS NOT A STRETCH:** you exercised the entire bronze→silver chain today
   and — more to the point — **you found that our documented read path was wrong and the code's was right.**
   The TRN converter reads monolith bronze, not the local OneDrive folder our runbook claimed; you checked
   all four converters rather than the flagged one; **and you skipped an inert documented step and the run
   succeeded on all seven legs, which is the proof.** C2 is the immediate next hop from the layer you have
   in hand. **The contracts must be built against the REAL read paths, not the documented ones** — that is
   precisely the knowledge Andrew's fleet narrowing was meant to preserve.

**ARBITRARY-DATE SAFETY IS NOT OPTIONAL AND YOU HAVE THE EVIDENCE FOR WHY.** Row 1 says *arbitrary-date
safe*, and today established what happens without it: `0.6.2~B` found **both** backfill pullers NOT-CAPABLE —
`--date` reaching nine LABEL sites and zero REQUEST sites, so a targeted run lands the RUN DATE's data under
the target key at exit 0. **C1 must not inherit that shape.** A historical bronze landing must produce that
date's silver, and it must be demonstrable that it did.
</scope>

<explicitly_out_of_scope>
- **C3 (gold → platinum publisher)** — `0.7.0_AE_CloudOps`, respawning, rows 3 + 10 + manifest wiring.
- **The manifest itself** (§3/§3.1/§3.2, row 9) and **the roster** (§2.6, rows 7 + 8) — fresh lanes.
- **Row 4, the sever-a-channel exercise — `3.0.0_SA_CVO`.** ⚠ **You must NOT verify your own contracts'
  independence.** If you build C1/C2 and also run the exercise that proves channels are independent, the
  highest-stakes assertion in the PRD is verified by its author. Hand it over.
- Composition/carry-forward/frontier/label (rows 5, 6, 11, 12) — `0.4.0_DS_ClientPlatform~A`.
</explicitly_out_of_scope>

<forbidden_shortcuts>
Per `docs/doctrine/A_VALUE_MUST_CARRY_ITS_CLAIM.md` @d3681d1d0:
- **Row 1 arbitrary-date.** *Easiest pass:* land a bronze partition for **today**, watch silver appear,
  call it arbitrary-date safe. **Today's date is exactly what a date-blind path produces anyway.** Land a
  HISTORICAL partition and prove the silver carries THAT date's data — the `~B` failure mode, one layer down.
- **Idempotency (both rows).** *Easiest pass:* re-deliver an event, see no error, call it idempotent.
  **No error is not "row unchanged."** Compare the row before and after, byte-level.
- **"Fires on EVERY landing."** *Easiest pass:* demonstrate one feed and generalise. **Enumerate the feeds
  and state the denominator** — how many exist, how many you exercised.
- **Read paths.** *Easiest pass:* build against the runbook. **You already know the runbook was wrong once
  today.** Build against the code and say which you checked.
**MISSING THIRD STATE:** a contract is `fires | does-not-fire | FIRES-BUT-UNEXERCISED-ON-THIS-PATH`.
</forbidden_shortcuts>

<constraint_deploy_blocked>
⚠⚠ **THE DEPLOY LEG IS BLOCKED AND THIS IS THE CONSTRAINT THAT SHAPES YOUR WHOLE TO.**
GitHub Actions is **billing-blocked ORG-WIDE** — `lambda-deploy.yml` and `ec2-deploy.yml` are **REFUSED AT
DISPATCH** (`steps=0`, `runner=""`, no log), and CLAUDE.md Rule 1 makes Terraform the only Lambda mechanism.
**SO C1 AND C2 CAN BE BUILT AND VERIFIED BUT NOT LANDED.** Build to the gate and STOP.
**DO NOT improvise a path around CI** — no manual deploy, no console, no direct code push, no re-run loop.
Only Andrew can clear it. **A held lane under a P0 clock is exactly when someone invents a route**; do not.
If billing clears mid-flight, landing resumes on CTO's gate — do not re-plan for it.
</constraint_deploy_blocked>

<compiler_tools_mandate>
  <before_write>`comp-pipescript io` on every converter touched; `comp-iam service <lambda>` after any new boto3 call — **NECESSARY NOT SUFFICIENT**: for a NEW bucket/table/ARN use `aws iam simulate-principal-policy` with **ONE `--resource-arns` per call** and the positive control run **SEPARATELY** (Rule 22a).</before_write>
  <before_commit>`.tools/commit-gate.sh` (Rule 14); `comp-pipescript deployed`; `comp-validate` — `NO_CONFIG`/`ZERO_CHECKS` means UNVALIDATED, never signal SAFE on it.</before_commit>
  <after_commit>Session log with `## Compiler Tools`; `org/compiler-tools-log.md` in the same pass.</after_commit>
</compiler_tools_mandate>

<acceptance_criteria>
1. **C1: a HISTORICAL bronze partition landed → silver appears with THAT DATE's data, no manual step.**
   Date fidelity demonstrated independently of the pipeline's own claim.
2. **C2: a silver landing → the gold DDB row appears, per partner.** Re-deliver the event → **row byte-unchanged.**
3. **Feed/partner DENOMINATORS stated** for both — how many exist, how many exercised, which are UNEXERCISED.
4. **Per-row verdict** from `fires | does-not-fire | FIRES-BUT-UNEXERCISED-ON-THIS-PATH`.
5. Deploy-completion ledger opened at start, closed on proof — **or explicitly left open with the billing
   block named as the reason**, which is a legitimate close-out state today.
6. Explicit-Z; NEVER#4; `0824` ONLY — and note the `master_for()` gate refuses an UNKNOWN purpose but
   **cannot refuse a WRONG-but-known one** (your own retraction, @08e47e8638).
</acceptance_criteria>

<deliverables>
  - Report at `org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/`, written for CVO.
  - To CTO (gate) + COO. **Commit; do NOT push — COO is push operator (Andrew ~1600Z).**
</deliverables>

<notes>
**A THIRTEENTH ITEM GOES TO CTO'S GATE AS AN AMENDMENT WITH EVIDENCE** — not absorbed silently, not parked
into a successor project.
Your `dff7849616` log amendment is still outstanding with me; it goes in the next flush.
</notes>
</task_order>
