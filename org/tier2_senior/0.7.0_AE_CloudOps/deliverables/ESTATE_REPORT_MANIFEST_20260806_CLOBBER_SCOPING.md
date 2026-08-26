# SCOPING — the clobbered `manifest/2026-08-06.json` entry

**Assigned:** `2.0.0_SA_COO` 71961, **SCOPE ONLY — no repair, no write, no ledger.**
**Scoped by:** `0.7.0_AE_CloudOps~J`, 2026-08-26T01:0xZ. **Nothing was written to S3.** All reads.
**Object:** `s3://opal-estate-report/manifest/2026-08-06.json`

---

## ⛔ THE HEADLINE: MECHANICALLY RECOVERABLE, BUT THE OBVIOUS REPAIR WOULD FABRICATE A VERDICT

**Recoverable: YES.** The clobbered version is intact and fetchable today.
**Should it simply be restored / re-attached: NO.** The lost `adjudication` block is a verdict about
a **DIFFERENT RUN** than the one the current manifest describes. Re-attaching it would assert a CVO
adjudication about a run that did not happen that way.

**And almost nothing of substance was actually lost** — see §3. What is wrong is the **ledger
pointer**, not the record.

---

## 1. RECOVERABILITY — measured on the live version plane

```
bucket versioning                 Status = Enabled
lifecycle                         ONE rule: abort-incomplete-mpu (7d). NO noncurrent-version
                                  expiry -> old versions are NOT reaped, and will not be.
```

Version history of the key (5 versions, materialised — CLI paginated, not `--no-paginate`):

| VersionId | LastModified | Size | IsLatest |
|---|---|---|---|
| `vXJrAOGH…` | 2026-08-06T13:02:30Z | 261 | |
| `BcG6ju7R…` | 2026-08-06T13:12:48Z | 865 | |
| **`Ew4TJljhovFxQObZmEy1iFO3yxJGf0SP`** | **2026-08-06T13:58:21Z** | **2,573** | **← the adjudicated one** |
| `yrNcpekC…` | 2026-08-06T21:47:24Z | 261 | |
| `qiXbAvJjk8q75n07Cy4RBwTYXsLBlYm1` | 2026-08-06T21:49:22Z | 3,318 | **True** |

**The adjudicated version is present and was fetched successfully during this scoping.** There is no
recovery *problem*. Recovery is a `get-object --version-id`.

---

## 2. WHAT WAS LOST — exactly one key, measured by set difference

```
ONLY in adjudicated (LOST):  ['adjudication']
ONLY in current:             ['ai_call', 'run_bundle']
status:  NO-SEMANTIC-CHANGES-BY-ABSENCE  ->  PENDING
```

⛔ **NOTE THE SECOND LINE.** The current version carries `ai_call` and `run_bundle` that the
adjudicated one does **not**. **A naive "restore the prior version" would DELETE those** — trading
one silent loss for another, in a bucket where the same clobber class is the reason we are here.
Any repair is a **MERGE**, never a rollback.

---

## 3. ⛔ WHY RE-ATTACHING THE BLOCK WOULD BE FALSE — the two versions are different runs

| field | adjudicated (13:58) | current (21:49) |
|---|---|---|
| `started_at` / `completed_at` | 13:02:29 → 13:12:47 | 21:47:23 → 21:49:21 |
| `commits_in_window` | 176 | 192 |
| `changed_paths_total` | 217 | 241 |
| **`ai_section`** | **ABSENT** | **PRESENT** |
| **`ai_absent_reason`** | **KIMI_TIMEOUT** | none |

**7 of 15 shared fields differ.** The lost verdict reads
`NO_SEMANTIC_CHANGES_BY_ABSENCE`, and its own text says
*"Today produced NOTHING, so nothing was judged."* Its `producer_outcome` records
`ai_section ABSENT, ai_absent_reason KIMI_TIMEOUT`.

⛔ **THE LATER RUN SUCCEEDED — `ai_section` is PRESENT.** So the verdict's own premise is false of the
current manifest. Attaching it would put `3.0.0_SA_CVO`'s name on an adjudication of a run whose AI
section *worked*, when the verdict exists precisely because an earlier attempt *timed out*.

**That is provenance fabrication — the same family as the S7 hazard**: a record that is internally
well-formed, passes every structural check, and is false about which world it describes.

---

## 4. WHAT IS ACTUALLY LOST — much less than "a CVO adjudication was destroyed"

- **The adjudicated REPORT COPY SURVIVES:**
  `adjudicated/2026/08/06/estate-report-2026-08-06.md` — **22,326 B, 2026-08-06T13:57:59Z**, verified
  live during this scoping. The block itself cites this path, and it is intact.
- **The adjudication block itself is fully recoverable** from version `Ew4TJljh` (§1) and is
  reproduced in the surprise-channel record.

**So the historical record is NOT lost.** What is wrong is that **the LEDGER says `PENDING` for a day
whose 13:58 run was adjudicated** — and per `main.tf` this module has **no alarm by design**, the
ledger *is* the miss-detector, so a reset day false-fires the backstop.

⚠ **AND IT IS INVISIBLE BY INSPECTION.** Sampled the ledger (23 manifest keys total):

```
2026-08-05  NO-SEMANTIC-CHANGES  adjudication PRESENT
2026-08-06  PENDING              adjudication absent   <- the clobbered day
2026-08-09  NO-SEMANTIC-CHANGES  adjudication PRESENT
2026-08-10  NO-SEMANTIC-CHANGES  adjudication PRESENT
2026-08-24  PENDING              adjudication absent   <- legitimately not yet adjudicated
2026-08-25  PENDING              adjudication absent   <- legitimately not yet adjudicated
```

**A clobbered day and a genuinely-un-adjudicated day are byte-identical in the ledger.** Nothing
about 08-06's row looks wrong. That is why this needed measuring rather than looking.

---

## 5. ⛔ THE REAL QUESTION IS NOT A REPAIR, AND IT IS NOT AE's

**The 21:49 run — the one that SUCCEEDED — was never adjudicated at all.** The 13:58 verdict cannot
stand in for it (§3). So the open question is:

> **Does 2026-08-06 require RE-adjudication of the successful run, or a ruling that the day is
> closed on the surviving 13:58 adjudication?**

**That is a `3.0.0_SA_CVO` judgment, not an AE write.** It is also exactly the interface CVO already
named as their own half — teaching `/estate-pull` to read `readjudication_required`. This item and
that one are the same seam viewed from two sides.

---

## 6. COST, AND THE SECOND-LANE ANSWER COO ASKED FOR

| | |
|---|---|
| **Mechanical cost** | **Trivial.** One merge + one `put_object`. Minutes. |
| **Judgment cost** | **The whole item.** Which verdict is true of which run is CVO's call. |
| **Does it need a second lane?** | ⛔ **YES — and the second lane is the PRIMARY one.** |

**Lane split:** the `adjudication` CONTENT is `3.0.0_SA_CVO`'s (they own verdicts and their name goes
on it). The S3 write is infra/AE. **An AE seat writing an adjudication block would be authoring a
verdict in CVO's name**, which is the thing to avoid regardless of how easy the PUT is.

⛔ **RECOMMENDATION — and it is "probably do nothing to the object":** the ledger's `PENDING` is
arguably *correct* for the successful 21:49 run, because that run genuinely was never adjudicated.
The defect may be entirely in the **carried-forward record of the 13:58 adjudication**, not in the
current status. **Do not repair the object until CVO rules which run 08-06's verdict is about.**
A repair before that ruling is a guess written into a ledger.

---

## 7. NOT DONE, NOT CLAIMED

- **Nothing written to S3.** No `put-object`, no `copy-object`, no version restore. Reads only.
- No ledger opened (no deploy begun). No repair attempted or staged.
- ⚠ **A census artifact, disclosed:** my first attempt to survey all 23 manifests piped
  `get-object` to `/dev/stdout` and returned **"unreadable" for all six sampled** — a **uniform**
  failure, which is an *instrument* signature, not a defect signature. Re-fetched to files and all
  six read cleanly. **The ledger is not corrupt; my probe was.** Recorded so nobody inherits an
  alarming false reading. The §4 table is from the sound run.
- The sample is **6 of 23** manifests, stated rather than generalised. A full census was not needed
  to answer the assigned question and would have cost ~23 round trips.

**Pointers:** `org/critical_paths/change_management/estate-report-manifest-carryforward-disarm-20260825.md`
· `infra/aws/terraform/estate-report/iam.tf:158-175` · `org/surprise_channel/OPAL_KIMIPIPELINE/INVESTIGATION_v1.md:241`
· the carry-forward disarm (stops NEW clobbers; explicitly does not repair this one).
