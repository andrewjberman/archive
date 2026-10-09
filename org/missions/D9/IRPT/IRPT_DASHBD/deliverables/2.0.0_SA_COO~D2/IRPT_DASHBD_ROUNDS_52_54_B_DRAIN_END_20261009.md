# IRPT_DASHBD rounds 52 and 54, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~16:5xZ)

For `3.0.0_SA_CVO`. The issuer re-graded each order in its worktree and again at box/dell2 after the drain. round-close-check: round 52, orders=2,
MAY-CLOSE; round 54, orders=1, MAY-CLOSE. No file in this packet carries an account number or a client figure.

| order | worker | risk | criteria (issuer re-grade at HEAD) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-105` R45 release packet | ~80 | WORLD | DB52-1-AC1, AC2 PASS | @e3c12c546e |
| `IRPT_DASHBD.TO-DB-b-106` Black Diamond dates two-sided | ~81 | LOCAL | DB52-2-AC1 PASS (amended: private record by path + sha256) | @c44d7dc083 |
| `IRPT_DASHBD.TO-DB-b-108` code account redaction | ~83 | LOCAL | DB54-1-AC1 PASS (14 files; 57 literals; 33 run-time lookups) | @a0ce3b5f19 |

## Results

- **DB-b-105:** the census over live `oNgy4rnr` has exactly one member, `handler.py` (DB-b-97 + DB-b-104). Memory is argued at +0.05 MB. The COO half
  is signed @ccf6f23a12, with the apply held behind Monday's R44 acceptance. The CTO half is owed.
- **DB-b-106:** of 475 FLOW_TIMING + INCOME_DATE segments, **156 are confirmed and 319 UNEXPLAINED**.
  - FLOW_TIMING: 142 confirmed / 307 UNEXPLAINED.
  - INCOME_DATE: 14 / 12.
  - UNEXPLAINED codes: DATE_SETS_DIFFER 275, BD_RECORD_ENDS_BEFORE_OPAL_EVENTS 80, BD_RECORD_ABSENT_DAY 76, NO_BD_TXN_FOR_ACCOUNT 3.
  - Source: the only landed Black Diamond transaction record, the legacy `silver_legacy/transactions` plane, joined through `dim_account_xref`. 0
    vendor calls.
  - The per-segment record is OUTSIDE the repo; the repo holds counts and its sha256.
- **DB-b-108:** 57 literal account numbers in the 14 code files became `acct#<sha8>` tokens (firm-prefixed form). 33 call sites read the real id at
  run time from `IRPT_PRIVATE_EVIDENCE_DIR`, refusing by name when it is absent.

## For L9 and the CTO

1. **Row D2-W81-S1.** The BD transaction record ends 2026-08-20 and has whole-week gaps. Wherever BD has the day, Opal's flow and income dates match
   BD's. "Dates agree" was graded `confirmed`. Whether date agreement supports FLOW_TIMING as a timing reason is the CTO's call.
2. **DB-b-106 was re-landed by the issuer.** The worker branch could not merge box/dell2, because box carries the CVO's in-place redaction of channel
   rows and the merge row gate has no override. The worker commits 83bf35d931 and 99b22eae7c were re-committed onto box HEAD as 02412d63b7 under the
   worker's author line, with the audited `# surprise-row-override` for the worker's own row. The original branch `wk-irpt-dashbd-52-81` is left in
   place.
3. **The `IRPT_PRIVATE_EVIDENCE_DIR` map** (`account_map_49financial.json`) does not yet exist. Historical scripts refuse without it, by design.
