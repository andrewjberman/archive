# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 31 (RIV-ya-1, RIV-yb-1) -- four modules to the rivalfunds stack, packages only

**Signer:** `2.0.0_SA_COO~RV` (dell1), 2026-10-15 ~22:0xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (asked).
**Why a deploy:** both cells are `LOCAL` and merged (RIV-ya-1 @a84447b8c0, RIV-yb-1 @17da2c6e4b). Andrew ruled round 31 ("Call bbd5: yes fix only round now") and, at this seat's terminal, the model move
("updated from 5.4 to 6", "gpt 6 astra"; record `org/tier1_exec/2.0.0_SA_COO~RV/deliverables/ANDREW_DIRECT_20261015_20xxZ_RIVALFUNDS_AI_MODEL_TO_GPT_6_ASTRA.md` @df2ca8f0a9). Neither takes effect until the packages move;
row `ETFS_RIVALS-D1-S16` (ARMED) disarms only when ya-1 is deployed, and the CVO's J1 read of yb-1 is a read of the first sweep after it.
**Applier:** `0.7.0_AE_CloudOps~DELL1`, on a task order from this seat after both halves are signed.

## VERDICT: SIGNED

Conditions:
1. **Pin: `34b2ab6351`** (scratch branch `pin-ETFS_RIVALS-r31`, author `2.0.0_SA_COO~RV`). It is the last applied pin `ea0e5025ac` (round 30) plus exactly four files at the merged HEAD's bytes:
   `gold_trade_schedule.py` blob `928331c8de7fde907d1cdf7a66f42a4be95ac51a` and `price_series.py` `4c932a816434a702648f13da0c6530d02e11d3fa` (RIV-ya-1), `ai_accounts.py`
   `917e2fa12e0b2cde80d4d29d7ab864d1a9ef9fb6` and `ai_client.py` `2b45ec0ac8c423ae6801c1370b8045f26fa52941` (RIV-yb-1); `render.py` stays `fda4ab160bb72d1f6e5b20ddf3a9df37997354fa` and `dramatic_move.py` `37397a1057439b90aa2a9b759beb159375e91673`.
   `git diff --stat ea0e5025ac 34b2ab6351`: 4 files, +61 -7. **It is NOT HEAD:** HEAD also carries RIV-xe-1 (`enrichment_bloomberg.py`) and RIV-xf-1 (`peer_groups.json`, `bbg_budget.json`), which are site Z's producer deploy under `1.0.0_SA_CTO~Z`'s half
   and ship nowhere here. A later commit stands only where its STAGED paths (`infra/aws/lambda/etfs-pipeline/rivalfunds_package.py`, `infra/aws/lambda/etfs-pipeline/` and `infra/aws/terraform/etfs-rivalfunds/`) are byte-equal to the pin's, tests left out.
2. **Plan.** 0 to add, **5 to change, 0 to destroy**: the five `aws_lambda_function.stage` code packages, attributes `source_code_hash` and `last_modified` only. No environment key (in particular **no `RIVALFUNDS_AI_MODEL`**: the model rides the code default), no IAM statement,
   no schedule, memory or timeout. Any other line in the plan is not covered: apply nothing and report.
3. **NEVER-2.** A ledger entry opened before the apply and closed at completion; legs L1 (apply) and L2 (this seat's read of the first runs on the pin: the 2026-10-16 11:00Z chain and the 13:00Z sweep).
4. **Window.** Never inside 10:55Z-11:15Z or 12:55Z-13:15Z. **Complete before 2026-10-16 10:45Z**, so the first chain on the pin is 2026-10-16 11:00Z and the first sweep 13:00Z.
5. No ad-hoc invocation, no test event, no search and no OpenAI call from the applier. The first run on the pin is the scheduled one.
6. Every read below holds at the apply.

## Blast radius

- **Code** (`git diff --stat ea0e5025ac 34b2ab6351`, tests left out): **4 files, +61 -7**.
  - `gold_trade_schedule.py` (RIV-ya-1): `load_actions` drops an INFERRED event row whose (normalised security_id, event_type, ex_date) a MEASURED row also holds, after the void drop and before the union; the count rides `df.attrs["precedence_dropped"]`; the stage `detail` carries it. Triple unchanged.
  - `price_series.py` (RIV-ya-1): the same rule over the chart's actions frame before the splits are applied (a Bloomberg split and an inferred split of one ex_date apply once, whatever the ratios); each key's result gains `precedence_dropped`.
  - `ai_accounts.py` / `ai_client.py` (RIV-yb-1): the default model `gpt-5.4` becomes `gpt-6-astra` (the env var still overrides); both clients send `temperature` only to a `gpt-5*` model. **Prompts, `PROMPT_VERSION` (`a1-chain/8`) and every grounding or wording rule unchanged.**
- **Addresses do not move:** `addr_parity.py . ea0e5025ac 34b2ab6351`: OK 31 / ERR 0 at each pin, **differences 0 of 31**.
- **Tests:** at HEAD, `rivalfunds/tests` plus the round-31 and round-30 xe3 checks: **1062 passed, 6 skipped, 0 failed** (main tree). The suite at the pin tree itself was NOT read by this seat; AC2 of the apply order reads it there.
- **The served output does not move where nothing differs (read-only, against the live store, 2026-10-15):**
  - G5: `round30_prep/xe3_live_delta.py 60` over 60 report dates, 13 funds: `infer_trades` old (2,062 x 43) = new, `infer_recon` old (734 x 38) = new, `held_funds` {} = {}: **DELTA = 0**.
  - Chart: `round31/ya1_live_delta.py 60` over 602 held securities and 365 days (G1 46,889 rows, G4 5,467 rows, 9,906 action rows, **0 INFERRED**): the series at the base module and at HEAD equal for every key, `precedence_dropped` 0 on all: **DELTA = 0**.
- **What DOES move, by design: the AI accounts.** From the first sweep on the pin every new `research_hypotheses` row carries `model_version` `gpt-6-astra` and its text is written by that model. Measured read-only before the cut (the production chain and prompts, page day 2026-10-15, 13 funds, 27 chat calls, nothing written):
  `gpt-6-astra` **26 of 26 items PASS, 1 correction**; the stored 13:00Z sweep on `gpt-5.4` was 24 of 26 PASS with 9 corrections (TXUE's two FAIL). Usage of that trial: 123,968 prompt tokens, 23,137 completion tokens, 523 s for the 13 funds sequentially.
  `gpt-6-astra` answers HTTP 400 to `temperature: 0.2`; the cell removes it for that model, and the trial ran the production client's request without it.
- **Egress:** one vendor, the same one (OpenAI chat completions); the chain's worst case is still 4 chats per fund; no SERP or Bloomberg path is touched. The price per token of `gpt-6-astra` against `gpt-5.4` is not measured here.

## Writers, and the expected outcome read from each producer's rule (both branches)

Writers of the objects `load_actions` and `price_series._actions` read (`gold/corporate_actions/date=<D>/`), counted from the code: **3** -- `enrichment_bloomberg` (`actions-<rev>`, claim MEASURED), `dramatic_move.write_rows` (`actions-inferred-<rev>`, claim INFERRED)
and `dramatic_move.void_rows` (`actions-void-<rev>`). This act changes the READ rule of two readers and no writer. Writers of `research_hypotheses` rows: 1 (`ai_accounts.write_rows` through `run_day`), unchanged apart from the model.

| property | writers | outcome after the pin |
|---|---|---|
| corporate actions served to G5 and the chart (the store today: 12 plain pulls, 0 inferred, 0 void) | 3 | branch A: nothing is dropped; both readers equal the old ones (DELTA 0, measured above) |
| an `actions-inferred-*` split of the same (security, ex_date) as a Bloomberg row | 1 | branch B: the inferred row is dropped and counted in both readers; it applies once, as the Bloomberg row |
| an `actions-inferred-*` row with no Bloomberg row of its key | 1 | applied, as the union intends |
| AI rows of a sweep | 1 | branch A: the request is accepted, rows carry `gpt-6-astra`. Branch B: the request is refused or the chain raises: `ai_stage.run_for_day` returns FAILED and the sweep republishes with `ai_run` FAILED (`sweep.py` lines 655-663); no account is invented; the previous day's rows are not relabelled |
| page `platinum/page/date=<D>/` | 1 | the audit and page footer read `Model gpt-6-astra` on the new rows; every other word unchanged |

## Rollback, per key

- **Code:** re-apply the tree at `ea0e5025ac` through `safe-apply` (a fresh worktree at that pin; its plan is 0/5/0 and restores the five packages). The round-30 trees `C:/tmp/rv-r30-dell1` and `C:/tmp/rv-r30-rollback` are kept until their ledger closes (it is CLOSED: they may be removed).
- **A wrong AI object:** `research_hypotheses` objects are append-only; a bad day's rows are superseded by a re-run under the restored code (a separate act, on this seat's word).
- **A page that reads wrong after the pin:** the code rollback above, then the next publish.

## Known and stated

- The CVO grades the J1 of RIV-yb-1 on the served sweep: `model_version` `gpt-6-astra` on 26 of 26 rows and a Grounding FAIL count no greater than the 2 of 26 of 2026-10-15.
- The live DELTA reads cover 60 report dates (G5) and 365 days over 602 keys (chart); both are reads of the store, not rebuilds.
- A store with an inferred row is NOT exercised live (none exists); the rule is exercised by the round-31 check files on planted stores, both branches.
- **L2** reads the first chain and sweep on the pin: the stage logs, the AI run record, the `model_version` column, the grounding counts, the G5 stage's `precedence_dropped` (0 expected), and the page footer.
