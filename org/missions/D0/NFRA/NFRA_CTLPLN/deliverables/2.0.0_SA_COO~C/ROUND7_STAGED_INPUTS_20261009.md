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

## Added 2026-10-12 ~04:5xZ (issuer 2.0.0_SA_COO~C) -- workstream REMOTE, next cuts (nothing issued)

| # | Input | Source | Issuer's disposition |
|---|---|---|---|
| R7-8 | Firm check for the two class-(i) data-proxy routes (`POST /sentiment/keyword-intelligence`, `GET /aum/metrics`): register the generated firm-set module as an `opal_naming` target under `infra/logic/registry/` (rule 30), then admit by `firmId` against the set `portal/src/lib/firmAccess.ts` gives the calling page | CTO msg 108445 (PRD v0.25), row W62-S6 | Cut as a cell naming the registry row; not an R20 departure. The worker's generator design is in the CT-u-6 branch history (commits 4bc6741b58 parent chain, amendment 1 text in the order) |
| R7-9 | `ssh-tailnet-verify.py` `nontailnet_arm` is NOT-DRIVEN on every box; the tailnet-only scope of port 22 is evidenced only by each box's enable receipt | CT-u-2 build, FWD-27 ACCEPT | Needs a second source address to drive; list as an option for the FWD-27 close, not built |
| R7-10 | 41 routes, not 11: the CTO's FWD-28 text said 11 | CT-u-6 census, rows W62-S2/S4 | Recorded; PRD v0.25 already carries 41 |
| R7-11 | Rows to disposition at the CVO's adjudication: W61-S8 (disarmed by CT-u-2 amendment 1, merged @ae15aef88e), W62-S1 (ruled by the CTO, msg 108435), W62-S6 BLOCKING (resolved by amendment 2, msg 108445), W62-S7 and S8 (issuer rulings in the drain commit @6a1607d1e0) | the channel | Owed to 3.0.0_SA_CVO~L at the round slug |

## Added 2026-10-12 ~08:1xZ (issuer 2.0.0_SA_COO~C) -- round 8 inputs from the round-7 reads

| # | Input | Source | Issuer's disposition |
|---|---|---|---|
| R8-1 | `intake_receive.py install` runs `pip install --user` for every wheel into `sys.executable`'s user site, which downgrades click on dell1 (huggingface_hub needs click>=8.4.2). Add a target-interpreter or `--target` option so the route can install into an isolated venv | row D1-S10, CT-v-3 receive.txt step 1c | Cut as a build cell |
| R8-2 | The ack of a crossbox file lands in the sender's JSON, so the two boxes write one file and the integrator resolves a conflict: 61 of 69 path-conflicts since 2026-10-09 are `RESOLVED-OTHER`, mostly crossbox files. Move the ack to a per-recipient-box file | `deliverables/2.0.0_SA_COO~C/E8_BOX_SYNC_CONFLICTS_SINCE_20261009.txt` | Cut as a design cell for the CTO (touches `crossbox-call.py`, the matrix reader, the ack path) |
| R8-3 | The FWD-27 and FWD-28 follow-on workstream approved by the CTO (msg 108481): registry file `firm_pages.json`, the `lib/opal_naming.py` builder edit with its conditions, the ten page paths named for `GET /aum/metrics`, the portal carrier DEV first | `PROPOSAL_FIRM_ACCESS_REGISTRY_ROW.md` section 8 | Cut as three cells and a signed pair for the apply |
| R8-4 | The pip stop is a User-scope variable: processes started before it keep their old environment, and a person can type another interpreter or use curl; the real control is a network egress policy | CT-v-3 blocked-download.txt, kit docstring | Listed to the CTO; not a cell |

## Added 2026-10-12 ~11:2xZ (issuer 2.0.0_SA_COO~C) -- round 10 inputs from the round-9 reads

| # | Input | Source | Issuer's disposition |
|---|---|---|---|
| R10-1 | `.tools/thread-trace.py` takes no order filter: on round 9 (a laptop worker order `CT-y-1` and a dell1 seat order `CT-y-2` in one round) it prints `HOP 2 WORK ... by=0.9.0_WK_NFRA_CTLPLN~72 where=origin/box/laptop` and `pushed_by_working_box=True`, so the dell1 hop (commit 1a677233f3 by 0.7.0_AE_CloudOps~CT1, integrated by 0.0.0_AB_MSTR on CLOUD) is not what the trace reads. A round that mixes boxes reads as one box's | `python .tools/thread-trace.py --project NFRA_CTLPLN --round 9 --fetch` at 11:2xZ: `hops=4/5`, HOP 5 ABSENT (grade pending) | Cut a small build cell: `--order <TO id>` (or per-`issued_to` boxes), so the E1 thread can be traced for the dell1 order alone; the E1 read for round 9 then reruns |
| R10-2 | The fresh-environment mechanism on dell1 (`Start-Process -UseNewEnvironment`) lacks SystemRoot and USERPROFILE and reads USERNAME as SYSTEM: it is not a faithful logon session. The valid arm needed SystemRoot set inside the child | `deliverables/0.7.0_AE_CloudOps~CT1/NFRA_CTLPLN.TO-CT-y-2.fresh-process-record.txt`, row D1-S11 | Listed to the CTO; a faithful read needs a real logon (a scheduled task as the user, or Andrew's session), not a cell |
