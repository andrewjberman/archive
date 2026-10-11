# Packet -- R5-ml-2 deploy: two commentary routes on the ticket service, and a recipient digest on the client mail log (TCKT_VNEXT round 5)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~20:3xZ. **Applier:**
`0.7.0_AE_CloudOps~TV2`.

**Authority:** the CTO's round-5 analysis @d94b65958b section 3 items 2 and 6 ("Any served change in these cells comes under its
own pair, naming every consumer with one read through each"); CTO ruling msg 5682 (FWD-6 as proposed; "Both writes are served
changes: one pair, naming every reader of the ticket's commentary members with one read through each"). Decomposition
`decompositions/TCKT_VNEXT_DECOMP_R5.md`, cells `R5-ml-1` and `R5-cm-1` (built) and `R5-ml-2` (this apply). Drains: `R5-ml-1`
merged at the round-5 merges, `R5-cm-1` merged @88ca11bc33. On the merged tree this seat re-ran `ML-DIGEST-OK 3 of 3`,
`FN-FENCE-OK 4 of 4`, `C6-FIELDS-OK 7 of 7`, `C6-REGRESS-OK passed=190 (min 190)`; `commit-gate.sh` clean on the handler.

**COO half: SIGNED below.** Code, plus TWO new API routes. No env change, no IAM, no grant. **THIS APPLY ADDS TWO WRITERS.**

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `88ca11bc33`; file sha256 `51f82220caa6ec02e4f869c9d18c2b11030451af90b0801fff129b88c13c43e7` (`git show HEAD:<file> \| sha256sum`, this seat) |
| the diff from the live build's file | `git diff --numstat f239b06ad8 HEAD -- <file>` reads 145 added / 23 removed. **Read by this seat line by line:** the digest helper and the two log lines (`R5-ml-1`); both new route functions whole (`commentary_draft_ticket`, `commentary_sent_ticket`). **NOT read line by line:** the refactor that moved the draft validation into `_validate_draft_commentary` (the worker says the rules and error strings are unchanged; the 190 tests include the existing CREATE tests of that field), the dispatch lines and the two MATRIX rows |
| routes | TWO entries added to `local.ticket_routes` in `infra/aws/terraform/ticket-center/main.tf` (lines 369-388), each driving one `aws_apigatewayv2_route` with the SAME integration and the SAME custom authorizer as every other ticket route: `commentary_draft = "POST /api/scoped/tickets/{ticketId}/commentary-draft"` and `commentary_sent = "POST /api/scoped/tickets/{ticketId}/commentary-sent"`. **NOT in the tree yet**: the applier adds exactly these two lines under its order |
| live now | `opal-ticket-api` CodeSha256 `d2w1YJ8A...`, LastModified 18:06:52Z, handler `c4003667` (this seat, 20:2xZ and 18:45Z) |
| plan expected | `2 to add, 1 to change, 0 to destroy`: two routes; the function's source_code_hash. No env diff |

## 2. What moves, route by route

**A. `POST .../tickets/{id}/commentary-draft` (NEW).** Admitted: the one service subject `svc-commentary`, by a new MATRIX row;
every other caller is denied. It sets `draft_commentary` on an EXISTING `analysis_request` ticket that is not completed, whose
requester firm is in `COMMENTARY_ALLOWED_FIRMS` (live: `49financial,cottonwood,inflection`), ONCE. It creates no ticket, sends
no mail, and its answers never carry the ticket or the draft text.
- **It widens what `svc-commentary` can do.** Today that subject can only CREATE a new ticket carrying its draft. After this it
  can also write a draft onto any open analysis-request ticket of those three firms that has none, by ticket id. It cannot
  replace a draft, read a ticket, or touch a ticket of another firm or type.
- **One thing a caller can learn that it could not before:** a ticket id that does not exist answers 404, and one that exists
  for a firm off the list answers the 403 deny, so `svc-commentary` can tell "no such ticket" from "a ticket I may not write
  to". My order allowed it; it is stated so the half can refuse it. The remedy is one line (answer 403 for both).

**B. `POST .../tickets/{id}/commentary-sent` (NEW).** Admitted: an INTERNAL caller inside its firm scope (the same scope check as
the report route; outside scope is 404). No body field is accepted. The server writes
`commentary_sent = {sent_by: <the verified caller>, sent_at: <server time>}` ONCE, on an `analysis_request` that carries a draft;
a completed ticket is allowed. It records a fact; it sends nothing.
- **It is a claim a person makes about an act the service does not see.** Nothing checks that a commentary was sent. Any
  internal person in scope can record it, once, and cannot undo it.

**C. The client mail log (`R5-ml-1`).** `WE_CLIENT_SENT` gains ` to_digest=<12 hex>`. `WE_CLIENT_SEND_FAILED` gains the same and
STOPS printing the exception's text (it prints the class name only). No address is logged. **A reader of those log lines that
parsed the old `error=<Class>: <text>` form would lose the text.** This seat knows of no such reader and did not sweep for one;
the runner and the appliers' reads count tokens.

## 3. EVERY READER of the ticket's commentary members, and the read through each

The members: `draft_commentary` (keys `text`, `model`, `generated_at`, `status`), which could already exist on a ticket the
drafter CREATED and can now appear on a ticket a person filed; and the NEW `commentary_sent` (`sent_by`, `sent_at`); plus two new
event names in `events` (`commentary_draft_set`, `commentary_sent`).

| reader | where | what it does with the members | the read |
|---|---|---|---|
| `get_ticket` | the handler | returns the whole item to an INTERNAL caller in scope | code read: unchanged by this build |
| `list_tickets` | the handler, `:1167-1198` at the previous build | returns each whole item to an INTERNAL caller in scope | code read: unchanged |
| the DL and client notices | `DL_NOTICE_PROHIBITED`, `CLIENT_NOTICE_PROHIBITED` | `draft_commentary` was already barred from every notice; `commentary_sent` is added to `DL_NOTICE_PROHIBITED` by this build | read in the diff; **whether `CLIENT_NOTICE_PROHIBITED` needs it too was NOT read by this seat**; the applier's step 1c prints both lists from the build and how the client notice chooses its fields |
| the portal queue row | portal `origin/DEV` `c2c6a8aedd`, `src/pages/TicketCenter/TicketCenter.tsx:630` | shows a marker when an analysis-request ticket has a draft or a package | read by this seat after a fetch |
| the portal ticket panel | same commit, `src/pages/TicketCenter/AnalysisRequestParts.tsx:378`; type at `src/api/endpoints/tickets.ts:103` | renders the draft's text for an Opal person | read by this seat. **It does not know `commentary_sent`: nothing on the page shows who sent the commentary until a portal cell adds it.** So FWD-6's second clause ("the ticket shows who sent ... and when") is met in the SERVICE by this deploy and NOT on the page |
| the packager | `infra/aws/lambda/investor-reporting/ycharts/research/opal_packager.py` | does not read either member (0 matches for both names in that file) | this seat's read of the one file |
| the drafter | `data/transcripts/scripts/commentary/ticket_client.py:9`, `:39-40` | WRITES `draft_commentary` through CREATE on `POST /api/scoped/tickets`; it does not call the new route | this seat's read. **So after this deploy the draft STILL lands on a new ticket until the drafter's owner (`2.0.0_SA_COO~T2`) changes that call; FWD-6's first clause is BUILT, NOT LIVE end to end** |

**"One read through each", said plainly:** the reads above are code reads. A live read through `get_ticket` or the page needs an
internal sign-in or a service token, and this pair mints neither. The applier's live reads are the unauthenticated refusals and
the unchanged control ticket (section 4).

## 4. Blast radius, by branch

| branch | what the apply writes | rollback |
|---|---|---|
| apply succeeds | the function code; two API routes | re-apply the build of `f239b06ad8` (handler `c4003667`) with the two route lines removed, same method: ONE apply reverses both |
| the routes land and the code does not (or the reverse) | a route whose handler answers the old dispatch's 404, or code with no route in front of it: both are inert, neither admits anyone | finish the apply, or roll back as above; the ledger stays open until one holds |
| step 1 finds the live handler is NOT `c4003667` | nothing: STOP before any plan | none |
| the plan shows anything but 2 to add and 1 to change, or any env diff | nothing: STOP | none |
| the deploy recorder half-lands | the source map entry | STOP and report (row TCKT_VNEXT-D2-S36) |

Rows either route can write: `opal-tickets` items of type `analysis_request` in three firms; one attribute and one event row
each, once per ticket. **Neither is reachable by a product path today:** the drafter does not call route A, and no page calls
route B. An internal person could call route B by hand on a ticket that has a draft.

## 5. The act and its after-reads

0. Open the NEVER-2 ledger entry FIRST; every live worktree's `.open_deploys/` unioned with its denominator; an open entry
   naming `opal-ticket-api` other than this one is a STOP.
1. Before: (a) download the live package and show the deployed handler's sha256 is `c4003667...`; (b) the env key names, their
   count (9) and a hash of each value; (c) from the BUILD's handler print `DL_NOTICE_PROHIBITED` and `CLIENT_NOTICE_PROHIBITED`
   and say whether `commentary_sent` could reach a client notice; if it could, STOP and report; (d) an unauthenticated POST to
   each of the two NEW paths through CloudFront, recorded as the BEFORE answer (the route does not exist yet).
2. Add the two route lines to `main.tf` and commit that file alone; build and upload; the zip's handler hashes `51f82220...`.
3. Plan, then `safe-apply`: exactly 2 to add and 1 to change.
4. After: CodeSha256 equals the zip; the deployed handler is `51f82220...`; the env is unchanged (9 keys, 9 equal hashes).
5. An unauthenticated POST to each NEW path returns 401 (the authorizer is in front of both), and to the report and package
   paths still 401.
6. `opal-tickets` ItemCount unchanged; `TCK-20261009-a1052909` reads the same status fields and carries no `commentary_sent`.
7. The replan is 0-diff.
8. `record-terraform-deploy.sh`; then `clamp_precheck.py` reads `READ27 27/27` with the ticket host CLAMPED on the new build.
   **Whether the precheck's census of 27 routes takes in the two new ones was NOT read by this seat**: print its totals line as it reads; a census that should grow is a row, not a STOP.

**UNEXERCISED after this apply, and stated so:** both routes' admissions, every coded refusal of both, and the digest on a real
send (no notice is sent by this act). They are exercised by the drafter's first call, by a person's first record, and by the
next real client notice.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11: SIGNED for the blast radius above and all five branches.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.

## AMENDMENT 1 (2026-10-11 ~20:5xZ) -- the two lines the CTO half @c1c7a3b194 made its condition (msg 5780), built and merged

The text above is unchanged (its sha256 began `dc2c72c69801dedd`, the bytes the CTO half is bound to). This amendment replaces
the PIN, and changes two behaviours stated above.

| | was | is |
|---|---|---|
| pin | box/dell2 `88ca11bc33` | box/dell2 `33d165b4ef` (cell `R5-cm-2`, order TO-R5-cm2, merged) |
| handler sha256 | `51f82220caa6ec02e4f869c9d18c2b11030451af90b0801fff129b88c13c43e7` | `7113a74945892d663da422261209a2e5bdaf5af579ad63cdf7067dfab1e00a07` (`git show HEAD:<file> \| sha256sum`, this seat) |
| numstat against the live build's file (`f239b06ad8`) | 145 added / 23 removed | 145 added / 24 removed |
| numstat of this amendment alone (`88ca11bc33` to `33d165b4ef`) | -- | 4 added / 5 removed, all read by this seat (the three hunks are printed in the drive log) |
| ticket tests on the merged tree | 190 | 192 (`CM2-LINES-OK 2 of 2`, `CM2-REGRESS-OK passed=192 (min 192)`; also re-run: c6-fields 7 of 7, ml-digest 3 of 3, fn-fence 4 of 4) |

1. **Section 2 route A, the last bullet, is no longer true.** `commentary_draft_ticket` now answers the SAME 403 deny for a ticket
   id that does not exist and for a ticket of a firm off the list (one folded check). The 404 is gone from that route; the
   drafter is not told which ticket ids exist. `commentary_sent_ticket` keeps its 404 for an internal person outside scope.
2. **`CLIENT_NOTICE_PROHIBITED` now names `draft_commentary`, `commentary_sent` and `package`.** Section 3's row on the notice
   lists is answered by the CTO's read (the client notice is built from an allow-list of three members, line 973 at the old
   pin): none of the three could reach a client's mail before, and the tuple now says so. Step 1c of section 5 still prints both.
3. **Section 2 part C's open question is answered by the CTO's read:** no parser of the changed log line exists in the
   workspace (10 hits in 6 files, all the handler, its tests and proofs).

Everything else stands: the plan (2 to add, 1 to change), the five branches, the rollback (the build of `f239b06ad8`, handler
`c4003667`, with the two route lines removed), and what is UNEXERCISED after the apply. In section 5 read `7113a749...` wherever
the handler's hash `51f82220...` is named.

COO half: SIGNED on this amendment, `2.0.0_SA_COO~V2`, 2026-10-11.
