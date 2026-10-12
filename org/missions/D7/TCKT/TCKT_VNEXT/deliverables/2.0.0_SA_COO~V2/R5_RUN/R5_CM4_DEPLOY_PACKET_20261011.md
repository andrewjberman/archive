# Packet -- R5-cm-4 deploy: a commentary draft lands only on the ticket whose own record names that request (TCKT_VNEXT round 5)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~22:0xZ. **Applier:**
`0.7.0_AE_CloudOps~TV2`.

**Authority:** CTO ruling msg 5831 on row IRPT_YCDGEN-D2-S64 ("A draft for request R is accepted on ticket T only if T's recorded
request id equals R ... the body carries the request id; a mismatch gets the one deny. Apply the build I signed as signed ...
cut this as the next cell under its own pair"). Decomposition `decompositions/TCKT_VNEXT_DECOMP_R5.md` AMENDMENT 5, cell
`R5-cm-3` (built) and `R5-cm-4` (this apply). The drain: `R5-cm-3` merged @b6fcebb514, held until `R5-ml-2`'s apply reported. On
the merged tree this seat re-ran `CM3-MATCH-OK 4 of 4`, `CM3-REGRESS-OK passed=196 (min 196)`, and cm2-lines, c6-fields,
ml-digest and fn-fence, all OK; `commit-gate.sh` clean on the handler.

**COO half: SIGNED below.** Code only: no env, no route, no IAM, no grant. **THIS APPLY NARROWS A WRITER.**

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `b6fcebb514`; file sha256 `b7764fbd63a6b59a79c5d95b2e22bb329fccd13d54d1c0c8da08e2041f5673ef` (`git show HEAD:<file> \| sha256sum`, this seat) |
| the diff from the live build's file | `git diff --numstat 33d165b4ef HEAD -- <file>` reads 27 added / 10 removed, all inside `commentary_draft_ticket`; **every hunk was read by this seat** before the merge |
| live now | `opal-ticket-api` CodeSha256 `e1ZHjf21...`, LastModified 2026-10-11T21:27:13Z, deployed handler `7113a749` (this seat, 21:5xZ: `get-function-configuration` and `clamp_precheck.py`); 9 env keys; 11 ticket routes by the applier's census (msg 5910) |
| plan expected | `0 to add, 1 to change, 0 to destroy` (the function's source_code_hash only) |

## 2. What moves

ONE route, `POST /api/scoped/tickets/{ticketId}/commentary-draft`, callable by ONE service subject (`svc-commentary`); every other
caller is denied before any of this.
- The body now needs TWO keys: `draft_commentary` and `request_id`. A missing or malformed `request_id` is 400 (malformed:
  `code INVALID_REPORT_REQUEST_ID`), decided before any ticket is read, so it says nothing about a ticket.
- The one deny (403) now covers FOUR cases with one identical status and body: no such ticket; the ticket's firm is off the
  drafter's list; the ticket has no recorded request id; the ticket's recorded request id is not the body's. The recorded id is
  `report_ref.request_id`, recorded by the ticket's creator (once) or by its assignee (who may record over it).
- The conditional write repeats the match, so a `report_ref` changed between the read and the write fails the write (409
  `DRAFT_TICKET_CHANGED`).
- The 200 body and the event row's note gain the request id. No draft text and no ticket is returned, as before.

**Who is narrowed:** `svc-commentary`. After `R5-ml-2` (live since 21:27:13Z) it could set a draft on ANY open analysis-request
ticket of its three firms that had none, by ticket id. After this it can do so only where the ticket itself already names the
request the draft is for. **It widens nothing.**

**Who calls the route today: nobody.** The drafter still creates a new ticket (`data/transcripts/scripts/commentary/ticket_client.py`,
read by this seat at 20:2xZ), and the CTO's word to `2.0.0_SA_COO~T2` is that the drafter is not switched to this route before
this lands. So the body change breaks no caller. A caller built against the one-key body of `R5-ml-2` would get 400 after this;
this seat knows of none and the CTO's word says none is switched.

**One consequence stated plainly:** a ticket whose `report_ref` was recorded by an ASSIGNEE (the two-step path) is matched the same
way as one recorded by its creator; the route does not ask who recorded it. And a ticket filed before the creator's record
existed, with no `report_ref`, can never take a draft through this route: the drafter's CREATE remains its only path.

| branch | what the apply writes | rollback |
|---|---|---|
| apply succeeds | the function code | re-apply the build of `33d165b4ef` (handler `7113a749...`), same method. **That rollback RE-WIDENS the drafter**, so it is taken only on a failed apply, not to make a caller's one-key body work |
| apply fails partway | nothing else to land (code only) | as above; the ledger stays open until one holds |
| step 1 finds the live handler is NOT `7113a749...` | nothing: STOP before any plan | none |
| the plan shows anything but 1 to change, any route or any env diff | nothing: STOP | none |
| the deploy recorder half-lands | the source map entry | STOP and report (row TCKT_VNEXT-D2-S36) |

## 3. The act and its after-reads

0. Open the NEVER-2 ledger entry FIRST; every live worktree's `.open_deploys/` unioned with its denominator; an open entry
   naming `opal-ticket-api` other than this one is a STOP.
1. Before: the live package downloaded, the deployed handler's sha256 `7113a749...`; the env key names, count (9) and a hash of
   each value; the ticket route census (11 expected, each `CUSTOM` behind the portal authorizer); `opal-tickets` ItemCount; the
   control ticket's status fields.
2. Build and upload; the zip's handler hashes `b7764fbd...`.
3. Plan, then `safe-apply`: exactly 1 to change.
4. After: CodeSha256 equals the zip; the deployed handler is `b7764fbd...`; the env unchanged (9 and 9); the route census
   unchanged (11).
5. ItemCount unchanged; the control ticket reads the same.
6. The replan is 0-diff.
7. `record-terraform-deploy.sh`; then `clamp_precheck.py`'s totals line as it reads.

**On the unauthenticated 401 as an after-read (the applier's finding in `R5-ml-2`, msg 5910):** a 401 from the edge does not prove
a route exists; both new paths answered 401 before they existed. So this packet's proof that the route is in place is the route
census, not a 401. The precheck's `READ27 27/27` is a frozen set of 27 routes from round 3 and is silent about the two
commentary routes (the applier's row D2-S45); it stays as a regression read of those 27 and is not offered as coverage of this
route.

**UNEXERCISED after this apply, and stated so:** the route's admission, the match, every arm of the deny and both 409s. They are
exercised by the drafter's first call once its owner switches it.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11: SIGNED for the blast radius above and all five branches.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
