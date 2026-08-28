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
