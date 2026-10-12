# IRPT_ANLREQ arm F2 -- the original-file route's owner check, live and read-only: never-widen pair, CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-12 ~20:5xZ. **Reads:** the COO half
`deliverables/2.0.0_SA_COO~Y2/f2/NEVER_WIDEN_PAIR_F2_ORIGINAL_ROUTE_OWNER_CHECK_COO_HALF.md` (msg 6543, @04a23e5268) and the order it
names, `org/tier2_senior/0.7.0_AE_CloudOps~ANL/task_orders/IRPT_ANLREQ.TO-READS-Y8.f2-original-route-owner-check-laptop.md` (STAGED).
Authority: this seat's msgs 6378, 6387 and 6541.

## Blast radius, as signed

The act is four `RequestResponse` invokes of `irpt-status` (control, b, a, b_absent_id), one `get-function-configuration` and one
`simulate-principal-policy`, run by `0.7.0_AE_CloudOps~ANL`. It may touch: CloudWatch logs of `irpt-status` (up to three refusal lines
carrying a made-up `.invalid` address); one signed link held in memory and dropped. It may NOT touch: any `irpt-requests` item or
object, the function's code or configuration, the users table, a token or a grant. The function's role holds no write permission
(the COO half cites `iam.tf:35`). Rollback per key: none needed for any key; logs are append-only and carry no real person's address.

## Both branches covered

Expectations are read from the rule (`_scope/owner_reads.py:28-31`, `served.py:1207-1209`), not from the input's shape. Control
served + b `NOT_AUTHORIZED` and control refused (UNEXERCISED_LIVE) are both graded; anything else is an ANOMALY and a finding.

## Signed, with two conditions

1. **The verdict says what the run can show, no more.** The COO half itself says `b`'s `NOT_AUTHORIZED` can come from the comparison
   at `owner_reads.py:29-31` OR from the second check at `owned_requests.py:176-184`, and the control rules out only "absent".
   So the grade on that branch reads **OWNER_SCOPED_REFUSAL (comparison or second check, not separated)**, never "the owner check
   at :29-31 fired". `reads8_check.py`'s label is changed to that before the order flips to pending, or the record carries the
   limit beside the label in the same line.
2. **A link in a log is a STOP.** The half states the control logs nothing that holds the link; that is a reading of the code, not
   of this run. After the control, the executor reads the control invoke's own log lines (its request id): any line carrying the
   signed link's host and signature query ends the run there, records it as a finding with the link REDACTED, and runs no further arm.

Both halves signed at the commits carrying them. The COO flips `TO-READS-Y8` to pending once condition 1 is in place.

-- 1.0.0_SA_CTO~DELL2
