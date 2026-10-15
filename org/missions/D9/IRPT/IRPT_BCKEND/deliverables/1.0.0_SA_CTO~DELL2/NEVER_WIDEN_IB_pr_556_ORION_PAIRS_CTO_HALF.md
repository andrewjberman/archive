# IRPT_BCKEND IB-pr-556 -- the Orion pairs, (a) the 36-key re-pull and (b) the scheduled raw producer: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~05:0xZ. **Bound to:** `deliverables/0.9.0_WK_IRPT_BCKEND~400/ORION_PAIRS_PACKET_V1.md`,
**sha256 `c3dcc22f02e8624eca4f402f77fe95ba28c3df331a0896e22ef94dd19bc56b62`** (this seat's `sha256sum`). The COO half is at those bytes
(`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_556_ORION_PAIRS_COO_HALF.md`, commit 17172025c0). A different hash voids this half.

## What this half covers (packet section 12)

- **The never-widen scope (section 3) is accepted.** The pair writes 36 bronze keys, one schedule, one function, and the snapshot date's silver
  convert the existing handler already writes. Nothing else.
- **The manual CLI writes are retired in the same release** that enables the fold, together with the three 11:15-11:32 UTC rules. The fold
  and the old rules never run side by side, so there is no second producer.
- **The names are builder output:** `orion-inf-raw-producer-daily` and `orion-inf-raw-producer-lambda`, at `cron(0 6 * * ? *)`
  `America/New_York`.
- **The trading-day frontier** comes from `lib/trading_calendar.py` (section 8).

## Conditions (they tighten, never widen)

1. **The daily flat-key writer is located BEFORE (b) deploys** (the COO half's condition 1, row D2-S184). Keys land at 11:39-11:56Z with no
   writer in the repo's AWS code, so look where a "manual" CLI could fire on a timer:
   - every box's Windows scheduled tasks (`schtasks /query /v` on dell1, dell2, laptop and site Z, through their MSTRs);
   - CloudTrail data events or S3 server access logs on `opal-data-inf/bronze/`, if enabled;
   - any ECS, Glue or Batch run whose start time precedes the keys.
   The located writer is retired in the same release as the old rules. **If it is not found, (b) does not deploy:** a fold writing the same
   keys beside an unknown writer is the shadow producer this estate forbids. That outcome comes back to this seat as a finding.
2. **Every reader of the bronze key whose shape changes is read before the build.** The deployed positions write moves from parquet to the
   flat `.jsonl.gz`. The positions silver convert, and any other reader the graph or `comp-find` names, must read the new shape. A test
   covers the convert on one flat key. A reader left on parquet is a STOP.
3. **Rollback by delete is Andrew's act.** Dell agents are denied `s3:DeleteObject*` on `opal-data-*`, and S3 deletes need his confirmation
   (CLAUDE.md Agent Autonomy). A failed read-back stops the run (section 9). The failed key is registered as ONE open-calls act with its exact
   key and VersionId. The lane never deletes.
4. **Silver for the 36 days is a separate later act.** Pair (a) writes bronze only, so B-IN's two needed days (07-01, 09-28) reach silver only
   through the existing convert run for those dates. It is cut next round under its own read: which served chains read that silver, with
   served DELTA stated. This pair does not carry it.
5. **The Scope addendum's attribution** (what replaces `members != 1` at `orion_account_mapping.py:84`) is a build-slice decision. Each
   account is attributed to itself, and no household figure is built from the feed's account rows (row D2-S60). `fee_basis` NET is recorded with
   its sample note.

**Both branches are covered:**
- A clean run writes 36 keys, each read back, and the fold fires daily with the old writers retired.
- A breach stops at the first failed key, with the written keys listed and the failed key's delete registered for Andrew.
- An unlocated writer means (b) does not deploy.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on sha256 `c3dcc22f02e8624e...`, with conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2

## VOID for execution (2026-10-15 ~06:1xZ)

**This half's pair (b) MUST NOT be executed on these bytes.** Condition 1 fired as designed. The flat-key writer is the gold chain's
INF_API_PULL steps on `inf-gold-layer-runner` (started by `inf-gold-trigger`, ~11:32Z), and those steps also feed silver (row D2-S186; CVO~IRPT
ADJUDICATION_v105 @bb31cfe773). Porting them would double the feed or starve silver. Ruled to `~P2` on msg 8124: (b) is RE-CUT as a re-timing of
the existing trigger into the 06:00 New York fold, with the frontier read first, and (a) re-runs the 36 days through the chain's own pull
steps. Both halves are re-signed on the NEW packet's bytes. Nothing on sha256 `c3dcc22f...` is executed.
