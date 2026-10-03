# wsj, barrons, bbg and sa terms, read verbatim -- automated access, datamining, circumvention, AI use, organisation agreements


> **ANDREW-DIRECT 2026-10-03 ~17:3xZ (record `org/tier1_exec/2.0.0_SA_COO/deliverables/ANDREW_DIRECT_20261003_17xxZ_RELEASE_ALL_QUARANTINE_NO_DATA_OPS_CHANGES_WITHOUT_DIRECTIVE.md` @4d393e3521):**
> "We have permissions in place, it is inappropriate for agents to adjust our data engineering operations without my
> explicit directive. Release any quarantine that may have been initiated in any capacity."
> This file reads the publishers' CONSUMER terms. It does not account for the permissions Opal holds, which this seat did not
> see. It is research only: no agent changes data collection, storage or serving on the basis of it without Andrew's explicit
> directive.

**Author:** 4.0.0_SA_CRO~Z. **Asked by:** 1.0.0_SA_CTO~Z, msg 28716 (ONE ASK, "the same way" as the FT read @0fab00b8a0). One card
goes to Andrew when all four land. **This file is all four.**

**Method:**
- Read 2026-10-02 ~20:0xZ.
- Microsoft Edge, headed, with a fresh temporary profile: no publisher account, no cookies, signed out. Launched with
  `playwright-core` from `portal/node_modules` on the site-Z box.
- Navigation and text extraction only: no form, no sign-in.
- The full texts stay in the session scratchpad and are not committed (publisher copyright text). The clauses are quoted verbatim,
  with curly quotation marks and apostrophes normalised to ASCII.

| publisher | URL read | result | document and vintage |
|---|---|---|---|
| wsj | `https://www.wsj.com/policy/subscriber-agreement` | 200, redirected to `https://www.dowjones.com/terms-of-use/` (text identical) | Dow Jones "Terms of Use", **"Effective Date: June 30, 2026"** |
| barrons | `https://www.barrons.com/policy/subscriber-agreement` | 403, a 404 page ("That content doesn't seem to exist") | **The same Dow Jones Terms of Use governs barrons.com by name**, so no separate read is needed |
| (both) | `https://www.dowjones.com/terms-of-use/` | 200, 41,416 characters | as above |
| bbg | `https://www.bloomberg.com/notices/tos/` | 200, 80,493 characters | Bloomberg "Terms of Service" (TOS): General Terms plus Subscription Terms. **No date is printed on the page**; it says changes are "effective immediately". |
| sa | `https://about.seekingalpha.com/terms` | 200, 48,914 characters | Seeking Alpha "Terms of Use", **"Updated: May 2, 2021"** |

## Answer

All four consumer terms bar the HARVST collection as built, as FT's do. Each bars:
- automated access (robots, scrapers, bots, scripts);
- building or storing a database of their content;
- personal-use limits that an internal research pipeline does not meet.

**Dow Jones (wsj, barrons) is the most explicit of the five publishers:**
- it names "browser automation tool, API client, AI agent";
- it bars AI use "for training or grounding";
- it bars circumventing "technological protection measures";
- it bars disguising the User-Agent, and requires answering human-or-software checks honestly.

Bloomberg.com and Seeking Alpha bar robots, data mining and databases, but carry no AI-specific clause.

**FinBERT (FWD-16):**
- Dow Jones bars it in words: AI use, and "text or data mining" on stored articles.
- Bloomberg and Seeking Alpha bar the scraping and storing it would run on, without naming AI.

**Every document names the same way through: the publisher's prior written consent or licence.**

## Dow Jones Terms of Use (wsj.com, barrons.com) -- Effective Date: June 30, 2026

**Scope:** "These Terms of Use (this "Agreement") govern your access or use of all digital products and services from The Wall
Street Journal, Barron's, MarketWatch, Dow Jones Risk Journal ... Examples of the digital products and services that this
Agreement governs include wsj.com, WSJ Video, barrons.com, barrons.com/penta, marketwatch.com ..."

**Organisation agreements:** the only enterprise clause covers Risk Journal alone: "If you access Risk Journal as an authorized
user (an "Enterprise User") under an enterprise subscription, corporate subscription, group subscription, or other agreement
between Dow Jones and your employer or another organization (an "Enterprise Agreement"), your access to and use of Risk Journal
will be governed by the terms of the applicable Enterprise Agreement ..." **No equivalent clause covers wsj.com or barrons.com.**

**9.1:** "The Services are for your individual, personal and non-commercial use only. Thus, you may not access or use the
Content, including without limitation, any Content made available through one of our RSS feeds, in any commercial product or
service, without our express written consent."

**9.2 (credentials):** "You may not share your log-in credentials (including your password) with any other person whatsoever
(except as expressly permitted under an authorized multi-user arrangement) ... You agree not to access or attempt to access any
part of the Services using another person's credentials (for example, their log-in credentials or cookies), except as expressly
permitted under an authorized multi-user arrangement. Any violation of this clause will constitute a material breach of this
Agreement and may result in Dow Jones blocking your access to the Services."

**Storing and text mining:** "You may occasionally download, print and/or store articles from a Service for your individual,
personal, and non-commercial use ... In addition, you may not use articles you have downloaded, printed or stored to develop or
operate an automated trading system, or for text or data mining any information or content (including associated metadata)."

**9.4.1 (automated means):** "You shall not access, view, retrieve, refresh, reload, scrape, text or data mine, index, process,
store, harvest, or otherwise ingest the Services or any Content, whether directly or through an intermediary, using any
automated means, webcrawler, spider, script, site search/retrieval application, extension, bot, browser automation tool, API
client, AI agent or assistant, or other manual or automated device, tool, process, software or other means, without our prior
written consent."

**9.4.2 (volume, AI, circumvention):**
- "Access to Content at volumes, rates, or frequencies that exceed what is reasonably consistent with individual, personal
  consumption, as determined by us in our sole discretion, is prohibited, regardless of the method used, unless you receive our
  prior written permission."
- "Without limiting the foregoing, you may not harvest, ingest, use or incorporate any Content available through a Service for
  any form of artificial intelligence ("AI"), including in any generative or other form of AI for training or grounding purposes,
  unless you receive our prior written permission."
- "You agree not to ... circumvent any technological protection measures that limit or restrict a user's access to or use of any
  Service, ... attempt to circumvent any restrictions imposed on your use or access of the Services, or provide false,
  misleading, or inaccurate information about your identity ..."

**9.4.3 (autonomous software; identity; human checks):**
- "You may not operate or deploy any semi-autonomous or autonomous software that attempts to access, accesses, or interacts with
  any portion of our Services without our prior written permission."
- "If, after receiving our written permission, you operate or deploy such software, you must truthfully populate all HTTP request
  header fields (including, without limitation, the User-Agent, Referrer, and cookies) and clearly disclose the identity of your
  software in the User-Agent HTTP request header ..."
- "You must not include in the User-Agent HTTP request header information which may have the effect of disguising your
  identity."
- "You agree to honestly answer any question or prompt intended to assess whether an interaction is generated by a human or by
  software."

**9.4.4:** "We reserve the right to monitor your use of the Services, including without limitation access frequency, volume,
patterns, and methods of access, for compliance with this Agreement."

**9.4.5:** "You are prohibited from performing text and data mining activities under Art. 4 of the EU Directive on Copyright in
the Digital Single Market or similar statutes in other jurisdictions."

## Bloomberg Terms of Service (bloomberg.com) -- no date printed

**Scope:** "These TOS set forth the legal terms and conditions governing your use of our website located at www. Bloomberg.com and
any other online and mobile websites, blogs and interactive applications operated by Bloomberg L.P. ("BLP") (unless a different
policy is provided on a particular site, application or service, in which case such different policy shall govern and
control)."

**A.3, Restrictions on Use:**
- "You agree to use the Service solely for your own noncommercial use and benefit, and not for resale or other transfer or
  disposition to, or use by or for the benefit of, any other person or entity."
- "The Service and the information contained therein may not be used to construct a database of any kind. Nor may the Service be
  stored (in its entirety or in any part) in databases for access by you or any third party or to distribute any database
  Services containing all or part of the Service."
- "You shall not violate the security of the Service or attempt to gain unauthorized access to the Service, data, materials,
  information, computer systems or networks connected to any server associated with the Service, through hacking, password
  timing or any other means."
- "You shall not use or attempt to use any "scraper," "robot," "bot," "spider," "data mining," "computer code," or any other
  automate device, program, tool, algorithm, process or methodology to access, acquire, copy, or monitor any portion of the
  Service, any data or content found on or accessed through the Service, or any other Service information without the prior
  express written consent of BLP."
- "You may not forge headers or otherwise manipulate identifiers in order to disguise the origin of any other content."

**A.4, License:** "Should you choose to download content from the Service, you must do so in accordance with the TOS. Such
download is licensed to you by Bloomberg ONLY for your own personal, noncommercial use in accordance with the TOS and does not
transfer any other rights to you."

**Organisation subscriptions (Subscription Terms, 4. Acceptable Use):** "Access for Authorized Subscribers will be granted to a
Bloomberg account associated with their Company/Organizational specific email address. ... Bloomberg hereby grants to Client a
non-exclusive, non-transferable, non-sub-licensable license to allow its Authorized Subscribers to consume Bloomberg content for
personal use and for internal work-related, research, and general awareness purposes."
- **Reading:** a group subscription widens the PURPOSE to internal research. Nothing in it lifts A.3's bars on robots, data mining
  or databases.

**AI:** no AI or machine-learning clause on the page. The one hit on the AI and data-mining tokens is the "data mining" item in
A.3.

## Seeking Alpha Terms of Use (seekingalpha.com) -- Updated: May 2, 2021

**Personal use:** "Modification of the Content or use of the Content for any purpose other than your own personal, noncommercial
use is a violation of our copyright and other proprietary rights, and can subject you to legal liability."

**Automated access:** you agree not to "Use any robot, spider, site search/retrieval application, or other manual or automatic
device or process to download, retrieve, index, "data mine", "scrape", "harvest" or in any way reproduce or circumvent the
navigational structure or presentation of the Site or its contents".

**Account:** "You may only maintain a single account"; "You may never share your account user name or password or knowingly
provide or authorize access to your account ..."

**AI:** none (0 hits on the AI and machine-learning tokens). **Organisation agreement:** none found on the page.

## What each bears on (for the CTO's card; the rulings are not this seat's)

| HARVST act | wsj / barrons (Dow Jones) | bbg (Bloomberg.com) | sa (Seeking Alpha) |
|---|---|---|---|
| Scripted collection on a stored session | barred, 9.4.1, by name ("browser automation tool, API client") | barred, A.3 ("scraper ... robot ... bot") | barred ("robot ... automatic device or process") |
| Storing articles in bronze, silver and gold | barred, the storage clause + 9.4.1 ("store, harvest, or otherwise ingest") | barred, A.3 ("construct a database of any kind") | barred, "download, retrieve, index ... harvest" |
| Passing a bot check automatically (bbg press-and-hold, limb 2a "MET" r37; the barrons slider) | barred, 9.4.2 ("circumvent any technological protection measures") and 9.4.3 ("honestly answer any ... prompt ... human or by software") | barred, A.3 ("violate the security of the Service") | n/a (no challenge recorded) |
| A Chrome-impersonating client (`contracts.json` barrons.required_headers) | barred, 9.4.3 ("must not include in the User-Agent ... disguising your identity") | A.3 ("forge headers or otherwise manipulate identifiers") | -- |
| **FinBERT tone (FWD-16)** | **barred by name**: 9.4.2 (AI) and the storage clause ("text or data mining") | no AI clause; barred through the database and data-mining clauses it would run on | no AI clause; barred through "data mine" |
| Volume | 9.4.2: beyond "individual, personal consumption"; 9.4.4: monitored | A.3: "unreasonable or disproportionately large load" | -- |
| The named way through | "prior written consent" / "express written consent" (9.1, 9.4.1-9.4.3) | "prior express written consent of BLP"; a group subscription widens purpose only | "prior written permission" |

**For the one card (the CTO writes it):** the five publishers' consumer terms all bar the pipeline's core acts. Two read
explicitly onto FinBERT (FT s.3.5; Dow Jones 9.4.2). The road the terms themselves name is a licence or written consent per
publisher: FT corporate licence or Datamining API; Dow Jones written consent (or its licensed products, not researched here);
Bloomberg written consent (and the held Terminal, under its own agreement, not read here); Seeking Alpha written permission.
Ruling on the stored corpus and on collection is Andrew's call; counsel's reading is his to ask for.

## Not claimed

- Any legal opinion. These are the clauses as printed, with this seat's reading per act.
- The Bloomberg Terminal's own agreement. The Terminal is a different service under a different contract, and was not read.
- Dow Jones's licensed products (Factiva, DNA, Newswires) and their terms.
- Whether Opal holds any group or enterprise agreement with any of these publishers. If one exists, it may govern instead (the FT
  s.1.4 pattern). Dow Jones's enterprise clause names Risk Journal only.
- That any publisher has detected or objected to HARVST.
