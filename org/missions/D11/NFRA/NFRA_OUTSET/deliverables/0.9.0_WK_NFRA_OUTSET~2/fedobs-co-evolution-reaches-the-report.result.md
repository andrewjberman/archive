# TO-OS-s-14 result -- comp-fedobs's co-evolution signal reaches the report's plumbing, and its 35,752 rows do not survive the producer

**TO:** `NFRA_OUTSET.TO-OS-s-14` (`.../task-orders/NFRA_OUTSET.TO-OS-s-14.fedobs-co-evolution-reaches-the-report.md` @`7771968abd`)
**Cell:** `OS-s-14` - **outcome_ref:** FWD-6, FWD-3 - **verb:** wire - **depends_on:** OS-s-10, OS-s-13
**Executed by:** `0.9.0_WK_NFRA_OUTSET~2` in worktree `C:/tmp/wk-OUTSET-2`, branch `wk-OUTSET-2`, base HEAD `7771968abd`

> **HEADLINE: the wire is built and exercised, and pushing the REAL signal through it found a defect that four batteries and four orders could not see.** `outset_seam.run_and_build` extracts rows with a hand-enumerated key roster -- `doc.get("paths") or doc.get("rows") or doc.get("uncommitted")` -- and comp-fedobs nests its data one level down at `signals.coevolution.rows`, **row_count 35752**. The artifact publishes `rc=0`, `answer_state=OK`, correct vintage, correct denominators, a correct re-run recipe -- and **zero rows**, which the report renders as *"zero rows -- this is a RESULT, the instrument ran and found nothing"*. Nothing is broken. The answer is simply empty when it should not be. Row `NFRA_OUTSET-W2-S21`.

---

## 0. FIRST ACT: `W2-S19`, WHICH I WROTE FOR THIS ORDER

The face carries my own row telling this assignee to run both pre-existing batteries first. I did,
before any edit: `16/16`, `12/12`, `12/12`. Then my edits broke **two** anchors, loudly:

```
test_os9_cochange_source.py   AssertionError: seam-branch anchor not unique
test_os10_seam.py             AssertionError: mutation anchor count != 1: 0
```

Both re-pointed in-grant with the mutants' **intent unchanged**. But `W2-S19` said **two** batteries
anchor into this file; the population is **three** -- I had enumerated the ones *I* wrote and
presented it as a census of the file. Corrected in `W2-S23`. The operational advice was right and
is what made the omission cheap.

## 1. WHAT I MEASURED -- both halves of the cell premise HOLD

| premise | measured |
|---|---|
| "served vintage is fresh daily" | `computed_at = 2026-09-05T04:30:38Z`, **7.3 h old** at time of run, `marker_head=f437d60b3c65`, `cse_log_total=89494` |
| "the producer rule is ENABLED" | the served artifact exists and is current; `comp-fedobs coevolution` returns rc 0 with 16 rendered pairs |
| "the reader is read by nothing" | confirmed -- no consumer existed; the served surface is `s3://opal-313476888478-globgrph/...`, and the estate-report-runner role has **nothing on the globgrph bucket** (`W1-S19`) |

## 2. WHAT I BUILT -- `estate_report_runner.py` only

| Change | What |
|---|---|
| `OUTSET_FEDOBS_KEY` | `comp_fedobs_coevolution.json`, beside the other seam keys |
| `OUTSET_GROUP_B_SOURCES` | a **declared precedence**, ordered by how well each source answers GROUP B's question: `comp_cochange.json` (resource grain -- B's question exactly), then `comp_fedobs_coevolution.json` (file-pair grain -- a real tool answer to a neighbouring question) |
| the grain declaration | when the fedobs source is used, the vintage reads `[grain=file-pair, NOT resource-grain]` and the denominator carries a GRAIN DECLARATION. **The grain switch is never silent** -- the defect `W2-S14` warned about |
| `absent` as a **field** | `_outset_read` now returns `absent=True/False` structurally, so a caller choosing between sources never greps the error prose |
| **only ABSENCE advances the search** | a present-but-broken publish is **never masked** by a healthy lower-precedence one |
| all-absent under a configured prefix | reads **FAILED** in the established `ABSENT` vocabulary -- never a quiet fall-back to the host number |

**Production is byte-unchanged**: `ESTATE_OUTSET_SEAM_PREFIX` stays unset, so every production run
still takes the host stand-in, still declaring itself.

## 3. ACCEPTANCE

### O14-AC1 -- PASS by output

`timeout 120 python .tools/tests/test_os14_fedobs_reaches.py` - **rc 0**

```
=== test_os14_fedobs_reaches: PASS (11/11) ===
```
Second grain: `python -m pytest -q` -> `1 passed in 1.16s`.

| arm | result |
|---|---|
| A1-A3 | the signal REACHES GROUP B; the stratum DECLARES the grain; the row is TRACEABLE to comp-fedobs (`rail-reproducible`, OS-s-11's contract holding on a new source) |
| **B RED MUTANT** | the criterion's named mutant -- the seam **severed** at the definition of `OUTSET_GROUP_B_SOURCES` -> `sentinel_present=False` |
| C1/C2 | with both published the resource-grain source wins, and no grain declaration is attached when none is needed |
| **D1/D2** | a **broken** (unreadable) and a **stale** higher-precedence publish are each **not masked** by a healthy lower one |
| **D3 RED MUTANT** | letting *any* failure advance the search **masks** the broken publish -> `status=OK` with the fedobs sentinel. D1 can fail |
| E | every source ABSENT under a configured prefix -> FAILED, never the host number |
| F | with no prefix, the host stand-in still runs and still declares itself |

**Regressions, all rc 0:** `test_os9_cochange_source.py` 16/16, `test_os10_seam.py` 12/12,
`test_os11_traceability.py` 12/12.

The battery is **offline by design**. The live comp-fedobs read belongs to AC2: a network arm would
let AC1 go red for a reason that is not the wire.

### O14-AC2 -- JUDGMENT (`judgment="true"`) -- EVIDENCE ONLY, NO VERDICT

The criterion says: show the signal in the report, **or** state the reason it does not belong --
silence is not a close. **The answer is both, and the second half is the finding.**

**IT BELONGS, AND THE WIRE WORKS.** The REAL producer half (`outset_seam.run_and_build`, imported
read-only) was pointed at a LIVE comp-fedobs run, published through `publish_artifact`, and read by
the REAL runner:

```
== 1. the PRODUCER half builds an artifact from a LIVE comp-fedobs run ==
   tool='comp-fedobs coevolution'  rc=0  answer_state=OK  rows=0
   vintage.answer_produced_utc=2026-09-05T11:46:51Z
== 2. PUBLISHED through the seam ==   published=True bytes=1306 error=None
== 3. the RUNNER reads it as GROUP B and RENDERS it ==
stratum: B_relationships
question: ARE OUR RELATIONSHIPS WHAT WE THINK? (which resources change together, trailing window)
vintage: comp-fedobs coevolution produced 2026-09-05T11:46:51Z ... [grain=file-pair, NOT resource-grain]
denominator: comp-fedobs coevolution -- tool_scalars.marker_head=f437d60b3c65..., source_table=iceberg.globgrph.cse
reproduce: tool=comp-fedobs coevolution  claim=rail-reproducible
           $ <python> .tools/comp-fedobs coevolution --json
rows: 0
  (zero rows -- this is a RESULT, the instrument ran and found nothing)
```

**AND THAT LAST LINE IS A LIE THE SEAM CANNOT DETECT.** The tool's own JSON carries:

```
signals.coevolution.rows        list of 35752
signals.coevolution.row_count   35752
signals.coevolution.columns     ['subject_a','subject_b','co_sessions','producers','sessions']
doc.get('paths') / doc.get('rows') / doc.get('uncommitted')   ->  None / None / None
=> extracted rows: 0
```

`outset_seam.run_and_build` uses `rows=doc.get("paths") or doc.get("rows") or doc.get("uncommitted") or []`
-- a hand-enumerated roster covering exactly the two comp-heat producers that existed when it was
written. **35,752 rows become a confident zero, and every honesty control in the seam passes.**

**Why no consumer-side guard is proposed** -- I tested the obvious one rather than assuming: "a
non-trivial denominator beside zero rows is suspicious" would fire on `comp-heat drift`, whose
legitimate answer on a clean tree *is* zero rows beside a real denominator. A remedy that cannot
tell a true zero from this one is not a remedy. **The fix belongs in the extractor.**

**Why I did not fix it:** `org/modules/heatmap/outset_seam.py` is not in my `<paths>` (`W2-S15`).
And `.tools/comp-fedobs`, which **is** granted, is the wrong place -- its `--json` is documented as
*"raw served JSON"* and NFRA_MOTIF and NFRA_PROMOTE consume the same served artifact, so reshaping
it for one consumer moves a contract three readers share.

**The reason the signal does not reach the report today, stated plainly:** three independent
blockers, none of them in this grant -- no producer registered in `SEAM_PRODUCERS` (`W2-S15`); no
IAM grant on any seam prefix, and comp-fedobs's own served surface is on the **globgrph** bucket the
runner explicitly has nothing on (`W1-S19`); and, if both were fixed today, the rows would still
arrive empty (`W2-S21`).

## 4. GATES

| Gate | Result |
|---|---|
| `bash .tools/commit-gate.sh` (4 files) | `OK: pre-commit gate clean for 4 of 4 file(s)`, rc 0 |
| non-ASCII introduced | **0** -- one glyph slipped into a runner comment and was caught by my own check and removed before commit |
| `comp-system --gate --changed` (both arms) | `NOT_APPLICABLE ... gate open`, rc 0 on both, so the granted `06_current_state` pair is correctly untouched |

## 5. ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `W2-S21` | OBSERVATION / **ARMED** | the seam drops 35,752 rows and publishes a healthy artifact; the report renders a confident zero |
| `W2-S22` | OBSERVATION / **ARMED** | all four seam fixtures are shaped like the two comp-heat producers, so the roster's uncovered member was unreachable by any test |
| `W2-S23` | OBSERVATION / INERT | **corrects my own `W2-S19`**: three batteries anchor into the runner, not two |
| `W2-S24` | OBSERVATION / **ARMED** | comp-fedobs accepts no `--budget`; the seam's bound is on the call, not a budget the tool honours, so a cut run reports nothing |

## 6. DECLARED NON-APPLICATIONS

- **`outset_seam.py` not edited** -- outside `<paths>`; the extractor fix and its fixture belong together, in one commit, with whoever holds it. `W2-S21`, `W2-S22`.
- **`.tools/comp-fedobs` not edited** although granted -- neither to reshape its JSON (a contract three readers share) nor to add `--budget` (Rule T is another family's work, and a flag that bounds nothing real is a carrier that lies). `W2-S24`.
- **No fixture arm asserting the current defective behaviour** -- it would enshrine the defect and break when fixed; an arm asserting the correct behaviour would make AC1 fail on a defect this cell does not own.
- **No default for `ESTATE_OUTSET_SEAM_PREFIX`**; no IAM change; no monitor, alarm or freshness-checker; no delete verb; no new dependency.
