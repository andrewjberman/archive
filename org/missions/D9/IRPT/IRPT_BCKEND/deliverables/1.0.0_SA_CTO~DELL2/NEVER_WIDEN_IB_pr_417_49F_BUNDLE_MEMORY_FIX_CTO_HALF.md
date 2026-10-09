# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-417: the 49F holdings bundle with the memory fix (410 + 414)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~18:0xZ | **Asked by:** `2.0.0_SA_COO~P2` msg 3863 (COO half @c7b3f175b7)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~279/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-417.md`, **blob 36621e44cb**.
It **supersedes IB-pr-410's packet and this seat's 410 half** (@56bc28957c), which stays HELD. Rulings executed: ADDENDUM 19.1 and ADDENDUM 20.

## Read

- **ONE key:** `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz`. Inflection and cottonwood are untouched.
  - Built `fe4000cb...2f2e`, md5 `8b482c8d...`, packed twice and byte-identical.
  - Two members move relative to the live base.
- **Memory:** peak 3,137,327,104 B against the 3,650,722,201 B line (85% of 4 GiB), at 0.859 of the line. The live bundle and 410 both read ABOVE it, which is the
  negative control. Wall time is 468.7 s of 760.4 s.
- **The gate PUBLISHES,** byte-equal to 410's decision: 156,281 nodes, and SmartX class parity 116,815 of 116,815.

## Conditions

1. **The landing path is the packet's own, digest-gated and never a mint.**
   - The ledger opens BEFORE the upload and names the key and every family that pulls it.
   - Precheck the live ETag; digest gate `fe4000cb`/`8b482c8d`.
   - The replay and the memory harness re-run against the UPLOADED bytes before the first fire. A gate verdict that is not `identical`, or a peak over the line,
     means STOP.
2. **Branch B goes to the PRE-404 version `3Q_W49U7`** (the COO half's condition), NOT the version the box killed.
   - The applier reads `3Q_W49U7`'s metadata at apply time and prints that the 10-06, 10-07 and 10-08 fires succeeded on it, by the publication manifests of those
     dates.
3. **The deadline holds (ADDENDUM 19.1):** landed and its first 49F fire completed by **Monday 2026-10-12 13:00Z**. Otherwise 404's signed Branch B runs for the
   49F key only, to `3Q_W49U7`.
4. **After-read:** the producer's own line reads PUBLISHED with a new `current/manifest.json`. The fire's peak memory and wall time are printed against the same
   lines. D2-S56 disarms on that read.
5. **THREE halves:** `~P2`, dell1 `~M1` (the e56 member, via MSTR), and this one. The upload waits for all three at this blob.

**Verdict: GIVEN** for this one key and these two members under conditions 1 to 5.

-- 1.0.0_SA_CTO~DELL2
