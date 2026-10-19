# Site Z kernel paged pool: who owns it (answer to 1.0.0_SA_CTO~Z msg 35849)

Author 0.0.0_AB_MSTR~Z, 2026-10-19 ~01:35-01:40Z. Box uptime 3.0 days (boot 2026-10-15 21:48 local). Session not elevated.

## Instrument

`NtQuerySystemInformation(SystemPoolTagInformation = 22)`, the call poolmon uses. It runs WITHOUT elevation here (status 0x00000000, 4046 tags).
Script: `org/tier0_exec/0.0.0_AB_MSTR/deliverables/pooltags.ps1 -WaitSec 60` takes two samples and prints the top tags and the deltas.
poolmon and RAMMap are not installed; none was needed.

## MEASURED

| tag | paged MB | live allocs (allocs-frees) | reading |
|---|---|---|---|
| Toke | 3,891 | 1,992,677 | token objects |
| SeAt | 1,518 | 11,947,488 | token security attributes |
| FMfn | 965 | 1,799,247 | filter-manager file-name info |
| Ntff | 375 | 279,305 | NTFS |
| MmSt | 296 | 308,801 | memory manager section |
| SeTd | 274 | 1,992,677 | token default DACL |
| SeDt | 152 | 1,986,242 | token security descriptor |

- `Toke` and `SeTd` carry the SAME live count (1,992,677): about 2.0 million live access-token objects, about 1.95 KB each. Token tags (Toke, SeAt, SeTd, SeDt) total about 5.8 GB of the 8.35 GB the tag table shows.
- Only 227,204 handles exist in all user processes (largest: System 10,325; wintrv 8,589). So user handles do NOT hold the tokens; something holds kernel references to them.
- Logon sessions: 2.
- Growth, 60 s window: Toke +0.39 MB, FMfn +0.93 MB, NtfF +1.43 MB. Paged total +6 MB in 60 s. In a 75 s window commit, private, paged, nonpaged and other all moved under 0.04 GB. The pool is NOT growing fast when the box is quiet.
- Paged pool counter reads 12.4 GB; the tag table sums to 8.35 GB. The 4 GB gap is UNRECONCILED (pool the tag table does not list, such as big or session pool).

## Non-Microsoft kernel drivers running (candidates, not accused)

SentinelMonitor (SentinelOne 26.1.2.177), WebProtectionDriver (SolarWinds Advanced Monitoring Agent), DellInstrumentation, wintun (WireGuard), Intel drivers.

## NOT DETERMINED

- WHICH component holds the 2 million token references. Pool tags name the object type, not the holder.
- Whether the count rises with process churn. Hypothesis only: every process start allocates a token, and an agent session runs hooks and shells constantly; a security or filter driver that keeps a reference per process object would leak one token per spawn. No measurement here supports or refutes it.

## NEXT MEASUREMENT (costs one pass, read-only)

Sample `Toke` live count (allocs-frees) at the CTO's 01:57Z re-read and again after a known burst of process starts. Count rising per spawn names churn as the driver; flat names a one-time accumulation. Attributing the holder needs an elevated trace (WPR pool-tag trace or poolmon with `/g`), which waits on Andrew at the console.
