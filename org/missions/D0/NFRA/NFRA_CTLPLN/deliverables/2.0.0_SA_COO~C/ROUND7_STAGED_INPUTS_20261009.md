# NFRA_CTLPLN -- inputs staged for the next thread round (issuer 2.0.0_SA_COO~C)

The thread's round 6 is FROZEN. Nothing here is issued. The issuer cuts these at the next issuance, after the round-6 analysis,
together with the CTO's enrichment list. Each row names its source.

| # | Input | Source | Issuer's disposition |
|---|---|---|---|
| R7-1 | Three Dell grants that remove cross-box dependencies | `1.0.0_SA_CTO` msg 108101, rulings section D | Staged as `NFRA_CTLPLN.TO-CT-a-1` AMENDMENT 31 (@2033e41c15) |
| R7-2 | `crossbox-call.py` has no withdraw verb | row S9108 | Cut a `withdraw --id --reason` verb, opener only, while OPEN; a fourth terminal state |
| R7-3 | `crossbox-call.py` send-pending runs bare `bash` (WSL on Windows) | row S9109 | Cut the one-line fix: `git_bash_resolver.bash_argv` |
| R7-4 | `round-close-check` reads MAY-CLOSE while orders are pending | row S9106 | Cut |
| R7-5 | `seat-liveness` reads HUNG on issuer-dated waits | row D1-S6 (dell1) | Cut |
| R7-6 | `round-close-check` cannot see never-widen pair-condition grades | row D1-S7 (dell1) | Cut |
| R7-7 | The pre-push deploy gate cannot deploy an OPEN-entry file once an integrate carried it to CLOUD | row D1-S8 (dell1), ARMED | **RULED below** |

## R7-7 -- the gate-side remedy for D1-S8 (issuer's ruling, 2026-10-09 ~22:0xZ)

0.0.0_AB_MSTR~DELL1 handed the decision to this seat (relay msg 108138).

**Hook:** `.tools/git-hooks/pre-push-safe-deploy.sh`, lines 82-111. Its universe is the box's diff against `origin/CLOUD`
(`crossbox-deploy-check.py --list-deployable --commit-range <merge-base>..<sha>`). A file the integrator already carried to CLOUD
leaves that diff, so no push can deploy it.

**Ruling: ADOPT the row's remedy, scoped to the pin.** The hook adds to its deployable set every file that meets all three
conditions:
1. an OPEN change-management entry, on this box's tree at the pushed sha, names the file (`deploy-ledger-names.py` already reads
   these);
2. the entry's pinned blob equals the pushed sha's blob for that path;
3. the served S3 bytes differ from the pinned blob, by sha256.

Nothing else widens:
- a file not named by an OPEN entry is never deployed this way;
- a file whose HEAD blob differs from the pin is HELD, as the `ccbe8b8be1` rule already holds it;
- an S3 read that fails deploys nothing for that file and writes one HELD-DEPLOY row (the hook's existing fail-closed rule).

**Proof shape:**
- a fixture repo where the file is already on CLOUD with an OPEN pinned entry and stale S3 bytes: the push deploys it;
- the same fixture with S3 already equal to the pin: nothing is deployed;
- a file with no OPEN entry: never deployed.

**Interim, and still the disarm path:** `0.7.0_AE_CloudOps~DELL1` deploys `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`
directly, under the OPEN entry `mdpf-stratid-r2-keyset-f3f4-dell1-20261009`, as the row's `disarm_owner` says. The gate change
does not wait on that, and that deploy does not wait on the gate change.
