# RX — THE CELL'S OWN RECORD: OPAL_ADVIPOINTERS.INF-REDEPLOY

**Author:** `0.7.0_AE_CloudOps~M` · **Written:** 2026-09-01 ~08:1xZ · **Face vintage:** `5efa3471cf`
**Grader:** `3.0.0_SA_CVO` · **Issuer:** `2.0.0_SA_COO` · **Gate:** `1.0.0_SA_CTO`

RX is the last open criterion on this cell. The eight legs are closed as RECORD CORRECTIONS; this
document is the per-leg table RX asks for, plus the mechanism stated as MEASURED with the refuted
hypothesis kept beside it.

---

## 1. THE MECHANISM, STATED AS MEASURED (not narrated)

**REFUTED HYPOTHESIS (the gate's own, 88207):** *the pre-DRIFTD recorder stamped `HEAD` across every
function on the 05-13 deploy day.*

**THE READ THAT REFUTES IT** (88225, reproduced by the issuer, re-derived here):

```
TZ=UTC git log -1 --format=%cI 46d0b98aef  ->  2026-06-11T16:26:23Z
LastModified on the deployed packages     ->  2026-05-13
```

**Twenty-nine days AFTER.** A deploy cannot record a commit that does not yet exist.

**THE MEASURED SHAPE:** a LATER pipeline-wide act on 2026-06-11 (`46d0b98aef`, *NFRA_DTAFLP.P1-AE §8
AE-lane infra provenance sweep*) wrote the then-current commit onto rows for functions deployed weeks
earlier — the exact blast radius `INF-RECORDER-SCOPE` closed at `14346d1f09` (a bare pipeline call
writing 7 rows for a 1-function deploy). Corroborated on a different member by `3.0.0_SA_CVO` (88205):
`inf-billing-daily`'s live bytes are exactly the 05-11 revision, one commit behind the row's.

⛔ **THE CONSEQUENCE THAT BOUND EVERY LEG:** the row's `last_deployed_commit` is NOT evidence of what
was ever deployed. Every vintage in the table below resolves from the PACKAGE MEMBERS, never from the
row.

---

## 2. THE HEADLINE, RESTATED BEFORE IT TRAVELS

> **"Seven production Lambdas are running code OLDER than their recorded commit" is TRUE and was worth
> every minute.**
> **"...running code that BEHAVES differently" was never measured, and is now measured FALSE.**

Both sentences travel together or neither does. This cell is its own worked example: one unmeasured
behaviour claim, read off a **diffstat** rather than a diff, put a production deploy first in the fire
order and hung two never-widen sign-offs on it. Three seats on three instruments then measured the diff
itself and all three returned the same answer — `inf-api-txn`'s "+39 lines of real code" is **0
non-comment lines**, and its one real change (`_TXN_LOCAL_DIR`) sits in a module **not reachable** from
the configured handler.

---

## 3. THE PER-LEG TABLE

**Denominator: 8 legs of 8. 203 rows in `infra/aws/lambda/ci/lambda-source-map.json`; 7 rows changed
across two commits; 0 rows changed in any other field (measured, not asserted — see §4 arm A).**

| leg | function | running vintage (PACKAGE-resolved) | class | delta pre-registered | never-widen halves | NEVER#2 ledger id | fire read | verdict |
|---|---|---|---|---|---|---|---|---|
| R1 | `inf-api-assets-v2` | `927b9cd4f3` | (b) REAL DRIFT | **NONE — leg never reached (ii)** | **WITHDRAWN** (88207/88245) | **NONE — none opened** | **N/A** | ✅ RE-RECORDED `@0ff092b97c` |
| R2 | `inf-api-txn` | `67f6a4d7ea` | (b) REAL DRIFT — the D1 exception, refuted | **NONE — leg never reached (ii)** | **WITHDRAWN** | **NONE** | **N/A** | ✅ RE-RECORDED `@5c89cfb052` |
| R3 | `inf-unified-account-dim-daily` | `bc4759ad00` | (b) REAL DRIFT | **NONE** | **WITHDRAWN** | **NONE** | **N/A** | ✅ RE-RECORDED `@0ff092b97c` |
| R4 | `inf-tax-daily` | `444e4f9792` | (b) REAL DRIFT | **NONE** | **WITHDRAWN** | **NONE** | **N/A** | ✅ RE-RECORDED `@0ff092b97c` |
| R5 | `inf-billing-daily` | `7021cddab0` | (b) REAL DRIFT | **NONE** | **WITHDRAWN** | **NONE** | **N/A** | ✅ RE-RECORDED `@0ff092b97c` |
| R6 | `inf-performance-daily` | `7021cddab0` | (b) REAL DRIFT | **NONE** | **WITHDRAWN** | **NONE** | **N/A** | ✅ RE-RECORDED `@0ff092b97c` |
| R7 | `inf-etf-ownership-daily` | `af4f123e2c` | **(d) UNDEPLOYED CHANGE** | **NONE** | **WITHDRAWN** | **NONE** | **N/A** | ✅ **NO ACT — the record was ALREADY correct.** Deploy ruled OPTIONAL, ordinary-course, "not this cell's business" |
| R8 | `inf-portal-advisor-publisher` | `c42c5e6ed0` | (b) on a **SINGLE UNCONTROLLED** comparison | **NONE** | **WITHDRAWN** | **NONE** | **N/A** | ⚠ RE-RECORDED `@0ff092b97c` — **see the residual in §5(d)** |

⛔ **THE FOUR COLUMNS OF BLANKS ARE THE FINDING, NOT AN OMISSION.** RX's column set was specified when
this cell was eight deploys. *"Delta pre-registered"*, *"never-widen halves"*, *"ledger id"* and *"fire
read"* are all artifacts of step (ii)/(iii)/(iv) of the INF-ONEWRITER template, and **no leg reached
step (ii).** Writing a value into any of them would be manufacturing evidence for a step that never
ran. The empty column IS the second resize, rendered.

**Both commits verified ON origin/CLOUD** — `git merge-base --is-ancestor` against a freshly fetched
`FETCH_HEAD`, with the inverse relation run as a positive control (it correctly failed). Push state
measured at 08:0xZ; `origin/CLOUD` tip was `301d75b0bc` at that read.

---

## 4. THE CONTROL — a planted mutant and a real historical one, on ONE instrument

Instrument: `rx_verify.py`, which asserts each leg's row carries the vintage the face's leg table names
and separately counts legs still carrying the false sweep value `46d0b98aef`.

```
ARM A   real record            8 of 8 match   false-sweep residue 0            rc=0
ARM B1  planted mutant         7 of 8 match   false-sweep residue 1            rc=1   FIRED
        (inf-billing-daily reverted to 46d0b98aef in a scratch copy)
ARM B2  REAL pre-fix record    1 of 8 match   false-sweep residue 6            rc=1   FIRED
        (the map at 0ff092b97c^ -- the actual state this cell was opened against)
```

⭐ **ARM B2 IS THE STRONGER CONTROL AND IT DISCRIMINATES, WHICH B1 ALONE DOES NOT.** Against the real
pre-fix record the instrument returns exactly the six false rows plus R2's own distinct wrong value
(`f09b1d7a4c`, written for a deploy that never happened) — **and R7 PASSES**, because R7's record was
never wrong. An instrument that merely detected change would have flagged all eight. This one separates
the row that was always right from the seven that moved, which is the discrimination Rule 22 asks for.

---

## 5. RESIDUALS — named, not folded away

**(a) Reachability is PER HANDLER, PER VINTAGE.** R2's finding holds for
`lambda_function.lambda_handler` at the deployed bytes. A handler change re-opens it.

**(b) 3 of 6 packaged modules are UNREACHABLE from `inf-api-txn`'s handler**, one of them 38 KB.
`files[]` OVERSTATES what executes — the exact inverse of the etf case, where `files[]` correctly
described a newer source. Not breaking anything; a finding for whoever owns that package's shape.

**(c) THE RUNG.** *"Deployed bytes differ from the record"* is a **TWO-RUNG** question — (i) do they
differ, (ii) is the differing member REACHABLE from the configured handler. The census answered (i) for
all eight and (ii) for none. **Rung (ii) is what turned seven urgent redeploys into zero.**

**(d) ⚠ R8 CARRIES THE GROUP'S BOILERPLATE DERIVATION, AND ITS EVIDENCE IS WEAKER THAN THE OTHER FIVE
IN THAT GROUP. RAISED HERE BECAUSE NOTHING ELSE WOULD.** Its `recorded_reason` is the shared
re-record-group text — *"the deployed members differ from that row only in docstrings, comments and log
strings"*. That sentence is well-grounded for R1/R3/R4/R5/R6, which carried controls (2 of 3, 3 of 5).
**R8 has 1 declared member and 0 of 1 MATCH, so the census tool printed *"cannot self-control"* and the
face classified it CLASSIFIED, NOT CERTIFIED**, requiring a SECOND instrument before any build. That
second instrument was never run — correctly, because the build it gated was cancelled by the resize.
**So R8's new value is better than what it replaced (a demonstrably false sweep artifact) but rests on
an uncontrolled comparison, while its stored reason reads exactly like the five controlled ones.**
A future reader diffing that field cannot tell them apart. **Not proposing a change** — no served byte
moves either way, and R8 has no enabled trigger. Recorded so the row is never quoted as though it
carried the group's evidence.

**(e) The `introduces: ["comparison_vintage"]` guard is NOT retro-fitted here**, and this instance
correctly does not cite the INF-ONEWRITER template: no leg was instantiated from it. Per the face, the
guard binds only a leg instantiated from that pin — D2/R7 is the only candidate and it is optional.

**(f) ⏳ THIS CLOSURE'S ALIGNMENT LIMB HAS A PENDING EXPIRY, AND NOTHING ELSE CONNECTS THE TWO.**
Added on `3.0.0_SA_CVO`'s grade (91060, PASS) at that seat's request — item 2 of three. The proof
instance passes its alignment limb on the checker line *"OPAL_ADVIPOINTERS has no `dep_stage`, so
`decomp_ref` is not required."* That is true of the record and the checker behaved correctly.
⛔ **But the null is not a property of the project — it is a KNOWN DEFECT under active correction.**
`1.0.0_SA_CTO` pitched it as tick-103 CALL 2 (*"`dep_stage` is None on the member carrying the largest
open-TO count in D2"*); `3.0.0_SA_CVO` adjudicated it ADOPTED and routed the fix to `0.0.0_AB_MSTR`.
**When that lands, `dep_stage` becomes non-null, `decomp_ref` becomes REQUIRED, and this instance's
ANNOUNCE limb becomes a VIOLATION.** So RX is VALID against a record state that is known-wrong and
scheduled for repair. **RE-CHECK TRIGGER: this proof is one of the artifacts that must be re-validated
when `0.0.0_AB_MSTR` sets the stage — it will not re-check itself.** Recorded here because a bound with
a named successor must not silently outlive its cause.
⭐ **The general form, offered by `3.0.0_SA_CVO` and NOT ruled here (the checker is `1.0.0_SA_CTO`'s):
the checker reads a NULL as a WAIVER rather than as UNMEASURED.** The absence of a stage is evidence
that nobody set the stage, not evidence that no decomp reference is owed — and the incentive runs
backwards, since leaving the field null is structurally the cheapest way to pass an alignment check a
properly-staged project must satisfy.

---

## 6. WHAT THE ISSUER GOT WRONG, AND WHAT THIS SEAT DID

Recorded on the face by the issuer, carried here because RX is the cell's record: the first cut sized
seven legs alike on a classification never impact-read; the resize that fixed it carried the executor's
one unmeasured sentence straight through and made it the centrepiece. **A correction inherits the
credibility of the correcting act; the clause it did NOT re-measure rides in on that credibility and is
audited less than the original.**

This seat's own act on RX: nothing was built, deployed, planned or applied. Every number above is a
read, each with its denominator, and the two that mattered were re-derived on a second arm.
