# CG-s-5 -- the gateway traversal: BUILT and DECLARED, world half BLOCKED at the HALT gate

**TO:** `NFRA_CLDGRPH.TO-CG-D-2` | **assignee:** `0.9.0_WK_NFRA_CLDGRPH~2` | **branch:**
`wk-NFRA_CLDGRPH-2` (based on CLOUD @`5644fee152`) | **date:** 2026-09-04

**Conclusion first.** The integration and the capability path are BUILT, gate-clean and committed
(`4c3999d`, LOCAL); the secret exists; the IAM grant and the ALB rule are DECLARED and their plan is
proven to touch exactly those two addresses. Nothing was APPLIED and nothing was DEPLOYED, because
both wrappers this order is required to use -- `.tools/safe-apply.sh` and
`infra/aws/ec2/safe-ec2-deploy.sh` -- refuse a spine-v3 worker serial at their shared HALT gate with
exit 3, which has no audited override (row `NFRA_CLDGRPH-W2-S1`, BLOCKING/ARMED, disarm owner
`1.0.0_SA_CTO`). So `D2-AC3`, `D2-AC4`, `D2-AC6` and `D2-AC9` record the world as it therefore
stands: the cell's closes-on -- a non-gateway seat getting the service's answer through the gateway
-- is NOT met, and the reason is a fabric gate, not the build.

---

## 1. MEASURED FIRST (the read, before any write)

| what | where (file:line @ vintage) | what it gave this order |
|---|---|---|
| the framework | `infra/aws/ec2/opal-gateway/app/integrations/base.py:41-44,47-67,93-139,142-169` @`2781aac326` (byte-identical at `5644fee152`) | `AuthKind.NONE`; the `IntegrationSpec` field order (**`description` is required and has no default** -- row W2-S3); `run_integration_tool`'s WHO/WHICH split; `hosts` non-empty or the spec is skip-registered |
| specimen 1 | `app/integrations/ycharts/integration.py:26-43` (SPEC), `:73-78` (ctor), `:91-103` (register + `run_integration_tool`), `:168-169` (the returned tool-name list) | the shape this integration copies exactly, minus the credential |
| specimen 2 | `app/integrations/opal_portal/` (mutating, `min_tier=standard`) | the counter-example: a mutating spec must carry an elevated tier; ours is read-only at the floor |
| the registry | `app/integrations/registry.py:37` (the pre-written slot), `:43-63` (`register_enabled`, skip-registration) | where the factory line goes and what "dormant" means mechanically |
| the bearer gate | `app/ms_ingest.py:43-45` (`configured`), `:48-50` (`_valid_bearers`), `:53-67` (`check_bearer`, `hmac.compare_digest`, no early exit) | copied verbatim in shape into `app/graph_read.py` |
| the capability routes | `app/server.py:526-534` (`_ms_guard`), `:537-548` (`_ms_run`), `:605-613` + `:607-612` route table (mounted OUTSIDE the `/mcp` Mount and therefore outside `GuardMiddleware`'s JWT path, `:74-77`) | the two new routes sit in the same table, with the same guard shape |
| the ALB precedent | `infra/aws/terraform/opal-gateway/alb.tf:219-234` (`otp_capability`, priority 30), `ms-ingest.tf:129-145` (`ms_ingest_capability`, priority 31) | the rule shape and the next free priority (32) |
| the secret + grant precedent | `ms-ingest.tf:16-18,44-48`; `ycharts-iam.tf:19-38`; `secrets-iam.tf:65-80`; `secrets.tf:6` | metadata-only data source + a SEPARATE scoped `aws_iam_role_policy`; **the value is created out-of-band and never enters TF state** |
| the deploy secret fetches | `deploy-to-ec2.sh:108-109,115,129-131,142` (fetches) and the single `.env` `printf` at `:165` | where `GRAPH_READ_BEARER` had to land: one fetch line + one `%s` + one argument |
| the service API | `infra/aws/globgrph/projection_server.py:413-431` (`_one_statement`: any non-`application/json` content type is read as the raw statement), `:477-500` (the handler) | `POST /cypher` `text/plain`, `GET /health`, response `{rows, vintage, age_line, manifest_sha256, artifact_prefix}` |

## 2. WHAT WAS BUILT

**(a) The integration** -- `app/integrations/globgrph/{__init__.py,integration.py}`:
`IntegrationSpec(id="globgrph", display_name="Estate graph (Kuzu projection)", description=...,
auth_kind=AuthKind.NONE, tool_prefix="graph_", read_only=True, min_tier="read_only",
hosts=("projection.opal-globgrph.local",))`. One proxy pair -- `query(statement)` POSTs the statement
as `text/plain` with a 20 s bound and returns the service's JSON verbatim; `health()` GETs `/health`
-- plus `register(mcp)` adding exactly `graph_cypher(statement)` and `graph_status()`, each through
`run_integration_tool(...)` with a credential provider returning `None`. Every failure is raised as
`IntegrationError`, so a proxy fault is a friendly error on the MCP surface and a 502 on the HTTP
surface, never a 500. The proxy reads no S3, caches nothing, and passes the statement through
unmodified. `registry.py` gains ONE `register_factory("globgrph", GlobgrphIntegration)` line at the
pre-written slot.

**(b) The capability path** -- `app/graph_read.py` (`configured()`, `_valid_bearers()`,
`check_bearer()` constant-time, and the two proxy functions re-exported so `server.py` never reaches
into the integrations package), routes `POST /graph/cypher` + `GET /graph/health` in `server.py`
beside `/ms/*`, sharing `_graph_guard` (503 unconfigured, 401 `{"error":"unauthorized"}` with
`WWW-Authenticate: Bearer`); the body is accepted as raw `text/plain` or as JSON
`{"statement": ...}`; `config.py` gains `GRAPH_READ_BEARER` exactly as `MS_INGEST_BEARER` is read;
`deploy-to-ec2.sh` fetches `opal/mcp/graph-read-token` beside `MS_INGEST_BEARER` and writes it into
the `.env` printf (9 placeholders, 9 arguments, order verified; the value never enters the SSM
command text). **One implementation, two surfaces**: the MCP tools and the HTTP path call the same
`query()`/`health()`.

**The secret + the grant** -- `opal/mcp/graph-read-token` minted OUT-OF-BAND (boto3, 48 alphanumeric
characters), ARN `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/graph-read-token-MGAqlV`
(live `describe-secret`); `graph-read.tf` references it metadata-only and declares
`aws_iam_role_policy.gw_graph_read_secret_read` granting `secretsmanager:GetSecretValue` on EXACTLY
that ARN on `opal-gateway-role` -- and nothing on any globgrph S3/ECS resource, which is the R3
control from V-2 B.3(iii). Why out-of-band rather than the order's `random_password` +
`aws_secretsmanager_secret_version`: row `NFRA_CLDGRPH-W2-S4` (the `random` provider is in neither
`required_providers` nor the lockfile, both outside this order's `<paths>`, and a `_version` resource
would put the value in TF state against `secrets.tf:6`).

**The ALB rule** -- `alb.tf` gains `aws_lb_listener_rule.graph_capability`, priority 32, exact paths
`["/graph/cypher","/graph/health"]`. Priorities 10/20/30/31 are taken on the declared plane AND on
the live plane (`elbv2 describe-rules`, 2026-09-04: 10, 20, 30, 31, default).

**The one edit this order did not ask for** -- `aws_lb.gw` gains
`lifecycle { ignore_changes = [access_logs] }` (row `NFRA_CLDGRPH-W2-S2`). The live ALB ships access
logs to `opal-data-security/waf-logs/alb-opal-gateway` with `enabled=true`; the repo declares
`access_logs` nowhere (0 hits / 496 terraform files; 0 hits / 28,361 files for the prefix). Every
listener rule's dependency closure reaches `aws_lb.gw`, so the targeted plan for this order's two
addresses planned `~ update aws_lb.gw` flipping that flag to **false**. The guard leaves the live
setting exactly as found; it is not a repair, and the drift stays for its owner.

## 3. THE PLAN, AND WHAT IT PROVES

`terraform plan -target=aws_iam_role_policy.gw_graph_read_secret_read
-target=aws_lb_listener_rule.graph_capability` -> `Plan: 2 to add, 0 to change, 0 to destroy`; the
plan JSON's `resource_changes` (denominator **7**) carries exactly two non-`no-op` rows, both this
order's. Before the `ignore_changes` guard the same command read `2 to add, 1 to change` with
`aws_lb.gw` in the change set -- so the guard is what makes "exactly your new addresses" TRUE rather
than asserted. `terraform fmt -check` rc=0 on both `.tf` files; `terraform init` reused the existing
lockfile (no provider added).

**The apply did not run.** `bash .tools/safe-apply.sh -chdir=infra/aws/terraform/opal-gateway apply
-input=false .build/cgd2-targeted.tfplan` -> **rc=3**, `HALT-GATE: SERIAL RESOLVES TO NO KNOWN AGENT`.
`bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` ->
**rc=3**, `HALT-GATE: IDENTITY UNRESOLVED` (that wrapper resolves `HALT_GATE_REPO_ROOT` against the
MAIN tree, so a session-serial file written in this worktree is invisible to it; its first run died
even earlier, at `jq: command not found`, until `.tools/` was put on PATH). `halt_gate_validate_serial`
(`.tools/halt-gate-check.sh:134-154`) requires an agent home folder under `org/tier*_*/` and a
single-uppercase-letter lane; 112 home folders were censused and none matches `0.9.0_WK`, and the
worker's slot suffix is a digit. Exit 3 carries no `HALT_ACK`/`HALT_OVERRIDE` path and the banner
forbids overriding, so nothing was overridden, no bare `terraform apply` was run, and no non-Rule-12
route to the box was taken.

## 4. THE ARCH-GATE RECORD G1-G8 (`NFRA_INTEGRATIONS_STANDARD.md:151-182`) -- D2-AC10, a reading act

| # | gate item | grounding produced by this order | standing |
|---|---|---|---|
| G1 | read-only confirmed | `validate_integration_spec(GlobgrphIntegration().spec)` -> `[]` (D2-AC1); `read_only=True`; both tools issue reads only -- `graph_cypher` POSTs a statement to a read-only projection service, `graph_status` GETs `/health`; there is no write verb on the proxy at all | GROUNDED (source + local execution) |
| G2 | (a) egress minimal | `hosts=("projection.opal-globgrph.local",)` -- exactly one host, the in-VPC Cloud Map name from the CG-s-4 handoff; no wildcard, no CDN/analytics host (the YCharts Pendo exclusion has no analogue here: there is no vendor) | GROUNDED |
| G3 | (b) tool surface deliberate | `register()` returns exactly `["graph_cypher","graph_status"]`; measured in-process: `register_enabled(mcp, ["globgrph"])` -> `{'globgrph': {'tools': ['graph_cypher','graph_status'], ...}}`, 2 tools, both `graph_`-prefixed, both read-only | GROUNDED (local, in-process) |
| G4 | (c) secret + IAM scoped | DECLARED: `graph-read.tf` grants `secretsmanager:GetSecretValue` on exactly the one secret ARN. **NOT APPLIED**: live `aws iam list-role-policies --role-name opal-gateway-role` returns 7 inline policies, none of them the graph grant (D2-AC6 FAIL). The secret exists live (`describe-secret`) and its value is in Secrets Manager only | **HOLD** -- declared-not-applied, blocked by W2-S1; a gate item that cannot be grounded on the live artifact is a HOLD, not a pass |
| G5 | `min_tier` + below-tier deny | `min_tier="read_only"` is a known `Tier` and IS the floor, so **no caller can be below it** -- the below-tier-deny exercise is N/A BY CONSTRUCTION for this integration (it exists for YCharts because that spec sits at `standard`). What is NOT N/A is that the tier is still RESOLVED and stamped on every audit record | N/A-BY-CONSTRUCTION, stated rather than skipped |
| G6 | audit wired | `run_integration_tool` (`base.py:93-148`) is the run-path for both tools: it resolves the caller, applies the identity scope + `enforce_min_tier`, and calls `audit.log_call` on the denied, error and ok branches. **The SERVED audit records (one ok + one denied read off the box's `audit.jsonl`) could not be produced**: no `graph_` call has ever run on the box, because the integration is dormant AND the deploy is blocked | **HOLD** -- source-grounded only; the served-record half awaits the deploy |
| G7 | fail-closed enablement | Measured in-process on this code: `register_enabled(mcp, [])` -> report `{}` and **0** tools added; `ENABLED_INTEGRATIONS` in `deploy-to-ec2.sh` is byte-unchanged (D2-AC5, exactly 1 occurrence of `ENABLED_INTEGRATIONS=ycharts opal_portal`). **On the DEPLOYED bytes this is unproven** -- the deployed bytes are still the pre-order ones, which do not contain the integration at all; that is dormancy of a stronger kind, but it is not the same measurement | PARTIAL -- proven locally, unprovable on the box until the deploy lands |
| G8 | enable = an arch-gated deploy | NOT SIGNED, and not this seat's to sign: **AWAITING the round-N analysis**. `globgrph` is absent from `ENABLED_INTEGRATIONS`; enabling it is env+IAM+deploy after the CTO signs G1-G7 | AWAITING `1.0.0_SA_CTO` at L10 |

**The framework diff, read as the standard's 5-step checklist.** `git diff --stat 5644fee152..HEAD`
touches, under the gateway app: `app/integrations/globgrph/__init__.py` + `integration.py` (NEW, step
1), `app/integrations/registry.py` (+6 lines: one comment block and one `register_factory` call at the
pre-written slot, step 2), and then `app/graph_read.py` (NEW), `app/server.py` (+72), `app/config.py`
(+10), `deploy-to-ec2.sh` (+10/-2). `base.py`, `tools.py`, `guard.py`, `tier.py` and `audit.py` do not
appear in the diff at all; `base.py`'s sha256 through `git show HEAD:` is unchanged from the cut
(D2-AC2). Steps 3-4 (secret + IAM) exist as the out-of-band secret and the declared grant; step 5
(enable + deploy) is deliberately NOT taken.

**Is the capability path inside or beside the checklist? BESIDE it, and this is the honest reading.**
The standard's five steps describe an integration reaching the MCP surface; `app/graph_read.py` and
the two `/graph/*` routes add nothing to that surface -- they are a second consumer of the same proxy
function, in the class the gateway already runs twice: `/otp/*` (PREMCP TO-P1c, `server.py:462-517`,
ALB rule priority 30) and `/ms/*` (NFRA_MSGRAPH S2, `server.py:526-582`, ALB rule priority 31), each a
static-capability bearer validated constant-time OUTSIDE the `/mcp` guard because a static bearer is
not an RS256 JWT. Two consequences the CVO should hold this order to. First, the fail-closed
enablement property of s.6 does NOT extend to this path: it is live the moment the code deploys and
`GRAPH_READ_BEARER` is set, exactly as `/otp/*` and `/ms/*` are, and its "off switch" is the bearer's
absence (503) plus the ALB rule, not `ENABLED_INTEGRATIONS`. Second, the arch-gate's three axes still
bind it and are answered above: egress is the same single host (G2), the tool surface it adds to the
crown-jewel MCP gateway is ZERO (G3 -- it adds an HTTP route, not a tool), and the secret+IAM axis is
the same one scoped grant (G4). What has NO precedent-inherited answer is who may hold the bearer;
today the answer is "whoever can read one Secrets Manager secret", which is the same answer `/ms/*`
gives, and it is stated here rather than assumed.

## 5. CRITERIA, as measured

| id | verdict | the deciding output |
|---|---|---|
| D2-AC1 | PASS | `VALIDATE []` |
| D2-AC2 | PASS | `718246435530d59e853ed7dca99791d59e1b629e2df516b6a98c3146902cf616` |
| D2-AC3 | **FAIL** | `HTTP_STATUS:302` (the ALB's authenticate-oidc default -- no `graph_capability` rule exists, and no gateway code on the box knows the path) |
| D2-AC4 | **FAIL** | `302` (same reason; the 401 this control is built to see can only come from the gateway app, which the request never reaches) |
| D2-AC5 | PASS | `ENUMERATE: 1 hit(s) across 236 lines / 31 section(s) scanned` |
| D2-AC6 | **FAIL** | 7 inline policies on `opal-gateway-role`, none matching `graph` (denominator 7) |
| D2-AC7 | PASS | `/opt/opal-gateway/.venv/bin/python3.11 .../uvicorn app.server:app --host 0.0.0.0 --port 8080 --workers 1` (PROBE-2; the TO's own `ps -C python3.11` form returns only its header -- row W2-S6) |
| D2-AC8 | PASS | `OK: pre-commit gate clean for 5 of 5 file(s)` |
| D2-AC9 | **FAIL** | `OPEN: cldgrph-cgd2-gateway-graph-path ... stranded=['L3','L4','L5','L6']` -- and note row W2-S5: this invocation could not have printed CLOSED even on a perfect run |
| D2-AC10 | judgment -- recorded above, no verdict | graded by `3.0.0_SA_CVO` at L9; G8 is `1.0.0_SA_CTO`'s at L10 |

**Controls that had to be able to fail, and did.** D2-AC2 is a hash of the record, not the worktree
(`git show HEAD:`), and would move on any framework byte. D2-AC4 and D2-AC5 are the fail-closed
controls; AC4 in fact FAILED, which is the control working -- it says the path is not reachable, not
that it is open. The spec validator was mutated twice (`hosts=()` -> `['hosts allowlist is empty
(egress-governance axis)']`; `tool_prefix=""` -> `['tool_prefix is empty (namespace-hygiene axis)']`),
so `[]` on the real spec is a measurement rather than a vacuous pass.

## 6. WHAT IS LEFT, AND FOR WHOM

The NEVER-2 ledger `cldgrph-cgd2-gateway-graph-path` is OPEN with L1 (commit) and L2 (secret) closed
with proof and L3-L6 never started; the entry file carries the four commands that close it and the
order to run them in. `deploy_ledger.py hold` was REFUSED for this entry -- correctly, since it cannot
tell a never-started deploy from a half-landed one -- so the entry stays OPEN and blares, which is the
signal this situation deserves. Six rows are filed (`W2-S1`..`W2-S6`), the channel's first
worker-coordinate rows; the header denominator was restated 32 -> 38.
