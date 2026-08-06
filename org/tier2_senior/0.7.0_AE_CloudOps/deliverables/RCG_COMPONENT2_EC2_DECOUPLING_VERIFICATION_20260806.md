# RCG Component 2 -- EC2-decoupling verification for the 70-file AE bundle

**From:** `0.7.0_AE_CloudOps`  **To:** `4.0.0_SA_CRO`  **Date:** 2026-08-06
**Authority:** Andrew-direct GO at this terminal 2026-08-06, scoped verbatim to CRO's two components.
**Condition discharged:** R-0026 clause (2) -- *"cohort-B = ONE cohort verdict ARCHIVE for the 51
seeking_alpha_scraper files CONDITIONAL on EC2-decoupling verification at derive."*

## VERDICT

**DECOUPLED -- the 51 `infra/aws/ec2/seeking_alpha_scraper/` files are archive-safe.**
No live EC2 flow pulls them. Grounding per claim below; every claim names the instrument that
produced it and the layer it observes (Rule 22a).

**SCOPE BOUND, stated first because it is the thing most likely to be over-read:** this verdict
covers **the 51 REPO FILES**. It is **NOT** a verdict on the two EC2 instances, and it is **not** a
warrant to terminate, modify, or reclaim them -- see finding F-4, where a second system documents
one of those boxes as its own deploy host.

## Vintage of the instrument (requested by CRO)

`infra/aws/ec2/EC2_MANIFEST.json` @ commit **`772ff82f558d0459162757a14d041ff2dd9f88f8`**,
2026-08-05 18:30:10 -0400, author `0.7.0_AE_CloudOps~C`. `_last_updated` field: `2026-08-05T22:30:00Z`.
Live-AWS reads below were taken 2026-08-06 ~17:1xZ, i.e. AFTER that vintage, so the live layer is
not stale relative to the declared one.

## Grounding table

| # | Claim | Layer | Instrument | Result |
|---|---|---|---|---|
| 1 | The tree IS a registered EC2 service | DECLARED | `EC2_MANIFEST.json` `services["seeking-alpha-scraper"]` | `source_path` = `infra/aws/ec2/seeking_alpha_scraper` -- **exact match to the 51** |
| 2 | Both backing instances are stopped | **LIVE** | `aws ec2 describe-instances` on both IDs | `i-06376c11d8b3c3443` **stopped**, `i-07ebae29a16e43ed1` **stopped** |
| 3 | Neither has been started in ~5.5 months | **LIVE / BEHAVIORAL** | `StateTransitionReason` | both *"User initiated"*, **2026-02-17** -- 170 days un-started as of today |
| 4 | Nothing schedules a start | LIVE | SSM `list-associations` (0 assoc.); EventBridge scan for `seeking`/`alpha` | 0 hits (see C-1 on this denominator) |
| 5 | The deploy path cannot reach the box | SOURCE + prior exercise | `deploy_hybrid.sh` reads scp/ssh over port 22; my lane's 2026-03-10 transport audit measured **port 22 CLOSED** | deploy path **DEAD** |
| 6 | The EC2 side fetches nothing from S3 | SOURCE | `deploy_hybrid.sh` | no S3 leg at all -- it scps from a workstation. Under Rule 12's *"check what the EC2 side actually fetches"*, the answer is **nothing**, because nothing can reach it |
| 7 | The 15 lambda strays back no live function | **LIVE, full denominator** | `aws lambda list-functions` walked to exhaustion | **196** functions total (single page, `NextMarker` absent = true total, not a page size). **0** name matches for `market_query` / `news_scanner` / `calc_aum|calc_normalized|calc_returns` / `unauth` |
| 8 | ...and no source-map function claims those dirs | DECLARED | `lambda-source-map.json` (197 entries) | 0 real claims; the 3 apparent hits are substring artifacts on **different** dirs (`tools/news_scanner/...`, `infra/aws/users/lambda/portal-authorizer`, `infra/aws/lambda/portal_data_proxy`) |

**The load-bearing row is #3, and it is deliberately the behavioral one.** Rows 1/4/5 are
declarative or config-layer. Row 3 is the path exercising itself over 170 days: had *any* live flow
started those boxes, they could not still be sitting on a February user-initiated stop. A rule
inventory can be incomplete; 170 days of not-started cannot be.

## Bundle composition -- confirmed exactly

| Component | Count | Paths |
|---|---|---|
| prompts | 4 | `infra/prompts/{data_scientist,devops_technician,quantitative_assistant,vba_programmer}.md` |
| lambda strays | 15 | `infra/aws/lambda/` -> `market_query` (3), `news_scanner` (3), `portal` (4), `test_seeking_alpha_unauth` (5) |
| seeking_alpha_scraper | 51 | `infra/aws/ec2/seeking_alpha_scraper/**` |
| **TOTAL** | **70** | matches CRO's stated bundle exactly |

All 51 carry `label=MIGRATE`, `binary=ARCHIVE_CANDIDATE`, `ruling=R-0020`, uniform -- no mixed
dispositions inside the cohort, which is what makes ONE cohort verdict legitimate.

## Findings CRO must read before executing the batch

**F-1 (CORRECTS THE OBVIOUS READ) -- the manifest DOES register this service.** A verification that
concluded "not in EC2_MANIFEST, therefore decoupled" would have been **wrong**. It is in there, its
`source_path` is exactly the 51-file tree, and its `deploy_script` is *itself a member of the 51*
(`deploy_hybrid.sh`). The decoupling is real but it rests on liveness (rows 2/3/5), **not** on
absence from the manifest.

**F-2 (DENOMINATOR GAP IN THE CONDITION'S OWN INSTRUMENT) -- there are TWO instances; the manifest
names ONE.** `EC2_MANIFEST.json` carries only `i-06376c11d8b3c3443`. The estate census and the live
API both show a second, `i-07ebae29a16e43ed1`, same Name tag, same type, also stopped. **R-0026's
condition says "verify per EC2_MANIFEST.json" -- executed literally, that instruction would have
checked one of two boxes and reported clean.** I checked both. Flagging because the condition's
wording, not my execution, is what was one short; a future condition phrased the same way inherits
the same blind spot.

**F-3 (BATCH MECHANICS) -- two members are not ordinary files.**
`cookie-env/lib64` is a **symlink** (venv artifact), and `seeking_alpha_cookies.json` is a
**captured-session credential artifact**. Neither changes the verdict, but a sha256-per-path batch
step will behave differently on a symlink than on a regular file, and the cookies file is worth
routing as a secret-hygiene item rather than a plain archive -- your call, flagging not adjudicating.

**F-4 (SCOPE FENCE -- the instance is NOT exclusively this tree's).**
`infra/aws/lambda/news_semantic_clustering/docs/DEPLOYMENT_STATUS.md` documents
`i-07ebae29a16e43ed1` as a **borrowed deploy host** (`./deploy_via_ec2.sh --use-existing-instance
i-07ebae29a16e43ed1`, listed as a "Next Step"). That system uses the *box*, not the *51 files*, so
it does not block this archive. **But it does mean "archive the tree" must not cascade into
"terminate the instances."** If anything later proposes reclaiming those boxes, that is a separate
decision with a different blast radius.

**F-5 (LEDGER CITATION MISMATCH -- your sha does not resolve).** You told me to verify your
B-0009 correction *"in the complete BATCHES.jsonl row -- verify there, not on my message."* I did.
**Your substantive correction is CONFIRMED: B-0009's 86 members contain ZERO `infra/aws/lambda`
paths** (independently recomputed from the row's own `paths` array). **But the sha256 you cited,
`a6542181877ecbc`, appears on no B-0009 row.** The three `id == "B-0009"` rows carry:

- row 36, `RATIFIED`, count 86, `sha256: null`, `paths: []` (the complete-row-first opening)
- row 37, `RATIFIED`, count 86, `sha256` **`44cee2ec777425b1ae83d8bac4582f3a12fd33fcf71824335badd42335185878`**
- row 38, `EXECUTED`, count 86, same `44cee2ec...`

So the claim is true and the pointer to it is wrong. I am reporting rather than reconciling it --
the ledger is yours. Note the direction of the risk: **you sent me to a sha as the authority
precisely so I would not trust your prose, and the sha is the part that did not resolve.** Had I
verified only the sha and not recomputed the membership, I would have reported your correct
correction as unverifiable.

## What I did NOT verify

- I did not exhaustively enumerate EventBridge rules. An attempted full walk hit the paginated-count
  artifact CLAUDE.md records (`list-rules` returning exactly 100), then MSYS argv mangling between
  native Python and the bash `aws` shim. **I abandoned it deliberately**: row 3 is stronger evidence
  than a rule census, and I would rather report one sound behavioral measurement than an
  inventory whose denominator I could not defend. Stated so it is not mistaken for coverage.
- I did not verify the *contents* of the boxes. Per the manifest's own `parity_note`, the 2026-07-23
  "remote path empty" SSM read was an **instrument false-verdict**, and no honest on-box baseline
  exists. Starting a stopped box to inspect it would change the very state I am certifying, so I did
  not. **What is on those disks is UNKNOWN and I am not claiming otherwise** -- the verdict is about
  whether a live flow pulls the repo files, which rows 3/5/6 answer without needing the disk.

## Disposition

Component 2's condition is **discharged**. The one-cohort ARCHIVE verdict for the 51 may execute on
your side; the 4 prompts and 15 lambda strays carry no EC2 condition and are clear on rows 7/8.
Ledger mechanics remain yours -- I supplied verification only and mutated nothing.
