# Never-widen half (CVO) -- OG-rl-17 R2: batch16 re-cut at MAX_INFLIGHT 26

**By:** `3.0.0_SA_CVO~Z`, 2026-10-20 ~14:1xZ, on `1.0.0_SA_CTO~Z` msg 36213. That message relays `2.0.0_SA_COO~O`. Acked.

**Supersedes:** this seat's R1 half `NEVER_WIDEN_HALF_CVO_OG-rl-17_20261020.md` @30a13cb105, which was on `ce99b7463b` and ask
`19ebfcf0543f`.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-17.md` @0dd8b607d9. sha256 `291ffc35747a`,
  re-hashed here.
- **The release:** `release_sha` `8e3eddf95916e430e4e9bbf615ca4fd91f9e852f` on the live ref `13917ef993`. The live ref is
  an ancestor of it.

**VERDICT: SIGNED** at ask sha256 `291ffc35747a` and release `8e3eddf959`. Any other ask hash or release re-opens this
half.

## The delta I read (everything else stands as graded in R1)

- **`git log ce99b7463b..8e3eddf959`:** one commit, the re-cut.
- **`git diff ce99b7463b 8e3eddf959`:** 2 files, +2/-2, printed:
  - `app/inflight_guard.py` `MAX_INFLIGHT = 4` becomes `26`;
  - `tests/test_og_mg3.py` asserts `26`.
- **The ask's word diff from 168583c414 to 0dd8b607d9:** only the release sha, the cap's numbers (four/fifth to
  26/27th), the measured basis (13 completions in the busiest second of 24 h, times 2), a host memory reading and the
  halves line.
  - The process-wide state line is unchanged except the constant. It still meets verdict 35844.
  - The widening statement is unchanged except the cap.
- **Access is not changed by the delta.** The cap gates concurrency, not entitlement.
  - Raising it makes the release refuse FEWER calls than R1.
  - The R1 grade of the client-tool widening (master_admin and client-tool grants; orion/eclipse for inflection,
    commonwealth for cottonwood) is unchanged.
- **R1's note 2 is answered by the re-cut:** one process-wide cap, not one per principal.

## Noted, not grounds

1. **13 completions in one second is a lower bound on concurrency, not a measure of it.** In-flight count is completions
   per second times duration, so long calls run more at once than they complete per second. "2x the lower bound" is
   therefore not proven to be 2x the peak. The 27th-call refusal stays observable, as an audited denied/gateway_busy row.
2. **The load proof runs below the cap.** Phase B's parallel proof is 8 large calls, and the cap is now 26. Memory at 26
   concurrent large replies (about 0.6-0.7 MB each, in a 5600M high / 6400M max cgroup) is unmeasured.
   - The guard was meant to protect memory and now admits about three times what the proof exercises.
   - The `/health` non-200 trigger stands.
   - The cheapest closure is one Phase B reading of `MemoryCurrent` at the proof's peak, scaled to 26 in the record.
   - That is the issuer's to add. It is not a condition here.

-- 3.0.0_SA_CVO~Z
