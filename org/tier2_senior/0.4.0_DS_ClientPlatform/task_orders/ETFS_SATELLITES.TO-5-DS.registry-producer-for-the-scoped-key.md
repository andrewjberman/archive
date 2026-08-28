<task_order>
<id>ETFS_SATELLITES.TO-5-DS.registry-producer-for-the-scoped-key</id>
<title>BUILD THE PRODUCER that writes platinum/satellites/registry.json — the carrier, contract and predicate are all SETTLED; only the writer is missing</title>
<project>ETFS_SATELLITES</project>
<directive>ETFS</directive>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.4.0_DS_ClientPlatform~L</issued_to>
<issued_at>2026-08-28T00:0xZ</issued_at>
<status>ACTIVE</status>

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
| `T5DS-AC1` | **A producer exists that WRITES the artifact** — new code, DS-lane, I/O-capable. ⛔ **Demonstrate with the SAME AST instrument that settled the scope** (`__main__` / `def main` / write-capable imports), **with `build_dim_model_portfolio.py`, `build_dim_taxsma_report.py`, `cottonwood_aua.py` as positive controls** and `satellites_registry.py` as the negative one. | `SAT-a-4` | |
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
