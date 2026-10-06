# LG1_ADMIT_SET -- how OG-rl-8 computes the /login admit set BEFORE and AFTER (OG-lg-1, CTO R24)

Author: 0.9.0_WK_NFRA_OPLGTW~22. Read-only method: nothing here writes a grant, a state-store record or a cache, and
no step calls a vendor. Never print an email: name every principal by `audit.email_digest(email)`.

## 1. The two rules

**BEFORE (live `cf4b036e62`).** `/login` admits any identity the access layer (ALB OIDC) and GuardMiddleware let
through: not blocked (`blocklist.enforce`), not on the email deny list (`data_entitlement.email_denial`).
`login()` itself adds no check.

**AFTER (`app/server.py` `login_admit_decision(email, principal=None)`).** The same two pre-checks run first,
unchanged. Then, in order:

| step | refuses with | admits with |
|---|---|---|
| no email | `no_identity` | |
| email in `{OTP_MAILBOX, MS_INGEST_IDENTITY}` | | `server_held` |
| a principal is known and `data_entitlement.current_access(principal).restricted` | `restricted_profile` (`restricted_unreadable` if the store cannot be read) | |
| identity provider not signature-verified, or `tier.resolve_tier` raises | `tier_unresolvable` | |
| email is a key of `identity_scope._load_scopes()` (a scoped service identity) | `scoped_service_identity` | |
| the resolved tier carries no Graph-using tool | `no_graph_tool_at_tier` | |
| otherwise | | `tier_graph_tools` |

**"Graph-using" is derived, not listed.** `server._graph_using_tools()` takes every tool registered on the live
`mcp` (`mcp._tool_manager.list_tools()`) and keeps those whose dispatch takes the caller's delegated Graph token:
a native tool always does (all 42 go through `tools._run` -> `get_token`); an integration tool does only if its
registered spec (`integrations.registry._ACTIVE_BY_TOOL`) has `auth_kind` `DELEGATED_USER`. A tool the tier
"carries" is one `guard.enforce(tool, email, tier)` lets through, the same G2 gate `tools._run` applies (READ_ONLY
carries the SAFE read tools; STANDARD_EMPLOYEE and MASTER_ADMIN carry the write-capable ones too). A new tool or a
new integration changes the set with no edit here.

**What the rule can and cannot see.** The `/login` request carries the access-layer EMAIL and no principal
(`context.py`, `set_current_email`). So on today's GUI path `resolve_tier(None, cfg)` answers the READ_ONLY floor,
which carries the read tools: the tier clause admits every verified, non-restricted, non-scoped identity. A
restricted profile is refused through its email's deny record (written by the restricted `activate` and the
deny-backfill, `access_state.py:458`), which GuardMiddleware checks before the rule runs. The principal branch of
the rule exists for a future path that carries a principal. See row `NFRA_OPLGTW-Z-W22-S11`.

## 2. The current principal population (READ-ONLY)

Build `population.json`, one object per principal: `{tid, oid, email, profile, email_denied, blocked}`.

1. **Persons who have signed in.** Read the refresh-family records of `gateway-access-state-table`
   (partition `RUNTIME#refresh#...`, sort key `oauth_refresh_family`; an authorization code carries `principal`,
   `tid`, `oid`, `email` -- `oauth_as.mint_code`). Use a read-only `dynamodb scan` with `--projection-expression`
   for those fields and `ConsistentRead`, or `AccessState.query` per partition. First print ONE record's KEY NAMES
   (not values) to confirm the family record carries the email; if it does not, take the email from the code or the
   principal-keyed cache owner map the release already reads, and say which in the output.
2. **`profile`.** Read `POLICY#<tid>#<oid>` / `principal_profile` for every principal in step 1 (and scan the
   `POLICY#` prefix for `principal_profile` to catch profiles with no sign-in). A record of any status = `true`.
3. **`email_denied`.** `data_entitlement.email_denial(email)` is the gateway's own read (None / 403 / 503): call it,
   or read `acs.email_deny_key(email)`. A 503 is recorded as `true` (fail closed) and listed.
4. **`blocked`.** `blocklist.enforce(email)` raising `AccessDenied`.
5. **Server-held identities.** Add one entry each for `OTP_MAILBOX` and `MS_INGEST_IDENTITY` (`tid`/`oid` null).
   Their email-keyed caches are not discoverable from the table.
6. Print the denominator: the count of each source and the count of the merged population.

Cross-check against the host: the host holds N principal-keyed caches (row S53 measured 3 written in the window).
File names are `sha256("principal:<tid>/<oid>")`, so they can be matched to step 1's keys without reading content.

## 3. The computation

Export the release's non-secret settings (`OTP_MAILBOX`, `MS_INGEST_IDENTITY`, `MASTER_ADMIN_PRINCIPALS`,
`WRITE_CAPABLE_PRINCIPALS`, `ENABLED_INTEGRATIONS`, `IDENTITY_PROVIDER=alb_oidc`) from the release's own non-secret
source -- never by sourcing `/opt/opal-gateway/.env` -- then, from the gateway directory of the release branch:

    cp lg1_admit_set.py.txt infra/aws/ec2/opal-gateway/lg1_admit_set.py     # scratch only; do NOT commit it
    cd infra/aws/ec2/opal-gateway && python lg1_admit_set.py population.json > admit_set.json

(`deliverables/0.9.0_WK_NFRA_OPLGTW~22/lg1_admit_set.py.txt`.) It prints, by digest only: `admit_before`,
`admit_after`, `lost` (admitted before, refused after, with the reason and whether restricted),
`lost_nonrestricted`, `restricted_not_denied`, and `graph_using_tools`. Exit 1 when `lost_nonrestricted` is not
empty. `RL8_LOGIN.json`'s `admit_before`, `admit_after` and `lost_nonrestricted` are those three arrays.

## 4. How to read the result

- A principal in `lost` that is `restricted: true` is expected (and was already refused today by the deny list
  unless `before` is true because no deny record exists -- then it is the profile-without-deny case below).
- **The Analyst's service identity (`opalbloomberg@opalinvest.com`, the one key of `identity_scope._SEED`) WILL
  appear in `lost_nonrestricted` with reason `scoped_service_identity` when it has signed in.** That is R22/R24's
  ruled refusal ("the Analyst's service identity stays REFUSED"), not a stranded person. The release halves should
  name it by digest and record it as ruled; see row `NFRA_OPLGTW-Z-W22-S12`.
- Any OTHER digest in `lost_nonrestricted` is the blocking case of OG-rl-8: file the BLOCKING row and stop. The
  reasons that can produce one are `tier_unresolvable` (the provider is not signature-verified -- a configuration
  fault, every person is refused) and `no_graph_tool_at_tier` (the registry yields no Graph-using tool the tier
  carries -- e.g. an unreadable registry).
- `restricted_not_denied` non-empty: a profile record with no email-deny record. `/login` cannot see a profile from
  an email, so these are ADMITTED. It is a finding for the halves (backfill the deny record via the existing
  deny-backfill path, by its owner), never a pass.

## 5. What the release proves host-locally (OG-rl-8, from the deployed code)

Synthetic principals only: one non-restricted (a tier-carrying identity) admitted -> consent -> its principal cache
written (a throwaway email, a throwaway cache directory); one restricted (an email on the deny list) refused 403;
one server-held admitted. Each request writes exactly ONE `event: gw_login` audit record; count them in the audit
sink: `requests == audit_records`. A record carries `outcome` (`admitted`/`refused`/`consent`), `email_digest`
(and `principal` for a consent), `reason`, `tier`; it carries no token, code, state or address.
