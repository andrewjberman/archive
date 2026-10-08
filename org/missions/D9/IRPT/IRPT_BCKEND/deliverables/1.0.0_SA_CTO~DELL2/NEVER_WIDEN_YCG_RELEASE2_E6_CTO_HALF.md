# NEVER-WIDEN SIGN-OFF -- CTO HALF -- irpt-ycharts-generate RELEASE 2 (E6): on-behalf upload with the E5 guard + the W174-S3 grant

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~19:0xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 1440 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release2_ycg/NEVER_WIDEN_PAIR_RELEASE2_E6.md`,
**blob 369629b0c9** (@8c11ac4ff1). **Pin:** 1b94d50b8c. **Built:** `Un0wVZqj...`. **Rollback:** `ZspX0qD2...`.
**Authority for the widened class:** Andrew-direct ~18:3xZ ("Opal does upload on behalf of partner firms, it is good to have this
function") and ~18:5xZ ("Alyssa can file on behalf of all partner firms").

## Measured by this seat

| claim | instrument | read |
|---|---|---|
| census = 4 owned members, no rider | `release-census.py irpt-ycharts-generate --pin 1b94d50b8c` | 100 / 100; changed generate_installed.py, interactive_access.py, served.py, uploads.py; `changed_members=4` |
| live = the rollback target | `lambda get-function-configuration irpt-ycharts-generate` | `ZspX0qD2bCkF...`, 2026-10-08T17:44:54Z |

## Blast radius signed

- **Code:** one function's code at the pin.
- **IAM:** ONE role-policy statement. It is `dynamodb:GetItem` only, on exactly `opal-partner-49financial`, `-cottonwood` and
  `-inflection`. There is no wildcard, no Query and no KMS statement.
- **Data:**
  - one synthetic test profile row, with no login identity, deleted in every branch;
  - the admit's `UPLOAD#` row and its S3 object, read back and deleted on the laptop through the fenced path.
- **The one widened class:** an OPAL_GLOBAL filer whose `allowedFirmIds` lists the firm, naming a verified advisor of that firm. Every
  other class is unchanged or refused, as in the packet's section 4 table.
- **Both branches:**
  - **A:** after-reads 0 to 8 pass.
  - **B:** code back to `ZspX0qD2...` in the same session, then cleanup, then the grant rollback, plus a BLOCKING row.

## Conditions this half adds (the packet's section 8 items are PRECONDITIONS, not follow-ups)

1. **No apply of any key until all three owed items are in the ledger:**
   - (a) `~P2`'s `served.py` diff-read note;
   - (b) pin 1b94d50b8c on origin CLOUD (`fetch` + `is-ancestor`);
   - (c) the named laptop seat's dry-probe result `ConditionalCheckFailedException`.

   With any of them missing, nothing moves.
2. **The order is fixed as the packet states:** grant -> read-back -> code -> equality -> test row -> admit -> refusals -> regression ->
   cleanup.
3. **Re-read live code at the start.** If it is not `ZspX0qD2...`, STOP.
4. **The real advisor in after-read 4 appears by opaque id only** in every file and message.

The Alyssa entitlement (`allowedFirmIds` = 49financial, inflection, cottonwood) is a separate pair (`~Y2`). It is not in this write set.

**Verdict: GIVEN**, for exactly this write set at this pin and blob, under the conditions above.

-- 1.0.0_SA_CTO~DELL2
