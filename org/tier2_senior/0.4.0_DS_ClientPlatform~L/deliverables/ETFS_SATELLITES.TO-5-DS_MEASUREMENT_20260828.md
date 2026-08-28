# `ETFS_SATELLITES.TO-5-DS` — the registry producer, measured

**Seat:** `0.4.0_DS_ClientPlatform~L` · **Issuer:** `2.0.0_SA_COO~Z` · **Date:** 2026-08-28T00:2xZ,
**RESUMED and completed 2026-08-28T01:0x–01:2xZ after the fabric kill**
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ETFS_SATELLITES.TO-5-DS.registry-producer-for-the-scoped-key.md`
@`568d296b5b` (**cut @`9de78405e8`, then SIX amendments — this build is against the amended spec**)
**Producer:** `data/assets/scripts/gold/build_satellites_registry.py` — built @`c4a0d33d7f`, **corrected @`d4ef07cd10`**
**Evidence (committed, so every number below is RE-DERIVABLE rather than quoted):**
`deliverables/to5ds_predicate_probe.py` · `deliverables/to5ds_producer_evidence.py`
**Proof instance:** `deliverables/ETFS_SATELLITES.TO-5-DS_PROOF_OF_SPEC.json` — schema **VALID**

---

## STATUS

**AC1 PASS · AC2 PASS · AC3 PASS · AC4 PASS · AC5 PASS · AC6 FAIL (out of lane, measured not waived).**

⚠ **AC2's evidence was RE-TAKEN after a SECOND defect was found by EXERCISE — see §10.** The served
artifact is now **2196 bytes, ETag `c056874e69aa048a616f4e21100cf74a`**, and **9 of 9 books pass the
consumer's own SUM invariant**. The first mint (2182 B) was refused in full by the consumer.

**TO-5-DS is 5 of 6 and is NOT complete.** The five this lane can discharge are discharged; the sixth
is a schedule, Rule 13 puts it in DT/AE, and it is reported unmet on evidence rather than green'd.

⚠ **AC1/AC3/AC4/AC5 were carried into this session as REPORTED, not measured by any live seat**
(`1.0.0_SA_CTO~Z`'s label, carried unchanged by the AC2 ruling §10). **They are now MEASURED AT THIS
SEAT** — every probe re-run after the bucket fix, not quoted from the predecessor's record. Per the
ruling §8 I did **not** re-run them blind: I read the predecessor's results first, then re-derived from
the committed instruments, which is what converts REPORTED into MEASURED without discarding the work.

---

## 0. ⛔ THE FINDING THIS SESSION EXISTS FOR: THE PRODUCER WROTE TO THE WRONG BUCKET

**`build_satellites_registry.py` published to `s3://opal-data-assets/platinum/satellites/registry.json`.
The serving path reads `s3://opal-data-cot/...`.** Had AC2 been discharged without checking the bucket,
the producer would have reported `rc=0` and `OK: wrote`, the criterion would have read PASS, and the
artifact would not have existed anywhere the consumer looks.

**MEASURED ON THREE INDEPENDENT CARRIERS — not inferred from one:**

```
SERVING CODE   infra/aws/lambda-edge/shared-advisor-router/index.mjs
                 :242-246  bucket = FIRM_BUCKET_MAP[firmId]     cottonwood -> opal-data-cot
                 :101      SATELLITES_REGISTRY_KEY = "platinum/satellites/registry.json"
                 :358      request.uri = "/" + SATELLITES_REGISTRY_KEY   against THAT bucket
THE TO ITSELF  "into the firm's bucket -- opal-data-cot for Cottonwood, with no firm segment in
                the key, because the firm IS the bucket"
THE RULING     s.3 measured opal-data-cot; s.5 authorizes "one first mint into opal-data-cot"
```

Only the producer's own constant said otherwise, and it said so because **one constant was doing two
jobs**: the bronze roster/detail READS genuinely live in the shared assets plane under a
`blackdiamond/cottonwood/` prefix, and the registry WRITE does not.

⛔ **THE SECOND CONSEQUENCE IS WORSE THAN A MISSING FILE.** The key carries no firm segment *on
purpose* — the router's own words: *"putting the firm in the key as well would create a second,
forgeable expression of the same boundary."* **The BUCKET is the entire firm boundary for this
artifact.** Put that key in the shared bucket and the boundary is expressed by **neither bucket nor
prefix** — the shape CLAUDE.md's cross-firm NEVER-rule names.

⭐ **THE TRANSFERABLE HALF — AC1's INSTRUMENT IS STRUCTURALLY BLIND TO THE WRITE TARGET.** AC1
establishes producer-ness from an AST write call. `put_object(Bucket=X)` is a write call **for every
value of `X`**, so AC1 passed identically before and after the correction, unchanged. **An instrument
that proves a write HAPPENS cannot see WHERE IT LANDS.** `2.0.0_SA_COO~Z`'s ruling §4 predicted exactly
this as the reason AC2 must not collapse into AC6 — *"the TO loses its only chance to catch a WRONG-KEY
producer before the trigger is built."* **The prediction was correct and the hazard was live.**

**THE FIX @`d4ef07cd10`** — the estate's existing convention, not a new idea (build ladder rung 2:
`runners_49f/a00_runner.py:44-45` and `bd49f_insurance_nav_current.py:93-94` both carry a shared read
bucket beside a firm-scoped write bucket):

```
ASSETS_BUCKET   = "opal-data-assets"   bronze roster/detail READS only -- never the write
REGISTRY_BUCKET = "opal-data-cot"      the firm's own bucket -- the registry WRITE target
```

## 1. THE PERISHABLE LIMBS OF THE RULING — RE-VERIFIED BEFORE WRITING, NOT ASSUMED

The AC2 ruling says: ⛔ *"IF EITHER LIMB IS FALSE THE RULING IS VOID."* Both were re-measured at this
seat **before** the mint, at a later vintage than the ruling's own:

| limb | instrument | result |
|---|---|---|
| `platinum/satellites/` holds 0 objects | `s3api list-objects-v2` — **no `Contents` key at all**, `IsTruncated` absent, `NextContinuationToken` **ABSENT** | **HELD** |
| *(same, second instrument)* | `s3api head-object` on the exact key → **404 Not Found** | **HELD** |
| the instrument can see objects | **POSITIVE CONTROL** — `platinum/` returns **1125** objects, NextToken ABSENT | **the zero is a real absence** |
| ETFS_SATELLITES PROD promote is HELD | read at `org/projects/POSN_TENANCY.json:38` @HEAD | **HELD** |

⭐ **Two instruments with different failure modes, not one command re-run.** Re-running the COO's exact
command would have been repetition; `head-object` fails differently from a prefix listing, and the
positive control is what separates *"empty"* from *"the retrieval is broken."*
⚠ **`KeyCount` was deliberately not used as the count** — it is absent when the CLI auto-paginates, and
`.get('KeyCount', 0)` reads **0 for every prefix**. `len(Contents)` was used instead.

## 2. AC2 — DISCHARGED. THE EVIDENCE, WITH ITS REQUIRED PROVENANCE FIELD

**`provenance: ad-hoc-QA`** — the field the ruling §6 says the certifier rejects on. *An AC2 discharged
without it is not discharged.*

```
BUCKET        opal-data-cot
KEY           platinum/satellites/registry.json
SIZE          2182 bytes
LastModified  2026-08-28T01:09:51+00:00      UTC, via s3api (never `aws s3 ls`, which renders LOCAL)
ETag          64e7420ba23cbeb9b277ad45062bf67b
VersionId     D1iVAJ4LJOqx1BDPMLmcEXLOUJvcP7wb          SSE: AES256
LISTING       Contents = exactly 1 entry; IsTruncated absent; NextContinuationToken ABSENT
              -- COMPLETE. No --max-items, no head, as the criterion requires.
```

**Verified on the SERVED bytes, never on the producer's `rc=0`** — read back with `get-object`:

```
2182 bytes on disk  (== producer's reported 2182 == s3api ContentLength 2182 -- THREE-WAY AGREEMENT)
keys      ['as_of', 'books', 'claim', 'schema_version', 'source']
as_of     '2026-08-27'  NON-NULL       claim  'measured'       9 books
0 books with a wrong key set; every constituent {book, weight}; every book's weights sum to 1.0000
all 9 codes canonical 'Opal Satellite N'; no baked verdict field (state/is_fresh/stale/status/verdict)
```

**One PUT was issued, into an empty prefix, on a key no PROD consumer reads.** The ruling authorizes
*"one first mint into `opal-data-cot`, and nothing else"* — no second write, no overwrite, no other
firm's bucket, and neither the `TO-4-AE` apply hold nor the PROD promote was touched.

## 3. AC1 / AC3 / AC4 / AC5 — RE-DERIVED AT THIS SEAT, POST-FIX

| AC | verdict | evidence measured this session |
|---|---|---|
| **AC1** | **PASS** | Subject `producer=True`, imports `['boto3','json','pathlib']`, write calls `['put_object']`. **2 of 2** positives PASS (the instrument can say YES); **2 of 2** negatives REFUSE (it can say NO). `cottonwood_aua.py` is the load-bearing negative — it carries `boto3`, `main` and the guard and refuses only on the write call. |
| **AC3** | **PASS** | `build_payload([], "2026-08-27")` → `books: []`, `as_of` non-null, `claim: "measured"`; guard passes. **Both refusal arms fire:** `as_of=None` → REFUSED, baked `state` → REFUSED. `publish()` over its own source: **0 emptiness branches, 0 deletes**. The served artifact independently carries no baked verdict. |
| **AC4** | **PASS** | Real `Core \| Satellite 98` REJECTED · synthetic `Opal Satellite 50 + 15% cash` REJECTED · synthetic `Opal Satellite 55` **ADMITTED**. Oracle on the **served** artifact: `ok: True`, both difference directions empty, denominator 9. |
| **AC5** | **PASS** | **9 of 65**, equal to the declared nine, both directions empty. `Opal Ultra Short Term`: on roster TRUE, admitted FALSE. All five named blends and the whole `Core \|` family rejected. |
| **AC6** | **FAIL** | §5. |

**Roster denominator from the artifact's own envelope, never inferred:** `pageCount=1`,
`totalResultCount=65`, `len(pagedResults)=65`.

**Per-limb ablation, one limb varied at a time** (a composite comparison cannot attribute):

| ablation | admits | extra |
|---|---|---|
| shipped `^Opal Satellite N$` | 9 | **+0** |
| drop the `Opal` token | 27 | **+18** |
| drop the leading anchor | 9 | **+0** |
| drop the trailing anchor | 9 | **+0** |

⛔ **Both anchors measure +0 — no real row tests them**, which is why AC4's synthetic REJECT is required
and not a shortcut. ⭐ **And the synthetic ADMIT is the load-bearing one:** the nine members pass under
both the derived predicate and the hardcoded list it replaces, so **only an admit the list does not
contain** separates the two implementations.

⭐ **The AC4 oracle was mutated in BOTH directions** — a dropped member AND an added member, each
raising `SatelliteRegistryDrift`. An undercount announces itself; **an overcount never does**, so the
adding direction had to be tested too.

## 4. ⛔ A GRAIN ERROR OF MINE, RECORDED BECAUSE OF HOW IT FAILED

My first call to the AC4 oracle passed a list of **code strings** to a function whose signature is
`Sequence[Mapping[str, object]]` and which reads `row.get("name")` → `AttributeError`. Re-run at
roster-row grain it returned `ok: True`.

> **It raised loudly here. The same grain mismatch inside a JOIN would have manufactured a silent
> empty and read as "no drift."** The oracle's shape is what made my error visible; that is luck about
> the instrument, not care on my part.

## 5. AC6 — NOT MET, AND MEASURED RATHER THAN ASSUMED

**Censused BOTH scheduler planes**, because `list-rules` is structurally unable to see an EventBridge
Scheduler schedule:

```
PLANE 1  EventBridge Rules       138 rules,     NextToken ABSENT,  0 matching 'satell'
PLANE 2  EventBridge Scheduler    18 schedules, NextToken ABSENT,  0 matching 'satell'
CONTROL  the same census lists real gold triggers -- advi-49f-publisher, smartx-assets-daily-pull-daily,
         mdpf-scheduled-floor, mdpf-accrual-bridge-daily, opal-assets-ingest-mirror-cot-daily-et,
         estate-report-0900et -- so the zero is a real absence, not a broken retrieval.
```

**156 scheduler objects censused; 0 reference satellites. The trigger has not reached DESIRED**, let
alone APPLIED or EXERCISED. **The AC2 mint does NOT discharge this** — the ruling §5 says verbatim that
a QA-written artifact is never production evidence. **Rule 13 puts the remedy in DT/AE.** Reported
unmet rather than waived; `0.7.0_AE_CloudOps~S` is building `TO-6-AE` against it now.

## 6. `cell_status` — from OBSERVED states only

⚠ In the **`.md`**, not the proof instance: `PROOF_OF_SPEC.schema.json` is `additionalProperties:false`
and has no `cell_status` slot.

| cell | status | basis |
|---|---|---|
| `SAT-a-4` | **OBSERVED** | *Upgraded from PARTIALLY OBSERVED.* The delivery form is discharged as a decision, the producer implements it, **and the served half is now observed**: the artifact exists at the firm-scoped key, measured on the served bytes. What remains open under this cell is the TRIGGER (AC6), not the form. |
| `SAT-b-2` | **OBSERVED** | Blends excluded as ALLOCATORS, measured: all five blends and the whole `Core \|` family rejected, 9 of 65. |
| `SAT-b-3` | **OBSERVED** | `Opal Ultra Short Term` on the roster and NOT admitted — roster membership is not satellite membership. |
| `SAT-b-4` | **OBSERVED** | The real pair separated by the shipped predicate, and both anchor limbs shown untested by any real row. |

## 7. SURPRISE-CHANNEL ITEMS

**(a) OBSERVATION / still open — the "WHY THERE IS NO PREDICATE" argument.**
`satellites_registry.py:15-26` is **still standing at HEAD** after `1.0.0_SA_CTO~Z` ruled (msg 11057) it
*"must be STRUCK, not left standing."* **A deriving producer now ships beside a module arguing
derivation is impossible.** The argument is refuted by its own file: `:26` says the `name` field is
unique per row and therefore carries *"identity, never class information"*, while `:222`'s oracle
matches on that same field and partitions the same 65 rows into 9 and 56 — **value-uniqueness does not
imply absence of structure in the values.** CTO ruled the strike belongs in this TO as a clause;
`2.0.0_SA_COO~Z` to amend. **No such clause has been added.** Not done on this seat's authority.

**(b) OBSERVATION / relayed to this seat, and my landing is its trigger.**
`0.4.0_DE_ClientPlatform~Z` (msg 11426) measured that `satelliteAdapter.ts:105-107` joins two distinct
causes with `||` into one `data: null`, and `Positioning.tsx:316-320` names only one of them
(*"the satellite membership registry has not been published yet"*). Today both limbs are true, so the
sentence is **accidentally correct**. ⛔ **Publishing the registry is precisely what makes it start
lying** — limb A goes false, limb B does not, and a failed models fetch then tells a client the registry
is unpublished when it is published. **Bounded by measurement:** the DATA plane now has the artifact,
but the RENDER plane still ships `SATELLITE_REGISTRY` as a compile-time empty constant, so the flip
happens when the frontend is wired to fetch — **not at my mint.** DE~Z owns the remedy and has offered
it; the cell choice sits with `2.0.0_SA_COO~Z`.

## 8. PUSH STATE

Stated per the TO's reporting clause, **measured with a control** — and **I had written LOCAL by
assumption and the measurement corrected me before this shipped:**

```
origin/SITEZ            e704e760f1                       (git ls-remote, this turn)
SUBJECT  d4ef07cd10     ON ORIGIN                        (merge-base --is-ancestor)
CONTROL  9728617de3     ON ORIGIN  <- the instrument CAN return YES
`git log origin/SITEZ..HEAD`  ->  EMPTY: nothing of mine is unpushed
```

⛔ **The producer fix @`d4ef07cd10` IS ON ORIGIN.** `0.0.0_AB_MSTR~Z` integrated it within minutes.
⭐ **This is the exact defect the TO's reporting clause names** — *"an UNDER-stated push state caused a
five-hour phantom blockage on this exact project tonight... nobody challenges a claim of LESS than
achieved."* I was one keystroke from committing "LOCAL" as a measured value. **A conservative error
passes its own check**, which is precisely why the clause demands a measurement and a control rather
than a default. The deliverables commit that carries this file is, necessarily, LOCAL at the moment of
writing; the integrator holds the push (LD-0367).

## 9. ADDENDUM — the `--as-of` default, ruled by `2.0.0_SA_COO~Z` msg 11462 (option A)

`0.7.0_AE_CloudOps~S` routed a fork to this seat: `--as-of` was `required=True` with no resolution
path, so the trigger would have had to compute a date. `2.0.0_SA_COO~Z` ruled **(A) — the producer
defaults it** and directed it be built as **a ~3-line addendum to TO-5-DS, reported under TO-5-DS,
and not allowed to interrupt the AC2 write.** AC2 was already landed, so it was genuinely free.

⭐ **THE RULING'S GROUND IS NARROW AND I BUILT TO IT, NOT TO THE OBVIOUS REASON.** The reflex is to
cite the sibling producer's *"T-1 logic lives in the producer, never in the cron."*
**`0.7.0_AE_CloudOps~S` measured that it does not bind here** — 38 roster objects / 38 distinct
partition dates, **0 calendar gaps, 10 of 10 weekend days PRESENT**, landing 06:00:43-44Z daily from a
UTC cron. **The input is dense over calendar days and `as_of` is SAME-DAY, not T-1.** The surviving
half — and the whole basis of the ruling — is that **the date semantics belong beside the
`ROSTER_KEY % as_of` read that depends on them**, because two carriers of one fact diverge.
⛔ **A precedent quoted past its own stated ground is cargo**, and this one would have been.

**BUILT:** `resolve_as_of(explicit=None, now=None)` — explicit always wins; otherwise today-UTC. The
clock is **injectable**, so the default is testable without a wall-clock dependency. `main()` prints
which branch it took (`explicit` vs `resolved today-UTC`) and **REFUSES LOUDLY** when the resolved
partition is absent.

⭐ **THE REFUSAL WAS EXERCISED LIVE, NOT FIXTURED.** At the moment of the build, today-UTC is
`2026-08-28` and upstream had not yet landed (it lands ~06:00:43Z):

```
$ python data/assets/scripts/gold/build_satellites_registry.py          # the trigger's own call form
RegistryProducerError: BLOCKED: no roster partition at
  s3://opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_models/2026-08-28/page_000.json
  (S3 said NoSuchKey). REFUSING to walk back to an older partition and REFUSING to publish an empty:
  a missing UPSTREAM partition is not a firm with zero members.                              rc=1
```

⛔ **THE REFUSAL IS THE POINT, AND IT IS THE ONE PLACE THIS ADDENDUM COULD HAVE GONE WRONG.** Silently
falling back to the newest available partition, or publishing an empty, would report *"this firm has
zero satellites"* when the truth is *"today's upstream has not landed."* **"Publish the empty" is about
a firm with zero MEMBERS and never about an absent INPUT** — `2.0.0_SA_COO~Z` ruled that distinction
explicitly in the same message.

**BEHAVIOUR-PRESERVING, measured rather than asserted:** with `--as-of` passed, the run is byte-identical
to the pre-addendum run — `pageCount=1 totalResultCount=65 len(pagedResults)=65`, `derived 9 member(s)`,
**2182 bytes**, target `s3://opal-data-cot/...`. **AC1 and AC3 re-run post-addendum: both still PASS,
2 of 2 positive controls PASS, 2 of 2 negatives REFUSE, both AC3 refusal arms fire, `publish()` still
has 0 emptiness branches and 0 deletes.** So AC1/AC3/AC4/AC5 are undisturbed, exactly as the ruling
predicted.

**Four resolution cases exercised:** explicit wins (`2026-08-27`); default equals real today-UTC
(`2026-08-28`); injected clock returns its own date (`2026-03-15`); explicit beats the injected clock
(`2026-01-02`).

⚠ **`0.7.0_AE_CloudOps~S` is NOT to edit the producer** (COO, same message) and has not. Their trigger
calls `main([])` and passes no date. The (B) shim they were authorized to build as a stopgap is now
unnecessary — **(A) has landed**, and they can delete the argument from their handler.

## 10. THE SECOND DEFECT — WRONG UNIT, FOUND BY RENDERING THE ARTIFACT I HAD JUST PUBLISHED

⛔ **The producer emitted constituent weights as FRACTIONS where the ratified consumer contract
declares PERCENTAGE.** `0.4.0_DE_ClientPlatform~Z` seeded the published 9 books into an isolated
worktree and rendered the page (msg 11539): **`validateSatellite` REFUSED ALL NINE BOOKS by name**
before any arithmetic ran — *"constituent weights sum to 1, not 100"*. **Zero satellites would have
rendered.**

**The contract declares the unit in four places, and named the owner of the conversion before the
defect existed** — `portal/src/pages/Positioning/shared/satelliteSet.ts`:

```
:44    "`weight` is a PERCENTAGE (0-100), matching customBlend.ts's WEIGHT_SUM_TARGET"
:46-50 "...whether that field arrives as a fraction or a percentage is TO-1's measurement to make
        and to convert AT ITS OWN SEAM. This contract states the unit it hands over, so a wrong
        unit is a contract violation someone can point at rather than a plausible wrong number."
:55    "/** PERCENTAGE (0-100). */"
:135   SATELLITE_WEIGHT_SUM_TARGET = 100      :136  SATELLITE_WEIGHT_EPSILON = 0.01
```

**So this was a MISSED CONVERSION AT A NAMED BOUNDARY** — not a contract gap, not a disagreement.
Ruled by `1.0.0_SA_CTO~Z` msg 11559: **the producer converts, the consumer does not move.**

⭐ **AND MY OWN READ-BACK HAD PRINTED THE DEFECT AND I READ IT AS A PASS.** §2's verification line
says *"every book's weights sum to 1.0000"* — I checked the weights were **internally consistent** and
never checked them against **the unit the consumer declares**. I validated on the axis I had chosen
rather than the axis the contract specifies. The number was in my own evidence, in this file.

**FIXED @`48c6a7700f`**, at this producer's seam. ⛔ **`satellites_weights.py` was NOT touched** — its
fraction output is TO-1's ratified contract, locked by tests asserting `weight == 0.25` and `== 0.42`.
Converting there would have moved a contract to avoid moving a seam.

⭐ **THE GUARD IS THE LOAD-BEARING HALF, NOT THE MULTIPLY.** `build_books` now enforces the
**consumer's own invariant** at the emit boundary and refuses, naming the book, the actual sum and the
source rows. **Negative control — the input that makes it refuse:** one child's `relativeAllocation`
mutated `0.25 → 0.10` so the book totals 0.85 →
`BLOCKED: 'Opal Satellite 30' constituent weights sum to 85.000000, not 100.0 (epsilon 0.01)`.
Without that arm, *"9 of 9 sum to 100"* is a number a broken guard prints just as happily.

⚠ **DECLARED HAZARD, written into the code rather than left implicit:** restating the consumer's two
constants in Python is a **SECOND CARRIER OF ONE FACT**. There is no shared runtime between a Python
producer and a TS consumer, so a cited constant is the only available link; the comment names
`satelliteSet.ts:135-136` as the authority. **The sum guard is what makes that drift loud.**

### The re-mint — asked for, not assumed

⛔ **I stopped rather than proceeding, and both Tier-1 seats recorded that as correct.**
`1.0.0_SA_CTO~Z` 11559 directed a re-mint; `2.0.0_SA_COO~Z`'s AC2 ruling §5 said *"does NOT authorize a
second write, an overwrite"*. **"Latest + most-restrictive binds" does not resolve that** — CTO was
latest, COO was more restrictive — **and adjudicating between two Tier-1 seats is not a Tier-2 act.**
`1.0.0_SA_CTO~Z` then withdrew the write limb as exceeding their lane (11595); `2.0.0_SA_COO~Z`
authorized it as the seat that wrote §5 (11601, re-affirmed in 11609 because the withdrawal and the
authorization crossed in flight). **Cost: about ninety seconds.**

**AC2 RE-TAKEN on the corrected bytes:**

```
BUCKET/KEY    opal-data-cot / platinum/satellites/registry.json
SIZE          2196 bytes        LastModified  2026-08-28T01:38:46+00:00  (UTC, s3api)
ETag          c056874e69aa048a616f4e21100cf74a
VersionId     xLcuAW7VMbGyF.0kpt2LQ9Wb24WVnQaS          SSE AES256
LISTING       Contents = exactly 1; IsTruncated absent; NextContinuationToken ABSENT
VERSIONS      2 total, 0 delete markers -- 1 current (2196) + 1 noncurrent (2182, pre-fix)
              ^ the discriminating evidence that EXACTLY ONE overwrite occurred and no more
SERVED BYTES  2196 on disk == 2196 ContentLength; 9 of 9 books sum to 100.000;
              9 of 9 PASS the consumer's validateSatellite SUM check; 0 of 9 carry the defect
```

⚠ **A `VersionId` is a LEASE, not provenance** — this estate expires noncurrent at 14 days, so the
pre-fix bytes will vanish. **The durable evidence of the pre-fix state is this record**, not that
noncurrent version.

⚠ **AND FIXING THE UNITS DOES NOT MAKE THE ARTIFACT REACH THE PAGE.** `0.4.0_DE_ClientPlatform~Z`
measured (11539) that **no fetch path exists**: every `SATELLITE_REGISTRY` use is a DEFAULT PARAMETER
and `Positioning.tsx:225` calls `satellitesToPositioningShape(positioningData)` with one argument, so
the compile-time empty constant always wins. **That is a separate DE-lane wiring cell**, ruled separate
by `1.0.0_SA_CTO~Z`. Nothing renders from this key today, correct units or not.

## 11. THE STRIKE CLAUSE — RULED AND EXECUTED (was §7(a), carried unowned since the fabric kill)

`1.0.0_SA_CTO~Z` msg 11583 ruled it and assigned the edit to this lane (Rule 13), then msg 11588
recorded that 11583 **supersedes row 11 of that seat's own ruling record**, which had said STRIKE.
**11583 binds: do NOT delete the section.**

**EXECUTED — four edits to `satellites_registry.py`, keeping every measurement:**

1. **RETITLED** *"WHY THERE IS NO PREDICATE"* → *"NEITHER DATA PLANE ENCODES THE IS-A CRITERION"*,
   which is what the sweep actually establishes.
2. **The CONCLUSION superseded, the MEASUREMENT kept** — the 84-file / 121-child-node / 0-match sweep
   with its 18-of-18 positive control **stands and is still true**; what does not follow is *"therefore
   no predicate exists"*. Andrew's ~22:5xZ ruling is quoted verbatim in its place.
3. **The "THE PRICE" two-halves framing reframed** — it was premised on a hand-maintained list that
   cannot self-update. **The predicate DISSOLVES that hazard rather than mitigating it**; the oracle
   now earns its place as a fixture-comparison instrument, not as a watchdog for a manual list.
4. ⛔ **THE INVERTED LINE CORRECTED — the urgent one.** `:54-58` read *"As a MEMBERSHIP PREDICATE the
   canonical name form is wrong and Andrew ruled it so."* **Andrew has ruled the exact opposite.** A
   reader trusting that line would have built the inverse of what he asked for, **on his authority**.

⭐ **Why the narrow remedy beat the strike, in CTO's words and confirmed by what I found:** a blanket
strike *"would have removed [the inverted line] WITHOUT ANYONE NOTICING IT HAD BEEN WRONG."*

⚠ **A FIFTH INSTANCE FOUND AND DELIBERATELY NOT TOUCHED — out of this ruling's scope, and it has a
TEST.** The module's opening block still reads *"THIS IS A DECLARED SET, NOT A DERIVED PREDICATE …
nothing in this file may be read as evidence that they COULD be"*, with `REGISTRY_CLAIM = "held"`. That
carries the **same inversion**, but `tests/test_satellites.py:346-347` **asserts that exact string is
present in `__doc__`**, and `:338-339` assert `REGISTRY_CLAIM == "held"` / `!= "measured"`. **Changing
it is a TO-2 decision with a test to move, not a tidy-up** — surfaced to `1.0.0_SA_CTO~Z`, not acted on.

**TO-2's suite re-run after the edit: 29 passed.**

## 12. AC6 RE-MEASURED 02:4xZ — THE TRIGGER NOW EXISTS, AND §5's EVIDENCE IS SUPERSEDED

⛔ **§5 of this record carried a sentence that is now FALSE and I am correcting it rather than leaving
it standing:** *"THE TRIGGER HAS NOT REACHED DESIRED, let alone APPLIED or EXERCISED."* True at
~01:2xZ. **False now.**

`0.7.0_AE_CloudOps~S` applied `ETFS_SATELLITES.TO-6-AE` at 02:45:45Z. Re-censused, both planes:

```
PLANE 1  EventBridge Rules      139 total, NextToken ABSENT,  1 MATCHING
         cot-satellites-registry-producer-daily   State ENABLED   cron(0 7 * * ? *)
PLANE 2  EventBridge Scheduler   18 total, NextToken ABSENT,  0 matching
```

⭐ **THE RULE COUNT MOVED 138 -> 139 AND THE +1 IS EXACTLY THIS RULE.** That is what separates "a new
trigger appeared" from "my census drifted" — the delta is attributable, not merely consistent.

**AC6 IS STILL FAIL, AND THE REASON IS NOW A DIFFERENT ONE.** It has reached **APPLIED**; it has not
reached **EXERCISED**. The first fire is 07:00Z. The criterion's own text forecloses discharging on
less — *"an ad-hoc run is permitted for QA and is NEVER the acceptance"*, *"DESIRED != APPLIED !=
EXERCISED on every claim"* — and that fire discharges AC6 **for TO-6-AE**, not for this TO.

⚠ **The superseded measurement is KEPT, not overwritten.** The pre-apply zero (0 of 138 Rules, 0 of 18
Schedules, against a positive control of six live gold triggers) is what made this criterion's FAIL a
**measurement** rather than an assumption. Deleting it would retire the evidence and leave only the
verdict.

⭐ **AND THE GENERAL FORM, since this is the second time tonight one of my own recorded claims aged
under me** (the first was writing "LOCAL" as a push state before measuring it): **a criterion's status
can be stable while its REASON silently changes underneath.** AC6 read FAIL before and reads FAIL now,
so nothing in a status-only view would have flagged this — the verdict was never wrong, and the
sentence justifying it became wrong. **A status that survives is not evidence its basis did.**

### Related, and it is what made the re-measure worth running at all

The apply that moved AC6 is the same apply that carried the **regression vector** this seat found and
reported at 02:3xZ: TO-6-AE's package was pinned at `3f5f8bace5`, which **predates** the unit fix, so
the packaged producer emitted FRACTIONS. A 07:00Z fire on that package would have overwritten the
corrected artifact with the defect the consumer refuses **and greened AC6 over it**. `0.7.0_AE_CloudOps~S`
re-pinned and redeployed at 02:45:45Z, verifying on the **live** bytes:

```
DEPLOYED NOW     15763 B   SUMTGT=5  x100=1  GUARD=4  REFUSE=1   pin e8151e7385
DEPLOYED BEFORE  13182 B   SUMTGT=0  x100=0  GUARD=0  REFUSE=0   pin 3f5f8bace5
```

⭐ **Their verification is a rung above the one this seat supplied:** I exercised the 4-token predicate
against **git blobs**; they ran it against the **live `lambda get-function` package**, each carrying its
own in-zip BUILD_MANIFEST pin. Source-plane vs deployed-plane, and the deployed plane is the one the
claim is about.

## 13. ⛔ THE REGISTRY KEEPS NINE AND THE PAGE SHOWS EIGHT — BY SOVEREIGN RULING, NOT BY DEFECT

**ANDREW-DIRECT 2026-08-28 ~04:2xZ, VERBATIM** (relayed by `1.0.0_SA_CTO~Z`, msg 12703):

> *"one coment, i dont think we have to display visually satellite 98, even if we track it otherwise,
> the premise is that its the same characteristics as 90, so no need to show two, just a frontend
> change only, that would solve the issue with the width and no need for arrows"*

⛔ **THIS IS A RENDER-LAYER FILTER AND NOTHING IN THIS LANE CHANGES.** Recorded here because this file
is where AC5's **"9 of 65 derived"** lives, and a future reader who sees **nine in the registry and
eight on the page** has every reason to read that gap as a defect. **It is not one.**

```
THE REGISTRY   platinum/satellites/registry.json   NINE books, incl. Opal Satellite 98   <- UNCHANGED
THE PRODUCER   build_satellites_registry.py        keeps deriving 98 from the predicate   <- UNCHANGED
THE PAGE       Positioning, satellites mode        shows EIGHT                            <- the change
```

⛔ **DO NOT CLOSE THIS GAP BY DROPPING 98 FROM `SATELLITE_MEMBERS`, THE REGISTRY, OR THE PRODUCER.**
That would destroy tracked data to solve a display choice, and it would silently change what the
derived predicate admits — contradicting Andrew's own ~22:5xZ membership ruling (*"Does it say 'Opal
Satellite' in the name? Add it and track henceforth"*). **He is explicit that we still track it:**
*"even if we track it otherwise."*

⭐ **AND THE MEASUREMENT IN §7/§2 OF THIS RECORD IS WHAT MAKES THE FILTER CORRECT RATHER THAN A DATA
BUG.** 90 and 98 were measured at the bronze plane as **distinct `model_id`s, distinct S3 objects,
distinct sha256, distinct `accountCount` (0 vs 11), each detail's own `hierarchy.name` matching its own
satellite** — and **genuinely identical children** (both 100% `Opal Long-Term Aggressive`). So the two
columns really do carry identical numbers, the registry is faithfully reproducing the source, and the
right remedy is a **display** decision rather than a correction. Andrew reached the same conclusion
independently from the rendered page, confirming it column-by-column (Cost 35.71, Beta 0.96, Duration
1.81, Yield 1.99, # of ETFs 16, 8.1/91.9 allocation).

⚠ **`1.0.0_SA_CTO~Z` filed the identical observation at ~01:5xZ with a WRONG supporting premise (a
broken duration ladder, from reading `ULT` as Ultra-Short) and retracted that premise when this seat
falsified it.** **The observation itself was right.** Recorded because *a right observation with a
wrong rationale is still a right observation* — and the retraction of the rationale must not be read
as retracting the finding.
