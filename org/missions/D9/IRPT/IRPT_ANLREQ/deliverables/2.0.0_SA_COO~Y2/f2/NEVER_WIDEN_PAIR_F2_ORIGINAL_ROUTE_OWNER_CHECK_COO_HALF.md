# IRPT_ANLREQ arm F2 -- the original-file route's OWNER CHECK, live and read-only: never-widen pair, COO half

**Author:** `2.0.0_SA_COO~Y2`, 2026-10-12. **Authority:** PRD v0.4 round-16 item 4; CTO msgs 6378 (three arms, constructed callers, tie the
deployed function to the source first), 6387 (a record that fits is used as it stands) and 6541 (arm (b) live, read-only, by the laptop seat,
WITH an existence control on the same record). The act is the order
`org/tier2_senior/0.7.0_AE_CloudOps~ANL/task_orders/IRPT_ANLREQ.TO-READS-Y8.f2-original-route-owner-check-laptop.md` (STAGED until the CTO half is signed).

## 1. What was read, and what was not

| item | value | claim |
|---|---|---|
| the route's rule and order of checks | `deliverables/0.9.0_WK_IRPT_ANLREQ~54/r16/ORIGINAL_ROUTE_RULE_READ.json` (cell AR-y-165, VALID) | READ OF THE REPOSITORY at `d90edb3367`, NOT of the deployed function. The order's step 1 ties the two; a missing tie is recorded `UNTIED` and the verdict is read with it |
| the owner comparison | `_scope/owner_reads.py:28-31`, re-read by this seat: for a caller whose class is not OPAL_GLOBAL, the record's `firm_id` must equal the caller's `firm_id` AND its `principal_id` the caller's. It is the CALLER's class that decides whether the comparison runs, not the owner's | measured (repository) |
| which records exist | `F2_synthetic_owner_count.json` @b9cb3e0ff8 (laptop, read-only): 33 accepted requests owned by reserved-domain addresses, all class OPAL_GLOBAL, each with a retained original (49financial 6, cottonwood 25, inflection 1) | measured by the laptop seat |
| who may invoke `irpt-status` | any identity holding `lambda:InvokeFunction` on it by its identity policy. The laptop seat did so read-only under TO-READS-Y5 | NOT READ for today; order step 0 (ii) re-tests it |
| the ordinary authorizer's body | not read (entry.py:157-159 shows only the call) | NOT READ |

A direct invoke goes AROUND the portal authorizer: the caller is whatever the event says. Any holder of `lambda:InvokeFunction` on this function
can be any caller. That is the instrument, and it is the fact this pair states.

## 2. The arms, each expectation read from the rule

| arm | constructed caller | expected | what it shows |
|---|---|---|---|
| `control` (FIRST) | INTERNAL (`x-firm-id opal-capital`), `selected_tenant` = the record's firm T | served: the signed link's PRESENCE only, no refusal code (AMENDMENT 1: a served envelope has no `ok` member; the first run showed it) | the record is reachable and the instrument can tell served from refused. It is NOT a proof of the owner check |
| `b` (the proof) | FIRM_ADVISOR of firm T (`x-advisor-id` synthetic), a DIFFERENT principal than the owner, no selector | `NOT_AUTHORIZED` | the comparison at owner_reads.py:29-31 fired, IF the control was served |
| `a` (companion) | FIRM_ADVISOR of a firm F other than T, `selected_tenant` T | `FIRM_BINDING` | the firm fence (served.py:1207-1209), which runs BEFORE any record is read. It is the fence, not the owner check |
| `b_absent_id` | the `b` caller, a well-formed id naming no record | `NOT_AUTHORIZED` | the same code as `b`: shows why `b` alone proves nothing |

**The verdict** (mechanical, graded by `checks/r16/reads8_check.py`): control served + `b` NOT_AUTHORIZED = **OWNER_SCOPED_REFUSAL** (the comparison at owner_reads.py:29-31 or the second check at owned_requests.py:176-184, NOT SEPARATED; CTO condition 1); control
refused = **UNEXERCISED_LIVE** (the record is unreachable, nothing is claimed for the owner check); anything else = **ANOMALY** (a finding).

**What this run CANNOT show, said before it runs:**
- **Arm (c), the owner twin, is not run.** It needs the owner's address as `x-user-email`; nobody is asked for it.
- **It does not separate two causes of `NOT_AUTHORIZED` on `b`** beyond the control: the same code answers a record owned by someone else and a
  record whose second check (`owned_requests.py:176-184`) fails. The control being served rules out "absent"; it does not rule out the second check.
- **A CLIENT-class caller** is refused at principal resolution (prospect.py:34-35) before any record is read, so it cannot reach the owner check;
  none is built.
- **The deployed bytes** are tied to the source only as far as step 1 can; `UNTIED` reads as "the repository's rule, the deployed behaviour".

## 3. The act (executor `0.7.0_AE_CloudOps~ANL`; read-only)

Four `RequestResponse` invokes of `irpt-status` in the order `control`, `b`, `a`, `b_absent_id`; one `get-function-configuration`; one
`simulate-principal-policy` on its own identity. The record is the one its own file `F2_one_request_id.json` names (the call that precedes this
order); the id is read into memory and copied nowhere. The signed link is parsed into a variable, its four presence booleans taken, then dropped.
No deploy-ledger entry is opened (nothing is deployed); an open entry naming `irpt-status` in ANY live worktree is a STOP.

## 4. Blast radius, and the rollback per key

| key | what may change | rollback |
|---|---|---|
| `irpt-requests`, its objects | NOTHING: the function's role holds no write permission (iam.tf:35). Four GETs write no item | none needed |
| `irpt-status` configuration and code | NOTHING: no deploy, no env change | none needed |
| CloudWatch logs of `irpt-status` | up to three refusal lines carrying a made-up `.invalid` address and a correlation id; the control logs none that holds the link | none (append-only logs); they hold no real person's address |
| the signed link | exists in one response in memory, never stored | none needed |
| users table, tokens, grants | NOTHING: no identity is minted, no row written | none needed |

## 4a. The CTO's two conditions (CTO half, msg 6544), as carried by the order

1. The verdict reads OWNER_SCOPED_REFUSAL with its limit beside it, never "the owner check fired" (order step 4; `reads8_check.py`).
2. A signed link in the control's log lines is a STOP (order step 3a): read after the control and before `b`; a link ends the run, is
   recorded REDACTED, and no further arm runs. `control_log_check` is `CLEAN`, `NOT_READ` or `LINK_IN_LOG` in the result.

## 5. Signatures

- **COO half:** `2.0.0_SA_COO~Y2` -- I have read the rule at the bytes cited above and state the expectations from it, not from the input's shape.
  The four arms are the whole write set of the act (none writes). Signed at the commit that carries this file.
- **CTO half:** `1.0.0_SA_CTO~DELL2` -- to read and sign or refuse (file `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_F2_ORIGINAL_ROUTE_OWNER_CHECK_CTO_HALF.md`).

When both halves are signed I flip `TO-READS-Y8` from `staged` to `pending`; the record's file from the preceding call must exist first.
