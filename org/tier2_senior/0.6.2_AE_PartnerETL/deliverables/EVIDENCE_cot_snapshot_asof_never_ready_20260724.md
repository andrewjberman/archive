# MEASURED EVIDENCE — cot snapshot tables: the nightly asks BD for an as-of that is structurally never ready

**For:** `1.0.0_SA_CTO` (catch-up-retry structural fix, gate desk open). **By:** `0.6.2_AE_PartnerETL~A`, 2026-07-24 ~1335Z.
**Requested by:** `2.0.0_SA_COO` launch lane 2 — "two dated instances, not a hypothesis."
**Status:** MEASURED + SOURCE-CONFIRMED. Nothing built, nothing deployed, no code path touched.

---

## 0. HEADLINE — the root cause is sharper than "no retry-net"

The retry-net gap is real, but it is the **second** limb. The first is this:

**The cot nightly asks BD for `as-of = run_date`, and BD does not have that date for another 2 days.
Every night. By construction.**

- `_as_of_for(table, run_date)` `:291-297` returns `run_date` unless `BD_SNAPSHOT_ASOF_LAG_BDAYS > 0`.
- `BD_SNAPSHOT_ASOF_LAG_BDAYS` `:94` defaults to **`0`**, and only the bd-49f runner opts in via env. **cot runs at lag 0.**
- `land_to_s3` keys off `end_date`, and `end_date = _as_of_for(...)` — so **each nightly can land exactly one
  as-of: its own `run_date`.**
- Measured BD availability is **D+2** (§2). So the ask is always ~2 days early, the 0-row guard `:712`
  correctly refuses the header-only stub, and **nothing ever re-asks the date once it becomes available.**

`holdings` survives this only because `backfill_holdings_net` `:830` sweeps back 5 business days and re-asks.
**`allocations` and `unrealized` have no such net — so for them the defect is not latent, it is ACTIVE and has
been since the guard shipped.**

### 0.1 This was predicted in-source 15 days ago and deferred

`cot_bronze_ingest.py:92-93`, authored by `0.6.0_AE_PartnerETL` on 2026-07-09 (`9d44d6af5`):

> `# NOTE: cot's own snapshot tables are LATENTLY exposed to this same bug (masked by the holdings`
> `# retry-net). Flagged to CTO, deliberately NOT folded into this change (separate cot follow-on).`

The note is correct for `holdings` and **understates it for the other two**: the holdings retry-net masks
nothing for `allocations`/`unrealized`, which have no net. The deferral has been running for 15 days.

---

## 1. The two dated instances COO asked for

| # | as-of | asked at | outcome | recovered |
|---|---|---|---|---|
| 1 | **2026-07-22** (Wed) | nightly 07-22T02:0xZ | 0-row reject (BD had no snapshot yet) | **hand** re-land 07-24T02:05:44Z = **D+2** |
| 2 | **2026-07-23** (Thu) | nightly 07-23T02:0xZ | 0-row reject | **still absent** at 1335Z 07-24 |
| 3 | **2026-07-24** (Fri) | nightly 07-24T02:0xZ | 0-row reject | not yet due (D+2 → 07-26) |

Instance 1 is the D+2 proof. Instance 2 is the one that stays broken **because nothing re-asks it.**

---

## 2. The D+2 cadence is measured, n=14, and it is CALENDAR days — it does not skip weekends

`holdings` is the only snapshot table with a working net, so it is the only clean instrument for BD's
publication lag. Landing times below are **explicit-Z** (`s3api`, not `s3 ls` — VERIFICATION LAW 11):

| as-of | dow | landed (UTC) | dow | lag |
|---|---|---|---|---|
| 2026-07-09 | Thu | 2026-07-11T02:00:52Z | **Sat** | D+2 |
| 2026-07-10 | Fri | 2026-07-12T02:00:45Z | **Sun** | D+2 |
| 2026-07-13 | Mon | 2026-07-15T02:01:26Z | Wed | D+2 |
| 2026-07-14 | Tue | 2026-07-16T02:01:27Z | Thu | D+2 |
| 2026-07-15 | Wed | 2026-07-17T02:01:26Z | Fri | D+2 |
| 2026-07-16 | Thu | 2026-07-18T02:00:54Z | **Sat** | D+2 |
| 2026-07-17 | Fri | 2026-07-19T02:00:48Z | **Sun** | D+2 |
| 2026-07-20 | Mon | 2026-07-22T02:01:54Z | Wed | D+2 |
| 2026-07-21 | Tue | 2026-07-23T02:01:01Z | Thu | D+2 |
| 2026-07-22 | Wed | 2026-07-23T10:50:38Z | Thu | D+1 |

**14 of 14 clean instances at D+2 (one early at D+1), including 4 landings that occurred on a Saturday or
Sunday.** The nightly runs 7 days/week and BD publishes 7 days/week. **The lag is CALENDAR, not business-day.**

*This corrects my own retry-net design §4, which asserted a 2026-07-25 recovery for 07-23 without resolving
the calendar (NEVER#1). The conclusion happens to hold — but it held by luck, not by grounding, and 2026-07-25
is a **Saturday**, which is exactly the case that would have broken it had BD been business-day driven.*

---

## 3. `allocations` / `unrealized` have NEVER recovered a day unattended — not once

| as-of range | how it landed | note |
|---|---|---|
| ≤ 2026-07-08 | nightly, D+0, **4,304 B / 3,742 B** | **header-only stubs** — landed before the 07-09 empty-export guard existed. This is the fail-silent-stub era `9d44d6af5` fixed. **They are still sitting in bronze.** |
| 2026-07-09 .. 07-21 | one ad-hoc bulk backfill, all at 2026-07-23T04:2x-04:29Z | D+2 through **D+14** |
| 2026-07-22 | my hand re-land, 07-24T02:05Z | D+2 |

**Every non-stub landing for these two tables was a human or an ad-hoc script. The scheduled nightly has
recovered exactly zero of them, ever** — which is precisely what §0 predicts and is the strongest available
argument for the fix.

**Side finding (not in scope, flagging only):** the ≤07-08 objects are 0-row stubs still present in bronze at
D+0 timestamps. They pre-date the guard, so nothing rejected them. Worth a separate disposition call —
they are indistinguishable from real data on any existence/freshness check.

---

## 4. Correction to my own delivered design — the completeness sidecar does not exist for these tables

Measured, 2 independent axes, with a positive control:

```
holdings/_complete/     21        allocations/_complete/   0
realized/_complete/     15        unrealized/_complete/    0
transactions/_complete/ 15
positive control: identical command shape vs holdings/_complete/ -> 21 rows (so 0 is a real absence)
```

**Source-confirmed cause:** `_write_completeness_sidecar` has exactly one call site — `:745`, inside
`ingest_table`, after `land_to_s3` `:738`. A day gets a sidecar IFF it lands through `ingest_table`.
Days that landed via the bypass never got one: `s3://opal-data-cot/code/bronze/qt_0722_reland.py:80` imports
`land_to_s3` and calls it directly, never writing the sidecar. **That is the script I fired via SSM `7bdac9e2`
last night — my own re-land created the two most recent sidecar-less days.** *(The 07-09..07-21 bulk is
INFERRED to be a similar ad-hoc path; I have not identified that specific script. The consequence does not
depend on which it was.)*

**Why it matters:** my design §2/§3 assumed good days carry sidecars, so the sweep short-circuits on them.
With zero sidecars, a generalized sweep would re-pull 5 bdays × 2 tables **every night, permanently**, never
converge (a re-pulled day BD still serves 0-row is rejected pre-sidecar, so it never acquires one), and —
worst — the §3 `still_incomplete` / `oldest_still_incomplete_bdays` marker, which we put in place of an alarm
per Andrew's standing "no more sentinels and alarms", would read **saturated-red from run one, permanently.**
An instrument that always fires is not an instrument.

**Proposed amendment (needs your gate):** extend `_table_complete` to fall back to a **content probe** on the
landed object (`_export_has_data_rows` ≥ 1) when no sidecar exists, and **write the missing sidecar on success
(heal forward)**. Content-grounded, so it does not regress to a `head_object` existence proxy; converges in one
run; no migration script; idempotent; and it retro-covers any future ad-hoc re-land. DS is holding this limb
as PROPOSED-PENDING-CTO and building the rest.

---

## 5. ⚠ TIME-CRITICAL — 07-23 will NOT recover tonight, and that is EXPECTED, not a regression

BD should have as-of 07-23 available at ~2026-07-25T02:00Z (D+2, and the weekend does not block it — §2).
**But the 07-25 nightly will ask only for as-of 07-25.** With no retry-net on these tables, **07-23 is never
re-asked and will still read absent tomorrow morning.**

**Anyone reading "07-23 still missing" tomorrow without this note will call it a new defect. It is not.**
It is the documented behavior of the current code, and it is the thing the fix changes.

**This creates a clean, time-boxed acceptance window:** if the generalized net (with the §4 amendment) is
deployed **before ~02:00Z tonight**, the 07-25 nightly re-lands `allocations@2026-07-23` +
`unrealized@2026-07-23` **unattended** — a first-run live proof. If it misses that window the test slips to
the next night, and the design must not be judged on catching that specific date.

Acceptance stays two-axis (row count vs the neighbor class **and** object size-class) + sidecars appearing,
with the coverage denominator stated. Mutant control: a date outside the 5-bday lookback must remain un-swept.

---

## 6. What I recommend

1. **Primary — generalize the retry-net** (already designed, already ACCEPTED-IN-PRINCIPLE 021726Z), **with the
   §4 heal-forward amendment.** This is the self-healing limb and it fixes recovery for all three tables.
2. **Consider, do not bundle — the as-of lag.** `BD_SNAPSHOT_ASOF_LAG_BDAYS` already exists, is firm-agnostic,
   and cot could opt in so the nightly asks for a date BD actually has. It attacks the §0 root directly rather
   than compensating for it. **But it is single-ask** — one miss and the date is lost again — so it is a
   complement to (1), never a substitute, and it shifts the whole as-of grid, which wants its own review.
   **Flagging for your routing; not proposing it in this package.**
3. **Separate small item:** fix or retire `qt_0722_reland.py` so the sidecar bypass stops producing
   sidecar-less days. Arguably mine, since I fired it.
4. **Separate disposition call:** the pre-guard 0-row stubs at ≤07-08 still in bronze (§3).

**Scope note:** `cot` only. The bd/49F plane has the same vendor gap (my 07-23 finding) but is a different firm
tree — firm-separation binds and `data/black_diamond/` is `0.6.0`'s lane. Flagging the parallel; not proposing
a cross-tree change.

---

## Grounding

| Claim | Grounded on |
|---|---|
| as-of = run_date, lag defaults 0 | `data/cot/scripts/bronze/cot_bronze_ingest.py:94, :291-297, :300-314` @ working tree (matches deployed: `_write_completeness_sidecar` count 2 == 2) |
| single sidecar call site | `:745`; `land_to_s3` single caller `:738` (grepped, whole file) |
| 0-row reject precedes land | `:711-716` (`return None` before `:738`) |
| bypass writes no sidecar | `s3://opal-data-cot/code/bronze/qt_0722_reland.py:80` (read from deployed object) |
| deferred-note provenance | `:92-93`, commit `9d44d6af5` 2026-07-09T04:52:28Z, author `0.6.0_AE_PartnerETL` |
| D+2 cadence, n=14 | `s3api list-objects-v2` explicit-Z LastModified, `forwardfill_v2/holdings/` |
| sidecar counts | `s3api`/`s3 ls` per-prefix + recursive count-by-table, positive control on holdings |
| 07-23/07-24 absent | full-key listing of all three prefixes at 1320Z + 1335Z 07-24 |
| 2026-07-25 = Saturday | `lib/trading_calendar.py` host + `date.strftime('%a')` |
