# ALERT DELIVERY — the alarm-to-topic-to-CONFIRMED-subscriber read (cell RP-s-6, outcome FWD-5)

Authority: `NFRA_REPORT_PRD.md` manifest row S6 (`FWD-5`), `C-ALARM-ANCHORED`, and ruling 12 via
`STATE_MODEL.md` (cell RP-s-1). **This is a READ.** The standing alerting/monitor moratorium is ARMED
(one of 12 NEVER clauses, `comp-schedule` C3); this cell mints no alarm, no topic, no subscription and
no notification. Every command run to build it is a read: `describe-alarms`,
`list-subscriptions-by-topic`, `get-subscription-attributes`, `get-sms-sandbox-account-status`,
`list-sms-sandbox-phone-numbers`. None creates, subscribes or arms anything.

## 0. The anchor (`C-ALARM-ANCHORED`)

The check is anchored on the **ALARM** and reads **CONFIRMED** delivery — never "subscribed" alone,
and never the alarm's own configuration (`ActionsEnabled: true` proves the alarm CAN evaluate; it
proves nothing about whether the resulting SNS publish reaches any human). A pending subscription
delivers nothing. **An alarm whose delivery leg cannot fire renders `INERT` on Axis 1 — ruling 12's own
worked example is exactly `opal-login-abuse-alerts`: `INERT`, never `RED`.**

## 1. THE MEASURED STARTING STATE, RE-VERIFIED AT THIS SEAT'S OWN VINTAGE

The cell's own measured/live claim — sourced from `1.0.0_SA_CTO~Z`'s row
`NFRA_OPSEC202609-Z-S151` (`org/missions/D12/NFRA/NFRA_OPSEC202609/surprise-channel/investigations/
INVESTIGATION_v1.md@f3731b9705`, measured 2026-09-09 ~15:45Z) — was **re-run independently at this
seat, 2026-09-09 ~21:01Z**, same account (`313476888478`), same instrument (`aws cloudwatch
describe-alarms` then `aws sns list-subscriptions-by-topic` per topic). This is a FRESHNESS
re-confirmation with the same instrument, not a different-instrument corroboration, and it is named as
such rather than overstated.

**RESULT: IDENTICAL.** 51 alarms, 7 distinct SNS topics. **3 of 7 have ZERO confirmed subscriptions**
(the list call returns `[]` — not a single pending entry, not a single confirmed one):

| SNS topic | Alarms backed (count) | Confirmed subscriptions |
|---|---|---|
| `opal-login-abuse-alerts` | 2 (`OPSEC-auth-login-rate-limit-blocked`, `OPSEC-auth-throttled`) | **0** |
| `astn-wsjft-alerts` | 1 (`astn-wsjft-orchestrator-errors`) | **0** |
| `etfs-reports-alerts` | 1 (`etfs-reports-orchestrator-errors`) | **0** |
| `inf-otp-alert` | 4 | 2 (`lambda`, `sms`) |
| `opal-critical-surface-alerts` | 7 | 2 (`sqs`, `sms`) |
| `opal-infrastructure-alerts` | 24 | 1 (`sms`) |
| `opal-partner-etl-ops-alerts` | 1 | 2 (`sqs`, `sms`) |

None of the "0" rows carries a `PendingConfirmation` placeholder either — the AWS API renders a
pending entry with `SubscriptionArn: "PendingConfirmation"` and a real ARN once confirmed; an empty
list means no subscription of ANY kind exists, confirmed or pending.

## 2. THE THREE ZERO-CONFIRMED-SUBSCRIBER TARGETS (satisfies AC1) — render `INERT`

**`opal-login-abuse-alerts`, `astn-wsjft-alerts`, `etfs-reports-alerts`** each render **Axis 1 =
`INERT`** (ratified, unedited, from `STATE_MODEL.md` §1 — "a control exists but CANNOT FIRE (names no
live role; pages no subscriber)"), with **no Axis 2 value** (not meaningful off `CHECKED`). This is
ruling 12's own worked example rendered, not invented: `opal-login-abuse-alerts` is `INERT`, **never
`RED`** — the alarm exists, evaluates, and is enabled; the thing that cannot fire is the delivery leg
past the topic, and that is exactly what `INERT` names. **None of the three is counted as
protection.**

## 3. THE POSITIVE CONTROL — WHAT IT PROVES, AND WHAT IT DOES NOT

Because 4 of 7 topics return non-zero confirmed subscriptions through the **identical call**, the
three zeros above are a **real absence**, not a broken probe (the same logic `NFRA_OPSEC202609-Z-S151`
used, re-run and confirmed here). **This is a control on the INSTRUMENT — it proves the check CAN
return non-zero — and it is not, by itself, a claim that all four "confirmed" topics deliver to a
human.** §4 goes one hop further than "confirmed subscription" to test that claim directly, because
that is exactly what this cell's ACT asks for: "make it readable whether a message would actually
ARRIVE AT A HUMAN BEING... one that would reach nobody is shown as reaching nobody and is NEVER
counted as protection."

## 4. GOING PAST "CONFIRMED SUBSCRIPTION" — THE SMS SANDBOX (new evidence, this seat, same session)

`NFRA_OPSEC202609-Z-S151` flagged, and explicitly did NOT resolve, one open question: *"`opal-
infrastructure-alerts` shows ONE CONFIRMED SMS subscriber, and CONFIRMED IS NOT DELIVERING: SMS
sandbox status is a separate property this seat did not read, so that target is NOT reported here as
healthy."* This cell's own ACT is precisely "would a message actually ARRIVE AT A HUMAN BEING," so
that open question sits directly on this cell's anchor, and it was cheap to resolve with two more read
calls:

- `aws sns get-sms-sandbox-account-status` → **`IsInSandbox: true`.** The account is in the SNS SMS
  sandbox, where SMS can be delivered ONLY to a destination number that has completed sandbox
  verification.
- `aws sns list-sms-sandbox-phone-numbers` → **exactly one number is registered, and its status is
  `Pending`, not `Verified`: `+17862617679`.**
- Every SMS-protocol subscription across all four "confirmed" topics was read back to its destination
  number (`get-subscription-attributes` → `Attributes.Endpoint`):

| Topic | SMS subscriber endpoint | Sandbox status | Can this leg currently deliver? |
|---|---|---|---|
| `opal-infrastructure-alerts` | `+17862617679` | `Pending` (registered, not verified) | **NO** |
| `opal-critical-surface-alerts` | `+17862617679` | `Pending` (registered, not verified) | **NO** |
| `opal-partner-etl-ops-alerts` | `+17862617679` | `Pending` (registered, not verified) | **NO** |
| `inf-otp-alert` | `+13052010419` | not present in the sandbox list at all | **NO** (an unregistered number cannot receive SMS in sandbox mode at all) |

**Every SMS-protocol subscription in the estate is currently non-functional.** This resolves
`NFRA_OPSEC202609-Z-S151`'s open question rather than merely restating it: `opal-infrastructure-alerts`
is not "unreported as healthy," it is **measurably reaching nobody right now**.

### Per-row consequence, rendered through `STATE_MODEL.md`'s ratified vocabulary only

- **`opal-infrastructure-alerts`** — its confirmed subscription IS the dead SMS leg above, and it has
  **no other subscriber**. This topic reaches nobody, the same practical outcome as the three zero-
  subscriber topics in §2, despite showing "1 confirmed subscription." Rendered **`CHECKED` / `BREACH`**
  — `CHECKED` because the look was carried all the way to the sandbox-verification layer and is
  trustworthy; `BREACH` ("outside standard, NOT contained," ruling 12's own words) because what was
  found is a total, uncontained delivery failure on this topic's only leg. **Not** rendered `INERT`:
  a subscriber does exist and is confirmed at the SNS layer — it is the destination protocol's own
  verification gate that cannot fire, a different mechanism from "pages no subscriber," and ruling 12's
  ratified values are not edited or stretched here to blur that distinction.
- **`inf-otp-alert`, `opal-critical-surface-alerts`, `opal-partner-etl-ops-alerts`** — each ALSO
  carries a non-SMS leg (`lambda`, `sqs`, `sqs` respectively) that this cell's anchor (alarm → topic →
  CONFIRMED SNS subscriber) is satisfied by independently of the dead SMS leg. **Whether that Lambda
  or SQS consumer, once invoked, in turn notifies a human is NOT traced here** — see the declared limit
  below. These three render `CHECKED`, Axis 2 left **UNASSERTED IN THIS DOCUMENT** rather than defaulted
  to `OK`: this cell measured that their SNS-layer subscription is real and confirmed, and explicitly
  did NOT measure what happens after the Lambda invocation or the SQS receive. Declaring `OK` here
  would be exactly the defect `C-AI` and ruling 12 exist to prevent — a found-and-verified fact
  standing in for one that was never checked.

## 5. Declared limits, named rather than hidden

- **Does not trace a Lambda or SQS subscriber's own downstream notification behavior.**
  `C-ALARM-ANCHORED` anchors this read on alarm → topic → CONFIRMED SNS subscriber; reading a Lambda's
  source/logs or an SQS queue's consumer to determine whether IT notifies a human is a materially
  larger investigation outside this cell's stated ACT and evidence bar, and is not attempted.
- **Mints nothing.** Every command run this session was a read. No topic was created, no endpoint was
  subscribed, no alarm was put. The standing moratorium (`comp-schedule` C3) is intact.
- **Does not re-grade any `TO-OP-S-*` face's own acceptance criteria** (mirrors the boundary
  `NFRA_OPSEC202609-Z-S151` itself drew) — this is a report-lane READ, not an OPSEC adjudication, and
  it says nothing about whether e.g. `TO-OP-S-6` was built correctly to its own criteria.
- **Does not reclassify or lower the "3 of 7 zero confirmed subscribers" count** — that count is
  unchanged by §4; §4 adds that at least one of the remaining four ("`opal-infrastructure-alerts`")
  reaches nobody for a DIFFERENT reason (a confirmed-but-unverified SMS endpoint) and that the
  human-reach of the other three is genuinely unmeasured past their SNS subscription, not that it is
  known-good.

## 6. What this does to "positive-controlled by the 4 that do"

The positive-control LOGIC in §3 stands exactly as measured: the probe can and does return non-zero,
so the three zeros are real. What this document adds, past what the cell's inlined text alone would
have supported, is that **"the 4 that do" is not a synonym for "the 4 that work."** One of the four
(`opal-infrastructure-alerts`) reaches nobody today for a reason this cell's own anchor is chartered to
find (a confirmed subscription whose protocol cannot currently fire), and the other three's human-reach
runs through a leg (`lambda`/`sqs`) this cell does not trace. **Of the seven alarm-backed SNS targets
read here, exactly ZERO are affirmatively shown, end to end, to reach a human today** — three by zero
subscribers, one by a dead SMS endpoint, three by an untraced downstream hop. Stating that plainly is
what "one that would reach nobody is shown as reaching nobody, and is never counted as protection"
(cell text, verbatim) requires.
