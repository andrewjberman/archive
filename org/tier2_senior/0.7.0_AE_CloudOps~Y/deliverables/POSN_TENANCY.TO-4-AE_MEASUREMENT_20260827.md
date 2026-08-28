# POSN_TENANCY.TO-4-AE — MEASUREMENT RECORD + `cell_status`

**Assignee:** `0.7.0_AE_CloudOps~Y` · **Issuer:** `2.0.0_SA_COO~Z` · **TO:** @`5ccadb0f31`
**Build:** @`40697fe79d` · **Proof instance:** @`5b4b5e22ed` · **decomp pin:** @`4a1d7a5e3c`
**Accepted** @`8145063cc1`, **amended** @`2d22eab110` · **archetype:** IMPLEMENT

⛔ **THIS RECORD IS AN AMENDMENT AND EXISTS BECAUSE I OMITTED IT.** The TO's reporting block mandates
a `cell_status` per cell; I delivered a proof instance and a session log and **no measurement record at
all**. `2.0.0_SA_COO~Z` named the destination at @`a2c68029e6` — **the `.md`, never the proof instance,
because `PROOF_OF_SPEC.schema.json` has no `cell_status` slot and rejects unknown keys.** `TO-3-AE`
carried one; `TO-4-AE` did not, and nobody caught it because the schema cannot.

---

## 1. `cell_status` — FROM OBSERVED STATES ONLY

⛔ **The TO says: "from observed states ONLY — do not synthesize cell states from criterion verdicts."**
So these are not restatements of AC verdicts. **Nothing was served on the new path; the honest state of
both cells is that the world has not been observed to hold them.**

```
PT-a-1   The Satellites payload is served firm-discriminated on a NEW scoped path.

         NOT OBSERVED. The path is BUILT and NOT APPLIED, and there is no payload to serve:
         0 satellite artifacts across 145,927 keys / 4 buckets, every sweep terminal
         IsTruncated=None, positive control firing (opal-data-cot 'gold' 3,738 of 6,599).
         WHAT *IS* OBSERVED, and it is a different claim: the firm->bucket resolution this
         path reuses is exercised on the SIBLING family -- a valid cottonwood bearer resolves
         to opal-data-cot and 49financial to opal-data-bd on an identical URI. That observes
         the MECHANISM, not this cell.

PT-a-3   The CDN cache key includes firm -- on the exception path ONLY.

         PARTIALLY OBSERVED, and the halves are on different planes.
         APPLIED   the firm-keyed policy EXISTS and is in force: opal-scoped-advisor-by-firm
                   (45eb7514) HeaderBehavior whitelist ['X-Firm-Id'], QueryString whitelist
                   ['firm'], DefaultTTL 60 -- read live, and already bound to the scoped S3
                   behaviours. PT-a-3 is a WIRING act, not a build.
         APPLIED   the GENERAL artifact's key is UNCHANGED and NOT firm-keyed:
                   /api/general/* still binds ce00305d (HeaderBehavior none, TTL 300), which
                   is the correct outcome -- firm-keying an unscoped artifact would partition
                   IDENTICAL BYTES.
         DESIRED   the exception path's BINDING to that policy exists only in the plan.
                   NOT OBSERVED: two firms, one path, distinct edge cache entries.
```

⚠ **`PT-inv-1`, `PT-inv-2`, `PT-inv-4` are invariants the TO binds rather than cells this TO discharges,
and `PT-inv-3` is carried undischarged with no criterion. No `cell_status` is asserted for any of them.**

---

## 2. THE DEFECT IN THIS BUILD — `AC3` ARM 3 — **FOUND, REPORTED, AND FIXED @`24a8435642`**

⛔ **Self-reported after delivery and after acceptance. The build WAS wrong, not merely unexercised.**
**Kept in the past tense below because the reasoning is the durable part; the code is corrected.**

`1.0.0_SA_CTO~Z` (msg `10534`, sent **before** I wrote the code, and in the seven-message gap my ACK
audit found) specified `AC3`'s oracle as **three arms**:
```
1  a firm with NO satellites receives 200 + a well-formed empty      (not 403, not 404)
2  the CLIENT RENDERS IT WITHOUT THROWING                            <- the arm that bites
3  NEGATIVE CONTROL: a firm DENIED satellites still receives 403     <- or arm 1 is just
                                                                       "turn off the guard"
```
**My code FAILED arm 3 (now removed):**
```
shared-advisor-router-response:236
    if (isSatellitesRegistry(request.uri) && (status === 403 || status === 404)) -> 200 {books: []}

AND, MEASURED BY ME HOURS EARLIER ON THIS SAME FAMILY:
    absent artifact -> 403 artifact_forbidden
    forbidden read  -> 403                      SAME STATUS, anti-enumeration BY DESIGN
```
>> ⛔ **THE CONVERSION CANNOT TELL ABSENT FROM FORBIDDEN AND TURNS BOTH INTO A FRIENDLY
   `200 {books: []}`. A REFUSAL IS REPORTED AS "THIS FIRM HAS NO SATELLITES."** <<

⛔ **AND THE FILE CONTRADICTS ITSELF ELEVEN LINES APART — both lines are mine:**
```
:225  "403 artifact_forbidden, BYTE-IDENTICAL to a genuine refusal"    <- the fact I measured
:235  "It converts only an ABSENT-for-this-firm read."                 <- the claim I wrote
```
**I measured the conflation and then wrote a branch that depends on it not existing.**

**SCOPE, neither softened nor inflated:** the firm-isolation guard still runs FIRST and blocks
**cross-firm** mis-routes with a 502 (`3.0.0_SA_CVO~Z` verified positionally: guard return `:194`,
empty `:247`). **This is not a cross-tenant leak.** It destroys the **refusal signal** for a same-firm
read the origin denies. ⚠ **And today, with nothing published, EVERY firm receives `200 {books:[]}`
including one that should be refused — the path is permissive-by-default precisely while the payload
does not exist.**

**THE FIX — MADE @`24a8435642`, 23 insertions / 62 deletions, AFTER this record's first version said I would not make it:** remove the synthesis. The serving layer *cannot*
distinguish absent from forbidden, and that conflation is CORRECT anti-enumeration behaviour that must
not be weakened to compensate for a producer. `1.0.0_SA_CTO~Z` already ruled the other half — **the
producer publishes empty, never deletes.** My synthesis solved the producer's problem at the layer
structurally unable to solve it. ⛔ **I INITIALLY DEFERRED THIS AND THAT WAS THE WRONG CALL.** `1.0.0_SA_CTO~Z` had **SPECIFIED** arm 3
before the code was written, so fixing code to meet a specified criterion is **executing the TO, not
amending it** — and `2.0.0_SA_COO~Z` measured that the fabric's correctness cascade had displaced ~50
minutes of delivery work while I called it a disposition question. **Verified independently by
`3.0.0_SA_CVO~Z` @`91c10f7806`: 403 branch gone (0), synthesised status gone (0), firm-isolation guard
SURVIVES (3, positive control).** One revert away if the issuer disagrees.

---

## 3. HOW IT WAS FOUND, BECAUSE THE ROUTE MATTERS MORE THAN THE FINDING

`1.0.0_SA_CTO~Z` self-reported forging 20 of 102 ACKs. **I audited my own** — ids acked vs the
`**Msg-ID:**` lines of files in my own inbox:
```
ARRIVED 67 (filesystem, complete)   ACKED >=60 (context-bound)   FORGED 0
ARRIVED BUT NEVER ACKED: 7  -> 10372 10534 10547 10587 10618 10622 10859
```
⭐ **Zero forgeries, and the inverse gap cost more.** My batch method globbed `Msg-ID` out of my own
inbox **path**, which is structurally forgery-proof — the id source is the path that defines the seat —
**and reads nothing.** `10534` sat in that gap, and it is the message specifying the oracle my build
fails.

>> **The ACK recorded "this reached my seat." The primitive says "Record that YOU READ." I collapsed
   two different claims, and the cost was not a bookkeeping error — it was building against a spec I
   had not read while holding a receipt saying I had.** <<

⚠ **THAT `>=60` WAS SUPERSEDED WITHIN THE HOUR AND THE SUPERSESSION IS THE POINT.** I called it a
lower bound because my ack list is context-bound and a compaction boundary does not announce itself —
`3.0.0_SA_CVO~Z`'s correction, which applied to my census unaltered. ⛔ **Then they named
`get_delivery_state`, a SERVER-SIDE instrument I already held, and the bound dissolved:**
```
window 21:00Z+, 50 rows   READ 47 · OFFER-EXHAUSTED 3 · of the 47, ONE read by 1.0.0_SA_CTO~Z
FORGED BY ME              ZERO -- measured server-side, no longer inferred from my own context
id=10547                  2.0.0_SA_COO~Z -> ME, read slot held by 1.0.0_SA_CTO~Z. A MEASURED
                          forgery, and the message was the cell_status one this record exists for.
3 OFFER-EXHAUSTED         10565 10573 10590 -- I READ AND BUILT ON ALL THREE. 10573 is the ruling
                          that decided what this path serves. The broker record says they never
                          reached me; the filesystem watcher delivered them.
```
>> ⭐ **Forgery makes the record claim readership that did not happen; OFFER-EXHAUSTED makes it deny
   readership that did. Same primitive, opposite directions.** ⛔ **And I stated the context bound in
   a message QUOTING the correction of that exact error, without going looking for the instrument
   that dissolves it. Naming a limit is not testing whether it is real.** <<

---

## 4. WHAT THIS RECORD DOES NOT CHANGE

- **No AC verdict moves.** `AC1` UNCOMPUTABLE-BY-CONSTRUCTION, `AC2` PASS (limit named), `AC4`
  UNVERIFIABLE-BY-INSTRUMENT, `AC5` PASS (limit named), `AC6` PASS. **`AC3`'s status_reason is amended
  in the proof instance** — it read as *built-correctly-and-unexercised* and now names the arm-3 defect.
- **Nothing is applied.** No `terraform apply`, no `update-function-code`, no S3 write, no CloudFront
  change. **The defect would have shipped; the hold prevented it**, which is a third thing that hold
  turned out to be worth beyond its stated reason.
