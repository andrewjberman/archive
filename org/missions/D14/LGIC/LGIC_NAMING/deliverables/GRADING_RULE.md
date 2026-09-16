# GRADING_RULE -- `grade(name, type) -> (verdict, canonical_form)`, applied by hand

**Cell:** LGIC_NAMING `LN-g-1` (PRD candidate N2), task order `LGIC_NAMING.TO-LN-g-1`, written by
`0.9.0_WK_LGIC_NAMING~1` on branch `wk-lgic-naming-1-1` off CLOUD @`6a5b276f8b`. **Re-cut in round 3** by
`0.9.0_WK_LGIC_NAMING~3` (task order `LGIC_NAMING.TO-LN-g-1-r3`, branch `wk-lgic-naming-3-3` off CLOUD @`6705066c68`):
R5 gains v1.7's two function-slot steps and the reason a function's words are kept, and R3 states its test as
adjacency. **Re-cut in round 4** by `0.9.0_WK_LGIC_NAMING~3` (task order `LGIC_NAMING.TO-LN-g-1-r4`, branch
`wk-lgic-naming-4-3` off `lgic-v19-group` @`bd0f5d2c6c`): the rule is re-cut against every schema field changed since
v1.4, the version it was cut at, and section 10 prints which step reads each one (row `LGIC_NAMING-W3-S6`). R5 is one
subtraction (FN1d); G2 excludes the names AWS fixes (AW1); V-2 takes the schema's four placeholders, so K3 and K4a
RAISE where they emitted `{tier}` and `{entity}`; the vocabularies read the identity registry. **Re-cut in round 5**
by `0.9.0_WK_LGIC_NAMING~1` (task order `LGIC_NAMING.TO-LN-g-1-r5`, branch `wk-lgic-naming-5-1` off CLOUD
@`119a08a196`): re-based on `NAMING_SCHEMA.json v1.10` (@`5a12d0b97c`), which lifts R3's bd-adjacency test into
`alias_adjacency` as data (A-3) and updates `refused_tokens.bd`'s prose to point at it -- section 10 adds both;
the two `globgrph` worked cases (S22, RULING R-5) are re-verdicted from `grade()` now that `systems.json` carries
the row (LGIC_ENFORCE EN-r-2); and the registry_hash decision below is stated for the first time.

**Grades against `NAMING_SCHEMA.json v1.10`** (every step; section 10 prints its coverage. Rulings FN1d and W3-S6 of
the round-3 analysis s.2, `org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_NAMING_ROUND3_20260915.md`
@`2f554182b6`; FN1b and FN1c of the round-2 analysis s.2,
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_NAMING_ROUND2_20260915.md` @`02f08322af`; A-3 of the
round-4 analysis s.2, `org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_NAMING_ROUND4_20260916.md`
@`5a12d0b97c`).

**Registry hash: deliberately unpinned.** `grade()` reads the identity registry LIVE at call time, never at a
stamped `registry_hash()` (`lib/opal_naming.py` `registry_hash()`, the sha256 GENERATED files carry as their
drift stamp -- never this rule's). Pinning one would freeze a verdict against a stale registry, exactly the gap
S22 exposed: the `globgrph` row landed between rounds (LGIC_ENFORCE EN-r-2) and the two held cases' verdict had
to move with it at the next grade, not wait for a re-stamp. This rule cites the registry's base commit in its
own history above (as every re-cut already did) but pins no hash inside `grade()` itself.

**What it reads.** Every clause below cites where its rule comes from:
- `org/standards/NAMING_SCHEMA.json` v1.9, cited as `DATA.<field>`, for every step;
- the identity registry `infra/logic/registry/` (`systems.json`, `scopes.json`), read at this rule's base
  @`bd0f5d2c6c` and cited as REGISTRY. Where it and the seed differ, the registry governs (`DATA.rows_owner`);
- `infra/logic/05_IDENTITY_SPINE.md` v0.1, the registry seed, cited as SEED;
- `infra/logic/09_NAMING_CENSUS.md`, cited as CENSUS;
- `LGIC_NAMING_PRD.md` v1.4, S1-S13;
- `org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json`, cited as the LIST.

**Membership is read from `LEGACY_SERVED_PATHS.json`.** That is `DATA.key.legacy_served_paths`, v1.4. This file carries
no copy of the LIST; a grader opens the LIST itself.

**The worked cases** in section 9 are live names from the fixed input `LIVE_NAMES.json`, at vintage *"Built from the
estate as of 2026-09-14 12:13:53 UTC"*. A case marked `specimen` has no live name of its form.

---

## 0. THE OUTPUT, AND THE ORDER OF STEPS

Every name gets exactly one of five outputs:
- **CONFORMANT**, **ALIAS** or **OUT-OF-PATTERN** -- the three verdicts (`DATA.grade.verdicts`). Each carries a
  canonical form; for CONFORMANT it is the name itself.
- **RAISE** -- the name cannot be placed. This is a defect in this rule, the data file or the registry, and the
  output names the step that raised (`DATA.grade.unplaceable`). It is never filed under a verdict.
- **NOT-GRADED** -- the type is outside the grade's domain (`DATA.grade.not_graded`, G1.2), or the name is one AWS
  fixes (`DATA.aws_fixed`, G2). This is not a fourth verdict.

Apply the steps in order, **G1, G2, G3, then the grammar of the type, then G6**. The first step that returns an
output decides.

## G1. THE DOMAIN

- **G1.1** The type must be one of the 33 keys of `DATA.kind.by_type` and `DATA.types_not_graded_by_kind`, spelled
  exactly. Any other type RAISES. A caller that grades a Terraform resource takes the type from `DATA.tf_type_map`
  (the resource type's `node_type`, always one of the 33) and the name from the attribute its `name_attribute` names
  (`DATA.tf_type_map_note`); the four types whose `name_attribute` is null are all NOT GRADED (G1.2). A Terraform type
  listed in `DATA.tf_unmapped_own_name` carries its own name but maps to no node type, so a grade of it RAISES here
  until a node type is added (`DATA.tf_unmapped_own_name_note`).
- **G1.2** A type whose `DATA.types_not_graded_by_kind` value begins `NOT GRADED` returns NOT-GRADED. There are 8 of
  them: IAM_USER, KMS_KEY, CLOUDFRONT_DISTRIBUTION, SERVICE_PRINCIPAL, VPC_ENDPOINT, ROUTE53_RECORD, API_ROUTE and
  EVENT_SOURCE.
- **G1.3** The other 25 types each take one grammar:

| grammar | types |
|---|---|
| RESOURCE (section R) | the 18 of `kind.by_type`; also EVENT_RULE and SCHEDULE, and IAM_POLICY with R8 |
| SECRET (section S) | SECRET |
| LOG GROUP (section L) | LOG_GROUP |
| BUCKET (section B) | S3_BUCKET and S3_BUCKET_POLICY |
| KEY (section K) | S3Key |

## G2. NAMES AWS FIXES -> NOT-GRADED

AWS fixes these names, so none can take a canonical form. They are outside the grade's domain, like the NOT GRADED
types: the output is NOT-GRADED, never a RAISE and never a fourth verdict (`DATA.aws_fixed`, RULING AW1).
- **G2.1 By name** (`DATA.aws_fixed.by_name`), exactly as it lists them:
  - a SECURITY_GROUP named `default` (the default group of every VPC);
  - a LOG_GROUP named `RDSOSMetrics`, or whose name begins `aws-waf-logs-` or `/aws/ecs/containerinsights/`.
- **G2.2 By ARN** (`DATA.aws_fixed.by_arn`): an IAM_POLICY whose ARN's account field is `aws`
  (`arn:aws:iam::aws:policy/...`) is AWS-managed, whatever its name says (`ReadOnlyAccess` carries no prefix).
  `grade(name, type)` never receives an ARN, so the caller that holds the node's ARN applies this exclusion before it
  calls the grade, and does not grade such a policy.

Nothing else is excluded by name. A name that `DATA.aws_fixed.by_name` does not list is graded as written, and so is a
policy that reaches the grade without the caller's ARN test: an `AWS`- or `Amazon`-prefixed name then RAISES at R1,
because `aws` and `amazon` are in no vocabulary. Adding an AWS-fixed name is an edit to the data file
(`DATA.aws_fixed.rule`), never to this rule.

## G3. NORMALISE, TO FIND THE TOKENS

The canonical form is built from the normalised tokens. A name that needed N1, N2, N3 or N4 therefore can never equal
its canonical form.
- **N1 Case and separator.** A resource name, a secret or a bucket is lowercase ASCII letters and digits joined by
  `-`. A secret, a log group or a key also uses `/`.
- **N2 Camel or Pascal case.** Split before each capital that follows a lowercase letter or a digit, and before the
  last capital of a run of capitals when a lowercase letter follows it. Then lowercase each piece. `SilverChain`
  gives `silver`, `chain`; `FIRMSEP-auth` gives `firmsep`, `auth`.
- **N3 Other separators.** In a resource name, `_` and `.` are token boundaries, like `-`.
- **N4 Generated suffixes.** A final token of 14 or more digits is a generated suffix (a Terraform `name_prefix`).
  It fills no slot, and the canonical form drops it.
- **N5 AWS-required affixes.** Keep these byte for byte; they are not tokens:
  - the `.fifo` suffix of a queue;
  - the `us-east-1.` prefix of a Lambda@Edge replica log group;
  - in an S3Key, everything from the first space on (a graph annotation such as `(name-grain: ...)`).
- **N6 Variable segments.** In an S3Key, `*`, `{...}` and `%s` stand for any value of the segment, or part of a
  segment, they occupy.

## V. THE VOCABULARIES THIS RULE USES

A token matches only as a WHOLE token: `bd49f` is not `bd`.

**V1 SYSTEMS** fill the system slot, and a key's `{source}`. They are the `systems` rows of REGISTRY `systems.json`,
which governs where it and the seed differ (`DATA.rows_owner`). The table reads the 17 rows at this rule's base; a row
the registry adds is in V1 from the commit that adds it, and this table is never a second source.

| token | class |
|---|---|
| `mdpf`, `etfs`, `irpt`, `advi`, `amgt`, `yang` | PRODUCT |
| `schwab`, `blackdiamond`, `orion`, `eclipse`, `smartx`, `pathfinder`, `trueshares`, `ycharts`, `fred`, `seeking-alpha` | VENDOR (`fred` and `seeking-alpha` are feeds; `seeking-alpha` is two tokens, matched as one) |
| `gateway` | PLATFORM_SUBSYSTEM (owner D9) |
| `opal` | reserved: `DATA.system.reserved`; see R2 |

The registry was seeded from SEED s.3 and from this rule's round-1 reading of CENSUS s.3. `astn`, `trade` and `news`,
which that reading listed as PRODUCT, have no owning directive, and the registry holds them unresolved (row
`LGIC_ENFORCE-W1-S6`), so they are V2.

**V2 UNRESOLVED** are REGISTRY `systems.json`'s `unresolved` tokens. A V2 token RAISES wherever the system slot needs
it:
- `estate`, `globgrph`, `semantic`, `agentbus`, `cmtque`, `opsec`, `firmsep`, `consolidation`, `canonical`,
  `gldinc`, `quartz`. CENSUS s.3 lists these as "PLATFORM subsystems and PROJECT CODES used as systems" and does not
  say which is which. A subsystem is a system; a project code never is (S6).
- `find`, `harvest`, `imo`. SEED s.3 marks them UNRESOLVED.
- `astn`, `trade`, `news`: no directive owns them (above).

**V3 NEVER A SYSTEM** (S6; CENSUS s.3; REGISTRY `systems.json` `refused_keys` carries the same members):
- every firm form in V4, and `bd` when it reads as the firm (R3);
- workstream codes, cadences and generic nouns: `wsb`, `wsd`, `historical`, `daily`, `weekly`, `monthly`, `hourly`,
  `exec`, `infrastructure`, `market`, `etf`, `ec2`, `cloudfront`, `portfolio`;
- the purpose words that open the purpose-first policies: `cross`, `s3`, `cloudwatch`, `invoke`, `secretsmanager`,
  `lambda`, `kms`, `secrets`.

**V4 SCOPES.** A scope's forms are its REGISTRY `scopes.json` row: the `long` form (the key) and its one sanctioned
`short` form. The data file carries no copy (`DATA.firm_forms_source`, RULING ONE, v1.9); v1.4's `DATA.firm_forms` is
gone. The table reads the rows at this rule's base, and is never a second source:

| key (long) | short | class |
|---|---|---|
| `49financial` | `49f` | FIRM |
| `inflection` | `inf` | FIRM |
| `cottonwood` | `cot` | FIRM |
| `demo` | `demo` | FIRM (`demo` reads as a firm in every naming slot, RULING DM) |
| `global` | `global` | GLOBAL (`DATA.global_scope`) |

- The MASTER rows `08242234` and `08335338` are scopes with a single form.
- The registry's PRODUCT rows (`mdpf`, `etfs`) are not V4 tokens. B2 and K2 say where a product is a scope.
- `bd` is a refused alias; see R3.
- `mockadv` is an alias row of `49financial` and never a valid spelling (`DATA.refused_tokens`).

**V5 KINDS** are `DATA.kind.by_type`: the kinds allowed for each of the 18 types.

**V6 CADENCES** (`DATA.cadence`): `daily`, `weekly`, `monthly` or `hourly`, or `on-` followed by one or more kebab
tokens.

**V7 TIERS** (`DATA.key.tier`): `bronze`, `silver`, `gold`, `platinum`, `state`, `code`.

**V8 THE ACCOUNT ID** is `313476888478`, the one account id carried by every live name that carries one (for example
`opal-313476888478-lambda-layers`).

## R. RESOURCE NAMES -- `{system}-{scope}-{function}[-{qualifier}]-{last}` (S3, `DATA.resource`)

After G3 the name is a list of tokens t1 ... tn.

**R1 THE SYSTEM SLOT.** V1 and V2 are REGISTRY rows (`DATA.rows_owner`).
- **a.** If t1 is in V1 (other than `opal`), or t1 is `bd` read as the vendor (R3), the system is t1.
- **b.** If t1 is `opal`, apply R2.
- **c.** If t1 is in V2, RAISE.
- **d.** If t1 is in V3, it is not the system. The system is the FIRST later token that is in V1:
  - if a V2 token comes before any V1 token, RAISE;
  - if no later token is in V1, the system slot is the placeholder `{system}`, because the name does not carry its
    system (`DATA.grade.placeholder`: the registry's resource-to-system rows fill it; row `LGIC_NAMING-W1-S3`).
- **e.** LAMBDA_LAYER only. A t1 in none of V1-V3 is a library (the CENSUS "library-first" layers), and is handled as
  in d.
- **f.** Any other t1 is in no vocabulary. RAISE: a token no registry row resolves.

The system token leaves its position. Every token before it that is not a scope joins the function slot, ahead of
the tokens after the system.

**R2 `opal`** (`DATA.system.reserved`).
- If t2 is in V1 (a REGISTRY system row), `opal` is a null prefix: drop it, and the system is t2.
- If t2 is in V2, RAISE.
- Otherwise the system is `opal`.

**R3 `bd`** is refused in every slot (S10). It is the VENDOR `blackdiamond` when a V4 firm token is next to it,
before or after, and the FIRM `49financial` otherwise. CENSUS s.1 item 4 gives both readings: in
`bd-49f-session-trigger` it is the vendor, in `bd-allocations` the firm. Either way it is an alias, and the canonical
form spells `blackdiamond`, or the firm's form for the slot. The test is ADJACENCY to a V4 firm token, never position:
`bd` first with no firm token next to it (`bd-allocations`) is the firm, and `bd` next to a firm token wherever it sits
(`bd-49f-...` first, `cot-bd-session-trigger-lambda-role` second) is the vendor (row `LGIC_NAMING-W4-S1`). This test is
also stated as data at `DATA.alias_adjacency.bd` (v1.10, A-3), lifted from this step so the canon's generated section
can render it; this step is R3's own authored answer, and `DATA.alias_adjacency` carries no rule `grade()` does not
already apply here. `DATA.refused_tokens.bd`'s prose points to `DATA.alias_adjacency` for the same reason (v1.10).

**R4 THE SCOPE SLOT.** The scope tokens are the V4 tokens, plus `bd` read as the firm.
- **No scope token:** the resource is shared or scoped by its system. The slot is omitted, never filled with a
  placeholder (S5).
- **One scope token:** it goes immediately after the system, in the SHORT form (S4): the `short` of its REGISTRY
  `scopes.json` row (`DATA.firm_forms_source`; `DATA.rows_owner`). `49financial` becomes `49f`, `inflection` becomes
  `inf`, `cottonwood` becomes `cot`, and `bd` read as the firm becomes `49f`. A scope token anywhere else moves here.
- **Two different firms** (after R3): RAISE. A resource has one scope.

**R5 FUNCTION AND QUALIFIER.** Once R1 and R4 have taken the system and scope tokens out, the remaining tokens, in
order, are the function slot, and the last of them is checked by R6 or R7. The function is every remaining token except
the one R6 or R7 keeps in the last slot. Then ONE subtraction acts on it (FN1d, `DATA.resource.function`, v1.8): remove
from the function, in one pass, every token written in the system or scope slot, as the canonical form spells it after
R2, R3 and R4's short form (FN1b), AND every token that is the resource's own kind, any kind in `DATA.kind.by_type` for
its type (FN1c). If the subtraction removes the last function token, RAISE (`DATA.grade.unplaceable`), whichever of the
two removed it.
- It is a set subtraction, so it has no order and its result never depends on one. `orion-inf-orion-ingest-daily`
  becomes `orion-inf-ingest-daily`; a LAMBDA `mdpf-lambda-gold` becomes `mdpf-gold-lambda`. A LAMBDA
  `mdpf-lambda-lambda` RAISES, and so does a LAMBDA `orion-orion-lambda-lambda`, whose function [`orion`, `lambda`]
  loses both tokens in the one pass (section 9).
- A placeholder (`{system}`) writes no token and removes nothing.
- Another type's kind that names the subject the resource serves is not the resource's own kind, and stays in the
  function as R6 already says (`blackdiamond-49f-runner-role` keeps `runner`, the runner the role serves).
- A type with no `kind.by_type` row (EVENT_RULE, SCHEDULE) has no own kind, so only system and scope tokens are
  removed.
- A function that is empty BEFORE the subtraction loses nothing to it, so this RAISE does not fire, and R6 or R7 still
  fills the last slot (`opal-gateway` gives `gateway-lb`, section 9; row `LGIC_NAMING-W3-S7`).

Beyond this subtraction the function is free vocabulary, and here is why. A grade reads a name and its type, and has no
item description. FN1's word-choice clauses (an agent noun describing the resource is written as its verb; a noun phrase
is written as named) therefore bind the NAMER only, who has the description. The grade keeps a function's words as
written and grades the grammar: slots, spellings and kinds. So `advi-49f-floor-scheduler-role` keeps `scheduler`, and a
function written `publisher` or `scanner` keeps it, although `DATA.kind.closed_at_l4` gives their canonical spellings as
`publish` and `scan`. A qualifier cannot be told from a function token by hand, and is graded the same way:
`DATA.resource.qualifier`'s clauses on which object a qualifier writes (the tier or a named table, never figures or
files: FN2) and on a CW_ALARM's condition noun (FN3) need the item's description, so they bind the namer too.

**R5 re-graded over round 2's firm patterns.** Round 3 applied FN1b and FN1c, now R5's one subtraction, to every
attributed canonical form in round 2's LN-f-1 record
(`org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n4-firm-patterns.md` @`a4480344e3`, the `attributed` object
of its one json block). All are IAM_ROLE (own kind `role`), and each has one scope token. None carries its system or
scope token in its function, none carries `role` there, and none is left without a function token. The one subtraction
removes what the two removed together, which is nothing, so LN-f-1's record is not re-graded.

FORMS CHANGED BY THE v1.7 STEPS: 0 of 68

**R6 THE LAST SLOT, for kind types.**
- If the last remaining token is a kind of this type (V5), it stays.
- Otherwise the type's kind is APPENDED, and that token stays in the function. This includes a token that is another
  type's kind, such as `-runner` on a LAMBDA, and the suffixes `trigger`, `publisher` and `scanner`, which are function
  tokens, never kinds (`DATA.kind.closed_at_l4`).
- A type with two kinds appends the first: SQS_QUEUE appends `queue`, SNS_TOPIC appends `topic`.

**R7 THE LAST SLOT, for EVENT_RULE and SCHEDULE: a cadence (V6).**
- If the last token is a cadence, it stays.
- Otherwise, if an `on-` run or a cadence token appears elsewhere in the name, it moves to the end.
- Otherwise `{cadence}` is appended (`DATA.grade.placeholder`: the schedule fills it; row `LGIC_NAMING-W1-S3`).

**R8 IAM_POLICY** is `{system}-{scope}-{purpose}-policy`: the kind is `policy` and the purpose sits in the function
slot (S9, `DATA.iam_policy`), where R5 applies to it as to any function. `DATA.iam_policy.purpose_slot` (FN4) applies
FN1 and FN2 to the purpose and writes it as one compound token (`read-gold`); that is word choice, and it binds the
namer.
- A name `X#policy` is a resource policy. Grade `X` by the grammar of the resource it names (a bucket name takes
  section B), and keep `#policy`.
- A duplicate policy name is refused when it is minted (`DATA.iam_policy.duplicate_name`). One name cannot show a
  duplicate, so the grade does not read it.

**R9 THE CANONICAL FORM** is the system, the scope (if any), the function tokens and the last slot, joined by `-`,
with any N5 affix put back.

## S. SECRETS -- `{system}/{scope}/{purpose}` (S4, S9, `DATA.secret`)

- **S1** Split on `/`. A name with no `/` is one segment: its first kebab token is read as the system, and the rest
  as the purpose.
- **S2** The first token of segment 1 is the system slot, and R1-R3 apply to it. If R1.d has to look further, it
  reads the first token of each later segment. The rest of segment 1 joins the purpose.
- **S3** Segment 2 is the scope when it is a V4 token, in the SHORT form, the `short` of its REGISTRY row
  (`blackdiamond/49f/credentials`). Otherwise the secret is shared: the slot is omitted (S5), and segment 2 begins the
  purpose. A V4 token found anywhere else moves to the scope segment.
- **S4** The purpose is every remaining segment, each lowercase kebab, joined by `/`. CENSUS s.2 counts 86
  slash-path secrets, and many of them use more than one purpose segment. `DATA.secret.purpose` (FN4) says what the
  purpose names: the credential's kind (`credentials`, `token`, `key`, `password`, `certificate`), after the interface
  it opens when the item names one (`api-credentials`). Like a function's words (R5), that binds the namer, and the
  grade keeps the purpose as written.
- **S5** The canonical form is `system/scope/purpose`, with the scope dropped when the secret has none.

## L. LOG GROUPS -- `/aws/{service}/{resource-name}` (S9, `DATA.log_group`)

- **L1** After G2, a log group takes one of three shapes: `/aws/{service}/{rest}`,
  `/aws/vendedlogs/{service}/{rest}`, or another `/`-path. A log group in none of them (a name with no leading `/`
  that `DATA.aws_fixed.by_name` does not list) RAISES: this rule gives it no service.
- **L2** The service names the resource type:

| service | resource type |
|---|---|
| `lambda` | LAMBDA |
| `codebuild` | CODEBUILD_PROJECT |
| `stepfunctions`, and `vendedlogs/states` | STATE_MACHINE |
| `events` | EVENT_RULE |
| `ecs` | ECS_TASK_DEFINITION |

  Any other service RAISES: this rule gives it no type.
- **L3** Grade `rest` by section R as that type; extra `/` segments in `rest` join with `-`. The log group takes that
  verdict, and its canonical form is `/aws/{service}/` followed by the resource's canonical form.
- **L4** A `/`-path that does not begin `/aws/` (for example `/ecs/{name}`) takes its service from its first segment
  and is graded as in L3. It can never equal its canonical form, so it is never CONFORMANT.

## B. BUCKETS -- `opal-data-{scope}` and `opal-{account-id}-{purpose}` (S2, `DATA.bucket`)

- **B1** `opal-data-assets` and `opal-data-portal-v2` stand (`DATA.bucket.standing_shared`): CONFORMANT.
- **B2** `opal-data-{rest}`: `rest` must be exactly one scope key, in the LONG form. That is a V4 long form (the
  `long` of its REGISTRY row), a MASTER key, `global`, or a PRODUCT in V1.
  - A short form, or `bd` (the firm), is an alias: ALIAS, with canonical form `opal-data-{long}`.
  - A VENDOR in V1: OUT-OF-PATTERN, with canonical `opal-data-{scope}`. A data bucket's scope is never a vendor, and
    no new bucket carries a vendor name.
  - A scope key followed by more tokens: OUT-OF-PATTERN, with canonical `opal-data-{key}`. A data bucket carries its
    scope and nothing else.
  - A first token in V2, or in no vocabulary: RAISE.
- **B3** Any other `opal-{rest}` takes the platform form `opal-{account-id}-{purpose}`, using V8.
  - The account id as the second token: CONFORMANT.
  - The account id elsewhere: it moves to second.
  - No account id: it is inserted.
- **B4** A name that does not begin `opal-`: OUT-OF-PATTERN, with canonical `opal-313476888478-{name}`.
- **B5** An S3_BUCKET_POLICY carries its bucket's name exactly (`DATA.types_not_graded_by_kind`) and is graded as
  that bucket.

## K. KEYS -- `{source}/{scope}/{tier}/{table}/{partition}[/{object}]` (S1, `DATA.key`)

- **K0** Split on `/` after N5 and N6. A trailing `/` names a PREFIX: it is graded on the segments it has, and the
  missing trailing segments are not a failure.
- **K1 The form is read from segment 1.**
  - If segment 1 is `code`, the key is a legacy root code home: K6.
  - If it is any other tier (V7), the key is TIER-FIRST: K5.
  - If it is a V1 token, the key is SOURCE-FIRST: K2-K4.
  - Anything else RAISES, because segment 1 is neither a source nor a tier. That covers a V2 token, `json`,
    `config`, `cache` and a variable segment.
- **K2 SCOPE.** Segment 2 is the scope, in the LONG form (the `long` of its REGISTRY row): a V4 long form, a MASTER,
  `global`, or a PRODUCT key beneath a VENDOR source (`DATA.key.scope_rule`, SC1).
  - A short form or `bd` is an alias: it gives ALIAS with the long form.
  - A PRODUCT key beneath any other source is not the key's scope (`mdpf/global/...`, never `mdpf/mdpf/...`): the
    canonical form writes `{scope}` in its place, which the bucket decides (K5.c).
  - Anything else is not a scope: the canonical form inserts `{scope}` before it.
  - The rest of `DATA.key.scope_rule` (a vendor master keeps its own scope; any other key's scope is its AUDIENCE)
    turns on what the data is, which a name does not carry. It binds the namer, and a MASTER or a firm in segment 2 is
    graded as written.
- **K3 TIER AND TABLE.** Segment 3 is a tier (V7). If it is not, RAISE (`DATA.grade.unplaceable`): the name does not
  carry its tier and no source outside the name fills one, so the tier is not a placeholder (`DATA.grade.placeholder`
  names the system, source, scope and cadence slots only). Segment 4 is the table, in snake_case
  (`DATA.key.table_case`). In tier `code`, segment 4 is the tier the code builds: bronze, silver or gold
  (`DATA.key.code`).
- **K4 BELOW THE TABLE** (`DATA.key.partition`). Segment 5 is a `date=YYYY-MM-DD` partition, an entity partition
  `{entity}={id}` with the object after it, or a named leaf. In an entity partition, `{entity}` is the KEY COLUMN's
  name as the table carries it (`advisor_id=A123`), as `date` is the column in `date=YYYY-MM-DD` (P1).
  - **K4a Tier `platinum`.** If the key is ON the LIST (K7), the path keeps its bytes (`DATA.key.legacy_served_path`)
    and nothing below the table can fail. If it is not, it is a NEW served path:
    - its leaf must be a kebab-case `.json` file;
    - a segment in the partition slot must be an entity partition `{entity}={id}`.

    A leaf with `_` or capitals fails, and the canonical leaf is lowercased with `_` turned to `-`. A partition
    segment that is not an entity partition (a bare id, literal or variable) RAISES (`DATA.grade.unplaceable`): its
    entity is the key column's name, which the name does not carry and no source outside the name fills, so it is not
    a placeholder (`DATA.grade.placeholder`).
  - **K4b Other tiers.** Any segment is a valid named leaf, so below the table only K4a can fail.
- **K5 TIER-FIRST.** This is the legacy layout of the firm buckets, portal-v2 and mdpf (CENSUS s.5), and it is always
  OUT-OF-PATTERN (order). Build the canonical form in four steps:
  - **a.** Look at the segments after the tier. If the next one is a V1 key, it is the source; if the one after that
    is a scope, it is the scope. This matches the portal bucket's `platinum/{product}/{scope}/` layout.
  - **b.** In tier `platinum`, look up the tail (the segments after those that a consumed) in the LIST. Compare it
    with the part of each entry below `{source}/{scope}/platinum/`.
    - If exactly one entry matches, that entry gives the source (if a did not) and the tail keeps its bytes.
    - If none matches, rewrite the tail by K4a's new-path forms; a bare id in it RAISES, as K4a says.
  - **c.** A source or scope still unknown becomes the placeholder `{source}` or `{scope}`
    (`DATA.grade.placeholder`: the bucket fills both). The S3Key node carries no bucket, and the bucket is what decides
    them (SEED s.3; row `LGIC_NAMING-W1-S3`).
  - **d.** The canonical form is `source/scope/tier/tail`.
- **K6 LEGACY ROOT `code/`.** A key whose segment 1 is `code` is a legacy root code home. It is OUT-OF-PATTERN, and
  its canonical form is the code-tier key `{source}/{scope}/code/{built_tier}/{file}`, built by K5.a and K5.c. The
  verdict was ruled at v1.4 (`DATA.key.code`), and a verdict is not a mandate to move.
- **K7 THE LIST** is `org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json`: the `paths` array,
  with its own `portal_vintage` and `denominator`. Each entry is a key template, and each `{...}` in it stands for any
  value of the segment, or part of a segment, it occupies. A key is ON the list when it matches an entry segment by
  segment.
  - The LIST is CLOSED, because a frozen portal adds no request (`DATA.key.legacy_served_paths`).
  - If the file is absent, a key whose verdict turns on membership RAISES.

## G6. THE VERDICT

- **V-1** Build the canonical form with the grammar of the type.
- **V-2** If the canonical form carries a placeholder (`{system}`, `{source}`, `{scope}` or `{cadence}`, exactly the set `DATA.grade.placeholder` allows): OUT-OF-PATTERN.
- **V-3** If the canonical form equals the name byte for byte: CONFORMANT.
- **V-4** If replacing alias tokens in place with their canonical spellings turns the name into the canonical form,
  and nothing else changes: ALIAS. The alias replacements, with a firm's forms read from its REGISTRY `scopes.json`
  row (`DATA.firm_forms_source`), are:
  - `bd` to `blackdiamond`, or to the firm's form for the slot;
  - a long firm form to the short one, in a resource name or a secret;
  - a short form or `bd` to the long one, in a bucket or a key;
  - `mockadv` to the firm's form.
- **V-5** Otherwise: OUT-OF-PATTERN.

## 8. WHAT THIS RULE DOES NOT DECIDE

These gaps are filed as rows on the project channel, not settled here:
- `LGIC_NAMING-W1-S1`: the portal census the order names reads too little. The LIST was built from a widened census.
- `LGIC_NAMING-W1-S2`: a V2 token has no REGISTRY system row, so it RAISES wherever the system slot needs it.
- `LGIC_NAMING-W1-S3`: some canonical forms need a slot the name does not carry, so they carry a placeholder.
- `LGIC_NAMING-W3-S7`: FN1d RAISES when the subtraction empties a function. A function that is empty before it
  (`opal-gateway`) is outside that clause as R5 states it, while the ruling's reason, that a name with no function
  cannot be placed, would reach it too.

## 9. WORKED CASES

`why` cites the rule lines applied. The vintage is `LIVE_NAMES.json`'s own.

```json
{
 "vintage": "Built from the estate as of 2026-09-14 12:13:53 UTC",
 "worked_cases": [
  {"name": "mdpf-gold-lambda", "type": "LAMBDA", "verdict": "CONFORMANT", "canonical_form": "mdpf-gold-lambda", "why": "N1 ok; R1.a mdpf in V1 (SEED product); R4 no scope token (S5); R5 function gold; R6 last token lambda is LAMBDA's kind; V-3 equal"},
  {"name": "mdpf-lambda-lambda", "type": "LAMBDA", "verdict": "RAISE", "specimen": true, "why": "R1.a mdpf in V1; R4 no scope token; R6 the last token lambda is LAMBDA's kind and stays; R5 the one subtraction (FN1d) removes lambda, the resource's own kind, from the function [lambda], and that was its last token: RAISE (DATA.grade.unplaceable)"},
  {"name": "orion-orion-lambda-lambda", "type": "LAMBDA", "verdict": "RAISE", "specimen": true, "why": "R1.a orion in V1 (REGISTRY vendor); R4 no scope token; R6 the last lambda stays; R5 the one subtraction (FN1d) removes orion (written in the system slot, FN1b) and lambda (the own kind, FN1c) from the function [orion, lambda] in one pass, which leaves no function token: RAISE (DATA.grade.unplaceable), whichever rule removed the last token"},
  {"name": "inf-silver-chain", "type": "LAMBDA", "verdict": "OUT-OF-PATTERN", "canonical_form": "{system}-inf-silver-chain-lambda", "why": "R1.d t1 inf is a firm (V3): no later token in V1, so {system}; R4 scope inf (short); R6 chain is no kind, lambda appended; V-2 placeholder"},
  {"name": "inf-api-eclipse", "type": "LAMBDA", "verdict": "OUT-OF-PATTERN", "canonical_form": "eclipse-inf-api-lambda", "why": "R1.d t1 inf is a firm: the first later V1 token is eclipse (SEED vendor), the system; R4 scope inf after it; R5 function api; R6 api is API_GW's kind, not LAMBDA's, so lambda appended; V-5"},
  {"name": "etfs-canon-fanin-role", "type": "IAM_ROLE", "verdict": "CONFORMANT", "canonical_form": "etfs-canon-fanin-role", "why": "R1.a etfs (SEED product); R4 none; R5 canon-fanin; R6 role; V-3"},
  {"name": "bd-49f-runner-role", "type": "IAM_ROLE", "verdict": "ALIAS", "canonical_form": "blackdiamond-49f-runner-role", "why": "R3 bd next to firm 49f reads as the VENDOR blackdiamond; R1.a system bd->blackdiamond; R4 scope 49f short, in place; R6 role; V-4 the only change is the refused alias bd -> blackdiamond (S10)"},
  {"name": "FredMacroIngestionLambdaRole", "type": "IAM_ROLE", "verdict": "OUT-OF-PATTERN", "canonical_form": "fred-macro-ingestion-lambda-role", "residue_class": "camel-iam", "why": "G2 not in DATA.aws_fixed.by_name; N1 fails (capitals); N2 fred macro ingestion lambda role; R1.a fred (CENSUS s.3 feed); R4 none; R6 role; V-5 case is not an alias change"},
  {"name": "irpt-directory-policy", "type": "IAM_POLICY", "verdict": "CONFORMANT", "canonical_form": "irpt-directory-policy", "why": "R8 policy grammar; R1.a irpt (CENSUS s.3 product); R4 none; R5 purpose directory; R6 policy; V-3"},
  {"name": "s3-etfs-read", "type": "IAM_POLICY", "verdict": "OUT-OF-PATTERN", "canonical_form": "etfs-s3-read-policy", "residue_class": "purpose-first-policy", "why": "R1.d t1 s3 is a purpose word (V3): the first later V1 token etfs is the system, and s3 joins the function ahead of read; R6 read is no kind, policy appended (R8); V-5"},
  {"name": "opal-data-49financial#policy", "type": "IAM_POLICY", "verdict": "CONFORMANT", "canonical_form": "opal-data-49financial#policy", "why": "R8 X#policy is a resource policy: X graded by B; B2 rest 49financial is a V4 long form; #policy kept; V-3"},
  {"name": "mdpf-daily-runner-profile", "type": "INSTANCE_PROFILE", "verdict": "CONFORMANT", "canonical_form": "mdpf-daily-runner-profile", "why": "R1.a mdpf; R4 none; R5 daily-runner (a cadence word is free inside the function); R6 profile; V-3"},
  {"name": "default", "type": "SECURITY_GROUP", "verdict": "NOT-GRADED", "residue_class": "default-sg", "why": "G2 (G2.1) DATA.aws_fixed.by_name lists default for SECURITY_GROUP: AWS names every VPC's default group and it cannot be renamed, so the name is outside the grade's domain (RULING AW1) -- never a RAISE and never a fourth verdict"},
  {"name": "etfs-reports-reporter-sg", "type": "SECURITY_GROUP", "verdict": "CONFORMANT", "canonical_form": "etfs-reports-reporter-sg", "why": "R1.a etfs; R4 none; R5 reports-reporter; R6 sg; V-3"},
  {"name": "opal-portal-data-proxy-api", "type": "API_GW", "verdict": "CONFORMANT", "canonical_form": "opal-portal-data-proxy-api", "why": "R2 t2 portal is in neither V1 nor V2, so the system is opal (reserved); R4 none; R5 portal-data-proxy; R6 api; V-3"},
  {"name": "irpt-jobs", "type": "DYNAMODB_TABLE", "verdict": "OUT-OF-PATTERN", "canonical_form": "irpt-jobs-table", "why": "R1.a irpt; R4 none; R5 jobs; R6 jobs is no kind, table appended; V-5"},
  {"name": "irpt-export-dlq", "type": "SQS_QUEUE", "verdict": "CONFORMANT", "canonical_form": "irpt-export-dlq", "why": "R1.a irpt; R4 none; R5 export; R6 dlq is one of SQS_QUEUE's two kinds; V-3"},
  {"name": "etfs-reports-alerts", "type": "SNS_TOPIC", "verdict": "CONFORMANT", "canonical_form": "etfs-reports-alerts", "why": "R1.a etfs; R4 none; R5 reports; R6 alerts is one of SNS_TOPIC's two kinds; V-3"},
  {"name": "Inflection-SilverChain-DimConversionFailure", "type": "CW_ALARM", "verdict": "OUT-OF-PATTERN", "canonical_form": "{system}-inf-silver-chain-dim-conversion-failure-alarm", "why": "N1 fails; N2 inflection silver chain dim conversion failure; R1.d t1 inflection is a firm, no later V1 token, so {system}; R4 scope inflection -> inf (S4 short); R6 failure is no kind, alarm appended; V-2"},
  {"name": "pandas-pyarrow-layer", "type": "LAMBDA_LAYER", "verdict": "OUT-OF-PATTERN", "canonical_form": "{system}-pandas-pyarrow-layer", "residue_class": "library-first-layer", "why": "R1.e a LAMBDA_LAYER whose t1 pandas is in no vocabulary is a library: handled as R1.d, no later V1 token, so {system}; pandas and pyarrow stay in the function; R6 layer; V-2"},
  {"name": "mdpf-daily-runner", "type": "EC2_INSTANCE", "verdict": "CONFORMANT", "canonical_form": "mdpf-daily-runner", "why": "R1.a mdpf; R4 none; R5 daily; R6 runner is EC2_INSTANCE's kind; V-3"},
  {"name": "opal-stitch-produce", "type": "CODEBUILD_PROJECT", "verdict": "OUT-OF-PATTERN", "canonical_form": "opal-stitch-produce-build", "why": "R2 t2 stitch is in neither V1 nor V2, so the system is opal; R5 stitch-produce; R6 build appended; V-5"},
  {"name": "opal-cot-silver-run", "type": "SSM_DOCUMENT", "verdict": "OUT-OF-PATTERN", "canonical_form": "opal-cot-silver-run-document", "why": "R2 t2 cot is a firm, not a system, so the system is opal; R4 scope cot short, in place; R5 silver-run; R6 run is no kind, document appended; V-5"},
  {"name": "globgrph-serving", "type": "ECS_TASK_DEFINITION", "verdict": "OUT-OF-PATTERN", "canonical_form": "globgrph-serving-task", "why": "R1.a t1 globgrph is now in V1: systems.json registers it (row key globgrph, class PLATFORM_SUBSYSTEM, minted by LGIC_ENFORCE EN-r-2), so the system is globgrph directly; R1.c's RAISE, cited when this case had no row (row LGIC_NAMING-W1-S2), no longer applies once the row lands (S22, RULING R-5); R4 no scope; R5 function serving; R6 serving is not ECS_TASK_DEFINITION's kind (task), so task is appended; V-5"},
  {"name": "YangDataPipeline", "type": "STATE_MACHINE", "verdict": "OUT-OF-PATTERN", "canonical_form": "yang-data-pipeline-sfn", "why": "N1 fails; N2 yang data pipeline; R1.a yang (CENSUS s.3 product); R5 data-pipeline; R6 sfn appended; V-5"},
  {"name": "opal-gateway", "type": "LOAD_BALANCER", "verdict": "OUT-OF-PATTERN", "canonical_form": "gateway-lb", "why": "R2 t2 gateway is in V1: systems.json registers it, class PLATFORM_SUBSYSTEM (2026-09-15, the registry owner under CLAUDE.md Rule 30, on 1.0.0_SA_CTO msg 97130), so opal before it is a null prefix and drops; R1.a system gateway; R4 none; R5 no function token; R6 lb appended; V-5"},
  {"name": "opal-globgrph", "type": "ECS_CLUSTER", "verdict": "OUT-OF-PATTERN", "canonical_form": "globgrph-cluster", "why": "R2 t2 globgrph is in V1: systems.json registers it (row key globgrph, class PLATFORM_SUBSYSTEM, minted by LGIC_ENFORCE EN-r-2), so opal before it is a null prefix and drops, as with opal-gateway (section 9); R2's RAISE branch for an unresolved token, cited when this case had no row (row LGIC_NAMING-W1-S2), no longer applies once the row lands (S22, RULING R-5); R1.a system globgrph; R4 none; R5 no function token; R6 cluster appended (ECS_CLUSTER's kind); V-5"},
  {"name": "etfs-netassets-daily", "type": "EVENT_RULE", "verdict": "CONFORMANT", "canonical_form": "etfs-netassets-daily", "why": "R1.a etfs; R4 none; R5 netassets; R7 daily is a cadence (V6) in the last slot; V-3"},
  {"name": "bd-49f-session-complete", "type": "EVENT_RULE", "verdict": "OUT-OF-PATTERN", "canonical_form": "blackdiamond-49f-session-complete-{cadence}", "why": "R3 bd next to 49f is the vendor; R1.a system blackdiamond; R4 scope 49f; R5 session-complete; R7 no cadence token and no on- run, so {cadence} appended; V-2"},
  {"name": "wsb-49f-model-aua-pull-daily", "type": "SCHEDULE", "verdict": "OUT-OF-PATTERN", "canonical_form": "{system}-49f-wsb-model-aua-pull-daily", "residue_class": "workstream-schedule", "why": "R1.d t1 wsb is a workstream code (V3, S6 never a system): no later V1 token, so {system}; wsb joins the function; R4 scope 49f; R7 daily last; V-2"},
  {"name": "mdpf-accrual-bridge-daily", "type": "SCHEDULE", "verdict": "CONFORMANT", "canonical_form": "mdpf-accrual-bridge-daily", "why": "R1.a mdpf; R4 none; R5 accrual-bridge; R7 daily last; V-3"},
  {"name": "/aws/lambda/mdpf-gold-lambda", "type": "LOG_GROUP", "verdict": "CONFORMANT", "canonical_form": "/aws/lambda/mdpf-gold-lambda", "why": "L1 /aws/{service}/{rest}; L2 lambda -> LAMBDA; L3 mdpf-gold-lambda is CONFORMANT by R (see the LAMBDA case), so the log group is; V-3"},
  {"name": "opal-data-bd", "type": "S3_BUCKET", "verdict": "ALIAS", "canonical_form": "opal-data-49financial", "why": "B2 data bucket; rest bd, with no firm next to it, reads as the FIRM 49financial (R3); a bucket takes the LONG form (S4); V-4 the only change is the refused alias bd -> 49financial"},
  {"name": "opal-cloudtrail-logs-313476888478", "type": "S3_BUCKET", "verdict": "OUT-OF-PATTERN", "canonical_form": "opal-313476888478-cloudtrail-logs", "why": "B3 platform bucket; the account id (V8) is the last token, not the second, so it moves to second; V-5"},
  {"name": "opal-data-cot", "type": "S3_BUCKET_POLICY", "verdict": "ALIAS", "canonical_form": "opal-data-cottonwood", "why": "B5 graded as its bucket; B2 rest cot is the short form; a bucket takes the LONG form cottonwood (S4); V-4"},
  {"name": "platinum/firm/header_metrics.json", "type": "S3Key", "verdict": "OUT-OF-PATTERN", "canonical_form": "advi/{scope}/platinum/firm/header_metrics.json", "form": "legacy-served", "why": "K1 segment 1 is a tier: TIER-FIRST, K5; K5.a firm is not a V1 key; K5.b tail firm/header_metrics.json matches exactly one LIST entry, which gives source advi and keeps the tail's bytes; K5.c the scope is the bucket's, so {scope}; V-2"},
  {"name": "code/gold/*", "type": "S3Key", "verdict": "OUT-OF-PATTERN", "canonical_form": "{source}/{scope}/code/gold/*", "form": "legacy-root-code", "why": "K1 segment 1 is code: K6 legacy root code home, OUT-OF-PATTERN as ruled at v1.4 (DATA.key.code); canonical is the code-tier key; K5.a gold is not a V1 key; K5.c source and scope unknown from the name; V-2"},
  {"name": "schwab/08335338/silver/fact_rps/", "type": "S3Key", "verdict": "CONFORMANT", "canonical_form": "schwab/08335338/silver/fact_rps/", "why": "K1 schwab in V1: SOURCE-FIRST; K2 08335338 is a MASTER scope (SEED; S1 allows a vendor master); K3 silver, table fact_rps snake_case; K0 trailing / is a prefix, graded on its segments; V-3"},
  {"name": "mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz", "type": "S3Key", "verdict": "CONFORMANT", "canonical_form": "mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz", "form": "code-tier", "specimen": true, "why": "K1 mdpf in V1; K2 global; K3 tier code, table gold = the tier the code builds (DATA.key.code); K4b the bundle is a named leaf; V-3. The CTO's S7 vector"},
  {"name": "advi/49financial/platinum/advisors/advisor_id=A123/positions.json", "type": "S3Key", "verdict": "CONFORMANT", "canonical_form": "advi/49financial/platinum/advisors/advisor_id=A123/positions.json", "form": "entity-partition", "specimen": true, "why": "K1 advi in V1; K2 49financial long; K3 platinum, table advisors; K4a not ON the LIST, so a NEW served path: advisor_id=A123 is an entity partition and positions.json a kebab-case .json leaf; V-3"},
  {"name": "advi/49financial/platinum/firm/fee_efficiency.json", "type": "S3Key", "verdict": "CONFORMANT", "canonical_form": "advi/49financial/platinum/firm/fee_efficiency.json", "form": "legacy-served", "pair": "on-list", "specimen": true, "why": "K1 advi; K2 49financial long; K3 platinum, table firm; K4a ON the LIST (K7: the portal requests firm/fee_efficiency.json), so the path keeps its bytes and the snake_case leaf is kept; V-3"},
  {"name": "advi/49financial/platinum/firm/top_holdings.json", "type": "S3Key", "verdict": "OUT-OF-PATTERN", "canonical_form": "advi/49financial/platinum/firm/top-holdings.json", "pair": "off-list", "specimen": true, "why": "Same shape as the on-list case. K1 advi; K2 49financial; K3 platinum, table firm; K4a NOT on the LIST (no entry matches), so a NEW served path, and its leaf must be kebab-case: top_holdings.json -> top-holdings.json; V-5"},
  {"name": "blackdiamond/49f/credentials", "type": "SECRET", "verdict": "CONFORMANT", "canonical_form": "blackdiamond/49f/credentials", "why": "S2 blackdiamond in V1; S3 segment 2 is 49f, the SHORT form (S4); S4 purpose credentials; V-3"},
  {"name": "inf/otp-relay/token", "type": "SECRET", "verdict": "OUT-OF-PATTERN", "canonical_form": "{system}/inf/otp-relay/token", "why": "S2 segment 1 inf is a firm (R1.d): no later segment opens with a V1 token, so {system}; S3 inf moves to the scope segment; S4 purpose otp-relay/token; V-2"},
  {"name": "4ba4753c-98f4-47c0-9a47-6dacaa1b6370", "type": "KMS_KEY", "verdict": "NOT-GRADED", "why": "G1.2 DATA.types_not_graded_by_kind.KMS_KEY begins NOT GRADED (AWS-issued identifier)"}
 ]
}
```

## 10. SCHEMA COVERAGE

Every field of `NAMING_SCHEMA.json` that changed from v1.4 (@`e04b802fe9`, the version this rule was cut at) to v1.10
(this rule's base @`5a12d0b97c`), derived at this base by the same grain `check_ln_r4.py g1-coverage` used through
v1.9, never typed: a top-level key, or each second-level key of a key that is an object in both versions; a key added
or removed whole counts once; `version`, `changelog` and `ratified_by` are excluded. Each line names every step of
this rule that reads the field. v1.9 -> v1.10 adds two: `alias_adjacency` (ADDED WHOLE) and `refused_tokens.bd`
(its prose changed to point at `alias_adjacency`) -- both read by R3 (A-3, round-4 analysis s.2).

- COVERS R3: reads `alias_adjacency` (`alias_adjacency.bd`) and `refused_tokens.bd` -- ADJACENCY to a firm token,
  never position, decides whether `bd` reads as VENDOR `blackdiamond` or FIRM `49financial` (v1.10, A-3)
- COVERS alias_adjacency: R3
- COVERS refused_tokens.bd: R3
- COVERS aws_fixed: G2, G2.1, G2.2, L1
- COVERS firm_forms: R4, S3, B2, K2, V-4
- COVERS firm_forms_source: R4, S3, B2, K2, V-4
- COVERS grade.placeholder: V-2, R1, R7, K3, K4a, K5
- COVERS iam_policy.purpose_slot: R8, R5
- COVERS key.partition: K4, K4a
- COVERS key.scope_rule: K2
- COVERS kind.closed_at_l4: R5, R6
- COVERS resource.function: R5
- COVERS resource.qualifier: R5
- COVERS rows_owner: R1, R2, R4
- COVERS secret.purpose: S4
- COVERS system.vendor_through_tiers: NO STEP -- which system a resource should take turns on what it builds from (one vendor's feed, or a combination of feeds), and grade(name, type) receives no description of that; R1 takes the system token the name carries, so the clause binds the namer.
- COVERS tf_type_map: G1.1
- COVERS tf_type_map_note: G1.1
- COVERS tf_unmapped_own_name: G1.1
- COVERS tf_unmapped_own_name_note: G1.1

SCHEMA COVERAGE SINCE v1.4: 19 of 19
