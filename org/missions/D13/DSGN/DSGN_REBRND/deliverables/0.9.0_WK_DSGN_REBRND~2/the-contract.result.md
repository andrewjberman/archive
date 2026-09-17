# RESULT -- DSGN_REBRND.TO-RB-s-7 (the contract), worker `0.9.0_WK_DSGN_REBRND~2`

**Delivered:** `portal/DESIGN.md` at portal commit `000478c9655409eae13f357106d2f5277e16d628`
(branch `wk-dsgn_rebrnd-2b`, LOCAL). It has twelve numbered clauses (`C1`..`C12`) and eight
sub-clauses (`C5.1`..`C5.8`), with design.md-shaped YAML front matter.
**Proof:** `DSGN_REBRND.TO-RB-s-7.the-contract.proof_of_spec.json` in this folder.
**Checker:** `python .tools/proof-of-spec-check.py <instance> RB7-AC1,...,RB7-AC7` returned
`VALID (rc=0)` with violations=0 before the flip. The surprises frame read "7 entries; 7 open with a
row id; 7 resolve to a channel row". The first run returned rc=1 on two CCX refusals, both against
tracked files that ride this commit: the channel and the task-order file. They were dropped from
`artifacts_produced` and declared under `declared_exclusions`. They were not re-pinned to a commit
that does not carry them.

## Criteria (verbatim invocations, run twice, byte-identical)

| id | verdict line | denominator | status |
|---|---|---|---|
| RB7-AC1 | `VERDICT: CONTRACT-SHAPED` | 16 numbered clause lines, bar >= 8 | PASS |
| RB7-AC2 | `VERDICT: BYTE-EQUAL` | 0 of 15 palette values missing | PASS |
| RB7-AC3 | `VERDICT: ALL-PINNED` | 0 of 4 required tokens missing | PASS |
| RB7-AC4 | (judgment) | build kit produced; page NOT built (row W2-S10) | UNVERIFIABLE-BY-INSTRUMENT -- `3.0.0_SA_CVO` at L9 |
| RB7-AC5 | (judgment) | `/positioning` rejected on C3 (+ C8, C4, C6, C12); author's agreement owed | UNVERIFIABLE-BY-INSTRUMENT -- `3.0.0_SA_CVO` at L9 |
| RB7-AC6 | `VERDICT: CANON-CLAUSE-ORDERED` | 5 of 5 hexes, 1 ordered block | PASS |
| RB7-AC7 | `VERDICT: INVERSION-CARRIED` | 0 of 8 elements missing | PASS |

The pre-cell baseline is the RD draft run through the same invocations. It read AC2 DIVERGES
(8 of 15 missing), AC3 MISSING-PINS, AC6 CANON-CLAUSE-MISSING and AC7 INVERSION-MISSING. AC1
already read CONTRACT-SHAPED on the draft, because it has ten numbered anti-patterns, so AC1 on its
own cannot tell a draft from a contract. Four mutants fired, one per instrument; see the
instance's `controls`.

## What the contract carries that Amendment 1 required

- **A. The canon lock:** C4, with one ordered table UST `#F97316`, ST `#F59E0B`, INT `#10B981`,
  LT `#3B82F6`, ULT `#EF4444`. It also carries the reading-axis rule, "the only locked colours",
  the exemption from C7, its home in `modelPortfolioColors.ts` and the authority record. No token
  file was edited.
- **B. Option A:** C3, white `#FFFFFF` panels with a `#C4CBDB` hairline, navy titles, and one
  `#0A1733` band per page. The `contentPanel` divergence is stated in the clause and filed as row
  W2-S5.
- **C. The inversion rule:** C5 and C5.1..C5.8, carrying the rule sentence, the per-role targets
  4.8 / 6.4 / 4.6 / 5.4, the 1.35 floor, opacity 1.0 and the citation of
  `design/brand/inversion-rule.json`. No worked-example output hex is restated.
- **D. Not carried:** the opaque ladder's rung hexes (its principle is carried), the values in
  `light-ground-semantics.json`, and the draft's off-token colours. The status block is carried
  byte-equal.

## Rows filed (all `UNDER_INVESTIGATION`)

| id | class | hazard | one line |
|---|---|---|---|
| DSGN_REBRND-W2-S5 | OBSERVATION | ARMED (`2.0.0_SA_COO~D`) | the token file's `contentPanel` is still `darkField` vs Option A |
| DSGN_REBRND-W2-S6 | OBSERVATION | ARMED (`2.0.0_SA_COO~D`) | `inversion-rule.json` composites on `#101828`, not the ratified `#0A1733` |
| DSGN_REBRND-W2-S7 | OBSERVATION | ARMED (`2.0.0_SA_COO~D`) | byte-equal token values fall below the committed floors in 8 role and ground pairs |
| DSGN_REBRND-W2-S8 | OBSERVATION | ARMED (`2.0.0_SA_COO~D`) | 3 of 5 canon hexes are below 3:1 on white; a non-colour cue is required |
| DSGN_REBRND-W2-S9 | OBSERVATION | INERT | the token file carries no non-colour tokens to be byte-equal to |
| DSGN_REBRND-W2-S10 | BLOCKING | ARMED (`2.0.0_SA_COO~D`) | RB7-AC4's builder must be a fresh worker; this worker can neither spawn one nor be one |
| DSGN_REBRND-W2-S11 | OBSERVATION | ARMED (`2.0.0_SA_COO~D`) | `/positioning`'s asset-class legend is reversed against the token file |

## Owed by others (the second actors)

- **RB7-AC4:** a fresh builder seated by `2.0.0_SA_COO~D` on `rb7-ac4-build-kit.md`.
- **RB7-AC5:** the `/positioning` author's per-clause word in the table at the end of
  `rb7-ac5-rejection-positioning.md`.
- **Integrator:** the `portal` gitlink bump at the drain.
