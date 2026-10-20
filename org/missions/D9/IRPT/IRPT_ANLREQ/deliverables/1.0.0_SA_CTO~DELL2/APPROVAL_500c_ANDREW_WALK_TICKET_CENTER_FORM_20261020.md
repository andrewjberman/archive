# CTO approval: row dell2-20261020T150743Z-500c, the Ticket Center form per Andrew's 2026-10-20 walk

**Seat:** 1.0.0_SA_CTO~DELL2. **Date:** 2026-10-20 ~15:12Z. **Asked by:** 4.0.0_SA_CRO~TCKT (msg 15:08Z).
**Branch:** `cand/dell2/anlreq-andrew-walk` @f41b4fce, one commit on origin/PROD 4546cee0.
**Authority:** `org/tier1_exec/4.0.0_SA_CRO~TCKT/deliverables/ANDREW_DIRECT_20261020_15xxZ_TCKT_SYNTHESIS_ANSWERS.md`
@f2581e90b9, items 2, 4, 5 and 7.

## What was read here

- **`git diff --stat origin/PROD f41b4fce`:** 8 files, +148/-24, all under `src/pages/TicketCenter/` (2 source files, 6 test files).
- **`src/pages/TicketCenter/analysisRequest.ts` is unchanged.** The analysis submission body, which the guard fix 4546cee0 made
  fileable, is untouched, so the guard regression of 09:28Z cannot recur from this change.
- **The Advisor field** already existed. It now starts as the signed-in filer's name and stays editable. A typed name is never
  overwritten.
- **The date ("Needed by") field** is removed, from the form and from Form as filed.
- **Other ETFs** are entered as chips with Enter. A typed ticker is added on blur.
- **Form as filed** drops the Variant, Needed by and Add commentary rows.

## Ruling

APPROVED, class Opal-internal (the Ticket Center is Opal-only).

- **The CROSS-BOX scope on the row** comes from a stale status line of a withdrawn AMGT_RESAPP order (row IRPT_ANLREQ-D2-S228).
  An approval row's validity is read by approval-status, and no cross-box ruling is required.
- **Timing:**
  - The DEV merge-forward may go now.
  - The PROD promote waits until run 7 (TO-RUN-COMMENTARY-E2E-7, GO ~14:31Z) is terminal. That run drives the current PROD
    form through a browser script, and the page must not change under it.
  - After the promote, one filing through the new form, by the same synthetic staff user, shows the four items still arrive.
