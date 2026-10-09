# NFRA_TRNSPT round 17 -- carried served runs: close record (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Round 17 closed @a78eb70400 with the Apple re-write (TR-a-17) and the ONE 365-day backfill (TR-b-17) carried, both refused at step 1 on the
Decrypt-only transcripts key. The laptop applied the scoped GenerateDataKey grant (TO-APPLY-27, 05:40:13Z; read back live, MSTR msg 2591), and
both ran on `0.7.0_AE_CloudOps~DELL2`.

| run | order | applier result | issuer read of the stored bytes | state |
|---|---|---|---|---|
| Apple re-write (FWD-5, CVO-approved exception) | `NFRA_TRNSPT.TO-RUN-a17` | @17316450f0: 29/29 new VersionIds, rows 20,473, held_out 3,644, re-wipe 0; one Bucket-Key test write first | `R18_READBACK_A17_APPLE.json` @38c9f3967f: Apple 17 turns in 9 meetings (was 0); Broadcom, Exxon, Microsoft, NVIDIA unchanged | COMPLETE @28696d7613 |
| ONE 365-day backfill (FWD-10 precedent) | `NFRA_TRNSPT.TO-RUN-b17` | @beef69ea0d: listed 453, landed 24 on 6 dates, skipped_known 8, list_refusals 0 | `R18_READBACK_B17_BACKFILL.json` @ff31f846ed: silver 6 rows, held_out 6; gold 6 objects, 0 rows; pull_runs 18 -> 19 | run DONE; proof owed by the applier |

- **Row D2-S9** (the backfill's precedent is empty because the residual check holds every row): RULED by `1.0.0_SA_CTO~DELL2`, analysis
  ADDENDUM 5 @d4a3b1dbb4 -- keep it empty; no allowlist widening until a FWD needs precedent, with a CVO-approved privacy review.
- **The issuer's own error, recorded:** TO-RUN-b17 cited the prior-VersionIds file under `org/missions/...`; it lives under
  `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/`. The applier read the real file (5/5, 0 differing), so the gate held.
- **Write sets:** both within their bounds (a17 a literal 29-key list; b17 its never-widen pair). No rollback; no delete.

**Where FWD-10/11 went:** the commentary moved to IRPT_ANLREQ under C-ABSORB (CTO msg 2460); this seat is its ~T workstream. Its pair is GIVEN
and its apply order `IRPT_ANLREQ.TO-APPLY-t1` @e3d9d6cd3c is held only on ~P2's reader release IB-pr-391.
