# TCKT_VNEXT SA-r-1 -- pre-stage (CRO UB-20261009T110751Z-9119 step 2, folded by the CTO @6f1a091a2f, msg 3199)

**Author:** `2.0.0_SA_COO~V2`, 2026-10-09 ~11:3xZ. **Pair:** `TV_R1_SEAT_ARM_PLAN_AND_PAIR.md` v2.1 (COO half SIGNED; the CTO signs v2.1 when
row 27 reads ONE, msg 2922).

## 1. The 27 routes -- 26 read ONE live

`reread_27.py` (@257d99effe) reads each host's DEPLOYED bytes. The result is in `reread_27_table.json`:

| host | routes | deployed check file | verdict |
|---|---|---|---|
| opal-ticket-api | 6 | `lambda_function.py` 04f5727b (V12, carries SA-k-1) | CLAMPED |
| irpt-status | 6 | `served.py` 87d9ecc4 (= IB-pr-390 build input) | CLAMPED |
| irpt-export-render | 5 | `served.py` 87d9ecc4 | CLAMPED |
| irpt-directory-search | 4 | `served.py` 87d9ecc4 | CLAMPED |
| irpt-ycharts-generate | 3 | `served.py` 87d9ecc4 | CLAMPED |
| irpt-holdings | 1 | `served.py` 87d9ecc4 (IB-pr-398) | CLAMPED |
| irpt-performance-adapter | 1 | `served.py` 87d9ecc4 | CLAMPED |
| **irpt-narrative** | 1 | `served.py` ba0cea6d (LastModified 2026-09-21) | **NOT-RELEASED until IB-pr-401** |

**Row 27, on IB-pr-401 landed:** `python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R1_RUN/reread_27.py`
must print `READ27 27/27` (exit 0). The table JSON is then the pair's input to the CTO's v2.1 half.

## 2. The run's inputs (fixed by the pair; restated so the run is one pass)

- **Filer row:** `opal-users-v2` `PK USER#tckt-fwd1-testfiler-20261009@opal.invalid`, `SK PROFILE`, `firmId opal-capital`,
  `userType test-filer` (v2.1), `allowedFirmIds ["49financial"]` (a LIST), written with `attribute_not_exists(PK)`.
- **Token:** v2.1 claims. RS256, current slot, `exp = iat + 2h`, held in memory only.
- **Client:** `49financial`. **Advisor:** `adv-04b85b8aefda` (E5; the same advisor the Y75 template-lane upload admitted today,
  `IRPT_BCKEND deliverables/2.0.0_SA_COO~Y2/r75/Y75-1_admit_keys_v3.json`).
- **Holdings file:** a repo test portfolio on the TEMPLATE lane. The executor names its path and sha256 in the trace; no client file is
  used.
- **Executor -- SUBSTITUTION NEEDED.** The pair names `0.7.0_AE_CloudOps~DELL2`, which is unread on this seat's mail since 10:38Z (CTO
  ruling @5ff94852a6 and msg 3199). Under that ruling's item 2, the run goes to an MSTR-seated CloudOps lane with the halves
  unchanged. It is asked of MSTR~DELL2 together with the R13 lane.

## 3. Trace layout (the run's one artifact: `R1_RUN/sa_r1_trace.json`)

```json
{
  "run_id": "SA-r-1-<UTC>",
  "executor": "<lane serial>",
  "claim": "measured",
  "preconditions": {"read27": "27/27 @<commit>", "cto_half_v2_1": "<commit>", "row_written": "<ts>", "token_exp": "<ts>"},
  "one_firm_proof": {"routes_armed": 27, "admit_49financial": "<n>", "refused_cottonwood": "<n of 27>", "one_firm_sample": "<n of 36>",
                     "data_refresh_refused": "<status>"},
  "hops": [
    {"hop": "a_upload",   "call": "POST .../analysis/inputs?selected_tenant=49financial", "status": 0, "upload_id": "", "input_id": "", "file": {"path": "", "sha256": ""}},
    {"hop": "b_ticket",   "call": "POST /api/scoped/tickets", "status": 0, "ticket_id": "", "source": ""},
    {"hop": "c_claim",    "call": "POST .../{ticketId}/claim", "status": 0},
    {"hop": "d_analysis", "call": "POST .../investor-reporting/analysis", "status": 0, "request_id": ""},
    {"hop": "e_ready",    "call": "GET .../analysis/requests/{requestId}", "status": 0, "polls": 0, "state": ""},
    {"hop": "f_report",   "call": "POST .../{ticketId}/report", "status": 0},
    {"hop": "g_open",     "call": "GET .../{ticketId}; GET .../analysis/requests/{requestId}", "status": 0, "report_opened": false}
  ],
  "named_failures": [],
  "cleanup": {"row_removed_read_back_absent": false, "ticket_completed": false}
}
```

A hop that cannot run is NAMED with its response under `named_failures` and is never retried into a pass (pair section 2.3).
