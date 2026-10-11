# DSGN_IRPTV1 FWD-1 -- one signed-in trace on portal DEV under a READ-ONLY synthetic identity: DRAFT never-widen pair

**Status: DRAFT. BOTH HALVES UNSIGNED. Nothing in this file authorises a run.** Author: `0.9.0_WK_DSGN_IRPTV1~47` for
`2.0.0_SA_COO~D2`, task order `DSGN_IRPTV1.TO-IV-e-87` (round 12, cell IV-e-87). Ordered by `1.0.0_SA_CTO~DELL2`'s ruling msg 4198:
no closer; one trace cell, signed in, portal DEV, the one named client end to end, each hop recorded with what it returned, under
a never-widen pair for a read-only synthetic identity on dell2.

**What the CTO ruled (the bounds this draft is cut to):** internal tier; the row LIST holds the one firm; a token of the run's
length and at most 30 minutes; every request a GET but the sign-in itself; the identity removed after `exp`; the trace records
hop, status and counts, and no figure, account id or screenshot enters the repository.

**Source of every request below:** `FWD1_TRACE_HOPS.json` in this folder (portal read at DEV tip
`1cd1cf252e`, by content; backend read in the workspace tree at `d1ed899ba9`). This cell read the repository only: no token, no
row, no AWS call, no request to a deployed service.

**Client-data rule.** The PRD's FWD-1 names a client and an account. Neither appears here: "the named client", "the named account".
The firm token is `cottonwood`, as the registry spells it (the generated firm table in the portal, and `tenants.py` lines 80-88 of
the performance package).

**Precedent reused by reference, not copied:** the TCKT_VNEXT R2-tr-1 pair (`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R2_RUN/R2_TR1_THREAD_RERUN_PAIR.md`),
its CTO half (`.../1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R2_TR1_THREAD_RERUN_CTO_HALF.md`) and its runner
(`.../0.9.0_WK_TCKT_VNEXT~8/fwd1_runner/fwd1_run.py`). **Where this trace differs from the precedent:** no upload, no ticket, no mail,
no vendor generation, no old test ticket to close; the identity is read-only and its firm is `cottonwood`, not `49financial`; the token
is capped at 30 minutes, not 60; the census is GET-only; the browser step may not be possible at all (see The act, step 6).

## Findings the halves must rule on (read these first)

The read of the code shows that "every request a GET but the sign-in" does not describe the Investor Reporting page, and that "GET"
does not always mean "reads". Each is listed in `FWD1_TRACE_HOPS.json`, none is shaped away.

| # | finding | where | what it means |
|---|---|---|---|
| F1 | `POST /api/scoped/investor-reporting/selections` WRITES one DynamoDB item per distinct selection (immutable, content-addressed, idempotent) | handler `directory/entry.py` 307-315 -> `_scope/selection.py` 60-74 -> `_scope/selection_store.py` 45 | The page cannot reach any account-level hop without it (the client pick is posted at `index.tsx` 247; the focused account at `accountFocus.ts` 68). A non-GET that is not the sign-in, and a server-side write. |
| F2 | `POST /api/scoped/investor-reporting/directory/resolve` only READS | handler `directory/entry.py` 261-304 | A non-GET that is not the sign-in. The page cannot open without it (`index.tsx` 111). |
| F3 | `GET /api/scoped/investor-reporting/performance/{accountSetId}` is a read-through store: a miss computes and PERSISTS (evidence object, retention promotion, report, pointer) | `performance/retained.py` 321, 324, 330, 338 | A GET that writes. For the named firm the fresh path is the VENDOR branch (`retained.py` 304-315; holdings sources are installed for two other firms only, `installed.py` 68): it refuses unless a server-approved single-use plan matches, and when one matches it writes a claim row (`authorization.py` 94) and makes a vendor call. See Blast radius and Branches. |
| F4 | A browser session sends `POST {analytics_api}/ingest` on a 10 second timer and on unload | `portal/src/services/analytics.ts` 777 | A non-GET, not the sign-in, handler not found in the tree (NOT_ESTABLISHED). |
| F5 | The page's session is made by `POST {auth_api}/auth/refresh` with a refresh COOKIE; a token placed in browser storage does not authenticate the page | `AuthContext.tsx` 174, 246-257; `api-client.ts` 46, 61-80 | The synthetic identity has no password and no cookie. The "page step" may be impossible under the ruled bounds. |
| F6 | After auth a browser session prefetches five `GET /api/scoped/advisor-intelligence/platinum/firm/...` files with the `49financial` override for any internal-tier claim | `AuthContext.tsx` 36, 42, 46-68 | Another product's routes, a firm other than the identity's one-firm LIST. Whether the row LIST clamps them is NOT_ESTABLISHED here. |

## Measured at signing

Filled from the repository where a repo read can fill it. Every live value is `OWED AT SIGNING` with its instrument; nothing here is a guess.

| item | value | instrument |
|---|---|---|
| Portal DEV tip | the order names `1cd1cf252e` (read by content). Whether it is the tip on origin at signing: OWED AT SIGNING | `git -C portal ls-remote origin DEV` |
| Portal DEV CI for that commit | OWED AT SIGNING (not read; no CI state is asserted) | `gh run list` on the portal repo |
| Whether the DEV site serves that build | OWED AT SIGNING | fetch the DEV site's served asset manifest and compare its build id to the commit |
| API host the DEV site calls | OWED AT SIGNING. The precedent runner's constant (`fwd1_run.py` line 71) is not confirmed to be the DEV site's | read the DEV build's API base setting |
| Lambda `irpt-directory-search` (resolve, browse, selections) | CodeSha256 OWED AT SIGNING; env `IRPT_REQUESTS_TABLE` = the core stack's `tables.requests` output (`directory/lambda.tf` 46); the table's live name OWED AT SIGNING | `get-function-configuration` |
| Lambda `irpt-holdings` | CodeSha256 OWED AT SIGNING | `get-function-configuration` |
| Lambda `irpt-performance-adapter` | CodeSha256 OWED AT SIGNING; whether env `IRPT_PERFORMANCE_APPROVED_PLAN` is set (`performance/lambda.tf` 51-54) OWED AT SIGNING | `get-function-configuration` |
| Lambda `irpt-49f-reporting-read-lambda` (the name the precedent runner lists, `fwd1_run.py` 88-91) | CodeSha256 OWED AT SIGNING; the name itself OWED AT SIGNING (the reporting-read stack derives its name from the naming registry, `reporting/entry.py` 135) | `get-function-configuration` |
| Code each Lambda runs equals the tree read here | OWED AT SIGNING, per Lambda | diff the deployed package against the build input, not by filename (CLAUDE.md 22a) |
| Whether platinum reporting files are published for the named account's firm | OWED AT SIGNING. If not, the PATH B reads answer NOT_READY and the trace records that | list the firm's `account=` prefix through the served graph, then one `get-object` head |
| Whether an accepted performance pointer exists for the named account's window | OWED AT SIGNING. Not readable from the tree | the requests table, pointer key shape at `retained.py` 237 |
| The synthetic row | ABSENT: OWED AT SIGNING | `get-item` on the users table with ConsistentRead (table name `opal-users-v2`, `fwd1_run.py` 74) |
| The firm's registry bucket map (the denominator of the census) | OWED AT SIGNING | the `IRPT_DIRECTORY_BUCKET_MAP` env of `irpt-directory-search` |
| Whether the edge authorizer admits `userType` `test-reader` | OWED AT SIGNING. The boundary treats any value other than `service` as the internal branch (`served.py` 1217-1229); the authorizer is not in the tree read | the precheck GET in The act, step 2 |
| Whether `0.7.0_AE_CloudOps~DELL2` (proposed executor) holds the read of the signing secret | OWED AT SIGNING | `comp-iam` for the seat's principal |

## The identity

- **Row**: users table `opal-users-v2`, `PK USER#irpt-fwd1-trace-reader@opal.invalid`, `SK PROFILE`. Fields: `email` the same
  address, `firmId opal-capital`, `status active`, `userType "test-reader"`, `name` "IRPT_DSGN FWD-1 synthetic trace reader",
  `allowedFirmIds` the LIST `["cottonwood"]` (exactly one member; never the string `ALL`, which an internal caller is refused,
  `served.py` 1144-1165). Written with `attribute_not_exists(PK)` and read back PRESENT with ConsistentRead. Field shapes follow the
  precedent runner's `put_row` (`fwd1_run.py` 234-243).
- **Token**: ONE RS256 token. Claims: `sub` the row address, `iss opal-portal-auth`, `aud opal-portal-api`, `firmId opal-capital`,
  `tier internal`, `role user`, `userType "test-reader"`, `name`, `iat`, `exp` (precedent `mint_token`, `fwd1_run.py` 262-277).
- **`exp` rule**: `exp = iat + N minutes`, where N is the run's SIZED length + 5 and never more than 30. `iat` is fixed BEFORE the
  row is written, so the cleanup knows `exp` whatever happens. The executor prints the sized length, N and `exp` before minting. A sized
  length over 25 is a STOP: the run is cut, not the cap raised. (The precedent runner caps at 60, `fwd1_run.py` 179; for this pair the
  cap is 30, so the runner needs that constant changed. See What must hold.)
- **Memory-only.** The token is never printed, stored or committed.
- **Who mints**: the EXECUTOR seat, with its own read of the signing secret (`opal/auth/jwt-private-key`, `fwd1_run.py` 75). No seat
  principal gains a key grant; the key read is reported after the fact through `0.0.0_AB_MSTR~DELL2`, as in the precedent.
- **Tier and reach**: tier internal means the authorizer derives all-firm reach; the row LIST is then the ONLY client reach. The
  clamp: an internal caller whose selected firm is not in the row LIST is refused FIRM_BINDING (`_authz/served.py` 1207-1229, reading
  `_internal_allowed_firms` at 1138-1166). On Global, each registry firm is resolved through the same boundary
  (`directory/entry.py` 430-435), so every firm outside the LIST comes back UNAVAILABLE (446-451).
- **Removed after `exp`**: cleanup deletes the row only after `exp` has passed (an earlier delete would WIDEN the token: the row
  LIST stops narrowing it) and reads it back ABSENT with ConsistentRead.

## The act

Executor: a CloudOps seat on dell2; **proposed `0.7.0_AE_CloudOps~DELL2`**, the halves name it. This drafting seat holds no key.
Runner: **none exists at a pin for this pair.** The TCKT runner is the model (see What must hold).

0. **Open the NEVER-2 ledger entry first.** Read every live worktree's `.open_deploys/` (`git worktree list --porcelain`, then
   `git -C <wt> ls-tree -r --name-only HEAD org/critical_paths/.open_deploys/`), union them, print the per-tree denominator. An open
   entry naming `irpt-directory-search`, `irpt-holdings`, `irpt-performance-adapter` or the reporting-read function, other than this
   run's, is a STOP.
1. **Prechecks, before any write.**
   - Each of the four Lambdas' live CodeSha256 starts with the prefix the halves signed (Measured at signing). Anything else is a STOP.
   - `IRPT_PERFORMANCE_APPROVED_PLAN` on `irpt-performance-adapter`: if it is SET and names the firm `cottonwood`, the performance
     hops H6 `GET /performance` requests are NOT ISSUED (STOP for those requests, run continues; recorded `PATH-A-SKIPPED-PLAN-SET`),
     because a matching GET would spend a single-use vendor authorization (F3). If it is unset or names no such firm, the GET
     refuses at `authorization.py` 90 before any write; it is issued.
   - The synthetic row is ABSENT.
2. **Write the row, read it back, mint the token** (iat fixed first). Then ONE authenticated GET to the lightest scoped read
   (`GET /directory/browse` with `selected_tenant` = `cottonwood`, limit 1) as the admit check: a 401 or 403 here (the authorizer
   refusing `test-reader`) is a STOP, cleanup, and the halves decide whether to reuse the precedent's `userType`.
3. **The live census, GET-only, BEFORE any hop,** with the ALL-origin token. Denominator printed: the registry firms in the bucket
   map. For each firm other than `cottonwood`: one `GET /directory/browse?selected_tenant=<firm>` (expected FIRM_BINDING, per
   `served.py` 1224-1229), and for each of the other three hosts (holdings, performance, reporting) one `GET` with
   `selected_tenant=<firm>` for ONE other firm (expected FIRM_BINDING; the clamp is the shared boundary every host bundles, runner
   table `READS_SELECTOR`, `fwd1_run.py` 111-121). `cottonwood` itself: expected 200 on browse. Any 2xx for an off-list firm, or any
   answer that is neither 200 nor FIRM_BINDING, is a STOP (cleanup per step 7). **No POST is sent in the census.** The two POST routes
   run on the same host and the same boundary as the browse GET, which is the reason a GET arm covers them.
4. **The hops, in order, by the API runner** (each records hop, status, counts, code; nothing else):
   - H2: `POST /directory/resolve` (selected_tenant global). Expect 1 firm READY, the rest UNAVAILABLE. Record the three counts.
   - H3: `GET /directory/browse` at the empty query, then at the named client's query. Record the entry count and whether the named
     client is present (yes/no).
   - H4: `POST /selections` for the picked client. Record the account count the selection names.
   - H5: `GET /holdings/{accountSetId}`. Record the state word, the account-node count, and presence flags for name, total, as-of.
   - H6: `POST /selections` for the focused account (the client's largest account, as the page preselects, `ReportingTab.tsx` 525-533),
     then `GET /reporting/{account_id}/manifest`; if served, `GET /reporting/{account_id}/series`; if the client lists more than one
     account, `GET /reporting/client/{client_id}/summary`. Only if PATH B is not served for the focused account, and only if step 1
     allowed it, `GET /performance/{accountSetId}`. Record the statuses, the codes, the series point count, and presence flags for
     a year-to-date value and a spread value.
   - H7: no new request: the Holdings tab reads H5's snapshot (`HoldingsTab.tsx` 217-221). Record from H5's answer the count of slices
     (Models, SMAs, Client) and of security rows.
   - The runner issues exactly the requests above. A POST or a write route not listed in `FWD1_TRACE_HOPS.json` is Branch D.
5. **H1, the sign-in hop.** On the API-runner path there is no HTTP sign-in: the token is minted offline (step 2). H1 is recorded
   `SIGN-IN-BY-MINTED-TOKEN`. The browser's `POST /auth/refresh` belongs to step 6 only.
6. **The page step, only if the halves rule it in (Open question 4).** Default: NOT RUN, recorded `PAGE-NOT-RENDERED` with the
   reason F5. If a method is agreed that opens a browser session for the identity with no new credential and no login-route change,
   the step opens the page on DEV, repeats the picks, and records ONLY: the page canvas colour, whether the card, the YTD line, the
   split and the security list are present (yes/no), the section counts. No screenshot enters the repository. The browser also sends
   F4 and F6 requests; the halves rule on them in the same breath.
7. **Cleanup, in this order.** WAIT until the token's `exp` has passed; then delete the row and read it back ABSENT with
   ConsistentRead. The proof prints `exp`, the later delete time and the absent read. There is no ticket to complete. The ledger
   entry closes only after this, on every branch.
8. **The zero-write read, with its positive controls** (over `iat` to `exp`):
   - **Data-refresh zero calls**, as the precedent's step 9 (`fwd1_run.py` 1084): count the identity's address in the data-refresh
     Lambda's log group, printing the streams searched; 0 streams searched is VOID. The positive control is the same filter over a log
     group that DOES log the identity's address on a route this run called. **Which log group logs the address is OWED AT SIGNING:**
     the precedent's control (`opal-ticket-api`) is not on this journey. No control found means the read is VOID, not clean.
   - **No fresh performance persist**: in the `irpt-performance-adapter` log group, count `irpt_performance_timing` lines
     (`performance/entry.py` 221) over `iat` to `exp` that carry a `persist_ms` or `pointer_publish_ms` lap. Expected 0. The control:
     the same window must hold at least one `irpt_performance_timing` line if H6 issued the performance GET (else the read is VOID).
   - **Selections written**: the runner's own count of `POST /selections` answered 200. Each is an idempotent put (F1); the count is
     recorded, not subtracted from.
9. **The trace** goes to the executor's folder; the drafting seat's successor copies identical bytes into the project folder.
   Statuses, codes, counts and presence flags only: no name, no figure, no account id, no screenshot.

## Blast radius

What the act may touch, per key, and the rollback. "Expected writes for a read-only identity" are the row itself and whatever a
read route logs or caches; this table names each such write from the handler's code.

| key | what may change | rollback |
|---|---|---|
| users table row `USER#irpt-fwd1-trace-reader@opal.invalid` | created; deleted after `exp` | delete after `exp` + ConsistentRead ABSENT; never before `exp` |
| requests table, partition `cottonwood`, sort keys `SELECTION#sel_<64 hex>` | API runner: at most 2 puts (the client set, the focused account). Browser step: up to 2 plus 2 per additional listed account (the chooser, `ReportingTab.tsx` 685-713; the Holdings prefetch, `HoldingsTab.tsx` 271, 283-287). Each is content-addressed and immutable, and a repeat is a no-op (`selection_store.py` 44-53) | none: a selection record grants nothing (`selection.py` 1-4) and is the same bytes any user's pick creates. Never deleted. The trace lists the count |
| performance retained store (S3 evidence object and report; the pointer item `PERFORMANCE_ACCEPTED#...` in the requests table) | **expected none** for the named firm: its fresh path is the vendor branch, which refuses without a matching approved plan (`authorization.py` 90). If a pointer and a retained report already exist, the GET reopens it (a read) | none possible once written; hence step 1's plan check and step 8's persist read |
| performance one-use claim row `PERFORMANCE_USE#...` (requests table) and ONE vendor call | **only if** an approved plan matching the exact account and window is installed (`authorization.py` 94). Outside this pair: the pair excludes any vendor call | step 1 makes this a pre-write STOP for the performance GET |
| holdings, reporting, browse: S3 gets, in-container directory cache (`_authz/loaders.py` 162-170) | no durable change | none |
| CloudWatch log lines in each Lambda's group, including the performance timing line | one or a few lines per request | none; logs are the zero-write read's instrument |
| analytics ingest store (browser step only; F4) | NOT_ESTABLISHED. Session events keyed to the identity's address | owner unknown; a row if the halves rule the step in |
| auth refresh record (browser step only; F5) | NOT_ESTABLISHED | the same |
| every other firm | nothing: the census proves one firm before any hop | STOP + cleanup |

No IAM, code, route or Terraform change. No key grant for any seat principal. No mail, no ticket, no upload, no generation.

## Branches

- **A.** Every hop of step 4 met (HTTP 200 with an answer-bearing body at H5, and presence flags yes at H5/H6/H7): the trace is
  FWD-1's one live trace for the API-runner hops; whether it grades FWD-1 rests on Open question 7 (the page step).
- **B. A hop refused.** Record hop, status and the refusal code, run on to cleanup, never retry around it. The code names the cell:
  - `FIRM_BINDING` at any hop but a census arm: the row LIST or the client's firm is wrong. STOP, cleanup. Nothing to FWD-1.
  - `OBJECT_NOT_COVERED` at H6/H7 or `NOT_READY` at the PATH B reads: the account is not covered or its platinum files are not
    published for the named firm. FWD-1 stays not realised; the next cell is publication for that firm.
  - `SELECTION_UNSUPPORTED` or `UNAVAILABLE`: recorded with the hop; the code names the next cell.
  - A vendor-path refusal from `GET /performance` (the plan is not installed; `authorization.py` 90): expected, and NOT a failure of
    the pair; it means the YTD and spread must come from PATH B, and if PATH B is not published the hop reads NOT_READY.
- **C. STOP before any hop** (steps 0-3: an open ledger entry, a code identity mismatch, an admit refusal, a census arm that is not
  200/FIRM_BINDING): nothing of the journey runs; cleanup if the row was written.
- **D. A non-GET request met that `FWD1_TRACE_HOPS.json` does not list,** or any write route, or a vendor-egress sign: stop issuing,
  cleanup, a BLOCKING row. (The listed non-GETs are the two POSTs of the API runner and, on the browser path only, the refresh and
  analytics POSTs.)
- **E. A fresh performance persist or a vendor claim observed in step 8:** a BLOCKING row; the cleanup still runs. The write cannot
  be undone, so the row names it.
- **F. The page step cannot open a session** (F5): recorded `PAGE-NOT-RENDERED`; the hops of step 4 stand. It is a row, not a
  failure of the run.

## What must hold before a run order cites this pair

1. **A runner at a pin.** There is none for this pair. The precedent runner (`fwd1_run.py`) is the model; reusable by reference:
   `put_row` 234, `read_row` 246, `mint_token` 262 (with `exp` by argument), `call` 280, `wait_past_exp` 962, `cleanup` 974,
   `data_refresh_zero_calls` 1084, the precheck 1133. To change, in a new cell: `EXP_MAX_MINUTES` 60 -> 30 (line 179);
   `FILER`, `FIRM`, `userType` and the row fields; the census made GET-only and cut to four hosts; the hops replaced by H2-H7; the
   ticket, upload and report code removed; the `irpt_performance_timing` persist read added; the POST allow-list made exactly the two
   routes of step 4. The new runner's tests must show: a POST outside the allow-list is refused before it is sent, `exp` over 30 is
   refused, and the row is deleted only after `exp`.
2. **The executor seat is named** (proposed `0.7.0_AE_CloudOps~DELL2`) and holds the read of the signing secret for the run; the
   key-read report goes through `0.0.0_AB_MSTR~DELL2`.
3. **Every OWED AT SIGNING item is filled** by the signer, at the signing time, with its instrument's output.
4. **The halves have ruled the open questions below,** in writing, in their halves.
5. Portal DEV CI for the commit reads green, or the order says the page step is skipped and why.
6. The CTO half matches this text.

**Open questions for the halves**

1. **F1: is `POST /selections` inside "read-only"?** It writes one immutable, content-addressed record per selection and the page
   cannot reach any account hop without it. If the answer is no, the trace cannot walk FWD-1's sentence and the pair must say what it
   replaces FWD-1 with.
2. **F2: is `POST /directory/resolve`, a POST that only reads, inside the pair?** The bound excepts the sign-in only.
3. **F3: the performance GET.** Rule on the pre-write plan check (step 1) and on whether a GET that may persist is inside the pair. If
   not, H6 reads PATH B only, and FWD-1's "year-to-date return with its spread" is exercised only if PATH B is published for the firm.
4. **F5: the page step.** The page authenticates by refresh cookie. Is there an agreed way to open a browser session for the identity
   with no new credential? If not, the pair covers the API-runner hops only (Branch F) and the PRD's "ending in the rendered page"
   (FWD-1, DONE WHEN) is not met by this trace; the CVO decides what that grades.
5. **F4 and F6: the browser's extra requests** (analytics POSTs; five advisor-intelligence GETs under the 49financial override). Inside
   the pair, or the browser step is out.
6. **`userType`.** `test-reader` is proposed so the identity carries none of the filing privileges of `test-filer`. Does the edge
   authorizer admit it? If not, reuse the precedent's value, or name another.
7. **What the trace grades.** An API-runner trace with every hop answered is a real login-free walk of the page's own requests; is it
   FWD-1's "one live trace, real login, real backend"? The word "real login" is not met by a minted token. The CVO rules.
8. **N, the token length.** Sized default: census 5 minutes, hops 5 minutes, margin 10, N = 25 with the +5. Cap 30. Confirm.
9. **Which log group is the positive control** for the data-refresh read (step 8).

## COO half

**UNSIGNED.** `2.0.0_SA_COO~D2` signs here, on this text and on the conditions of the section "What must hold before a run order
cites this pair", after the open questions are ruled.

## CTO half

**UNSIGNED.** `1.0.0_SA_CTO~DELL2` signs here. The precedent's CTO half read the code the journey runs and set conditions on what it
found; the same is owed on findings F1 to F6.
