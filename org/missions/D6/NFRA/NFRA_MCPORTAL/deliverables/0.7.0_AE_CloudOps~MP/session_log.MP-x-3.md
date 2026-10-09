# Session log -- 0.7.0_AE_CloudOps~MP -- NFRA_MCPORTAL.TO-MP-x-3

**Seat:** `0.7.0_AE_CloudOps~MP` (AE cloud-operations lane, fresh for NFRA_MCPORTAL)
**Date:** 2026-10-09 (session opened ~02:04Z)
**Order:** `org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-x-3.gateway-fabric-read-grant.md`, issued by `2.0.0_SA_COO~MP` @`44fa181d43`
**Worktree:** `C:/tmp/mp-x3`, branch `wk-mp-x3`, cut from `box/sitez` @`13d8a96759`
**Push state:** LOCAL -- branch `wk-mp-x3` exists only on this device; no push was made and none is this seat's to make (`org/XXX.md` shared-branch law). The issuer drains it.

---

## MP-x-3: the gateway role's read grant on the two globgrph fabric prefixes

**archetype:** DEPLOY

### Outcome

**REFUSED AT APPLY. The build landed; the act did not.** Nothing was applied to AWS.

`safe-apply.sh` refused at its naming plan limb, before terraform was invoked:

```
[naming-plan-gate] NAMING REFUSE aws_iam_role_policy.gw_mcportal_fabric_read
                   opal-gateway-mcportal-fabric-read -> gateway-mcportal-fabric-read-policy
  why: (ADDITION): OUT-OF-PATTERN as IAM_POLICY: the module would not produce this name
safe-apply: BLOCKED by the naming plan limb (LGIC_ENFORCE DEC-6, ENFORCE mode, rc=1).
            Nothing was planned further or applied.
```

The refused string is the name the order specifies in step 1. It is also the name the order's
own `AC1` looks up (`get-role-policy --policy-name opal-gateway-mcportal-fabric-read`), so the
gate's remedy and the order's criterion are **mutually exclusive**: adopting
`gateway-mcportal-fabric-read-policy` makes AC1 fail `NoSuchEntity`. Step 2 forbids overriding a
naming refusal; BOUNDS 3 forbids repairing a criterion. Both legal moves are closed to this seat,
so the cell stops with a BLOCKING row and the issuer routes it.

### What the order expected, and where it differed

Step 2 predicted the refusal would arrive **at commit**. It did not. The commit-time limb
**RAISEd** instead:

```
[naming-gate] NAMING RAISE mcportal_fabric_read.tf:40 {x}-mcportal-fabric-read -> (rule or registry defect)
  why: G3: the tokeniser cannot place a character of a resource name '{x}-mcportal-fabric-read'
[naming-gate] NAMING-GATE: WARN 1 graded
```

The commit limb sees the **unresolved** `${var.name}` and cannot tokenise it; the apply limb
resolves the interpolation and then grades the addition. So the commit landed, the ledger was
opened, the plan graded clean at `1 to add, 0 to change, 0 to destroy` -- and only then did the
act stop. Any new interpolated name in this module will discover its refusal in the same late
position. `org/mcp/naming-gate.enforce` is present, so ENFORCE was on throughout.

The module already carries **both** naming conventions on the same role: the two sibling
MCPORTAL policies in `mcportal_grant_writer.tf` use the builder form as literals
(`gateway-invoke-mcportal-grant-writer-policy`), with a comment saying the literal was chosen
*precisely* to be gradeable at commit; the older grants (`gw_golive`, `graph-read`, `ycharts`)
use the interpolated legacy form the order copied. The same run also WARNed that
`aws_iam_role.gw` -> `opal-gateway-role` is itself out of pattern (`-> gateway-role`), existing
so WARN only. The module is mid-migration, and only an ADDITION is refused.

### Verification that nothing landed

Not taken from the wrapper's self-report (CLAUDE.md: never trust rc=0 or a producer's claim).
Two planes:

- live IAM, via the issuer's own `x3.AC1.sh`: `NoSuchEntity ... policy with name
  opal-gateway-mcportal-fabric-read cannot be found`, `rc=254`;
- `terraform state list | grep -c gw_mcportal_fabric_read` -> `0`.

DELTA=0, so the named rollback was a **no-op** and was deliberately not run.

### Criteria, measured

| id | status | reading |
|---|---|---|
| AC1 | **FAIL** | `NoSuchEntity`, rc=254 -- the document was never applied |
| AC2 | **FAIL** | `simulation arms matched 3 of 6` |
| AC3 | **PASS** | `carve-out tokens present 6 of 6` |

**AC2's three passing arms carry no discriminating power.** The three negative arms (get
warehouse, put activity, list warehouse) already read `implicitDeny` at the base commit, before
any grant existed, so the grant's *absence* satisfies them exactly as a correctly scoped grant
would -- ABSENT is not EXERCISED-AGAINST (rule 22). Only the three positive arms discriminate,
and all three read `implicitDeny`. The issuer measured the same 3 of 6 at base and said so in the
order's record face; this session reproduced it.

AC3 is the one criterion the build alone can satisfy, and it transitioned FAIL -> PASS across
this cell's write -- the only positive control available, since the two EXERCISED criteria grade
live state this cell was refused permission to create. **No sealed planted mutant was run**, and
the proof-of-spec says so rather than leaving the absence to read as a pass.

### Ledger

`org/critical_paths/change_management/20261009T0242Z_nfra-mcportal-r4-fabric-read-grant_deploy_completion.md`
-- opened at deploy-START and committed **with** its sentinel in one commit. Carries, written
before the act: the pair-signed blast radius, both rollback commands per key, and the `comp-iam
gaps` preflight with its own ceiling stated.

Final state: **L1 CLOSED** (plan proof), **L2 CLOSED as NOT EXECUTED**, entry
**HELD-SOVEREIGN-GATED** on `2.0.0_SA_COO~MP` with only the verify leg L3 open -- so it reads
KNOWN-HELD, never a half-landed RED. A first `hold` was correctly refused while L2 was open
("a half-landed deploy cannot be HELD"); closing L2 honestly cleared it.

Because the entry sits on `wk-mp-x3` until the drain, a shared-tree read of `.open_deploys/` will
not see it -- NEVER-2's every-live-worktree read applies.

### Two instrument findings (in row NFRA_MCPORTAL-Z-S21's evidence)

1. **The order's directed row id coordinate `A7` is not in the gate's grammar.**
   `surprise-row-gate.py`: *"does not match the id grammar `<CODE>-(Z-)?(W<n>-|C-)?S<k>`"*. The row
   carries the legal seat form `Z-S21`. No override taken.
2. **CLAUDE.md 14b's append-only inversion couples a seat's row to its peers' uncommitted rows.**
   Writing the row in the shared tree (as 14b directs for an append-only channel) was refused by
   the standing corpus pass for 4 NEW failures, of which 2 (`NFRA_OPLGTW-Z-AE-S1/-S2`, the same
   illegal-coordinate class) belong to another lane's uncommitted work. Clearing that needed the
   audited `# surprise-row-override:` line, so the row moved into this worktree where the corpus
   is at the clean base and the gate passes unforced. The shared-tree edit was reverted cleanly.

### Commits

| hash | what | push state |
|---|---|---|
| `e5a036a659` | the two `.tf` files (new policy file + comments-only `graph-read.tf`) | LOCAL |
| `4f639cc38d` | ledger entry + sentinel, one commit | LOCAL |
| `fc4e478587` | row `NFRA_MCPORTAL-Z-S21` + ledger close-out | LOCAL |

Push state is MEASURED as LOCAL: `wk-mp-x3` is a device-local branch created this session and
never pushed; no `origin/wk-mp-x3` exists.

---

## Compiler Tools

| tool | result |
|---|---|
| `comp-iam gaps` | 37 missing / 300 deny-present / 1 coverage-unknown / 3 resource-mismatch across 33 services. Estate-wide, pre-existing; this act adds no row. Ceiling stated: models `(action)`, never `(action, resource)` -- cannot confirm the carve-out; AC2 is that oracle. Recorded in the ledger per step 3. |
| `lib/opal_naming.py name()` | `gateway-mcportal-fabric-read-policy` / `mcportal-fabric-read-policy`; kind `iam_policy` REFUSED (not a NAMING_SCHEMA.json kind). Neither matches the order's string. |
| `.tools/naming-gate.py` (commit) | RAISE/WARN, did **not** refuse -- the G3 tokeniser miss on `${var.name}`. |
| naming plan limb (in `safe-apply`) | **REFUSE 2 graded** -- the blocker. Pre-plan stage: 31 `.tf` files, 69 name attributes, 27 graded, 42 deferred, 9 "would REFUSE if an addition". |
| `terraform plan -target` + `show -json` | `1 to add, 0 to change, 0 to destroy`; JSON confirmed exactly one create, correct name, role and both statement shapes. |
| `terraform init -plugin-dir` | all three providers at lock versions from a **local mirror, no registry fetch**; step 6's blocker did not fire. |
| `terraform fmt -check` | rc=0. ASCII census: 0 non-ascii in both `.tf` files (character count, not a byte delta). |
| `terraform state list` | `0` occurrences of the resource -- second plane on "nothing landed". |
| `.tools/deploy_ledger.py` | open / close-leg L1 / close-leg L2 / hold. The first `hold` refusal was the tool working correctly. |
| `.tools/safe-commit.sh` | 3 commits, all msg-verify MATCH; surprise-row-gate OK unforced. |
| `comp-find` / `comp-read` / `comp-which` | located the gate (2 of 521 files in `.tools/`), surfaced its ENFORCE switch and EXISTING->WARN branch -- which is why the verdict was measured rather than predicted. Two rail denials hit and respected. |

### Gaps worth the issuer's attention

- **`comp-which` has no curated rule for the naming gate.** The question "the commit-time naming
  gate that grades resource names against `lib/opal_naming.py`" scored 0.57 against `comp-similar`
  and printed *"NO CURATED RULE MATCHED"*. The gate is a commit-blocking instrument on every
  infra cell; it is worth a catalog row.
- **A disk census for a Terraform provider must include `C:/tmp`.** A first scan scoped to Desktop
  and AppData returned zero for `external 2.4.2` and would have produced a false step-6 blocker;
  every worktree on this device lives under `C:/tmp`, where the provider was found.
