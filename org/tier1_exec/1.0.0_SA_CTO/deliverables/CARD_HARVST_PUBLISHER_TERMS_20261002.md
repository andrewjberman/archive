# CARD for Andrew -- AMGT_HARVST against the five publishers' terms (`1.0.0_SA_CTO~Z`, 2026-10-02 ~20:2xZ)

**Evidence** (each read verbatim in a headed browser on an Opal machine by `4.0.0_SA_CRO~Z`):
- FT: `org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/FT_SIGNIN_ROUTES_20261002/FT_TERMS_VERBATIM_20261002.md` @0fab00b8a0;
- wsj, barrons, bbg and sa: `org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/HARVST_PUBLISHER_TERMS_20261002/PUBLISHER_TERMS_VERBATIM_20261002.md` @961a99cd64
  (with its per-act table).

## What the terms say about what HARVST does

| HARVST act | FT | wsj / barrons (Dow Jones ToU, effective 2026-06-30) | bbg (Bloomberg.com TOS) | sa (2021) |
|---|---|---|---|---|
| scripted collection on a stored session | barred (spidering, scraping) | barred BY NAME (9.4.1: "browser automation tool, API client, AI agent") | barred (A.3: "scraper ... robot ... bot") | barred ("robot ... automatic device or process") |
| storing articles (bronze, silver, gold) | barred ("systematic download-and-store") | barred ("store, harvest, or otherwise ingest") | barred ("construct a database of any kind") | barred ("download, retrieve, index ... harvest") |
| passing bot checks automatically | barred (s.3.2, circumvention) | barred (9.4.2, 9.4.3) | barred (A.3) | -- |
| FinBERT tone | barred (s.3.5: ML/AI "to generate any data") | barred BY NAME (9.4.2, AI) | barred via the data-mining and database clauses | barred via data mining |
| **the named way through** | an organisation's agreement prevails (s.1.4) | "prior written consent" | "prior express written consent of BLP" | "prior written permission" |

**The conflict, stated plainly.** FWD-11's RULE carries Andrew's own words: "that project is not over until we beat captchas and have
robust auth solution"; "we do not accept any defeat to that end". Passing the publishers' bot checks automatically is what four of
the five sets of terms bar as circumvention. This seat cannot reconcile a standing word of Andrew's with a third party's contract.
That reconciliation is his, and it is a legal-risk judgement.

## Taken now by this seat (reversible; nothing deleted; no new exposure added)

1. **FinBERT (HARVST FWD-16 / FWD-17) is HELD,** for every publisher, not only ft. It is new work that has not been cut, and Dow
   Jones bars AI use by name. DSGN FWD-21's tone fill renders its designed "no clear tone" state until then.
2. **ft stays hard-stopped,** and its 62 stored articles are quarantined, not deleted (@ce138d2314).
3. **Collection on wsj, barrons, bbg and sa is UNCHANGED** pending his word. Pausing it would override his standing RULE, so
   `2.0.0_SA_COO~H` readies the pause (the STOP set, every publisher) to flip the minute he says so.

```
+-- CALL 1 of 1 ----------------------------------------------------+
  **Pause HARVST's automated collection on wsj, barrons, bbg and sa
  until written consent or licences are in place? (a) pause now
  (b) continue at your risk while consent is sought**
  All five publishers' terms bar scripted collection, storage, and
  automated bot-check passing; Dow Jones names "browser automation
  tool" and "AI agent". Each names written consent or a licence as
  the way through. FWD-11's "beat captchas" asks for what four of
  them call circumvention.
  --------------------------------------------------------------------
  **REC --** (a): pause new collection now (one STOP flip, reversible
  in a minute); keep the stored corpus where it is, and the portal's
  internal display of headlines with links, pending counsel's read;
  and open the consent / licence requests (Dow Jones, Bloomberg,
  Seeking Alpha, and the FT quote already carded). Every run adds to
  an exposure the terms call a breach of contract and possibly of
  copyright, while consent is the route each publisher itself names.
+---------------------------------------------------------------------+
```

**Not claimed:** any legal conclusion. The terms are read verbatim; what they mean for Opal's position is counsel's to say.

## ADDENDUM 1 (`1.0.0_SA_CTO~Z`, 2026-10-03 ~16:3xZ) -- the call re-worded, because the state it asked about has changed

**What changed** (`2.0.0_SA_COO~H` msg 28883, read 16:2xZ): every backfill has finished. sa finished at 04:46Z (89/89 pairs,
11,125 stored, not interrupted), and bbg, barrons and wsj finished earlier. ft is STOP_FT. The scheduled task "Opal Data Harvest -
Local Publications" is Disabled, and no HARVST collector process is running. A pause is therefore moot: nothing is collecting. The
only live exposure is a RELAUNCH, and no seat starts one until he answers. CALL 1 above is superseded by the card below. The
evidence, the table and items 1-2 of "Taken now" stand unchanged.

```
+-- CALL 1 of 1 (re-worded) ----------------------------------------+
  **Authorize any further automated collection on wsj, barrons, bbg
  or sa? (a) none until written consent or licences are in place
  (b) relaunch at your risk while consent is sought**
  Collection has stopped on its own: every backfill finished and no
  collector is running. Nothing new is collected unless a seat
  relaunches, and none will without this word. All five publishers'
  terms bar scripted collection and storage, and each names written
  consent or a licence as the way through.
  --------------------------------------------------------------------
  **REC --** (a): no relaunch. Keep the stored corpus where it is,
  with FinBERT and the event rebuild still held, pending counsel's
  read. Open the consent / licence requests (Dow Jones, Bloomberg,
  Seeking Alpha, and the FT quote already carded). (a) costs
  nothing today, and every relaunched run adds to the exposure.
+---------------------------------------------------------------------+
```
