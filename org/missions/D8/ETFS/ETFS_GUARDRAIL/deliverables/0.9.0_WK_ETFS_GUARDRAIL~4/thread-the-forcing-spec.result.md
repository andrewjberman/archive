# ETFS_GUARDRAIL.TO-EG-s-24 -- THE FORCING SEAM, THREADED AND DEPLOYED

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` · **Face:** hardened at `e618f3f88d` · **Branch:** `wk-etfs_guardrail-3-4`
**Outcome:** `S24-AC1` **PASS by output** (10 of 10 arms), `S24-AC2` RECORDED.
**Rows:** `W4-S3` (the two-gate bind, now cleared by the merge), `W4-S4` (my correction to `W4-S1`), `W4-S5` (the second writer).

> **NO SEND, NO ORCHESTRATOR INVOKE.** `EG-s-21`'s single permitted driven run is **unspent**.

---

## 1. UNBLOCKING FIRST -- the merge, done under the guard

`W4-S3` was right and the fix was one act: `bash .tools/safe-merge.sh CLOUD`. It conflicted on the
append-only channel exactly as the tool's own header predicts (3 of 3 on round 4's drains). I
resolved by **union from the three index stages** rather than by splicing markers: base was a strict
prefix of ours; CLOUD had additionally bumped the header denominator; so the union is CLOUD's trunk
plus my `W4-S2/S3/S4` sections. **0 duplicate ids, 0 markers left, all 8 JSON blocks parse.**
`--continue` graded the *merged* index and landed `0228b9c456`; the row gate printed **66 rows**,
matching the header I had written. The lane gate then resolved and the code commit landed unmodified.

## 2. THE SEAM

```
FORCING_KEY     = "force_fixture_remove"
FORCING_SPEC_RE = ^[a-z0-9][a-z0-9_-]{0,31}:\d{4}-\d{2}-\d{2}(,\d{4}-\d{2}-\d{2})*$
MONTH_RE        = ^\d{4}-(0[1-9]|1[0-2])$          <- the second writer's fence (s.3)
_forcing_spec(event) -> validated spec, or "" for OFF   (needs test_run AND the forcing key)
_render_command(month, forcing="")                      <- DEFAULTED; "" appends nothing
```

Forcing requires the **test marker**, which is exactly what `EG-s-20`'s forbidden-filter keys on, so
**a run that drops its own input data can never be a run whose recipients include aj@.**

## 3. CONDITION (b) FOUND A SECOND WRITER, AND MY OWN EARLIER CENSUS COULD NOT SEE IT

I had censused the **four event keys the handler reads** and called that the writer census.
Censusing the **command builder's own source** gives:

| | |
|---|---|
| DENOMINATOR | **6** inputs reaching the built command |
| parameters | `month`, `forcing` |
| module globals | `ETFS_BUCKET`, `REPORTS_PREFIX`, `ARTIFACT_PREFIX`, `REGION` |
| exclusions | those 4 are each `os.environ.get(<name>, <literal>)`, Terraform-set, and no event key maps to any -- **4 of 6 excluded** |
| **invoker-writable** | **2, not 1** |

`month` was interpolated into the same single-quoted SSM string **unvalidated**. Measured, not reasoned:

```
event {"mode":"run","month":"2026-08 --fixture-remove cottonwood:2026-08-04"}
  _forcing_spec(event) -> ''          (the purpose-built fence correctly refuses)
  '--fixture-remove' in the built command -> True
```

The same hole reached `--s3-out`, `--no-ladder`, or a quote-break out of the shell string. It
**pre-dates this cell** (it arrived with `EG-s-15`'s month override and was live in the served
function from 01:16:14Z) and it is row **`W4-S5`**. Fixed by `MONTH_RE`, enforced **inside
`_render_command`** -- the one place the string is built -- failing **loud** rather than falling back.

**A fence on one writer of a property is not a fence on the property.** That is the finding.

## 4. THE DEPLOY

| | |
|---|---|
| pre | `ag4La0jgP8JEr55FCvXx+gnR5pDqw1CpvbEHZBrBTPc=`, 03:54:09Z, 13,785 B |
| post | `rCrGrYPZNKgWQ4uX3NGFGqm7v1s+KcfQlJ7na+soz+g=`, 05:42:07Z, 16,210 B |

Entry opened **05:38:12Z**, code committed `3a326438d3` **before** the apply, targeted plan to a
saved plan file (`Plan: 0 to add, 1 to change, 0 to destroy.`, 1 of 1 resource), apply 05:41:32Z ->
05:42:12Z, entry **closed and committed** `98ef9d28dc` before the grading read. Served == built ==
predicted; member == `git show HEAD:<path>`; pre-change blob does **not** match. Re-plan rc=0
`No changes.` Halt gate passed with **no `HALT_ACK`**, printing *"worker … has no inbox; scanning
its issuer 2.0.0_SA_COO"*.

**Condition (a), verified by my own sha256 before AND after the apply:** `EG-s-25`'s renderer served
at 66,756 B / `b08a646d5755f501…` (05:19:37Z) against my pre-`EG-s-25` baseline 62,880 B /
`55701125e86740f3…` with **zero** disclosure tokens; it now carries `forced` 9, `run_id` 27.
**Disclosure existed before forcing became reachable.**

## 5. THE CRITERIA

### `S24-AC1` -- PASS by output

```
$ timeout 600 python org/.../test_egs24_forcing_seam.py
arms: 10 of 10 HOLD
EGS24-FORCING-THREADED-SCHEDULE-CLEAN     rc=0
```

(a) pre-change code: 5 of 5 shapes carry no `--fixture-remove`, token absent from its whole source ·
(b) 5 of 5 marker-free shapes build a **byte-identical** command · (c) 0 of 20 payloads reach the
flag in code, 8 of 8 month injections refused, and **on the deployed payload** the live rule sends
1 key `['mode']` with positive control `mode='run'` present while `test_run`,
`force_fixture_remove` and `month` all read absent · (d) the spec reaches `--fixture-remove`
verbatim and parses under the renderer's own `_parse_fixture_remove`, and cannot persist (0 globals,
0 env writes, 0 SSM/S3 persistence, warm-container tested) · (e) three-read equality with a negative
control, entry opened-before / closed-before · (f) 0 START RequestId in my window against **1 of 4**
in a positive-control window.
Hermetic side: `pytest infra/aws/lambda/etfs-reports-orchestrator/ -q` -> **27 passed** (20 before).

### `S24-AC2` -- RECORDED, judgment, NO VERDICT

- **The forcing key's shape, and why it cannot be confused with a scheduled field.** Two keys must
  co-occur (`test_run` + `force_fixture_remove`) and the schedule's entire deployed Input is
  `{"mode":"run"}`. It is a verb-phrase in the imperative, not a noun a scheduler emits, and it is
  matched exactly: `FORCE_FIXTURE_REMOVE`, `fixture_remove`, `--fixture-remove` and a nested
  `detail.*` copy all resolve to OFF.
- **What a caller could still do wrong.** (i) Name a partner or date that does not exist -- the
  renderer's `_apply_fixture_remove` does `daily.get(p, {}).pop(d, None)`, a silent no-op, so the run
  would PUBLISH while the operator believed it forced. That is a *disclosure* problem and it is
  precisely what `EG-s-25` now writes onto the verdict, which is why the ordering condition exists.
  (ii) Force on a month whose holes are class D, which does not refuse: the class table decides, not
  the forcing. (iii) Force a month with no served data at all and read the empty result as a refusal.
- **Other callers of `_render_command`, censused not recalled:** AST walk -> **1** call site; a pytest
  arm asserts that count *and* that `forcing` is defaulted, so an unknown future caller is unchanged.
- **What this seam does NOT make reachable:** no S3 write or delete; no change to which month
  publishes beyond the `YYYY-MM` already accepted (now *narrower* than before, since `MONTH_RE`
  rejects `current`/`last`, which the orchestrator never sent); no recipient change; no survival into
  a scheduled fire; no persistence into a later invocation; no shell metacharacter into the SSM
  command.
- **One thing I would flag to the CVO.** `MONTH_RE` is *stricter* than the renderer's own
  `_resolve_month`, which accepts `current` and `last`. The orchestrator never sent those, so nothing
  regresses -- but the two validators now disagree about what a legal month is, and a future seat
  wiring `current` through the orchestrator will meet a loud refusal rather than a silent pass. I
  judge that the right side to fail on; it is recorded so it is a choice and not a surprise.

**Vintage:** deployed orchestrator `LastModified 2026-09-10T05:42:07Z`; served renderer
`b08a646d5755f501…`; live schedule read 05:3xZ; code `@98ef9d28dc`.

## 6. WHAT I DID NOT DO

No send, no orchestrator invoke, no S3 write or delete, no override of any gate. No edit to
`data/etfs/scripts/presentation/` (`EG-s-25`, `~5`) or `data/etfs/scripts/coverage/` (`EG-s-23`,
`~1`) -- I imported the renderer's parser and read its line numbers, nothing more. The 05:08Z entry
opened before the merge was **deleted while still untracked**: no deploy ever began under it and it
never entered the record.
