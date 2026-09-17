# OWNER_CARDS_R4 -- the registry campaign's NOT-JUDGED cards, round 4

Measured 2026-09-17 by 0.9.0_WK_LGIC_ENFORCE~1, worktree wk-lgic-enforce-4-1, registry@R4_BASE
(af8d694cced2b38e52f5735a35bd4ea0f7655eda) unchanged (see the fence/mint-basis finding below).
Every one of the 351 triples in RAISE_POPULATION_S6.r3.md is carded here (0 minted). WHY zero
minted is itself a measured finding, stated first because it governs every card beneath it.

## Why this campaign mints nothing (read this before any single card)

`grade()`'s registry-lookup mechanism (`lib/opal_naming.py` `_slots`, `:1113-1164`) consults
`resources.json` (`v.resources.get((nm, typ))`) in exactly ONE branch: when a name's first token
`t1` is ALREADY classified in `v.v3` (systems.json `refused_keys` + cadences + scope keys + `bd`,
`:1006-1007`) or the type is `LAMBDA_LAYER` (`:1135`), AND no later token resolves a system, AND no
earlier v2-token conflict has already raised inside the same loop (`:1140-1141`, R1.d). A triple
that reaches RAISE_POPULATION_S6.r3.md was, by construction, captured because `grade()` raised on
it (RAISE_POPULATION_S6.r3.md line 6-7: `grade()` called on every item, RaiseDefect recorded). For
every R1.d-message row in this population (the 9 `semantic-news-*` rows), the raise happens INSIDE
that loop because a v2 token (`news`) was hit BEFORE any system -- so `resources.json` is never
reached for it either. For every other message class in this population (R1.c, R1.f, R2, B2, K1,
K3, K4a, R8, L2), `t1` (or the K-grammar's segment 1) is NOT in `v.v3` and the type is never
`LAMBDA_LAYER` here (the two `LAMBDA_LAYER` rows are `news-trending-deps`, and `news` is in `v.v2`,
which is checked BEFORE the `v.v3`-or-`LAMBDA_LAYER` branch, so it raises R1.c and never reaches
resources.json's fallback either -- confirmed against the population's own message for that row).

CONSEQUENCE, MEASURED: `resources.json` cannot change the `grade()` outcome for ANY of the 351
triples in this population. The only registry file whose contents can resolve any of them is
`systems.json` (`v.v1` membership, checked FIRST in `_slots`, `:1088-1093`, and in `_grade_bucket`'s
`v.products`/`v.vendors` checks, `:1304-1313`, and in `_grade_key`'s `v.v1` source check, `:1388`,
`:1441`). Every candidate token this cell researched (see the cards below) either (a) already
carries a MEASURED no-owner finding in `systems.json`'s own `unresolved` block (astn, trade, news --
Cards 2-4), or (b) has NO declared source at all (no Terraform file, no `lambda-source-map.json`
entry, no `EC2_MANIFEST.json` entry) naming an owning directive, or (c) collides on one token with
an ALREADY-established different (and differently-owned) meaning, so minting it would misattribute
resources the evidence does not support (Card 6). None qualifies under WORKER FACE instruction 1
("A row's owner is read, never guessed"). Zero mints follow from that, not from a shortfall of
effort: every token below was researched against `infra/aws/terraform/`, `org/missions/DIRECTIVES.yaml`,
`org/projects/*.json` and the live-AWS census instruments before being carded.

Filed as a BLOCKING surprise row (LGIC_ENFORCE-W1-S1): the round's own C23R4-AC2 checker arm
(`c23_mint_basis`) cannot detect a `systems.json` addition at all (measured: it reads
`infra/logic/registry/systems.json: 0 row(s) at the worktree` against a file `validate` reports as
carrying 25 system rows -- `_added_rows`'s `"resources" in cur` test is false for `systems.json`,
whose top-level list key is `"systems"`, so `rows` falls through to `[]` regardless of content), and
a `resources.json` row carrying the `owner_claim`/`owner_basis` fields AC2 requires is REFUSED by
`lib/opal_naming.py validate()`'s closed `RES_FIELDS = ("name", "type", "system", "evidence")`
schema (measured directly: adding those two fields to a test row produced `VALIDATE: REFUSED 1
refusal(s)`, reverted). So the one file capable of curing this population (systems.json) is
invisible to AC2, and the one file AC2 can see (resources.json) is schema-closed against the fields
AC2 requires -- and, per the finding above, resources.json cannot resolve any of these 351 triples
regardless. AC2 is unsatisfiable for this cell by any registry write inside `<paths>`.

---

## Card 1 -- S3Key path-grammar (K1/K3/K4a) is out of mint reach

**Question:** can a `systems.json` or `resources.json` row resolve a `repo`/`S3Key` RAISE whose
message is K1 ("segment 1 is neither a source nor a tier"), K3 ("is not a tier (V7)") or K4a ("is
not an entity partition")?

**Why it RAISEs:** `_grade_key` (`lib/opal_naming.py:1399-1478`) requires segment 1 of an S3 key to
be EITHER one of `NAMING_SCHEMA.json` `key.tier` (`:43`, `["bronze","silver","gold","platinum",
"state","code"]`, not a registry file) OR a `systems.json` `v.v1` key (a "source"). K1 fires when
segment 1 is neither. K3 fires when a LATER segment that must be a tier (after source/scope are
consumed) is not one of that same fixed tier list. K4a fires on a served-path partition segment that
is not `{entity}={id}`.

**What was measured:** every segment-1 token this cell's 119 K1/K3/K4a triples carry (`json`,
`cache`, `config`, `consolidated`, `exports`, `timeseries`, `uploads`, `otp`, `_quarantine`,
`quarantine`, `security-reports`, `trending_reports`, `daily`, `daily-reports`, `backfill_v2`,
`forwardfill_v2`, `data-refresh`, `infrastructure`, `investor-reporting`, `json-tiered`, `macro`,
`views`, `warehouse`, `allowlists`, `contract_integrity`, `agendas`, `%s`, `benchmarks`, `ec2`, and
the K3 second-segment tokens `feeds`, `jwt`, `platform`, `raw`, `meta`, `_ops`, `session-trigger-mode.json`,
`bronze-trigger-mode.json`) is an S3-KEY-PATH CONVENTION WORD, not an AWS resource with a Terraform
declaration, a `lambda-source-map.json` entry or an `EC2_MANIFEST.json` entry -- there is no
"resource" for the mint rule's evidence sources to attribute an owner to. Where the leading segment
IS an existing `systems.json` key (`smartx/jwt/...`, `orion/jwt/...`, `blackdiamond/49f/_ops/...`,
`blackdiamond/cottonwood/meta/...`), the RAISE still fires on the SECOND segment (K3: it is neither a
recognised scope nor a tier), which no `systems.json`/`resources.json` row touches -- that slot's
vocabulary is `NAMING_SCHEMA.json` `key.tier` (code, not registry) and `scopes.json` (LGIC_LGCTFM's
file this round, not `<paths>`). No systems.json/resources.json row can change either outcome.

**Missing instrument:** a `NAMING_SCHEMA.json` `key.tier` change (code, outside `<paths>`) or a live
key-path rename (a pipeline change, not a registry mint) or a `scopes.json` row (LGIC_LGCTFM's file
this round, preflight contention EN-h-24-r4).

---

## Card 2 -- news (unresolved, no directive owner)

**Question:** does any directive own the `news` token?

**Why it RAISEs:** `news` is in `systems.json`'s own `unresolved` list (`:358-361`), which is
DELIBERATE -- `t1 in v.v2` raises R1.c/R2/R1.d before any placeholder/resources.json fallback runs
(`lib/opal_naming.py:1129-1134`, `:1140-1141`).

**What was measured:** `infra/logic/registry/systems.json:358-361` (this row itself): "news's 34
live resource names ... carry NO org/missions/DIRECTIVES.yaml line ... and NO mission-tree D<n>
project. Its only named project relation, ASTN_WSJFT ... is itself unregistered/closed ...
owner_directive cannot be written." This cell re-confirms the finding is still current at HEAD (no
new commit touches this row since it was written) and extends it to every `news`-token triple in
this round's 99-row set (live + repo, every type: DYNAMODB_TABLE, EVENT_RULE, IAM_POLICY, IAM_ROLE,
LAMBDA, LAMBDA_LAYER, LOG_GROUP, S3_BUCKET). No new Terraform/DIRECTIVES/mission-tree evidence
surfaced this round that would change the prior measurement.

**Missing instrument:** a DIRECTIVES.yaml line or mission-tree D<n> project claiming the news
pipeline, or Andrew's own card assigning it (the astn/trade/news pattern, Rule 24 record already
filed at `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/RETIRED_CLASS_RULE24.r3.md`
for the sibling `imo` case).

---

## Card 3 -- trade (unresolved, no directive owner)

**Question:** does any directive own the `trade` token?

**Why it RAISEs:** `trade` is in `systems.json`'s own `unresolved` list (`:354-357`), same mechanism
as Card 2.

**What was measured:** `infra/logic/registry/systems.json:354-357`: "trade's 22 live resource names
... are S3-backed ... or EXTERNAL ... NOT from the tradeops second-fabric root ... Its projects
(TRSB_LEDGER, TRSB_TFIMPT, TRSB_PATHFIX) are LEGACY FLAT, carry NO org/missions/DIRECTIVES.yaml line
... and name SEAT owners ... not a directive. No mission-tree D<n> project claims it." Re-confirmed
current, extended to every `trade`-token triple in this round's 46-row set.

**Missing instrument:** same as Card 2.

---

## Card 4 -- astn (unresolved, no directive owner)

**Question:** does any directive own the `astn` token?

**Why it RAISEs:** `astn` is in `systems.json`'s own `unresolved` list (`:350-353`), same mechanism
as Card 2.

**What was measured:** `infra/logic/registry/systems.json:350-353`: "astn's 14 live resource names
... trace to project ASTN_WSJFT ..., a LEGACY FLAT project carrying NO ... DIRECTIVES.yaml line ...
and NO ... MACROS.yaml entry, status 'closed' ... its registry 'owner' field names a SEAT ..., not a
directive." Re-confirmed current, extended to every `astn`-token triple in this round's 33-row set
(includes the one `S3Key` row `ec2/astn-wsjft/deploy.sh`, whose own RAISE is independently K1
(Card 1's reason) but is carded here under the `astn` heading since that is the more specific,
already-measured finding).

**Missing instrument:** same as Card 2.

---

## Card 5 -- security-sweep tooling (NFRA_TERRAFORM, closed and unregistered)

**Question:** does any directive own the `security-sweep-comprehensive` / `SecuritySweepComprehensive`
/ `security-sweep-dedicated-role` resource family (the `security` token in its R1.f sense)?

**Why it RAISEs:** `security` is in no vocabulary at all (`v.v1`/`v.v2`/`v.v3` all miss it), so
`_slots` falls to the final `else: raise RaiseDefect("R1.f: ...")` (`lib/opal_naming.py:1150-1151`).

**What was measured:** `infra/aws/terraform/security-ops/main.tf:1-8` declares
`security-sweep-comprehensive` (with `access-anomaly-scanner` and `cost-anomaly-scanner`, not in
this population) "adopted under NFRA_TERRAFORM-P2". `org/projects/NFRA_TERRAFORM.json`: `"status":
"closed"`, `"phase": "closed 2026-08-25 -- SPRING CLEAN, Andrew-direct ... a project not attached to
org/missions/DIRECTIVES.yaml is closed rather than left floating unaddressed as live"`. Grep of
`org/missions/DIRECTIVES.yaml` for `NFRA_TERRAFORM`: 0 hits. This is the same measured shape as
astn/trade/news (Cards 2-4): a legacy flat project, closed, not attached to any directive, no
mission-tree D<n> project claims the security-sweep resource family. `owner_directive` cannot be
written.

**Missing instrument:** a DIRECTIVES.yaml line or mission-tree D<n> project claiming the
security-sweep/anomaly-scanner tooling, or Andrew's own retirement/reassignment card.

---

## Card 6 -- opal-data-security and opal-data-security-access-logs (scope-key question, token collision)

**Question:** can `security` be minted as a `systems.json` PRODUCT so `opal-data-security` /
`opal-data-security-access-logs` (+ their `#policy`/`S3_BUCKET_POLICY` forms) resolve via B2?

**Why it RAISEs:** `_grade_bucket`'s B2 branch (`lib/opal_naming.py:1301-1313`) needs `first` (the
token after `opal-data-`) in `v.long_scope`, `v.products`, `v.scope` or `v.vendors`; `security` is in
none of them.

**What was measured:** `infra/aws/terraform/opsec/s3_evidence.tf:1-20` (`opal-security-evidence`,
cell OP-s-17, PRD v0.10) and `infra/aws/terraform/opsec/s3_access_logs.tf:1-20`
(`opal-data-security-access-logs`, cell OP-s-27, PRD s.7.6 C-15) are both declared under project
`NFRA_OPSEC202609`, which IS a current `org/missions/DIRECTIVES.yaml` member (D12 "Platform
Operations", `:485`). That is genuine directive evidence -- for THOSE TWO specific buckets. But
`grade()`'s vocabulary is a FLAT per-token map: minting `security` as a `v.products` row owned by
D12 would ALSO resolve every `security-sweep-*` resource-name RAISE in Card 5, which this cell just
measured as NFRA_TERRAFORM's (closed, unowned, unrelated project) -- a single-token mint cannot carry
two different, non-overlapping owners for two genuinely different systems that happen to share one
English word. Minting it as D12's would misattribute the security-sweep family; minting it as
NFRA_TERRAFORM's is not possible (no directive). Additionally, B2's actual need here is a SCOPE key,
not necessarily a PRODUCT: `opal-data-{scope}` names a bucket's firm/scope, and the scope vocabulary
is `scopes.json`'s domain, which LGIC_LGCTFM's `LT-x-1` writes this round (this order's own preflight,
contention line) and which is not in this cell's `<paths>`.

**Missing instrument:** a `scopes.json` row (not `<paths>`) or a per-resource `resources.json` row --
but Card 1's general finding above shows `resources.json` cannot be reached for a B2 raise on this
population's shape (t1 is checked directly in `_grade_bucket`, never through the `_slots` v3/LAMBDA_LAYER
branch that consults `resources.json`). Filed alongside as informational surprise row (non-blocking):
the token collision itself, for whoever next revises the `security` vocabulary question.

---

## Card 7 -- vpc (no declared source)

**Question:** does any Terraform file, `lambda-source-map.json` entry or `EC2_MANIFEST.json` entry
declare VPC flow-log resources (`VPCFlowLogsPolicy`, `vpc-flow-logs-role`, log group
`/aws/vpc/flowlogs`)?

**Why it RAISEs:** R1.f (no vocabulary) for the two IAM names; L2 ("service 'vpc' gives no resource
type", `lib/opal_naming.py:1281-1283`, against the hardcoded `_LOG_SERVICE` dict, `:947`) for the log
group.

**What was measured:** a repo search (native Grep tool) across `infra/aws/terraform/` for
`vpc-flow-logs-role`, `VPCFlowLogsPolicy`, `aws_flow_log` and `flow_log`: 0 hits. These are
LIVE-no-DECLARED resources -- no Terraform source exists to read an owner from, which is the mint
rule's first and only failure mode that is not even a vocabulary question: there is nothing to cite.

**Missing instrument:** a Terraform import/adoption of the VPC flow-log resources (an infra project,
not a registry mint) that would then let a `resources.json`/`systems.json` row cite it.

---

## Card 8 -- portal and cache (portal-auth / data-refresh, no directive names the cross-product edge layer)

**Question:** does any directive own `portal-auth` (CloudFront edge auth: `portal-origin-verify-secret`,
`cache-control-injector`, `opalinvest-auth-lambda-role`) or the `data-refresh` module's
`portal-time-machine` / `portal-time-machine-invoke-downstream` / `portal-auth-lambda-role`
(proposed-adoption)?

**Why it RAISEs:** R1.f ("portal"/"cache" in no vocabulary) for the resource names;
B2 ("portal" after `opal-data-` is no scope key) for `opal-data-portal-s3`.

**What was measured:** `infra/aws/terraform/portal-auth/iam.tf:236` (`portal-origin-verify-secret`),
`infra/aws/terraform/portal-auth/lambda-edge.tf:149-152` (`cache-control-injector`, Lambda@Edge,
"ALL MANAGED by portal-auth module" per `infra/aws/nfra_terraform_p1/slice_compute.json:1920`),
`infra/aws/terraform/data-refresh/main.tf:122,139` (`portal-time-machine`,
`portal-time-machine-invoke-downstream`), `infra/aws/terraform/data-refresh/zz_adoption_candidate.tf.proposed:58-67`
(`portal-auth-lambda-role`, a PROPOSED, not-yet-applied adoption candidate). `org/missions/DIRECTIVES.yaml`:
0 hits for `PORTAL:` as its own directive/system entry; `PORTAL.` only appears as a SUBGROUP label
nested under other directives' own products (`PORTAL.MODEL_PORTFOLIOS` under D8, `:49,73,83,334`;
`PORTAL.ADVISOR_INTELLIGENCE` under D2, `:59`) -- meaning "PORTAL" names a portal-hosting surface for
several products, never itself a directive-owned system. No DIRECTIVES.yaml line or mission-tree
D<n> project claims `portal-auth` or `data-refresh` as its own system.

**Missing instrument:** a DIRECTIVES.yaml line or mission-tree D<n> project naming an owner for the
portal-auth/data-refresh modules themselves (as distinct from the PORTAL subgroup label their output
serves).

---

## Card 9 -- sentiment (no declared source, LIVE-no-DECLARED)

**Question:** does any Terraform file, `lambda-source-map.json` entry or `EC2_MANIFEST.json` entry
declare `sentiment-query-api` / `sentiment_query_api` / `sentiment_query_api-role`?

**Why it RAISEs:** R1.f ("sentiment" in no vocabulary).

**What was measured:** a repo search (native Grep tool) for `sentiment_query_api`/`sentiment-query-api`
across the repo found matches ONLY in observation/census instruments
(`infra/system/ontology/worldmodel/10_census/instruments/lambda_list_full.json:5995-5998`,
`iam_roles.json:743-744`, `re_us-east-1.json`, and the parity dump `kuzu_aws_nodes_raw.txt`) -- every
hit is a LIVE-AWS OBSERVATION, never a Terraform `resource` block, a `lambda-source-map.json` entry
or an `EC2_MANIFEST.json` line. Same failure mode as Card 7: nothing to cite an owner from.

**Missing instrument:** a Terraform import/adoption of the sentiment-query resources.

---

## Card 10 -- F49ServedAndSourceRead (naming-order defect, unreachable via resources.json)

**Question:** can `resources.json` place `F49ServedAndSourceRead` under `advi` (its genuine Terraform
owner)?

**Why it RAISEs:** R1.f. Tokenized, the name's first token is `f49` (not `49f`), which is in no
vocabulary (`v.v1`/`v.v2`/`v.v3` all miss it) -- `_slots` falls straight to the `else: raise
RaiseDefect("R1.f: ...")` branch (`lib/opal_naming.py:1150-1151`), the SAME branch Card 1's general
finding shows never reaches `resources.json`.

**What was measured:** `infra/aws/terraform/49f-value-parity/49f_value_parity.tf:1-11` (header:
"ADVI_BREAKS TO-6 detection-4 -- 49F per-firm value-parity reader") -- `advi` (D2) is ALREADY a
`systems.json` v1 key, so the resource's TRUE owner is genuinely measured. The obstacle is not
ownership, it is that the resource's own live name reorders the registered scope token (`f49` rather
than the registered `49f` short form used everywhere else, e.g. `wsb-49f-model-aua-daily-role` in
`resources.json`), so no token in the name is `advi`, `49f`, or any other `v.v1`/`v.v3` member --
and, per Card 1's general finding, `resources.json`'s per-name fallback is never reached for an
R1.f raise in the first place. No `<paths>` write can fix a token-order defect in a live resource's
own name.

**Missing instrument:** a live rename of `F49ServedAndSourceRead` (an infra act, not a registry mint)
or a code-level tokenizer accommodation (outside `<paths>`).

---

## Card 11 -- dowjones (no declared source)

**Question:** does any Terraform file or code reference declare the `dowjones/credentials` secret's
owner?

**Why it RAISEs:** R1.f ("dowjones" in no vocabulary).

**What was measured:** a repo search (native Grep tool) for `dowjones` across `infra/` and `tools/`:
0 hits outside the population document itself. No Terraform `aws_secretsmanager_secret` resource, no
`lambda-source-map.json` entry, no code reference. Same failure mode as Cards 7 and 9: secrets of
this shape are created out-of-band (matching the sibling `astn/*` secrets, Card 4), and nothing in
the repo names an owner to cite.

**Missing instrument:** a Terraform import/adoption of the secret, or a code reference identifying
its consumer.

---

## Card 12 -- opal-data-imo (retired token)

**Question:** can `imo` be minted as a scope/product so `opal-data-imo` resolves?

**Why it RAISEs:** B2 ("imo" after `opal-data-` is no scope key). `imo` is NOT in `v.long_scope`,
`v.products`, `v.scope` or `v.vendors` -- B2 does not consult `refused_keys` at all (only the R1-R4
`_slots` v3 branch does), so `imo`'s membership in `refused_keys.retired` has no effect on this
bucket's B2 grading.

**What was measured:** `infra/logic/registry/systems.json:225-228`: "`imo`" is in `refused_keys.retired`,
citing "R-6 ...: tick-list row 18 (opal-data-imo, 304 per-company planes, 103d dead at census) was
RESOLVED by Andrew's card 9 as RETIRE (`org/tier1_exec/4.0.0_SA_CRO/deliverables/04_SCOPE_TICKLIST.md
:15, :66`)." RETIRE is not a scope grant -- it is the opposite: the bucket is on its way out, not
being registered. Minting a scope for a bucket Andrew already ruled RETIRE would contradict the
existing, cited ruling.

**Missing instrument:** none needed -- this is measured, not missing; the correct disposition is
retirement of the live bucket (an infra act), not a registry mint.

---

## Card 13 -- opal-data-pm, opal-data-portfolio, opal-data-research (scope-key vocabulary, not ours)

**Question:** can `pm`, `portfolio` or `research` be minted as a scope/product?

**Why it RAISEs:** B2, same mechanism as Card 12, for each of the three buckets.

**What was measured:**
- `portfolio`: `infra/logic/registry/systems.json:301` already lists `portfolio` in
  `refused_keys.generic_noun` (a common English noun, deliberately never a system, per
  `refused_keys.basis` `:224`). B2 does not consult `refused_keys` (Card 12's finding), so this
  existing classification does not resolve the bucket, and adding `portfolio` as a NEW `v.products`
  row would directly contradict the already-recorded generic_noun judgment without new evidence.
- `pm`: no Terraform file, DIRECTIVES.yaml line, or mission-tree project names a `pm` product; a repo
  search found no `aws_s3_bucket "..."` resource declaring `opal-data-pm`. Nothing to cite.
- `research`: `infra/aws/terraform/harvest/s3.tf:3-5`: "STAGE 1: declared at its CURRENT name
  `opal-data-research` so this module can IMPORT it without touching it. Stage 2 renames it to
  `opal-data-harvest` per Andrew's approved rename map." `harvest` is ALREADY a `systems.json` v1 key
  (`:213-221`, D5, AMGT_RESAPP). So `opal-data-research` is a MEASURED, INTERIM, PRE-RENAME name for
  a bucket whose real, already-registered product is `harvest` -- minting `research` as a second,
  separate scope/product for the same bucket would be wrong (two owners for one resource) and would
  also outlive its own Stage-2 rename.

**Missing instrument:** `pm`: none found (genuinely unmeasured). `portfolio`: none -- already
correctly refused. `research`: none needed -- the Stage-2 rename (an infra act already approved)
resolves it, not a registry mint.

---

## Card 14 -- the five #policy R8 rows (structural, ungradable from name)

**Question:** can a `systems.json`/`resources.json` row place `opal-cloudtrail-logs-313476888478#policy`,
`opal-cur-313476888478#policy`, `opal-security-evidence#policy`, `opal-served-key-write-trail-logs#policy`
or `opalinvest-portal#policy`?

**Why it RAISEs:** R8 (`lib/opal_naming.py:1204-1217`). For `X#policy`, if `X` starts with
`opal-data-` or `opal-{account}-` it is graded as a bucket (Card 6/12/13's B2 path); otherwise the
code takes `X`'s LAST token and looks for exactly one resource TYPE whose `kinds_by_type` (NAMING_SCHEMA.json,
not a registry file) contains that token -- `owners = [t for t, ks in v.kinds_by_type.items() if
xt and xt[-1] in ks]`, and raises when `len(owners) != 1`. None of these five bucket names fits
`opal-data-` or `opal-{account}-313476888478-` (the account digits sit at the END of the name, e.g.
`opal-cloudtrail-logs-313476888478`, not the start), so all five fall to the kind-lookup path, and
their last tokens (`313476888478`, `evidence`, `logs`, `portal`) match no type's `kinds_by_type`
list. `_grade_resource` (where a `resources.json` row could matter) is only called AFTER `owners`
already has exactly one entry (`:1216`) -- so a `resources.json` row is never reached; there is no
`typ` argument to key it on.

**What was measured:** traced the R8 code path for each of the 5 names against `kinds_by_type`'s
membership; none resolves to a single type. This is a naming-grammar dead end (the bucket names
themselves do not fit either of the two blessed bucket patterns), not an ownership question.

**Missing instrument:** a live rename of the five buckets to `opal-data-{scope}` or
`opal-{account}-{purpose}` form (an infra act, not a registry mint).

---

## Card 15 -- L2 log-group service tokens (hardcoded dict, code change not registry)

**Question:** can a `systems.json`/`resources.json` row resolve `/aws/vendedlogs/pipes/...` or
`/opal/github-actions-runner`?

**Why it RAISEs:** L2 (`lib/opal_naming.py:1281-1283`): the log group's `service` segment
(`vendedlogs/pipes`, `opal`) is looked up in `_LOG_SERVICE`, a dict HARDCODED in `lib/opal_naming.py`
itself (`:947`), never read from `systems.json` or `resources.json`.

**What was measured:** `lib/opal_naming.py:947` is outside `<paths>` (`<paths>` names only
`infra/logic/registry/systems.json` and `infra/logic/registry/resources.json`); no registry row
this cell can write changes `_LOG_SERVICE`'s membership.

**Missing instrument:** a code change to `_LOG_SERVICE` (outside `<paths>`, a different project's
lane).
