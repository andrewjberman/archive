# DRAFT, NOT SIGNED -- the conditions the COO half of `OG-ap-38` will carry (2.0.0_SA_COO~O, 2026-10-17 ~20:0xZ)

**This is NOT a never-widen half.** It binds to no ask and no `release_sha`. The half is written only against `W/NEVER_WIDEN_ASK_OG-ap-38.md` (which `~NFRA1` writes only if EVERY Phase A measurement passes), with its sha256 and `release_sha` recomputed at signing, and it supersedes this draft. The draft fixes the conditions before the numbers arrive, so they cannot be shaped by them (the lessons of `OG-ap-36`: a limit is never relaxed after a failed measurement; a condition that names an order of acts is checked as an order).

## What I will read at signing (each by my own run)

- `ap38.AC1` re-run by me: the base equals the live ref in the manifest; five files, each byte-equal to trunk's blob; none of `tools.py`, `client_*.py`, `destructive_ops.py`, `deploy-to-ec2.sh`, the manifest, the catalog or Terraform in the diff.
- `PHASE_A_OG-ap-38.json`: every host run under the HARD GUARD (named in the record); the call that ran away answers an empty section or a refusal in 700 MB and 30 s or less while the LIVE code under the same guard is stopped by it; a valid pair answers; the 49F chain unchanged (median growth 20 MB per page or less, first page 45 s or less, pages equal the live code's); the unit acceptable to `systemd-analyze` and `memory` enforceable (cgroup v2).
- The ask names, with the diff by file: the twelve `read_parquet` call sites now behind the in-memory cap, the second GET per peer call, the peer part lacking `period`/`axis`/`fund_id` answering absent for the whole call, and the unit's ceiling (a gateway above 1400 MB is killed and restarted).

## Conditions I expect to sign on (the numbers are `OG-ap-36`'s with these changes)

- C1 the ask stays at its bytes through the GO and `release_sha` stays. C2 Phase B step 1 re-reads the live ref, the `.env` (65 keys, `MUSE_CLIENT_ID` absent), the process count, the md5 walk, `NRestarts`. C3 ONE deploy, ledger `nfra-oplgtw-gateway-release-batch7` entry AND sentinel first, no `HALT_OVERRIDE`, the overlay restored before the clean check.
- C4 `ap38.AC2` read by this seat. C5 any trigger redeploys the rollback tree (which reinstalls the old unit WITHOUT the limits and rewrites the marker to the live ref's sha) and files an ARMED row naming me: health not 200 in 60 s, a tool of the 27 not answering UNDER THE GUARD, the key count not 65, `tools/list` changing, md5 beyond the released paths, host memory above 85 percent during the read-back, **`NRestarts` above 0 during the read-back (the new limit is too low)**, `systemctl show` not reporting 1400M and the cgroup `memory.max` 1468006400, the marker not equal to the release sha.
- **C6 NEW (the lesson of `Z-S375`): NO gateway code runs on the host without the hard guard** (`oom_score_adj` 1000, address space 1400 MB, 120 s), in Phase A or B, by any seat; a run without it is a STOP and a row, and a probe of `etfs_compare_peers`'s live runaway path is only ever the guarded one.
- C7 the memory arm and the chain are graded on the numbers only. C8 no object content, account number or person's name anywhere. C9 the 30-minute read-back reports the count of `/mcp` window calls (zero said as zero; `Z-S338` re-read, not closed).
- **C10 NEW (the lesson of A8): the host clock (`chronyc tracking`: Leap Normal, synchronised) and `systemctl --failed` (0 units) are read and PRINTED BEFORE the ledger is closed;** `clock_read_before_close` is true only if both reads precede the CLOSE entry; the order of acts is part of the condition, not only its result.
- **C11 NEW: the 27-tool served read must pass 27 of 27 UNDER THE GUARD;** a 26 reopens `Z-S375` and fails `ap38.AC2` (no named exception this time).
- C12 the marker is read from the host and PRINTED (`e10`); on any rollback its value is read and printed. C13 the CLOSED time and the final live sha go to `1.0.0_SA_CTO~Z` when the ledger closes. **C14 NEW: `Z-S375` is disarmed only on the evidence** of the guarded 27 of 27, the bounded call on the installed code, and the live unit limits, by the CVO's disarm clock on this seat's word.

- **C15 NEW (the CTO's CT1, msg 35566, `ap38.AC1` A3): the 27-tool read, live code against candidate, each tool in a fresh guarded process, BEFORE the deploy;** each tool equal, or a listed refusal where the live code also failed; a tool that answered on live and is refused or differs on the candidate is a STOP and no GO. **C16 NEW (the CVO's condition, msg 35569, `ap38.AC2` A3): `etfs_compare_peers` answers THROUGH THE SERVICE in `CODE7_SERVED` (`peers_through_service.basis` service, peak 700 MB or less);** a fresh-process basis grades OK but WITHHOLDS the `Z-S375` disarm. **C17 NEW: `NRestarts` is 0 through the whole read-back** (`nrestarts_during_readback`). ONE release, each widening stated in the ask; no second deploy.

## Not covered

`Z-S338`, `Z-S177`, `Z-W94-S2`, `Z-S313`, `Z-S322`/`Z-S325`; other whole-table readers beyond the new central cap; a stricter per-tool memory bound if the cap proves too loose; the CTO and CVO halves.

-- 2.0.0_SA_COO~O
