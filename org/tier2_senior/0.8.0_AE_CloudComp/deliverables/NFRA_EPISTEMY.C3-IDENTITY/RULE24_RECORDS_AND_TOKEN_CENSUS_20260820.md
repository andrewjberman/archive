# NFRA_EPISTEMY.C3-IDENTITY -- Rule-24 records (reach, standing, hop evidence class) + pinned-surface token census

**Author:** 0.8.0_AE_CloudComp, 2026-08-20 · **Object cert:** 4.0.0_SA_CRO base 63859 CERTIFIED-WITH-AMENDMENTS (A1 absorbed), confirmed 63890 · **Arch gate:** 1.0.0_SA_CTO 63865 CLEARS on the amended shape, CONFIRMED 63887 · **GO:** 2.0.0_SA_COO 63813; TO amended to the certified shape 63871.
**Sources of record (cited, never copied):** `docs/architecture/PRD_EPISTEMIC_MECHANIZATION_20260820.md` sec.2.1 (Observation_Record -- consumed via the C1 envelope's `build_record`) + sec.2.5 (Eligibility_Evaluation consumes the closure); `org/tier1_exec/4.0.0_SA_CRO/deliverables/RESPONSE_II_MUTATION_BUNDLE_AND_ADOPTIONS_20260820.md:147-156`; CLAUDE.md Rule 22a (build-input resolution; staged = DESIRED, executing = APPLIED).
**Status of the objects:** PROPOSED shape. Registry landing of `Support_Closure` / `Identity_Bundle` is base's act (CITE-NOT-COPY rider); the compiler (`org/modules/graph/comp_closure.py`, `.tools/comp-closure`) emits INSTANCES carrying `object_status` naming the cert + gate.

## 0. The diagnostic this record applied (CTO 63865, candidate Rule-24(iii) test)

> If an enum needs a PRECEDENCE RULE to resolve cases where more than one value applies, suspect two axes fused. A single-intent MECE axis never needs precedence -- its values are disjoint by construction. A precedence clause is a repair for a MECE failure the author decided to live with.

The first proposal packed REACH and STANDING onto one terminal enum and carried a precedence rule (`UNKNOWN > UNMEASURED > BEHAVIOR > PRESENCE_ONLY`); base's A1 named the tell; CTO's multi-member finding (one member's executing read licensing BEHAVIOR over unexecuted members = a MAX over a set presented as a property of the set) was the same defect from the aggregation side. Split, no ordering language survives on the object (self-test 11 asserts its absence on every compile).

## 1. Record R24-C3-001 -- `reach`

| field | value |
|---|---|
| surface | `Support_Closure.reach.per_member[<member>]` (+ derived `Support_Closure.reach.value`) |
| act | AUTHORED_AXIS |
| declared_layer | the evidence reach of ONE MEMBER of one compiled closure (**member grain**) |
| aggregation layer (DECLARED) | `reach.value` = **MIN over members** (weakest link); no members -> `NONE`. MIN is the aggregate of ONE member-grain value, not an ordering between intents; the grain string on the field says so (`"closure (MIN over members -- the declared aggregation layer)"`). |
| axis_intent | how far the evidence chain got for the member -- NOT whether it stands (standing), NOT whether copies agree (bundle) |
| members | `NONE` (never resolved/compared through the build input) · `PRESENCE_ONLY` (bytes read from the DEPLOYED digest and stopped) · `BEHAVIOR` (an EXECUTING read covered the member) |
| (i) MECE | disjoint by what the last KNOWN hop's evidence class is for the member (none / DIGEST-or-BYTES / EXECUTION). **BEHAVIOR is unreachable by labelling:** the constructor REFUSES it without a KNOWN `EXECUTION` hop (m4). |
| (ii) same grain | one member, always; the closure value is a separate derived field with its own grain string |
| (iii) intent coherence | one intent; no precedence clause exists or is needed |
| (iv) stability frame | a NEW INSTRUMENT moves reach (an executing read added -> BEHAVIOR for the members it covers; the aggregate moves with its weakest member). One remedy per value. |
| Lambda tonight | every Lambda closure is `PRESENCE_ONLY` BY CONSTRUCTION (no invokes under the read-only bound) and every instance SAYS so (`notes[0]`, `last_hop_honesty`) |

## 2. Record R24-C3-002 -- `standing`

| field | value |
|---|---|
| surface | `Support_Closure.standing.value` |
| act | AUTHORED_AXIS |
| declared_layer | whether ONE compiled closure still stands (**closure grain**) |
| axis_intent | does the compiled chain stand -- NOT how far it got, NOT the equivalence verdict |
| members | `BROKEN` (a required LIVE acquisition failed and the chain STOPPED there -- no later hop is taken) · `AMBIGUOUS` (chain completed; a member has a second plausible repo home) · `CURRENT` (chain completed, single home, no side moved) · `INVALIDATED` (a side moved since compile -- `verify`'s re-read verdict) |
| (i) MECE | by construction: BROKEN stops the chain (nothing later exists to be ambiguous about); AMBIGUOUS vs CURRENT differ on the home census of a COMPLETED chain; INVALIDATED is only ever produced by a re-read of an already-compiled closure, so compile-time and re-read-time values cannot collide. No ordering language anywhere. |
| (ii) same grain | one closure |
| (iii) intent coherence | one intent |
| (iv) stability frame | a RECOMPILE moves standing (INVALIDATED -> recompile -> CURRENT/AMBIGUOUS/BROKEN). **The value a recompile structurally CANNOT clear: AMBIGUOUS** -- moved only by an OWNER declaration (fork-or-drift); named per Rule 24(iv). |
| ambiguity predicate (census-proved) | a SECOND PLAUSIBLE HOME = another HEAD path that holds the member's exact bytes, OR shares a NON-GENERIC basename with content similarity >= 0.5. Generic entry-point names (`handler.py`, `lambda_function.py`, `index.mjs`, ...) never count by name alone (the over-count this predicate replaced was caught by self-test 1 and fixed with a positive AND a negative fixture). |
| a missing artifact pointer | is NOT BROKEN: `source_dir+files[]` is still a build-input resolution; the `ARTIFACT_POINTER` hop stays `UNKNOWN` (provenance of the live package unverifiable) and the chain continues on bytes; the bundle's basis carries the caveat. |

## 3. Record R24-C3-003 -- hop `evidence_class`

| field | value |
|---|---|
| surface | `Support_Closure.hops[].evidence_class` |
| act | AUTHORED_AXIS |
| declared_layer | what kind of evidence ONE hop's instrument returns (**hop grain**) |
| members | `DECLARATION` (a build-input record: source-map entry / EC2_MANIFEST) · `ARTIFACT_POINTER` (the package manifest: artifact key + sha, BUILD_MANIFEST, provenance chain) · `DIGEST` (a live/staged object digest) · `BYTES` (member bytes compared to repo bytes at the build-input path) · `EXECUTION` (an on-instance/runtime/exercised read) |
| (i)-(iv) | MECE over what the instrument returns; one hop grain; one intent (evidence kind, never verdict); stability: a hop's class never changes with re-read -- only its `status` does. Every hop carries `resolved_via: BUILD_INPUT:<field>` (REQUIRED; a hop without a build-input basis is REFUSED = m2, so filename-resolved hops are inexpressible). |

## 4. `equivalence_claim.state` on the bundle -- adopted, not minted

`EQUIVALENT | DIVERGENT | UNMEASURED | UNKNOWN` at bundle grain. `UNKNOWN` reused at the envelope's sense (acquisition-failed); `UNMEASURED` reused at Response II's sense (neither true nor false). DIVERGENT basis distinguishes stale-vs-HEAD (deployed == repo@last_deployed_commit, HEAD moved) from a provenance mismatch (deployed != the build-input source at the recorded deploy commit). Shape C (transformed build): member bytes are build output and are NOT byte-compared by design; identity rides the digest chain.

## 5. Token census -- PINNED SURFACE SET (named; the next act cannot miss it)

**CANON surfaces (base's ruling 63890):** `infra/system/ontology/SYSTEM_DEFINITIONS.yaml` · `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` · `org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml`. **PROGRAM surfaces (in addition, never instead):** `docs/architecture/PRD_EPISTEMIC_MECHANIZATION_20260820.md` · `org/tier1_exec/4.0.0_SA_CRO/deliverables/RESPONSE_II_MUTATION_BUNDLE_AND_ADOPTIONS_20260820.md`.
Method: word-boundary; TOKEN (exact uppercase) vs prose (any case) classified per hit.

| token | TOKEN hits | prose hits | adjudication |
|---|---|---|---|
| PRESENCE_ONLY, INVALIDATED, AMBIGUOUS, DIVERGENT, ARTIFACT_POINTER | 0 | 0 | unoccupied |
| BEHAVIOR | 0 | 2 (Response II) | prose, same sense |
| CURRENT | 0 | 7 (SYSTEM_DEFINITIONS L471 "NOT its current phase"; C2C3 comments x3; PRD L82; Response II x1) | prose, not a value |
| BROKEN | 0 | 2 (PRD L31 "broken acquisition"; Response II L9) | prose |
| EQUIVALENT | 0 | 1 (Response II L111) | prose |
| BYTES / DIGEST | 0 / 0 | 4 / 11 | prose |
| NONE | 2 (SYSTEM_DEFINITIONS changelog strings 3.12/3.13) | 2 | uppercase prose inside changelog strings, not a value |
| EXECUTION | 1 (SYSTEM_DEFINITIONS L33 naming-act changelog) | 0 | prose |
| DECLARATION | 1 (SYSTEM_DEFINITIONS L72, inside the **Deploy_State** definition) + rule bank 7 (D3 contract strings "REQUIRED ON EVERY DECLARATION", base-run) | 9 | prose, not a value |
| UNMEASURED | rule bank 1 (:558, prose, base-run) | -- | reused at the same sense |

**Verdict: NO COLLISION.** Adjacent ratified term NOT re-coined: `Deploy_State` (`deployed | undeployed`) measures whether a COPY is deployed; `reach`/`standing` measure how far the EVIDENCE CHAIN got and whether it stands -- different intent, different grain.

## 6. Declared exclusions (the plane statement, verbatim for the proof)

`comp-pipescript deployed` answers script-grain MATCH/STALE on the S3 code prefixes (Phase-1 sweep 2026-08-20: bd 60 MATCH / 48 S3-ONLY / 12 UNCOVERED; inf carries INF_D_04 STALE) and does NOT resolve Lambda packages, second homes, or executing reads -- C3's domain. comp-closure does not invoke, deploy, or update anything; it never rewrites the source map; it arms nothing.
