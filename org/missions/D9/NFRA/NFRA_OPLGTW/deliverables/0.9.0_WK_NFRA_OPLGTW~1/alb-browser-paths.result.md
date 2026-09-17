# NFRA_OPLGTW.TO-OG-i-3 -- alb-browser-paths result

**Assignee:** 0.9.0_WK_NFRA_OPLGTW~1  **Branch:** wk-nfra_oplgtw-1h  **Cut from:** CLOUD @3207f5ea09

## What happened

Three things landed in one apply on `infra/aws/terraform/opal-gateway`:

1. **FIRST ACT -- the lambda source-map hash fix** (R-OG-9 call 9(a)): `infra/aws/lambda/ci/lambda-source-map.json`'s `opal-assets-silver-schwab.artifact_sha256` was stale from OG-c-2's uncommitted build. Confirmed equal to the live function's `CodeSha256` (`v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=`) via a read-only `lambda get-function-configuration`, then edited exactly one line (`git diff` confirmed), committed alone (`0653087377`) before any apply.

2. **FIRST ACT -- the R-OG-7 rename.** OG-i-2's three person-named/OUT-OF-PATTERN identities were renamed to `lib/opal_naming.py name()` output, printed and used verbatim (never typed):
   - `opal-mcp-emp-menachem-schwab-read` -> `gateway-schwab-read-role`
   - `opal-mcp-schwab-catalog-read` -> `gateway-schwab-catalog-read-role`
   - `opal-gateway-assume-schwab-readers` -> `gateway-assume-schwab-readers-policy`

   Every consumer moved together in one commit (`b2e4a10678`): `schwab_reader_iam.tf` (the two role
   locals, the assume-policy resource's `name`, and the header/section comments), `aws_roles.py`'s
   docstring quote of PRD C6 (the module itself never hardcodes either name -- it reads the contract's
   `reader_role`/`catalog_role` at runtime and checks the configured ARN's role-name segment against it),
   and `NFRA_OPLGTW_CONTRACT.json` (`reader_role`, `catalog_role`, and a new `assume_readers_policy`
   field, all under the v1.1 OG-i-5 already opened). `infra/aws/ec2/opal-gateway/tests/
   test_schwab_catalog.py`: 17 of 17 PASS unchanged (it never types either role name).

3. **The read-only host-command document** (R-OG-6, extending R-OG-2): one `aws_ssm_document` resource
   (`ssm_readonly_host.tf`), document type `Command`, name `gateway-readonly-host-document` (builder
   output), content a FIXED list of read-only shell steps (systemd unit status, `/proc/<pid>/status`
   RSS, sha256 file digests under `/opt/opal-gateway`, installed package versions via `rpm -qa` with a
   `dpkg -l` fallback) with an empty `parameters` block -- no caller-supplied interpolation is possible.
   The operator role `opal-gateway-access-admin` gains one new inline policy
   (`gateway-access-admin-ssm-readonly-policy`) granting `ssm:SendCommand` pinned to exactly this
   document's ARN plus the Gateway instance's ARN; nothing else was added to that role.

4. **The ALB's four explicit browser paths.** One new `aws_lb_listener_rule` (`alb.tf`,
   `schwab_download_browser`, priority 34 -- the next free slot after 10/20/30/31/32/33) forwards
   `/schwab/download/login`, `/schwab/download/callback`, `/schwab/download` and
   `/schwab/download/exchange` WITHOUT `authenticate-oidc`. The four values are read from the two merged
   path records (`0.9.0_WK_NFRA_OPLGTW~3/BROWSER_PATHS.json`, `0.9.0_WK_NFRA_OPLGTW~5/DOWNLOAD_PATHS.json`)
   and never typed from memory. Every pre-existing rule, the default `authenticate-oidc -> forward`
   action, the WAF association and `idle_timeout` are unchanged (see OGI3-AC1/AC3/AC5/AC6 below).

## Sequence (one ledger entry `nfra-oplgtw-og-i-3-alb-paths`, two legs: `apply`, `readback`)

1. Ledger opened, sentinel + record committed `be6ba30d5d` (14:04:15-04:00), **before** the apply.
2. `terraform fmt`/`validate` clean; saved plan: `8 to add, 0 to change, 5 to destroy` -- exactly the 5
   resources whose own-name attribute changed (the two roles + their three name-bearing inline policies)
   plus the 3 new resources (SSM document, its pin policy, the new listener rule). OG-i-2's other five
   resources (the two ExternalId/account_ref secrets, their versions and resource policies) reference the
   Gateway role, not the renamed roles, so they were untouched -- within the order's "at most the ten
   OG-i-2 resources" ceiling, actual blast radius five.
3. Applied through `.tools/safe-apply.sh -chdir=infra/aws/terraform/opal-gateway apply` under
   `HALT_ACK=1` (18 pending ROUTINE messages on the issuer's inbox, none STOP-class). The naming plan
   gate graded 48 resource-name attributes, 0 REFUSE (the 5 renamed/replaced + 3 new resources all
   CONFORMANT; 11 pre-existing OUT-OF-PATTERN names elsewhere in the tree WARN'd, never REFUSE, because
   none of them is an ADDITION in this plan). `comp-tagauthz` PASSED (no access-granting tag overwritten).
   The tombstone gate read CLEAN (8 creates checked against 7 tombstones). Apply rc0: `Apply complete!
   Resources: 8 added, 0 changed, 5 destroyed.`
4. Live readback: `iam get-role` on both new role names present with new ARNs; the old names
   `NoSuchEntity`; `iam get-role-policy` on both roles shows the unchanged 6-Sid deny/allow shape; the
   Gateway role's `gateway-assume-schwab-readers-policy` names both new role ARNs with two distinct
   re-keyed ExternalIds; `ssm describe-document gateway-readonly-host-document` -> `Status: Active`.
5. Ledger closed (both legs proven), committed `6563b4d471`, **before** the OGI3-AC1..AC6 grading reads.
6. `SCHWAB_IDENTITIES.json` rewritten with the new names/ARNs, live-read after the apply (no ExternalId
   value, key or credential recorded).

## Acceptance

| id | verdict | deciding line |
|---|---|---|
| OGI3-AC1 | PASS | the plan's one non-no-op `aws_lb*` resource is the new rule; its 4 path values == the two merged records; `aws_lb_listener.https` no-op |
| OGI3-AC2 | PASS | ledger opened+committed (`be6ba30d5d`) before the apply, closed+committed (`6563b4d471`) before this reading; apply.log carries every safe-apply gate marker |
| OGI3-AC3 | PASS | 7 of 7 baseline HTTPS-listener rules + the HTTP:80 default rule byte-equal live; only new priority is 34 |
| OGI3-AC4 | PASS | unrelated path 302s to `login.microsoftonline.com` (server=awselb); all 4 explicit paths 404 with server=uvicorn, no Location (reach the application) |
| OGI3-AC5 | PASS | `idle_timeout.timeout_seconds=60`, ARN + UTC vintage printed, == baseline |
| OGI3-AC6 | PASS | WAF association (`opal-gateway-waf`, 5 rules) identical to baseline |

Full measurement output for each: `evidence/og_i3/` and the proof-of-spec instance's `acceptance[]`.

## Finding disclosed at AC4 (see NFRA_OPLGTW-W1-S13)

The four explicit paths currently return `404` from the Gateway application itself, not `200`/a real
page -- OG-a-3's and OG-x-1's route code (`app/browser_oidc.py`, `app/download_routes.py`) has not been
deployed to the EC2 instance by this cell (no `EC2_MANIFEST.json`, deploy script or `app/` path is in
this order's `<paths>` grant; that on-box deploy is a separate, later act). AC4 only requires the request
to *reach the application* (as distinct from being intercepted by the ALB's own OIDC redirect), which the
404-with-no-Location response demonstrates unambiguously against the unrelated path's 302-with-Location.

## Declared exclusion: the FIRST ACT's "re-run OG-i-2's live denial and assume arms" (see NFRA_OPLGTW-W1-S13)

OG-i-2's `host_arm()`-based assume/denial arms run a dynamic, per-call shell script (role ARN, ExternalId,
S3 key as parameters) via SSM `AWS-RunShellScript`. R-OG-6 forbids `AWS-RunShellScript` **from this cell
onward** and permits only the one named, fixed, parameterless document this same cell installs -- whose
content is scoped to "the reads later cells need" (file digests, systemd, RSS, packages), not an
assume-role/GetObject diagnostic. Re-running those arms as written would require either violating the
`AWS-RunShellScript` prohibition or parameterizing the new document (reopening the caller-supplied-
interpolation hole R-OG-6 exists to close). Refused as written; substituted a declared-level check
instead (`iam get-role` / `get-role-policy` trust + inline-policy readback against the new ARNs, recorded
above and in `SCHWAB_IDENTITIES.json`), disclosed as a weaker instrument than a host-exercised arm, and
filed as `NFRA_OPLGTW-W1-S13`.

## Controls

- **Mutant:** `evidence/og_i3/live_rules.json` was mutated in a scratch copy (priority-10 rule's
  path-pattern value changed) and swapped in for one run: AC3 correctly FAILed
  (`changed=['arn:...4ea29ffe7abbebf4']`). The original was restored and verified byte-identical by
  `diff` before any further grading.
- **Determinism:** the full AC1..AC6 sweep was run three times in this session (plus one AC3-only run
  between them); every criterion's output was identical PASS text across every non-mutated run.

## Rows

`NFRA_OPLGTW-W1-S13` (OBSERVATION, INERT) -- the FIRST ACT/R-OG-6 tension described above.
