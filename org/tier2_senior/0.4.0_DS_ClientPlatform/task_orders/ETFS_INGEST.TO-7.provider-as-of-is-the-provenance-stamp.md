# TO ETFS_INGEST.TO-7 — the PROVIDER's "as of" IS the provenance stamp (`ETFS_INGEST-Z-S16`)

**Issued:** 2026-08-24T23:20Z by `2.0.0_SA_COO~Z`
**Executor class:** DS (producer code) + AE (deploy) — see LANES

<issued_to>0.4.0_DS_ClientPlatform~P</issued_to>

> ⛔ **SEATED 2026-08-27 ~17:2xZ by `2.0.0_SA_COO~Z` — THIS TO SAT UNASSIGNED FOR THREE DAYS AND
> NOTHING SURFACED IT.** It carried an executor CLASS (`DS + AE`) and no INSTANCE, so
> `to-check.py` rendered it `-> (unassigned)` while every other field looked complete — including a
> **sovereign word** and a `1.0.0_SA_CTO~Z` sequencing ruling that says *"if only one 13:00Z fix
> lands, THIS ONE GOES FIRST."* **A TO with a class and no instance reads as issued and is held by
> nobody**, and the highest-priority item in its project is exactly where that is most expensive.
> **A CLASS IS NOT AN ASSIGNEE.** Found by a COO seat-census, not by any gate — recorded so the next
> census knows to look at the instance field, not the class field.
> Seat: `0.4.0_DS_ClientPlatform~P` (fresh lane, `ETFS_INGEST` ONLY per Rule 27; spawned by
> `0.0.0_AB_MSTR~Z` msg 9331 on this office's call). **The AE deploy limb is NOT seated by this
> line** — it stays an AE-class act and `~P` must route it, not perform it.
**Basis:** **ANDREW-DIRECT ~23:0xZ**, relayed verbatim by `1.0.0_SA_CTO~Z` (5645), recorded at
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_ANDREW_DIRECT_20260824_PROVIDER_AS_OF_IS_THE_PROVENANCE_STAMP_FROM_BRONZE_ONWARD.md`
**Sequencing:** `1.0.0_SA_CTO~Z` ruling (2) — **if only one 13:00Z fix lands, THIS ONE GOES FIRST.**
**Decomp cell:** **`INGEST-T2-4`** — *"THE AS-OF CONVENTION — three date semantics in ONE artifact …
One declared as-of per row + the issuer's date both-stored"*, SIZED, certified `@fcdf042972`.
**Surprise-channel item:** `ETFS_INGEST-Z-S16` (`3.0.0_SA_CVO~Z`), BLOCKING, now carrying sovereign word.

> ⭐ **THIS IS IN SPEC, AND I NEARLY SHIPPED IT AS AN EXCEPTION.** My first draft of this TO declared
> it *"issued outside the certified decomp"* as a Rule-27 surprise-channel remediation. **That was
> wrong: `INGEST-T2-4` covers it exactly, it was SIZED at authoring, and I wrote that cell myself
> three hours earlier.** I reasoned about my own artifact from memory of its scope instead of reading
> it — and the fabric's framing of this as *"the Z-S16 surprise item"* made an in-spec cell look like
> new scope. **No cell is added, edited, or renumbered; the certification stands untouched.**
>
> **What Andrew's ruling actually did is RESOLVE this cell's open decision.** T2-4 was sized as a
> question — *which* as-of governs. **He answered it: the provider's.** A sovereign ruling that
> settles a sized question is not new scope, and treating it as new scope would have quietly moved
> work out from under a certified verdict that already covers it.

---

## HIS WORD, VERBATIM

```
"Yes it is crucial that appropriate timestamps are measured when presenting infromation, all
downloaded information from the providers platforms (trueshares and pathfinder) should have some
kind of "as of" field so it is clear when that data is from, that needs to be what is used for any
date stamping on provenance. it is fine to track metadata of when we've updated data or performed
operations on it, but that is a very different figure than the actual data "as of" provenance
timestamp. Just something that needs to be accounted for and maintained from bronze ingestion
onward"
```

---

## ⛔ READ THIS BEFORE YOU WRITE A LINE — THREE THINGS THAT WILL WASTE YOUR TIME OR BREAK SOMETHING

### 1. `:526` IS NOT THE SITE. It is `return s` inside `_norm_date`, a helper BOTH vendors call.

Three seats quoted three different line numbers for this defect (`:526`, `:704`, `:1034`). Measured
at HEAD 2026-08-24T23:1xZ: **`:526` is the fallback return of `_norm_date`.** An edit there changes
date parsing for **filepoint as well**, which is currently correct. **Locate by CONTENT below, and
re-locate rather than trusting any line number in this file including mine.**

### 2. ⛔ THE FIELD YOUR FIX WOULD READ DOES NOT EXIST IN PRODUCTION.

**Measured in the DEPLOYED BYTES of `etfs-netassets-daily` (negative control run):**

```
LastModified 2026-08-24T20:31:09Z   CodeSha256 BEITykjhmRlEvcM8p9cB...
  DEPLOYED lambda_function.py : 1,127 lines      TREE: 1,335 lines   -> 208 LINES BEHIND
  vendor_trueshares_Date .... 0     as_of_basis ............... 0
  _v_ts_Date ................ 0     zzz_no_such_token_9999 .... 0   <- NEGATIVE CONTROL
  TS_HOLDINGS_ENABLED ....... 6     fetch_trueshares_holdings . 3   <- these ARE deployed
```

**TO-4's conventions layer is COMMITTED AND NOT RUNNING.** The 22:00Z partition has **17 columns**.
>> **A fix that points `data_as_of` at `vendor_trueshares_Date` would pass commit-gate, cite Andrew's
>> ruling correctly, and BE A NO-OP until the Lambda is redeployed.** That is why AC2 exists.
> This is CLAUDE.md **Rule 22a's CODE layer** — deployed bytes older than the tree, passing every
> other rung.

### 3. THE 13:00Z FIRE READS A PARTITION THAT IS ALREADY ON DISK.

The defect is in the **silver** producer (fires 22:00Z, **already fired**).
`silver/holdings/2026-08-24.parquet` was written **22:00:17Z**. The 13:00Z fire is **gold**, and gold
reads that file whole (`_read_parquet(ETFS_BUCKET, SILVER_HOLDINGS + "/" + as_of + ".parquet")`,
**no filter on the `date` column**). **A code fix plus a redeploy still leaves tomorrow's served
provenance wrong** unless the partition is rewritten — see AC3, which is **gated on CTO~Z's word**.

---

## THE MECHANISM — a CONFLATION, with the correct pattern already in the same file

```
SUBSTITUTION   "data_as_of": rec.get("net_assets_as_of")   <- a HOLDINGS row's provenance
                                                              taken from a NET-ASSETS field
CONSUMED BY    "date": h["data_as_of"]
SOURCE A (TS)  "net_assets_as_of": _ts_asof_after(html, ">Net Assets<")    <- the HTML PAGE
SOURCE B (FP)  "net_assets_as_of": holdings_date
               holdings_date = _norm_date(fund_rows[0].get("Date"))        <- the HOLDINGS FILE
```

⭐ **Filepoint already implements Andrew's ruling exactly** — it stamps holdings provenance from the
holdings file's own `Date`. For filepoint the two values coincide **by construction**, which is why
the defect is invisible there. For TrueShares they are **genuinely different documents**.
**The task is to make the TrueShares path do what the filepoint path already does. Do not touch
the filepoint path.**

**Measured evidence both ends (`2.0.0_SA_COO~Z`, 23:1xZ):**
```
BRONZE  trueshares/{DIVZ,IDVZ}/bronze/holdings/20260824/*.csv
        DIVZ 29 data rows · IDVZ 44 · DISTINCT Date values = ['8/24/2026'] in BOTH
SILVER  silver/holdings/2026-08-24.parquet · 187 rows · 17 cols
        trueshares 73  date = data_as_of = 2026-08-21   <- WRONG, from the net-assets page
        filepoint 114  date = data_as_of = 2026-08-24   <- correct, untouched
```

---

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`INGEST-TO7-AC1`** | For `source == "trueshares"`, a holdings row's `data_as_of` (and the `date` derived from it) is the **holdings sheet's own `Date`**, normalized. **The filepoint branch is byte-unchanged.** | `INGEST-T2-4` | source diff + a unit/scratch exercise on the real bronze bytes |
| **`INGEST-TO7-AC2`** | ⛔ **The change is EXERCISED IN THE DEPLOYED ARTIFACT, not the tree.** Deployed-bytes token census shows the new logic present, with a **negative control**. | `INGEST-T2-4` | Rule 22a CODE layer: download the package, census the member |
| **`INGEST-TO7-AC3`** | ⛔ **GATED — needs `1.0.0_SA_CTO~Z`'s word.** `silver/holdings/2026-08-24.parquet` is REWRITTEN so its 73 TrueShares rows carry `data_as_of = 2026-08-24`. | `INGEST-T2-4` | re-read the partition; per-source value counts |
| **`INGEST-TO7-AC4`** | `as_of_basis` moves WITH the value: a row stamped from the holdings file reads `issuer-holdings-file`. **A row whose basis label and basis source disagree is the defect respelled.** | `INGEST-T2-4` | value counts by `source` |
| **`INGEST-TO7-AC5`** | The **operation** clock stays a separate field and is NOT collapsed into the provenance stamp — Andrew's *"a very different figure"*. | `INGEST-T2-4` | field census: both present, independently valued |
| **`INGEST-TO7-AC6`** | **NEGATIVE CONTROL ON THE FIX ITSELF:** feed a fixture whose holdings `Date` and net-assets page as-of **differ**, and show the emitted stamp follows the **holdings file**. **A fixture where they agree cannot distinguish fixed from broken** — and on today's filepoint rows they always agree. | `INGEST-T2-4` | the fixture + its output |

> **AC6 is the load-bearing one.** Every filepoint row in production has the two values equal, so a
> test drawn from live filepoint data **passes whether or not you fixed anything**.

---

## Premise oracles — run at pickup, and STOP if one fails

```
1. the substitution site still exists, CONTENT-located:
     grep -n 'rec.get("net_assets_as_of")' <the netassets lambda>          expect >= 1
2. the filepoint reference is still correct-by-construction:
     grep -n '"net_assets_as_of": holdings_date'                          expect >= 1
3. the deployed/tree gap is still open (if CLOSED, AC2 changes shape):
     deployed-bytes census of vendor_trueshares_Date / as_of_basis        expect 0 / 0
4. the 08-24 partition still carries the wrong stamp (if not, AC3 is moot):
     trueshares rows' data_as_of in silver/holdings/2026-08-24.parquet    expect 2026-08-21
```

**If oracle 3 returns non-zero, the Lambda was redeployed after this TO was written — re-read before
proceeding; the no-op hazard in §2 is discharged and AC2 is a confirmation rather than a trap.**

---

## LANES

- **`0.4.0_DS_ClientPlatform~Z`** — authors the producer change. Path is
  `infra/aws/lambda/etfs-pipeline/**` (`.owned-paths.yaml` longest-match `POD4_OR_AE`:
  **DS authors producer code, AE deploys**). **Commit only; do not apply.**
- **`0.7.0_AE_CloudOps~Z`** — the redeploy (AC2) and, if CTO~Z rules it, the partition rewrite (AC3).
- **`1.0.0_SA_CTO~Z`** — **AC3 is yours to authorize.** Rewriting a production silver partition is a
  backfill and interacts with the ad-hoc-runs rule; it is **named here, not taken.**
- **`3.0.0_SA_CVO~Z`** — `Z-S16` closes on AC1+AC2+AC4, **not on AC1 alone.**

## Standing constraints

- **Filepoint is CORRECT and is the reference implementation. Do not "harmonize" it.**
- **Do not edit `_norm_date`** — shared by both vendors (the `:526` trap).
- **Bronze is untouched** (Rule 17a) — the provider's `Date` is already in the stored bytes; this is
  a silver-side read of it, never a re-ingest.
- **Silver stays dedup + dtype only** (Rule 17). Reading the provider's own declared date is
  *preserving* vendor truth, not applying business judgment — **the current behaviour is the Rule-17
  violation, the fix is the compliance.**
- **One variable at a time.** The GICS field (TO-6) and the `is_cash` silver gap are SEPARATE cells.
  Do not fold them in.
- **No alarms, monitors, SES or freshness checkers** (standing moratorium). A finding lands as a
  finding.

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). POSITIONAL — no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json INGEST-TO7-AC1,INGEST-TO7-AC2,INGEST-TO7-AC3,INGEST-TO7-AC4,INGEST-TO7-AC5,INGEST-TO7-AC6
       ⛔ CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL.
       ⚠ The checker's `firm` enum still has NO ETFS value (['49F','INF','COT','MDPF','FABRIC']) — a
       Rule 24(i) CE failure inside the gate that enforces Rule 24. Enter FABRIC and DECLARE it, as on
       TO-2 and TO-4. Routed to CTO~Z as gate owner; neither of us edits a gate.
       ⚠ AC3 is GATED ON CTO~Z's WORD. If he withholds it, the instance records AC3 as BLOCKED with
       his decision cited — it is NOT dropped from the set, because a criterion deleted to make a
       contract pass is the coverage frame lying about its own domain. -->
  <criterion id="INGEST-TO7-AC1" cell_refs="INGEST-T2-4"/>
  <criterion id="INGEST-TO7-AC2" cell_refs="INGEST-T2-4"/>
  <criterion id="INGEST-TO7-AC3" cell_refs="INGEST-T2-4"/>
  <criterion id="INGEST-TO7-AC4" cell_refs="INGEST-T2-4"/>
  <criterion id="INGEST-TO7-AC5" cell_refs="INGEST-T2-4"/>
  <criterion id="INGEST-TO7-AC6" cell_refs="INGEST-T2-4"/>
  <expected_criteria>INGEST-TO7-AC1,INGEST-TO7-AC2,INGEST-TO7-AC3,INGEST-TO7-AC4,INGEST-TO7-AC5,INGEST-TO7-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-7_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## What this closes

`ETFS_INGEST-Z-S16` — and it is the **bronze→silver leg of Andrew's chain**. His obligation runs
*"from bronze ingestion onward"*; the serving end already implements the separation he asked for
(`generated_at` vs `data_as_of`, censused by CTO~Z, confirmed under an actual republish by DE~Z's
2,384-leaf diff). **The gap is exactly here and nowhere else.**
