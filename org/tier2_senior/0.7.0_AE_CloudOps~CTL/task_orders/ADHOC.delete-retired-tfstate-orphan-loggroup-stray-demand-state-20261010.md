# pipeline-override: one-off deletes outside any project round, on Andrew's explicit per-item delete word (record @d02b5d81e1 rows 8-10), routed by 1.0.0_SA_CTO msg 108155 to the laptop COO lane as issuer
<task_order id="ADHOC.delete-retired-tfstate-orphan-loggroup-stray-demand-state-20261010">
<to_id>ADHOC.delete-retired-tfstate-orphan-loggroup-stray-demand-state-20261010</to_id>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~CTL</issued_to>
<date>2026-10-10</date>
<status>complete</status>
<risk>WORLD</risk>

<closure>
COMPLETE (issuer, ~14:0xZ). AC1 is graded MET by the issuer's live re-read:
- T1, T2 and T4 `head-object` rc=255 (absent);
- T3 exact-name describe returns 0;
- controls: the state bucket still lists objects, and a sibling log group returns 1.
All four were absent from 13:56Z; ledger CLOSED; receipt
`org/tier2_senior/0.7.0_AE_CloudOps~CTL/deliverables/ADHOC_DELETES_20261010/RECEIPT.md` @46cca3496a. Recoverability:
T1, T2 and T4 left delete markers on versioned buckets, plus hashed copies; T3's 4,811 bytes are gone, with its metadata saved.
Two findings the order did not predict, both favouring the deletes:
- the retired roots are empty directory husks;
- T4's request keeps its live state under request_state/, so the deleted demand_state/ object was a stray.
</closure>

<title>Delete four approved AWS objects: two retired Terraform state objects, one orphan log group, one stray demand_state object -- read each first, delete, read the absence after</title>

<context>
Andrew answered the CTO's open-item list at ~13:3xZ. The record is
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261010_133xZ_FIFTEEN_OPEN_ITEMS_ANSWERED.md` @d02b5d81e1. His words,
verbatim: "8) agreed 9) delete 10) delete". The rows were raised by dell1 (cluster rows -bf6d / -838c / -5f4b, -c20b / -69ef,
-f23d). The CTO routed them in msg 108155. His word covers EXACTLY these four targets and nothing else:

| id | item | target |
|---|---|---|
| T1 | 8 | `s3://opal-313476888478-terraform-state/canonical-schwab-si2-schedule/tfstate` |
| T2 | 8 | `s3://opal-313476888478-terraform-state/opal-assets-absence/tfstate` |
| T3 | 9 | CloudWatch log group `/aws/lambda/opal-assets-absence-check` |
| T4 | 10 | `s3://opal-data-assets/bloomberg/global/silver/demand_state/request=ETFS_RIVALS-HISTORY-OWED-DAILY/state.json` |
</context>

<scope>
1. **Open ONE NEVER-2 ledger entry** before any act, naming the four targets as four legs.
2. **READ each target first, and print the result.** If any check fails for a target, do NOT delete that target: report it,
   and continue with the others.
   - **Exists.** T1, T2 and T4: `s3api head-object` (key, size, LastModified UTC, ETag, VersionId if the bucket is versioned);
     also read `get-bucket-versioning` for each bucket. T3: `logs describe-log-groups --log-group-name-prefix` with an exact-name
     match (storedBytes, creationTime, retention).
   - **Matches what was approved.** T1 and T2 are state files of RETIRED roots. A state whose `resources` list is NON-empty
     means live infrastructure may still be tracked: STOP for that target and report the resource count and types (never
     values). T3: the Lambda `opal-assets-absence-check` must NOT exist (`lambda get-function` returns ResourceNotFound); if
     it exists, STOP for T3.
   - **No reader.** T1 and T2: no `backend` block under `infra/` names either key; use `comp-find` with the key path, print
     the denominator, and run a positive control on a key you know is live. T4: no scheduled producer or consumer names the
     request id `ETFS_RIVALS-HISTORY-OWED-DAILY`; use `comp-find -i` with the denominator printed. A hit that is a live reader
     is a STOP for that target.
3. **SAVE before deleting** into this seat's deliverables folder, each with its SHA-256:
   - T1 and T2: the state file bytes (they hold no secret values by design; do not print them);
   - T4: `state.json`;
   - T3: the log group's metadata only, no events.

   These copies are the rollback. If a bucket is versioned, record the VersionId as the second rollback.
4. **DELETE** exactly the four targets (`s3api delete-object` with the exact key; `logs delete-log-group` with the exact
   name). No prefix delete, no wildcard, no `--recursive`.
5. **READ THE ABSENCE after**, with a positive control on the same instrument:
   - S3: `head-object` returns 404, or a delete marker on a versioned bucket (say which); a sibling object in the same prefix
     still reads 200.
   - Logs: an exact-name describe returns 0, and a sibling log group still returns 1.
6. Close the ledger entry with each leg's proof.
7. **Write a receipt** at `org/tier2_senior/0.7.0_AE_CloudOps~CTL/deliverables/ADHOC_DELETES_20261010/RECEIPT.md`: per target,
   the before read, the saved copy and its hash, the delete call, and the after read. Commit with `.tools/safe-commit.sh`, then
   report the receipt path, the commit and the measured push state to 2.0.0_SA_COO~C.
</scope>

<proof_of_spec>
<criterion id="AC1" cell_refs="ADHOC" judgment="true"/>
`AC1` -- each approved target is absent after the act, with a positive control on the same instrument, or STOPPED with the
reason. Graded by the issuer from the receipt and a live re-read.
</proof_of_spec>
<expected_criteria>AC1</expected_criteria>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~CTL/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~CTL/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
</paths>

<rules>
- Only these four targets; Andrew's word covers no other object.
- No secret value is read or printed.
- A STOP on one target never blocks the others.
</rules>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule changes; step 2 reads that no scheduled reader names T4.
comp-iam: DECLARED-NOT-APPLICABLE -- denominator: 0 policy changes; the seat's existing delete rights on two buckets and one log group. BLIND: whether those rights cover the state bucket; an AccessDenied is reported, never worked around.
comp-adversary: RUN -- 4 targets, each guarded: a prefix or recursive delete (forbidden; exact keys only); a state still tracking live resources (STOP when resources is non-empty); a live reader of the demand_state key (comp-find census plus positive control); a log group whose Lambda still exists (STOP); an unrecoverable delete (bytes saved and hashed first, plus VersionId where versioned). BLIND: readers outside this repository (another box's local scripts); the dell1 rows that raised these name none.
lane: ADHOC under Andrew's explicit delete word; the <paths> block is the grant.
</preflight>
</task_order>
