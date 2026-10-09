# OG-tm-1 amendment A3 -- the new rule takes the builder's name (row NFRA_OPLGTW-Z-S68, option (c))

Nothing applied, uploaded or sent. Worker `0.9.0_WK_NFRA_OPLGTW~39`.

- **Derivation, not typing.** `lib/opal_naming.py name("schwab", None, "canonical-si2-08403355-pull", "daily")` returns
  `schwab-canonical-si2-08403355-pull-daily`, and `grade(that, "EVENT_RULE")` returns `CONFORMANT`. The arguments were found by
  trying the builder until it printed the gate's own string: system `schwab`, no scope (a shared resource), function
  `canonical-si2-<master>-pull`, kind (cadence) `daily`. No registry row was needed.
- **In Terraform** (`monolith-daily-schedule.tf`): `module "si2_daily_rule_name"` (`../modules/opal_name`, the HCL builder), `for_each`
  over `local.si2_daily_builder_named = {"08403355"}`, with `function = "canonical-si2-${each.key}-pull"`; the rule's `name` is
  `module.si2_daily_rule_name[each.key].name` for that key and the unchanged sibling string for the other two. Nothing else in the
  file changed (the cron, label, description, targets, role and policy are as before; a `terraform fmt` realignment of three
  unrelated lines was reverted).
- **Plan** (`plans/canonical-schwab-ec2.A3.txt`): `2 to add, 0 to change, 0 to destroy`: `aws_cloudwatch_event_rule.si2_daily["08403355"]`
  (`name = "schwab-canonical-si2-08403355-pull-daily"`) and its target. The two sibling rules and targets are absent from the plan
  (no change). The earlier box-grant change is gone because Leg B is applied.
- **The gate, on that plan** (`plans/canonical-schwab-ec2.A3.naming-gate.txt`, `.tools/naming-apply-gate.py --plan-json`, run
  read-only): the new rule `NAMING CONFORMANT ... (ADDITION): CONFORMANT as EVENT_RULE`; the two siblings `NAMING WARN ... (existing)`,
  which is rule 30's non-application; rc 0, `NAMING-PLAN: WARN 15 graded`, no REFUSE.
- **Text that still names the old rule string:** the ask (`NEVER_WIDEN_ASK_OG-tm-1.md`) and the COO half name the rule
  `canonical-schwab-si2-08403355-daily-pull`; they are signed text and I did not edit them. The rule is now
  `schwab-canonical-si2-08403355-pull-daily` (A3).
