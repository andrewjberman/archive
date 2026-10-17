# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-38 (round-41 sixth batched release: the Z-S375 repair)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the ask's sections 1-8 plus CT1**, 2026-10-17 ~22:1xZ.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-38.md`, sha256
`33686c0a63cbb9a882c88c575e6e30488aa77be73e3e2ae8567f9ff30cd14dc8` (re-hashed at signing). Release `d077cef04333500595a7a531ebddc2f43e5f8789` on
live `efcc8ae19f`.

## What I measured myself

`git diff --stat efcc8ae19f d077cef043` = 5 files, +621/-39, which equals section 1:
- `typed_scope.py`, `etfs_rivals_flow.py` and `deploy/opal-gateway.service`;
- 2 tests.

No IAM, Terraform, catalog, env or tool-list change.

## Accepted

- **One release, one ask, each change with its own stated widening.** That is what "each under its own never-widen" meant in
  msg 35540. Two deploys are not required.
- **The runaway call is repaired:** live MemoryError against candidate 475.5 MB / 4.48 s, an empty section with the available
  periods and axes, and a valid pair of 57 rows.
- **The unit ceiling:** MemoryHigh 1200M, MemoryMax 1400M, OOMScoreAdjust 300. The gateway becomes the preferred OOM victim ahead of
  every system daemon, which is the point of Z-S375's second half.
- **The chain limb** is graded by amendment A2's rule, fixed before the five runs: median of medians 11.4 MB. The first run's 21.5 MB
  is named and not dropped.
- **Rollback is the efcc8ae19f tree**, proven by the 139/139 md5 walk. The marker discipline carries.

## Condition of this half

- **CT1 -- the twelve `read_parquet` callers, before deploy.** This release changes the behaviour of every `typed_scope.read_parquet`
  caller (12 call sites in 8 modules), toward refusal. Phase A adds one run: the 27-tool read in a fresh process under the hard
  guard, against BOTH the live code and the candidate, with one call per tool and the same arguments.
  - **PASS** needs all of the following:
    - `etfs_compare_peers` answers on the candidate;
    - every other tool's candidate answer equals its live answer on row count and canonical sha256;
    - or, where it differs, the candidate refuses with `TypedOverCap` only where the live call also failed or exceeded the 64 MB
      footer cap. Each such case is listed by tool and argument.
  - A tool that answered on live and refuses on the candidate is a STOP, not a deploy. That would be a narrowing of a served answer
    that this ask does not state.
- **Carried:** Z-S338 closes only on an organic window call. The chrony and systemctl --failed read precedes the ledger close, as the
  ask's step 5 states.
