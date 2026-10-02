# ETFS_RIVALS -- DECOMPOSITION, ROUND 6 (ENRICHMENT) -- DRAFT: the AI accounts in production, the A1 plausibility guard, dividend currency and child identity, one repair cell; the backfills and the G4 price history as issuer acts

```json
{
 "project": "ETFS_RIVALS",
 "round": 6,
 "prd_ref": "org/missions/D5/ETFS/ETFS_RIVALS/prd/ETFS_RIVALS_PRD.md (v0.11 @f62abbafc5; ADMITTED @bd166222b0, ratified-text half 3.0.0_SA_CVO~RV)",
 "prd_version": "v0.11",
 "analysis_ref": "org/missions/D5/ETFS/ETFS_RIVALS/ledger/ROUND_ANALYSIS.round5.md@56c99763bb (section 4)",
 "author": "2.0.0_SA_COO~RV",
 "cells": 4,
 "issuer_acts": 3,
 "chains": 3,
 "join_cells": 1,
 "frozen": false,
 "status": "DRAFT -- written under the FAST lease (to 17:08:53Z); cut as ONE issuance at the FAST -> FULL boundary, every check dry-run at the base first"
}
```

**Issuer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~14:3xZ (draft).
**Source:** the round-5 analysis section 4 (cells 1-7, CTO~Z msg 28485). Also binding:
- CRO~RV CALL 13 (@6e3c94774a): C1 amended for cell 2; C2 as this round's L5 rule;
- `org/ref/VENDOR_EGRESS_WHITELIST.yaml` VEW-2 (OpenAI, the rivalfunds AI chain only);
- Andrew-direct 13:33Z (@74e6e01a5b).

**Input state (2026-10-02 14:2xZ):**
- Lambdas at CLOUD 722f0db291 + the publish-page bronze-read grant (r12, r13 CLOSED).
- The served 10-02 page is fast-a1-publish-1002f, 13 of 13.
- The vehicle runs round 5's code from the CLOUD tree from 2026-10-05 07:00 ET.
- Cell 6 of the analysis (PFOE's source URLs) is DONE under FAST (addendum 12; CTO~Z: dropped).

## Issuer rulings at this cut

1. **Cut by write set; three worker chains, one join cell, three issuer acts.** Fan-out: 3 of 3 chains at issuance, cap 8.
   The join starts when both of its parents are terminal.
   - `~1` ap-1 (`ai_accounts.py`, `sweep.py`, `gen_policies.py`, `policies/*.json`, `main.tf`).
   - `~2` rk-2 (`gold_holding_contribution.py`, `guardrails_config.json`, `render.py`).
   - `~3` e-2 (`enrichment_bloomberg.py`, `gold_trade_schedule.py`).
   - JOIN r-6 after ap-1 and rk-2: it writes `ai_accounts.py` and `render.py`.
2. **Workers never call a vendor, never write S3, never deploy** (rounds 1-5 stand). Every Bloomberg or OpenAI act, every S3
   write and every deploy in this round is the issuer's: the acts I-1 to I-3, each deploy under its own never-widen pair, and
   the vehicle-run drains after a morning read, as in round 5.
3. **Cell 7's premise is corrected by a measurement, not the analysis's words (S14).**
   - G4 DOES carry prices now. `security_market` date=2026-09-29 holds a newer object with `px_close` on 430 of 434 rows, and
     S14's 0-of-172 read the older object. Date=2026-10-01 has 32 of 32.
   - The gap is HISTORY: rk-1 read ONE G4 date (10-02 manifest: `g4_dates` 1; `price_source` holding_implied 1849 / missing
     1498).
   - The code is already there. `gold_holding_contribution.handler_entry` reads every G4 date in the window
     (`_newest_by_date` over `security_market`) and `build` prices a day from `px_close`. The market pull answers a past date
     through `_blp_historical_data`, labelled per s-6.
   - Cell 7 is therefore NO worker cell. It is issuer act I-3: the historical market pull over the YTD window, within the
     Bloomberg budget (`integrations/bloomberg/READ_HERE.md`), with cost measured first.
4. **The AI client in the Lambda uses `requests`, which the layer already carries** (`pandas-pyarrow-requests`, main.tf:93),
   against the OpenAI REST API: build-ladder rung 5, so no `openai` SDK is vendored. The seat path keeps `OpenAIClient`.
5. **One AI run per page day stands (CALL 5).** The production stage is idempotent on its own marker per page day, a
   grounding FAIL is shown and never re-rolled, and the key is read at runtime from the DEDICATED secret, never persisted.
6. **CALL 13 C2 is this round's L5 rule:** every judgment criterion names its positive control.
7. **Every check is issuer-written and dry-run at the base before the cut.** Each FAILs there for the defect it names, and
   its controls PASS there.

## Rulings reaching every cell

Rounds 1-5's rulings stand (`ETFS_RIVALS_DECOMP.round{1..5}.md`):
- builder-only addresses (`homes.address`, `lib/opal_naming.py`);
- markers;
- one revision contract;
- per-source floors through `guardrails.load_config()`;
- the Positioning pull read-only;
- column-optional readers;
- the A1 contracts of amendment A1.

## 3. THE CELLS

### `RIV-ap-1` -- the AI accounts as a production stage (analysis cell 1; WORLD at its deploy)
- `publish_page.handler_entry`, after `produce_a1` and before `load_a1`, calls `ai_accounts.run_day(day, sink,
  client=ai_accounts.default_client(), provenance={"run_path": "scheduled", ...})` when `RIVALFUNDS_AI_ENABLE == "1"` and the
  page day holds no `research_hypotheses` object. That makes one run per page day (CALL 5), and a FAIL is shown, never
  re-rolled.
- Only the daily Lambda carries the gate, so the run lands at the 09:00 ET sweep. The 07:00 marker-driven publish
  (publish-page Lambda) never calls the vendor.
- `ai_accounts.RestClient(api_key)`: `requests`, already in the layer, POSTs chat completions (model, messages,
  `response_format` json_object, temperature 0.2). `default_client()` returns a RestClient built from the secret's
  `api_key`, read at call time. Web search stays unavailable in the Lambda (VEW-2: a fallback only; internal readings first).
- The dedicated secret is named by `name()` (an LGIC registry row is added if the builder refuses). `gen_policies.py`
  grants `secretsmanager:GetSecretValue` on that ONE ARN to the daily role alone. The generated `lambdas` map gives the daily
  Lambda an `environment` {RIVALFUNDS_AI_ENABLE: "1", RIVALFUNDS_OPENAI_SECRET: <name>}, which `main.tf` reads.
- The secret's VALUE is set by the issuer at the deploy, never by a worker. Tests stub the transport.

### `RIV-rk-2` -- the A1 plausibility guard (analysis cell 2; CRO~RV CALL 13 C1 as amended)
- `gold_holding_contribution.plausibility_guard(df, bounds=None) -> df`, applied in `handler_entry` before the write.
- Per fund x period, never the table, the security rows give way to ONE row: axis "refused", bucket = the bound, contribution
  = the offending value.
  - (a) a total below -100% -> `total_below_minus_100pct` (hard), checked first;
  - (b) one holding with |c| above `contribution_single_holding_bound` (guardrails_config.json, 0.25, PROVISIONAL) ->
    `single_holding_above_bound`;
  - (c) NAV reconciliation where a NAV is on file, its tolerance from the residual distribution (PROVISIONAL; no NAV is on
    file today, so (c) ships as a documented no-op hook).
- `render._rank_panel` shows "Rankings refused" with the bound, marked `data-refused="<bucket>"`, in place of the panel.
- Measured at 14:2xZ: the served 10-01 and 10-02 tables refuse nothing (lowest total -4.9%, largest holding 3.6%).

### `RIV-e-2` -- dividend currency and child identity (analysis cell 5; W3-S11, W3-S12)
- `DVD_CRNCY` joins the dividend request: the plan mode's `fields` list it beside `DVD_HIST_ALL`.
- `rows_from_responses` fills G3 `currency` from a security's `DVD_CRNCY`, NULL when absent.
- `gold_trade_schedule.dividend_ccy(security_key, g3_currency) -> (ccy, source)`: the G3 currency wins ("g3"); otherwise
  the suffix table answers, labelled "suffix_table", with the mixed-unit LN/SJ/IT rule unchanged. G5's income conversion
  uses it.
- W3-S12 (child identity) is code only after issuer probe I-2 names a field; until then the child line keeps its "entry"
  label.

### `RIV-r-6` -- the repair cell (remediations batched; JOIN after ap-1 and rk-2)
- (1) An absence sentence reads as a sentence: the reason after "No AI account." (and "Input census not available.")
  starts with a capital letter.
- (2) grounding_check/5: a digit run INSIDE a market reading's own name, quoted in the text (a trending-topic headline,
  "... 20 Years ..."), is not a figure. The run-time grade gets the names from the readings; the publish recheck gets them
  from the row's `input_vintages` keys. A bare number outside the name still fails.
- (3) Prompt a1-chain/5 names a security by its name, not its Bloomberg ticker form (CALL 10 style). JUDGMENT.
- Dropped from the remediations, measured: the census lists are already collapsed in `<details>` (render `_census`).

## ISSUER ACTS (no worker; each WORLD under its own pair)

- **I-1 (analysis cell 3): W4-S9's disarm.**
  - ONE deliberate marker batch above 45 dates against the deployed Lambda.
  - The first backfill batch is the carrier.
  - Proof: the G1 cursor continues across invocations and the batch's marker lands (b-2's bound).
- **I-2 (analysis cells 4 and 5): the backfills and the probe.**
  - IDVZ, PFOE, ACWI, IWM, after the v0.8 leg's request-cost measurement and the ACWI/IWM G9 style-read preview (CVO~Z's
    condition). The gate `RIVALFUNDS_LEG_ENABLE=1` is set, and the IDVZ/PFOE `home_producer` read retires.
  - The G5/G6 replay runs under its own never-widen pair.
  - The W3-S12 Bloomberg field probe.
- **I-3 (analysis cell 7): the G4 price history.**
  - The existing market pull's historical path over the YTD window's trading days, within the Bloomberg budget.
  - Cost measured first per READ_HERE.md.
  - Proof: a republish's `holding_contribution` manifest reads `g4_dates` above 1, and the security rows priced from G4
    (`price_source` g4_tri / g4_close, or mixed) rise from 0 while `holding_implied` falls.

## 4. DEPENDENCY EDGES AND CHAINS

| cell(s) | writes | after |
|---|---|---|
| ap-1 (`~1`) | `ai_accounts.py`, `sweep.py`, `gen_policies.py`, `policies/*.json`, `main.tf` | -- |
| rk-2 (`~2`) | `gold_holding_contribution.py`, `guardrails_config.json`, `render.py` | -- |
| e-2 (`~3`) | `enrichment_bloomberg.py`, `gold_trade_schedule.py` | -- |
| r-6 (join) | `ai_accounts.py`, `render.py`, `gold_input_census.py` | ap-1, rk-2 |

## 5. BATTERY -- issuer-written, DRY-RUN AT THE BASE (CLOUD 722f0db291+, 2026-10-02 ~14:5xZ): every check FAILS there for its defect

Checks: `deliverables/2.0.0_SA_COO~RV/round6/checks/` (shared `_common.py` re-exports round 5's fixtures). At most THREE
mechanical criteria per build order:

| order | AC | invocation | at base |
|---|---|---|---|
| ap-1 | AC1 | `python checks/ap-1.AC1.py` -- publish with the gate: one research_hypotheses object, the second publish calls nothing | FAIL (0 objects); control (gate off) OK |
| ap-1 | AC2 | `python checks/ap-1.AC2.py` -- RestClient's request; default_client from the named secret | FAIL (no RestClient) |
| ap-1 | AC3 | `python checks/ap-1.AC3.py` -- GetSecretValue on one ARN, daily role only; the gate and secret name on the daily Lambda only | FAIL |
| rk-2 | AC1 | `python checks/rk-2.AC1.py` -- planted -188% refuses (a); TXUE untouched; the served 10-02 table refuses nothing (S3 READ-ONLY) | FAIL (no guard) |
| rk-2 | AC2 | `python checks/rk-2.AC2.py` -- the 0.25 PROVISIONAL bound in config; 0.31 refuses (b), 0.24 passes | FAIL |
| rk-2 | AC3 | `python checks/rk-2.AC3.py` -- the page shows "Rankings refused" with `data-refused`, no table; control renders | FAIL |
| e-2 | AC1 | `python checks/e-2.AC1.py` -- the plan's fields list DVD_CRNCY | FAIL; control (DVD_HIST_ALL) OK |
| e-2 | AC2 | `python checks/e-2.AC2.py` -- G3 currency from DVD_CRNCY; NULL without it | FAIL; control OK |
| e-2 | AC3 | `python checks/e-2.AC3.py` -- dividend_ccy: g3 wins, suffix_table labelled, the LN base rule kept | FAIL (no function) |
| r-6 | AC1 | `python checks/r-6.AC1.py` -- the absence sentences start with a capital | FAIL |
| r-6 | AC2 | `python checks/r-6.AC2.py` -- a quoted headline's digits pass at the recheck AND at run time; a bare 20 fails | FAIL; control OK |

JUDGMENT, graded at L9, each with its positive control (CALL 13 C2):
- ap-1: the first scheduled account reads as well as a seat run's; positive control: the 10-02 accounts, run
  20261002T110438Z-ai-rg4.
- r-6 (3): the next run names securities by name; positive control: a 10-02 account's ticker forms (e.g. TXUE's "ORA FP
  Equity").
