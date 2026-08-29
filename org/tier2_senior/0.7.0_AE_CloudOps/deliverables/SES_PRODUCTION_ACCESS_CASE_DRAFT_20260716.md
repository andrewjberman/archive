# SES Production-Access Request -- CASE DRAFT (NOT SUBMITTED)

**Author:** 0.7.0_AE_CloudOps~A | **Date:** 2026-07-16 | **Status:** AT 1.0.0_SA_CTO's GATE. **DO NOT SUBMIT WITHOUT HIS WORD.**
**Authorization:** CTO 20260716T212657Z -- *"SES production-access = your lane motion, CASE TEXT AT MY GATE before submission (rule-23 history)"*.
**Account:** 313476888478 | **Region:** us-east-1

---

## >> READ THIS BEFORE THE DRAFT: WHAT I MEASURED vs WHAT OUR OWN RECORDS SAY <<

**A production-access review is exactly where AWS verifies sending identities.** The 2026-07-13 incident (a support case drafted claiming `opalcapital.com` as ours) came from asserting a fact nobody had measured. So every claim below is measured live this session, and **where our own record and the live state disagree, the live state wins and I say so.**

### FINDING -- CLAUDE.md Rule 23 says `opalinvest.dev` is "DKIM-signing + DMARC-aligned." MEASURED, THAT IS HALF TRUE, AND THE OTHER HALF WOULD HAVE BEEN A FALSE CLAIM TO AWS.

| Claim | Measured | Verdict |
|---|---|---|
| DKIM signing on `opalinvest.dev` | `DkimEnabled: true`, `DkimVerificationStatus: Success`, 3 tokens | **TRUE** |
| "DMARC-aligned" | `_dmarc.opalinvest.dev` -> **NXDOMAIN** (8.8.8.8). **No DMARC policy record exists.** | **AMBIGUOUS -> DO NOT WRITE IT** |
| SPF on `opalinvest.dev` | **No SPF TXT record** | **ABSENT** |

**The distinction that matters:** DMARC *alignment* (our `From: noreply@opalinvest.dev` matches the DKIM `d=opalinvest.dev`) **does** hold -- that relationship is real. But a **published DMARC policy** does not exist. Rule 23's phrase collapses the two, and an agent reading it would write *"DMARC-aligned"* into a case where a reviewer checks for a `_dmarc` record and finds nothing. **Same shape as the rule-23 incident: a record stating a conclusion without its mechanism, read outward as a fact.** The draft below therefore claims DKIM only.

**This is NOT a blocker for production access** (AWS requires DKIM + a coherent bounce/complaint story, not a DMARC policy). It IS a precision defect in CLAUDE.md worth CTO's ruling -- and separately, publishing a DMARC policy on `opalinvest.dev` is cheap and would make the claim true. **Note it touches `opalinvest.dev` DNS only -- NOT `opalinvest.com`, whose SPF/DKIM/DMARC carry live M365 company mail and are out of scope by law (a second SPF record on that domain is an RFC-7208 `permerror` = firm-wide mail damage).**

### The honest posture gap (stated, not papered)

- **Account-level suppression list: ENABLED for `BOUNCE` and `COMPLAINT`** -- a real, measured control.
- **Bounce/complaint forwarding: ENABLED** on `opalinvest.dev` and `noreply@opalinvest.dev` (`ForwardingEnabled: true`) -- real, but it is *email forwarding*, not programmatic handling.
- **The website sender uses NO configuration set** (measured: 0 occurrences in `ses-sendmail.sh`; the one config set that exists, `trade-pipeline-notifications`, belongs to a different system). **So there is no SNS/event-destination pipeline for website bounces today.**
- I am **not** claiming a handling pipeline we do not have. An AWS reviewer finding an unclaimed gap is survivable; finding a **claimed control that does not exist** is the rule-23 class again.

### Measured account state (as of 2026-07-16 ~21:2xZ)

```
ProductionAccess : false          SendingEnabled : true      EnforcementStatus : HEALTHY
Max24HourSend    : 200.0          MaxSendRate    : 1.0/s     SentLast24Hours   : 7
Send stats (last 6 data points): 9 delivery attempts, 0 bounces, 0 complaints, 0 rejects
```

---

## DRAFT CASE TEXT (this is what would be pasted into the AWS console)

> **Subject:** Request production access -- transactional email for corporate website contact form (us-east-1)
>
> **Mail type:** Transactional
> **Website URL:** https://opalinvest.com
> **Sending identity:** `noreply@opalinvest.dev` (domain `opalinvest.dev`, DKIM-verified in this account)
>
> **How we will use Amazon SES**
>
> We are Opal Capital, an investment platform for independent financial advisors. We use SES for a single, narrow, transactional purpose: our corporate WordPress website (https://opalinvest.com, hosted on EC2 in this account) sends a notification email to our own staff when a visitor submits the site's contact form. That is the entire use case today. There is no marketing email, no newsletter, no bulk or campaign sending, and no mailing lists. We do not buy, rent, scrape, or otherwise acquire address lists.
>
> Recipients today are Opal employees at our own corporate domain. We are requesting production access for two reasons: (1) the sandbox restricts delivery to pre-verified recipient addresses, which is a fragile constraint for a live public website -- a routine change such as sending a confirmation to the person who submitted the form would silently fail; and (2) we want a delivery path whose failure mode is a visible bounce rather than a rejection, so a prospective client's inquiry is never lost without a trace.
>
> Our expected volume is very low. Over the last 24 hours this account sent 7 messages. We anticipate on the order of tens of messages per day at steady state, driven entirely by inbound contact-form submissions on a low-traffic corporate site.
>
> **How we manage bounces and complaints**
>
> - The account-level suppression list is enabled for both BOUNCE and COMPLAINT, so SES automatically suppresses addresses that hard-bounce or generate a complaint.
> - Bounce and complaint notifications are enabled on the sending identity and are delivered to a monitored mailbox.
> - Sending is DKIM-authenticated: the `opalinvest.dev` domain is DKIM-verified in this account and all messages are signed, with the From address on the same domain as the signing domain.
> - Our sender is a no-reply transactional address used only by the website; it is not used for correspondence or outbound outreach.
> - We currently have zero bounces and zero complaints on this account.
> - Because every message is triggered by a visitor's own submission of our contact form, we do not send unsolicited mail; there is no recipient list to manage, and consequently no unsubscribe surface. If we later add any message type that is sent to an address we did not receive directly from that person's own form submission, we will add an unsubscribe mechanism and a dedicated configuration set with SNS event destinations for programmatic bounce and complaint processing before doing so.
>
> **How recipients receive our mail**
>
> Every message is a direct, immediate response to an action the recipient's counterpart took on our website: a visitor fills in our contact form, and our staff receive a notification containing what that visitor wrote. No recipient is ever contacted without such a trigger.

---

## PRE-SUBMISSION CHECKS (for the CTO gate)

- [x] **`opalcapital.com` appears NOWHERE** -- verified by reading the draft; it is not ours (Andrew-direct 07-13) and the 07-13 draft that named it was corrected unsubmitted.
- [x] **No claim of a DMARC policy** (measured NXDOMAIN). DKIM claimed, and DKIM is measured true.
- [x] **No claim of an SNS/event-destination bounce pipeline** -- we do not have one for this sender; the draft states the suppression list + notification forwarding we DO have, and commits to the pipeline only as a precondition of a future change.
- [x] **No claim about `opalinvest.com` mail records** -- out of scope; they carry live M365 mail.
- [x] Volume figures are measured (`SentLast24Hours: 7`), not estimated upward.
- [x] "Zero bounces / zero complaints" is measured (`get-send-statistics`, 0/0/0 across all data points).
- [ ] **CTO word to submit** -- OPEN.

## OPEN QUESTIONS FOR CTO

1. **Submit as-is, or arm the bounce pipeline first?** A dedicated configuration set + SNS event destination for the website sender would let the case claim programmatic handling rather than forwarding. It is a Terraform motion in my lane, ~1 window. **My read: submit as-is.** The use case is genuinely tiny and trigger-only; the suppression list is the control AWS actually cares about and it is on; and arming a pipeline solely to strengthen case prose is building an instrument for the reviewer rather than for us. But it is your call.
2. **Publish a DMARC policy on `opalinvest.dev`?** Cheap, makes Rule 23's sentence true, and improves deliverability posture. Out of this case's scope; flagged as its own motion. **`opalinvest.dev` DNS only -- never `opalinvest.com`.**
3. **Rule 23 precision defect** -- "DMARC-aligned" reads as a published policy and is not one. Recommend the clause distinguish *alignment* (true) from *published policy* (absent), or that we publish the record and make the original sentence true. Your ruling; CLAUDE.md is not my lane.
