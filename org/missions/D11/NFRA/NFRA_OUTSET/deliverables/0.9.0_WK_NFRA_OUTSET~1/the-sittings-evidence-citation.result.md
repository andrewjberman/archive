# NFRA_OUTSET.TO-OS-s-17 -- RESULT: the tool-row citation, inspected and then built

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (L7 worker subagent of `2.0.0_SA_COO`, spine v3)
**Branch:** `wk-OUTSET-1` (linked worktree `C:\tmp\wk-OUTSET-1`) · **Base:** `ed5c4e2b5b`
**Cell:** `OS-s-17` · **outcome_ref:** FWD-4 · **verb:** build · **depends_on:** `OS-s-11`, `OS-s-12`

This cell ran in two phases. **Phase 1 was an inspection under a grant with no repo surface**, and
it ended in a BLOCKING row (`W1-S24`) because a `build` verb had nothing to build on. The issuer
accepted that as its own cut defect and amended `<paths>` at `ed5c4e2b5b`. **Phase 2 is the build.**
Both are recorded here; the phase-1 census is not re-run and is not reopened.

---

## 0. THE HEADLINE, IN TWO SENTENCES THAT MUST BE READ TOGETHER

**The producer now requires a proposal to cite the tool row behind it, and refuses it separately if
it does not.** **No published day carries that yet and none will until a deploy nobody has
authorised** — so a green criterion here is not a live effect, and `NFRA_OUTSET-W1-S26` exists so
that cannot be misread.

## 1. PHASE 1 -- WHAT A DAY'S PROPOSALS ACTUALLY CARRIED (recorded, not re-run)

7 consecutive published days, **61 proposals, 61 of 61 carrying a non-empty `evidence_cited`, 0
discarded — and 0 of 61 citing a tool row at `path@vintage`**, 0 naming any comp-tool, 0 naming any
`.json` artifact key. The zeros are absences, not dead reads: the same detector family returns
**2 of 61** on a bare `@<hex>` (on 2026-09-04 the literal `@351f309e`), and a negative control
returns 0. Full census and controls in `NFRA_OUTSET-W1-S24`.

**And the mechanism the manifest credits is real — it answers a different question.**
`evidence_resolves()` passes if a known ruling id appears, or if any distinctive token of **the
`evidence_ref` this runner itself put in the prompt** survives into the citation. Its docstring
records the 2026-08-06 repair that made it a real control after a prefix match passed 7 of 7 live
calls including a planted fabrication. It establishes that the model quoted what it was shown. It
cannot establish that what it was shown came from a named tool at a named vintage — **a verifier
scoped by the same set as the act.** That is the gap this cell closes.

## 2. PHASE 2 -- WHAT WAS BUILT

All in `infra/aws/ec2/estate-report-runner/estate_report_runner.py`:

- **`tool_row_ref(stratum)`** — mints `<stratum>@<vintage>` from the stratum's own `OS-s-11`
  `reproduce` recipe, and returns `None` when there is no recipe. An untraceable stratum has no row
  to cite, and that must read as *"there is none"* rather than as an empty string a citation could
  trivially match.
- **`tool_row_resolves(cited, stratum)`** — requires the stratum **name AND the vintage** in the
  citation. **An AND, not an OR, and that is the load-bearing choice:** the name is guessable from
  the prompt's own headings and the vintage is shared by every stratum of the day, so either alone
  would resolve to a *region* rather than to a *row*.
- **`citation_verdict(parsed, cand, strata, nugget_ids) -> (ok, code, reason)`** — the whole
  decision as one named thing. **The order is the contract:** the anti-fabrication gate runs first
  and unchanged; the tool-row gate runs after it with its own code. A proposal failing both is
  reported against the first, because *"you did not cite what you were shown"* is the more serious
  finding and collapsing the two would hide it.
- **The author prompt** shows the row and demands `tool_row_cited` back, stating that the two
  obligations are discarded separately.
- **An accepted proposal carries `tool_row_cited` *and* the full `tool_row` recipe**, so a reader of
  the artifact can re-run what the proposal rests on without leaving the document.

### 2.1 The constraint I was given, and how it is held rather than asserted

**`evidence_resolves()` is byte-unchanged.** The tool-row requirement sits *beside* it, never in
place of it. And the assertion that it still fires is itself a live control: **arm F** restores the
2026-08-06 defect in a temporary copy, and under that mutant the same fabricated citation is
**accepted**. **Arm G** removes the tool-row gate and the same `'nonsense'` citation is **accepted**.
A control nobody has watched fail is a promise.

### 2.2 One refactor, named because it changed a shape

The citation decision was **inline** in the author loop, so the only way to check which gate refused
first was to read the source and believe it. It is now `citation_verdict()`, exercised directly by
every arm with **no model call anywhere**. The loop's behaviour is unchanged; what changed is that it
can be watched.

## 3. ACCEPTANCE

### O17-AC1 -- JUDGMENT (`judgment="true"`) -- RECORDED, NO VERDICT

```
[PASS] A-REAL-STRATUM-YIELDS-A-CITABLE-TOOL-ROW -- runner-produced stratum -> 'A_propagation@n/a (host-limited) @PIN9' (its recipe honestly names tool='none', the 'nothing ran' shape) ; a rail-reproducible row -> 'B_relationships@git history @351f309e' naming tool='comp-heat drift' ; both resolve against their own stratum
[PASS] B-TOOL-ROW-CITATION-IS-AN-AND-NOT-AN-OR -- exact citation accepted; refused: {'name only': True, 'vintage only': True, 'empty': True, 'wrong stratum': True, 'unrelated prose': True}
[PASS] C-A-STRATUM-WITH-NO-RECIPE-FAILS-CLOSED -- tool_row_ref(no recipe) = None ; verdict = (False, 'TOOL_ROW_ABSENT')
[PASS] D-ANTI-FABRICATION-LIMB-STILL-FIRES -- a fabricated evidence_cited is refused as CITATION_UNRESOLVED even WITH a perfect tool row; an honest one passes both gates -> (True, 'OK')
[PASS] E-GATES-ARE-IN-SERIES-AND-THE-FIRST-ONE-WINS -- both-bad -> CITATION_UNRESOLVED ; only-tool-row-bad -> TOOL_ROW_UNRESOLVED ; distinct reasons=True
[PASS] F-RED-MUTANT-1-WEAKENED-ANTI-FABRICATION-IS-CAUGHT -- under the mutant a FABRICATED evidence_cited is ACCEPTED (OK) while production refuses the identical input (CITATION_UNRESOLVED)
[PASS] G-RED-MUTANT-2-REMOVED-TOOL-ROW-GATE-IS-CAUGHT -- under the mutant a proposal citing 'nonsense' as its tool row is ACCEPTED (OK) while production refuses the identical input (TOOL_ROW_UNRESOLVED)
[PASS] H-MUTATION-ANCHORS-UNIQUE
[PASS] I-AUTHOR-PROMPT-SHOWS-THE-TOOL-ROW-AND-REQUIRES-IT
[PASS] J-AN-ACCEPTED-PROPOSAL-CAN-CARRY-ITS-ROW
OS17-TOOL-ROW BATTERY: 10/10 PASS (denominator 10; 0 model calls, 0 AWS, 0 network)
```
rc=0, stable across 2 direct runs; pytest `1 passed in 0.47s`.

**Denominator:** 10 of 10 arms; 2 RED mutants, both fired; 5 refusal shapes checked on the AND;
61 of 61 proposals in the phase-1 census across 7 of 33 published days, with 1 positive and 1
negative control.

**WHAT THIS DOES NOT SHOW.** It does not show a published day whose proposals cite tool rows, and it
cannot. The served producer is `s3://opal-estate-report/code/estate_report_runner.py`, **125,857 B
dated 2026-08-25**; the box runs whatever bytes sit there. **No deploy is authorised and no cell of
the 17 owns one.** The next published day will look exactly like the seven censused in phase 1.

**No verdict is written here or in the proof-of-spec instance.** `3.0.0_SA_CVO` grades it at L9.

## 4. REGRESSION + GATES

| check | result |
|---|---|
| `python .tools/tests/test_os17_tool_row.py` | `10/10 PASS`, rc=0 (x2) |
| `python -m pytest -q .tools/tests/test_os17_tool_row.py` | `1 passed in 0.47s`, rc=0 |
| `test_os9_cochange_source.py` | `PASS (16/16)`, rc=0 |
| `test_os10_seam.py` | `12/12 PASS`, rc=0 |
| `test_os11_traceability.py` | `PASS (12/12)`, rc=0 |
| `test_os14_fedobs_reaches.py` | `PASS (11/11)`, rc=0 |
| `bash .tools/commit-gate.sh` on the 2 touched files | `OK: pre-commit gate clean for 2 of 2 file(s)`, rc=0 |

This cell edits a file that four drained cells own, so the whole set was re-run rather than the one
battery I wrote. The gate's non-ASCII WARN names 3 lines that are **unchanged from HEAD** (3 at HEAD,
3 in the worktree) and are not mine.

## 5. A CORRECTION TO MY OWN EARLIER ROW -- `NFRA_OUTSET-W1-S27`

`W1-S25` offered four tokens as evidence that the served producer predates this project's work. **Two
of them — `rerun_recipe` and `tool_invocation` — are zero at HEAD as well**, so their zero measured
my own spelling rather than the artifact. I re-derived the set rather than taking the correction on
the issuer's word:

| token | HEAD | served | discriminates? |
|---|---|---|---|
| `_outset_read` | 4 | 0 | yes |
| `OUTSET_ANSWER_STATE_TO_STATUS` | 3 | 0 | yes |
| `reproduce` | 18 | 1 | yes |
| `render_trace` | 2 | 0 | yes |
| `rerun_recipe` | 0 | 0 | **no** |
| `tool_invocation` | 0 | 0 | **no** |
| `_stratum(` | 16 | 11 | positive control — same program, older vintage |

The conclusion is unchanged and now rests on the four that separate the two. **The general form,
since it has bitten me twice in this project: every token in a presence/absence census needs its own
positive control — a census of four tokens is four detectors, not one.**

## 6. ROWS FILED

| row | class | standing |
|---|---|---|
| `W1-S24` | **BLOCKING** | phase 1 — a `build` cell with no write surface. **Resolved by the issuer's amendment at `ed5c4e2b5b`.** |
| `W1-S25` | OBSERVATION | ARMED — committed ≠ served by 11 days |
| `W1-S26` | OBSERVATION | ARMED — the build cannot reach a published day; a green criterion is not a live effect |
| `W1-S27` | OBSERVATION | INERT — corrects `W1-S25`'s instrument, re-derived |

## 7. WHAT I DID NOT DO

- **I did not weaken `evidence_resolves()`.** It is byte-unchanged, runs first, and two mutants
  prove both claims.
- **I did not deploy anything**, and I am not proposing a mid-round deploy.
- **I made no AWS write of any kind.** The only AWS calls in this cell were phase 1's read-only ones.
- **I wrote no verdict** on a judgment criterion.

## 8. PUSH STATE

**LOCAL.** Nothing pushed. Measured with `git ls-remote` at report time — see the WORKER REPORT.
