# MDPF_CANON round 7 -- never-widen pair for CN-j-1: the publisher deploy that serves the history leaf (four new read-only keys), and what else the rebuilt package carries

**COO half SIGNED, CTO half OWED.** Drafted by a fork of `2.0.0_SA_COO~D1` on 2026-10-14 ~15:5xZ, against the MERGED cell (trunk `1c8ebf3e5d`), replacing the pre-build
draft `NEVER_WIDEN_PAIR_R7_CN_J_1.md` (21:1xZ 2026-10-13, removed with this commit); read in full by the issuer. A signature is a line in a commit by the signing seat. Nothing here is deployed.

**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on `ADHOC.canon-r7-publisher-deploy` (draft beside this file; WORLD; the publisher package only).
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1`, to be recorded at `ledger/NEVER_WIDEN_R7_J1_PUBLISHER_CTO_HALF.md`; COO half = this lane.
**Rulings this pair carries:** CTO msgs 5086-5088 and the PRD ENDPOINT FWD-9 ("a READ-ONLY served history route over the existing objects ... its own cell under its own never-widen
pair; the grade is read with that route live", PRD lines 229-235); the round-6 analysis section 4. **Cell:** `TO-CN-j-1`, merged `1c8ebf3e5d`, instance VALID, AC1 6/6, AC2 8/8, AC3 6/6 (the
issuer re-ran all three at the merged tree, 2026-10-14 ~15:3xZ); AC4 judgment is the CVO's and waits on this deploy.
**What changed since the pre-build draft, and why the old numbers are void:** the cell is built; the dated gold objects number 95, not 91 (row D1-W23-S2); the package a rebuild produces
carries eight other modules (section 1a: this is the largest correction); a read-back script and a bounded on-demand run (D2) now exist; the PRD's own text names the route.

## 1. Code

- **Pin:** a commit that is an ancestor of origin's `box/dell1` (`git ls-remote`, then `git merge-base --is-ancestor`), carries merge `1c8ebf3e5d`, and is named in the order at GO. The
  order re-runs section 1a at that pin before building; a different pin moves the section 1a table, never the cell.
- **The cell (3 files, 664 lines with its records; the product change is 180 lines in `lambda_function.py`):** `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py`
  gains `load_latest_pointer_doc`, `assemble_history_leaf`, `_content_sha`, `_publish_history_one`, `_client_aum` and a handler hook; `tests/test_history_leaf.py` (new, not shipped);
  `tests/test_completeness.py` (three serve-write filters only).
- **The rule as built (read from the merged code):** for each scope that has dated `category-views` gold (the scope set comes from the gold listing), list `portal/gold/mdpf/<scope>/category-views/`,
  read every dated object, assemble `{schema, leaf, scope, n_dates, dates[], client_supervised[], client_unsupervised[], omitted[]}` (+ `_provenance` at write), and write it to
  `platinum/mdpf/<scope>/category-views-history.json`. A Client node or `aum` that is missing, non-numeric, a bool or non-finite is `null`; a measured `0.0` stays `0.0`. An unparseable object, a
  non-object, or an `as_of` whose first ten characters differ from the key date is left out of every array and named in `omitted`. The leaf's own content sha (canonical JSON, `_provenance`
  excluded) is the D5 key: the previous pointer's `history_rows[<scope>/category-views-history].content_sha256` equal to this run's AND the served key listed means `unchanged`, no write.
  The rows live in `history_rows` of the run manifest and of the pointer, outside `results`, `expected`, `failed` and `all_present`.
- **What it does not change:** the 18 gold-projected leaves' code path (`_publish_one`), the artifact-type axis (the build derives it from the consolidator by AST: the four type names read the same
  at HEAD as in the deployed manifest), the gold tier, the portal, the edge, any IAM statement.

### 1a. What the rebuilt package carries beyond the cell (MEASURED 2026-10-14; this section is new and is why the draft's "the plan moves the code and one environment value" is incomplete)

The function's code is the 2026-10-01 build at `e8994f23af` (`CodeSha256` `pj+Jat96t5dijB+0SQF918S1pi3AZBs1eQNvMXLYEJA=` = hex `a63f896adf7ab797628c1fb449017dd7c4b5a62dc0641b3579036f3172d81090` = the committed
sidecar's `zip_sha256`). The builder reads every member from the pinned commit. Comparing the deployed manifest's per-module sha256 with the blobs at HEAD (`924bae22cc`):

| packaged member | deployed vs HEAD | change since `e8994f23af` |
|---|---|---|
| `lambda_function.py` | DIFFERS | the cell (180 lines) |
| `lib/opal_naming.py` | DIFFERS | 1,042 lines changed, 40 commits |
| `infra/logic/registry/systems.json` | DIFFERS | 215 lines |
| `infra/logic/registry/exemptions.json` | DIFFERS | +146 |
| `infra/logic/registry/reporting_policies.json` | DIFFERS | +76 |
| `org/standards/NAMING_SCHEMA.json` | DIFFERS | 31 lines |
| `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` | DIFFERS | 28 lines |
| `infra/logic/registry/scopes.json` | DIFFERS | 24 lines |
| `infra/logic/registry/resources.json` | DIFFERS | -6 |
| `infra/logic/registry/remediations.json`, `tiers.json` | EQUAL | none |
| `artifact_types.json` (derived at build) | will differ in `derived_from` only | the consolidator's source sha moved; the four type names are the same |
| `partner_roster.json` (build-generated) | not compared | not at HEAD by name |

Eight modules besides the cell move, 1,397 insertions and 171 deletions. The publisher uses the naming library in ONE place (`lambda_function.py:146-159`, the Tax control location). **Measured:** that call,
`address("mdpf", lookup("global")["long"], "state", "taxsma_control", "current.json")`, returns `s3://opal-data-mdpf/mdpf/global/state/taxsma_control/current.json` under BOTH the `e8994f23af` modules
and the HEAD modules, each run from a directory holding only the ten packaged files (so the smaller registry set of the package, not the full tree). **Not measured:** the rest of the new library's
behaviour under the Lambda's python3.11 (the commit gate lints at py39; the local interpreter here is 3.14), and the Tax stamp path end to end. The on-demand run D2 and the readback H8 exist to read it
(the existing 18 leaves, the Tax-stamped ones included, must equal their gold sources apart from `_provenance`). The pair asks the CTO half to ACCEPT this drift knowingly (section 8, item 2).

## 2. Deploy acts (one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | before the build, download the artifact key's CURRENT version bytes and hash them (the rollback copy); `build_package.py --pin <pin>` (publisher package; it refuses a moving ref); upload the zip to the artifact key with metadata `content-sha256` = the zip's sha256 hex; edit the ONE `.tf` value `MDPF_PUBLISHER_COMMIT` (and its comment) to the full SHA the build resolved; commit that file with `safe-commit.sh`; then ONE targeted `safe-apply` on `module.mdpf_publisher` whose plan moves the function's code (`s3_object_version`, `source_code_hash`) and the single environment value and NOTHING else | `s3://opal-313476888478-lambda-artifacts/opal-assets/opal-assets-mdpf-portal-publisher.zip` (current VersionId `Deg26fXt..bp.9N3HB4sZKEu.MYLj4y2`, 555,056 B, `content-sha256` `a63f896a...`); function `opal-assets-mdpf-portal-publisher`; `infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf:163` (prior value `e8994f23af282296037bd28bb539ac55cc9465dd`) | re-upload the saved prior bytes to the key (a new version, metadata `content-sha256` `a63f896a...`), restore the `.tf` value and comment, apply the same target; read back `CodeSha256` = `pj+Jat96t5dijB+0SQF918S1pi3AZBs1eQNvMXLYEJA=`. The previous artifact version `ZLaQC2nGuQ2hP72JpdTA4RWfciYhFoql` (2026-08-29, 53 KB) is NOT a rollback target |
| D2 | **ONE on-demand invoke, event `{}` (the schedule's own input), after D1 and outside the clock window of section 2a. DECISION FOR THE CTO HALF (item 1): REC keep.** It writes the four new keys, overwrites the 18 existing leaves with their own gold bytes (only `_provenance.written_at` differs), writes one new run manifest and overwrites the pointer | the four keys under `platinum/mdpf/<scope>/`; the 18 leaves; `platinum/mdpf/_manifests/<date>/<run-id>.json` (new); `platinum/mdpf/_manifests/latest.json` | the four keys are new (nothing to restore); the 18 leaves are re-copied from the VersionIds recorded in the before print if a data field differs (H8's rule); the manifest is write-once and inert; the pointer is additive (the prior code reads only `rows`, so a rollback does not choke on `history_rows`) |
| D3 | read-only after D2: the edge hop (GET the route for each leaf through the public host), the listing diff, the 18 baselines | -- | none |
| D4 | the first SCHEDULED run (2026-10-15 13:50Z at the earliest) is read by the ISSUER with `r7_history_readback.py read`, never a leg of the order | -- | none: read only |

**Why D2 is asked for (the argument for the CTO half to weigh):** the scheduled run lands at 09:50 ET on a business morning and republishes all 18 live leaves with the rebuilt package, eight drifted
modules included. An afternoon run finds a break with a day of rollback time instead of at client load; it adds no key the scheduled run would not write. Against it: it is an off-schedule run of a
production pipeline (permitted as QA by the workspace rule; never production evidence), and it rewrites the 18 live objects once mid-day (content equal; `_provenance.written_at` moves). If D2 is struck,
the order's leg is struck by amendment and D4 stays the first look.

**2a. Preconditions the order reads first (any false: do nothing, report which):** (a) the issuer's written GO; (b) the pin on origin and carrying `1c8ebf3e5d`, section 1a re-run at the pin and printed;
(c) both halves of this pair SIGNED; (d) the clock: no act within 45 minutes before the 13:30Z gold fire or the 13:50Z publisher run, and none while the gold lambda, the runner dispatch or the publisher
runs (D1 and D2 therefore start after ~14:10Z); (e) the edge read (below); (f) no FIRMBKTS window act in flight and none of the six R2 files touched (`shared-advisor-router`, the guard, the
CloudFront behaviours, `data/mdpf/config/bronze_homes.json`, `firm-config.mjs`, the portal-auth WAF rider); (g) no open deploy sentinel names the publisher function or `platinum/mdpf/` other than
this order's own, and no gold-package deploy for `mdpf-gold-lambda` is mid-act (CN-h-1 and CN-l-1 ride their own order; two acts never share one window).
**The edge read (e), re-measured by this draft 2026-10-14:** CloudFront `EVTSA9VEHNZVH` has ONE wildcard behaviour `/api/general/*` (no per-leaf pattern, no function association; Lambda@Edge
viewer-request, origin-request, origin-response); `public-data-router` rewrites `/api/general/mdpf/` to `/platinum/mdpf/` by prefix only (`index.mjs:51-56`); the bucket policy `AllowCloudFrontOACPublicData`
grants `GetObject` on `platinum/mdpf/*`. The WAF `opal-cloudfront-protection` was read by the cell's worker (its Step 0: no leaf named) and was NOT re-read here.

**Sequencing and attribution.** The publisher run is a different clock from the gold fire, so this change does not wait on the fold or the frontier-count deploy. It does need its own attribution:
the first scheduled run after D1 serves the leaf; the leaf's only inputs are `nodes.Client.children[<two names>].aum` of the dated `category-views` objects. The two gold-package cells (CN-h-1, CN-l-1)
write the time series, `aum-metrics` and account counts; **whether the `category-views` builder reads any of those is NOT verified here**, so H3 (leaf equals the dated nodes to the cent) and H8 (the 18
leaves equal their gold sources) are what separate the causes if both deploys land the same day.

## 3. Writers of the property (N counted at the merged tree)

Property A, the content of `platinum/mdpf/<scope>/category-views-history.json`: **N = 1**. `_publish_history_one`, called only from `lambda_handler`. A native search for `category-views-history` and
`HISTORY_LEAF` over `*.py *.ts *.tsx *.mjs *.js *.tf *.json *.yaml *.yml *.sh` in the workspace returns 7 files: the publisher's `lambda_function.py` (the writer), its two test files, the worker's proof
instance, the issuer's `r7_cn_j_1.py`, `r7_history_readback.py` and `ref/make_reference_publisher_j1.py` (readers and fixtures). `portal/src` names the key in 0 files: no reader exists yet.
Property B, `history_rows` in the run manifest and the pointer: **N = 1** (`lambda_handler`'s two `put_object` calls); the only other writer of an `_manifests/latest.json` in the workspace is
`data/assets/scripts/gold/runners_49f/d_publisher_port.py`, whose `SERVE_ROOT` is `platinum/advi/49financial` (a different pointer).
Property C, the function's `MDPF_PUBLISHER_COMMIT` and code: one writer, the targeted apply of D1 (and its rollback).
Principals holding `PutObject` on `platinum/mdpf/*` were NOT enumerated: the function runs as the egress role `opal-assets-mdpf-egress-publisher-role`, deliberately unfenced, so what bounds the write is the
code, not the policy. The simulator reads `PutObject` ALLOWED on all four leaf keys (2026-10-14).

## 4. Blast radius (what the act may touch)

- **Moves:** FOUR new keys, `platinum/mdpf/{49financial,inflection,cottonwood,global}/category-views-history.json`; `history_rows` in each run manifest and in the pointer; the function's code
  (section 1a: the cell plus eight drifted modules) and `MDPF_PUBLISHER_COMMIT`; under D2 only, the 18 existing leaves rewritten with identical data, a new manifest, a new pointer version.
- **Cannot move:** the data field of any existing leaf, any dated gold object, the gold tier, any firm bucket, any IAM statement, the edge, `layers` (the function's layer is
  `pandas-pyarrow-requests-layer:1` and version 1 is the only version, so Terraform's latest-resolved layer cannot drift the plan; any plan line for `layers` stops the order).
- **Measured now:** dated `category-views` objects 27, 26, 20, 22 = 95 (2026-10-14 ~15:4xZ); the real arm assembles leaves of 988, 931, 916 and 845 bytes (the arm's own size figure; the served document adds `_provenance`,
  est. under 0.5 KB, not measured); the last scheduled run took 5 seconds (13:50:48Z to 13:50:53Z, manifest `20261014T135048Z-2ca57833`, 18 rows, `all_present` true). The cell adds 4 listings, 95 reads
  and 4 writes per run; the function's timeout is 120 s and 256 MB; the added time in the function was NOT measured.
- **Production reality that shapes both branches (measured):** the run manifest says `prior_pointer_note: AccessDenied ... s3:GetObject ... latest.json` and the simulator reads `GetObject` on that key
  `implicitDeny`; so in production every run publishes every leaf and the `unchanged` branch never fires. The pointer exists (version `oWlJmSz46pAngbwHkQH6.oHmnZ50jv6D`, written 2026-10-14 13:50:54Z; previous
  `oK.mQCOOlBV8hVGN91S39Xv2kYl9tZtO`, 10-13 13:50:54Z): it is overwritten daily and read by no one. Each run therefore adds four leaf versions (the bucket `opal-data-portal-v2` has versioning Enabled).
- **State writes:** a run already writes a manifest and the pointer; they gain a key. The pointer's current shape is `{manifest_key, rows (18), run_id}`; it gains `history_rows`.
- **Exposure:** only the date axis and the two Client aum series per scope; each value is that scope's own Client node, already served for the latest date in `platinum/mdpf/<scope>/category-views.json`.
  No model, firm, account or cross-scope figure. All four leaves have both Client nodes on all 95 dated objects (R2 of the real arm: 190 of 190 cells), so no `null` is expected today.
- **Absent now (measured):** `platinum/mdpf/<scope>/category-views-history*` returns no object under any of the four scopes; the same listings return 4, 4, 5 and 5 keys for the existing leaves (the positive
  control), 18 in all.

## 5. Expected outcome, read from the rules (BOTH branches)

- **Branch 1, the pointer is unreadable (production today):** every run publishes the four leaves (`status published`), `omitted` empty on today's data; `published`, `unchanged`, `missing_pairs`,
  `unexpected_pairs` and `all_present` read as without the cell; the pointer written carries `history_rows` with each leaf's `content_sha256` and `served_sha256`.
- **Branch 2, the pointer is readable (if an IAM grant lands later):** a leaf whose content sha equals the pointer's and whose key is listed reads `unchanged` with no write; any other leaf
  publishes; a scope that failed keeps its prior pointer row so the next run does not rewrite a good leaf. The pair does not depend on which branch holds.
- **A dated object malformed or with an `as_of` differing from its key:** omitted from the arrays and named in `omitted`; the other dates and scopes publish; no zero is written for it.
- **A Client node missing:** the date stays with `null` for that chip; the Trend draws nothing, never `$0`.
- **A scope with no `category-views` gold:** no leaf and no `history_rows` row for it; the existing `missing_pairs` names the pair exactly as today.
- **A failure writing or reading one scope's leaf:** that row is `error` with the message; no other leaf, no gold-projected pair and no `all_present` changes. **Accepted, and stated because it is quiet:**
  a history-leaf failure does not turn `all_present` false or add to the run's failure counts; it is visible only in `history_rows` (H7 reads it; no alarm is built, by the standing moratorium).
- **The new code raises outside the per-scope isolation:** the invoke fails as a whole. The 18 pair leaves are written BEFORE the history hook runs (`lambda_handler` order: pairs, then history rows, then
  the manifest, then the pointer), so they are already rewritten with their gold bytes; the manifest and the pointer, written last, are not written for that run. This is why D2 runs in the afternoon and
  D1's rollback is the saved prior zip.
- **The edge names a leaf allowlist:** precondition (e) stops the order; nothing is applied.
- **The artifact upload carries a wrong `content-sha256`:** the plan shows `source_code_hash` moving to a value that is not the zip's sha256; the order compares them before the apply and stops.

## 6. Client-visible deltas this pair accepts

None on its own: no existing page changes and no reader of the new keys exists. The leaf is invisible until the Trend (CN-i-1, a portal candidate not landed; landing is Andrew's) reads it. The Trend's
Client chips then draw on the leaf's dates. The cent-exact sum for a chip date is read against that date's own dated time-series object, not the newest (row D1-S21).

## 7. Acceptance after the act (the issuer reads; never a leg of the CloudOps order)

`round7/checks/r7_history_readback.py read` (9 arms; H1-H9) on (i) the D2 run if D2 is kept (QA, never production evidence) and (ii) the first SCHEDULED run after D1 (2026-10-15 13:50Z at the earliest), with
denominators printed: the four keys exist; `dates[]` equal the dated gold objects less `omitted` (27, 26, 20, 22 today, +1 per scope per day); each array equals the dated Client node's `aum` to the cent; the
shape is exactly the declared key set; the last date agrees with the served `category-views.json`; the manifest carries `history_rows` x4 with `omitted` empty and the 18 pair rows unchanged in count;
each of the 18 existing leaves equals its gold source apart from `_provenance`; each leaf's `LastModified` is after the deploy ledger's close. Plus: the function's `CodeSha256` is the built zip's and
`MDPF_PUBLISHER_COMMIT` is the pin; the run manifest's `config_hashes.artifact_types.json` differs from earlier runs (its `derived_from` moved with the consolidator; expected, not a delta).

## 8. What the COO half asks the CTO half to read

1. **D2 (section 2):** keep or strike the one on-demand invoke. REC keep, for the reason given.
2. **Section 1a:** the rebuild ships eight drifted modules (1,397 insertions) beside the 180-line cell. Do you accept that knowingly, on the evidence that the one naming call is unchanged and H8 reads the
   18 existing leaves after D2? The alternative is no deploy of this cell until the package is rebuilt for its own reason.
3. **PRD scope row (line 562):** the "what this project touches" table lists `platinum/mdpf/global/` and "platinum's shape" as excluded, untouched. FWD-9's ENDPOINT text (lines 229-235) names this very
   route and its own pair, and round 6's fold already moved served Global objects under FWD-3. Does the ENDPOINT govern, and does the row want an addendum (a ratified-text-half question for the CVO)?
   The CONTRACTS row for the served platinum JSON (line 295) lists four leaves and does not name `category-views` or the history leaf; the publisher's header now carries a paragraph for the one derived leaf.
4. **The failure that does not turn the run red (section 5):** accepted as stated, or a gate wanted?
5. **Precondition (e):** the WAF was read by the worker, not re-read here; the CloudFront and router reads are re-measured above. Whether `/api/general/mdpf/<scope>/category-views-history.json` needs a session
   at the public host is NOT verified; the order's D3 records the status it gets and stops that sub-leg on a 401 or 403 without failing D2.
6. **The upload method:** the repository shows the artifact key, the module's `content-sha256` rule and the precedent order's words "built from the pin, uploaded", not the exact upload command (the module's comment
   names a `build-and-upload.sh` that this package does not have). The order states the required end state and read-backs and leaves the command to CloudOps's logged practice.

## COO half -- SIGNED

`2.0.0_SA_COO~D1`, 2026-10-14 ~16:2xZ, on the bytes above: signed for the blast radius in section 4 (four new read-only keys, one per scope; the 18 existing leaves rewritten with their own gold bytes),
every branch in section 5, and the rollback per key in section 2 (the four leaves are new and inert, a delete of one needs a human's word; the 18 leaves restore from recorded VersionIds; the function
restores from the saved prior zip). THE SECTION 1a DRIFT (the rebuilt package carries eight other modules, 1,397 insertions, beside the 180-line cell) IS NOT ACCEPTED BY THIS HALF ON THE CTO'S BEHALF:
the issuer signs the cell and the act as drafted, and the drift, the PRD scope-row conflict (section 8 item 3), D2 and the unguarded history-leaf failure (item 4) are the CTO half's to rule; the COO
half does not read as authority to proceed until the CTO half answers each by number. On the conditions that the pin is on origin before D1, both halves are signed, the issuer's written GO precedes
D1, and the edge read of precondition (e) reads clean.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
