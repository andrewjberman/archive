# NFRA_OPSWKF OW-s-d-1 -- the FWD-8 release: packet and COO half (never-widen), 2026-10-11

**Issuer:** `2.0.0_SA_COO~O2` (dell2). **Applier and executor of the live reads:** a CloudOps lane seated for this act (named in
section 8 at the cut of its apply order). **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.
**Cell served:** OW-s-2 (pin in section 8). **PRD:** v0.6 @ca5f93a729, ratified-text half SIGNED @d4d5a850cf.
**Row:** NFRA_OPSWKF-D2-S6 (why "internal" is tier `internal` OR firmId `opal-capital`).

## 1. The act (write set = a literal key list)

| # | Key | Change | Writers of this property (counted) |
|---|---|---|---|
| K1 | Lambda `trade-dashboard-api`, code | `_require_internal(event)` first in every handler but `get_users_me`: 403 unless the authorizer context carries tier exactly `internal` OR firmId exactly `opal-capital`; the router passes the event to every handler | 1: `infra/aws/terraform/trade-pipeline` via the versioned artifact `s3://opal-313476888478-lambda-artifacts/trade-pipeline/trade-dashboard-api.zip` (`lambdas.tf:107-119`) |
| K2 | `opal-users-v2`, THREE synthetic rows (section 4), written and later deleted | create, then delete after the last token's exp | 1: the executor, by conditional put (`attribute_not_exists(PK)`) |

No env key, grant, route, table, layer or other function changes. No portal file changes (the page's own guard is a follow-on
the PRD names; it is not this act).

## 2. Blast radius

- **Who is served today and refused after: every caller who fails both comparisons.** Measured 2026-10-11 ~18:3xZ
  (`opal-users-v2`, 87 rows, no further page): tier `advisor` 52, `internal` 6, absent 29. A portal user whose firmId is not
  `opal-capital` and whose tier is not `internal` gets 403 on the eight routes after the act. That is the intended change.
- **Who must still be served: the 9 rows of `trade-users`** (9 of 9 scanned, all at Opal's domain). Joined to their portal rows:
  5 carry tier `advisor`, no userType, firmId `opal-capital`; 2 carry tier `advisor`, userType `Dev`, firmId `opal-capital`;
  2 carry tier `internal`. All 9 pass the ruled check (9 of 9 by firmId, 2 of 9 also by tier). The join read the STORED row;
  the token a live session carries is minted from it at login and was not read.
- **The portal's own callers of the eight routes, one read through each** (`portal/src/api/endpoints/trade-submission.ts`):

  | route | client function (line) | called from |
  |---|---|---|
  | `submissions` | `getAllSubmissions` (333) | no caller in `portal/src` |
  | `submissions/pending` | `getPendingApprovals` (340) | no caller in `portal/src` |
  | `submissions/by-initiator` | `getMySubmissions` (347) | `pages/TradeSubmission/hooks/useTradeSubmissionState.ts:84` |
  | `submissions/by-approver` | `getSubmissionsApprovedBy` (356) | no caller in `portal/src` |
  | `submissions/by-status` | `getSubmissionsByStatus` (367) | `useTradeSubmissionState.ts:97,110,122,134` |
  | `submissions/{id}` | `getSubmission` (378) | no caller in `portal/src` |
  | `submissions/{id}/excel` | `downloadExcelFile` (389) | `pages/TradeSubmission/hooks/useTradeSubmissionActions.ts:182` |
  | `users` | `getTradeUsers` (405) | no caller in `portal/src` |

  Denominator: a native search of `portal/src` (`*.ts`, `*.tsx`) for the eight function names; `opal_ai` searched for the
  route strings, 0 files. `mcportal` and any caller outside these two trees: NOT searched. One page calls three of the eight
  routes; five have no caller in the portal.
- **A non-internal person who opens `/trade-submission` after the act** (the page is `<ProtectedRoute>` with no tier guard,
  `portal/src/App.tsx:516-522`) sees the page with its lists failing 403. That is a worse page for a person who should never
  have had the data; the page's guard is the follow-on.
- **`users/me` is unchanged**, so the page's tab gating (`TradeSubmission.tsx:28`) reads as today for every caller.
- **The submit and workflow functions are not in this act.** OW-s-1's record
  (`deliverables/0.9.0_WK_NFRA_OPSWKF~7/FOUR_FUNCTIONS_WHAT_A_NON_INTERNAL_CALLER_CAN_DO.md`) says what they admit; their
  owner lines are the CTO's.

## 3. Expected plan (both branches)

- **Branch A, proceed:** `0 to add, 1 to change, 0 to destroy`: `aws_lambda_function.trade_dashboard_api`
  (`s3_object_version` and `source_code_hash` only).
- **Branch B, STOP and report:** anything else, including a change on any other function of the stack, the role, a table, a
  route, or a destroy. Nothing is applied on branch B.

## 4. The three synthetic callers (K2), and the live reads

The executor holds the signing key read; this seat holds no key. The shape and bounds are TCKT_VNEXT's
(`org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/TV_R1_SEAT_ARM_PLAN_AND_PAIR.md`, v2.2 with AMENDMENTS 1-2).

| caller | row `PK` (`SK PROFILE`) | token claims that matter | passes which comparison |
|---|---|---|---|
| OUT | `USER#opswkf-fwd8-out-20261011@opal.invalid` | `tier advisor`, `role user`, `firmId fwd8-synthetic-nofirm`, `userType test-filer` | neither |
| IN-T | `USER#opswkf-fwd8-int-20261011@opal.invalid` | `tier internal`, `role user`, `firmId fwd8-synthetic-nofirm`, `userType test-filer` | tier only |
| IN-F | `USER#opswkf-fwd8-inf-20261011@opal.invalid` | `tier advisor`, `role user`, `firmId opal-capital`, `userType test-filer` | firmId only |

- Each row carries `status active`, its `firmId`, `tier`, `userType`, a `name` beginning `NFRA_OPSWKF FWD-8 synthetic`, and
  `allowedFirmIds ["fwd8-synthetic-nofirm"]` as a LIST of one (the shape TCKT_VNEXT's clamp narrows on; an empty list's
  meaning on those surfaces was not read, so it is not used). `fwd8-synthetic-nofirm` is a firm id no data is filed under,
  so the list admits no real firm; this is narrower than the PRD's "one firm". NOT established by this seat: that every
  clamped surface narrows an ALL-origin token to the row list (taken from TCKT_VNEXT's pair, v2.2, not re-read here).
- Each token: RS256 with the current slot of the portal signing key, `iss opal-portal-auth`, `aud opal-portal-api`,
  `exp = iat + the run's length + 5 minutes` (the run spans the apply; the executor states the length before minting). Held in
  the executor's memory only: never stored, printed or committed.
- `userType test-filer` is carried as TCKT_VNEXT's pair v2.1 carried it, to keep `data_refresh` refusing the filers; that
  effect is that pair's reading and is confirmed by ONE extra read in the run: IN-T on one data-refresh GET route, expect
  refused; an admit is a STOP and cleanup.
- **What IN-T widens:** `tier internal` makes the authorizer derive `allowedFirmIds = ALL` for the token's life. Its row's
  one-entry list narrows it on the clamped surfaces (the ticket service and the investor-reporting hosts); the unclamped routes
  stay as reachable as for any internal user. This is the one widening in the act, bounded by the exp, and it is the question
  for the CTO half. If the CTO refuses it, the tier-internal arm is read instead by a real internal session at the page
  (section 6, alternative), and IN-T is not minted.

**The reads, every one through the CloudFront host, one route: `GET /api/general/trades/submissions/pending`.** The executor
records the status code and the response's `count` field ONLY; no submission body is written to any file or message.

| # | when | caller | expect | on the other answer |
|---|---|---|---|---|
| R0 | BEFORE the apply | OUT | 200 (the defect, read live for the first time) | 403 -> STOP: the defect is not what the census says; nothing is applied; cleanup |
| R1 | AFTER | OUT | 403 | 200 -> the release did not take: read the deployed bytes, then roll back K1 |
| R2 | AFTER | IN-T | 200 | 403 -> roll back K1 |
| R3 | AFTER | IN-F | 200 | 403 -> roll back K1 (this is the branch a tier-only check breaks: 7 of the 9 people) |
| R4 | AFTER | OUT, on `GET /api/general/trades/users/me` | 200 with its own email | anything else is recorded, not a rollback |

## 5. After-reads (the executor, each printed)

- **(a)** `CodeSha256` of `trade-dashboard-api` equals the uploaded zip's; the zip is diffed against the build input MEMBER BY
  MEMBER (`dashboard_api.py`, `config.py`, `excel_generator.py`, and any other member, each by sha256 against the file at the
  pin), with the member count printed.
- **(b)** Env and layers unchanged: `SUBMISSIONS_TABLE` and `openpyxl-layer:3` as before, read before and after.
- **(c)** R0-R4 as the table above, with the time of each.
- **(d)** The replan is 0-diff.

## 6. Rollback (per key)

- **K1:** re-point the function to the PRIOR artifact `s3_object_version`, read and recorded BEFORE the apply; one
  `safe-apply` at the parent of the pin. The prior version serves every caller as today.
- **K2:** each row stays in place until its token's `exp` has passed; then it is deleted and read back ABSENT with
  ConsistentRead. (A row removed early widens: the row list is the narrowing, TCKT_VNEXT row D2-S20.) The ledger closes only
  after the three ABSENT reads.
- **Alternative for the tier-internal arm,** if IN-T is refused by the CTO half: an Opal staff member whose row carries tier
  `internal` opens `/trade-submission` after the act and the History tab lists; that read is recorded by the seat that
  watched it, and R2 is marked by-session.

## 7. COO half

`2.0.0_SA_COO~O2` signs the blast radius above for keys K1 and K2, for both plan branches and for both answers of each of
R0-R4, with the rollback per key. The ledger entry is the applier's, opened at step 0 and closed after K2's three ABSENT
reads.

**COO half -- SIGNED at the pin in section 8.**

## 8. Pin and applier

- **Pin:** box/dell2 @abf78fcb7f (the merge of `wk-NFRA_OPSWKF-8` @c8030a7c36). The build input is
  `infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/` at that commit; `dashboard_api.py` sha256 begins
  `b152580eaf2066ad`, last changed by c8030a7c36. `config.py` and `excel_generator.py` are unchanged by this project.
- **Graded at the pin by the issuer, on the merged tree:** `OW-S2-TESTS-OK passed=8`;
  `OW-S2-PROBE-OK refused=80 of 80 (8 outsiders x 10 routes), served=30 of 30 (3 insiders), users/me own row`;
  the commit gate clean on 2 of 2 files. The issuer read the whole handler diff: one helper, two constants, `event` threaded to
  every handler, the check first in each, the `/excel` branch checked before its 400, `get_users_me` untouched.
- **Applier and executor:** `0.7.0_AE_CloudOps~DELL2` (LIVE and idle at 18:5xZ by the broker's roster). If the dell2
  principal cannot plan or apply the `trade-pipeline` root, or cannot read the signing key, the act goes cross-box to the
  laptop's cloud-ops seat as the owner's ruling offers, under this same pair; nothing is applied in between.
- **Condition carried from `1.0.0_SA_CTO~DELL2` msg 5588:** the positive arm is read twice, by IN-T and by IN-F (R2 and R3).
- **The apply order is cut by the issuer when the CTO half is given,** and not before.

-- 2.0.0_SA_COO~O2, 2026-10-11
