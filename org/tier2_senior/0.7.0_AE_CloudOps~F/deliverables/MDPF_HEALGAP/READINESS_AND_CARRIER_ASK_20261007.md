# 0.7.0_AE_CloudOps~F -- readiness for the MDPF_HEALGAP cot-rebalancer-runner deploy, and ONE carrier ask

**Seat:** `0.7.0_AE_CloudOps~F` (laptop). **Seated by:** `1.0.0_SA_CTO` msg 106115, on
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_FOR_THE_DELLS_20261007_0930Z.md` section 2.
**Issuer of the task order:** `2.0.0_SA_COO~G1` (dell1). **Nothing is built in this record. Zero writes outside this file.**

## 1. THE ASK -- who carries the task order from dell1 to this inbox? (owner `0.0.0_AB_MSTR`)

`2.0.0_SA_COO~G1` reads **NOT REGISTERED** on this broker: `get_live_agents` at 2026-10-07T10:0xZ returns 7 live
(`0.0.0_AB_MSTR`, `0.7.0_AE_CloudOps~E`, `0.7.0_AE_CloudOps~F`, `1.0.0_SA_CTO`, `2.0.0_SA_COO~C`, `3.0.0_SA_CVO`,
`4.0.0_SA_CRO`) and no dell1 lane among them. `opal-agent-comms` is localhost-only, so the issuer cannot write this
inbox directly.

Two carriers are possible and **this seat watches only the first**:

| carrier | path | watched by this seat |
|---|---|---|
| `/agentbus` relay into the lane inbox | `org/mcp/inbox/0.7.0_AE_CloudOps/~F/` | YES -- Monitor task `b9lbpolgc`, script pid 12252 |
| the order committed to the trunk | `org/missions/D8/MDPF/MDPF_HEALGAP/task-orders/` | NO -- nothing polls git for me |

`/agentbus` is `0.0.0_AB_MSTR`'s arm per `org/XXX.md` Step 1b-F, not this seat's; this seat arms zero crons. So the
ask is MSTR's to answer: relay it, or tell this seat to read the trunk, naming the ref.

## 2. The ruling's three preconditions, graded against what exists NOW

The ruling names three reads, "each a refusal if absent". Measured 2026-10-07T09:5x-10:0xZ. Trunk read is
`origin/CLOUD` = `75c5672586c10a110e086e231400ff2fa01b86f7` (`git ls-remote origin CLOUD`); local `CLOUD` is
`8b83fd1d6f2a10e0c9f99f78ba53ee4f82101361` (other laptop seats are committing into the shared tree).

### Precondition 1 -- PRD ADMITTED, and brief + PRD + decomp on the trunk: **PASSES**

`python .tools/prd-signoff.py status MDPF_HEALGAP` -> `MDPF_HEALGAP v0.1 @78db344481 dep_stage=EXECUTING -> ADMITTED`;
ratified-text half **SIGNED** by `3.0.0_SA_CVO`, **current**; brief half auto-admitted because the CRO wrote the brief
(spine v3.19 L4-R, the PROPORTIONATE SIGN-OFF clause of CLAUDE.md rule 27). Pin `78db344481` is an ancestor of
`origin/CLOUD` (`git merge-base --is-ancestor`, with a positive control on `HEAD~1` that returned YES, so the
instrument was working).

All three artifacts are present **on the trunk**, read by content with `git ls-tree -r origin/CLOUD` (positive control:
the same read on `org/missions/SEQUENCE.yaml` returned it):

- brief -- `docs/briefs/mdpf-healgap-midstream-brief-20261007.md` (and the older `docs/architecture/MDPF_HEALGAP_BRIEF.md`)
- PRD -- `org/missions/D8/MDPF/MDPF_HEALGAP/prd/MDPF_HEALGAP_PRD.md`, with `prd/signoff/3.0.0_SA_CVO.json`
- decomp -- `org/missions/D8/MDPF/MDPF_HEALGAP/decompositions/MDPF_HEALGAP_DECOMP.md`

The Andrew-direct behind the hold is on the trunk too:
`org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20261007_075xZ_MDPF_HEALGAP_THROUGH_CANONICAL_FLOW_CRO_WITH_CTO.md`.

`python .tools/sequence-check.py --project MDPF_HEALGAP` reads **UNPLACED** -- "a register project the sequence does not
list: not sequenced, so its own directive's rules govern it". That is not a refusal; it is recorded so no later read
mistakes the absence for a WAITING.

### Precondition 2 -- built artifact sha equals `QxLvPLTMO5YSkS+vaRXEkhaA78ZAr1arTyS0ADOOMvk=`: **CANNOT PRE-PASS; it is an unbuilt target**

The apply directory is `infra/aws/terraform/opal-assets/` (module declared in `cot_rebalancer_runner.tf:133`,
`function_name = local.cot_rebalancer_runner_name` = `"cot-rebalancer-runner"` at `:33`), **not** `cot-pipeline/`.

| object | measured value | vintage |
|---|---|---|
| live `cot-rebalancer-runner` `CodeSha256` | `b1m7jUh6jC55tBfoUX20xRmmKAjB4P1Wvxnwvn2N/Fw=` | `LastModified 2026-09-11T03:26:00Z` |
| staged S3 artifact `s3://opal-313476888478-lambda-artifacts/opal-assets/cot-rebalancer-runner.zip` | 12,087 bytes, `VersionId XeSy4IKGvKXGsEwBQRpeXUekk5qb.TYp` | `LastModified 2026-09-11T03:18:08Z` (`s3api`, UTC) |
| sha named by `2.0.0_SA_COO~G1` | `QxLvPLTMO5YSkS+vaRXEkhaA78ZAr1arTyS0ADOOMvk=` | not present in either place |

So the live bytes and the staged artifact are the **same 2026-09-11 vintage**, and the named sha is neither deployed nor
staged. This is a real code change, not a DELTA=0 no-op, and the build is part of the work rather than something this
seat can verify in advance. On building, a sha that is not byte-equal to the named one is a **refusal**, not a rounding
error: it would mean a non-reproducible build or the wrong source ref.

The source to build from **is on the trunk**, which is why this is not a blocker. `git log origin/CLOUD` on
`infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/` carries, above the deployed vintage:

- `8af853ce59 build(MDPF_HEALGAP.TO-HG-t1, 0.9.0_WK_MDPF_HEALGAP~1): runner guard decides by listing, induce=auth-lapse exercise hook`
- `c53e48f7fb fix(cot-rebalancer-runner): a count mismatch is DISCLOSED, not fatal -- one closed account froze the Cottonwood model chain for 11 days; COMMITTED, NOT DEPLOYED`

That second commit states its own non-deployment, and it names the cost of the gap: eleven days of a frozen Cottonwood
model chain. The local working tree for that source directory is **clean** (`git status --porcelain`, empty).

### Precondition 3 -- `cot_rebalancer_reattempt.tf` not in the apply: **PASSES by absence**

The file exists **nowhere on this laptop**: not on the trunk (`git ls-tree -r origin/CLOUD --
infra/aws/terraform/opal-assets`, which returned `cot_rebalancer_runner.tf` and no reattempt file), and not in the
working tree (`ls -1 infra/aws/terraform/opal-assets/`). `git status --porcelain infra/aws/terraform/opal-assets/` is
empty, so nothing uncommitted can carry it in either. It therefore cannot enter the apply from this box.

Read alongside, not as a refusal: `MDPF_HEALGAP.TO-HG-t2.reattempt-on-bronze-complete.md` **is** on the trunk as a task
order, so the reattempt is a real and separate cell. Its Terraform has not reached this device. Nothing here needs it.

## 3. What this seat will do the moment the order lands, and what it will not do

On the order: read it in full, flip `<status>` to `pending`, open the NEVER-2 ledger entry in
`org/critical_paths/change_management/` naming **the laptop** as the box (the ruling places it here), then build, stage,
`.tools/safe-apply.sh` (never bare `terraform apply`, CLAUDE.md NEVER block and `/cloud-ops` rule 18), verify
`CodeSha256` equals the named sha, re-plan for 0-diff, tag, close the ledger entry in-session.

Not done here and not assumed: the two never-widen halves are **dell1's** (`1.0.0_SA_CTO~DELL1` and `2.0.0_SA_COO~G1`)
per the ruling; this seat does not sign them and does not grade whether they exist. No build, no plan, no init and no
apply has been run -- the seating message said to start nothing before the order, and nothing has been started.

-- `0.7.0_AE_CloudOps~F`, 2026-10-07
