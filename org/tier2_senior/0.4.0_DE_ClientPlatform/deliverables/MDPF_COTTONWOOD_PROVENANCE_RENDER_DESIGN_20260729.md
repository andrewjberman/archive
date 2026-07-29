# MDPF cottonwood — provenance rendering design (CTO item 1)

**Author:** 0.4.0_DE_ClientPlatform · **Date:** 2026-07-29 · **Status:** DESIGN ONLY — not built,
gated on DS~A's design + CTO's gate (CTO 161504Z / 162343Z / 163432Z).
**Vintage of all citations:** portal DEV `b0fc1e75`.

## The requirement

CTO, verbatim: *"A backfilled estimate that reaches the screen looking like measured data is WORSE
than the gap it fills."* Andrew is actively reading this partner AUM chart and must be able to tell
which points are reconstructed. Enum on every provenance slot
(`pairedProvenanceRead.ts:33`): `measured | interpolated_estimate | absent`.

## What already exists — extend this, do not invent a second visual language

The page already HAS a provenance channel end-to-end. It should be extended, not replaced:

| Layer | Where | Behaviour |
|---|---|---|
| Enum + reader | `pairedProvenanceRead.ts:33`, `:227-256` | Never silently degrades to `measured`: an invalid or missing class becomes `interpolated_estimate` + loud warn (`:233`, `:239`). Correct posture — keep. |
| Choke point | `ModelPortfolios.tsx:967-984` `trendInterpolatedDates` | Its own comment `:973-974`: *"the single choke point — band, dashed overlay, legend entry, and bar outlines all derive from it."* |
| Dashed overlay | `:2232-2233` `interp_total` | Traces the model-stack total only on interpolated dates; shrinks as re-emits flip points to measured. |
| Gap semantics | `:2236-2238`, `:1289-1297` | Null = declared gap; the all-null row filter drops the row and the stack bridges. No client roll-forward. |
| Global opt-out | `:976` | At Global grain the set returns empty — banding is a PER-FIRM treatment. Cottonwood is per-firm, so it is in scope. |

## THE DEFECT — and it is live today, independent of DS~A's fix

`ModelPortfolios.tsx:981`:

```
for (const p of series) if (p.pointClass === 'interpolated_estimate') s.add(p.period)
```

**It keys on CLASS ALONE and never consults the VALUE.** So a date labelled `interpolated_estimate`
whose value is `null` still enters the choke set — and therefore gets the band, the dashed overlay,
the legend entry and the bar outlines. The page asserts *"we estimated this period"* across a hole.

That is exactly DS~A's finding (`:587` copies the one-off's provenance row verbatim → 44 splice dates
carry `interpolated_estimate` on cohorts whose value is None). **The render half of this defect is
mine and it exists now.**

Partial self-protection, worth stating so the fix is not over-scoped: the dashed overlay at `:2233`
computes `trendInterpolatedDates.has(period) ? modelSum : null`, so when every model is null the
overlay is null anyway. **The ReferenceArea band, the legend entry and the bar outlines do NOT
self-protect** — they derive from the set directly.

## DESIGN PRINCIPLE

> **An estimate is a claim ABOUT A VALUE. Where there is no value, there is nothing that could have
> been estimated. The visual assertion must key on `(class === interpolated_estimate AND value !=
> null)` — never on class alone.**

This is deliberately **structural, not corrective**. It makes the render correct *even if DS~A's
label fix is partial, or regresses later, or a future producer emits the same shape*. The render
stops depending on upstream labels being right. Controls over care: I do not want a page whose
honesty is contingent on an upstream field nobody re-checks.

The 44 dates then need no coordination at all — they fall out of the band automatically, before
DS~A's fix and after it.

## The three classes, three treatments

| Class | Value | Treatment |
|---|---|---|
| `measured` | present | Solid stack, no ornament. The default. |
| `interpolated_estimate` | **present** | Existing band + dashed overlay + legend "Interpolated" (already built — keep as-is). Reads unmistakably as reconstructed. |
| `interpolated_estimate` | **null** | **Treated as `absent`.** No band, no overlay, no legend, no outline. This is the 44-date case. |
| `absent` | null | Gap. Row drops, stack bridges (`:2236-2238`). Never `$0`, never a band. |

**`absent` gets no new ornament by design.** A gap is already legible as a gap, and adding a third
visual language to say "nothing here" would compete with the estimate treatment — which is the signal
that actually needs to be loud. The requirement is that an estimate never *looks* measured; it is not
that absence needs decoration.

## Implementation sketch (NOT BUILT — for CTO's gate)

One-line-shaped change at the choke point. The values are already present at runtime — `:978-979`
annotate the series as `{ period, pointClass? }` while the real objects carry `aum` too
(`:767-771`, `:785-789`), so the annotation widens to `{ period, aum?, pointClass? }` and:

```
for (const p of series) if (p.pointClass === 'interpolated_estimate' && p.aum != null) s.add(p.period)
```

Because `:973-974` guarantees one choke point, band + overlay + legend + outlines all correct together.

**Second, same class, different component — the Non-Model tile** (`:1205-1207`):

```
currentAUM:
  perFirmAumMetrics?.total?.non_model_aum ??
  (perFirmMdpfData ? lastRealPoint(readNonModelSeries(perFirmMdpfData))?.value ?? 0 : 0),
```

Both legs terminate in `?? 0`, so an ABSENT non-model quantity renders a confident **$0**. On a
partner AUM page $0 is not a neutral placeholder — it is a claim that the partner holds no non-model
assets. The chart band beside it correctly shows a gap while the tile asserts zero. Fix is the page's
existing honest-absence idiom (the em-dash `AUA_UNAVAILABLE` treatment used for the headline), not a
new one.

✅ **SETTLED 2026-07-29 — field-read, no longer inferred. It is a LATENT TRAP, not a live defect.**
`s3://opal-data-portal-v2/platinum/mdpf/cottonwood/aum-metrics.json` states
`total.non_model_aum = 337,882,950.89`, and the identity holds to the cent:
`model_aum 125,132,212.03 + non_model_aum 337,882,950.89 = 463,015,162.92 = aum`. **The first leg is
populated, so the tile renders $337.9M today — it does NOT render $0.** Nobody should chase this as a
live bug.

The hardening still stands on its own merits (an absent leg would render a confident `$0` on a
partner AUM page), but its priority drops from *defect* to *latent*. **Sequence it behind the band
guard, which IS live.**

Worth noting for DS~A/CTO: cottonwood's point-in-time `non_model_aum` is STATED while its
`non_model_aua` **series** is 0/450 — consistent with the derived-balance account (computable at the
frontier, undecidable across history where custody is absent). The tile and the band are reading two
different producer surfaces, which is exactly why one is populated and the other is empty.

## Axis recommendation (CTO item 2 — RECOMMEND ONLY)

Facts: axis spans 450 days to 2024-11-01; cottonwood has no history before 2026-05-28 in any
artifact; and per CTO custody data begins ~06-09, so **even after the server-side non-model fix lands
correctly, the Non-Model band populates from June — not across the axis.**

**Recommendation: the axis should follow the data's real extent per firm, not a fixed 450-day
window.** Then absence-of-history reads as *"this partner onboarded 2026-05-28"* rather than *"this
chart is broken."* A fixed window against a two-month-old partner advertises emptiness it cannot
fill, and that emptiness is indistinguishable from a data outage — which is precisely the confusion
that put four agents on a cottonwood hunt today.

Explicitly NOT recommending back-filling the axis visually or padding it — that would be inventing
history. **Not changing a client-facing axis unilaterally** (CTO's instruction); this is a
recommendation awaiting his word.

## Open questions for the gate

1. Does the `(class AND value)` predicate belong in the page's choke point, or pushed down into
   `pairedProvenanceRead` so every consumer inherits it? My read: **the reader** is the better home —
   it is the same "never silently measured" posture already at `:233`/`:239`, and it would protect
   consumers beyond this page. Page-level is the smaller diff. CTO's call.
2. Tile honest-absence: reuse the em-dash `AUA_UNAVAILABLE` idiom, or a distinct treatment for
   "producer states nothing" vs "fetch failed"? These are different facts and the page currently has
   one idiom for both.
3. Sequencing with DS~A: the `(class AND value)` guard is correct **independently** of their label
   fix, so it need not wait on them. Confirm we want it landed on its own merits rather than bundled.

---

# ADDENDUM 2026-07-29 ~1730Z — DS~A exchange: a THIRD gap, and two rulings

⚠ **VINTAGE:** all citations ABOVE are `@b0fc1e75`. The PROD back-merge landed as `a969d615` and
shifted this file by +45 lines, so **the line numbers above are stale for current head** — re-locate
by symbol, never by number. Citations in this addendum are `@a969d615`.

## GAP 3 (NEW, mine) — the Non-Model band has NO provenance channel to the screen

`ModelPortfolios.tsx:1323-1331`:

```
const perFirmNonModelByPeriod = useMemo(() => {
  const map: Record<string, number | null> = {}   // <- VALUE ONLY, by type
  for (const p of readNonModelSeries(perFirmMdpfData)) {
    map[p.period] = p.value                       // <- p.pointClass DISCARDED here
  }
```

`readNonModelSeries` correctly *returns* `pointClass`; this map throws it away before the render sees
it. And the choke set (`trendInterpolatedDates`, `:977-982`) draws only from `timeSeriesData.aggregate`
and `by_model` — the non-model map is not among its inputs. **So the Non-Model band cannot render
provenance at all, regardless of how the producer labels it.**

Full gap list:
| # | Status | What |
|---|---|---|
| 1 | **LIVE** | Band/overlay/legend keys on class ALONE → paints "estimated" over null values |
| 2 | latent | Non-Model TILE `?? 0` → an absent quantity would render a confident `$0` |
| 3 | **NEW** | Non-Model BAND discards `pointClass` → no provenance channel at all |

## RULING — DS~A's enum question: reuse `absent`. Mechanism, not preference.

Their options were (i) reuse `absent` vs (ii) add `underivable` for "inputs exist, derivation not
possible". **Ruled (i)**, because `pairedProvenanceRead.ts:239` degrades an *unrecognized*
`point_class` to `interpolated_estimate` + loud warn (the deliberate "never silently measured"
posture at `:233`). Therefore:

> An `underivable` string arriving at a renderer that does not know it is **coerced to
> `interpolated_estimate`, over a None value — which is exactly the 44-date defect the fix exists to
> remove.** (ii) fails INTO the defect, not away from it.

**SHARPENED by DS~A 173513Z, verified by me at source — it is worse than the argument above, and the
asymmetry is the point.** The coercion at `:240` is
`return { cls: 'interpolated_estimate', confidence: entry.confidence ?? null }` — **it PRESERVES
`entry.confidence`.** So an `underivable` row carrying `confidence: 1.0` would not merely be
mislabelled; it would arrive as `{cls: 'interpolated_estimate', confidence: 1.0}` over a `None` —
**byte-for-byte the 44-date artifact, manufactured by the fix meant to remove it.**

Contrast `:234`, the *missing-entry* path: it returns `confidence: null` and therefore **cannot forge
a confidence**. Only the **invalid-enum** path preserves it. So the enum route is specifically the
dangerous one, and "unknown class" is not one failure mode but two with different blast radii.
*(DS~A cited `:241`; actual is `:240` — `:241` is the closing brace. Substance unaffected.)*

(ii) also buys **zero pixels**: `absent` and `underivable` render identically under this design (a
gap, no ornament), since the signal that must stay loud is *"this point is an ESTIMATE"*, not *"this
point is missing"*. Real risk, no benefit.

**Third option offered and recommended:** keep the ENUM at `absent`, carry the precise distinction in
a **non-enum sibling field** (a reason/status string). The render safely ignores unknown non-enum
fields, diagnostic precision is preserved, the contract does not change, and if the distinction should
later become *visible* the render can start consuming it with no producer change. **Enum widening is a
one-way door; a sibling field is not.**

Recorded semantics under (i): **`absent` = "nothing to show at this point"** — covering both "no data
exists" and "inputs exist, derivation not possible". Stated explicitly so the narrow reading is not
re-derived later.

## RULING — DS~A's 32 derivable-but-empty dates: stay on (A), leave them None

Their condition: *"if you cannot show (B) as partly-estimated, (B) is worse than the gap."* **Measured,
and I currently cannot — Gap 3 is why.** A (B) hybrid (MEASURED custody − INTERPOLATED model) would
reach the screen indistinguishable from measured no matter how it is labelled. At ~$330mm on a
client-facing series with Andrew actively reading the page, not worth a wider band.

**This is a sequence, not a refusal.** (B) becomes correct — and better — after:
1. the Gap-1 band guard lands `(class === interpolated_estimate AND value != null)` *(gated, CTO)*
2. `pointClass` is carried through `:1323-1331` and the non-model series feeds the choke set *(small; mine)*
3. then (B) renders visibly reconstructed and honestly triples the band.

**(A) is correct-until-step-2, NOT final.** DS~A asked to be told the moment it flips.

## Housekeeping
`NOT_MEASURED` / `non_model_aua_status`: **1 hit in 404 files scanned, and it is a COMMENT**
(`ModelPortfolios.tsx:304`), not a predicate. Nothing in the render keys off DS~A's fossil string, so
the IAM grant landing breaks nothing here — it only makes that comment stale. Correct on next touch.
