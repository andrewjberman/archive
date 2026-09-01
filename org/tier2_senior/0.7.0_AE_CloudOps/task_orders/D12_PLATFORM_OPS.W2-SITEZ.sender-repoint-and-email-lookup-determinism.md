# TO D12_PLATFORM_OPS.W2-SITEZ — auth sender repoint + email-lookup determinism

<task_order id="D12_PLATFORM_OPS.W2-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T01:0xZ</issued>
<status>CLOSED - COMPLETE. D12 send-fix accepted (1.0.0_SA_CTO~Z) + certified (3.0.0_SA_CVO~Z), verified on prod v2.1.174, commits ON ORIGIN. Face closed by issuer 2.0.0_SA_COO~Z 2026-09-01 to free the lane for D12_PHONE_OTP_ALL_AWS (Rule 27).</status>
<priority>P1 — cell 2 is a live auth-path defect; cell 1 is Andrew-authorized and small.</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~00:5xZ, VERBATIM AND ENTIRE: "All of these functions should be noreply,
there is nobody responding to these so noreply is the coreect point. on call 2, i want to test it with
a few people first, including myself. I want to try logging in and seeing that MFA actually works."
⭐ HIS BASIS FOR THE REPOINT IS SEMANTIC, NOT REMEDIAL — "there is nobody responding to these". He gave
it on CORRECTED information, after being told the mailer was broken and then having that claim
falsified. The earlier hold (COO 17251) is DISCHARGED.
Cell 2 is 1.0.0_SA_CTO~Z's lane ruling from tonight's trace (msg 17261), decided not asked.
</authority>
<proof_of_spec>
  <expected_criteria>W2-1,W2-2,W2-3,W2-4,W2-5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D12_PLATFORM_OPS.W2_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 1. CELLS

| Cell | Deliverable |
|---|---|
| **W2-a** | Repoint the auth sender from `support@opalinvest.dev` to `noreply@opalinvest.dev`. `1.0.0_SA_CTO~Z` located `FROM_EMAIL` at `auth-handler/src/email.ts:5`, used by lines 42 and 130; line 234 already uses `AUTH_FROM_EMAIL` and does not change. ⛔ **He said ALL of these functions — do NOT scope to the two already named. Census the auth path for any other sender and report the denominator.** |
| **W2-b** | `getUserPKByEmail` (`db.ts:66-84`) does `Limit: 1` on a GSI with **no uniqueness constraint**. Two records sharing an email resolve **NONDETERMINISTICALLY**, and every auth path routes through it. **Surface the ambiguity; do not silently pick.** A second match is a data-integrity event, not a tie to break. |

## 2. ⛔ THE CONSTRAINT THAT MATTERS MOST ON W2-a

**RECORD, IN THE COMMIT ITSELF, THAT THIS REPOINT FIXES NOTHING SECURITY-WISE.**

The role's `opalinvest-auth-permissions` condition (`ses:FromAddress = noreply@opalinvest.dev`) is
**defeated by a second, unconditioned `ses-send-email` Allow on the same role.** IAM is a union of
Allows with no Deny, so the condition restricts nothing.
> **If the commit message implies the sender restriction now holds, it manufactures exactly the false
> confidence this whole thread nearly shipped.** The repoint is a SEMANTIC correction Andrew asked for.
> It is not a remediation, and it must not be recorded as closing the IAM finding.

⛔ **DO NOT WIDEN OR NARROW ANY IAM POLICY.** The two-Allow structure is `1.0.0_SA_CTO~Z`'s finding
with its own owner and gate. Nothing is failing today.

## 3. ACCEPTANCE — proof-of-spec criteria

| id | must observe |
|---|---|
| **W2-1** | Every auth-path sender now reads `noreply@`. **Print the denominator** — how many sender constants/usages exist in the auth path, and that all of them were checked. A census of two when he said "all" is not this criterion. |
| **W2-2** | ⚠ **AMENDED 2026-09-01 ~02:0xZ — SEE §3b. AS ORIGINALLY WRITTEN THIS CRITERION WAS UNSATISFIABLE WITHOUT BREAKING §4's OWN STANDING RULES.** Now: **DEFERRED to the first NATURAL send of a changed mailer** (password-reset or welcome) — observe its `From` then. Deployed-byte currency stated (running `CodeSha256` == the sha the build emitted) is required NOW and is independent. |
| **W2-3** | `getUserPKByEmail` with **two records sharing one email** returns a surfaced ambiguity rather than an arbitrary pick. **Construct the collision** — a fixture with two rows, not an argument that it could happen. Then show the single-match path still returns normally (positive control). |
| **W2-4** | **NEGATIVE — nothing alarm-shaped created, no IAM policy widened or narrowed.** Enumerate what changed; print the created/modified resource set. |
| **W2-5** | **NEGATIVE — no account beyond `andrew@opalinvest.com` had MFA enabled by this work.** Census `mfaEnabled` across all accounts with its denominator. |

⚠ **W2-4 and W2-5 are negative criteria: carry a POSITIVE CONTROL or they cannot tell a true absence
from a broken probe.**

## 3b. ⛔ W2-2 AS I FIRST WROTE IT CONTRADICTED §4 — MY DEFECT, RECORDED AND FIXED

`0.7.0_AE_CloudOps~Z` hit this and **recorded the conflict rather than resolving it by quietly breaking
one of my rules.** That was the right act and the contradiction is mine:

- W2-2 demanded *"a real auth email is sent after the change and its **From** observed."*
- The only senders this work CHANGED are **password-reset** and **welcome** (the OTP mailer already
  used `noreply@`). Firing either means unsolicited auth mail to a real mailbox, **or** a test account
  on a live human address — which **§4 rule 1 of this same TO forbids**, and §4 rule 2 forbids aiming an
  outbound-side-effect route at a live sender. A `.invalid` recipient sends but cannot be READ, so it
  cannot satisfy *"observed"*.
> **I wrote an acceptance criterion whose only satisfying act my own standing rules prohibit.** A spec
> that cannot be satisfied without violating itself is a spec defect, not an executor problem.

### THE DISPOSITION — DEFERRED, NOT WAIVED, AND NOT N/A

⛔ **I AM NOT RULING IT N/A ON THE RUNNING-BYTES CENSUS**, which was offered and is tempting. That
census shows the deployed code contains only `noreply@` and zero `support@` — real evidence, and
**exactly one rung below what the criterion names.** Substituting the code rung for the observation
rung is the precise error that let W1 pass 10/10 on a feature no human could use, and I am not
committing it twice in one night to close a row faster.
✅ **DEFERRED to the first NATURAL send of a changed mailer.** No unsolicited mail, no rule broken, and
the observation happens for real when it happens. **The likeliest trigger is the WS-4 admin UI creating
its first account (welcome mailer), or any genuine password reset.** Whoever observes it closes W2-2 by
reporting the `From` header.
**Not blocking:** W2's other four rows stand on their own, and nothing downstream waits on W2-2.

## 4. THREE STANDING PRACTICE RULES — from tonight's trace, binding on this TO and after

1. ⛔ **NO TEST ACCOUNT MAY USE A LIVE HUMAN EMAIL ADDRESS.** Tonight a test account carrying Andrew's
   address sent him two real emails indistinguishable from production; he reasonably concluded a
   feature was broken. **The only tell was a greeting.** Cost: a false bug report from the principal
   and ~40 minutes of three seats' time.
2. ⛔ **AN ENDPOINT SWEEP MUST NOT FIRE `/auth/forgot-password` (or any outbound-side-effect route)
   AGAINST A LIVE SENDER.** W1-6 swept 14 routes in one second to prove no secret leaks — correct test,
   real side effect: it sent mail. Use a non-sending target or an explicit stub.
   ⭐ **NEITHER OF THESE IS A CRITICISM OF W1.** W1-6 found exactly what it was built to find; the side
   effect is a design gap in how we probe, not a lapse.
3. ⛔ **DO NOT ENABLE MFA ON ANY ACCOUNT.** See §5.

## 5. ⛔ THE PILOT IS NOT YOURS, AND THE COHORT IS NOT NAMED

Andrew ruled a **NAMED PILOT**, rejecting both a full rollout and a wait-for-WS-3: *"i want to test it
with a few people first, including myself."*
**He has not named the few. DO NOT ENABLE MFA ON ANY ACCOUNT BEYOND HIS OWN** until he does — and that
naming comes to this seat, not to the lane. His account is already enabled and is the pilot's first
member.

⚠ **AND HIS LOGIN IS THE FIRST REAL EXERCISE, NOT A RE-CONFIRMATION OF W1-3.** Measured by
`1.0.0_SA_CTO~Z`: exactly ONE account has ever produced an `mfa_challenge_issued` event, and it was the
now-deleted **test** account — W1-3's end-to-end ran on that account, not on his. **Read the result of
his login as a first exercise on a real account.** If it fails, that is new information and not a
regression of W1.

## 6. NOT IN SCOPE

Anything in WS-3 (remembered device), WS-4, WS-5, WS-6. The IAM two-Allow finding. DMARC report
collection (ruled out in W1 and unchanged). D7 in any form — it is PARKED behind D12.
⛔ **Section 9 of the W1 TO still binds: ten base-addressed TOs across five projects are NOT yours.**

## 7. REPORTING

Report to `2.0.0_SA_COO~Z` (validation) and `1.0.0_SA_CTO~Z` (acceptance). State push state as a
MEASURED value. Surprise items to `0.0.0_AB_MSTR~Z` — there is still no CVO reader on this device.
⭐ **And keep doing the thing that made W1 recoverable: bound your own findings.** `APPLIED, NOT
EXERCISED` and `UNVERIFIABLE-BY-INSTRUMENT` were what let two corrections land cleanly instead of
contradicting a claimed pass.
