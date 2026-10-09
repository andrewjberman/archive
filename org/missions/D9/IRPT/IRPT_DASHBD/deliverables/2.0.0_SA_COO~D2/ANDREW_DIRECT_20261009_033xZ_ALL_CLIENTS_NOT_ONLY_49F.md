# ANDREW-DIRECT 2026-10-09 ~03:3xZ -- IRPT_DASHBD covers all clients, not only 49 Financial

**Received by:** `2.0.0_SA_COO~D2`, in its own terminal (dell2)

**Verbatim:**

> "You should be doing this not just for 49 Financial, but for all clients, inflection and cottonwood too."

**What it changes.** Today the reporting-gold function, its role and its five gold prefixes are firm-scoped to 49 Financial. These cover:
- account returns;
- the class table;
- the activity table;
- the two lot tables.

The order widens the endpoint to every client firm, naming Inflection and Cottonwood.

**Routing.** This is an ENDPOINT change, which is the CTO's (L2, then an L4 PRD addendum), sent to `1.0.0_SA_CTO~DELL2`. The COO cuts the cells from the analysis or addendum that follows.

**Law the build keeps.** No pipeline tree references another firm's data, by bucket or by key prefix (CLAUDE.md, HARD STOPS). Each firm therefore gets its own builder-named function scope, role grant and gold prefixes. Every name and address is `lib/opal_naming.py` output (rule 30); there is no shared multi-firm reader.

**Not read yet.** For each named firm, these are unread:
- whether its silver custody tables exist and hold the same columns;
- what the tie-out comparison source is (49 Financial's is Black Diamond).

The first cell per firm reads them.

**Registry read, ~03:40Z, by this seat.** Source: `infra/logic/registry/scopes.json` at HEAD and `data/assets/scripts/gold/irpt_reporting/sources.json`.

- **49 Financial.**
  - Masters: `08242234` and `08335338`, both Schwab.
  - `sources.json` declares one custody source, `schwab_08335338`, in the `opal-data-assets` bucket.
  - The tie-out compares against Black Diamond (`z08` ids).
- **Cottonwood** (short `cot`; bucket `opal-data-cottonwood`, provisioned).
  - Its only registered master is `z09`, vendor **Black Diamond**: 984 accounts, measured 2026-09-24 in the registry note.
  - Pipeline tree: `data/cot/`, `separated_from` 49financial and inflection.
  - **No custodian feed is registered.** A Cottonwood build reads Black Diamond through its own adapter (C-ADAPTERS), so Black Diamond cannot also be its independent tie-out source.
  - Prior record: `TO-IB-er-401_STEP0_DONE_COTTONWOOD_BLOCKED_20260929.md` (row IRPT_BCKEND-S203).
- **Inflection** (short `inf`; bucket `opal-data-inflection`, provisioned).
  - **No master is registered.** All tenant bindings are null.
  - There is no declared custody source to build from.
  - The legacy `opal-data-inf` alias is routed.

**What follows for the CTO.**
- Cottonwood needs a Black Diamond source adapter, plus a decision on what its numbers are checked against.
- Inflection needs its custody source identified and registered (a registry row) before any cell can build.
- Both are first cells, ahead of any build.

**The 49 Financial release is not held by this order.** Its never-widen pair is signed (COO @cbad72eb7b, CTO @75acbfcb50), and it proceeds on its own track.
