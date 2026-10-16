# NEVER-WIDEN, COO HALF -- the Cottonwood reporting-publish function: publisher 0.4.0 and the full republish of the 939 Cottonwood series (IRPT_DASHBD round 149)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-16 ~22:5xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_HOP2_HISTORY_SCOPE_REPUBLISH.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_HOP2_HISTORY_SCOPE_REPUBLISH.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_HOP2_HISTORY_SCOPE_REPUBLISH.md`), sha256 `584a774339a15acac39defbab5919cb9a8400eeef98dd63aa10be46aeb0c9c36` (computed by this seat on the file; 11001 bytes; blob `008efedd5f08e7861d77ae3ea60b0d51d4782378`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2.

## 1. What this half covers

Six acts, in order: the bundle build and upload as a NEW VERSION of the artifact key (base64 sha256 `vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE=` or STOP); ONE `safe-apply` of `reporting-publish-iso` with the plan exactly 0 add / 1 change / 0 destroy (the function's code); the PRE-WRITE read with its STOP lines and ONE dry run; a ONE-account canary that shows the flip; the FULL republish of the 939 series at the same keys; the receipt. **Served output moves**, and this half signs the three client-facing movements by their counts: 102 series lose the sentence "Returns from <date>.", 657 series show a restated daily return on past days, 826 series end a day later; no series changes `value`.

## 2. What this seat measured and ran, and what it did not

- **Read-only, by this seat:** the live function (`CodeSha256` `GagDGBNG...`, 1,024 MB, 900 s, no environment), the disabled schedule, the artifact versions, the 939 published series (all PARTIAL_HISTORY, publisher 0.3.0).
- **Run by this seat:** the new publisher in-process over the rewritten gold for all 939 accounts, compared with the published series (`reads/RD_COT_PUBLISH_OFFLINE_DIFF_20261016.json`, tool `reads/cot_publish_offline_diff.py`): 102 PARTIAL to FULL, 0 FULL to PARTIAL, 826 gain a day, 657 changed daily returns on common days, `value`, `income`, `holdings_price_return` unchanged, 0 refused.
- **NOT done by anyone:** a `terraform plan` of this root with the new bundle; the function's own run of the new code over the real gold; the series contract's validation of the new series by the function (the dry run is the first).

## 3. Writers, blast radius, limits

Writers of the changed properties: the code has ONE writer (the Terraform root); the objects have ONE rule (`publisher.py`) and ZERO enabled schedules (the daily schedule is DISABLED), so only Acts 4 and 5 write (the packet's section 5). Blast radius: 1,878 keys at the same addresses, prior versions kept, rollback per key in the packet's section 7. **Client-facing sentences this pair can move: 102 (the Returns-from sentence), counted before the write.** Not covered: the schedule's enabling, any environment variable, any delete, any act inside 12:05-12:45 UTC on a weekday.

## 4. Both branches, rollback

As the packet's sections 6 and 7: a plan line outside the gate, a different build hash, a FULL to PARTIAL flip, flips above 150, a changed `value`/`income`/`holdings_price_return` on a common day, more than 800 series with a changed daily return, or a refusal above 10 percent STOPS before any write; the rollback is the prior artifact version `4wX9zhqX6x4x73i1vX1ADsXfv1LyDzRA` through `safe-apply` and the prior version of each key.

## 5. Conditions of this half

Ledger first, bound to the packet's sha256; live state re-read at each act; no act between 12:05 and 12:45 UTC on a weekday; stop at once on a timeout, an AccessDenied, a Max Memory Used above 819 MB or a count outside the STOP lines; counts and words only, never an account id.
