# The Canonical MDPF Clock — T2.C Declaration (v1)

    author:     0.7.0_AE_CloudOps
    declared:   2026-08-03 (DECLARE-EARLY per TO; implementation follows this doc)
    authority:  T2.B ruling @440d16e018 (MDPF_GLOBAL_PRD.md s.C.3) + T1.A census @389c528ddb
    consumers:  T1.C (0.2.0_DS -- cottonwood schedule values), T3.B (~F -- invalidation slot),
                T5 sequencing. Values below are the ones those legs pend on.
    status:     v1 DECLARED. CTO may redline; consumers verify their legs against it.

## 1. Timezone + DST posture (the one-sentence version first)

**The canonical clock is UTC-FIXED end to end.** Every leg below is an EventBridge cron in UTC;
ET wall times shift by one hour across DST (EDT/EST both shown) and the **ordering invariants hold
in UTC regardless of season** — that is the point of the posture. The existing accrual + publisher
schedules are already UTC-fixed (census rows); anchoring the new floor in UTC means no leg of the
canonical chain can reorder across a DST transition. ET-anchored schedules in the estate
(`America/New_York`: the SmartX 09:00–09:35 ET pulls, `etfs-reports-monthly-run`) feed the
NON-canonical underscore plane or other products — no ordering dependency on this clock
(INFERRED for the SmartX pulls' role; DS to confirm, see §5).

## 2. The declared clock (all four scopes + global; one row per leg)

| # | Leg | UTC | EDT / EST wall | Mechanism (live today unless marked NEW) |
|---|---|---|---|---|
| 1 | Overnight canonical input pulls | 03:05–05:00 | 23:05–01:00 / 22:05–00:00 | `opal-assets-bd49f-dim-convert-daily` 03:05 · `wsb-49f-model-aua-pull-daily` + `wsd-49f-partner-held-etf-pull-daily` 03:30 TUE–SAT (T-1 pattern) · `opal-assets-ingest-mirror-cot-daily` 03:30 · `opal-assets-silver-blackdiamond-sweep-daily` 05:00 |
| 2 | Morning silver sweeps | 12:15 | 08:15 / 07:15 | `opal-assets-silver-schwab-sweep-daily` 12:15 — the LAST canonical morning input (measured census cron) |
| 3 | **T-1 SILVER CLOSE (declared)** | **13:00** | 09:00 / 08:00 | Declared close: all canonical T-1 inputs for `fact_model_aum_daily` and siblings have landed, 45-min buffer after leg 2. This is the value `_provenance.frontier_basis: t-1-settled-close` refers to. |
| 4 | **REVAMP REBUILD — the schedule floor (NEW, the T2.C implement)** | **15:00** | 11:00 / 10:00 | NEW EventBridge **Scheduler** schedule (one-capacity-one-service standard: Scheduler, not a scheduled Rule) firing the producing tree daily MON–FRI... see §3. The INF completion event (`mdpf-daily-refresh-trigger`, typically ~14:30–15:00 UTC when green) is demoted to **ACCELERATOR-ONLY**: when it fires first, the floor run must no-op safely (§3 guard). |
| 5 | Accrual bridge | 15:45 | 11:45 / 10:45 | `mdpf-accrual-bridge-daily` (existing Scheduler cron(45 15) → `mdpf-accrual-trigger`); stays ungated-by-design per T2.B clause 3 |
| 6 | Publisher | 16:15 | 12:15 / 11:15 | `opal-assets-mdpf-portal-publisher-daily` (existing Rule cron(15 16)) |
| 7 | **Invalidation window (T3.B slot — declared, not implemented here)** | **16:15–16:45** | 12:15–12:45 / 11:15–11:45 | The slot T3.B designs into; a scheduled publish must be edge-visible by 16:45 UTC. |

**Cadence window for T1.C rows 1/2/12:** the cottonwood leg runs inside legs 4–6 on this clock —
dedicated schedule = the leg-4 floor (all four scopes rebuild in one producing-tree run), cadence
window = 15:00–16:15 UTC, evidence clock = served-artifact frontier advance vs
`lib/trading_calendar.py` within that window, 3 consecutive trading days.

**Stage-6d pin (DS edge, T1.A census F6):** the floor at 15:00 UTC fires ~11.5h after the 03:30 UTC
cottonwood mirror, so run-time partition resolution (`mdpf-daily-dispatch.sh:521-524`, DS citation)
deterministically selects the same-day (= T-1 data) partition. A floor placed before ~04:00 UTC
would flip that resolution — this is why the fire time is pinned relative to leg 1, not just leg 3.

## 3. Leg-4 mechanism notes (design points the implementation must honor)

- **The floor must NOT inherit the INF gate.** The 08-03 freeze mechanism (T2.A @0b5acf3148): INF
  `pipeline-failed.json` kept the event-gated chain from rebuilding while the revamp inputs were
  fresh (scratch rebuild on the 08-03 partition emitted `as_of_last=2026-07-31`). A floor that
  routes through the same INF-spine freshness gate defers on exactly the day it exists for. The
  floor's own gate is the T-1 arithmetic of its ACTUAL inputs (`fact_model_aum_daily` frontier vs
  `lib/trading_calendar.py`), not INF's sentinel. Implementation shape (Scheduler → dispatch with a
  floor-mode flag vs a gate bypass in `mdpf-daily-trigger`) is settled at Phase-1 comp-blast against
  the deployed dispatch script — declared here as a REQUIREMENT, not an implementation.
- **Same-day double-fire must be safe.** Accelerator (leg 4a, ~14:30–15:00 UTC) + floor (15:00 UTC)
  can both fire within minutes. The implementation must verify the existing dispatch's concurrency /
  idempotency posture (run lock or vintage check) BEFORE the TF lands; if the chain is not
  double-fire-safe, the floor demotes the event edge by REMOVING nothing but must serialize (e.g.
  the floor run no-ops when the day's vintage already advanced). Evidence at Phase 1.
- **Trading-day posture:** floor fires MON–FRI; on a non-trading day the T-1 arithmetic yields
  "already at frontier" and the run no-ops — NEVER#1 (trading-day frontier, not wall-clock) is the
  no-op predicate, never a calendar hack in cron.

## 4. What the clock CANNOT govern alone (carried from T3.A, per COO 21:18Z)

- **Client-observed staleness is co-governed by T3.B cache policy.** T3.A F1 (CTO-validated): mdpf
  responses carry NO `Cache-Control` end-to-end since the 07-29 router flip; browsers apply RFC 9111
  heuristic freshness (~10% of artifact age), ungoverned and invalidation-unreachable. Until T3.B
  lands explicit cache policy, a client can hold a pre-publish body past leg 7 with no
  invalidation reaching it. The declared publish window + T3.B's policy TOGETHER bound
  client-observed staleness; this clock bounds only edge/origin.
- **T3.A F4 interaction:** DataRefresh rollback purges edge but NOT platinum objects — a rollback
  inside legs 5–7 can re-pin the edge to a platinum body the rollback did not touch. T3.B designs
  the interaction; declared here so the slot (leg 7) is chosen with it in view.
- **Legacy `json/mdpf` plane (T1.A census F5):** NO scheduled producer exists for it; it is
  HOLD-protected (live producer input, 49F count axis). This clock does NOT schedule it — its
  freshness remains ad-hoc until the decouple work closes (DO_NOT_DECOMMISSION doc). Declared as a
  standing gap, deliberately outside T2.C scope.

## 5. INFERRED rows awaiting confirmation (labeled per standing norms; none blocks the floor TF)

| Claim | Label | Confirmer |
|---|---|---|
| The 16:00 UTC silver sweeps (eclipse/orion/smartx) are NOT binding inputs to the canonical T-1 rebuild (successful T-1 serves have occurred with rebuilds completing ~15:00 UTC, before those sweeps) | INFERRED from timing evidence | 0.2.0_DS (producer owner) |
| SmartX ET-anchored pulls (09:00–09:35 ET) feed the underscore plane only | INFERRED | 0.2.0_DS |
| Typical INF completion (accelerator fire) lands 14:30–15:00 UTC when green | INFERRED from 07-31/08-03 observations | census of run history at Phase 3 |

## 6. Proof protocol (acceptance restated as the measurement)

3 consecutive NYSE trading days: all four scopes' served `platinum/mdpf/{scope}/aggregate-aua-timeseries.json`
advance to the SAME expected frontier (`lib/trading_calendar.py` `expected_last_trading_day`) within
the 15:00–16:15 UTC window, timestamps read LIVE per day; ZERO hand-runs in the window (run
provenance from existing logs only — no new monitors, standing moratorium).
