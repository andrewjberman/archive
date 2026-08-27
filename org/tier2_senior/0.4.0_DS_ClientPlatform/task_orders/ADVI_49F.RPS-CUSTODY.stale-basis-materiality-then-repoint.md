# TO ADVI_49F.RPS-CUSTODY — a CLIENT-FACING figure is valued on JULY-23 custody. MATERIALITY FIRST, repoint second.

<task_order id="ADVI_49F.RPS-CUSTODY" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform (producer-owner, WS-E script)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T23:44Z</issued>
<status>complete 2026-08-27T17:33Z -- ALL SEVEN AMENDED CRITERIA PASS (RPS-1, 1b, 1c, 2, 3, 4, 5); proof instance VALID TRUE rc=0 over the 7-id set. RPS-1 delta LARGE: served client-facing non_model_aua understated +$91,476,329.17 / +63.07% at as_of 2026-08-26, drifting -$1.94M/day. RPS-2 caveat REQUIRED, text ACCEPTED by COO 76210 s.2 (COO surfacing to Andrew). RPS-3 repointed to the CORRECTED target 08242234 (NOT the TO's original 08335338, disowned by issuer 76210) @d5fd2e4c79, deployed and verified on the DEPLOYED BYTES. RPS-4 basis stated in the emitted row. Deploy ledger CLOSED: org/critical_paths/change_management/advi-49f-rps-custody-wse-repoint-20260827.md. NOT CLOSED BY THIS TO: the 23 served partitions carrying the July-23 basis (no backfill authorized; caveat is the treatment) and the false Rule-25 dormancy marker (COO lane).</status>
<priority>P1 — client-facing TODAY</priority>
<authority>AE_CloudOps row 3 (233851Z, measured during the feeder-regression repair) + CTO priority endorsement with three riders (234046Z).</authority>
</task_order>

## The finding
`opal-data-bd/schwab/silver/rps/` is **27 DAYS STALE** — 634 materialised partitions, newest
`date=20260723`. **WS-E reads it LIVE** for `partner_custody_total` (`/mdpf/custody_source =
"schwab"`). So **49F's `non_model_aua` — a client-facing figure — is computed against a July-23
custody snapshot**, and did so again in tonight's recovered catch-up
(`49f_straight_rps_custody_minus_smartx_model_schwab_native`).
Successor exists: `opal-data-assets/schwab/08335338/silver/fact_rps/`.

**AE correctly re-pointed NOTHING** — re-cutting a custody basis inside a regression repair is how a
repair becomes its own incident.

## ⛔ RIDER 1 — MATERIALITY IS PRINTED FIRST, BEFORE ANY REPOINT
**Your FIRST act is the delta read**, not the fix: `partner_custody_total` computed from the
**July-23 legacy partition** vs the **successor's current partition**, side by side, both denominators
printed.
- **Delta small** -> the repoint is calm and proceeds normally.
- **Delta large** -> **the recovered headline needs a STATED CAVEAT wherever it is quoted** until the
  repoint lands, and you tell me that before anything else.
**Measured either way. Do not repoint before this number exists** — a repoint that silently moves a
client-facing figure by an unknown amount is the change we would least be able to explain afterwards.

## RIDER 2 — THE REPOINT ITSELF
Producer-owner act (WS-E script), deploy through the normal cycle, **AFTER** the materiality print —
not with it. It changes a **custody basis inside a client-facing figure**, so it carries served-
semantics weight: state the basis, and do not let a correction ship silently.

## Acceptance criteria
- **RPS-1 MATERIALITY PRINTED** — legacy vs successor `partner_custody_total`, side by side, both
  denominators, before any change.
- **RPS-2 CAVEAT DECISION STATED** — whether the recovered headline needs one, on the RPS-1 number.
- **RPS-3 REPOINT LANDED** to the successor, verified on the **stored/served artifact** (Rule 22a
  APPLIED layer), never rc=0.
- **RPS-4 BASIS STATED** in the artifact so the change is visible downstream rather than silent.
- **RPS-5 proof instance VALID rc=0**, ids `RPS-1..RPS-5`, run against the named expected-id set with
  the TRUE rc cited (measured without a pipe).

<proof_of_spec>
  <!-- AMENDED 2026-08-27 by COO ruling 76210 s.5: RPS-1 / 1b / 1c stand as three separate
       measured rows. Element updated by 0.4.0_DS_ClientPlatform to match the issuer's own
       written amendment (implementing, not adjudicating) so the machine-readable half does
       not contradict the ruling prose above it. -->
  <expected_criteria>RPS-1,RPS-1b,RPS-1c,RPS-2,RPS-3,RPS-4,RPS-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_49F.RPS-CUSTODY_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

---

# ⛔ SEPARATE DEFECT ROW — **THE FALSE RULE-25 MARKER IS MINE**

`opal-data-bd/schwab/silver/rps/` carries a **Rule-25 retention marker dated 2026-08-18 — MY OWN
DECLARATION** — stating it is *"DORMANT AS A PRODUCER … no live reader after 2026-08-18 —
B_00.canonical_holdings re-pointed to the successor."*

**THE "NO LIVE READER" CLAIM IS FALSE.** WS-E reads that exact prefix daily, for a client-facing
figure.

**HOW I GOT IT WRONG — the zero-access-oracle class, and it is already in my own memory:** I stamped
a dormancy marker from **a reader census that enumerated the wrong plane.** `B_00` had indeed been
re-pointed, so the plane I looked at was clean — and WS-E was never on it. **A census that cannot see
a reader returns "no readers" and "no readers" with a blind census are byte-identical.**

**WHY THIS IS ITS OWN ROW AND NOT A FOOTNOTE (CTO's rider 2):** the marker will **mislead whoever
next reasons about DELETING that tree.** A false dormancy stamp is not a stale label — it is a
standing invitation to delete a live dependency. **Rule 25 is explicit that dormant is never a
deletion warrant, and this is exactly why.**

**REMEDY, and it is not just correcting this one marker:** whoever owns the marker process **re-runs
the reader census with the WS-E miss as the FIXTURE** — otherwise the next Rule-25 stamp carries the
same blindness. **Correcting this marker alone fixes the instance and leaves the instrument.**
Owner: COO (mine to route; the marker is mine).

---
## ⚖ COO RECONCILIATION 2026-08-27 (P0.2 record pass, D2 brief @e4f7ecbfdc)

Verdict: **STAND, unchanged.** This TO is orthogonal to the 08-26 TWR remediation design (custody
basis staleness in WS-E, not the flow-ledger/TWR chain) — no clause is superseded or absorbed.
Unstarted; the issuing state (staged, GO paired, materiality-first riders) remains the dispatch
surface. Re-seats to a DS-class producer-owner seat on Andrew's word (08-27 seat list); if the legacy prefix
is still the live basis, the staleness has only grown since the 08-19 measurement (27d then; re-read
at RIDER 1, not assumed here) — which raises RIDER 1's urgency, not its design.

**D2 LOCK-IN RIDER (CVO 76086, additive) on RPS-5:** validated BY RC (the TRUE-rc clause above
already binds), and the validator invocation + its TRUE rc recorded as evidence IN the instance.
GO pairs only AFTER `3.0.0_SA_CVO` cert step-zero; the re-seat is the S6 word @1d761ded1f.

---
## ⚖ COO RULING 2026-08-27 ~16:5xZ — THE REPOINT TARGET, on the RIDER-1 print (the hold this face records is RELEASED into the amended sequence below)

**The seat's hold was CORRECT and the TO's named successor is MINE to disown: this face's
"Successor exists: `opal-data-assets/schwab/08335338/silver/fact_rps/`" was transcribed from the
AE row-3 finding without account verification — a name-is-not-identity defect by the issuer.** The
seat's fixed-vintage control (legacy == `08242234` to the cent; `08335338` differs by +$91.5M /
+63.07%) discriminates the accounts cleanly: the legacy basis IS the `08242234` population.
`08335338` = ADVI Advisor Intelligence (Black Diamond); `08242234` = MDPF Model Portfolios
(SmartX) — never substitute one for the other (standing law, and this is the trap firing).

**AMENDED SEQUENCE, binding:**
1. **⛔ DO NOT REPOINT TO `08335338` — ever, under this TO.** A repoint there moves a served
   client-facing figure +63% by silently changing its ACCOUNT, not its freshness.
2. **RPS-1b — MEASURE THE TRUE SUCCESSOR:** `opal-data-assets/schwab/08242234/silver/fact_rps/`
   (or the measured 0824-tree equivalent): EXISTS + FRESH (newest partition, production cadence),
   denominator printed. **A successor that is not currently produced is not a successor.**
3. **RPS-1c — RE-PRINT THE MATERIALITY ON THE TRUE PAIR:** legacy@2026-07-23 vs the 0824 successor
   CURRENT, side by side, both denominators. **The RPS-2 caveat decision RE-BASES on THIS delta** —
   the +63% legacy-vs-0833 print is evidence for the wrong-account finding, NOT the staleness
   caveat's basis (it conflates account-population delta with time drift; the fixed-vintage
   control proved the account is the variable).
4. **RPS-3 (amended target): repoint WS-E to the 0824 successor** — RIDER 2 disciplines unchanged
   (after the print, normal cycle, APPLIED-layer verification, basis stated). If step 2 finds the
   0824 tree stale or unproduced, **HOLD and report — a repoint to a stale successor re-creates
   this exact defect one tree over.**
5. RPS-4/RPS-5 unchanged; the proof instance cites the AMENDED criteria set (RPS-1 original print +
   1b + 1c stand as three separate measured rows).
