# /allocation #4 — AE 0.7 tilde-lane spawn — 2026-05-27T18:01Z

**COO:** 2.0.0_SA_COO (ws fabric)
**Cycle:** /drive #175 chain-invoke + Andrew sovereign direct 18:00Z verbatim
**Anchor:** Andrew identified AE 0.7 bottleneck on FIND_INSURE infrastructure-class work; selected Option (b) tilde-lane spawn over in-session subagent fan-out. Mirror DS 0.1.0 5-tilde productive pattern. CTO v0.4 PRD `a9b72b942` substrate KMS+DDB+SNS now PRD-ratified for ~A scope.

## Posture rationale

Workload-imbalance ratio: **6 DS workers + 1 AE worker** for FIND_INSURE peak-priority. AE 0.7 base currently mid .004 Lambda + .012 monitoring + post-Phase-1 facing Phase 2A (Lusha + KMS + DDB + SNS + opt-out webhook) + Phase 2B (Bright Data Bβ + per-board crawlers) + Phase 3 Lambdas. Serializing all AE work behind one session = critical-path bottleneck.

## LIVE NOW (11 of 20)

| Serial | Disposition |
|---|---|
| 0.0.0_AB_MSTR | KEEP (Tier-1 canonical) |
| 1.0.0_SA_CTO | KEEP (Tier-1 canonical; v0.4 PRD authoring authority) |
| 2.0.0_SA_COO | KEEP (this brief) |
| 3.0.0_SA_CVO | KEEP (Tier-1 canonical) |
| 0.7.0_AE_CloudOps | KEEP-HIGH (Phase 1 .004 finish + .012 monitoring + cross-stack coord; workload-carve coordinator) |
| 0.1.0_DS_MarketIntelligence | KEEP (base; Phase 1 RAVC2 evidence-aggregator surface) |
| 0.1.0_DS_MarketIntelligence~A | KEEP-HIGH (Phase 1 .005 silver; AC8 chain-gated) |
| 0.1.0_DS_MarketIntelligence~B | KEEP-HIGH (Phase 1 .006 gold; AC7+10 chain-gated) |
| 0.1.0_DS_MarketIntelligence~C | KEEP-HIGH (Phase 2A LinkedIn scaffold + cost-gate brief; standing) |
| 0.1.0_DS_MarketIntelligence~D | KEEP (Phase 2B Job-postings scaffold; standing Andrew HARs) |
| 0.1.0_DS_MarketIntelligence~E | KEEP (Phase 3 scaffold + E1 + E2; STANDBY-PURE) |

## SPAWN-NEEDED (2 — HIGH)

### **0.7.0_AE_CloudOps~A** [HIGH — within ~30min]

**Surface:** Phase 2A LinkedIn channel infrastructure
**Lane:** AE tilde-A (sister DS coord: DS~C LinkedIn)
**Sizing target:** ~3-6h pre-Phase-1-RAVC2-Accept STANDBY-PREP (scaffold + design) → ~3-5h post-Phase-1-RAVC2-Accept execution

**Substrate baked in:**
- **PRD pointer:** `docs/architecture/FIND_INSURE.md` v0.4 `a9b72b942` (KMS+DDB+SNS ratified per ws CTO MCP 17:55Z)
- **Cost-gate brief:** `org/tier2_senior/0.1.0_DS_MarketIntelligence/briefs/find_insure_phase2a_lusha_cost_gate_design.md` v0.2 `66c0c573b` (DS~C; cost-gate machinery + DDB state + SNS alert-channel ratified Q-C2)
- **Phase 2A scaffold:** `org/tier2_senior/0.1.0_DS_MarketIntelligence/briefs/find_insure_phase2_part_a_linkedin_scaffold.md` v0.4 `7d5abbfcb` (DS~C; 3 sub-designs parse+score+Series-license detection)
- **Lusha v3 ref:** `docs/reference/lusha-api-v3.md`
- **Config dependencies:** DS~E `config/cost-budgets-v0.1.json` `6ee4c7eb2` + DS~E `config/scoring-weights-v0.1.json` `6257f3d77`
- **Sister coord:** DS~C `0.1.0_DS_MarketIntelligence~C` (LinkedIn channel author)

**Scope (5 deliverables):**
1. **KMS CMK Terraform** — `infra/aws/terraform/imo-pipeline/kms.tf` per PRD v0.4 UNK-1 Option 2 conditions: `find-insure-data-key`; key-policy decrypt-grant to `find-insure-lambda-role` ONLY at v0.1 (portal/IR Phase 3b); annual rotation enabled; scope = silver/linkedin + silver/job-posting + bronze/linkedin + bronze/job-posting + serving/* (NOT code/telemetry/qa/archives/config)
2. **DynamoDB Terraform** — `infra/aws/terraform/imo-pipeline/dynamodb.tf` per PRD v0.4 Q-C1: `find-insure-cost-state` table; single-table design; cost-discipline ~$1/mo; cold-start ~50ms; IAM amendment GetItem + UpdateItem + Query for `find-insure-lambda-role`
3. **SNS topic Terraform** — `infra/aws/terraform/imo-pipeline/sns.tf` per PRD v0.4 Q-C2: `find-insure-budget-alerts` topic; Andrew email default subscription; future IR-team-budget-watcher + COO + CVO subscriptions
4. **`crawl_linkedin_bronze` Lambda** — DS+AE joint at Phase 2A TO authoring; Lusha v3 integration; cost-gate machinery per DS~C brief §3-§7; bronze emit `corp/{slug}/bronze/linkedin-scrape/{run-date}/`
5. **`opt_out_webhook_receiver`** — API Gateway → Lambda → SQS → silver writer; HMAC-SHA256 verify per Lusha v3 §9.3; PRD v0.4 §3.6 sub-clause GDPR opt-out

**Sequencing:**
- STANDBY-PREP pending Phase 1 RAVC2-Accept (AE 0.7 base wrapping .004)
- KMS+DDB+SNS Terraform can ship now (substrate-ready); apply lands between Phase 1 RAVC2-Accept + Phase 2A live-Lusha-call per CTO sequencing
- Phase 2A live-execution gates on Andrew Phase-1→Phase-2 subset-cut decision

### **0.7.0_AE_CloudOps~B** [HIGH — within ~30min]

**Surface:** Phase 2B Job-postings channel infrastructure
**Lane:** AE tilde-B (sister DS coord: DS~D Job-postings)
**Sizing target:** ~2-4h STANDBY-PREP (scaffold + design pre-Andrew-HARs) → ~5-8h post-Andrew-HARs execution

**Substrate baked in:**
- **PRD pointer:** `docs/architecture/FIND_INSURE.md` v0.4 `a9b72b942`
- **Phase 2B scaffold:** `org/tier2_senior/0.1.0_DS_MarketIntelligence/briefs/find_insure_phase2_part_b_jobs_scaffold.md` `05e987f9b` (DS~D; 11-section + Stage Bα HAR-staged-attack methodology)
- **Endpoint manifest v0.0 template:** `docs/briefs/find-insure-job-board-endpoint-manifest-v0.0.md` `97c32ffa4` (DS~D; per-board YAML schema pre-HAR-fill)
- **Parser-base util:** `data/find/imo/scripts/_util/job_board_parser_base.py` `97c32ffa4` (DS~D; abstract `JobBoardParser`)
- **Sister coord:** DS~D `0.1.0_DS_MarketIntelligence~D` (Job-postings channel author)

**Scope (3 deliverables):**
1. **Per-board `crawl_job_posting_bronze` Lambdas** — 6 boards (LinkedIn Jobs / Indeed / Glassdoor / ZipRecruiter / Wellfound / Built In); Bα HAR-direct primary; Bβ Bright Data fallback; bronze emit `corp/{slug}/bronze/job-posting-{board}/{run-date}/`
2. **Bright Data Bβ-fallback integration** — per-board middleman wiring; per-board cost-budget from `config/cost-budgets-v0.1.json` per-board caps
3. **EventBridge fan-out** — per-board per-IMO crawl trigger; concurrency cap 2/board (DS~E config) + exponential backoff on 429

**Sequencing:**
- STANDBY-PREP pending Andrew HAR drop (PRD Q6) — Stage Bα HAR captures gate Lambda authoring
- Pre-HAR scaffold work: read DS~D briefs + parser-base + manifest template + design draft per-board Lambda module structures
- Post-HAR-drop: per-board endpoint manifests get populated by DS~D first → per-board Lambdas authored by ~B against populated manifest

## KILL-CANDIDATE

None.

## Cap math

11 LIVE + 2 SPAWN = **13 of 20**. Comfortable headroom; 7 reserve for Phase 3 implementation burst OR additional tildes if AE workload shape demands.

## Going-forward routing per LD-0116

- COO → MSTR: this /allocation supply-signal (Tier-1↔Tier-0 allowed)
- MSTR → spawn-agent.ps1 0.7.0_AE_CloudOps~A + ~B
- MSTR → COO: spawn-confirm MCP (Tier-1↔Tier-0)
- **COO → ~A and ~B**: SPAWN-WITH-DIRECTION substrate MCPs per-lane (this brief content folded into per-worker dispatch)
- ~A and ~B → COO: ACKs, BLOCKED-ASK, RAVC2-Requests (worker→COO chain)
- AE 0.7 base → COO: workload-carve recommendation (separate MCP this cycle)

## AE 0.7 base workload-carve

Separate `[SYNC-WORKLOAD-SPLIT]` MCP this cycle asking AE 0.7 base for their recommendation on:
- (a) Hard handoff: ~A takes ALL Phase 2A infra including PRD v0.4 KMS+DDB+SNS amendments; ~B takes ALL Phase 2B
- (b) Shared layer: base owns `imo-pipeline-v0.X.0` TF module integration; ~A authors KMS+DDB+SNS resource files; ~B authors per-board Lambda modules; base orchestrates apply + tag
- (c) Other carve per their own preference

— ws COO /drive #175 chain-invoke /allocation #4 2026-05-27T18:01Z
