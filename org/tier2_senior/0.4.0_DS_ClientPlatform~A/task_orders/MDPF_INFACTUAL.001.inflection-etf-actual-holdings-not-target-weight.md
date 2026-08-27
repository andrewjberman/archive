# BRIEFING / TASK ORDER -- INFLECTION ETF HOLDINGS: USE THE ACTUAL VALUE

**Issued to:** `0.4.0_DS_ClientPlatform~A`
**Issued by:** `2.0.0_SA_COO` · 2026-07-29
**Authority:** Andrew-direct ~2144Z (recorded verbatim @`11599d60f4`) + Andrew-direct ~0016Z (this briefing)
**Arch gate:** `1.0.0_SA_CTO` · **Status:** `<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "MDPF_INFACTUAL" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending</status>`

---

## 1. THE ASK, IN ONE LINE

**Andrew-direct, verbatim:**
> *"there is absolutely no excuse for any kind of interpolation or estimation when it comes to asset
> valuation; that is a raw pull."*
> *"I dont want to stack more numbers and processes, i want it to simply use the actual value, not a target
> value or a theoretical value."*

**Inflection's holdings of the four Opal ETFs are currently ESTIMATED from model target weights. Replace
that with the measured position value. Nothing else.**

---

## 2. WHAT IS WRONG TODAY (MEASURED)

Served artifact `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/{date}.json`:
```
attribution_basis: "rps_actual:49financial;target_weight:inflection"
```
- **49financial** -> `held` comes from **real Schwab-RPS positions**. Correct.
- **inflection** -> `held` = `model_aua x target_weight`. **An inference from INTENT, not an observation.**

Measured 2026-07-28, inflection held (estimated): DIVZ 18,382,174.73 · IDVZ 17,367,784.99 ·
PFDE 14,300,934.55 · PFOE 8,215,381.40 = **$58,266,275.67**.

**The estimator's own bias is documented** (`data/mdpf/scripts/feeders/HANDOFF_DSA_wsd2_aggregator_wire.md:18`):
> *"model_aua x target_weight, which runs ~1-3% HIGH and OVER-ATTRIBUTES PFOE"*

**So the served number is knowingly ~$0.6-1.7mm high, daily, on a quantity we can compute exactly.**

**Why it was left this way (NOT a defect of anyone's care):** WS-D.2 shipped the real-holdings override for
49financial and explicitly deferred inflection on a **materiality** argument (`:114`, *"small: ~$8M PFOE /
~$10M PFDE"*). **Andrew's rule replaces that materiality test with a SOURCE test: "we have the endpoints" is
the whole argument, and the size of the number does not enter it.** The threshold was reasonable when set
and silently expired as the exposure grew to ~$58mm.

---

## 3. ⚠ DO NOT BUILD NEW MACHINERY -- THE OVERRIDE PATH ALREADY EXISTS AND ALREADY EXPECTS YOU

**This is the load-bearing instruction and it is what makes the ask "no new numbers, no new processes."**

`HANDOFF_DSA_wsd2_aggregator_wire.md` -- the design that shipped the 49F override -- **already names this
exact task and states the aggregator needs no change:**
> *"A WS-C Eclipse-positions feeder would emit `partner_held_etf` rows for `firm_id=inflection` and **the
> same override path picks them up -- no further aggregator change needed.**"*

The consuming code is already generic:
```python
# build_etf_decomposition -- existing, unchanged
for firm_id in set(held_by_partner) | {f for (f, t) in partner_held if t == etf}:
    if (firm_id, etf) in partner_held:
        held_by_partner[firm_id] = partner_held[(firm_id, etf)]
```
It is keyed `(firm_id, ticker) -> held_value` and is **firm-agnostic**. It already overrides 49financial.
**Feed it inflection rows and it overrides inflection.**

>> **THEREFORE THE DELIVERABLE IS ONE FEEDER, NOT AN AGGREGATOR EDIT.** << And that matters for a second
reason: `mdpf_aggregate_aua.py` is the **LEGACY** producer, and CTO's Ruling 1 holds legacy untouched
(no diagnosis, no point-fixes) until the cutover. **A feeder is PURE-ADD and does not breach it.** If your
implementation finds itself editing the aggregator, **STOP and route to CTO** -- that is a different
decision.

---

## 4. THE SOURCE -- FACT TABLES IN `opal-data-assets`

**PRIMARY (measured, T-0 fresh, already in the monolith -- no vendor call required):**
```
s3://opal-data-assets/orion/inflection/silver/fact_assets/date={YYYY-MM-DD}/data.parquet
   2,283 daily partitions · newest date=2026-07-28 · ~35,098 rows · 64 cols
   COLUMNS YOU NEED: ticker · currentValue · currentShares · currentPrice · isin
                     accountNumber · accountId · clientId · asOfDate · snapshot_date
```
*(Schema independently verified by `1.0.0_SA_CTO` on the 2026-07-28 partition.)*

**⚠ TWO SOURCE CAVEATS -- resolve BOTH before you build, do not inherit them:**
1. **The handoff doc says "Eclipse-positions"; the measured ticker-level holdings are in ORION
   `fact_assets`.** In this estate **eclipse = inflection MODEL** (`fact_portfolios_full`), **orion =
   inflection CUSTODY**. ETF holdings are a custody quantity. **Verify which table actually carries
   ticker-level position values before wiring -- the doc predates the orion source and may be stale.**
2. **`fact_assets` vs `fact_positions`** -- both exist under that silver prefix. **My earlier measurement
   attributed 2,283 partitions to `fact_positions` and a subagent corrected it to `fact_assets`.
   ENUMERATE the prefix and confirm which carries `ticker` + `currentValue`. Do not construct the path.**

**SIBLING PATTERN TO MIRROR (49F, already working):** the `partner_held_etf` feeder for 49financial reads
Schwab RPS silver and emits `(firm_id, ticker, held_value, as_of)` rows. **Mirror its shape exactly** --
same feeder contract, same columns, different source table.

---

## 5. THE CALCULATION

**Per (date, ticker), the actual held value is a sum over positions. That is the whole computation:**
```
held_value(inflection, TICKER, D) = SUM(currentValue)
                                    FROM orion/inflection/silver/fact_assets/date=D
                                    WHERE ticker == TICKER
```
for `TICKER in {DIVZ, IDVZ, PFDE, PFOE}` (confirm the canonical ticker set against the existing ETF
roster rather than hardcoding this list).

**No weights. No ratios. No model composition. No fallback to intent.**

**Emit one row per `(firm_id='inflection', ticker, date)` with `held_value` and the source partition
recorded**, matching the existing feeder's column contract. The aggregator's roll-forward/`_date_used`
convention already exists -- **follow it, do not invent a second one.**

---

## 6. NON-NEGOTIABLES

1. **NEVER fall back to `target_weight` silently.** If a position partition is missing for a date, emit
   **NO ROW** -- the aggregator's existing behaviour is to fall back to the estimate, and the
   `attribution_basis` string will then honestly say so. **An absent measurement must never be laundered
   into an estimate wearing a measured label.**
2. **The `attribution_basis` string MUST change** for dates where the override applies -- e.g.
   `"rps_actual:49financial;positions_actual:inflection"`. **A consumer must be able to tell measured from
   estimated per firm per ticker.** This is the disclosure contract; do not drop it.
3. **Do not backfill history from weights.** Apply the actual value **only** where position data exists.
   Where it does not, the estimate remains and remains labelled. **(This is the same distinction Andrew drew
   for Cottonwood: interpolation is forbidden where a source EXISTS, sanctioned and labelled where none
   does. Inflection positions exist from the partition floor forward -- establish that floor and state it.)**
4. **Bronze is raw; silver is dedup + dtype only.** This is a feeder reading silver -> emitting a feeder
   artifact. **No business logic in silver** (CLAUDE.md Rule 17).
5. **`from __future__ import annotations`** at the top of every gold/silver/bronze `.py` (Rule 15).

---

## 7. ACCEPTANCE -- machine-checkable

1. **`attribution_basis` flips** to name inflection as measured, for every date with position coverage.
2. **The inflection held values MOVE DOWN ~1-3%** vs the estimate, with **PFOE moving most** -- the
   documented bias direction. **A move UP, or a move of the wrong magnitude, means the join is wrong** --
   investigate, do not accept.
   *Current estimated baseline to diff against (2026-07-28): DIVZ 18,382,174.73 · IDVZ 17,367,784.99 ·
   PFDE 14,300,934.55 · PFOE 8,215,381.40 · total 58,266,275.67.*
3. **`verify_wsd2_clears_identity2.py` still passes** and the aggregate reconciliation is `PASS`.
4. **Run the existing acceptance from the handoff doc**, unchanged:
   `python data/mdpf/scripts/gold/mdpf_aggregate_aua.py --date <D> --source s3 --dry-run` -> exit 0.
5. **FULL-AXIS DIFF, not a spot check.** Diff every shared date of the produced artifact against the
   current one and **name every mover**. Tonight a region-scoped check cleared a serve-affecting change
   three separate times; **an unexplained mover is a STOP.**
6. **Print the DENOMINATOR** of the position scan (rows, accounts, dates) and the **PREDICATE** (the exact
   ticker filter). A zero needs a positive control.

---

## 8. WHAT IS EXPLICITLY OUT OF SCOPE

- **No aggregator edit** (see §3). No legacy diagnosis or point-fixes (CTO Ruling 1).
- **No alarms, monitors, freshness checkers or notifications** -- standing moratorium, CLAUDE.md NEVER
  section @`638cf6c36`.
- **No re-phasing of any schedule.** Cadence work is WO-4c/WO-5 and is not yours.
- **The 49financial leg is already correct** -- do not touch it.
- **No deploy, no apply.** Commit and route; the apply gate is CTO's and the tree is under a freeze.

---

## 9. COMPILER TOOLS MANDATE

**Phase 1 (before write):** `comp-pipescript io mdpf_aggregate_aua.py` -- expect the feeder READS and the
`partner_held_etf` contract; **if the override path does NOT appear, STOP and route to COO** (the premise of
§3 is then false). `comp-grep "partner_held_etf"` -- expect the 49F feeder + the aggregator consumer;
**print the scanned denominator.**
**Phase 2 (before commit):** `comp-validate` on the produced artifact -- `NO_CONFIG`/`ZERO_CHECKS` means
UNVALIDATED, never signal safe.
**Phase 3 (after commit):** `comp-blast` on the new feeder -- expect no consumers beyond the aggregator; a
new downstream node means someone wired it mid-flight, surface it.

---

## 10. REPORT BACK

To **`2.0.0_SA_COO`** (issuer) + **`1.0.0_SA_CTO`** (arch gate), with: the resolved source table (§4
caveats settled), the four before/after values, the `attribution_basis` string, the full-axis diff with
every mover named, and the denominator/predicate of your scan.

**Commit; do NOT push** -- COO is push operator (Andrew ~1600Z 2026-07-24, `org/ref/PUSH_OPERATOR_PROCESS.md`).

-- `2.0.0_SA_COO`
