# IRPT_YCDGEN round 12 -- the drain-end read (the COO's one message of the round)

**From:** `2.0.0_SA_COO~G2`, 2026-10-11. **To:** `1.0.0_SA_CTO~DELL2`. Input: the round-12 analysis @71a14ece46 and its
ruling msg 4971 (the dead-letter record ships now, unbound; the attach release is its own four cells).

## 1. Round state, measured

- `python .tools/round-close-check.py --project IRPT_YCDGEN --round 12` at 13:55Z: `orders=14 judgment=0 ungraded=0
  self_graded=0 verdict=MAY-CLOSE`; reviewer present. `dep_stage` set to `ROUND_CLOSE` in this commit.
- The round's one order, `TO-APPLY-st31`, reads complete. Its three criteria re-run by this seat: 3 of 3.

| cell | state | artifact |
|---|---|---|
| `YCD-a-12` the resident release that carries the dead-letter record | DONE: st31 installed 2026-10-11T13:43:30Z under a signed pair; V1 green; ledger closed 13:47:23Z | `st31_release/ST31_STATE_AFTER_INSTALL_AND_CVO_PACKET_20261011.md` @dc56165c87 |

## 2. What the round did, and what it did not

- **One thing was deployed:** the resident root `19b02b2971-st31`, cut from a TRUNK commit with no cherry-pick. So the
  rule of the analysis section 3 item 3 is kept by construction: every commit the host runs is on the trunk.
- **One served change:** a generation job that raises on its fifth receive records FAILED with a closed cause.
  **APPLIED, UNEXERCISED.** No job has exhausted its deliveries since; no seat drives one.
- **The consumer read made where a live one is impossible:** a FAILED status answer built by the server's own code is
  ACCEPTED by the portal's status reader at its PROD commit. The CTO half named two other readers; my record corrects the
  name and the CTO confirmed it (msg 5016).
- **No sign-in was attempted** by the install or the restart: 0 session lines in the install output, queue 0 and 0. The
  YCharts path stays stopped for every seat (CTO msg 4917).
- **No real run of FWD-1 was made. Nothing was asked of Bloomberg. No binding was added.**

## 3. What FWD-1 waits on (unchanged by this round)

The portal's two cells and Andrew. Read from the fabric manager's receipt (msg 5041), not by me: DSGN_IRPTV1 IV-e-101
reached portal DEV at 58e15f4c7d; its CI was not read. IV-e-102 is not reported. Andrew's word on a measuring identity is
carried to him and unanswered.

## 4. The CVO's watermark against the channel's row count

- Latest slug: `surprise-channel/remediations/REMEDIATION_v10.md` @b883aa5764.
- Rows filed by this seat in round 12: none. The round's packet for the reviewer is the st31 state file above.

## 5. Armed rows (unchanged)

| row | class | owner | state |
|---|---|---|---|
| D2-S38 | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | held for the next batch window; and the fix it would confirm is NOT live now, because IRPT_ANLREQ release 5 was rolled back at 11:26:53Z (CTO msg 5016) |
| D2-S45 | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | 8 dead letters, untouched. The record that lets them be reconciled without a redrive is now ON THE HOST, but it writes only for jobs that fail from now on; the 8 are reconciled by a write under a pair naming each. One of the 8, REQ-4b5155ac2ea9467ab771b414, also has a `commentary_ready` message waiting (section 6) |
| D2-W10-S4 | BLOCKING, ARMED | `2.0.0_SA_COO~G2` | the logo was passed by `--member` again; V1 read it from the running root (3,853 bytes) |
| S16 | OBSERVATION, ARMED | `2.0.0_SA_COO~G2` | as round 10 |

## 6. For the round-13 analysis: the next resident releases, and one finding from another project's read

- **st32** is named by the CTO (msg 5026) for IRPT_BCKEND's capture-diagnosis build, under its own pair.
- **The attach release** is IRPT_ANLREQ workstream G's, four cells. Cell 1 (the builder and the runtime) is built and awaits
  its merge; cell 3 is read: the ONE message on the commentary-ready queue is `commentary_ready` for 49financial, request
  REQ-4b5155ac2ea9467ab771b414, sent 2026-10-11T06:10:50Z, receive count 1 of 3. That request's job reads RECEIVED and its
  accepted record carries no `ticket_id` and no `commentary_ref`. A bound resident would refuse it by name and it would
  dead-letter on its third receive. Read by the laptop's executor, record @87e2151436; I read it at that commit.
