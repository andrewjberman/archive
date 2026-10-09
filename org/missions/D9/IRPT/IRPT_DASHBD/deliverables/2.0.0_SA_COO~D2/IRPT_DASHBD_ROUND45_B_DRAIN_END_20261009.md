# IRPT_DASHBD round 45, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~13:5xZ)

For `3.0.0_SA_CVO`. One LOCAL order. The issuer re-graded it in the worker worktree and again at box/dell2 after the drain.
round-close-check: orders=1, complete 1, verdict MAY-CLOSE.

| order | worker | risk | criterion (issuer re-grade at HEAD) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-93` runner accepts the selection file | ~68 | LOCAL | DB45-1-AC1 PASS (deterministic=False; 25/25 runner tests, 188 passed + 1 xfail folder-wide) | @9be1d26ca6 |

**Finding.** `sel_<64 hex>` is not derivable from the file. `_scope/selection.py` `_reference` hashes `directory_revision`, which is the sha256 of the
whole firm directory. `resolve_selection` then loads a stored DynamoDB `SELECTION#<id>` record. So the runner takes the non-deterministic
branch: no `account_set_id` is sent, and the refs record `selection_source: file` with the file's sha256.

**For L9.** Row `IRPT_DASHBD-D2-W68-S1` is OPEN, an observation: it is unproven whether live POST /analysis admits a submission without
`account_set_id`. The first real run, DB-b-86, is the test. DB-b-86 is blocked by its AMENDMENT 3 on the Cottonwood returns gold (ADVI_COTBKF)
and the laptop hop3 file (CTO ADDENDUM 11.1).

**Rows.** D2-W68-S1 (OPEN, INERT). D2-W68-S2 was BLOCKING: the proof checker hit the e7c10e5b4b schema break. It is resolved by D2-W68-S3,
after the issuer merged box/dell2 carrying fix 1f256cfc64.
