# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-40 (round-42 eighth batched release: the loopback probe listener)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the ask's sections 1-8 plus CT1-CT4**, 2026-10-18 ~09:2xZ.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-40.md`, sha256
  `723cf849a41a27dcaacc39856b85ea8f696eb72dbecea703b5bec3211ee61ee1` (re-hashed at signing);
- release `3b94a83e0572f9a14851c2f229ca4aba64c7e670` on live `aa2efa2cf3dee82030c00f85425f686132adcf4a`;
- `harvest_research.py` blob `574959b682d4a13a0a429c45fa00b77b6caa2ab5`.

## What I measured myself

- `git log -1 3b94a83e05`: its parent is `aa2efa2cf3`, the live ref.
- `git diff --stat aa2efa2cf3 3b94a83e05`: 3 files, +843/-3 (`probe_listener.py` new, `server.py`, `tests/test_og_pr1.py`), which
  equals section 1.
- The `harvest_research.py` blob at the release is `574959b682...`, so it is carried.
- `server.py`: the only change is the import and the `lifespan` hookup (start the listener and the heap signal, stop it in a
  `finally`). No route or middleware moves.
- `probe_listener.py` is byte-equal to trunk's blob. Its constants are `PROBE_HOST = "127.0.0.1"`, `PROBE_PORT = 8099`,
  `LEASE_MAX = 60 min`, and `PROBE_TOOLS` lists exactly `etfs_compare_peers` and `client_get_transactions`. An unreadable lease
  fails closed.

## Against my round-41 ruling (`ROUND_ANALYSIS.round41.md` UPDATE)

Every element is present:
- a SEPARATE listener on 127.0.0.1, measured unreachable from the private address and in no target group;
- OFF by default, armed by an SSM lease of at most 60 minutes that expires closed;
- exactly the two tools;
- a fixed server-held principal with the audit label `probe:<order>`;
- one test account; other accounts are refused 403;
- the heap read on the service PID by SIGUSR2;
- OG-sec-1 read CLEAN before the cut, 0 of 18. The 2 config-sourced JWKS fetches are row Z-S384 and are not caller-controlled.

## Accepted, with the disclosures read whole

- **The guard-chain bypass (item 2) is the design, not a defect.** The probe measures heap and memory behaviour on the service PID,
  not entitlement. Entitlement stays proven by the MCP path.
- **The Opal-domain probe principal (item 3)** is bounded by the lease and the loopback binding. Any future change that admits on the
  Opal domain alone must exclude `opal-gateway-probe@opalinvest.com`; row Z-W146-S3 carries that as a standing observation.
- **The instance role (item 8)** was read by simulation only. The first real read is Phase B's armed call, and a denied read fails
  closed as `probe_not_armed`, so the worst case is an inert listener.
- **Rollback is the aa2efa2cf3 tree** (139/139 md5 walk, tarball sha256 recorded), plus deleting the lease.

## Conditions of this half

- **CT1 (blob at Phase B):** the host md5 of `app/harvest_research.py` is printed beside `596c299597067fe5a8afb8e3493a0ed9`. A mismatch
  is a rollback.
- **CT2 (base):** a live marker other than aa2efa2cf3 at Phase B is a STOP and a re-cut.
- **CT3 (heap ceiling during the probes):** after the `etfs_compare_peers` call and after each window page, the service VmRSS is
  printed.
  - If it exceeds 1200 MB (the unit's MemoryHigh) at any read, the chain stops at once, the lease is deleted, and the result is
    recorded as a FAIL of the probe, not of the release.
  - Z-S375 disarms only on a call with the service PID unchanged, NRestarts 0, and the before and after VmRSS printed.
- **CT4 (Z-S338's bound):** the window chain closes Z-S338 only if the first page is under 15 s and the median per-page heap growth
  is under 20 MB (round-41 cell 1's bound, set before the run). If it misses, Z-S338 stays open with the numbers. The bound is never
  re-read after the fact.
- **Carried:**
  - the lease parameter is DELETED and read absent before the ledger closes;
  - a 200 from `/probe/` with no lease is a rollback trigger (section 6);
  - the chrony and `systemctl --failed` read precedes the close;
  - the 82 inline audit sites (Z-W147-S1) are a round-43 candidate.
