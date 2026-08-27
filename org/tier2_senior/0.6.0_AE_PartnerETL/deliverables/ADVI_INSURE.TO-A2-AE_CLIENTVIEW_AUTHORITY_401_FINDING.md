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

## Status

`INSA2AE-AC1`: **UNCOMPUTABLE-BY-DEPENDENCY**, dependency named — the ClientView authority mint on the
49F principal. Not a refusal, not an absence, not a failure of the capture design. Nothing landed;
no bronze written. The capture resumes the moment a ClientView mint succeeds, unchanged.
