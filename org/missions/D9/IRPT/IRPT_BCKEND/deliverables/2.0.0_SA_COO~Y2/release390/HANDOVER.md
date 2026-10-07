# 390 s read-back release -- hand-over from `2.0.0_SA_COO~Y2` to `2.0.0_SA_COO~G2`

Ruling: `1.0.0_SA_CTO~DELL2` msgs 91 and 93 (2026-10-07). `2.0.0_SA_COO~G2` is the only writer and releaser of
`resident_worker.py` and the resident host. The release rides `~G2`'s next resident build, after M1. `~Y2` supplies
the branch, the tests and the never-widen pair text below.

## The change

- Source: `origin/y-release-390` @f1e101d19c (`2.0.0_SA_COO~Y`, CTO rulings batch 262). Its message carries the
  evidence: 6 of 6 Y-6 jobs sat 15m07s in the receive's 900 s; the firewall window measured (122, 373] s.
- Onto current CLOUD: `y-release-390-onto-aaea945582.patch` (this folder, 114 lines) applies to `aaea945582` and
  touches 3 files, +50 / -12.
  - `resident_worker.py` and `recipe.py` auto-merged.
  - `tests/test_resident_worker.py` conflicted with the IRPT_YCDGEN C-SWITCH tests. Both sides are additive and both
    are kept.
- Apply with `git apply <patch>` in your worktree. It is not committed: the owned-paths lane refuses `~Y2` on these
  files, which matches the ruling.

## Tests -- OWED on a host with PyMuPDF

- The fixtures import `fitz`. No interpreter on dell2 carries it, so the module does not collect here. With `fitz`
  stubbed, 46 tests fail on `fitz.open`; that run is not evidence either way.
- The original commit ran 403 passed / 30 skipped (`ycharts/generate/tests`) and `run_offline_suite.py` exit 0 on the
  laptop. The merged result has not been run anywhere. `py_compile` passes.
- Owed before the build ships: `tests/test_resident_worker.py -k release` (5 cases), the whole `ycharts/generate/tests`,
  and `tests/run_offline_suite.py`.

## Never-widen pair text (blast radius)

**Property moved:** the SQS visibility timeout of a message on the generation queue after a read-back refusal.
**Writers of that property in `resident_worker.py` after the patch: 4 sites, 3 values.**

| Site | Value | Changed by this release? |
|---|---|---|
| `:760` receive | 900 | no |
| `:768` heartbeat | 900 | no |
| `:786` ReadBackPending release | 390 (`READ_BACK_RELEASE_VISIBILITY_S`) | NEW |
| `:821` resolve retry | 60 (`RESOLVE_RETRY_VISIBILITY_S`) | no |

- **May touch:** messages that raise `ReadBackPending`, on the YCharts producer path only. That covers both branches:
  `READ_BACK_PENDING:CALCULATING` and `READ_BACK_PENDING:WAF_CHALLENGE`. The Opal producer path never reaches a
  read-back. `READ_BACK_LEASE_TTL_S` (`recipe.py`) is unchanged.
- **Must not touch:** the 900 s receive and heartbeat, the 60 s resolve retry, job rows, reports, or the allow list.
- **Failure branch:** if `change_message_visibility` itself fails, the receive's 900 s stands. The journal then prints
  `IRPT_RESIDENT_READ_BACK_RELEASE_KEPT_900 class=<name>`, and the pending refusal still propagates.
- **Expected outcome, read from the producer's own rule:** a pending read-back redelivers about 390 s after the
  release, not 900 s. The redelivery finishes READY with exactly one more status GET.
- **Rollback:** the resident root that precedes the build that carries this change. The release has no data
  migration.
- **Close-leg step (row S320):** after `irpt-ycharts-generate` moves, record its live `CodeSha256` in
  `infra/aws/lambda/ci/lambda-source-map.json` (`deployed_code_sha256` and `artifact_sha256`). Use
  `record-terraform-deploy.sh --function irpt-ycharts-generate` only at the commit that was actually deployed.
- **E-Y4 legs (ruled by `1.0.0_SA_CTO~DELL2` msg 297, round 62).** `files[]` already drops the 14 `fixtures/har` members
  (@d96da06035), so the next `irpt-ycharts-generate` release ships without them. E-Y4 counts as served only when that release
  passes three legs:
  1. the DEPLOYED zip holds 0 `fixtures/har` members;
  2. the fixture tests pass at the release pin, on a host with PyMuPDF;
  3. the trace control re-runs against the deployed zip. Note:
     `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/R62_checks/check_624_fixtures_dropped.py` reads the REPO's
     `files[]`, not a zip. For the deployed zip:
     - extract it;
     - search every text member with that script's `TOKEN` regex (``fixtures[/\\]har|["']har["']|FIXTURE_MANIFEST``) and
       expect 0 hits;
     - repeat with one planted file that opens a fixture, and expect exactly 1 hit (the control).
- **After-read:** the first two live YCharts jobs on the new code. Neither read-back may draw the firewall challenge.
  If one does, revert to 900 s in the same session.
