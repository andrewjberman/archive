# L8 drain end -- ADVI_COTBKF round 61

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~06:55 | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB61bi1-AC2 and CB61bi2-AC2)

Round 61 was cut as one issuance @28fbb42d46 on `1.0.0_SA_CTO~DELL2` ruling @27ba4d3769 (cross-box call
XB-20261011T055236Z-0989 from site Z): this project's CB-d-4 selector made every `shared-infra` plan fail.

| order | item | assignee | state |
|---|---|---|---|
| CB-bi-1 | the CRM-scope selector reads an explicit registry attribute under `one()` | ~88 | complete @84457822bb, drained @8c6fc7652a on the CTO's word (msg 4313) |
| CB-bi-2 | plan proof on the worker's worktree, no apply | `0.7.0_AE_CloudOps~CB2` | STOPPED and reported @6a87256d6e; `<status>` still `issued`; CB61bi2-AC1 reads FAIL as written |

**Mid-round rulings.** CB-bi-1 AMENDMENT 1 @0fbc02bf85: the schema owner's terms (laptop `1.0.0_SA_CTO`, relayed): a VIEW field
holding a list of `systems.json` keys. CB-bi-2 AMENDMENT 1 @6d616df83c: released on the worker's commit.

## The real run, shared tree at 8c6fc7652a, by the issuer

```
CRM-SCOPE-SELECT managed_firm_rows=2 rows_with_attribute=1 selector_lines=1 reads_attribute=True reads_masters=False postulates=4 census_tokens=4
lib/opal_naming.py validate: OK 54 system row(s), 14 scope row(s), 0 warning(s)
the two infra blobs at HEAD equal the blobs planned at 84457822bb
```

**The issuer ran NO terraform command.** Every `init`, `plan`, state and IAM read below is the applier's.

## For L9

**CB61bi1-AC2** (the row, the postulates, the census), from ~88's record
`deliverables/0.9.0_WK_ADVI_COTBKF~88/CRM_SCOPE_ATTRIBUTE_RULE24.json`:
- attribute `restricted_prefix_hosts`, a list of `systems.json` keys; its one value is present in `systems.json`;
- the row is the one the old selector chose before 5f962296ae (that commit added `masters` to one other managed row only);
- census before the edit: 0 hits in 79,319 files for the name and for two rejected candidates; 139 ephemeral-floor and 14,401 binary
  files not searched.

**CB61bi2-AC2** (the watched set's coverage and the control), from the applier's report
`deliverables/0.7.0_AE_CloudOps~CB2/shared_infra_plan_proof.md`:
- `CRM-PLAN resources=242 watched=12 watched_changed=2 other_changed=2`; the 12 watched addresses are listed there; both
  `aws_s3_bucket_policy.lgic_firm[...]` read no-op. The CRM statements are inline in one of those policies, not a resource.
- The 2 watched creates are the break-glass role and its inline policy: never applied (0 of 253 state rows; NoSuchEntity live).
- Control: at 28fbb42d46 the root fails at `init` with the `one()` error; the selected set is 2 rows, not the 3 the ruling counted.
- **CB61bi2-AC1 reads `watched_changed=2` against `watched_changed=0`: FAIL as the issuer wrote it.** The CTO ruled its own proof
  MET (msg 4313): the proof asked 0 changes to the statements and the firm bucket policies. The criterion was written wider than
  the proof; that is the issuer's wording error, and the order is not flipped on it.

## Rows of this round

- D2-S91 (applier, BLOCKING): the break-glass creates. D2-S92 (applier, ARMED, owner the CTO): a refreshing plan on dell2's
  credentials reads the portal bucket as deleted. The CTO ruled: no seat applies `shared-infra` from dell2 meanwhile.
- D2-S93 (issuer, BLOCKING): FWD-7's break-glass role exists in code only; its create is FWD-7's own never-widen act and pair,
  never a rider. Not read: whether any byte sits under the restricted prefix.

**Carried, not decided here:** the disposition of CB-bi-2's face (stopped, proof instance VALID with AC1 FAIL); the FWD-7 role act.

**Round-close check:** REFUSED on CB61bi1-AC2, which is ungraded (yours). It counts 1 judgment criterion; CB-bi-2's is not counted
while that order is not complete.
