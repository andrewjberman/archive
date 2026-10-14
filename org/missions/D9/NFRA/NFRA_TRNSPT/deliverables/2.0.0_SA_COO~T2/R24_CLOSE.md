# NFRA_TRNSPT round 24 -- close record: the four Monday meetings answer `refused` in the completeness table; the drafter's first live post stays parked on one staff filing (2.0.0_SA_COO~T2, dell2, 2026-10-14)

Issuance `adf48aa85c` (CTO round-24 analysis @8905ffd1fa, decomposition `decompositions/NFRA_TRNSPT_DECOMP_R24.md`). `round-close-check --round 24`:
MAY-CLOSE (8 orders in scope, 8 complete, proofs 8 of 8 structural OK, 0 judgment). Every figure below is the issuer's own read at 2026-10-14T11:3xZ unless it names a record.

| cell | merged / act | what exists |
|---|---|---|
| TR-cm-24 (FWD-4) | worker `0.9.0_WK_NFRA_TRNSPT~1`, build f7dc2041ec, proof 458bfc50dd, drain dad5c0cce0 | `teams/completeness.py` classifies a listed, allowlisted meeting whose content read was refused as `refused`; a listed meeting with no read-refusal evidence still raises `unclassifiable`. Re-run `R24-CM24-OK 23 passed` |
| TR-cl-24 (FWD-4) | issuer live read | `R24-CL24-OK 2026-04-10=refused 2026-04-13=refused 2026-05-04=refused 2026-06-01=refused 2026-10-05=here` (positive control `here`) |
| TR-dp-24 (FWD-10) | PARKED, WORLD | packet `R24_TR_DP24_DRIVEN_DRAFT_PACKET_20261012.md` (DRAFT, not sent). Precondition 1 needs a request filed by one Opal staff member in 49financial naming ticket `TCK-20261012-c546fead`; nobody has reported it filed. No applier order is cut |
| TR-fr-24 (FWD-2) | issuer read, event, half read | see below |

## TR-fr-24: the scheduled fire after the 2026-10-13 asset_management_ic meeting

`run.json` `run=2026-10-13T22:00:09Z`, transport gateway, read from `s3://opal-data-transcripts/teams/transcripts/state/pull_runs/`:

| series | listed | landed | held | read_refused | refused |
|---|---|---|---|---|---|
| `monday_meeting` | 20 | 0 | 16 | 4 (2026-06-01, 05-04, 04-13, 04-10; `GatewayGraphError status=502`) | 0 |
| `ocio_ic` | 8 | 0 | 8 | 0 | 0 |
| `asset_management_ic` | 8 | 0 | 8 (includes `ICA-20261013-0958`) | 0 | 0 |
| `research_meeting` | 0 | 0 | 0 | 0 | 1 (`list GatewayGraphError status=502`) |

The asset_management_ic half: the 2026-10-13 meeting was listed and HELD by the fire after it, as the hold window requires; it did not land. The ocio_ic half is UNEXERCISED: its newest listed meeting is `ICO-20261006-0959`, so no fire has followed a newer one.

## Open at round close

| item | state | owner |
|---|---|---|
| TR-dp-24 | WAITING on one staff filing in 49financial (a person's act); `2.0.0_SA_COO~V2` and `~Y2` live and told | Andrew's staff; then the issuer sends the packet to `1.0.0_SA_CTO~DELL2` |
| TR-fr-24 ocio_ic half; first landing under a scheduled fire and its `Max Memory Used` | UNEXERCISED; wait on the next ocio_ic meeting and on a readable transcript | issuer, at that fire |
| `research_meeting` listing (FWD-2, 1 of 4 series) | 502 on every fire; the folder is Lauren's OneDrive `Recordings` (CTO msg 6903); waits on a share-link resolver from site Z | site Z, then the issuer cuts the read-only listing cell |
| FWD-3 wording: the four Monday meetings | read-refused, not absent; hold-lapse evidence recorded in `R24_FWD3_29SEP_EVIDENCE_READ_20261012.md` (06-01 undecidable on the 29 September cutoff); one ask to `1.0.0_SA_CTO~DELL2` | CTO |
| Commentary model | Kimi K3 now, an OpenAI key swapped in later on Andrew's word only (record `ANDREW_DIRECT_20261013_211xZ_COMMENTARY_MODEL_KIMI_K3_NOW_OPENAI_LATER.md`) | none today |
