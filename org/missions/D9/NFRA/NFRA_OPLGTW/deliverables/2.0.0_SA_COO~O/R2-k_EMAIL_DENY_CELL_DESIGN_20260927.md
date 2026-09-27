# NFRA_OPLGTW R2-k -- the email-keyed deny cell (row W3-S22): design for the cut

**By:** `2.0.0_SA_COO~O`, OPLGTW's COO leg since the re-seat @6fba157e76. Routed by `1.0.0_SA_CTO~O`'s ruling
`deliverables/1.0.0_SA_CTO~O/RULING_W3-S22_20260927.md` @244cd0d80f. The fix is CTO ruling 97251 (row S17): "an
email-keyed deny record in the access-state table". It is DUE before the next restricted profile is granted to anyone who
can complete the ALB login.

**Source:** a read-only design pass over `infra/aws/ec2/opal-gateway/` at HEAD 0aaf865219. Paths below are relative to that
directory; line numbers are HEAD's. HEAD differs from the live 110d93fb73 only by TX-g-1 (`server.py:65,899-902`,
`config.py:221-229`, tests), so `server.py` lines sit +1 against live.

## Design

- **Record.**
  - Key: pk `POLICY#EMAILDENY#<sha256hex("og-email-deny/v1|" + email.strip().lower())>`, sk `email_deny`.
  - Body: `{tid, oid, status:"active"}`, no TTL. It is a new POLICY record type `email_deny`.
  - It cannot collide with a real principal: a 64-hex digest is never a 36-character GUID oid.
  - The email is HASHED because the adapter puts a refused key into exception text. That text reaches denial bodies (`data_entitlement.py:403`), the audit detail (`server.py:552`) and admin CLI output. The hash is key hygiene, not secrecy.
  - It only ever adds denial, as the email lines in `revocation.py:107-111` do.
- **IAM / Terraform / .env:** no change.
  - The table name is a constant (`access_state.py:42`).
  - The operator role and the grant-writer Lambda already hold PutItem on `POLICY#*` (`terraform/opal-gateway/schwab_access_state.tf:154-158`, `mcportal_grant_writer.tf:87-91`).
  - The runtime GetItem is unconditioned (`:99`), and runtime writes stay refused (`access_state.py:172-177`, IAM `:112`).
- **Guard.** Add `data_entitlement.email_denial(email, store)`, returning 403 when denied, 503 when the table is unreadable, and None otherwise.
  - `GuardMiddleware`, right after `enforce(email)` at `server.py:206`. One hook covers `/login`, `/sprint`, `/sprint/`, `/sprint/archive` and `/sprint/{day}`. It runs before any S3 read (`sprint_view.py:190,199,224`) and before the consent URL (`server.py:432-434`).
  - Legacy `/callback` (`server.py:479-491`), which runs no `enforce()` today: between `:483` and `redeem_consent` at `:485`.
  - A second check on the validated principal email inside `token_broker.redeem_consent`, after `:337` and before the cache writes at `:339-340`. The Entra account picker (`token_broker.py:223`) lets the signed-in account differ from the state's email.
  - boto3 blocks, so the lookup runs in the thread pool under a time budget, as `browser_oidc.py:170-175` does.
- **Writer** (`ops/schwab_entitlement_admin.py`).
  - `access_state` relaxes the one-partition rule (`:438-439`) to "the principal's partition plus at most one `email_deny` put".
  - A restricted `activate` (`:309-324`) adds the deny put with condition `attribute_not_exists(pk) OR (tid=:tid AND oid=:oid)`, so re-activation still works.
  - The email comes from the candidate (`:158`) or else the stored profile; with neither, it refuses (`CandidateRejected`).
  - A one-shot `deny-backfill --tid --oid [--email ...]` mode strongly reads the profile and writes the deny record(s) plus an audit item in one transaction. It serves the one profile that exists (OA-g-3).
- **Second writer:** the grant-writer Lambda (`lambda/mcportal/mcportal-grant-writer-lambda/lambda_function.py:280-295`) runs a staged copy of the same `activate`. It must be rebuilt and applied, or its first profiles get no deny record.

## BUILD cell criteria (all runnable without moto; moto is not installed on site Z)

1. `python -m pytest tests/test_email_deny.py -q -p no:cacheprovider` reads `10 passed`. The 10 tests, run through the existing seams `AccessState(client=stub)`, `store=` and `server.app` in a TestClient with the ALB check stubbed (the `test_owner_gate.py:36-93` pattern):
   - key shape and normalisation;
   - a runtime write is refused;
   - the 5 routes return 403 and touch neither S3 nor the consent URL;
   - a non-denied email gets 200;
   - a store error gives 503 on all 5 routes;
   - legacy `/callback` returns 403 and never calls `redeem_consent`;
   - a restricted `activate` puts the deny record in the same single transaction;
   - revoke leaves the deny record;
   - backfill writes one transaction;
   - backfill refuses when no profile exists.
2. `python -m pytest tests/test_owner_gate.py tests/test_portal_grant.py tests/test_sprint_view.py tests/test_asker_scope.py -q -p no:cacheprovider` reads `24 passed`, with its value at the base recorded first. `test_owner_gate.py:152-163` needs a stub store, or `/sprint` answers 503.
3. `python ops/schwab_entitlement_admin.py deny-backfill --help`: rc 0, listing `--tid --oid --email --approver --source-authorization`.

## SERVED steps after the build (separate acts, each under never-widen)

1. A narrow gateway release: live commit + this change, the MX-r-3 pattern. Afterwards, `/sprint` still serves a non-restricted staff account.
2. `deny-backfill` for the OA-g-3 principal under `opal-gateway-access-admin`, then read back: that account now gets 403 on `/sprint` and `/login`.
3. The grant-writer Lambda rebuilt and applied.

## Calls that are the CTO's (a contract change and served behaviour)

| # | Call | COO recommendation |
|---|---|---|
| 1 | Revoke KEEPS the deny record (a revoked profile still makes the person restricted, `data_entitlement.py:31-33`; no delete path or DeleteItem exists). An explicit lift act, yes or no? | Keep it on revoke. A lift is a later, separate operator act, cut only when someone must be un-restricted. |
| 2 | Fail-closed (503) on the 5 routes when the table is unreadable takes tenant-wide `/sprint` down during a DynamoDB outage | Fail-closed, matching the file's convention for restricted profiles (`access_state.py:20-22`, `data_entitlement.py:446-447`). |
| 3 | The ALB `email` claim (`config.py:164`) may differ from the address the operator supplies | Backfill and activate accept repeated `--email`, one deny record per alias, and the post-validation check in `redeem_consent` stays. |
| 4 | Release base: HEAD also carries TX-g-1 | Build from the live 110d93fb73 plus this change (R-8 narrow). TX-g-1 ships on its own word. |
| 5 | `org/standards/NFRA_OPLGTW_CONTRACT.json` `record_types` grows 9 -> 10 | A contract amendment, the CTO's. |

Also known: until the Lambda is rebuilt (SERVED step 3), a first profile created through the grant writer gets no deny
record. So step 3 must land before any grant is made through the dashboard.
