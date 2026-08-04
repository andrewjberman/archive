# GRF — Global T+2 Roll-Forward: SCOPING (design-only)

**Status:** SCOPING DELIVERABLE v1.0 — the 0.5.0_AE_OpalETL handoff artifact (Andrew brings
that seat in HIMSELF; nobody in the fabric dispatches it — his own naming, carried verbatim).
**Author:** 0.4.0_DS_ClientPlatform. **TO:** MDPF_CANRTE.GRF (@ade230bc70, amended @e6c531812).
**Authority:** ANDREW-DIRECT ~17:15Z (verbatim record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260804_1715Z_GLOBAL_ROLLFORWARD_DESIGN.md`
— the phrasing IS the ruling) · CTO 1738Z narrowing (the carry machinery already exists for the
timeseries; this document designs ONLY the two derived artifacts + the contract + the lag rows).
**Citations:** `file:line` resolve @0a61583b2 (dim = `data/mdpf/scripts/gold/
dim_mdpf_aggregate_aua_timeseries.py`, metrics = `.../dim_mdpf_aum_metrics.py`, dist =
`.../dim_mdpf_account_distribution.py`).
**Law dispositions CARRIED, not re-litigated:** (1) no-LOCF stays the PER-FIRM law; the Global
fold gets a DECLARED, MARKED carry (the sovereign refinement is scoped to the fold — the
existing carry-window machinery is its own precedent). (2) The 1646Z frontier-clamp edict
STANDS; this design makes it naturally non-binding, it does not remove it (§5).

---

## 1. What ALREADY EXISTS (cite, don't design — the CTO 1738Z ground)

For **Global `aggregate-aua-timeseries`** the ruling's semantic is LIVE today:
- Bounded carry window, roster-derived: `_cot_carry_policy` reads
  `gate_policy.per_partner_max_lag_trading_days` (cottonwood 3 TD, cadence composed in)
  [dim:1749-1775].
- Every carried point is MARKED: `carried_at_declared_cadence(as_of=...)` labels +
  `as_of_by_partner` [dim:1940-2030] — Andrew's "marked interim" verbatim, already emitted.
- Natural overwrite: the fold rebuilds from sources every cycle; when cottonwood's real value
  lands, the carried point is replaced by construction (no special path).
- DE's frontier clamp reads carried points as PRESENT — the frontier self-advances (the two
  halves of one mechanism, built by two seats independently; folded here per the TO's record
  note). Today's 07-30 clamp was the bounded carry REFUSING a freeze that EXCEEDED the window
  — correct behavior; no window widening anywhere in this design.

**Nothing in this section is implementation surface for 0.5.0_AE. It is the pattern the two
sections below extend.**

## 2. Design: Global `aum-metrics.json` — per-model carry in `by_model`

**The mechanism (one rule): THE METRICS NEVER DERIVES ITS OWN CARRY — IT IMPORTS THE SPINE'S.**
The metrics artifact is a thin projection off the Global spine (`build_firm_aum_metrics`
family; period = the spine's `as_of_last` [metrics meta, verified in today's water test]). The
spine's carried tail already carries cottonwood's per-model values with the carry labels (§1).
Therefore:
- **Values:** no new computation. At a period that falls on a carried-tail date, the by_model
  cells and totals ARE the spine's (already-carried) values — the tie law (metrics == spine to
  the cent, exercised 3x today) is UNCHANGED under carry.
- **Marking (the new, small surface):** the metrics doc gains a `meta.interim` block IMPORTED
  from the spine's carry meta — `{carried_firms: [cottonwood], as_of_by_partner: {...},
  carried_dates_in_window: [...]}` — copied field-for-field from the spine artifact's own
  carry emission [dim:1940-2030 output], never recomputed (the shared-derivation law: one
  carry decision, one author, importers copy). `meta.interim` ABSENT == nothing carried ==
  today's shape (additive, zero consumer break).
- **The composition gate MUST HOLD under carried legs (TO's named question), the rule:** the
  carried by_model KEY SET is frozen to the carried `as_of`'s roster BY CONSTRUCTION — a carry
  copies the last real snapshot, so no key can appear or vanish on a carried date. A
  vocabulary change therefore only ever lands WITH real data, where the existing gates
  adjudicate it. **Reference fixture (today, live):** the fef636c2 'Opal Moderate Income
  Portfolio' arc — the vocabulary gate REFUSED an unknown name on real data, the roster
  question was adjudicated (composition-absent → G8 residual), and the carried tail never saw
  a mixed roster. That is the gate holding under exactly the stress this design must survive;
  0.5.0_AE's acceptance re-exercises it (§6).

## 3. Design: Global `account-distribution.json` — account-COUNT carry semantics

- **What carries:** cottonwood's last real per-model funded counts + `account_units` sidecar
  values (integer counts; the 1.51x non-summability law applies to any cross-model total —
  counts carry PER-MODEL, totals recompute from carried per-model cells by the existing
  formula, never independently carried).
- **Marking:** the dist doc's existing `source` block (which already names the cottonwood
  sidecar + its `__as_of__` [dist:614-657 class]) gains the same imported `meta.interim` block
  as §2 — one marking vocabulary across both derived artifacts.
- **The G8 residual carries alongside:** the Income non-model meta class (~$6.22M/8 accts
  after today's fef636c2 join) rides the same carried as_of, stays in meta, NEVER enters
  by_model (the standing ruling; carrying must not become the door it re-enters through).
- **Coherence rule under carry:** the frontier-count coherence check (account_dist as the ONE
  count source [dim:614-657]) compares LIKE vintages: a carried-count date carries its
  source's as_of, so the check binds carried-to-carried and real-to-real, never across.
- **COMPOSITION SEAM (COO 181037Z; Andrew-direct at 0.2.0's terminal ~17:5xZ): Global
  account-distribution today EXCLUDES cottonwood entirely** (holdings count / container
  metrics / bell curve). 0.2.0_DS + DE spec the INCLUSION fix (49F/INF as the reference
  shape). **The two specs COMPOSE in this order: INCLUSION FIRST (their spec), then THIS
  section's carry semantics apply to the included cottonwood leg** — carry semantics on an
  excluded leg are vacuous, so nothing here lands ahead of theirs. 0.5.0_AE: treat their
  inclusion spec as a PREREQUISITE input for the §3 half of your surface (the §2 aum-metrics
  half has no such dependency). Cross-spec conflicts route to CTO (triangle law), never
  adjudicated in either document.

## 4. The lag declarations — W-1 binding rows (SPEC; declared, never re-inferred)

To land in `data/mdpf/config/route_bindings.yaml` (@8058f5523) as pure-add rows on this
document's acceptance (copy-paste ready; `kind: declared` rows tie to THIS document + the
Andrew record, having no module constant to tie to):

```yaml
# firms.{firm}: add
    effective_lag_trading_days: 1     # 49financial (reliably T+1 -- Andrew 1715Z verbatim)
    effective_lag_trading_days: 1     # inflection  (reliably T+1)
    effective_lag_trading_days: 2     # cottonwood  (BD effectively T+2; carry window 3 TD
                                      # stays roster-derived -- the window is NOT this row)
# global: add
    fold_carry:
      basis: "declared-window marked carry (dim:1749-1775 + :1940-2030 mechanism)"
      marked_by: "carried_at_declared_cadence(as_of=...) + as_of_by_partner + meta.interim"
      overwrite: "natural on rebuild -- no special path"
      authority: "ANDREW_DIRECT_20260804_1715Z_GLOBAL_ROLLFORWARD_DESIGN.md"
```
A lag is a DECLARED property of a vendor feed; nothing may re-infer it from observed landings
at run time (re-inference converts a late feed into a silently-moved contract).

## 5. Frontier-clamp interaction (one paragraph, per the TO)

The clamp (DE-side) reads carried points as PRESENT, so once §2/§3 land, every Global surface
carries a T+1 frontier whenever cottonwood is inside its declared window — the clamp simply
never binds on the ordinary T+2 lag. It REMAINS in place and still binds when a freeze exceeds
the declared window (today's 07-30 instance — the bounded refusal that is the guard working).
It is NOT removed or loosened by this design absent Andrew's word.

## 6. HANDOFF — 0.5.0_AE_OpalETL implementation surface (cold-read section)

*You are implementing a small, additive change to two gold-staging producers. Everything you
need is in this section; the rest of the document is why.*

- **Repo/files:** `data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py` (Global scope path) and
  `data/mdpf/scripts/gold/dim_mdpf_account_distribution.py` (`--firm global` path). Deploy =
  `aws s3 cp` to `s3://opal-data-mdpf/code/scripts/gold/` (DS-cycle Rule 13; verify with
  `comp-pipescript deployed <script> --pipeline mdpf` = MATCH).
- **Input (the one new read):** the Global spine artifact
  `s3://opal-data-assets/gold/mdpf_revamp/global/aggregate_aua_timeseries.json` ALREADY
  carries the carry meta: per-point `carried_at_declared_cadence(as_of=...)` labels in
  `cohort_provenance` + `as_of_by_partner` (+ `meta.cottonwood_carry` policy block). Both
  producers already read this artifact — no new S3 permission, no new source.
- **Change per producer:** IMPORT (copy, never recompute) the spine's carry facts into a new
  additive `meta.interim` block `{carried_firms, as_of_by_partner, carried_dates_in_window}`;
  emit it ONLY when the spine's frontier includes carried points. Values/totals: UNCHANGED
  code paths (the carry is already in the values the producers read).
- **Do NOT:** derive a carry from observed landings (§4 law); touch per-firm artifacts
  (no-LOCF stands there); widen any window; touch the timeseries fold (live, §1); let
  anything into `by_model` from the Income residual meta (G8).
- **Acceptance (the marked-interim ROUND TRIP, on SCHEDULED cycles):**
  1. On a cycle where cottonwood is at T+2: Global aum-metrics + account-distribution emit
     `meta.interim` naming cottonwood + the carried as_of; values tie the spine to the cent
     (the existing tie law).
  2. On the next cycle where cottonwood's real value lands: the same dates' values are the
     REAL values and `meta.interim` no longer names them (natural overwrite, verified by
     comparing the two cycles' artifacts).
  3. The composition/vocabulary gates still fire on real-data roster changes (re-exercise
     the fef636c2-class refusal path once, on a fixture).
- **Contract statement you inherit (steady state):** cottonwood at T+2 inside its 3-TD
  declared window ⇒ carried on the T+1 tail ⇒ Global frontier at T+1 every day — **PROVIDED
  THE DAILY CHAIN RUNS.** The schedule dependency is REAL and is NOT yours: `mdpf-daily-
  trigger` fires on an event, not a schedule (NEVER#4 class; the 08-03 no-cycle gap is the
  measured instance) — named here and routed to CTO as adjacent debt, not absorbed.

## 7. Self-audit (TO phase-2)

Marking mechanism artifact-carried + reader-distinguishable (§2/§3: `meta.interim`, absent ==
none) ✔ · overwrite idempotent (natural rebuild, no special path) ✔ · lag rows declared-not-
inferred (§4, with the re-inference prohibition stated) ✔ · clamp interaction stated (§5,
edict stands) ✔ · 0.5.0_AE handoff cold-readable (§6, self-contained) ✔ · law dispositions
carried verbatim, not re-litigated (header) ✔ · citations @0a61583b2 or labeled; the §1
mechanism rows cite dim line ranges read this session; INFERRED remainder: none load-bearing.
