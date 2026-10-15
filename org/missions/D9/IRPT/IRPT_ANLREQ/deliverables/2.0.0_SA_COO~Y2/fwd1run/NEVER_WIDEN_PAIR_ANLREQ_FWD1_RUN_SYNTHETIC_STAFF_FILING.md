# IRPT_ANLREQ FWD-1 run -- one synthetic Opal staff user signs in to the portal, files ONE Analysis Request through the Ticket Center page, and nobody touches it after Submit -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No run order is released until the CTO half is signed on this file's blob AND every precondition of section 5 reads green at step 0.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-15. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
It is the run the PRD names (`prd/IRPT_ANLREQ_PRD.md` FWD-1, lines about 28-38: "on DEV, a SYNTHETIC Opal staff user (minted and deleted under a never-widen pair) signs in, opens the Ticket Center ... CHOOSES the partner firm ... Nobody touches anything after Submit"). The CTO ruled the executor and the mail guard (msg 7944: `0.7.0_AE_CloudOps~AQ2` mints the user and files through the DEV page; the live `TICKET_DL_MAP` is `{}`; a step-0 re-read and a STOP on any non-`@opalinvest.com` recipient). It follows release 31 (pair signed, blob `8fb19a3356`; legs L and R to be applied first). Cells: `AR-y-342` (prerequisites read, merged `ae407c4f8f`), `AR-y-343` (run mechanics read, merged `833cacb2b7`), `AR-y-344` (login read, merged `99599a99ed`), `AR-y-345` (the driver and mint helper build, merged `94b3abe514`).

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened, with its check re-run (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read. A statement with none of these words is a plan.

## 1. What moves

One run, in this order, by ONE applier (`0.7.0_AE_CloudOps~AQ2`, on the dell2 box), driven by ONE script (`fwd1_driver.mjs`, RECORD, `AR-y-345`):

| step | what | where |
|---|---|---|
| M | ONE users-table row is written: `USER#fwd1-staff-r41a@opal.invalid` / `PROFILE`, with a bcrypt password hash, `status` active, `firmId` `opal-capital`, no MFA, a 3-hour `exp` | `opal-users-v2` (`fwd1_mint.py mint`) |
| S | the script signs in through the real `/auth/login` form on the LOCAL dev build (`http://localhost:5174`, which reaches the live API and auth through CloudFront), opens the Ticket Center, CHOOSES the firm `49financial`, fills the form (variant Overview), attaches the synthetic holdings CSV, clicks Submit | the portal page; four live calls |
| P | the script then only READS: it reloads the ticket page for up to 20 minutes and records which of the four attachments are present and openable | the portal page |
| R | in a `finally` block the minted row is deleted and read ABSENT by a ConsistentRead and the email GSI | `opal-users-v2` (`fwd1_mint.py remove`) |

Nothing else moves: no IAM, queue, secret, Lambda, Terraform or portal deploy. **Not in this run:** the partner-firm filing (parked, ADDENDUM v0.6), a PROD action, the removal of `fwd1-staff-r41a@opal.invalid` from the producer list (owed to the next resident release after this run, CTO 7890 condition 3).

## 2. Start state (RECORD / MEASURED; the applier re-reads it at step 0, and any difference ABORTS)

- **The user store:** `fwd1-staff-r41a@opal.invalid` has no row (the applier reads a ConsistentRead and the email GSI at step 0; a present row ABORTS, because the name is never reused).
- **The portal:** `origin/DEV` carries the three FWD-1 candidates (MEASURED by this seat, ls-remote read 2026-10-15 ~02:2xZ: DEV `ad7c100b` contains `a17932990a` the commentary reader, `6f4e5f671f` J7 the staff filer's firm choice, `406345bce1` the always-send `commentary_requested`). The page is the local build of that head, started by the applier.
- **The pieces this run needs (the applier reads each; the issuer's last read is cited):** leg L closed (the irpt-status route and the AR-y-71/32 reads), leg R closed (the resident at r31: both queue wirings, the packager block, the two-entry producer list), the intake Lambda accepting `commentary_requested` (IRPT_BCKEND IB-pr-456, Andrew's act f61b: NOT applied at the record; the build record says the digest the apply must print is `AHxuDf7h...`), the drafter Lambda live (RECORD, `TO-READ-R31`: ENABLED mapping, env set), `TICKET_DL_MAP` empty (CTO, live read ~02:1xZ), the packager secret and door (RECORD, `TO-READ-R32`).
- **The producer choice:** a request whose accepted `owner.principal_id` is `fwd1-staff-r41a@opal.invalid` takes the Opal producer; any other principal takes the YCharts path, down since 10-11 (pair 31, W1).

## 3. Artifact, pins, rollback

- **The script and helper (RECORD, `AR-y-345`, re-run by this seat):** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~149/fwd1_driver/` -- `fwd1_driver.mjs` (348 lines), `fwd1_mint.py` (148 lines), `fwd1_holdings_49financial.csv`; the applier prints each file's sha256 at step 0 and the order carries them. Offline self-test 29 cases, the guard mutant FIRES, the hash check `scheme=2b cost=12 python=ok bcryptjs=ABSENT`. **NOT exercised before the run (named): the login of a Python-written hash through the auth handler's bcryptjs (`bcryptjs` is absent on this box; both are bcrypt `$2b$12$`), and the page selectors against the live DEV head.** A failed sign-in therefore ABORTS the run with the row removed.
- **Rollback / cleanup:** the minted row is removed by the script's `finally`; if the script dies, the applier runs `python fwd1_mint.py remove` by hand and the 3-hour `exp` is the backstop. The ticket, the retained input and the request this run creates are NOT rolled back: they are the evidence and are named in the run record; their later removal is a separate delete call for Andrew (an S3 delete of the input, per the earlier c449 precedent).

## 4. Blast radius -- what a person or a system meets

Five things, each named.

1. **W1, a transient INTERNAL login exists.** For the minutes between step M and step R a users row can sign in to the portal with a password that only the running script holds (generated in memory, 24+ characters, passed to the helper on stdin, never written, logged or put in an argument; the redactor strips it from every log line, RECORD). **What it can do while alive:** the portal issues it `tier internal`, which the authorizer maps to ALL firms (`computeAllowedFirms`, RECORD `AR-y-342` q2): the SESSION is a full internal staff session. The script's route guard admits only GET/HEAD/OPTIONS and seven named POSTs (the login, refresh and logout routes and the four filing routes), and aborts everything else (RECORD, selftest). **What survives the removal:** the 15-minute access token (the authorizer verifies the signature only) -- at most 15 minutes of an already-issued internal bearer, held only inside the script's browser; and nothing else: `/auth/refresh` re-reads the row and answers `User not found` once it is gone (MEASURED by this seat, `auth.ts` lines 484-540), so the 7-day refresh cookie is dead at removal. **Limit named:** the credential is a password row, the first of its kind in this estate other than the dormant UI walker; it exists only while the order runs.
2. **W2, one ticket is created.** `POST /api/scoped/tickets` for an `analysis_request` in `49financial`, chosen by the staff filer (J7). **No mail:** a successful create calls `notify_dl_isolated`; the live `TICKET_DL_MAP` is `{}`, so the notifier refuses and logs `WE_DL_UNCONFIGURED` (CTO 7944, live read; `lambda_function.py` line 923). **Guard (CTO):** the applier re-reads the map at step 0; non-empty: resolve the chosen firm's recipients first, any non-`@opalinvest.com` recipient is a STOP; a `WE_DL_SENT` for a non-Opal address in the trace is a STOP.
3. **W3, one retained input and one analysis request.** The upload door stores the synthetic holdings (the R29 D1 file, synthetic, RECORD) as a retained input of `49financial`; the analysis submit accepts a request owned by `fwd1-staff-r41a@opal.invalid` (`home_firm_id` `opal-capital`), which the Opal producer serves (W1 of pair 31) and which the drafter Lambda turns into a commentary draft.
4. **W4, an external model call.** The drafter sends the report's key surfaces (abstract fields only, no client identity: PRD FWD-3) to the Kimi model (the standing C-KIMI route). The input is synthetic. No client data leaves.
5. **W5, the first real attach.** The resident's packager principal `svc-irpt-packager` calls `POST /tickets/{id}/package` for the first time (its token, signature, `iss` and `aud` are unverified until now, pair 31 limit). If it is refused, the ticket stays open without the package and the run records which of the four attachments are missing: that is a finding, not a defect of this window.

## 5. Order of the run and the reads

Each read carries its claim word; a missing read is `ABSENT`, and ABSENT is not EXERCISED.

**Step 0 (the applier, within the hour before the first act; ANY red ABORTS and mints nothing):** R0a: this file and BOTH halves signed at the same blob; one NEVER-2 ledger (`irpt-fwd1-run-<date>`; legs M mint, S submit, P poll, R remove); no open deploy entry in any live worktree names the resident, `irpt-status`, the ticket service, the users table or `opal-users-v2`. R0b: the user is ABSENT (ConsistentRead and the GSI). R0c: `origin/DEV` contains `a17932990a`, `6f4e5f671f` and `406345bce1`; the local dev build is started from that head under a private worktree outside the product tree with `bun run dev:live --port 5174` (port 5174 only), and `GET http://localhost:5174/` answers. R0d: `irpt-status` CodeSha256 is `PcGK+EpSq0EelZP+2T8+PB6b+ZXB+q3BCjD9g4UNiLE=` (leg L). R0e: the resident root is `0485393f3a-r31` (the host read of leg R's record) and `commentary_ready` and `analysis_ready` read 0 and 0. R0f: `irpt-ycharts-generate` has the IB-pr-456 digest (read-only; f61b's release: if it reads the pre-apply digest `tdpterTMfJl...`, ABORT). R0g: `TICKET_DL_MAP` re-read: `{}` or resolve-and-STOP as section 4 W2. R0h: the packager secret's `LastAccessedDate` read and printed (the run's first attach moves it; the order records before and after). R0i: the script's three checkers re-run (the driver check prints `DRIVER-OK 29 selftest cases`).
**Step run:** `node fwd1_driver.mjs --base http://localhost:5174 --firm 49financial --holdings <the csv> --out <dir> --poll-minutes 20 --go IRPT_ANLREQ.TO-RUN-FWD1.<id>`. The script runs M, S, P, R as section 1 states and writes `run_report.json` and screenshots. The applier does not touch the browser.
**After-reads (V):** F1 the removal lines: `ABSENT GSI` and `ABSENT CONSISTENT` for the address. F2 the ticket id, its status (still OPEN) and the attachments the script recorded (four expected). F3 the request's accepted record: `owner.principal_id` is the synthetic address, `commentary_requested` true, the producer recorded as Opal. F4 the queue depths read afterwards (all five, no DLQ grew). F5 `TICKET_DL_MAP` and the ticket Lambda's log: `WE_DL_UNCONFIGURED` and no `WE_DL_SENT`. F6 the packager secret's `LastAccessedDate` after (it moved if the attach was attempted). F7 an Opal person's acceptance is the ACCEPT of the PRD: the order reports the ticket id to `2.0.0_SA_COO~Y2`, who asks the CRO (the trace seat) to open it.

## 6. Both branches (the expected outcome is stated for each)

| state | safe? | evidence |
|---|---|---|
| step 0 red | **SAFE: nothing minted** | the order stops and reports which read |
| M fails (`MINT-REFUSED`) | **SAFE** | no row, nothing signed in |
| sign-in fails | **SAFE: the `finally` removes the row** | F1 |
| Submit lands, the chain completes, four attachments present | the intended state | F2 |
| Submit lands, an attachment is missing | **SAFE, a finding** | the run record names which hop; no retry in this window (a retry is a new order and a new address) |
| the script dies mid-run | **cleanup by hand** | `python fwd1_mint.py remove`; the `exp` backstop is 3 hours |
| a non-Opal recipient appears in the mail trace | **STOP** | CTO 7944; the run reports at once |
| rollback | there is none for the ticket and input: they are evidence | section 3 |

## 7. Limits named

- The page selectors, the Submit control (`File Analysis Request`, `TicketCenter.tsx` line 731, no `data-slot`: row `W149-S2`) and the login of the Python-written hash were not exercised live before this run (section 3).
- `bcryptjs` is absent on the dell2 box, so the cross-library hash check is `ABSENT`, not passed (row `W149-S3`).
- The commentary model, the packager's first attach and the producer-list address in use are first exercised here; their PASS is the run's finding, not this file's claim.
- The run depends on Andrew's act f61b (the IB-pr-456 release by IRPT_BCKEND); until R0f reads the new digest this window does not open.
- The ticket, retained input and request persist after the run; their deletion is a later call.

## 8. Owed before any run order is released

1. The CTO half on this file's blob, covering both branches of section 6, including: **(a)** that W1 to W5 are the whole widening, W1 (a transient internal password login, the first of its kind) in particular; **(b)** that the mail guard of msg 7944 is carried as the step-0 and F5 gates; **(c)** that the persisted ticket, input and request are accepted as evidence with a later delete call.
2. The run order to `0.7.0_AE_CloudOps~AQ2` (STAGED until leg L, leg R and f61b read green), carrying a `# pipeline-override:` line, cut by this seat only after (1).
3. The NEVER-2 ledger opened at the start of the run.
