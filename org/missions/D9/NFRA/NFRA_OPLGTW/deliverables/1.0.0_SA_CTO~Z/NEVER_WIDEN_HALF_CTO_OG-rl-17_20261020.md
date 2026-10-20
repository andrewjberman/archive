# Never-widen half (CTO) -- OG-rl-17, batch16: client fences, size caps, the in-flight guard (SIGNED, condition C1)

By: `1.0.0_SA_CTO~Z`, 2026-10-20 ~12:0xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-17.md`, sha256 prefix `19ebfcf0543f`. This seat recomputed it,
and it is equal.
Release: `ce99b7463b` on the live ref `13917ef993`.
Window: 2026-10-21 06:00Z-06:45Z.
COO half: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-rl-17_20261020.md` (L1-L5).

## Read by this seat

- **`git diff --stat 13917ef993 ce99b7463b`:** 26 files, +1969 -75. This equals the ask's section 1.
- **`app/inflight_guard.py`, read whole:**
  - one process-wide semaphore;
  - `MAX_INFLIGHT = 4`, `QUEUE_WAIT_S = 20.0`;
  - a refusal returns `gateway_busy`;
  - counters for peak and refused;
  - the configuration is constants only.
- **The widening (ask section 3) is accepted as stated.**
  - The `client_*` tools answer for orion, eclipse and commonwealth, only for principals already entitled to the client
    surface (master_admin today, v3.14), and per vendor and firm pair.
  - The Cottonwood false zero ends.
  - Replies are smaller, `news_for_security` answers by name, and `index_pairs` is on the owner route.
  - There are no tool, env, IAM or unit changes. The `admin_people_access` pair is inert.

## Condition C1 -- the in-flight limit is set from measured traffic, not chosen

`MAX_INFLIGHT = 4` is a single process-wide bound across every user and every agent seat on every box, most of which sign in
as one identity. Its trade-offs:
- A slow tool holds a slot for its whole run (`schwab_get_access` measured over 120 s in the audit).
- Four slow calls make every other caller wait 20 s and then be refused.
- That is the "timing out on other devices" Andrew asked about (2026-10-19 ~18:2xZ), turned into a refusal.
- No measured concurrency figure backs the number 4.

**C1, before the GO:** the applier measures the peak number of concurrent tool calls from the audit lake over the 24 h to
06:00Z on 10-21. Overlap is computed per call, from its start and end times. The result is recorded in the ledger. Then:
- **If the peak is 3 or fewer:** the release goes as signed.
- **If the peak is 4 or more:** the release does NOT go at 4. The constant is re-cut to at least 2x the measured peak (8 GiB
  holds it), and all three halves re-sign on the new bytes.

**Read-back addition:** the guard's `peak` and `refused` counters are printed at the end of the 30-minute read-back, with
`gateway_busy` audit rows counted. One `gateway_busy` row in production traffic during the read-back is a trigger to report,
not to roll back.

## SIGNED

Signed on C1 and the COO half's L1-L5. Any change to the ask's bytes or to `release_sha` re-opens this half.
