# LGIC_NAMING -- TENSION RANKING: what each of the ten naming surfaces costs today

**Cell:** `LN-t-1` (PRD candidate N7; serves FWD-6). **Author:** `0.9.0_WK_LGIC_NAMING~2`, task order
`LGIC_NAMING.TO-LN-t-1`.

**Sources, and nothing else:** the ten rows of Part IV.7 of `docs/briefs/d14-naming-schema-brief-20260913.md` at
commit `1b42dbe758` (read with `git show 1b42dbe758:<path>`, lines 179-191), and `infra/logic/09_NAMING_CENSUS.md`
(measured 2026-09-13 ~03:3xZ UTC over 2,531 live nodes, 33 node types; 1,912 names over the 19 types we name).
Every figure below is quoted from one of those two files, with its section. Nothing was measured again for this
file.

**Order and scope.** The rows are in the brief's order and keep its ranks. Nothing is re-ranked. Each row states
only what the surface costs today: what breaks, what someone has to do by hand, or what it blocks. It does not
propose a fix. Any fix is minted where the resource lives, citing the row number here.

Where neither source gives a figure for a cost, the row says so and does not supply one.

---

## 1. Firm spelled `bd`/`49f`/`inf`/`cot` in ~330 resource names, firm-as-system in ~210

**Costs today.**
- **Breaks:** the cross-firm fence is a list of name patterns (`role/cot-*`, `role/inf-*`). A resource named with
  any other spelling of the same firm falls outside the list, and nothing reports that it did.
- **By hand:** finding every resource that belongs to one firm takes a search under each of its spellings, in two
  positions. For 49 Financial that is three spellings.
- **Blocks:** a new firm-scoped name has no rule to follow, so its author copies whichever spelling they saw
  last. The runner-name collision (D8 brief IV.11) is one case of this.

**Figures.** 49 Financial is `bd` ~120, `49f` ~45 and `49financial` 4. Inflection is `inf` ~140 and `inflection` 4.
Cottonwood is `cot` ~30 and `cottonwood` 2 (brief IV.3; census §1.3, §4). The firm is the first token (it sits
where the system should) in ~210 names and the second token in ~75 (brief IV.3).

## 2. `bd` = vendor AND firm

**Costs today.**
- **By hand:** a name that holds `bd` does not say whether it means Black Diamond (the vendor) or 49 Financial
  (the firm). Someone has to know the resource to tell which. `cot-bd-session-daily-et` is a Cottonwood resource
  in which `bd` is the vendor. In `bd-allocations` and in the bucket `opal-data-bd`, `bd` is the firm (census §1.4).
- **Breaks:** a search or a pattern keyed on `bd` returns vendor names and firm names mixed together, including
  resources that belong to other firms. This is inside the tenant boundary, which is exactly where the fence needs
  the firm to be readable.

**Figures.** `bd` is the first token of 119 names (census §3). The brief puts it at ~120 names, plus one bucket
(`opal-data-bd`) and one IAM fence pattern (brief IV.4).

## 3. Key grammar split: source-first (assets) vs tier-first (bd/inf/cot/49financial/portal-v2/mdpf)

**Costs today.**
- **By hand:** anyone writing or reading an S3 key has to know first which of two grammars the key's bucket uses.
  Assets puts the source first. The firm buckets, portal-v2 and mdpf put the tier first.
- **Breaks:** the same data does not read as the same key string in the monolith, a firm bucket and a product
  bucket.
- **Blocks:** the two D8 migrations are this row (brief IV.7). Until they land, the split stays, and the brief
  records the ruling as source-first.

**Figures.** The brief lists six tier-first bucket families (bd, inf, cot, 49financial, portal-v2, mdpf) against
one that is source-first (assets). Neither source counts keys or tables per grammar. The census does not measure key
grammar at all. It points to `01_CENSUS.md` (36 buckets) and `06_CONFORMANCE_LEDGER.md` for that (census §5).

## 4. 96 camel IAM policies incl. 6× `CloudWatchLogs` duplicates; 6 camel roles; 6 camel alarms

**Costs today.**
- **Breaks:** six policies share the name `CloudWatchLogs`. A name picks out none of them; only the ARN can.
- **Breaks:** camel-case names do not split on `-`, so any tool that reads names by kebab tokens gets them wrong or
  drops them.
- **By hand:** these names have to be found and handled one at a time, because no pattern check can read them.

**Figures.** 96 camel policies of 502 customer-managed (census §1, §2). `CloudWatchLogs` appears 6 times (brief
IV.2). There are 6 camel roles, for example `FredIngestionLambdaRole`, and 6 camel alarms (census §1). The census
counts the camel IAM and alarm residue together at ~110 (census §2 totals).

## 5. 339 `LIVE-no-DECLARED` nodes (Lambda 15, role 16, rule 10, log 68, policy 36 …)

**Costs today.**
- **Blocks:** these resources exist in AWS but no Terraform declares them. The naming flagger works at authoring
  time, so it cannot check them. The brief expects the pattern to keep breaking here.
- **By hand:** each one has to be found and then declared or retired before any naming rule can reach it. Nobody
  knows how they were made: console, CLI or a retired module (census §5).

**Figures.** 339 nodes in total (brief IV.7; census §5). By type, the census table lists Lambda 15, IAM role 16,
IAM policy 36, event rule 10 and log group 68. That is 145 of the 339. The census does not say which types the
other 194 are.

## 6. Project/workstream codes as systems (`gldinc`, `quartz`, `cmtque`, `wsb`, `wsd`)

**Costs today.**
- **By hand:** a project code in the system slot outlives its project. After that it reads as a system, but no
  registry lists it. To learn what owns such a resource, someone has to know the project's history.
- **Blocks:** with no closed list of systems, nothing stops a new project code from being minted into the slot.

**Figures.** `gldinc` 7, `quartz` 5, `cmtque` 4, `wsb` 6, `wsd` 6: 28 names in total (census §3; brief IV.5). The
estate has 118 distinct first tokens and no registry of which ones are systems (census §3).

## 7. `opal-` as a null prefix (445 names, 18 types)

**Costs today.**
- **Breaks:** filtering on `opal-*` returns 445 names that are not one system; the brief reads them as eighteen.
- **By hand:** where `opal-` is only a prefix, the real system is the next token or the one after
  (`opal-assets-mdpf-portal-publisher`, `opal-bd-49f-session-fetch`). A reader who takes the first token as the
  system gets it wrong, and has to read further along the name.

**Figures.** 445 names across 18 types (census §3; brief IV.5).

## 8. Purpose-first IAM policy names (`cross-*` 39, `s3-*` 29, `cloudwatch-*` 23)

**Costs today.**
- **Breaks:** IAM policies use two grammars. Searching for a system's policies by its system prefix misses every
  policy that starts with the purpose instead.
- **By hand:** finding which system a purpose-first policy serves means reading the policy, not its name.

**Figures.** `cross-*` 39, `s3-*` 29, `cloudwatch-*` 23: 91 names. The census rounds this to ~90 purpose-first
policies (census §2 totals). Only 42% of IAM policy names put the system first (census §2).

## 9. Secrets: 10 of 96 off the slash-path grammar

**Costs today.**
- **By hand:** a lookup by the `{system}/{scope}/` path prefix misses these 10 secrets, so anyone looking for one
  has to know its name already. The brief calls this cost small: the slash-path grammar is otherwise the best-kept
  grammar in the estate.

**Figures.** 86 of 96 secrets are slash-path. The other 10 are kebab (8) and flat or camel (2) (census §2).

## 10. Terraform LABELS and tags — UNMEASURED

**Costs today.**
- **Blocks:** Terraform labels and tags are where the flagger works when someone writes a name, and they are the
  one plane the census could not see. So nobody can say how far they depart from the pattern, and nobody can size a
  flagger rule for them.

**Figures.** None. The census states this plane was not measured: Terraform resource labels and module names were
out of reach, and tags were not tokenised (census §5).

---

```json
{"rows": [
  {"rank": 1, "surface": "Firm spelled `bd`/`49f`/`inf`/`cot` in ~330 resource names, firm-as-system in ~210", "cost": "The cross-firm fence is a name-pattern list (`role/cot-*`, `role/inf-*`), so a resource named with another spelling of the same firm is outside the fence and nothing reports it. Finding one firm's resources takes a search under every spelling in two positions (49 Financial: `bd` ~120, `49f` ~45, `49financial` 4). Each new firm-scoped name copies whichever spelling its author last saw."},
  {"rank": 2, "surface": "`bd` = vendor AND firm", "cost": "A name holding `bd` does not say whether it means Black Diamond (the vendor) or 49 Financial (the firm), so someone has to know the resource to tell which. A search or pattern on `bd` returns vendor and firm names mixed, including other firms' resources (`cot-bd-session-daily-et`). Figures: 119 names start with `bd` (census 3); the brief puts it at ~120 names plus the bucket `opal-data-bd` and one IAM fence pattern."},
  {"rank": 3, "surface": "Key grammar split: source-first (assets) vs tier-first (bd/inf/cot/49financial/portal-v2/mdpf)", "cost": "Anyone writing or reading an S3 key has to know first which of two grammars the key's bucket uses, and the same data is not the same key string across the monolith, a firm bucket and a product bucket. The two D8 migrations are this row. Figures: six tier-first bucket families against one source-first (assets); neither source counts keys per grammar."},
  {"rank": 4, "surface": "96 camel IAM policies incl. 6× `CloudWatchLogs` duplicates; 6 camel roles; 6 camel alarms", "cost": "Six policies share the name `CloudWatchLogs`, so a name picks out none of them and only the ARN can. Camel-case names do not split on `-`, so any tool reading names by kebab tokens gets them wrong or drops them, and they have to be handled one at a time. Figures: 96 of 502 customer-managed policies are camel; 6 camel roles; 6 camel alarms."},
  {"rank": 5, "surface": "339 `LIVE-no-DECLARED` nodes (Lambda 15, role 16, rule 10, log 68, policy 36 …)", "cost": "These exist in AWS with no Terraform declaration, so the authoring-time naming flagger cannot check them. Each has to be found and then declared or retired by hand before any naming rule reaches it, and nobody knows how they were made. Figures: 339 in total; the census breaks down 145 of them by type (Lambda 15, role 16, policy 36, rule 10, log 68), not the other 194."},
  {"rank": 6, "surface": "Project/workstream codes as systems (`gldinc`, `quartz`, `cmtque`, `wsb`, `wsd`)", "cost": "A project code in the system slot outlives its project and then reads as a system that no registry lists, so learning what owns the resource takes knowing the project's history. With no closed list of systems, nothing stops a new code from being minted into the slot. Figures: 28 names (gldinc 7, quartz 5, cmtque 4, wsb 6, wsd 6), among 118 first tokens with no registry."},
  {"rank": 7, "surface": "`opal-` as a null prefix (445 names, 18 types)", "cost": "Filtering on `opal-*` returns 445 names across 18 types that are not one system. Where `opal-` is only a prefix, the real system is a later token (`opal-assets-mdpf-portal-publisher`), so a reader who takes the first token as the system gets it wrong and has to read further along."},
  {"rank": 8, "surface": "Purpose-first IAM policy names (`cross-*` 39, `s3-*` 29, `cloudwatch-*` 23)", "cost": "IAM policies use two grammars. A search for a system's policies by its system prefix misses every policy that starts with the purpose, and finding which system such a policy serves means reading the policy, not its name. Figures: 91 purpose-first names (39 + 29 + 23); only 42% of policy names put the system first."},
  {"rank": 9, "surface": "Secrets: 10 of 96 off the slash-path grammar", "cost": "A lookup by the `{system}/{scope}/` path prefix misses these 10 secrets, so anyone looking for one has to know its name already. The brief calls this small. Figures: 86 of 96 slash-path; the other 10 are kebab (8) and flat or camel (2)."},
  {"rank": 10, "surface": "Terraform LABELS and tags — UNMEASURED", "cost": "This is where the flagger works when someone writes a name, and it is the one plane the census could not see. Nobody can say how far labels and tags depart from the pattern, and nobody can size a flagger rule for them. Figure: none; census section 5 states Terraform labels, module names and tags were not measured."}
]}
```
