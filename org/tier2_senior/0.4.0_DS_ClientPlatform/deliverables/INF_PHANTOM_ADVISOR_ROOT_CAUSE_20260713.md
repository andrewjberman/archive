# INF phantom advisor — ROOT CAUSE: Orion dropped 3 accounts from /NewPortfolio on 2026-07-09

**archetype:** DIAGNOSE
**Author:** 0.4.0_DS_ClientPlatform · 2026-07-13
**Tasked by:** 2.0.0_SA_COO (URGENT, question-first: *"WHY is rep_id NULL in silver for accounts
560/703/1225? Read the silver converter. Do NOT build. Do NOT run a gold rebuild."*)
**Status:** ANSWERED. No build. No gold run. COO's re-derivation HOLD respected throughout.
**Code vintage for every citation below:** `@ 5581c0de1` (last commit touching the three scripts);
working tree at `d1aa7a51d` is identical for them.

---

## 1. The answer in one line

**`rep_id` is not a transaction field.** It is a LEFT JOIN from the *current* `accounts_v2`
dimension onto the full-history transaction spine. It is NULL for accounts 560/703/1225 because
**Orion's `/Portfolio/Accounts/NewPortfolio` endpoint stopped returning those three accounts on
2026-07-09**, so they vanished from `accounts_v2`, so the join found nothing.

Our filters did not drop them. There was nothing to drop.

---

## 2. Where `rep_id` is born

`data/inf/scripts/silver/convert_transactions_to_silver.py:519 @ 5581c0de1`

```python
rep_join = (rep_lookup[["account_id", "rep_id"]]
            .rename(columns={"account_id": "accountId"}))
df = df.merge(rep_join, on="accountId", how="left")     # <-- rep_id is created HERE
```

`rep_lookup` = `_load_rep_lookup()` (`:260-280`) = the **latest**
`silver/api_dims/accounts_v2/**/data.parquet`.

The script's own docstring already says the whole thing — `:61`:

> `rep_id NULL = account absent from accounts_v2 silver (data quality signal)`

And `accounts_v2` (`convert_orion_api_to_silver.py:400-540`) has exactly **one** source:
`bronze/orion-api/{date}/new_portfolio_accounts.json` — `GET /Portfolio/Accounts/NewPortfolio`.

Two gates stand between that bronze and `accounts_v2`:
- `:431` `df[df['custodian'].isin(['Fidelity_Inflection','Fidelity_LH'])]`
- `:513` merge `household_rep_mapping` on `household_id` (`clientId` → `household_id`, `:442`)
- `:540` `out[out['rep_id'].isin(INFLECTION_REP_IDS)]` — and **`NaN.isin(...)` is `False`**, so a
  household with no rep mapping is *deleted*, not flagged.

---

## 3. The measurement (denominators printed on every scan)

### 3.1 `accounts_v2` — all 69 partitions walked

| snapshot | accounts | rep 11 (Patrick) | 560 | 703 | 1225 |
|---|---|---|---|---|---|
| 2026-07-07 | 868 | 147 | ok | ok | ok |
| **2026-07-08** | **873** | **144** | ok | ok | ok |
| **2026-07-09** | **870** | **141** | **GONE** | **GONE** | **GONE** |
| 2026-07-10 | 871 | 141 | GONE | GONE | GONE |
| 2026-07-12 | 873 | 141 | GONE | GONE | GONE |

`-3` accounts, `-3` on rep 11, **no other rep moved.** This is the day the phantom appeared and
the day Patrick's served NNA went short $52,604.80.

### 3.2 The raw vendor bronze — the decisive read

| date | `new_portfolio_accounts.json` rows | 560 / 703 / 1225 |
|---|---|---|
| 2026-07-07 | 2,960 | present |
| **2026-07-08** | **2,968** | **present** |
| **2026-07-09** | **2,965** | **ALL THREE ABSENT** |
| 2026-07-10 | 2,966 | absent |
| 2026-07-12 | 2,971 | absent |

On **07-08** all three were present and healthy:
`custodian=Fidelity_Inflection`, `clientId=227`, `isActive=True`,
`accountStatus='Normal Downloading'`, `representativeName='Patrick Scanlan'`.

I **replayed both pipeline gates** against that bronze row-by-row:
`custodian` gate → **True**; `clientId 227 → rep 11` gate → **True**. Verdict: **KEPT, KEPT, KEPT.**

On **07-09** they are simply not in the payload. `-3` rows, exactly.

### 3.3 The cascade (source-confirmed + exercised end to end)

1. Orion `/NewPortfolio` drops 3 accounts (07-09; cause vendor-side — see §6).
2. `accounts_v2` is built from `/NewPortfolio` **only** → accounts vanish. **Silently.** 873 → 870.
   No detector, no alarm; an account leaving is not an event to this pipeline.
3. `convert_transactions_to_silver:519` LEFT JOIN → `rep_id = <NA>` on **all 3,283** txn rows,
   back to 2023. `:648` *does* log `WARN: N rows with null rep_id` — and writes the parquet anyway.
   **A WARN in a log is not a gate.**
4. `INF_C_01.canonical_nna.py:446` `.map()` → `NaN` → `:463`
   `.fillna('inflection_unmapped_rep')` → **the phantom advisor**.
5. Served: a 5th "advisor" on `advisor_nna_canonical.json` holding **$52,604.80 of Patrick's money**.

**Blast radius, measured:** exactly **3 accounts / 3,283 rows / $588,312.30** `|transAmount|`
carrying a null rep. Reproduces CTO's 3,283 to the row.

---

## 4. Four independent oracles say the money is Patrick's

None of these routes through `accounts_v2`:

| oracle | says |
|---|---|
| `household_rep_mapping` (all **70** partitions incl. 2026-07-12) | hh 227 → **rep 11, Patrick Scanlan**. *It never left.* |
| firm roster `GET /Portfolio/Accounts` (20260710, 3,113 rows) | all 3 present, `clientId=227` |
| Custom Report 28198 `repName` **on their own txn rows** | **'Patrick Scanlan'** (2,677 enriched rows) |
| REST txn spine | 3,283 rows, trading through **2026-06-26** — live accounts |

Household 227 = *"Judith & David Saarinen"*, `custodian=Fidelity_Inflection`,
`managedAccount=True`. **One** Orion endpoint dropped them; four others did not.

---

## 5. The real defect — and it is not the phantom

> **`accounts_v2` is a CURRENT-STATE dimension serving as the SOLE rep source for a
> FULL-HISTORY transaction spine. The two have different lifetimes.**

An account can leave the current-state dim while three years of its transactions remain. There is
**no last-known-rep carry-forward**, and **nothing asserts the join is total** — that every
`accountId` in the spine resolves to a real advisor. When that assertion is absent, the residual
puts on an advisor's shape and walks onto the served spine.

### 5.1 …which is also COO's item (3): the 2.6M all-time drift

Same line. `:519` joins the **current** `accounts_v2` rep onto **every historical txn row back to
2020**, then `:551` stamps `df["rep_id_is_historical"] = False`. **So when a book moves, all
history moves with it on the next nightly.** `accounts_v2` shows the book move on **07-08**, one
day *before* the phantom:

```
07-07  {IWM: 17, joe: 67, patrick: 147, peter: 637}
07-08  {IWM: 21, joe: 83, patrick: 144, peter: 625}    joe +16, peter -12, patrick -3, firm +4
```

That reshuffle is COO's **joe +2.1M / peter −1.6M / patrick −981K**. Directions match.

### 5.2 The flag that declares this is a lie nobody reads

**Census BY FUNCTION, not by mention:** `rep_id_is_historical` is **written** at `:551` and has
**zero functional consumers**. The only other references in the entire tree are
`INF_A_01.advisor_assignments.py:19` (a docstring) and `lib/txn_cache_reader.py:81` (a comment) —
**prose, not detectors.**

The column tells the exact truth — *"this attribution is current-state, not historical"* — and not
one line of code asks it. **It is a comment with a dtype.**

---

## 6. HARD GAP — not guessed

**WHY** Orion's `/NewPortfolio` stopped returning three live, managed, `Fidelity_Inflection`,
`Normal Downloading` accounts on 07-09 is **UNGROUNDED**. Determining it requires an Orion API
call = **vendor egress**, which requires **Andrew's explicit per-use word**. I did not make it and
will not.

This is a hard external gate, stated plainly — not a default and not a deferral. Everything above
is grounded on artifacts we already hold (S3 bronze + silver + local pulls).

---

## 7. My own instrument lied. Reporting it.

**Probe 1 concluded "hh 227 is ABSENT from `household_rep_mapping`." That was FALSE** — an
Int64 `227` matched with `.isin()` against a **string** `household_id` column returns zero rows.

I had a complete, elegant mechanism built on that zero: a **rep-10 allowlist gap** —
`SERVICING_REP_IDS = {6, 10, 11, 12}` (`:625`, *"Brandenburg / **Soderblom** / Scanlan / Lee"*)
vs `INFLECTION_REP_IDS = {3, 6, 11, 12}` (`:631`) — under which a household serviced by Noel
Soderblom (rep 10) would be picked as rep 10 and then **silently deleted** by the `:540` `isin`
filter. There are in fact **five disagreeing definitions** of "the Inflection rep scope" across
the tree (`_orion_api_silver_lib.py:113` `{3,6,11,12}`; `convert_orion_api_to_silver.py:631`
`{3,6,11,12}`; `pull_inflection_representatives.py:65` `[3,6,7,8,10,11,12]`;
`pull_inflection_assets.py:53` `[3,11,12]`; `manual_api/create_*.py` `[3,6,11,12]`).

**The partition walk killed it.** hh 227 is present in all 70 partitions under rep 11.

**When the answer is ZERO, open the file.** I nearly shipped a pretty mechanism over a
measurement — the precise failure CTO's own amendment was written about. The rep-10 hole is
**real and latent** and I am filing it **separately** (§8) rather than smuggling it in as this
incident's finding, because it is *not what happened here*.

---

## 8. Latent, filed separately (NOT this incident)

**L1 — the rep-10 / Noel Soderblom deletion hole.** A household whose primary servicing rep is
10 (Soderblom) gets `rep_id=10` from `_pick_primary_rep_id` (`SERVICING_REP_IDS` includes 10) and
is then **deleted** from `accounts_v2` by `:540` (`INFLECTION_REP_IDS` excludes 10) — producing
this identical phantom cascade. Noel currently has 0 households in the mapping, so it has never
fired. **Inflection's core business model is onboarding advisors.** It is a landmine.

**L2 — five disagreeing definitions of the Inflection rep scope** (listed in §7). Two independent
paths to one fact with nothing asserting they agree.

---

## 9. Proposed — NOT BUILT, awaiting GO

1. **DETECT.** Assert every `accountId` in the txn spine resolves to a rep on the canonical
   roster; **RAISE**. And `accounts_v2` must not silently shrink — *an account leaving is an event*.
2. **NEVER EMIT.** `inflection_unmapped_rep` must never be served as an advisor
   (CLAUDE.md ruling: assert the shape where you cannot remove the residual).
3. **CARRY FORWARD** the last-known rep when an account leaves `/NewPortfolio` but retains
   transactions — and then `rep_id_is_historical` must actually be **set**, and actually be **read**.
4. **BUSINESS RULING NEEDED (Andrew/Inflection, not mine):** is current-state attribution of *all*
   history the **intended** semantic? If yes, it must be said out loud. If no, (3) is mandatory.

---

## Compiler Tools

| tool | result |
|---|---|
| `comp-which "which script converts bronze transactions to silver for the inflection pipeline"` | routed to `comp-dispatch` — did not fit; fell through to `comp-glob`/`comp-grep` as designed (no dead-end) |
| `comp-glob "data/inf/scripts/silver/*.py"` | 18 silver scripts — located the converter set |
| `comp-grep "rep_id" data/inf/scripts/silver` | per-file **denominator** (17 hits in `convert_transactions_to_silver.py`) — identified the writer |
| `comp-grep "rep_id_is_historical" .` | the census-by-function that proved **zero** functional consumers |
| `comp-grep "silver/transactions"` | producer/consumer map for the spine |

**Gap found:** `comp-which` did not route a "which script writes silver X" question to a producer
lookup — `pipescript --resource` would have. Worth a routing entry.

**Raw-search overrides used** (`# rail-checked:`): 3, all for reading a *known* line range of a
*known* file (`sed -n`), which no comp-tool answers.
