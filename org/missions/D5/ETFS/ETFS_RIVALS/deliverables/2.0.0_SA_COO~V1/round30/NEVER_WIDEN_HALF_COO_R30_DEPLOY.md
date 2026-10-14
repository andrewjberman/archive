# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 30 (RIV-xa-2, xc-2, xe-3) -- three modules to the rivalfunds stack, packages only

**Signer:** `2.0.0_SA_COO~V1` (dell1), 2026-10-14 ~15:0xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~DELL1`'s half (asked).
**Why a deploy:** the three cells are `LOCAL` and merged (xa-2 @dff53957e5, xc-2 @8475f46512, xe-3 @fb61d59cf4). The CVO's two J1 reads (xa-2: the sentence beside every
calendar; xc-2: openings in distinct families or a stored reason) are read on a page the DEPLOYED code publishes, and RIV-xe-2's incremental pull waits on xe-3 DEPLOYED and read once
(CTO msg 5577). Until the packages move neither can happen.
**Applier:** `0.7.0_AE_CloudOps~DELL1` (live, idle), on a task order from this seat after both halves are signed.

## VERDICT: SIGNED

Conditions:
1. **Pin: `ea0e5025ac`** (scratch branch `pin-ETFS_RIVALS-r30`). It is the last applied pin `de3c6bf211` (round 29) plus exactly three files at the bytes of `fb61d59cf4`:
   `ai_accounts.py` blob `724b9ca5b1880bf47c45c9f9f5f0da967d862341` (RIV-xc-2), `render.py` `fda4ab160bb72d1f6e5b20ddf3a9df37997354fa` (RIV-xa-2),
   `gold_trade_schedule.py` `63c7f134d17a89a5e84806b104f3debd41a59941` (RIV-xe-3); `dramatic_move.py` stays `37397a1057439b90aa2a9b759beb159375e91673`. **It is NOT HEAD:** HEAD
   also carries RIV-xe-1 (`enrichment_bloomberg.py`), RIV-xf-1 (`peer_groups.json`, `bbg_budget.json`) and other seats' changes; none ships here (xe-1 and xf-1 are site Z's producer
   deploy under `1.0.0_SA_CTO~Z`'s half). A later commit stands only where its `STAGED` paths (`infra/aws/lambda/etfs-pipeline/rivalfunds_package.py`) and the two infra roots are
   byte-equal to the pin's, tests left out.
2. **Plan.** 0 to add, **5 to change, 0 to destroy**: the five `aws_lambda_function.stage` code packages. Nothing else: no environment key, no IAM statement, no schedule, memory or
   timeout. Any other line in the plan is not covered.
3. **NEVER-2.** A ledger entry opened before the apply and closed at completion; legs L1 (apply) and L2 (this seat's read of the first runs on the pin: the 2026-10-15 11:00Z chain and the
   13:00Z sweep).
4. **Window.** Never inside 10:55Z-11:15Z or 12:55Z-13:15Z. **Complete before 2026-10-15 10:45Z**, so the first chain on the pin is 2026-10-15 11:00Z and the first sweep 13:00Z. The apply may
   run any time after both halves are signed that this holds.
5. No ad-hoc invocation, no test event and no search from the applier. The first run on the pin is the scheduled chain's.
6. Every read below holds at the apply.

## Blast radius

- **Code** (`git diff --stat de3c6bf211 ea0e5025ac` over the staged paths, tests left out): **3 files, +94 -19**.
  - `ai_accounts.py` (RIV-xc-2): `frame_of` v2 (the first clause, a stop-list `FRAME_STOP`, eight tokens); `run_chain` stores `shared_frame_with` and `frame_still_shared` in
    `input_manifest`; `PROMPT_VERSION` and every prompt unchanged;
  - `render.py` (RIV-xa-2): `CALENDAR_AXIS_SENTENCE`; `_calendar` puts the sentence as the paragraph before each rendered calendar table; the legend's bytes unchanged;
  - `gold_trade_schedule.py` (RIV-xe-3): `load_actions` reads the UNION of every pull's event rows per security, de-duplicated on (`security_id`, `event_type`, `raw_event_type`, `ex_date`) with the
    latest pull winning, status rows as before, `actions-void-*` objects honoured as `price_series` does (CTO msg 5577 and AMENDMENT 1).
- **Addresses do not move:** `addr_parity.py . de3c6bf211 ea0e5025ac`: OK 31 / ERR 0 at each pin, **differences 0 of 31**.
- **Tests at the pin tree:** `rivalfunds/tests` **1000 passed, 6 skipped**; the three round-30 checks (xa2, xc2, xe3) at that tree: 9 passed. At HEAD: 1037 passed, 6 skipped.
- **The served G5 output does not move (the CTO's arm (a), measured):** `round30_prep/xe3_live_delta.py 60` read-only against the live store: 11 `corporate_actions` objects (9,745 rows, 809
  securities), every object a plain pull (no void, no inferred object). The union adds **101 event rows** (old rule 5,636 rows, new reader 5,737) with ex-dates 2024-09-03 to 2025-09-24, all
  at least ten months before the earliest of the 60 report dates read (2026-07-21 to 2026-10-13, 13 funds, 46,873 G1 rows), far outside any trade window between two report dates. Over those dates `infer_trades` old (2,063 x 43) = new,
  `infer_recon` old (734 x 38) = new, `held_funds` old {} = new {}: **DELTA = 0**. The harness control (the old reader against itself, 20 dates) also read DELTA = 0. NOT read: a replay of
  report dates older than 2026-07-21 (it would read the 101 rows: more complete, never fewer); no scheduled job replays.
- **Egress:** unchanged. The AI chain's worst case is still 4 chats per fund; a verdict whose opening shares a family with an earlier fund's goes back through the chain's EXISTING single
  correction, so the correction frequency may rise, its ceiling does not. No SERP or Bloomberg path is touched.

## Writers, and the expected outcome read from each producer's rule (both branches)

Writers of the objects `load_actions` reads (`gold/corporate_actions/date=<D>/`), counted from the code: **3** -- `enrichment_bloomberg` (`actions-<rev>`), `dramatic_move.write_rows`
(`actions-inferred-<rev>`) and `dramatic_move.void_rows` (`actions-void-<rev>`). This act changes the READ rule of the one reader that served G5 (`gold_trade_schedule.load_actions`, two callers:
the trade-schedule stage and `sweep.py:319`), and no writer. Writers of G5 (`gold/trade_schedule`): 1 (`gold_trade_schedule`), unchanged.

| property | writers | the rule's outcome after the pin |
|---|---|---|
| G5 trade rows (store of full-snapshot pulls, today) | 1 | branch A: the union equals the old rule inside every trade window (DELTA 0, measured above); the output is unchanged |
| G5 trade rows after a short incremental pull lands (RIV-xe-2, not in this act) | 1 | branch B: a security keeps every older action beside the short pull's; the old rule would have dropped them (the reason this cell precedes xe-2) |
| an `actions-inferred-*` row (a web find) | 1 (`run_for_day`) | the old rule hid it from G5 whenever a later Bloomberg pull of the same security existed; the union lets it reach G5 flow adjustment, as `price_series` already does for the chart. Not yet reachable: the live store holds none |
| a voided row | 1 (`void_rows`) | dropped from the union, as `price_series._actions` drops it |
| page `platinum/page/date=<D>/` | 1 | the audit page gains one sentence per rendered calendar; verdict openings may be re-asked once on a family collision |

## Rollback, per key

- **Code:** re-apply the tree at `de3c6bf211` through `safe-apply`; its plan is 0/5/0 and restores the five packages (the round-29 rollback tree `C:/tmp/rv-r29-rollback` is b86feccfeb, older: use a fresh
  tree at `de3c6bf211`).
- **A wrong G5 object:** G5 objects are append-only revisions; rebuild the affected window through the stage's own replay under the restored code (a separate act, on this seat's word).
- **A page that reads wrong after the pin** (a sentence beside a calendar, a re-asked opening): the code rollback above, then the next publish.

## Known and stated

- **The sentence beside each calendar and the frame families** are graded on the served page by the CVO (J1), at the production URL, not by this act.
- **The live DELTA read covers 60 report dates**, the span a daily or backfill stage builds; it is a read of the store, not a G5 rebuild.
- **L2** reads the first chain and sweep on the pin: `audit.html` of BIDD, CGIC and SCHY (the sentence beside each calendar), the verdict openings (families and stored reasons), and the G5 stage's next
  build wherever it runs (rows equal to the previous day's method on unchanged inputs; read, not assumed).
