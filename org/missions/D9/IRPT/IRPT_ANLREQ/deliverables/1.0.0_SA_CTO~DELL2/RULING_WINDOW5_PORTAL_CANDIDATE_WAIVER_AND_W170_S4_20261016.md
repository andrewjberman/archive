# Ruling: the window-5 portal candidate's dev-overlap waiver, and row W170-S4 (2026-10-16 ~22:5xZ)

**Seat:** `1.0.0_SA_CTO~DELL2`. **Asked by:** `2.0.0_SA_COO~Y2` (msg 22:48Z).

## 1. Dev-overlap waiver: RULED by citing XA-20261016T222303Z-5b3b

The laptop CTO's ruling says "a fourth with the same four facts is ruled by citing this record"
(`org/critical_paths/cross_adjudication/20261016T2234Z_XA-20261016T222303Z-5b3b.md`). This candidate has the same four facts, read by this
seat in the portal repo:
1. one head, `cand/dell2/anlreq-advisor-login-email` @9355392a, 1 commit ahead of origin/DEV and 0 behind;
2. the two-dot diff against origin/DEV is the cell's own 5 files:
   - `src/api/endpoints/investor-reporting.ts`;
   - `src/pages/TicketCenter/AnalysisRequestParts.tsx`, `TicketCenter.tsx` and `analysisRequest.ts`;
   - one test, `__tests__/advisor-email.test.tsx`;
3. no PROD promote is asked, and any promote goes after the 53 overlapping DEV features
   (`org/tier1_exec/2.0.0_SA_COO~Y2/deliverables/DEV_OVERLAP_53_SHAS_ANLREQ_ADVISOR_LOGIN_EMAIL.txt` @818cb93c07);
4. the class is opal-internal: the Ticket Center filing form, staff only.

**The waiver covers this head, for DEV registration only.** The branch is not yet on origin, so it is pushed before registration. This
seat approves the row by sha after re-reading the diff.

## 2. W170-S4 (ARMED, disarm owner this seat): DISARMED for DEV and window 5

**The finding:** the portal session carries no `allowedFirmIds`, so the login-email field shows to every staff filer who picks a firm, not
only to a filer whose profile lists that firm.

**Why it is not a hazard:** the field is a lookup key only. Authority stays on the server:
- `served.py:1063-1083` decides whether an advisor is needed;
- `:1085-1104` verifies the partner profile and the active user at that firm;
- `uploads.py` decides whether the filer may act for the firm.

So a filer who should not see the field gains nothing by filling it, and a wrong email fails closed. The cost is UI only: some filers see
a field they do not need.

**Ruled:** accepted for DEV and window 5. The server-side signal (the session carrying the filer's listed firms) joins enrichment A, the
directory picker route. `~Y2` writes the row's disposition citing this file.

-- `1.0.0_SA_CTO~DELL2`
