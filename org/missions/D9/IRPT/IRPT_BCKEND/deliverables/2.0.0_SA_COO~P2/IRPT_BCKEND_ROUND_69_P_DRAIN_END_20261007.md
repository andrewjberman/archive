# L8 drain end -- IRPT_BCKEND round 69, workstream ~P (the back-fill of covered_account_ids)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~23:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD (one S3 write)

**Cut from:** the CTO half of IB-pr-343's emergency release (msg 576): "existing exports stay refused until the v0.30 back-fill, which
you cut next under its own pair". Issuance @3e85fbf2b0, decomposition section 62. **Judgment criteria:** 0.

## The order

**IB-pr-350.** Applier: laptop `0.7.0_AE_CloudOps~I`. Its work reached dell2 through origin (@8eaf445c12, complete flip @f3e5e8a8b7).

**Pass 1 (read-only).**
- Census: listed 1, read 1, filled 1, unfillable 0, would_write 1, denied 0. The 1 receipt is 49financial; cottonwood listed 0.
- The applier's identity decrypted the SSE-KMS receipt that dell2 could not (row W145-S5).
- Packet blob 2e073c2d3e.

**Halves.**
- COO @295835f61f and CTO @c48b2d2442, both signed against that blob.
- The CTO added a condition: the bundle and pending.json must name the same account set at apply.

**Pass 2 (the write).**
- The account-set condition was checked first: both sides named 1 account, with 0 in only one of them.
- The dry run re-read the same counts, then wrote **ONE** key.
- Version 3BN57Lb6hJ7._Nn0hGZ4Yj7NEFYOV_Qa became Jg0xDC0pFmB8UBfEv0sl1eOQ_OrcSAqs. SSE-KMS is kept, and the prior version is
  retrievable (the rollback source).

**After-reads on the deployed bytes.**
- An in-scope principal is ADMITTED.
- An out-of-scope principal is REFUSED on the counts branch, which proves the fill took.
- No token was minted (AMENDMENT 1).

**Graded.** IB69-1-AC1 PASS, re-run by the issuer at dell2 HEAD: 1 listed, 1 written and re-read, 0 unfillable, 0 denied. Two mutants
fired at the applier. The ledger is CLOSED and nothing was rolled back.

## Outcome

The one pre-343 export is readable again for a principal whose scope covers its account, and is still refused for anyone else. With
IB-pr-349 (round 68) this closes the W142-S4 exposure end to end: the read fails closed, and the existing data meets the closed read.

## Rows

| row | status |
|---|---|
| S382 | Ruled (row S386): new-export READY stays OPEN-BY-DESIGN until the first real Opal export. |
| S384 | Fixed (row S387): the issuer's r68 check now resolves Git Bash. |
| S381 | OPEN, owned by ~P2: the export build's drift gate flags backfill_covered_account_ids.py, which sits in export/ unpackaged. It goes to the next repair cell. |

**Push state:** LOCAL at the time of writing.
