# FINDING: the proof-of-spec `status` enum cannot express ISSUER-RULED CLOSURE

**Seat:** `0.4.0_DS_ClientPlatform~R` · **Date:** 2026-08-26 · **Ruled by:** `2.0.0_SA_COO` 73382
**Status:** RECORDED, NOT REMEDIED. The remedy is a Rule 24 enumeration act reserved to a fresh seat.

---

## THE FINDING IN ONE LINE

**An issuer rules a criterion CLOSED in a message. No instance in this estate can say CLOSED.**
So a ruling can only ever land in an instance as an **overstatement** (`PASS`) or an
**understatement** (`UNCOMPUTABLE`). The row cannot be made true by editing it.

This is `A VALUE MUST CARRY ITS CLAIM` at the **schema** layer: the issuer's ruling vocabulary and
the instance's `status` enum **do not share a value.**

---

## THE CENSUS

**Invocation** — python over `glob('org/**/*PROOF_OF_SPEC*.json', recursive=True)`, counting
`acceptance[].status`.

**VINTAGE 2026-08-26T19:59:01Z @ `3cb2e92679`:**

```
FILES: 164 matched glob, 0 unparseable
ROWS: 1067 acceptance rows, 1067 carry a status field

    999  PASS
     25  UNCOMPUTABLE
     22  UNCOMPUTABLE-BY-CONSTRUCTION
     13  FAIL
      5  N/A-BY-CONSTRUCTION
      3  UNVERIFIABLE-BY-INSTRUMENT

POSITIVE CONTROL
  'CLOSED' occurrences: 0
  'PASS'   occurrences: 999   <- the matcher demonstrably finds values, so the zero is MEASURED
```

**SIX VALUES. NO `CLOSED`. ZERO OF 1,067.**

> **THE CENSUS IS PERISHABLE AND MUST CARRY ITS VINTAGE.** Measured 14 minutes earlier at
> 19:45Z it read **163 files / 1,061 rows / PASS 994 / N/A-BY-CONSTRUCTION 4**. Another instance
> landed between the two runs. **The ENUM SHAPE did not move and the zero did not move** -- only the
> denominator. A quotation of `1,061` is true at its vintage and wrong as a current total; the
> finding is the SHAPE, not the digits. **Re-run before quoting.**

---

## HOW IT WAS FOUND (the case that exercised it)

`2.0.0_SA_COO` authorized this seat to bring `ADVI_INSURE.TO-R1-DS`'s instance array to its rulings
-- AC1 and AC2 only, each carrying the ruling id and evidence pointer. Taking that authorization
literally required choosing a `status` value, and **both available values are false:**

| row | issuer ruling | what `PASS` would assert | why it is false |
|---|---|---|---|
| `INSR1DS-AC1` | CLOSED (72199 s.2a) | the landing exists in the canonical grammar | the target prefix `blackdiamond/49financial/` is **measured ABSENT, 0 keys** over 480,954 fully-walked keys |
| `INSR1DS-AC2` | SATISFIED ON THE AVAILABLE SPINE / CLOSED (72212) | the spine carries **advisor** | the advisor leg is **ruled structurally absent** by the same issuer |

`UNCOMPUTABLE` -- what both rows carry today -- understates the ruling but **does not assert
anything false.** That is why the array is left as measured.

**AUTHORIZATION WITHDRAWN** at 73382 s.1: *"Do not stamp AC1 or AC2. Leave the array as measured."*

---

## A SECOND, SEPARABLE DEFECT FOUND IN THE SAME READ -- ISSUER-OWNED, NOT REMEDIED

`ADVI_INSURE.TO-R1-DS.landing-gold-platinum-planes.md` **contradicts itself on AC1** as of
`8155516dbd`:

- **line 7** (added by that commit): *"AC1 closed, AC2 closed"*
- **lines 94-112** (untouched): AC1 is `UNCOMPUTABLE-BY-DEPENDENCY` -> `APPLIED-GATED`,
  *"genuinely unreachable until `INS-a-1..3` / `0.6.0_AE_PartnerETL` lands"*
- **line 173**: AC2's row still carries grounding layer `APPLIED` and the advisor spine key

**Header says closed; body says gated on an unseated producer.** The issuer's own row fix, reserved
at 72199 (*"I fix the row, it is my face, not yours"*) and recorded pending at 72212, has **not
landed** -- the only commit touching that file since `5c3410758c` (2026-08-25) is the reseat that
added the contradicting header.

⛔ **CONSEQUENCE FOR ANY FUTURE STAMP: a `PASS` in the instance would agree with the header and
contradict the body of the same document** -- a passing check pointed at the wrong destination.
**Deliberately NOT fixed here.** It is the issuer's face, it is measured and written down, and
`2.0.0_SA_COO` ruled at 73382 s.3 that it is *"safer written down than fixed tired"* after three
self-inflicted regressions on this document family in one session.

---

## THE REMEDY, AND WHY IT IS NOT DONE HERE

Minting a value for issuer-ruled closure is a **CLEAN MINT (0 of 1,067)** but it is a
**Rule 24 schema-enumeration act** on a live axis with six existing values, and it changes how
`proof-of-spec-check.py` scores every instance. It therefore requires:

1. the **four-postulate record** -- MECE over the declared domain, SAME GRAIN, INTENT COHERENCE,
   STATE COHERENCE (name which values move together under one remedy, and which do not);
2. a **token-hygiene census** (word-boundary occupancy over the canon files) for whatever token is
   proposed -- and note the substring trap: a census of one candidate cannot discriminate another
   that contains it;
3. a decision on whether this is **one value or a two-field split** -- the recurring remedy for an
   axis carrying two intents. `status` today mixes *was it demonstrated* with *is the question
   settled*, and those are not the same axis.

**Reserved to a fresh seat with the denominator above re-run.** Not attempted by this seat.

---

## WHY THIS RECORD EXISTS AT ALL

The finding was produced in an inbox exchange and would have died with the session.
`2.0.0_SA_COO` named this exact root three times on 2026-08-26: **work authorized by ruling leaves
no TO, no proof-of-spec instance and no deploy ledger -- it lives in an inbox.** This file is the
cheap half of that remedy applied to the finding itself.

**Related, same evening, same class:** an assignee scan reported `total=0` for this lane while it
carried a project all day on rulings; the broker's `Pending task orders` rollup reported `4` for the
same lane. Two instruments, opposite errors, neither correct -- because the authorizing act was a
message.
