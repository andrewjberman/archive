# Round-47 items owed to the next L10 slug (draft, written by 2.0.0_SA_COO~O while OG-ap-50 Phase B runs)

State at writing (2026-10-19 ~17:0xZ): round 46 has OG-gd-2, OG-cd-2, OG-cd-3 complete; OG-ap-50 in Phase B at `0.7.0_AE_CloudOps~NFRA1` (ledger `nfra-oplgtw-gateway-release-batch14` OPEN); OG-ap-51 and OG-ev-13 staged. The CTO analyses the round; this list is what the COO owes it, each item with its source. Nothing here is cut; the round-46 spec is frozen.

| # | item | source | note |
|---|---|---|---|
| 1 | Mask the AWS error text in `app/family_depth.py` `_why` (scrub ARN, twelve-digit and instance-id shapes) | row `Z-S407`, ruling row `Z-S408`; CVO condition C1 (`3.0.0_SA_CVO~Z` half, `b6d2c59637`) | COO is the disarm owner. Until it lands, nothing surfaces the route's response beyond the owner. One-function change; needs a release and a landing |
| 2 | Narrow the `*/silver/*` `s3:ListBucket` statement of `gateway-family-depth-read-policy` | `OG-cd-3` Phase B CT3 census (`FD_CT3_CENSUS.json`): 4 top-level prefixes beyond the eight sources hold a silver child (bloomberg, commonwealth, gateway, yahoo) | CTO half of `OG-cd-3`: narrow to `<source>/*/silver/*` if the count is non-zero. It is non-zero. Terraform via `safe-apply`, own ask, three halves |
| 3 | The `audit.py` comment fix, and `total_max_attempts: 1` if one send is the intent | CTO ruling on `OG-ap-48` (msg 35909): "rides the next audit.py change" | Rides any later `audit.py` release; no release of its own |
| 4 | Ship `app/admin_people_access.py` and `tests/test_admin_people_access.py` whole from trunk (`b6dd9f9249`) | `2.0.0_SA_COO~MP` written yes, msgs 35981 and 35990 (row `Z-W27-S1` is closed) | Inert, unmounted; mounting stays with PD under the CTO's hold. `admin_people.py` is NOT in the take |
| 5 | The owner-session read of `/api/admin/gateway/families` | `OG-ap-50` honest limit; Andrew's, later | The route's 401 after deploy is the served proof of the gate; an owner read is the real one |

Added from the CTO (msg 36020, ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_GATEWAY_ASSETS_AUDIT_DEFECT_ROUTING_20261019_Z.md` @473f5177a8, on CRO~Z's audit @216dfc8144; the CTO cuts them in the analysis; no hand fix outside a release):

| # | item | note |
|---|---|---|
| 6 | D1, FIRST: no `fence_kind` for orion, eclipse or commonwealth, so `firm_not_served` on every call | the CTO orders it first |
| 7 | D2: the Cottonwood Black Diamond `_date()` accepts ISO only, against MM/DD/YYYY source dates | |
| 8 | D3: `client_resolve_account` keeps the first adapter's envelope and hides other vendors' refusals | |
| 9 | P1 handler half: the breakdown handler supplies (vendor, firm) per index | |

The auditor files D1-D3 as rows in this channel with me as disarm owner (not yet read as filed at writing).

Waiting, not items: `OG-ev-13` (GO no earlier than 2026-10-20 07:45Z, essential wait); FWD-21 (Andrew's act, open call `5b35`); the Schwab pilot walkthrough (open calls `a485`, `2ac2`).

Added 2026-10-19 ~17:5xZ (urgent session, Alyssa 19:00Z):

| # | item | source | note |
|---|---|---|---|
| 10 | Master-wide Schwab scope resolved at read time, no stored account list | CTO msg 36025, Andrew-direct @65a05f6658 ("there shouldnt be a persisted list") | `OG-mg-2` is the interim (re-activation at current accounts); this is the code cell |
| 11 | A memory guard for concurrent battery load on the gateway host | CTO msg 36045; `2.0.0_SA_COO~MI` msg 36038 (hang at `MemoryHigh` 1.2 GB, six parallel runners, 10-17 reading 87 percent) | the restart is `OG-rs-1`; the guard is the cause |
| 12 | Z-S409..Z-S412: D1, D2 (ARMED, Z-S410: Cottonwood answers an empty list as if the account had none), D3, S1 | CRO~Z msg 36027 | rows filed with me as disarm owner |
| 13 | Menachem's Schwab grant, the same shape as Alyssa's, over the full current accounts; activate AFTER her 19:00Z session proves the shape; own never-widen | Andrew-direct via CTO msg 36049, record `ANDREW_DIRECT_20261019_175xZ_ROSTER_OPEN_CALLS_YES_TO_RECS_SCRATCH_NO_REC_WIDENINGS.md` @50bd4a33b4 | not granted: Wayne's client tools, AJ's Black Diamond fees, Yang's Schwab access |
| 14 | The `client_*` tools for Alyssa and for Menachem, each under its own never-widen | same record | sequenced AFTER D1-D3 (items 6-8) land |
