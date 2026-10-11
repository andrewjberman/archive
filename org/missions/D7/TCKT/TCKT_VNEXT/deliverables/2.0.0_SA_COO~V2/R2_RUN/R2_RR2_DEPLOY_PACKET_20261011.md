# Packet -- R2-rr-2 deploy: the ticket report route refuses a request id the report reader cannot open (TCKT_VNEXT round 2)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~03:5xZ. **Applier:** a
`0.7.0_AE_CloudOps` lane seat on dell2, seated by this seat once both halves are signed.

**Authority:**
- CTO round-2 analysis @bbba700c22 section 4 item 2 ("its own never-widen pair ... lands before item 3's run");
- decomposition `decompositions/TCKT_VNEXT_DECOMP_R2.md`, cells `R2-rr-1` (built) and `R2-rr-2` (this apply);
- the drain: `R2-rr-1` merged @a366ce52ec, `R2-ts-1` merged @b4a65a4bbd. On the merged tree the issuer re-ran, with the default test
  guard live: `RR-SHAPE-OK passed=4 of 4`, `TS-GUARD-OK passed=3 of 3`, `TC-REGRESS-OK passed=154 (min 147) failed=0`;
  `commit-gate.sh` clean for 4 of 4 files.

**COO half: SIGNED below.** Code only: no env, no route, no IAM, no grant.

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `a366ce52ec`; file sha256 (hex) `ca3be34307f70079e48c4a26d1f711e47318285f2cf2722fdf0cfdcbd637eade` (`sha256sum` of the tree file by this seat) |
| the diff from the build it replaces | 4 inserted lines, 0 removed (`git diff --stat 5a36586b5f a366ce52ec -- <file>`): one module-level pattern `REPORT_REQUEST_ID = re.compile(r"REQ-[0-9a-f]{24}")` and one 3-line refusal in `report_ticket` using `fullmatch` |
| live now | `opal-ticket-api` CodeSha256 `HK82TEd0SQWe...`, LastModified 2026-10-09T11:43:28Z (`get-function-configuration`, this seat, 2026-10-11 ~03:5xZ). The deployed FILE is EXPECTED to be the pre-merge tree file, sha256 `670686262068808f...57a8` (`git show 5a36586b5f:<file>`), per the SA1 order's close note; **not measured by this seat** -- the applier's first read (section 3, step 1) |
| plan expected | `0 to add, 1 to change, 0 to destroy` (the function's source_code_hash only) |
| test files | `tests/conftest.py`, `tests/test_no_real_aws.py`, `tests/test_report_ref_shape.py` are in the tree, not in the function package's behaviour. If the build zips the `tests/` folder, the applier says so; it changes no handler path |

## 2. Blast radius, by branch

**Behaviour that moves (read from the code at `a366ce52ec`):** ONE route, `POST /api/scoped/tickets/{ticketId}/report`.
- A `request_id` that passes every existing check and does NOT fully match `REQ-[0-9a-f]{24}` now gets HTTP 400 with
  `code: INVALID_REPORT_REQUEST_ID`, before any table write. It used to be stored.
- A well-formed id is stored exactly as before. Every earlier check keeps its place and message. No other route changes.

**Who calls the route (N = 1 writer found, printed):** the portal Ticket Center page,
`portal/src/pages/TicketCenter/analysisRequest.ts:161-170`. It submits the analysis and records `issued.requestId`, the id the
analysis service ISSUES, not the `tckt-<ticket>` idempotency token it sends (`:131`). The round-1 seat runner was the second caller
and is retired.
- **The one way this apply can hurt a user:** if the analysis service ever issues an id that is not `REQ-<24 lower-case hex>`, the
  portal's record step gets a 400. The report would exist and the ticket would not point at it. Read, not exercised: the read plane
  accepts only that shape (`ops/owned_requests.py:18`), and ids of that shape appear across the IRPT code and tests, so an id of
  another shape could not be opened anyway. The first live exercise is `R2-tr-1`.
- **Existing tickets are not rewritten.** Two test tickets carry a malformed `report_ref` (`TCK-20261009-a1052909`,
  `TCK-20261009-67ab7f27`); they keep it. A census of every ticket's `report_ref` shape was NOT run.

| branch | what the apply writes | rollback |
|---|---|---|
| apply succeeds | the function code | re-apply the build of `5a36586b5f` (file `67068626...`), same method |
| apply fails partway | nothing else to land (code only) | as above; the ledger stays open until one holds |
| step 1 finds the live file is NOT `67068626...` | nothing: STOP before any plan | none; the difference is reported to the CTO, because the rollback target would be unknown |

## 3. The act and its after-reads

0. Open the NEVER-2 ledger entry FIRST. Read every live worktree's `.open_deploys/` (`git worktree list --porcelain`, then `ls-tree`
   per tree), union them and print the per-tree denominator; an open entry naming `opal-ticket-api` is a STOP.
1. Before the apply: download the live package and show the deployed `lambda_function.py` sha256 is `67068626...`. Otherwise STOP.
2. Apply through `safe-apply` (Terraform only; never `aws lambda update-function-code`), plan read first: exactly 1 to change.
3. After: CodeSha256 equals the uploaded zip, and the deployed `lambda_function.py` sha256 equals `ca3be343...`.
4. An unauthenticated POST to the report route returns 401 (the authorizer still fronts it).
5. `opal-tickets` ItemCount is unchanged, and `TCK-20261009-a1052909` reads the same status fields as before (positive control).
6. The replan is 0-diff.

**Both live arms of the new check (a well-formed id stored, a malformed one refused) need an in_progress ticket held by an internal
assignee, so they are exercised by `R2-tr-1` under its own pair, not here.** This pair writes no ticket and mints no identity.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11: SIGNED for the blast radius above and all three branches.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
