<task_order>
<to_id>OPAL_GWRENAME.TO-1</to_id>
<title>Execute the m365 -> opal-gateway live cutover (S1-S6)</title>
<issued_by>0.0.0_AB_MSTR</issued_by>
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_at>2026-08-15T01:30:00Z</issued_at>
<status>pending</status>
<project>OPAL_GWRENAME</project>
<authority>Andrew-direct 2026-08-15, VERBATIM: "Ok let's get this whole thing done, no one is online but you so if you need other agents instantiate them now with relevant instructions."</authority>

<spec>
`docs/runbooks/opal-gateway-rename-cutover-runbook.md` @433454738b IS your spec. Execute S1
through S6 in order. Do not re-derive it; do not skip its stage gates. Ledger context: LD-0414
(scoping), LD-0415 (P0 landed + hazards).

P0 is already done: repo homes, runbooks, manifest PATHS and CI source maps are renamed, and every
LIVE-PLANE name is deliberately PINNED to m365 with a comment at its own site. Those pins are
YOURS TO UNPIN, in the order the runbook gives.
</spec>

<read_first>
The runbook's section 0 -- FOUR HAZARDS. Three are invisible in a `terraform plan` and one fails
GREEN. In particular **H1**: the ALB listener's `authenticate_oidc.client_secret` is a placeholder
held out of TF state by `ignore_changes`, and `alb.tf:90-93` states its own runbook -- *re-run the
CLI set-secret on ANY listener recreate*. A `var.name` flip recreates that listener. Skip the
re-set and the ALB is healthy, the target is healthy, `/health` answers, **and every agent OIDC
login fails.** That is why acceptance is an authenticated round-trip, never rc=0.
</read_first>

<stop_conditions>
- **S2 ENDS AT PLAN ONLY.** Report the plan; do not apply on your own initiative.
- **If the plan shows `forces replacement` on `aws_instance.gw`, STOP and escalate to MSTR.** The
  instance is NOT supposed to be replaced (SG + instance-profile changes are in-place). A plan
  that would replace it means my read was wrong and the operation is much heavier than scoped.
- **Do not begin S6 (retire) until S5's authenticated round-trip has PASSED.** After S6 the rename
  is one-way.
- Anything outside this runbook's named acts needs Andrew's word. His reserved categories
  (S3 object deletion, EC2 stops, anything unrecoverable) are unchanged -- S6's secret and
  prefix deletions ARE named here and ARE authorized by his "get this whole thing done", but a
  `--force-delete-without-recovery` on a secret is NOT, and never is.
</stop_conditions>

<compiler_tools_mandate>
BEFORE WRITE: `comp-iam service` on both liveness lambdas; `comp-blast` on the gateway before the
apply. Remember comp-iam models `(action)` never `(action, resource)` and reads TF-DESIRED -- for
the new secret ARNs and the new S3 prefix, ground on the live primitive
(`aws iam simulate-principal-policy`, ONE `--resource-arns` per call, positive control as a
SEPARATE invocation).
BEFORE COMMIT: `.tools/commit-gate.sh` (automatic via safe-commit).
AFTER COMMIT: re-run the section-2 acceptance census with denominators printed.
</compiler_tools_mandate>

<acceptance_criteria>
Runbook section 2 -- zero `m365`/`M365` across all 14 named surfaces, each reported WITH ITS
DENOMINATOR (e.g. "0 of 206 roles"). Materialise paginated `list-*` results client-side: `--query
'length(...)'` returns a PAGE count and `--no-paginate` returns page 1 looking complete. An
ABSENCE verdict carries its denominator or it is not a verdict.

The gateway serves a real authenticated MCP tool call through `https://mcp.opalinvest.dev/mcp/`
after the flip. A green target group is NOT acceptance.
</acceptance_criteria>

<proof_of_spec>
Criterion ids, each needing a live-primitive citation:
  GW-1  4 new secrets exist, values sha256-identical to sources (never print a value)
  GW-2  S3 artifact tree copied to ec2/opal-gateway/*
  GW-3  terraform plan clean, instance NOT replaced (attach plan excerpt)
  GW-4  apply landed via safe-apply; ALB/TG/SG/role/profile/WAF all opal-* on live read
  GW-5  OIDC client_secret re-set on the new listener (H1) -- cite the CLI call
  GW-6  authenticated MCP round-trip through mcp.opalinvest.dev SUCCEEDS
        [AMENDED 2026-08-15 by 2.0.0_SA_COO per MSTR 015746Z: the evidence MUST be a COLD
        OIDC login (fresh seat / fresh token exchange through the recreated listener).
        A warm session holds a pre-flip bearer token and structurally CANNOT see H1 --
        record warm calls only as "warm call OK (non-discriminating)" beside the cold result.]
  GW-7  on-box: opal-gateway.service active, /opt/opal-gateway serving, old unit gone
  GW-8  8 hardcoded literals in otp-liveness.tf + ms-ingest.tf renamed; both lambdas live opal-*
  GW-9  old secrets + old S3 prefix + old log groups retired
  GW-10 TF state key migrated; EC2_MANIFEST key + deploy-to-ec2.sh fully unpinned
  GW-11 acceptance census: 0 m365 across all 14 surfaces, denominators printed
</proof_of_spec>

<deploy_discipline>
Terraform is the ONLY deploy mechanism; `safe-apply.sh` never bare apply; `safe-ec2-deploy.sh` for
code; `EC2_MANIFEST.json` is the source of truth. **Verify the EC2 deploy ON-BOX, never by the
wrapper's exit code** -- it has a known Windows-charmap false-negative that reports failure after a
SUCCESSFUL SSM deploy. Open a deploy-completion ledger entry in
`org/critical_paths/change_management/` at S3 start and close it at S5: **a begun deploy FINISHES
in-session or rolls back and escalates loud** (NEVER#8).
**No alarms, monitors, SES, or freshness checkers** -- the moratorium is standing and this work
will tempt you toward one. A finding lands as a finding, not as notification machinery.
</deploy_discipline>

<cross_domain_coordination>
`2.0.0_SA_COO` drives and verifies INDEPENDENTLY -- report each stage to them as you complete it.
`0.0.0_AB_MSTR` holds arch calls, integration and the push. Commit under your own author line
(this is your lane; the P0 commits crossed into it under an audited override precisely because you
were not live, and your taking the work retires that crossing).
</cross_domain_coordination>

<reporting>
Report at every stage boundary S1..S6, and IMMEDIATELY on any stop-condition. Ground every claim
on the live primitive, not on a plan, not on rc=0, not on your own prior step's self-report
(Rule 22a: staged code is DESIRED, executing code is APPLIED).
</reporting>
</task_order>
