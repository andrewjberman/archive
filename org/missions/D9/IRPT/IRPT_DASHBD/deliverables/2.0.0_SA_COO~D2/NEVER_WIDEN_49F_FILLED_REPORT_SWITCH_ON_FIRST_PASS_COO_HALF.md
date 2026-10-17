# NEVER-WIDEN, COO HALF -- the 49 Financial filled-report SWITCH-ON and the FIRST PASS (IRPT_DASHBD round 150, IB-pr-551 hop 2)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED. **Date:** 2026-10-17 ~06:1xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md`), sha256 `3248f3c488fff06b00a165ee5a98da0bd0f509a013d23238dd8590af04290573` (computed by this seat on the file; 14,420 bytes; blob `e3f84e06cc5e`). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2. **Named V leg:** 2.0.0_SA_COO~S2 (CTO msgs 10294, 10295, 10306, 10307).

## 1. What this half covers

Nine acts, in order: the bundle build to the base64 sha256 `4SF81dqnVu8rqP3xT0dWtQ8br1w9hvjQft/0knAtaic=` (17 members) or STOP; ONE code-only `safe-apply` of `reporting-publish` (plan exactly 0 add / 1 change / 0 destroy) and the OFF no-op probe; ONE `safe-apply` adding the one environment variable `FILLED_REPORT_PASS` (plan exactly 0 / 1 / 0, environment only); a dry run in seven shards writing nothing; ONE canary client written and graded; the mint leg (two synthetic principals, removed and read ABSENT twice) and `~S2`'s V leg on the canary only; the full pass in seven shards; the after-read and receipt. **The only objects written are the new `client=<id>/filled_report.json` keys; no series, summary, route, grant or schedule changes.**

## 2. What this seat measured and ran, and what it did not

- **Read-only, by this seat:** the live function (code hash, 1,024 MB, 300 s, no environment), the role's eight statements (it already holds PutObject on the platinum reporting prefix and GetObject on the filled gold prefix: no IAM change), the artifact versions and the rollback version, the three schedules; the build-only hash at `44faca6460`.
- **Run by this seat:** `p192` AC1..3 on the landed trunk (PASS) and its selftest (green on the reference, red on 10 single-fault mutants); the 188 reporting-publish tests pass.
- **NOT done by anyone:** the reader against the real gold partition inside the function; any event with the switch ON; the mint of the viewer pair; the page.

## 3. Writers, blast radius, limits

Writers of the changed properties: the Terraform root through `safe-apply` (code and the one variable, N = 1) and the pass (the objects, N = 1; no schedule sends the event, recorded in Act 3). Blast radius: an artifact version, one environment variable, one new object per directory client, two users rows written and removed. **A client-facing sentence this pair can move: each client's filled report becomes readable through the live route by a viewer whose scope covers the client; no page in the portal branch read by this seat calls the route.** Not covered: any other variable, any IAM or schedule change, any delete of a written document, the Cottonwood filled report, any portal promotion.

## 4. Both branches, rollback

As the packet's sections 5 and 6: a plan line outside a gate, a different build hash, an Act 2 probe other than the exact OFF no-op, an event outside its stop lines, a failed canary validation or a LEAK graded by `~S2` STOPS the pair before the next act. Rollback: revert the one environment line (the pass reads OFF) and point the entry back to artifact version `oXM0wQg8revg3asMHOhpbz1gPDnXaatK`, both through `safe-apply`; written documents stay (a delete needs a human).

## 5. Conditions of this half

Ledger first, bound to the packet's sha256; live state re-read at the moment of each act; no act in a weekday fire window; stop at once on a timeout, an AccessDenied, a Max Memory Used above 819 MB, a duration above 240 s or an unexpected response; counts and words only, never a client id, a name, a password, a token or a body in any file, row, log or message; the canary id travels by broker to `~S2` only.
