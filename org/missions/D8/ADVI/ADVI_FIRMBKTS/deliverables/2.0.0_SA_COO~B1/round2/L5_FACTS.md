# ADVI_FIRMBKTS -- round 2 L5 fact sheet (2.0.0_SA_COO~B1, dell1, 2026-10-11 ~02:3xZ-03:2xZ)

Read-only measurement at the cut, as `arn:aws:iam::313476888478:user/cloudops-dell1-agent-user`. Inputs: `ledger/ROUND_ANALYSIS.round1.md`
@4c9229fee2, its addenda 1-2 @a7ef4d08ab, `deliverables/2.0.0_SA_COO~F1/round2/L5_FACTS_PRE.md` @24011d42a4, PRD v1.3.
Every figure below names its instrument. A figure marked INFERRED was not measured.

## 1. The table's repair list (enrichment item 2)

Instrument: `deliverables/mapping.json` (444 rows) over `deliverables/census.json` (listed 2026-10-09T20:19Z).
- 226 FAULT rows in 32 reason groups: 41 classes (16,457 objects) "gold root file or directory no 1b row names"; 35 (12,606)
  logs and scratch; 19 (17,235) backup and rollback copies; 17 orion state files; 13 (4,457) rebuild, quarantine and
  reconciliation copies under inf `platinum/`; 12 (1,966) forwardfill dated files beside `_complete/` markers; the rest in
  groups of 9 and fewer (market-price silver, raw vendor downloads, lambda artifacts, smartx raw dumps, leading-slash
  keys, 14 MIXED classes that need a finer grain).
- 13 destination-table groups where two or more classes of ONE bucket share (source, scope, tier, table), over the 209
  placed rows (class counts in brackets): bd `gold/account_gains` [2], `platinum/entities` [3], `platinum/firm` [2],
  `state/parity` [7], `state/watermarks` [4]; inf `platinum/firm` [34 single-file classes], `state/manifests` [2],
  `orion silver/api_dims` [12], `orion silver/orion-rest` [2]; cot `gold/positions_cube` [2], `platinum/entities` [3],
  `platinum/firm` [2], `state/watermarks` [2]. Whether two classes of a group write the SAME destination key is
  unmeasured: it needs both listings, and the cell measures it.

## 2. F4 -- whom the fence admits and refuses (item 3)

- `get-bucket-policy` is readable on `opal-data-inflection` and `opal-data-cottonwood`: statement
  `DenyForeignFirmPrincipals`, 7 admitted patterns each (firm glob plus six named users and roles, both CloudOps users
  among them). The positive arm is reachable and passes today (`r2_f4.py --arms positive`, 3 of 3, live).
- The negative arm cannot be run from this identity directly. Measured: (a) 0 of 9 `*-cot-*` roles are assumable by the
  dell1 user (trust principals are services, other roles and the two Andrew users; the dell agents' group policies carry
  no `sts:AssumeRole`); (b) `iam:SimulatePrincipalPolicy` on a role and `iam:SimulateCustomPolicy` are both refused to
  this user, so the engine cannot be asked either.
- One route exists with no new IAM object: `irpt-cot-ycharts-research-role` (matches `*-cot-*`) trusts
  `role/irpt-ycharts-runner-role`, which is the instance profile of `i-0167fd745ad906a66` (`irpt-ycharts-runner`,
  running, SSM `Online` at the cut; 4 SSM-managed instances in all). One `AWS-RunShellScript` command from the dell1 user
  would assume the role and make one read-only list of each bucket. INFERRED, not tried: that the dell1 user holds
  `ssm:SendCommand` on that instance, and that the runner has an AWS CLI or boto3. An S3 AccessDenied message names the
  deciding statement kind ("explicit deny in a resource-based policy"), which is what separates the fence's refusal from
  an identity-policy gap. The cell is cut on that route; if the send is refused it is a BLOCKING row, not a recut.

## 3. F7 -- 49 Financial's served keys (item 4)

- Instrument: `checks/r2_f7.py manifest` against `opal-data-bd` at 2026-10-11T02:5xZ: **52,910 objects in the 11 served
  platinum classes** (census at 2026-10-09: 52,851; the daily producers added 59). **52,910 of 52,910 placed by
  `address()`, 0 refused, 0 destination collisions.** Destination `opal-data-49financial` `advi/49financial/platinum/`:
  0 objects (compare: present 0, missing 52,910). Default encryption AES256 on both sides, so ETag equality is content
  equality for single-part objects.
- THE SOURCE MOVES. `head-object` on `platinum/firm/advisor_nna_canonical.json` reads LastModified 2026-10-11T01:11:26Z;
  every census class's `last_modified_max` is 2026-10-09 05:27Z-06:15Z. The producers rewrite these keys daily, in a window
  that closes about 06:15Z. A copy is therefore a SNAPSHOT: `compare` reports source-changed-since-manifest as its own
  count, and a router flip served from a stale copy would show users yesterday's numbers (FWD-4 fails the morning after).
- `gold/platinum/firm/` (2 objects) and `platinum/firm/` (15) share a destination table and are disjoint by key in the
  manifest (0 collisions). `gold/platinum/firm/` is reachable by no router route (see section 4).
- Identity: `iam:SimulatePrincipalPolicy` on the caller's own ARN reads `allowed` for `s3:PutObject`, `GetObject` and
  `ListBucket`; the 49financial policy's three other statements concern the performance adapter only.
- Residue (row D1-S2's bound): `opal-data-49financial` holds at least 1,000 keys outside `advi/49financial/platinum/`
  (tier-first `gold/advi/**`, `_campaign/`). The cell records their counts before and after the copy.

## 4. F6 -- the router (item 5)

- Instrument: `infra/aws/lambda-edge/shared-advisor-router/index.mjs` (435 lines) at fda1c4f0cc; its own gate reads
  **31 pass / 0 fail across 2 files** (`bun test test/`).
- The router resolves the bucket from `FIRM_BUCKET_MAP` (generated from the registry: `49financial` and `mockadv` ->
  `opal-data-bd`, `inflection` -> `opal-data-inf`, `cottonwood` -> `opal-data-cot`) and rewrites the advisor-intelligence
  suffix to a LEGACY key (`/platinum/**`, `/gold/entities/**`, `/gold/views/**`, `/gold/artifacts/**`, ...). One router is
  the `origin-request` function on FIVE CloudFront behaviors; a deploy moves all five, for every partner firm.
- A second, independent path class already exists: `platinum/advi/{firm}/` resolves to `opal-data-portal-v2` under the
  P4R-3 tenant assertion. The twins are not 49 Financial's served platinum and are left exactly as they are.
- `firm-config.mjs` carries a standing warning: editing a `bucket` value that makes two firmIds share a bucket needs the
  `advTenant` remedy FIRST (mockadv and 49financial share `opal-data-bd` today). The cutover edit is therefore NOT this
  round's: this round builds the canonical key path DORMANT, keyed to the registry's own map, and edits no map value.
- 10 of the 11 served classes are reachable by a router route; `gold/platinum/firm/` is not (the router's
  `platinum/...` suffix passes through to `/platinum/firm/...`, never `/gold/platinum/firm/...`).
- The staff proxy (`opal-capital`, `?firm=49financial`) already resolves to bucket `opal-data-49financial` today and
  would receive canonical keys under an ungated build; the dormant design gates the canonical path on the registry's
  map naming that bucket for the firm, so every request resolves exactly as it does now (the difference arm proves it).

## 5. Item 6 -- the tolerant load (S11)

- `build_canonical_prices_v2.py` NO LONGER carries the literal the naming gate refused (row MDPF_DEMQUE-D1-W7-S2): the
  ADVI_COTBKF writers (CB-ap-1, CB-at-1, CB-ax-1 @19b3550e8a) moved every input key onto `legacy_addresses.json` rows read
  beside the writer. The "literal rename" half of item 6 is already done by another project; no cell renames anything.
- The patch `...2.0.0_SA_COO~Q1/ADVI_FIRMBKTS_INPUT_S00_TOLERANT_LOAD.patch` @091ccbafa2 applies cleanly to the builder
  at HEAD (`git apply --check` rc 0). Its TEST file is what the gate still refuses (NAMING REFUSE on the `silver/...`
  literal at :46); reproduced today with `naming-gate.py --diff <patch> --enforce`.
- Reference run by the issuer in a scratch tree: builder hunks applied + a test reading every key from the module's own
  `INPUT_ADDRESSES`: 3 passed; the two existing price tests 12 passed; the naming gate on that diff `PASS`.
- The optional S_00 SSM step is DROPPED, with its reason (section 7).

## 6. Instruments proved before the cut (feed the checker)

| check | base | reference or control |
|---|---|---|
| `r2_mapping.py --arms structure` / `repair` | 0 of 5 / 0 of 4 (mapping_v2.json absent) | 5 of 5 / 4 of 4 on a reference table; one mutant each: no owner 4 of 5, typed address 3 of 5, disturbed round-1 row 3 of 5, unruled collision 3 of 4 |
| `r2_reader.py --reader A` | 0 of 2 | 2 of 2 on a full answer set; 1 of 2 with one id missing |
| `r2_f4.py --arms positive` | 3 of 3 (a live control, PASS at base by construction) | -- |
| `r2_f4.py --arms negative` | 0 of 4 (evidence absent) | 4 of 4 on a reference record; three mutants 3 of 4 each |
| `r2_f7.py manifest --verify` / `compare` | evidence absent -> rc 1 | verify: 52,910 placed, 0 refused, 0 collisions; compare: missing 52,910 (nothing copied yet) |
| `r2_f6.mjs diff` / `seam` | NOT RUN (handleWithMap absent) | reference router: 193 of 193 identical; 20 of 20 + 9 of 9 controls; mutants: no registry gate 183 of 193, views class mis-pointed 18 of 20 |
| `r2_s11.py` | NOT RUN (empty diff) | gate PASS on the reference diff |

The first `r2_f6.mjs diff` compared two THROWs (a corpus of descriptors passed where events belong) and read 193 of 193;
a mutant with no registry gate also read 193 of 193. Caught by feeding it a mutant before trusting it, fixed, re-run.

## 7. Rulings by the issuer inside this decomposition

1. **F6's DEPLOY is not a round-2 cell.** Section 3's measurement: the producers keep writing `opal-data-bd`, so a router
   flip before the producers write `opal-data-49financial` serves a day-old copy; dual write is DEC-17's NEVER. The
   deploy waits for F10's platinum-producer repoint (or its own resync inside the flip window with producers redirected),
   and for the `advTenant` remedy if a map value changes. The round BUILDS the dormant path and proves it against the table
   and the copy; its deploy is a no-behavior-change release that the next round may take first. Row D1-S4.
2. **S_00 is dropped.** MDPF_DEMQUE closed its own S_00 SUPERSEDED (ruling msg 1368: its store is the queue's own price
   store, not `canonical_prices.parquet`), so the step would add a production step to the cot daily chain that nothing
   consumes. The rename and the tolerant load do not split and are kept.
3. **F4's negative arm runs through the one existing principal route** (section 2), under a bound the face carries.
4. **Readers.** Answers are graded on `system`, `firm`, `tier` and the `table` slot (the contents clause at the table
   grain); the free-text gloss is recorded for the CVO. The reader's worktree withholds the project folder (sparse).
5. **No worker decides the table.** The repair rules are the issuer's, in the face of FB-e-1: a class they do not place
   stays FAULT with a named owner. A collision whose measured overlap is not 0 makes BOTH classes FAULT, owned by
   `1.0.0_SA_CTO~DELL1`.
