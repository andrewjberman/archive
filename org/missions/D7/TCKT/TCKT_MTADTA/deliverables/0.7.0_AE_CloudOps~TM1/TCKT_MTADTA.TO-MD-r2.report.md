# Report -- 0.7.0_AE_CloudOps~TM1, TCKT_MTADTA.TO-MD-r2 (2026-10-16)

**archetype:** DEPLOY

No secret, tenant id, client id or token appears below. Times are UTC.

## Acceptance
| criterion | line |
|---|---|
| MD2-r2-AC1 | `R2-APP-OK keys=tenant_id,client_id,client_secret` |
| MD2-r2-AC2 | `R2-SUBS-OK Audit.Exchange,Audit.General,Audit.SharePoint` |
| MD2-r2-AC3 | `R2-FIRES-OK invocations_since_start=2 (pages=1) function_errors=0 timeouts=0` (against `fires_since.txt`, 2026-10-16T14:02:59Z) |
| MD2-r2-AC4 | not run, graded or claimed here: the CVO's, on Andrew's live read |
| MD2-r2-AC5 | `R1-GETOBJECT-OK` (admin GetObject on the existing cursor key: AccessDenied; HeadObject: 403) |

Control: the same fires check against `subs_started_at.txt` still refuses (`invocations_since_start=5 ... timed_out_or_errored_reports=3`).

## The steps, in order
1. **Consent (item 2).** The commands for Andrew are in `TCKT_MTADTA.TO-MD-r2.andrew_consent_card.md` (commit ccb3137620). He ran `register_app.py --apply` at about 13:16Z as himself; the issuer relayed it (msg 6692). The consent URL failed with AADSTS1003031 because the script never sets `requiredResourceAccess`; the issuer reports the role assignment was made. The seat did not read the Entra tenant.
2. **Subject key (item 3).** Written once, 64 characters, never printed. The container held no version before.
3. **Subscriptions (item 4), 2026-10-16T13:22:40Z.** Token call HTTP 200. `Audit.Exchange` HTTP 200, `Audit.SharePoint` HTTP 200, `Audit.General` HTTP 200. The sign-in feed is not subscribed. The unified audit-log check (RUNBOOK step 1) was never run: nobody holds an Exchange role.
4. **First collector build failed (item 5).** The 13:31:22Z scheduled fire hit the 300 s limit, verbatim in the log: `REPORT ... Duration: 300000.00 ms ... Status: timeout`; Lambda retried the same request at 13:37 and 13:44. The fires check then printed `R2-FIRES-OK invocations_since_start=2 function_errors=0` on it: it counted REPORT lines and grepped only `errorMessage` and `Traceback`. Reported to the issuer; row `TCKT_MTADTA-D1-S11`; the issuer corrected the check and reopened TO-MD-x2.
5. **Redeploy (item 5a), 2026-10-16T14:02:59Z.** Plan: one in-place update of `aws_lambda_function.collector` (`source_code_hash`, `timeout`), 0 added, 0 destroyed. `safe-apply` rc=0. Live: `Timeout` 900, `CodeSha256` equal to the built zip. Ledger `tckt-mtadta-collector-redeploy-20261016` closed. The earlier ledger `tckt-mtadta-m365-secret-values-and-subscriptions-20261016` still holds its fires leg HELD on the old timeout; it can be released now that AC3 reads OK.
6. **Two scheduled fires.** Fire 1, 14:31:22Z to 14:44:17Z: `fire fetched=1124 bronze_objects=24 failed=0 complete=True`, 774460.97 ms of 900 s. Fire 2, 15:31:22Z: `fire fetched=26 bronze_objects=3 failed=0 complete=True`, 25184.28 ms. No hand invoke. CloudWatch `Errors` 0 for the 14Z and 15Z hours.
7. **Fires check paging defect.** After fire 2 the check printed `R2-FIRES-REFUSED invocations_since_start=1`: its filtered call returned one event plus a `nextToken` and it did not follow it. The issuer corrected it (commit faf5a9fdd3); the rerun reads OK.

## For Andrew's read through the door
The group's invoke needs `aws:MultiFactorAuthPresent`. The commands to take an MFA session and the three environment variables boto3 reads are in the consent card, last section. His MFA devices are `mfa/Andrew_Phone` and `mfa/Yang_Phone` (row `TCKT_MTADTA-D1-S9`).

## Open
- Unified audit logging is unverified; content arrived on the first fire, which suggests it is on.
- Fire 1 took 774 s of 900 s on the 7-day backlog; later fires should be short, and fire 2 took 25 s.
- The admin GetObject refusal covers one key; the cursor is the only object read.
- Push state: LOCAL on box/dell1 at the time of this commit (the origin hash is measured in the commit report).

## Compiler Tools
- `safe-apply.sh`: one apply in this order (5a), rc=0; worked.
- `deploy_ledger.py open / close-leg / hold / close`: worked on two entries; `hold` accepted the open fires leg once the apply legs were proven.
- `r2_check_r2.py fires`: wrong twice. First it read OK on a timeout, then it refused on an unfollowed `nextToken`; both found by reading the log directly, both corrected by the issuer.
- `aws logs filter-log-events`: a filtered call returns a partial page with a `nextToken`; an unfiltered read paginates. Gap: the check had no page count, now added.
- `proof-of-spec-check.py`: VALID rc=0.
