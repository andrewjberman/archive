# /allocation — FIND_INSURE peak-priority spawn — 2026-05-27T16:47Z

**COO:** 2.0.0_SA_COO (ws fabric)
**Cycle:** /drive #170 chain-invoke + Andrew sovereign direct 16:46Z verbatim "FIND_INSURE Stages 1-3 done asap; agents on this NOW"
**Anchor:** SOVEREIGN-OVERRIDE 16:40Z (CVO ADDITIVE-2 vacated) + Andrew explicit peak-priority dispatch 16:46Z

## Posture

DEMOV1 demoted to background. FIND_INSURE Phases 1 (web-scrape) + 2 (LinkedIn + Job-postings) + 3 (consolidated serving) is the entire operational priority. All capacity rotates to FIND_INSURE.

## LIVE NOW (7 of 16)

| Serial | Disposition |
|---|---|
| 0.0.0_AB_MSTR | KEEP (Tier-1 canonical) |
| 1.0.0_SA_CTO | KEEP (Tier-1 canonical; Phase 1+2+3 architectural authority) |
| 2.0.0_SA_COO | KEEP (this brief) |
| 3.0.0_SA_CVO | KEEP (Tier-1 canonical; Phase 1+2+3 verifier authority) |
| 0.7.0_AE_CloudOps | KEEP-HIGH (firing FIND_INSURE.001+.003 NOW; Phase 1+2 Lambda orchestration + Bright Data + Lusha + job-board HAR-endpoint; load-bearing for all 3 Stages AE-side) |
| 0.1.0_DS_MarketIntelligence | KEEP-HIGH (FIND_INSURE.002+.002b shipped; will coordinate Phase 1 parse + Phase 2 LinkedIn subset + Phase 3 consolidated serving; load-bearing for all 3 Stages DS-side) |
| 0.4.0_DS_ClientPlatform~D | **KILL-CANDIDATE** (DEMOV1 Phase 4 RAVC2 prep no longer urgent per Andrew demote; ClientPlatform domain not a fit for FIND_INSURE MarketIntelligence work; free capacity for FIND_INSURE tilde-lanes) |

## SPAWN-NEEDED (urgency-ordered)

### HIGH — within ~30min (Phase 1 parallelism)

**0.1.0_DS_MarketIntelligence~A** [HIGH]
- **Why:** Phase 1 `parse-web` Lambda authoring (HTML structure → silver). Per-IMO bronze HTML → page-text + link-graph + title/meta/headings + structured address blocks. ~3-5h Lambda development sizing.
- **Substrate baked in:** PRD v0.3 §3.4 + §4 Phase 1 deliverable 2; data/find/imo/scripts/silver/web-scrape/ landing path per medallion convention; `_util/slugify.py` for path determination; parallel to ~B `score-web`.
- **Spawn-with-direction:** "FIND_INSURE Phase 1 parse-web Lambda; PRD v0.3 §3.4 + §4 deliverable 2; silver-tier HTML structure extraction; landing at silver/web-scrape/{slug}/{run-date}/; parallel to ~B score-web; standing for AE 0.7 .001 RAVC2 + .004 crawl-web bronze output."

**0.1.0_DS_MarketIntelligence~B** [HIGH]
- **Why:** Phase 1 `score-web` Lambda + asset-management-transition indicator-term taxonomy (gold tier). Term-class taxonomy IS itself a deliverable per PRD v0.3 §4 Phase 1 deliverable 3.
- **Substrate baked in:** PRD v0.3 §4 Phase 1 deliverable 3 (15+ initial seed terms including RIA, Series 65/66/7/24, Form ADV, AUM, model portfolio, TAMP, IAR, fiduciary); gold-tier write at gold/web-scrape/{slug}/{run-date}/.
- **Spawn-with-direction:** "FIND_INSURE Phase 1 score-web Lambda + indicator-term taxonomy authoring; PRD v0.3 §4 Phase 1 deliverable 3; gold-tier write; parallel to ~A parse-web; sister-coordinate with ~A on silver→gold contract."

### MEDIUM — within ~60min (Phase 2 prep + advance scaffold)

**0.1.0_DS_MarketIntelligence~C** [MED]
- **Why:** Phase 2 Part A LinkedIn channel design (parse-linkedin + score-linkedin Lambdas + Series-license detection). Pre-spawn for scaffolding-while-Phase-1-runs.
- **Substrate baked in:** PRD v0.3 §4 Phase 2 + Lusha v3 doc at `docs/reference/lusha-api-v3.md`; endpoint mapping (Search+Prospecting+Enrich+S&E for Part A); ADDITIVE-1 named-IR-individual pre-Phase-3 gate noted but not blocking Phase 2 scaffold.
- **Spawn-with-direction:** "FIND_INSURE Phase 2 Part A LinkedIn channel scaffold; PRD v0.3 §4 Phase 2 + Lusha doc; standing for Phase 1 subset-cut decision (Andrew gate); scaffold parse-linkedin + score-linkedin Lambda designs + Series-license-detection regex/NLP draft; ship design brief pre-Phase-2-execution-trigger."

**0.1.0_DS_MarketIntelligence~D** [MED]
- **Why:** Phase 2 Part B Job-postings channel design (Stage Bα HAR-staged-attack methodology). Pre-spawn for parallel-prep alongside ~C LinkedIn.
- **Substrate baked in:** PRD v0.3 §4 Phase 2 Part B + Stage Bα HAR-primary methodology + Q6 HARs-from-Andrew pre-gate; investment-keyword + Series 63/65/66/7 + corp-finance/tech-hire detection per Andrew "begets m&a/growth activity" framing.
- **Spawn-with-direction:** "FIND_INSURE Phase 2 Part B Job-postings scaffold; PRD v0.3 Stage Bα HAR-staged-attack; standing for Andrew HARs (Q6 pre-gate); scaffold parse-jobs + score-jobs Lambda designs + investment-keyword taxonomy draft + union-schema across job-boards; ship design brief pre-Phase-2-execution-trigger."

**0.1.0_DS_MarketIntelligence~E** [MED]
- **Why:** Phase 3 consolidated serving-build design (companies/employees/scoring tables + relevance-scoring formula). Pre-spawn for parallel-prep.
- **Substrate baked in:** PRD v0.3 §4 Phase 3 + relevance-scoring formula sketch (Employee score = f(years_at_company, title_seniority, series_license_count_weighted, title_keyword_match); Company score = aggregate); ADDITIVE-1 IR-named-individual gate noted for AC5.
- **Spawn-with-direction:** "FIND_INSURE Phase 3 consolidated serving-build scaffold; PRD v0.3 §4 Phase 3; design companies.{json,parquet} + employees.{json,parquet} + scoring.{json,parquet} schemas + join logic + relevance-scoring v0.1 weights; standing for Phase 2 close + ADDITIVE-1 IR-individual gate."

## KILL-CANDIDATE detail

**0.4.0_DS_ClientPlatform~D** — DEMOV1.012 Phase 4 RAVC2 prep was the standing role. Andrew demoted DEMOV1; FIND_INSURE peak priority. ~D's ClientPlatform domain not a fit for FIND_INSURE MarketIntelligence work. AE 0.7 can ship single-author .012 RAVC2 when Fire 1 terminal fires (vs joint with DS~D); not ideal but acceptable per priority shift. Freed slot reallocates to DS 0.1.0~A/~B/~C/~D/~E spawn capacity.

## Cap math

Current 7 LIVE - 1 KILL + 5 SPAWN = **11 of 16**. Comfortable; headroom for AE 0.7~B if Phase 1 crawl-web capacity bottlenecks (defer to /allocation #5 if needed).

## Sequencing

1. MSTR KILL 0.4.0_DS_ClientPlatform~D
2. MSTR SPAWN ~A + ~B (HIGH; parallel; Phase 1 critical-path)
3. MSTR SPAWN ~C + ~D + ~E (MED; parallel; Phase 2/3 advance scaffolding)
4. All ~A through ~E receive SPAWN-WITH-DIRECTION substrate per per-serial specs above
5. AE 0.7 continues firing .001+.003 in parallel with /allocation execution; AE 0.7 will receive Phase 1 .004 crawl-web TO from me once Phase 1 design from ~A/~B converges

## Tier-1 supervision parallel

ws CTO authoring Phase 1+2+3 TOs (TO triad .004/.005/.006 + Phase 2 design briefs + Phase 3 scaffold) in parallel to spawn-execute.
ws CVO verify-channel on Phase 1 RAVC2 (gold/web-scrape 4-check) at Phase 1 ship moment.
COO drives the multi-lane dispatch + RAVC2 chain.

— ws COO /drive #170 chain-invoke /allocation 2026-05-27T16:47Z
