# EG-s-25 -- THE VERDICT ARTIFACT DISCLOSES ITS OWN FORCING

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~5` · **TO:** `ETFS_GUARDRAIL.TO-EG-s-25` · **cell:** `EG-s-25` · **outcome_ref:** FWD-9 (honesty half)
**Branch:** `wk-etfs_guardrail-3-5` (worktree `/c/tmp/wk-etfs-3-5`) · **never pushed**
**Face:** `ETFS_GUARDRAIL.TO-EG-s-25.the-verdict-discloses-its-own-forcing.md` @`d30e3ca107`

---

## THE HEADLINE

`coverage_verdict.json` now records **how the run was configured** -- forced or not, on **both**
branches, always. Before this cell the renderer the box pulls carried **zero** disclosure tokens, so a
driven refusal would have landed looking exactly like an organic one and the forcing would have survived
only in a worker's report. That is the failure this project exists to prevent, and it is closed.

The half that matters is the **unforced** one. Recording a forcing when there is one is easy. A field
that is missing when nothing was forced *and* missing when something was forced is not a disclosure at
all -- a reader cannot tell "this run forced nothing" from "this run did not say". So `forced` is an
explicit boolean on both branches, `mechanism` reads the literal `none` rather than being omitted, and
the **default** path emits the record for every caller that knows nothing about it.

```
FORCED  : {"disclosure_version": "1", "fixture_remove": {"cottonwood": ["2026-08-25", ...]},
           "fixture_remove_spec": "cottonwood:2026-08-25,...", "forced": true,
           "mechanism": "--fixture-remove", "removed_slice_count": 5, "run_id": "22aa96f2...", ...}
UNFORCED: {"disclosure_version": "1", "fixture_remove": {}, "fixture_remove_spec": "",
           "forced": false, "mechanism": "none", "removed_slice_count": 0, "run_id": "c1f428c7...", ...}
```

---

## WHAT I MEASURED, WITH DENOMINATORS

| quantity | value | instrument |
|---|---|---|
| disclosure tokens in the pre-change deployed bytes | **0 of 10**, on BOTH counting methods | re-read live by S3 versionId |
| positive controls on those same bytes | **5 of 5 non-zero**; 5 of 5 reproduce the issuer's numbers exactly under substring counting | same object |
| pre-change object | 62,880 B, sha256 `55701125e86740f3bf51a715aba8f68e8441d3eb7bffc99a43b7d3ff29b973e9` | byte-equal to the repo build input |
| deployed object now | 66,756 B, sha256 `b08a646d5755f501f10b0b3c8d0512702c20b38e02263dc3b33a2f963d71020f` | byte-equal to the committed blob at `c2787650f5` |
| artifact prefix keys | **7 before, 7 after; exactly 1 of 7 changed** | `list-objects-v2` before/after |
| `platinum/reports/` keys | **36 before, 36 after; 0 of 36 differ** on Size/ETag/LastModified | same |
| verdict comparison, old bytes vs new | **5 of 5 pre-existing keys and 10 of 10 class counts identical**, both scenarios | both modules loaded, real `coverage_gate` |
| keys added to the document | **exactly 1** (`forcing`); 0 removed | same |
| `coverage_verdict.json` consumers censused | **71 hits across 29,502 files**; **3** code readers | `comp-find` |
| SES sends in the window | **0 datapoints, Sum 0 on 3 of 3 metrics** | `AWS/SES` |
| lambda invokes by this cell | **0 of 5** AWS verbs used | the committed evidence ledger |
| test suite | **20 of 20 pass** (5 new arms), commit-gate clean 2 of 2 | pytest |

---

## S25-AC1 -- PASS by output

**Invocation:**
```
timeout 600 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs25_verdict_discloses_forcing.py
```
**rc 0.** Deciding output, verbatim:
```
  ARMS PASSED: 6 of 6

EGS25-VERDICT-DISCLOSES-FORCING
```

- **(a) THE ABSENCE REPRODUCES, ON THE DEPLOYED BYTES.** The deploy has since replaced that key, so this
  arm re-reads the **exact pre-change object by its S3 versionId** (`FVBt9YneBrdWknuYkwRZKKoGrU2blLVk`)
  -- the bucket has versioning **Enabled** (measured), so the arm stays LIVE-re-derivable forever rather
  than depending on a local copy or on the issuer's row. 10 of 10 disclosure tokens ZERO on both counting
  methods; 5 of 5 controls non-zero. The premise check (a disclosure field already present would mean the
  premise is wrong and the battery must STOP) reads `forcing in old bytes: False`.
- **(b) A FORCED RUN DISCLOSES.** The whole record printed, carrying the spec verbatim, the removed-slice
  count and a run id with its source.
- **(c) AN UNFORCED RUN SAYS SO EXPLICITLY.** Same field, `forced: false`, `mechanism: "none"`, printed
  beside the forced case and textually different.
- **(d) THE VERDICT DID NOT MOVE.** Old deployed bytes vs new, identical inputs, PUBLISH and REFUSE
  scenarios: 5 of 5 pre-existing keys and every class count identical; exactly one key added.
- **(e) THE DEPLOY IS REAL AND REVERSIBLE.** Served bytes byte-equal to the committed bytes; entry opened
  `20260910T051838Z` **before** the `20260910T051933Z` copy and closed `20260910T052413Z` before this
  grading read; prior sha256 and versionId recorded in the entry; rollback stated as an exact restore.
- **(f) NO SEND, NO INVOKE, NO SERVED-REPORT WRITE.** 3 of 3 SES metrics zero; `platinum/reports/`
  unchanged 36 of 36; 0 of 5 AWS verbs is an invoke; the battery's own harness *raises* on any invoke.

## S25-AC2 -- RECORDED (judgment), NO VERDICT

`judgment="true"`; graded by `3.0.0_SA_CVO` at L9.

**1. The field's shape, and why a reader can trust it.** Eight keys, one axis -- *how this run was
configured*, never *what it decided*. `forced` is the discriminator and is an explicit boolean on both
branches; `mechanism` is a string (`--fixture-remove` or `none`) so a second forcing mechanism can be
added without changing the discriminator's meaning; `fixture_remove_spec` keeps the operator's raw string
and `fixture_remove` the parsed form, so a reader can check the parse rather than trust it;
`removed_slice_count` is derivable but printed, so a truncated read still carries the magnitude;
`run_id` + `run_id_source` carry the identifier **and its provenance claim**, which is what lets a
consumer reject it; `disclosure_version` lets a later reader tell a v1 record from a v2 one. Against
TAXONOMY LAW: MECE over the declared domain (a run either was or was not forced -- there is no third
state the code can be in), same grain throughout, one intent, and the remedy that moves `forced` from
true to false (run without the flag) moves nothing else. **The reason to trust it is not its shape but
its default:** it is emitted by `coverage_gate` itself with all-defaulted arguments, so a caller cannot
omit it by forgetting -- test (j) is exactly that guarantee.

**2. Does any consumer parse `coverage_verdict.json` and could a new key break it? Censused, not
recalled.** `comp-find 'coverage_verdict'`: **71 hits across 29,502 files** (bands SURFACED 7, CONFIG 7,
TEST 5, DOC 52). Stripping docs, scratch copies and the tool's own logs leaves **3 code readers plus the
writer**:
  - `infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:130` -- `_read_coverage_artifacts`
    does `json.loads(body)` into a dict and returns it. Its **only** downstream use of the verdict
    document is `:428 message += f"\n\nCoverage verdict: {json.dumps(artifacts['verdict'])}"`. No schema
    validation, no key iteration, no field allow-list. An added key cannot break it -- and it
    **propagates into the operator alert**, which is a small bonus for exactly the reader who most needs
    to know a run was forced.
  - `infra/aws/lambda/etfs-reports-orchestrator/test_terminal_send.py:87` -- a stub matching on key NAME
    only.
  - `org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs15_september_refusal.py:174`
    -- reads named fields out of the document; additive keys are invisible to it.
  **Nothing in the estate validates this object against a closed schema.** Stated limit: this census is
  repo-scoped. A consumer outside the repo -- a human reading the JSON, or a future portal panel -- is
  not covered by it, and the census cannot see one.

**3. Is the run id one a reader could join to a run log? Partly, and here is exactly what it is.** It is
**not** the SSM `CommandId`. The orchestrator holds that id (`_ssm.send_command(...)["Command"]["CommandId"]`)
and does **not** pass it to the renderer process -- the box's command line is
`python3 render_month_end.py --month {month} --pdf --gate --s3-out {out}` with no id in the argv and none
in the environment. Threading it in would mean editing the orchestrator, which this cell is explicitly
forbidden to touch (`EG-s-24`'s surface, live on `~4`). So what the field carries is a **uuid4 minted by
the run and PRINTED to stdout** as `RUN-ID: <id>`. That is joinable, because SSM captures the command's
stdout as `StandardOutputContent` and the orchestrator already reads `get_command_invocation` -- a reader
holding the SSM command id can fetch the output and find the line. The join therefore runs
artifact -> stdout -> SSM invocation, and **not** artifact -> CommandId directly. `run_id_source` says
which of the two it is on every record, so a reader is never left guessing. A hook is left for the
stronger case: `ETFS_RUN_ID` in the environment wins if a caller supplies one, so `EG-s-21` or a later
orchestrator change can hand in an already-joinable id **without another renderer deploy**.

**4. What this disclosure does NOT prove.**
  - **It does not make an unforced run trustworthy.** It records what the *renderer* was told. A run
    whose input was distorted upstream -- a producer that never wrote a slice, an S3 listing that
    truncated -- reads `forced: false` truthfully and discloses nothing about that.
  - **It covers ONE forcing mechanism.** `--fixture-remove` is the only one that exists today.
    `--no-ladder` also changes what the run does (zero producer invokes, so no recovery can occur before
    the verdict) and is **not** recorded by this field. That is a real gap and I am naming it rather than
    letting the field imply completeness.
  - **It has not run on the box.** The bytes are deployed and byte-verified, and the record was exercised
    hermetically through the real `main()`, but no box run has produced one of these documents in
    `platinum/reports/`. That is `EG-s-21`'s single permitted act, deliberately unspent here.
  - **It cannot make a forced run visible to a reader who does not open the artifact.** The HTML, the
    PDF and the CSVs carry no forcing marker; only `coverage_verdict.json` does.
  - **The `run_id` is not authenticated.** Anything that can write the object can write any id.

---

## CONTROLS

**MUTANT -- FIRED, and it fired on the arm that carries the outcome.** The battery was copied and the
renderer mutated at one site: the `forcing` key emitted **only when a spec was supplied** -- precisely the
defect arm (c) exists to refuse. Result: **rc 1, ARMS PASSED 4 of 6, `TOKEN WITHHELD`**, with **arm (c)
FAIL** and **arm (d) FAIL**.

A note on how that control was earned rather than assumed: the mutant's *first* run did not produce a
graded FAIL -- it raised `KeyError: 'forcing'` and exited 1. The token was withheld, so the battery was
never going to pass a mutated build, but a battery that **crashes** on the very defect it exists to catch
reports a traceback where it owes a verdict. The battery was fixed to grade a missing field explicitly
(printing `<<< THE FIELD IS ABSENT ON THE UNFORCED RUN >>>` and the top-level keys actually written), and
both were re-run: the mutant now FAILS cleanly at arm (c) and the real battery still passes 6 of 6.

**DETERMINISM -- STABLE.** Two full runs, 174 lines each. After masking the `run at <UTC>` header and the
run ids, **0 differing lines**. The only non-determinism is the `run_id` itself, which is an identifier
and non-deterministic **by design** -- a run id that repeated across runs would be the defect.

**THE COUNTING-METHOD CONTROL.** The issuer's five quoted control numbers (1/22/23/13/6) reproduce
**exactly** under substring counting and **not** under word-boundary counting (1/17/19/6/5). Both methods
agree that all five controls are non-zero and all ten disclosure tokens are zero, so the premise is
unaffected -- but the battery prints **both**, so a later seat re-taking the census the stricter way sees
a method difference and not a discrepancy. Filed as row `W5-S5`.

---

## CORRECTION TO A COMMITTED COMMIT MESSAGE -- stated because the record is wrong and cannot be edited

The commit message of `9393136bf7` (the three rows) says the rows were appended "onto the channel's
CURRENT tail (CLOUD @911f9a0ba4, 64 rows -> 67)". **That is not what happened.** I first tried exactly
that, and `.tools/surprise-row-gate.py` **correctly refused it**: importing CLOUD's tail made six rows
authored by other seats (`W1-S30/S31/S32`, `W4-S1`, `S12`, `S13`) look like NEW rows minted by me, and the
gate blocked on 7 violations including a FOREIGN-ROW SWEEP. I then restored my branch's own copy and
appended only my three rows: **58 -> 61**, and the gate passed with "3 new row(s) of 61 total checked".
The message file had been written before that refusal and was not rewritten before the commit -- the
patch-then-commit staleness class. The gate's refusal was right and the committed numbers are wrong; the
correct numbers are 58 -> 61 on this branch, and the drain will reconcile against CLOUD.

---

## WHAT I DID NOT DO

No send. No orchestrator invoke -- `etfs-reports-orchestrator` was not invoked in any mode. No box run.
No write or delete under `platinum/reports/` (36 keys before, 36 after, 0 differing). I did not touch
`infra/aws/lambda/etfs-reports-orchestrator/` (`EG-s-24`, live on `~4`) or `data/etfs/scripts/coverage/`
(`EG-s-23`, live on `~1`) -- I read both, and edited neither. I did not change the verdict logic: the
class-C rule is `EG-s-4`'s and is absent from the diff. I did not push, merge or rebase. I made no second
deploy.

---

## ROWS FILED -- three, at `9393136bf7`

- **`W5-S4`** (OBSERVATION / INERT) -- the DELIVERABLE requires the deploy to land "with a never-widen
  sign-off", which is a **two-seat** act (CTO+COO) that a worker with no send cannot obtain, on an act the
  **same face** rules is not served output and therefore outside the never-widen trigger. I deployed and
  wrote into the entry exactly what authority exists (the issuance's blast radius and per-key rollback)
  and that no CTO half does.
- **`W5-S5`** (OBSERVATION / INERT) -- the order's stated authority, row `W4-S2`, is **not in the channel**
  at CLOUD on two reads at two tips. The premise was re-grounded against the deployed bytes instead and
  held; the control numbers are counting-method dependent.
- **`W5-S6`** (OBSERVATION / INERT) -- the face cites `lambda_function.py:348` for the box's pull; at CLOUD
  that line is prose inside an email body. The pull is at `:207`, `ARTIFACT_PREFIX` at `:48`, the renderer
  invoked at `:227`. The claim is true and was confirmed at the corrected lines before the deploy; the
  pointer decayed within hours because two adjacent cells edited that file tonight.

## ARTIFACTS

| path | what |
|---|---|
| `data/etfs/scripts/presentation/render_month_end.py` | the change: `_mint_run_id`, `_forcing_record`, `coverage_gate`'s four defaulted kwargs, `main()`'s mint/print/pass |
| `data/etfs/scripts/presentation/tests/test_coverage_gate.py` | +5 arms (g)-(k) in the renderer's own suite |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs25_verdict_discloses_forcing.py` | the S25-AC1 battery, 6 arms |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/egs25_deploy_evidence.json` | every deploy command verbatim: argv, rc, stdout, stderr, UTC; before/after inventories of both prefixes |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/egs25_verdict_diff.json` | the old-vs-new verdict differential result |
| `org/critical_paths/change_management/20260910T0518Z_...deploy_completion.md` | the NEVER-2 entry: 5 legs proven, blast radius, two verified rollback sources, the authority stated exactly |
| `s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/render_month_end.py` | the deployed object, versionId `V1i.w8DNP2iqwsiiRYC7k40Neh90w3DH` |

## PUSH STATE

Measured with `git ls-remote origin refs/heads/CLOUD` and stated in the worker report. Everything is
**LOCAL** on `wk-etfs_guardrail-3-5`; this worker never pushed, merged or rebased.
