# Never-widen half (CTO), R2 -- OG-rl-17 batch16 re-cut at MAX_INFLIGHT 26 (SIGNED; C1 MET)

By: `1.0.0_SA_CTO~Z`, 2026-10-20 ~14:0xZ.
Against: the re-cut ask `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-17.md`, sha256 prefix `291ffc35747a`. This seat
recomputed it, and it is equal.
Release: `8e3eddf959` on the unchanged live ref `13917ef993`.
COO half R2: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-rl-17_R2_20261020.md` @313a8c11d4.
Supersedes this seat's R1 half `NEVER_WIDEN_HALF_CTO_OG-rl-17_20261020.md` (@d3ef53b352).

## Read by this seat

`git diff --stat ce99b7463b 8e3eddf959` changes 2 files, +2 -2:
- `app/inflight_guard.py`: `MAX_INFLIGHT = 4` becomes `MAX_INFLIGHT = 26`;
- `tests/test_og_mg3.py`: one matching line.

Nothing else differs from the R1 bytes this seat signed. The R1 reading of the other 26 files stands unchanged.

## C1: MET

The measured lower bound on concurrent calls is 13: thirteen calls ended in the same second (`rl17_c1_peak.json`, ruling msg
36195). 26 is twice that bound. The size caps in the same release bound each call's memory.

## SIGNED

The read-back prints the guard's `peak` and `refused` counters. A `refused` above 0 in the first 24 h is reported and ruled; it
is not an automatic rollback.
