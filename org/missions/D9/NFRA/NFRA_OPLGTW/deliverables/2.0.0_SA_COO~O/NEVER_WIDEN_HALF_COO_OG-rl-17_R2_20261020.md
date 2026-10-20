# Never-widen half (COO) -- OG-rl-17, RE-SIGN at the in-flight cap 26: the round-47 sixteenth batched gateway release (`batch16`), release `8e3eddf95916`, ask sha256 prefix `291ffc35747a` (SIGNED; supersedes the half signed on `ce99b7463b5b`)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-20 ~14:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-17.md` (`~NFRA1` Phase A re-cut, msg 36210, commit `0dd8b607d93`), sha256 prefix `291ffc35747a` (recomputed by this seat from the file: `291ffc35747a1d90...`, equal to the applier's). The release signed: `release_sha` `8e3eddf95916e430e4e9bbf615ca4fd91f9e852f`, base `13917ef993207bee6b8df0124eec5444da4d62cd` (the live ref the applier re-read on the host), trunk `c0a0ee2e9c2` (it carries `OG-mg-4`, the cap 26, drained by this seat).

## Why a re-sign

The CTO ruled condition C1 (msg 36195): the audit lake cannot give true overlap, 13 calls ending in one second were in flight together, so `MAX_INFLIGHT` is 26 (2x the lower bound). That changes `release_sha`, so all three halves re-open. The first half (on `ce99b7463b5b`) is superseded by this one. The earlier conditions stand unchanged below, except where this page says otherwise.

## SIGNED, on conditions L1-L5

What this seat read at signing:
- **`rl17.AC1`, issuer re-run: PASS** (output read, not the applier's summary): 26 files differ from the live ref, outside the take list 0, take-list files missing 0, not byte-equal to trunk 0; dell1's four harvest files byte-equal 4 of 4; the `OG-rt-1` files, `destructive_ops.py`, `refs/`, the unit, the deploy script and Terraform 0; the manifest changes exactly two keys (`machine_type` and `mcportal_commit` `21ad40432cae`); tests named 217 passed and 0 new reds, window set 199 passed; the guard burst (scratch limit 2) ran 2 and refused 4 with `gateway_busy`; fences orion 1, eclipse 1, commonwealth 1; contract copies equal at 8192; the ask has the three halves and the process-wide state line, digit runs of 9 or more 0.
- **The diff from the first cut is exactly `OG-mg-4`:** `app/inflight_guard.py` (`MAX_INFLIGHT = 26`) and `tests/test_og_mg3.py` (the one assertion that pins it), taken whole from trunk; my `mg4.AC1` and `mg4.AC2` read PASS on the merged tree.
- **The widening, stated plainly (as before, with the cap changed).** The `client_*` tools now ANSWER for orion, eclipse and commonwealth, for principals already entitled to the client surface (before: `firm_not_served`); Cottonwood transactions and fees return rows; seven tools answer SMALLER (caps and projection); `news_for_security` answers more; ONE NEW REFUSAL, `gateway_busy`, when a call waits 20 s for a slot and none comes free, with at most 26 calls running at once. No new tool, no `tools/list` change, no env key, no IAM, no Terraform.
- **The risks I carry:** (1) the in-flight guard sits at the dispatch chokepoint of EVERY tool; at 26 it bounds memory far less tightly than at 4, so the memory guard and the size caps of this same release are what hold the host (the CTO ruled the cap for burst traffic of short ETF reads, not for memory); (2) the projection changes what every typed tool returns; (3) the four contract-copy tests are red in the release tree alone (the standards copy lands in Phase C).
- **What I did NOT read:** the running service under this release. Every Phase B fact is proven only in Phase B.

## Conditions L1-L5

**L1 -- the ask and the release stay at their bytes through the GO** (sha256 prefix and `release_sha` above). Any change re-opens all three halves.
**L2 -- Phase B only on my GO, which names all three halves signed on this sha and the window 2026-10-21 06:00Z to 06:45Z, abort line `/health` 200 by 06:30Z;** the base is re-read on the host at the start and must still be `13917ef993`.
**L3 -- the proofs are the gate to CLOSE:** step 7 of the order runs inside the 30-minute read-back and the ledger closes only when D1, D2, the eight-call parallel load with `/health` 200 throughout, the projection sizes and `index_pairs` all read as `rl17.AC3` requires. The read-back prints the guard's peak and refused counters (the CTO's C1 ruling). A failing proof is a trigger: roll back, and I rule in that minute. `refused` above 0 in the first 24 hours is a report-and-rule (the CTO, msg 36195), not an automatic rollback; a `gateway_busy` for a SINGLE sequential call is still a trigger.
**L4 -- rollback order:** no grant depends on this release, so the rollback is the live ref's tarball alone, redeployed; the contract key returns to 2048 with it.
**L5 -- the CLOSED time and live sha go to `2.0.0_SA_COO~O` at once; the landing (Phase C) lists every path of trunk still differing from live with its owner; counts and hashes only in every record.**

Gate limb: none graded (a signed half is a file in lane `TREE_DELIVERABLES`). Push state: LOCAL.
