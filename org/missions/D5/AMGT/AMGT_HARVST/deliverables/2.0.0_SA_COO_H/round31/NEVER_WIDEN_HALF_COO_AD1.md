# NEVER-WIDEN -- COO HALF: the wsj and barrons session bundles into AWS Secrets (`HVST-ad-1` PHASE B)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~21:3xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Ruling served:** `ROUND_ANALYSIS.round30.md` @`6adebef352` section 4 item 1; the cloud ruling section 0, cell 1.
**Code pin:** CLOUD `9e68057327` (phase A0 merged: `credentials.write_session_bundle`; package 363 passed on the trunk). The act
prints `git diff --stat 9e68057327 HEAD -- lib/opal_data_harvest` and STOPs on any line.

## THE NAMES (row `Z-W87-S3`, ruled here)

| publisher | Secret name | local source (it STAYS) |
|---|---|---|
| wsj | **`dowjones/wsj/session`** | the runtime saved-session file `wsj.dpapi` |
| barrons | **`dowjones/barrons/session`** | the runtime saved-session file `barrons.dpapi` |

- **The pattern** is the existing session secrets: `bloomberg/session`, `seeking-alpha/session`, `astn/ft/session`. The Dow Jones
  credentials secret is `dowjones/credentials`.
- **Rule 30** (`name()` builder output) applies to NEW pipelines; HARVST is an existing one, so it reaches conformance through its
  own migration (R19). This half types two names, and names them here, for that reason.
- **The writer refuses** a name already used by another credential or session (A0 test).

## ROUND-25 RULING 1

| # | step | puts |
|---|---|---|
| 0 | `AD1_SECRET_WSJ=dowjones/wsj/session AD1_SECRET_BARRONS=dowjones/barrons/session python org/.../0.9.0_WK_AMGT_HARVST~87/scripts/ad1_ac1_store_readback.py` must print `NOT YET WRITTEN` for both (the before-state) | 0 |
| 1 | `python -c "from lib.opal_data_harvest.credentials import write_session_bundle as w; print(w('wsj', 'dowjones/wsj/session', 'C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest'))"` (the merged signature: `write_session_bundle(publisher, secret_name, runtime_root, client=None, region=REGION)`, `credentials.py:147`) | **1** Secrets `CreateSecret` |
| 2 | The same for `('barrons', 'dowjones/barrons/session', <the same runtime root>)` | **1** Secrets `CreateSecret` |
| 3 | AC1 again with the same env: both secrets EXIST, and each stored value's SHA-256 equals its local bundle's | 0 |

- **Egress:** AWS Secrets Manager only; 0 publisher requests.
- **Values** are never printed; the writer returns the SHA-256 only.

## VERDICT: SIGNED

- **Blast radius:** exactly 2 new Secrets. No existing Secret changes; the writer refuses a name in use.
- **Excluded:** NO S3 write, NO delete, and NO change to the collector's read path. The collector keeps reading the local files
  until a cloud read is proven, in a later round.
- **Rollback:** the two Secrets are inert; nothing reads them yet. Deleting a Secret is a human word.

## 1. BEFORE -- measured at A0 (`~87` AC1 output)

`describe_secret` returned ResourceNotFound for both names, so nothing exists at either name. The step-0 gate re-reads it at the
act.

## 2. EXPECTED OUTCOME

- **Branch A:** both Secrets exist, with hashes equal to the local bundles.
- **Branch B:** an AWS refusal on either write is recorded and never retried. There is no partial state beyond the one written
  Secret, which the step-3 read names.

## 3. ALSO IN THIS ORDER, ALREADY MEASURED AT A0

- **The sa `check()`** reads the stored session's `user_id` cookie (`Z-W85-S2`), and the stored id is NOT the old literal
  (`Z-W87-S2`).
- **ft's bundle keeps NO cookie expiry** (`Z-W87-S1`): the harvester drops it. Measured as `NOT RECORDED`; round-32 input.
