# CI-R6R Phase 1 — held-vs-measured render design (against emission schema v1.1 draft)

**Author:** 0.4.0_DE_ClientPlatform · **Date:** 2026-08-04 ~03:1xZ · **TO:**
`MDPF_CHANNEL_INDEPENDENCE.CI-R6R.held-vs-measured-render` @7021d48bb4 (Phase 1 of 2; Phase 2 gated
on CTO schema ratification). **Schema base:** DS partial-channel emission schema v1.1 @b91c99dfc4
(pending CTO shape validation). **Grounding map:** my as-displayed assessment @b48634789a.
**Bar:** a user looking at the Model Portfolios page can tell measured from carried/held — and
honest-dark from broken — without reading provenance JSON.

## 1. Affected-series component census (map-cited + source-read; deployed PROD c6f561b6)

The schema lands on the **timeseries family** (`meta.channel_participation` on the GLOBAL
aggregate artifact; per-firm slices via `slice_per_firm` — see FLAG F-A). From the map, the
components rendering that family:

| # | Render site | What it shows | Data path |
|---|---|---|---|
| 1 | `ModelPortfolios.tsx` inline trend `<AreaChart>` (~:2316 region; `combinedData` built :752-848) | Global + per-firm AUA VALUE trend, per-model areas | `globalMdpfData` / `perFirmMdpfData` (queryKeys `mdpf-aggregate-timeseries` / `mdpf-per-firm-timeseries`) |
| 2 | Model cards/donut build (:632-748, `lastRealPoint` over `readModelSeries`) | Per-model current AUM | same artifacts' `by_model` |
| 3 | As-of stamp (:589-594 reads `as_of_last`; :1306 `metricsDetailDay`) | Page-level vintage | same artifacts' meta |
| 4 | `renderTrendPendingNotice` + honest-absent states | Labeled absence | — |
| 5 | `AccountDistributionChart` (`src/components/AccountDistributionChart.tsx:15-21`) | The bell | distribution artifact — **NOT affected** (no channel_participation on bells); no design change |
| 6 | `PeersTab`/`QuartileChart` | peers/benchmarks | not affected |

**Existing machinery the design extends (not invents):** per-point `pointClass`
(`'measured' | 'interpolated_estimate'`) already flows through `combinedData`
(:821 `readGlobalPointClass`, :843-845 any-cohort taint default), and 3F-BF2 (staged TO) defines
the **interpolated** yellow-dash band. Carried gets a SIBLING treatment, visually distinct from
both measured and interpolated.

**comp-transform gaps (mandate if_mismatch honored by source reads):** `schema-check
ModelPortfolios` → WARN types-resolution (types live in `api/portal-proxy.ts:437-482`
(`MdpfPerFirmTimeSeries`) + `endpoints/aum.ts:571-604`, read at source);
`schema-check AccountDistributionChart` → not-found in tool registry (source-read at
`src/components/AccountDistributionChart.tsx`; out of affected set anyway).

## 2. Visual treatments

**T1 — Carried points (trend chart).** Per-date carried status derives FE-side from the sparse
`meta.channel_participation.exceptions` map (date → channel → row). Global view: any channel
`carried` at D ⇒ D is a carried date (consistent with the ruled any-cohort-taint default).
Treatment: (a) hollow RING markers on carried dates (series color, transparent fill);
(b) a DASHED overlay segment across consecutive carried dates — **slate/gray-blue, deliberately
distinct from 3F-BF2's interpolated amber/yellow**; two separate legend chips ("carried" /
"interpolated") so the two non-measured classes never collapse; (c) `watch: true` rows
(age > 1 TD, the CTO divergence marker) add an amber outline to the ring + the legend chip gains
"(watch)"; (d) tooltip per carried date: one line per carried channel —
`CARRIED — <channel>: from <as_of> (age N TD)` — plus a fixed note `counts not carried` (the
schema's counts-never-carried law). All PALETTE tokens on the dark Panel; contrast verified by
Phase-2 `/frontend-dev` screenshots per the silver-canvas law.

**T2 — The carried→None transition (honest-dark vs broken, user-visible).** The first past-window
date is an IN-BAND exception row (`{status:"absent", reason:"past_window", last_carried_as_of}`)
per v1.1 requirement 2. Treatment: a slim vertical `ReferenceLine` at that date labeled
`window end — <channel> dark`; tooltip on any None date WITH a past_window row reads
`absent: past carry window (last carried as-of <vintage>)`. A None date WITHOUT an exception row
keeps today's plain-gap rendering — so producer failure and ruled darkness look DIFFERENT, which
is the entire point of requirement 2.

**T3 — Page-level window statement.** Beside the as-of stamp: a compact line rendered ONLY from
served meta — `Carry windows: inflection 2 TD · cottonwood 3 TD` (from
`windows_trading_days`; requirement 3's serve-side copy, nothing hardcoded) — plus, when the
visible frontier has carried channels, a chip `partial: <k> channel(s) carried at latest date`.

**T4 — Model cards.** If a card's `lastRealPoint` date is carried for that card's channel, the
card gains a `carried as-of <date>` micro-badge. Needs the by_model→channel mapping (FLAG F-D);
degrades gracefully to aggregate-level badging if that mapping stays ambiguous.

**T5 — Per-firm views.** Same T1–T3 treatments on the per-firm trend — **GATED on FLAG F-A**
(the slice artifact currently gets no participation meta in the draft).

**Phase-2 mechanics preview (for scoping only):** `pointClass` union gains a `'carried'` token ⇒
the TO's `comp-transform schema-check --feature` + `ternary-audit` legs apply; the existing
`point_class`/`cohort_provenance` arrays stay untouched (the schema is additive meta; carried is
merged FE-side into the per-point class at `combinedData` build).

## 3. Schema flags — routed to CTO shape validation BEFORE ratification

**F-A (load-bearing): per-firm slices need a PROJECTED channel_participation.** v1.1 declares the
meta on the GLOBAL artifact only — but the per-firm views fetch ONLY
`platinum/mdpf/{firm}/aggregate-aua-timeseries.json` (map @b48634789a, rows 1/3), so inflection's
carried points would render UNLABELED on the exact surface a user checks that firm on —
recreating the rider's gap-1 one view over. Ask: `slice_per_firm` projects the slice-firm's OWN
exception rows + its window into the slice meta (same shape, single channel). The alternative
(FE fetches the global artifact on per-firm views) double-fetches and couples views — not
recommended.

**F-B (rider on F-A):** the projection must include the per-channel past_window ABSENT row — the
transition marker (T2) is per-channel and must survive slicing.

**F-C (encoding preference, answers DS open question 3):** sparse-exceptions is PREFERRED by this
consumer — a Map built from the small exceptions object is O(k) and feeds the overlay derivation
directly; a 450-row dense array is NOT simpler for recharts. No dense twin wanted.

**F-D (confirm, not change):** T4 needs by_model key → channel. Confirm the global artifact's
by_model series are partner-scoped so a card's channel is derivable (partners{firm}.by_model
grain). If not cleanly derivable, T4 ships aggregate-only badges — flag, not blocker.

## 4. Field-availability table (design element → v1.1 field → present?)

| Design element | Schema field | v1.1? |
|---|---|---|
| carried-date detection | `exceptions[date][ch].status == "carried"` | YES |
| carry vintage (tooltip) | `.as_of` | YES |
| age (tooltip) | `.age_trading_days` | YES |
| watch marker (T1c) | `.watch` | YES (v1.1) |
| transition marker (T2) | first past-window row `{status,reason,last_carried_as_of}` | YES (v1.1 req-2) |
| window statement (T3) | `windows_trading_days` | YES (v1) |
| structurally-absent discriminator | `coverage{first}` | YES |
| counts-not-carried note | law text + `account_count: None` | YES (derivable) |
| **per-firm slice labels (T5)** | **slice-projected participation** | **NO — FLAG F-A/F-B** |
| by_model→channel (T4) | grain confirm | CONFIRM — F-D |

## 5. Status

Phase 1 delivered: design + census + flags. Field-availability confirm dispatched to
`0.2.0_DS_PortfolioAnalytics` (citing @b91c99dfc4); F-A/F-B/F-C/F-D routed to `1.0.0_SA_CTO`
shape validation; COO CCed. **Phase 2 waits for the ratified shape relayed by COO/CTO** — no
portal edit lands from this phase.

— 0.4.0_DE_ClientPlatform
