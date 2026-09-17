# Owner cards -- `astn`, `news`, `trade` stay `unresolved`, EN-r-5-r3

**Author:** `0.9.0_WK_LGIC_ENFORCE~2`. Per R-6 s.3 (`SELF_DRIVE_LGIC_RULINGS_20260916.md` :229-238):
"A token whose resources link to NO directive stays `unresolved` with the MEASURED fact written
into its `why`, and the cell returns ONE card to Andrew naming the owner question per such token."
Each card below is that return. Each `why` is already landed in
`infra/logic/registry/systems.json` `unresolved`; this file is the standalone card, one per token.

---

## Card 1 -- `astn`

**Question for Andrew: who owns the `astn` resource family (14 live resource names --
`infra/aws/terraform/astn-pipeline/`, the `astn-wsjft-orchestrator`/scraper EC2 pair, secrets under
`astn/*`) now that `ASTN_WSJFT` is closed?**

**Measured, not guessed:**
- `ASTN_WSJFT` (`org/projects/ASTN_WSJFT.json`) is the only project this resource family traces to.
  It is a LEGACY FLAT project (`org/projects/`, not `org/missions/D<n>/`), carries NO
  `org/missions/DIRECTIVES.yaml` line (0 hits on `ASTN` there, `comp-find` denominator = 1 file
  scanned) and NO `org/missions/MACROS.yaml` entry.
- Its own `status`/`phase` fields read `closed`, "SPRING CLEAN, Andrew-direct ~18:24Z + ~18:4xZ: a
  project not attached to `org/missions/DIRECTIVES.yaml` is closed rather than left floating
  unaddressed as live... Recovery is explicit: 'we can reinvent a project'."
- Its `owner` field names a SEAT, `0.7.0_AE_CloudOps` (assigned 2026-08-19 by `0.0.0_AB_MSTR` via
  LD-0090, "an empty owner field measured as the DRIFT GENERATOR") -- a seat, not a directive; the
  registry's `owner_claim` contract (`systems.json` `_about.row_fields`) needs a D-code resolving in
  `DIRECTIVES.yaml`, which a seat assignment cannot supply.
- The pipeline itself reads LIVE and OPERATIONAL as of its last update (autonomous 3am-ET schedule
  ENABLED 2026-06-25) -- this is not a dead resource, it is a live one with no directive claimant.

**Why this cell does not write D5 or any other code:** `AMGT_RESAPP`'s project.json lists
`ASTN_WSJFT` under `related` (a cross-reference, not a subordination -- the same field also lists
`ADVI_BDAPIMIG.P1` and `D5_ALT_RESEARCH`, neither of which AMGT_RESAPP owns either), and no D<n>
mission-tree project's `related`/`prds`/`decompositions` names `astn` as ITS resource. Inferring D5
(or any D-code) from the `related` cross-reference alone is exactly the guess R-6 s.3's closing
line refuses: "an inferred owner without a citation is the guess the registry's `owner_claim` field
exists to refuse."

**Disposition:** `astn` stays `unresolved` in `systems.json`, `why` updated to this measured state
(commit alongside this card). Recovery path per `ASTN_WSJFT`'s own closure note: "we can reinvent a
project" -- either re-register `ASTN_WSJFT` under a D<n> directive, or fold its resource family
into an existing directive's mission-tree project, Andrew's call.

---

## Card 2 -- `news`

**Question for Andrew: who owns the `news` resource family (34 live resource names --
`infra/aws/terraform/news-pipeline/`'s 7 Lambdas + 24 EventBridge rules, `tools/news_scanner`)?**

**Measured, not guessed:**
- `org/missions/DIRECTIVES.yaml` carries 0 hits for `news`, `trending`, `sentiment`,
  `keyword.intelligence` or `news.pipeline` (case-insensitive, `comp-find`, denominator = 1 file
  scanned each pattern) -- no directive's projects line names this resource family.
- The only project-shaped relation this family carries is to `ASTN_WSJFT` (Card 1: closed,
  unregistered, seat-owned) -- `org/tier1_exec/2.0.0_SA_COO/deliverables/
  UNOWNED_CODE_ASTN_WSJFT_NEWS_SCANNER_20260819.md` is a durable COO carry stating this directly:
  "`tools/news_scanner`'s last 12 commits span SIX authors" including a RETIRED serial
  (`2.1.0_SA_COO`), and "`ASTN_WSJFT` -- the consumer project, `status: active` [at that 2026-08-19
  census] -- carries NO DECLARED OWNER in its registry entry... these rows had no claimant because
  there is nobody to claim them." Its own generalisation: "A REGISTRY ENTRY WITH NO OWNER IS NOT A
  METADATA GAP -- IT IS A GENERATOR."
- `ASTN_WSJFT` has since (2026-08-19, same day) been assigned a SEAT owner (Card 1) and then
  (2026-08-25) CLOSED for being unregistered -- so the ownership gap that 2026-08-19 record
  documented is, as of this cell, unresolved in the direction that matters for `systems.json`
  (a directive, not a seat).
- A recent (2026-09-16) deep-dive, `org/tier2_senior/0.1.0_DS_MarketIntelligence/deliverables/
  NEWS_SCANNER_DEEP_DIVE_20260916.md`, traces the live pipeline end to end on Andrew's direct ask
  but does not itself claim or assign a directive; its author's own seat is a DS pod, not itself a
  directive-owning role.

**Disposition:** `news` stays `unresolved`, `why` updated to this measured state. The underlying
condition is the SAME one the 2026-08-19 carry named for `ASTN_WSJFT`: an unowned code family
accretes contributions and reads as backlog. This card does not re-open that carry's remediation
(already routed, per that file's Disposition section); it names the SAME gap surfacing here as a
naming-registry question, one level up.

---

## Card 3 -- `trade`

**Question for Andrew: who owns the `trade` resource family (22 live resource names --
`infra/aws/terraform/trade-pipeline/`'s 11 Lambdas, 5 S3 buckets, 3 DynamoDB tables)?**

**Measured, not guessed -- and R-6's own hypothesis is FALSIFIED:** R-6 s.1 flagged `trade` as
"plausibly the TRADEOPS second fabric's product (its own root and broker), i.e. possibly not this
register's row at all." Measured this cell:
- `infra/aws/terraform/trade-pipeline/lambdas.tf` :1-14 declares its 11 Lambdas S3-backed from
  `s3://opal-313476888478-lambda-artifacts/trade-pipeline/` (4 functions, "repo source reclaimed,
  TRSB_TFIMPT.W2 / TRSB_LEDGER.001 / TRSB_LEDGER.003") or `EXTERNAL` (7 functions, no repo source,
  console-deployed) -- every source is inside `ajb_workspace` (this repo) or an S3 bucket this
  repo's Terraform manages.
- The "TRADEOPS second fabric" (per this device's memory record
  `project_tradeops_is_a_second_fabric_ajb3_ajb4_own_root_env_var_and_broker_port_7801.md`) is a
  wholly SEPARATE git repository, `Opal-Capital/tradeops` at `C:/Users/AndrewBerman/Downloads/
  docs_abcdeg`, established 2026-09-11 for AGENT ORCHESTRATION (Claude/Codex seats, its own broker
  port 7801, its own MCP channel) -- it is not a business/trading pipeline and shares nothing with
  `infra/aws/terraform/trade-pipeline/` beyond the English word "trade". **The R-6 hypothesis does
  not survive measurement: this `trade` is not that fabric's.**
- The projects this family traces to -- `TRSB_LEDGER`, `TRSB_TFIMPT`, `TRSB_PATHFIX`
  (`org/projects/TRSB_LEDGER.json`, `TRSB_TFIMPT.json`, `TRSB_PATHFIX.json`) -- are LEGACY FLAT
  (`org/projects/`, not `org/missions/D<n>/`), carry 0 `org/missions/DIRECTIVES.yaml` hits on
  `TRSB` (comp-find, denominator = 1 file scanned), and their task orders/logs name SEAT owners
  (`0.7.0_AE_CloudOps`, `0.3.0_DT_TradingOperations`, `0.5.0_AE_OpalETL`), not a directive.

**Disposition:** `trade` stays `unresolved`, `why` updated to record BOTH the falsified tradeops
hypothesis and the measured legacy-flat/seat-owned state. This is a DIFFERENT owner-gap shape than
Cards 1-2 (no single unowned-code carry exists for `trade`/TRSB yet) -- surfaced here as its own
question, not folded into theirs.

---

## Disposition summary

All three tokens (`astn`, `news`, `trade`) stay `unresolved` in `infra/logic/registry/systems.json`
with a NEW, measured `why` (landed same commit as this file). None resolves to a `PRODUCT` row
this cell can write without guessing a D-code the estate does not, at this cut, declare.
