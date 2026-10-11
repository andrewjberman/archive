# ADVI_FIRMBKTS -- round 3 L5 fact sheet (2.0.0_SA_COO~B1, dell1, 2026-10-11 ~05:2xZ-06:0xZ)

Read-only measurement at the cut, as `arn:aws:iam::313476888478:user/cloudops-dell1-agent-user` unless a row says
otherwise. Inputs: `ledger/ROUND_ANALYSIS.round2.md` @ba27c8c055, `surprise-channel/remediations/REMEDIATION_v3.md`,
`deliverables/2.0.0_SA_COO~B1/round2/R2_CLOSE.md`, PRD v1.3. Each figure names its instrument.

## 1. The compare instrument (D1-C-S7, item 2)

- `r2_f7.py compare` decides equality, where ETag forms differ (the multipart key), by hashing the CURRENT source
  object (`_sha(s3, SRC_BUCKET, src)`), so source drift reads as a wrong destination.
- `opal-data-bd` is versioned. The one multipart key in the manifest, `gold/views/client_tax_liability.parquet`
  (manifest ETag `8edee8b4...-2`, 11,392,210 bytes), has 37 versions; two carry the manifest's ETag (2026-10-10 05:12:31Z
  and 2026-10-11 00:10:57Z); the current version (05:10:08Z) does not. `list_object_versions` and `GetObjectVersion`
  are allowed to this identity.
- Reference build (scratchpad `r3_f7_reference.py`, not committed): `compare` live reads DEST present 52,910 missing 0
  mismatch 0 extras 0 and SOURCE changed-since-manifest 36,742 at 05:5xZ, and 40,948 on the next run a few minutes later
  (the producers' window was still open). The round-2 reading of "changed 1" at 05:07Z preceded the window.

## 2. The table repair (item 3)

- `mapping_v2.json`: 498 rows, 89 FAULT (owner `1.0.0_SA_CTO~DELL1` on all 89), 24 re-grids, 28 collision rulings.
- FAULT reason groups: 12 market-price silver (vendor not derivable); 8 + 3 + 2 + 2 + 2 + 2 + 2 + 1 + 1 destination-key
  overlap rows; 7 "no repair rule places it"; 6 zero-byte marker at the class prefix (live HEAD of `gold/cohorts/`,
  `gold/clients/`, `gold/nna/` in `opal-data-bd`: size 0); 5 interleaved completion markers and data (inf
  `bronze/eclipse/`, `bronze/eclipse_qa/`, `bronze/orion-api/`, `gold/eclipse/`, `silver/eclipse/`: 1,798, 871, 17,170, 529,
  660 objects); 5 "overlap 0 of N keys with the group"; 4 silver/bronze root files; 3 Lambda artifacts (R16); 3
  leading-slash keys; 2 runtime telemetry.
- Rules (a)-(e) are the CTO's, `ROUND_ANALYSIS.round2.md` section 2 item 3. Instrument `checks/r3_mapping.py`.

## 3. F4 own-firm admit (item 5)

- 9 `*-cot-*` roles. Five carry an inline policy that names `opal-data-cottonwood`. The one the runner can assume is
  `irpt-cot-ycharts-research-role` (trust: `role/irpt-ycharts-runner-role`, the instance profile of
  `i-0167fd745ad906a66`): `s3:GetObject`/`PutObject` on `irpt/cottonwood/state/ycharts_responses/*` and
  `.../ycharts_runs/*`, no `ListBucket` (which is why round 2's `ListObjectsV2` was an identity-side implicit deny).
- Issuer's dry run (the cell's own act, SSM command `0e7afa57-7961-4575-b7cd-becebda020da`, Success): CALLER the research
  role; OWN `GetObject` of `.../ycharts_runs/index=latest/latest_by_portfolio.json` returned 431 bytes; OUT `GetObject`
  of `irpt/cottonwood/code/gold/investor-reporting-holdings.tar.gz` refused "no identity-based policy allows"; INF
  `ListObjectsV2` on `opal-data-inflection` refused "explicit deny in a resource-based policy". `r3_f4.py` 4 of 4. The
  cell re-runs this under its own order so the evidence belongs to the order.

## 4. The producers (cutover step 2)

- The 11 served classes of the round-1 table (`mapping.json`, bd MOVE, platinum tier) hold 52,910 objects at the manifest:
  `gold/entities/{accounts,advisors,clients}/` 27,530, `platinum/clients/` 16,766, `platinum/accounts/` 7,562,
  `platinum/advisors/` 980, `gold/artifacts/` 43, `platinum/firm/` 15, `gold/views/` 10, `gold/platinum/firm/` 2,
  `platinum/49financial/` 1.
- `comp-pipescript io D_04 --pipeline bd-gold`: D_04 alone writes 22 keys/key-families across `platinum/{accounts,
  advisors,clients,firm}/` ([HARDCODED] literals) and reads 29. The gold scripts take the bucket from
  `data/black_diamond/scripts/gold/lib/config.py:14`, `S3_BUCKET = os.environ.get('BD_S3_BUCKET', 'opal-data-bd')`, ONE
  value for every read and every write (D_04 imports it as `BUCKET`). 42 scripts under the two gold script directories
  import it (fixture count, `r3_census.py` re-counts it). A repoint is therefore not a constant edit: the same value
  moves every read.
- Producer census, writer by writer, is the cell `FB-f-6`; the repoint (`FB-f-9`) is cut staged and amended from it.

## 5. The advTenant remedy (cutover step 1)

- `_shared/firm-config.mjs` header: "DO NOT ADD OR EDIT AN ENTRY THAT MAKES TWO firmIds SHARE A `bucket` VALUE ... the
  remedy lands FIRST." The remedy is not in the code at HEAD (`grep advTenant` hits comments only). The Rule-24 record
  it cites, `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ADVI_P4R3_ADVTENANT_RULE24_RECORD_20260821.md`, does not
  exist at HEAD (a `comp-find` of the name returns the config header and one unrelated record).
- The router asserts the tenant by comparing buckets (`index.mjs:410-436`, `FIRM_BUCKET_MAP[platinumAdviFirm]` against
  the caller's resolved `bucket`); the response guard re-derives it (`shared-advisor-router-response/index.mjs:89-122`).
  At the cutover `49financial` resolves to `opal-data-49financial` while `mockadv` stays on `opal-data-bd`: the buckets
  differ, so the alias that works today by sharing a bucket would be refused by both layers.
- The response guard's suite needs `bun install --frozen-lockfile` before `bun test` (35 pass at base in a scratch copy;
  `@aws-sdk/client-sns` is absent otherwise).
- The registry already generates the served-tenant set (`lib/opal_naming.py _tenants()`, line 972 comment); the field
  the router needs is an emission of data the registry holds, not a new fact.
- The last AE deploy of this function (2026-08-21, P4R-3, `logs/2026-08-21/session_1531-1712Z_p4r3_route_act.md`)
  took a deploy ledger, `safe-apply` through `infra/aws/terraform/portal-auth/`, a lifecycle pin defect (`ignore_changes =
  [qualified_arn]`) and an exercised authenticated fetch that found a 502 from the guard. That log is the checklist the
  deploy cells carry. The same log records an open sovereign call: whether to build the remedy at all (mockadv has zero
  users, measured then); the CTO's round-2 analysis orders it built.

## 6. Instruments proved before the cut

| check | base | reference or control |
|---|---|---|
| `r3_f7_ctl.py --arms live` | 0 of 3 (instrument absent) | 3 of 3 on a reference build, live |
| `r3_f7_ctl.py --arms mutant` | 0 of 2 | 2 of 2 on the reference (one altered ETag reads COPY-NOT-COMPLETE) |
| `r3_mapping.py --arms structure` / `repair` | 0 of 5 / 0 of 5 (v3 absent) | 5 of 5 / 5 of 5 on a fixture derived from v2; mutants: dropped collision entry 4 of 5, a rule-(a) row left FAULT 3 of 5, a disturbed round-2 address 3 of 5 |
| `r3_reader.py --reader A` | 0 of 3 | 3 of 3 on a fixture answers file; an extra file in the directory 2 of 3 |
| `r3_agree.py` | not graded | fixture: canonical both-right 209 of 209, legacy 0 of 209 (all unknown) |
| `r3_f4.py --arms ownfirm` | 0 of 4 (evidence absent) | 4 of 4 on the issuer's dry-run record |
| `r3_census.py` | 0 of 3 (census absent) | 3 of 3 on a fixture; a census with one object count off by one 2 of 3 |
| `r3_advt_record.py` | 0 of 3 (record absent) | 3 of 3 on a fixture |
| router `run-gate.sh` | 39 pass (the new arms expect 42 or more) | -- |
| guard `bun test` | 35 pass (the new arms expect 36 or more) | -- |
| `r2_f6.mjs diff` | 193 of 193 identical (control: PASS at base by construction) | -- |

## 7. Rulings by the issuer inside this decomposition

1. **The window's four acts are cut STAGED, not omitted.** Each carries its un-park condition; a cell whose face
   needs a measurement this round makes is amended by the issuer, in the amendment commit, before its GO (rule 27).
2. **Readers are not committers.** The readers' directories are outside any checkout, hold only `LOCATIONS.json`, and
   the issuer ingests each `ANSWERS_<X>.json` and writes the order's proof instance from the grader's output. The
   worker's standing tree-presence test is waived by the order for these two cells.
3. **Every invocation names its worktree by absolute path** (rows `D1-W9-S2`, `D1-W9-S5`, `D1-W4-S7`).
4. **Every worker order names the instance as the order stem** (analysis section 2 item 5).
