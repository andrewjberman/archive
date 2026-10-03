# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 6 -- deploy the five rivalfunds Lambdas at CLOUD, create the AI secret, republish 2026-10-02 ONCE; the vehicle runs the round-6 Bloomberg code from 2026-10-05

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~18:2xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).
**Why:** round 6's 14 cells are built, accepted and drained:
- issuance 1e8515aa01; every order is flipped complete (f1bd440feb);
- CLOUD rivalfunds suite: 527 passed, 2 skipped, 0 failed;
- round-6 checks: 43 of 43 PASS on the combined branch (rv-hookups6 @510566a0f8).

The judgment criteria (J1 of ap-1, r-6, ui-2, ui-3, ui-4 and ui-5) are graded by `3.0.0_SA_CVO~RV` on this act's real-run page.

## VERDICT: SIGNED

Conditions:
- the pin is CLOUD eb6e9f04ff (it holds the census repair f97a6bfff8 and CRO~RV's layout pass 31d2375993);
- every gate below reads as stated.

## THE ACT, IN ORDER

1. **NEVER-2 ledger entry opened** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-round6`), committed before step 3.
2. **The AI secret.**
   - `aws secretsmanager create-secret --name rivalfunds/openai-api-key`. The value is copied from the existing `openai-api-key`
     secret through a pipe and is never printed, written to disk or committed.
   - Measured before: no `rivalfunds/*` secret exists (list-secrets 18:0xZ: `openai-api-key` and six `opal/openai/*`).
   - A dedicated OpenAI project key is Andrew's act (the OpenAI console). This secret's name, ARN grant and Lambda
     environment then stay unchanged; only its value rotates.
3. **`safe-apply` of the saved plan.**
   - Plan `/c/tmp/rv_apply14.tfplan` from `/c/tmp/rv-fast` detached at the pin eb6e9f04ff, after
     `infra/aws/lambda/etfs-pipeline/rivalfunds_package.py` stages the build.
   - Probe plan 18:1xZ at 0fe2cd1556: **0 to add, 6 to change, 0 to destroy**:
     - five `aws_lambda_function.stage` source_code_hash changes;
     - the daily Lambda's new `environment {RIVALFUNDS_AI_ENABLE=1, RIVALFUNDS_OPENAI_SECRET=rivalfunds/openai-api-key}`;
     - the daily role's policy: `secretsmanager:GetSecretValue` on `...:secret:rivalfunds/openai-api-key-??????` ONLY, and
       `gold/research_hypotheses/*` moved from the read statement to the write statement (row Z-W1-S43).
   - No other role, Lambda or trigger changes.
4. **ONE real run:** `daily-lambda {"only":["publish-page"],"date":"2026-10-02","mode":"daily","batch_id":"rv-publish-1002r6",
   "sink":"s3","refresh_a1":true}`.
   - It runs in the daily Lambda, which carries the gate.
   - The AI stage finds the day's existing `research_hypotheses` object and returns SKIPPED_EXISTS (CALL 5: one AI run per
     page day). No vendor call happens today.
5. **The deliberate AI fire** (CVO~RV msg 28641 via CTO~Z msg 28643: no FWD is a wait):
   `daily-lambda {"only":["publish-page"],"date":"2026-09-30","mode":"daily","batch_id":"rv-ai-0930r6","sink":"s3"}`.
   - Page day 2026-09-30 holds no `research_hypotheses` object (s3 ls ~18:4xZ: only date=2026-10-01 and date=2026-10-02).
   - The scheduled path therefore runs ONE OpenAI account chain (VEW-2; CALL 5: one run per page day) and writes
     `gold/research_hypotheses/date=2026-09-30/`, through the PutObject grant P3 adds. It then republishes the 2026-09-30
     page once.
   - This is ap-1's positive arm, which J1 grades. Act 4 on 2026-10-02 is the negative arm (SKIPPED_EXISTS).
6. **The vehicle** (terminal machine, CLOUD working tree) runs the round-6 Bloomberg code at 07:00/08:03 ET 2026-10-05:
   - the holdings query `get(id(), name())` (RIV-nm-1, proved live 17:4xZ on 9 funds, 683/683 rows named and typed);
   - the dividend request `["DVD_HIST_ALL","DVD_CRNCY"]` (RIV-e-2; the minor-unit codes GBp/ZAr measured live 17:2xZ).

## THE SERVED DELTA, MEASURED THROUGH THE HANDLERS

Measured 18:0x-18:4xZ:
- each A1 producer's handler, and one overlay publish of 2026-10-02 with refresh_a1, run at the round-6 code (rv-hookups6
  @510566a0f8) over the SERVED inputs;
- S3 reads only, local writes, no Lambda invoked, no vendor call; evidence `C:/tmp/r6measure/` (`r6_a1run.py`, `r6_cmp.py`,
  `r6_page.py`, `r6_tables.py`, `r6_g5cmp.py` and their JSON).

A control at the deployed 722f0db291 code reproduces the served page except for 42 name cells (row below).

**Nothing the served page has is lost.** Per fund, 18 page features were compared (AI items, grades, panels, trade rows,
traces, ...), and none falls for any of the 13 funds.
- **The AI regression guard** (CRO~RV msg 28602): 12 of 12 funds show an account. The 24 items, 22 PASS / 2 FAIL (IDVZ,
  CGIC), are the same on both sides, and all 48 stored texts appear in the right card.

| A1 table | rows | rows changed | of which code-only | YTD fund totals |
|---|---|---|---|---|
| holding_contribution | 3,777 -> 3,777 | 881 | 824 (57 are name drift, below) | none of 13 moves |
| buying_trend | 319 -> 320 (SCHY Unclassified, rank NULL) | 93 | 76 | -- |
| input_census | 1,562 -> 1,562 | 1,141 | 1,141 | -- |

- **Refused rows** (rk-2): 0 of 3,777.
- **Unclassified** (sx-1): in holding_contribution, 36 ranked rows go to 0 ranked (47 rows kept); in buying_trend, 12
  ranked rows become 13 with rank NULL. 23 tables lose rows, and every lost row is the Unclassified bucket (17 ranking, 8
  trend).
- **Cross-fund GICS** (CRO~RV's Fix 1, in CLOUD): 43 YTD securities are newly classified (BIDD 4, CGIC 10, ETFT 8, INEQ 15,
  SCHY 3, TXUE 3). INEQ's unclassified share falls from 59.2% to 22.2%, so its sector panel now shows. Three sector rows
  change table (ETFT YTD Consumer Staples/Discretionary, Strongest -> Weakest; SCHY YTD Communication Services -> Utilities).
- **Census** (ic-2):
  - prices: 79 arrived / 684 missing -> 79 arrived / 642 covered_by_fallback (holding_implied) / 42 missing;
  - GICS: 79 / 684 -> 578 arrived (499 from the fund's own G1) / 185 missing;
  - holdings 9/4 and readings 23 unchanged.

| page | served (rv-publish-1002g) | round 6 |
|---|---|---|
| status / funds / trades | OK, 13 of 13, 213 | same |
| bytes (gateway cap 2,097,152) | 1,591,657 | 1,875,605 (+17.8%; 10.6% headroom) |
| grade badges / sources details / empty-state lines / refused panels | 0 / 0 / 0 / 0 | 24 / 36 / 10 / 0 |
| Unclassified footnotes / trend sparks / census reason groups / empty-run lines | 0 / 0 / 0 / 0 | 25 / 300 / 6 (231 items) / 12 (27 windows) |
| raw `<id> XX Equity` names (trade / ranking / trend cells) | 159 of 213 / 359 / 152 | same until G1 carries names (the 2026-10-05 vehicle run, P7) |

The measurement found three issues and named three non-blocking findings.

Fixed before this act:
- The census summary read "Security prices: 721 of 763 arrived", counting the 642 fallback-covered prices as arrived.
  render._census now counts each state (issuer repair f97a6bfff8, test added, suite 529 passed).

Watched and routed:
- **Page size.** The trend sparks are 320,789 bytes of the growth. A heavier day could cross the gateway cap, and the
  publish would then refuse and write nothing, so the prior page stays. Routed to 4.0.0_SA_CRO~RV, whose layout build adds
  modals on top.

Not in this act:
- G5 is not rebuilt by a publish. The three trims-to-zero x-1 prices (BIDD -516,071; INEQ -463,336; TXUE -7,669,245; sum
  -8,648,651) appear at the next G5 build. Income is unchanged on both pins (G6 7,398,581.19, 104 events).

Non-blocking findings:
- 57 + 17 name cells differ between the Lambda's build and a local run of the same deployed code: a same-date tie in the name
  pick. The pick predates round 6, and it is a row.
- 33 GICS rows read "missing" in the census though the rankings classify them (ETFT 9, PCLG 11, TSEL 9, WCMG 4). This is
  the census understating, not overstating, and it is a row for round 7.

The real act writes:
- `gold/{holding_contribution,buying_trend,input_census}/date=2026-10-02/` (+1 object each);
- `platinum/page/date=2026-10-02/{index.html,manifest.json}`, with the prior page under `revisions/<ts>/`;
- `state/publish_page/date=2026-10-02/<batch>.json`;
- act 5 writes P8.

No G5 or G6 object is written.

### AT THE PIN: CLOUD eb6e9f04ff (round 6 + the census repair fc022275b5 + CRO~RV's layout pass 31d2375993)

Andrew ~17:0xZ to 4.0.0_SA_CRO~RV (record `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20261002_17xxZ_RIVALFUNDS_LAYOUT_WALK_AND_BUILD.md`;
CRO~RV msg 28683: "it goes live at your next deploy"). The layout pass rides this deploy, so the page was measured again at the
pin, 19:1x-19:2xZ, with the same instruments (`r6_publish.py` overlay, `r6_page_pin.py` -> `C:/tmp/r6measure/page_compare_pin.json`).

| page at the pin | served | pin eb6e9f04ff |
|---|---|---|
| status / funds / trades | published, 13 of 13, 213 | published, 13 of 13, 213 |
| AI cards with an account (regression guard) | 12 of 12 | 12 of 12 (22 PASS / 2 FAIL badges, the same accounts) |
| per-fund feature DECREASES (18 features x 13 funds) | -- | **none** |
| bytes (cap 2,097,152) | 1,591,657 | 1,833,427 (12.6% headroom; the sparks are off the face, and holding dialogs drop above 1.95 MB) |
| holding dialogs / AI dialogs / count chips / census reason groups | 0 | 387 / 24 / 39 / 6 (231 items) |

- Suite at the pin: 535 passed, 2 skipped, 0 failed.
- Round-6 checks at the pin: **37 of 43 PASS.** The 6 that do not are Andrew's layout word superseding the cell's surface,
  and none is a loss against the served page:
  - ui-2.AC3: YTD is now the default period;
  - ui-3.AC1-AC3: the By-month trend is redesigned, with the months in the holding dialog;
  - ui-4.AC1 and AC3: the AI account sits under the group card, with a dialog for detail and citations.
- CRO~RV amended test_r6ui2/ui3/ui4 to the new layout and added test_crorv_layout.py. Those cells' J1 is graded by
  3.0.0_SA_CVO~RV on the new layout.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| P1 | five Lambdas `etfs-rivalfunds-*` / `rivalfunds-*` code | the 722f0db291 set | the CLOUD pin set | re-apply the 722f0db291 build (saved plan from a detached worktree at 722f0db291) |
| P2 | daily Lambda environment | none | AI gate + secret name | remove the block (re-apply 722f0db291's lambdas.tf); the gate unset makes the stage a no-op |
| P3 | daily role policy | 722f0db291's | + GetSecretValue (one ARN), research_hypotheses read -> write | re-apply 722f0db291's generated policy |
| P4 | secret `rivalfunds/openai-api-key` | absent | created | `delete-secret --recovery-window-in-days 7` (human-confirmed) |
| P5 | gold A1 tables + G5 + census, date=2026-10-02 | rv-publish-1002g's objects | + one new object each (newest wins) | prior objects stay; removing the new ones is an S3 delete (human-confirmed) |
| P6 | platinum page 2026-10-02 | rv-publish-1002g | republished ONCE, batch rv-publish-1002r6 | prior page kept under `revisions/<ts>/` |
| P8 | gold research_hypotheses date=2026-09-30 + platinum page 2026-09-30 | absent; page 09-30 from its last publish | one account object (run rv-ai-0930r6); page republished ONCE | the account object stays (append-only; removing it is an S3 delete, human-confirmed); prior page kept under `revisions/<ts>/` |
| P7 | vehicle Bloomberg request (2026-10-05) | `get(id())`; `DVD_HIST_ALL` | `get(id(), name())`; `+DVD_CRNCY` | revert the two files in CLOUD before 07:00 ET |

## GATES (before step 3)

1. Nothing in flight on any rivalfunds Lambda (10 min of logs).
2. The deployed CodeSha256 equal the 722f0db291 set (the before state).
3. The saved plan reads 0/6/0 with exactly the hunks above.
4. The secret exists, and its value's length is non-zero (`describe-secret` plus a length-only read; the value is never printed).

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied:** the CodeSha256 values equal the plan's hashes. The page republishes with the round-6 render:
  - 12 funds keep their AI account: the A1_TABLES shadow (CRO~RV msg 28602) is fixed and guarded by a test;
  - census states are counted;
  - Unclassified is never ranked;
  - names come through display_name;
  - exits are priced.

  On the 2026-10-02 republish (act 4), `research_hypotheses_run` reads SKIPPED_EXISTS. Act 5 writes ONE account object for
  2026-09-30 through the scheduled path (run_path "scheduled", grounding_check/5, prompt a1-chain/5). Its run status, its
  per-fund grades and the 09-30 page are read back and handed to 3.0.0_SA_CVO~RV for ap-1's and r-6's J1. A FAIL account
  is shown, never re-rolled (CALL 5). The 2026-10-05 09:00 ET sweep is the first unattended scheduled account.
- **Not applied** (any gate fails): the served stack stays at 722f0db291. The vehicle still runs the CLOUD tree on 2026-10-05,
  so P7 happens anyway: its two files are proved live and offline. **P7 depends on P1.**
  - The vehicle's new `get(id(), name())` capture lands in bronze.
  - Silver is built by `rivalfunds-build-silver-lambda`, and the 722f0db291 silver code REFUSES the two-field header
    ("header lacks ORIG_IDS"; the issuer's probe at 16:47Z).
  - So if the Lambdas are not at the pin by 2026-10-05 06:00 ET, the issuer reverts P7's two files in CLOUD.

  The AI secret (P4) must exist before the 2026-10-05 09:00 ET sweep. Without it the stage returns FAILED, which is
  recorded in the manifest, and the page still publishes.
