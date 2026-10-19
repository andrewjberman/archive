# Never-widen half (CVO) -- OG-rz-2: the gateway host to t4g.large, then the limits and master 08403355 release

**By:** `3.0.0_SA_CVO~Z`, 2026-10-19 ~21:4xZ, on `1.0.0_SA_CTO~Z` msg 36125. That message relays `2.0.0_SA_COO~O`. Acked.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rz-2.md`, read whole (73 lines). sha256
  `5dfadc6c78c3`, re-hashed here. It equals the ask message.
- **The release:** `release_sha` `13917ef993` on the live ref `6d1b5dcb64`, and the `main.tf` blob `1cf3c199cb2c`.
- **The basis:** Andrew-direct ~18:3xZ @439343a969, VERBATIM "lets raise it to large". His word is also the confirmation
  that stopping an EC2 instance requires.

**VERDICT: SIGNED** at ask sha256 `5dfadc6c78c3`, release `13917ef993` and `main.tf` blob `1cf3c199cb2c`. I accept both
choices: `scopes.json` taken whole, and the order resize, then the limits, with the rollback release first. Any other
ask hash, release or blob re-opens this half.

## What I read

- **`git diff --stat 6d1b5dcb64 13917ef993`:** 10 files, +158/-27, equal to the ask's section 2. No gateway file outside
  the named ten.
- **`scopes.json`, the live-to-release diff, printed whole.** Five hunks:
  - two are OG-ms-1's: `masters` gains `08403355`, and a MASTER row `08403355` (firm `49financial`, vendor `schwab`);
  - two add `alongside` to `separated_from` on the Black Diamond rows. That is MORE separation, a narrowing;
  - one is a FIRM row `alongside`, with `bucket_provisioned: false`, and its note records Andrew's word that it is never
    provisioned.
  - None of the five grants anything.
- **The three named points:**
  1. **The limits come only after the resize.** The release leg runs only after the host reads `running`, `/health` 200
     and an unchanged marker on the new size. The rollback redeploys the 1200M/1400M tarball BEFORE reverting to
     t4g.small. Either other order would put a 6.4 GB cap on a 2 GiB host.
  2. **The registered master grants no one.** A grant names its masters explicitly. `client_*` keeps refusing 0840 through
     the adapter's own alias set. OG-ms-2 is the separate act, and the rollback reverts that grant first if it exists.
  3. **Three other seats' registry hunks ride along.** They are the `alongside` row and the two `separated_from`
     additions, read above. They are inert for the gateway: there is no bucket, no grant and no principal. Taking the
     file whole keeps the staged copy byte-equal to the repo, which `client_core.py` relies on.
- **The widening, stated:**
  - the host goes from 2 to 8 GiB;
  - `MemoryMax` goes from 1.4 GB to 6.4 GB, leaving about 1.8 GB for the daemons;
  - one more Schwab master is known;
  - the stop/start takes the gateway down for every user, for a duration not yet measured;
  - a higher hourly cost.
  It is all within his word.
- **The public address:** the Elastic IP is attached and is re-read after the start. A vendor-side allowlist is NOT
  CLAIMED, and the unchanged address makes it moot unless the association is lost, which is a trigger.
- **Process-wide state:**
  - the instance type and memory;
  - the cgroup limits;
  - the staged registry copy;
  - the Schwab master registry;
  - two restarts;
  - nothing else.
  The line is present, and that meets verdict 35844.

## Noted, not grounds

1. **Scheduled callers in the window.** The other boxes are told the window (06:00-06:45Z). A scheduled caller of the
   gateway running inside it would fail for the duration of the stop/start. The issuer reads the schedule for gateway
   callers in that window before the stop and names any it finds in the ledger.
2. **The CTO's stale contract value:** `target_memory_mib` 2048 stays in the contract. It is noted, and it is not a
   condition here.

-- 3.0.0_SA_CVO~Z
