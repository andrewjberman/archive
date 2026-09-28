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

---

# ADDENDUM -- amendment A2 (2026-09-28 ~09:0xZ): the closure moves to build time, and I had missed a dependency

`2.0.0_SA_COO~O` amended the order at `@864ea3b7ef` on `1.0.0_SA_CTO~O`'s Z-S43 ruling `@e4b19b9898`.
The document is re-edited accordingly; **still PHASE A, still nothing deployed.**

## The ruling changed the shape, and it is a better shape than the one I proposed

I proposed publishing `opal_naming` plus the 7 registry JSONs plus `NAMING_SCHEMA.json` into the firm
bucket. The ruling refuses that and resolves the closure **at build time** instead: MX-s-11
(`0.4.0_DS_ClientPlatform~D`) generates a 49F **pin** that the pull module imports in place of
`opal_naming`, so **the multi-firm registry never travels to bd's bucket at all.**

That is the correct call and my proposal was the worse one. Copying a *multi-firm* registry into a
single firm's bucket to satisfy an import would have put cot's rows inside 49F's plane — the exact
firm-separation line CLAUDE.md rule 13 and this module's own `assert_firm_separation` exist to hold.
I was solving for "make the import resolve" and not asking what the artifact *contained*.

## A dependency I missed, and why my instrument could not see it

A2 also names `code/lib/silver_ids.py`, which my Phase A census did not. Verified at the cited lines
rather than taken on trust -- `build_bd_assets_dim.py:64-70`:

```
_REPO_ROOT       = <four levels above silver/>
_SILVER_IDS_PATH = _REPO_ROOT/lib/silver_ids.py
_spec = importlib.util.spec_from_file_location('opal_lib_silver_ids', _SILVER_IDS_PATH)
_spec.loader.exec_module(_silver_ids)          # at MODULE LOAD, top level
```

It is a hard dependency, and the builder's own comment (`:56-63`) explains why it is loaded by
location: inside that file the name `lib` is already gold's, so `import lib.silver_ids` raises
`ModuleNotFoundError` -- measured, and re-ordering cannot fix it without breaking
`lib.etf_classifier`.

**My dependency census used an import-statement regex** (`^\s*(import|from)\s+(lib|...)`). A
`spec_from_file_location` load is *invisible* to it. So the census returned a clean, denominated,
confidently-wrong closure. I have now swept both scripts for every by-location mechanism
(`spec_from_file_location`, `exec_module`, `importlib`, `__import__`, `SourceFileLoader`, `runpy`) and
found exactly one, the one A2 names; and I checked `etf_classifier.py`'s own imports, which are stdlib
and `boto3` only, so the closure is complete at six members.

This is the **second** time this session a regex-shaped instrument of mine under-counted a real set --
the first read 6 occurrences where 18 existed, because one combined alternation swallowed the match it
was looking for. Same failure class: a pattern that matches the *usual spelling* of a relationship and
silently misses the unusual one, while still printing a denominator that makes the answer look measured.

## The document after A2

| | |
|---|---|
| runCommand lines | 97 -> **98** (7 dropped, 8 added) |
| `opal_naming` / `code/registry/` / `NAMING_SCHEMA.json` fetches | **0** (deleted, with their `infra/logic/registry` and `org/standards` mkdirs) |
| shutdown index vs `exit 1` | **90 < 95**, one of each -- KEEP property re-asserted after the patch |
| non-ASCII | **0** |

Staged closure, each asserted present **exactly once**:

| member | into |
|---|---|
| `code/bronze/pull_bd_asset_dim_rest.py` | `$RUNROOT/data/black_diamond/scripts/bronze/` |
| `code/bronze/_asset_dim_rest_pin.py` | same dir (the generated 49F pin, MX-s-11) |
| `code/silver/build_bd_assets_dim.py` | `$RUNROOT/data/black_diamond/scripts/silver/` |
| `code/gold/lib/etf_classifier.py` + `__init__.py` | `$RUNROOT/data/black_diamond/scripts/gold/lib/` |
| `code/lib/silver_ids.py` | `$RUNROOT/lib/` |
| `code/lib/trading_calendar.py` | `$RUNROOT/lib/` |

## Step 2 is no longer refused -- it is SEQUENCED

A2 sets it to run when the issuer relays **MX-s-11's `s11.AC2` and `s11.AC3` at PASS**. So this seat is
not blocked and not waiting on a ruling; it is waiting on a named upstream signal from another cell.
Row `Z-S43` stays ARMED with `2.0.0_SA_COO~O` as `disarm_owner` until that relay lands and the run
happens.

**What the never-widen halves are still being asked to sign remains a document READ, not a document
EXERCISED** -- and the `asset_id`-set diff is still not in this file, for the same reason. That does
not change under A2.

---

# STEP 2 ADDENDUM -- two ad-hoc runs, neither reached the vendor; a second BLOCKING row (Z-S44)

Issuer GO at 094028Z (its own s11.AC1/AC2/AC3 re-run at HEAD). Before running I re-ran `s11.AC2` and
`s11.AC3` myself -- PASS and PASS, 4 of 4 byte-identical to HEAD -- so the gate rested on three
independent runs (DS's, the issuer's, mine) rather than a producer's self-report.

**Neither run reached Black Diamond. Zero vendor calls have been made by this cell.** That matters
because the order budgets "one ad-hoc run": attempt 1 died inside the document's own date resolution
before any network call, and attempt 2 died at the Secrets Manager read, which precedes
`mint_bearer`. The vendor budget is intact.

## The BEFORE/AFTER oracle, and why its DELTA=0 is NOT the acceptance

One instrument, run on both sides -- writing a second differently-shaped reader would have made any
difference unattributable between the world and the instrument.

| | BEFORE | AFTER |
|---|---|---|
| LastModified | `2026-09-28T06:22:06Z` | **`2026-09-28T06:22:06Z`** |
| ETag | `a218b3ddb9f93db93ba6fa45b3a97f66` | **identical** |
| rows / unique `asset_id` | 12,141 / 12,141 | 12,141 / 12,141 |
| `asset_id` set sha256 | `b38a8b0a…4cb9616a` | **equal** |
| added / removed | -- | **0 / 0** |

**Read this correctly.** The served `silver/bd_assets_dim.parquet` was **not touched** -- which is the
NEVER-1 assurance worth having, since both runs failed on a SERVED-class producer. But the DELTA=0 is
**produced by the failure, not by agreement**: the pull never ran, so nothing could have differed. It
is a zero measured downstream of the bypass. The order's and the ruling's DELTA=0 -- the pull running
and yielding the same `asset_id` set -- **remains unexercised**, and the never-widen halves should not
read this table as satisfying it.

The BEFORE side does cross-check independently: 12,141 = MX-s-9's 12,132 pulled rows + the 9-row
union tail it measured, and `asset_id` is unique 1:1 with rows.

## Attempt 1 -- `ssm:c8c60492-b443-4839-b16c-8eebf1e1c859`, Failed rc=1, 09:49:03->09:49:11Z

Cause was **mine**: `ERROR: could not resolve the last completed trading day; refusing to guess a date`
-> `PULL_RC=91`. The log stderr names it exactly:

```
TypeError: prev_trading_day() missing 1 required positional argument: 'date'
```

`lib/trading_calendar.py:93` is `def prev_trading_day(date: object)`. I wrote that call from the
MX-s-9 spec's *prose* ("via `lib/trading_calendar.prev_trading_day`") without reading the signature --
the same class of error I spent this session catching in other people's work. Ruled as amendment A3
`@9b5e3c3fd9`, which prescribes the fix I had already applied; the issuer diagnosed it independently
from the same log.

**What it proved anyway:** the A2 closure staged **7 of 7** objects into the RUNROOT tree, every fetch
succeeding -- so the dependency set and the tree shape are right. And my refusal guard did its job:
rather than passing an empty or guessed date to the vendor, it stopped.

The fix is verified twice, not once: `prev_trading_day(now(utc).date())` returns **09/25/2026**
locally, and the **exact line lifted from the document** -- same quoting, same shell -- also resolves
`09/25/2026`. A3 asked for the local run first; that is it.

## Attempt 2 -- `ssm:103d29fd-1960-4944-ba60-17b797c603f9`, Failed rc=1, 10:07:37->10:07:47Z

The as-of resolved and the run advanced to `pull_bd_asset_dim_rest.py:172 load_bd_cookie`, where:

```
botocore.exceptions.ClientError: AccessDeniedException ...
User: arn:aws:sts::313476888478:assumed-role/bd-exporter-ec2-role/i-0e6f6dc014fdcf1cd
is not authorized to perform: secretsmanager:GetSecretValue
on resource: blackdiamond/49f/session
```

**This refutes this order's own preflight**, which declares `comp-iam:
DECLARED-NOT-APPLICABLE -- the instance role already reads blackdiamond/49f/session (used by the
MX-s-9 module)`. Filed as row **`Z-S44`**, under the same preflight's own contingency: *"if a
permission is missing, that is a BLOCKING row, never a hand-added grant."*

Why the premise was wrong, as a mechanism rather than a slip: it reasoned *the MX-s-9 module reads
this secret, therefore the instance role reads it.* The module does read it -- but every run of it so
far was made by a principal that **holds** the grant, never by `i-0e6f6dc014fdcf1cd`. Moving a working
script to a new host moves it to a new **principal**, and the script's past success carries its old
identity context silently.

Measured, on both planes:

- **DESIRED** (`comp-iam role bd-exporter-ec2-role`, chosen over a raw `get-role-policy` because its
  TF-vs-live reconcile is what catches a declared-but-unapplied control): 34 statements, exactly
  **one** `GetSecretValue`, on `anthropic-api-key-*`, `openai-api-key-*`, `opal/bd/credentials-*` and
  one entry the tool truncated as `... +1 more`. **The truncation is named, not read through** -- the
  absence verdict rests on the live refusal, never on that elided list.
- **Whose grant it is** (`comp-find 'blackdiamond/49f/session'`, 570 hits / 76,953 files, all 10 DEF
  shown): every consumer is a **Lambda** (`bd-49f-runner:56`, `bd-49f-fees-runner:40`,
  `bd-49f-keepalive:45`, `bd-49f-freshness-probe:55`, `bd-49f-session-trigger:76`,
  `opal-assets-bd49f-daily-pull:70`, `-reporting-pull:45`) or the `bd-49f-auto-login` EC2, which
  **writes** it. Not one is `bd-exporter-ec2-role`.

So the role is provisioned for the **portal era**: its one secret grant is `opal/bd/credentials` --
the username and password this very order removes.

**The delta is one statement**, and I did not add it: `secretsmanager:GetSecretValue` on
`arn:...:secret:blackdiamond/49f/session-*`, via Terraform and `safe-apply` (rule 18). Not proposed as
a rider, because an EC2 instance role gaining read on a live vendor session token is a widening that
wants its own sign-off -- the same instance runs the other BD Playwright downloaders, so the grant is
not scoped to this producer alone. Two things Z-S44 does **not** claim: that the grant is safe to add
(the grantor's call), and that it is sufficient -- nothing past `load_bd_cookie` has ever run.

## The KEEP properties are now exercised three times

Across the MX-s-4 planted probe and both of these real failures, SSM recorded **Failed** and the
instance **stopped itself** every time -- 09:51:38Z and 10:10:28Z here. The honest exit and the
shutdown-before-exit ordering are no longer single-observation properties.

## What PHASE B still needs

1. **Z-S44** -- the IAM statement. Hard gate; without it the producer cannot authenticate at all.
2. **Then step 2 re-run, and only then the halves.** The `asset_id`-set diff the halves are meant to
   weigh still does not exist, for the third time of saying so.
3. Rollback unchanged: prior document version **3**, Active, hash `490af524...d442129`.
