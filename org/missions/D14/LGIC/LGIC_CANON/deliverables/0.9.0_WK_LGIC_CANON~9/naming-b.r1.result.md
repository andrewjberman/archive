# naming-b.r1.result -- 0.9.0_WK_LGIC_CANON~9 on LGIC_CANON.TO-CN-n-2 (cell CN-n-2, round 1)

Worktree `.worktrees/wk-lgic-canon-1-9`, branch `wk-lgic-canon-1-9`, base `f95470f38400da6d2a40eeaa7469651e32ddb95e`
(the base CLOUD commit the order names; `git rev-parse HEAD` read it before any commit).

## What was done

The fixed naming job `org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/CN_NAMING_JOB.json`
(6 items, firm 49 Financial) was answered by CALLING the builders in `lib/opal_naming.py` at base, never by typing a
name. The firm's spelling comes from ONE registry row, `infra/logic/registry/scopes.json#49financial` (class FIRM,
tenancy FIRM, long `49financial`, short `49f`, bucket `opal-data-49financial`, tenant display_name `49 Financial`).
The builders write the LONG form in the bucket and key slots and the SHORT form in a resource name's scope slot
(NAMING_SCHEMA.json key.scope_form LONG, bucket.data_bucket_scope_form LONG, resource.scope_form SHORT).

| item | builder call (lib/opal_naming.py at base) | output |
|---|---|---|
| n1 | `lookup('49financial')['bucket']` (scopes.json row; opal-data-{scope}, LONG) | `opal-data-49financial` |
| n2 | `key('mdpf','49financial','gold','category_views','date=2026-09-15')` | `mdpf/49financial/gold/category_views/date=2026-09-15` |
| n3 | `address('advi','49financial','platinum','advisors','advisor_id=A123')` | `s3://opal-data-49financial/advi/49financial/platinum/advisors/advisor_id=A123` |
| n4 | `name('advi','49financial','dashboard-publish','lambda')` | `advi-49f-dashboard-publish-lambda` |
| n5 | `name('irpt','49financial','export','dlq')` | `irpt-49f-export-dlq` |
| n6 | `name('blackdiamond','49financial','session-runner','role')` | `blackdiamond-49f-session-runner-role` |

System keys are systems.json rows: `mdpf` (long model-portfolios), `advi` (advisor-intelligence), `irpt`
(investor-reporting), `blackdiamond` (VENDOR; the resource IS the vendor integration, NAMING_SCHEMA.json
system.vendor_as_system_only_when). Tier homes come from tiers.json homes.FIRM (gold and platinum: scope, i.e. the
firm bucket). Kinds: `lambda` (LAMBDA), `dlq` (SQS_QUEUE), `role` (IAM_ROLE) from NAMING_SCHEMA.json kind.by_type.

Supplementary read, not a criterion: `grade()` at base returns CONFORMANT for n1, n2, n4, n5 and n6 (5 of 6). n3 was
not graded: a platinum key's verdict turns on the legacy served-path list (NAMING_SCHEMA.json key.legacy_served_paths)
and the order asks for the builder output, which `address()` gave.

Answer file: `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/naming-b.tsv` (first line `# base <sha>`, then
6 rows `<id> TAB <answer> TAB registry: infra/logic/registry/scopes.json#49financial`).

Blindness kept: `CN_NAMING_KEY.json`, `naming-a.tsv` and `naming-compare.md` were not opened, and no other worktree or
git history was searched for them.

## Criteria (run in the worktree, bounded)

N2-AC1 -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py n2-named`

```
ITEMS: 6  NAMED FROM A CITED REGISTRY ROW: 6
VERDICT: PASS-NB-NAMES-CITED
rc=0
```

N2-AC2 -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py n2-base`

```
BASE: f95470f38400da6d2a40eeaa7469651e32ddb95e  resolves to a commit: True
VERDICT: PASS-NB-BASE-STATED
rc=0
```

Surprises: none filed.
