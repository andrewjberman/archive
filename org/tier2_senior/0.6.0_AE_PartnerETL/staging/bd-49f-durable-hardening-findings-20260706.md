# BD 49F un-freeze — durable-hardening findings (2026-07-06 incident)

Banked from the 07-06 BD txn un-freeze (deploy-ledger 20260706T1355Z...bridge-0702-coherent). All three
are the SAME family — heavy/long operations on 15-min Lambdas + auth/retry robustness — and are the
generalization of Andrew's 2026-07-06 design flag ("what lambda are we relying on for such a heavy job?").
Route as a durable-hardening PAIR/BUNDLE (WS-5 robustness) after the served-close. Owners noted.

## Finding 1 — runner token-expiry mis-classified as cookie-death (F3/F4). OWNER: 0.6.0 (runner .py author), 0.7.0 deploy.
- MECHANISM (0.7.0-base source-grounded): bd-49f-runner mints ONE bearer token at start (lambda_function.py:124)
  and reuses it for the whole run. A long force sweep (5x~85MB txn chunks) OUTLIVES the token -> mid-sweep 401s.
  The handler L147 `_is_auth_error(exc)` short-circuits to auth_dead=True + break (NO retry) BEFORE the L158-159
  re-mint path can run -> a RE-MINTABLE token-expiry is treated as fatal cookie-death -> 3/4 tables abort ->
  RuntimeError -> sentinel withheld. Live incident: 3 identical async-retry failures 13:59/14:05/14:15Z.
- FIX (Path A, CTO PRE-APPROVED 2026-07-06): on `_is_auth_error(exc)`, re-mint the bearer ONCE from the SAME
  cookie + retry the table; only if the re-mint ITSELF auth-fails (or retry still 401s after MAX_RETRIES) is it
  TRUE cookie-death -> auth_dead. Anti-storm preserved (bounded MAX_RETRIES=3). CTO 4 conditions: (1) idempotent
  mid-sweep resume (txn per-tile writes + _already_landed head-skip => re-do only the failed tile, no double-write);
  (2) crisp binary; (3) pre-emptive TTL re-mint = optional; (4) exercise-gated (clean all-real force run self-completes
  + emits + parity + N-nightly). Align classification with A-prime schwab OAuth-refresh §2.3.

## Finding 2 — heavy force-backfill on a 15-min Lambda is the wrong compute tier. OWNER: 0.6.0 (runner), arch = CTO.
- Andrew-flagged. bd-49f-runner (900s Lambda) is correct for the LIGHT daily incremental, WRONG for a heavy
  force-backfill: a full coherent day = ~450MB+ downloads (txn 5x~85MB + unrealized 37MB + alloc 12MB), each with
  BD's multi-min query->poll->export. Compounded by async Lambda auto-retry (2x) = 3 concurrent heavy runs -> BD
  rate-limit + token-expiry. FIX: heavy/backfill pulls on EC2/SSM (cot-exporter model) OR Fargate, SEQUENTIAL BD
  calls, NO async retry-storm; keep the Lambda for the light daily delta. (Today's un-freeze used a LIGHT session-pull
  of only the 2 stub snapshots + a no-force sentinel-only invoke to sidestep this entirely.)

## Finding 3 — bd-silver-merge at 93% of the 900s Lambda ceiling on recovery re-merge. OWNER: 0.7.0~A (bd-silver-merge).
- 0.7.0~A grounded: today's recovery re-merge REPORT = Duration 837,883ms / Billed 838s of the 900s HARD cap (93%,
  Max mem 2018/3008MB). Normal nightly is lighter, but the FREEZE-RECOVERY re-merge (many reprocess files: new=5
  reprocess=7 txn + new-4 unrealized etc.) barely fit -> the NEXT freeze-recovery could exceed 900s -> timeout ->
  re-freeze. FIX: incremental/chunked recovery-merge OR move the heavy merge to EC2/Batch.

## Finding 4 (gold blocker durable #1) — runner "full" mode does NOT force A_00 --full. OWNER: CTO (arch + lane call); impl in gold_dispatch.sh. STATUS: DEPLOYED 2026-07-06 (commit af1a57c10 -> s3 code/gold/ 23:00Z; CTO-blessed 221022Z + formal-gate; COO owned-paths grant 95f191504). Exercise-verify (dim=bool after a --full-rebuild run) PENDING next mode=full trigger (validate-on-scheduled-nightly, no ad-hoc).
- MECHANISM (exact, source-grounded 2026-07-06): `run_gold_layer.sh` maps BOTH modes to `gold_dispatch.sh --chain full` (incremental) / `--chain full --force` (full). `--force` ONLY bypasses the chain-level freshness GATE -- it does NOT change per-script modes. `gold_dispatch.sh` CATALOG L79 hardcodes `A_00|A_00.accounts_dimension.py|--upload --incremental` (+ C_06 L95); comment L264-265/705: "A_00/C_06 always incremental in chain runs." So EVERY chain run (incl "full") invokes A_00 --incremental -> A_00 `_run_incremental` early-returns without save_dimension when 0 new txn files (A_00 L690-698) -> the producer dtype-gate never fires -> no re-baseline.
- FAILURE it caused (2026-07-06): the account_is_open dtype fix "didn't take" via a full re-dispatch (A_00 ran incremental, no-save), forcing the DELETE-the-dim + fall-back-to-full HACK to get a clean bool re-baseline. A `--full` producer run would have been a one-flag re-baseline.
- FIX: add a `--full-rebuild` flag (or make runner "full" mode) that swaps the A_00 (+ C_06) CATALOG entry from `--incremental` to `--full` (A_00 argparse default IS --full when --incremental absent, A_00 L775-797). Then `mode=full` at bd-gold-trigger produces a clean producer re-baseline, no delete-hack. Preserve DH-2 (chain-level --incremental still rejected). CTO: arch-gate + confirm the impl lane (gold_dispatch.sh sits in data/black_diamond/scripts/gold/ = DS dir, but it's runner dispatch orchestration).

## Finding 5 (gold blocker durable #2) — gold freshness window is CALENDAR-day, not trading-day (holiday-gap). OWNER: DS.
- MECHANISM (source-grounded): B_01.holdings_lots.py `_resolve_unrealized_key` L489 `for delta in (0,1,2)` = a 2-CALENDAR-day lookback for silver/unrealized. On a holiday frontier (run_date 07-06; 07-03=July-4 holiday, 07-04/05 weekend), the freshest VALUED unrealized partition is 07-02 = 4 CALENDAR days back -> OUTSIDE the 2-cal-day window -> falls back to nearest-existing (degraded) or hard-aborts (L523-526) -> degrades holdings_lots -> D_03.composition_artifacts firm_composition EMPTY -> rc=1 chain-halt (tonight's blocker #4; fixed interim by D_03 non-fatal 51a46de30). D_03.composition_artifacts L702 ALREADY comments this exact root.
- CRITICAL NUANCE (don't naive-widen): the 2-day cap is a DELIBERATE guard against the 2026-03-29 stale-key false-close incident (B_01 L479-485; a wider window re-reaches a truly-stale partition -> false Rule-3 force-closes). So the fix is NOT "widen to N days" -- it's count TRADING days not calendar days (07-02 is 1 TRADING day back from 07-06), so the holiday gap resolves while the stale-key guard is preserved. Respect the 2026-03-29 caution.
- FIX (DS): make the delta lookback trading-day-aware (NYSE calendar; there's precedent -- cot_bronze_ingest COT_MARKET_HOLIDAYS env). Self-heals firm_composition/firm_mix (currently last-good 07-03).

## Finding 6 (P2 audit-hygiene, non-urgent next-touch) — BD bronze sentinel stamps producer="cot_bronze_ingest.py". OWNER: DS (shared script); AE co-sequence on next bd-bronze touch.
- SURFACED: CVO 49F Lever A belt-close (flagged by COO 002536Z + 0.7.0~A 002539Z). The bd sentinel bronze/{date}/_BRONZE_COMPLETE.json carries producer="cot_bronze_ingest.py" -- a cot-named producer in a BD-firm artifact.
- GROUNDED BENIGN (CVO+COO+0.7.0~A confirm; NOT a firm-sep breach): data/cot/scripts/bronze/cot_bronze_ingest.py is a SHARED Model-B module firm-bound to bd at runtime (bd-49f-runner sets BD_S3_BUCKET=opal-data-bd + BD_FIRM_ID=49f, pulls from bd's own code prefix, _assert_firm_separation ABORTS if bucket!=bd, IAM Deny on opal-data-cot). Data + separation correct; only the producer LABEL reads cross-firm.
- WHY IT MATTERS: firm-sep (bd<->cot) is a NEVER-rule, so a cot-named producer in a bd artifact reads as a cross-firm leak on a glance -- every auditor (or future-us) must re-derive it's benign.
- FIX OPTIONS: (a) MINIMAL (0.7.0~A rec, preferred): in the shared emit_bronze_sentinel, set producer from a firm-neutral source (BD_FIRM_ID / a neutral module tag) not the hardcoded cot filename -- single-source, correct for BOTH firms. (b) FULLER (COO rec): rename the module firm-neutral (shared_bronze_ingest.py) -- touches shared bd+cot refs = non-trivial, would need COO scoping as a small durable. LANE: DS owns data/cot/scripts/bronze/*.py; AE co-sequences on the next bd-bronze touch. P2, NOT tonight.

## Cross-cutting (0.7.0~A banked AUTHCHAIN-F3F6 8f09c57ed)
- A runner-run / sentinel-emit FAILURE ALARM: today produced 2 SILENT failures (runner errored, no sentinel, no
  page). A completion/freshness alarm on the fire-and-forget producer is a default-robustness contract (echoes the
  PPLINF fire-and-forget WS-5 candidate). 0.7.0 owns the alarm half.
