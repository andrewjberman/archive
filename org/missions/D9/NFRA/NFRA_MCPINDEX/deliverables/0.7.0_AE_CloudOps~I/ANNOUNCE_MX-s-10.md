# ANNOUNCE -- MX-s-10 PHASE A: the asset-dim document is ported; its ad-hoc test is REFUSED with its measurement

**Seat:** `0.7.0_AE_CloudOps~I` · **Order:** `NFRA_MCPINDEX.TO-MX-s-10` @`ed19b7b4e4` (identical at HEAD)
**Ruling (the spec):** `1.0.0_SA_CTO~O` @`bf94418eb8` · **Row filed:** `NFRA_MCPINDEX-Z-S43` (BLOCKING)
**Date:** 2026-09-28 07:4x-08:1xZ · **Nothing was deployed.** No SSM version published, no Terraform applied.

**The never-widen halves are asked on this file.** One thing below changes what they are signing off on:
step 2's test did not run, so **no run of the new path has been observed anywhere.** The halves would be
signing a document read, not a document exercised. That is stated here rather than left to be noticed.

---

## Step 1 -- the document is ported

`infra/aws/ssm/opal-bd-asset-dim-download.json`, repo only. Asserted in the edit script, not eyeballed:

| property | before (v3) | after | required by |
|---|---|---|---|
| runCommand lines | 66 | 97 | -- |
| `download-daily-asset-dim.ts` refs | 1 | **0** | step 1, AC1 |
| `BD_PASSWORD` / `BD_USERNAME` refs | 2 / 1 | **0 / 0** | step 1, AC1 |
| `opal/bd/credentials` read | 1 | **0** | step 1 |
| `pull_bd_asset_dim_rest.py` refs | 0 | **3** | step 1, AC1 |
| `build_bd_assets_dim.py` refs | 0 | **3** | step 1, AC1 |
| shutdown index vs `exit 1` index | 58 < 63 | **89 < 94** | KEEP (MX-s-4 / Z-S17) |
| count of each | 1 / 1 | **1 / 1** | KEEP |
| log upload | present | **present** | KEEP |
| non-ASCII chars | 2 | **0** | CLAUDE.md (production AWS) |

The edit refuses to apply unless the inbound payload is exactly the 66-line v3 it was written against, so
it cannot be applied twice or onto a payload someone else has moved.

**Two design decisions that are not cosmetic, both forced by what the scripts actually do:**

1. **It stages a TREE, not two files.** `pull_bd_asset_dim_rest.py:66` inserts `sys.path` four levels
   above itself and `:67` does `from lib import opal_naming`; `build_bd_assets_dim.py:50-51` inserts
   `../gold` and imports `lib.etf_classifier`. The v3 document's only python fetch was a FLAT
   `aws s3 cp ... convert_assets_to_silver.py .`. A flat copy puts the pull script where its
   four-levels-up resolves to `/`, and the import dies before any vendor call. So the new payload builds
   a `RUNROOT` that mirrors the repo shape.

   *The naming gate earned its keep here.* My first version wrote
   `RUNROOT=/opt/bd-exporter/restrun` and the commit was **REFUSED**: LGIC_ENFORCE DEC-6 graded it a
   *"NEW hand-kept carrier of 'bd' outside every permitted context"*. It was right -- the v3 line 2
   already does `cd /opt/bd-exporter`, so re-typing the firm path was both a rule-30 violation and a
   duplicated literal. It now reads `RUNROOT="$PWD/restrun"`, derived from that `cd`. Recorded because
   a gate refusal that produced a better line is worth more in the record than a silent fix.
2. **It resolves `--as-of` itself and refuses rather than guessing.** The MX-s-9 scheduling spec (s.5)
   requires the last COMPLETED trading day via `prev_trading_day`, "never a hand-typed date" -- but the
   module **defaults `as_of` to `datetime.now(timezone.utc)`** at `:526`. At the 22:10Z slot, today may
   not be loaded at the vendor. The module will not compute it and it is a rule-13 DS-owned path, so the
   document computes it and sets `PULL_RC=91` with a loud message if it cannot. It never guesses a date.

## Step 2 -- REFUSED, with its measurement (bound 4)

**The ad-hoc run was not fired, and could not be.** Row `Z-S43`. The order's condition was "if [the
scripts] are not yet published where the instance reads" -- and that condition reads **FALSE for the
scripts and TRUE for their dependency closure**, which is the split worth naming:

- Both scripts are published and current: `comp-pipescript deployed` reads **MATCH** for
  `pull_bd_asset_dim_rest.py` (bd-bronze) and `build_bd_assets_dim.py` (bd-silver), basis *"raw bytes
  (working tree and S3 object are byte-identical)"*. This is not a stale-deploy finding.
- Their imports are **absent from the whole bucket.** Whole-bucket key census of `opal-data-bd`, with a
  positive control so a zero reads as absence and not as an out-of-corpus read:

  | dependency | keys in bucket |
  |---|---|
  | `opal_naming` | **0** |
  | `trading_calendar` | **0** |
  | `registry/` · `scopes.json` | **0** |
  | `etf_classifier` (POSITIVE CONTROL) | **2** |

  The control is the point: `etf_classifier` **is** published, at `code/gold/lib/etf_classifier.py`,
  which is exactly why the builder's dependency resolves and the pull's does not.

**What must be published, to the instance's read channel, before step 2 can run:**
`lib/opal_naming.py` · `lib/trading_calendar.py` · the 7 `infra/logic/registry/*.json`
(`systems, scopes, tiers, exemptions, remediations, resources, reporting_policies` -- from
`opal_naming.py:54-55`) · `org/standards/NAMING_SCHEMA.json` (`:52`).

All four groups sit under rule-13 DS-owned or non-granted paths, so **none is this lane's to publish.**
The ported document carries a `BLOCKED:` marker on those exact fetch lines, and **must not be made
DEFAULT until they land.**

## Step 3 -- caller census

### `download-daily-asset-dim.ts` -- 0 live callers besides this schedule. RETIREABLE.

`comp-find 'download-daily-asset-dim'`: **36 hits across 76,897 files scanned**; bands HEAD=10,
SURFACED=11, CONFIG=3, DOC=12. Exactly one *executing* reference:
`infra/aws/ssm/opal-bd-asset-dim-download.json:39` -- the document this order edits. Every other hit is
prose (`docs/architecture/BD_ASSET_DIM_PIPELINE.md`), historical task orders and logs, the AC1 check
script itself, this order's own text, label/prediction corpora (`rcg/ledger/LABELS.jsonl`,
CRO `predictions_*.jsonl`), a token census (`LGIC_ENFORCE/CARRIER_CENSUS.md`), and a **docstring
comment** at `bd-asset-dim-trigger/lambda_function.py:6` -- a comment, not an invocation.

One stale doc to correct rather than trust: `NFRA_GRAPHUNI.P1-B` line 40 records this producer as
"(Step Functions)". It is SSM, not Step Functions.

**Path note, not a silent widening:** the retirement targets are
`infra/aws/ec2/bd-exporter/src/stepwise/download-daily-asset-dim.ts` and its `_ts_source` entry at
`infra/aws/ec2/EC2_MANIFEST.json:309` (rule 8's source of truth). **`infra/aws/ec2/` is not in this
order's `<paths>`.** So the census clears it for retirement but this lane cannot perform it. Issuer call.

### The fees downloader -- 1 LIVE caller. **NOT retireable**, and it is a second live instance of Z-S8/Z-S9.

The preflight says the fees schedule leg is removed "only after its caller census reads 0". **It reads 1.**
Measured live, not from the repo:

- `bd-fees-pipeline-trigger`: **ENABLED**, `cron(15 22 ? * MON-FRI *)`, target `bd-fees-trigger`
  (the Terraform resource name in the docs is `bd_fees_pipeline`; the live rule name is
  `bd-fees-pipeline-trigger`, and `bd-fees-pipeline` does not exist -- `ResourceNotFoundException`).
- `bd-fees-trigger/lambda_function.py:30` -> `SSM_DOCUMENT = 'opal-bd-fees-download'` (the only DEF-band
  hit in 428).
- `opal-bd-fees-download.json:39` -> `bun run src/stepwise/download-daily-fees.ts`.

So the chain is wired and firing every weekday, five minutes after asset-dim, on its own instance
`i-0868fc7e7ebec26f2`. **I did not retire it and did not touch it.**

**The finding that came out of this census, which the order did not ask for and which I am not fixing:**

| | asset-dim (fixed under MX-s-4) | **fees (still live)** |
|---|---|---|
| failing logs / denominator | 69 of 119 | **69 of 121** |
| first failure | 2026-06-23 | **2026-06-23** |
| last good | 2026-06-22 | **2026-06-22** (2,816 bytes) |
| failure signature | `TimeoutError ... navigation to **/bd3.bdreporting.com/**` | **identical** |
| every failing log's size | -- | **exactly 886 bytes, 69 times** |
| SSM verdict on a failed run | Failed (since MX-s-4) | **Success** |
| `exit 1` in the document | present at :94 | **absent entirely** |

The fees document's failure branch (`:53-56`) echoes ERROR, re-uploads the log, and falls straight
through to `shutdown -h +2 &` at `:59`. There is **no `exit` of any kind** in its 60 lines. So it always
reports Success and 69 consecutive failures are invisible -- the same defect MX-s-4 step 2 removed from
asset-dim, still standing here. It does NOT strand its instance (shutdown is unconditional and last),
so this is the Z-S9 half without the Z-S17 half.

The data is not at risk -- the ruling records `bronze/fees` as current via the REST runner. What is
live is a **producer that fails daily and says it succeeded.** Not in this order's scope; named for
the issuer rather than absorbed.

## Step 4 -- Terraform

**The asset-dim document change needs no Terraform.** `comp-find 'aws_ssm_document'`: 225 hits, 3 DEF.
`infra/aws/terraform/bd-pipeline/` declares exactly **one** `aws_ssm_document` --
`bd_49f_session_fetch` (`bd-49f-session-chain.tf:67`). Neither `opal-bd-asset-dim-download` nor
`opal-bd-fees-download` is Terraform-managed, matching the 2026-04-10 AE record: *"Registered via
`aws ssm create-document` ... not managed by Terraform"*.

And **no EventBridge or Lambda change is in PHASE A's scope**, because the fees leg is not being removed
(its census reads 1, not 0).

**`terraform plan` was NOT run, declared rather than skipped.** `infra/aws/terraform/bd-pipeline/.terraform`
is absent, so `plan` requires `init` -- a provider download and a mutation of the working tree -- and it
would grade resources this phase does not change. Per CLAUDE.md section 2 (when the next check would not
change what you do, stop) I did not run it. **If the issuer wants the baseline plan recorded anyway, say
so and I will init and run it** -- it is a read-only plan and the only cost is the provider fetch.

## Criterion state right now

| | verdict | why |
|---|---|---|
| `s10.AC1` | **FAIL** -- served: rest-pull 0, builder 0, playwright 1, BD_PASSWORD 2 | correct: it grades the SERVED document and PHASE A deploys nothing |
| `s10.AC2` | **PASS** -- ENABLED, `cron(10 22 ? * MON-FRI *)`, 1 target = `bd-asset-dim-trigger` | regression guard intact; one producer before, one after |
| `s10.AC3` | not yet gradeable | its acceptance is the next scheduled 22:10Z fire |

## What PHASE B needs before GO

1. **The dependency publish (Z-S43) -- the hard gate.** Until it lands the document cannot run at all,
   so making it DEFAULT would replace a producer that fails loudly with one that fails at `aws s3 cp`.
2. **Step 2's ad-hoc run, then the halves.** The ruling asks both halves on "one ad-hoc run of the new
   SSM path producing the same dim as the MX-s-6 result: same `asset_id` set, row counts stated." That
   run has not happened, so the `asset_id`-set diff this announce was meant to carry **is not in it.**
3. The rollback to record at PHASE B: the prior document version is **3** (Active, default,
   hash `490af524...d442129`), restorable as DEFAULT.

## Bounds honoured

One producer before and after; no second schedule, no parallel path, no comparator. Nothing under
`data/cot/`. Served gold untouched. No account ids or asset rows in the repo -- this file carries counts,
byte sizes and hashes only. No push.
