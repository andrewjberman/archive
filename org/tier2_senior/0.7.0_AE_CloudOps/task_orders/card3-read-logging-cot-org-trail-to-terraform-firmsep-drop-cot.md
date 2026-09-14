# TO card3-read-logging -- READ LOGGING ON: opal-data-cot into the organisation trail's read selector, the trail brought under Terraform by a 0-diff import FIRST, the firm-bucket template given read logging, and opal-data-cot DROPPED from FIRMSEP-s3-direct-access-bypass in the SAME change

<task_order>
<id>2.0.0_SA_COO~E-2026-09-13-card3-read-logging</id>
<project>NONE -- a non-pipeline order on Andrew's card-3 ruling. It serves ADVI_FIRMBKTS FWD-6 and MDPF_CANON FWD-8 as an INPUT and is a cell of neither (see WHY NON-PIPELINE below)</project>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO~E</issued_by>
<date>2026-09-13</date>
<status>complete -- 0.7.0_AE_CloudOps 2026-09-14 ~01:5xZ. Proof-of-spec VALID rc=0 (deliverables/CARD3_READ_LOGGING/CARD3_READ_LOGGING_PROOF_OF_SPEC.json: 16 of 16 rows, 0 violations; 15 mechanical rows PASS; R-AC15 is judgment, recorded UNVERIFIABLE-BY-INSTRUMENT for 2.0.0_SA_COO~E at RAVC-4). Terraform landed at 9f3fd2cf4a (import) and 37931439cf (S3), both on origin/CLOUD; ledger card3-read-logging CLOSED 5/5. PRIOR: pending -- GO CARRIED ON THIS FACE by the issuer 2026-09-13 ~22:5xZ, because it cannot ride the broker. The LD-0529 send gate admits a GO only if it cites `<PROJECT>.TO-<id>` (org/mcp/cvo_send_guard.py:152-156, TO_ID_RE), and a code-less order like this one cannot carry that token. So the GO message was REFUSED ("cites NO task order"), and the act lives here, in the recipient's own home -- which is what LD-0529 requires.</status>
<priority>P1 -- ADVI_FIRMBKTS FWD-6's 45-day quiet-window clock does not start until this lands</priority>

## AUTHORITY -- FOUR ANDREW-DIRECT WORDS, EACH IN ITS OWN RECORD, NONE WIDENED HERE

1. **~18:4xZ 2026-09-13, "recs approved"**, card 3 of 7, REC verbatim: *"Yes: add cot to the audit trail's read logging, move that setting into Terraform, and give the bucket template read logging. It only records reads and sends nothing, so it is not an alert, but the logging is billed, which makes it your word."* Record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260913_184xZ_OPEN_CALLS_ALL_SEVEN_RECS_APPROVED.md` @`e2210bf34c`. Card 2 of the same frame: the quiet window is **45 days, counted from when read logging is live**.
2. **~19:0xZ, "yes to both"** -- seat `0.7.0_AE_CloudOps` for this item, under that lane's own apply rules (safe-apply, change-management entry). Same record, @`82c00bd4ef`.
3. **~20:1xZ, "if its not registered to a fabric in directives its not in contention"** -- the base seat is a legal addressee. Same record.
4. **~21:3xZ, "yes 2 all"**: card 2 seats a `2.0.0_SA_COO` lane to write THIS ONE order; card 3 rules remedy **(a)** -- *drop `opal-data-cot` from `FIRMSEP-s3-direct-access-bypass`'s bucket list in the SAME change that turns on cot read logging.* **bd and inf stay in the rule; the rule is not disabled, rescoped or repaired; its SNS legs stay as they are; whether the rule should exist is NOT ruled.** Record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260913_213xZ_MACROS_RATIFIED_COO_SEAT_FIRMSEP_DROP_COT.md` @`464c1096d5`.

Issuer `2.0.0_SA_COO~E`, seated by `0.0.0_AB_MSTR` on word 4; its scope is this one order.

## WHY NON-PIPELINE -- DISCLOSED, NOT GLOSSED

At ~20:1xZ `1.0.0_SA_CTO` recorded this as a non-pipeline order. **Since then `ADVI_FIRMBKTS` was registered (@`f25395446e`, `dep_stage=REGISTERED`, no PRD, no decomposition).** Filing this order under that code would claim it is a decomposed cell of that project, which it is not -- it is a direct ruling on the infrastructure plane that FWD-6 depends on -- and three issuance hooks would correctly refuse it for lacking a decomposition that does not exist. So `<project>` reads NONE and the filename carries no project code. The audited `# pipeline-override:` line below covers `to-pipeline-gate.py` layer 3 only; `<proof_of_spec>` and `<preflight>` are PRESENT and are not overridden.

## THE STATE THIS STARTS FROM -- 0.7.0_AE_CloudOps's OWN PRE-ORDER READ (msg 96399, ~20:1x-20:2xZ), RE-ESTABLISHED BY R-AC1 BEFORE ANY EDIT

- `opal-organization-trail` (multi-region, `IsOrganizationTrail=false`), `get-event-selectors`: [management, All] + [data, **ReadOnly**, `AWS::S3::Object`, `arn:aws:s3:::opal-data-bd/`, `arn:aws:s3:::opal-data-inf/`]. Set by CLI 2026-05-11 (`infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:208-212`). **Not in Terraform**: the only `aws_cloudtrail` in the tree is `served_key_write` (`globgrph/item2e_served_write_trail.tf:110`). Cross-check at the issuer's seat: `comp-find --corpus aws 'opal-organization-trail|FIRMSEP-s3-direct-access-bypass'` returned 1 hit across 2,531 AWS nodes (vintage 2026-09-13 12:15:54Z), the rule only -- **the trail is OUT-OF-CORPUS on that plane, not absent**; your live `describe-trails` is the authority.
- `opal-data-cot` has NO read data events on any trail (`opal-served-key-write-trail` logs cot WRITES under `platinum/firm/` only).
- `opal-data-49financial` is the bucket `infra/aws/terraform/shared-infra/s3-49financial.tf` (the firm-bucket template) mints; it has no read logging, and the template provisions no read instrument (`3.0.0_SA_CVO` @`614423c438`).
- `FIRMSEP-s3-direct-access-bypass` (`cloudwatch-alarms.tf:219-238`, drift=DECLARED) is ENABLED, matches `GetObject` on `["opal-data-bd","opal-data-inf","opal-data-cot"]` with a non-CloudFront userAgent, and targets SNS `opal-infrastructure-alerts`. Issuer's `comp-blast` at the same vintage: 1 downstream node, that topic. It sends nothing today only because two legs are broken in series (EventBridge->SNS fails on every invocation; SNS->SMS). Its cot arm is dormant only because cot has no data events -- **this order is what would arm it, which is why remedy (a) rides the same change.**

## THE WORK -- IN THIS ORDER

**S0.** Open the change-management ledger at START: `python .tools/deploy_ledger.py open --slug card3-read-logging --author 0.7.0_AE_CloudOps --title "..." --leg ...`, one leg per act below, each apply leg naming its rollback:
- git -- the commit(s) carrying the Terraform.
- activation, portal-auth -- the FIRMSEP pattern narrowed. ROLLBACK: restore the pattern from `rule_pre.json`.
- activation, trail import -- `terraform import` of the `aws_cloudtrail` resource only. ROLLBACK: `terraform state rm` (no AWS change).
- activation, trail selector -- cot and 49financial added to the ReadOnly selector. ROLLBACK: `put-event-selectors` from `selectors_pre.json`.
- verify -- R-AC6 through R-AC13, and R-AC16 (added ~23:5xZ on route (a)).

**S1. CAPTURE PRE-STATE** into `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/`: `selectors_pre.json` (get-event-selectors), `trail_pre.json` (describe-trails), `rule_pre.json` (describe-rule), `targets_pre.json` (list-targets-by-rule). **The pre-captures are the rollback artifacts and the differential baselines.** Then one test `GetObject` on a small `opal-data-cot` object at T0, recorded (the negative arm, R-AC9).

**S2. IMPORT THE TRAIL TO A 0-DIFF PLAN, BEFORE ANY SELECTOR CHANGE.** Module: `shared-infra`, per the 2026-06-30 `1.0.0_SA_CTO` ruling quoted at `globgrph/item2e_served_write_trail.tf:15-18` that calls the org trail "shared-infra/security-TF" -- and it is also the template's module. If you find a reason it cannot live there, record the module chosen and why in the ledger entry. The declared config reproduces the live trail EXACTLY, basic `event_selector` blocks included. Import the `aws_cloudtrail` resource ONLY -- its log bucket, bucket policy, KMS key and any other dependency stay unmanaged, referenced by literal. R-AC2 gates S3.

**S3. ONE CHANGE, ONE COMMIT, ONE LEDGER ENTRY, TWO APPLIES IN THIS ORDER:**
- (a) `cloudwatch-alarms.tf:229`: `bucketName = ["opal-data-bd", "opal-data-inf"]`. Nothing else on the rule or its target changes. The `:216` comment may record the drop and cite this order. **safe-apply portal-auth FIRST.**
- (b) The trail's ReadOnly data selector gains `arn:aws:s3:::opal-data-cot/` and `arn:aws:s3:::opal-data-49financial/`; `bd/` and `inf/` are untouched. **safe-apply the trail module SECOND** -- so the rule never sees a cot data event (R-AC5).
- (c) The template carries the read-logging declaration so that a bucket minted by copying `s3-49financial.tf` is born inside that ReadOnly selector. **The mechanism is yours** -- name it and the copy step in the ledger entry. Graded as R-AC15 (judgment).

**S4. EXERCISE.** One test `GetObject` each on `opal-data-cot` and `opal-data-49financial` at T1 after the trail apply. After CloudTrail delivery (allow ~15 min -- a delivery latency on an act you drove, not a wait), read the trail's DELIVERED log objects for them (R-AC10, R-AC11), with the bd positive control (R-AC8).

**S5. CLOCK START -- REPORT, STAMP NOTHING.** `1.0.0_SA_CTO` has decided which value starts the clock (msg 96424; a ruling line on ADVI_FIRMBKTS's tree row @`34ca8cab31`), verbatim: **"LIVE MEANS OBSERVED RECORDING, NOT APPLIED CONFIGURATION."** Each bucket's 45-day window starts at the eventTime of the FIRST data event for THAT bucket observed on the trail, never at the apply time. The probe read is excluded from the quiet census by its principal and eventTime, and nothing else is. So report, per bucket (opal-data-cot, and opal-data-49financial for the record):
- (i) the trail apply's completion time (UTC), as context only;
- (ii) the first observed data event's `eventTime` and `userIdentity.arn`, and whether it is your probe or organic -- an organic first event still starts the clock and stays in the census;
- (iii) EVERY probe read you made -- the T0 negative-arm read and each T1 read -- with its principal ARN and eventTime as its delivered record carries them. The T0 read has no record (R-AC9), so report its principal and the time you made it.
The census excludes exactly the probes you list.

**S6.** Close every ledger leg with proof, then `deploy_ledger.py close`.

## THE ONE SCRIPT THE CRITERIA NAME

Author `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py` and commit it, so every criterion is re-runnable by the validator. Output contract, one line per call:
- `events --bucket B --since ISO [--until ISO]` -> `DATA_EVENTS bucket=B n=<int> first=<eventTime|none>`. It reads the org trail's delivered log objects (bucket from `describe-trails ... S3BucketName`), filtering `eventCategory=Data`, `eventName=GetObject`, `requestParameters.bucketName == B`, `eventTime` in window. It must NOT read `opal-served-key-write-trail`'s bucket, and it must never count a write.
- `order --since ISO` -> `ORDER putrule=<t|none> puteventselectors=<t|none> rule_first=<true|false|unknown>`, from `lookup-events` (management events) for PutRule on the rule and PutEventSelectors on the trail. **`unknown` when either event is not found** -- a missing event is not a pass.
- `same-rule <rule_pre> <rule_post> <targets_pre> <targets_post>` -> `RULE_UNCHANGED_EXCEPT_BUCKETS=<true|false>`: every rule field, the event pattern with its bucketName list removed, and the target list compared byte-for-byte.
- `same-trail <selectors_pre> <selectors_post> <trail_pre> <trail_post>` -> `TRAIL_UNCHANGED_EXCEPT_READ_VALUES=<true|false>`: everything except the ReadOnly selector's `Values` list compared byte-for-byte (the management selector, ReadWriteType, multi-region, log bucket, KMS, log group).

<compiler_tools_mandate>
  <phase id="1" when="before any edit">
    <step>
      <run>comp-blast FIRMSEP-s3-direct-access-bypass</run>
      <expect>Exactly 1 downstream node, SNS_TOPIC opal-infrastructure-alerts (the issuer's read at vintage 2026-09-13 12:15:54Z).</expect>
      <if_mismatch>STOP. A new consumer of the rule changes what remedy (a) covers; report it to 2.0.0_SA_COO~E before editing.</if_mismatch>
    </step>
    <step>
      <run>aws cloudtrail describe-trails --trail-name-list opal-organization-trail</run>
      <expect>One trail; IsMultiRegionTrail true; IsOrganizationTrail false; HomeRegion and S3BucketName recorded in the ledger entry.</expect>
      <if_mismatch>STOP. The import target is not the trail 96399 measured.</if_mismatch>
    </step>
    <step>
      <run>R-AC1's invocation (the ReadOnly selector values, sorted)</run>
      <expect>Exactly bd/ and inf/.</expect>
      <if_mismatch>STOP and report. Another act has moved the selector and this order's premise is falsified; do not "correct" it.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before each apply">
    <step>
      <run>.tools/safe-apply.sh -chdir=infra/aws/terraform/portal-auth apply -target=aws_cloudwatch_event_rule.firmsep_s3_bypass   (its plan, read before approving)</run>
      <expect>Exactly 1 in-place update, aws_cloudwatch_event_rule.firmsep_s3_bypass; 0 to add; 0 to destroy. ROUTED 2026-09-13 ~23:5xZ by 2.0.0_SA_COO~E on 0.7.0_AE_CloudOps's HOLD (msg 96438, route (a)). The untargeted portal-auth plan carries one PRE-EXISTING, unrelated in-place update: aws_wafv2_web_acl.opal_cloudfront_protection (row ADVI_FIRMBKTS-S1 @926e18a2ce). Its managed-rule blocks plan as remove-and-re-add, with content equal to live. This order does NOT apply that update, so the portal-auth apply is TARGETED at the rule. safe-apply forwards its arguments to terraform (.tools/safe-apply.sh:274, :291).</expect>
      <if_mismatch>STOP. Anything in the targeted plan beyond the one rule update is not this order's; surface it as a row and hold.</if_mismatch>
    </step>
    <step>
      <run>safe-apply's plan for the trail module after the S3 edit</run>
      <expect>One in-place update of the imported aws_cloudtrail (the ReadOnly selector values), plus only the resources your S3(c) mechanism names; 0 destroy; no replace of the trail.</expect>
      <if_mismatch>STOP. A trail REPLACE would recreate the organisation audit trail -- never apply it.</if_mismatch>
    </step>
    <step>
      <run>comp-iam gaps</run>
      <expect>DECLARED-NOT-APPLICABLE unless your mechanism touches iam.tf; if it does, no new gaps.</expect>
      <if_mismatch>STOP. This order grants nothing.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after both applies">
    <step>
      <run>R-AC3 through R-AC14, then R-AC16, in order</run>
      <expect>Each matches its expect below.</expect>
      <if_mismatch>Roll back per the ledger leg that failed; report the failure to 2.0.0_SA_COO~E. Never leave one apply landed and the other not: if the trail apply fails after portal-auth landed, the rule is narrowed and nothing is armed, so report the failure and hold -- that half-state is safe. The reverse order is the one this sequence exists to prevent.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule, cron, cadence or trigger is created or changed. The one EventBridge rule touched is an event-PATTERN rule, and the change NARROWS its match set by one bucket.
comp-iam: DECLARED-NOT-APPLICABLE -- no role, policy or grant is authored or changed. CloudTrail data events need no new permission, and the test reads use the operator's existing principal. Re-opened by the Phase 2 step if the S3(c) mechanism touches iam.tf.
comp-adversary: DECLARED-NOT-APPLICABLE -- every figure inherited on this face (the selector values, the rule's bucket list, its one consumer) is either re-derived at the issuer's seat with its vintage printed (comp-blast, comp-find --corpus aws) or re-established at the assignee's own vintage by R-AC1 and Phase 1 before any edit. Nothing is carried forward on trust.
</preflight>

# pipeline-override: this order stands OUTSIDE the pipeline by construction -- it is Andrew's card-3 ruling (~18:4xZ "recs approved", remedy (a) ~21:3xZ "yes 2 all"), written by a COO lane he seated for exactly this one order, addressed to the seat he approved (~19:0xZ "yes to both"). It is not a cell of ADVI_FIRMBKTS, whose registration (@f25395446e, dep_stage REGISTERED) came after 1.0.0_SA_CTO recorded this as a non-pipeline order at ~20:1xZ, and whose PRD and decomposition do not exist. Filing it under that project to satisfy layer 3 would assert a decomposition that is not there. <preflight> and <proof_of_spec> are PRESENT and not overridden; only layer 3's project-row limb is.

<proof_of_spec>
<expected_criteria>R-AC1,R-AC2,R-AC3,R-AC4,R-AC5,R-AC6,R-AC7,R-AC8,R-AC9,R-AC10,R-AC11,R-AC12,R-AC13,R-AC14,R-AC15,R-AC16</expected_criteria>

<criterion id="R-AC1" judgment="false">
  <invocation>aws cloudtrail get-event-selectors --trail-name opal-organization-trail --query "EventSelectors[?ReadWriteType=='ReadOnly'].DataResources[].Values[]" --output text | tr -d '\r' | tr '\t' '\n' | sort | tr '\n' ' '</invocation>
  <expect>^arn:aws:s3:::opal-data-bd/ arn:aws:s3:::opal-data-inf/ ?$</expect>
</criterion>
<criterion id="R-AC2" judgment="false">
  <invocation>terraform -chdir=infra/aws/terraform/(trail module) plan -detailed-exitcode -input=false; echo "PLAN_RC=$?"   (run after the import and BEFORE the S3 edit; record the module path you used)</invocation>
  <expect>PLAN_RC=0(?![0-9])</expect>
</criterion>
<criterion id="R-AC3" judgment="false">
  <invocation>aws events describe-rule --name FIRMSEP-s3-direct-access-bypass --query EventPattern --output text</invocation>
  <expect>"bucketName":\s*\["opal-data-bd",\s*"opal-data-inf"\]</expect>
</criterion>
<criterion id="R-AC4" judgment="false">
  <invocation>python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py same-rule rule_pre.json rule_post.json targets_pre.json targets_post.json   (FORBIDDEN SHORTCUT: disabling or deleting the rule, or dropping bd/inf, also removes cot -- this is the criterion that fails on it)</invocation>
  <expect>RULE_UNCHANGED_EXCEPT_BUCKETS=true</expect>
</criterion>
<criterion id="R-AC5" judgment="false">
  <invocation>python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py order --since (S0's ledger-open time)</invocation>
  <expect>rule_first=true</expect>
</criterion>
<criterion id="R-AC6" judgment="false">
  <invocation>aws cloudtrail get-event-selectors --trail-name opal-organization-trail --query "EventSelectors[?ReadWriteType=='ReadOnly'].DataResources[].Values[]" --output text | tr -d '\r' | tr '\t' '\n' | sort | tr '\n' ' '   (FORBIDDEN SHORTCUT: a prefix or wildcard selector over opal-data-*, or conversion to advanced selectors -- the first logs all 20 opal-data-* buckets, which nobody ruled; either one empties this read)</invocation>
  <expect>^arn:aws:s3:::opal-data-49financial/ arn:aws:s3:::opal-data-bd/ arn:aws:s3:::opal-data-cot/ arn:aws:s3:::opal-data-inf/ ?$</expect>
</criterion>
<criterion id="R-AC7" judgment="false">
  <invocation>python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py same-trail selectors_pre.json selectors_post.json trail_pre.json trail_post.json</invocation>
  <expect>TRAIL_UNCHANGED_EXCEPT_READ_VALUES=true</expect>
</criterion>
<criterion id="R-AC8" judgment="false">
  <invocation>python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py events --bucket opal-data-bd --since (T0) --until (T0 + 30 min)   (POSITIVE CONTROL: bd is already logged and read about 250K times a day, so a zero here means the scanner is blind and R-AC9's zero proves nothing)</invocation>
  <expect>DATA_EVENTS bucket=opal-data-bd n=[1-9]</expect>
</criterion>
<criterion id="R-AC9" judgment="false">
  <invocation>python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py events --bucket opal-data-cot --since (T0) --until (the trail apply's start)   (NEGATIVE ARM: the T0 test read happened in this window and must NOT appear)</invocation>
  <expect>DATA_EVENTS bucket=opal-data-cot n=0(?![0-9])</expect>
</criterion>
<criterion id="R-AC10" judgment="false">
  <invocation>python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py events --bucket opal-data-cot --since (T1)   (FORBIDDEN SHORTCUT: counting cot WRITES from opal-served-key-write-trail -- the script's filter excludes both)</invocation>
  <expect>DATA_EVENTS bucket=opal-data-cot n=[1-9][0-9]* first=20[0-9][0-9]-</expect>
</criterion>
<criterion id="R-AC11" judgment="false">
  <invocation>python org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/card3_probe.py events --bucket opal-data-49financial --since (T1)</invocation>
  <expect>DATA_EVENTS bucket=opal-data-49financial n=[1-9][0-9]* first=20[0-9][0-9]-</expect>
</criterion>
<criterion id="R-AC12" judgment="false">
  <invocation>terraform -chdir=infra/aws/terraform/portal-auth plan -target=aws_cloudwatch_event_rule.firmsep_s3_bypass -detailed-exitcode -input=false; echo "PLAN_RC=$?"   (RE-CUT ~23:5xZ on route (a): the rule's declared state equals live. The pre-existing WAF diff belongs to R-AC16, not this criterion.)</invocation>
  <expect>PLAN_RC=0(?![0-9])</expect>
</criterion>
<criterion id="R-AC16" judgment="false">
  <invocation>terraform -chdir=infra/aws/terraform/portal-auth plan -input=false -no-color | tr -d '\r' | grep -E '^  # .* (will be|must be) ' | tr '\n' '|'   (DIFFERENTIAL, after the targeted apply: the untargeted plan carries EXACTLY the one pre-existing WAF update that row ADVI_FIRMBKTS-S1 records, and nothing this order introduced)</invocation>
  <expect>^  # aws_wafv2_web_acl\.opal_cloudfront_protection will be updated in-place\|$</expect>
</criterion>
<criterion id="R-AC13" judgment="false">
  <invocation>terraform -chdir=infra/aws/terraform/(trail module) plan -detailed-exitcode -input=false; echo "PLAN_RC=$?"   (after the trail apply)</invocation>
  <expect>PLAN_RC=0(?![0-9])</expect>
</criterion>
<criterion id="R-AC14" judgment="false">
  <invocation>python -c "import pathlib; s=pathlib.Path('org/critical_paths/.open_deploys/card3-read-logging.json'); e=sorted(pathlib.Path('org/critical_paths/change_management').glob('*card3-read-logging*')); print('SENTINEL', 'ABSENT' if not s.exists() else 'PRESENT', 'ENTRIES', len(e), 'CLOSED' if e and 'CLOSED' in e[-1].read_text(encoding='utf-8') else 'NOT-CLOSED')"</invocation>
  <expect>SENTINEL ABSENT ENTRIES 1 CLOSED</expect>
</criterion>
<criterion id="R-AC15" judgment="true"><!-- The template carries read logging so that a bucket minted by COPYING s3-49financial.tf is born inside the ReadOnly selector, with no edit anywhere the copier would not be led to. That is FWD-6's precondition at mint, and CloudTrail data events do not backdate. Graded by 2.0.0_SA_COO~E at RAVC-4 against the mechanism named in the ledger entry. NOT self-graded: record UNVERIFIABLE-BY-INSTRUMENT with a status_reason naming 2.0.0_SA_COO~E. --></criterion>

<instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/CARD3_READ_LOGGING_PROOF_OF_SPEC.json</instance_path>

Validate BEFORE the complete flip, positional id set, taking the rc without a pipe: `python .tools/proof-of-spec-check.py org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/CARD3_READ_LOGGING_PROOF_OF_SPEC.json "R-AC1,R-AC2,R-AC3,R-AC4,R-AC5,R-AC6,R-AC7,R-AC8,R-AC9,R-AC10,R-AC11,R-AC12,R-AC13,R-AC14,R-AC15,R-AC16"`. The parenthesised values -- the trail module, T0, T1, the ledger-open time and the apply times -- are yours to fill, and each is recorded in the instance as the value used.
</proof_of_spec>

<acceptance_criteria>
The sixteen criteria above, one clause each. Also: the session log's Compiler Tools section reproduces every `<run>` in the mandate with its observed output and pass/fail against its `<expect>`. Missing rows = REWORK. The completion report carries S5's per-bucket report and the push state as a MEASURED value (ls-remote read).
</acceptance_criteria>

<do_not>
  <rule>Do not add any subscriber, alarm, metric filter, EventBridge rule or other consumer of the new data events. This is logging, and Andrew's word covers logging only (CLAUDE.md alert moratorium).</rule>
  <rule>Do not repair, rescope, disable or re-target FIRMSEP-s3-direct-access-bypass beyond removing opal-data-cot. That includes its EventBridge-to-SNS leg and the topic policy. Its future is NOT ruled.</rule>
  <rule>Do not touch the SMS leg or the d12 ledger (org/critical_paths/.open_deploys/d12-sms-tfn-registration-and-production-access.json -- LD-0537, 0.0.0_AB_MSTR's).</rule>
  <rule>Do not add any opal-data-* bucket beyond cot and the template's opal-data-49financial (20 exist; bd and inf are already present). Do not use a prefix or wildcard selector. Do not convert the trail's basic selectors to advanced ones.</rule>
  <rule>Do not import or modify the trail's log bucket, its policy, a KMS key or opal-served-key-write-trail. Import the aws_cloudtrail resource only.</rule>
  <rule>Do not sweep unrelated portal-auth or shared-infra drift into either apply. This order does NOT apply the pre-existing aws_wafv2_web_acl.opal_cloudfront_protection update (row ADVI_FIRMBKTS-S1); disposing of it is that row's owner's job.</rule>
  <rule>Do not push. CLOUD is pushed only by 0.0.0_AB_MSTR on Andrew's word (LD-0522). Commit, and state the push state as LOCAL with the ls-remote hash.</rule>
  <rule>Do not touch the base seat's five other non-terminal orders (96399 FLAG B). They are out of contention by Andrew's ~20:1xZ word.</rule>
</do_not>

<surprise_channel>
Anything odd off-task: append ONE row (spec_asserts + world_is) to `org/missions/D8/ADVI/ADVI_FIRMBKTS/surprise-channel/investigations/INVESTIGATION_v1.md` (lane ANY; your row creates the file if absent) and keep working. This order serves that project's FWD-6, which is why its channel is the one named. A broker message is never the carrier. An ARMED hazard disarms same-turn via the row's disarm_owner.
</surprise_channel>

<paths>
infra/aws/terraform/portal-auth/cloudwatch-alarms.tf
infra/aws/terraform/shared-infra/  (the imported trail's file, the s3-49financial.tf template edit, and the stack's CHANGELOG.json -- or the module you record in the ledger entry)
infra/aws/terraform/portal-auth/CHANGELOG.json
org/critical_paths/change_management/  and  org/critical_paths/.open_deploys/card3-read-logging.json
org/tier2_senior/0.7.0_AE_CloudOps/deliverables/CARD3_READ_LOGGING/
org/tier2_senior/0.7.0_AE_CloudOps/task_orders/card3-read-logging-cot-org-trail-to-terraform-firmsep-drop-cot.md  (the status flips only)
org/tier2_senior/0.7.0_AE_CloudOps/logs/
org/missions/D8/ADVI/ADVI_FIRMBKTS/surprise-channel/investigations/INVESTIGATION_v1.md  (rows only)
</paths>

<completion>
`<status>` reads pending at issue: the GO is on this face (see the status line for why it could not ride the broker). -> complete ONLY with a VALID proof-of-spec instance (rc=0). Then one message to 2.0.0_SA_COO~E carrying: the commit hash(es); the push state, measured; S5's per-bucket report, each probe's principal and eventTime included; the validator's rc; and the S3(c) mechanism. 2.0.0_SA_COO~E validates (RAVC-4), grades R-AC15, and relays S5's report to 1.0.0_SA_CTO, whose ruling (96424 @34ca8cab31) sets the FWD-6 clock.
</completion>
</task_order>
