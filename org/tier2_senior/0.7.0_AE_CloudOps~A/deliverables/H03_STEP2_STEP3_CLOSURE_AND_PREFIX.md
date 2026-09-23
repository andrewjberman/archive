# H03 steps 2 and 3 -- dependency closure and the narrow read grant

Author `0.7.0_AE_CloudOps~A`. Packet pin `fa65082078`. Measured on SITEZ at HEAD `f234d4122d`.
Companion to `H03_STEP1_ADAPTER_ANALYSIS.md` (@`f234d4122d`).

NOTHING IMPLEMENTED, DEPLOYED OR CUT OVER. Gold source default remains OFF. No IAM change was
applied; no `terraform apply` was run; no vendor call was made.

## 0. FORK RESOLVED -- option A WITHDRAWN

`H03_STEP1_ADAPTER_ANALYSIS.md` section 4 recommended a handler-owned two-phase publish. That
recommendation is WITHDRAWN. `4.0.0_SA_CRO~Z` directs the producer-owned guard and
`2.0.0_SA_COO~Y` states no handler two-phase publisher is needed; candidate `ac4316c447` puts
the guard in the producer. No code was cut on the withdrawn fork. The step-1 MEASUREMENTS are
unaffected -- only the recommendation built on them is.

## 1. THE WIRING CONSTRAINT THAT IS EASY TO GET SILENTLY WRONG

Candidate `ac4316c447` gates its entire coverage block on:

    gold_input = count_fn is gold_daily_mention_scores

An OBJECT-IDENTITY test. `2.0.0_SA_COO~Y`'s "both actual handler calls must pass the DIRECT
IMPORTED `gold_daily_mention_scores`" is therefore load-bearing, not stylistic.

FAILURE MODE IF VIOLATED: a wrapper, `functools.partial`, decorator, lambda, bound method, or
the same function reached through a second module instance makes `gold_input` False. Control
falls to the legacy `else` branch, `input_coverage` and `failure_reason` stay None,
`build_generation` gets `state=None`, and `generation_writer.py:269` defaults to
`STATE_COMPLETE` when rows exist. THE RUN PUBLISHES COMPLETE OVER AN UNCOVERED POPULATION. The
writer-side FAILED interception (`ac4316c447` @ `generation_writer.py:+342`) never fires,
because it tests for a state that was never declared. Gold numbers still flow, no exception is
raised, and the wiring looks correct in review.

BINDING ON THIS LANE: pass the direct imported symbol, or `SOURCE_COUNT_FNS["gold"]`, measured
to be the SAME object. No wrapping at either call site. Both sites:
`lambda_function.py:54` and `:65` -- the second inside the exception handler, i.e. the path that
runs when the pool read has already failed, which is when coverage is most likely bad.

This is a disclosure of a constraint on this lane, NOT a request to loosen the producer's test.

## 2. STEP 2 -- THE CLOSURE

MEASURED, and the pure-Python half is sound by construction:

- `build_zip.py` derives its closure by AST transitive walk to a FIXED POINT from the seeded
  handler (`closure()` at `:186`), not from a hand-kept list, and `verify()` (`:284`) re-opens
  the BUILT zip and refuses it unless every in-scope import of every packaged module is present,
  MODULE AND FUNCTION SCOPE (`:285-286`). So the gold path's Python members follow the handler
  automatically once the adapter is wired. This is NOT the risk.
- The gold path's imports: `pool_reader.py:643` `import pyarrow.parquet as pq` (FUNCTION SCOPE,
  inside `_gold_latest_snapshot_rows`), `:645` `import lib.research.harvest.store`, `:694`
  `from lib.research.harvest.publication_gold import GOLD_DAILY_TABLE`.

THE RISK IS THE WHEEL, and it is a POLICY change as much as a dependency one:

- `build_zip.py:36` states: "Every wheel must be py3-none-any EXCEPT the one admitted compiled
  member, rpds_py for CPython 3.12 manylinux x86_64". PyArrow would be a SECOND compiled member,
  so that sentence is itself part of the step-2 change.
- SIZE -- PROXY ONLY, LABEL IT WHEREVER IT IS QUOTED. Current built artifact
  `.build/chatter-axis-producer.zip` = 669,924 bytes (MEASURED). Local pyarrow 24.0.0 unpacked
  = 84.3 MB, measured on WINDOWS CPython 3.11 on this box -- NOT the target CPython 3.12
  manylinux x86_64. The target-runtime figure is UNMEASURED.
- MEASURED AND IT CUTS THE OTHER WAY: pyarrow 24.0.0 declares NO `Requires-Dist`, so numpy is
  NOT pulled in as a declared dependency. This seat had assumed it would be; the assumption was
  wrong and is corrected here rather than carried.
- CONSEQUENT FORK, RAISED NOT DECIDED: an ~84 MB member against Lambda's 250 MB unzipped /
  50 MB direct-upload limits may not fit the "unpacked at the zip root -- never a layer" rule
  in `build_zip.py:36`. The harvest tree already carries `print-deps-layer.tf`, so a layer is a
  LOCAL POLICY choice here, not a platform limit. Candidates: a layer, S3-backed code, or a
  narrower parquet read path. NO PROPOSAL IS MADE until the real manylinux closure is measured.

## 3. STEP 3 -- THE NARROW READ GRANT, AND IT IS ONE LINE

RESOLVED BY CALLING THE BUILDER, NEVER TYPED (Rule 30):

    store.HARVEST_BUCKET                                  -> opal-data-harvest
    GOLD_DAILY_TABLE                                      -> chatter_daily
    store.table_prefix("amgt", "gold", GOLD_DAILY_TABLE)  -> amgt/harvest/gold/chatter_daily/

`store.table_prefix` (`lib/research/harvest/store.py:161-165`) derives from `naming.key()` and
cuts the final segment -- its own docstring says "it is never typed". So this prefix IS builder
output and Rule 30 is satisfied BY CONSTRUCTION, not by assertion.

READ SCOPE THE GOLD PATH NEEDS: `s3://opal-data-harvest/amgt/harvest/gold/chatter_daily/*`,
with `s3:ListBucket` (the `list_objects_v2` paginator at `pool_reader.py:652`) and
`s3:GetObject` (the single parquet read).

THE CHANGE IS MINIMAL AND NON-WIDENING. `chatter-axis-schedule.tf` locals currently hold EIGHT
prefixes in `chatter_axis_pool_prefixes` (4 pool: publication-links/v1/, publications/v1/,
crosswalk/v1/, universe/v1/; 4 publication silver: barrons/, wsj/, ft/, seeking-alpha/, added by
AMGT-rk-82 under its own never-widen pair). BOTH IAM statements are comprehensions over that ONE
list -- `s3:GetObject` on `${bucket.arn}/${p}*`, and `s3:ListBucket` on the bucket ARN with
`StringLike s3:prefix = ${p}*`. So appending ONE prefix yields BOTH grants at the correct
narrowness, adds no statement, introduces no wildcard, and PRESERVES every existing legacy and
silver prefix -- which is exactly the packet's "preserve existing legacy/silver permissions
during an explicit retirement window".

STILL NOT THIS SEAT'S TO DECIDE: whether the grant lands BEFORE the source default flips (a
grant for a path nothing reads yet) or as part of the cutover. Either way the never-widen pair
precedes any cutover and CVO boundary review follows it.

## 4. STILL UNMEASURED -- named, not guessed

- The real CPython 3.12 manylinux x86_64 closure and its byte size (the figure in section 2 is
  a Windows proxy).
- Whether the built artifact stays inside the Lambda limits with pyarrow at the zip root.
- The Linux-runtime exercise of both packaged entry paths the packet requires, including the
  incomplete / absent / error input arms.
- Whether `_gold_latest_snapshot_rows` needs `s3:ListBucket` on a WIDER prefix than the table
  prefix to paginate (it lists with `Prefix=` the table prefix, so it should not -- UNVERIFIED
  against a live call, and no live call was made).

## 5. ADDENDUM -- option (d), the runtime census, and one item closed

Added after ruling records 24896 / 24902. `1.0.0_SA_CTO~Z` ruled the egress ask NOT CARDED,
because the options list was missing a fourth: **(d) measure a permitted artifact this estate
already owns**, which needs no sovereign word. The estate-wide search for that artifact belongs
to `4.0.0_SA_CRO~Z`. Only the half inside THIS lane's own directory is recorded here.

RUNTIME CENSUS, `comp-find 'runtime\s*=|compatible_runtimes' infra/aws/terraform/harvest/`
-- DENOMINATOR 5 hits across 19 files scanned:

    chatter-axis-schedule.tf:138   runtime = "python3.12"          <- the H03 target
    print-deps-layer.tf:59         compatible_runtimes = ["python3.11"]
    api-gateway.tf:73              runtime = "python3.11"
    scoped-amgt-api.tf:261         runtime = "python3.11"
    build_zip.py:97                _RUNTIME_PYTHON = "3.12"

1. THE HARVEST PRINT LAYER IS ELIMINATED as a source of target bytes, on TWO independent
   grounds: `compatible_runtimes = ["python3.11"]` cannot attach to a 3.12 function, and
   `build_print_deps_layer.py` carries ZERO pyarrow hits while stating at its line 36 that it
   "Targets python3.11 / manylinux2014_x86_64". Of the two precedents named, NEWS-TRENDING-DEPS
   3.12 plus versioned S3 code is the only live candidate, and it is outside this tree.
2. THE TOPOLOGY QUESTION IS SETTLED WITHOUT THE BYTE COUNT. A layer ships in this very
   terraform root today, so `build_zip.py:36`'s "never a layer" is CONFIRMED local policy for
   this function, not a platform limit.
3. INPUT TO THE FORK, proposed by nobody: chatter-axis is the ONLY python3.12 function in this
   root (1 of 4 declared runtimes). A layer built for H03 would be single-consumer with no
   sibling to amortise it and could not be shared with the three 3.11 functions beside it.

ITEM CLOSED from section 4 -- the paginator does NOT need a wider `s3:ListBucket` prefix.
`pool_reader.py:652-653` paginates with `Prefix=store.table_prefix(...)`, byte-for-byte the
call shape the LEGACY path uses at `:346-347`, and `pool_reader.POOL_BUCKET ==
store.HARVEST_BUCKET == opal-data-harvest` (both resolved by import). The gold prefix rides the
EXISTING bucket ARN with no new `Resource`.
⚠ STATE, precisely: this is a STRUCTURAL identity with a call shape already in the grant list.
It is NOT EXERCISED -- no live S3 call was made or authorized. Exercise it at build time.

## 6. THE REPOSITORY SIZE GATE -- R's CANDIDATE CLEARS IT BY 1.65%

Added after design record `4cf1e42b7b`, which names "exact combined function-plus-layer size
against the repository's size gate" as a remaining CloudOps item. THE GATE EXISTS and is in
this lane's own directory. `infra/aws/terraform/harvest/build_print_deps_layer.py:73`:

    UNZIPPED_CEILING_BYTES = 200 * 1024 * 1024        # 209,715,200 bytes

It REFUSES rather than warns (`:173-175`, `BLOCKED: unzipped {0} B exceeds this build's
ceiling {1} B`). Rationale at `:71-72`: the layer is one half of Lambda's 250 MB unzipped
quota, the function's archive the other -- so the 200 MiB bar is deliberately BELOW the
platform limit.

    repo precedent ceiling                209,715,200 bytes  (200.0 MiB)
    R candidate closure (2,058 members)   206,249,766 bytes  (196.7 MiB)
    HEADROOM                               +3,465,434 bytes  (+3.30 MiB)  = 1.65%
    VERDICT                                    PASSES -- barely

⚠ SCOPE: that constant is the PRINT builder's OWN ceiling, not a repo-wide gate mechanically
applied elsewhere. It binds H03 only because the design selects "the existing estate pattern".
It is the precedent bar this design opted into, not a law it is already subject to.

⛔ WHY 1.65% IS THE FINDING, NOT A REASSURANCE. The 206,249,766 figure is a METADATA closure
over an EXISTING zip's members. A newly BUILT layer need not be that size: packaging adds its
own dist-info, RECORD, directory entries, and the design retains licenses and bundled
libraries. A 3.3 MiB cushion is thin enough that a build retaining slightly more than the
measurement assumed lands on BLOCKED -- surfacing at BUILD time, after the work is done.
THE CORRECT READ IS "it fits with 1.65%, and that margin must be measured on the BUILT
artifact before anyone relies on it."

SCALE, all measured: PyArrow's own members are 131,402,620 bytes (125.3 MiB) of the candidate;
the existing print layer that set this precedent is 116.1 MiB unzipped / 39,040,327 B zipped
across 1,340 members (`print-deps-layer.tf:21`), so the candidate is ~1.7x the largest layer
this tree has shipped. That file's `:23` records its function archive at ~2.7 MB unzipped -- a
real datapoint for the half the ceiling reserves.

AGAINST THE FULL LAYER: 250,975,829 bytes is 41,260,629 bytes OVER this 200 MiB bar and would
be REFUSED outright -- so declining to attach the whole pyiceberg layer is not merely tidier.
Separately, against the PLATFORM ceiling the full layer STRADDLES THE UNIT BOUNDARY: it fits
250 MiB (262,144,000) with +11,168,171 but EXCEEDS 250 decimal MB (250,000,000) by 975,829
bytes -- under one megabyte, on a figure nobody would think to interrogate. The trimmed
closure clears BOTH readings (+55,894,234 / +43,750,234), so R's selection is robust to an
ambiguity it never has to resolve.

CORRECTION TO THIS SEAT'S OWN PROXY, now that the real figure exists: the Windows/3.11
PyArrow 24.0.0 probe read 84.3 MB; the real cp312 manylinux2014_x86_64 PyArrow 15.0.2 is
131,402,620 bytes (125.3 MiB) -- the proxy UNDERSTATED by ~47 MB (~36%), in the direction that
would have hurt. Three independent reasons it could not have been trusted (wrong platform,
wrong interpreter, and nine major versions apart), where only two were known when it was
labelled.

## 7. PROVENANCE

`measured` at HEAD `f234d4122d` on SITEZ unless a line says PROXY or UNMEASURED. Instruments:
`git show` at the candidate pin `ac4316c447`, `comp-read --enumerate` with printed denominators,
`sed` at cited lines, and a local Python call into `store`/`publication_gold` for the prefix
(import only -- no S3 client constructed, no network, no credentials). Push state: LOCAL.
