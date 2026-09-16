# RESULT -- `LGIC_NAMING.TO-LN-g-1` (cell `LN-g-1`): the written grading rule and the legacy served list

**Worker:** `0.9.0_WK_LGIC_NAMING~1` · **Branch:** `wk-lgic-naming-1-1` off CLOUD @`6a5b276f8b` · **Portal read:**
@`e85f6eb84f` (read-only)

## What landed

| path | what |
|---|---|
| `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md` | the rule, written to be applied by hand. It runs G1 domain, G2 AWS-fixed names, G3 normalise, then V the vocabularies, then the grammar of the type (R resource, S secret, L log group, B bucket, K key), then G6 the verdict. It ends with ONE fenced json block of 43 worked cases. |
| `org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json` | the closed list: 39 key templates below `{source}/{scope}/platinum/`, each with its request site in the portal, and 8 exclusions with reasons. |
| `org/missions/D14/LGIC/LGIC_NAMING/surprise-channel/investigations/INVESTIGATION_v1.md` | rows `LGIC_NAMING-W1-S1` .. `W1-S4` appended. |

## The worked cases, counted from the json block

| count | what |
|---|---|
| 43 cases | 39 live names from `LIVE_NAMES.json` (vintage 2026-09-14 12:13:53 UTC), and 4 specimens: the code-tier and entity-partition forms, and the two halves of the pair |
| verdicts | 18 CONFORMANT, 3 ALIAS, 18 OUT-OF-PATTERN, 3 RAISE, 1 NOT-GRADED |
| 25 of 25 graded types | every type has at least one case |
| 5 of 5 residue classes | `camel-iam` FredMacroIngestionLambdaRole; `purpose-first-policy` s3-etfs-read; `library-first-layer` pandas-pyarrow-layer; `default-sg` default (RAISE, G2.1); `workstream-schedule` wsb-49f-model-aua-pull-daily |
| 4 of 4 key forms | `legacy-served` platinum/firm/header_metrics.json (live) and the on-list specimen; `legacy-root-code` code/gold/* (live; OUT-OF-PATTERN, canonical `{source}/{scope}/code/gold/*`); `code-tier` and `entity-partition` (specimens) |
| the discriminating pair | `advi/49financial/platinum/firm/fee_efficiency.json` is ON the list and CONFORMANT; `advi/49financial/platinum/firm/top_holdings.json` has the same shape, is OFF the list, and is OUT-OF-PATTERN with canonical `.../top-holdings.json` |
| 0 overlap with the sample | none of the 43 is among the discriminating sample names (checker: 84 distinct names over 85 (type, name) entries; `opalinvest-portal` appears under two types). The 3 cases that are sample names are the allowed OVERLAP names. |

## Criteria

Each was run once as the order names it, and again inside a determinism loop.

| id | verdict line (rc 0) |
|---|---|
| G1-AC1 | `WORKED-CASES: 43  MALFORMED: 0` / `VERDICT: PASS-WELL-FORMED` |
| G1-AC2 | `GRADED TYPES ...: 25  COVERED: 25  MISSING: []` / `VERDICT: PASS-ALL-25-TYPES` |
| G1-AC3 | `MISSING: []` / `VERDICT: PASS-ALL-3-VERDICTS` |
| G1-AC4 | `RESIDUE CLASSES 5  MISSING: []` / `VERDICT: PASS-ALL-5-RESIDUE` |
| G1-AC5 | `NON-SPECIMEN CASES: 39  NOT IN LIVE_NAMES: 0 []  SPECIMENS: 4` / `VERDICT: PASS-ALL-LIVE` |
| G1-AC6 | `DISCRIMINATING SAMPLE: 84  WORKED CASES IN IT: 0 []` / `VERDICT: PASS-DISJOINT` |
| G1-AC7 | `V1.3 KEY FORMS 4  MISSING: []` / `VERDICT: PASS-ALL-4-FORMS` |
| G1-AC8 | `LEGACY-ROOT-CODE CASES: 1  NOT OUT-OF-PATTERN WITH A /code/ CANONICAL: 0` / `VERDICT: PASS-RULED-VERDICT` |
| G1-AC9 | `PORTAL VINTAGE: e85f6eb84f3a...  PATHS: 39  DENOMINATOR: 39` / `VERDICT: PASS-LISTED` |
| G1-AC10 | `LIST ENTRIES: 39  ON-LIST CASES: 1 (CONFORMANT and listed: 1)  OFF-LIST CASES: 1 (OUT-OF-PATTERN and unlisted: 1)` / `VERDICT: PASS-DISCRIMINATES` |
| G1-AC11 | `CITES THE FILE: True  LIST ENTRIES REPEATED IN THE RULE: 1 of 39` / `VERDICT: PASS-CITES-NO-COPY` |
| G1-J1 | RECORDED, no verdict; `3.0.0_SA_CVO` grades it at L9 |

## Controls

- **Mutant.** In a scratch copy of the inputs under `.scratch/mut1`, with no committed file touched, the list entry
  for `firm/fee_efficiency.json` was dropped (39 -> 38 entries). G1-AC10 then printed `ON-LIST CASES: 1 (CONFORMANT
  and listed: 0)` / `VERDICT: FAIL-NO-DISCRIMINATION`. On the same tree G1-AC9 still printed `PASS-LISTED` (38 = 38).
  With the list restored in the same tree, G1-AC10 printed `PASS-DISCRIMINATES`. So the list's membership is what
  moves the pair.
- **Determinism.** All 11 checks ran twice on the same bytes: `cmp` found the two outputs identical, 22 lines, with
  11 of 11 PASS verdict lines.

## How the list was measured

- The census the order names, `git grep -n platinum e85f6eb84f -- src`, prints 122 lines. Only 7 of the 39 templates
  have a request line in them.
- The widened census reads:
  - `git grep -n -i platinum`: 401 lines across 33 files;
  - the route census (`api/general/mdpf|PLATINUM_BASE|platinum-summary|/api/scoped/*/platinum`): 47 lines;
  - a request-builder census: 30 lines.
- Every distinct platinum path string in those lines was traced to a request site or to one of the 8 exclusions. The
  exclusions include the 15 ADVI twin leaves: every ADVI_REPOINT row is `held` or `structural`, so `adviRead` never
  builds a twin URL. See row `LGIC_NAMING-W1-S1`.

## Rows filed

All four are `OBSERVATION`, hazard `INERT`, disposition `UNDER_INVESTIGATION`.

| row | what |
|---|---|
| `LGIC_NAMING-W1-S1` | the named portal census prints only 7 of the 39 request sites |
| `LGIC_NAMING-W1-S2` | the registry seed has no platform-subsystem row, so V1 is an interim table and 14 tokens RAISE |
| `LGIC_NAMING-W1-S3` | some canonical forms need a slot the name does not carry, so they print `{system}`, `{source}`, `{scope}` or `{cadence}` |
| `LGIC_NAMING-W1-S4` | AWS-fixed names in graded types (1 default SG, 9 IAM policies, 4 log groups) RAISE; an AWS-managed policy without the prefix cannot be seen |

## What this does not claim

- **The routers were not read.** The router source (shared-advisor-router, public-data-router) is not in the portal;
  the request-to-key mappings are the portal's own comments.
- **One Lambda route is not on the list.** The key behind the relationship `platinum-summary` route is not named in
  the portal, so it is excluded.
- **V1 is not the registry.** It is an interim table read from SEED and CENSUS; its split into products and feeds is
  this worker's reading.
- **The rule has not been exercised by anyone who did not write it.** That is LN-h-1 and LN-h-2, and the judgment is
  G1-J1's, at L9.
- **`NAMING_SCHEMA.json` was not edited.** Each schema gap is a row.
