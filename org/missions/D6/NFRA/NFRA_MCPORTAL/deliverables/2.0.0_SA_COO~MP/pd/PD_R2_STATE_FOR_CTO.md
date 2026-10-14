# NFRA_MCPORTAL -- PC ROUND 2: where it stands, and the one thing it waits on -- 2.0.0_SA_COO~MP, 2026-10-14 ~20:2xZ

For `1.0.0_SA_CTO~Z`. Answers your msg 34162 (the round) and msg 34168 (Andrew: finish what remains, then close or hold).

## Built and drained: 6 of 8 cells (MP-pd-1 to MP-pd-6), all local on box/sitez

| cell | result | merged |
|---|---|---|
| MP-pd-1 (R1) | the People view read under the OPERATOR role equals the grant store: 1 of 1 principal, 5 of 5 tools. Z-W24-S2's limit is closed. Only one principal holds a data grant today | @9771f6af91 |
| MP-pd-2 (F2 writer) | `set_person_access` in the grant-writer Lambda: 12 new tests, suite 36 passed. Refuses with RECORD-KIND-NOT-LIVE until the live gateway's `access_state` knows the type | @dc132db72a |
| MP-pd-3 (F2 handler) | owner-gated `GET`/`POST /api/admin/people/{tid}/{oid}/access`; People rows carry `principal`. Amended once (my cut defect) | @75248b6d2e |
| MP-pd-4 (F2 page) | People page controls (channel and tool switches, stop and restore, history); bun 51 pass 0 fail; mcportal DEV is at f7760a6 (pushed by MSTR~Z, ls-remote read). Amended once (the 409 mapping) | @1b60a93715 |
| MP-pd-5 + MP-pd-6 (U2) | the status-line command is ENABLED on site Z and a live `rate_limits` payload was SEEN: the member is present, snapshot `measured` with both windows. FWD-22's source question is answered on this box | @e327ca0703, @e0af5e8f7f |

Measured on the live snapshot at 20:09Z (this box's login only): 5-hour used 4 percent, weekly used 84 percent. Both come from the payload, not a guess.

## What is NOT done, and why

1. **MP-pd-7 (the F2 release) and MP-pd-8 (the close run) are STAGED and gated on two things outside this project.**
   - NFRA_OPLGTW's OG-cp-1 (the gateway reader of the `person_access` record) must be RELEASED. Its order is still a draft (`DRAFT_NOT_ISSUED_TO-OG-cp-1_...`). The writer Lambda stages its closure from the live gateway release, so a Lambda built before that release refuses every write; releasing F2 earlier would ship an inert control.
   - Andrew's sitting on the People page: the writer verifies the owner's signed header, which no seat can produce, so the six test-principal changes are his, then a worker reads them back.
2. **FWD-22 is not REALIZED and its panel is not built.** The snapshot is a file on one box; the control-plane page is served from AWS and cannot read it. The transport (the per-box producer carrying the snapshot, the gateway handler passing it through, the panel printing it) is the next enrichment. I ruled it out of this round in decomposition PD.8 item 3, under your "do not open new outcomes".
3. FWD-21's DONE WHEN needs MP-pd-7 and MP-pd-8, so FWD-21 is not REALIZED either.

## The ask

Close or hold? My recommendation: **HOLD NFRA_MCPORTAL at "F2 release and close run staged, waiting on OG-cp-1 and Andrew's sitting; FWD-22 panel transport unbuilt"**, because nothing at this seat can advance without NFRA_OPLGTW's release, and Andrew asked that site Z's effort go to the first three items. When OG-cp-1 is released, MP-pd-7 is one release and MP-pd-8 one sitting.
