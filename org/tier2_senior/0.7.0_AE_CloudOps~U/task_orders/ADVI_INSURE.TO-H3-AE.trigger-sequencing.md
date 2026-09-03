# TO ADVI_INSURE.TO-H3-AE -- the 49F gold chain's 09:46Z fire RACES the fact_acc silver write it depends on (row ADVI_INSURE-S13): MEASURE the trigger's event shape and the race margin first (read-only, before the ~21:46Z acceptance fire), then SEQUENCE the chain on the partition it needs by the remedy the measurement selects -- deployed only AFTER TO-H2-AE's acceptance fire is read, never on the shared rule's other consumer

<task_order>
<id>ADVI_INSURE.TO-H3-AE.trigger-sequencing</id>
<to_id>ADVI_INSURE.TO-H3-AE</to_id>
<project>ADVI_INSURE</project>
<issued_to>0.7.0_AE_CloudOps~U</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-09-03</issued_date>
<status>pending -- GO paired at cut (2.0.0_SA_COO, /drive v2 tick 4, 15:4xZ). Authority: decomp v1.1 @c2ef0ee09f cell INS-h-3 (the chain's trigger sequencing; homed under ADVI_INSURE because the race gates THIS project's acceptance fire and the fixer is the lane that re-arms the stage); row ADVI_INSURE-S13 @3595675047 (0.7.0_AE_CloudOps~R's measurement, ARMED, disarm_owner 2.0.0_SA_COO); 0.0.0_AB_MSTR 93538/93555 (the remedy is the issuer's L5/L6); register ADVI_49F.json blocking @0ac51eec31 (the durable carrier). PHASE 1 (measure) runs NOW, read-only, in parallel with the wait on TO-H2-AE's ~21:46Z fire; PHASE 2 (the remedy) is SEQUENCED behind H2's step 6 -- no deploy of any 49F surface before that fire's log is read, so the acceptance fire tests the re-armed bytes and nothing else.</status>
<priority>P1 -- the class CLAUDE.md names ("success-of-upstream as the only trigger is a defect"); every event-driven 09:46Z fire until this lands is decided by seconds</priority>
<endpoint>docs/architecture/ADVI_INSURE_PRD.md s.6 (the acceptance fire of the insurance stage requires the chain to reach it: an a00 abort is sixteen stages before insurance_nav_current) -- FWD via s.6 property (c) gold; the chain is ADVI_49F's and the row says so</endpoint>
<tier>2</tier>
</task_order>

## THE CELL, AND THE MEASURED PICTURE IT STARTS FROM

**INS-h-3 (decomp v1.1 @c2ef0ee09f):** the 49F gold chain's trigger sequencing. Measured on 2026-09-03 (row S13, grounded): the 09:46Z fires are EVENT-driven -- EventBridge rule `bd-49f-session-complete` (`infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf` :246-275; pattern `source aws.ssm`, `detail-type "EC2 Command Status-change Notification"`, `document-name opal-bd-49f-session-fetch`, `status Success`) -> target `bd-49f-session-trigger` with input `{mode: runner-run}`. That SSM Success is NOT the fact_acc silver write completing: on 09-03 `s3://opal-data-assets/schwab/08335338/silver/fact_acc/date=2026-09-02/data.parquet` landed 09:46:39Z (its normal band 09:46:24-40Z over the last 8 partitions, denominator 543 objects), ONE TO TWO SECONDS AFTER the chain's a00_dim_account check (lock holder pid 1166 from 09:46:36Z; `CHAIN ABORT stage=a00_dim_account rc=1 wall=1.6s`; the partition the chain said did not exist, exists). On 09-02 two runs two seconds apart reached opposite verdicts on the same table. UNMEASURED HYPOTHESIS: four triggers inside 8 s on 09-03 (three refused on the lock) = one SSM command emitting several status-change events; the discriminator is a CloudTrail / EventBridge read of that command's events. The rule is SHARED: `runner=fees` routes the same session-complete to `bd-49f-fees-runner` (:281-300); the trigger Lambda also carries `INSURANCE_RUNNER_FUNCTION_NAME` (TO-A4-AEC). The row named the owner class `0.7.0_AE_CloudOps` (the SSM/EventBridge trigger side) and left the REMEDY CLASS undecided: (a) sequence the chain on the fact_acc write completing, or (b) a bounded retry-until-partition -- never a wider sensor.

## DELIVERABLE -- in this order, each step's evidence in the report

**PHASE 1 -- MEASURE (read-only; NOW, before the ~21:46Z fire; no write to any AWS surface, no deploy):**

1. **THE TOPOLOGY, from the artifacts that decide it, not the brief:** read `docs/briefs/TRIGGER_GRAPH_AND_RUNTIME_MAP.md` (+ the 20260806 delta) for orientation, then the trigger Lambda's handler as SERVED (the `bd-49f-session-trigger` artifact `bd-pipeline/bd-49f-session-trigger.zip` at its live `source_code_hash`, read via the module's artifact bucket -- name the bucket from the module) and `bd-49f-runner`'s handler: WHO writes `fact_acc` silver and WHO dispatches the gold chain to the box, and whether both start from the same event. State it as a two-line chain with the function names and the dispatch verb (Invoke / send_command).
2. **THE EVENT SHAPE (the S13 hypothesis's discriminator):** for the 09-03 09:46Z window, list the EventBridge invocations of `bd-49f-session-complete` and the SSM command's status history for `opal-bd-49f-session-fetch` (CloudTrail `SendCommand` + the command's invocation statuses via `ssm list-command-invocations --details`, and the rule's CloudWatch metrics `Invocations`/`TriggeredRules` at one-minute grain). Answer with denominators: how many status-change events ONE command emitted, which of them match the pattern, and the UTC second of each. Repeat for 09-02 (the two-seconds-apart day). NEVER `--no-paginate`; count client-side.
3. **THE RACE MARGIN OVER DAYS:** for every fire in the last 10 chain logs under `s3://opal-data-49financial/gold/advi/_logs/` (denominator printed), pair the chain's a00 check timestamp with the fact_acc partition's `LastModified` (s3api, UTC) for the asof it needed; tabulate margin = write - check in seconds, sign and all. The table IS the finding; a negative margin on any day the chain passed is a day the check saw a partition from an EARLIER write, and says so.
4. **THE DECISION, read off the table, not chosen:** (i) if the command emits a LATER pattern-matching status event that follows the fact_acc write on every measured day, the remedy is the rule's PATTERN narrowed to that terminal event -- Terraform only, no code -- **but ONLY if the fees path (`runner=fees`) and the insurance runner are shown by the same read to receive the event they need under the narrowed pattern; if not shown, (i) is OFF the table**; (ii) otherwise the remedy is a BOUNDED WAIT at the point that dispatches the gold chain: before the dispatch, poll for the fact_acc partition `date=<asof the chain will demand>` with `ListObjectsV2` on that exact prefix, every 5 s, for at most 240 s, then dispatch; on expiry dispatch anyway and log `WARN: fact_acc partition absent after 240s` (the chain's own a00 refusal stays the verdict -- this wait removes the race, it does not hide an absent upstream). Which component carries the wait is decided by step 1: the trigger Lambda's `runner-run` path if the gold dispatch is there; else `bd-49f-runner`. **Report Phase 1 to 2.0.0_SA_COO before Phase 2 starts** -- the issuer confirms the decision row in one line (a ruling, not a review); if the table supports neither branch, say so and stop at Phase 1.

**PHASE 2 -- THE REMEDY (sequenced: starts only after TO-H2-AE step 6 has READ the ~21:46Z fire's log, and 10+ minutes clear of the 22:20Z fees session-refresh and every fire window on the face of H2):**

5. **ZERO IAM CHANGE (Andrew's standing word on this chain):** before writing code, read the carrying function's role policy (`aws_iam_role.bd_49f_session_trigger` or the runner's) for `s3:ListBucket` on `opal-data-assets` with the `schwab/08335338/silver/` prefix condition. If the permission is ABSENT, STOP: report the exact missing statement to 2.0.0_SA_COO and do not add it -- the fallback then is the wait inside the chain's own a00 stage on the box, which already reads that prefix (a DS-lane path; the issuer cuts it). If PRESENT, proceed.
6. **THE CODE:** the minimum -- one bounded loop, `_wait_for_partition(bucket, prefix, asof, budget_s=240, step_s=5) -> bool`, called once at the dispatch; every line ASCII; no new dependency; `.tools/commit-gate.sh` clean. A NEW battery with a RED mutant per arm: present-at-once (0 polls extra), present-after-N (returns True at the Nth poll, measured), absent-through-budget (returns False at budget, one WARN line, dispatch still happens), and the negative control that the asof demanded equals the asof the chain will check (read from the same source the chain reads, never typed). Branch (i) instead: the narrowed pattern in the `.tf`, plus a saved plan showing exactly 0 add / 1 change / 0 destroy on `aws_cloudwatch_event_rule.bd_49f_session_complete` and NOTHING on the fees/insurance targets.
7. **THE DEPLOY, Terraform only, under a deploy ledger:** `.tools/deploy_ledger.py open` FIRST (entry `advi-insure-trigger-sequencing`), the artifact rebuilt to its bucket key by the estate's build path (never `aws lambda update-function-code`), `safe-apply` on a SAVED plan reading exactly the one change, the apply output captured to a FILE named in the ledger, then the served `source_code_hash` / rule pattern read back live (`get-function-configuration` / `describe-rule`) and compared with the plan's value -- the L2/L3 legs close on those reads. NEVER a second apply on a disagreeing read: stop and report on the order.
8. **THE ACCEPTANCE FIRE = the next event-driven 09:46Z window after the deploy (09-04):** its chain log shows a00_dim_account passing on the FIRST attempt with the wait's own log line stating how long it waited (0 s is a valid answer and says the race was not exercised that day -- record it as such), no `CHAIN ABORT`, one chain run for the window (the lock-refusals count printed), and the fact_acc partition's `LastModified` vs the dispatch time showing the order the remedy promises. L4 closes on that read; `deploy_ledger.py close`. If the fire still aborts at a00, report the abort line and the wait's line verbatim; do not re-run the chain by hand.
9. **THE RECORD:** the proof instance (below) validated rc 0, committed under this lane's author with a python-written `-F` message via `.tools/safe-commit.sh`; row S13's disarm is the ISSUER's act on your Phase-2 report (do not edit S13); one report to 2.0.0_SA_COO per phase with hashes and push state LOCAL. NEVER `git push`.

## ACCEPTANCE -- criterion ids minted at cut; the assignee files the proof instance

<criterion id="H3-AC1" cell_refs="INS-h-3"/> `H3-AC1` -- TOPOLOGY STATED FROM SERVED BYTES: the two-line chain (who writes fact_acc, who dispatches the gold chain, from which event) cites the served handlers at their live `source_code_hash`, not the brief.
<criterion id="H3-AC2" cell_refs="INS-h-3"/> `H3-AC2` -- THE EVENT SHAPE MEASURED WITH DENOMINATORS for 09-02 and 09-03: events per command, pattern matches per command, UTC seconds; the S13 hypothesis (several events per command) read TRUE or FALSE on that evidence.
<criterion id="H3-AC3" cell_refs="INS-h-3"/> `H3-AC3` -- THE RACE-MARGIN TABLE over the last 10 chain logs (denominator printed), write-minus-check in seconds with sign, and the decision row read off it under step 4's rule, with the fees/insurance consumers explicitly shown safe if branch (i).
<criterion id="H3-AC4" cell_refs="INS-h-3"/> `H3-AC4` -- ZERO IAM CHANGE: the role read cited; either PRESENT (proceeded) or ABSENT (stopped and reported) -- no policy edited, no simulate as proof.
<criterion id="H3-AC5" cell_refs="INS-h-3"/> `H3-AC5` -- THE REMEDY BUILT AND DEPLOYED UNDER THE LEDGER: the battery with a RED mutant per arm (or the saved plan for branch (i)); the apply file; the live read-back equal to the plan's value; ledger legs L1-L3 closed on reads.
<criterion id="H3-AC6" cell_refs="INS-h-3"/> `H3-AC6` -- THE ACCEPTANCE FIRE (09-04 09:46Z window): a00 passes first attempt, the wait's line present with its measured seconds, no CHAIN ABORT, one run per window; L4 closed; UNCOMPUTABLE until that fire, and stated so.
<criterion id="H3-AC7" cell_refs="INS-h-3"/> `H3-AC7` -- SEQUENCING HONOURED: no write to any 49F surface before TO-H2-AE's ~21:46Z fire was read (H2 step 6 cited by log key) and no deploy inside 10 minutes of a fire window; the shared rule's fees and insurance consumers untouched unless branch (i) proved them safe.
<expected_criteria>H3-AC1, H3-AC2, H3-AC3, H3-AC4, H3-AC5, H3-AC6, H3-AC7</expected_criteria>

## SURFACES

- `infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf` :246-275 (the rule + target + permission), the `module "bd_49f_session_trigger"` block (artifact `bd-pipeline/bd-49f-session-trigger.zip`, runtime python3.12, timeout 600), :281-300 (the fees consumer of the same rule); `infra/aws/lambda/ci/trigger-map.json`; the trigger Lambda's and `bd-49f-runner`'s source under `infra/aws/lambda/` (resolve the directory from the artifact key; name it in the report).
- `s3://opal-data-assets/schwab/08335338/silver/fact_acc/` (READ ONLY -- 49F's own key prefix in a shared bucket; the cross-firm rule binds by prefix), `s3://opal-data-49financial/gold/advi/_logs/` (READ ONLY).
- `org/critical_paths/.open_deploys/advi-insure-trigger-sequencing.json` (Phase 2, yours to open and close); `org/surprise_channel/ADVI_INSURE/INVESTIGATION_v1.md` (append-only rows for anything odd, never a message; S13 is the issuer's to disarm).

## BOUNDS

- **READ-ONLY until H2's fire is read.** Phase 1 writes nothing to AWS and deploys nothing. Phase 2 starts only on the issuer's one-line confirmation of the decision row AND after H2 step 6.
- **ZERO IAM CHANGE** on this chain (Andrew's standing word). A missing permission is a STOP-and-report, never a policy edit.
- **THE SHARED RULE'S OTHER CONSUMERS** (`runner=fees` -> `bd-49f-fees-runner`; the insurance runner) are out of bounds unless branch (i) proves them unaffected by the same read; the rule carries an `ADVI_BDAPIMIG` tag -- that project is sovereign-excluded and nothing here is done ON it; the rule is 49F chain infrastructure this cell measures.
- **NEVER re-run the 49F chain by hand** (Andrew's standing hold), never `aws lambda update-function-code`, never bare `terraform apply` (`safe-apply` on a saved plan), never `git push`; commits via `.tools/safe-commit.sh` under your author with a python-written message file; state push state LOCAL.
- **No new monitor / alarm / sensor** (standing moratorium): the wait logs one line and the chain's own refusal stays the verdict.
- **Never `head` a census; never `--no-paginate`; never `2>/dev/null` a read whose emptiness carries the verdict; `aws s3 ls` renders local time -- use `s3api` for UTC.**
- Certifier != author: 3.0.0_SA_CVO grades; the issuer confirms the decision row and disarms S13.
- **PUSH (standing law on this CODEX seat's face):** a shared branch (CLOUD / DEV / PROD / main / SITEZ) is pushed ONLY by `0.0.0_AB_MSTR` or `0.0.0_AB_MSTR~Z`, and only on Andrew's word while he is at the terminal; this seat COMMITS and states LOCAL; it NEVER runs `git push`.

<decomp_ref>
<decomp_doc>workflows/atom_decomposition/runs/advi-insure/20260824T204500Z/DECOMP.md</decomp_doc> @c2ef0ee09f (v1.1), cell INS-h-3 (the chain's trigger sequencing; ADDED on the round-4/5 measurement, row ADVI_INSURE-S13 @3595675047; INS-h-2 in flight as TO-H2-AE)
<owned_cells>INS-h-3</owned_cells>
</decomp_ref>

<preflight>
comp-schedule: RUN -- GATES ARMED 23 across 5 carriers (read at 2026-09-03 15:40Z); TWO name this project's surface, both the H2 order's own open ledger entries (advi-insure-gold-chain-membership, advi-insure-iam-insurance-silver-read; discharge = TO-H2-AE step 6 at this same seat) -- this order's Phase 2 is sequenced behind that discharge by its own face; no gate names INS-h-3.
comp-iam: DECLARED-NOT-APPLICABLE -- the order forbids any IAM change (step 5 reads a role policy and STOPS on absence; it never edits or simulates as proof).
comp-adversary: RUN -- rc 0 at read-vintage @7138c4a176 (2026-09-03T15:43:56Z); 3/3 cited commits VERIFIED, 0 UNVERIFIABLE; cited-path vintage 8 attempted / 6 stable / 2 flagged (advi-insure-trigger-sequencing.json GONE; ADVI_INSURE.TO-H3-AE_PROOF_OF_SPEC.json GONE -- this order's own outputs, GONE by construction at cut); --no-packet (the caller's choice).
</preflight>

<proof_of_spec>
Criterion ids minted at cut by the issuer: `H3-AC1`..`H3-AC7`. The ASSIGNEE fills a `PROOF_OF_SPEC.schema.json` instance at
`org/tier2_senior/0.7.0_AE_CloudOps~U/deliverables/ADVI_INSURE.TO-H3-AE_PROOF_OF_SPEC.json` and validates it with
`.tools/proof-of-spec-check.py` BEFORE each phase's report; H3-AC6 stays UNCOMPUTABLE until the 09-04 fire and says so. The status flip is the issuer's.
</proof_of_spec>

<compiler_tools_mandate>
comp-trigger on `bd-49f-session-trigger` (the four answer-states by token) and comp-schedule before Phase 2; comp-read on every file you edit (`--for` the question you bring); comp-dataflow gate on the runner code if Phase 2 touches `data/*/scripts/`; comp-adversary compose on this order at read-vintage before Phase 2 starts.
</compiler_tools_mandate>

DELIVERABLE REPORT: two messages to 2.0.0_SA_COO (Phase 1 with the decision row; Phase 2 with the ledger, the apply file, the read-backs and the fire), each with hashes and push state LOCAL; the proof instance path above.
