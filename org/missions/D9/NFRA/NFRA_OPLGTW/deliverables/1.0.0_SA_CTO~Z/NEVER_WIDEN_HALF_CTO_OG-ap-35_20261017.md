# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-35 (narrow Alyssa's grant by one key: `download_filtered`)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the COO's C1-C7 plus CT1**, 2026-10-17 ~03:3xZ.
**Bound to:** ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-35.md`, sha256
`224a80d88a5248397aa5617d40a3584832828c8d7523e12a5d996a631fe88249` (re-hashed at signing). Read whole (COO~O msg 35324).
**Basis:** my ruling @aed4469fa6, upheld at XA-20261017T024251Z-a7a7, which enforces Andrew's 2026-10-08 "no downloads needed yet".

## What I accept

- **The write set:** one principal's partition, four items. The only changed key in the grant is `operations`. The two other
  principals' hashes are proven unmoved before and after. No IAM, no delete, no tombstone.
- **The side-writes were read this time, the lesson of OG-mg-1.** Section 3 names the `email_deny` re-put of her EXISTING record:
  identical tid, oid and status, so there is no browser change. C7 requires the before and after hashes to be equal.
- **The usage census meets the XA condition (1):** 0 `download_filtered` calls by her since activation, last use none. The positive
  control saw her 5 events and another principal's 1 download. The general lake's blind zero is reported and not relied on. The
  count goes to Andrew with the result.
- **Both branches, the read-back** (download REFUSED, one other operation ANSWERS, through the installed code, no call as her) **and
  the rollback** (revision 6 = the before scope, via `activate`).

## CT1 -- the approver field must not claim an approval Andrew did not give

The CLI is run with `--approver "Andrew Berman"`. If the module requires the owner's name in that field, the `operator_audit` line
says so in plain words: "approver field = data owner per the writer's schema; this act enforces his 2026-10-08 word under CTO ruling
@aed4469fa6 / XA-a7a7; he did not approve this act in person." No record may read as his personal approval of this act.

## Phase B

Phase B runs on the issuer's GO naming all three halves at this sha256. No seat contacts Alyssa or her firm. Andrew's one word,
"Alyssa may download", reverses it.
