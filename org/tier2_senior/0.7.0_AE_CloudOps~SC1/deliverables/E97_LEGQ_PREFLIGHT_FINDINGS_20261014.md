# TO-SC-e97b leg Q -- preflight findings and the one decision needed (0.7.0_AE_CloudOps~SC1, 2026-10-14 ~06:15Z)

Written for a reader with zero prior context. GO msg 5440 (05:57:19Z) asks this seat to run C_06 ALONE once on
unchanged inputs after the 04:00:46Z chain has stopped (amendment 2, ruling XA-20261014T054803Z-7d27). Nothing
has been run and nothing has been written: leg Q is NOT opened in the ledger. The order's own step 2 says to
STOP and report if the runner has no single-step path for C_06. A single-step path exists, but two facts about
reaching it change what the run would prove. Each is marked MEASURED (read from a file or a live call) or
INFERRED (reasoned from measured facts).

## Finding 1 -- a plain `--single C_06` writes the LEGACY bucket, not the served canonical home (MEASURED)

`data/black_diamond/scripts/gold/gold_dispatch.sh` lines 1084-1093 (the FB-f-9 PLATINUM-MODE block) export
`BD_PLATINUM_MODE=canonical` ONLY when `MODE=chain`, not a dry run, not a QA invocation, and the variable is
unset. For `--single` the variable stays unset, and `lib/platinum_dest.py` reads unset as `legacy`.
The FB-f-9 proof for this block (`ADVI_FIRMBKTS.TO-FB-g-15` AC1, 12 cases) records it: `PASS single -> 'UNSET'`.

So `bash gold_dispatch.sh --single C_06` as-is would READ and WRITE the opal-data-bd legacy keys
(`gold/entities/clients/`, `gold/views/mix_daily_summary.json`, `platinum/firm/mix_summary.json`), which since
2026-10-12 06:18Z are stale copies, not the served objects. The order's BEFORE and AFTER lists name the
canonical (`opal-data-49financial`) keys. Result if run as-is: those lists would read DELTA=0 because the run
never touched them, and the QA would have tested a different state (the stale legacy one). That is a pass that
proves nothing, and it would also overwrite legacy keys another reader may still use.

The same block ACCEPTS `BD_PLATINUM_MODE=canonical` preset on a non-QA single run (case `mode already set to
canonical -> canonical`) and REFUSES it on a QA run (`GOLD_KEEP_ALIVE=1` or the `/tmp/GOLD_QA_REBUILD` marker),
so the QA runner `i-0090b823a4a0997e3` cannot be used: it can never write the served home.

## Finding 2 -- the production runner has no "up but idle" state: booting it runs a chain (INFERRED from measured facts)

Measured: `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh` is "executed on every boot by systemd" and
ends in `shutdown -h now`; it runs `run_gold_layer.sh incremental`, which delegates to
`gold_dispatch.sh --chain full` (freshness-gated). The `2026-04-08` AE log records `systemctl enable
gold-layer-runner`. Measured today: the launches at 09:46:59Z (10-13) and 12:45:16Z (10-13) each ran S_00, A_00
and A_02 telemetry only and stopped about ten minutes later. I did not read the unit state on the instance
(the runner is up until its chain ends, and I made no SSM call to it).

Inferred: starting the instance to get a place to run C_06 starts that same boot chain. With silver unchanged
it behaves like the two launches above (S_00, A_00, A_02, then the gate) and then shuts the instance down.
Consequences for "C_06 alone on unchanged inputs":
- the boot chain's A_00 rewrites or no-ops `gold/dimensions/accounts_dimension_latest.parquet`, which C_06 reads
  (MEASURED: `comp-pipescript io C_06` lists `ACCOUNTS_DIMENSION <- A_00`); if A_00 rewrites it the inputs are
  not unchanged and a non-zero delta would be ambiguous;
- the dispatcher defers its auto-shutdown to the LAST chain-bearing process (`SHUTDOWN_DEFERRED`), so an SSM
  `--single C_06` sent while the boot chain is still running would take over the shutdown; sent after the
  boot chain has ended, the instance is already halting.

## The decision (one ask)

Authorize this sequence for leg Q, or name another:
1. After the 04:00:46Z chain has stopped, take the BEFORE lists as the order says, and ALSO record the ETag and
   VersionId of `gold/dimensions/accounts_dimension_latest.parquet` (opal-data-bd), so an input change by the boot chain is visible.
2. Start the runner; let the boot chain run; when its A_02 step has finished (read from its log, not assumed),
   send ONE SSM command that pulls `gold_dispatch.sh` from S3 and runs
   `BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --single C_06` (script from S3, no inline code, per
   rule 12). Shutdown stays on, so the single's own end halts the instance.
3. Take the AFTER lists; report DELTA, the accounts-dimension before/after, and the `C06-ROLLING-REDERIVE`
   line; if any ETag differs, restore by BEFORE VersionId as the order says.

What I will NOT do without your word: start the runner (it launches a production chain), set
`BD_PLATINUM_MODE` by hand, or send anything to the instance. The finish line stays before the 23:00Z fire;
a decision by about 20:00Z leaves room. Nothing written, nothing to restore.

## Finding 3 (added ~06:35Z, after amendment 3 / msg 5445) -- the authorized sequence cannot hold the instance up (MEASURED)

Nothing has been started. The runner is still on the 04:00:46Z chain. Reading the boot path for the sequence
amendment 3 authorizes:

- `code/runner/run-gold-layer.sh` as SERVED (ETag `12ad546fdda541a40e86b1e382f02bbc`, 2026-05-13, equal to the repo
  copy) ends with `shutdown -h now` unless `GOLD_KEEP_ALIVE=1`. That line runs seconds after
  `run_gold_layer.sh` returns (a log upload and a pending-marker check sit between). It is not the
  dispatcher's `shutdown -h +2`, which `sudo shutdown -c` could cancel; and it ignores the dispatcher's
  "last chain-bearing process arms" deferral.
- The 10-13 no-work boot launches measure the whole chain at about 3 minutes (09:46:59Z launch; S_00 09:47:35 to
  09:49:49; A_00 and A_02 09:49:54 to 09:49:58; EC2 gone by the next CloudWatch bucket). C_06's last runs took 186 s
  and 353 s. A single sent while the boot chain runs is killed by that `shutdown -h now`, mid-write on served keys;
  a single sent after the boot chain ends finds a halting instance (amendment 3 (f) is that case).
- `GOLD_KEEP_ALIVE=1` is not a way out: `gold_dispatch.sh:1085-1089` REFUSES `BD_PLATINUM_MODE=canonical` when it is
  set, by design.

So no sequence made of "start the runner, then one SSM command" can run C_06 to completion on the production
runner. Options, each outside the one-SSM-command bound and so needing your word:

A. As the FIRST SSM command, as soon as the agent is online, `sudo systemctl stop gold-layer-runner`. It kills the
   boot wrapper (the shutdown line never runs) and, if S_00 has started, S_00 with it; S_00 is silver-prep and
   reruns on every launch, but I cannot rule out a partial write from being killed mid-run. The instance then
   stays up (the watchdog needs 10 minutes of uptime and 5 minutes of no gold process), and the second SSM command
   is the authorized `BD_PLATINUM_MODE=canonical bash /tmp/gold_dispatch.sh --single C_06`. The single's own end
   arms `shutdown -h +2`. Side effect that helps the test: A_00 does not run, so the accounts dimension cannot move.
B. Do not run leg Q on the production runner, and disarm D1-W83-S5 on other evidence (the issuer's and the CTO's
   call; the ruling named this run as the instrument).
