# opal-data-schwab -- the CANONICAL SILVER MECHANISM (clean parquets, master-scoped)

**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-07-13
**archetype:** DIAGNOSE + IMPLEMENT (**design; NO CODE WRITTEN, NO BYTES MOVED**)
**Authorization:** **ANDREW-DIRECT, ~23:12Z, VERBATIM:**

> ***"No you can be delegated to handle that work with 0.6.2_AE, that is fine. We will need to figure out a mechanism
> to essentially manage silver-level clean parquets stored in canonical fashion in opal-data-schwab."***

**Partner:** `0.6.2_AE_PartnerETL` (bronze/retrieval). **DS owns silver.**

---

## 1. 🔴 THE BUCKET HAS NO CANONICAL LAYOUT. IT HAS AN ARCHAEOLOGY.

**Grounded, read-only, `s3://opal-data-schwab/` top level:**

```
01_raw/                     CRS{date}.{EXT}, FLAT              <-- ⚠️ NO MASTER IN THE KEY
01_raw_quartz_validation/
02_anonymized/
03_mappings/
03_silver/                  TRN/ TRN_NNA/ account_xref/        <-- generation 2
_archive/  _ops/
backfill/08335338/          acc/ fam/ rld/ rlu/ ...            <-- 0.6.2's. MASTER-SCOPED. ✅
bronze/                     rps/
silver/                     ACC/ TRN/ ULN/                     <-- generation 3
                            silver/ACC/date=20240116/data.parquet   <-- ⚠️ NO MASTER IN THE KEY
```

> ## **AT LEAST FOUR COMPETING LAYOUT GENERATIONS COEXIST IN ONE BUCKET, AND THE EXISTING SILVER HAS NO MASTER DIMENSION AT ALL.**

## 2. 🔴 **THE CONSEQUENCE, AND IT IS THE THING ANDREW EXPLICITLY FORBADE**

`silver/ACC/date=20240116/data.parquet` -- **which master?** **You cannot tell from the key.**

> ### **=> IF 0833 WERE WRITTEN INTO THE EXISTING LAYOUT, IT WOULD SILENTLY COMMINGLE WITH 0824, AND NOTHING IN THE KEY WOULD REVEAL IT.**
> **Andrew, verbatim:** *"The two need to be in their own folders... **they do NOT overlap**"* / *"do not commingle."*
> **The existing layout CANNOT satisfy that instruction. Not "does not" -- CANNOT. There is no field to put the master in.**

**AND IT IS THE SAME DISEASE AS EVERY OTHER FINDING TONIGHT, ONE LAYER DOWN:**
> # **THE KEY DOES NOT SAY WHAT IT IS *OF*.**
> `partner_custody_total` does not carry its master -- **and a Tier-1 architect misread it tonight.**
> `silver/ACC/date=.../data.parquet` does not carry its master -- **and nobody has misread it yet ONLY because there
> has only ever been one master in the bucket.** **That protection expires the moment 0833 lands.**
> ### **THE IDENTITY CHANNEL IS DEAD AT THE STORAGE LAYER TOO. AC4 IS NOT A ROW-LEVEL FIX -- IT IS A KEY-LEVEL ONE.**

---

## 3. ⛔ **THE TRAP: DO *NOT* ASSUME THE EXISTING SILVER IS 0824**

**The obvious next move is: *"migrate the existing silver into the new master-scoped layout under `/08242234/`."*
DO NOT.**

- The existing silver derives from **`01_raw/`, which has NO master in the key** -- filenames are `CRS20230117.RLD`,
  date + type, **no master**.
- **So migrating it under `/08242234/` would be ASSERTING that every one of those files is 0824 -- WHICH WE HAVE NOT
  VERIFIED.**

> ## **"IT IS ALL 0824" IS AN ASSUMPTION. AND ASSUMING A MASTER IS *EXACTLY* TONIGHT'S DISEASE.**
> *I assumed disjointness and produced a false $1.7B. CTO assumed `total_aua` was cross-master and mis-built a
> reconciliation. **Assuming which master a file belongs to would be the same error, written into the storage layout,
> permanently, at scale.***

**THE GOOD NEWS -- THE ANSWER IS IN THE BYTES, NOT IN AN INFERENCE.** `0.6.2` confirmed the vendor stamps the master
in every file's H1 header:
```
H1|SCHWAB|0008335338|49 FINANCIAL|20260710|BDRECPOS|01.06
              ^^^^^^^^^^ THE MASTER, IN THE FILE, FROM THE SOURCE
```
> ### **=> THE MASTER IS DERIVED FROM THE H1 HEADER. NEVER FROM THE FOLDER IT WAS FOUND IN, NEVER FROM "WELL, IT MUST BE."**
> **That single rule makes the migration SAFE and makes it VERIFIABLE.** *(And it is the storage-layer form of AC4's
> `_declared` vs `_observed` discipline: **the master is OBSERVED from the artifact, never INFERRED from its
> location.**)*
> **A file whose H1 cannot be read is `UNKNOWN` and goes to quarantine. It does NOT get a default.**

---

## 4. THE CANONICAL LAYOUT (proposed)

```
s3://opal-data-schwab/{master}/bronze/{TYPE}/{YYYYMMDD}/{vendor_file}          RAW, byte-for-byte.  0.6.2's lane.
s3://opal-data-schwab/{master}/silver/{TYPE}/date={YYYY-MM-DD}/data.parquet    CLEAN PARQUET.       DS's lane.

  {master} = 08242234 ("49F Schwab SmartX")  |  08335338 ("49F Schwab Black Diamond")
```

**WHY EACH PIECE, AND EVERY ONE IS A RULE, NOT A PREFERENCE:**

| choice | why |
|---|---|
| **`{master}` is the TOP folder** | **Andrew, verbatim:** *"/0824#### is its own folder as /0833#### is its own folder."* **Commingling becomes structurally impossible, not merely discouraged.** |
| **parquet lives ONLY under `silver/`** | **Rule 17a: BRONZE IS RAW. PARQUET IS A SILVER FORMAT.** A `.parquet` under `bronze/` coerces schema/dtypes AT INGEST and destroys bronze's one job. **Andrew's own phrasing -- "silver-level clean parquets" -- is this rule.** |
| **`silver/` = dedup + dtype ONLY** | **Rule 17.** **NEVER slim fields, NEVER fillna/dropna, NEVER drop a vendor column.** Anything needing judgment about field relevance is **gold**. *We preserve every column Schwab ships, even the ones nobody reads yet.* |
| **master in the KEY** | a row can never be orphaned from its identity. **This is AC4, at the storage layer.** |
| **`date=` partitioning** | matches the existing silver convention (`date=20240116`) -- **the one thing generation 3 got right, and worth keeping.** |

**AND THE INGESTION-ROBUSTNESS CLAUSES (Andrew's other half -- these are AC11/AC15/AC16, applied here):**
- **AN ABSENT DAY IS ABSENT.** No roll-forward, no zero row, no "carry the last value." **A missing partition must be
  visible AS missing.** *(`0.6.2`'s freshness oracle already does this consumer-side: `OK` / `STALE` / **`ABSENT`**,
  counted in **TRADING DAYS** -- NEVER#1.)*
- **IDEMPOTENT:** skip already-converted dates; `--force` rewrites; `--since` scopes. *(The `49-schwab-conv` pattern,
  already proven.)*
- **DELIVERY IS VERIFIED, NOT ASSUMED.** `head-object` / byte-count the landed parquet. **`exit 0` must mean "the
  bytes are in S3," not "I did not crash."** *(Instance #6: `etf_probe`'s bare `except` -> `exit 0`.)*
- **`from __future__ import annotations`** on every silver script (Rule 15, gate-enforced).

---

## 5. WHAT I AM **NOT** DOING

- **NOT writing the CBUGL converter yet.** **`0.6.2`'s puller is BUILT, NOT DEPLOYED, and bronze has no bytes.**
  > ### **A CONVERTER BUILT AGAINST NO DATA IS A CONVERTER TESTED AGAINST A FIXTURE AND CALLED DONE.** *That is
  > instance #9 of tonight's class and I am not writing it.* **The design lands now; the code lands on bytes.**
- **NOT migrating the existing silver.** It requires the H1-header master derivation above, and **that is a decision
  with a sovereign-held surface under it.** **Proposed, not taken.**
- **NOT touching `opal-data-bd/schwab/silver/*`** (the legacy SmartX silver). **Held surface. Out of scope. Noted as
  tech-debt-on-the-way-out per Andrew's PIT thesis -- not as work.**
- **NOT deriving the 49F bucket relationship.** Ordered stopped (CTO~B); ruled out of scope by Andrew three times.
  **Nothing in this design needs it** -- *which is the test: **if a design is invariant to a question, that question
  does not need answering.***

## 6. FENCES
**No code. No bytes moved. No mdpf run. No sentinel. INF HELD. Frozen 3 untouched.** Read-only `s3 ls` on
`opal-data-schwab` (inspection only -- **no object read, no client data touched**).

## 7. OPEN, FOR CTO~B / CTO / ANDREW
1. **Adopt `{master}/silver/{TYPE}/date=/` as canonical?** (My recommendation: **yes** -- it is the only layout that
   can satisfy Andrew's "own folders / do not commingle" instruction.)
2. **The existing non-master-scoped silver: migrate (via H1-derived master) or freeze-and-supersede?** **A decision,
   not a task. I am not taking it.**
3. **The four legacy generations (`01_raw/`, `02_anonymized/`, `03_*`, `bronze/`, `silver/`)** -- **an inventory, not
   a cleanup.** ⚠️ **A tidy-up here is a DELETION-CLASS action on a sovereign surface. Nobody touches it on
   inference.**
