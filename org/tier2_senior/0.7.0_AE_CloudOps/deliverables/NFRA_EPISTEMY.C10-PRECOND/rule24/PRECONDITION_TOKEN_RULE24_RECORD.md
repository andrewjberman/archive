# Rule-24 record + token census -- Precondition_Token object (NFRA_EPISTEMY C10-PRECOND leg)

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-08-20 · **Status:** PROPOSAL PACKAGE (not landed).
**Schema act routes through 4.0.0_SA_CRO base** (registry executor, S2); base's spec cert precedes
1.0.0_SA_CTO's arch gate. This record is the proposal's required companion under the widened Rule 24
(Andrew-direct 2026-08-20: every schema-enumeration act -- minting, adding values, OR adopting --
arrives WITH its four-postulate record and a token-hygiene census, or it is not a proposal).
**Nothing here is minted in-lane.** Source of record CITED, never re-declared: S5 sec.1/2
(`org/tier1_exec/4.0.0_SA_CRO/deliverables/NFRA_EPISTEMY/S5_PROFILE_ALGEBRA_AND_MUTATION_GATEWAY_SPEC_20260820.md`).

## What is being enumerated

The Precondition_Token object (S5 sec.1 `precondition_token` row) itself REUSES S5's vocabulary --
its rejection is (gate=TRANSACTION, reason=PRECONDITION_CHANGED), reused not re-coined. Two small
value-spaces are introduced by the *implementation* and are the subject of this record:

- **Axis A -- `target_state_digest` state:** what state of the target the token asserts.
- **Axis B -- rejection `detail` sub-codes:** the discriminator carried inside a single
  (TRANSACTION, PRECONDITION_CHANGED) rejection, distinguishing WHY the precondition did not hold.

Both are held to the four postulates below. A distinct *typed reason* for token-inadmissibility is
explicitly NOT coined here -- it is recorded as a proposal to base (see "Proposal to base").

## Axis A -- target_state_digest state

Values (the CLEAN enum): **ETAG** (a concrete content-address the store returned) · **ABSENT** (the
first-mint sentinel; the token asserts the target does not exist). `null` is NOT a third value: per
S6 absence semantics it is the ABSENCE of a value, handled as REFUSED, never as a state.

| Postulate | Verdict |
|---|---|
| (i) MECE | Exclusive: a token asserts exactly one of ETAG / ABSENT. Collectively exhaustive over the *live target states* a read can return: PRESENT -> ETAG, clean-404 -> ABSENT. An unreadable target yields NO token at all (`read_precondition_token` returns None), so "unknown" never becomes a digest value -- it is refused upstream. |
| (ii) same grain | Both at the single-target-object grain (one S3 key). |
| (iii) intent | One intent: "what state of the target the write is bound to." No handling-policy or output-class mixed in. |
| (iv) stability | ETAG and ABSENT MOVE TOGETHER under one remedy (a write): a first mint flips ABSENT->ETAG; a delete flips ETAG->ABSENT. One instrument (the conditional put) moves both. `null` does not sit on this axis -- naming it as a value would be the two-grains-on-one-axis defect (a live state beside an inadmissibility marker); it is kept OFF the axis as the S6 not-a-value. PASSES. |

## Axis B -- rejection detail sub-codes

Values: **WINDOW_EXPIRED** · **READ_WINDOW_NULL_REFUSED** · **DIGEST_NULL_REFUSED** ·
**READ_AT_NULL_REFUSED** · **ETAG_MISMATCH_412** · **ALREADY_EXISTS_412**.

| Postulate | Verdict |
|---|---|
| (i) MECE | Exclusive by construction: token validation is first-match (window-null -> digest-null -> read_at-null -> window-expired), and the two 412 codes are on the store path, disjoint from the token-validation codes. CE over the ways a precondition fails: malformed token (3 null cases), stale token (WINDOW_EXPIRED), world-moved (2x 412). |
| (ii) same grain | One admission attempt. |
| (iii) intent | One intent: "the discriminating cause of a PRECONDITION_CHANGED." |
| (iv) stability -- **BLATANT FAILURE NAMED** | The six codes carry THREE remedy classes under one reused reason, and they DO NOT move together: the three `*_NULL_REFUSED` codes are TOKEN-AUTHORING defects (remedy: fix how the token is built); WINDOW_EXPIRED is a TIMING outcome (remedy: re-read / shorten read-to-act latency); the two `*_412` codes are WORLD-MOVED outcomes (remedy: re-read the new state and retry). This is exactly the axis a stability frame is meant to surface: one reason value presenting three workstreams. It is tolerated ONLY because the detail STRING is a diagnostic annotation, not an enumerated axis a consumer branches on -- and it is the direct evidence for the proposal to base below. |

## Proposal to base -- RESOLVED (base spec cert 63913, S5 0.1.2 @c67ef52c1a; CTO concur 63945)

The proposal is ruled, and the Axis-B(iv) finding was correct. This record originally proposed a
distinct TRANSACTION reason (candidate `TOKEN_INADMISSIBLE`) for the null/malformed-field cases.
**Base ruled AGAINST that homing and FOR a cleaner one: the three `*_NULL_REFUSED` cases are a
BUNDLE-SHAPE defect and home at `(COMPILATION, BUNDLE_MALFORMED)`, NOT under TRANSACTION.** The
reasoning (CTO's remedy-by-gate argument, applied): a malformed bundle's remedy is FIX-THE-CALLER,
which has no business inside the retry-or-escalate TRANSACTION gate -- minting `TOKEN_INADMISSIBLE`
under TRANSACTION would have put two remedies behind one gate. `PRECONDITION_CHANGED` stays reserved
for the genuine world-moved / read-too-old cases (WINDOW_EXPIRED + the two 412s). The implementation
now emits `(COMPILATION, BUNDLE_MALFORMED)` for the three null cases and `(TRANSACTION,
PRECONDITION_CHANGED)` for the rest -- three `detail` sub-codes under each of the two reasons, so the
stability defect Axis B (iv) named is resolved: each reason now carries ONE remedy class.

## Token census (word-boundary occupancy over the canon surfaces, run 2026-08-20)

Surfaces: `CLAUDE.md`, `rcg/rulings/RULINGS.jsonl`, `infra/system/ontology/SYSTEM_DEFINITIONS.yaml`
(the canonical term registry). Method: `grep -cwo <token>` per surface.

| token | CLAUDE.md | RULINGS | SYSTEM_DEFINITIONS | class |
|---|---|---|---|---|
| WINDOW_EXPIRED | 0 | 0 | 0 | NEW, clear |
| READ_WINDOW_NULL_REFUSED | 0 | 0 | 0 | NEW, clear |
| DIGEST_NULL_REFUSED | 0 | 0 | 0 | NEW, clear |
| READ_AT_NULL_REFUSED | 0 | 0 | 0 | NEW, clear |
| ETAG_MISMATCH_412 | 0 | 0 | 0 | NEW, clear |
| ALREADY_EXISTS_412 | 0 | 0 | 0 | NEW, clear |
| PRECOND_ABSENT | 0 | 0 | 0 | NEW sentinel, clear |
| VERIFY_FAILED | 0 | 0 | 0 | NEW outcome, clear |
| StopAndSurface | 0 | 0 | 0 | NEW, clear |
| Precondition_Token | 0 | 0 | 0 | NEW object, clear |
| put_if_precondition | 0 | 0 | 0 | NEW fn, clear |

**Reused (same sense, compatible):**
- `PRECONDITION_CHANGED`, `TRANSACTION` -- from S5 sec.2. 0 occurrences in the canonical
  SYSTEM_DEFINITIONS because S5 is PROPOSED 0.1.1 (its vocabulary lives in the S5 spec + exchange
  records, cited); reused, not re-coined.
- `ABSENT` (the sense inside the `PRECOND_ABSENT` sentinel) -- same sense as C1's
  `status.acquisition = ABSENT` (object-not-present). Compatible; the sentinel value string is the
  bare word `ABSENT`, and the Observation_Records this leg emits use C1's acquisition enum directly.

**RESULT: no collision.** Base runs the authoritative census at the schema act; this is the
proposal-companion census.
