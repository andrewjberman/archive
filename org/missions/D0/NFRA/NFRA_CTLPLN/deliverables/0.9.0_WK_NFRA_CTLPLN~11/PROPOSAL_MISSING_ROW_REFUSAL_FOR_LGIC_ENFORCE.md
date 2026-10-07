# Proposal to LGIC_ENFORCE: refuse an apply that adds a resource with no registry row

**To:** the owner of LGIC_ENFORCE (the project that owns `.tools/naming-apply-gate.py` and the naming limb in `.tools/safe-apply.sh`).
**From:** `0.9.0_WK_NFRA_CTLPLN~11`, worker for NFRA_CTLPLN task order `NFRA_CTLPLN.TO-CT-d-8` (round 4, cell CT-d-8, PRD v0.13 C-NAMING).
**Status:** a proposal. It changes no file of LGIC_ENFORCE, LGIC_NAMING or the registry, and it instructs nobody. Every statement
about what the gate does is tagged READ (I read it in the code at commit 208c5d85ee) or MEASURED (the probe
`.tools/tests/probe_missing_registry_row.py` in the NFRA_CTLPLN worktree, run on 2026-10-07 against that tree; no AWS call, no
terraform, no backend).

## 1. What the apply path does today (measured)

The probe feeds `.tools/naming-apply-gate.py --plan-json FILE` three synthetic `terraform show -json` plans, each adding one
`aws_lambda_function`. This is the same call `.tools/safe-apply.sh` makes at line 181, with no `--enforce` flag. The gate reads its own
mode (section 5). Results:

| Case | Name | In `resources.json`? | Gate line | Exit code | Result |
|---|---|---|---|---|---|
| A, a registered name | `inf-gold-trigger` | yes, 1 row | `NAMING REFUSE aws_lambda_function.registered_probe inf-gold-trigger -> advi-inf-gold-trigger-lambda` | 1 | refused |
| B, well-named, no row | `blackdiamond-49f-missing-row-probe-lambda` (built by `lib/opal_naming.py name()`) | no, 0 occurrences in any of the 8 registry files | `NAMING CONFORMANT aws_lambda_function.unregistered_probe blackdiamond-49f-missing-row-probe-lambda -> blackdiamond-49f-missing-row-probe-lambda` | 0 | admitted |
| C, badly formed | `bd_probe_lambda` | no | `NAMING REFUSE aws_lambda_function.badly_named_probe bd_probe_lambda -> {system}-49f-probe-lambda` | 1 | refused |

The gate's summary lines were `NAMING-PLAN: REFUSE 1 graded` (A), `NAMING-PLAN: PASS 1 graded` (B) and `NAMING-PLAN: REFUSE 1 graded` (C).
The probe's last line was:

`MISSING-ROW-PROBE registered_wellnamed=refused unregistered_wellnamed=admitted badly_named=refused gate_mode=ENFORCE ok=True`

Case C is the positive control: the gate does refuse a bad name, so the gate was exercised and B's admission is a measurement,
not a failure to run. **The finding is that a well-formed name with no registry row is admitted.** Nothing in the gate consults the
registry for the existence of a row for the resource being added (READ: `run_plan` at `.tools/naming-apply-gate.py` lines 326-374
calls only `judge()`, which calls `lib/opal_naming.py grade()`; the registry reaches the gate only as the vocabulary `grade()` uses).

Two further facts that the proposal depends on:

1. **No row in `resources.json` names a conformant resource (MEASURED).** The probe's registry census printed
   `resources.json holds 465 row(s); 0 of 465 row name(s) grade CONFORMANT under lib/opal_naming.grade()`. Case A is therefore not
   a "registered well-named" resource; none exists. It is a registered legacy name, and the gate refuses it on its grade, so
   a row today neither admits a resource nor is required for one. (This is surprise row `NFRA_CTLPLN-W11-S1`.)
2. **A row for a conformant name is refused by the registry validator (MEASURED).** `resources.json`'s `_about` and
   `lib/opal_naming.py` lines 605-610 and 642-664 (READ) say a row fills a `{system}` placeholder for a name whose own tokens resolve
   no system. The validator refuses a row whose name already resolves the same system as redundant. I appended a row for case B's
   name to a scratch copy of the registry (in `.scratch/regcopy`, not the registry) and ran `lib/opal_naming.validate(reg_dir=...)`:
   one refusal, `'blackdiamond-49f-missing-row-probe-lambda' already resolves 'blackdiamond' from its own tokens (type 'LAMBDA'); a row
   naming the same system is redundant`. The unmodified registry returns 0 refusals. (This is surprise row `NFRA_CTLPLN-W11-S2`.)
   I did not measure which commit or CI gate runs `validate()`; only the function's return.

The second fact is the question this proposal cannot settle and which you must answer first (section 7).

## 2. The refusal proposed

When the plan's resource is an ADDITION (as `_is_addition` at lines 314-323 already decides: an action including `create`, or an
`update` that changes the own-name attribute) and its name grades CONFORMANT or NOT-GRADED under its own node type, look the
`(name, node type)` pair up in the registry's resource index. If there is no row, refuse that resource with a line naming
the resource and the missing row, for example:

`NAMING REFUSE aws_lambda_function.unregistered_probe blackdiamond-49f-missing-row-probe-lambda -> no registry row`
`  why: ... (ADDITION): CONFORMANT as LAMBDA, but infra/logic/registry has no row for (name, LAMBDA); the row lands in the same commit as the Terraform (C-NAMING clause 3)`

A resource that is not an addition keeps today's behaviour. This is unchanged in the proposal: it only ever WARNs (READ: lines 368-371).

**Out of scope, because the resource has no name of its own.** The plan loop already skips these and the proposal inherits that
(READ, lines 355-359): any resource whose Terraform type is not in the schema's `tf_type_map` (`.tools/naming-gate.py` `TF_NODE`),
that is, the types with no own-name attribute (attachments, permissions, routes, associations) and the 30 types that carry a name
but map to no node type (the gate's own docstring, lines 27-28, lists `aws_ecr_repository.name` and `aws_kms_alias.name` among
them); and a resource in a data block or any `mode` other than `managed`. The two NOT-GRADED types (`aws_iam_user`,
`aws_route53_record`, line 87) are a decision for you: they carry a name but no grade, so a missing-row refusal on them has no
grade to stand beside.

**What a first mint looks like.** C-NAMING clause 3 says the row lands in the same commit as the Terraform, so on the first apply of a
new resource the row is already in the tree that `safe-apply.sh` runs. The gate reads the registry from the same checkout
(`REPO`, line 81), so a first mint whose commit carries its row passes, and a first mint whose commit lacks it is refused before
anything is planned further. There is no separate "first-mint" state; the refusal and the first mint are the same event.

## 3. Where it would sit in the gate (READ)

- **`.tools/naming-apply-gate.py`, `run_plan()`, lines 366-373.** After `judge()` returns for an addition (line 369), add the
  registry lookup and, on a miss, replace the verdict with `REFUSE` and `refuses=True`. `judge()` (lines 239-253) is shared with
  `judge_capped()` (lines 256-263), which the non-addition branch uses, so the lookup belongs in `run_plan` and not in `judge()`.
- **`_main_plan()`, lines 435-471.** No change to exit behaviour is needed: any `refuses=True` row already yields the
  `NAMING-PLAN: REFUSE` summary and exit 1 under enforce (lines 459-471). The module docstring's plan matrix (lines 43-50) gains one row.
- **`.tools/safe-apply.sh`, lines 175-205.** No change: the wrapper turns a non-zero exit of the plan call (line 181) into exit 7 in
  ENFORCE (lines 186-188, 202-205), and it already covers the unscoped apply, the targeted apply and the saved-planfile apply (lines 168-178).
- **The index itself.** `lib/opal_naming.py` already builds a `(name, type) -> system` dictionary from `resources.json`
  (`_Vocab.resources`, lines 1226-1229), so the lookup needs no new reader, only a public accessor.

## 4. Cost and non-application

**Cost.** One registry read per apply: the gate already loads `lib/opal_naming.py`, and with it the registry, for every plan; the
lookup is one dictionary access per added resource. A plan with no additions costs nothing extra. The cost that is not small is
the one in section 7: the index may have to change.

**Non-application.**
- A resource being changed, destroyed or left unchanged (READ: not an addition; the limb "never blocks it", docstring lines 11-12 and 49-50).
- Existing pipelines' legacy names. `legacy_addresses.json` and `exemptions.json` do not bear on a resource-name refusal. READ of
  their `_about` blocks: `legacy_addresses.json` is "one row per S3 store that predates the canon ... a READ address: it authorizes
  no write and moves no object", keyed for `legacy_address()` and not for resource names. `exemptions.json` is the fence's per-firm-bucket list of principals exempt
  from `DenyForeignFirmPrincipals`, with their sign-offs. Neither lists a resource name, so neither can excuse a missing row; if a
  legacy-named resource must be added, it is already refused on its grade today (case A) and that stays the gate's existing outcome.
  The 465 legacy rows in `resources.json` are the legacy names' attribution and they are existing resources, which the
  non-addition rule already protects.
- A replace is an addition (it includes `create`, line 319). A replace of a legacy-named resource with no conformant name is already
  refused on its grade today; the new check would add nothing there.

## 5. The mode it should start in, and why

**Today the gate is in ENFORCE (READ and MEASURED).** `enforcing()` (lines 106-107) is true when `--enforce`, `NAMING_GATE_ENFORCE=1`
or the file `org/mcp/naming-gate.enforce` is present. That file is tracked in git and was flipped by `2.0.0_SA_COO~G` on 2026-09-17
(commit d181e0ac5a, whose text in the file says "Remove this file to return the naming limbs to WARN"). The probe reported
`gate_mode=ENFORCE` and cases A and C exited 1.

I propose the new check **start in WARN**, which is the repo's pattern for a new naming gate (the file's own "WARN window", and the
`WARN window` text at lines 466-467). Reasons: (a) section 1's second fact means that a refusal today could refuse every
conformant new resource with a row the validator will not accept, so the first window should only count; (b) the gate's single switch
makes any new check enforce the moment it lands, because `enforcing()` serves every verdict. The cost is therefore a second, separate
switch for this one check (for example its own flag file), default WARN, with its first window printing `NAMING WARN ... no registry row`
and no change to the exit code; (c) the plan is the only evidence this check sees, so one window across the first real applies is cheap.
I do not propose a length for the window or the criterion for ending it; those are yours.

## 6. What it does not cover

- **A create outside Terraform (C-NAMING clause 1).** A CLI or SDK create call never produces a plan, so `safe-apply.sh` and this gate
  never see it. The NFRA_CTLPLN PRD says the Dell create grant permits such a create. This check does not close that.
- **A name the plan does not state.** `run_plan` skips a resource whose own-name attribute is not a string in the plan (line 364, READ),
  for example a name computed at apply time. It is neither graded nor checked for a row today; the proposal inherits that gap. I did
  not measure it with the probe.
- **S3 addresses and keys (C-NAMING clause 2, second half).** `address()` output is not a resource name; no resource-name gate sees it.
- **That the row is correct.** The check tests that a row exists for `(name, type)`, not that its system attribution is right.
- **A Dell.** I did not run the gate on dell1 or dell2; the PRD records that as UNMEASURED and it stays so.

## 7. The question this proposal hands you

C-NAMING clause 3 and the PRD's "no gate refuses an apply for a missing registry row" assume that `resources.json` holds a row for each new
resource. It does not today for any conformant name (0 of 465), and its validator refuses a row for one (section 1, fact 2). A refusal
on "no row in `resources.json`" is therefore only coherent if you either (a) let `resources.json` carry a row for a conformant name
(change the validator's redundancy refusal, or add a field that marks a row as a registration and not a placeholder fill), or
(b) name a different index for registration, which the CTO's order calls "some index we have for this exact purpose". I did not search
for one and cannot say that one exists. The refusal's placement in section 3 is the same either way; only the lookup's target changes.
