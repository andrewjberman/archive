# NFRA_TRNSPT round 12 -- close record: the FWD-10 thread (AI investment commentary) (2.0.0_SA_COO~T2, dell2, 2026-10-08)

Issuance `71b72d7a3e` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R12.md`; Andrew-direct ~22:2xZ @a4fdb78bbe, CTO msgs 1763, 1780).

| cell | hop | merge | criterion |
|---|---|---|---|
| TR-e-12 | H2 READY event -> abstract request + separate ticket context; READY-event contract draft | `98ca40fd4c` | `R12-E12-OK fields=9, 6 passed` |
| TR-d-12 | H3 slicer over gold + H4 Kimi drafter (injected model, wipe-gate refusal) | `6c4581b47c` | `R12-D12-OK 6 passed` |
| TR-t-12 | H6 ticket-write client to ~V2's contract v0.1 @a8410fcca3 + its section-5 stub | `34ec06266d` | `R12-T12-OK 3 passed` |

Drain: transcripts tests `-k "commentary or slicer or outlook or research"` 100 passed, 0 failed; `commit-gate.sh` clean on the 3 modules.

## The journey trace (`R12_THREAD_TRACE.json`; synthetic READY event and composition, live gold count, FAKE model)

- H1 READY hook -- STUBBED (IRPT_BCKEND `~P2`). Consumer target given to ~P2: `outlook-global-commentary-draft-lambda`, DLQ
  `outlook-global-commentary-draft-queue` (`lib/opal_naming.py name()` output; not deployed).
- H2 -- 1 result, 0 failed; abstract keys `request_id, yc_variant, comparison_keys, account_type, themes, holdings_categories, requester`;
  ticket keys separate.
- H3/H4 with the gate NOT passed -- `REFUSED WIPE_GATE_NOT_PASSED`. This is today's real state: TR-w1's planted-token test is complete, but no
  record declares C-WIPE-GATE passed.
- H3/H4 with the gate simulated passed and a FAKE model -- `DRAFT`, `no_precedent` TRUE (gold holds 0 objects live), 0 candidates; planted
  identity (household, firm, client email, requester name and email) in the prompt: none; in the draft: none.
- H5 -- STUBBED (TCKT_VNEXT `~V2`, contract section 5).
- **H6 -- BROKEN: `ok false, action dead_letter`, error "missing required value: 'generated_at'".** The contract's `draft_commentary`
  requires `generated_at`; the drafter emits none. Row **NFRA_TRNSPT-D2-S6** (BLOCKING): round 13's first cell.

## Rows

- D2-S6 (BLOCKING, INERT): the H4 -> H6 seam (above).
- D2-W1-S5 (OBSERVATION): the retained composition is not measured to carry `account_type`, `themes`, holdings category weights or
  `household`; `ref.request_ref` as the composition id is unconfirmed. The READY contract lists them "unknown -- producer to confirm".

## Open for the CTO

1. **C-WIPE-GATE** is not recorded passed, so no real Kimi call was made. The first real call is unlocked by Andrew's 2026-09-30 word only
   after the gate is recorded passed.
2. **Precedent:** commentary gold holds 0 objects, and silver's 3 commentary rows are all held out, so every draft today is no-precedent.
