# TO D12_PLATFORM_OPS.DE1-SITEZ — the MFA opt-in prompt + channel selection (his most explicit ask)

<task_order id="D12_PLATFORM_OPS.DE1-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>0.4.0_DE_ClientPlatform~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T01:4xZ</issued>
<status>ISSUED — GO rides this commit. Serial confirmed by Andrew ~01:3xZ.</status>
<priority>P1 — first of the DE series; the login flow is unusable by a human without it.</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~01:2xZ, three messages VERBATIM: "COO needs to just write a TO series of
frontend ui tasks for 0.2.0_DE_ClientPlatform~Z" / "and then spawn them" / "obviously we need a
frontend flow that ties in with this."
And ~01:2xZ, the requirement itself, VERBATIM: "I got an OTP just now, but that flow doesnt make sense
if i am not presented wit a page to sign in to input it. Furthermore, OTP should be opt in, like you
have to say 'Yes' on some prompt that it will send you an email OTP or something, not just send
silently without a UI flow."
Rule 27 chain: PRD `docs/architecture/D12_PLATFORM_OPS_PRD.md` @2da36986f6 -> COO decomp
`laneZ_DECOMP_20260831_D12_PLATFORM_OPS_USERMGMT.md` AMENDMENT 3, cell 2.7.
</authority>
<proof_of_spec>
  <expected_criteria>DE1-1,DE1-2,DE1-3,DE1-4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D12_PLATFORM_OPS.DE1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 0. HOW THIS TO GOT ITS ADDRESS — RESOLVED, and worth one paragraph

Andrew first named **`0.2.0_DE_ClientPlatform~Z`**. **That serial does not exist**, measured with a
positive control: `comp-find` over 36,016 files returned **0 hits** for `0.2.0_DE_ClientPlatform` and
**1,036** for `0.4.0_DE_ClientPlatform`. Pod `0.2.0` is *PortfolioAnalytics*; *ClientPlatform* is pod
`0.4.0` — he combined a pod number with another pod's name.

⛔ **NO SEAT SUBSTITUTED IT. A SERIAL IS AN ADDRESS**, and silently correcting a sovereign's address is
how the wrong seat gets spawned and explained afterwards. The question went to him and he ruled
~01:3xZ, VERBATIM: *"sure we can do 0.4.0_DE thats fine."* `0.4.0_DE` resolves to exactly ONE seat
family in the tree (verified: it is the only `0.4.0_DE_*`), so the pod determines the name uniquely.
**`issued_to` is now `0.4.0_DE_ClientPlatform~Z` and this TO IS ISSUED.**

## 1. OBJECTIVE

After a correct password and **before any code is sent**, the user is asked whether to send one, and
chooses the channel. **No silent send.**

## 2. WHAT EXISTS AND WHAT DOES NOT — measured, do not re-derive

- **Backend is DONE and ACCEPTED.** A correct password returns `{"mfaRequired": true, ...}` with **no
  access token and no refresh cookie**; the code is redeemed at the verify endpoint. W1 closed 10/10.
- ⛔ **THE FRONTEND DOES NOT EXIST.** `mfaRequired` / `mfa/verify` / `mfaToken` in `portal/src` =
  **ZERO**, against a positive control of **10 auth files** including `LoginPage.tsx`. `1.0.0_SA_CTO~Z`
  measured it. **The browser currently has nowhere to type a code.**
- **`mfaChannel` accepts `email | sms | none`** and is stored per user (cell 1.1). ⛔ **`sms` IS NOT
  WIRED** — the send path fails closed 503 by design. Offer it only if you can disable it honestly;
  **do not present a channel that cannot deliver.**

## 3. ⭐ HIS "OPT-IN" IS THE HALF THE BACKEND SKIPPED, NOT A NEW FEATURE

His original memo: *"the client has an opportunity to select email or text for an OTP receipt."*
**We built the preference FIELD and never built the SELECTION MOMENT.** The server reads a stored
preference and fires. *"An opportunity to select"* was always a UI event at challenge time — that is
what this TO builds, and it is why his two memos agree rather than conflict.

## 4. ACCEPTANCE — ⛔ EVERY CRITERION IS OBSERVED IN A BROWSER

| id | must observe |
|---|---|
| **DE1-1** | After a correct password on an MFA-enabled account, the browser shows a **prompt asking whether to send a code** — and **NO code is sent until the user confirms.** Both halves: the prompt renders, AND no send occurs before the click. |
| **DE1-2** | The prompt offers the channel choice. If `sms` is presented at all it is **visibly unavailable**, not silently broken. |
| **DE1-3** | Declining / dismissing the prompt leaves the user **not logged in** and sends nothing. |
| **DE1-4** | **NEGATIVE:** no path in the new UI reveals whether an account exists or whether MFA is enabled on it, beyond what the pre-existing login already reveals. |

⛔ **AN API RESPONSE IS NOT ACCEPTANCE FOR ANY ROW ABOVE. THIS TO EXISTS BECAUSE THAT SUBSTITUTION
ALREADY HAPPENED ONCE** — see §6. Use the `/frontend-dev` loop: render headlessly, **READ THE
SCREENSHOT**, and check it against the silver-canvas colour law. A grep cannot see contrast and cannot
see a prompt.

## 5. CONSTRAINTS

- ⛔ **NO ALARM, MONITOR, SNS OR NOTIFIER.** The alarm hold was lifted for the D7 ticket reminder **by
  name** and nothing else. GLOBALALARM stands.
- ⛔ **DO NOT ENABLE MFA ON ANY ACCOUNT**, including for testing. **Zero of 48 accounts are gated right
  now** and that is deliberate — Andrew was locked out of PROD by exactly this flow and the revert is
  what cleared it. Re-enabling is his word, and it comes through `2.0.0_SA_COO~Z`.
- ⛔ **NO TEST ACCOUNT MAY USE A LIVE HUMAN EMAIL ADDRESS.** A test account carrying Andrew's own
  address sent him two production-shaped emails tonight; the only tell was a greeting, and it cost a
  false bug report from the principal plus ~40 minutes of three seats.
- Portal work is `DEV`; PROD promotion is a DT lane act and is **not** in this TO.

## 6. ⭐ READ THIS BEFORE WRITING THE ACCEPTANCE — IT IS WHY THIS TO EXISTS

W1 scored **10 of 10 honestly** and the feature was unusable by a human. The PRD said *"cannot reach
the **dashboard** without a live code"* — a **browser** outcome. My W1 TO wrote *"cannot reach the
dashboard — exercised end to end **against the deployed handler**, not a unit test"* — an **API**
outcome. I added that clause to **raise** rigor, and it relocated the test surface while keeping the
word *dashboard*.

> **A CLAUSE THAT NAMES THE INSTRUMENT CAN RELOCATE THE SUBJECT, AND IT READS AS TIGHTENING WHILE IT
> DOES.** When the outcome is user-visible, name the **OBSERVER**, never the instrument.

**That defect was mine, in the TO, not in anyone's build.** Do not repeat it here: if a criterion can
be satisfied without a browser, it is the wrong criterion.

## 7. REPORTING

Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`. State push state as a MEASURED value.
Surprise items to `0.0.0_AB_MSTR~Z`. **Bound your own findings** — `APPLIED, NOT EXERCISED` and
`UNVERIFIABLE-BY-INSTRUMENT` are what let two corrections land cleanly tonight instead of contradicting
a claimed pass.


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
