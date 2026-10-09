# gate-built-names.r20.result.md -- LGIC_ENFORCE.TO-EN-z-4 (0.9.0_WK_LGIC_ENFORCE~2)

Row LGIC_BLANKFIX-D1-W2-S9: the commit gate now grades a name built by name() at a call site, or prints that it did not.

## What changed (`.tools/naming-gate.py`)

- `tf_built()` reads each `module "x" { source = ".../opal_name" ... }` block that meets the added lines; `py_built()` reads
  each bare `name(...)` call (four or more arguments) and each `opal_naming.name(...)` call.
- `grade_built()` composes the name with `lib/opal_naming.py name()` when every argument is a literal, and grades it through
  `judge()` like any other literal (hint = the node type of its kind), printing the usual `NAMING <verdict> <file>:<line> <name> -> <canonical>`
  line; it is counted in the `NAMING-GATE: <v> N graded` summary.
- Otherwise it prints `NAMING BUILT-NOT-GRADED <file>:<line> <why>` (non-literal argument, name() refused the arguments, or the
  built name could not be classified). It counts as PASS and never blocks, but a pass there is no longer silent.
- A built name is not a hand-kept firm carrier: the builder writes the firm's short form ("cot"), so the carrier context rule is
  skipped for a built literal (`Lit.built`). Without this the correct built name was REFUSED as a NEW carrier of "cot"
  (seen on the first run). A hand-typed copy of the same name is still REFUSED, which the new control arm records.
- A module block that passes none of system/function/kind (a registry-map reader) names nothing and is skipped. An omitted
  `scope` is the module's own default null (a shared resource).
- NEW test: the pre-image's own built names are added to the pre text, so an unchanged block touched by an edit is not NEW.
- `--self-test` gains 8 arms (`built_self_test`): module literal, call literal, call with keywords, module with a variable,
  registry reader (no row), call with a variable, call name() refuses, hand-typed control.

## Fixtures (check_en_r20.py s9)

    tf-module: NAMING CONFORMANT infra/aws/terraform/zz-r20-s9-probe/main.tf:1 irpt-cot-reporting-gold-scheduler-role -> irpt-cot-reporting-gold-scheduler-role
    py-call:   NAMING CONFORMANT infra/aws/lambda/zz-r20-s9-probe/handler.py:3 irpt-cot-reporting-gold-scheduler-role -> irpt-cot-reporting-gold-scheduler-role

## Demonstration over one real root (a diff adding every file of infra/aws/terraform/investor-reporting/reporting-gold)

`NAMING-GATE: PASS 8 graded` over iam.tf, lambda.tf, schedule.tf: 3 opal_name/name() sites graded as built names
(irpt-reporting-gold-lambda, irpt-reporting-gold-scheduler-role, irpt-reporting-gold-scheduler-policy), 4 BUILT-NOT-GRADED
(module blocks whose `scope` is not a literal: iam.tf:24, iam.tf:32, lambda.tf:26, schedule.tf:74), 1 hand-typed literal
(irpt-performance-native-layer) graded as before.
