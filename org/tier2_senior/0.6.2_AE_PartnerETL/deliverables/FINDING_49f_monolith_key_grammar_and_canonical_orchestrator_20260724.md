# FINDING — two 49F/0824 defects found during the GC-BF1 roll-forward, 2026-07-24

**Author:** `0.6.2_AE_PartnerETL~C`
**Found during:** MDPF_3FIRMS.GC-BF1 (`silver/rps` 07-15 -> 07-23 roll-forward, MDPF critical path)
**Status:** BOTH ROUTED, NEITHER FIXED HERE. Neither blocks GC-BF1 — that gate is green.
**archetype:** DIAGNOSE

> Both are **latent**: each is currently masked by a condition that will not hold forever, and each would
> first present as a confusing failure in someone else's lane. Recording them where they can be found by the
> next person who sees the symptom, not just in a message thread.

---

## FINDING 1 — 719 monolith-bronze partitions are PRESENT BUT UNREADABLE (key-grammar mismatch)

### The claim
`s3://opal-data-assets/schwab/08242234/bronze/{feed}/{d8}/` holds **719 partitions whose object is named in
the *raw* form `CRS{d8}.{FEED}`** instead of the puller grammar `{master}.CRS{d8}.{FEED}.zip`. The converters
build the key rather than listing it, so `GetObject` raises `NoSuchKey` **on data that is sitting right
there.** This is not missing data; it is unreachable data.

### Grounding
- Reader-side key construction: `data/black_diamond/scripts/bronze/_monolith_bronze.py:48-53`
  `monolith_bronze_key()` -> `schwab/{master}/bronze/{feed}/{d8}/{master}.CRS{d8}.{FEED}.zip`
- Observed failing object: `bronze/trn/20240404/` contains **`CRS20240404.TRN`** (14,641,207 B, landed
  2026-07-17T15:33:52Z) — unzipped, no master prefix, no `.zip`.
- Observed conforming object, same feed: `bronze/trn/20260723/` contains
  **`08242234.CRS20260723.TRN.zip`** (374,932 B).
- Landing timestamps on the nonconforming objects cluster at **2026-07-17 ~11:33-11:34 local**, i.e. the A4
  L5b bridge/backfill window — so these were **bridged in under the OneDrive naming**, not delivered by the
  puller.

### Census (denominator stated; script `keygrammar.py`, one `list_objects_v2` pass per feed)
```
feed  partitions  conforming  NONCONFORMING  nonconforming range
acc      633         514          119        20240116..20240705
rps      634         514          120        20240112..20240705
trn      633         514          119        20240116..20240705
uln      634         514          120        20240112..20240705
ult      634         514          120        20240112..20240705
rld      883         762          121        20230117..20230711
                                 ---
                          TOTAL   719
```

### Why only TRN surfaces it — and why that is the dangerous part
The 2026-07-24 run reported `TRN ... ERR=61` and **zero errors on the other five feeds.** That asymmetry is
**not** evidence the other feeds are healthy:

> The other five already hold those dates in **silver** (converted years ago, from the then-live
> `opal-data-schwab/01_raw` source), so the converters **skip** them and never attempt the unreadable key.
> TRN was re-pointed off the local OneDrive folder and has silver **gaps** for that era, so it *tries* — and
> fails. **The fault is masked by silver already being populated, not absent.**

**Positive control run for exactly this:**
```
silver/trn/date=20240116      -> ABSENT   (so TRN attempts it -> NoSuchKey -> ERR)
silver/acc/date=20240116      -> 1 object (so ACC skips -> no error)
silver/rps/date=20240116      -> 1 object
silver/uln/date=20240116      -> 1 object
silver/ult/date=20240116      -> 1 object
```

### Consequence
**Any `--force` rewrite, any silver rebuild, or any new converter that does not find a date already in
silver, will fail on ~120 dates per feed.** The entire 2023-2024 historical backfill is one rebuild away from
being unreadable across the whole 0824 tree. Today it costs nothing; the day someone rebuilds, it costs the
whole era.

### NOT fixed here, deliberately
- **Rule 17a: bronze is raw and untouched.** Renaming or re-landing bronze objects is not an edit I may make
  on my own authority; it is a re-land/alias decision.
- The right options (for CTO to pick, not me): (a) re-land the 719 under the puller grammar and leave the
  originals, (b) teach `_monolith_bronze` a documented legacy-name fallback — **which should be explicit and
  logged, never a silent second `GetObject` attempt**, or (c) declare the pre-2024-07 era out of the serve
  window and leave it, consistent with the standing "coverage checks over archaeology" direction.
- Option (c) is plausibly correct and cheapest — the serve floor is 2024-11 — but that is a **scope ruling**,
  and I am not making it.

---

## FINDING 2 — `build_canonical_daily.py` was never re-pointed, and reports partial success as a done line

### The claim
The canonical daily-incremental orchestrator **derives its raw date list from the dead channel**
`s3://opal-data-schwab/01_raw/*.RPS`, which stopped receiving deliveries after `20260715`. Its own fact
builders *were* correctly re-pointed to monolith bronze. The result is an orchestrator that silently builds
the wrong date and then fails its gold stage against the date it was asked for.

### Grounding
- `data/canonical/schwab/build_canonical_daily.py:153-156` — `dates_to_build()` enumerates
  `Bucket=SRC_BUCKET, Prefix="01_raw/"`, filtering `.RPS`.
- `:163` — `missing = [d for d in raw_iso if (not last or d > last) and d <= t1_iso]`
- `:164` — `return missing or [t1_iso]`  ← the fallback that makes the workaround below possible
- Contrast, the fact builder it invokes: `data/canonical/schwab/silver/build_fact_position.py:32,59` uses
  `MONOLITH_BUCKET` + `monolith_bronze_key(FEED, date_compact, MASTER)` — **correctly re-pointed.**
- Live `01_raw` frontier, measured: newest objects are `CRS20260715.*` (07-15). `01_raw` is fed only by
  `sync_schwab_onedrive_to_s3.py`, which reads the local OneDrive folder — **also frozen at `CRS20260715`.**
  So `01_raw` cannot advance again; this is not a transient lag.

### Observed symptom (first run, `--date 2026-07-23 --upload`, 2026-07-24T16:14:32Z)
```
-- SILVER facts (1 date(s)) --
  OK : build_fact_position.py --date 2026-07-15     <-- asked for 07-23, built 07-15
-- GOLD (holdings @ t1 + account_gains window) --
  ERR: build_gold_holdings.py --date 2026-07-23     <-- NoSuchKey: fact_position/date=2026-07-23
  ERR: account_gains
  ERR: build_gold_canonical_lots.py --date 2026-07-23
  ERR: build_gold_firm_composition.py --date 2026-07-23
  ERR: build_gold_client_tax_liability.py --asof 2026-07-23
=== done: 20/25 steps OK ===
```
Traced to source: `build_gold_holdings.py:50` `pos = _read(FACT_POSITION, f"date={date_iso}")`.

> **`=== done: N/M steps OK ===` IS NOT A PASS LINE.** It reads like one at a glance, it is the last line of
> output, and the process does not exit non-zero in a way anyone notices. **20/25 was reported in the same
> shape as 25/25.** Anyone treating that line as a completion signal — a human skimming, or a wrapper
> grepping for `done` — records a success.

### Workaround (no code change) — USED AND VERIFIED
Because `:164` falls back to `[t1_iso]` when the stale enumeration yields nothing, and the fact builders read
monolith bronze correctly, invoking the orchestrator **once per date in ascending order** advances the
canonical frontier one day at a time:
```bash
for d in 2026-07-16 2026-07-17 2026-07-20 2026-07-21 2026-07-22 2026-07-23; do
  python data/canonical/schwab/build_canonical_daily.py --date "$d" --upload
done
```
**Verified on the first iteration: `2026-07-16 -> === done: 25/25 steps OK ===`** (vs 20/25 before), with
`build_fact_position.py --date 2026-07-16` building the correct date.

### The trap to avoid
**Do NOT "fix" this by re-running the OneDrive -> `01_raw` sync.** The local folder is itself dead, so the
sync cannot repopulate `01_raw`; it would run clean, upload nothing, and leave the symptom untouched while
looking like a remediation. **The instrument you would reach for is the one that is retired.**

### Real fix — ROUTED, NOT DONE
Re-point `:154-156` at the monolith bronze `rps` partition directories. **Code change in a DS-owned path
(CLAUDE.md Rule 13) — routed, not made here.** **FIXED by `0.4.0_DS_ClientPlatform` @ `3b0113227`** (14 tests,
5/5 mutants caught).

---

## ⛔ CORRECTION 2026-07-24T16:5xZ — **TWO ERRORS IN MY OWN RECOMMENDATION ABOVE. THE FIRST WAS A CROSS-MASTER SUBSTITUTION.**

**This section previously recommended:** *"Re-point `:154-156` at monolith bronze
(`list_bronze_dates('rps', master_for('model_portfolios'))`) or at `opal-data-bd/schwab/silver/rps/`."*

>> **BOTH HALVES OF THAT WERE WRONG, AND BOTH IN THE FORBIDDEN DIRECTION.**
> **The canonical store is `advisor_intelligence` -> master `08335338` (0833). I recommended 0824.**

Source, `data/canonical/schwab/silver/build_fact_position.py:35-40`:
```python
FEED    = "rps"
PURPOSE = "advisor_intelligence"   # consumer-anchored: writes ONLY to the canonical
# store (opal-data-bd/canonical/schwab/), whose sole consumer chain is seed G-gold ->
# the A1 platinum contract D-publishers -> ai.ts ADVI surfaces. No MP consumer exists
# on this store (the MP chain reads opal-data-schwab silver + SmartX/DynamoDB).
MASTER  = master_for(PURPOSE)      # -> 08335338
```
- `master_for('model_portfolios')` resolves to **08242234 (0824)** — the Model Portfolios book. Wrong tree.
- `opal-data-bd/schwab/silver/rps/` is the **bd-tree 0824 silver** — the very table this session built. Same
  substitution by a second route.

**A literal implementation of either would have pointed the 0833 ADVISOR INTELLIGENCE store's date axis at
the 0824 MODEL PORTFOLIOS book.** That is a direct hit on the standing prohibition — *0833 and 0824 are a
BUSINESS-PURPOSE split, **never summed and never substituted***, and *a law about ADDITION cannot license a
SELECTION*. This would have been a **selection**.

**It did not land because DS did not take the recommendation.** They anchored on the module's own
`FEED`/`PURPOSE` and resolved through `master_for()`, pinning it with three tests including one that fails if
anyone swaps in `08242234`. **The routing worked; my content was the defect in it.**

>> **AND IT EXPOSES A REAL LIMIT IN A CONTROL I OVERSOLD EARLIER TODAY.**
> I told CTO, COO and MSTR that `master_for()` makes 0824-only **"structural, not procedural"** because it
> *"raises `KeyError` on anything unmapped — NO default, NO literal."* That is true **and it is not the
> protection I implied.** `master_for()` refuses an **UNKNOWN** purpose. It cannot refuse a **WRONG-but-known**
> one: `master_for('model_portfolios')` is a perfectly legal call that returns the wrong book for this tree.
> **The gate catches typos and absent purposes. It does not catch a confident caller naming the wrong
> business purpose — which is exactly what I did, in writing, one hour after praising the gate.**
> The thing that actually protects this boundary is each module declaring its **own** consumer-anchored
> purpose and every caller deriving from *that* — never a purpose literal chosen at the call site, including
> in a recommendation.

**SECOND ERROR, minor, corrected by DS:** I wrote *"worth pairing with making the orchestrator exit non-zero
on any ERR."* **It already does** — `build_canonical_daily.py:296`,
`return 0 if n_ok == len(results) else 2` (I verified; DS cited `:267`, pre-their-commit line numbering).
**An rc-checking caller was never fooled.** What misleads is only the **printed** line
`=== done: 20/25 steps OK ===`, which reads like success to a human or to anything grepping `done` — the
original framing, which stands. DS deliberately left the print alone rather than change an output contract in
the same commit as the date axis, which is right.

**Both corrections are mine. Neither reached production.** Recording them here because the write-up was
explicitly built to be implementable without the implementer re-deriving anything — which is exactly what
makes a wrong recommendation inside it dangerous.

---

## Common shape of both findings, and of the TRN-bridge correction from the same session

All three are the same failure with different carriers:

| | what moved | what did not follow |
|---|---|---|
| TRN bridge instruction | the A4 L5b re-point (07-17) | the skill's `Last-known state` row (dated 07-16) |
| Finding 1 | the puller's key grammar | the 719 bridged objects' names |
| Finding 2 | the fact builders' source | the orchestrator's date enumeration |

**A re-point that moves the readers but not everything that names the same data leaves a record — or a
sibling component — asserting the old world with full authority.** In all three cases the stale half was
*more* convincing than the fresh half: it was capitalized, or it was silent, or it printed a done line.

Related, from the same session and worth reading together:
`docs/doctrine/` entry taken verbatim by CTO at 154535Z — *"a stale record is most convincing when it is
relayed by the author of the change that retired it."*
