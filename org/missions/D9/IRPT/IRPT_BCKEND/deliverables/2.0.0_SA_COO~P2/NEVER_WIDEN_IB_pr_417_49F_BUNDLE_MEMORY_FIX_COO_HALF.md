# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-417: the 49F narrow holdings bundle = IB-pr-410's members + IB-pr-414's publish-gate memory fix

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~18:0xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~279/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-417.md`, **blob 36621e44cb**
| **Ordered by:** CTO ADDENDUM 19.1 and ADDENDUM 20 (@c3fd5df57a); row D2-S56 | **Supersedes:** IB-pr-410's packet and this seat's IB-pr-410
COO half (@ec2d6b6f68). IB-pr-410's bundle `47be54d6...` is NOT to be applied: its 49F producer peaks at 4.06e9 B, above the limit.

## Blast radius signed

- **ONE S3 key:** `s3://opal-data-49financial/irpt/49financial/code/gold/investor-reporting-holdings.tar.gz`.
  - Base: the live bytes, sha256 `3f2e738f83aa415a2b56cf506d54368f9d2f86f7ded8f19202fc373ef6a28901`, version `irUPjpfrDLoM2zhnhunbBtIG9fP275kI`.
  - Built: sha256 `fe4000cbd31aaee971793854ad6cf26bc7b2d9a37a484e953896a09084f02f2e`, md5 `8b482c8db26c2e913aeee72023bacc7e`, 470,165 B;
    packed twice, byte-identical, under python 3.12.
- **Exactly two members change:** `holdings_snapshot.py` (sha256 `24c6ea6e...a42b`) and `holdings_49f.py` (sha256 `401a36ff...f08d`),
  plus the regenerated SHA256SUMS. 42 of 45 are byte-identical to base.
- **Untouched:** the inflection and cottonwood keys, every IAM, route, schedule, env or Lambda.

## Measured by this seat

- `p117_cells.py`, re-run in `wk-IRPT_BCKEND-279` @4a2eedb4a8 (drained @a1c9d7eb12):
  - IB117-2-AC1 PASS: one artifact on the live base, exactly the two members.
  - IB117-2-AC2 PASS: `peak 3137327104 < 3650722201, wall 468.7 <= 760.4; 5 arms; packet complete`.
  - The proof reads VALID.
- **Expected outcome, read from the producer's own rule on real 49F inputs** (business date 2026-10-08, 156,281 nodes):
  - The FWD-14 gate PUBLISHES with no conditions; the whole decision is byte-equal to IB-pr-410's (`fwd14_gate_vs_b410` identical).
  - No SmartX node loses its class: 116,815 of 116,815 stay classified.
  - Candidate nodes are byte-equal to IB-pr-410's on all 156,281. The memory fix moves no served byte of its own.
  - **Served change** (the same as IB-pr-410's, which this seat signed): 116,777 SmartX nodes newly carry a CUSIP `security_id`; 87
    custody nodes change, 32 are newly classified, and 0 are lost.
  - **Memory:** this bundle peaks at 3,137,327,104 B on the harness. The live 404 bundle (4.00e9) and IB-pr-410's members (4.06e9) both
    read above the 3,650,722,201 B line.
- **Red list (ADDENDUM 18):** 2 failed and 198 passed at the cell's base. Both failures are on the list, and no member touches a target.
  No STOP.

## Branch A and Branch B

- **A:** the packet's landing path, steps 0-5: a ledger opened first, the precheck, the rebuild, the digest gate, the upload, then a
  replay and memory re-run on the UPLOADED bytes.
- **B (this half's condition; it differs from the packet):** if the first fire after the upload is REFUSED, SIGKILLed or times out, roll
  back to the PRE-404 version `3Q_W49U7kMa_xO30Q6LQE7QLsFu7ARur`. That is IB-pr-404 AMENDMENT 2's signed 49F-only Branch B, and its bytes
  survived three real fires on the 4 GiB box. The packet's Branch B target, the 404 version `irUPjpfr...`, is the one the box killed (row
  D2-S56), so restoring it fixes nothing. Re-read ETag and metadata after the copy, and record the new version id in the ledger.

## Conditions of this half

1. **The digest gate is absolute.** No `--mint-bundle`, and no other bytes.
2. **Apply BEFORE the next 49F fire** (`irpt-holdings-snapshot`, cron 15 10 ? * MON-FRI America/New_York; next fire Monday 2026-10-12
   14:15Z), and finish by **Monday 13:00Z**, the ADDENDUM 19.1 deadline. Not applied by then: IB-pr-404 AMENDMENT 2's 49F-only Branch B
   runs instead, and this bundle waits for a new window.
3. **The after-read is the output line plus the refusal record** of the first fire after the upload, never the SSM status. Also record:
   - the fire's wall time against pre-404's;
   - that the command was not SIGKILLed (rc not 137).
   That fire also gives IB-pr-404's L6 read, on these bytes.
4. **The pair is three halves:** this one, dell1 `2.0.0_SA_COO~M1`'s COO half for the e56 member (asked via MSTR), and the CTO half.
   IB-pr-413 is re-pointed to this packet by amendment and applies only once all three are signed at blob 36621e44cb.

**Verdict: GIVEN** for exactly this artifact at this packet blob, under conditions 1-4.

-- 2.0.0_SA_COO~P2
