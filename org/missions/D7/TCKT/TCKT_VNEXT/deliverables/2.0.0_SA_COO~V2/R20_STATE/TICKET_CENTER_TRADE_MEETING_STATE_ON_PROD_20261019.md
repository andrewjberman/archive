# Ticket Center on PROD: Trade Request and Meeting Request, measured state (2.0.0_SA_COO~V2, 2026-10-19 19:40Z; Trade section rewritten 23:10Z after TO-R20-PROD3 closed)

Asked by the CTO (msg 10900, Andrew's dell2 priority order). Base: origin/PROD `8cd45f623bdf` (`git -C portal ls-remote origin refs/heads/PROD` read 19:37Z). Drain: 0 worker branches, 0 worktrees of this lane (five TCKT_VNEXT branches merged into box/dell2).

## Meeting Request -- WORKS on PROD (measured, exercised)
Run: TO-R20-PROD2 by 0.7.0_AE_CloudOps~TV2, 18:11Z to 18:29Z, https://opalinvest.dev, ticket TCK-20261019-c50b4967.
- Filer filed a Meeting Request; it showed "Waiting for the coordinator" (shot prod_filer_waiting).
- Coordinator, inside ONE routing window (open 18:16:24Z, closed 18:23:40Z), saw the proposed times and "Confirm this time" and confirmed one (shot prod_coordinator_controls).
- Filer reloaded and read "Confirmed for 2026-10-26 14:00 ET ... by tckt-r20-pcoord-20261019@opal.invalid" (shot prod_filer_confirmed).
- Routing restored: meeting_request.primary = jeanette@opalinvest.com alone, read back. Ticket and both synthetic rows deleted 18:29:30Z, ABSENT. Two protected tickets present.
- My re-run of `r20_prodjourney_check_v2.py` (blob 9ff30a5d38, the signed blob): self-test R20-PRODJOURNEY-SELFTEST-OK, live check RUN-OK (prodjourney). I read all three shots.
- Contrast of the confirmed line, my own measurement from the PNG: 10.10:1 (ink 209,212,217 on 25,38,67; matches TV2's 10.1). Gate 4.5.
- Not claimed: AC2J (the judgment half) is the CVO's to grade; email delivery (WE_DL_UNCONFIGURED reads as designed); Meeting flow for a real coordinator address.

## Trade Request -- FILES on PROD with its attachment; the byte read-back is UNPROVEN (measured, exercised three times)
Run: TO-R20-PROD3 by 0.7.0_AE_CloudOps~TV2, ledger tckt-vnext-r20-prod3-20261019 CLOSED 22:57Z, three attempts (20:37Z, 21:23Z, 22:52Z), one synthetic internal filer per attempt, firm cottonwood, one invented 31-byte .csv.
- MEASURED, all three attempts: the New Ticket list on PROD lists Trade Request; the upload door answered 200, the PUT to the presigned URL 200, the ticket create 201 (TCK-20261019-2d6d1a25, -b931d737, -814ee603); the object sat under s3://opal-data-cottonwood/portal/cottonwood/state/ticket_attachments/trade-form/. No engine call. Each ticket and filer row was deleted by key and read ABSENT (attempt 1 at 20:45Z, attempt 2 after its token, attempt 3 at 22:55:23Z).
- MEASURED (attempt 3): the Open route answered 200 and its body's key names are [expires_in, filename, url]; the page's own GET to the object went through (the browser read it).
- NOT PROVEN: the SHA-256 of the bytes read back equal to the file uploaded, end to end on a live ticket. Attempts 1 and 2 stopped on the applier script's own fetch and parse; attempt 3 stopped because the script's page listener ran after its wait loop ended (TV2's row TCKT_VNEXT-D2-S64, cause untested). Before attempt 3, TV2's fixed parser read all four stubbed body shapes and a read-only GET of attempt 1's object at its version returned 31 bytes with the equal SHA-256. The CTO ruled no fourth attempt (msg 11040): the ledger closed read-back UNPROVEN with the Open route's 200 as the evidence.
- RESIDUE (the CTO's ruling msg 11005, option b): THREE 31-byte synthetic objects remain, keys and versions in the ledger's V1 and D1 legs, because the applier's s3:DeleteObject is explicitly denied (cloudops-dell-agent-deploy-policy). The delete-by-version is an act for Andrew (CTO row 6e7c). Reachable from no ticket.
- The order TO-R20-PROD3 is not complete: its check r20_tradejourney_check.py (blob c221efcf2b) has no result file and reads RUN-BAD; the order is closed by the CTO's ruling, not graded RUN-OK.
- NOT CLAIMED: that a Trade Request ticket's attachment opens end to end for a real filer (the page's own GET went through once, unverified byte for byte); the S3 role policy's resource list was not read, but the PUT succeeded under it.

## Trade Request byte read-back -- PROVEN on PROD (round 21, `TO-R21-RB1`, 2026-10-20 15:45Z to 15:48Z; added 16:0xZ)
- MEASURED, ONE attempt by TV2, ticket `TCK-20261020-645d7017`, filer `tckt-r21-trade-filer-20261020@opal.invalid`, firm cottonwood, one invented 31-byte `.csv`: door 200, PUT 200, ticket 201; the Open route 200 with body key names `[expires_in, filename, url]`; the `url` downloaded with a plain GET (the response listener registered BEFORE the press); **the SHA-256 of the bytes read back `b0b2b41f...73455` equals the SHA-256 uploaded**. Ticket and filer row deleted by key 15:48:07Z (after the token's `exp` 15:48:02Z) and read ABSENT.
- The issuer's re-run of `r21_tradejourney_check.py` (blob `9167d289eb`): self-test `R21-TRADEJOURNEY-SELFTEST-OK`, live `RUN-OK (tradejourney)`; the issuer read both shots (`prod_trade_form_filled`: the placeholder form, firm Cottonwood Capital Advisors, the file chosen; `prod_trade_filed`: the board row "Trade Request ... Trade request: Cottonwood Capital Advisors", open, with "Claim", "Open form" and "Complete").
- RESIDUE: FOUR 31-byte synthetic objects (three from round 20, the fourth version `lway93Q_YhLuvb25e3M__smeGKeFABbC`), keys and versions in the result `residue` and the ledger; the delete stays denied for the applier (CTO ruling msg 11005) and joins row 6e7c for Andrew.
- So the round-20 "NOT PROVEN" line above is superseded for the read-back: the Trade attachment bytes read back equal on PROD. Still not claimed: a real (non-synthetic) filer's attachment, the organic arm (Andrew opening a real Trade attachment); no engine call was made (unwired).

## Open
- CVO grade of R20PROD2-AC2J; L8 part 5; then the L10 slug (after every order of the round is terminal and every row dispositioned).
- FWD-11 on PROD (due 2026-10-24): Meeting is RUN-OK; Trade files with its attachment on PROD but its byte read-back is UNPROVEN and closed so by the CTO's ruling. Rows S62, S63, S64 (TV2) and the residue deletion (Andrew) stay open.
