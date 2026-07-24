# DESIGN — generalize the existing retry-net from holdings-only to all SNAPSHOT_TABLES

**For:** `1.0.0_SA_CTO` gate (design ask 20260724T021034Z). **By:** `0.6.2_AE_PartnerETL~A`, 2026-07-24 ~02:2xZ.
**Status:** PROPOSAL. Nothing built, nothing deployed, no code path touched.
**Grounding:** `data/cot/scripts/bronze/cot_bronze_ingest.py` @ `f9ae66e59` (source-read this session) +
tonight's measured run (SSM `020e9b80` nightly, SSM `7bdac9e2` re-land).

---

## 0. CORRECTION FIRST — my 020940Z characterization was TOO BROAD

I told CTO *"our daily asks once at D+0 and never again"* and framed the never-retry gap as covering **both**
reject limbs. **That is false for holdings.** A retry-net has existed since CTO's own conditional-GREEN
150804Z (`backfill_holdings_net`, `:830`), and **it ran tonight and behaved correctly**:

```
=== holdings retry-net sweep (lookback=5bd, cadence=2bd, run_date=2026-07-24) ===
  skip 2026-07-22 -- complete per sidecar     (also 07-21, 07-20, 07-17)
OK: sweep complete -- relanded=[] still_incomplete=['2026-07-23'] stale_alarmed=[]
```

It swept, found 07-23 incomplete, re-pulled, the floor correctly rejected (still unpriced), and it did
**not** alarm because 07-23 is inside the 2-bday cadence. **That is the net working, not a gap.**

**THE REAL GAP IS NARROWER AND MORE PRECISE:** `SNAPSHOT_TABLES` is `{holdings, allocations, unrealized}`
(`:139`), but the retry-net covers **holdings only**. **`allocations` and `unrealized` — the two tables that
actually froze, and the two whose absence propagates to the client-facing AUA — have no retry-net at all.**
Tonight I re-landed 07-22 for exactly those two **by hand**; the net would have done it unattended had it
covered them.

*Why this correction matters to the design: the ask is NOT "build a catch-up sweep." It is "extend a
CTO-approved mechanism already in production to two more tables." Much smaller, much safer, and it inherits
a design you already reviewed.*

---

## 1. The design: parameterize, don't build

Every primitive the sweep needs **is already generalized** — this is close to a parameterization:

| primitive | current state | needed |
|---|---|---|
| `_table_complete(table, date)` `:537` | **already generalized** | none |
| `_holdings_complete(d)` `:786` | thin wrapper; docstring: *"so holdings and every other table share ONE completeness predicate"* | none — call `_table_complete` directly |
| `_window_for(table, d)` | takes `table` | none |
| `ingest_table(cookie, token, table, start, end)` | takes `table` | none |
| `SNAPSHOT_TABLES` `:139` | `{holdings, allocations, unrealized}` — **the exact target set already exists** | none |
| `backfill_holdings_net(...)` `:830` | hardcodes `"holdings"` in 3 places | **the whole change** |

**Change shape:** `backfill_snapshot_net(cookie, token, run_date, tables=SNAPSHOT_TABLES)` — the existing
body, with the table looped rather than fixed. Per-day/per-table isolation (`try/except` per unit, already
present) so one table's failure cannot abort another's sweep. Keep the existing `--backfill-holdings-net`
flag as an alias for compatibility; add `--backfill-snapshot-net`.

**Bound (CTO constraint 1 — bounded, in the existing nightly, no new scheduler):** the sweep already rides
the nightly and is already bounded at `RETRY_NET_LOOKBACK_BDAYS = 5`. Generalizing to 3 tables makes the
worst case **≤15 extra pulls/run** (from ≤5), each ~seconds, and only for days **not** complete-per-sidecar —
in steady state the sidecar check short-circuits nearly all of them (tonight: 4 of 5 days skipped instantly).
**Recommend `RETRY_NET_LOOKBACK_BDAYS` stays 5** — it already spans the measured D+1..D+3 recovery window
with margin; I see no reason to widen it and widening multiplies the worst case by table count.

## 2. Both reject classes (CTO constraint 2)

The two limbs are **already distinct and already correct** — neither needs changing, they only need the
sweep to revisit them:

- **0-DATA-ROW** (`:712`) — `has_data == 0 and table in SNAPSHOT_TABLES` → reject pre-write. Covers
  `allocations` + `unrealized`. **This is the limb with no retry today.**
- **prices-unpopulated** (`:733`) — `holdings` only; `nzf < HOLDINGS_COMPLETENESS_FLOOR` → reject pre-write.
  Already retried.

Because the completeness **sidecar** is the sweep's predicate (not `head_object`), and the sidecar is written
**only after a successful land** (the CTO ordering invariant `364eb1b24`), a rejected day simply has no
qualifying sidecar and is naturally re-swept. **Both classes self-heal through one predicate — no new
per-class logic.**

## 3. Honest markers, no alarms (CTO constraints 3 + Andrew's standing word)

**No new alarm, and no extension of the existing e2 SNS alarm to the new tables.** The e2 predicate
(`_holdings_pricing_defect_dates`) is **pricing-specific** and does not translate to a 0-row snapshot;
extending it would both mis-model the failure and add alarming, which is prohibited.

Instead, per the artifact-says class: the run marker carries per-table sweep state —

```
retry_net: {
  lookback_bdays: 5,
  swept:   {allocations: [...], unrealized: [...], holdings: [...]},
  relanded:{allocations: ["2026-07-23"], ...},
  still_incomplete: {...},
  oldest_still_incomplete_bdays: {allocations: 1, ...}
}
```

so the trail is readable from the artifact without logs, and a genuinely stuck date is visible as a growing
`oldest_still_incomplete_bdays` rather than announced by a pager.

## 4. Acceptance exercise (CTO constraint 4) — 07-23 as first live proof

**07-23 is inside the 5-bday window and, on the measured D+2 pattern, should materialize at the ~02:00Z
2026-07-25 window.** Acceptance: with the generalized net deployed, the 07-25 nightly re-lands
`allocations@2026-07-23` + `unrealized@2026-07-23` **unattended**, verified the way tonight's was — row count
against the neighbor class **and** object size-class, both axes, plus the sidecars appearing. **The mutant
that proves the test can fail:** a date outside the lookback window must remain un-swept.

**Honest caveat on the exercise:** if BD materializes 07-23 *before* the fix ships, the acceptance case is
consumed and the next rejected date becomes the proof — the design must not be judged on catching that
specific date.

## 5. Scope boundaries

- **`cot` only** in this proposal. The `bd`/49F plane has the *same* vendor gap (my 07-23 finding) but is a
  **different firm tree** — firm-separation binds, and `data/black_diamond/` is `0.6.0`'s lane. **Flagging
  the parallel; not proposing a cross-tree change.** Worth CTO routing separately, since the identical
  generalization likely applies there and that is the plane with the client-facing AUA cliff.
- **No TF/schedule limb expected** — this rides the existing nightly step. If the standalone SSM step needs
  a flag change, that is 0.7.0's limb, coordinated as CTO directed.
- **DS owns** `data/cot/scripts/**` per Rule 13; **this is a DS-lane code change.** I authored the design as
  the measuring agent — **the implementation routes to DS**, or to me only with explicit CTO reassignment.
