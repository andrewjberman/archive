# The Canonical MDPF Clock — T2.C Declaration (v2)

    author:     0.7.0_AE_CloudOps
    declared:   2026-08-03 (v2 ~21:50Z; v1 ~21:20Z superseded-in-place, delta log at bottom)
    authority:  T2.B ruling @440d16e018 · CTO anchor redline 212557Z + resolution datum 212952Z ·
                COO amendments #1-#3 (@17d5fe3db5, @0360dc60be, @983a22c255) · DS measured landing
                table (0.2.0_DS 212937Z + checklist v1.1 @b808db920e) · T1.A census @389c528ddb
    consumers:  T1.C (0.2.0_DS -- rows 1/2/12), T3.B (~F -- invalidation bound), T5 sequencing,
                COO + CTO. v2 is the contract; v1 values are VOID.
    status:     v2 DECLARED (mandated re-declaration per amendment #3 -- v1's 13:00Z close was
                measured-wrong: two binding inputs land after it). TF implements against THIS doc.

## 1. Anchor (CTO-ruled, 212952Z): America/New_York, WHOLE CLOCK

Every leg of the canonical clock — floor, accrual bridge, publisher, T3.B bound — binds to
**`America/New_York` (DST-aware)** via `ScheduleExpressionTimezone`. The decision datum: the
latest-landing binding input (Orion) gives a 44-minute margin to the floor in summer, and a
fixed-UTC clock loses 60 minutes of that margin at the EST shift — **negative margin in winter**.
ET-anchoring preserves measured margins year-round because the latest inputs are ET-anchored at
source. UTC-fixed upstream jobs shift EARLIER in ET during winter — the safe direction (shown in §2).
Implementation consequences: the incumbent accrual Scheduler re-anchors from `cron(45 15)Z` to
ET-expression; the incumbent publisher is an EventBridge RULE (UTC-only by API) and MUST migrate to
an ET-anchored Scheduler schedule, or the accrue→publish order inverts in winter (11:45 ET accrual
vs a fixed-16:15Z publisher = 11:15 ET winter). That migration is an implementation leg of this TO.

## 2. The measured per-input landing table (the close is DERIVED from this — both DST regimes)

Binding-input set: source-cited by 0.2.0_DS (T2.A/T1.C, msg 212937Z). Producing-job attributions
are from my T1.A census crons; job→table rows marked INFERRED are a Phase-1 proof obligation.

| Binding input (table) | Producing job (census) | Job anchor | Measured landing → EDT wall | EST projection | Season-worst ET |
|---|---|---|---|---|---|
| `smartx/platform/silver/fact_model_aum_daily` (THE axis frontier source, dim `:787-789`) | SmartX ET pull chain 09:00–09:35 ET (INFERRED-from-timing, DS 2 samples) | **ET** | 13:40–13:41Z = **09:40–09:41 ET** (07-31, 08-03) | 09:40–09:41 ET (14:40Z) | 09:41 ET |
| `orion/inflection/silver/fact_assets` | `opal-assets-ingest-mirror-inf-daily` cron(15 14)Z (landing 14:16:05Z = cron+65s; INFERRED) | UTC | 14:16Z = **10:16 ET** | 14:16Z = 09:16 ET | **10:16 ET (summer)** |
| `schwab/08242234/silver/fact_rps_s2` | `opal-assets-silver-schwab-sweep-daily` cron(15 12)Z | UTC | 12:15Z = 08:15 ET | 07:15 ET | 08:15 ET |
| `eclipse/inflection/silver/fact_portfolios_full` | overnight job ~03:30Z (measured 03:30:30Z; job id INFERRED) | UTC | 03:30Z = 23:30 ET(-1) | 22:30 ET(-1) | 23:30 ET(-1) |
| `blackdiamond/cottonwood/silver/{fact_model_assignment,fact_holdings}` | cot mirror 03:30Z + bd silver sweep 05:00Z + dim-convert 03:05Z | UTC | ≤05:00Z = 01:00 ET | 00:00 ET | 01:00 ET |
| roster / crosswalk / frozen snapshot | static | — | n/a | n/a | n/a |

**Season-max lateness = Orion at 10:16 ET (summer).** In winter every UTC-fixed input lands earlier
in ET and the ET-anchored SmartX chain is season-stable — so the summer row is the binding regime.
Sample size is 2 days; **Phase-1 evidence: DS pulls a week of per-input landings (their offer,
212937Z) and the derived close below is re-checked against it before the apply.**

**⚠ Winter-collision watch (UTC-fixed jobs entering the window):** the 16:00Z silver sweeps
(eclipse/orion/smartx) land at 11:00 ET in winter — exactly the floor hour. DS's landing data
indicates the binding tables are produced by the EARLIER jobs (mirror/pulls/overnight), making the
16:00Z sweeps second refreshes — **but job→table is unproven. Phase-1 obligation: prove no 16:00Z
sweep produces a binding table, else escalate before the apply** (re-timing those sweeps is outside
T2.C scope).

## 3. The declared clock (all `America/New_York`; UTC shown for both regimes)

| # | Leg | ET | EDT = UTC | EST = UTC | Mechanism |
|---|---|---|---|---|---|
| 1 | Overnight + morning inputs land | ≤10:16 ET season-worst (table §2) | — | — | existing jobs, untouched |
| 2 | **T-1 SILVER CLOSE (derived)** | **10:45 ET** | 14:45Z | 15:45Z | = season-worst landing 10:16 ET + 29-min buffer; `_provenance.frontier_basis: t-1-settled-close` |
| 3 | **REVAMP REBUILD FLOOR (NEW — the implement)** | **11:00 ET, DAILY incl. weekends** | 15:00Z | 16:00Z | NEW EventBridge Scheduler, `cron(0 11 * * ? *)` @America/New_York → `mdpf-daily-trigger` with static input `source=mdpf.scheduled-floor`. Margins: 44 min over Orion (season-stable by construction), 79 min over SmartX. Daily-incl-weekends per the 06-08 lesson (weekday-only cron missed the Saturday T+1 INF reconciliation — `scheduled-floor.tf` header); Sunday no-ops via trading-calendar arithmetic, never a cron carve. INF completion event (`mdpf-daily-refresh-trigger`) = ACCELERATOR-ONLY, retained untouched. |
| 4 | Accrual bridge | 11:45 ET | 15:45Z | 16:45Z | existing Scheduler `mdpf-accrual-bridge-daily`, RE-ANCHORED to `cron(45 11 * * ? *)` @America/New_York (supersedes the 07-29 UTC-deliberate note in accrual-bridge.tf, per CTO 212952Z) |
| 5 | Publisher | 12:15 ET | 16:15Z | 17:15Z | MIGRATES: rule `opal-assets-mdpf-portal-publisher-daily` (UTC-only) → ET-anchored Scheduler schedule, same target. Anchor coherence requires it (§1). |
| 6 | **T3.B invalidation bound** | **12:15–12:45 ET** | 16:15–16:45Z | 17:15–17:45Z | ~F confirmed edge-visible ≤ ~5 min post-publish on TTL alone (their 212626Z, 25-min margin); invalidation is belt-and-suspenders. Day-1-new-scope error-caching nuance carried to the leg-6 spec (~F item 4). |

**T1.C values (rows 1/2/12):** dedicated schedule = leg-3 floor (cottonwood inside the same
producing-tree run); cadence window = **11:00–12:15 ET**; evidence clock = 3 consecutive NYSE
trading days, per-scope served frontier vs `lib/trading_calendar.py` inside that window.
**Stage-6d pin:** floor 11:00 ET ≥ 10h after the 03:30Z cot mirror both regimes — run-time partition
resolution (`mdpf-daily-dispatch.sh:521-524`, DS citation) deterministically selects the T-1 partition.

## 4. Leg-3 mechanism requirements (unchanged from v1, one addition)

- **The floor must NOT inherit the INF gate.** NEW SOURCE FINDING sharpening it: the deployed
  handler's floor path has its own calendar `run_date` (`lambda_function.py:729-732` — correct) but
  the spine hard-DEFER at `:769` (`GATE_ENFORCE and not spine_fresh`) applies to floor fires too —
  **on the exact 08-03 shape (INF failed, revamp inputs fresh) the built floor would DEFER, not
  heal.** The implementation therefore includes a floor-mode gate change: in floor mode the
  inflection leg joins the per-partner roll-forward path (stale partner → skip feeders + roll
  last-good block, `as_of_by_partner` on the face) instead of hard-deferring the aggregate. Design
  settled WITH 0.2.0_DS at Phase 1 (they own the producer semantics); Lambda change rides the same
  TF cycle (source-map updated, Rule 4).
- **Double-fire safety:** accelerator + floor same-day converge via C3 deterministic run_id + the
  manifest writer's S3-412 convergence (interface @f030ac80d). Proven against the DEPLOYED dispatch
  at Phase 1, per the TO.
- **Adopt, don't duplicate:** the existing built-not-landed `scheduled-floor.tf` (closure row 10,
  20:00Z UTC RULE form) is SUPERSEDED by this leg-3 Scheduler form — modified in place, never two
  floor resources. Its DLQ-policy widening note (one `aws_sqs_queue_policy` per queue) carries.

## 5. What the clock cannot govern alone (unchanged from v1)

T3.A F1 (no Cache-Control → RFC 9111 heuristic client caching; T3.B policy co-governs client-observed
staleness) · T3.A F4 (DataRefresh rollback purges edge, not platinum) · census F5 (legacy `json/mdpf`
plane has NO scheduled producer; HOLD-protected; outside T2.C scope, standing gap).

## 6. Proof protocol (amended per COO amendment #2 @0360dc60be)

3 consecutive NYSE trading days, and a green cycle is evidenced by **PER-STAGE status reads — never
the chain's terminal completion marker** (the 6c lesson: STAGE6-REVAMP errored five nights while the
marker read complete). Per day: (a) chain `status.json` per-stage rc fields, (b) all four scopes'
served `platinum/mdpf/{scope}/aggregate-aua-timeseries.json` Last-Modified inside 11:00–12:15 ET,
(c) frontier == `lib/trading_calendar.py` `expected_last_trading_day`, (d) zero hand-runs (run
provenance from the trigger-identity self-log, `lambda_function.py:702`). A cycle with a complete
marker and ANY errored canonical stage is a RED cycle.

## v1 → v2 delta log (why each changed value changed)

| Value | v1 | v2 | Forcing evidence |
|---|---|---|---|
| Anchor | UTC-fixed all legs | America/New_York all legs | CTO 212952Z: winter DST turns the 44-min Orion margin negative under UTC |
| T-1 close | 13:00Z | 10:45 ET (derived) | DS measured: fact_model_aum_daily ~13:40Z + orion ~14:16Z land AFTER 13:00Z — v1's close was factually contradicted |
| "Last canonical morning input" | schwab sweep 12:15Z | orion mirror 10:16 ET (summer) | table-grain measurement beats job-name inference |
| Floor | 15:00Z MON-FRI | 11:00 ET DAILY incl. weekends | anchor ruling + the 06-08 Saturday-reconciliation lesson (row-10 TF header) |
| Publisher leg | existing rule, untouched | migrates to ET Scheduler | anchor coherence — a UTC-only rule inverts the order in winter |
| Proof | artifact frontier in window | + per-stage rc, marker-blind | COO amendment #2 (the 6c find) |
| Floor-gate posture | requirement stated | + source finding `:769` spine-DEFER applies to floor; per-partner roll-forward design item with DS | lambda_function.py read this session |
