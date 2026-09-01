# AUTH_SELFHEAL.TO-A1 — the cookie-riding consumer inventory

**To:** `0.6.2_AE_PartnerETL`
**By:** `2.0.0_SA_COO`
**Issued:** 2026-08-31T23:45Z
**Project:** `AUTH_SELFHEAL` (D8, `macro_code: AUTH`)
**Cut from:** decomp cell **A1**, run `auth-selfheal-consumer-class/20260831T231221Z` @`3a8bfec867`
**PRD:** `AUTH_SELFHEAL_PRD_v0.1.md` @`094d18aaee` — DoD **item 1**, scope §3 item 4

<status>pending</status>

<decomp_ref>workflows/atom_decomposition/runs/auth-selfheal-consumer-class/20260831T231221Z/rectangle.c0.json
-- discharges cell AUTH-a-1 (short label A1, "THE COOKIE-RIDING CONSUMER INVENTORY").
This TO discharges that cell ALONE. It does NOT discharge AUTH-a-2 (the session-age instrument),
and it is explicitly BLOCKING for AUTH-b-1 through AUTH-b-5, whose denominator this cell produces.
AUTH-x-1 and AUTH-x-2 are NOT_MEASURABLE and are not dischargeable by any TO.</decomp_ref>

<proof_of_spec>
  <expected_criteria>AC1,AC2,AC3,AC4,AC5,AC6</expected_criteria>
  <instance_path_grammar>org/tier2_senior/{assignee_folder}/deliverables/AUTH_SELFHEAL_PROOF_OF_SPEC_{seat}_{YYYYMMDD}.json</instance_path_grammar>
  <group id="inventory-AC1-AC6" status="NOT_YET_MINTED" instance_path="org/tier2_senior/0.6.2_AE_PartnerETL/deliverables/AUTH_SELFHEAL_PROOF_OF_SPEC_062_20260831.json"/>
</proof_of_spec>

---

## ⛔ UNCERTIFIED DECOMP

This TO is cut from a decomp that **`3.0.0_SA_CVO` has not certified**. Certification is requested and
outstanding. The issuer states this on the face per Stage-3 rather than letting the TO imply a
certified provenance. **If certification changes cell A1, this TO changes with it.**

## WHY THIS TO EXISTS AND WHY IT IS FIRST

Every other cell in the decomp (B1–B5) asserts a property over *"every cookie-riding consumer."*
**That set does not exist.** A per-property TO cut before this one closes would be accepted against
whatever population the executing seat assembled for itself — error direction **FALSE PASS**.

**A1 is also the only cell whose work is placement-independent.** D8's placement is an open sovereign
call and every resource-touching cell is frozen behind it; a repo/live census returns the same answer
from either fabric, so this cell can proceed while that call is pending.

## THE TASK

Produce the inventory the PRD's DoD item 1 requires: **every consumer that depends on a BD vendor
session, across both firms**, each row carrying **secret · mint schedule · fire schedule · exposure
window**.

## ⭐ THE ISSUER'S MEASUREMENT — A STARTING POPULATION, NOT AN ANSWER

Two censuses were run at the COO seat. **They disagree, and that disagreement is the point:**

```
  I1  secret-name grammar 'blackdiamond/[a-z0-9]+/session'       48 files
  I2  shared-loader tokens 'load_bd_session|...|\.bd\.identity'  41 files
      UNION 56 | INTERSECTION 33 | SEEN BY EXACTLY ONE INSTRUMENT 23  (41% of the union)

  only I2 sees:  dump_enriched_templates.py, probe_holdings_nzf.py        <- real bronze producers
  only I1 sees:  cot_backfill_date_probe.py, bd49f_pull.tf,
                 bd49f_reporting_pull.tf, cot_rebalancer_runner.tf
```

> **A consumer that reaches the cookie through the shared loader without naming the secret is invisible
> to I1. A consumer named only in terraform wiring is invisible to I2. THE ERROR DIRECTION IS TOWARD
> ABSENCE** — a missed consumer looks exactly like a consumer that does not exist.

**Candidate runtime consumers (~12), to be confirmed or refuted, not adopted:**
`bd-49f-fees-runner` · `bd-49f-freshness-probe` · `bd-49f-runner` · `bd-cot-freshness-probe` ·
`cot-rebalancer-runner` · `opal-assets-bd49f-daily-pull` · `opal-assets-bd49f-reporting-pull`
(+`insurance_leg`) · `cot_bronze_ingest.py` · `cot_backfill_date_probe.py` ·
`dump_enriched_templates.py` · `probe_holdings_nzf.py` · `bd_endpoint_sweep.py`

**Supply side — NOT consumers, must not be counted as such:** `bd-49f-keepalive` ·
`bd-cot-keepalive` · `bd-49f-session-trigger` · `cot-bd-session-trigger` · both auto-login EC2 boxes ·
`cot_bd_session_fetch.py`

## ⛔ THE THIRD INSTRUMENT I DID NOT TAKE — AND IT MAY BE THE BEST ONE

Both of my censuses read **the repo**. A genuinely independent framing exists and this seat should
consider taking it: **IAM principals holding `secretsmanager:GetSecretValue` on the session secrets,
on the LIVE plane.** That answers *"who CAN ride the cookie"* rather than *"who mentions it in
source"* — a different question with a different failure mode, and it would catch a deployed consumer
whose source is not in this repo at all.

⚠ **AND THE TRAP ON THAT INSTRUMENT, from tonight's E7 re-measurement at this very seat:** in a
permission simulation, **the rows you expect to be DENIED can never validate your ARN** — a wrong ARN
denies everything. **Only a row you expect to be ALLOWED can.** Any principal sweep here carries a
positive control or it is unable to detect its own subject error.

## ACCEPTANCE CRITERIA

1. **AC1 — the inventory exists** as a durable artifact, one row per consumer, with the four columns.
2. **AC2 — the denominator is printed and the method is named**, including which instruments were run
   and what each one structurally cannot see. A row count without its instrument is not an inventory.
3. **AC3 — CONSUMER vs SUPPLY-SIDE is an explicit column**, not an implicit judgement. The keepalive
   and mint paths are not consumers and a reader must not have to infer that.
4. **AC4 — every row carries its claim** (`measured` / `inferred` / `held` / `absent`) per the PRD's §0
   binding constraint. A row whose mint schedule is unknown says `absent`; it does not omit the field.
5. **AC5 — the ≥2-instrument requirement is discharged or refused with reason.** If this seat judges
   one instrument sufficient for some subset, say which subset and why — do not silently narrow.
6. **AC6 — disagreement between instruments is REPORTED, not resolved by picking a winner.** The union
   is the candidate set; a member seen by only one instrument is a finding about the instruments.

## BOUNDARIES

- **READ-ONLY as to PRODUCTION STATE: this TO authorizes no code, no terraform, no deploy, and no
  production write.** It is a census; its deliverable is a document.
- ⚠ **EGRESS — CORRECTED AFTER THIS TO WAS FIRST DRAFTED, READ THIS ROW RATHER THAN ASSUMING.** The
  first draft said "NO VENDOR EGRESS." That is **superseded** by Andrew-direct 2026-08-31 ~23:4xZ,
  verbatim: *"if its easier to make it explicit, all vendor egress is allowed tonight for all agents."*
  **ALL AGENTS · ALL VENDOR EGRESS · TONIGHT.**
  - **This TO still does not NEED egress** — the inventory is answerable from the repo and the AWS
    control plane. If this seat judges a vendor call genuinely necessary, it is permitted; say why.
  - ⛔ **The one surviving bound is TEMPORAL and undefined: "tonight."** Operative reading, stated so
    it can be corrected — it runs through the current overnight working window and does **not** roll
    into a new working day. **A lapsed "tonight" is not a standing grant.**
  - ⛔ **A grant to spend egress is not a licence to skip judgement.** "Allowed" is not "advisable."
- ⚠ **THE TWO HOLDS THIS TO'S FIRST DRAFT LEANED ON ARE DISCHARGED** (Andrew-direct ~23:4xZ): the
  2026-08-19 BUILD-ONLY / DEPLOY-SERVE-HELD cap is **RELEASED** and the 2026-08-21 49F-flip hold is
  **DISCHARGED for the serve act**. Neither constrains this TO, and no seat should quote this file's
  earlier framing as evidence they stand.
- **This is an inventory, not a remedy.** Do not fix an ordering violation you find — record it; B1
  owns it and is frozen behind placement.
- **Do not build a detector.** If the inventory suggests a monitor, that is HELD under the alarm
  moratorium / `GLOBALALARM` D10. **This project FIXES; it does not NOTIFY.**
- **Do not close a PRD §5 open quantity by reasoning.** Session age at failure stays open.

## ⚠ A PRE-EXISTING ENCUMBRANCE ON THIS SEAT — NAMED, NOT IGNORED

`to-check --all` shows one PENDING TO on this serial from a **different** project:
`COT_SUPERVISED.G1-G7.retroactive-filter-and-portfolio-group` (issued by me 2026-08-20, 11 days old,
co-assigned `0.2.0_DS_PortfolioAnalytics` + this seat for the **bronze fetch leg G1**).

**This seat is BARRED from acting on that TO while seated on `AUTH_SELFHEAL`** (Rule 27, one project
per instance). It is **my** face to triage — I issued it — and I am carrying it as an open item rather
than leaving it to be discovered as a collision. **This TO does not create that encumbrance and does
not resolve it.** If that face is in fact world-done, say so and I will close it SUPERSEDED rather than
re-execute it.

## RAVC

Report the inventory artifact's path, the instruments run with each denominator, the consumer /
supply-side split with its counts, and — explicitly — **what the inventory still cannot see.** A stated
blind spot is worth more here than a clean-looking table, because the next five cells will be graded
against this denominator.
