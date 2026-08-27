# TO-A2-AE: the advisor capture is blocked UPSTREAM of every surface — the ClientView authority 401s while DataMining mints, on ONE cookie

**Seat:** `0.6.0_AE_PartnerETL` · **Measured:** 2026-08-27 ~18:0xZ · **Against:** `ADVI_INSURE.TO-A2-AE`
(INSA2AE-AC1), COO ruling 76247/76292, Andrew egress word @a1e9fbcca7 (surface-scoped reading, 76291).
⛔ **DISTRIBUTION: NOT TO `4.0.0_SA_CRO`.**

## The result, stated at the right grain

**`relationshipdetail` WAS NEVER CALLED. Zero calls. Therefore this file contains ZERO evidence about
that surface's entitlement, its shape, or whether advisor data exists on the 49F principal.**

That distinction is the whole point of INS-a-3, and it cuts against my own convenience here: it would
be easy to file this as "the advisor capture refused" and let it read as a fact about advisor data. It
is not. The failure is **upstream of every insurance surface**, at the authority mint.

| | |
|---|---|
| what failed | `GET /session/token` — the **ClientView authority mint** |
| what did NOT fail | the cookie, and the **DataMining authority** |
| surfaces reached | **0** |
| what this says about `relationshipdetail` | **nothing** |

## The measurement — a paired rate test on ONE cookie

The cookie is alive: retrieved from `blackdiamond/49f/session`, **1647 bytes, contains `.bd.identity=`**.

```
RATE TEST, 3 paired attempts, one cookie, same seconds:
  clientview   GET /session/token           minted 0/3
  datamining   GET /datamining/auth/token   minted 3/3
```

**A total failure on one arm beside a total success on the other, from the same cookie in the same
seconds, is an AUTHORITY-SPECIFIC signature** — not a transient, not an expired session, not a dead
cookie. Each arm is the other's control; neither verdict rests on a probe that could only say one thing.

⚠ **A CORRECTION TO MY OWN FIRST READING, recorded because it nearly became the finding.** My first
two-arm run reported `cookie retrieved: NO` and a clientview 401 — I had guarded the cookie fetch with
`hasattr` on a **guessed** function name (`get_session_cookie`; the real one is `load_bd_session`), so
the guard silently passed `cookie=None` and ARM A 401'd because it was unauthenticated. That 401 tested
nothing. Had I reported it, "the 49F cookie is dead" would have gone on the record, aimed the remedy at
the wrong lane, and been *consistent with every symptom*. The instrument failed and was about to be
read as a verdict.

## What this falsifies — and it is my own lane's claim

`insurance_leg.py`'s module docstring records, from 2026-08-25:

> *MEASURED 2026-08-25 on the 49F principal: the two mints return BYTE-IDENTICAL bearers
> (sha256[:16]=e3c20170eedbafd3, len=66 both). So on bd3, the bearer is PER-SESSION, not per-app.*

**That is no longer true.** Two days later one authority mints and the other 401s. The relationship
between the two authorities was measured correctly on 08-25 and has since **diverged**.

This is also why `INSA1AE-AC1` was reported FAIL-by-design: its third clause asserted the authorities
were *distinct*, measurement said byte-identical, and the conjunction was reported false rather than
massaged. **The clause the criterion asserted is now the state the vendor is actually in.**

**AND THE LEG PREDICTED EXACTLY THIS, IN WRITING, AND DESIGNED AGAINST IT:**

> *DO NOT COLLAPSE THE ROUTING ON THAT RESULT. Three reasons it stays per-surface: (1) the identity is
> a MEASUREMENT OF TODAY'S SESSION, not a contract BD owes us — collapsing to one ambient token makes a
> future divergence a **silent 401 in production**…*

Had the leg collapsed to one ambient token on the 08-25 identity, today's divergence would have surfaced
as an unexplained 401 inside a data pull. Because routing stayed per-surface and each surface declares
its authority, the divergence is **legible at the mint** instead. A design decision taken against a
measurement the author distrusted paid out in 48 hours.

## Blast radius — beyond this TO, and named rather than chased

`SURFACES` authority routing, read at source:

| surface | auth | status today |
|---|---|---|
| `insurancerelationshiplist` (S1) | **datamining** | mint works |
| `relationshipaccountdetailsearch` (S3) | **clientview** | blocked at mint |
| `relationshipdetail` (S4) — *this TO's target* | **clientview** | blocked at mint |
| `accountdetailsearch` (S2) | clientview | egress-held anyway (D3 carve-out) |

⛔ **WIDER THAN THE INSURANCE LEG:** `lambda_function.py:290`, inside the vehicle's own `run()`, calls
`get_clientview_token(cookie)`. The deployed **bd49f reporting producer's main path mints the failing
authority**, so it would 401 on invoke today. I have not invoked it to confirm — that is another lane's
surface and its own act. **Named, not chased.**

Also measured, so the remedy is not aimed at the wrong component: **`bd-49f-keepalive` is healthy** —
State=Active, **24 invocations / 0 errors in the last 6h**. The keepalive is doing its job; whatever
extends the session server-side is not what is failing. The `bd-49f-auto-login` chain
(`infra/aws/ec2/bd-49f-auto-login/`) is the component that re-establishes a ClientView session.

## RESUME PROTOCOL — binding on whoever runs this capture next (3.0.0_SA_CVO 76309 + 2.0.0_SA_COO 76310)

⛔ **DO NOT resume by re-running the cohort loop.** Two rules were ruled by `3.0.0_SA_CVO` (76309,
landed `org/surprise_channel/ADVI_INSURE/INVESTIGATION_v1.md @bc30c64c53`) AFTER this finding was
filed and BEFORE any byte is captured. They are written here because a rule that lives only in a
message is not a protection — the message scrolls, the artifact persists.

1. **PROBE FIRST.** When the ClientView mint recovers, capture **ONE** relationship id and read
   `financialTeam[]` **before spending the cohort**. The bounded capture script defaults to
   `CAPTURE_LIMIT=3`; **set it to 1 for the probe.** Spending the cohort first is the failure this
   rule exists to prevent.

2. **AN EMPTY `financialTeam[]` IS A COMPLETE ANSWER AND A REAL FINDING — NOT A FAILED CAPTURE.**
   It closes the question as a Black Diamond **CONFIGURATION** state; the advisor-basis stamp moves
   to a vendor-config value and the resulting ask routes to Andrew. Sibling to AC1's
   refusal-is-complete law. **NO retry, NO widening the surface set, NO quiet absorption** — an empty
   result must not be re-run until it returns something.

3. **THREE OUTCOMES ARE PRE-REGISTERED, AND EACH IS COMPLETE** (`2.0.0_SA_COO` 76310): an **EMPTY**
   return, a **REFUSED** return, and a **POPULATED** return are **three different findings**, all
   scored as complete. None of them is a failed capture, and none licenses a retry.

⚠ **EXPECT EMPTY — AND THAT IS WHY PROBE-FIRST MATTERS.** The population expectation that made a
populated `financialTeam[]` seem likely rested on **COTTONWOOD** bytes. On 49F, the sibling `teams[]`
field is affirmatively empty **77 of 77**. **The FIRM is the variable, not the surface.** So the
single most probable result of this capture is an empty array that CLOSES the question as a Black
Diamond configuration state — and spending the whole cohort to learn it would be pure egress with no
additional information.

**Owner of the unblocking act:** the bounded ClientView re-establishment is routed to
`0.7.0_AE_CloudOps~L` (76305), the owning family's seated member — **not this seat, and not the
keepalive.** This seat does nothing to the auth chain; it fires the one-relationship probe on
mint-restored.

**The interlock that makes this the strong form:** because the authority block stopped the capture,
`0.4.0_DS_ClientPlatform~R`'s both-branch AC1 prep is **pre-registered before any byte exists** — a
discriminator registered ahead of its data, which is the strongest form a pre-registration can take.
Do not spend that advantage by capturing broadly and deciding the interpretation afterwards.

## Status

~~`INSA2AE-AC1`: **UNCOMPUTABLE-BY-DEPENDENCY**, dependency named — the ClientView authority mint on
the 49F principal. Nothing landed; no bronze written.~~

⛔ **SUPERSEDED 2026-08-27 ~18:3xZ — THE DEPENDENCY WAS DISCHARGED AND THE CAPTURE RAN.** Struck rather
than deleted, because the block was real and its evidence is what routed the remedy.

`0.7.0_AE_CloudOps~L` restored the ClientView authority (76345, bounded single act: clientview **3/3**,
datamining **3/3** held as the control). The probe fired immediately after, under the protocol above.

**RESULT — the pre-registered EMPTY outcome fired.** `relationshipdetail` on 49F relationship
`z08117302`: HTTP-200, 3093 bytes, landed raw. **`financialTeam` is PRESENT, a list, length 0 —
affirmatively empty, not absent and not null**; `financialTeamTemplateId` is `None`. The surface DOES
carry the advisor hop and 49F has no team assigned: a **Black Diamond CONFIGURATION state**. Probe-first
was honoured — **1 of 50 harvested ids spent, the cohort was not.**

`INSA2AE-AC1` closes **PASS/MEASURED**. Full scoring, controls and denominators:
`ADVI_INSURE.TO-A2-AE_PROOF_OF_SPEC.json` (VALID, `TRUE_RC=0`, 4 rows, 0 violations).

**One residual, stated because the finding must not be read wider than it is:** 1 relationship was
measured *directly*, of a server total of **77**. I do not claim all 77 are empty. The corroboration is
that the sibling `teams[]` is empty on **50 of 50** rows of the cohort page I landed myself — which
independently reproduces the 77/77 prior from another seat, on a different page of the same cohort.
