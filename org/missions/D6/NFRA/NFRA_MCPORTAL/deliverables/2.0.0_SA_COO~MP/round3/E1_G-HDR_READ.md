# NFRA_MCPORTAL round 3 -- E1, the G-HDR read (R-7), `2.0.0_SA_COO~MP`

**archetype:** VALIDATE

Read 2026-09-28 ~20:2xZ over SSM `AWS-RunShellScript` on `i-07dccb1615503ac99`, command id
`93a7fd46-fe48-4b1f-a1f7-9640c1bf6d94`, status `Success`. Read-only. `oid`/`sub` values redacted on the host by `sed`
before the output left it (the line carries keys only, so nothing was redacted).

## Denominators printed beside the read

| probe | value |
|---|---|
| `journalctl --list-boots` rows | 4 |
| first `opal-gateway` journal entry | 2026-08-15T03:02:10+0000 |
| `opal-gateway` journal lines (control) | 552671 |
| `Started ` lines in the unit | 373 |
| `OWNER-HEADER-CLAIMS` lines | **1** |

## The line (keys only)

```
2026-09-28T14:59:58+0000 ... uvicorn[369668]: OWNER-HEADER-CLAIMS keys=email,exp,family_name,given_name,iss,name,picture,sub
```

## Branch picked (MP-a-1 step 1, round-1 R-2)

- G-HDR: **DONE**. The line exists (matches Andrew's "Done." at ~15:2xZ,
  `org/tier1_exec/2.0.0_SA_COO~O/ANDREW_DIRECT_20260928_152xZ_NFRA_GATES_ANSWERED.md` row 5).
- `oid` ABSENT, `sub` PRESENT -> `MCPORTAL_OWNER_KEY_CLAIM=sub`. The key value is Andrew's own
  `/api/admin/whoami` `sub` (runbook `ANDREW_SWITCHOVER_RUNBOOK.md` step 7). It is NOT yet supplied.
- `iat` ABSENT, `exp` PRESENT -> the header's lifetime comes from `exp`.
- Both absences trigger **G-C4**: the CTO's C4 wording addendum (C4 at `prd/NFRA_MCPORTAL_PRD.md:203-207` names
  "Andrew's Entra object id" and "a header older than a short window") signed by `3.0.0_SA_CVO~O` before the apply.
  `prd-signoff.py status` at this read: ratified-text SIGNED current at v0.2 @87b310f4c2, i.e. BEFORE any addendum.
- G-PYPI: **GIVEN** ("Go ahead.", same record, row 6). The fetch has not happened, so the word still covers it.

## What MP-a-1's spawn waits on

1. G-C4 signed (the CTO, then `3.0.0_SA_CVO~O`).
2. Andrew's `sub` value, given to the issuer off-repo (one card).
