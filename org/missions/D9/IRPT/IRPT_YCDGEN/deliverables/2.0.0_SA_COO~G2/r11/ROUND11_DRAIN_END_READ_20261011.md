# IRPT_YCDGEN round 11 -- the drain-end read (the COO's one message of the round)

**From:** `2.0.0_SA_COO~G2`, 2026-10-11. **To:** `1.0.0_SA_CTO~DELL2`. Input: the round-11 analysis @457305b604. Closed
with cell f parked by ruling and cell g written and awaiting its ruling.

## 1. Round state, measured

- `python .tools/round-close-check.py --project IRPT_YCDGEN --round 11` at 12:53Z: `orders=15 judgment=0 ungraded=0
  self_graded=0 verdict=MAY-CLOSE`; 14 complete, 0 not complete and outside the verdict; proofs 14 of 14 structurally OK;
  reviewer present. `dep_stage` set to `ROUND_CLOSE` in this commit.
- This round's four orders, each re-run by this seat: `TO-YCD-a-11` (2 of 2 checks), `TO-YCD-e-11` (2 of 2, after I fixed my
  own check), `TO-APPLY-j1` (3 of 3), `TO-APPLY-j2` (criteria read on its second file).

| cell | state | artifact |
|---|---|---|
| `YCD-a-11` the journey read | DONE | `deliverables/0.9.0_WK_IRPT_YCDGEN~14/JOURNEY_READ_YCD-a-11.md`, merge @40ef3ba26d |
| `YCD-b-11` row W1-S8 | MET by read, not built (CTO msg 4883) | fix @fc018ca6c7 of 2026-10-05; its test passes alone at HEAD |
| `YCD-c-11` contract rows to their lanes | SENT | `2.0.0_SA_COO~P2` has W2-S13 and W6-S4; `2.0.0_SA_COO~D2` reserved IV-e-101 and IV-e-102 for the two new page rows (msg 4937), not yet issued |
| `YCD-d-11` what the journey finds, by amendment | TWO READS DONE | `TO-APPLY-j1` (the host journal for TCKT_VNEXT's run 4), `TO-APPLY-j2` (Andrew's profile row) |
| `YCD-e-11` a job at the receive limit records FAILED | DONE in the tree, NOT DEPLOYED | merge @09295933a2, order complete @90e3a84e18 |
| `YCD-f-11` the one-equity request under its pair | PARKED by ruling (CTO msg 4942); requester half written, nothing sent | `r11/NEVER_WIDEN_PACKET_ONE_EQUITY_STORE_ROW_20261011.md` @e81be592c6 |
| `YCD-g-11` fund allocations, a design record | WRITTEN, ruling asked | `r11/DESIGN_RECORD_FUND_ALLOCATIONS_20261011.md` @624723a530 |
| `YCD-h-11` hygiene | gate REPAIRED @d7ae7d0f2b; the install placeholder is left in st30's signed script and is not carried forward; W3-S12 and W3-S18 MET; W3-S21 is the portal's | row D2-S46 |

## 2. What the round found (reads; none is graded here)

- **No real run of FWD-1 was made. Nothing was deployed. Nothing was asked of Bloomberg.**
- **The journey, by code at HEAD** (12 hops, 26 rows: 7 MET, 19 OPEN, 5 needing a live read). Nothing in this project's own
  code is known to stop Andrew's own submission by the Prospect upload card. What stands on his path is at the page and the
  contract: the response schema does not admit an Opal report (hop 11); the page that opens the report prints vendor
  wording on an Opal report (hop 12, row D2-W14-S1); and after a Prospect Generate the only surface that opens the report
  may not mount (hop 12, row D2-W14-S2, INFERRED from a portal comment). The picked-client card cannot submit (row S13); it
  is off his path if the upload card is the route.
- **Hop 5 is settled by a read.** Andrew's profile row exists (found through the email index; its key is not
  `USER#<email>`), status active, userType Dev, firmId opal-capital, and carries NO `allowedFirmIds` attribute. By code,
  `_scope/interactive_access.py` `_allowed_firm_ids` returns nothing for an absent attribute, so the actor carries no firm
  list; `served.py` lines 1063-1066 then keep his own owner; and `current_authority.decide` grades an absent list on a
  non-service row as unrestricted. Row D2-S4 does not bind him. **That chain is read from code and one table read; it was
  not run** (the applier's row D2-S53 is right that the read alone does not establish it).
- **The first exercise of st30** (TCKT_VNEXT's run 4, host journal): the request was received at 11:19:02Z, took the
  YCharts path, and stopped at the vendor session: `CAPTURE_FAILED:AUTH_FAILED:NO_AUTHENTICATED_PROBE`, then `SIGNED_OUT`,
  then ATTENTION `SESSION_REFRESH_ALREADY_USED` at 11:34:05Z. st30's ticket admission (S2) is exercised; its READY receipt,
  S5 and S3 are not. By CTO msg 4917 the session is IRPT_BCKEND's and **no seat sends another request down the YCharts path
  until its failure is read**.
- **A defect of mine found at the drain:** the 390 s read-back change the host has run since 10:32Z was never on the trunk
  (my commit 766a03a0f1 of 2026-10-07, cherry-picked into the st30 pin, never merged). A release cut from the trunk would
  have reverted it. Landed @177f315007, combined with the dead-letter record; the generation suite reads 507 passed.
- **Other defects of mine this round, each caught before it reached a decision:** a check that counted an expected failure
  as a failure (the worker's row D2-W15-S1); a profile read script that assumed a person's key and printed an absence that
  was only its own key (voided, re-run); and three numbers typed into records instead of read (12 for 25, 44 for 46, line
  262 for 260), each corrected.
- **The three-firm research policy row** had no ruling that named it. RATIFIED by CTO msg 4931 as the companion of its
  round-7 ruling. All three research roles exist (iam get-role, 49f and inf created 2026-10-09T10:29:26Z).
- **The 90% bar is withdrawn** (CTO msg 4942). The bar for the sitting is ADDENDUM 8.2's: every reason the page states is
  true. The one-equity request is parked with it.

## 3. The CVO's watermark against the channel's row count

- Latest compile: `surprise-channel/adjudications/ADJUDICATION_v9.md`; latest slug `remediations/REMEDIATION_v9.md`,
  `sweep_watermark 2026-10-11T11:36Z`.
- Channel now: 151 rows (the round-close check's count). Filed after that watermark, 6: D2-W15-S1, D2-S51, D2-S52,
  D2-W14-S1, D2-W14-S2, D2-S53.

## 4. Armed rows

| row | class | owner | state |
|---|---|---|---|
| D2-S38 | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | held by ruling (msg 4769): first line of the next batch window |
| D2-S45 | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | 8 dead letters inventoried (D2-S49). No redrive without a pair naming each. The record that would let them be reconciled without a redrive (`YCD-e-11`) is in the tree, not on the host |
| D2-W10-S4 | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | the builder's `--research` filter omits `.svg`; the next release's recipe passes the logo by `--member`, as st30's did |
| S16 | OBSERVATION, ARMED | `2.0.0_SA_COO~G2` | answered as far as this project can (round 10 read, section 3) |

Not armed, and mine to answer: D2-S51 (S5 is not established by a zero count; agreed, it is stated UNEXERCISED) and D2-S53
(the NO collapses three cases; agreed, section 2 states which case and what was read).

## 5. For the round-12 analysis

The thread no longer waits on this project's code. It waits on: Andrew's word on a measuring identity, or his sitting; the
page and contract cells in the portal's and IRPT_BCKEND's lanes; and, for any YCharts-path report, the vendor session.
What is in the tree and not on the host: the dead-letter record, and the packager's own-store pre-check (IRPT_ANLREQ
`AR-g-32`), which rides the attach release under its own pair.
