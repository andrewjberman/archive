# NFRA_MCPINDEX.TO-MX-s-2 -- the Black Diamond cusip bridge

Seat `0.4.0_DS_ClientPlatform~D`, worktree `/c/tmp/mx-s2-d`, branch `wk-mcpindex-s2-d`, cut at `e470835e7c`.
Source row `NFRA_MCPINDEX-Z-C-S13`; ruling R-2 of `ledger/ROUND_ANALYSIS.round1.md`; Andrew option 4.

**Headline: the remedy as ruled would not have worked, and the real cause is one level further up.**
`build_bd_assets_dim.py`'s only input is frozen on the same day the bridge is, because the nightly Black
Diamond download has failed **69 consecutive runs since 2026-06-23** on a portal login timeout -- while
reporting `Status: Success, ResponseCode: 0` every night. **All three criteria FAIL. Nothing was scheduled,
nothing served was rewritten, and no sign-off was consumed.**

---

## 1. WHAT R-2 (2) ASSUMES, AND WHAT IS ACTUALLY THERE

R-2 (2) says: *"Schedule build_bd_assets_dim.py ahead of the daily merge, as a production schedule."*
The order restates it as *"No scheduler runs its builder."* Measured, live, read-only:

| claim | measured |
|---|---|
| the bridge is stale | TRUE -- `silver/bd_assets_dim.parquet` LastModified **2026-04-14T20:44:16Z** |
| no scheduler runs the builder | TRUE for `build_bd_assets_dim.py` itself |
| **(unstated)** the builder's INPUT is current | **FALSE** -- `silver/bd_assets.parquet`, its only input, LastModified **2026-04-14T20:09:23Z**, 35 minutes BEFORE the bridge, `trade_date` range ending 2026-04-13 |
| **(unstated)** no schedule exists for the leg | **FALSE** -- `bd-asset-dim-pipeline-trigger` is **ENABLED**, `cron(10 22 ? * MON-FRI *)`, and fired last night |

**The decisive number.** 791 distinct `asset_id`s appear in silver transactions since 2026-04-14 and are
absent from the bridge. Of those 791, the number present in the builder's source today is **0**.
`silver/bd_assets.parquet` and `silver/bd_assets_dim.parquet` hold **the same 10,937 asset_ids**.

So scheduling the builder, exactly as ruled, would read a frozen source, write a bridge with the same
10,937 rows, move `LastModified`, and resolve **0 of 791** missing assets. **It would satisfy AC1's second
limb while fixing nothing** -- AC1 asks only that the file was written after the order's issue.

## 2. THE REAL CAUSE, at the bottom of the chain

The chain is `BD portal -> forwardfill_v2/assets (xlsx) -> convert_assets_to_silver.py -> silver/assets/{date}
-> silver/bd_assets.parquet -> build_bd_assets_dim.py -> silver/bd_assets_dim.parquet`.

`bd-asset-dim-pipeline-trigger` (ENABLED, weekdays 22:10Z) invokes `bd-asset-dim-trigger`, which starts EC2
`i-0e6f6dc014fdcf1cd` and sends SSM document `opal-bd-asset-dim-download`. The lambda succeeds and **does not
wait for or check the result**. The SSM command's own output, read for the 2026-09-25 run:

```
Phase 1: Login
FAILED
Error: TimeoutError: forURL: Timeout 30000ms exceeded.
waiting for navigation to "**/bd3.bdreporting.com/**" until "load"
Download exit code: 1
SKIP: silver conversion skipped (download_rc=1)
ERROR: Asset-dim pipeline failed (download_rc=1 merge_rc=99)
```

**And SSM reports `Status: Success`, `ResponseCode: 0` for that same invocation.** The wrapper exits 0 on a
failed pipeline, so every instrument above it reads healthy. That is why this survived 95 days.

**Bounded from the daily logs, which have been in S3 the whole time.** All 119 of
`s3://opal-data-bd/logs/asset-dim-download-*.log` read in full:

| | count |
|---|---|
| logs read (denominator) | **119** |
| FAILED | **69** |
| of which the SAME login `TimeoutError` | **69 of 69** -- one signature, one cause, not 69 |
| OK | 50 |
| unclassifiable | 0 |
| last OK | **2026-06-22** |
| first FAILED | **2026-06-23** |
| last FAILED | **2026-09-25** |

`silver/assets/` stops at 2026-06-18 and `forwardfill_v2/assets/` at
`AssetDimTXNs_OpalCapital_Daily_2026-06-18_to_2026-06-18.xlsx`, both consistent. Meanwhile
`forwardfill_v2/transactions/` is current to **2026-09-26** -- the transactions leg is alive; only the
asset-dim leg is dead. And the compaction to `bd_assets.parquet` had already stopped earlier, at 2026-04-14,
while `silver/assets/` was still being written through 06-18 -- so there are **two sequential breaks**, not one.

## 3. THE SERVED FIGURE

Probe `probes/mx_s_2.py`. Latest partition `gold/timeseries/holdings_lots/2026-09-18.parquet`:

```
DENOMINATOR: 1,264,679 rows
  null cusip (incl. literal CASH) : 22,173
  of which cash by the substitute : 15,185
  NON-CASH null cusip             :  6,988   <- AC3 counts this
  ... of those, blank asset_name  :     98
VERDICT: FAIL-MXS2-AC3
```

**AC3's rule is not computable as written, and the probe says so rather than pretending.** B_01's cash rule
keys on `asset_id == 4` (`B_01.holdings_lots.py:284-292`), and **the served partition carries no `asset_id`
column at all**. The probe substitutes a stated `asset_name` token rule, prints the tokens, and prints the 98
rows it cannot classify either way.

**AC3's bar of zero is unreachable by construction.** The bridge itself carries **1,037 of 10,937 asset_ids
with no cusip at all** -- BD supplies none. No rebuild, however current, gives those a cusip.

**How much a re-run could actually fix, bounded rather than asserted.** Of the 6,988 non-cash nulls, **1,798
carry a ticker today's bridge could resolve** and **5,190 do not**. The 1,798 is an **upper bound**: B_01
joins on `asset_id`, not ticker, and the two keys can disagree, so a ticker hit is evidence the asset is in
the bridge, not that B_01's join would resolve it. I did **not** measure that a re-run changes nothing --
I measured that at most 1,798 of 6,988 rows could move, for reasons unrelated to the frozen bridge.

## 4. WHAT I DID NOT DO, AND WHY

**No schedule created.** Two reasons, either sufficient. (a) CLAUDE.md rule 13 gives PROD triggers to DT/AE,
and the order itself says not to work around the lane gate. (b) Scheduling the builder resolves 0 of 791
while its input is frozen -- it would be a fix in name only, and AC1 would certify it. The spec DT/AE needs
is in section 5.

**No served rewrite, and no sign-off consumed.** `SIGNOFF_REQUEST_bd_cusip.md` is written as the order
requires, with the blast radius and the rollback per key -- and it **recommends the halves NOT be signed
yet**, because a rewrite against today's frozen bridge cannot reach AC3, could move at most 1,798 of 6,988
rows, and would spend a never-widen sign-off on an act whose benefit is unmeasured. The order's STOP is
honored: nothing served moved.

**No NEVER-2 ledger entry opened.** The entry exists to bound a deploy; no deploy occurred. AC2 therefore
reads `entry files at HEAD=0 ... RESULT: FAIL`, which is the honest state, not an omission.

**No alarm, monitor or notification built** (standing moratorium), including for the 69-night silent failure.
It is filed as a row with an owner.

## 5. THE SCHEDULE SPEC -- for the DT/AE apply

The useful act is **not** a new trigger for the builder. In order:

1. **Fix the BD portal login** on `opal-bd-asset-dim-download` (EC2 `i-0e6f6dc014fdcf1cd`). Until this lands,
   every step below is a no-op. Owner AE/CloudOps; if it needs a credential or a vendor interaction, that is
   Andrew's word, not mine. **This is the whole fix.**
2. **Make the wrapper's exit code tell the truth.** It currently returns 0 on `download_rc=1 merge_rc=99`, so
   SSM reports Success. A non-zero exit is not an alarm -- it is a producer reporting its own result honestly.
3. **Restore the compaction to `silver/bd_assets.parquet`**, which stopped at 2026-04-14 even while
   `silver/assets/` was still landing. `convert_assets_to_silver.py` writes it unless `--no-compacted` is
   passed; check what the SSM document passes.
4. **Only then** add the builder to the chain, after the compaction and before the silver merge that consumes
   the bridge. Name from `lib/opal_naming.py name()` containing `assets-dim` (note: the existing rule is
   `bd-asset-**dim**-pipeline-trigger`, singular, which is why AC1's `assets-dim` substring test reads
   ENABLED=0 against a live rule). A production schedule, never an alarm.

Step 4 alone -- the literal reading of R-2 (2) -- fixes nothing. Steps 1-3 are the remedy.

## 6. CRITERIA

| AC | verdict | why |
|---|---|---|
| AC1 | **FAIL** (exit=1) | `schedules/rules named *assets-dim* ENABLED=0; bd_assets_dim.parquet LastModified=2026-04-14T20:44:16+00:00 after issue=no`. Not created: out of lane (rule 13) and a no-op while the input is frozen. |
| AC2 | **FAIL** (exit=1) | `entry files at HEAD=0; sentinel at HEAD=no; listed OPEN/HELD=0; SCAN DENOMINATOR: 12 of 12 sentinel(s) scanned`. No deploy occurred, so no ledger entry exists to close. |
| AC3 | **FAIL** | 6,988 non-cash null-cusip rows of 1,264,679. Its zero bar is unreachable by construction (1,037 bridge assets have no cusip), and its cash rule is not computable from the served artifact (no `asset_id` column). |

No criterion was widened, repaired, or met by a route the face does not name.

## 7. ROWS FILED

| row | class / hazard | what |
|---|---|---|
| `Z-S8` | BLOCKING / ARMED | the BD asset-dim download has failed 69 consecutive runs since 2026-06-23 on one login timeout; this is the root cause of C-S13 and R-2 (2) does not reach it |
| `Z-S9` | OBSERVATION / ARMED | the SSM wrapper exits 0 on a failed pipeline, so SSM reports `Success` -- why 95 days of failure were invisible |
| `Z-S10` | OBSERVATION / ARMED | AC3's zero bar is unreachable and its cash rule is not computable from the artifact it names |

(The ids are `Z-S8..Z-S10`, not `Z-S7..Z-S9`: a peer appended a row to the shared channel while this order
was running, and the append recomputed the next free `k` from the file rather than assuming it.)

**Attribution note, stated rather than left to look like mine.** These three rows are at CLOUD HEAD --
3 of 3 verified present, with a negative control on a non-existent id -- but they were carried in by
`2.0.0_SA_COO~O`'s commit `8fc747bc09`, not by a commit of mine. That seat committed the shared tree while
my append sat uncommitted in it, so its commit swept up my rows alongside its own `Z-S7`. The rows landed
correctly and the row gate graded them; only the authorship is not what the log implies. This is the
shared-index race CLAUDE.md 14b names as the cost of NOT isolating an append-only channel -- the cost was
paid as designed, and it is cheaper than the guaranteed conflict isolation would have caused. Recorded, not
adjudicated.

## 8. COMPILER TOOLS

| tool | result |
|---|---|
| `comp-schedule` | the order's preflight says RUN AT THE ACT. **No act was taken**, so it was not run; the schedule this order contemplated was never created. Recorded rather than silently skipped. |
| `comp-find` | used for the writer census of `bd_assets.parquet` -- 68 hits / 75,160 files, **N=1 writer** (`convert_assets_to_silver.py`), which is what showed the input was frozen by a single dead producer. |
| `comp-pipescript io` | not run for `build_bd_assets_dim.py`: the same gap recorded under MX-s-1 -- the `data/assets` and BD asset-dim trees resolve in no indexed pipeline. |
| live AWS reads | EventBridge rules, lambda logs, SSM `get_command_invocation` (by exact CommandId, as a positive control after `list_commands` returned a bare 0), S3 heads and full-corpus log reads with printed denominators. |
