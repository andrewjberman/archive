# TO-EN-o-35-r7 -- owner confirmation, round 7 -- RESULT

`0.9.0_WK_LGIC_ENFORCE~1`, worktree `wk-lgic-enforce-7-1b`, base `50e217ba84` (round-7 L6 issuance
this slot's fixed-input pin references, `R7_BASE.json base_commit 2c3d7b0cb2`).

## What this is

Round 6 resolved 41 `owner_claim` rows and every one reads `inferred`, because LEG B of each row's
`owner_basis` inherits its system from a SIBLING resource's own IAM role -- and that sibling's own
claim is itself `inferred`. A sibling's reading is not a confirmation; it is the same reading one
resource over.

This cell adds a FOURTH leg per row (LEG D), reached OUTSIDE that inheritance chain: a registered
project (`org/projects/<CODE>.json`) or a `DIRECTIVES.yaml` member row that CLAIMS the resource
directly -- names it as its own deliverable, work item, TO history or change log -- rather than
merely sharing a system tag with it.

## Method

1. Read all 41 rows of `PLACEHOLDER_CAMPAIGN_R6.json.resolved` whole, including every `owner_basis`
   string (`.scratch/r6_owner_basis.txt`, not committed -- working notes only).
2. Grouped the 41 by the project/directive TOKEN already visible in LEG B/LEG C of each row's
   `owner_basis` (e.g. `ADVI_INFSHIP`, `ADVI_INFETL`, `ADVI_INFINGE`, `ADVI_ORIAPI`, `ADVI_BDAPIMIG`,
   `ETFS_SETUP`, `POSN_ASTTAX`) or noted NONE where the citation was only a generic Terraform-root /
   shared-IAM-role sentence (`inf-exporter`, `inf-client-detail`, `inf-portal-advisor-publisher`,
   `etf-positioning-producer`, `wsb-49f-model-aua-daily`, `wsd-49f-partner-held-etf-daily`).
3. For every token, checked `ls org/projects/` for a matching `<CODE>.json` and confirmed its
   `project_code` field matches the token verbatim -- a REGISTERED project, not an inferred label.
   7 tokens confirmed this way: ADVI_INFSHIP, ADVI_INFETL, ADVI_INFINGE, ADVI_ORIAPI, ADVI_BDAPIMIG,
   ETFS_SETUP, POSN_ASTTAX (POSN_ASTTAX corroborated a second way -- it is also a `DIRECTIVES.yaml`
   D4 member, `org/missions/DIRECTIVES.yaml:84`).
4. For the 6 with NO token in `owner_basis`, ran `comp-find` over `org/projects` (464 files scanned)
   for each bare resource name (`inf-exporter`, `inf-client-detail`, `inf-portal-advisor-publisher`,
   `etf-positioning-producer`, `wsb-49f-model-aua-daily`, `wsd-49f-partner-held-etf-daily`) to look for
   a genuine claim outside the inheritance chain:
   - `inf-exporter` -> `org/projects/ADVI_INFLEC.json:61`, pod W2 "Compute provisioning (gold runner
     EC2 + Lambda shells + inf-exporter EC2 with OTP relay)" -- the project's OWN deliverable list.
   - `inf-client-detail` -> `org/projects/ADVI_INFFIN.json:15`, changelog entry naming
     "inf-client-detail Lambda ... W2.3 STUB", W2.3 matching the TF section header
     `infra/aws/terraform/inf-pipeline/iam.tf:334`.
   - `inf-portal-advisor-publisher` -> `org/projects/ADVI_INFETL.json:5`, open backlog item "(c) full
     implementation of inf-portal-publisher and inf-portal-advisor-publisher Lambdas".
   - `etf-positioning-producer` -> `org/projects/ETFS_POSITIONING.json:63-64`, TO-D4c history:
     "etf-positioning-producer-daily cron(0 13) ENABLED". ETFS_POSITIONING is also a D4 member,
     `org/missions/DIRECTIVES.yaml:84`.
   - `wsb-49f-model-aua-daily` / `wsd-49f-partner-held-etf-daily` -> ZERO hits in `org/projects`
     (comp-find, denominator 464 files scanned). Checked the source directly:
     `infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:1-25`'s own file header names only
     "Andrew P0 2026-07-16" and CTO gate timestamps 051145Z/052551Z -- no project/directive token.
     `infra/logic/registry/resources.json` carries a `system` field only, no owning-project field on
     any of its 91 rows (checked against `inf-gold-layer-lambda-role`'s own entry as a second
     instrument). These two resources (6 of the 41's rows, both planes x IAM_POLICY/LAMBDA) stay
     CARDED.
5. Wrote `OWNER_CONFIRMATION_R7.json`: 35 CONFIRMED (LEG D added, `owner_claim: confirmed`,
   `owning_directive`, `directive_citation`, `owner_basis_round_6` preserved verbatim beside a NEW
   `owner_basis`), 6 CARDED (`owner_claim` stays `inferred`, `reason` names what was searched and not
   found). `current` field disambiguated to `"<name> [<type>/<plane>]"` because R6's bare resource
   names repeat across distinct (type, plane) rows (`inf-bronze-runner` x2, `inf-accounts-v2-daily`
   x3, etc. -- (current, type, plane) is unique across all 41, bare `current` is not) and the
   checker's dedup test in `core_o35_population` keys on bare `current`.

## Arm results (post-commit, on `OWNER_CONFIRMATION_R7.json` at `b8b1fddf0f`)

```
=== o35-population ===
population pinned at 41 ; confirmed 35 + carded 6 = 41
a row in BOTH lists (must be empty): []
VERDICT: PASS-O35-EVERY-ROW-ADDRESSED
=== o35-directive ===
confirmed rows: 35
without an owning_directive (must be 0): 0 []
without a directive_citation (must be 0): 0 []
VERDICT: PASS-O35-CONFIRMED-CITES-A-DIRECTIVE
=== o35-claim-moves ===
confirmed still reading `inferred` (must be 0): 0 []
carded NO LONGER reading `inferred` (must be 0): 0 []
carded with no reason (must be 0): 0 []
VERDICT: PASS-O35-CLAIM-MATCHES-ITS-LIST
=== o35-no-silent-upgrade ===
confirmed rows: 35
whose basis is BYTE-IDENTICAL to round 6's (must be 0): 0 []
not carrying round 6's basis for comparison (must be 0): 0 []
VERDICT: PASS-O35-NO-SILENT-UPGRADE
```

## Controls

`selftest-arms` run FIRST, before any write: 21 arms, 8 positive-satisfiability, `VERDICT:
PASS-ARMS-DISCRIMINATE` -- no arm was unsatisfiable and no BLOCKING row was owed.

Four live mutants driven through the REAL reader on the COMMITTED record, each alone, each restored
byte-identical (`hashlib.sha256`, worktree bytes, not `git hash-object`) and verified clean by
`git status --porcelain` afterward:

| mutation | arm | expected | observed |
|---|---|---|---|
| drop the last carded row | o35-population | FAIL-O35-EVERY-ROW-ADDRESSED | FAIL-O35-EVERY-ROW-ADDRESSED |
| strip `owning_directive` from confirmed[0] | o35-directive | FAIL-O35-CONFIRMED-CITES-A-DIRECTIVE | FAIL-O35-CONFIRMED-CITES-A-DIRECTIVE |
| set confirmed[0].owner_basis = its own round-6 basis | o35-no-silent-upgrade | FAIL-O35-NO-SILENT-UPGRADE | FAIL-O35-NO-SILENT-UPGRADE |
| set confirmed[0].owner_claim back to `inferred` | o35-claim-moves | FAIL-O35-CLAIM-MATCHES-ITS-LIST | FAIL-O35-CLAIM-MATCHES-ITS-LIST |

4 of 4 fired as expected. Restore proven by byte-equality AND sha256 match after each of the four
mutations (`RESTORE after M<n>: bytes equal: True`), and a final full re-run of all four arms on the
restored bytes PASSED all four again. `git status --porcelain` on the record was empty after the
whole cycle.

## What was NOT done

- No grade moved. Round 6's 41 resolutions are byte-untouched (`PLACEHOLDER_CAMPAIGN_R6.json` was
  read-only throughout; not staged, not in the commit).
- `DIRECTIVES.yaml`, every `project.json` and `infra/logic/registry/` were READ, never edited (the
  order's bound); no diff exists on any of them.
- Nothing live moved. Every read was a repo file read; no AWS call was made this cell (the two
  earlier `EC2_INSTANCE` rows' `plane` field -- `live` vs `repo` -- came from round 6's own record,
  not from a fresh AWS read here).
- The 6 CARDED rows are a real finding, not a shortfall: no registered directive claims either mdpf
  49F feeder resource; Andrew's own P0 word authorized their build directly, which is real
  authorization but not a registered OWNING DIRECTIVE in the sense this cell tests.
