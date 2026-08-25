# PRFR1AE-AC2 — IAM FOR EACH NEW PERFRP KEY. **PASS.** No new IAM is required, proven per key.

**Seat:** `0.7.0_AE_CloudOps~G` · **Cell:** PRF-c-1 · **Measured:** 2026-08-25T09:59Z–10:0xZ
**Verdict: PASS — all 11 round-1 PERFRP leaves are already covered by the existing scoped grant.**

⛔ **WHY THIS COULD RUN UNDER ANDREW'S HOLD:** AC2 is **read-only** — `simulate-principal-policy`,
`validate-policy`, `get-role-policy`, `terraform plan`. It writes nothing, publishes nothing, and
needs no leaf to exist. It is the same instrument and the same property that let AC5 run ahead of the
start condition (TO line 20). **Nothing here advances publication; it only establishes that IAM will
not be the thing that blocks it.**

## The grant under test

| | |
|---|---|
| Role | `arn:aws:iam::313476888478:role/bd-exporter-ec2-role` |
| Inline policy | `advi-49f-publisher-platinum-put` (Sid `AdviPublisherScopedPut`) |
| Action | `s3:PutObject` — **only** |
| Resource | `arn:aws:s3:::opal-data-portal-v2/platinum/advi/49financial/*` |
| Condition | **NONE — measured, not assumed** (see false-deny mode 2 below) |

## Rule 22a — three layers, each on its own instrument

**DESIRED** — `infra/aws/terraform/bd-pipeline/iam.tf:1171-1185` declares the policy; every field
matches APPLIED (name, Sid, Effect, Action, Resource, absence of Condition).
`terraform plan -lock=false -target=aws_iam_role_policy.bd_exporter_advi_49f_publisher_put` →
**"No changes. Your infrastructure matches the configuration."**
⚠ **Disclosed: the plan was `-target`ed**, so the 0-diff is scoped to this resource and is NOT a
statement about the rest of the `bd-pipeline` configuration. Terraform's own targeting warning is in
the output and is not suppressed here.

**APPLIED** — `aws iam get-role-policy --role-name bd-exporter-ec2-role --policy-name
advi-49f-publisher-platinum-put` returned the live document quoted above.

**EXERCISED** — 11 simulates, **one `--resource-arns` per call**, leaf names derived from the DEPLOYED
registry rather than typed:

| # | leaf | decision |
|---|---|---|
| 1 | `perfrp_activity_relationship.json` | allowed |
| 2 | `perfrp_activity_account.json` | allowed |
| 3 | `perfrp_performance_relationship.json` | allowed |
| 4 | `perfrp_performance_account.json` | allowed |
| 5 | `perfrp_allocation_relationship.json` | allowed |
| 6 | `perfrp_allocation_account.json` | allowed |
| 7 | `perfrp_gainloss_relationship.json` | allowed |
| 8 | `perfrp_gainloss_account.json` | allowed |
| 9 | `perfrp_transactions_relationship.json` | allowed |
| 10 | `perfrp_roster_relationship.json` | allowed |
| 11 | `perfrp_book_advisor.json` | allowed |

**DENOMINATOR: 11 allowed of 11 PERFRP leaves simulated.**

## The three false-deny modes, each closed explicitly

`simulate-principal-policy` has three independent ways to return a deny that is not a deny. **11/11
`allowed` is also exactly what an undiscriminating instrument returns**, so the controls are the
evidence, not the count.

| mode | closure |
|---|---|
| **(1)** 2+ `--resource-arns` flips held ones to `implicitDeny` | **ONE resource per call**, 13 separate invocations. Controls run in their **own** invocations — a control bundled with the target is disarmed by this very mode. |
| **(2)** conditioned statement + no `--context-entries` → `implicitDeny` | **Does not apply, and that is MEASURED**: the live policy document carries **no `Condition` key**. Stated as a measurement because assuming it is how this mode bites. |
| **(3)** a NONEXISTENT action name also returns `implicitDeny` | `aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY` on `s3:PutObject` → **0 findings**. `simulate` is NEVER used to test whether an action name is real. |

## Controls — the part that makes 11/11 mean something

| control | resource | result | what it proves |
|---|---|---|---|
| **POSITIVE** (separate call) | `.../49financial/leaderboard.json` | **allowed** | the path resolves for a key known to be served |
| **NEGATIVE** (separate call) | `.../platinum/mdpf/whatever.json` | **implicitDeny** | ⛔ **the instrument DISCRIMINATES** — it is not returning `allowed` for everything |
| **UNBORN KEY** (separate call) | `.../49financial/perfrp_zzz_hypothetical_9999.json` | **allowed** | the `/*` wildcard covers leaves **that do not exist yet** — this is the actual AC2 claim |

**The unborn-key test is the load-bearing one.** "No new IAM needed" is a claim about keys that have
never been written. Simulating only the eleven named leaves would have left that claim resting on a
construction argument about wildcards; this measures it.

## Conclusion

**No IAM change is required for any round-1 PERFRP key, and none was made.** The existing scoped grant
covers all eleven by prefix wildcard, and the firm pin proven at AC5 is unaffected — the grant remains
`s3:PutObject` only, on `platinum/advi/49financial/*` only.

## Vintage

Repo HEAD at measurement: `6dcc2c9a61`. ⛔ **A repo commit does not vintage an AWS account.** The
APPLIED and EXERCISED rows above are true of **2026-08-25T09:59Z–10:0xZ** and of nothing else; an IAM
change by any actor after that instant invalidates them without editing this file. Re-measure before
citing this at a publish act.
