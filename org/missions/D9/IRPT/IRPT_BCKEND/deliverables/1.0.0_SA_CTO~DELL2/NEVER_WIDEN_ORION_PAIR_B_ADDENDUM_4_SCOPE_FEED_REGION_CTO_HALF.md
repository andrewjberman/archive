# CTO half -- Orion pair (b) ADDENDUM 4: the Scope feed script with its region named

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~12:5xZ.

**Addendum:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_4_SCOPE_FEED_REGION.md`, blob `22172a052e8de14c97c5eed0846fa78239964ea3` (7,087 bytes), equal in the working tree. Commit 1d1034aef2. Applier: `0.7.0_AE_CloudOps~IB2`.

**SIGNED.**

## Read at signing

- `git diff 7b47813ad1 3b3d3e9f94 -- data/inf/manual_api/pull_inflection_scope_account_returns.py` shows exactly 2 lines added and 1 removed in `session_token()`. The secretsmanager client gains `region_name="us-east-1"`, with one `RUNNER-REGION` comment. Nothing else changes.
- The new blob is `e2ed945d2e92`, equal at `3b3d3e9f94` and in the working tree.

## Blast radius

The same as ADDENDUM 3, section 5:
- the script's code object is overwritten with the new bytes, and the saved replaced object (`4527c57f...`) is the rollback;
- the dispatch gains its one catalog row and chain entries;
- the first scheduled chain writes the feed's two prefixes as new keys, each read ABSENT first.

**Served values changed:** none.

**Both branches are covered.** The 11:33Z chain's failure was already rolled back by Branch B (restored at 12:09:21Z, sha256 equal).

## Conditions

- **The widened smoke is accepted:**
  - live prefixes;
  - `session_token()` building its real client under a scrubbed AWS environment;
  - a PLAN-ONLY run.

  A smoke that builds no client is no longer sufficient for this script.
- **The sidecar must equal the builder-generated address.** An absent or different sidecar is a STOP, as written.
- **One firm per fire day:** this apply touches only the Inflection Scope feed. It runs outside the weekday 11:30Z to 14:15Z band and never on the day of the Inflection transaction apply.
