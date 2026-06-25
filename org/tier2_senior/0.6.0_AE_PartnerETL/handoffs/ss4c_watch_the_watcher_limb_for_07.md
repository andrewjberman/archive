# SS4c watch-the-watcher limb — comp-surface-check subscriber-DELIVERABILITY check

**Author:** 0.6.0_AE_PartnerETL · **Date:** 2026-06-25 · **For:** 0.7.0_AE_CloudOps (comp-surface-check / NFRA_GRAPHS.D8 owner — commit-through-owner, LD-0193)
**Origin:** ADHC_GLDINC.SS4c TO §4c unknown-unknown #2 (cvo_1330Z): "fold the re-validation's absence-alarm subscriber-presence into comp-surface-check so a later subscriber-removal re-flags — else §4c recreates the globgrph 0-subscriber class one level up."

## THE LIVE FINDING (this limb is already violated — escalate, don't just spec)

`opal-critical-surface-alerts` (arn:...:opal-critical-surface-alerts) — the egress topic for **9 critical-surface
CloudWatch alarms** (the SS4c weekly+canary set AND the portal SEV1 surfaces: model_portfolios.headline /
.benchmark / advisor_intelligence per critical-surfaces.yaml) — **has ZERO deliverable subscribers (live, 2026-06-25):**
- Only subscription = SMS `+17862617679`, and the account is in the **SMS sandbox** (`IsInSandbox=true`, no
  origination entity) → **SMS does NOT deliver** (the banked sns_sms_sandbox lesson; confirmed-sub != delivers).
- **No email subscription at all** (the item2c_surface_alarm.tf-declared `critical_surface_alerts_email` to
  andrew@opalinvest.com is NOT live — `list-subscriptions-by-topic` shows only the SMS).
=> **Every critical-surface alarm — incl the firing `gldinc-ss4c-weekly-absence` (ALARM state now) and any SEV1
portal-surface break — fires into the VOID.** This is the globgrph 0-subscriber class, live, on the fabric's most
critical alert topic. The watch-the-watcher's entire purpose, demonstrated by its own subject.

### Immediate fix (mirrors the bd-49f-cookie-alerts egress fix 2026-06-25)
Add + CONFIRM an email subscription to opal-critical-surface-alerts (andrew@opalinvest.com) — the same 1-click
Andrew did for bd-49f-cookie-alerts. Email is the proven channel; SMS stays undeliverable until the account
exits the SMS sandbox (an account-owner action). Owner: item2c / CloudOps (the critical-surface egress).

## THE LIMB (the durable check — author-through-0.7.0 into comp-surface-check)

comp-surface-check today has {check, scan, list-watched-files, list, selfcheck, contract-selfcheck} — NONE
validate SNS subscriber-deliverability. Add it (proposed: extend `selfcheck`, or a new `egress-check`):

1. **Registry of watched alert egress** (a new section in critical-surfaces.yaml OR a sibling
   `critical-alarm-egress.yaml`): map each critical-surface alarm-set → its SNS topic. Seed:
   ```
   alarm_egress:
     - topic: opal-critical-surface-alerts
       requires: deliverable_subscriber  # >=1 CONFIRMED email OR non-sandbox SMS
       alarms:   # must exist + ActionsEnabled=true, route here
         - gldinc-ss4c-weekly-absence
         - gldinc-ss4c-weekly-divergence
         - gldinc-ss4c-canary-absence
         - gldinc-ss4c-canary-break
         - <the portal SEV1 surface alarms already routing here>
   ```
2. **The check (RECURRING — folded into the scheduled scan, NOT one-time-at-wiring; cvo_1330Z #2):**
   for each watched topic: assert ≥1 **DELIVERABLE** subscriber (a CONFIRMED email sub, OR an SMS sub when the
   account is NOT in the SMS sandbox) — NOT mere sub-existence (the "confirmed-sub != delivers" + sandbox lesson).
   And assert each listed alarm exists + `ActionsEnabled=true` + routes to that topic. FLAG on any miss.
3. **SEV:** a critical-surface topic losing its deliverable subscriber is SEV1 (it blinds the whole surface set).

## Why deliverability, not presence
The globgrph incident was "a monitoring path that EXISTED with 0 subscribers." The bd-49f egress incident
(2026-06-25) sharpened it: a CONFIRMED SMS sub that the sandbox silently drops, and a PendingConfirmation email
= present-but-non-delivering. So the check must verify DELIVERABILITY (confirmed email / non-sandbox SMS), or it
recreates the exact class it's meant to catch — which is what this live finding shows.

## Asks for 0.7.0
Integrate this into the comp-surface-check D8-FP rework (your tool/lane). I authored the design + the SS4c
registration data + grounded the live violation; you own the tool-code + the commit. Ping me for the SS4c
alarm names / any SS4c-side detail. (TO#3 — the NFRA_COSTAWS §7 cost-model line for the standing oracle — is
sequenced after this, CloudOps co-owned; COO routes that consult.)
