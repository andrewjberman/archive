# NFRA_EPISTEMY.C4-LEASE -- Rule-24 records (lease state, evaluation result) + pinned-surface token census

**Author:** 0.8.0_AE_CloudComp, 2026-08-21 · **GO:** 2.0.0_SA_COO 64063 (/drive, Andrew-scoped "NFRA_EPISTEMY to close") · **Spec cert:** 4.0.0_SA_CRO base 64109, S3_C4_LEASE_ELIGIBILITY_SPEC_CERT_20260821.md @053b83f414 -- CERTIFIED-WITH-ONE-ADJUDICATED-DEVIATION (D1 ruled: moved-identity -> EXPIRED supersedes Response III sec.1.4's "changed digest -> INVALID"; INVALID is an EVALUATION'S result, a changed digest without re-evaluation has produced none) · **First basis:** kb-20260821-6ce229dd (five nulls, digest via the normative home; consumed with the digest REPRODUCED before use).
**Sources of record (cited, never copied):** PRD sec.2.5 + sec.1 row 4 + sec.3 law 7; KNOWLEDGE_BASIS.schema.json 0.1.1 @151eaf7e4c; C3 Support_Closures (the identity substrate); CTO Note 2 (the effect pair) via COO 64063.
**Objects:** PROPOSED shape; registry landing is base's act (rider b); every instance carries `object_status`.

## 1. Record R24-C4-001 -- the lease `state` axis (computed, never stored)

| field | value |
|---|---|
| surface | the value returned by `comp-lease state` for ONE lease (lease grain) -- **there is no stored state field**; the axis exists only as a read-time computation |
| act | AUTHORED_AXIS |
| declared_layer | what a consumer may RELY ON NOW, for one lease |
| members | `VALID` · `INVALID` · `UNKNOWN` · `EXPIRED` |
| (i) MECE | by a TWO-LEVEL PARTITION TREE, no ordering language: LEVEL 1 -- does the minting evaluation still BIND (no support identity moved since it ran AND the validity window is open)? NO -> `EXPIRED` (the last result is OUT OF SCOPE, not out-ranked; "failure to reevaluate never preserves validity" is THIS BRANCH, not a precedence rule). YES -> LEVEL 2, the evaluation's result: supported -> `VALID`, unsupported -> `INVALID`, undeterminable -> `UNKNOWN`. CE hunted: `NEVER_EVALUATED` is UNREACHABLE BY CONSTRUCTION (a Lease requires `minted_by_evaluation`); a closure standing AMBIGUOUS evaluates `UNKNOWN` on the axes ambiguity blocks (not a fifth value); a side-read retrieval failure is `UNKNOWN`, never `VALID`. |
| (ii) same grain | one lease, always |
| (iii) intent coherence | one intent: reliance-now. NOT evidence reach (C3 `reach`), NOT chain standing (C3 `standing`), NOT edit eligibility (the sibling object's `result`). The C3 diagnostic applied IN ADVANCE: no precedence clause exists because no case satisfies two members. |
| (iv) stability frame | re-evaluation moves every value; the value nothing at THIS grain can move is `INVALID`-because-unsupported -- only a change in the SUPPORTED THING (a new closure vintage) reopens it. Named per 24(iv). |
| adjacency (census-caught, named, not re-coined) | the rule bank's `EXPIRED` (:501, declaration-concealment axis: "an expired declaration must stop concealing") is a DIFFERENT intent at a different grain. |

## 2. Record R24-C4-002 -- the evaluation `result` axis

| field | value |
|---|---|
| surface | `Eligibility_Evaluation.result` |
| act | AUTHORED_AXIS (adopting the PRD's own value set at its own sense -- adoption re-runs the record) |
| declared_layer | may this claim/edit proceed under the current basis and support state (one evaluation) |
| members | `ELIGIBLE` · `INELIGIBLE` · `UNKNOWN` |
| (i) MECE | {yes, no, cannot-determine}; CE closed by `UNKNOWN` (side unreadable -- a retrieval failure is never support) |
| (ii)/(iii) | one evaluation; one intent (proceed-under-basis) |
| (iv) stability | a basis or support change moves results only THROUGH a new evaluation -- the one-per law (m4: identical (assessment, scope, basis digest, support-state digest) REFUSED) makes re-litigation in place impossible |

## 3. Content-addressed ids -- derivation homes IN THE CONTRACT (COO 64098, the three-for-three pattern)

Every content-addressed id this component mints derives via **the normative home** `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_EPISTEMY.C10-PRECOND/precondition_token.py` `_request_hash` (json.dumps sort_keys=True, separators=(",",":"), UTF-8, "sha256:"+hexdigest) **over a NAMED payload** -- any other serialization is NON-CONFORMANT even if the digest pattern matches:

| id | payload (exact keys) |
|---|---|
| `evaluation_id` (`ee-<12hex>`) | `{"a": assessment_digest, "s": scope, "b": current_basis.digest, "v": support_state_digest}` -- hex chars 7..19 of the hash |
| `lease_id` (`lease-<12hex>`) | the minting evaluation's id suffix (one lease per minting evaluation, by construction) |
| `support_state_digest` | `{member_id: identity}` over the five support members, via the normative home |
| `assessment_ref.digest` | sha256 over the closure file's BYTES (immutability of the assessed artifact -- not a serialization) |
| consumed: `Knowledge_Basis.digest` | base's mint, REPRODUCED through the normative home over `members` before use; a non-reproducing mint is REFUSED loudly |

## 4. Token census -- PINNED SURFACE SET (canon 3 + program 2; word-boundary)

`infra/system/ontology/SYSTEM_DEFINITIONS.yaml` (91,348 B) · `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` (109,368 B) · `org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml` (49,181 B) · `docs/architecture/PRD_EPISTEMIC_MECHANIZATION_20260820.md` · `RESPONSE_II_MUTATION_BUNDLE_AND_ADOPTIONS_20260820.md`.

| token | hits | adjudication |
|---|---|---|
| VALID 2 / INVALID 1 / EXPIRED 2 / ELIGIBLE 1 / INELIGIBLE 1 | PRD's own component-4 / sec.2.5 lines + rule-bank prose | source-of-record reuse at the same sense; rule-bank `VALID` (:455) and `EXPIRED` (:501) are DIFFERENT senses -- adjacencies named (sec.1) |
| Lease 0 / effect_as_recorded 0 / effect_as_evaluated 0 / UNCOMPUTED 0 / EXPANDING 0 / exclusion_proof 0 / intersecting_changes 0 / NEVER_EVALUATED 0 | -- | unoccupied |
| Eligibility_Evaluation 1 | the PRD's own sec.2.5 heading | the object being implemented |
| residual 4 | prose | reuse at the same sense |

**NO COLLISION.**

## 5. The live flip (L5) -- the real support change is this deliverable's own landing commit

Pre-flip (PRINTED, HEAD 5d453a6b9b24): leases lease-7c2dc1f71fb9 (inf-gold-trigger), lease-7e8dfe7f4e72 (finbert-batch-processor), lease-c61eada968fe (public-data-router) all read `VALID` with the capped axes named and support_state_digest reproduced True. The commit that lands this file MOVES `repo_head` -- a REAL support identity change on the real tree -- and the post-commit state read must print `EXPIRED` for every lease ("the minting evaluation no longer BINDS"). Shown in the proof, not asserted (CRO 64109's condition). Live INELIGIBLE specimens also on disk: the first mint round raced PEER COMMITS on the shared worktree (repo_head moved between compile and evaluate -- ee-47a5343910e8, ee-95e9e2b566eb) and the OLD committed closure @d652c88490 evaluated INELIGIBLE (ee-f315be98c8fa) -- the pipeline detecting a genuinely moved identity, three times, before the battery's synthetic mutants ever ran live. lease-97d3b394cc5c is the fixture-basis first mint of finbert, retained as a labelled build-transcript artifact and superseded by lease-7e8dfe7f4e72.

## 6. Declared exclusions

Components 5/6 (policy/scope/epoch; transaction kernel) consume leases -- nothing built for them. The basis is CONSUMED (base authors it); Discrimination_Certificates are optional members not yet attached. The one-per refusal is process-local today (declared in the output contract's blind_spots). Nothing armed; read-only AWS; the objects land in no registry from this lane.
