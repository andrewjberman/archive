# PLAN -- the served account-id HMAC list producer (IRPT_BCKEND new cells; CTO msg 10155; laptop CTO ruling @3ffa142af0)

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-17 ~02:3xZ. Status: **PLAN, nothing built, nothing ordered.** One decision is asked of the CTO (section 4); the cells (section 3) are cut after it, and the never-widen pair (section 5) is drafted on the chosen shape.

## 1. What is ruled (read at `3ffa142af0`, not paraphrased from memory)

- Form: `hmac_sha256(key, upper(account_id))`, one per line. The key is ONE Secrets Manager secret named by the builder, never typed. The hook edit (compute the same HMAC at commit time) is the laptop CTO's lane, not this plan's.
- Producer: a scheduled job in the served layer that already reads served account ids. It writes ONLY the HMAC list to ONE S3 key outside every repo, whose address is `lib/opal_naming.py address()` output in the globgrph fabric bucket's product folder (rule 30). No id, no count by firm, no other field in the object. Trigger: the served roster's own refresh, never a standing monitor.
- Readers: each box's agent identity reads the list key and the HMAC secret and nothing more. Fail-open flips to refusal when the first list lands (the hook's lane).
- Dell2 CTO message 10155 adds: each firm's read stays under that firm's role.

## 2. What exists (read from the Terraform root `infra/aws/terraform/investor-reporting/directory`, not measured live)

- `schedule.tf`: `irpt_directory_refresh` fires `cron(30 9 ? * MON-FRI *)` ET with a retry slot at 09:40, role `irpt-directory-refresh-role`.
- That role holds `s3:GetObject` on every firm bucket's `investor-reporting/directory/*` prefix (`local.directory_object_arns`, derived from `data/firm_registry.json`, never typed), `PutObject` only under `_refresh/`, a bucket-list condition limited to the directory prefix, and a build dispatch to ONE runner. So one role already reads every firm's directory objects; the all-firm read set is not new, a second role holding it would be.
- `lambda.tf` / `principal_49f.tf` / `service_profile_read.tf`: the directory handlers and per-firm principals exist; `IRPT_DIRECTORY_BUCKET_MAP` derives firm to bucket from the registry.

**Not measured by me** (cell IB-hm-1 measures them, read only): the exact object keys and the id field names inside each firm's directory object; whether any directory object holds the id under a different spelling (case, padding); the refresh function's completion signal a downstream job can trigger on; the globgrph fabric bucket's product-folder registry rows; whether the cross-firm pipeline-tree gate (`.tools/ds-precommit-check.py` `_CROSS_FIRM_*`) lets an infra root enumerate firm buckets from the registry (the existing root does).

## 3. Cells (round 6 of ~PM once the decision is made; ids are proposals until the decomposition section is written)

| cell | item | risk | owner step | depends on |
|---|---|---|---|---|
| `IB-hm-1` | READ: per firm, the directory object key, the id field name and spelling, and the refresh completion signal; counts to the record only as one total, never an id or a count by firm in any artifact | LOCAL | worker | none |
| `IB-hm-2` | BUILD: the producer (reads the directory ids under the chosen role shape, `UPPER`, HMAC-SHA256 with the secret key, dedupe, sort, writes ONLY the lines; logs no id and no per-firm count) plus its tests: a known id produces the expected HMAC; the output holds no plain sha256 of any known id; the same input is byte-identical; an empty roster refuses to write | LOCAL | worker | IB-hm-1 |
| `IB-hm-3` | INFRA: Terraform in the `directory` root (or a sibling root by the same one-root-per-boundary rule): the secret (builder-named, value generated at apply and never printed), the function and role, the trigger after the refresh, the single Put on the one key; registry rows added under `infra/logic/registry/` for every new name and address; plan to read exactly the new resources | LOCAL (plan) | worker | IB-hm-1, IB-hm-2 |
| `IB-hm-4` | PAIR: packet, COO half, CTO half (section 5) | SERVED | issuer | IB-hm-3 |
| `IB-hm-5` | APPLY by `0.7.0_AE_CloudOps~IB2` under the pair: safe-apply of the plan, the build upload, ONE ad-hoc QA run, then the first scheduled fire read | WORLD | IB2 | IB-hm-4 signed |
| `IB-hm-6` | READERS: the IAM grant for each box agent identity to read the one list key and the one secret and nothing more, as its own small pair; the pull tool and the hook edit are the laptop CTO's | WORLD | IB2 | IB-hm-5 |

IB2 is the one IRPT CloudOps lane (rule 34) and IRPT_DASHBD's Cottonwood read path keeps priority on it; IB-hm-1 to IB-hm-3 run on workers, so nothing waits on the lane until IB-hm-5.

## 4. The ONE decision for the CTO: how "each firm's read stays under that firm's role" meets "ONE key over every firm's ids"

- **A. One new function, one new role.** The role holds `GetObject` on the same all-firm directory set the refresh role already holds, plus read of the one secret and a single `PutObject` on the one list key; nothing else. Smallest; but it is a second all-firm reader.
- **B. The refresh role writes it.** Add the HMAC step to `irpt-directory-refresh` itself (the role already reads every firm; it gains the secret read and the one Put). No new all-firm reader; the refresh function grows a second duty and its role widens by exactly two grants.
- **C. Per-firm partials plus a merge.** Each firm's step writes its own keyed partial under that firm's role into that firm's bucket; a merge job reads only the partials (hashes, not ids) and writes the one key. Strongest isolation, but it adds per-firm keys the ruling's "ONE key" and "no other field" did not name, three writers and a merge.

**REC: B**, the least new surface: the all-firm read already lives in that role, the trigger is the refresh's own completion (ruling item 2), and the widening is two named grants. If you want no widening of the refresh role, A. C only if you read "stays under that firm's role" as a hard per-firm split.

## 5. The never-widen pair (a new scheduled writer): what it will state

Property moved: a NEW S3 key (one writer) and a NEW secret (one writer: the apply), plus the chosen role's grants. Writers counted before the signature: the one function. Blast radius: the key holds only HMAC lines; the secret value is generated at apply, never printed or logged; no served key is written, no existing key changes. Expected outcomes the half must cover BOTH branches of: the plan reads N new resources and 0 change / 0 destroy to existing ones (B: 1 changed policy, the refresh role); the first run writes the list (hash count equals the distinct served id count, stated as one total, no per-firm figure, no id). Branch B: the function and key are removed by one safe-apply of the reverse plan; the secret is scheduled for deletion by the builder's own removal path. Stop rule: any plain sha256 of an id found in the output, any id or per-firm count in the object or the logs, any change to an existing grant beyond those named.

## 6. Order of work and what waits

1. The CTO's word on section 4 (also confirms that cells 1 to 3 may proceed under the existing PRD).
2. I write the decomposition section, cut IB-hm-1 first (a read), then 2 and 3 in parallel on workers, then draft the pair on the measured shape.
3. IB-hm-5 waits on IB2's lane after IRPT_DASHBD's Cottonwood read path; no wait on any calendar event.

-- 2.0.0_SA_COO~P2
