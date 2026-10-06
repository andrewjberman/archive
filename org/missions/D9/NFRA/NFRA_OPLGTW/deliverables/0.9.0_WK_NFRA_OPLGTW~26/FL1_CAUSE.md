# FL1_CAUSE -- why test_ogx2_ac01 was intermittent (OG-fl-1, row NFRA_OPLGTW-Z-W15-S58)

cause: other: a PRODUCT defect -- engine.process_rss_bytes built a new ctypes WinDLL and Structure class on every RSS poll
(reference-cycle garbage freed only by the cyclic GC), so the gateway parent's tracemalloc footprint during an export
depended on the job's duration and on GC timing; not the test's timing assumption, a shared path, or the engine deadline.

fix: commit b065029296 (engine.py: kernel32 and the counters Structure class are built ONCE and cached). Row
NFRA_OPLGTW-Z-W26-S7 is in commit 6d99c16138. A regression test (tests/test_schwab_rss_poll.py) is in the commit that
carries this file. test_ogx2_ac01 itself is UNCHANGED: same assertions, same 1.2 limit, no skip, no retry.

## What fails

The failing assertion is `assert big["parent"] <= 1.2 * small["parent"]` (the parent's tracemalloc peak during
generate_csv, 100k rows vs 10k rows). The child ratio is 1.06-1.08 on every run. No `job_failed` was reproduced in any run
(`job_failed` is only the fallback reason string in integration.export_query when a job has none); the engine deadline
(30 s) was not hit, and the files in the export directory were clean.

## Evidence

1. Reproduction. 8 sequential idle runs: 8 pass. 12 own-process runs started at once on this 20-core device: 8 pass, 4 fail,
   every failure on the parent assertion with parent ratios 1.212, 1.286, 1.255, 1.245. Failing runs had a LOWER 10k
   parent peak (0.77-0.83 MiB) than idle (0.93 MiB) and a 100k peak near 1.0 MiB.
2. Mechanism. A tracemalloc snapshot taken at the start of write_csv (after export_query returned, before one row was
   read) held 403-431 KB for a 10k export and 290-318 KB for a 100k export, of a 0.65-0.9 MiB parent peak. Its top entries
   were engine.py:885 (the per-call `_Counters` class), ctypes/__init__.py:421 and :491 (a WinDLL's function pointers)
   and ctypes/_layout.py:282. That is garbage from the poll loop (`ExecutionEngine.submit` polls every 5 ms in this test),
   not data from the export: its size is the number of polls since the last collector run, which is noise.
3. A unit probe: 600 calls of process_rss_bytes + pid_alive with the collector off grow the traced heap by 4,934,319
   bytes on the old code and by under 32 KB on the new code (tests/test_schwab_rss_poll.py: FAIL on the HEAD bytes,
   PASS on the fix).
4. After the fix. tracemalloc at the start of write_csv is 22-25 KB; the parent peak is 612-615 KB for 10k and for 100k
   in 6 of 6 probe runs; 12 own-process runs started at once: 12 pass, parent ratio 1.004 in all 12 (was 1.21-1.29 in 4 of 12).
   tests/test_schwab_engine.py: 14 passed.

## Reach

Windows branch of engine.py only (the Linux /proc branch and the psutil branch are untouched). It is a product file, so
the fix rides the next release of the gateway.
