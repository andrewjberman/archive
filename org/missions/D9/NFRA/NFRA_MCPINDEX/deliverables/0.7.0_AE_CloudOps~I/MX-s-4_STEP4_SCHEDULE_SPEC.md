# MX-s-4 step 4 -- the schedule spec for `build_bd_assets_dim.py`, for a LATER ask

**Author:** `0.7.0_AE_CloudOps~I`. **Order:** `NFRA_MCPINDEX.TO-MX-s-4`, step 4 -- *"Adding the builder to
the schedule is NOT this order's: report the spec (section 5, item 4) for a later ask."*
**Nothing here is applied.** This is a spec, and it is deliberately not an act.

---

## 1. THE HEADLINE: DO NOT BUILD THIS YET, AND THE SOURCE SAYS SO TOO

The DS result this spec descends from is explicit: *"The useful act is **not** a new trigger for the
builder"*, and *"Step 4 alone -- the literal reading of R-2 (2) -- fixes nothing. Steps 1-3 are the
remedy."* Adding a schedule while the input is frozen buys a reliably-scheduled no-op.

The ordering constraint is a hard one: the builder must run **after** the compaction and **before** the
silver merge that consumes the bridge. Today neither of its preconditions holds.

## 2. THE PRECONDITIONS, AND THEIR MEASURED STATE

| # | precondition | state, measured 2026-09-26 | owner |
|---|---|---|---|
| 1 | The Black Diamond login works | **NOT MET.** All three BD downloaders (asset-dim, fees, allocation) fail on the same login timeout; last clean 2026-06-22, first failing 2026-06-23, identical across all three | Andrew's word (vendor-side) |
| 2 | The wrapper exit code is honest | **CODE FIXED, NOT DEPLOYED** at `4b3a757410`; held to batch with precondition 1 | this lane |
| 3 | The compaction to `silver/bd_assets.parquet` runs | **NOT MET, and not for the stated reason** -- see row `Z-S15` | DS lane (rule 13) |

>> Precondition 3 is the one that moved. The order and the DS result both say the script *"writes the
compacted file unless `--no-compacted` is passed"*. It does not. `convert_assets_to_silver.py` has ONE
`write_compacted(df)` call, at line 279, gated at line 278 by `if args.backfill and not
args.no_compacted:`. The SSM document passes `--latest` and never `--backfill`, so the branch is
unreachable on the scheduled path. **Fixing the login does not restore the compaction**, and the remedy
is a change to a `data/*/scripts/silver/*.py` file, which CLAUDE.md rule 13 puts on the DS lane. <<

## 3. THE NAME -- BUILDER OUTPUT, NOT HAND-TYPED

CLAUDE.md rule 30 requires every resource name to be `lib/opal_naming.py name()` output, and requires
the PRD to cite that output rather than type a name. Run at authoring time:

```
name('blackdiamond', None, 'assets-dim', 'daily')      ->  blackdiamond-assets-dim-daily
name('blackdiamond', 'global', 'assets-dim', 'daily')  ->  blackdiamond-global-assets-dim-daily
```

**RECOMMENDED: `blackdiamond-assets-dim-daily`** -- scope `None`, because the asset dimension is a
shared reference table, not firm-tenanted (grammar S5: a shared resource carries no scope). The `kind`
slot takes a cadence for a SCHEDULE, per `name()`'s own docstring.

It also satisfies the DS's stated test: the name contains the substring `assets-dim`.

>> **THE LIVE RULE IS NON-CANONICAL ON THREE COUNTS, and this is why MX-s-2's AC1 read ENABLED=0
against a rule that exists.** Live: `bd-asset-dim-pipeline-trigger`. Canonical:
`blackdiamond-assets-dim-daily`.
> 1. `bd` should be `blackdiamond` (the registry's system key).
> 2. `asset-dim` should be `assets-dim` -- singular vs plural is the exact substring miss.
> 3. `pipeline-trigger` is not a cadence; a SCHEDULE's last element is one.
>
> Renaming the EXISTING trigger is **not** proposed here. Rule 30's non-application clause is explicit:
> existing pipelines reach conformance through their own migration project (R19), never as a rider. The
> mismatch is recorded so the next reader knows the substring test is measuring a naming gap, not an
> absent schedule.

## 4. THE SPEC, WHEN THE PRECONDITIONS HOLD

- **Resource:** EventBridge schedule `blackdiamond-assets-dim-daily`.
- **Position:** after the compaction step inside the existing chain, before the silver merge that reads
  the bridge. Sequenced, not parallel -- the builder consumes the compaction's output.
- **Preferred shape:** extend the EXISTING `opal-bd-asset-dim-download` SSM document with a builder step
  rather than mint a second trigger. That keeps one clock for one chain and needs no new rule at all.
  A separate schedule re-introduces the two-clocks race the single document currently avoids.
- **Trigger discipline:** a production schedule. CLAUDE.md is explicit that success-of-upstream as the
  only trigger is a defect, and equally that this must never be an alarm, a monitor or a notification
  (the standing moratorium). It is a producer running on its own clock.
- **Deploy path:** the SSM document is NOT terraform-managed -- no `aws_ssm_document` resource anywhere
  under `infra/aws/terraform/` names it, and the live document is Owner `313476888478`, Status Active,
  DocumentVersion 1, hand-created 2026-04-14. A NEW EventBridge rule, by contrast, IS Terraform and goes
  through `safe-apply`. If the preferred shape above is taken, no Terraform is involved.
- **Ledger:** a NEVER-2 deploy-completion entry, opened before the act with its blast radius and
  rollback per key, as MX-s-3's was.

## 5. WHAT THIS SPEC DOES NOT SETTLE

- Whether the Black Diamond login is repairable without a new credential, an MFA device or a vendor
  interaction. That is Andrew's word and is the gate on everything above.
- Whether the compaction fix should change the script's condition or the flags the document passes.
  DS's call, not this lane's.
- The `bd` / `blackdiamond` and `asset-dim` / `assets-dim` naming migration, which belongs to an R19
  migration project and is named here only so the substring miss is not re-derived.
