# ETFS_GUARDRAIL.TO-EG-s-21 -- THE DRIVEN REFUSAL: BLOCKED AT THE CUT, NOT INVOKED

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` (L7 worker subagent of `2.0.0_SA_COO`, round 3, cell `EG-s-21`)
**Worktree:** `/c/tmp/wk-etfs-3-4` on `wk-etfs_guardrail-3-4`
**Window:** 2026-09-10 ~04:3xZ -> ~04:5xZ
**Outcome:** `S21-AC1` **FAIL**. The order stays OPEN; its `<status>` is NOT flipped.
**Row:** `ETFS_GUARDRAIL-W4-S2` -- BLOCKING / ARMED.

> **NOTHING WAS INVOKED.** No orchestrator invoke, no producer probe invoke, no SES send, no S3
> write, no S3 delete. Every AWS call this seat made is a read: `lambda:GetFunction`
> (+`Configuration`), an HTTPS GET of the presigned code location, and `s3:GetObject` on the box's
> renderer artifact and the served coverage documents. **NO CODE WAS CHANGED.**

---

## 1. THE PRECONDITION HOLDS -- measured at my own run's time, not inherited

The face makes this the one bound with no override, and requires it re-taken on the bytes deployed
at *my* run's time because "a proof taken before a later deploy is a proof about different bytes".

| | |
|---|---|
| read at | **2026-09-10T04:35:14Z** (and again inside the battery, ~04:4xZ) |
| served `CodeSha256` | `ag4La0jgP8JEr55FCvXx+gnR5pDqw1CpvbEHZBrBTPc=` |
| `LastModified` | 2026-09-10T03:54:09.000+0000 |
| zip member | `lambda_function.py`, 1 of 1, 40,790 B, sha256 `ac0484b73a26865eab649917cec7d1bf9c5d604ccd293cc72f17cb83e9e17000` |
| deployed constants | `TEST_MARKER='test_run'`, `TEST_FORBIDDEN_RECIPIENTS=['aj@opalinvest.com']`, `TEST_DEFAULT_RECIPIENTS=['andrew@opalinvest.com']` |

**aj@opalinvest.com appears in 0 of 18 resolved test-invocation recipient lists** (9 adversarial
events x 2 recipient carriers), and the marker-free scheduled payload still resolves to
`['aj@opalinvest.com', 'andrew@opalinvest.com']`. The module was imported with every boto3 client
replaced by a stub that **raises** on any call, so no code path inside it could reach AWS.

That is arm (a), and it is the only arm of `S21-AC1` that can be measured.

---

## 2. WHY ARMS (b)-(g) CANNOT BE MEASURED -- two blocking findings

The cell requires three things that cannot simultaneously hold:

1. a class-C-or-worse condition **FORCED** by "the least invasive mechanism that reaches the
   classifier's real code path";
2. that forcing **DISCLOSED on the produced verdict document**, with the run id;
3. the **ORCHESTRATOR's** terminal send fired on the refusal branch (arm (e) = FWD-10);

while binding **"NO CODE CHANGE"** and granting `<paths>` that deliberately exclude
`lambda_function.py` and never mention the renderer at all.

### FINDING 1 -- no forcing can reach the classifier through an orchestrator invocation

The deployed orchestrator builds a **fixed** render command:

```
f"python3 render_month_end.py --month {month} --pdf --gate --s3-out {out}"
```

An AST census over the same deployed bytes (3,142 nodes walked) shows the handler reads **exactly
four** event keys -- `mode`, `month`, `probe`, `test_recipients`. So `month` is the only
event-derived input that reaches the box. No forcing spec can ride an invocation.

**The mechanism the face prefers already exists and is unreachable.** The renderer's own
`--fixture-remove` is documented "EG-s-6 QA: remove these slices from the loaded series IN MEMORY
before rendering/gating; **nothing on S3 is ever touched**" -- literally "an input fixture the
classifier reads", which the face prefers over editing a real month. The orchestrator simply never
threads it.

**And arm (e) closes the obvious substitute.** A renderer-only SSM run *could* carry the flag, but
the terminal send lives only in the orchestrator (`_send_terminal_unresolved` at deployed `:307` and
`:605`), and the deployed renderer has **0 SES call sites** (0 of 4 call-site tokens over 62,880 B).

> A number I printed and then had to correct: a bare substring count of `ses` in the renderer
> returns **12** -- `uses`, `series`, `closes`. My first run printed that as "occurrences of any SES
> send: 12", a figure that *contradicted the very claim it was printed to support*. The battery now
> counts call-site tokens and word boundaries and discloses the artifact beside the real value.

### FINDING 2 -- the verdict artifact has no field able to disclose a forced condition

Censused over **the renderer the box actually pulls** -- `s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/render_month_end.py`,
62,880 B, sha256 `55701125e86740f3bf51a715aba8f68e8441d3eb7bffc99a43b7d3ff29b973e9`, byte-equal to
the repo build input (the GRAIN that matters: the box `aws s3 cp`s this artifact at run time, so the
repo file is the build input, not the deployed object):

| | |
|---|---|
| disclosure tokens | `forced`, `FORCED`, `is_forced`, `run_id`, `runid`, `run-id`, `request_id`, `requestId`, `trigger`, `driven` -- **10 of 10 ZERO** |
| positive controls | `generated_at` 1, `fixture_remove` 22, `verdict` 23, `unresolved` 13, `per_partner` 6 -- **all non-zero** |
| served verdict keys | `['generated_at', 'holes', 'month', 'per_partner', 'unresolved', 'verdict']` |

The controls are what make the zeros an **absence** rather than a dead read. Producing such a field
is a code change to `data/etfs/scripts/presentation/render_month_end.py` **plus** a re-upload of the
S3 renderer artifact -- a second lane, outside the grant, and forbidden by the face's own bound.

---

## 3. WHY I DID NOT FIRE ANYWAY

An unforced run **cannot** refuse. The classifier's own rule, quoted from the deployed artifact:

```
render_month_end.py:963   verdict = "REFUSE" if any_c else "PUBLISH"
```

Class **C only**. D and UNKNOWN are reported, never refused. The last real run's served verdict:

| partner | A | COVERED | B | C | D | UNKNOWN | holes |
|---|---|---|---|---|---|---|---|
| 49financial | 3 | 5 | 0 | **0** | 1 | 0 | `['2026-09-09']` |
| cottonwood | 3 | 5 | 0 | **0** | 1 | 0 | `['2026-09-09']` |
| inflection | 3 | 6 | 0 | **0** | 0 | 0 | `[]` |

`verdict=PUBLISH holes=2`, class C = **0 of 3 partners**.

So firing would have spent this order's **one permitted run** on a PUBLISH that writes the served
publish keys and sends the **ordinary monthly email to both recipients** -- precisely what round 1
did by accident (`W1-S22`, `W1-S23`, `W1-S24`) -- while proving nothing about FWD-10. Knowingly
repeating a measured mistake is worse than not acting, and the face's "ONE driven run" bound means
the run spent that way is not recoverable.

---

## 4. WHAT A RE-CUT NEEDS -- both small, both outside this grant

1. **Thread a forcing spec from the event into `_render_command`** in
   `infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py` -- the same shape as EG-s-15's
   `month` override. Note CLAUDE.md's NEVER clause: such an override **creates a new reachable
   state on the manual path**, and the sign-off must cover that state or the override does not land.
2. **Have the renderer record the forcing and a run id on `coverage_verdict.json`** in
   `data/etfs/scripts/presentation/render_month_end.py`, re-uploaded to the artifact prefix.

Both are code cells. `EG-s-21` as cut is a *run-it-as-deployed* cell, and the capability it needs to
run was never built. That is the whole finding.

---

## 5. THE CRITERIA

### `S21-AC1` -- FAIL

```
$ timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs21_driven_refusal.py
ARM (a) PRECONDITION : HOLDS -- 0 of 18 resolutions reach aj@
ARMS (b)-(g)         : NOT MEASURABLE -- the cell's forcing premise fails.
    BLOCKING: no forcing reaches the classifier through the orchestrator
    BLOCKING: the verdict artifact cannot disclose a forced condition or a run id

NOTHING WAS INVOKED. NO SEND WAS FIRED. NO S3 KEY WAS WRITTEN OR DELETED.

EGS21-BLOCKED-NO-FORCING-PATH
rc=2
```

Expected `EGS21-REFUSAL-DRIVEN-AND-SENT`; got `EGS21-BLOCKED-NO-FORCING-PATH`. **No match, so FAIL.**
The battery is written so it *cannot* print the success token -- a battery that could pass without a
driven refusal would be the confident-wrong shape this project exists to kill.

Full output: `EG-s-21_S21-AC1_battery_output.txt`.

### `S21-AC2` -- RECORDED, judgment, NO VERDICT

The criterion asks how a person would read the refusal, whether the driven condition is a faithful
analogue, whether the disclosure is enough, and what the send's evidence proves about delivery.
**No refusal was produced, so three of those four have no object to grade.** What can be recorded:

- **The disclosure question is answerable in advance, and its answer is the block.** The face is
  right that a driven artifact which looks organic is the confident-wrong shape. On the deployed
  renderer there is *no way to make it look driven*: a forced run and an organic run would emit
  byte-identical schemas, distinguishable only by an out-of-band note in a ledger entry. That is
  exactly the failure mode the requirement exists to prevent, which is why I read the requirement as
  load-bearing rather than decorative and stopped instead of firing without it.
- **On emission vs delivery, unchanged from EG-s-20:** the `MessageId` line added at `:307`/`:605`
  is an emission oracle, not a delivery oracle. Nothing here moves that.
- **On the faithfulness of the analogue, one thing is worth the CVO's attention:** `--fixture-remove`
  forces a C by hiding a slice the classifier would otherwise see, so the *probe* still reports the
  upstream present and priced -- which is precisely the real class-C shape ("upstream present and
  priced > 0, no slice -- producer never fired for this date"). It is a faithful analogue. The
  mechanism is sound; only its reachability is missing.

**Evidence vintage:** deployed orchestrator as of `LastModified 2026-09-10T03:54:09Z`; deployed
renderer sha256 `55701125e86740f3...` read 2026-09-10 ~04:4xZ; served verdict `generated_at
2026-09-10T01:20:19.883859+00:00`; code citations `@9e3040a75f`.

---

## 6. WHAT I DID NOT DO

- **No invocation of anything** -- not the orchestrator, not a producer probe, not SSM.
- **No NEVER-2 entry opened.** The face requires one *before the act*; there was no act. Opening and
  closing an entry for a deploy that never happened would put a false event in the change-management
  record.
- **No code change**, and no write to `.tools/`, the renderer, or the orchestrator.
- **No S3 write and no S3 delete.** NEVER-AUTO-DELETE was never approached.
- **No status flip.** `S21-AC1` FAILs, so `ETFS_GUARDRAIL.TO-EG-s-21` stays `pending`.
- **No second attempt at anything.** The "ONE driven run" bound is intact and unspent.

## 7. PUSH STATE (MEASURED)

See the WORKER REPORT. Commits are LOCAL on `wk-etfs_guardrail-3-4`; the issuer drains the branch.
