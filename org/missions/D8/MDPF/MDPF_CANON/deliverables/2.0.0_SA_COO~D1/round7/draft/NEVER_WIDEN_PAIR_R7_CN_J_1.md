# MDPF_CANON round 7 -- never-widen pair for CN-j-1: the history leaf (four new read-only served keys over the dated category-views objects)

**DRAFT -- COO half UNSIGNED.** Written by a fork of `2.0.0_SA_COO~D1` on 2026-10-13 ~21:1xZ for the issuer to read and sign; a signature is a line in a commit by the issuer
and no fork carries it. Nothing here is deployed and the cell is not yet built.

**Deployer:** `0.7.0_AE_CloudOps~DELL1`, on an ADHOC order the issuer cuts after the drain (shape of `ADHOC.canon-r6-fold-deploy`; publisher package only).
**Halves:** CTO half = `1.0.0_SA_CTO~DELL1`, to be recorded at `ledger/NEVER_WIDEN_R7_CN_J_1_CTO_HALF.md`; COO half = this lane.
**Rulings this pair carries:** CTO msgs 5086-5088 (PRD v2.15): "cut a read-only history route over the existing dated objects as its own cell and pair; the chips may ship as-of
first, but the grade waits for the route"; v2.16 (FWD-9). Design: `round7/HISTORY_ROUTE_DESIGN_READ.md` @add7fc4481, option B. Cell: `TO-CN-j-1` (draft beside this file).
**Evidence the issuer holds before signing:** `round7/checks/r7_cn_j_1.py` unit 6/6, seam 8/8, real 6/6 on a scratch reference and 0/6, 3/8, 2/6 at base (controls named); two mutants RED.

## 1. Code

- **Pin:** the cell's drain merge (not yet made). It must be an ancestor of origin's `box/dell1` before the deploy.
- **What changes (all under the cell's grant):** `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` gains `assemble_history_leaf`, `_content_sha`,
  `_publish_history_one`, `load_latest_pointer_doc` and the handler hook; `tests/test_history_leaf.py` (new); `tests/test_completeness.py` (three serve-write filters only).
- **The rule as built:** for each scope that holds `category-views` gold, read its dated objects, write
  `platinum/mdpf/{scope}/category-views-history.json` = `{schema, leaf, scope, n_dates, dates[], client_supervised[], client_unsupervised[], omitted[], _provenance}`. A missing
  Client node is `null`, never `0.0`; a measured `0.0` stays `0.0`; a malformed or `as_of`-mismatched dated object is omitted and named in `omitted`. The leaf is not a gold pair:
  it is outside `results`, `expected`, `failed` and `all_present`; its rows are `history_rows` in the run manifest and the pointer.
- **What it does not change:** the 18 gold-projected leaves (byte-equal apart from the `_provenance.written_at` they already advance), the artifact-type axis,
  `a4_expected`, the gold tier, the consolidator, the portal, the edge, any IAM statement.

## 2. Deploy acts (one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | `build_package.py --pin <pin>` (publisher package only), upload, then ONE targeted `safe-apply` on the publisher function whose plan moves the function's code and the single environment value `MDPF_PUBLISHER_COMMIT` (set to the full SHA of the pin actually built; the D1-S18 class of stamp) and nothing else | the function `opal-assets-mdpf-portal-publisher`; `infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf` | redeploy the prior package and restore the prior `MDPF_PUBLISHER_COMMIT` (value printed before D1) |
| D2 | NO on-demand publisher invoke: an invoke writes real served keys. The first leaves are written by the next scheduled run (`cron(50 13 * * ? *)` UTC) | -- | none owed |
| D3 | after that run: read the four leaves and the manifest (section 7) | -- | none: read only |

**Preconditions (the order reads them first):** (a) the issuer's written GO; (b) the pin on origin; (c) both pair halves signed; (d) no act within 45 minutes before the publisher's
13:50Z run; (e) **the edge read**: no CloudFront behaviour, function association or WAF rule names an individual `platinum/mdpf/*` leaf or limits the path to a fixed leaf list
(the cell's Step 0 reports it; the order repeats it; a finding stops the order -- the leaf would be unreachable and an edge change is R2's); (f) no FIRMBKTS window act in flight
and none of the six R2 files touched.

**Sequencing.** One change per scheduled fire applies to the GOLD fire; this change rides the PUBLISHER run (13:50Z), not the gold lambda, so it need not wait for the fold or the
frontier-count cell's fires. It does wait for the fold's deploy ledger to be CLOSED only if both orders touched one key (they do not: the fold touched the gold lambda and the
`code/` tree, this touches the publisher package). FWD-9's grade waits for this leaf to be served.

## 3. Writers of the property (N = 1, counted from code)

The property: the content of `platinum/mdpf/{scope}/category-views-history.json`.

| # | writer | what it writes |
|---|---|---|
| W1 | `_publish_history_one` (called only from `lambda_handler`) | the leaf, per scope |

No other function in the publisher, the consolidator, the gold lambda, the daily emitter, the runner scripts or the portal names the key (native Grep over `infra/` and `portal/src` for
`category-views-history`: 0 files at the base). Principals holding `PutObject` on `platinum/mdpf/*` were not enumerated (the egress grant's own comment warns that a new
principal with write there would not be blocked); the leaf's content is written by code, not by a principal acting by hand.

## 4. Blast radius (what the act may touch)

- **Moves, from the first scheduled publisher run after D1:** FOUR new keys, `platinum/mdpf/{49financial,inflection,cottonwood,global}/category-views-history.json`;
  `history_rows` is added to each run manifest (`platinum/mdpf/_manifests/<date>/<run-id>.json`) and to the pointer (`platinum/mdpf/_manifests/latest.json`); the function's
  `MDPF_PUBLISHER_COMMIT` value.
- **Cannot move:** any existing served leaf's data (the 18 gold-projected leaves, `json/*`), the gold tier, the A4 frame, any firm bucket, any IAM statement, the edge.
- **Measured size now:** 815 to 958 bytes per leaf at 19 to 26 dated objects; about 40 bytes per date; under 64 KB for decades. Per-run cost: one list and N reads of the dated
  gold objects (91 reads across the four scopes now, +4 per day); the function's timeout is 120 s and 256 MB.
- **State writes:** a scheduled publisher run already writes a manifest and the pointer; they gain a key, no new object. The pointer READ is denied in production today
  (`AccessDenied` on `latest.json`, manifest `20261013T135047Z-4fca44fb`), so every run publishes every leaf, the four new ones included; their content is deterministic and
  differs only in `_provenance.written_at`.
- **Exposure:** only the date axis and the two Client aum series per scope. Each value is that scope's own Client node, already served for the latest date in
  `platinum/mdpf/{scope}/category-views.json`; the leaf adds the time axis. No model, firm, account or cross-scope figure is carried.

## 5. Expected outcome, read from the rules (all branches)

- **Normal day:** the run completes; the four leaves are written with every dated object of the scope; `published`/`unchanged`/`missing_pairs`/`unexpected_pairs`/`all_present` read
  exactly as they would without the cell; `history_rows` shows `published` x4 (production, pointer unreadable) with `omitted` empty.
- **A dated object malformed or with an `as_of` that differs from its key:** that date is omitted from the arrays and named in `history_rows[...].omitted`; the other dates and scopes
  publish; no zero is written for it.
- **A Client node missing in a dated object:** the date is kept with `null` for that chip; the Trend draws nothing, never `$0`.
- **A scope with no `category-views` gold:** no leaf for it; the existing `missing_pairs` names the pair exactly as today.
- **A failure writing one leaf:** that row is `error` with the message; no other leaf, no gold-projected pair and no `all_present` changes.
- **The edge names a leaf allowlist (precondition e):** the order stops; nothing is applied.
- **The publisher's role could not write the key:** the simulation reads PutObject ALLOWED for `platinum/mdpf/global/category-views-history.json` (2026-10-13); a runtime AccessDenied
  would be an `error` row, never silent.

## 6. Client-visible deltas this pair accepts

None on its own: no existing page changes. The leaf is invisible until the Trend (CN-i-1) reads it. The Trend's Client chips then draw on the leaf's dates and are absent elsewhere.
The cent-exact sum for a chip date is read against that date's own dated time-series object, not the newest (row D1-S21: the snapshot and the newest time series differ by up to
301,207.84 on the same date; 0.00 against the date's own object).

## 7. Acceptance after the act (the issuer reads; never a leg of the CloudOps order)

On the first scheduled publisher run after D1 (13:50Z), with denominators printed:
1. the four keys exist and are served through `/api/general/mdpf/{scope}/category-views-history.json` (200, JSON), at the stated vintage;
2. each leaf's `dates` equal that scope's dated `category-views` keys (26, 25, 19, 21 at the base, +1 per scope per day) and its arrays equal the dated Client nodes' `aum` (the real arm
   of `r7_cn_j_1.py` re-run against the served leaf instead of an assembled one);
3. the manifest carries `history_rows` x4 with `status` published or unchanged and `omitted` empty; `all_present`, `published`, `missing_pairs`, `unexpected_pairs` are what the run
   would read without the cell;
4. every existing served leaf equal to its previous object apart from `_provenance.written_at`; the function's `CodeSha256` is the built package's and `MDPF_PUBLISHER_COMMIT` the pin;
5. nothing else under `platinum/mdpf/` moved (a listing diff before and after: four added keys, no removed key).
The issuer's read-back script for this list is OWED (`round7/checks/r7_history_readback.py`) and is written and dry-run against the reference leaf before the order is issued.

## 8. What the COO half asks the CTO half to read

1. Section 3 (N = 1) and section 4 (what moves, what cannot, the exposure line).
2. **The PRD's CONTRACTS row for the served platinum JSON** enumerates four leaves and does not name `category-views` or `category-views-history`; the leaf is a derived,
   non-1:1 served object, which the publisher's header forbids for gold-projected leaves ("NEVER patches shape, renames, or synthesizes fields"). The precedent for a
   deliberate extension is `taxsma_extend` (contract 0.6.0). Is a CONTRACTS addendum (ratified-text half, the CVO's) needed before this pair is signed? REC: yes, one row.
3. Precondition (e): the edge read is the one fact not measured by the issuer; a CloudFront or WAF finding stops the order and routes to FIRMBKTS ownership (R2).
4. The separate finding that the publisher's role cannot read its own pointer (the D5 "unchanged => no write" comparator is dead in production): not this pair's to repair; a row and
   its own pair (an IAM grant on one key) are the issuer's to file.

## COO half -- OWED (`2.0.0_SA_COO~D1`)

Sign on the bytes the CTO read, naming: the blast radius in section 4, every branch in section 5, the rollback per key in section 2 (the four keys are new; bucket `opal-data-portal-v2`
has versioning Enabled, so a later write of a leaf has a prior VersionId; a delete of a leaf needs a human's word), and the conditions that the pin is on origin before D1 and the
edge read of precondition (e) reads clean.

## CTO half -- OWED (`1.0.0_SA_CTO~DELL1`)

Sign, or refuse naming what is missing; a signature is a line in a commit by that seat, and no message carries it.
