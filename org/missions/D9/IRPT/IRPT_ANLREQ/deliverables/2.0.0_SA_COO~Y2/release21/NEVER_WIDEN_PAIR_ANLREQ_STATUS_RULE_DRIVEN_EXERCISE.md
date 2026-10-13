# IRPT_ANLREQ round 21 -- the driven exercise of the status rule on `irpt-directory-search` (two refusal arms, one optional admitted arm) -- never-widen pair, COO half

**WRITTEN, NOT RUN. Nothing is minted until the CTO half is signed on this file's blob and an order cites both.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-13. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Asked for by the CTO's round-21 analysis (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_ANLREQ_Y_ROUND_21_20261013.md`, section 2 item 4 and section 3 item 3: "NO FWD IS A WAIT: drive it"). It rests on the design record of cell `AR-y-223` (`deliverables/0.9.0_WK_IRPT_ANLREQ~69/r21/EXERCISE_DESIGN.json`, drained @99be725fee), which the cell's own proof (VALID) and check (`Y223-DESIGN-OK`) carry and this seat re-ran. Shape and precedent: the R2-cw-1 pair (`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_CW1_CRAWL_PAIR.md` and its CTO half).

Claim words: MEASURED = this seat ran or read it; RECORD = a committed record this seat opened (and re-ran where it says so); OFFLINE = run on the shipped bytes without a token, a key or an AWS call; INFERRED = said so.

## 1. What the act is, and why it is driven

The status rule (an internal caller who selects another firm is admitted only with an `active` row in `opal-users-v2`; no row or any other status is refused `FIRM_BINDING`) has run in all eight packagers since 2026-10-13 ~13:07Z. In its first hour no internal caller met it (A4: 0 `INTERNAL-CALLER-CLASS` lines; the zero is vacuous for seven functions and for directory-search none of 57 to 69 invocations was a cross-firm selection). Waiting for one is a wait, so the exercise drives it with two synthetic internal identities, in one sitting, and removes them.

## 2. The route, the request, the firm (RECORD, read from the code by `AR-y-223`)

- `GET /api/scoped/investor-reporting/directory/search` on `irpt-directory-search`; the firm is selected by the query member `selected_tenant=cottonwood` (`directory/entry.py` 392-393; `_authz/served.py` 535-560); no `q`, no `limit`, no body. Read-only.
- **The selected firm is `cottonwood`, and no other choice exists.** The live map (`IRPT_DIRECTORY_BUCKET_MAP`, `directory/lambda.tf` 44; `iam.tf` 28, 31-34, 48) admits only client firms (49financial, inflection, cottonwood); `demo` and `mockadv` are refused BEFORE the status test with no class line (`served.py` 1240-1241), so no non-client firm can make the rule decide.

## 3. The identities (synthetic, internal tier, minted for this sitting only)

| name | users row | token | expected (OFFLINE, on the shipped `served.py`, the rule's real reader over a fake users table) |
|---|---|---|---|
| `disabled` | `PK USER#irpt-r21-status-disabled@opal.invalid`, `SK PROFILE`, `email` = that address, `firmId opal-capital`, `status disabled`, `userType test-filer`, `allowedFirmIds ["cottonwood"]` | RS256, `iss opal-portal-auth`, `aud opal-portal-api`, `tier internal`, `role user`, `firmId opal-capital`, `exp` at most 20 min after `iat` | REFUSED `FIRM_BINDING`; ONE line `INTERNAL-CALLER-CLASS class=row_non_active outcome=refused`; the dependencies of cottonwood are NOT reached |
| `norow` | none (token only; before the request the email-index query returns no item and a ConsistentRead of `USER#...@opal.invalid/PROFILE` reads absent) | same claims, address `irpt-r21-status-norow@opal.invalid` | REFUSED `FIRM_BINDING`; ONE line `class=row_absent outcome=refused`; dependencies NOT reached |
| `active` (optional arm, section 6) | `status active`, `allowedFirmIds ["cottonwood"]`, `email` = its address | same claims | ADMITTED; ONE line `class=row_present outcome=admitted`; the dependencies of cottonwood ARE reached |

`allowedFirmIds` names the selected firm in both rows, so a refusal can come only from the status test (`served.py` 1177-1178 raises before the list is read; the offline run confirms the list is never read). The row MUST carry `email`: the rule finds a user only through the email-index GSI and requires the row's `email` to equal the address (`canonical_profile_reads.py` 70-94); a row without it reads as absent (the offline control arm shows a disabled row without `email` reads `row_absent`). The R2-cw-1 row listing omitted `email`.

## 4. The act (executor: a Dell `0.7.0_AE_CloudOps` lane; this seat holds no key)

0. Open the NEVER-2 ledger entry first (`irpt-status-rule-exercise-<date>`); read every live worktree's `.open_deploys/` (`git worktree list --porcelain`, then `ls-tree` per tree) and print the per-tree denominator; an open entry naming `opal-users-v2` or `irpt-directory-search` is a STOP.
1. ConsistentRead the target keys: all three `USER#` keys read ABSENT, and the email-index query returns nothing for the three addresses. Any other state: STOP, nothing written.
2. Write the `disabled` row (and the `active` row if section 6 is signed) with `attribute_not_exists(PK)`; read each back with ConsistentRead. The `norow` identity writes nothing.
3. Mint ONE token per identity, current signing slot, `exp` = the run's length + 5 minutes and never more than 20 minutes after `iat`; held in the executor process only, never written to a file, a log or a trace. The signing-key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`, as in R2.
4. One GET per identity (the order: `norow`, `disabled`, then `active`), each with its own token, through the edge route. Record status and the refusal code only (status and a sha256 of the body; no body is kept).
5. Count the class lines: `filter-log-events` over `/aws/lambda/irpt-directory-search` from the first request to the last plus 5 minutes, pattern `"INTERNAL-CALLER-CLASS class="`, auto-paginated and counted client side (never `--no-paginate`); print the window, the distinct `logStreamName` count and the total. **Zero streams searched is VOID.** Expected total: one line per request, in request order. The line carries no identity, so a total other than the number of requests is NOT attributed to the identities: it is a surprise row, not a guess.
6. **Removal, same sitting:** after the LATER `exp` has passed, delete the written rows (`DeleteItem`, condition `attribute_exists(PK)`), then read ALL THREE addresses by the rule's own path: the email-index GSI query AND a ConsistentRead GetItem. ABSENT on both reads for all three. The GSI is eventually consistent: repeat a GSI read that is not yet ABSENT within a printed bounded window. The ledger closes only after this. A PRESENT read after the delete is a STOP.

## 5. Blast radius (what the act may touch, and the rollback per key)

| key | what may change | rollback |
|---|---|---|
| `opal-users-v2` items `USER#irpt-r21-status-disabled@opal.invalid` (and `-active@`) | created, then deleted after `exp` | delete + GSI and ConsistentRead ABSENT. `norow` is never written |
| the edge's token verification | the three tokens are presented once each; the signing key is READ (by the executor to sign, reported after the fact) | none: read only |
| `irpt-directory-search` and its log group | three requests, three class lines (two if the optional arm is dropped) | none: a refusal changes nothing; the admitted request is a read |
| cottonwood's directory artifact and ownership map | **read ONLY by the `active` arm**: one GetObject each through the function's dependencies (`loaders.py` 320-349; `served.py` 855). They are not holdings, but they are the client firm's directory and ownership data | none: read only, not reversible. This is the reason for section 6 |

The identities may do: one GET each of the route above with `selected_tenant=cottonwood`. They may not: any write through the route, any other firm, any second selection in one request, any IRPT holdings read, any other route, a second token or a refresh, a token past 20 minutes. No IAM, code, route or Terraform change. No client figure in any tracked file; no response body is kept.

## 6. What the CTO half decides (the one open choice)

**The admitted `active` arm reads cottonwood's directory and ownership artifacts** (`AR-y-223` row `IRPT_ANLREQ-D2-W69-S1`: the premise "opens no client data" does not hold for that arm). The R2-cw-1 half covers the cottonwood ticket board, not these reads. Two ways, this seat recommends the first:
- **(A) Sign the arm as read-only, with the bound above (status, body sha256, nothing kept).** The two refusal arms prove the rule REFUSES; only the admitted arm proves the rule still ADMITS a legitimate internal caller through the live edge, which is the other half of "the rule works". The reads are what every real internal user of the directory makes.
- **(B) Drop the `active` arm.** The sitting then proves the refusals only; the admitting path is covered by the 23 real internal rows (21 `active`) and the release-20 tests, not by a live read.

## 7. After-reads, both branches

- **Pass:** `norow` and `disabled` each refused `FIRM_BINDING` with the expected class line counted; (A) `active` admitted with its line; all three addresses ABSENT after removal; the ledger closed. Disarm `IRPT_ANLREQ-D2-W55-S1`'s limit on "the rule not yet exercised" and record the three counts with the window and streams denominator.
- **A refusal arm admits, or a class line is absent or of the wrong class:** STOP, remove the rows (step 6), close the ledger FAILED, file a BLOCKING row; the rule is then NOT doing what the release claimed and the CTO is told the same hour.
- **A write fails or a token is refused at the edge:** remove what was written, record the status and reason; no retry with a second token.

## 8. Limits named

- The identities are EXERCISED through the edge; the offline prediction is not (it bypasses token verification, `AR-y-223` `does_not_carry_over`).
- The class line cannot be attributed to an identity; the count rests on the request count and the window.
- The signing-key read: the executor's lane needs the grant the Dell identities are being given (`2.0.0_SA_COO~C` round 12); if the lane lacks it the act is a STOP and a surprise row, never a laptop order (Andrew-direct, relayed msg 6938).
- Not read by this seat: the live token path, the users table, the edge's header rewrite beyond `served.py` 1209-1210.

## 9. Owed before any order is cut

1. The CTO half on this file's blob, choosing (A) or (B) in section 6 and naming the executor lane.
2. The executor lane's grants (DynamoDB read and write on the three keys, the signing-key read, `logs:FilterLogEvents`), read as met by the lane at its step 0.
3. Nothing from Andrew (no client-facing page, no PROD change).
