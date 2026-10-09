# Never-widen sign-off packet -- IB-pr-389 (release of IB-pr-384): the directory runner refuses a build that drops a source entry

Prepared by 0.9.0_WK_IRPT_BCKEND~200 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO msg 2507 (b)). Nothing here was uploaded, deployed, applied or written: BUILD_ONLY from a clean tree, offline replays, AWS reads only.
Files beside this packet: `IB97-2_release_census.json`, `IB97-2_release_replay.json`, `replay/replay_runner_drop.py` (the replay script). Model: `..._IB-pr-380_381.md` (~189).

**READ THIS FIRST (row IRPT_BCKEND-D2-W200-S1, OBSERVATION, INERT).** The order names the live runner bundle as version `OxaIJns0` (IB-pr-383). Read live at packet time (2026-10-09T05:1xZ) the object is already
**`W2WragrP52i8M7MfL22oXVPuHsTjyVLO`** (written 2026-10-09T04:16:44Z, 112,861 bytes, ETag `5547fa5e6601c042beef7146c0064def`), and it is **byte-identical to the bundle built at the pin**. The refuse-drop runner is therefore already in the
world, minted by an actor the repo does not name, with no signed pair. Against the live object the build has 0 changed members and Branch A is a no-op at the object. Everything below is stated against BOTH live versions.
The behaviour can only withhold a landing (replay: nothing differs while nothing is dropped, 9 of 9 arms); the issuer or the CTO decides whether the pair is still signed or closed as already applied.

## The pin and the build

- **Release pin P: `45c061c282039c892fbeedfff5583485df3800c5`** (branch `wk-IRPT_BCKEND-200`, the merge of issuance `ae687597ec` into box/dell2). The code is `c7b401e8f7` (IB-pr-384), in P through the drain `1895f16a0b`.
- **Artifact: runner bundle `investor-reporting.tar.gz`** = `irpt_runner_bundle_uri` in `infra/aws/terraform/investor-reporting/directory/schedule.tf` = `s3://opal-data-mdpf/code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz`.
  Built with the mint's own deterministic builder (`safe_deploy_core.build_bundle_payload` over bundle `investor_reporting`), from a clean tree (porcelain 0 lines before and after), twice, byte-identical:
  **built sha256 `f6d48603a6496f78733312e49b0e279b0907288db3423575f735835e896a0118`** (md5 = the ETag a verified upload must echo: `5547fa5e6601c042beef7146c0064def`, 112,861 bytes, 12 members). Nothing uploaded.
- **live_before: `W2WragrP52i8M7MfL22oXVPuHsTjyVLO`** (sha256 `f6d48603a6496f78733312e49b0e279b0907288db3423575f735835e896a0118`, equals the built bytes). The version the order named, `OxaIJns0x1vkrd924gLPTyOMGzL_KQxK` (03:42:25Z, 112,575 bytes, sha256
  `2e3e6648312f5daad1da91f0c3aaeb4736a81b16cc9bb0dd4f43e5e93886b968`, ETag `b0356a757b1ae92e3a4b46a847378315`), is the previous version.
- **Changed members.** Built versus live_before: none (0 of 12). Built versus `OxaIJns0`: ONE of 12, `data/assets/scripts/gold/investor_reporting/directory_runner.py` (built `23b7eaf6f278`, prior `08e5e1abc92a`; stamp `directory-runner-sha256`), owner commit `c7b401e8f7` (IB-pr-384).
  The `directory_runner.py` blob at P equals the live member.
- **Census of the functions the code reaches.** No Lambda zip carries `directory_runner.py` (the source map has no entry for it). The one function that triggers the runner: `release-census.py irpt-directory-refresh --pin P` -> built 5, live 5, `changed_members=0`.
  `main.tf` of the directory module changed by `c7b401e8f7` in comments only (the stale SKELETON clauses); there is nothing to apply.
- Deploy path (the applier's, DS lane, CLAUDE.md rule 13): `bash .tools/safe-deploy.sh data/assets/scripts/gold/investor_reporting/directory_runner.py` routes the member to `mint_bundle('mdpf','investor_reporting')`
  (upload with the sha stamps, head-object verifies ETag == md5 and every stamp). No Terraform change: the next SSM run fetches the object at the URI.

## What the release does

`run_firm` raises `REFUSED: BUILD_DROPS_SOURCE_ENTRY` (the opaque ids named, 0 S3 puts) before `land()` when the previous served directory holds a client that the source snapshot still holds but this build lacks, on a call that writes
(upload or local mirror). A genuine source removal still lands carried TERMINATED (IB-pr-381). Unknown source keys refuse only when a previous client is missing. A call that writes nothing (a dry run) records `carried_forward.refused` and `main()` returns 1 (row D2-W195-S1).
A refusal is an SSM command failure with no put: the served directory stays at its prior as_of, and goes OVER_AGE on the usual calendar (cottonwood 2026-10-12, inflection 2026-10-13) if refused until then.

## Writers of the changed properties

- **The bundle object** `code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz`: 1 writer in code, `mint_bundle('mdpf','investor_reporting')` via `.tools/safe_deploy_core.py` (the only reference to the key; the Terraform module only READS the URI into the SSM command's environment).
  The one observed put of the built bytes (`W2Wragr`, 04:16:44Z) is attributed to no ledger entry in the repo (row S1). N rules read: 1.
- **The served directory** `investor-reporting/directory/<as_of>/directory.json` and `latest.json` (what the runner produces): 1 writer, `directory_runner.land` (IB93-1 census, 33 of 33 live versions matched to one runner SSM command each). This release adds a rule BEFORE that writer;
  it adds no writer and no key. N writers: 1; N rules read: 1 (the refusal in `run_firm`, which precedes `land`).

## Branch A (released: the built bundle is the live bundle)

1. **Object:** nothing to upload. Live is already the built bytes. If the applier re-mints, `safe-deploy.sh` of `directory_runner.py` yields the same bytes (deterministic build) and a new version id with identical content; the ledger entry closes SUPERSEDED/already-applied.
2. **Served effect:** the next scheduled fires (09:30 and 09:40 ET) land exactly what they landed before while nothing is dropped (replay arms `real_*`: identical canonical landing at all 3 firms). A build that drops a source entry lands nothing and the served directory stays at its prior as_of.
3. **Blast radius:** no S3 key changes unless a run lands, and a run that lands writes the same two keys per firm as today. Rollback per artifact: Branch B.

## Branch B (rolled back)

- Runner bundle: copy S3 version **`OxaIJns0x1vkrd924gLPTyOMGzL_KQxK`** (ETag `b0356a757b1ae92e3a4b46a847378315`, 112,575 bytes, the IB-pr-381 runner without the refusal) back over the key, or re-mint from the commit before `c7b401e8f7`
  (`directory_runner.py` blob prefix `08e5e1abc92a`). Re-read live after a copy: ETag `b0356a75...` and `directory-runner-sha256` `08e5e1abc92a...`. The runner has no other state; the next SSM run fetches whatever the key holds.
  A rolled-back runner lands a build that drops a source entry (the replay arm `drop_*_live_prior_vs_built`): do not roll back through a window in which the build is known to drop one.
- No route, IAM, schedule, env or Terraform change to revert. No served key was written by this cell.

## The replay arm for the applier (rerun before the ledger)

Against the artifacts actually in play: extract the bundle to be uploaded (and the live version, and `OxaIJns0`) into separate empty directories, with AWS reads and a scratch directory OUTSIDE the worktree:
`python -I replay/replay_runner_drop.py run <bundle_dir> <scratch> <label> <fire date>` once per bundle (labels `built`, `live_current`, `live_prior`), then
`python -I replay/replay_runner_drop.py compose <scratch> <out.json> <pin> built live_current,live_prior`.
Recorded (`IB97-2_release_replay.json`, 18 arms = 3 firms x 3 arms x 2 live labels, 2026-10-09 fire):
- `real_*` (real source snapshot, previous = the served directory, nothing dropped): **identical** for both live labels at inflection (294 entries), cottonwood (269) and 49financial (4719): same canonical landing hash (payload without `generated_at`), held 0, carried 0.
- `drop_*` (fixture: one entry the source still holds is dropped from the build; the runner's real `land()` with boto3 swapped for a put-counting fake): the built bundle **refuses with 0 puts** at all 3 firms and names only the dropped opaque id;
  `live_current` is identical (it is the same bytes); `live_prior` (`OxaIJns0`) **lands it** (2 puts, the entry absent from the landed directory) -- verdict `expected-diff` at all 3 firms.
- `genuine_removal_*` (NEGATIVE CONTROL: the entry is gone from the build AND the source): built and both live labels **land it carried TERMINATED** (2 puts, carried 1) -- identical at all 3 firms, so the refusal does not fire on a vendor removal.
- 49financial, not replayed in IB93-1, was replayed here (the source read worked from this seat). Stop the apply if the built `drop` arm does not refuse with 0 puts, or the `genuine_removal` arm does not land.
- Delete the scratch directory afterwards.

## The after-read

The next scheduled landing at all 3 firms, read as landed: for each firm the runner's SSM command `irpt directory refresh <firm> <date>` succeeds, `latest.json` and the dated `directory.json` carry a LastModified 0-300 s after it,
the dated `directory.json`'s `carried_forward` has no `refused` key and `entry_count` equals the replay's expectation for that day. Absence of a new landing is a REFUSAL to be read from the SSM command output (`REFUSED: BUILD_DROPS_SOURCE_ENTRY`), not a stale pipeline, and its opaque ids name the dropped entry.
Ledger: open before, close after; rows to read with it: IRPT_BCKEND-D2-W200-S1.
