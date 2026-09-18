# REGISTRY_TOKEN_CLASSES -- EN-r-2 RULING ROWS over the RAISE population

**Cell:** `EN-r-2` (LGIC_ENFORCE round 2, decomposition v2.1 @`8e0d09e418` s.0b), task order
`LGIC_ENFORCE.TO-EN-r-2-r2`, written by `0.9.0_WK_LGIC_ENFORCE~1`.

**Population:** every group of `fixed_inputs/r2/RAISE_POPULATION.json`'s `union_groups` (152 groups,
live 115 / repo 134, 37 repo-only), each a token a RAISE message quotes, at registry@`ba5318901b937130`.
`token:gateway` is excluded: it is `EN-r-5`'s pre-landed row and is in no group at this registry.

**Method.** Each group was classed by (1) reading the group's live+repo `examples` (name, type, raise
step) in full, not truncated; (2) for every candidate class (a)/(b)/(c), EMPIRICALLY TESTING in a scratch
copy of `lib/opal_naming.py` + the registry whether the proposed registry action actually silences EVERY
example of that group (Rule 22 discrimination -- the claim is falsifiable, and several plausible
classifications were falsified this way, see below); (3) citing the estate's own evidence (repo file
paths, `docs/architecture/*_PRD.md`, `org/missions/DIRECTIVES.yaml`, `infra/logic/05_IDENTITY_SPINE.md`
s.3, `infra/logic/09_NAMING_CENSUS.md` s.3) for every class (a) and workstream-shaped class (b) call.

**A finding this cell had to make before classifying anything:** `B2` (a data bucket's scope) and `K1`
(an S3Key's segment 1) accept ONLY a V1 token (a registered system) -- `refused_keys` (V3) membership
does **not** satisfy either clause. This is not stated plainly in `GRADING_RULE.md`'s prose, so it was
tested directly rather than assumed: adding `'pm'` to `refused_keys.generic_noun` in a scratch copy left
`grade('opal-data-pm', 'S3_BUCKET')` RAISING unchanged, and adding `'sentiment'` left
`grade('sentiment/keyword-sentiments.json', 'S3Key')` RAISING unchanged. Independently, two tokens already
LIVE in `refused_keys.generic_noun` before this cell ran -- `ec2` and `infrastructure` -- both still raise
via `K1` in this same population, which is direct, no-action-needed confirmation of the same fact. **This
governs every class (d) call below**: a group whose examples include a `B2`, `K1`, `R8`, `L2` or `G2.3`
raise cannot be moved to class (a)/(b)/(c) unless EVERY one of its examples would also resolve (which, for
`B2`, means becoming a genuine `PRODUCT` -- never asserted here without directive evidence -- and for `K1`/
`R8`/`L2`/`G2.3`, is not achievable by any registry row at all).

**Classes, MECE by subtraction from the printed 152-group union (`Rule 24(i)`):**
- **(a) system rows -- 7**: five PLATFORM_SUBSYSTEMs (`agentbus`, `cmtque`, `estate`, `firmsep`,
  `globgrph`) and two VENDORs (`bloomberg`, `msci`), each backed by repo evidence of an ongoing,
  cross-cutting capability (tooling used estate-wide, or a financial-data feed), never tied to one
  completed project. Every step these 7 tokens raise on (`R1.c`, `R2`) is resolved once the token is V1;
  none of the 7 carries a `B2`/`K1`/`R8`/`L2`/`G2.3` example.
- **(b) workstream/project codes and generic nouns/purpose words -- 93**: `S6`/`NAMING_SCHEMA.json
  system.never_a_system` govern this whole class (firm forms, project codes, workstream codes, cadences,
  generic nouns are its members; `refused_keys` is the ONE registry destination for all of them). Eight
  are named, evidenced workstream/project codes (`canonical`, `consolidation`, `gldinc`, `quartz`,
  `opsec`, `outset`, `semantic`, `wp5`); the remaining 85 are ordinary generic nouns/purpose words used as
  IAM-policy/resource-name prefixes, added to `refused_keys.generic_noun` alongside the 8 already there.
  Every one of these 93 raises PURELY via `R1.f`/`R1.c`/`R1.d`/`R2` (resource-grammar steps V3 resolves);
  none carries a `B2`/`K1`/`R8`/`L2`/`G2.3` example (verified by full step-set, not just the printed
  examples).
- **(c) library -- 0**: `R1.e` (LAMBDA_LAYER only) applies to no group here; zero of the population's 517
  examples are typed LAMBDA_LAYER (measured, denominator printed).
- **(d) rule gap, stays a loud RAISE -- 46**: 27 pure-`K1` path-segment tokens (see the `_K1_GROUP_NOTE`
  entry of `why`, below); 5 `R8` `X#policy`-on-a-bucket tokens; 3 `L2` log-group-service tokens (`opal`,
  `vendedlogs/pipes`, and `vpc` mixed with `R1.f`); 1 `G2.3` code/doc-divergence token
  (`aws-waf-logs-opal-cloudfront`); 5 `B2`-bearing tokens that are not defensible PRODUCTs (`pm`,
  `portfolio`, `research`, and `portal`/`security` mixed with `R1.f`); 2 `K1`-mixed tokens (`cache`,
  `sentiment`); `otp` (pure `K1`, despite resembling `D12_PHONE_OTP_ALL_AWS`'s subject -- the mechanism
  does not reach it); and `f49`, a garbled alias of the scope `49financial`'s short `49f`, not a word.
- **(undecided) -- 6, listed under `for_1.0.0_SA_CTO`**: `astn`, `trade`, `news` (row
  `LGIC_ENFORCE-W1-S6`: `GRADING_RULE.md` V1 names them PRODUCT candidates, but no `DIRECTIVES.yaml` line
  and no mission-tree project names an owner -- CENSUS measured 0 hits for each) and `find`, `harvest`,
  `imo` (`infra/logic/05_IDENTITY_SPINE.md` s.3 tick-list row 18: doctrinally UNRESOLVED whether each is a
  product, a vendor, or retired). None of these 6 is touched in the registry: they remain exactly as they
  sit in `systems.json`'s `unresolved` list, so they stay a loud RAISE (AC5) and the open question travels
  to the CTO undecided rather than guessed.

**What moved in the registry** (`infra/logic/registry/systems.json`): the 7 class (a) rows were added to
`systems`; the 8 workstream/project codes were added to `refused_keys.workstream_code`; the 85 generic
nouns/purpose words were added to `refused_keys.generic_noun`; all 11 of those tokens (5 class-a + 6
class-b, of the 17 that were `unresolved` V2 tokens) were removed from `unresolved`. The 6 undecided
tokens (all V2) are untouched, still `unresolved`. `python lib/opal_naming.py validate` reads `VALIDATE:
OK 24 system row(s), 9 scope row(s), 16 warning(s)` -- every warning is an `owner_directive ... is
inferred, owed a confirmation` line (the same shape carried by the 9 pre-existing inferred rows), never a
REFUSED line.

```json
{
 "population": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/RAISE_POPULATION.json",
 "classes": {
  "a": [
   "token:agentbus",
   "token:bloomberg",
   "token:cmtque",
   "token:estate",
   "token:firmsep",
   "token:globgrph",
   "token:msci"
  ],
  "b": [
   "token:aaii",
   "token:access",
   "token:additional",
   "token:ai",
   "token:anthropic",
   "token:auth",
   "token:bounded",
   "token:brightdata",
   "token:bronze",
   "token:by",
   "token:canonical",
   "token:code",
   "token:codebuild",
   "token:comp",
   "token:conferenceboard",
   "token:consolidation",
   "token:cost",
   "token:cse",
   "token:data",
   "token:ddb",
   "token:deck",
   "token:derive",
   "token:describe",
   "token:drift",
   "token:dynamo",
   "token:ecr",
   "token:ecs",
   "token:events",
   "token:fargate",
   "token:fear",
   "token:fedobs",
   "token:finbert",
   "token:github",
   "token:gldinc",
   "token:gold",
   "token:google",
   "token:incremental",
   "token:incrparity",
   "token:jwt",
   "token:keyword",
   "token:layer3",
   "token:massive",
   "token:moltbot",
   "token:monitor",
   "token:monolith",
   "token:multi",
   "token:nessie",
   "token:nopecha",
   "token:opalinvest",
   "token:openai",
   "token:opsec",
   "token:outset",
   "token:partner",
   "token:partners",
   "token:pipeline",
   "token:price",
   "token:projection",
   "token:public",
   "token:publish",
   "token:quartz",
   "token:quo",
   "token:rds",
   "token:recheck",
   "token:resource",
   "token:runner",
   "token:self",
   "token:semantic",
   "token:send",
   "token:served",
   "token:ses",
   "token:shared",
   "token:sms",
   "token:sns",
   "token:sqs",
   "token:sscn",
   "token:ssm",
   "token:start",
   "token:stitch",
   "token:surface",
   "token:test",
   "token:tier",
   "token:trending",
   "token:trino",
   "token:twilio",
   "token:unknown",
   "token:user",
   "token:volatility",
   "token:website",
   "token:workspace",
   "token:wp5",
   "token:x",
   "token:yfinance",
   "token:yield"
  ],
  "c": [],
  "d": [
   "token:%s",
   "token:_quarantine",
   "token:agendas",
   "token:allowlists",
   "token:aws-waf-logs-opal-cloudfront",
   "token:backfill_v2",
   "token:benchmarks",
   "token:cache",
   "token:config",
   "token:consolidated",
   "token:contract_integrity",
   "token:daily",
   "token:daily-reports",
   "token:data-refresh",
   "token:ec2",
   "token:exports",
   "token:f49",
   "token:forwardfill_v2",
   "token:infrastructure",
   "token:investor-reporting",
   "token:json",
   "token:json-tiered",
   "token:macro",
   "token:opal",
   "token:opal-cloudtrail-logs-313476888478",
   "token:opal-cur-313476888478",
   "token:opal-security-evidence",
   "token:opal-served-key-write-trail-logs",
   "token:opalinvest-portal",
   "token:otp",
   "token:pm",
   "token:portal",
   "token:portfolio",
   "token:quarantine",
   "token:research",
   "token:security",
   "token:security-reports",
   "token:semantic_clusters",
   "token:sentiment",
   "token:timeseries",
   "token:trending_reports",
   "token:uploads",
   "token:vendedlogs/pipes",
   "token:views",
   "token:vpc",
   "token:warehouse"
  ],
  "undecided": [
   "token:astn",
   "token:find",
   "token:harvest",
   "token:imo",
   "token:news",
   "token:trade"
  ]
 },
 "counts": {
  "a": 7,
  "b": 93,
  "c": 0,
  "d": 46,
  "undecided": 6
 },
 "for_1.0.0_SA_CTO": [
  "token:astn",
  "token:find",
  "token:harvest",
  "token:imo",
  "token:news",
  "token:trade"
 ],
 "why": {
  "token:agentbus": "PLATFORM_SUBSYSTEM: .tools/agentbus-consumer.py + agentbus-sqs.sh, the cross-device agent messaging bus (OPAL_SQSCHAT); DIRECTIVES.yaml :146 names 'the agentbus'. Owner D0 (Agent Infrastructure) inferred: no DIRECTIVES.yaml projects line names it.",
  "token:cmtque": "PLATFORM_SUBSYSTEM: infra/aws/terraform/shared-infra/cmtque-alarms.tf, the commit-queue worker behind safe-commit.sh's shared-index serialization (CLAUDE.md 14b). Owner D0 inferred.",
  "token:estate": "PLATFORM_SUBSYSTEM: infra/aws/ec2/estate-report-runner/, the estate-wide freshness/comp report runner, the subject of D11's NFRA_OUTSET/NFRA_COMPEFFICACY briefs. Owner D11 inferred.",
  "token:firmsep": "PLATFORM_SUBSYSTEM: .tools/comp-firmsep-sweep(.py), the cross-firm credential-isolation sweep behind CLAUDE.md's cross-firm-data hard stop. Owner D0 inferred (comp-* tooling, D0 also holds NFRA_COMPTOOLS).",
  "token:globgrph": "PLATFORM_SUBSYSTEM: docs/architecture/NFRA_GLOBGRPH_PRD.md, infra/aws/globgrph/, ECS cluster opal-globgrph -- the estate-wide dependency graph behind Rule 20 and comp-find. Largest V2 group (67 live names). Owner D0 inferred: NFRA_CLDGRPH is D0's current graph project; NFRA_GLOBGRPH is not itself a live DIRECTIVES.yaml line, read as the same subsystem's earlier project code.",
  "token:bloomberg": "VENDOR: a financial-data feed vendor (integrations/bloomberg/READ_HERE.md). No directive names it as its own; read as D8's by the same inference already carried by the 8 existing feed VENDOR rows.",
  "token:msci": "VENDOR: a financial-data feed vendor (msci-api-credentials). Same D8-inferred basis as the other feed VENDOR rows.",
  "token:consolidation": "workstream/project code: DIRECTIVES.yaml :392 names the 'Global Pipeline Consolidation' work, whose one project moved to D8; resources (consolidation-gold-runner) are that workstream's runner, not an independent system.",
  "token:canonical": "workstream/project code: the canonical-prices / canonical-schwab-si2 firm-data canonicalization workstream (data/assets/docs/SCHWAB_AUTO_PULL_DESIGN.md); org/tier2_senior/.../andrew_direct_canonical_prices_deprecation_141xZ.md records it DEPRECATED -- a retired workstream whose resources still bear its code (CENSUS s.3: 'a project code in a resource name outlives the project').",
  "token:gldinc": "workstream/project code: 'gold incremental' -- the bd/cot gold-layer incremental-load workstream (docs/architecture/ADHC_GLDINC_PRD.md, data/black_diamond/scripts/gold/gldinc_*.py, data/cot/scripts/gold/gldinc_*.py); a named pipeline-build initiative, not a distinct vendor/product.",
  "token:quartz": "workstream/project code: the Schwab si2 auto-pull spike/box project (ADVI_SCHWABAUTO, per org/critical_paths/change_management/2026070*_schwab-si2-*.md, 'quartz-si2-spike-role'), the same project 'canonical-schwab-si2' also names -- a retired/completed project's code still on its resources.",
  "token:opsec": "workstream/project code: matches D12's active project NFRA_OPSEC202609 exactly; the OPSEC-auth-* CW_ALARMs are that project's own literal deliverable (security-ops alerting), not a system other products build on.",
  "token:semantic": "workstream/project code: the semantic-clustering stage of the news processing pipeline (news-ingestion -> sentiment -> semantic-clustering -> layer3-curation -> keyword-intelligence, org/tier1_exec/.../SEMANTIC_NOTES_ddb_tables.md); a pipeline stage/build-workstream tied to the (undecided) news product, not an independent system.",
  "token:outset": "workstream/project code: matches D11's active project NFRA_OUTSET exactly (outset-drift-publisher-laptop is that project's own tooling).",
  "token:wp5": "workstream code: 'WP5' (work-package numbering), the same shape as the already-registered wsb/wsd workstream codes.",
  "token:f49": "not a generic word: a reversed/misspelled form of the scope 49financial's sanctioned short 49f (V4 short is '49f', never 'f49'); this is a genuine alias defect the rule correctly keeps loud, not a word for refused_keys -- adding it there would misrepresent it as a generic noun.",
  "token:opal": "L2 rule gap: LOG_GROUP '/opal/github-actions-runner' does not begin /aws/; L2's service table has no entry for a bare /opal/ path, and no registry row supplies one.",
  "token:vendedlogs/pipes": "L2 rule gap: the L2 service table maps vendedlogs/states -> STATE_MACHINE but carries no entry for vendedlogs/pipes; a registry row cannot add an L2 service mapping.",
  "token:aws-waf-logs-opal-cloudfront": "G2.3 rule/doc gap: GRADING_RULE.md's G2 documents only G2.1/G2.2; the live grade() raises via a 'G2.3' this rule does not document, on a name G2.1's own text ('a LOG_GROUP ... whose name begins aws-waf-logs-') reads as excluded -- a code/doc divergence, not a vocabulary gap.",
  "token:opal-cloudtrail-logs-313476888478": "R8 rule gap: 'X#policy' bucket-shaped resource policies (a platform bucket per B3) RAISE instead of being graded by section B as R8 directs ('Grade X by the grammar of the resource it names'); same defect on all 5 R8 examples in this population.",
  "token:opal-cur-313476888478": "R8 rule gap, same defect as opal-cloudtrail-logs-313476888478.",
  "token:opal-security-evidence": "R8 rule gap, same defect as opal-cloudtrail-logs-313476888478.",
  "token:opal-served-key-write-trail-logs": "R8 rule gap, same defect as opal-cloudtrail-logs-313476888478.",
  "token:opalinvest-portal": "R8 rule gap, same defect as opal-cloudtrail-logs-313476888478 (X#policy on a bucket-shaped resource).",
  "token:pm": "B2 rule gap: 'opal-data-pm' -- B2 accepts only a V4/MASTER/global scope or a PRODUCT in V1 for a data-bucket's scope; 'pm' is none, and (empirically verified) adding it to refused_keys does not silence a B2 raise -- only V1/PRODUCT membership would, which is not defensible here.",
  "token:portal": "B2 rule gap (mixed with R1.f): 'opal-data-portal-s3' fails B2 the same way as pm; the R1.f examples alone would resolve via refused_keys, but the B2 example would not, so the group as a whole stays class (d) (AC4 requires every example to resolve).",
  "token:portfolio": "B2 rule gap, same as pm -- 'portfolio' is ALREADY a registered generic_noun and 'opal-data-portfolio' still raises via B2 at this population (empirical proof that refused_keys cannot fix a B2 raise).",
  "token:research": "B2 rule gap, same as pm ('opal-data-research').",
  "token:security": "B2 rule gap (mixed with R1.f): 'opal-data-security' / 'opal-data-security-access-logs' fail B2 the same way as pm; mixed group stays class (d) for the same reason as portal.",
  "token:cache": "K1 rule gap (mixed with R1.f): 'cache/fred/BAMLC0A0CM.csv' fails K1 (segment 1 must be a V1 source or a V7 tier; empirically, refused_keys membership does not satisfy K1); mixed group stays class (d).",
  "token:sentiment": "K1 rule gap (mixed with R1.f): 'sentiment/keyword-sentiments.json' fails K1 the same way as cache; mixed group stays class (d).",
  "token:vpc": "L2 rule gap (mixed with R1.f): LOG_GROUP '/aws/vpc/flowlogs' has no L2 service-table entry for 'vpc'; mixed group stays class (d).",
  "token:otp": "K1 rule gap: 'otp/state.json' etc. are pure K1 (no R1 raise at all); K1 has no V3 branch (empirically verified: refused_keys membership does not resolve a K1 raise), so this stays loud despite superficially resembling D12_PHONE_OTP_ALL_AWS's subject.",
  "_K1_GROUP_NOTE": "The remaining class (d) tokens (%s, _quarantine, agendas, allowlists, backfill_v2, benchmarks, config, consolidated, contract_integrity, daily, daily-reports, data-refresh, ec2, exports, forwardfill_v2, infrastructure, investor-reporting, json, json-tiered, macro, quarantine, security-reports, semantic_clusters, timeseries, trending_reports, uploads, views, warehouse) raise PURELY via K1: 'segment 1 is neither a source nor a tier'. K1's own text (GRADING_RULE.md K1) explicitly anticipates this ('Anything else RAISES ... That covers a V2 token, json, config, cache and a variable segment'), and it is EMPIRICALLY VERIFIED here that refused_keys membership cannot satisfy K1 (two of these tokens, ec2 and infrastructure, are ALREADY registered generic_noun and STILL raise via K1 in this same population -- direct proof). These keys come from buckets/paths outside the source-first or tier-first grammar K1 covers; no registry row -- system, workstream, or otherwise -- can resolve a K1 raise. This is the rule's own coverage boundary, not a missing vocabulary entry.",
  "token:astn": "undecided, not guessed: GRADING_RULE.md V1 names astn a PRODUCT candidate, but row LGIC_ENFORCE-W1-S6 already measured that no DIRECTIVES.yaml line and no mission-tree project names its owner (CENSUS: org/missions/DIRECTIVES.yaml @e0171ca585, 0 hits). No D-code can be cited, so no class (a) row can be written; left for 1.0.0_SA_CTO.",
  "token:trade": "undecided, same basis as astn (row LGIC_ENFORCE-W1-S6: 0 DIRECTIVES.yaml hits, no mission-tree project).",
  "token:news": "undecided, same basis as astn (row LGIC_ENFORCE-W1-S6: 0 DIRECTIVES.yaml hits, no mission-tree project).",
  "token:find": "undecided: infra/logic/05_IDENTITY_SPINE.md s.3 (tick-list row 18) marks harvest/find explicitly UNRESOLVED as a doctrinal open question (product, vendor, or retired); classifying it here would pre-empt that open question rather than answer it.",
  "token:harvest": "undecided, same basis as find (spine s.3 tick-list row 18, same table row).",
  "token:imo": "undecided, same basis as find (spine s.3 tick-list row 18: 'whether imo is a product, a vendor, or retired is a word')."
 }
}
```
