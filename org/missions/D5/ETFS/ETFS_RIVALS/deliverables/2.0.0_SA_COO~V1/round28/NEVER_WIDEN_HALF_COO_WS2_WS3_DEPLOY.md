# NEVER-WIDEN -- COO HALF: ETFS_RIVALS workstreams 2-3 -- the Lambda deploy of RIV-wa-1, wb-1, wc-1, wc-2, wd-1, we-1, we-2, wf-1, wg-1, wh-1 at pin b48273e3d0

**Signer:** `2.0.0_SA_COO~V1` (dell1), 2026-10-09 ~14:2xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (asked).
**Placement:** `ledger/CTO_RULING_WORKSTREAM2_SPLIT_ADJUST_TRADE_LIST_SCOPE_20261009.md` guard (3) and ADDENDA 5-6 (the
WS2/WS3 code ships under ONE pair, wh-1 included; the RIV-wi-1 hookup ships later under its own pair). **Applier:**
`0.7.0_AE_CloudOps~DELL1` on a task order from this seat, in its own tree. Model: round 28's aw-1 half
(`deliverables/2.0.0_SA_COO~RV/round28/NEVER_WIDEN_HALF_COO_R28_AW1_DEPLOY.md`).

## VERDICT: SIGNED

Conditions:
1. **Pin.** The plan is made in a tree at **b48273e3d0**, or at a later commit whose seven `STAGED` paths of
   `infra/aws/lambda/etfs-pipeline/rivalfunds_package.py` are byte-equal to that pin's
   (`git diff --stat b48273e3d0 <commit> -- <the seven paths> ':!**/tests/**'` prints nothing). RIV-wi-1 (sweep.py,
   dramatic_move.py and STAGED itself) is NOT in this pin and is NOT covered here.
2. **Plan.** 0 to add, 5 to change, 0 to destroy, and the only attribute that changes is each function's code package
   (`source_code_hash` / the zip). Any IAM, schedule, memory, timeout or environment change: not covered.
3. **NEVER-2.** A ledger entry is opened by the applier before the apply and closed at completion. Its L2 is this seat's
   read of the 2026-10-10 11:00Z chain and 13:00Z sweep.
4. **Window.** Any time after both halves are signed, never inside 10:55Z-11:15Z or 12:55Z-13:15Z, and the apply must
   complete before 2026-10-10 10:45Z.
5. **Snapshot before the apply (the rollback of the one in-place writer).** The bucket `opal-data-etfs` has no
   versioning (`get_bucket_versioning`: no Status, read 14:1xZ). Before the apply, the applier copies every
   `rivalfunds/etfs/gold/holdings_coverage/date=<D>/holdings_coverage.parquet` for the 20 trading days ending 2026-10-09
   to a local directory, and commits the list of keys with byte counts and sha256 in its report. No snapshot means no
   apply.
6. No republish of a past page, no `replay` mode and no ad-hoc run of any stage under this half. The first runs of the new
   package are the scheduled 2026-10-10 11:00Z chain and 13:00Z sweep.
7. Every read below holds at the apply.

## Blast radius

- **What moves:** the code package of the five rivalfunds Lambdas (daily, fetch-holdings, build-silver,
  build-canonical-shape, publish-page). Nothing else. Terraform: `git diff --stat 39889dd4d7 b48273e3d0 --
  infra/aws/terraform/etfs-rivalfunds infra/aws/lambda/etfs-pipeline` prints nothing.
- **What the package gains over the live pin 39889dd4d7** (read with `git diff --stat 39889dd4d7 b48273e3d0 -- <seven
  paths> ':!**/tests/**'`): 19 files, +5027 -95.
  - rivalfunds, 9 files: `ai_accounts.py` 75 (wg-1, wh-1: `a1-chain/8`, `opening_check`, `_mn` thousands, `fact_pack`
    skips below-tolerance, zero and unnamed trades), `dramatic_move.py` +349 (wb-1; NO production caller at this pin,
    row D1-S10), `gold_canonical_shape.py` 60 (we-1: `source_report_date` = the vendor's claimed as-of; `delivered_on` =
    the requested date), `gold_holdings_coverage.py` 40 (wf-1: `regressed`, claim against the previous claim),
    `gold_trade_schedule.py` 100 (wd-1, we-2: `INFER_VERSION`/`GOLD_VERSION` /3 -> /4, `below_tolerance` under 20 bps,
    no trade read across a repeat), `price_series.py` 92 (wa-1: `adjustment` from stored corporate actions; a >3x move
    with no stored action is flagged `GAP_REASON_BIG_MOVE`), `publish_page.py` 10 (skip below-tolerance rows,
    `cash_equiv_lines`, chart `adjustment`), `render.py` 99 (wc-1, wc-2: the trade list closed by default and scoped to
    the selected window, the header Period bar gone, the audit's cash line, `regressed` label), `page_theme.py` 2.
  - Shared dependencies, other seats' commits carried by the pin:
    - `lib/opal_naming.py` +2 -1 (`_is_cadence` accepts the interval form).
    - `infra/logic/registry/` 7 files, +4135 -1, additive.
    - `lib/research/identity/crosswalk.py` +123 -5 and `crosswalk.schema.json` +28. The hunks are in `build_crosswalk`,
      `_legal_name_for` (new issuer functions), `_carry_served` and `main`; **`resolve()`, the only function
      `gold_canonical_shape` calls, has no hunk.**
    - `lib/trading_calendar.py`, `NAMING_SCHEMA.json`, `etf_positioning_gold.py`: 0 lines.
- **Addresses do not move.** `python -I deliverables/2.0.0_SA_COO~RV/round28/addr_parity.py <repo> 39889dd4d7
  b48273e3d0`: 30 literal call sites, OK 30 / ERR 0 at each pin, **differences 0 of 30**.
- **What the deploy writes:** nothing in S3. The first writes are the next scheduled runs.

## Writers, and the expected outcome read from each producer's rule (both branches)

N = 6 served properties this code reaches; writers counted per property (helper read, 13:3xZ, of `sweep.py`,
`publish_page.py`, `gold_*` and `ai_accounts.py` at HEAD):

| property | writers | dates a scheduled run writes | the rule's outcome on 2026-10-10 |
|---|---|---|---|
| page `platinum/page/date=<D>/` | 1: publish-page (the sweep's republish uses the same runner) | D only; the prior page is copied to a `rev_` object first; identical bytes write nothing | Branch A (fresh G5 for D): new page with the WS2/WS3 render. Branch B (no fresh G5): the page publishes with every fund marked not updated, in the new render |
| G5 `trade_schedule` + G6 `flow_reconciliation` | 1: `gold_trade_schedule.handler_entry` (build-canonical-shape stage chain and the sweep) | the batch's report dates, each with its prior date; `/3` != `/4`, so `_g5_target` writes a NEW `-vNN` object, never an overwrite | rows with |share move| under 20 bps of NAV carry `action = below_tolerance` (kept as rows, never trades on the page); no trade read across a repeated report. Branch: a fund with no new report writes nothing new |
| G1 `canonical_shape` | 1: `gold_canonical_shape.handler_entry` | the batch's report dates; a changed `source_report_date` is a new revision object | Bloomberg rows: `source_report_date` = the claimed as-of (equal to the partition: 0 of 18,000+ rows differ, row D1-S7), `delivered_on` = requested date. Branch: no Bloomberg capture -> nothing new |
| G2 `holdings_coverage` | 1: `gold_holdings_coverage.handler_entry` | **the last 10 trading days, IN PLACE at a fixed key, whenever bytes differ** | a capture whose claim is newer than the previous claim reads `new` (CGIC 10-05/06/07 `new`, 10-01/02 `repeat` in the issuer's local run); an older claim reads `regressed`. Rollback: condition 5's snapshot |
| `research_hypotheses` | 1: `ai_stage.run_for_day` in the sweep (`RIVALFUNDS_AI_ENABLE == "1"`) | D only, append-only (a new run object) | `a1-chain/8`. The issuer's two real runs on this code: grounding 26 of 26, '$0.0 million' 0, bare identifiers 0, most shared verdict opening x1 of 13 (`round28/WG1_J1_REAL_RUN_20261009.md`, `WH1_J1_REAL_RUN_20261009.md`) |
| `corporate_actions` | **0 production writers at this pin** (`dramatic_move.write_rows` has no Lambda caller) | none | `price_series` adjusts only where a stored action exists: none are stored, so NO chart is adjusted; a >3x move (Tokio Marine 10-07) is flagged as a big-move gap instead of drawn as a cliff. The adjustment arrives with RIV-wi-1's own pair |

## Rollback, per key

- Lambda code: re-apply the 39889dd4d7 package from the aw-1 tree (`C:/tmp/rv-r28-dell1`, archive pairing intact) through
  `safe-apply`.
- Page `date=<D>`: restore the `rev_` copy publish-page wrote before the overwrite.
- G5 / G6 / G1: no overwrite occurred; rerunning the old code writes a newer object that readers take (newest wins). No
  delete.
- G2: put back condition 5's snapshot bytes for each changed key (a served write under this half's rollback clause only).
- `research_hypotheses`: append-only; the page reads the newest run, so the old code's next run supersedes it.

## Known and stated

- RIV-wa-1's split adjustment is NOT served by this deploy (no stored corporate actions; row D1-S10). RIV-wi-1 brings
  the lookup under its own pair (CTO ADDENDUM 6), with its one-ARN secret read.
- The CVO's open grades: wa-1 J1 HELD for the first published page (this deploy serves the flag, not the adjustment);
  wd-1's repeat clause HELD for the first page rendered with wf-1 (2026-10-10's page).
