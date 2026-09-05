# CG-s-5 -- the gateway traversal: APPLIED, DEPLOYED, ENABLED and EXERCISED from a non-gateway seat

**TO:** `NFRA_CLDGRPH.TO-CG-D-2` (REOPENED by the issuer 2026-09-04 ~10:0xZ) | **assignee:**
`0.9.0_WK_NFRA_CLDGRPH~2`, re-dispatched fresh into slot ~2 | **branch:** `wk-NFRA_CLDGRPH-2` (based
on CLOUD @`d5ce612d16`, which already carries the predecessor's build @`4c3999de4a` via the drain
@`329f61c687`) | **date:** 2026-09-04

**Conclusion first.** The cell's closes-on is MET. A seat that is not the gateway host and is not
inside the VPC issued one Cypher traversal through the gateway over HTTPS and got the projection
service's own answer -- `{"rows":[{"nodes":27276}],"vintage":"2026-09-04T12:48:00.440101+00:00",...}`
at HTTP 200 -- and the same request without a bearer got the app's 401. The two Terraform addresses
are APPLIED and read `no-op` on a fresh unscoped plan; the code is DEPLOYED to `i-07dccb1615503ac99`
through `safe-ec2-deploy.sh`; the `globgrph` MCP integration is ENABLED under the CTO's SIGNED G8
(94158) and its two `graph_` tools are registered on the live surface; `--workers 1` is untouched on
the running process; the NEVER-2 ledger `cldgrph-cgd2-gateway-graph-path` is CLOSED with all six legs
proven. Nine of nine mechanical criteria PASS by output. D2-AC10 is judgment and carries no verdict
from this seat. Three new rows: `W2-S8`, `W2-S9`, `W2-S10`.

**What changed since the predecessor's record.** Only the world half. The predecessor's four FAILs
(`D2-AC3`, `D2-AC4`, `D2-AC6`, `D2-AC9`) were all downstream of ONE fabric block -- the shared HALT
gate of `.tools/safe-apply.sh` and `infra/aws/ec2/safe-ec2-deploy.sh` refusing every spine-v3 worker
serial with exit 3 (row `W2-S1`). `1.0.0_SA_CTO` fixed that gate @`68f22f74f5` ("a `0.9.0_WK_<CODE>~<n>`
is a real principal iff a NON-TERMINAL task order under `<CODE>` at HEAD is issued to it"), the issuer
reopened this order, and this seat re-ran the world half. The BUILD is the predecessor's, unmodified
except for the one line G8 authorises; this seat's code delta is `ENABLED_INTEGRATIONS`.

---

## 1. THE APPLY (step 4) -- ledger leg L3

`graph-read.tf` was ALREADY in the shape the reopen asks for and needed no fix: a metadata-only
`data "aws_secretsmanager_secret" "graph_read_bearer" { name = "opal/mcp/graph-read-token" }` plus a
separate `aws_iam_role_policy.gw_graph_read_secret_read` -- the `ms-ingest.tf:16-17,47` shape, no
`random_password`, no `aws_secretsmanager_secret_version`, so no secret value ever enters TF state.
Read and confirmed before touching anything (`comp-read ... --for "whether the secret is referenced by
data source or declared as a resource pair"`).

| step | invocation | result |
|---|---|---|
| init | `terraform -chdir=infra/aws/terraform/opal-gateway init -input=false` | rc 0; lockfile reused, no provider added (`Reusing previous version of hashicorp/aws`) |
| targeted plan | `plan -target=aws_iam_role_policy.gw_graph_read_secret_read -target=aws_lb_listener_rule.graph_capability -out=.build/cgd2-targeted.tfplan` | **`Plan: 2 to add, 0 to change, 0 to destroy`** |
| plan read BY ADDRESS | plan JSON `resource_changes` | DENOMINATOR **7**; exactly two non-`no-op` rows, both this order's |
| apply | `bash .tools/safe-apply.sh -chdir=... apply -input=false .build/cgd2-targeted.tfplan` | halt gate PASS as `0.9.0_WK_NFRA_CLDGRPH~2`; comp-tagauthz PASSED (1 candidate, no access-granting tag overwritten); tombstone-gate CLEAN (2 creates vs 7 tombstones); **`Apply complete! Resources: 2 added, 0 changed, 0 destroyed.`** |

**The terraform binary is named, because it is not the default one.** `.tools/terraform.exe` is
gitignored (`.gitignore:193 .tools/*.exe`), so it does not exist in a `git worktree` checkout and
`safe-apply` would have fallen through to the PATH binary, **v1.14.5**, against a state this tree has
only ever been applied to with the estate's own sibling **v1.9.8**. Rather than let a worktree
accident bump the state format under other seats, the apply ran with
`SAFE_APPLY_TERRAFORM=<main tree>/.tools/terraform.exe` -- which is exactly the binary
`safe-apply.sh`'s documented resolution order prefers when it is present.

**LIVE verification (DESIRED is not APPLIED), read after the apply, not from it:**

```
$ .tools/aws iam get-role-policy --role-name opal-gateway-role --policy-name opal-gateway-graph-read-secret-read
{
    "RoleName": "opal-gateway-role",
    "PolicyName": "opal-gateway-graph-read-secret-read",
    "PolicyDocument": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": ["secretsmanager:GetSecretValue"],
                "Effect": "Allow",
                "Resource": "arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/graph-read-token-MGAqlV",
                "Sid": "GraphReadCapabilityBearerRead"
            }
        ]
    }
}
```

ONE statement, ONE action, ONE secret ARN. **Nothing on any globgrph S3 bucket, nothing on ECS,
nothing on service discovery** -- the R3 control from CG-s-12 ("the moment `opal-gateway-role` needs
`s3:GetObject` on the globgrph bucket, R3 has been broken") holds on the applied plane, not just the
declared one. `list-role-policies` denominator: **8** inline policies, the graph grant the eighth
(it was 7, none matching `graph`, at the predecessor's read -- so the delta is exactly one).

`elbv2 describe-rules` on the HTTPS listener: priority **32** = `["/graph/cypher","/graph/health"]`;
priorities 10 / 20 / 30 / 31 / default unchanged. Exact paths, no wildcard.

**The C-1 control (step 4's second half) -- ledger leg L6.** ONE unscoped
`terraform plan -out=.build/cgd2-unscoped-postapply.tfplan` after the apply, read BY ADDRESS LIST:
`resource_changes` DENOMINATOR **66**; **both of this order's addresses are present and read
`no-op`** (applied and converged); **zero adds** in the headline (`Plan: 0 to add, 2 to change, 2 to
destroy`). The four non-`no-op` rows belong to nobody in this project -- `aws_instance.gw` [update],
`aws_wafv2_web_acl.gw` [update], `aws_wafv2_ip_set.opal_blocked_ips_regional_v4` and `_v6` [DELETE].
That is pre-existing drift, left EXACTLY as found and filed as row **W2-S10** (ARMED: an unscoped
apply in this module would destroy two live WAF IP sets). This order applied two addresses and
touched no WAF or instance file.

## 2. THE ENABLEMENT (step 5) -- the ONE code line G8 authorises

`deploy-to-ec2.sh`'s single `.env` `printf` goes from `ENABLED_INTEGRATIONS=ycharts opal_portal` to
`ENABLED_INTEGRATIONS=ycharts opal_portal globgrph`. Nothing else in the script moved: the
`GRAPH_READ_BEARER` fetch line and the printf's 9-placeholder / 9-argument pairing are byte-unchanged
from `4c3999de4a`, and the value never enters the SSM command text (Rule 12). The comment block above
it was rewritten from "the DORMANCY line below" to the enablement it now describes, with G8's
signature and its conditions named -- a comment that still said DORMANT would be a second carrier of
a quantity that had moved. **No other integration id was added.** Commit `03b1cb0f7d` (LOCAL).

**G7's before-reading, measured on the box rather than assumed** (SSM, `i-07dccb1615503ac99`, BEFORE
the deploy): `.env` carried `ENABLED_INTEGRATIONS=ycharts opal_portal`; `grep -c '^GRAPH_READ_BEARER='`
= **0**; `localhost:8080/graph/health` = **404** (the route did not exist in the deployed bytes).
That is a state that could not be confused with the after-state, which is the point of taking it.

## 3. THE DEPLOY (step 6) -- ledger leg L4

`bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
(Rule 12: local -> S3 -> SSM; no SSH, no inline Python on the box, no file written by hand), rc 0,
one deploy, no re-deploy. `EC2_MANIFEST.json` recorded
`deployed_commit 03b1cb0f7d7fd08984a9845ba53fe7a766bb52d5`, `deployed_by 0.9.0_WK_NFRA_CLDGRPH~2`,
`deployed_at 2026-09-04T12:52:42Z`, and the wrapper self-committed it as `480ffaf58e`.

**Getting the wrapper to run at all cost one write the order did not name** -- row **W2-S9**: the
wrapper deliberately points `HALT_GATE_REPO_ROOT` at the MAIN worktree ("runtime state ... ALWAYS
lives in the MAIN worktree"), and the halt gate resolves its principal from
`${HALT_GATE_REPO_ROOT}/org/mcp/sessions/${CLAUDE_CODE_SESSION_ID}.serial`, so the session serial had
to be written in `ajb_workspace`, not in this worktree. It is gitignored runtime state keyed to this
session's unique id; `git ls-files org/mcp/sessions/` is EMPTY, so no tracked byte moved.

**THE BOX-VERIFY, by SSM, quoted whole** (the deploy's own rc is not evidence -- Rule "NEVER trust a
producer's self-report"):

```
UNIT:
active
HEALTH:
200
POST-ENABLED:
ENABLED_INTEGRATIONS=ycharts opal_portal globgrph
GRAPH-BEARER-LINES:
1
GRAPH-HEALTH-NOBEARER:
401
GRAPH-HEALTH-WITHBEARER:
{"status":"ok","vintage":"2026-09-04T12:48:00.440101+00:00","pointer_read_at":"2026-09-04T12:49:24.482507+00:00","last_swap":"2026-09-04T12:49:24.489568+00:00"}
HTTP:200
INTEGRATION-REPORT:
Sep 04 12:52:31 ip-172-31-89-135.ec2.internal uvicorn[552785]: [integrations] enabled: ['ycharts', 'opal_portal', 'globgrph'] -> {'ycharts': {'tools': [...6 ycharts_ tools...]}, 'opal_portal': {'tools': ['opal_data_refresh_upload'], ...}, 'globgrph': {'tools': ['graph_cypher', 'graph_status'], 'spec': {'id': 'globgrph', 'display_name': 'Estate graph (Kuzu projection)', 'auth_kind': 'none', 'tool_prefix': 'graph_', 'read_only': True, 'min_tier': 'read_only', 'hosts': ['projection.opal-globgrph.local'], 'secret_id': None}}}
```

and the running process, read off the unit's MainPID rather than the unit file (row `W2-S6`:
`ps -C python3.11` returns only its header on this box):

```
MainPID=552785
/opt/opal-gateway/.venv/bin/python3.11 /opt/opal-gateway/.venv/bin/uvicorn app.server:app --host 0.0.0.0 --port 8080 --workers 1
```

`--workers 1` UNTOUCHED, measured AFTER the deploy. `/mcp` unauth still 401 (the wrapper's own
hard gate line), on-box md5 `app/server.py` = `56cdab4f54595eca69680c25608b6d0f`.

## 4. THE EXERCISE (step 7) -- the cell's closes-on -- ledger leg L5

From THIS seat (`hostname` = `Andrew`), which is not `i-07dccb1615503ac99` and is not inside
`vpc-0cc0c6a75e54605e3`, so it cannot reach `http://projection.opal-globgrph.local:8181` at all:

```
$ bash .../deliverables/0.9.0_WK_NFRA_CLDGRPH~2/graph_query.sh
SEAT: Andrew (NOT the gateway host i-07dccb1615503ac99, NOT in the VPC)
POST https://mcp.opalinvest.dev/graph/cypher
STATEMENT: MATCH (n) RETURN count(n) AS nodes
--- response ---
{"rows":[{"nodes":27276}],"vintage":"2026-09-04T12:48:00.440101+00:00","age_line":"Built from the estate as of 2026-09-04 12:48:00 UTC.","manifest_sha256":"7b3d6fd93e7b56c93c2db9e1469582e664cbd3298e2f1c1fc00a4a82716f09e7","artifact_prefix":"projection/2026-09-04T12:48:00.440101+00:00/"}
HTTP_STATUS:200
```

The bearer was read from Secrets Manager into a shell variable with this seat's AWS credentials and
never echoed, never written to a file, never committed. **The vintage, age_line, manifest_sha256 and
artifact_prefix are the SERVICE's own stamps**, passed through verbatim -- this seat invented no
vintage.

**The negative control, and it is a real one:** the same POST with no `Authorization` header ->
**401**. The predecessor read **302** here (the ALB's `authenticate-oidc` default action, because no
`graph_capability` rule existed and the request never reached the gateway app). The move 302 -> 401
is the discriminator: it says the listener rule now forwards the path AND the app then refuses it.
A 302 would have been indistinguishable from "the feature does not exist".

**A second call, seven minutes later, returned a DIFFERENT vintage** --
`{"rows":[{"nodes":27206}],"vintage":"2026-09-04T12:55:59.236365+00:00",...}` -- because the
projection service rebuilt between them. That drift is itself evidence for R3: the gateway holds no
copy and no cache, so what it serves moves when the service moves.

## 5. THE ARCH-GATE RECORD G1-G8 (`NFRA_INTEGRATIONS_STANDARD.md:151-182`) -- D2-AC10, a reading act

| # | gate item | grounding produced by this order | standing |
|---|---|---|---|
| G1 | read-only confirmed | `validate_integration_spec(GlobgrphIntegration().spec)` -> `[]` (D2-AC1, re-run this session); `read_only=True` on the LIVE box's own startup report; both tools issue reads only -- `graph_cypher` POSTs a statement to a read-only projection service, `graph_status` GETs `/health`; the proxy has no write verb at all | **GROUNDED (source + local execution + live box report)** |
| G2 | (a) egress minimal | `hosts=('projection.opal-globgrph.local',)` -- exactly one host, and now read back off the DEPLOYED process's integration report, not only from source. No wildcard, no vendor, no CDN/analytics host | **GROUNDED (live)** |
| G3 | (b) tool surface deliberate | the deployed gateway's startup report: `'globgrph': {'tools': ['graph_cypher', 'graph_status'], ...}` -- EXACTLY two tools, both `graph_`-prefixed, both read-only, on the live MCP surface. The HTTP capability path adds ZERO tools | **GROUNDED (live)** |
| G4 | (c) secret + IAM scoped | LIVE `iam get-role-policy` (quoted in s.1): `secretsmanager:GetSecretValue` on EXACTLY `arn:...:secret:opal/mcp/graph-read-token-MGAqlV`, one statement, and nothing on any globgrph S3/ECS resource. The secret's VALUE exists only in Secrets Manager and on the box's chmod-600 `.env` (minted out-of-band, row `W2-S4`) | **GROUNDED (applied plane)** -- was HOLD in the predecessor's record |
| G5 | `min_tier` + below-tier deny | `min_tier='read_only'` is a known `Tier` and IS the floor, so **no caller can be below it** -- the below-tier-deny exercise is **N/A BY CONSTRUCTION** for this integration (it exists for YCharts because that spec sits at `standard`). Said rather than skipped. What is not N/A: the tier is still resolved and stamped on every audit record by `run_integration_tool` | **N/A-BY-CONSTRUCTION, stated** |
| G6 | audit wired | `run_integration_tool` (`base.py:93-148`, byte-identical to the cut) calls `audit.log_call` on the denied, error and ok branches, and the two tools are now REGISTERED on the live surface. **The served record could still not be produced**: the box's `audit.jsonl` holds **41,489** records and **0** containing `graph_`, because the only run-path that audits is an MCP tool call and `/mcp` requires an ALB `authenticate-oidc` session this seat cannot complete; the `/graph/*` HTTP routes are audit-silent BY CONSTRUCTION, exactly as `/ms/*` and `/otp/*` are. Row **W2-S8** | **PARTIAL -- mechanism grounded, tools live, served record awaits the first authenticated MCP caller** |
| G7 | fail-closed enablement | BEFORE (on the box, not in-process): `.env` = `ycharts opal_portal`, `GRAPH_READ_BEARER` lines **0**, `/graph/health` **404**. AFTER: `.env` = `ycharts opal_portal globgrph`, bearer lines **1**, integration report lists globgrph with exactly **2** tools, `/graph/health` **401** without a bearer and **200** with it. The count moved 0 -> 2 only when the id was added to the list | **GROUNDED (deployed bytes, both sides measured)** -- was PARTIAL |
| G8 | enable = an arch-gated deploy | **SIGNED.** `1.0.0_SA_CTO` to `2.0.0_SA_COO~A`, Msg-ID **94158**, 20260904T094459Z, verbatim: *"THE G8 ARCH-GATE (registry.py ENABLED_INTEGRATIONS, CTO-arch-gated): SIGNED for `globgrph`, riding D-2's deploy, on these conditions which are the order's own criteria: AuthKind.NONE inside the VPC behind the static-bearer path (/graph/cypher, /graph/health), the token only in Secrets Manager (opal/mcp/graph-read-token, minted out of band), the gateway role's policy scoped to that secret's ARN (graph-read.tf), the ALB rule scoped to the graph capability, the deploy change-managed (the cldgrph-cgd2-gateway-graph-path ledger closed at completion), and W2-S2's lifecycle guard on aws_lb.gw kept (a guard, not a repair -- the LIVE-no-DECLARED access_logs are NFRA_GLOBGRPH's surface, carried with its owner). A read-only capability with no write path needs no wider sign."* | **SIGNED, and all six conditions MET** |

**G8's six conditions, each against this order's own evidence:** (1) AuthKind.NONE inside the VPC
behind the static-bearer path -- live report `'auth_kind': 'none'`, `hosts` the one in-VPC Cloud Map
name, both `/graph/*` routes bearer-gated (401 without). (2) The token only in Secrets Manager --
minted out-of-band, no `_version` resource, no value in TF state / repo / log / commit; on the box it
reaches a chmod-600 `.env` and nothing else. (3) The role policy scoped to that secret's ARN -- the
live `get-role-policy` above. (4) The ALB rule scoped to the graph capability -- priority 32, exact
paths, live `describe-rules`. (5) The deploy change-managed -- ledger
`cldgrph-cgd2-gateway-graph-path`, six legs, CLOSED. (6) W2-S2's `lifecycle ignore_changes =
[access_logs]` on `aws_lb.gw` KEPT -- `alb.tf:76-79` unmodified by this seat, and the proof it is
still doing work is that this order's apply reported `0 changed` while the live ALB's access_logs
remain enabled.

**The framework diff, read as the standard's 5-step checklist.** `git diff --stat 5644fee152..HEAD`
over `infra/aws/ec2/opal-gateway/` + `infra/aws/terraform/opal-gateway/` = **9 files, 409
insertions, 2 deletions**: `app/integrations/globgrph/__init__.py` (+6) and `integration.py` (+151)
NEW = **step 1**; `app/integrations/registry.py` (+6: one comment block, one `register_factory` call
at the pre-written slot) = **step 2**; `graph-read.tf` (+48) = **steps 3-4** (the out-of-band secret
+ the one scoped grant); `deploy-to-ec2.sh` (+15/-2) = **step 5** (the fetch, the `.env` line, and
now the enablement); plus `app/graph_read.py` (+64), `app/server.py` (+72), `app/config.py` (+10) and
`alb.tf` (+39) for the capability path. **`base.py`, `tools.py`, `guard.py`, `tier.py` and `audit.py`
do not appear in the diff at all** -- `git diff --name-only` over `app/` returns 6 files, none of
them a framework file -- and `base.py`'s sha256 through `git show HEAD:` is
`718246435530d59e853ed7dca99791d59e1b629e2df516b6a98c3146902cf616`, the value measured at the cut
(D2-AC2). The framework is UNMODIFIED.

**Is the capability path inside or beside the checklist? BESIDE it, and this is the honest reading.**
The standard's five steps describe an integration reaching the MCP surface; `app/graph_read.py` and
the two `/graph/*` routes add nothing to that surface -- they are a second consumer of the same
`query()`/`health()` functions, in the class the gateway already runs twice: `/otp/*` (PREMCP TO-P1c,
`server.py:462-517`, ALB rule priority 30) and `/ms/*` (NFRA_MSGRAPH S2, `server.py:526-582`, ALB
rule priority 31), each a static capability bearer validated constant-time OUTSIDE the `/mcp` guard
because a static bearer is not an RS256 JWT. Two consequences the CVO should hold this order to, and
one of them is now MEASURED rather than predicted. First, **s.6's fail-closed enablement property
does NOT extend to this path**: it went live the moment the code deployed and `GRAPH_READ_BEARER` was
set, and its off switch is the bearer's absence (503) plus the ALB rule, not `ENABLED_INTEGRATIONS`.
The pre/post box readings show the two halves moving independently -- `/graph/health` answered 404
before and 401-without-bearer after, on the same deploy that took the MCP tool count 0 -> 2. Second,
**what has NO precedent-inherited answer is who may hold the bearer**; today the answer is "whoever
can read one Secrets Manager secret", the same answer `/ms/*` gives, stated here rather than assumed.
Third, added by this seat: **the capability path is AUDIT-SILENT** (row W2-S8) -- also the same
answer `/ms/*` and `/otp/*` give, and also stated rather than assumed.

## 6. CRITERIA, as measured this session

| id | verdict | the deciding output |
|---|---|---|
| D2-AC1 | PASS | `VALIDATE []` |
| D2-AC2 | PASS | `718246435530d59e853ed7dca99791d59e1b629e2df516b6a98c3146902cf616` |
| D2-AC3 | **PASS** | `{"rows":[{"nodes":27276}],"vintage":"2026-09-04T12:48:00.440101+00:00",...}` / `HTTP_STATUS:200` |
| D2-AC4 | **PASS** | `401` (was 302 before the listener rule existed) |
| D2-AC5 | PASS | `ENUMERATE: 1 hit(s) across 241 lines / 31 section(s) scanned` |
| D2-AC6 | **PASS** | `POLICYNAMES opal-gateway-graph-read-secret-read` among 8 inline policies (was 7, none matching) |
| D2-AC7 | PASS | `... uvicorn app.server:app --host 0.0.0.0 --port 8080 --workers 1` (MainPID 552785, AFTER the deploy) |
| D2-AC8 | PASS | `OK: pre-commit gate clean for 5 of 5 file(s)` |
| D2-AC9 | **PASS** | `1` -- `**Status:** CLOSED -- nothing stranded -- closed 20260904T131003Z` |
| D2-AC10 | judgment -- recorded in s.5, no verdict | graded by `3.0.0_SA_CVO` at L9 |

**Controls that had to be able to fail.** D2-AC2 hashes the RECORD (`git show HEAD:`), not the
worktree, and moves on any framework byte. D2-AC4 is the fail-closed control and it FAILED for the
predecessor and PASSES now, with a DIFFERENT failure value (302 vs 401) that names which layer
answered. The spec validator was mutated live this session on the real spec: `hosts=()` ->
`['hosts allowlist is empty (egress-governance axis)']`, `read_only=False` -> `['a mutating
integration (read_only=False) requires an explicit elevated min_tier ...']`, baseline `[]` -- so
D2-AC1's `[]` is a measurement, not a vacuous pass. Determinism: D2-AC4 read `401` on two
consecutive runs; D2-AC3's SHAPE is stable across two runs while the vintage and node count moved
(27276 @12:48:00 -> 27206 @12:55:59), which is the service rebuilding, not the criterion wobbling --
and is itself the evidence that the gateway caches nothing.

## 7. THE LEDGER, and what is left

`cldgrph-cgd2-gateway-graph-path` is **CLOSED** -- `**Status:** CLOSED -- nothing stranded -- closed
20260904T131003Z` -- with all six legs carrying proof: L1 commit, L2 the out-of-band secret, L3 the
targeted apply + live IAM/ALB reads, L4 the deploy + on-box md5/unit/argv, L5 the exercise + the
negative control, L6 the unscoped-plan address assertion. The sentinel
`org/critical_paths/.open_deploys/cldgrph-cgd2-gateway-graph-path.json` was present but UNTRACKED in
this worktree (`git ls-files` empty for it, though five sibling sentinels ARE tracked -- the
predecessor's row `W2-S7`), and `deploy_ledger.py close` removed it; so the closure travels in the
entry `.md`, and there is no sentinel byte left to commit.

Nothing on this order is left undone. Carried for others, none of it acted on: **W2-S8** (the served
audit record needs an authenticated MCP caller), **W2-S9** (the worktree/main-tree split in the
deploy wrapper's identity contract), **W2-S10** (four drifting addresses in the opal-gateway
Terraform tree, two of them WAF IP-set deletes, ARMED for the next unscoped apply). Downstream and
not this seat's: CG-s-6 (the thin client consumes `/graph/cypher`) can now be built against a live
endpoint.
