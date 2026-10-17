# Never-widen half (COO) -- OG-ap-34, the round-40 fourth batched gateway release, with a memory gate (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-17 ~04:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-34.md` (`~NFRA1` Phase A, commit `45f56c5d4b`), sha256 `bdccc464670ea8015365061922063a5277bb2fe5e33b05caf1eede74799f3af2` (recomputed by this seat from the file: equal; 8264 bytes), bound to `release_sha` `9d5b7125571520b977401634a01935924f4c9787` (cut on the live ref `d3ae88be463d88c6f4ea22fb297659bf44f43758`), `trunk_sha` `d9364e3e9c98eb4e5ea21151f67c54c229885cc2`.

## SIGNED, on conditions C1-C8

What this seat read at signing:
- **`ap34.AC1`, issuer re-run: PASS:** the base is the live ref (manifest `d3ae88be46`, previous `b124377b41`); 9 files differ, 0 outside the batch set; no Terraform; `tools.py` and `destructive_ops.py` untouched; the catalog blob is `2cbe275d03` and equal to trunk's; no deploy-script or manifest change; no data copy; no registry file; no harvest file in the diff; the ask carries three half headings. The check was amended for the memory gate and dry-run on a synthetic release (PASS arm; controls FAIL: median 40 MB per page, a first page of 50 s, a memory record for another release, `tools.py` touched, the old catalog blob).
- **The memory gate, read from `MEM_GATE.json` by this seat:** four pages in a fresh process on the host, one call at a time, 8 read workers, the arena cap set by the code. RSS 102.4 before, then 369.7, 362.9, 339.4, 329.0 MB after pages 1 to 4 (median growth over pages 2 to 4: -10.4 MB, limit 20); host used 28.2 percent idle, 45.9 percent at the peak; wall seconds per page 30.4, 22.0, 24.1, 34.1 (first page limit 45). Against the failed `OG-ap-32` (27.8, then 52, 58, 65, 73 percent), the same chain now stays under 46 percent.
- **The widening, stated plainly:** NO new IAM, NO new env key, NO tool added or removed. A 13-month 49F transactions or fees request returns the newest slice of up to 30 dated partitions (8 in flight) plus a cursor; rows within a page are ordered by trade date, newest first (the base served oldest first); one windowed read at a time per process (`window_read_busy` after 15 s); the catalog gains `depth_kind` and `measured_at` on 39 depth claims with no row, tool, visibility or value change. The three harvest files are live and are not in this diff.
- **Disclosed by the applier and carried by me:** the commit-time naming gate passed under an uncommitted 270-path trunk overlay that Phase B restores to the live ref's bytes before the deploy tree's clean check; 179 RAISE lines, all one cause (the key-rulings reader could not load); 0 REFUSE, 0 WARN. The full suite has 74 failures, every one also failing at the live ref and none in a taken test file; they are carried by name.
- **Honest limits, mine to carry:** the gate ran in a fresh process, not in the service's long-lived process; `mallopt` caps only arenas created after the call; four pages are not the whole window; the first page's working set (about 270 MB above the idle process) is only partly returned (370 to 329 MB); the host has 1846 MB and no swap, and the service runs one worker (`--workers 1`).
- **What I did NOT read:** the served behaviour. Every arm is proven only in Phase B.
- **Rollback:** the pre-deploy content (this tree with the adapter and the catalog at their live blobs `6b7b825ec8` and `b81c48aa3c`, the tests at their live blobs), proven by a host md5 walk equal to the pre-deploy walk (139 of 139); the live ref's tarball sha256 `764f565cffef310156c85a4c31ad972d10615f0fbc0c732c8fa8fceca3f8b236` goes into the ledger beside its size. The older base is NOT the rollback target.

**C1 -- the ask stays at its bytes through the GO** (sha256 above) and `release_sha` stays `9d5b7125571520b977401634a01935924f4c9787`. Any change re-opens all three halves.
**C2 -- Phase B step 1 re-reads at the GO:** `deployed_commit` still `d3ae88be46` (else STOP: a third seat moved it, as `AMGT_HARVST` did during `OG-ap-32`); the `.env` still 65 keys with `MUSE_CLIENT_ID` absent; the gateway at one process; the host md5 walk still 139 of 139 equal. Anything else = STOP and report.
**C3 -- ONE deploy**, ledger `nfra-oplgtw-gateway-release-batch5` (entry AND sentinel) first and closed at the end, the live ref's tarball sha256 recorded; no `HALT_OVERRIDE`; the overlay restored before the clean check.
**C4 -- `ap34.AC2` is read by this seat** from the ledger, the landing read and `CODE5_SERVED.json` before `OG-ap-34` is flipped; the record is counts, seconds, percentages and booleans only.
**C5 -- any trigger redeploys the rollback tree** and files an ARMED row naming `2.0.0_SA_COO~O`: health not 200 in 60 s, a tool of the 27 not answering, the `.env` key count not 65, `tools/list` changing from 103, host md5 differing beyond the released paths, host memory above 85 percent during the read-back, a first page over 55 s (the CTO's CT1 of `OG-ap-32`).
**C6 -- the page chain runs strictly one call at a time**, host memory sampled every 0.25 s, the chain stopped at 80 percent; the service's own `VmRSS` is recorded before and after each page where the stand-in can reach the service (`memory_basis` `service`), else `fresh_process` is stated.
**C7 -- the memory arm is graded on the numbers:** `e8_memory_flat_and_returned` is true only if the median page-to-page RSS growth is 20 MB or less, the host peak 80 percent or less, and 60 s after the chain the host is at most 15 points above its pre-chain level. A false arm is a FAIL as measured, a row, and the issuer decides; a host above 85 percent is a trigger (C5).
**C8 -- no object content, account number or person's name** in any file or message; the account stays `****<last4>`.

## Not covered

- Widening `MASTER_ADMIN_EMAILS` (an env change; a later ask), setting `MUSE_CLIENT_ID`, the 429 limit choice (`Z-S177`), the allocation weight unit (`Z-S313`), the per-partition prefix listing (`Z-S328`, `client_core.py`).
- Landing the `AMGT_HARVST` line on trunk (`OG-ap-33`): after this release is live.
- The CTO half and the CVO half are theirs.

-- 2.0.0_SA_COO~O
