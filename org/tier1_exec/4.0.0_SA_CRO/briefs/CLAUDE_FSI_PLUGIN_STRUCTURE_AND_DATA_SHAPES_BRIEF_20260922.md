# CLAUDE FOR FINANCIAL SERVICES: what "the plugin" is, where its data comes from, and the shape of that data on the wire

**Author:** 4.0.0_SA_CRO~F (Chief Research Officer, site-Z lane F)
**Home:** org/tier1_exec/4.0.0_SA_CRO/
**Recon ID:** RCN-0011 -- registered in RECON_REGISTER.md (brief 1 of 2; brief 2 is `RESAPP_CLAUDE_FSI_THREADING_PROPOSAL_20260922.md`)
**Date:** 2026-09-22 ~15:0xZ-15:5xZ. **Commissioned:** Andrew-direct at this terminal ~14:5xZ, verbatim in
`../deliverables/ANDREW_DIRECT_20260922_145xZ_CLAUDE_FOR_FINANCE_RESAPP_RESEARCH_PROJECT.md` @c23d5f7dc0: *"1.) Secure the
Claude for Finance plugin access ... figure out the endpoint or if we have to download a MCP ... 2.) Study the MCP/endpoints
... what is the shape of that data coming in over the wire. Maybe use LLY as a test case"*.
**Subject:** Anthropic's open-source **Claude for Financial Services** plugin marketplace (`github.com/anthropics/financial-services`)
and the LLY research pack Yang Liu produced with it, in the synced SharePoint library.

---

## 0. What this is, and its denominators

A TEARDOWN in the RCN-0001/0002 pattern, from captured artifacts, with the CAPABILITY / FEASIBILITY / PLAN split kept. This
brief is CAPABILITY (what the thing is and what it emits). Feasibility against Opal's data and the PLAN are brief 2.

```
  EVIDENCE BASIS -- every figure below was read at a stated vintage, not recalled
    A  the marketplace repo   anthropics/financial-services @574ed36 (2026-09-21 14:10:41 -0700), cloned 2026-09-22 ~15:0xZ
                              19 marketplace entries; 10 agent plugins; 6 vertical plugins; 2 partner plugins; 1 M365 installer
                              (files read: README.md, CLAUDE.md, .claude-plugin/marketplace.json, 5 .mcp.json, 3 SKILL.md,
                              2 agents/*.md, 1 cookbook agent.yaml, lseg/CONNECTORS.md, spglobal/README.md)
    B  the LLY pack           OneDrive - Opal Capital/Shared - Documents/Claude Financial Services/2026Q2/LLY (synced locally,
                              cloud placeholders hydrated on read): 12 folders, 58 files, README.md + SOURCES.md read in full,
                              3 xlsx (13 sheets) opened, 2 Opal-branded docx text-extracted, 4 md heads read
    C  endpoint discovery     12 of 12 declared MCP servers probed UNAUTHENTICATED (card + raw JSON in
                              ../deliverables/CLAUDE_FSI_RECON_20260922/)
    D  public documentation   platform.claude.com MCP-connector page; anthropic.com/news (2025-07, 2026-05-05);
                              docs.daloopa.com (3 pages); docs.kensho.com (2 pages); academy.claude.com install tutorial
    E  prior estate work      1.0.0_SA_CTO~W substrate card 1 @5007337353 (2026-09-15, Boeing 10-K through the Claude API)
    F  local Claude Code      2.1.278; ONE marketplace registered (claude-plugins-official); ZERO plugins installed
```

**DECLARED GAPS, in-band:** `[BODY-NOT-CAPTURED]` for every vendor's `tools/list` and every tool's response body -- no vendor
token exists here and no vendor tool was called; vendor record shapes below come from the vendors' PUBLIC docs and from the
skill files that name their tools, and are marked so. The Cowork UI path was not exercised (no Claude Desktop session on
this seat). Yang Liu's own session transcript was not read; what the pack's own README says about its session is quoted.

**EGRESS DISCLOSURE:** two acts left the estate, both under step 1 of the verbatim instruction and both credential-free: a
`git clone` of the public repo, and the unauthenticated discovery handshake (C). No Opal data, no security name and no
Bloomberg-derived content was sent anywhere. No vendor data API was called.

---

## 1. THE FINDING FIRST: the plugin is FILES, not ACCESS -- and the LLY pack was built WITHOUT the connectors

1. **"The plugin" is a public GitHub marketplace of markdown and JSON** (Apache-2.0): agent system prompts, skills, slash
   commands, and a list of twelve vendor MCP server URLs. It ships no data and no credential. `claude plugin marketplace add
   anthropics/financial-services` puts it on a box; nothing about that call reaches a vendor.
2. **Every one of the twelve data connectors is a remote MCP server behind OAuth 2.1 against the VENDOR's authorization
   server** (C, 12 of 12). Access = a subscription with that vendor + a per-user browser login. The plugin cannot "secure"
   access; only an account can.
3. **The LLY pack used none of them.** Its README, verbatim: *"The institutional connectors configured in this environment
   (FactSet, Daloopa, S&P Global, Morningstar, BlackRock, Addepar, iCapital, Orion, Tamarac) require OAuth authorisation that
   could not be completed in a non-interactive session; Vanguard Advisor Tools, Definite and Zocks failed to connect."* and
   *"Built entirely from public sources."* SOURCES.md then names them: SEC EDGAR (six filings, archived in `01_filings/`),
   third-party transcript renderings (Globe and Mail, Seeking Alpha, StockAnalysis, AlphaStreet, GuruFocus), StockAnalysis.com
   for every price/multiple/margin figure, Fintel/HoldingsChannel/VCP Scanner/WallStreetZen for 13F and short interest,
   Benzinga/ChartMill/MarketBeat/Yahoo for targets, and press for consensus (two conflicting Q2 EPS figures, both carried).
   **So the "API access to all this information" is, on this pack, the model's web-search and web-fetch tools plus EDGAR.**
4. **At the vintage cloned, the core plugin's connector manifest does not parse.** `plugins/vertical-plugins/financial-analysis/.mcp.json`
   @574ed36 is missing the comma before `"box"` and one closing brace (`json.loads` -> *Expecting ',' delimiter: line 47*);
   the two partner manifests parse. A Claude Code install from that commit registers zero of the twelve core connectors and
   says nothing. (Whether the 2026-09-21 commit introduced it was not bisected; the file's last touch is that commit.)

Everything below is the anatomy behind those four sentences.

---

## 2. THE MARKETPLACE, PART BY PART (A)

**Surfaces it targets** (README + the 2026-05-05 announcement): Claude **Cowork** (Settings -> Plugins -> add marketplace from
GitHub), **Claude Code** (`claude plugin ...`), **Claude Managed Agents** (`scripts/deploy-managed-agent.sh <agent>` posts the
cookbook to `/v1/agents`), and the **Microsoft 365 add-in** (Excel/PowerPoint/Word/Outlook; its installer is the 19th plugin).
Paid plan required for Cowork/Code; connectors "may require a separate subscription or API key from the respective provider".

| layer | what it is | where | measured @574ed36 |
|---|---|---|---|
| marketplace | `claude-for-financial-services`, the install namespace (`<plugin>@claude-for-financial-services`) | `.claude-plugin/marketplace.json` | 19 entries |
| agent plugins | one self-contained plugin per named agent: `agents/<slug>.md` (system prompt) + bundled skill copies | `plugins/agent-plugins/` | 10: earnings-reviewer, gl-reconciler, kyc-screener, market-researcher, meeting-prep-agent, model-builder, month-end-closer, pitch-agent, statement-auditor, valuation-reviewer |
| vertical plugins | skill SOURCES + slash commands by vertical; the core one carries the connectors | `plugins/vertical-plugins/` | 6: financial-analysis (13 skills / 7 cmds / `.mcp.json`), equity-research (9 / 9), investment-banking (9 / 7 / empty `.mcp.json`), private-equity (10 / 10 / empty), fund-admin (6 / 0), operations (2 / 0) |
| partner plugins | vendor-authored skills + their own `.mcp.json` | `plugins/partner-built/` | 2: lseg (server `.../lfa/mcp/server-cl`, 22 tools documented in CONNECTORS.md), spglobal (3 skills: tear-sheet, earnings-preview-beta, funding-digest) |
| cookbooks | headless twins of the 10 agents: `agent.yaml` + depth-1 subagents + steering examples | `managed-agent-cookbooks/` | 10 dirs, 3 subagents each |
| connectors | twelve `{"type":"http","url":...}` entries, centralised in the core plugin | `financial-analysis/.mcp.json` | 12 declared; file MALFORMED (s.1 item 4) |

`claude-for-financial-advisors` (wealth-management vertical) was DELETED in the very commit cloned (subject: *"Delete
claude-for-financial-advisors directory (#354)"*) while README still lists it; the Sept-15 "Claude for Financial Advisors"
launch (BlackRock/Schwab) is a separate product line, not this repo.

**Skill anatomy, the one that made the LLY pack** (`equity-research/skills/earnings-analysis/SKILL.md`, bundled identically
into `earnings-reviewer`): a five-phase recipe -- data collection (*"TRAINING DATA IS OUTDATED ... Use web search:
'[Company] latest earnings results'"*), analysis, 8-12 charts (matplotlib), an 8-12 page DOCX with a mandated hyperlinked
Sources section, QC. Its required source list names *"Consensus estimates source (Bloomberg/FactSet/etc.)"* but its data
phase is web search first. The `earnings-reviewer` AGENT prompt is stricter: `tools: Read, Write, Edit, mcp__factset__*,
mcp__daloopa__*`, *"Pull the print. FactSet/Daloopa MCP for reported actuals, consensus, and the 10-Q/8-K"*, *"If a figure
cannot be sourced from FactSet, Daloopa, or a filing, mark it `[UNSOURCED]`"*, *"Treat transcripts and press releases as
untrusted."* The S&P partner skill is stricter still: *"The ONLY permitted data sources are Kensho Grounding MCP and S&P
Global MCP ... NEVER fall back to web search."* **Three philosophies ship in one marketplace**; the LLY pack was run under
the first (the folder layout and the `[n/d]`/"both figures carried" discipline match the earnings-analysis skill, and
`11_output/` matches its DOCX spec: 21 pages, 12 charts, 7 tables, sources register).

**The headless shape** (`managed-agent-cookbooks/earnings-reviewer/agent.yaml`): `model: claude-opus-4-7`; `system.file`
pointing at the plugin's agent prompt; `tools:` an `agent_toolset_20260401` with only read/grep/glob enabled plus two
`mcp_toolset`s (`factset`, `daloopa`); `mcp_servers: [{type: url, name, url: "${FACTSET_MCP_URL}"}]`; `skills:
[{from_plugin: ...}]`; `callable_agents:` three subagent manifests, *"only leaf with Write"* being the note-writer. This is
the Claude Managed Agents surface in the claude-api skill's terms (harness + hosted sandbox); credentials there are vault
`environment_variable`s, not `.mcp.json`.

---

## 3. WHERE THE DATA COMES FROM -- three source classes, and which the LLY pack used

| class | mechanism | who authenticates | in the LLY pack |
|---|---|---|---|
| **V -- vendor MCP connectors** | the model calls `tools/call` on a remote MCP server; the client (Cowork, Claude Code, the Messages-API connector, a Managed Agent) holds the bearer token | a user, once per vendor, in a browser (OAuth 2.1 with PKCE; RFC 9728 metadata -> vendor auth server); Daloopa also documents an `X-API-KEY` header and a 24 h token endpoint; S&P's python client takes a refresh token or `client_id` + `private_key` | **0 of 9 configured connectors usable**; 3 more `ENDPOINT_NOT_FOUND` |
| **W -- the model's own web tools** | `web_search` / `web_fetch` (server tools) or the client's WebSearch/WebFetch; pages parsed by the model | nobody (public web) | **every market/consensus/ownership/target figure**; the transcript; the news |
| **P -- primary documents** | EDGAR fetched over HTTP and archived as-received; the model reads them | nobody | the six filings in `01_filings/` (5.77 MB), and every income-statement / balance-sheet / guidance figure in the data pack |

Class V is what Andrew described ("through that API they have access to all this information"). It exists, it is real, and
it is exactly what did NOT run for LLY. What the pack demonstrates is classes W + P at skill-level quality -- with the
skill's own disclosure discipline doing the work a vendor feed would otherwise do (two consensus figures carried; 13F flagged
five months stale; Q3-2025 marked derived; `n/d` where an aggregator could not be verified).

**The twelve connectors and their gates (C, summarised; the card has every header):**

| vendor | endpoint | auth server | note |
|---|---|---|---|
| Daloopa | `mcp.daloopa.com/server/mcp` | `mcp.daloopa.com` | fundamentals with filing citations; API-key path documented |
| Morningstar | `mcp.morningstar.com/mcp` | same host | scopes `openid email profile offline_access` |
| S&P Global (Kensho) | `kfinance.kensho.com/integrations/mcp` | `kfinance.kensho.com/integrations` | scope `kensho:app:kfinance`; requires the "LLM-ready API" subscription (S&P README) |
| FactSet | `mcp.factset.com/mcp` | `auth.factset.com` | scope `mcp`; bearer accepted in header or body |
| Moody's | `api.moodys.com/genai-ready-data/m1/mcp` | same path root | scopes incl. `claudeai`, `mdcapp` |
| MT Newswires | `vast-mcp.blueskyapi.com/mtnewswires` | a Cloud Run auth server | **404 at the declared path** |
| Aiera | `mcp-pub.aiera.com` | same host | transcripts/events |
| LSEG | `api.analytics.lseg.com/lfa/mcp` | `login.ciam.refinitiv.com` | 22 tools named in CONNECTORS.md |
| PitchBook | `premium.mcp.pitchbook.com/mcp` | `mcp.pitchbook.com` | private markets |
| Chronograph | `ai.chronograph.pe/mcp` | not published (no RFC 9728 metadata) | PE portfolio monitoring |
| Egnyte | `mcp-server.egnyte.com/mcp` | `mcp-oauth.egnyte.com` | document store |
| Box | `mcp.box.com` | `api.box.com` | document store |

The 2026-05-05 announcement adds connectors NOT in this repo's manifest (Dun & Bradstreet, Fiscal AI, Financial Modeling
Prep, Guidepoint, IBISWorld, SS&C Intralinks, Third Bridge, Verisk, MSCI) -- those live in Claude's connector directory
(Enterprise/Team admin), not in the plugin. Not measured here.

---

## 4. THE SHAPE ON THE WIRE -- three layers

### 4.1 Layer 1: the transport and the envelope (measured for the handshake; documented for the rest)

- **Vendor side:** MCP over Streamable HTTP. JSON-RPC 2.0: `initialize` -> `tools/list` -> `tools/call {name, arguments}`;
  a tool result is `{content: [{type: "text", text: ...} | {type: "resource", ...}], isError}`. Unauthenticated: HTTP 401 +
  `WWW-Authenticate: Bearer resource_metadata="<url>"` (measured on 7 of 12; the other 4 return a bare 401). Sessions carry
  `Mcp-Session-Id`. **The MCP connector supports tool calls ONLY** -- no prompts, no resources -- per the platform page.
- **Anthropic Messages API side (if Opal's own code calls the vendor through Claude):** beta header `mcp-client-2025-11-20`;
  request carries `mcp_servers: [{type: "url", url, name, authorization_token}]` AND `tools: [{type: "mcp_toolset",
  mcp_server_name, default_config: {enabled, defer_loading}, configs: {<tool>: {...}}}]` (both halves or a 400); the response
  carries `mcp_tool_use {id: "mcptoolu_...", name, server_name, input}` and `mcp_tool_result {tool_use_id, is_error,
  content: [...]}` blocks. Works in the Batches API at the same price. **Not covered by zero-data-retention.** The API
  consumer *"is expected to handle the OAuth flow and obtain the access token prior to making the API call, and to refresh
  the token as needed"* -- i.e. the token lifecycle is ours.
- **Claude Code / Cowork side:** `.mcp.json` `{"mcpServers": {"<name>": {"type": "http", "url": ...}}}`; the client runs the
  OAuth flow interactively and stores the token per user; the model sees tools as `mcp__<server>__<tool>` (the agent prompt's
  `mcp__factset__*` grant is that namespace).

### 4.2 Layer 2: the vendor record (public docs only -- `[BODY-NOT-CAPTURED]` for live bodies)

- **Daloopa** (the one vendor with a public field list, `GET /v3/companies/{id}/fundamentals`): a datapoint is `{id,
  series_id, document_id, label, title, category, value_raw, value_normalized, unit, original_unit, conversion_factor,
  calendar_period, fiscal_period, span, fiscal_date, filing_type, document_type, filing_date, document_released_at,
  restated, created_at, updated_at, derived_components}`; sections `INCOME_STATEMENT | BALANCE_SHEET | CASH_FLOW_STATEMENT |
  KPIS | GUIDANCE | SEGMENTAL_INFORMATION | GEOGRAPHICAL_INFORMATION | GAAP_TO_NON_GAAP | ...`; periods `YYYYQn | YYYYHn |
  YYYYFY`, fiscal vs calendar both carried. **This is the closest published analogue to our model block's typed row
  `(security_key, fiscal_year, mnemonic)` -- with a per-figure filing citation, which ours lacks.**
- **S&P Global kfinance** (tool names from the partner skill; shapes not published on the pages read): `get_info_from_identifiers`,
  `get_company_summary_from_identifiers`, `get_latest`, `get_next_earnings_from_identifiers`, `get_earnings_from_identifiers`,
  `get_latest_earnings_from_identifiers`, `get_transcript_from_key_dev_id`, `get_competitors_from_identifiers
  (competitor_source="all")`, `get_prices_from_identifiers (periodicity="day")`, `get_financial_line_item_from_identifiers
  (line_item, period_type="quarterly", num_periods)`, `get_capitalization_from_identifiers (capitalization="market_cap")`,
  `get_consensus_estimates_from_identifiers (period_type, num_periods_forward)`. The skill's rules reveal the grain: fiscal
  quarter labels come from the earnings-call name; NTM EPS = the sum of the next four quarterly consensus means; LTM = the
  last four reported quarters.
- **LSEG LFA** (CONNECTORS.md): the four tools that matter for a single-name page -- `qa_ibes_consensus` (EPS/revenue/EBITDA/DPS
  with analyst count, dispersion, high/low), `qa_company_fundamentals`, `qa_historical_equity_price` (OHLCV, total return,
  beta), `tscc_historical_pricing_summaries` -- plus 18 rates/FX/credit/options tools irrelevant to RESAPP.
- FactSet, Morningstar, Moody's, PitchBook, Aiera, Chronograph, MT Newswires, Egnyte, Box: **no tool catalogue in the repo
  and none read from public docs** -- unmeasured.

### 4.3 Layer 3: what the skill EMITS -- the pack's own files (B, measured)

```
  2026Q2/LLY/                       58 files, compiled 2026-09-18; Opal-branded outputs added 2026-09-19 01:3xZ
    README.md                       folder map, the quarter in one table, 8 conclusions, "Data availability -- what could not be obtained"
    SOURCES.md                      five source tiers, per-figure derivations, "Institutional data sources NOT available for this pack"
    01_filings/      6 .htm         8-K x3 (Q4-25, Q1-26, Q2-26), 10-Q Q2-26, 10-K FY25, DEF 14A 2026 -- EDGAR bytes as received
    02_transcript/   1 .md          call notes: participants, prepared remarks, CFO table, pricing disclosure, Q&A (NOT verbatim)
    03_financials/   1 .xlsx        8 sheets: Summary | Income Statement | Non-GAAP Bridge | Revenue Detail | Balance Sheet & Cash Flow |
                                    Guidance | Quarterly Series | Ownership & Short Interest -- row 2 of every sheet is its source filing;
                                    values are STRINGS ('22974', '0.4766...'), not typed numbers
    04_market_data/  1 .md          price, multiples (trailing/guidance/ex-IPR&D/NTM), profitability, capital structure -- StockAnalysis
    05_ownership_short/ 1 .md       13F top holders (Q1-26, 3 of 10 with counts, 7 n/d), short interest, register structure
    06_supply_chain/ 1 .md          manufacturing footprint, capex, tariff/onshoring, DISCLOSURE GAPS named
    07_analyst_sentiment/ 1 .md     targets (avg/high/low/3m change), FY27 EPS revision (+6.2%/90d, 13 up 1 down), ratings actions, social (qualitative)
    08_dcf_model/    .xlsx + .md    DCF | Sensitivity | WACC; live formulas; author's assumptions on blue rows; memo
    09_peer_analysis/ .xlsx + .md + 5 png   Large-Cap Pharma (9 names x 23 cols: price, mkt cap, EV, P/E TTM/fwd, P/S, ...) | Obesity Franchise (asset table)
    10_company_specific/ 2 .md      catalyst calendar (dated events); idiosyncratic risk + governance (DEF 14A comp, pay ratio, auditor)
    11_output/       2 docx + 2 pdf + 12 png (+ Opal: 2 docx + 2 pdf + 13 png)
       LLY_2Q26_One_Pager_Opal.docx  53 paragraphs, 5 tables, 4 images: KPI tiles (revenue, vs consensus, non-GAAP EPS, EPS ex-IPR&D,
                                     gross margin, FY26 revenue) -> "The quarter" bullets -> "What decides the next twelve months" (dated)
                                     -> Valuation -> guidance tiles (prior vs updated) -> "Bottom line" -> Sources line
       LLY_2Q26_Earnings_Update_Opal.docx  215 paragraphs, 11 tables, 14 images: Position summary -> Headline results (Positives/Negatives)
                                     -> Results in detail (geographic, segment) -> Guidance, margins, cash -> ... -> sources register
```

Three properties of this emitted shape matter for brief 2: (i) **it is a per-(security, quarter) folder**, not a feed -- a
snapshot at a compilation date, with the compilation date and price stamped in every file; (ii) **every file carries its
source at the top** and the register separates reported / third-party / derived / author's-assumption -- the same
four-way split RESAPP's provenance face (FWD-3) and check face (FWD-10) exist to render; (iii) **the numbers are
web-sourced third-party numbers** (StockAnalysis, Fintel) wherever they are not filing numbers -- a different BASIS from the
Bloomberg basis the PRD binds (`C-BLOOMBERG-BASIS`), and the pack itself warns *"Peer forward P/E definitions vary by vendor
and may not be on a consistent fiscal basis."*

---

## 5. HOW ACCESS IS ACTUALLY OBTAINED -- the five paths (CAPABILITY; feasibility in brief 2)

| path | what "install" means | who holds the token | fits |
|---|---|---|---|
| P1 Claude Code plugin | `claude plugin marketplace add anthropics/financial-services` + `claude plugin install financial-analysis@claude-for-financial-services` (writes `~/.claude/plugins/`, USER scope on this shared box; every session then offers the OAuth prompts) | each user, per vendor, in a browser | an analyst's interactive session on their own machine |
| P2 Cowork | Claude Desktop -> Cowork -> Customize -> Browse plugins -> add marketplace from GitHub | same | Yang's path; the LLY pack |
| P3 Messages-API MCP connector | our code passes `mcp_servers` + `mcp_toolset` with an `authorization_token` we obtained and refresh ourselves | Opal, per vendor, stored in Secrets Manager | a pipeline that wants the MODEL to call the vendor |
| P4 Managed Agent | `deploy-managed-agent.sh earnings-reviewer` with vault credentials substituted at egress | Opal, in an Anthropic vault | a headless per-name run without our own loop |
| P5 vendor REST, no MCP | Daloopa `X-API-KEY`; kfinance `client_id + private_key`; LSEG/FactSet enterprise APIs | Opal service credentials | an ordinary harvest channel under H0-store, the MODEL never in the data path |

**The binding constraint on P1-P5 alike is a SUBSCRIPTION**, and that is Andrew's call, not a technical step. The estate
holds ONE paid single-name data entitlement this seat can see: the Bloomberg terminal (six bronze requests already land under
the harvest grammar, `refdata, histdata, histdata_daily_px, bestdata, identity, exec_officers` -- `bestdata` being BEst
consensus). Nothing in the plugin replaces it; the connectors would sit BESIDE it.

Nothing was installed on this box: P1 changes user-scope config for every seat sharing this Windows user and would raise
vendor OAuth prompts in every session; the cloned repo in the session scratchpad is the plugin's entire content and served
this study. Installing is a one-line act once Andrew says which surface he wants it on.

---

## 6. WHAT WAS NOT CAPTURED (the honest list)

- Any vendor `tools/list`, tool schema or live tool body (no token). The Kensho OpenAPI page and the Daloopa MCP tool list
  did not render through the fetch tool; their field lists above are from the pages that did.
- Yang Liu's session: which surface (Cowork is inferred from the README's "configured in this environment"), which model,
  cost, wall-clock. The pack stamps only compilation date/time.
- The Cowork UI and the Claude Enterprise connector directory (where the May-2026 connectors live).
- Whether Opal holds any vendor subscription; the Anthropic plan tier Yang used.
- The 2026-09-21 commit's diff (whether the malformed manifest is new or long-standing).
- The LSEG `server-cl` sibling endpoint (declared by the partner plugin, not probed).
