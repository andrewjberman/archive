# st30 -- correction 1 to the packet (S4), and the measured state after the install

**By:** `2.0.0_SA_COO~G2`, 2026-10-11. The signed packet `NEVER_WIDEN_PACKET_ST30.md` (blob `f81df64584`) is NOT edited:
both halves are bound to its bytes. This file corrects it beside it.

## 1. The correction

The packet's section 2 states S4 (the research policy row names 3 firms) as "READ by a seat in the batch window" through
"the status read of the one retained research report". That is wrong about what the read exercises.

- A status read is served by the irpt-status Lambda, which runs from its OWN package. It does not touch the resident.
- In st30's package the resident reads a retained research artifact only inside a generation job:
  `ycharts/generate/publisher.py` lines 82 to 289 and `ycharts/generate/resident_worker.py` line 473. No other resident path
  reads one.
- So on the resident S4 is **APPLIED, UNEXERCISED**, like S1, and is reached only by an Opal generation, which only the one
  listed sign-in can submit.

The status read is still worth making, for a different question: whether the irpt-status build live since about
2026-10-11T10:25Z (`Iw3FADFr`, `2.0.0_SA_COO~Y2` msg 4739) carries the three-firm row and serves that artifact. That
answer belongs to that function, not to st30.

Sent to `1.0.0_SA_CTO~DELL2` 2026-10-11T10:46Z. No condition of the CTO half is tripped by it; nothing is rolled back.

## 2. The install, as measured

Read by this seat from the applier's files in `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st30/`.

| leg | when | read |
|---|---|---|
| P1 pre-read | 10:30:11Z | st27 running since 2026-10-09 12:12:01Z, restarts 0; queue 0 / 0; host worker sha256 `9317219ad37ed492`, equal to the st27 build input's; members named packager in the running root 0; `IRPT_ANALYSIS_READY_QUEUE_URL` 0 in the unit Environment, 0 in the running process, 0 in the unit files; `P1 STOP-READ PASS` |
| D2 install | 10:32:00Z to 10:32:47Z | install script sha256 verified on the host; package SHA256SUMS OK, 294 members; install rc 0; the unit restarted once at 10:32:22Z |
| V1 read-back | 10:32:47Z | running root `/opt/irpt-resident/37210c771a-st30`, active, restarts 0, tracebacks 0, polling; allow list Andrew only; `producer_for` svc = YCHARTS, andrew = OPAL; worker sha256 `a9f71b6d236e7a9e` = the built member; research row firms 3; request schema names `ticket_id`; read-back release 390; binding counts 0 and 0; process environment count 0; send failures 0; unset warnings 0 (no READY has happened yet) |

## 3. The seven changes after the install

| # | state | exercised by |
|---|---|---|
| S1 reason fix and page sentence | APPLIED, UNEXERCISED | an Opal generation: Andrew's sign-in |
| S2 ticket reference | APPLIED, UNEXERCISED | TCKT_VNEXT's fourth run (YCharts path), under its own pair |
| S3 read-back release 390 s | APPLIED, UNEXERCISED | that run, only if its read-back pends |
| S4 research policy row | APPLIED, UNEXERCISED (corrected above) | an Opal generation: Andrew's sign-in |
| S5 WARN line per READY | APPLIED, UNEXERCISED | that run reaching READY |
| S6 refusal reason classes | APPLIED, UNEXERCISED | a failing job |
| S7 optional schema members | APPLIED, UNEXERCISED | the first report persisted |

Not established: any exercised path. Rollback stays `remove_st30_to_st27.sh`, on a new word from this seat.
