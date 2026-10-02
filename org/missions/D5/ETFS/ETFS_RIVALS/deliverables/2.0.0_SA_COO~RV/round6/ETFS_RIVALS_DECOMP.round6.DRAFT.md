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
- A DAG stage `ai-accounts` after the A1 producers and before `publish-page`. It is idempotent on a marker per page day
  (CALL 5: one run per page day).
- It calls `ai_accounts.run_day` with a `requests`-based client (`RestClient`: chat completions; `web_search` left
  unavailable, since VEW-2 names web search a fallback only, and internal readings come first).
- The key is read at runtime from a dedicated secret named by `name()` (an LGIC registry row added if the builder refuses).
- `gen_policies.py` grants `secretsmanager:GetSecretValue` on that ARN only, to the daily role.
- `main.tf` sets `RIVALFUNDS_AI_ENABLE=1` and `RIVALFUNDS_OPENAI_SECRET` on the daily Lambda alone.
- The secret's VALUE is set by the issuer (I-act at the deploy), never by a worker.
- Tests stub the transport.

### `RIV-rk-2` -- the A1 plausibility guard (analysis cell 2; CRO~RV CALL 13 C1 as amended)
- Refusal is per fund x period, never the table:
  - (a) a period total below -100% refuses (hard), and a planted -188% refuses;
  - (b) a single holding with |c| > 0.25 refuses (PROVISIONAL, `guardrails_config.json`);
  - (c) NAV reconciliation where a NAV is on file, with its tolerance from the residual distribution (PROVISIONAL).
- A refused fund x period writes one row naming the bound it failed, and the page shows the refusal in place of the panel.

### `RIV-e-2` -- dividend currency and child identity (analysis cell 5; W3-S11, W3-S12)
- `DVD_CRNCY` joins the enrichment request inside the worded rivalfunds pull (W3-S11).
- G5 converts dividends by it and drops the exchange-suffix table (`SUFFIX_CCY`, `MIXED_UNIT_SUFFIX`) where it is present;
  the suffix table stays the fallback, labelled.
- W3-S12 is code only after issuer probe I-2 names a field. Until then the child line keeps its "entry" label.

### `RIV-r-6` -- the repair cell (remediations batched; JOIN after ap-1 and rk-2)
- The AI placeholder "No AI account. the ..." capitalised.
- A trending-topic headline's own digits are not read as figures. They are identifiers of the reading, like ticker forms
  (grounding_check/5).
- The census renders as counts with the 766-line lists collapsed.
- The prompt names securities by name, not ticker form (CALL 10 style; prompt a1-chain/5).

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

## 5. BATTERY (to write and dry-run at the base before the cut; at most THREE mechanical criteria per build order)

- ap-1:
  - (1) the DAG runs `ai-accounts` once per page day: a second invocation is a no-op on its marker;
  - (2) `RestClient` builds the documented request with a stubbed transport and reads the key from the named secret only;
  - (3) the generated policy grants GetSecretValue on the one ARN to the daily role alone.
  - JUDGMENT: a production-run account reads as well as the seat run's, against the 10-02 accounts as the positive control.
- rk-2:
  - (1) a planted -188% fund x period refuses, and the 10-02 tables refuse nothing else;
  - (2) |c| > 0.25 refuses at the provisional bound;
  - (3) the page shows the refusal reason in place of the panel.
- e-2:
  - (1) `DVD_CRNCY` is in the request's field list;
  - (2) G5 converts by it, with the suffix table as the labelled fallback;
  - (3) a stubbed child-identity field (if I-2 names one) ties the child to the parent.
- r-6: the four repairs each have a named before/after string on the served page's overlay.
