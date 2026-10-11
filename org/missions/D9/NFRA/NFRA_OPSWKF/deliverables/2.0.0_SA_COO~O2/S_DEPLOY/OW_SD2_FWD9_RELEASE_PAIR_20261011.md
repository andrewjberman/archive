# NFRA_OPSWKF OW-sd-2 / OW-sr-2 -- the FWD-9 release: packet and COO half (never-widen), 2026-10-11

**Issuer:** `2.0.0_SA_COO~O2` (dell2). **Applier and executor of the live reads:** `0.7.0_AE_CloudOps~DELL2` (it applied this root
and read the signing key today under TO-APPLY-S1; no grant is added). **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.
**Cell served:** OW-s-3, merged @234c3b4b10 (worker commit c27307ec2e). **PRD:** v0.8 @cfc5091071, ratified-text half SIGNED
@1b8530a2fc. **Conditions carried:** `1.0.0_SA_CTO~DELL2` msgs 5704 and 5710.

## 1. The act (write set = a literal key list)

| # | Key | Change | Writers of this property (counted) |
|---|---|---|---|
| K1 | Lambda `trade-submission-handler`, code | `_require_internal(event)` FIRST in `lambda_handler`, after the CORS preflight and before the body is parsed: 403 `Forbidden: trade submission answers Opal staff only` unless the authorizer context carries tier exactly `internal` OR firmId exactly `opal-capital` | 1: `infra/aws/terraform/trade-pipeline` via the versioned artifact `s3://opal-313476888478-lambda-artifacts/trade-pipeline/trade-submission-handler.zip` (`lambdas.tf`, the `trade_submission_handler` resource) |
| K2 | `opal-users-v2`, TWO synthetic rows (section 4), written and later deleted | create, then delete after the tokens' exp | 1: the executor, by conditional put (`attribute_not_exists(PK)`) |

Build input, three members (`infra/aws/lambda/ci/lambda-source-map.json`), sha256 hex at the pin `234c3b4b10`:
- `submission_handler.py`  466334f98aa3707c75b177cab14ff4df9c832176dc33bb4d794adab36960ab8c
- `email_utils.py`         1c6f63a57215843ccbbdfc6552092b51e62373cae769303af8c0390554bc6d6b
- `config.py`              042efba5f0cf06ed15d0617ec1105f68d5f9131ef42498edb5143853ce59aa56

The handler BEFORE the fix (parent of the merge) hashes to
`fc59cd256c1797860277a200a39d47a493f06cef56e4c6ac6f10010c1bb146a4`, the value TO-APPLY-D1 deployed on 2026-10-09. No env key,
grant, route, table, layer, SES setting or other function changes. No portal file changes.

## 2. Blast radius

- **Refused after, served today:** every verified caller who fails both comparisons. Today such a caller with an email can store
  a PENDING_APPROVAL submission and cause a mail to the approvers group (OW-s-1's record, section 1). After the act it gets 403
  before the body is parsed.
- **Must still submit: Opal staff.** The 9 rows of `trade-users` all carry firmId `opal-capital` on their portal rows (measured
  18:3xZ, row D2-S6), so 9 of 9 pass. The stored rows were read; live tokens were not.
- **Callers of the route, one read through each:** the portal's `submitTrade` (`portal/src/api/endpoints/trade-submission.ts:239-241`),
  used by the Trade Submission page and by this project's Ticket Center trade form (`TradeRequestParts.tsx`, on DEV). The Ticket
  Center is internal-only today (decomposition, round 1, Rule 24 remainder). `opal_ai`: 0 files name the route. `mcportal` and
  callers outside these trees: NOT searched.
- **A tension this act makes concrete, for the CTO:** FWD-1's ACCEPT reads "an advisor files a trade request in the Ticket
  Center" and the bridge carries it to this route. After FWD-9, a filer whose portal row is not `opal-capital` and not tier
  `internal` is refused at the engine. No such caller exists today (the Ticket Center is internal-only), so nothing live breaks;
  the two outcomes disagree only when advisor reach is built.
- **The handler's two older refusals** (no email; a body `initiator_email` that differs) are unchanged for Opal-internal callers
  and are no longer reachable by anyone else: an outsider meets the new 403 first.
- **Proven at the pin by the issuer, on the merged tree:** `OW-S9-TESTS-OK passed=7`; `OW-S9-PROBE-OK refused=28 of 28 (7
  outsiders x 4 bodies) with the new message and nothing touched, insiders at the 400=2 of 2`; `OW-S9-REGRESS-OK passed=29
  across 4 test file(s)`; round 1's `OW-TRADE-REGRESS-OK` (both trade handler suites and the actor-identity script). The issuer
  read the handler diff whole: two constants, one helper, one call, 28 lines.

## 3. Expected plan (both branches)

- **Branch A, proceed:** `0 to add, 1 to change, 0 to destroy`: `aws_lambda_function.trade_submission_handler`
  (`s3_object_version` and `source_code_hash`; Terraform's computed `last_modified` moves with any code change and is not a
  departure).
- **Branch B, STOP and report:** anything else. Nothing is applied on branch B.

## 4. The two synthetic callers (K2), the ONE body, and the three reads

| caller | row `PK` (`SK PROFILE`) | token claims that matter | Opal-internal? |
|---|---|---|---|
| OUT | `USER#opswkf-fwd9-out-20261011@opal.invalid` | `sub` and `email` = that address, `tier advisor`, `role user`, `firmId fwd9-synthetic-nofirm`, `userType test-filer` | no (fails both comparisons); carries a verified email |
| IN | `USER#opswkf-fwd9-in-20261011@opal.invalid` | `sub` and `email` = that address, `tier advisor`, `role user`, `firmId opal-capital`, `userType test-filer` | yes, by firmId |

Rows: `status active`, a `name` beginning `NFRA_OPSWKF FWD-9 synthetic`, `allowedFirmIds ["fwd9-synthetic-nofirm"]` as a LIST.
Tokens: RS256 with the current signing key, `iss opal-portal-auth`, `aud opal-portal-api`, ONE absolute `exp` for both =
run start + the run's stated length + 5 minutes; the length is stated before minting and is as short as the acts allow. Token
values in memory only. No tier-internal token is minted (the CTO's ruling on FWD-8's IN-T stands here unasked).

**The ONE body, posted to `POST /api/general/trades/submit` through the CloudFront host:**
`{"fund": "PFDE", "ticket_id": "not-a-ticket-id"}` -- no `initiator_email`, no securities. On the bytes live today the handler
answers it at `submission_handler.py:198-202` (`400 ticket_id is malformed`) BEFORE `dynamodb.Table(...)`, `get_user`, the put
or the mail; after the release an outsider never reaches that line.

| # | when | caller | expect | on the other answer |
|---|---|---|---|---|
| P0 | BEFORE R0 | -- | the DEPLOYED `submission_handler.py` (package downloaded) hashes to `fc59cd25...b146a4` | any other hash -> STOP before any POST: the body's "stores nothing" rests on those bytes; cleanup; report |
| R0 | BEFORE the apply | OUT | `400`, message `ticket_id is malformed` | `403` -> STOP: the defect is not what the record says (a finding for the CTO); `200` -> STOP and report AT ONCE: a row was stored and a mail sent, name the submission id; apply nothing |
| R1 | AFTER | OUT | `403`, message EXACTLY `Forbidden: trade submission answers Opal staff only` | `400` -> the release did not take: re-read the bytes, then roll back K1; a 403 with any OTHER message -> not the new check: treat as not taken |
| R2 | AFTER | IN | `400`, message `ticket_id is malformed` | `403` -> roll back K1 (Opal staff would be locked out); `200` -> STOP and report at once, as R0 |

Each read records the status code and the `message` field only. **No row and no mail, shown, not assumed:** after R2, a query
of `opal-trade-submissions` index `by-initiator` for each of the two synthetic addresses, expect Count 0 for both, with one
control beside them (the same query for an initiator known to have submissions returns a non-zero Count; the count only).

## 5. What each synthetic caller is on every OTHER surface, for its token's life

Read from each surface's own rule. **The executor makes NO call on any surface in this table.** The token never leaves the
executor's memory, so this table is what the token COULD do if it did, not what the run does.

How the authorizer fills the context for both (`infra/aws/users/lambda/portal-authorizer/index.mjs:293-322`, read): neither is
`Dev` nor tier `internal`, role is `user`, so `allowedFirmIds` = the caller's own firmId and nothing else: `fwd9-synthetic-nofirm`
for OUT, `opal-capital` for IN.

| surface | its rule (read by the issuer unless marked) | OUT | IN |
|---|---|---|---|
| `trade-dashboard-api`, 8 routes (FWD-8, live since 19:30Z) | tier `internal` OR firmId `opal-capital` | refused | **served: the blotter and the trade-users list** |
| `trade-dashboard-api` `users/me` | own row by email | its own (empty) record | its own (empty) record |
| `trade-submission-handler` (this act) | before: an email; after: Opal-internal | before: can store a submission and mail approvers; after: refused | **can store a submission and mail the approvers, before and after** |
| `trade-workflow-handler` | a trade-users row and a group (OW-s-1's record; not re-read) | refused: no trade-users row | refused: no trade-users row |
| `opal-data-refresh-api`, every route incl. `upload-urls`, `trigger`, `rollback`, `time-machine` and the security-scanner routes | `validate_user_type`: `Dev` OR `is_opal_internal` (`data_refresh/lambda_function.py:142-216`; 12 call sites of `validate_user_type` counted in the file) | refused | **ADMITTED AS OPAL-INTERNAL, write routes included. `userType test-filer` does not narrow it (row D2-S7).** |
| `opal-portal-content-api` | GET: no check; PUT and DELETE: firmId == `opal-capital` (OW-s-1's record) | reads all overrides | **reads all overrides AND may write or delete one** |
| `opal-portal-data-proxy` | no check (OW-s-1's record) | reads every dataset it serves | the same |
| `opal-research-pull-enqueue` | no check (OW-s-1's record) | can queue a research pull | the same |
| `opal-ticket-api` | `principal_class` (`ticket_center/lambda_function.py:312-330`): `userType service` -> a named service or nobody; else firmId `opal-capital` -> INTERNAL; any other non-null firm -> CLIENT. `_in_profile_scope` (`:404-406`) narrows to the row list | CLIENT of a firm that does not exist | **INTERNAL human: create, claim, list and work tickets, narrowed to the row list (one non-existent firm)** |
| `opal-partners-data` (27 routes) and the billing read | `is_authorized`: `allowedFirmIds == ALL` or the requested firm is in it (`opal-partners-data/lambda_function.py:296-310`; `advi/billing-read/entry.py:104-110`) | only firm `fwd9-synthetic-nofirm`: no real firm | only firm `opal-capital`: whatever those routes hold under that firm id (NOT read: what that is) |
| the investor-reporting functions (24 routes) | the verified `X-Firm-Id` header, then a grant resolved per principal (`_authz/served.py:19-40` read; `enforce.py` NOT read to the end) | a firm with no bucket mapping: refused by the header's own account, not confirmed by this seat | firm `opal-capital`: **NOT ESTABLISHED** what an opal-capital principal with this row is granted |
| `opal-amgt-scoped-api` (19 routes) | **NOT READ** | not established | not established |
| `trade-identifier-cache` (2 routes) | source not in the repository | not established | not established |
| routes made in the console, incl. the data proxy's `$default` | not in the repository | not established | not established |

**What this table says plainly:** OUT is an ordinary signed-in outsider with no firm: it can do what any portal login can do on
the four caller-blind surfaces and nothing firm-scoped. IN is an Opal staff member in everything but a trade-users row: for its
token's minutes it could trigger or roll back a data refresh, write portal content, work tickets and submit a trade. That is
the cost of proving the admitted arm on the deployed service with a synthetic identity, and it is bounded only by (a) the token
living in one process's memory, (b) its exp, (c) the executor making exactly two calls with it (R2 and nothing else). Three
rows are not established, and for IN they could be wider than stated.

**The alternative that mints no Opal-internal identity:** R2 is read by-session instead: an Opal staff member posts nothing
new, the page's ordinary submit simply keeps working, and the admitted arm on the deployed service is recorded UNEXERCISED
until a real submission lands (the organic arm). The issuer signs either; the choice is the CTO half's.

## 6. After-reads (the executor, each printed with its time)

- **(a)** `CodeSha256` equals the uploaded zip's; the DEPLOYED package diffed against the build input MEMBER BY MEMBER, both
  directions, member count printed (expected 3).
- **(b)** Env key NAMES and layers unchanged from BEFORE.
- **(c)** R1 and R2 as section 4; the two `by-initiator` Count reads and their control.
- **(d)** The replan is 0-diff.

## 7. Rollback (per key)

- **K1:** re-point the function to the PRIOR `s3_object_version`, read and recorded BEFORE the apply; one `safe-apply`. The prior
  version serves every caller as today.
- **K2:** each row stays until the shared `exp` has passed; then it is deleted and read back ABSENT with ConsistentRead, with a
  control. The ledger closes after the two ABSENT reads.
- **A stored submission** (R0 or R2 answering 200): it is NOT deleted by the executor. It is reported at once with its id; its
  disposal is the CTO's word.

## 8. COO half

`2.0.0_SA_COO~O2` signs the blast radius above for keys K1 and K2, both plan branches, every answer of P0, R0, R1 and R2 as
tabled, the rollback per key, and section 5 as read, with its three NOT ESTABLISHED rows stated as such.

**COO half -- SIGNED** at pin `234c3b4b10`. The apply order is cut when the CTO half is given, and not before.

-- 2.0.0_SA_COO~O2, 2026-10-11
