# SHAPE (d) — consumer-side discrimination for pre-guard 0-row bronze objects

**For:** `1.0.0_SA_CTO` (item (d), ruled 20260724T133901Z: *separate item, and DO NOT TOUCH BRONZE*).
**By:** `0.6.2_AE_PartnerETL~A`, 2026-07-24 ~1430Z. **Status:** SHAPE + a completed census. Nothing changed.
**Binding constraint accepted:** **BRONZE IS RAW AND UNTOUCHED** (CLAUDE.md 17a). No delete, no overwrite, no
"cleaning." The remedy lives entirely outside bronze. I am not proposing a bronze mutation.

---

## 0. The census — and how far the estimate moved as the instrument sharpened

I probed **every** `allocations` + `unrealized` object in `opal-data-cot/forwardfill_v2/` (n=86 each, 172 total)
with `_export_has_data_rows` from the **deployed** module. Zero unparseable.

| instrument | allocations "affected" | note |
|---|---|---|
| **size screen** (`< 50,000 B`) | **52** | my first pass — **wrong by 62%** |
| **content probe** (`_export_has_data_rows == 0`) | **32** | the actual 0-row population |
| **+ trading-calendar classification** | **10** | the genuine anomaly class |

**A 5× narrowing from screen to finding.** Size is not rows — the codebase says so at
`_export_has_data_rows:738-742` and I proved it against myself. *(For the record the two classes do separate
cleanly in hindsight — 0-row tops out at 4,305 B / 3,744 B, smallest with-rows is 5,629 B / 4,788 B — but that
boundary was **only knowable after probing**, and my 50,000 B guess sat nowhere near it.)*

### The classification (NEVER#1 — resolve the calendar before calling anything a defect)

32 zero-row as-of dates, **identical set for both tables** (0 dates differ — itself evidence of a common cause):

- **20 WEEKEND** — a point-in-time snapshot legitimately does not exist on a non-trading day.
- **2 US HOLIDAY** — `2026-05-25` (Memorial Day), `2026-07-03` (July 4 observed).
- **10 BUSINESS DAY** ← **the only genuine anomaly class**:
  `06-22 Mon, 06-23 Tue, 06-26 Fri, 06-29 Mon, 06-30 Tue, 07-01 Wed, 07-02 Thu, 07-06 Mon, 07-07 Tue, 07-08 Wed`

**They stop at 2026-07-08. The empty-export guard shipped 2026-07-09 (`9d44d6af5`). Nothing has landed a stub
since. The guard works** — this is a bounded historical population, not an ongoing leak.

### ⚠ The control that partially falsified my own classification

I ran the inverse check — *do any WITH-ROWS objects fall on a weekend?* — and **two do: `2026-06-20` (Sat) and
`2026-06-21` (Sun).** So BD **sometimes** serves a data-bearing weekend export. **"Weekend ⇒ legitimately
empty" is therefore a strong presumption, not a definition,** and the registry must record it as a
*classification with a stated basis*, never as a proven-benign verdict. Had I not run the inverse control I
would have shipped 22 dates labelled definitively-benign on an assumption with live counterexamples.

---

## 1. The shape

A **consumer-side registry** — an artifact *outside* bronze that names the affected keys, so a reader can
discriminate. Bronze bytes are never touched.

**Location:** `s3://opal-data-cot/quarantine/bronze_zero_row_registry.json` (a **new** prefix — not under
`bronze/`, not under `forwardfill_v2/`, so it cannot be mistaken for data and cannot be picked up by any
table-resolving consumer). Committed to the repo as the source of truth and deployed as an artifact.

```json
{
  "schema_version": 1,
  "generated_at": "...", "generated_by": "...", "method": "_export_has_data_rows @545bde4e9 over 172 objects",
  "bucket": "opal-data-cot", "prefix": "forwardfill_v2/",
  "denominator": {"objects_probed": 172, "unparseable": 0},
  "entries": [
    {"table": "allocations", "as_of": "2026-07-08",
     "key": "forwardfill_v2/allocations/ALLOCATIONS_DAILY_2026-07-08.xlsx",
     "bytes": 4304, "data_rows": 0,
     "classification": "BUSINESS_DAY_ANOMALY",          // | NON_TRADING_DAY_PRESUMED_BENIGN
     "classification_basis": "weekday, not in US market holiday set",
     "landed_before_guard": true, "guard_commit": "9ae66e59/9d44d6af5"}
  ]
}
```

**`classification` is the field a consumer rejects on** — the same rule CTO gated twice today (`basis` on the
sidecar, `basis` on the AUA). `NON_TRADING_DAY_PRESUMED_BENIGN` deliberately says *presumed*, because of the
06-20/06-21 counterexamples.

### What consumes it

**Nothing automatically, at first.** The registry's first job is to *exist* and be citable — today an
0-row pre-guard object is indistinguishable from real data on every existence/freshness check we own, so the
minimum viable fix is a discriminator a human or a script can consult. A silver-side read that skips
`BUSINESS_DAY_ANOMALY` keys is the obvious follow-on, but it is a **separate change with its own gate** and I
am not bundling it.

---

## 2. Why not the alternatives

- **Delete/overwrite the stubs** — forbidden (17a), and it would destroy the evidence that the pre-guard era
  happened. **Not proposed.**
- **Backfill them from BD** — these are as-ofs BD may still not have; a re-pull would just 0-row-reject now that
  the guard exists. It would also be an ad-hoc vendor pull outside the standing grant.
- **Derive it live in each consumer** — that is the re-derivation-at-each-consumer pattern that produced today's
  three-basis AUA divergence. **Decide once, carry the label.**
- **A sentinel/alarm on stub detection** — prohibited (Andrew standing, *"no more sentinels and alarms"*), and
  pointless for a closed historical population.

---

## 3. Acceptance

1. Registry regenerated from a clean run reproduces **exactly** 32 entries / 10 `BUSINESS_DAY_ANOMALY`
   (determinism).
2. **Positive control:** a known-good key (e.g. `allocations@2026-07-22`, 342,860 B, rows > 0) is **absent** from
   the registry. A registry that lists everything discriminates nothing.
3. **Negative control:** a known 0-row key (`allocations@2026-07-08`) **is** present with `data_rows: 0`.
4. **MUTANT:** replace the content probe with a size threshold → the entry count must change (52 vs 32),
   proving the registry is content-determined and not size-determined.
5. The generator states its **denominator** (objects probed) in the artifact, so a future reader can tell a
   complete scan from a partial one.

---

## 4. Scope + honest bounds

- **`cot` tree only**, `allocations` + `unrealized` only. I did **not** probe `holdings`, `transactions`, or
  `realized` — holdings has a floor guard and the two PERIOD tables legitimately return 0 rows over a
  non-trading window, so the same probe would mean something different there. **Not claiming this is the whole
  bronze surface.**
- The `bd`/49F tree very likely has an equivalent pre-guard population (same vendor, same guard date, same
  code). **Firm separation binds and `data/black_diamond/` is `0.6.0`'s lane — flagging, not proposing.**
- Raw census retained at `scratchpad/stub_census.json` (per-object: as-of, key, bytes, probe result).
- **Andrew's standing scope note applies and I am honoring it:** validation is scoped to the serve window
  (2024-11+); this is a 2026 population, so it is in scope — but the ≤2026-06-19 weekend entries are
  *labelling*, not archaeology, and I am not investigating why any individual pre-guard date is empty.
