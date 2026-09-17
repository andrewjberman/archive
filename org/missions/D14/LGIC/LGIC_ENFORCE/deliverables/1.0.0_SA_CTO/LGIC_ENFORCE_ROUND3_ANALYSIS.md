# L10 ROUND-3 ANALYSIS -- LGIC_ENFORCE

**Written** 2026-09-17 ~18:5xZ by `1.0.0_SA_CTO` on `3.0.0_SA_CVO`'s L10 slug (97630, adjudication @262053c98c) over
`2.0.0_SA_COO~G`'s drain-end (97620, issuance @faf031f8d3, HEAD e405b6d942).

**Read for this analysis:** the slug; the drain-end; round 2's analysis @8f3badfbbf; the PRD's ENDPOINT (FWD-1..FWD-7);
rulings R-29 @b0ce1c4f5d and R-30 @eda81ff5c6; row W4-S6 and `RAISE_POPULATION_S6.r3.md`.

---

## 1. Outcome grades after round 3

| Outcome | Grade after round 3 | What moved it |
|---|---|---|
| FWD-1 a pipeline asks for its address, never types it | REALIZED (round 1) | unchanged |
| FWD-2 names are generated and the firm-separation rule comes from the same source | **REALIZED at APPLIED** (was EXERCISED-ON-PLANS, the applied bar owed) | EN-w-7 measured the LIVE policy on `opal-data-49financial` against the builder's output: Deny 17 == builder 17, and all four writers dispositioned with no applied policy moved. The CVO graded W7R3-AC3 PASS on evidence that names query, window and count |
| FWD-3 one list says where a firm's data lives | REALIZED, coupling disclosed (round 2) | unchanged; S60 below is its standing finding |
| FWD-4 a wrong name is stopped and the right form printed; existing work keeps running | **REALIZED** (was REALIZED-ON-PRACTICE, the estate flip bound) | issuer act 2b: `org/mcp/naming-gate.enforce` @d181e0ac5a, after EN-n-1 drained. 68 planned roots read with the switch on: 16 refusals, 16 of 16 on create/update, **0 on an existing resource**, positive control fires. EN-n-1's baseline reproduced exactly (3815/2917/90) and graded PASS |
| FWD-5 one run lists every out-of-pattern name across the estate | **NOT REALIZED**, moved to round 4 by design | EN-s-6 under R-29's amendment: judged 21 (was 3), one measured mint (`inf-otp-relay-api`), two owner cards, then the 25-RAISE timebox tripped with **351 distinct RAISEs** measured ahead (`RAISE_POPULATION_S6.r3.md`, row W4-S6). S6R3-AC5 graded PASS: all 124 uncompared rows carry a stated reason |
| FWD-6 a clean-up cannot quietly stall | REALIZED (round 1) | unchanged |
| FWD-7 taking on a new firm is one entry in one list | REALIZED (round 2) | unchanged |

**Round summary: REALIZED 6 of 7. NOT REALIZED 1 (FWD-5), carried to round 4 on a measured list.** The project is NOT
CLOSED. Round 3 did what it was cut to do: the flip and the applied bar both landed, and the census failed HONESTLY at a
ruled boundary rather than by surprise.

## 2. What round 3 proved about the census, and why the timebox was right

The census is not one stuck name; it is a population. Round 2 read 3 of 1,821 live names judged. Round 3, with the
registry paths granted, judged 21 and then measured what remained instead of grinding: **351 distinct RAISEs**, plus 8
`{system}`-placeholder rows (W2-S10's class) that are a separate rule, not RAISE-bounded. Had the worker continued, the
round would have ended in an unbounded registry campaign inside a cell cut for a census. R-29's timebox converted an open
grind into a measured backlog with an owner. **That list is round 4's input, and its size is the reason round 4 exists.**

## 3. Rulings this analysis carries

**R-32 (round 4's shape).** FWD-5 closes through a REGISTRY CAMPAIGN, not another census run. Round 4 is cut as:

| cell | what it does | bar |
|---|---|---|
| R4-a **the campaign** | work the 351-name list: mint the registry row where owner and token are MEASURED from a declared source (lambda-source-map, EC2 manifest, terraform tree); otherwise one owner card with the reason, name recorded NOT-JUDGED | every name in the list is minted or carded; the carded count and its denominator printed; `validate` stays OK |
| R4-b **the placeholders** | the 8 `{system}`-placeholder rows (W2-S10) resolved or carded | 0 placeholder rows reach a report row, or each carries a card |
| R4-c **the run to the end** | re-run `census --live --repo` to completion on both planes | `judged + carded == nameable` on BOTH planes, denominators printed, the live plane's `built:` vintage stated |
| R4-d **R-30's criterion text** | DEC-4(ii) amended: a NOT_A_PRINCIPAL claim on a bucket with no live CloudTrail data-event selector is REFUSED; disposition comes from a direct IAM-grant read or a NOT-JUDGED card | the amended text is in the round-4 cut, and a planted claim on such a bucket is refused |
| R4-e **S60** | the ship classifier's undercount (R-16), graduated as a standing finding by the CVO this round, gets a disposition: fixed, or carded with its owner and reason | either the classifier's count matches a measured denominator, or the card names who owns the gap |

**The fence guard from R-29 carries verbatim into R4-a**: a row whose mint would change a GENERATED POLICY on an APPLIED
resource is NOT minted -- it is carded BLOCKING for never-widen sign-off (`1.0.0_SA_CTO` + `2.0.0_SA_COO`).

**R-33 (the timebox travels).** R4-a carries its own bound: if the measured list grows past 351 + 25 while the campaign
runs, the cell stops, files the delta, and the remainder rides round 5. A campaign cell without a bound is the grind R-29
refused.

## 4. Closure test, stated now so round 4 is cut against it

LGIC_ENFORCE closes when FWD-5 grades REALIZED with the other six unchanged. **The bar for FWD-5 is `judged + carded ==
nameable` on both planes with denominators printed -- NOT "zero carded".** A carded name is a named gap with an owner,
which is what the outcome promises; a run that stops early is not.

## 5. Recorded, not this round's

- **S60** (R-16's ship classifier undercounts) is a live standing finding, now R4-e.
- **S56/S57** graduated: the static-lane wall was discharged by the `<paths>` grant mechanism, confirmed when EN-r-5-r3's
  worker committed the registry file directly and drained clean.
- **W2-S12** GRADUATED and DISARMED under R-30 in one write, owner CloudOps -> CTO.
- EN-s-6's `<status>` stays `pending` by design (R-29's timebox); the gate's own L10 line reads it terminal by VALID proof.
