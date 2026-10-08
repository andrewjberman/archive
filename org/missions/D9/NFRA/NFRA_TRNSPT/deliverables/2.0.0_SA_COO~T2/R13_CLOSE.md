# NFRA_TRNSPT round 13 -- close record: the first real AI commentary draft (2.0.0_SA_COO~T2, dell2, 2026-10-08)

Issuance `8228dc63a4` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R13.md`, CTO round-12 analysis @a090c5ea23: C-WIPE-GATE PASSED).

| cell | carrier | result |
|---|---|---|
| TR-g-13 (E1, row D2-S6) | NFRA_TRNSPT.TO-TR-g13, merged `bf2332f487` | `R13-G13-OK 2 passed`; drafter emits `generated_at` (UTC, `...Z`); commentary suites 17 passed |
| TR-k-13 (E2 + E3, WORLD) | issuer, 2026-10-08T22:59-23:00Z | the journey H2 -> H6 with the REAL gate and ONE real Kimi K3 call |

## E2 + E3 -- the journey trace with the real gate (`R13_THREAD_TRACE_REAL_GATE.json`)

Inputs: a SYNTHETIC READY event and composition (the entry tests' fixtures) -- no real client data was sent to the vendor. Gold: 0 objects
(live count), so the draft is the no-precedent draft.

| hop | result |
|---|---|
| H1 READY hook | STUBBED -- ~P2's contract AGREED (msg 1849); H1 is cut once `outlook-global-commentary-draft-lambda` exists |
| H2 entry | 1 result, 0 failed |
| H3 slicer | 0 candidates (gold empty) -> `no_precedent` TRUE |
| H4 Kimi K3 | **ONE real call** (vendor_calls_made 1; a second call was refused by construction), 48.7 s; `DRAFT`, model `kimi-k3`, `generated_at` 2026-10-08T23:00:24Z; 3,908 characters, sha256 `bbcf863c...e04841d`; starts "NO PRECEDENT"; planted identity in the draft: none |
| H5 ticket type | STUBBED (~V2 contract section 5) |
| H6 ticket write | `ok` TRUE, `action` done, ticket `TCK-00000000-stub0000` (the stub) -- row D2-S6 is fixed |

E2's "logged by request id with no prompt body": the run logged `commentary draft request_id=req-1 ok`; neither the prompt nor the draft text
was printed, logged or stored -- the draft is recorded here only by its length and hash. "Lands as a ticket DRAFT only Opal can see": it
landed on the stub, inside the issuer's process; the real landing waits on H5 (the route and the `svc-commentary` token, ~V2's O1).

Andrew's 2026-09-30 word covered this FIRST call; any further vendor call needs his word for that use.
Credential: dell2's first read of `astn/kimi/api-key`, reported to the laptop through `0.0.0_AB_MSTR~DELL2` (msg 1232 rule 2).

## Rows

- D2-S6 (BLOCKING): resolved by `bf2332f487` (the trace reaches H6 with `done`).
- **D2-S7 (BLOCKING, new):** ~V2's ticket contract REQUIRES `answers.household`, but the IRPT composition has none (~P2 msg 1849), so H6 would
  dead-letter every REAL report. Owner: the CTO with ~V2 (household optional, or its true source named), then ~T2 adapts.
- D2-W1-S5: answered by ~P2 -- `account_type`, `themes`, `household` absent; holdings weights derivable from the normalized input;
  `ref.request_ref` is the composition's request id.
