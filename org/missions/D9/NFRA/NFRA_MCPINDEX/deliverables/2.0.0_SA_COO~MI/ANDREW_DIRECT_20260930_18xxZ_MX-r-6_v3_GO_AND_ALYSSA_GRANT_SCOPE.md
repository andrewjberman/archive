# ANDREW-DIRECT 2026-09-30 ~18:0xZ -- MX-r-6 v3 GO, and the scope of Alyssa's Schwab grant

**Where:** the 2.0.0_SA_COO~MI terminal, site Z, answering this seat's `/open-calls` (2 cards).
**His words, VERBATIM:** "recs approved, proceed"

## What it answered (the two cards, their RECs, as put to him)

1. **CALL 1 (BLOCKING):** "GO on the Schwab enable release, MX-r-6 v3: yes / no?"
   - REC: yes.
   - Halves: COO @20599c0c29, CTO @c0308f8b75, CVO @5c54630648 (guards H1-H3). COO~O released its hold (msg 27307).
   - Earlier this session he had asked this seat to wait for his word before the GO.
2. **CALL 2 (CARRIED):** "Alyssa's new Schwab grant: all accounts under both masters, read-only (list/describe/query, no
   download) -- confirm?"
   - REC: confirm as stated.
   - This completes his "agreed" (@29bc46d827), which named the two masters and the four datasets.

## Reach (no wider, no narrower)

- **GO for MX-r-6 v3 PHASE B**, on the signed pins: release a5e73b6e72, deploy-only 42c52ed4d9, live ref
  4ce794642699e78a718b8154664e1428737f996a. The deploy runs with `DEPLOY_BASE_REF` (CVO H1), and the targeted IAM
  plan must read 0/1/0.
- **Alyssa's ONE new Schwab grant** (tid 6810043e-d171-4adc-9975-068b35e179da, oid ad037ea5-fee8-412e-9da9-15c6cf2a4fbc):
  - masters 08242234 and 08335338, and every account under each;
  - datasets dim_position, dim_balance, dim_asset and dim_transaction, with all contracted columns;
  - operations list, describe and query only (no download_filtered);
  - dates rolling_complete_window;
  - her portal channels unchanged.
  It is written through `ops/schwab_entitlement_admin.py` as `opal-gateway-access-admin`, after v3 lands, and recorded
  before and after. Raw account ids stay out of the repo.
- No other grant, principal, or surface.
