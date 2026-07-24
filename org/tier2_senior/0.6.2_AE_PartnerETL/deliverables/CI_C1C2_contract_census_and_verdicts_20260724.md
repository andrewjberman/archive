# CI-C1C2 — CONTRACT C1 / C2 census and verdicts

**TO:** `MDPF_CHANNEL_INDEPENDENCE.CI-C1C2` @`53efddff35` · **PRD** §2.2, §3a rows 1+2
**Author:** `0.6.2_AE_PartnerETL~C` · **Written for:** `3.0.0_SA_CVO`
**Window:** 2026-07-24T17:27Z .. 18:1xZ · **archetype:** DIAGNOSE
**Status:** ROW 1 COMPLETE (verdicts + denominators). ROW 2 verdict established; **C2 IMPLEMENTATION NOT BUILT** — see §5.

---

## 0. THE HEADLINE, AND IT CORRECTS TODAY'S DIAGNOSIS

> **CONTRACT C1 IS NOT MISSING. IT EXISTS, IT IS WIRED ON 8 OF 8 FEEDS, AND IT FIRED EVERY TRADING DAY OF
> THE "FREEZE" — INCLUDING ALL SIX DAYS I CONVERTED BY HAND THIS AFTERNOON.**
>
> **MDPF reads a SECOND silver lineage (`opal-data-bd/schwab/silver/rps/`) that has NO event wiring.** That
> one was frozen at 2026-07-15. The event-driven lineage was never stale.
>
> **So today's P0 was a LINEAGE problem, not a conversion failure** — and the work in front of the program is
> **migrate a consumer onto a contract that already works**, not *build a contract*. CTO has accepted this and
> is correcting the diagnosis he gave Andrew twice.

---

## 1. CONTRACT C1 — bronze → silver. **VERDICT: `fires`, 8 of 8.**

**Denominator: 8 wired `LambdaFunctionConfigurations` on `opal-data-assets` / 8 examined / 0 unexamined.**
Read live from `get-bucket-notification-configuration`, not from a doc. All `s3:ObjectCreated:*`.

| config | actor lambda | bronze prefix | newest bronze | newest silver | verdict |
|---|---|---|---|---|---|
| silver-schwab-08242234 | opal-assets-silver-schwab | `schwab/08242234/bronze/` | 2026-07-23 | 2026-07-23 | **fires** |
| silver-schwab-08335338 | opal-assets-silver-schwab | `schwab/08335338/bronze/` | 2026-07-23 | 2026-07-23 | **fires** |
| silver-blackdiamond | opal-assets-silver-blackdiamond | `blackdiamond/cottonwood/bronze/` | 2026-07-24 | 2026-07-24 | **fires** |
| silver-eclipse | opal-assets-silver-eclipse | `eclipse/inflection/bronze/` | 2026-07-23 | 2026-07-23 | **fires** |
| silver-orion | opal-assets-silver-orion | `orion/inflection/bronze/` | 2026-07-24 | 2026-07-24 | **fires** |
| silver-etf-divz | opal-assets-silver-etf | `trueshares/DIVZ/bronze/` | 2026-07-23 | 2026-07-23 | **fires** |
| silver-etf-idvz | opal-assets-silver-etf | `trueshares/IDVZ/bronze/` | 2026-07-23 | 2026-07-23 | **fires** |
| silver-etf-filepoint | opal-assets-silver-etf | `pathfinder/filepoint/bronze/` | 2026-07-23 | 2026-07-23 | **fires** |

**`does-not-fire`: 0.  `FIRES-BUT-UNEXERCISED-ON-THIS-PATH`: 0 configs — but see §3, which is a property, not a feed.**

### 1.1 The event property, measured per object (not inferred)

`schwab/08242234`, the feed on today's critical path — every trading day through the freeze:
```
bronze 08242234.CRS20260723.RPS.zip   landed 2026-07-24T10:15:57Z
silver fact_rps/date=2026-07-23/      landed 2026-07-24T10:16:04Z     -> +7 seconds
  07-16 -> silver 07-17T10:16:01Z    07-20 -> 07-21T10:16:00Z    07-22 -> 07-23T10:16:01Z
  07-17 -> silver 07-18T10:16:00Z    07-21 -> 07-22T10:16:01Z    07-23 -> 07-24T10:16:04Z
```
Cross-feed median lag **0.08–1.58 min**. `filepoint` bronze 22:00:10Z → both silver scopes 22:00:16Z (+6s).

> **INSTRUMENT CAVEAT, stated rather than buried:** my per-feed coverage % compares *bronze dates across ALL
> feed types* against *silver dates for one table*, so the schwab rows read 67–71% and that is **an artifact of
> my denominator, not a gap**. The trustworthy signals are the newest-date equality and the per-object lags
> above, which are like-for-like. The two schwab rows' apparent `-0.02m` median lag is the same artifact
> (max-across-all-bronze-types vs one silver table); the clean per-object measurement is **+7s**.

### 1.2 ⚠ A FALSE `does-not-fire` I REPORTED AND RETRACTED — the method matters more than the row

I first reported **`silver-etf-filepoint  0 silver / 0.0% / does-not-fire`**. **That was wrong.** filepoint is a
**1→2 fan**: one bronze object produces silver under **two** delivery scopes, `pathfinder/PFDE/` and
`pathfinder/PFOE/` (deployed `etf_conversion.py:13`), *not* `pathfinder/filepoint/silver/`.

**My census derived each feed's expected silver prefix FROM its bronze prefix.** True for seven feeds, false
for the fan — so a feed that violated my assumption read as **ABSENT** rather than **UNMEASURED**.

**AND THREE SIGNALS AGREED WITH THE WRONG ANSWER:**
| signal | why it agreed | what it actually measured |
|---|---|---|
| silver prefix empty | I looked in the wrong place | my assumption |
| DLQ depth 0 | nothing failed | that nothing failed |
| log filter `"filepoint"` → 0 events | that lambda logs **no application text** (START/END/REPORT only) | that no lambda logs feed names |

A fourth near-miss: my first CloudWatch query returned 0 events for a window whose **start time was in the
future**. It was caught by a positive control, not by the zero looking wrong.

> **THE TRANSFERABLE POINT: corroboration between instruments that share an assumption is not corroboration.**
> What broke it was reading the deployed converter's source — the one signal not derived from my model of the
> system. This is DS's fixture lesson from the same day (*a fixture parameterised by the thing under test
> cannot detect a change in it*), and I wrote it into a census four hours after banking it.

---

## 2. THE TWO-LINEAGE FINDING — **migration REFUSED without reconciliation (CTO gate)**

Same master, same date `2026-07-23`, both read directly:

| | `opal-data-assets` `fact_rps` (event-driven) | `opal-data-bd` `rps` (hand-run) |
|---|---|---|
| rows | **93,131** | **93,126** |
| columns | **63** | **11** |
| shared column names | \-- | **5** |
| wiring | S3 event, daily, ~7s | **none — hand-run** |
| Rule 17 | compliant COMPLETE `fact_{type}` | **field-slimming violation** |

**5-row delta, unexplained. 6 of the 11 bd columns are RENAMES** (`market_value`, `ticker`,
`quantity_cash/margin/short`, `file_date`).

> **"POINT THE MDPF GATE AT THE FRESHER ONE" IS THE MOST TEMPTING SENTENCE IN THIS PROGRAM AND IT IS WRONG.**
> It is a **migration, not a repoint**: every consumer of those 11 names breaks, and 5 rows are unaccounted
> for. **A fresher second source is not a drop-in for a different one** — the same error I made this morning
> recommending a 0833→0824 source. I am **naming the option and explicitly not recommending it** until (a) the
> 5 rows are reconciled and (b) the 11 names are mapped. CTO has made that a gate.

---

## 3. ARBITRARY-DATE SAFETY — **`UNEXERCISED` for C1, by CTO ruling, deliberately**

PRD §2.2 obligation 2. **I asked to land a historical bronze object to exercise it. CTO ruled NO**, and I had
proposed the honest alternative myself rather than the exercise:

1. **Rule 17a is the hardest line in the estate** — bronze is raw, byte-for-byte as delivered. A synthetic or
   re-landed object to exercise a property is what it forbids.
2. **The test would not prove the property anyway.** C1 has only ever processed same-day bronze because bronze
   lands same-day. Landing a historical object proves the lambda fires *on that object*; it does not establish
   the chain is correct for a historical **date**.

**Therefore: C1 arbitrary-date safety is `UNEXERCISED`.** What *is* established: the converters are
date-parameterised from the **key**, not the clock (`monolith_bronze_key(feed, date_compact, master)`), and my
own GC-BF1 run this afternoon converted **six historical dates** (07-16..07-23) through the same converter
family and produced partitions carrying **those** dates — content-verified, `file_date` inside each parquet
matching its own partition. **That is evidence about the CONVERTERS, not about the EVENT PATH**, and I am not
merging the two.

> **An honest UNEXERCISED is worth more than an exercise that lands bytes in bronze to produce a weaker claim
> than it appears to.** Legitimate future paths: a non-production bucket, or a naturally-occurring vendor
> re-delivery.

---

## 4. CONTRACT C2 — silver → gold DDB. **VERDICT: `does-not-fire`. It does not exist.**

**Denominator: 3 candidate buckets examined, 3 of 3.**
- `opal-data-assets` — **8 configs, ALL bronze-prefixed.** None silver→gold.
- `opal-data-bd` — 3 configs, none matching `schwab/silver/*`: `bd-allocation-processor`
  (`forwardfill_v2/allocations/`), `bd-gold-trigger` (`silver/prices/20`), `bd-silver-merge`
  (`bronze/*_BRONZE_COMPLETE.json`).
- `opal-data-mdpf` — **notification configuration EMPTY.**

**C2's target is `opal-assets-daily-aua`** — HASH `run_date`, RANGE `cohort_id`, 34,950 items.
⚠ **`opal-partner-49financial` is NOT the gold row** — it is a user/access table (`email` HASH, 11 items). The
name invites the mistake; recording it so the next lane does not make it.

---

## 5. WHAT IS **NOT** DONE — stated plainly

- **THE C2 IMPLEMENTATION IS NOT BUILT.** No lambda code, no Terraform, nothing landed. This report establishes
  the verdict, the target, and the wiring shape; **it is not a delivery of C2.**
- **C1 arbitrary-date: UNEXERCISED** (§3), by ruling.
- **Idempotency: NOT byte-tested on either contract.** C1's is asserted by the converters' skip-converted-dates
  design and PRD §2.2 ("YES — already"); **I did not re-deliver an event and byte-compare**, so per the TO's
  own forbidden-shortcut list I am not claiming it. C2 has no implementation to test.
- **Row 4 (sever-a-channel) NOT RUN — `3.0.0_SA_CVO` owns it**, and I ran no partial or informal version.
  *For CVO: the exercise must sever a **HEALTHY** channel; cottonwood (permanently absent count feed, D+2
  vendor) would produce a clean pass proving nothing.*

## 6. DESIGN CONSTRAINTS C2 MUST MEET (for whoever builds it)

1. **Trigger:** S3 `ObjectCreated` on the silver partition — per PRD §2.2, not a schedule and not a poll.
2. **NO CROSS-PARTNER READ.** State it positively: *the writer reads exactly one partner's silver and writes
   exactly that partner's row.* **Do NOT justify the design as "removing the all-or-nothing gate"** — §7.
3. **Idempotent by construction**, keyed `(run_date, cohort_id)`: a re-delivered event must leave the row
   **byte-unchanged**, not merely error-free.
4. **Arbitrary-date safe:** the row's `run_date` comes from the **partition key**, never from the clock. This is
   the `~B` NOT-CAPABLE shape one layer up — `--date` reaching nine LABEL sites and zero REQUEST sites, landing
   run-date data under the target key at exit 0.
5. **A SCHEDULED FLOOR AS WELL AS THE EVENT** — per the amended NEVER#4 (2026-07-24): *a pipeline whose only
   trigger is another pipeline's success has no schedule and is a defect.* Event-driven is an accelerator.

## 7. §1 RE-ANCHOR — grounded at source, not taken from the relay

CVO found the PRD's §1 defect is already gone; COO relayed it and **explicitly asked me to ground it myself
rather than accept a sixth restatement.** I did, in the file I had md5-matched to the deployed bytes:

- `:541` — the **spine** gate: `if GATE_ENFORCE and not gate["spine_fresh"]` → DEFER.
- `:562-589` — a **separate, later** fail-safe: `if stale_partners:` → `_roll_source_exists(as_of)` → if any
  unresolvable, **DEFER**.

> **The code reaches `:562` with `spine_fresh` TRUE. A healthy Inflection is stopped by a stale 49F — but via
> the roll-source fail-safe, NOT the all-or-nothing freshness AND that §1 describes and that was removed
> 2026-07-09.** Confirmed independently. **CVO is right: a builder handed §1 as-is fixes something already gone.**

### 7.1 Evidence for the 13th item (CTO's amendment) — a sharper mechanism than the missing grant

`_roll_source_exists` (`:338-370`) classifies on **`s3.head_object`** (`:354`). CVO's 403-vs-404 point is
correct — S3 returns 403 for a missing key when the caller cannot list, so a self-clearing **DATA** gap is
labelled a permanent **IAM** fault, which is why the remedy pointed at the wrong thing for six days.

> **But granting `s3:ListBucket` fixes the symptom and leaves the wrong instrument in place.** `HeadObject`
> **is** `s3:GetObject`, and this estate's standing rule is that **landing verification is LISTING-based;
> HeadObject is never the acceptance instrument.** `ListObjectsV2` returns an **empty listing** for a missing
> object — unambiguously ABSENT, with no 403/404 collapse to disambiguate. **The durable fix is the instrument,
> not only the grant.** Evidence only — **not touched**, CTO's to rule.

---

## 8. Compiler Tools

| Tool | Result |
|---|---|
| `comp-which` (×2) | **honest no-match both times** — no curated rule for "post-run steps after the canonical gold build" or the S3-event question; it said so rather than guessing, and I did not pick a fuzzy candidate |
| `comp-pipescript postdeps` / `io` | **GAP** — `data/canonical/schwab/` gold family (25 steps) invisible: "No dependencies declared", "Script not found". Sibling of the cot-tree gap logged 07-23 |
| deployed-code pull + `md5sum` | PASS — `mdpf-daily-trigger` byte-identical to repo HEAD, which is why §7's line citations are citations of the **deployed** logic |
| `aws lambda get-policy` (live primitive) | PASS — `AllowS3InvokeFromMonolith` present; ruled out permission as the filepoint cause **before** I found the real one |
| CloudWatch `filter-log-events` | **FAILED TWICE AS AN INSTRUMENT** — future-dated window (caught by positive control); text filter on a log with no application text (caught by reading source) |

**Gap re-confirmed, 3rd session:** no comp-tool returns an S3 object **body**; every load-bearing verification
today needed raw `get-object`.
