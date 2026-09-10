# ETFS_GUARDRAIL.TO-EG-s-29 -- RESULT

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~5` · **branch** `wk-etfs_guardrail-3-29` ·
**code commit** `903c5cba50` · **served** `s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/render_month_end.py`
VersionId `lvBC1IFEk3Fpfry_ysQfCNf5PIA8f00E`, sha256 `ba410ee5c9c4263e8fe37ade171aa4d61f834df246d0f57f30299dbba03a031a`.

---

## S29-AC1 -- PASSES BY OUTPUT, 7 of 7 arms

```
invocation : timeout 600 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs29_skipped_branch_carries_the_property.py
rc         : 0
last line  : EGS29-SKIPPED-BRANCH-CARRIES-THE-PROPERTY
transcript : org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/egs29_battery_output.txt (343 lines)
```

| arm | control kind | the deciding number |
|---|---|---|
| (a) | CENSUS | 5 of 5 UNRESOLVED-record sites across BOTH files, by AST from source; BEFORE renderer 0 of 1 carries `provider`, AFTER 1 of 1, remediate.py 4 of 4; the BEFORE skipped branch records 0 egress asks |
| (b) | DIFFERENCE | 4 of 4 records carry `provider`; value equals `remediate.remediate_month`'s own output for the same partner; date/class/reason identical either side, so the only difference is the new field |
| (c) | POSITIVE | an unmapped partner yields `<no provider mapped>`, byte-identical to the ladder branch's value for the same partner; 0 records carry a null provider |
| (d) | DIFFERENCE (carries the outcome) | the run records an ask at `coverage_egress_ask_ladder_skipped.json` and does NOT write rung 3's key; 7 of 11 fields differ from a real rung-3 ask over the same input, all enumerated; 4 of 4 ask rows carry date+partner+provider; `authorization`, `ask_scope`, `partners_covered` byte-identical to rung 3's |
| (e) | INVARIANCE | 24 of 24 compared quantities identical on `ladder=True` across 2 scenarios; the two scenarios disagree with each other (PUBLISH vs REFUSE), so "identical" is a measurement; EG-s-25/EG-s-26's records 12 of 12 fields present and 0 of 12 moved on BOTH branches |
| (f) | CENSUS | served sha256 == committed, re-downloaded by VersionId; prior differs (negative control); 1 of 7 artifact keys moved since the entry opened; 0 of 37 reports keys moved by both instruments; 0 of 6 SES datapoints overlap; 0 invocations across 13 of 203 functions; 0 of 25 steps off-axis; the battery itself made 0 AWS calls |
| (g) | CENSUS | branch `wk-etfs_guardrail-3-29`, HEAD `903c5cba50`; comp-rail corpus fix present (`def corpus_root` x1) AND `838b963638` in ancestry rc=0; probe file present here and ABSENT on CLOUD |

**The issuer's conformance count, restated and MET:** 2 difference controls -- (b) and (d),
and (d) carries the outcome. (c) is a positive control and is not a difference control.
(e) is an invariance proof; (a), (f), (g) are censuses with printed denominators.

---

## WHAT WAS BUILT, AND THE ONE DESIGN DECISION THAT IS NOT OBVIOUS

The skipped branch resolves `provider` through `remediate._provider_for` -- imported and
called. A second `.get(partner, "<no provider mapped>")` in the renderer would have been a
second writer of the same property, which is the defect this cell exists to close.

The ask is built by **rung 3's own code**. `_Rung3AskRedirect` is a read-through,
key-redirecting, write-capturing facade handed to `remediate.rung3_stop_and_ask`, so the
cross-partner merge (EG-s-23), `ask_scope`, `partners_covered` and the PER-USE
`authorization` string are rung 3's OUTPUT and not a re-implementation of it. The facade
exposes `get_object` **only when the wrapped client has one**, because
`_read_prior_asks` deliberately distinguishes "no read capability" from "object absent",
and a facade that always answered would have collapsed the two -- EG-s-23's exact defect,
one layer up.

**IT WRITES ITS OWN KEY** -- `platinum/reports/<month>/coverage_egress_ask_ladder_skipped.json`
-- for two load-bearing reasons, not for tidiness:

1. `--no-ladder` is the QA/rehearsal shape. Writing rung 3's canonical key would let a
   rehearsal run MERGE INTO and republish the document a person authorises real egress on.
2. EG-s-26's disclosure says `coverage_egress_ask.json` is ABSENT BY CONSTRUCTION for a
   ladder-skipped run. That is TRUE and stays true only while this branch writes elsewhere
   -- which is also how arm (e)'s "present and unchanged" is met without a contradiction
   inside the verdict artifact.

EG-s-21's arm (d), re-cut on R-EG-8, accepts an ask "written by rung 3 **or** by EG-s-29's
rung-3-equivalent ... and the record must say WHICH WROTE IT". It does, in its first field.

---

## S29-AC2 -- JUDGMENT, RECORDED. NO VERDICT. For `3.0.0_SA_CVO` at L9.

### (i) Is the equivalent a FAITHFUL ANALOGUE, or merely a record with the same shape?

**It is not "the same shape" -- the shape is not copied, it is PRODUCED BY THE SAME
FUNCTION.** `remediate.rung3_stop_and_ask` builds this record; the renderer supplies the
unresolved days and the storage key and stamps provenance. Nothing about the ask's content
is re-implemented, so it cannot drift from rung 3 the way a copy would.

**Every difference measured in arm (d), 7 of 11 fields, none omitted:**

| field | difference | is it a difference of KIND or of RUN? |
|---|---|---|
| `written_by` | present on the equivalent, ABSENT on a real ask | KIND -- deliberate; it is the whole disclosure |
| `rung3_ran` | `false` on the equivalent, ABSENT on a real ask | KIND -- deliberate |
| `ask_content_built_by` | present / ABSENT | KIND -- deliberate |
| `equivalent_of` | present / ABSENT | KIND -- deliberate |
| `stored_at` | present / ABSENT | KIND -- deliberate |
| `generated_at` | different instants (ms apart in the battery) | RUN |
| `asks[].reason` | `"ladder skipped (--no-ladder)"` vs `"rung 1 invoke returned but no slice landed on rung 2 re-check"` | **RUN, and this is the one that matters -- see below** |
| `month`, `ask_scope`, `partners_covered`, `authorization` | IDENTICAL | -- |
| `asks[].date/partner/provider/class` | IDENTICAL in the battery's paired run | -- |

**THE DIFFERENCE THAT IS NOT COSMETIC IS `reason`, AND IT IS NOT A DEFECT OF THIS RECORD
-- IT IS THE TRUTH ABOUT THE RUN.** A real rung-3 ask says *"rungs 1 and 2 were tried on
this day and failed"*. The equivalent says *"the ladder was skipped, so nothing was
tried"*. Those are different facts about the same date and the equivalent states the one
that is true of it. A reader who does not notice would over-estimate how much recovery had
already been attempted. **The record does not merely permit that reading, it forces it:**
the reason is on every row and `written_by` is the first field in the document.

**Where the analogue is genuinely WEAKER, stated rather than implied:** a real rung-3 ask
is a claim about days that survived three rungs; the equivalent is a claim about days no
rung touched. The SET can therefore be larger -- a day rung 1 would have recovered is in
this ask and would not be in rung 3's. **The equivalent over-asks; it cannot under-ask.**
That direction is the safe one for an egress decision (a person is shown more than is
strictly outstanding, never less), and it is the opposite direction from EG-s-23's defect,
which under-reported.

### (ii) Could a person authorise egress on it as safely as on a real ask?

**On the arithmetic, yes; on the framing, only if they read the first field.** Every
property a person needs is present and is rung 3's own: the days, the partner, the
provider, the class, the PER-USE `authorization` string, and the merged
`partners_covered` so a partner that never wrote is not invisible (EG-s-23's fix,
inherited rather than re-derived). Nothing here is executed by any process, exactly as
rung 3 guarantees.

**The residual risk is over-approval, not under-approval,** for the reason above: some
days in this ask might have been recoverable by a rung 1 that never ran. A person who
authorises egress on all of them approves *more* than the minimum -- which costs a vendor
ask that was not strictly necessary and never fabricates a value. **I record, without
weighing it, that "ask the vendor for a day the producer could have re-run" is a real
operational cost and the CVO may not consider it acceptable.** The mitigation available
inside this cell is the one taken: every row says `ladder skipped (--no-ladder)` in the
field a reader is looking at when deciding.

### (iii) Does any consumer parse either artifact, and could the new field break it?

**CENSUS, with its denominator.** `comp-find "coverage_egress_ask|coverage_unresolved"
--all` (run in this worktree, positive control in arm (g)): **413 hit(s) across 29,653
file(s) scanned, corpus=all**; bands DEF=7 SURFACED=101 CONFIG=52 TEST=64 DOC=189.
Subtracting the two PRODUCERS, this cell's own scratch/deliverable files, the three graph
recognizers and the graph `derive_runner` (which match the string as a PATTERN, not as a
read), and all DOC/task-order text, **the first-party CODE consumers are ONE**:

* `infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py` @`e94ce02a92`
  * `_normalize_unresolved` (:266-300) copies each row with `dict(r)` -- **it enumerates
    no keys, so a new key cannot break it.**
  * `_build_terminal_email` (:368-373) already reads `u.get('provider') or '(not
    stated)'` -- **the new field is CONSUMED, not merely tolerated**; that line is what
    made the "(not stated)" column, and it now renders a real provider on this branch.
    That is what makes FWD-10's accept (ii) satisfiable on a shape-1 run.
  * `_read_coverage_artifacts` (:333-346) reads a **literal three-filename tuple** and the
    ladder-skipped key is not in it.

**TWO ROWS CAME OUT OF THIS CENSUS AND BOTH ARE FILED, NEITHER FIXED** (that file is
outside this order's `<paths>`): `W5-S14` -- the comment at :369-371 asserting that the
producer does not write `provider` is now FALSE for both branches, and it is the comment
EG-s-28's own face quoted as the defect's evidence. `W5-S15` -- the terminal email built
on a shape-1 run will carry **no egress-ask block**, because the orchestrator reads only
rung 3's filename. FWD-10's accept (ii) does not depend on that block -- it is served by
the unresolved rows, which now carry the provider -- but a reader of the email is not told
that an ask was recorded and must open S3 to find it.

### (iv) What a reader STILL cannot tell from a shape-1 run after this change

1. **From `coverage_verdict.json` alone: that an egress ask exists at all.** The `forcing`
   block still says rung 3's artifact is absent by construction -- true -- and says nothing
   about the equivalent, because the only field family that could carry the pointer is the
   one arm (e) freezes. Row `W5-S13`. The pointer lives in the run's stdout and in the
   object itself.
2. **From the terminal email: that an ask was recorded.** Row `W5-S15`.
3. **From the ask alone: how much recovery was attempted.** It says the ladder was skipped
   on every row, which is the fact; it cannot say which of those days a rung-1 re-run
   would have fixed, because nothing ran. **That is a property of shape 1 itself, not of
   this record**, and no artifact written by a ladder-skipped run can answer it.
4. **From any of it: whether the organic monthly run would have produced the same set.**
   The driven run forces its own input (EG-s-25's disclosure covers that half).

---

## THE DEPLOY

Ledger entry `etfs-guardrail-egs29-renderer-skipped-branch-property-20260910`, opened
`2026-09-10T14:09:00Z` **BEFORE** the copy (object LastModified `14:09:53Z`), five legs,
all proven, **CLOSED `2026-09-10T14:15:13Z` -- before the grading battery run recorded in `egs29_battery_output.txt`**. Completion record:
`org/critical_paths/change_management/20260910T1409Z_etfs-guardrail-egs29-renderer-skipped-branch-property-20260910_deploy_completion.md`.

* **prior** VersionId `TkhI7NPt_hpJUaXYAlBnjZggJQDz.wBG`, 69,879 B, sha256 `9b9cdd9c...`
  -- recorded before any write, **taken from the VERSION HISTORY and not from "latest"**,
  because this script is re-runnable and on a second invocation `latest` IS this act's own
  upload; reading it as the prior would have made the rollback a no-op and the negative
  control a tautology, and both read CLEAN.
* **served** VersionId `lvBC1IFEk3Fpfry_ysQfCNf5PIA8f00E`, 77,130 B, sha256 `ba410ee5...`,
  **re-downloaded by that VersionId**, byte-equal to git blob
  `903c5cba50:data/etfs/scripts/presentation/render_month_end.py`. The uploaded payload was
  the **committed blob** (`git show`), never the worktree file -- on an autocrlf box a
  worktree read hashes the checkout; both were measured and are equal anyway.
* **rollback, exact, one command:**
  `.tools/aws s3api copy-object --bucket opal-313476888478-lambda-artifacts --key ec2/etfs-reports/render_month_end.py --copy-source 'opal-313476888478-lambda-artifacts/ec2/etfs-reports/render_month_end.py?versionId=TkhI7NPt_hpJUaXYAlBnjZggJQDz.wBG'`
* **blast radius on the CONSUMER, both producer branches named:** `ladder=True` moves
  NOTHING (24 of 24); `--no-ladder` gains a `provider` field on every unresolved record and
  writes ONE NEW KEY per month, `coverage_egress_ask_ladder_skipped.json`. No existing key
  is overwritten by it and it never merges into rung 3's.

**Evidence:** `egs29_deploy_evidence.json` (25 steps, argv verbatim, rc each).

---

## ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `W5-S11` | OBSERVATION / **ARMED**, `disarm_owner 2.0.0_SA_COO` | one `pytest` run of this cell's own suite PUT a real object under `platinum/reports/` and every assertion still passed; recurrence closed by an autouse fixture, the object left in place because an S3 delete on an unversioned bucket is Andrew's to confirm |
| `W5-S12` | OBSERVATION / INERT | the face cites `remediate.py:130` for the provider default; at HEAD it is `:91` and `:130` is the ask-merge's `doc.get("asks")` |
| `W5-S13` | OBSERVATION / INERT | `coverage_verdict.json` cannot point at the equivalent ask without moving the record arm (e) freezes; recorded to AC2 instead of widening the order |
| `W5-S14` | OBSERVATION / INERT | the orchestrator comment asserting the producer never writes `provider` is now false on both branches |
| `W5-S15` | OBSERVATION / INERT | the orchestrator reads a literal three-filename tuple, so a shape-1 run's terminal email carries no egress-ask block |

**W5-S11 is the one to read first.** It is filed against my own act, and its mechanism is
CLAUDE.md Rule 22's shared-dependency blindness in miniature: three test arms shared a
premise that was a property of the CODE ("this branch touches no S3"), one change killed it
for all three at once, and every per-arm assertion kept passing.
