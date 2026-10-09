# NFRA_OPSWKF -- Andrew-direct 2026-10-09 ~05:xxZ: a localhost dashboard the operations lead owns

**Author:** `2.0.0_SA_COO~O2` (dell2). **For:** `1.0.0_SA_CTO~DELL2` (an ENDPOINT addition is the CTO's).

## Andrew's words (verbatim, in session at the 2.0.0_SA_COO~O2 terminal)

> If you look at my conversation with Menachem, I think it would be helpful for him to have a really easy dashboard that
> he can control the design of on localhost. Essentially we do it for him, like a super light dashboard layout that has
> basic opal branding and the data, but tell him he can have his claude just edit it however he wants and if he needs
> more data from it, just ask and we'll go figure out what alerts to connect to the back and so on, something like that
> i think would be fun for him to feel he has control over it and it is designed to his liking

## Context in the Teams 1:1 (read 2026-10-09 via the gateway)

- Andrew, 2026-10-08T13:54Z, option B: "The summary data can be streaming to an internal ops dashboard (like those alerts
  you mentioned + key metrics)"; option A, one server his Claude pulls from (NFRA_MCPINDEX, site Z).
- The operations lead's list, 2026-10-07T22:36Z: billing; trade rec; post model update rec; high cash account alert FA;
  assets transfer alert FA; restricted account alert FA.

## What this seat reads it as (proposal; the CTO rules)

1. A starter kit, not a portal page: a small local web app (Opal branding: the portal's colour law and logo), runnable
   with one command on his machine, whose code he edits with his own Claude. Opal ships the first layout and the data
   adapter; he owns the design from then on.
2. Data enters through ONE adapter that reads what NFRA_MCPINDEX serves (option A), so a new panel is "ask for data",
   never a new pipeline. No AWS credentials on his machine.
3. "Figure out what alerts to connect to the back" is Andrew's word that alerts for him are in scope LATER, on his ask
   per alert. The kit ships with NO alert, notification or monitor (the moratorium stands until a named alert is asked).
4. Proposed as FWD-7 of this project (it is his workflow), sequenced after the FWD-1 thread or in parallel on a
   disjoint surface (a new folder; it touches no ticket or engine file).

## Open questions for Andrew (asked in session)

- Where the kit lives and how he gets it (a repo folder he clones, or a zip in SharePoint).
- Which of his six items are the first panels.
