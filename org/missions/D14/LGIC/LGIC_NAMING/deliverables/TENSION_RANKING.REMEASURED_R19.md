<!-- ADDITIVE SIBLING. The original is READ-ONLY and not one byte of it moved.
     Author: 0.9.0_WK_LGIC_ENFORCE~1, LGIC_ENFORCE round 19, cell EN-h-1.
     Hand side re-measured at the census vintage the MACHINE side used:
       Built from the estate as of 2026-09-18 12:17:28 UTC. Stitch source: stitch-codebuild built 2026-09-18T03:01:14Z. manifest 247f3933a1fd
       org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NAMING_CENSUS_REPORT.r8.md @54659987c0
     The machine side is NOT re-graded here and grade() is never called.
-->

# TENSION RANKING -- HAND SIDE RE-MEASURED (round 19)

Sibling of `org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md`. 10 ranked surfaces, re-quoted at the r8 census vintage.

```json
{
 "vintage": "Built from the estate as of 2026-09-18 12:17:28 UTC. Stitch source: stitch-codebuild built 2026-09-18T03:01:14Z. manifest 247f3933a1fd",
 "note": "Re-measured hand side of TENSION_RANKING.md. The original states 'Nothing was measured again for this file' and quotes infra/logic/09_NAMING_CENSUS.md of 2026-09-13; its instrument is 'quote the naming census', so the re-measure RE-RUNS THAT INSTRUMENT at 54659987c0. Rank 5 is NOT re-quoted: its hand figure comes from comp-find's drift_class over the live graph, which the census cannot reproduce, so re-quoting would fabricate an agreement.",
 "rows": [
  {
   "rank": 1,
   "surface": "Firm spelled `bd`/`49f`/`inf`/`cot` in ~330 resource names, firm-as-system in ~210",
   "cost": "The cross-firm fence is a name-pattern list (`role/cot-*`, `role/inf-*`), so a resource named with another spelling of the same firm is outside the fence and nothing reports it. Finding one firm's resources takes a search under every spelling in two positions (49 Financial: `bd` ~120, `49f` ~45, `49financial` 4). Each new firm-scoped name copies whichever spelling its author last saw.",
   "figures": [
    {
     "figure": "names carrying bd/49f/inf/cot as a token",
     "hand_remeasured": 397,
     "hand_at_round_9": 330,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "firm as FIRST token over LAMBDA/IAM_ROLE/EVENT_RULE/LOG_GROUP (hand's grain: census s.1(c) pos0 47+55+45+57=204)",
     "hand_remeasured": 206,
     "hand_at_round_9": 210,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "firm as FIRST token over every type (no hand figure at this grain; census s.3 first-token inf 136 + bd 119 + cot 30 = 285)",
     "hand_remeasured": 296,
     "hand_at_round_9": 285,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "bd as FIRST token (hand's grain: census s.3 first-token 119)",
     "hand_remeasured": 120,
     "hand_at_round_9": 120,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "49f anywhere (hand's grain undeclared; census s.2 per-type sums are any-position)",
     "hand_remeasured": 68,
     "hand_at_round_9": 45,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "49financial anywhere (census s.1: 1 role, 1 policy, 1 table, 1 bucket)",
     "hand_remeasured": 7,
     "hand_at_round_9": 4,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "inf as FIRST token (hand's grain: census s.3 first-token 136)",
     "hand_remeasured": 138,
     "hand_at_round_9": 140,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "inflection anywhere (census s.1: 1 role, 3 alarms)",
     "hand_remeasured": 6,
     "hand_at_round_9": 4,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "cot as FIRST token (hand's grain: census s.3 first-token 30)",
     "hand_remeasured": 35,
     "hand_at_round_9": 30,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "cottonwood anywhere",
     "hand_remeasured": 4,
     "hand_at_round_9": 2,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 2,
   "surface": "`bd` = vendor AND firm",
   "cost": "A name holding `bd` does not say whether it means Black Diamond (the vendor) or 49 Financial (the firm), so someone has to know the resource to tell which. A search or pattern on `bd` returns vendor and firm names mixed, including other firms' resources (`cot-bd-session-daily-et`). Figures: 119 names start with `bd` (census 3); the brief puts it at ~120 names plus the bucket `opal-data-bd` and one IAM fence pattern.",
   "figures": [
    {
     "figure": "names whose FIRST token is bd",
     "hand_remeasured": 120,
     "hand_at_round_9": 119,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 3,
   "surface": "Key grammar split: source-first (assets) vs tier-first (bd/inf/cot/49financial/portal-v2/mdpf)",
   "cost": "Anyone writing or reading an S3 key has to know first which of two grammars the key's bucket uses, and the same data is not the same key string across the monolith, a firm bucket and a product bucket. The two D8 migrations are this row. Figures: six tier-first bucket families against one source-first (assets); neither source counts keys per grammar.",
   "figures": [
    {
     "figure": "tier-first keys present in the census (hand: split exists, >=1)",
     "hand_remeasured": 1,
     "hand_at_round_9": 1,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "tier-first keys grade() rules OUT-OF-PATTERN, as a share of tier-first (hand: ruling is source-first => all)",
     "hand_remeasured": 94,
     "hand_at_round_9": 94,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 4,
   "surface": "96 camel IAM policies incl. 6× `CloudWatchLogs` duplicates; 6 camel roles; 6 camel alarms",
   "cost": "Six policies share the name `CloudWatchLogs`, so a name picks out none of them and only the ARN can. Camel-case names do not split on `-`, so any tool reading names by kebab tokens gets them wrong or drops them, and they have to be handled one at a time. Figures: 96 of 502 customer-managed policies are camel; 6 camel roles; 6 camel alarms.",
   "figures": [
    {
     "figure": "camel IAM policies",
     "hand_remeasured": 99,
     "hand_at_round_9": 96,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "customer-managed IAM policies",
     "hand_remeasured": 515,
     "hand_at_round_9": 502,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "CloudWatchLogs policies",
     "hand_remeasured": 6,
     "hand_at_round_9": 6,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "camel IAM roles",
     "hand_remeasured": 6,
     "hand_at_round_9": 6,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "CW alarms carrying capitals (hand's grain: census s.2 '6 Camel/Pascal-kebab', hyphens allowed)",
     "hand_remeasured": 13,
     "hand_at_round_9": 6,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 5,
   "surface": "339 `LIVE-no-DECLARED` nodes (Lambda 15, role 16, rule 10, log 68, policy 36 …)",
   "cost": "These exist in AWS with no Terraform declaration, so the authoring-time naming flagger cannot check them. Each has to be found and then declared or retired by hand before any naming rule reaches it, and nobody knows how they were made. Figures: 339 in total; the census breaks down 145 of them by type (Lambda 15, role 16, policy 36, rule 10, log 68), not the other 194.",
   "figures": [
    {
     "figure": "live names with no same (name,type) on the census repo plane",
     "hand_remeasured": 339,
     "hand_at_round_9": 339,
     "basis": "UNREVISED-INSTRUMENT-GAP"
    },
    {
     "figure": "LAMBDA",
     "hand_remeasured": 15,
     "hand_at_round_9": 15,
     "basis": "UNREVISED-INSTRUMENT-GAP"
    },
    {
     "figure": "IAM_ROLE",
     "hand_remeasured": 16,
     "hand_at_round_9": 16,
     "basis": "UNREVISED-INSTRUMENT-GAP"
    },
    {
     "figure": "EVENT_RULE",
     "hand_remeasured": 10,
     "hand_at_round_9": 10,
     "basis": "UNREVISED-INSTRUMENT-GAP"
    },
    {
     "figure": "LOG_GROUP",
     "hand_remeasured": 68,
     "hand_at_round_9": 68,
     "basis": "UNREVISED-INSTRUMENT-GAP"
    },
    {
     "figure": "IAM_POLICY",
     "hand_remeasured": 36,
     "hand_at_round_9": 36,
     "basis": "UNREVISED-INSTRUMENT-GAP"
    }
   ],
   "result_against_the_census": "DISAGREE"
  },
  {
   "rank": 6,
   "surface": "Project/workstream codes as systems (`gldinc`, `quartz`, `cmtque`, `wsb`, `wsd`)",
   "cost": "A project code in the system slot outlives its project and then reads as a system that no registry lists, so learning what owns the resource takes knowing the project's history. With no closed list of systems, nothing stops a new code from being minted into the slot. Figures: 28 names (gldinc 7, quartz 5, cmtque 4, wsb 6, wsd 6), among 118 first tokens with no registry.",
   "figures": [
    {
     "figure": "gldinc",
     "hand_remeasured": 7,
     "hand_at_round_9": 7,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "quartz",
     "hand_remeasured": 5,
     "hand_at_round_9": 5,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "cmtque",
     "hand_remeasured": 4,
     "hand_at_round_9": 4,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "wsb",
     "hand_remeasured": 6,
     "hand_at_round_9": 6,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "wsd",
     "hand_remeasured": 6,
     "hand_at_round_9": 6,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "total",
     "hand_remeasured": 28,
     "hand_at_round_9": 28,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 7,
   "surface": "`opal-` as a null prefix (445 names, 18 types)",
   "cost": "Filtering on `opal-*` returns 445 names across 18 types that are not one system. Where `opal-` is only a prefix, the real system is a later token (`opal-assets-mdpf-portal-publisher`), so a reader who takes the first token as the system gets it wrong and has to read further along.",
   "figures": [
    {
     "figure": "names whose first token is opal",
     "hand_remeasured": 508,
     "hand_at_round_9": 445,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "types among them",
     "hand_remeasured": 22,
     "hand_at_round_9": 18,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 8,
   "surface": "Purpose-first IAM policy names (`cross-*` 39, `s3-*` 29, `cloudwatch-*` 23)",
   "cost": "IAM policies use two grammars. A search for a system's policies by its system prefix misses every policy that starts with the purpose, and finding which system such a policy serves means reading the policy, not its name. Figures: 91 purpose-first names (39 + 29 + 23); only 42% of policy names put the system first.",
   "figures": [
    {
     "figure": "cross-*",
     "hand_remeasured": 40,
     "hand_at_round_9": 39,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "s3-*",
     "hand_remeasured": 33,
     "hand_at_round_9": 29,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "cloudwatch-*",
     "hand_remeasured": 23,
     "hand_at_round_9": 23,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "total",
     "hand_remeasured": 96,
     "hand_at_round_9": 91,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 9,
   "surface": "Secrets: 10 of 96 off the slash-path grammar",
   "cost": "A lookup by the `{system}/{scope}/` path prefix misses these 10 secrets, so anyone looking for one has to know its name already. The brief calls this small. Figures: 86 of 96 slash-path; the other 10 are kebab (8) and flat or camel (2).",
   "figures": [
    {
     "figure": "secrets",
     "hand_remeasured": 99,
     "hand_at_round_9": 96,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    },
    {
     "figure": "secrets with no slash",
     "hand_remeasured": 10,
     "hand_at_round_9": 10,
     "basis": "REVISED-REQUOTED-AT-CENSUS-VINTAGE"
    }
   ],
   "result_against_the_census": "AGREE"
  },
  {
   "rank": 10,
   "surface": "Terraform LABELS and tags — UNMEASURED",
   "cost": "This is where the flagger works when someone writes a name, and it is the one plane the census could not see. Nobody can say how far labels and tags depart from the pattern, and nobody can size a flagger rule for them. Figure: none; census section 5 states Terraform labels, module names and tags were not measured.",
   "figures": [],
   "result_against_the_census": "AGREE"
  }
 ]
}
```
