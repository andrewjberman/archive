# MDPF_VARFLAG — CVO Review of the v0.1 Proposal (2σ Variance Flag on Critical Served Cells)

**Reviewer:** 3.0.0_SA_CVO · 2026-07-17 ~14:4xZ
**Target:** `docs/architecture/MDPF_VARFLAG_PROPOSAL.md` @ `6b86d2712` (renamed from DRFR_VARFLAG @ `c1d1f9718`)
**Asked:** four named asks (§1) + attack the five pre-registered failure modes (§6).
**Verdict shape:** design is SOUND in architecture (staging+gate at the served-JSON choke point,
shadow-first, fail-closed timeout). Two premises are materially wrong against live state — the
history-bootstrap claim and the 2σ/cell-count arithmetic — and both are fixable inside the
existing phasing. No P0 blocks the SHADOW phase; two P1s bind before the GATE phase arms.

## Grounding performed (live reads, this session, 2026-07-17 ~14:3xZ)

- `aws s3api get-bucket-versioning --bucket opal-data-portal-v2` → **Enabled**.
- `list-object-versions json/benchmarks/model_portfolio_benchmarks.json` → **7 versions, earliest
  2026-07-01**; stack contains 3 versions dated 2026-07-17 alone (12:57 / 13:44 / 14:19Z), the
  07-16 corrupt vintage (19,267B), and a 07-17 12:57Z restore byte-sized identical to 07-12
  (19,204B — the rollback).
- `list-object-versions json/peers/peer_performance.json` → **ONE version (2026-07-01)**.
- Cell census on the served artifacts (downloaded this session): benchmarks JSON **385 numeric
  leaves**, peers JSON **210 numeric leaves** — ≈595 total, ≈500+ of them statistical cells.

---

## For CTO — the four named asks

### (a) Delta-vs-level for Peers ranked/percentile cells — LEVEL-DOMAIN + STRUCTURAL, not delta

Delta is right for Benchmark return/vol cells; it is the wrong stationary axis for ranked and
percentile cells, for three mechanism reasons:

1. **Bounded support.** A percentile lives in [0,100]; near the bounds the delta distribution is
   asymmetric by construction (a 98th-percentile fund can only move down). σ estimated over a
   history that sat mid-range mis-sizes the threshold at the bounds.
2. **Quantization.** Ranks are integers over a small peer set; delta σ can be near-zero for a
   stable fund, making 2σ fire on any movement — pure floor territory.
3. **Denominator coupling.** One peer entering/leaving the universe shifts EVERY rank/percentile
   cell simultaneously. Under per-cell delta stats that is a mass-flag event (cry-wolf), yet it is
   a single structural fact.

**Recommendation:** for ranked/percentile cells, (i) always run the free deterministic
level-domain check (percentile ∈ [0,100], rank ∈ [1, N_peers]); (ii) flag on delta with a floor
denominated in rank/percentile points (see (b)); (iii) add a **peer-universe sentinel** — if
N_peers changed vs prior vintage, suppress the per-cell rank flags and raise ONE structural flag
naming the composition change. Where the underlying level statistic (return/vol behind the rank)
is present in the artifact, run the delta stat on the LEVEL and let rank cells ride as
derived-annotation. Note peers cadence is not weekly (one served version since 07-01) — delta
history there is thinner than Benchmark's; see (c).

### (b) Floor sanity — classes are too coarse; one seasonal discontinuity is unhandled

The floor direction (flag iff |Δ| > max(2σ, floor)) is correct and the numbers are reasonable
opening bids, with three corrections:

1. **"Return cells" is not one class.** A 0.50pp weekly-delta floor spans UST (typical weekly
   move ~0.05pp — floor masks a 10-typical-σ error) and equity YTD (routine 1–2pp weekly moves —
   floor is a no-op and 2σ carries everything). Floors should key on **(cell class × period
   class)** at minimum: {return, vol, aum} × {short-period: 1D/1W/MTD, long-period: YTD/1Y/SI}.
   Config-only change; same file.
2. **YTD reset is a guaranteed annual mass-flag.** At the first upload of January every YTD cell's
   delta is ≈ −(prior full-year return) — tens of cells flag at once, all legitimate. Pre-register
   the year-boundary as a structural event (compare against period-reset semantics, or reset the
   YTD delta history at the boundary), or the control's first January is a cry-wolf event that
   teaches operators to bulk-acknowledge.
3. **AUM 2% relative:** sane as a floor, but note legitimate single-account flows routinely exceed
   it on smaller books — expect real flags; that is the control working, not a defect. Fine as-is.

### (c) N=12 window — right target, WRONG bootstrap premise against live state

The premise *"S3 object versions of the served JSON — the history already exists, no new storage
needed"* is **materially overstated** (live-read above):

- Versioning is Enabled, but the benchmarks stack holds **7 versions spanning 07-01→07-17** —
  nowhere near 13 vintages for 12 deltas. Peers holds **one** version: zero deltas available.
- **The version stack is not a vintage series.** Today alone has three versions (multiple
  promotes), the 07-16 corrupt vintage is in-stack, and the 07-17 rollback restore duplicates
  07-12 byte-for-byte. Raw consecutive-version deltas mix intra-day re-uploads (Δ≈0, deflating σ),
  rollback restores (large artificial Δ), and real weekly moves.

**Recommendation:** keep N=12 as the steady-state target, but (i) define "vintage" as an
**accepted-upload event** (keyed on the SFN execution record / DDB row once staging exists;
bootstrapped by de-duplicating the current stack on content-hash + dropping known-bad vintages by
execution metadata), never as "an S3 version"; (ii) accept that bootstrap is floor-only-dominant
for ~a quarter — the proposal's <6-vintage floor-only rule already covers this, just say so
honestly in §1 rather than claiming history exists; (iii) at N=12 with any classical estimator the
σ estimate itself is noisy — the floor is the real control at small N (this strengthens the case
for floors keyed per (b)).

### (d) MAD vs classical σ — MAD, plus metadata exclusion; MAD alone is not sufficient

**Both, layered:**

1. **MAD (×1.4826) as the estimator.** Breakdown point 50% — yesterday's corrupt vintage poisons
   TWO deltas (into the bad vintage and back out of it: the .ST case is −9.48 then +9.48), i.e.
   2 of ≤12 samples; classical σ inflates by an order of magnitude and goes blind for a quarter,
   MAD moves barely. This is exactly the live instance CTO named — MAD wins it.
2. **But also exclude acknowledged-bad vintages by METADATA, not only by robustness.** Two
   mechanism reasons: (i) at bootstrap N (6–8 deltas), 2 poisoned samples approach MAD's
   breakdown; (ii) a robust estimator hides the poison, it does not remove it — the corrupt
   vintage still sits in the pair-chain, so the delta OUT of it is computed against a wrong base
   and the next healthy delta is misestimated. Once the gate exists, every vintage carries an
   execution disposition (promoted / acknowledged-over-flag / cancelled / rollback-restore):
   compute deltas only across **promoted-clean → promoted-clean** pairs, skipping
   acknowledged-bad and rollback-restore vintages in the chain. Config/metadata-driven, no
   statistics needed.
3. Corollary: **rollback restores must not enter the history** (they are re-publications of an old
   vintage; the post-rollback delta legitimately spans 2+ weeks of drift and will read hot). Same
   metadata exclusion covers it.

---

## For CTO — attacking the five pre-registered failure modes (§6)

**FM-1 Cry-wolf — the arithmetic makes this the binding constraint, and it is worse than
"floors too tight."** Grounded census: ≈595 numeric cells across the two named artifacts. A pure
2σ rule under approximately-normal deltas fires ~4.6% two-sided per cell → **expected ~23–27
spurious flags per perfectly clean upload**, against a shadow exit criterion of ≤1. The exit
criterion and the threshold are mutually unsatisfiable unless floors dominate almost every cell —
at which point the control IS the floor table and "2σ" is labeling. Surface to Andrew (his verbatim
says "2 standard deviations" — the scope/threshold trade is his to rule, surfaced not adjudicated):
either (i) per-cell threshold ≈3σ (per-cell FPR ~0.3% → ~2 expected flags/upload), or (ii) keep 2σ
and let the floor table carry the real work, or (iii) 2σ on a much smaller named-critical-cell
subset rather than all 595 leaves. The SHADOW phase measures exactly this — good — but pre-register
the arithmetic now so a 25-flag first shadow run reads as "as predicted," not as a failed build.
**Also: with >5–10 flags on one upload, the all-or-nothing acknowledge UX becomes a wall of text
with one button — reflexive acknowledgment is the trained response.** The UX mock (2 flags) is the
best case, not the typical case at 2σ.

**FM-2 Poisoned baseline** — answered in ask (d): MAD + metadata exclusion, layered. Add one
requirement: the shadow phase must REPLAY the 2026-07-16 corrupt vintage as an exercised
regression — positive control (corrupt vintage flags ST YTD + vol) AND negative control (healthy
07-12 passes clean), run as separate invocations, mirroring the `validate_data_pkl.py` @`2d62804b6`
precedent (exercised FAIL on corrupt 0716 / PASS on healthy 0712). §0 says the design is "judged
against" the test case — make that an executed check, not a thought experiment.

**FM-3 Slow drift** — correctly named out-of-scope. Agree; no change. One note: the excluded class
includes a slow-walk performed via repeated acknowledge-over-flag (an operator acknowledging a bad
number ratifies it INTO the baseline unless (d)(2)'s exclusion also covers acknowledged-over-flag
vintages that later prove bad — the audit trail (§3) is what makes retro-exclusion possible; keep
the DDB flag records permanent).

**FM-4 The gate becomes the outage** — the 24h auto-cancel is right and matches estate law
("a known-wrong frozen number is strictly safer than an unheld pipeline"). Two additions:
(i) AWAITING_ACKNOWLEDGMENT must PAGE a live human at flag time, not only stall — an unread gate is
indistinguishable from a pass nobody mentioned (the standing clock-owner law); name the notified
operator set in the design. (ii) Verify the freshness instruments' `max_age` on these artifacts
tolerates a 24h pause + weekly cadence without a false staleness page, so the gate pausing doesn't
trip a second alarm claiming the pipeline is broken (trading-calendar/T-1 doctrine: the pause is a
HEALTHY state).

**FM-5 Emergency Rollback bypass** — correct that rollback must not be variance-gated. The residual
is the history side, covered in (d)(3): a bypass on the GATE must also be an exclusion in the
BASELINE, or every rollback poisons the next quarter's σ with an artificial jump. One config, both
uses.

**FM-6 (not pre-registered — added): the gate fails OPEN on a config miss.** §2's scope guard
routes ONLY configured key patterns through staging; everything else publishes directly, silently.
A typo'd pattern, a renamed artifact, or a new file added to the tab reverts that surface to
today's ungated behavior with zero signal — the failure mode is invisible precisely because the
unflagged path is the legacy path. **Requirement: a registration invariant per run** — every
configured pattern must match ≥1 staged key, and every staged key under the gated prefixes must
match ≥1 pattern; either miss is a loud structural flag (the "a sweep that cannot find a
known-present instance is a broken instrument" law, applied at design time). Cheap: one set
comparison in the varflag-check Lambda.

---

## For DT (0.2.0 — BE/pipeline lane, when TOs land)

- The staging restructure changes generators' write target. Verify the promote-copy step against
  **listing-based** acceptance (ListObjectsV2 key+ETag+Size — estate standard), and confirm any S3
  event notifications / CF invalidation triggers keyed on the served prefixes behave identically
  under promote-copy writes as under today's direct writes before P2 arms.
- New Lambda + SFN edit ride the standard chain: Terraform-only, source-map entry, `comp-iam
  service` + live `simulate-principal-policy` per Rule 22a for the new staging-prefix and DDB
  permissions (one `--resource-arns` per call, separate positive control).

## For DE (0.2.0 — FE lane, when TOs land)

- Design the acknowledge screen for the N=25 case, not the N=2 case (FM-1): grouped-by-artifact
  collapse, worst-N-first, and the flag count in the button label ("Acknowledge 25 flagged cells &
  publish") so the operator's click names what it ratifies.
- F4 identity sequencing is correctly load-bearing — the acknowledge audit is worthless while the
  identity fallback is `dev@test.com`. Concur with F4-first ordering.

---

## Priority summary

- **P1 (before GATE/P2 arms):** FM-1 threshold/scope ruling surfaced to Andrew with the grounded
  arithmetic (595 cells × 2σ ≈ 23 clean-upload flags vs exit criterion ≤1); FM-6 config
  registration invariant; (c)/(d) vintage-definition-by-execution-metadata (not raw S3 versions)
  incl. rollback/bad-vintage exclusion.
- **P1 (shadow acceptance):** the 07-16 corrupt-vintage replay as exercised positive control +
  healthy 07-12 negative control, separate invocations.
- **P2:** floor classes keyed (cell × period); YTD year-boundary pre-registration; peer-universe
  sentinel; acknowledge-UX N=25 design; FM-4 paging + freshness-instrument tolerance check.
- **No P0.** Nothing blocks the SHADOW build; shadow-first phasing is the correct order and P1
  items all land naturally inside it.

## What you should have asked but did not

Whether the **weekly-upload cadence premise holds at all for the Peers tab** — the live stack
shows `peer_performance.json` served ONCE (2026-07-01) since versioning began, and the benchmarks
artifact re-published 3× today alone. The statistical design (N=12 weekly deltas ≈ one quarter)
assumes a cadence the estate does not currently exhibit on either artifact in opposite directions:
Peers may take a YEAR to accrue 12 vintages (floor-only forever = the 2σ control never actually
arms there, silently), while Benchmark's multi-promote days mean "consecutive vintages" must be
defined by upload EVENT or same-day re-runs collapse σ toward zero and make 2σ hair-trigger. The
cadence census per artifact — not the statistics — is what decides whether this control ever
reaches its armed state on each tab, and nobody has measured it. One
`list-object-versions` per configured artifact, charted by month, before P1 exit criteria are set.

— 3.0.0_SA_CVO
