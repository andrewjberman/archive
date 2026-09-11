# IB-s-17 RESULT -- TENANT-SCOPED STORAGE, KEYS AND QUEUES: the core root applied once

**TO:** `IRPT_BCKEND.TO-IB-s-17` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-1-1`
**base commit:** `410f28f7db` (HEAD of `CLOUD` at hand-off, carrying the merged IB-s-18 foundation)
**This cell APPLIED infrastructure.** 17 resources added, 0 changed, 0 destroyed, under a change-management
entry opened before the act and closed and committed before the grading reads.

## Criteria

| id | verdict | invocation | deciding line |
|---|---|---|---|
| `S17-AC1` | **PASS-by-output** | `timeout 300 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_s_17.py` | rc=0, `arms: 5 of 5 evaluated; arms holding: 5 of 5; assertions failed: 0` then `IBS17-STORAGE-APPLIED` |
| `S17-AC2` | **PASS-by-output** | `timeout 120 .tools/terraform.exe -chdir=infra/aws/terraform/investor-reporting/core plan -no-color -input=false -lock=false` | rc=0, `No changes. Your infrastructure matches the configuration.` |
| `S17-AC3` | **RECORDED (judgment)** -- no verdict | evidence assembled for `3.0.0_SA_CVO` at L9 | in the proof-of-spec instance under `UNVERIFIABLE-BY-INSTRUMENT` |

Transcripts committed beside this file: `IB-s-17_S17-AC1_battery_output.txt`, `IB-s-17_S17-AC2_plan_output.txt`.

## What was applied

`safe-apply` rc=0: **`Apply complete! Resources: 17 added, 0 changed, 0 destroyed.`** The pre-apply plan read
`17 to add, 0 to change, 0 to destroy`, so no existing bucket, table, queue or key was in the blast radius.

- **KMS** one CMK `7f4d3042-10d8-49a7-b55e-3c963cea8111` + `alias/investor-reporting`; rotation measured
  ENABLED (365 d) **by key id**, because the CLI v1 shim refuses `get-key-rotation-status` on an alias.
- **S3** `opal-data-ycharts`, measured ABSENT (HeadBucket 404) before the act: SSE-KMS with that key, Block
  Public Access 4 of 4, versioning Enabled, and **0 objects** -- the prefixes are DECLARED in `layout.json`,
  never created as empty objects.
- **DynamoDB** `irpt-requests`, `irpt-jobs`, `irpt-outbox`, `irpt-checkpoints`: SSE-KMS with that key, PITR
  ENABLED, PAY_PER_REQUEST, 4 of 4. Every one tenant-partitioned except `irpt-checkpoints`, which is keyed by
  SOURCE because a mailbox delta cursor is not per-tenant.
- **SQS** `irpt-{intake,generation,export}` + one DLQ each: KMS, redrive `maxReceiveCount` 5,
  `MaximumMessageSize` 4096 on 6 of 6.

**The gates that ran, and what each one actually did.** The HALTGT checkpoint resolved this worker through a
NON-TERMINAL task order issued to it and then **scanned its ISSUER's inbox** -- `HALT-GATE: worker
0.9.0_WK_IRPT_BCKEND~1 has no inbox; scanning its issuer 2.0.0_SA_COO~B` -- which is the gate's designed
worker path, not a concession to one. `comp-tagauthz` PASSED with 0 candidate resources (this root creates no
`aws_instance`), having swept 229 roles and found 9 tag-conditioned statements. The tombstone gate checked 17
creates against 7 tombstones and read CLEAN. **No override was used anywhere**: no `HALT_ACK`, no
`TAGAUTHZ_OVERRIDE`, no `--force`, and `org/git-author-override-audit.log` carries no entry from this cell.

## The two mechanisms worth reading

**"Queues carry ids, not attachments" is a TRANSPORT REFUSAL here, not a convention.**
`max_message_size = 4096` means an attachment cannot fit: SQS itself rejects it at SendMessage, loudly, at the
producer. `keys.py queue_message()` refuses the same shapes for the same reason, so a producer that bypasses
the library still cannot put a payload on the queue.

**"Client names are never cache keys" has TWO arms and neither is a list of names.** A POSITIVE GRAMMAR (a
component is admitted by SHAPE; free text has no admissible shape) and a REGISTRY-DERIVED NEGATIVE (firm ids,
aliases, tree tokens and e-mail-domain labels read live from `data/firm_registry.json`, matched whole-token).
CLAUDE.md section 5 says an enumerated ban list lapses silently when a name changes; neither arm is an
enumeration, so neither can lapse.

**A hole the tests caught, named rather than quietly patched.** The first draft's parameter ladder ended in
`REVISION_RE`, and `"Smith-Family"` is a well-formed revision token -- so the grammar ADMITTED a dashed human
name. The test failed, the ladder now ends in an enum token, and the reason is a comment at the site. A
revision belongs in its own named position, where it is a revision by construction.

## Rows filed

- `IRPT_BCKEND-W1-S3` (OBSERVATION, INERT) -- safe-apply's FIRST identity gate refused fail-closed until
  `org/mcp/sessions/<session>.serial` named the acting serial (`OPAL_AGENT_SERIAL` satisfies only the second
  gate). That file is gitignored, has no commit plane, and the gate prints its own one-line remedy. Also names
  the coupling: the gate admits a worker only while a task order issued to it is NON-TERMINAL, so **a worker's
  own complete flip withdraws its apply grant** and every apply must precede the flip.
- `IRPT_BCKEND-W1-S4` (OBSERVATION, INERT) -- `**/.terraform.lock.hcl` is ignored at `.gitignore:206` while 35
  sibling roots track one, so this root's provider pins (aws 5.100.0, local 2.9.1) live only in the worktree
  and in this cell's ledger entry. Not fixed: both coherent remedies are neighbouring defects.
- `IRPT_BCKEND-W1-S5` (OBSERVATION, INERT) -- IB-s-18's arm (d) asserts no root is initialised, and this cell
  initialised `core/`. Measured mitigation rather than assumed: `.terraform/` is gitignored and the backend is
  S3, so a re-grade from a fresh worktree still passes; only a re-run in a used worktree reads a false FAIL.

## Bounds observed

One root applied and no other. No firm-specific data written -- the bucket carries 0 objects. The firm list is
READ from the registry at plan time (3 of 3 enabled client firms), never typed. No IAM role, no bucket policy
and no key-policy grant created: `comp-iam` reads ZERO investor-reporting roles, so there is no principal to
grant to, and IB-s-5 owns the per-firm conditions. No monitor, alarm, SNS or SES send -- a DLQ is a durable
place a person reads, not a notification. No live vendor call, no mailbox read, no credential in any artifact.
No served output touched. `.tools/safe-apply.sh` only, `.tools/terraform.exe` by its provisioned path. Every
`.py` passed `.tools/commit-gate.sh`. Every invocation ran under `timeout`.
