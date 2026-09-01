# TO D12_PLATFORM_OPS.DE2-SITEZ — the MFA challenge screen (the page he had nowhere to type into)

<task_order id="D12_PLATFORM_OPS.DE2-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>0.4.0_DE_ClientPlatform~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T01:4xZ</issued>
<status>ISSUED — GO rides this commit. Sequenced after DE1.</status>
<priority>P1 — this is the literal missing artifact: "i am not presented wit a page to sign in to input it."</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~01:2xZ, VERBATIM: "I got an OTP just now, but that flow doesnt make sense if
i am not presented wit a page to sign in to input it." Plus his TO-series instruction relayed in
`1.0.0_SA_CTO~Z` 17286. Decomp cell 2.7, AMENDMENT 3.
</authority>
<proof_of_spec>
  <expected_criteria>DE2-1,DE2-2,DE2-3,DE2-4,DE2-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D12_PLATFORM_OPS.DE2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 1. OBJECTIVE

After the user opts in (DE1) and a code is sent, the browser presents a screen to **enter** it, with
**resend** and honest **error states**.

## 2. THE BACKEND CONTRACT YOU ARE BUILDING AGAINST — measured, do not re-derive

- Correct password on an MFA-enabled account -> `{"mfaRequired": true, ...}`, **no access token, no
  refresh cookie.** The session does not exist until the code is redeemed.
- ⛔ **A CONSUMED CODE IS DELETED, NOT FLAGGED.** Replay returns 401 — exercised (W1-5). So a
  double-submit is a genuine failure, not a no-op: **do not auto-retry a submit.**
- A wrong code returns 401 (W1-4). The OTP secret is **never** returned by any endpoint — 14 endpoints
  probed, 0 leaking (W1-6). **Keep it that way: nothing about the code goes into client state, logs,
  URLs or analytics.**

## 3. ACCEPTANCE — ⛔ EVERY CRITERION IS OBSERVED IN A BROWSER

| id | must observe |
|---|---|
| **DE2-1** | A code delivered to a real mailbox is **typed into the screen and the user reaches the dashboard.** ⭐ **THIS IS THE CRITERION W1 LOST — it is a PERSON reaching a PAGE, not an endpoint returning 200.** |
| **DE2-2** | A **wrong** code shows an error and the user stays out. |
| **DE2-3** | A **replayed** (already-consumed) code shows an error and the user stays out — not a spinner, not a silent retry. |
| **DE2-4** | **Resend** issues a new code and the previous one no longer works. |
| **DE2-5** | **NEGATIVE:** the code appears in no URL, no console log, no analytics payload and no persisted client state. Enumerate where you looked and carry a **positive control** proving the search would have found it. |

⛔ **AN API RESPONSE IS NOT ACCEPTANCE FOR ANY ROW.** Use `/frontend-dev`: render headlessly, **READ
THE SCREENSHOT**, check it against the silver-canvas colour law — light text or ghost-white buttons
outside a dark Panel is this portal's #1 recurring visual defect.

## 4. CONSTRAINTS

Same fences as DE1 and they are not boilerplate: **no alarm/monitor/notifier** (GLOBALALARM stands);
⛔ **do not enable MFA on any account, including for testing** — 0 of 48 are gated right now,
deliberately, because Andrew was locked out of PROD by this exact flow; **no test account on a live
human email address**; portal work is `DEV`, PROD promotion is a DT act and not in this TO.

## 5. SEQUENCING

**DE1 -> DE2 -> DE3.** DE2 can be BUILT alongside DE1, but its DE2-1 acceptance needs DE1's opt-in
path to reach it. DE3 exercises the whole flow end to end.

## 6. REPORTING

Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`. Push state MEASURED. Surprise items to
`0.0.0_AB_MSTR~Z`.


## ⛔ YOU ARE BARRED FROM FOUR BASE-ADDRESSED TASK ORDERS — MEASURED AT SEATING

**Your `~Z` lane is CLEAN: 0 open TOs besides this series** (computed, not eyeballed). But the **BARE
BASE** `0.4.0_DE_ClientPlatform` holds **FOUR**:

| status | task order |
|---|---|
| ACTIVE | `D3_MODELOVERLAY.TO-D3.4` |
| ACTIVE | `NFRA_MOTIF.P0.tsgraph-p2-2-cluster-materialize` (DE is a gated co-assignee) |
| ACTIVE | `NFRA_MOTIF.P1.absorb-detectors-c2-catalog` (DE is a gated co-assignee) |
| PENDING | `OPAL_ADVIPOINTERS.P4-REPOINT-49F` |

⛔ **A BARE-BASE TO BELONGS TO NO LANE, SO IT READS AS YOURS THE MOMENT YOU RUN A ROSTER QUERY ON YOUR
OWN SERIAL.** It is not addressed to you. **DO NOT ACT ON ANY OF THEM** — that would put two projects
on one instance, the Rule 27 violation this bar exists to prevent. **Your project is
`PLATFORM_OPS_USERMGMT` and nothing else.** If a roster query surfaces one, **REPORT it to
`2.0.0_SA_COO~Z` and keep working.**
⚠ **I measured that they are OPEN and BASE-ADDRESSED. I did NOT measure whether their work is
finished** — an `[ACTIVE]` face over completed work and a genuinely open TO render identically. Their
disposition belongs to their issuers, not to this lane.
⚠ **INSTRUMENT:** `to-check --assignee` SUBSTRING-matches and matches the ISSUER as well as the
assignee. **Read the ROWS, never the count.** (`--project` filters correctly — an earlier report that
it did not was withdrawn after three seats measured it with negative controls.)
