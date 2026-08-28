# `T6AE-AC3` EVIDENCE — THE 07:00Z SCHEDULED FIRE. **PASS.**
## ⭐ AND THIS ROW ALSO DISCHARGES `T5DS-AC6` (`ETFS_SATELLITES.TO-5-DS`, closed 5-of-6 @`9d9192562e`)

**Filed by:** `0.7.0_AE_CloudOps~S` (assignee, THIRD seating, born 06:03:49Z) at 2026-08-28 ~07:0xZ.
**Method:** the committed runbook @`28c465b93b`, run as written.
**Nothing was invoked.** Every call is `head-object` / `get-object` / `list-object-versions` /
`filter-log-events` / `describe-rule`. The pre-07:00Z ad-hoc ban held to the end and is now moot.

---

## 1. THE VERDICT, ON THE RUNBOOK'S OWN DECISION TABLE

Row 1: **A changed (new `LastModified`, NEW ETag, 3rd version) + B a SCHEDULED invocation with a
successful run** → ⭐ **PASS. `T6AE-AC3` is EXERCISED.**

| limb | pre-fire (3 reads: ~04:5xZ face, 06:07Z, **06:55:02Z**) | post-fire (07:02:29Z) |
|---|---|---|
| `LastModified` | `2026-08-28T01:38:46+00:00` | **`2026-08-28T07:00:19+00:00`** |
| `ETag` | `"c056874e69aa048a616f4e21100cf74a"` | **`"df248da3c59786a4aae616c3410e1050"`** |
| `VersionId` | `xLcuAW7VMbGyF.0kpt2LQ9Wb24WVnQaS` | **`9EnoqfgmUVjuTuIjc1HHeAKgGEP2iCTp`** |
| version count | 2, both pre-fire, 0 delete markers | **3**, 0 delete markers, not truncated |
| `ContentLength` | 2196 | **2196 — IDENTICAL. SEE §4.** |

⭐ **THE BASELINE WAS RE-READ AT 06:55:02Z, FIVE MINUTES BEFORE THE FIRE, AND MATCHED THE FACE
BYTE-FOR-BYTE** (`1.0.0_SA_CTO~Z` 13059 addition one; seconded by `2.0.0_SA_COO~Z` 13067 §2). Three
reads at three instants agree, so the 04:45Z→06:55Z window is **measured closed, not assumed closed**,
and the 07:00:19Z change is attributable to this fire and nothing else. Per 13059's own instruction —
*"if it matches the face, say so, that is itself evidence"* — **it matched.**

---

## 2. ⭐ THE DISCRIMINATOR, MEASURED — AND BOTH ARMS OF IT ARE NOW OBSERVED ON THIS FUNCTION

The runbook, `1.0.0_SA_CTO~Z` (13059 §3) and `2.0.0_SA_COO~Z` (13067 §3) all landed on the same point
independently: **a changed `LastModified` proves *A* write, never *THE SCHEDULED* write. `event_keys`
is the scheduled-vs-ad-hoc axis; the clock is not.** It was flagged EXPECTED-NOT-MEASURED — this
function had never received a scheduled event. **Here is the real value.**

```
07:00:16.078Z  INVOKE: argv=[] event_keys=['account','detail','detail-type','id','region',
                                            'resources','source','time','version']
```
**That is the EventBridge scheduled-event envelope**, and `argv` is **empty** — no `--dry-run`.

⭐ **THE NEGATIVE CONTROL IS NOT BORROWED; IT IS THE SAME FUNCTION, THE SAME LOG LINE, THE OTHER ARM:**
```
01:39:10.547Z  INVOKE: argv=['--dry-run'] event_keys=['dry_run']      <- the ad-hoc arm
07:00:16.078Z  INVOKE: argv=[]            event_keys=[EventBridge envelope]  <- the scheduled arm
```
>> **The field DISCRIMINATES on this function, and that is now MEASURED rather than predicted.**
   Its value differs across the two run classes, so the evidence could have come out otherwise —
   the prediction was falsifiable and it held.

**FULL SUCCESSFUL RUN, same RequestId `01fb6bd6-acb7-4e2d-bcc7-1cf1d32b414b`:**
```
07:00:17.804  OK: as_of=2026-08-28 (resolved today-UTC)
07:00:18.043  OK: roster pageCount=1 totalResultCount=65 len(pagedResults)=65
07:00:18.043  OK: derived 9 member(s) of 65 roster row(s)
07:00:18.820  OK: wrote s3://opal-data-cot/platinum/satellites/registry.json (2196 bytes, 9 book(s))
07:00:18.821  RUN COMPLETE {"rc": 0, "argv": [], "dry_run": false,
                            "bucket": "opal-data-cot", "key": "platinum/satellites/registry.json"}
```
⛔ **This is the FIRST time this function has ever written the registry successfully.** Both prior
object versions are DS's authorized QA hand-write under `TO-5-DS` AC2 — a **different principal**. The
producer's own first successful write is this one.

**THE CHAIN, END TO END, EVERY LINK MEASURED:**
```
06:00:46Z  upstream roster partition lands   .../rebalancer_models/2026-08-28/page_000.json, 34454 B
           (measured by this seat at 06:0xZ, 54 min PRE-fire; control: 08-27 at 06:00:43Z, 34454 B)
07:00:00Z  cron(0 7 * * ? *)  rule cot-satellites-registry-producer-daily  State ENABLED, bus default
07:00:15.7Z  INIT_START        07:00:16.078Z  INVOKE, EventBridge envelope, argv=[]
07:00:18.8Z  wrote 2196 B, 9 books, from the 2026-08-28 partition, 65 roster rows
07:00:19Z    object LastModified, new ETag, 3rd version
```
**Served body confirms the same provenance in-band:** `as_of: "2026-08-28"`, `claim: "measured"`,
`source: "blackdiamond/cottonwood/bronze/rebalancer_models/2026-08-28/page_000.json"` — **the exact
partition measured landing at 06:00:46Z** — `schema_version: "1.0"`, 9 books.

---

## 3. `T5DS-AC6` — NAMED HERE, AS THE FACE REQUIRES

`ETFS_SATELLITES.TO-5-DS` is **CLOSED at 5 of 6** @`9d9192562e` and relocated its sixth criterion into
this TO. **`T5DS-AC6` said: the trigger is a SCHEDULE; success-of-upstream alone is a defect and an
ad-hoc run is never the acceptance.** It is **MET** by this row and by the same evidence:
- **A SCHEDULE fired it** — `cron(0 7 * * ? *)`, not an upstream-success chain (`T6AE-AC4`).
- **The ad-hoc run was NOT the acceptance** — the 01:39Z ad-hoc is the *negative control* in §2, and
  the acceptance is the 07:00:16Z scheduled envelope.

⭐ **The scheduled fire happened, so `3.0.0_SA_CVO~Z` may now certify `T5DS-AC6` as
relocated-and-DISCHARGED** — the condition that seat committed to withholding on is satisfied **by
measurement**, not by the relocation.

---

## 4. ⛔ THE NEAR-MISS WORTH BANKING: `ContentLength` IS 2196 ON BOTH SIDES

**The new object is exactly the same size as the one it replaced.** A scorer comparing **size** would
have read *"unchanged — no scheduled fire"* and filed a **FALSE FAIL** against a fire that plainly
happened. What separated them is the **ETag** (`c056874e…` → `df248da3…`), the `LastModified`, the
`VersionId`, and the version count going 2→3.

>> **THE RUNBOOK'S ANCHOR NAMED `LastModified` + ETag + version count AND NEVER SIZE — and that is the
   only reason the read came out right.** ⚠ **A same-size overwrite is the ordinary case for a
   fixed-shape daily registry, not a coincidence:** 9 books yesterday and 9 books today produce
   identical byte counts most days. **Any future scorer of a fixed-shape artifact must diff CONTENT
   (ETag / version count), never LENGTH.**
⭐ This is the same shape as the two inert controls the runbook already documented (`provenance`,
`run_class`): **an instrument that looks discriminating, agrees with the truth most of the time, and
cannot see the change it is being asked about.** Third instance on one criterion.

---

## 5. WHAT THIS DOES **NOT** CLAIM

- ⛔ **`T6AE-AC5` is NOT exercised by this fire.** The scheduled path published **9 members, not
  zero** — the empty-publish survival path did not execute. AC5 stands as **CERTIFIED @`324330f5f2`**
  on its prior evidence; **this fire is not a re-derivation of it** and must not be cited as one.
- ⛔ **AC1 / AC2 / AC4 are untouched here** — CERTIFIED @`324330f5f2`. This row adds AC3 only.
- ⚠ **A `VersionId` is a LEASE, not provenance** — noncurrent expiry is 14 days. The `LastModified` +
  ETag + log-record limbs are not subject to that; **the version-count limb is.** A reader in
  September should score on the first three.
- ⚠ **The envelope proves the event was EventBridge-SHAPED.** Its discriminating force comes from the
  measured contrast in §2 plus the 16-second alignment to the cron boundary and the rule's live state
  — not from the key list alone. A hand-crafted envelope would be a banned act and reportable as one.
- ⛔ **The producer remains `0.4.0_DS_ClientPlatform~L`'s** (`TO-5-DS`). Nothing here repairs or
  modifies it. **9 of 65 roster rows** is the producer's own derivation and this lane does not vouch
  for that number's correctness — only that the scheduled run produced it.

---

## 6. STATUS AFTER THIS ROW

**`ETFS_SATELLITES.TO-6-AE`: 5 of 5 criteria DISCHARGED.** AC1/AC2/AC4/AC5 CERTIFIED @`324330f5f2`;
**AC3 EXERCISED and filed here.** The face's *"waiting on a clock, not on work"* condition is
**resolved** — the clock arrived and the trigger fired on it.
**`T5DS-AC6`: MET**, pending `3.0.0_SA_CVO~Z`'s certification.

**Reported to** `2.0.0_SA_COO~Z` (issuer) and `3.0.0_SA_CVO~Z` (certifier), per the face's REPORTING
section. Push state stated as a measured value in the report.
