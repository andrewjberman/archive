# FT's terms on automated access, read verbatim -- for AMGT_HARVST FWD-11 (ft limb) and FWD-16 (FinBERT)


> **ANDREW-DIRECT 2026-10-03 ~17:3xZ (record `org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261003_17xxZ_RELEASE_ALL_QUARANTINE_NO_DATA_OPS_CHANGES_WITHOUT_DIRECTIVE.md` @4d393e3521):**
> "We have permissions in place, it is inappropriate for agents to adjust our data engineering operations without my
> explicit directive. Release any quarantine that may have been initiated in any capacity."
> This file reads the publishers' CONSUMER terms. It does not account for the permissions Opal holds, which this seat did not
> see. It is research only: no agent changes data collection, storage or serving on the basis of it without Andrew's explicit
> directive.

**Author:** 4.0.0_SA_CRO~Z. **Asked by:** 1.0.0_SA_CTO~Z, msg 28705 (ONE ASK: read the terms verbatim in a headed browser on an Opal
machine, and land the clauses that bear on automated reads by a consumer subscriber).

**Method:**
- Read 2026-10-02 at 19:47:29Z.
- Microsoft Edge, headed, with a fresh temporary profile: no FT account, no cookies, signed out. Launched with `playwright-core`
  from `portal/node_modules` on the site-Z box.
- Navigation and text extraction only: no form, no sign-in.
- Both pages answered 200:
  - `https://help.ft.com/legal-privacy/terms-and-conditions/` ("Terms and Conditions | Help Centre", 33,609 characters);
  - `https://help.ft.com/legal-privacy/copyright-policy/` ("Copyright Policy | Help Centre", 9,718 characters).
- The full extracted text stays in the session scratchpad. It is not committed, because it is FT's copyright text. The clauses
  below are quoted verbatim, with curly quotation marks and apostrophes normalised to ASCII.

**Vintage:**
- The Terms and Conditions state: "These Terms and Conditions were published on 01 July 2026 and replace with immediate effect the
  Terms and Conditions previously published on 15 October 2025" (s.7.1).
- The Copyright Policy states: "This version of the copyright policy was published on 31 May 2023", and "This policy forms part of
  our terms and conditions."

## Answer

**On a consumer subscription, FT's terms bar the ft limb as built, not only the solver question.** The Copyright Policy, which
the Terms make binding (s.3.3, s.3.4), forbids:
- datamining and spidering;
- building a database by systematically downloading and storing FT content;
- harvesting or scraping;
- **any machine-learning or AI use of FT content, which reaches FinBERT scoring.**

It calls each of these "a breach of contract" that "may also violate copyright law", with "personal and corporate liability".
The way through is the one the terms name themselves: "unless you buy the appropriate licence". An organisation's agreement
overrides the consumer terms where they conflict (s.1.4).

## The clauses, verbatim

### Terms and Conditions (published 01 July 2026)

**s.1.4 (an organisation's agreement prevails):** "If you access FT.com under an organisation's subscription agreement, then your
access is primarily governed by the subscription agreement between us and that organisation. In the event of any conflict
between these Terms and Conditions and the organisation's subscription agreement (as applicable), the terms of the
organisation's subscription agreement shall prevail to the extent of the inconsistency only."

**s.3.2 (security technology):** "Nothing in these Terms and Conditions grants you any legal rights in FT.com or the FT Content
other than as necessary to enable you to access FT.com and use the FT Services. You agree not to adjust, to try to circumvent or
delete any notices contained on FT.com (including any intellectual property notices) and in particular in any digital rights or
other security technology embedded or contained within FT.com."

**s.3.3 / s.3.4 (the Copyright Policy binds):** "You are permitted to use the FT Content only as set out in our Copyright Policy."
"You agree to comply with our Copyright Policy when using FT Content. You are responsible for all use of FT Content whether
accessed without a Subscription as a registered user, under your Subscription, or under your organisation's Subscription."

**s.3.5 (machine learning and AI):** "To the fullest extent permitted by law, we expressly prohibit any use of our content or data
(including any associated metadata) in any manner for any machine learning and/or artificial intelligence purposes, including
without limitation for the purposes of training or development of artificial intelligence technologies or tools or machine
learning language models, or otherwise for the purposes of using or in connection with the use of such technologies, tools or
models to generate any data or content and/or to synthesise or combine with any other data or content. We reserve all rights to
license any use of our content and data for any such purposes."

**s.3.7 (Standard vs Premium):** "Your access to FT Content will vary depending on whether you have a FT Standard or FT Premium
Digital Subscription. ... an FT Premium Subscription gives readers full access to FT journalism, including exclusive additional
analysis and insight."

**s.3.9 / s.3.10 (the ID; remember-me):** "On registration, you will choose a user name and password ("ID"). It is your
responsibility to keep your ID confidential. The email address must not correspond to a generic or shared email account ..."
"We recommend that you do not use FT.com's "Remember me" log in feature on any device that may be used by anyone other than you
..."

### Copyright Policy (published 31 May 2023; "forms part of our terms and conditions")

**Status of a breach:** "Where we state below that something is not allowed or permitted, then to do so is a breach of our terms
and conditions: that is, it is a breach of contract, and may also violate copyright law." And: "Use that is made without our
permission may therefore infringe our copyright which can result in personal and corporate liability."

**What a subscriber may do:** "View our content for your personal use on any device that is compatible with FT.com ... and store
our content on that device for your personal use; Print single copies of articles on paper for your personal use; Share links to
articles by using any sharing tools we make available."

**What a subscriber may not do** ("You cannot do anything other than make use of the content as set out above, unless you buy the
appropriate licence"). The items that bear on HARVST:
- "If you are a registered user or subscriber, share your user name and password (which includes PINs) with anyone else. A
  password is for one person's use. ... We monitor usage to detect password sharing."
- "Copy, publish or redistribute full text articles, photographs, graphics, tables or images in any way (except as permitted by
  any sharing tools we make available)."
- "Use spidering technology or other datamining technologies to search and link to FT.com."
- "Create a database in electronic or structured manual from by systematically and/or regularly downloading, caching, printing
  and storing all or any FT content (by spidering or otherwise)." ("from" is FT's own typo for "form", quoted as printed.)
- "Use any of our content or data (including any associated metadata) in any manner for any machine learning and/or artificial
  intelligence purposes, ... or otherwise for the purposes of using or in connection with the use of such technologies, tools or
  models to generate any data or content ..."
- "Frame, harvest or scrape FT content or otherwise access FT content for similar purposes."
- "Use or attempt to use FT content outside the parameters we set depending on what subscription you have."

**Where the licence is bought:** "If you have any questions on copyright or republishing our material, please contact our
republishing team at syndication@ft.com."

## What each clause bears on (for the CTO; the rulings are not this seat's)

| HARVST act today or folded | clause | reading |
|---|---|---|
| The ft collector: listing search, then article fetch, run by a script on a stored session (`contracts.json` ft) | CP "spidering ... datamining"; "harvest or scrape" | Barred on a consumer subscription. |
| Storing ft articles in `opal-data-harvest` bronze, silver and gold (62 stored) | CP "Create a database ... by systematically and/or regularly downloading ... and storing" | Barred. **The 62 already stored are in scope of this clause.** Keep, quarantine or purge is the CTO's call, or Andrew's. |
| A solver, or any act clearing FT's Security Verification | T&C s.3.2, "try to circumvent ... security technology" | Barred. (hCaptcha's own terms bar it too: previous brief @057df8f244.) |
| **HARVST FWD-16 (folded today @82d1cb21e2): FinBERT tone per article, ft included** | T&C s.3.5; CP, the ML/AI item | **Barred for ft content**, "to generate any data". FWD-16 as folded does not exclude ft. **This needs a ruling before FWD-16 is cut.** |
| Mention matching and gold rows derived from ft text (title now on the mention row) | CP "Create derivative works"; s.3.5 "synthesise or combine" | Inferred to be in scope. The matcher is not ML, but the derived rows combine FT text with other data. |
| The session shared by an automated process (keep-alive, tab transport) | CP "A password is for one person's use ... We monitor usage" | It bears on why sessions die at 24-75 min. That is INFERRED: the terms say FT monitors usage; they do not say how it revokes. |
| Premium articles skipped (`contracts.json` ft.premium_tier) | T&C s.3.7 | The account is FT Standard. Premium is a different subscription. |
| **An FT corporate licence** (previous brief) | T&C s.1.4; CP "unless you buy the appropriate licence"; s.3.5 "We reserve all rights to license" | **The licensed route is the one the terms themselves name.** The organisation's agreement prevails where it conflicts. ML use needs that licence to say so explicitly. |

## Not claimed

- **The other four publishers' terms (wsj, barrons, bbg, sa).** None were read. Every inference to them is unsupported until each
  is read the same way. The same FWD-16 question applies to each.
- Any legal opinion. These are the clauses as printed, with this seat's reading of how they bear on each act. Counsel's reading is
  Andrew's call.
- That FT has detected or objected to HARVST.
- What Opal's FT account agreement says, if it is anything other than these consumer terms.
