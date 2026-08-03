# OVP WS-1 -- Vendor As-Of Endpoint Census: Denominator + Tranche Ledger

**archetype:** TRACE
**Author:** 0.4.0_DS_ClientPlatform
**Date:** 2026-08-03 (T1 tranche)
**TO:** OPAL_VENDORPROVENANCE.WS1.asof-endpoint-census (GO 20260803T201222Z; D-1/D-2/D-3 folded @e82271228b)
**Registry:** `data/_contracts/vendor_asof_registry.yaml` (canonical home per D-1)

---

## 1. Denominator derivation method (live, not memory)

The denominator is the set of BRONZE-WRITING INGEST PATHS into the four census buckets
(`opal-data-assets`, `opal-data-bd`, `opal-data-inf`, `opal-data-cot`). Derived from four
independent instruments, each labeled per claim:

| # | Instrument | What it grounds | Denominator printed |
|---|---|---|---|
| M1 | Live `aws s3 ls` on all 4 bucket roots + every vendor prefix + recent bronze partitions (2026-08-03) | What is ACTUALLY landing (APPLIED) | 4 buckets, 12 monolith top prefixes, 7 vendor sub-buckets; per-partition listings for opal-data-inf 07-31..08-03 |
| M2 | `comp-estate --list` (29 verticals / 138 chains, census vintage 2026-07-30) + `comp-estate advi-inf` | Producer->served chain context (SEED, drift-checked against M1/M3) | advi-inf: 14 chains read in full |
| M3 | Repo source: puller code + Terraform EventBridge (`comp-grep` on-rails; 68-file inf-pipeline sweep, 9/9 pullers route-grounded) | DESIRED schedules + endpoint literals + as-of mechanisms | 18 schedule_expressions in inf-pipeline TF; 9 Orion pullers + 1 Eclipse puller + 1 orchestrator |
| M4 | Contract docs: `OPAL_ASSETS_V2_LAMBDA_CONTRACT.md` (10-family ingest table), `INFLEC_API_ENDPOINTS_CATALOG.md` (endpoint contracts), `_orion_vendor_asof.py` (sealed semantics) | Monolith ingest family map + endpoint contracts | 10 monolith bronze families enumerated |

Census-vintage drift found and grounded live: the estate census carries the PRE-shift crons
(12:30-13:00 UTC); TF + live landings carry the +47min shift (@b2f61bed83, 2026-07-01).
The TF is authoritative; the estate snapshot is 5+ weeks stale on this axis.

## 2. Denominator table (ingest inventory, all four buckets)

Status: `T1-LANDED` = registry row committed this tranche. `T2`/`T3`/`T4` = assigned tranche
per D-3 order (Orion -> SmartX/BD/cot -> Schwab-0824/Eclipse -> rest; Eclipse landed early
in T1 because its grounding was already sealed in source).

### opal-data-inf (firm bucket, Inflection)

| Ingest path | Producer | Trigger (DESIRED) | Vendor endpoint(s) | Status |
|---|---|---|---|---|
| bronze/assets/{date}.parquet(+.jsonl.gz) | inf-api-assets-v2 Lambda | cron(32 13 UTC) | orion Assets/{date} per-client | T1-LANDED |
| bronze/orion-api/{date}/positions* | inf-api-positions Lambda | cron(37 13 UTC) | orion Assets/{date} per-client | T1-LANDED |
| bronze/orion-api/{date}/new_portfolio_accounts.json + accounts_roster.json | inf-accounts-v2-daily Lambda + EC2 orchestrator | cron(22 13 UTC) + cron(30 13 UTC) | orion Accounts/NewPortfolio + Accounts | T1-LANDED (x2 rows) |
| bronze/orion-api-v2/{date}/representatives.json + household_rep_mapping.json | inf-api-reps Lambda | cron(17 13 UTC) | orion Representatives + Clients?repId | T1-LANDED (x2 rows) |
| bronze/orion-api/{date}/unified_account_dim.csv | inf-unified-account-dim-daily Lambda + orchestrator | cron(27 13 UTC) + cron(30 13) | orion Envision 'Unified Account Dim' | T1-LANDED |
| bronze/orion-api/{date}/billing.csv | inf-billing-daily Lambda + orchestrator | cron(22 14 UTC) + cron(30 13) | orion Envision 'Billing Dim' | T1-LANDED |
| bronze/orion-api/{date}/tax_unrealized.csv + tax_realized.csv | inf-tax-daily Lambda + orchestrator | cron(42 13 UTC) + cron(30 13) | orion Envision 'Tax * Dim' x2 | T1-LANDED |
| bronze/orion-api/{date}/performance_dim.csv | inf-performance-daily Lambda + orchestrator | cron(27 14 UTC) + cron(30 13) | orion Envision 'Performance Dim' | T1-LANDED |
| bronze/orion-api/{date}/transactions.csv | inf-api-txn Lambda + orchestrator | cron(47 13 UTC) + cron(30 13) | orion Custom Reports/28198 | T1-LANDED |
| bronze/eclipse/{date}/* (4 artifact classes + sidecar) | inf-bronze-runner EC2 (pull_eclipse_portfolios.py) | inf-bronze-trigger cron(30 13 UTC) | eclipse /v1/portfolio/* + /v1/modeling/* | T1-LANDED (x4 rows) |
| orion/jwt/current.json + eclipse JWT | inf-jwt-trigger + inf-exporter EC2 | cron(0 13 UTC) + cron(0 21 UTC) | orion auth + /v1/admin/Token | AUTH-ONLY (no as-of row; recorded here) |

### opal-data-assets (monolith) -- V2 contract 10-family bronze map

| Family | Prefix | Bronze producer | Vendor | Status |
|---|---|---|---|---|
| 3 | orion/inflection/bronze/ (.jsonl.gz) | opal-assets-ingest-mirror Lambda (mirror of opal-data-inf bronze) | orion | T1-LANDED (semantics inherit from firm-bucket rows; mirror adds no vendor call) |
| 4 | eclipse/inflection/bronze/ (.json) | opal-assets-ingest-mirror | eclipse | T1-LANDED (same inheritance) |
| 1-2 | schwab/08242234/bronze/ + schwab/08335338/bronze/ (.zip CRS/CS) | AE OneDrive->S3 sync (49-schwab-conv) + canonical-schwab-si2 EC2 sdd-daily-pull.ps1 (meta/pulls manifests land daily) | schwab | T3 |
| 5 | blackdiamond/cottonwood/bronze/ | opal-assets-ingest-mirror (from opal-data-cot) + cot-rebalancer-runner DIRECT (rebalancer_* families) | blackdiamond | T2-LANDED |
| -- | blackdiamond/49f/bronze/ | opal-assets-bd49f-daily-pull cron(30 2)+(30 4)Z (allocation_390224/fees_435407/template_roster, live thru 07-31) + opal-assets-bd49f-reporting-pull (reporting_*, DRY-gated, one partition 07-17) | blackdiamond | T2-LANDED |
| 6-7 | trueshares/DIVZ/bronze/ + trueshares/IDVZ/bronze/ | ETF chain (etf_conversion.py family) | trueshares | T4 |
| 8 | pathfinder/filepoint/bronze/ (+ live PFDE/ PFOE/ prefixes to reconcile) | ETF chain | pathfinder | T4 |
| 10 | smartx/{platform,model/{guid},account/{guid},allocation/{guid}}/ | smartx-assets-daily-pull Lambda (C5), Scheduler cron(30 9 ET) daily; manifests live thru 2026-08-03 | smartx | T2-LANDED |
| 9 | msn/ | STRUCK (Andrew-direct via COO 182117Z; 0 keys) | -- | CLOSED |

### opal-data-bd / opal-data-cot (legacy partner buckets; D-2 first-class)

| Ingest path | Producer | Vendor | Status |
|---|---|---|---|
| opal-data-bd/forwardfill_v2/{transactions,realized,allocations,unrealized,assets} | bd-49f-runner Lambda (shared cot_bronze_ingest.py firm-bound, LAG=1) via session chain cron(0 0 UTC) + daily belt | blackdiamond | T2-LANDED with U-5 STATUS FLAG (last landings 01-27/06-18 -- retired vs stalled = CTO call) |
| opal-data-cot/forwardfill_v2/{transactions,realized,allocations,unrealized,holdings} + _retry_net | cot-exporter EC2 via SSM opal-cot-bronze-run, session chain cron(30 16 ET); nightly ~22:01 ET | blackdiamond | T2-LANDED |
| opal-data-bd legacy bronze/ + blackdiamond/ prefixes (Andrew manual TRN CSV heritage etc.) | legacy landing surfaces predating the REST migration | blackdiamond | T2-residue (enumerate-and-classify with the U-5 ruling) |

**Denominator coverage after T2: 34 registry rows. opal-data-inf 10/10 data paths (T1);
monolith families 3/3 mirror + smartx 10 routes + blackdiamond 49f monolith 4 feeds (one
UNKNOWN-gated); firm buckets bd 2 rows (U-5 flagged) + cot 3 rows. Open enumeration:
schwab (T3: OneDrive delivery + sdd-daily-pull EC2), trueshares/pathfinder ETF chain (T4),
opal-data-bd legacy prefix classification (rides U-5), out-of-census-bucket smartx
legacy chains (opal-data-smartx-v2 + DDB -- noted, not census scope).**

## 3. UNKNOWNs (loud; also in the registry `unknowns:` block)

| ID | Endpoint | One-line question | Status |
|---|---|---|---|
| U-1 | orion Assets/{date} | Post-open pulls: prior-settled or intraday marks? | **RESOLVED 2026-08-03** by CTO-authorized A/B probe (s.7) |
| U-2 | orion Envision family (5 feeds) | Report-engine value vintage at run time; no as-of field in CSVs | OPEN -- A/B morning-vs-after-close probe, or vendor doc |
| U-3 | orion NewPortfolio | current_value refresh timing | OPEN -- same probe class |
| U-4 | smartx holdings/aum family | Valuation basis (settled custody vs intraday platform marks) at the 09:30 ET pull | OPEN -- A/B within standing SmartX lift, or vendor doc |
| U-5 | blackdiamond 49f firm-bucket plane | Retired vs stalled (last landings 01-27 / 06-18 vs a daily monolith twin) | OPEN -- CTO/AE classification ruling |
| U-6 | blackdiamond portfolioreporting (taxsma) | As-of semantics + cadence behind the DRY_RUN egress gate | OPEN -- egress gate decision + one characterized response |

UNKNOWN count after T2: 5 open (U-2..U-6) + 1 resolved (U-1). None blocks dedup-key
research; each blocks a value-level completeness CERTIFICATION for its feeds -- named
risks, not silent assumptions.

## 4. Findings surfaced by the census (beyond the rows)

1. **Weekend-labeled partitions are live**: daily crons run 7d/week; bronze/assets/
   2026-08-01 (Sat) + 2026-08-02 (Sun) exist and carry Friday's settled state under
   weekend labels (live s3 ls). Any dedup/completeness canon must count NYSE trading days
   and treat weekend partitions as carries. (Registry standing-law block.)
2. **The +47min shift crossed market open** for assets/positions (08:45/08:50 -> 09:32/09:37
   EDT), retiring the seal's literal "pre-open" premise -> U-1. The shift itself was
   deliberate and value-correcting (@b2f61bed83: prior-close settling lag understated AUA
   ~$440K/0.22%).
3. **Dual-producer overlap**: 6 dim feeds have BOTH a per-dim Lambda cron AND the EC2
   orchestrator (cron 30 13) writing the same bronze keys. Live 07-31 landing times match
   the Lambda crons for billing/perf but the _BRONZE_COMPLETE sentinel landed 09:36 ET
   with several dim files landing AFTER it (09:49-10:27) -- single-trigger attribution per
   file is NOT clean. Flagged for WS-5 (which producer satisfies the completeness rule).
4. **transactions.csv for the 07-31 partition was written 08-01 09:47 ET** (next day) --
   consistent with rolling-window re-pull overwriting into a prior date key. WS-4 must pick
   the stable key with this mutation pattern in view (EditedDate rows mutate).
5. **Declarative drift, small but real**: performance puller docstring says "stale since
   2026-04-28" while the feed lands daily; estate census carries pre-shift crons. Neither
   is a data defect; both are records trailing the estate.
6. **Rule 17a-shaped observation (existing, not new)**: opal-data-inf bronze/assets/
   carries .parquet alongside .jsonl.gz. The 17a bucket-policy gate covers opal-data-assets
   only ("partial closure: one bucket" per CLAUDE.md 17a). Not a WS-1 action; recorded so
   the sweep owner sees it.

## 5. Compiler Tools (mandate phases run this tranche)

| Run | Observed | vs expect |
|---|---|---|
| `comp-estate --list` | 29 verticals / 138 chains | PASS (seeded vendor-feeding verticals) |
| `comp-estate advi-inf` | 14 chains; inf-bronze-api-pull + inf-bronze-runner-ec2 producer detail | PASS (chain context seeded; cron drift noted + grounded live per if_mismatch) |
| `comp-glob` inf-pipeline + data/assets/scripts + data/inf/scripts/bronze | 68 + 81 + 6 files | PASS (enumeration denominators printed) |
| `comp-grep` orionadvisor / routes / asof / schedule_expression / opal-data-assets / orion-inflection / mirror | 9/9 pullers route-grounded; 18 TF schedules; monolith writer resolved | PASS |
| `comp-pipescript io mirror_conversion.py` | REFUSED rc=2: --pipeline required; script not under data/*/scripts gold trees | TOOL GAP per if_mismatch: mirror_conversion is an assets-monolith silver module outside the tool's pipeline map; manual source-read with file:line cites substituted (registry rows cite it). Gap noted for WS4-hardening owner. |
| `comp-estate smartx` (T2) | 3 chains: dormant EC2 CSV path (DISABLED rule), model-monthly-pull (DISABLED), REST-daily-ingest (live, feeds opal-data-smartx-v2 + DDB -- out of census buckets) | PASS as seed; the census-scoped monolith producer (smartx-assets-daily-pull) is NOT in this vertical's chains -- estate-census gap noted, grounded via comp-grep + live manifests instead |
| `comp-grep` T2 sweeps (smartx endpoints, BD templates, schedules, meta/pulls grammar) | 9 smartx routes + BD datamining/rebalancer/portfolioreporting flows + all T2 crons grounded file:line | PASS |
| live `aws s3 ls` T2 (monolith smartx/blackdiamond prefixes, both firm buckets, partition tails) | APPLIED evidence per row; surfaced U-5 (bd firm-bucket staleness) + the cot label-forward fact | PASS |
| `comp-blast` (phase 2) | N/A -- census is read-only; zero shared helpers touched; new files only (data/_contracts/ single-writer per TO, this doc, session log) | PASS per expect |
| `comp-validate` (phase 3) | N/A per TO expect (registry draft; no validate config exists) | PASS per expect |

## 4a. T2 findings (SmartX + Black Diamond)

7. **SmartX is the eclipse class**: zero date parameters on any consumed route (pull.py
   url tables) -- every {YYYYMMDD} partition is a run-date label, historical gaps are
   permanently unfillable, and the same false-vintage hazard applies to any backdated
   re-label. Two vendor hazards are already guarded in the puller and now recorded as
   registry facts: the vendor silently ignores unknown modelid filters (returns the
   UNFILTERED universe), and a well-formed-empty payload is a valid landing (the $1.43B
   near-miss -- content bar is a separate instrument).
8. **BD as-of is date-addressed and BACKFILLABLE** (the only census vendor so far where
   history is recoverable), with a measured mechanism: snapshot tables return 0-row
   shells for an as-of not yet completed in ET (4,595B vs 12.9MB A/B in source). 49f
   monolith + firm-bucket runners configure LAG=1 around it.
9. **cot's snapshot tables run LAG=0 -- the latent 0-row-shell exposure is LIVE**, masked
   by the holdings retry-net; CTO-flagged at source (cot_bronze_ingest.py:92-93), now a
   named registry risk on the cot snapshot row.
10. **cot labels lead content by one ET day** (nightly 02:0xZ run labels with UTC
    run-date: TRANSACTIONS_DAILY_2026-08-03.xlsx landed 22:01 ET 08-02) -- filename dates
    on cot period tables are run labels, never content claims.
11. **The bd 49f firm-bucket plane looks superseded, unclassified** (U-5): transactions
    last 2026-01-27, allocations 2026-06-18, while the monolith twin lands daily. Needs a
    one-line retired-vs-stalled ruling.
12. **The taxsma portfolioreporting family is egress-HARD-GATED by design** (DRY_RUN=1
    default; one live partition 2026-07-17) -- recorded as UNKNOWN semantics (U-6), not
    probed.

## 6a. U-1 A/B probe record (run 2026-08-03 21:08Z; CTO authorization 20260803T210542Z)

Read-only; existing endpoint; lifted Orion egress; zero production writes. Script:
session scratchpad `u1_ab_probe.py` (probe design: A = the 09:32 ET production capture
already in bronze; B = fresh Assets/08-03-2026 pull post-close 17:08 ET; C = fresh
Assets/07-31-2026 pull, prior NYSE trading day; 3 sampled clients).

```
jwt issued=2026-08-03T21:01:02Z expires=2026-08-04T07:02:02Z
A-side: bronze/assets/2026-08-03.parquet rows=35219 cols=58 (S3 LastModified 13:35:42Z)
sampled clientIds=[1357, 1408, 522] (asset rows: 6, 7, 9)
per client: asOfDate uniques B(req 08-03)=['2026-08-03'] C(req 07-31)=['2026-07-31']
AvsB (22 common assets): currentValue/currentPrice/currentShares n_diff=0 max_abs=0.0000
BvsC (22 common assets): currentValue/currentPrice/currentShares n_diff=0 max_abs=0.0000
VERDICT: A==B (no intraday movement 09:32->17:08 ET on a traded Monday);
         B==C ({today} request returns prior-settled values; echo mechanism live)
```

Registry updated: assets_v2 grounding block carries the probe; U-1 moved to `resolved:`.
The `_orion_vendor_asof.py` docstring premise refresh routes through COO to the inf-tree
DS lane per CTO instruction -- NOT edited from this seat.

## 6. Next tranches

- **T2 (next)**: SmartX (4 monolith prefixes + exporter chain) + Black Diamond bd/cot
  (both firm buckets + blackdiamond/{49f,cottonwood} monolith families). MDPF_GLOBAL.T4A
  consumes these rows -- tranche-report immediately on landing.
- **T3**: Schwab-0824 (AE-owned OneDrive delivery; census from code/records only, per TO)
  + Schwab-0833.
- **T4**: trueshares, pathfinder (incl. PFDE/PFOE prefix reconciliation), remaining
  monolith residue; final denominator-completeness statement for the CTO gate.
