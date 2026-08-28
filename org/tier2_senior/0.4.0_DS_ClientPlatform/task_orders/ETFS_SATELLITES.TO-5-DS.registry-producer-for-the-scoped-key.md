<task_order>
<id>ETFS_SATELLITES.TO-5-DS.registry-producer-for-the-scoped-key</id>
<title>BUILD THE PRODUCER that writes platinum/satellites/registry.json — the carrier, contract and predicate are all SETTLED; only the writer is missing</title>
<project>ETFS_SATELLITES</project>
<directive>ETFS</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~L</issued_to>
<issued_at>2026-08-28T00:0xZ</issued_at>
<status>closed -- 5 of 6 criteria PASS as filed; `T5DS-AC6` is RELOCATED, and it is neither waived nor
withheld. **NO SEAT IS NEEDED ON THIS TO.** Disposed 2026-08-28 ~03:5xZ by `2.0.0_SA_COO~Z` (issuer).

⛔ **THE LEAD WORD IS `closed` AND NOT `complete`, DELIBERATELY.** The filed proof instance carries
`T5DS-AC6 = FAIL`, so `complete` would assert a six-of-six discharge nobody performed. `closed` says
the TO is disposed and carries its exclusion on its face.

**AC1-AC5: PASS** in `0.4.0_DS_ClientPlatform~L/deliverables/ETFS_SATELLITES.TO-5-DS_PROOF_OF_SPEC.json`.
⚠ **NOT YET CERTIFIED — `3.0.0_SA_CVO~Z` holds that**, and this disposition does not presume it. A
certification must read **"5 of 6, one criterion RELOCATED by cited TO"**, never a bare 5/6.

⛔⛔ **CORRECTED 2026-08-28 ~04:5xZ by `2.0.0_SA_COO~Z` (issuer), on `3.0.0_SA_CVO~Z`'s certification
finding (12804). THE SENTENCE BELOW SAID `T5DS-AC6` "LIVES IN" `TO-6-AE`. IT DOES NOT.**

>> **THE REMEDY WENT OUT OF LANE TO `TO-6-AE` (Rule 13: PROD triggers are DT/AE). THE CRITERION DID
   NOT. `AC6` IS STILL `AC6` ON THIS TO, DISCHARGED *HERE* BY AN EVENT -- NOT MET ELSEWHERE.**
⛔ **Why it matters and is not wording:** a certification reading *"relocated"* **sends a reader to
another TO for a criterion that lives on this one.** ⭐ **A forward pointer that resolves to the WRONG
PLACE is worse than none** -- this office built the four-part pointer to make it resolvable and pointed
it one TO too far.
**THE CORRECT READING: 5 PASS + 1 NOT-YET-EXERCISED. NOT COMPLETE, AND CORRECTLY LEFT OPEN.**
**ONLY THE ~07:00Z FIRE DISCHARGES `AC6` -- not the apply, not the census, and not a change of enum
value.** The ~07:00Z fire is the same EVENT that discharges `T6AE-AC3`; one event, two criteria, each
on its own TO.

⚠ **KNOWN CONDITION, NOT CHASED TONIGHT (the lane is gone):** the filed instance carries `AC6` as
**`FAIL`**, and `3.0.0_SA_CVO~Z` measured that **the schema already carries the right value** --
`UNCOMPUTABLE-BY-CONSTRUCTION`, whose own definition is *"rides a NAMED later run"*, and the row's
`status_reason` already says exactly that. ⛔ **`FAIL` means EVALUATED AND FALSE; nothing failed -- the
fire has not happened.** **A consumer filters on the ENUM**, so a reader scanning statuses sees `FAIL`
on a TO whose work is complete and correct. **This is a MIS-STATED VALUE, not mis-stated evidence** --
correcting it changes no measurement, and it is NOT a schema edit (the value already exists).

⭐ **AND THE ROW IS OTHERWISE THE BEST-EVIDENCED ONE OF THE NIGHT** (`3.0.0_SA_CVO~Z`'s words): both
EventBridge planes censused with denominators printed, the 138->139 delta used as CORROBORATION that
the +1 IS the satellites rule rather than census drift, and DESIRED/APPLIED/EXERCISED held apart.

**ORIGINAL SENTENCE, PRESERVED:** ⭐ ~~`T5DS-AC6` LIVES IN `ETFS_SATELLITES.TO-6-AE`~~, and that is a CARRIER, not a waiver.** Rule 13 puts
PROD triggers in the AE/DT lane, so a DS lane structurally could not discharge it; `~L` MEASURED the
absence in both scheduler planes (0 of 138 Rules, 0 of 18 Schedules, positive control) and filed **FAIL
rather than waiving it** — which is why the gap was findable at all. **Verified at this seat, not taken
from a face:** the schedule is applied @`3f5f8bace5` and `TO-6-AE` AC1/AC2/AC4/AC5 are CERTIFIED by
`3.0.0_SA_CVO~Z` @`324330f5f2` (both shas read with `git log`; a bogus sha fails as the negative control).

⛔ **DISTINCT FROM `ETFS_INGEST.TO-7` AC3, AND THE TWO MUST NOT BE BLURRED.** That one is
**TERMINAL-WITHHELD** — it will never be met, by ruling. **This one WILL be met**, on `TO-6-AE`'s
`AC3`, when the schedule fires on its own trigger at ~07:00Z. **A relocated criterion has an owner and
a clock; a withheld one has neither.**

**FORWARD POINTER, ALL FOUR PARTS** (`3.0.0_SA_CVO~Z` 12566: without all four, *"5 of 6, one
relocated" is exactly as opaque as a bare 5/6* — a reader learns a criterion moved and cannot
follow it):
```
  destination criterion   T6AE-AC3
  its TO                  ETFS_SATELLITES.TO-6-AE
  its OWNER               0.7.0_AE_CloudOps~S
  its CLOCK               ~07:00Z, cron(0 7 * * ? *) UTC, cot-satellites-registry-producer-daily
```
⛔ **AND THE FAILURE BRANCH, WHICH THIS DISPOSITION DID NOT TRACK WHEN FIRST WRITTEN:** if that
fire **fails or does not occur**, `T5DS-AC6` is unmet and this TO is already closed. **The
back-pointer is recorded on `TO-6-AE` itself** — its `AC3` evidence names `T5DS-AC6`, and a FAIL or
non-fire is reported to `3.0.0_SA_CVO~Z` explicitly. ⚠ **`3.0.0_SA_CVO~Z` will NOT certify the
relocation as discharged until `T6AE-AC3` is MEASURED — a relocated criterion is met by the FIRE,
not by the relocation.**</status>

<decomp_ref>
workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md — stage-3 decomp for
ETFS_SATELLITES. **Cells this TO discharges: SAT-a-4, SAT-b-2, SAT-b-3, SAT-b-4.**

⚠ **`SAT-a-4` IS ALREADY DISCHARGED AS A DECISION AND IS CITED HERE AS A CONSTRAINT, NOT A QUESTION.**
It read *"DELIVERY FORM IS AN OPEN CUT AND IS MINE TO MAKE: served block vs portal-fetched vs
build-time constant."* **Both cuts have been made:** this office eliminated **build-time constant** at
`2026-08-27T182114Z` (msg 9539, quoted verbatim in `satelliteSet.ts`'s header — *"measures the wrong
clock WHILE STILL RETURNING FRESH"*), and **Andrew ~22:1xZ chose the scoped API path**, which is
portal-fetched from a served key.
</decomp_ref>

<the_write_shape_is_YOURS_TO_WRITE>
⛔⛔ **FIFTH AMENDMENT — THIS SECTION PREVIOUSLY TOLD YOU TO CALL `payload()`. THAT WAS FALSE, AND IT
WAS MY ERROR RATHER THAN A SUPERSESSION.** I wrote *"two shapes, two ends of one contract"* over a
relationship I never measured. `3.0.0_SA_CVO~Z` retracted their own build input before you reached
it; **you** measured the structural reason; `1.0.0_SA_CTO~Z` confirmed all three rows.

**THE SETTLED READING — TWO ARTIFACTS, NEVER ONE SHAPE DISPUTED:**
```
REGISTRY  platinum/satellites/registry.json   { books: SatelliteBook[], as_of }   <- YOURS
WEIGHTS   satellites_weights.payload()        TO-1's artifact; "WRITES nothing.
                                              This module DERIVES; it does not publish."  <- NOT YOURS
```
**Why a rename could never have bridged them — your measurement, and it is the load-bearing one:**
`payload().satellites` is a **LIST OF NAME STRINGS** (`resolve_set()`, `satellites_weights.py:200`,
surfaced `:331`); `SatelliteBook` requires **OBJECTS with a nested `constituents` array**
(`satelliteSet.ts:66-70`). `payload()` does carry constituent detail, but **FLAT in `rows`** — one row
per constituent. ⭐ **So a key-name change produces strings where the ratified contract requires
objects. The vocabulary argument was mine and it was the weaker one; the structural argument is
yours and it settles it.**

⭐ **THE REGISTRY PAYLOAD BUILDER DOES NOT EXIST — IT IS YOURS TO WRITE.** Corroborated at this seat
by a DIFFERENT instrument than CVO's (they read the weights docstring; I searched the registry module
for a write shape): `satellites_registry.py` resolves — 17408 B, the positive control — and defines
**no** payload/block function.

⭐⭐ **WHAT TRANSFERS IS THE DESIGN, NOT THE DICT.** `1.0.0_SA_CTO~Z` named this the sharpest row, and
it is what keeps the build ladder's *"the estate already has it"* from collapsing into *"copy the
shape"*:
```
CALL IT, artifact-agnostic   assert_no_baked_verdict(block)  refuses {state, is_fresh, stale, ...}
CALL IT, do not reimplement  vintage(as_of, now)             the trading-day frontier
COPY THE SHAPE OF            read(block, now)                verdict COMPUTED at read, never baked
```
**That read-time split IS this office's `SAT-a-4` ruling. Your artifact inherits the RULING; it does
not inherit the DICT.**

⛔ **BINDING — `1.0.0_SA_CTO~Z` amend6 plus one clause. THE EMPTY IS THE CASE THAT BREAKS:**
```
{ books: [], as_of: <the partition date the producer RAN> }   NON-NULL ALWAYS, INCLUDING WHEN EMPTY
read({as_of: "2026-08-27", rows: []}) -> OK       read({as_of: null, rows: []}) -> RAISES ValueError
                                                  read({rows: []})              -> RAISES KeyError
```
⚠ **DO NOT LIFT `{books: [], as_of: null}`.** It sits in `0.7.0_AE_CloudOps~Y`'s **removed** code and
is quoted in their proof-of-spec record, and it was correct for a **different case**: *no artifact
exists at all*, where stamping a time would manufacture a freshness signal for data never published.
**Yours is PUBLISHED-EMPTY — a pull HAPPENED and found nothing. Zero members is a measurement WITH a
date, not the absence of one.** That is Andrew's R4 (publish the empty, never delete the key) meeting
`T5DS-AC3`, and ⛔ **the natural shape to reach for is the one that raises.**
</the_write_shape_is_YOURS_TO_WRITE>
<the_code_form_RULED>
⛔ **`SatelliteBook.code` = THE CANONICAL NAME, VERBATIM** — e.g. `"Opal Satellite 50"`.
**`1.0.0_SA_CTO~Z`'s ruling**, raised by you and correctly not invented at the executor.
`displayName` is free to differ and is unconstrained by this.
```
1 PROVABLE NON-COLLISION  MODEL_BOOKS UST/ST/INT/LT/ULT + ETF DIVZ/IDVZ/PFDE/PFOE. A 3-5 char
                          mnemonic CANNOT equal an anchored 3-token form. Positive control passing.
2 IT IS ALREADY THE KEY   MEMBER_NAMES is a frozenset of exactly these and the predicate matches on
                          this field. Any other choice mints a SECOND identity space plus a mapping.
3 NO NEW TABLE            build ladder rung 1/2 -- a code convention is code nobody has to write.
```
⭐ **THE NAMED COLLISION HAZARD IS STRUCTURALLY UNREACHABLE, not merely avoided** (`3.0.0_SA_CVO~Z`):
`bookSet.ts:167` warns of *"the day a satellite code collides with a model-notes key"*, but
`hasModelKeyNotes` has ONE call site — `PositioningSummary.tsx:1240`, guarded by
`HEADER_TRIGGER[bookMode] === 'model-notes' && …`, and `HEADER_TRIGGER.satellites = 'none'`
(`bookSet.ts:171-175`). **The `&&` short-circuits, so a satellite code never reaches it at all —
regardless of what the code is.**

⚠ **AND THE ONE ARTIFACT THAT COULD HAVE CONTRADICTED THE RULING, MEASURED AT THIS SEAT AND CLEARED —
recorded so you do not hit it as a false blocker.** A `SAT-` census over the portal returns **3 hits,
all in one file**, `portal/scripts/satellites-mode-axis-exercise.mjs` (`:205` `SAT_KEYS`, `:249`,
`:250`), where a satellite code appears as the mnemonic **`SAT-15`** — the opposite form to the one
ruled:
```
after.satelliteSet.satelliteDisplayName('SAT-15', [
  { code: 'SAT-15', displayName: 'Opal Satellite 15', constituents: [] },
]) === 'Opal Satellite 15'
```
>> ⭐ **IT SUPPLIES BOTH SIDES — the code AND the registry it resolves against — so it asserts the
   RESOLUTION MECHANISM, not a code FORM. It passes identically with `code: "Opal Satellite 50"` and
   places NO constraint on the producer.** `SAT_KEYS` is fixture data, not a declared convention. <<
⛔ **A seat who greps `SAT-15` and stops at the literal concludes the consumer expects short codes and
that this ruling breaks a committed exercise. That reading is FALSE, and the discriminator is that
the fixture is SELF-SUPPLYING — a test that defines both sides of a lookup cannot constrain an
external producer.**
</the_code_form_RULED>

<what_is_and_is_not_missing>
⛔ **READ THIS BEFORE SCOPING ANYTHING. FOUR FRAMINGS WERE WRONG TONIGHT AND THIS IS THE FIFTH,
MEASURED.**
```
NOT MISSING  the membership PREDICATE      satellites_registry.py:213 carries ^Opal Satellite <N>$
NOT MISSING  the CARRIER                   the scoped path, BUILT by 0.7.0_AE_CloudOps~Y in
                                           POSN_TENANCY.TO-4-AE (apply HELD on this artifact)
NOT MISSING  the CONTRACT                  SatelliteBook, and satelliteAdapter.ts:100 +
                                           satelliteSet.ts:106/:112/:173 already accept an
                                           INJECTED registry -- the seam exists, the empty
                                           constant is only the DEFAULT
MISSING      a PRODUCER that WRITES platinum/satellites/registry.json
```
⛔ **`satellites_registry.py` IS NOT THAT PRODUCER AND MUST NOT BE MADE INTO ONE.** Measured by
`3.0.0_SA_CVO~Z`: its whole public API is `canonical_roster_names`, `drift_report`,
`SatelliteRegistryDrift`, `assert_no_drift`; `drift_report` returns a **symmetric difference** and its
own docstring says ***"this oracle never decides."*** **It is a CONFORMANCE CHECKER by design.**
⚠ Corroborated by AST: **it imports nothing capable of I/O** — no `boto3`, `json`, `os`, `open`.
⭐ **Use it. Do not convert it.** It is the right instrument for `AC4`.
</what_is_and_is_not_missing>

<acceptance_criteria>

| id | criterion | cell_refs | status |
|---|---|---|---|
| `T5DS-AC1` | **A producer exists that WRITES the artifact** — new code, DS-lane. ⛔⛔ **AMENDED — THE INSTRUMENT I MANDATED COULD NOT ESTABLISH WHAT THIS CRITERION CLAIMS, AND BOTH HALVES WERE FOUND BY OTHERS.** **(a) `0.4.0_DS_ClientPlatform~L`, by EXERCISING it:** I named `cottonwood_aua.py` a POSITIVE control for producer-ness and **it never writes** — `boto3` client `:106`, `get_object` `:118`/`:147`, `main()` `:217` derives and **PRINTS**; no `put_object`, no upload, no file write. **Had it PASSED, my instrument would have been saying YES to a non-writer.** **(b) `1.0.0_SA_CTO~Z`, on the instrument itself:** ⛔ **`boto3` COVERS READS — an import proves a file can TALK to S3, never that it WRITES.** So the `write-capable imports` column **cannot discriminate a reader from a writer**, and this criterion must not rest on it. ⭐ **THE DISCRIMINATOR IS AN ACTUAL WRITE CALL** (`put_object` / `upload_*` / a file write), present in the AST — `__main__` / `def main` remain necessary-not-sufficient shape checks. **CORRECTED CONTROL SET:** **POSITIVE** `build_dim_model_portfolio.py`, `build_dim_taxsma_report.py` — 2 of 2 PASS; **NEGATIVE** `satellites_registry.py` (by design — no write-capable imports at all) **and `cottonwood_aua.py` (BY DISCOVERY)** — 2 of 2 REFUSE; **SUBJECT** `build_satellites_registry.py`. ⭐⭐ **`cottonwood_aua.py` IS THE STRONGER NEGATIVE AND THAT IS WHY IT IS KEPT: it wears every producer signal — `boto3`, `main()`, the guard — and refuses on the HARD one, where `satellites_registry.py` refuses on the easy one.** A control set whose negatives all fail on the easy signal never tests the discriminator. | `SAT-a-4` | |
| `T5DS-AC2` | **The artifact EXISTS at the key `POSN_TENANCY.TO-4-AE` serves** — bucket, key, byte size, `LastModified` (UTC, `s3api`) recorded. ⛔ **COMPLETE listing: `NextToken` shown ABSENT or paginated to exhaustion. `--max-items`/`head` are BANNED** — a lexicographic head is not a population and that instrument killed a real hazard on this estate today. | `SAT-a-4` | |
| `T5DS-AC3` | ⛔ **PUBLISH THE EMPTY, NEVER DELETE THE KEY.** Andrew ~22:5xZ R4: *"if an Opal Satellite disappears from daily pulls, now it is no longer tracked"* — **zero members is a STEADY STATE, not day one.** A firm with zero members gets a **published artifact with an empty member set**, never a missing key. ⛔⛔ **CORRECTED 00:0xZ — THE SENTENCE I FIRST WROTE HERE WAS A STALE FACT ABOUT ANOTHER LANE'S CODE, AND ITS CORRECTION MAKES THIS CRITERION LOAD-BEARING RATHER THAN BELT-AND-BRACES.** <br>~~`0.7.0_AE_CloudOps~Y`'s synthesis fires only on 403/404, so a published-empty passes through untouched.~~ **THE SYNTHESIS NO LONGER EXISTS.** They **REMOVED** it `@24a8435642` (23 insertions / 62 deletions) because it failed `1.0.0_SA_CTO~Z`'s AC3 arm 3: **it converted BOTH 403 AND 404 into `200 {books: []}`, and on this family an ABSENT artifact and a FORBIDDEN read are THE SAME STATUS by design — so it reported a REFUSAL as "this firm has no satellites."** `3.0.0_SA_CVO~Z` verified the removal at source (403 branch gone = 0, synthesised status gone = 0, **firm-isolation guard SURVIVES = 3, positive control**). <br>>> ⛔ **CONSEQUENCE FOR THIS PRODUCER, AND IT IS THE WHOLE POINT: THE SERVING LAYER NO LONGER COVERS FOR A DELETING PRODUCER.** <br>`BEFORE` a producer that DELETED on empty was silently papered over — the edge manufactured a friendly `200 {books: []}`. <br>`AFTER` **a missing key stays a 403, indistinguishable from a refusal, all the way to the consumer.** << <br>⭐ **So "PUBLISH THE EMPTY, NEVER DELETE THE KEY" is not a nicety here — it is the ONLY thing standing between a zero-member firm and a screen that reads as "you are not allowed to see this."** | `SAT-b-2` | |
| `T5DS-AC4` | ⛔⛔ **AMENDED 00:0xZ — MY ORIGINAL WORDING WAS ONE WORD TOO BROAD AND SHIPPED THE ANCHORS UNTESTED. THE PREDICATE HAS THREE LIMBS AND THE CORPUS EXERCISES ONE.** Measured per-limb on the 65-row roster by `1.0.0_SA_CTO~Z`: <br>`drop the token Opal` → `/satellite/i` → **+18 extra admits — EXERCISED** (this is where `Core \| Satellite 98` lives) · `drop leading ^` → **+0 — UNEXERCISED** · `drop trailing $` → **+0 — UNEXERCISED**. <br>>> ⛔ **A PREDICATE WITH THE `$` DELETED SCORES 9/9 AND WOULD HAVE PASSED THIS CRITERION AS I FIRST WROTE IT.** << <br>**SO BOTH ARE REQUIRED, AND THE INSTRUCTION SPLITS BY LIMB:** <br>**(a) `Opal` TOKEN — EXERCISE ON THE REAL PAIR, DO NOT BUILD A FIXTURE.** `SAT-b-4`: `Core \| Satellite 98` (9 accounts) beside `Opal Satellite 98` (11). **A pass built against a hand-made row here tests the fixture, not the predicate.** <br>**(b) LEADING `^` AND TRAILING `$` — CONSTRUCT FIXTURES, because the corpus has NO natural mutant for either.** Each anchor deleted must produce a MEASURABLE extra admit against a row built for it; **an anchor with no failing input is an untested anchor.** <br>⚠ **Use `drift_report`/`assert_no_drift` as the oracle — that is what they are for.** ⭐ **AND THE PROVENANCE OF THIS AMENDMENT IS THE POINT: I over-corrected `3.0.0_SA_CVO~Z`'s "the corpus is vacuous" into "it is not," when the measured truth is PARTIALLY VACUOUS — 1 limb of 3.** | `SAT-b-4` | |
| `T5DS-AC5` | **Blends are EXCLUDED as ALLOCATORS, not as name-misses** — `SAT-b-2`, Andrew ~16:1xZ: *"Some SMA that has a blend of a Satellite and Opal Model is not a Satellite, they merely are allocating to a Satellite."* ⛔ **The criterion is IS-A vs HOLDS-A and it DOES NOT DRIFT.** Expected: **9 of 65**, the five named blends and the whole `Core \| Satellite *` family excluded. ⚠ **`Opal Ultra Short Term` is EXCLUDED** (`SAT-b-3`, Andrew ~16:1xZ) — **it is on the roster as a MODEL, and roster membership is not satellite membership.** | `SAT-b-2` `SAT-b-3` | |
| `T5DS-AC6` | **The trigger is a SCHEDULE.** ⛔ **Success-of-upstream as the only trigger is a defect**, and **an ad-hoc run is permitted for QA and is NEVER the acceptance** — *"ad-hoc artifacts are never production evidence."* **`DESIRED ≠ APPLIED ≠ EXERCISED` on every claim; no criterion discharged by "the commit gate passed."** | `SAT-a-4` | |

</acceptance_criteria>

<reporting>
Deliverable + proof instance in this lane's own `deliverables/`, via
`.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~L <0.4.0_DS_ClientPlatform~L@opal.agent>" -F <msgfile>`,
message file written by a **non-shell writer**, never a heredoc.
⚠ **PUSH STATE MEASURED with a control, or the words "push state UNMEASURED."** ⛔ **An UNDER-stated
push state caused a five-hour phantom blockage on this exact project tonight** — a seat reported
"LOCAL" when both remotes contained the work, and nobody challenges a claim of *less* than achieved.
⛔ **`cell_status` per cell from OBSERVED states only, in the `.md` MEASUREMENT RECORD — NOT the proof
instance** (`PROOF_OF_SPEC.schema.json` is `additionalProperties:false`).
</reporting>

<standing>
· **Surprise channel:** anything odd that is not this task -> one line to `3.0.0_SA_CVO`, cc the
  issuer (`2.0.0_SA_COO~Z`), **and KEEP WORKING.**
· ⛔ **No new alert/alarm/monitor** — standing moratorium. **No shadow pipeline, no duplicate output
  path** — Andrew complete veto.
· ⚠ **`POSN_TENANCY.TO-4-AE` IS BUILT AND ITS APPLY IS HELD ON THIS ARTIFACT.**
· ⛔⛔ **CORRECTED 00:0xZ — THIRD STALENESS, AND THIS ONE WOULD HAVE SENT YOU TO THE WRONG FILE.**
  ~~Do NOT design the served shape — it is `TO-4-AE`'s and it is already built.~~
  **FALSE. `0.7.0_AE_CloudOps~Y`'s path DEFINES NO SUCCESS-PAYLOAD SHAPE.** Read at source: the only
  object their handler constructs is the pre-existing **error envelope**
  (`{error, uri, firmId, status, request_id}`). **Since `@24a8435642` a successful registry read
  PASSES THROUGH UNTOUCHED** — a side effect of the arm-3 fix, which they reported as one:
  ***"my path now takes no position on the shape."***
  >> ⛔ **HAD YOU FOLLOWED MY CLAUSE YOU WOULD HAVE GONE LOOKING IN `TO-4-AE` FOR A CONTRACT THAT IS
     NOT THERE, AND THE SHAPE WOULD HAVE BEEN DEFINED BY NOBODY.** <<
  ⭐ **THE SHAPE IS `SatelliteBook` IN `portal/src/pages/Positioning/shared/satelliteSet.ts`** — the
  CONSUMER's declared type. This office's own `SAT-a-4` ruling says it verbatim: ***"The shape above
  IS the contract that read must satisfy."*** **Write to THAT type.**
· ⛔ **STRUCTURAL NOTE FOR THIS TO AND THE NEXT ONE — THREE STALENESSES IN TEN MINUTES, ONE
  MECHANISM:** I cited **other lanes' live implementations** as facts inside criteria, and each aged
  the moment they committed. ⭐ **A criterion that quotes another lane's current code INHERITS THAT
  LANE'S VELOCITY.** **Cite the REQUIREMENT and its DURABLE CARRIER — a declared type, a ruled
  invariant, a sovereign word — never a sentence about what someone's handler does today.**
  ⚠ **`0.7.0_AE_CloudOps~Y` swept every remaining clause about their work and verified the rest
  (`:28-29`, `AC2`, `AC3` as amended) ACCURATE — so this sweep is bounded, not open.**
· **No gate gets loosened, waived or expected-green'd.** A criterion that fires is right.
</standing>

<proof_of_spec>
  <criterion id="T5DS-AC1" cell_refs="SAT-a-4"/>
  <criterion id="T5DS-AC2" cell_refs="SAT-a-4"/>
  <criterion id="T5DS-AC3" cell_refs="SAT-b-2"/>
  <criterion id="T5DS-AC4" cell_refs="SAT-b-4"/>
  <criterion id="T5DS-AC5" cell_refs="SAT-b-2,SAT-b-3"/>
  <criterion id="T5DS-AC6" cell_refs="SAT-a-4"/>
  <expected_criteria>T5DS-AC1,T5DS-AC2,T5DS-AC3,T5DS-AC4,T5DS-AC5,T5DS-AC6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~L/deliverables/ETFS_SATELLITES.TO-5-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 4 (SAT-a-4, SAT-b-2, SAT-b-3, SAT-b-4); criteria: 6. FORWARD — 6 of 6 criteria carry >=1 cell_ref. BACKWARD — 4 of 4 declared cells reachable (SAT-a-4 from AC1/AC2/AC6, SAT-b-2 from AC3/AC5, SAT-b-3 from AC5, SAT-b-4 from AC4). Unmapped 0; untraceable 0. *(The decomp's other 21 cells are NOT this TO's: the (c)/(d)/(e)/(f) families are render/mode/gate surfaces carried by ETFS_SATELLITES TO-1..TO-4, and SAT-inv-1..4 bind as standing clauses. SAT-a-4 is cited as a DISCHARGED DECISION constraining this build, not as an open cut.)*</alignment_denominators>
  <criterion_status_note>⛔ AC4 is the one that can be falsely passed, and it nearly was at the spec level: an earlier draft of this TO told the executor to CONSTRUCT a negative fixture because the corpus was believed vacuous. It is not — `Core | Satellite 98` vs `Opal Satellite 98` is a live pair in the roster and the predicate must separate them. A pass produced against a hand-built fixture instead of that pair tests the fixture, not the predicate.</criterion_status_note>
</proof_of_spec>
</task_order>
