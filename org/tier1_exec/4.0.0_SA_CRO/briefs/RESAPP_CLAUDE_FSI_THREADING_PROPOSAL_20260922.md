# THREADING CLAUDE FOR FINANCIAL SERVICES INTO AMGT_RESAPP -- an implementation PROPOSAL

**Author:** 4.0.0_SA_CRO~F (Chief Research Officer, site-Z lane F)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Recon ID:** RCN-0011 (brief 2 of 2; the teardown this builds on is `CLAUDE_FSI_PLUGIN_STRUCTURE_AND_DATA_SHAPES_BRIEF_20260922.md`)
**Date:** 2026-09-22 ~15:5xZ. **Commissioned:** Andrew-direct ~14:5xZ at this terminal, step 3 verbatim: *"Assess where/how we
can thread in some of these channels into the RESAPP security analysis research application on the Dashboard ... 2.) An
implementation proposal on how to thread this in to the RESAPP application."*
**Status:** **PROPOSAL.** Nothing here is a cell, an FWD number, a PRD edit or a dispatch; those are `1.0.0_SA_CTO~Z`'s (L2/L4)
and `2.0.0_SA_COO~Z`'s (L5/L6). Mid-round AMGT_RESAPP is frozen (round 28 in flight @0ed364cff0); this lands as CTO intake.

---

## 0. The frame, and what RESAPP already is

Grounding read at HEAD (2026-09-22): PRD v0.22 (20 outcomes FWD-1..20, 12-row surface manifest), `lib/research/` (18
modules, 105 non-test .py), portal `SecurityAnalysis` (5 tabs: Thesis, Exec Management, Peers, Model, Posture; Lead Panel;
overlay, provenance line, check-face badge, print export). The page's producers today:

| RESAPP surface | outcome | producer today | basis |
|---|---|---|---|
| Model block (~20 line items x 10 FY + ~25 header scalars) | FWD-1/3 | Bloomberg terminal -> harvest bronze (6 requests incl. `bestdata`) -> `model_block` silver | Bloomberg |
| Thesis prose + one chart | FWD-18/9 | `lib/research/filings` (EDGAR 10-K/20-F, Item 1A + 7, two passes, citations resolved to passages) -> `drafting` with the verbatim gate | filing |
| Exec Management + tenure | FWD-17 | filing officer section + Lusha profile + Bloomberg `exec_officers` fallback | filing / Lusha |
| Peers (comparable multiples) | FWD-8 | CSC-shaped table on Bloomberg fields; the SET is the measured defect (48 of 54 stale) | Bloomberg |
| Posture | FWD-19 | ETF holdings plane + scanner presets (DIVZ 13 codes, PFOE 16) + comparable-set judgment | Opal |
| Lead panel (trending / breakout x price / chatter) | FWD-16 | `opal-harvest-security-metrics` generations | Bloomberg + harvest |
| Coverage / chatter / news | FWD-4/11 | AMGT_HARVST publications (SA, Bloomberg.com, Barron's, WSJ, FT) + social | publishers |
| Print pack | FWD-5 | print renderer to Adam's template | -- |

The rule this proposal is written under is the CRO charter's METHOD-vs-NUMBERS split: the LLY pack is a defensible
REFERENCE for STRUCTURE (what a per-name earnings pack contains and how it discloses), never the source of our NUMBERS,
which stay Bloomberg/filing-based under `C-BLOOMBERG-BASIS`. And the standing veto: no shadow pipeline -- a second pack
producer standing BESIDE the page is exactly what "build alongside" forbids; every channel below feeds a page surface or it
is not proposed.

---

## 1. CHANNEL BY CHANNEL: what the pack has, what the page has, what would thread in

| pack folder / channel | RESAPP surface it maps to | today | what the channel ADDS | source class (brief 1 s.3) | threading option (s.2) |
|---|---|---|---|---|---|
| `01_filings/` 8-K earnings releases, 10-Q, DEF 14A | FWD-18 filings analyzer; FWD-17 exec/tenure | 10-K / 20-F only, Items 1A + 7 | **the quarterly EVENT**: 8-K release (non-GAAP bridge, guidance table, price/volume decomposition), 10-Q, and the proxy for comp/tenure/pay ratio | P (EDGAR) | **T1** extend `filings/fetch.py` forms + a new `earnings_event` analysis object |
| `03_financials/` data pack (8 sheets) | FWD-1 model block | Bloomberg FY series | nothing on the FY figures; **Non-GAAP Bridge, Guidance (prior vs updated), Quarterly Series** are NOT in the model block | P | T1 (same object) |
| `02_transcript/` call notes | none today | -- | **a transcript channel**: prepared remarks, CFO table, Q&A themes; the pack's is a third-party rendering, not verbatim | W (SA/Globe) or V (Aiera, FactSet, S&P `get_transcript_from_key_dev_id`) | **T3** as a HARVST publication type (SA already a harvester) or **T2** with a subscription |
| `07_analyst_sentiment/` targets, revisions, ratings | none on the page; the brief's O4 "what has been said" is publications, not estimates | -- | **consensus + estimate REVISIONS + target dispersion** -- the pack calls revisions "the cleanest bullish signal" | V (kfinance `get_consensus_estimates_from_identifiers`, LSEG `qa_ibes_consensus`, FactSet) -- OR **Bloomberg `bestdata`, which the harvest already lands** | **T4** revisions from bestdata bronze VINTAGES (bronze is never overwritten, so each pull is a dated consensus snapshot: the revision series is the diff) |
| `05_ownership_short/` 13F, short interest | none | -- | register structure, short interest, insider % | W (Fintel) or Bloomberg fields | T4 (Bloomberg) -- a new bronze request, not a web aggregator |
| `08_dcf_model/` live DCF + WACC + sensitivity | FWD-20 house forward view; Model tab Upside/Base/Downside cases | cases exist; no DCF | a DCF with the house's own drivers on blue rows, and the sensitivity grid | model computation over P + V inputs | **T5** the `dcf-model` SKILL's method as a spec for `lib/research/model` cases, not a vendor call |
| `09_peer_analysis/` comps table + obesity map | FWD-8 peer set | CSC shape right, set BROKEN | a **candidate peer SET** chosen by the model from public lists + `get_competitors_from_identifiers` if subscribed; the multiples table is our CSC already | W or V | T5 (candidate set proposed, `C-IDENTITY-RESOLVED` confirms) |
| `10_company_specific/` catalyst calendar, governance | Thesis (big bets/challenges); Exec tab | prose only | **dated catalyst calendar** (a timeline object) ; governance figures from DEF 14A | P + W | T1 (DEF 14A) + T5 |
| `06_supply_chain/` | Thesis | prose | mostly disclosure-gap statements; low value beyond what 10-K Item 1A already yields | P + W | none proposed |
| `04_market_data/` | Lead panel / overlay | Bloomberg histdata | nothing (third-party multiples on a different basis) | W | none -- basis conflict |
| `11_output/` one-pager + earnings update docx/pdf + charts | FWD-5 print renderer | Adam's Excel->Word one-pager | a **second print artifact class** (the quarterly earnings update) and a docx authoring engine | skill | **T5** the earnings-update SECTION STRUCTURE as the print renderer's second template; the numbers from the page, never re-fetched |

Subtraction over the pack's 11 content folders: 8 map to an existing outcome, 2 are genuinely new surfaces (transcript;
consensus/revisions/ownership), 1 is not proposed (supply chain). Over the page's 20 outcomes: 12 untouched by this
proposal (FWD-2, 6, 7, 10, 11, 12, 13, 14, 15, 16, 19 and 3 is only fed); the channels above touch FWD-1, 5, 8, 9, 17, 18,
20 and would need two NEW outcomes (the CTO's to number) for the earnings event / consensus surfaces.

---

## 2. THE THREE WAYS TO THREAD IT IN, and which to use where

**A. Skill-as-producer** -- run the plugin's `earnings-analysis` (or the `earnings-reviewer` cookbook) headless per
(security, quarter), land its folder as a bronze channel under the harvest grammar, type its xlsx tabs as silver.
*Pros:* one afternoon to an LLY-like pack for any name; the disclosure discipline comes free. *Cons:* the figures are
web-sourced third-party numbers on a non-Bloomberg basis (`C-BLOOMBERG-BASIS` says no); prose is machine-written and must
pass FWD-9's marking rule and the verbatim gate, which the skill's DOCX does not carry; a whole pack beside the page is the
shadow-pipeline shape; per-run cost unmeasured (card 1 measured USD 1.06 for ONE filing pass; a full pack is many passes
plus web tools). **Use ONLY for structure and for prose sections the page already owns (T5), never as a number source.**

**B. MCP connector inside our own producers** -- our `filings/analyze.py`-class calls pass `mcp_servers` + `mcp_toolset`
so the MODEL fetches consensus/transcripts from a vendor mid-call. *Pros:* zero client code for the vendor protocol.
*Cons:* needs a vendor subscription AND an OAuth token Opal obtains interactively and refreshes itself (Secrets Manager
custody, a rotation job -- a new substrate); the vendor data enters through the model's context, so bronze-as-received
(`C-BRONZE-AS-RECEIVED`) cannot be satisfied -- there is no as-received object, only `mcp_tool_result` blocks; not ZDR.
**Not recommended for a pipeline. Fine for an analyst's interactive Cowork/Code session.**

**C. Vendor REST as an ordinary harvest channel** (Daloopa `X-API-KEY`, kfinance `client_id + private_key`, LSEG/FactSet
enterprise APIs) -- H0-store bronze (bytes as received), silver typed, the model never in the data path; MCP reserved for
humans. *Pros:* fits every ratified harvest contract without exception; the Daloopa datapoint (`value_raw, value_normalized,
unit, fiscal_period, calendar_period, filing_type, document_id`) types directly onto our `(security_key, fiscal_year,
mnemonic)` grain AND brings the per-figure filing citation ours lacks. *Cons:* subscription; one channel writer per vendor
(the H1-bloomberg pattern, ~1 cell each). **Recommended IF a subscription exists.**

**The recommendation, in two cases:**

- **No new subscription (today's estate):** T1 + T4 + T5 + T3. Extend the filings channel to the quarterly event (8-K, 10-Q,
  DEF 14A) and build the earnings-event object; derive consensus/revisions from Bloomberg `bestdata` vintages already
  landing; take the skills' METHODS (earnings-update section structure, DCF driver layout, peer-candidate selection) as specs
  for surfaces the page already owns; put transcripts through HARVST as a publication type. **Zero vendor MCP, zero new
  token custody, everything under the harvest grammar.** This reproduces roughly 8 of the pack's 11 folders from data the
  firm already pays for.
- **With one subscription (S&P kfinance or Daloopa -- Andrew's call, priced by the vendor):** add C for consensus,
  estimates and transcripts, which closes the two genuinely new surfaces with a citable vendor basis and gives the
  Bloomberg-vs-vendor consensus discriminator the LLY pack could not have (its two EPS figures stayed unresolved).

---

## 3. WHAT MUST BE MEASURED BEFORE A CELL (Rule 28 cards, each with an owner)

| # | substrate | question | owner |
|---|---|---|---|
| S1 | Bloomberg `bestdata` bronze | does it carry BEst EPS/revenue means, counts, and does a second pull differ (i.e. is a revision series derivable)? denominator: names x pulls | `2.0.0_SA_COO~Z`'s harvest cells (H1) |
| S2 | EDGAR 8-K / 10-Q / DEF 14A through `filings/fetch.py` | form selection by `filing_identity`, the 8-K exhibit (EX-99.1) that carries the release, the proxy's officer table | the filings chain |
| S3 | Claude API cost per earnings-event pass | one 8-K + 10-Q through the two-pass analyzer with citations; card 1's shape | `1.0.0_SA_CTO~Z` (vendor account owner: Andrew) |
| S4 | transcript source terms | SA's terms Andrew cleared (PRD v0.13) cover articles; do they cover transcripts? Globe and Mail? | Andrew |
| S5 | print renderer second template | the earnings-update section structure vs Adam's one-pager: which is the print target for a QUARTER? | Andrew + Adam |
| S6 | vendor subscription | which, if any; price; whether an API-key path (Daloopa) or OAuth-only (S&P) | Andrew |

---

## 4. SEQUENCING (proposed, for the CTO's round-N analysis; the COO cuts)

1. **Intake:** this brief into `CTOZ_AMGT_RESAPP_PANEL_BRIEFS_INTAKE_20260918.md` as an ADD (earnings event + consensus)
   and a RESTATE (transcript via HARVST). No round is re-cut.
2. **Cards S1-S3** as measurement acts (not cells) at the next L10; S4-S6 as open calls to Andrew.
3. **Round N+1 candidates** (dependency order): filings forms extension -> earnings-event object -> Model tab's guidance /
   non-GAAP bridge rows -> bestdata revision series -> Lead panel / Thesis consumers -> print template 2. Transcript type in
   HARVST is that project's, driven by `2.0.0_SA_COO~Y`.
4. **Vendor channel C** only after S6 says yes -- one H1-style writer per vendor.

---

## 5. OPEN CALLS FOR ANDREW (each with this seat's recommendation)

1. **Subscription?** Recommend: none until S1 shows Bloomberg `bestdata` cannot give revisions; then Daloopa first
   (API-key path, published record shape, filing citations) over S&P (OAuth-only, the full LLM-ready API).
2. **Install the plugin on this box?** Recommend NO on the shared Windows user (every seat's sessions would get twelve
   vendor OAuth prompts); YES on an analyst's own machine or in Cowork, which is where it earns its keep. The cloned copy in
   this seat's scratchpad already served the study; the skills' methods can be lifted into specs from the repo directly.
3. **Print target for a quarter:** Adam's one-pager stays the ratified artifact (FWD-5); is the LLY-style earnings update a
   second template or a replacement? Recommend: second template, same renderer, same numbers.
4. **Egress class for any skill run** that web-searches: it is class W egress through Anthropic's tools, not Bright Data;
   recommend it stays an interactive-analyst act, never a scheduled producer.

---

## 6. WHAT THIS BRIEF DOES NOT DO

It mints no FWD, edits no PRD, cuts no cell, installs nothing, calls no vendor, and does not settle whether Yang's pack
is the artifact Adam wants -- that is a design question for Andrew and Adam. Every "adds" claim in s.1 is against the page
as read at HEAD today; a surface landed by round 28 after this read would move a row from "none" to "exists".
