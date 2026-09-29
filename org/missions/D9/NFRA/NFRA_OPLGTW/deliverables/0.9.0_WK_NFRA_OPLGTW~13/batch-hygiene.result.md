# OG-h-1 batch hygiene -- result (0.9.0_WK_NFRA_OPLGTW~13)

Per item: the row it answers and what a reader should now see.

## A -- eol rules (row W2-S8), landed under amendment A1 @fd841cd02b
`.gitattributes` gains one block: `infra/aws/ec2/opal-gateway/**/*.<ext> text eol=lf` for the seven extensions `service txt yaml json md html jsonl`
(gateway tree only, a two-line comment naming W2-S8), then the one exception line `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml -text`.
Nothing was renormalized. Domain: 41 tracked gateway files; 40 read `eol: lf`, none of them stored CRLF; the exception reads `text: unset`.
`git status --short` shows no change to DATA_CATALOG.yaml. Its shipped bytes do NOT change: it stays stored CRLF, as it has always shipped, until
MDPF_CANON's remediation renormalizes it. The first attempt (rule plus renormalize) was refused by the naming limb (row Z-W13-S5); that row's
hazard is disarmed by this commit. Reader sees: `hy.AC1` PASS -- 40 outside the exception at eol=lf, exception -text=yes, 0 stored CRLF outside it.

## B -- out-of-repo citations (row S43)
`OUT_OF_REPO_CITATIONS.md`: 36 citing lines in 12 files, one register row per line; 35 `ABSENT-ON-SITE-Z`, 1 `DURABLE` (the inherited
`QUALIFIED_VERSIONS.json`, matched by its three VersionIds). 64 lines in 19 files citing transient `C:/tmp/wk-*` and `C:/tmp/og-*` paths were
excluded. The notes under the table say why the SSM reseal parameters are not counted as the same content as the lost salt and answers, and
why the OG-c-2 source map is not durable (its sha256 matches none of the 1305 committed versions of the repo map). No completed order, result or proof was touched.

## C -- suite writes a tracked file (row W3-S2)
`tests/conftest.py` already pointed `AUDIT_PATH` at a private temp file before any `app` import (added earlier, OG-d-1). The gap against
the order was that it overwrote an `AUDIT_PATH` the environment already set. It now takes the environment value when present and a temp file otherwise.
Reader sees: `hy.AC2` runs with `AUDIT_PATH` unset and 0 tracked files modified.

## D -- process-wide fake clock (row W3-S6)
`tests/test_ratelimit.py`: the module-level `rl.time.monotonic = ...` is replaced by an autouse fixture using `monkeypatch.setattr`, restored after each
test; the module's assertions are unchanged, and the `__main__` smoke installs the clock itself. Control: the pre-fix module copied beside
`test_ogq1_ac02` and run in one process was killed by the 60 s timeout (rc 124); the repaired module then `test_ogq1_ac02` passes.

## E -- two nondeterministic tests (row W6-S9)
- `tests/test_schwab_engine.py::test_ogq1_ac02`: the constant `child_lag < 0.25` and `loop_lag > 4 * child_lag` are replaced by `loop_lag > 1.0` and
  `child_lag < loop_lag / 2`: the child arm is judged against the in-loop arm, so load that lengthens both arms no longer fails it, and a job that
  blocks the loop still does (its lag reaches the busy time, about 1.5 s). The 0.446 s child lag measured under load passes at that ratio.
- `tests/test_schwab_export.py::test_ogx1_ac01`: the `?`, `amazonaws`, `s3`, `x-amz` and `presign` checks read the URL with its fragment removed;
  the `startswith(BASE_URL + DOWNLOAD_PAGE_PATH + "#")` check is kept on the full URL.

## F -- card (row W2-S6)
`CARD_W2-S6_PROBE_FIXTURES.md`: 8 probe items of 203 scanned (195 others, count only) and the delete command per key. Nothing was deleted.

## Proof
`hy.AC1`, `hy.AC2` (two runs of the four modules, 52 tests each), `hy.AC3`: see the proof instance.
