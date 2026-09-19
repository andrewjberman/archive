# LT-r-3-r7 result -- remediation census-and-route

**Worker:** `0.9.0_WK_LGIC_LGCTFM~3` on `LGIC_LGCTFM.TO-LT-r-3-r7`. **Branch:** `wk-lgic-lgctfm-7-3`
@`e788f77fd1`. **PRD** @`459b4a736d`. **Decomp** v1.8 @`5bb26b51e5`, cell `LT-r-3` (section 18). **Fixed
inputs pin:** `check_lt_r7.py` / `R7_BASE.json`, both at `5bb26b51e5` (`cut_pin` `ed073a4d48`).

## What ran

Re-parsed all 35 ```` ```json ```` fences in `REMEDIATION_v1.md` at write time (not inherited from the
order's own table) -- 35 unique row objects, 0 duplicate ids, matching the order's stated denominator.
Chose the predicate `closed == false (or the key absent)` over the order's alternative `disarm empty`
framing: `closed` is the one field every row from v1 through v6 carries uniformly, while `disarm` is a
sub-object present only on some early rows and dropped by convention from v3 onward, so keying on its
emptiness would conflate a schema-shape change with an actual disposition. Population under that
predicate: **23** (matches the order's own broader "not closed" count).

For each of the 23, read the row's own `remedy` field (not re-derived from mechanism alone) and wrote
either a concrete `next_act` naming who does what, or the literal `RETIRE` where the remedy text and
evidence show the finding is already fully discharged.

## Disposition

- **Routed: 16** -- S18, W1-S21, S21, S26, W1-S24, W1-S25, W1-S30, S32, S33, W2-S36, W2-S37, W1-S36,
  W1-S37, S41, S42, S44. Each `next_act` quotes or closely paraphrases the row's own stated remedy.
- **Retired: 7** -- S1, W2-S35, W1-S35, W1-S38, W1-S39, S35, S43. Each cites a completing commit
  (`1d4df2c115`, `21a163f492` x2, `d08be0b693`, `1df2481ca0`) or an explicit "nothing further owed" in
  the row's own text. Three of the seven (S43, W1-S38, S35) carry an EXTRA confirmation this cell found
  independently: their standing lesson is already codified into round 7's own fixed input --
  `R7_BASE.json`'s `the_new_bar_this_round_carries` (adopting S43's carrier verbatim, held by
  `1.0.0_SA_CTO` @`ed073a4d48`) and `stale_proof_bar` (matching S35/W1-S38's SET-EQUALITY-plus-informational-count
  shape) sections.
- **Unroutable: 0.** Every row in the 23-member population had a legible remedy text naming a concrete
  next act or a clear completion; none needed the honest "cannot decide" answer.

## Owner flags

Two rows carry an owner that does not match the act the remedy text itself describes, noted in each
row's `basis` rather than silently re-assigned:

- **W2-S37**: recorded owner `2.0.0_SA_COO~G` (this project's issuer), but its own remedy says "the
  surface is not this project's" -- the routing decision belongs to comp-system's owning seat.
- **S42**: recorded owner `2.0.0_SA_COO~G`, but the owed act is on a ROUND-N ANALYSIS, which the
  canonical workflow assigns to the CTO, not the project issuer.

No other owner among the 23 was found wrong or stale; the remaining 21 are held by `2.0.0_SA_COO~G` or
`1.0.0_SA_CTO`, both live in this session (COO~G issued this very round at `5bb26b51e5`; CTO closed
round 6 at `ed073a4d48`).

## A finding this cell did not fix

Row **W1-S37**'s own remedy is "stop quoting a derived arm-count in an order; the run prints its own" --
and this very round's own task order (`LGIC_LGCTFM.TO-LT-r-3-r7`) quotes `"34 arms, 10 positive, 4
driving the WIRING"` as a fixed expectation rather than letting `selftest-arms` print its own count. It
happened to match (confirmed: `selftest-arms` -> 34 arms, 10 positive, 4 wiring), but the pattern the row
warns against is still live in this project. Noted in the row's `basis`, not remedied here (cell 3
routes, it does not fix).

## Mechanical controls

- **Mutant:** blanked `remediation_route.predicate` in a scratch copy, re-ran `r3-route` ->
  `FAIL-R3-ROUTE` ("NO PREDICATE STATED..."), exactly the order's own `MUTANT-route-no-predicate`
  self-test shape. File restored byte-identical before this record was written.
- **Determinism:** `r3-route` run twice in succession against the unmutated record -> byte-identical
  output both times.

## Criteria

| id | verdict | evidence |
|---|---|---|
| R3R7-AC1 | PASS | `r3-route` -> `VERDICT: PASS-R3-ROUTE` (35/23/16/7/0) |
| R3R7-AC2 | PASS | `r7-vintage-field` -> `VERDICT: PASS-R7-VINTAGE-FIELD` (1 record present, this cell only) |
| R3R7-AC3 | PASS | `r7-stale-proofs` -> `VERDICT: PASS-R7-STALE-PROOFS` (1 commit since cut, informational; 0 at risk) |
| R3R7-AC4 | judgment, no verdict from this worker | recorded for `3.0.0_SA_CVO` at L9 |

Full instance: `LGIC_LGCTFM.TO-LT-r-3-r7.remediation-route.proof_of_spec.json` (this folder). Route
record: `REMEDIATION_ROUTE_R7.json` (this folder) @`e788f77fd1`.
