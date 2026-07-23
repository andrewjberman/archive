# TO 3F-B6 (LIVENESS PORTION) — Feed-Level Liveness Signal for the COT Rebalancer Feed

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-22 ~21:1xZ · **Scope:** deliverable (a) only — the
TEMPORAL-vs-CURRENT probe is sequenced LAST per COO 204647Z / CTO 204557Z (PRD v1.8) and is NOT run here.
**This portion gates 3F-G8.**

## The signal

**Nightly vendor-revaluation drift in `rebalancer_model_detail`.** Black Diamond's Rebalancer re-marks
every composite model's component weights (`relativeAllocation` / `absoluteAllocation`) and stamps
`updatedAt` in a vendor-side nightly batch (~05:01Z — CRO's A5 observation, now mechanism-confirmed as a
revaluation, not a config edit). Those weights are **market-priced quantities**: they move when the vendor's
data plane is alive, regardless of whether any assignment changes.

**Liveness check (per trading-day pair D-1 -> D, evaluated on already-landed bronze):**
```
ALIVE   <=> at least one common model_detail payload differs (or max updatedAt advanced)
FROZEN  <=> all model_detail payloads byte-identical across a TRADING-day pair
```
NOT a roster diff: the discriminating fields are valuation marks, not assignments. The check reads
`blackdiamond/cottonwood/bronze/rebalancer_model_detail/{date}/` — **no new endpoint, no producer change,
no extra vendor calls.**

## Demonstrated discrimination (the two live pulls, denominators printed)

Pulls: 2026-07-21T23:31:2xZ (deploy-day run) and 2026-07-22T06:00:4xZ (first scheduled cron(0 6) fire —
schedule exercised). Note these bracket ZERO trading sessions (Tue post-close -> Wed pre-market), which
makes the result sharper:

| Surface | 07-21 vs 07-22 | Verdict |
|---|---|---|
| `rebalancer_models` (roster) | 1/1 page byte-identical (md5) | assignment STABLE |
| `rebalancer_accounts` (book) | 5/5 pages byte-identical (md5) | assignment STABLE |
| `rebalancer_model_detail` | **20/25 models differ**; field classes: `relativeAllocation` 473 leaves, `absoluteAllocation` 473, `updatedAt` 31 | feed ALIVE |

Both states measured simultaneously on the same pull pair: **the roster read "no change" while the feed
proved itself alive** — precisely the case CRO §7.4 says storage cannot discriminate. The refinement to
§7.4: that indistinguishability is a property of the ASSIGNMENT surfaces (`models`/`accounts`); the SAME
feed's `model_detail` surface carries a per-day vendor heartbeat, and it is already in our bronze.
(The weights moved across a no-market-hours window because the ~05:01Z batch re-marks to the prior close —
the signal keys on the vendor's BATCH running, which is exactly "the data plane is alive.")

## Honest limits

1. **5/25 models static across the pair** (simple/single-component models with structural weights, incl.
   pinned 1.0 compositions). The check is fleet-level (ANY model moved), never per-model.
2. **Market-closed-day pairs:** weights may legitimately freeze when the prior close is unchanged
   (calendar-first, NEVER#1 — evaluate on trading-day pairs only). Whether `updatedAt` still advances on
   closed days is UNDETERMINED until the feed's first weekend (07-25/26) is observed; until then closed-day
   pairs are simply not evaluated.
3. The signal covers the REBALANCER app's data plane (where weights recompute). A broader BD-platform
   canary (the DataMining HOLDINGS_DAILY file, which changes every delivery — measured in 3F-B5) is
   corroborating but is a different feed; the model_detail signal is the feed-level one this TO demands.
4. Two data points exist today (the feed is 2 days old — that is its age, not a gap). The signal's
   false-alarm rate accrues measurement for free with every daily pull.

## Carried bindings (per the TO)

- **Fingerprint BAN carried:** holdings-basket fingerprinting stays banned by measurement (pairwise cosine
  0.62–0.98, mostly >0.90) — nothing here weakens it.
- **~05-28 structural depth ceiling stands** regardless of any probe outcome: no Opal-model series can
  predate the models' creation (2026-05-28..07-17).
- **Zero backfill executed; forward-only stands.** The TEMPORAL probe (with its mandatory positive
  control — CRO churn data supports construction: 5-of-296 new accounts since 06-08, models created on
  07-06 for a quarter of the book) runs LAST in the sequence, per the consolidated order.

## Phase-3 denominators (bronze re-list)

`rebalancer_models`: 1 page/day x 2 days · `rebalancer_accounts`: 5 pages/day x 2 days (rows 911/911
via manifest totalResultCount) · `rebalancer_model_detail`: 25 files/day x 2 days, 25/25 common ·
`meta/pulls/{date}/`: 2 manifests/day x 2 days. Series is 2 days old because it STARTED 07-21 — not a gap.

## Probe prep (added ~21:47Z — the control is constructed BEFORE the probe runs, per the TO's hard gate)

**15 positive-control candidates identified and banked**: Opal-assigned accounts in today's rebalancer
book (295 Opal of 911 total) that are ABSENT from the 2026-06-09 `fact_holdings` book (680 distinct
accounts) — their assignment necessarily changed (none -> Opal) between the probe windows. First eight:
`658508703` (Sat 50), `658508963` (Sat 40), `658509261` (Sat 60), `658508828` (Sat 60),
`638432512` (66% LT/34% UST), `Z40493496` (Cash+Sat 50), `658509146` (Sat 60), `658509145` (Sat 80).
The control can fail in BOTH directions: a TEMPORAL surface must return these absent/unassigned for the
06-09 window; a CURRENT-stamped surface returns them carrying today's Opal strategy under a 06-09 label.
~~The probe itself runs LAST in the consolidated sequence, after tonight's qt1 template dump.~~

**SUPERSEDED ~22:31Z (CTO ruling 222856Z, relayed COO 223148Z — which retracts COO 222951Z):** the
temporal-vs-current probe is **ABSORBED into CRO's Andrew-authorized BD campaign (his terminal ~2210Z)**.
0.6.2 does NOT run it; 0.6.2 CONSUMES CRO's results. Rationale on the record: CRO's intrinsic controls
(April "No Strategy" sentinels + the 05-28..07-17 model-creation timeline) are failable positive controls
baked into the data, and a second agent probing the same live session/IP-bound DataMining surface is a
401-manufacture hazard, not free redundancy. The 15 banked control accounts above are OFFERED to CRO as a
belt-and-suspenders cross-check (offered 222902Z, pre-ruling). **My B6 = the liveness signal (CLOSED,
accepted 211113Z) + the fingerprint-ban and forward-only carriers in this deliverable. The mutation-risk
re-persist probe piece is retired with the absorption.**

**TERMINAL ESCAPE MECHANICS (CTO 224317Z via COO 224949Z — supersedes "explicit GO only"; the last word):**
the confirmation run is **PRE-AUTHORIZED on a machine-checkable condition evaluated by 0.6.2 at the 02:00Z
on-box window**: IF CRO's campaign artifacts show EITHER (a) a TEMPORAL verdict OR (b) a CURRENT-only
verdict with the window-integrity limb demonstrated GREEN -> STAY RETIRED (record which). ELSE (silent, or
CURRENT-only with that limb missing/not-green) -> RUN the confirmation in-session (one fresh session, one
IP, sequential-not-concurrent with CRO, timestamp-coordinated; method = past-window qt5-style run checking
the 15 banked control accounts), no GO to fetch, and fold the result here alongside CRO's.
**+ PRECONDITION (COO 230011Z, additive): the run limb ALSO requires a FRESH BD session** — CRO's campaign
is HELD on a 16-day-stale session; forcing a run against a stale session manufactures the 401 this whole
chain exists to avoid. Three clean outcomes at 02:00Z: sufficient-verdict -> retired; insufficient + fresh
session -> run; insufficient + stale session -> record `BLOCKED-ON-SESSION-CAPTURE`, do NOT force. NOTE:
the SAME session gate may bind B5(c)'s template dump (same DataMining surface; cot DataMining silver
stale since 07-09) — evaluate with a cheap read-only auth probe (mint the DataMining bearer) BEFORE the
dump; a 401 there = B5(c) BLOCKED-ON-SESSION-CAPTURE too, recorded, not forced.

## DISTINCT FOLLOW-ON (WS-1 feed-liveness, SECOND session surface — named per COO 230232Z, NOT a B6 re-open)

**The BD session-capture chain's own liveness is UNDETERMINED while its product keeps working.** Two
independent groundings, 2026-07-22: (a) CRO @4c701a0b4 — SM `blackdiamond/cot/session` LastChanged ~07-06
and session-fetch logs stop ~06-26, i.e. the jar has not been re-WRITTEN in ~16 days on his instruments;
(b) mine — DataMining bearers mint successfully off that jar DAILY (3 qt tables landed 07-22 02:03-04Z)
and the Rebalancer bearer minted this morning. Reconciles only if durable device/identity cookies outlive
the product-API TTLs — meaning **the nightly 02:00Z "fresh capture" may be firing without writing, and
nothing would notice until the durable cookies expire** (the B6-liveness class on a SECOND surface: the
producer looks alive because its output is consumed, but the producer may be dead). JOINT VERDICT
COMPATIBLE (CRO 231255Z) is unaffected tonight — auth works on the CURRENT jar either way. **Window
observation planned (cheap, settles it): read the SM secret's LastChangedDate at ~02:05Z — advanced =
capture writing; static = the chain fires-without-writing and the WS-1 follow-on is REAL.** Owner: 0.6.2
(WSE_COTMDL WS-1 lane); qt4/qt5 run-level freeze (silver frozen since 07-09) is the SIBLING defect,
unified with the ADVI-perception freeze + the banked 18-day alarm per COO 230659Z.

## ESCAPE EXECUTED (2026-07-23 02:02-02:12Z) — RESULT: HELD-ON-THE-FEED, temporal question stays OPEN

Condition evaluated 02:02Z: no CRO verdict artifact existed (probe [HELD] in the campaign brief) -> escape
FIRED with the amended instrument (CRO's `cot_qt5_temporal_probe.py`, joint-verdict COMPATIBLE), run ONCE
on-box (SSM a051ffc7, python3.11, sequential after B5(c), CRO holding zero concurrent calls). Verbatim:
`token minted OK / HELD: baseline read HTTP 500 -- no verdict.` **Error class captured: NOT auth** (bearer
minted; template GETs succeeded x4 minutes prior; qt1/qt2/qt3 DataMining RUNS succeeded 02:03-04Z same
jar), **NOT the 0-row shell** — a server-side HTTP 500 on the qt5 explicit-window RUN call itself.
**Root read (source-confirmed): the 07-09 qt4/qt5 freeze is a TABLE-SPECIFIC RUN-LEVEL vendor-side
failure; session/auth fully exonerated** (and the WS-1 fires-without-writing finding above was
triple-confirmed in-window: SM LastChangedDate ~07-06 across reads 02:02:07/02:02:54/02:08:36Z + the
harness's own `captured_at=2026-07-06T02:02:47Z`). Mechanism hypotheses (UNTESTED): the 06-30 qt4
template re-persist (templates/unrealized.json rewritten 06-30T15:25Z; templateId 237784 vs the 226xxx
siblings) / a vendor change ~07-08. **No verdict was manufactured; the temporal question is UNANSWERED
pending the qt5 feed repair** — that repair gates it, and carries the unified defect (ADVI-perception
freeze + the banked 18-day alarm + this). B5(c) note: the dump ran CLEAN the same window (4/5 tables;
qt3 realized = selectable-but-unpersisted, no templateId — RF-14 refinement).

## For CRO (A5 residual, now determined)

CRO's "whether updatedAt movement is composition edits or a system touch is not determined": **determined —
it is a nightly revaluation batch.** The updatedAt advances ride WITH 473 re-marked weight leaves across a
window containing no human edit and no market session; a config-edit explanation cannot produce that
signature across 20 models simultaneously at 05:01Z.
