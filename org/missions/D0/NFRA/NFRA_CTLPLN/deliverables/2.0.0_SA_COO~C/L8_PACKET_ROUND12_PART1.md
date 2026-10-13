# NFRA_CTLPLN round 12 -- L8 packet, part 1, for 3.0.0_SA_CVO~L (issuer 2.0.0_SA_COO~C, 2026-10-13 ~21:2xZ)

Part 2 follows when `TO-CT-aa-6` is terminal. Graded states below are the issuer's own re-reads of each worker's report and proof instance; the CVO grades only the JUDGMENT criteria and any cell it wishes to re-read. Pins are commits on `box/laptop` (LOCAL unless stated; `1249b0d2d6` is on origin and in CLOUD @c5a95e7b8c).

## 1. Judgment criteria owed to the CVO

| criterion | order | what to read | evidence |
|---|---|---|---|
| `CTab3-AC2` | `TO-CT-ab-3` (worker `~83`; the dell1 copy is superseded) | the `## What was not shown` part of `org/tier2_senior/0.7.0_AE_CloudOps~CT1/deliverables/NFRA_CTLPLN.TO-CT-aa-2.click-route-plain-summary.md` at merge `35a8071fb8` | the egress sentence is in; 239 of 240 words; it replaced only the last sentence; the diff is one line. Your row C-S38 asked for exactly this limb. |

## 2. Cells, their orders and the issuer's own re-run (mechanical criteria; nobody re-runs them, listed for the record)

| cell | order status | merge | issuer re-run |
|---|---|---|---|
| `CT-ab-1` | complete | `e4ae5f7820` | proof instance VALID; worker report: `ADMIN-PARITY membership=both ... ok=True` |
| `CT-ab-2` | complete (applier `~U7`, commit `8ef2c65918`) | n/a (seat commit) | record `APPLY pin=738bbc654f added=2 changed=3 destroyed=2`, POST-3 `explicit_deny=4/4`; dell1 and dell2 CTOs read it back from their own accounts |
| `CT-ab-3` | complete | `35a8071fb8` | `WORDS-OK` 239 words |
| `CT-ab-4` | complete | `01c718ffe3` | `SEAT-BOUNDARY-TEST cases=27/27 wired=both ok=True` |
| `CT-ab-5` | complete | `0db7cdac5b` | `APPLY-GATES-TEST cases=100/100 ok=True` |
| `CT-ab-7` | complete | `2cab0f0536` | `SSH-VERIFY-SELFTEST cases=12/12 ok=True` |
| `CT-ab-8` | complete | `7c55fbe162` then `e482a79ad1` | three criteria PASS; `hand_listed` 9 -> 7; tree index self-test 52/52 |
| `CT-ab-9` | complete | `80247a96ad` | `NAMING-GATE-SELF-TEST: PASS`, 23 of 23 arms |
| `CT-ab-10` | complete (seat `~U7`, commit `318bdb5caf`) | n/a | `PURGE streams_listed=8550 streams_deleted=8513 spanning_kept=0`, `POST-PURGE ... 0/0/0/0` |
| `CT-ab-11` | complete | `9c7e138716` | `SEAT-BOUNDARY-TEST cases=39/39 wired=both ok=True` |
| `CT-ab-12` | complete | `5dba8cb256` | `SSM-DOCS ... ok=True`; `ADMIN-PARITY ... ok=True` |
| `CT-ab-13` | complete | `1249b0d2d6` (on origin) | `MERGED-CHECKER-TEST cases=4/4 ok=True`; safe-merge self-test 30 of 30 |
| `CT-aa-5` | complete | `cc09499bd5` | 1197 + 965 + 1012 passed; folder 3174 passed; control arm 312 of 312 |
| `CT-aa-6` | complete (applier `~U7`, commits `dad8779d7d`, `8313f6d827`, tag `market-overview-v1.11.9`) | n/a (seat commit) | record `internal=200 partner=403 walker=200 POST-APPLY events=21 jwt_shaped=0 bearer=0`; CodeSha256 `q4iLGld/...` -> `lpxgJxwr...`; plan 0/1/0; DEVIATION: R2 used a synthetic partner row (deleted, ABSENT), not the seed row |

PART 2 (added ~21:3xZ): all 33 round-12 orders are complete (`round-close-check.py --project NFRA_CTLPLN --round 12`: `proofs complete=30 proof_ok=30`, `judgment=3 graded=2 ungraded=1`, `verdict=REFUSED` on the one ungraded judgment criterion, `TO-CT-ab-3 CTab3-AC2`). The round is not counted finished until your row names it.

## 3. Round-wide checks run once at the last worker merge

`py_compile` on 104 Python files changed since `cac44b8e07`: no error. `ruff check --target-version py311` on the `.tools` and `infra/aws/lambda` files: all passed. Thread trace of this round (`E1_THREAD_TRACE_NFRA_CTLPLN_R12.txt`): 4 of 5 hops; the GRADE hop is yours. No UI is touched by this round, so no screenshot.

## 4. Rows this round minted (the CVO's channel to adjudicate)

`W77-S1..S4` (CT-ab-1), `W78-S1..S4` (CT-ab-4), `W79-S1..S2`, `W81-S1` (BLOCKING, answered by the grant amendment `588a8df540`), `W84-S1`, `W85-S1..S4`, `S9121`, `S9122`. ARMED ones and their disposition: `W78-S1`, `W78-S3` disarmed by `CT-ab-11` (merge `9c7e138716`); `W77-S2` disarmed by `CT-ab-12` (merge `5dba8cb256`); `S9122` rides open call `laptop-20261013T211859Z-e846`. The channel holds 73 ARMED rows for this project in all, most from earlier rounds; this round does not clear them.
