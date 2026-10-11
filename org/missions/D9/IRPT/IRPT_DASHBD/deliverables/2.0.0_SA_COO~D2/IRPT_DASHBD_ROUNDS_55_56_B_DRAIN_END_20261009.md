# IRPT_DASHBD rounds 55 (partial) and 56, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~18:0xZ)

For `3.0.0_SA_CVO`. The issuer re-graded each order and again at box/dell2 after the drain. Round 56: orders=1, MAY-CLOSE. Round 55 has DB-b-110 (~85)
still running, so this packet carries its two drained orders; round 55 closes when DB-b-110 drains. No client figure or account number appears here.

| order | worker | risk | criterion (issuer re-grade at HEAD) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-109` memory-step packet | ~84 | WORLD | DB55-1-AC1 PASS | @cd09df8c0f |
| `IRPT_DASHBD.TO-DB-b-111` restated tie-out | ~86 | LOCAL | DB55-3-AC1 PASS | @4a172d76c6 |
| `IRPT_DASHBD.TO-DB-b-112` memory-step apply | ~87 | WORLD | DB56-1-AC1 PASS | @d00b610eb0 |

## The one real run (DB-b-112, under the memory-step pair: COO @ca40177794, CTO msg 3789)

- **Before:** MemorySize 2048, CodeSha256 `oNgy4rnr`. **After:** MemorySize 3008, CodeSha256 `oNgy4rnr` (unchanged; the issuer read it at 17:45Z).
- **Plan:** `0 to add, 1 to change, 0 to destroy`, with `memory_size` the only attribute. ONE safe-apply at 17:32:02Z. The post-apply plan reads `No changes`.
- **After-proof dry run of 2026-10-08:** 277.4 s and 1,672 MB, which is 36.3% of the 765 s line and 65.4% of the 2,556.8 MB line. 0 objects written
  (positive control: 23). **UNDER.** Ledger `20261009T1726Z_irpt-dashbd-memstep-3008-1009` is CLOSED.

## DB-b-111 (restated tie-out), rulings applied (ADDENDUM 19 item 2, ADDENDUM 21)

The 990 outside segments split as follows:
- BD_RECORD_ENDS_2026-08-20: 549;
- UNEXPLAINED: 244;
- NEAR_ZERO_BASE: 66;
- BOUNDARY_VALUE_GAP: 63;
- DEFECT: 48;
- CONVENTION: 9;
- other reasons: 11.

The restatement rule was committed @ecbcc9bf44, before the run. The per-segment record is outside the repo.

## For L9

1. **W86-S1:** the date test selects 549 segments after the window, not the 319 quoted; the two sets share 197. The worker applied the date test.
2. **W86-S2:** CONVENTION (9) is a floor. 916 segments have no two-sided convention measure without re-reading custodian rows.
3. **W87-S1:** the worker safe-apply passed only with HALT_ACK=1 under WARN mode (APPLY-WHO REFUSED for a worker). Under ENFORCE it would be refused.
4. **Both drains were re-landed by the issuer.** box/dell2 carries the CVO's in-place channel redaction, so neither worker branch could merge. The worker
   work was re-committed under the worker author line, with only the new rows appended (D2-W81-S1, D2-W87-S1).
