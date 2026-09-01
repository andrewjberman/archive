# TO D12_PLATFORM_OPS.DE3-SITEZ — the browser end-to-end exercise (the criterion W1 lost, rebuilt as its own TO)

<task_order id="D12_PLATFORM_OPS.DE3-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>⛔ **PENDING — ANDREW'S SERIAL CONFIRMATION. SEE DE1 §0. THIS TO IS NOT YET ISSUED.**</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T01:3xZ (authored; NOT issued)</issued>
<status>NOT-YET-ISSUED. DEP-BLOCKED on DE1 + DE2.</status>
<priority>P1 — this is the acceptance the whole workstream was missing.</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~01:2xZ TO-series instruction (17286) + "obviously we need a frontend flow
that ties in with this." PRD `docs/architecture/D12_PLATFORM_OPS_PRD.md` WS-2 exercise, restored to its
original BROWSER grain. Decomp AMENDMENT 3.
</authority>
<proof_of_spec>
  <expected_criteria>DE3-1,DE3-2,DE3-3</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D12_PLATFORM_OPS.DE3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 1. ⭐ WHY THIS IS ITS OWN TO AND NOT A LINE IN DE2

**This is the criterion the workstream already lost once**, and burying it inside a build TO is how it
got lost. The PRD's WS-2 exercise reads *"an account with MFA enabled **cannot reach the dashboard**
without a live code"* — a **browser** outcome. My W1 TO rendered it *"exercised end to end **against
the deployed handler**, not a unit test"* — an **API** outcome — and W1 then scored an honest **10 of
10** on a feature no human could use.

> **A CLAUSE THAT NAMES THE INSTRUMENT CAN RELOCATE THE SUBJECT WHILE READING AS TIGHTENING.**
> The defect was in my TO, not in anyone's build.

**Giving the browser outcome its own TO, its own id and its own proof row means it cannot be satisfied
by a proxy that happens to pass.**

## 2. OBJECTIVE

**A person, in a real browser, completes the whole MFA login and reaches the dashboard — and cannot
reach it without the code.**

## 3. ACCEPTANCE

| id | must observe |
|---|---|
| **DE3-1** | **THE POSITIVE PATH, END TO END IN A BROWSER:** password -> opt-in prompt -> confirm -> code arrives in a real mailbox -> typed -> **dashboard renders.** State the mailbox, the folder observed, and attach the screenshot you actually read. |
| **DE3-2** | **THE REFUSAL, IN THE SAME BROWSER:** with the correct password and **no** code, the dashboard is **not reachable** — by URL, by back-navigation, or by refresh. ⛔ This is the security property. A success-path-only exercise scores identically whether the gate exists or not. **Name the input that makes it refuse, and run it.** |
| **DE3-3** | The whole flow renders correctly against the **silver-canvas colour law** — screenshot READ, not asserted. |

⛔ **NO ROW HERE MAY BE SATISFIED BY AN API CALL.** If it can be, it is the wrong row and this TO has
failed at the thing it exists for.

## 4. ⛔ THE ACCOUNT PROBLEM — READ BEFORE PLANNING DE3-1

**Zero of 48 accounts have MFA enabled right now, deliberately.** Andrew was locked out of PROD tonight
by this exact flow and the revert is what cleared it.
- ⛔ **DO NOT ENABLE MFA ON ANY ACCOUNT TO CREATE YOUR TEST SUBJECT.** That is `2.0.0_SA_COO~Z`'s to
  arrange on Andrew's word.
- ⛔ **DO NOT CREATE A TEST ACCOUNT ON A LIVE HUMAN EMAIL ADDRESS.** One did exactly that tonight,
  mailed Andrew two production-shaped messages, and cost a false bug report plus ~40 minutes of three
  seats. The only tell was a greeting.
- **When you reach this cell, STOP AND ASK `2.0.0_SA_COO~Z` for a test subject.** Requesting one is one
  message; provisioning one yourself is how tonight's incident happened.

## 5. WHAT THIS TO DOES NOT DO

It does not re-enable Andrew's account (his word, via `2.0.0_SA_COO~Z`); it does not start the pilot
cohort (unnamed, and it cannot begin before this flow exists); it does not promote to PROD (a DT act);
and it does not touch IAM — **FINDING F-1 stays open with its own owner.**

## 6. REPORTING

Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`. Push state MEASURED. Surprise items to
`0.0.0_AB_MSTR~Z`.
⭐ **And if a criterion here cannot be satisfied honestly, say so in those words.** Tonight
`UNVERIFIABLE-BY-INSTRUMENT` on a folder observation was upgraded to PASS by a different observer
hours later — **a bounded refusal survived contact with the truth, and a guess would not have.**
