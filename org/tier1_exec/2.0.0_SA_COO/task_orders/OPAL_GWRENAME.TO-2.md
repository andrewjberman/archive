<task_order>
<to_id>OPAL_GWRENAME.TO-2</to_id>
<title>Drive + independently verify the opal-gateway cutover to close</title>
<issued_by>0.0.0_AB_MSTR</issued_by>
<issued_to>2.0.0_SA_COO</issued_to>
<issued_at>2026-08-15T01:30:00Z</issued_at>
<status>complete</status>
<completed_at>2026-08-15T03:43:00Z</completed_at>
<completion_evidence>org/tier1_exec/2.0.0_SA_COO/deliverables/OPAL_GWRENAME_VERIFICATION_20260815.md -- every stage S1-S6 verified-independent on COO live reads; GW-6 PASS (two bracketing cold seats, MSTR-fired) + GW-12 PASS (MSTR oracle + COO whoami full Graph payload); final census 0 m365 on every LIVE surface with denominators, reproduced number-for-number; H1 held at DESIRED-grade with substitute oracle named; TO-1 complete @0a90de81e8, ledger CLOSED 0336Z. Open items + method findings carried in the record.</completion_evidence>
<project>OPAL_GWRENAME</project>
<authority>Andrew-direct 2026-08-15, VERBATIM: "Ok let's get this whole thing done, no one is online but you so if you need other agents instantiate them now with relevant instructions."</authority>

<spec>
`docs/runbooks/opal-gateway-rename-cutover-runbook.md` @433454738b is the spec.
`0.7.0_AE_CloudOps` EXECUTES it under OPAL_GWRENAME.TO-1. You DRIVE it to close and VERIFY
INDEPENDENTLY. MSTR holds arch calls, integration and the push.

This is the ONLY live mandate at this seat tonight. MDPF_TRGALN is closed; OPAL_MDPFCLEANUP is
not yours this session unless Andrew says otherwise.
</spec>

<the_job>
1. **Drive.** Keep AE moving stage to stage (S1 additive -> S2 plan-only -> S3 apply -> S4 on-box
   -> S5 verify -> S6 retire). Unblock, sequence, escalate. Do not execute infra yourself -- that
   is AE's lane.
2. **Verify INDEPENDENTLY.** Your verification is worth something only where it does not share a
   derivation with AE's. Read the live primitives yourself; do not re-report their report.
   Shared-derivation instruments cannot cross-check.
3. **Hold the acceptance bar.** Runbook section 2, every surface, denominators printed.
</the_job>

<the_one_check_that_matters>
**H1 -- the OIDC listener secret.** `alb.tf:90-93` states its own runbook: re-run the CLI
set-secret on ANY listener recreate. The `var.name` flip recreates the listener, and the real
`client_secret` is held out of TF state by `ignore_changes`. If AE misses that step: ALB healthy,
target healthy, `/health` answers 200 -- **and every agent OIDC login fails.**

**A HEALTH CHECK STRUCTURALLY CANNOT DETECT THIS.** Your acceptance evidence for the flip is a
REAL AUTHENTICATED MCP TOOL CALL through `https://mcp.opalinvest.dev/mcp/`, made by you, after the
apply. Not a green target group, not rc=0, not AE's word that they ran the CLI command. Exercise
the path that fails if the claim is false.

[AMENDED 2026-08-15 by 2.0.0_SA_COO per MSTR 015746Z: "made by you" is NECESSARY but NOT
SUFFICIENT -- a WARM session's call rides a bearer token minted BEFORE the flip and succeeds on
a broken gateway (H1 is exercised at LOGIN). Acceptance evidence is a COLD OIDC login: plan of
record is MSTR spawning a throwaway fresh seat at S4-complete whose cold MCP mount + first tool
call is the discriminating instrument. Warm calls are regression checks only, recorded as
"warm call OK (non-discriminating)". Fallbacks: direct token-exchange exercise against the
listener, or a demonstrated cold re-handshake.]
</the_one_check_that_matters>

<gates_and_scope>
- **ZERO crons.** `/drive` stays OFF unless I explicitly arm it -- and I have not. Andrew's
  standing order and the slimmed XXX.md row both bind. This TO is not a `/drive` authorization.
- **Do NOT manufacture approval gates.** No co-signs, no "MSTR must bless before AE proceeds"
  beyond the stop-conditions the runbook already names. Andrew's 2026-08-06 no-gates ruling binds.
- The runbook's stop-conditions ARE the gates: S2 ends plan-only; an `aws_instance.gw` replacement
  in the plan STOPS and escalates to me; S6 does not start until S5 passes.
- Surface findings loudly and same-turn; never hold silently.
</gates_and_scope>

<acceptance_criteria>
Runbook section 2 census reads zero `m365`/`M365` on all 14 surfaces WITH DENOMINATORS, and the
authenticated round-trip passes on YOUR read. Report to MSTR with evidence per stage; final report
carries the full census plus anything you left undone and why.
</acceptance_criteria>

<proof_of_spec>
Validate AE's GW-1..GW-11 criterion set against live primitives. Your PASS on GW-6 (the
authenticated round-trip) must rest on a call YOU made, not on AE's report of theirs.
</proof_of_spec>

<reporting>
Report to `0.0.0_AB_MSTR` at each stage boundary and immediately on any stop-condition or
surprise. If the cutover cannot complete tonight, say so plainly with the exact stage reached and
the state left behind -- a half-landed deploy is RED-ALERT material, not a follow-up (NEVER#8).
</reporting>
</task_order>
