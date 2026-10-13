# AMGT_HARVST round 84 -- the drain-end packet to the CVO (`2.0.0_SA_COO~W1`, 2026-10-13 ~21:1xZ)

Round 84 has six orders, all terminal. `round-close-check.py --project AMGT_HARVST --round 84` reads `orders=6 ... 5 complete, 0 not complete and outside the verdict ... verdict=MAY-CLOSE`
(six orders: bz-3, bz-4, bz-5, bz-6, bz-7, bz-8; the five complete are all but bz-7, which is CANCELLED). No order of the round is open. No ledger of the round is open.

## Orders and what each one's own criteria read

| order | executes | status | criteria |
|---|---|---|---|
| bz-3 | worker `~138` | complete | AC1 7 passed, AC2 61 passed; merged `995adcaeaa` under COO `4ed2d30312` and CTO `42064bd87b` |
| bz-4 | `~ZW` | complete | AC1-AC3 PASS (windowless runner, `pythonw`, no `conhost` child); ledger CLOSED |
| bz-5 | `~ZW` | complete | AC1 PASS: `CYCLE=20261013T080909Z STOPPED=bot_check FAILED=1 NAMED=1` @5142731071; read again by me on the committed record, prior record as control. The cycle did NOT complete |
| bz-6 | `~ZW` | complete | AC1/AC2 PASS under the amended invocation (@f11e5a062f; `~ZW` @53aa581851): `VALID=True` for wsj and barrons; `VALID` is a local predicate |
| bz-7 | `~ZW` | **CANCELLED, NOT MET** | AC1 did not match: wsj `sign_in_refused` after 35 pairs / 69 min, barrons `sign_in_refused` after 0 pairs / 21 s. CTO msg 5143 carries it |
| bz-8 | `~HV1` | complete | AC1-AC3 PASS: `astn-wsjft-3am-run` DISABLED, expression unchanged, source DISABLED (drain `57c79777e7`); applied 0/3/0 under a re-signed pair |

## Rows for your compile (watermark of your last compile: v78, 2026-10-13T19:45Z)

- `AMGT_HARVST-Z-S119` (BLOCKING / INERT, my disarm_owner): after bz-6 both sessions read `VALID=True` yet both publishers' next cycle ended `sign_in_refused`. CTO ruling (A), next round: the runner refreshes once
  per publisher per cycle through the existing `SessionManager`, Barron's refusal class printed first. My word: the row is carried by that cell, not answered.
- `AMGT_HARVST-D1-S14` (BLOCKING / INERT, my disarm_owner, filed by `~HV1`): bz-8's targeted plan read 0/3/0, not 0/1/0 (a `-target` plan pulls the schedule's dependencies and their pending diffs). The seat stopped; nothing was applied. Answered
  by the re-signed pair. My word: the plan-reading defect was in the blast radius I signed (N=1 writers of the property, not the dependency pull).
- `AMGT_HARVST-D1-S15` (OBSERVATION / INERT, my disarm_owner, filed by `~HV1`): the signed apply STARTED the stopped instance `i-059405dfefcb4b44a`; both halves had said it would not. Names-only process read: no python, node, chrome, Xvfb or run.py. UPDATE ~21:1xZ: stopped on
  Andrew's word (CTO ADDENDUM 3, dfecbbe7d4) by `~HV1`: one `stop-instances` at 21:04:03Z, `describe-instances` read `stopped` at 21:04:28Z, and I re-read it `stopped` (user initiated) after; both bz-8 ledgers CLOSED; drain `af4002d649`.
- Earlier rows already read: `Z-S118` dismissed by you (v78); `D1-W135-S2` disarmed (f1cbe20bb6); `Z-S115` disarmed; `Z-S116`, `Z-S117` answered. `D1-S13` (07:30Z, a CRLF on one tracked file in the shared tree) is listed in case v76 to v78 did not read it.

## What I did NOT verify

- Whether the 07:00Z fire does not run: to be read after 07:00Z (the Lambda `Invocations` metric for that window).
- That any WSJ or Barron's session survives a cycle (bz-7 is NOT MET).
- Site Z is not readable from dell1: bz-4, bz-5, bz-6, bz-7 evidence is `~ZW`'s, committed on `box/sitez` and read here from those commits.

## For the CTO's round-84 analysis (not for grading here)

The FWD board (denominator 18; last full board 8 of 17 at round 49) is a grading act. Inputs: the PRD ENDPOINT section `org/missions/D5/AMGT/AMGT_HARVST/prd/AMGT_HARVST_PRD.md` (v0.22), the round-83 and round-84 evidence above, and the staged
enrichment item `deliverables/2.0.0_SA_COO_W1/staged/ENRICHMENT_ITEM_ARTICLE_LINK_VIEW_20261013.md` (F3 of the servable-prefix list). Pivot packet O4 items closed this session: bo-1, bp-1 cancelled; the bs-3 ledger closed.

Push state: every commit named here is LOCAL on `box/dell1`; `box-sync` carries it.
