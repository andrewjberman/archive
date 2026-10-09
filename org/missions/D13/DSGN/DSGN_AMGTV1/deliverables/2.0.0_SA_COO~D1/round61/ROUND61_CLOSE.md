# DSGN_AMGTV1 round 61 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~10:1xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round60.md` @0b03adc339 section 3, items 1-4. Items 1-2 (repairs) are batched into one cell, so four items make three cells. |
| issuance | @c50860341b (+ line-ending fix @ffc8c87244); fan-out 3 of 3, cap 8 |
| orders | `TO-AV-zzm-1` -> ~131 (worker-light), drained @15ddfb11c5; `TO-AV-zzm-2` -> ~132 (worker), drained @01ccd374c0; `TO-AV-zzm-3` -> ~133 (worker-light), drained @b88e98a980. All three instances VALID (proof-of-spec-check rc=0). |
| checks | r61 3/3, r61b 3/3, r61c 3/3 (re-run by the issuer on each worker's tree and on both candidates); battery29 ALL PASS on both candidates (14 of 14 harnesses, tsc and eslint rc=0) |
| DEV | candidate `b3f1b54a` = DEV `d7427de7` + 3, APPROVED (`1.0.0_SA_CTO~DELL1` msg 2234); `0.0.0_AB_MSTR~DELL1` lands it, re-cut if DEV moved (DEV read `6d383958` at 10:0xZ) |
| PROD | candidate `90db1e84` = `fa5ba2af` + the same 3 SA-only commits. CTO half `ledger/NEVER_WIDEN_PORTAL_PROD_PROMOTE_90db1e84_CTO_HALF.md`, COO half beside it. |
| rows | `DSGN_AMGTV1-D1-S1` @647ffaac45: the gate refuses a CRLF re-write of a modified order. Workers ~131 and ~133 filed none. |
| round-close-check | `verdict=REFUSED`: the three AC3 judgment criteria are UNGRADED until the CVO grades them (L9) |

## The real run -- 09:50Z-09:58Z, signed-in, `dev:live` build of the DEV candidate's SA tree (portal `2a54cbd8` = e6fb269c + 3)

There were two walks. `tmp/ui-walk/20261009T095015Z` opened on the default Thesis tab. `tmp/ui-walk/20261009T095512Z` used a scratch,
reverted default-tab edit (`news`), because the walker does not press tabs on `/security-analysis`. Both walks covered AMD and Lenovo:
59 screenshots each, 0 API issues, 0 guard aborts. The walker disarmed and its login is refused (401).

| criterion | what the screenshots show |
|---|---|
| `TO-AV-zzm-1` AC3 | Lenovo 992 HK, Peers, "What is not on file" fold (`039-Lenovo-Peers-expanded`). The fold reads: "These peers report it with no stated currency, so the Average row shows no figure for Price (last)." The Average price cell is blank, and that line says why. The rename changed no assertion: `tabs.harness` went from 20 to 21 checks, one split into two. |
| `TO-AV-zzm-2` AC3 | AMD and Lenovo, News tab (`004-AMD-overlay`, `032-Lenovo-overlay`, second walk). The price line is drawn over the article bars on a right-hand axis (AMD 150-750, Lenovo 8-40), and "Price" is in the legend. Neither name lacks stored prices, so the "No price line" sentence was not seen on the page; it is covered by r61b arm 2. |
| `TO-AV-zzm-3` AC3 | AMD, News tab: the list opens on items mentioned 3, 3, 2, 2, 2, 2, 2, 1, 1, 1 times, each with "Mentioned N times". Lenovo: 5, 1, 1, 1, 1. |

## Carried to round 62 (CTO msg 2234)

- **The price line breaks at every day with no close** (weekends and holidays). On a nine-month spine it reads as dashes, not a line.
- **The right-hand price axis has no label;** the left one reads "Articles per day".
- **FWD-1:** Andrew's own signed-in walk on PROD (open-calls 2caa).

## After the close (10:1xZ)

- **L9:** 3.0.0_SA_CVO graded all three AC3 MET (`surprise-channel/adjudications/ADJUDICATION_v34.md`). `TO-AV-zzm-2` carries one branch:
  the next walk names a security with no stored prices. round-close-check reads `verdict=MAY-CLOSE` (3 of 3 graded).
- **Live:** portal DEV `9b06f6ed` (MSTR's re-cut of `b3f1b54a` onto `6d383958`) and PROD `90db1e84` (ls-remote read 10:12Z).
- **Round-62 prep:** `round62/PREP.md`, `round62/checks/r62.cjs`.
