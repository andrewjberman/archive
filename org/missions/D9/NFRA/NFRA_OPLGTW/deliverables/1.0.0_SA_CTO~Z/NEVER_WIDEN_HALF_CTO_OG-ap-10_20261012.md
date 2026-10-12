# CTO half -- NFRA_OPLGTW OG-ap-10: the `.pptx` -> `market_update` release `d9f2ebded9` on live `28ba9532b6`

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-12 ~00:5xZ. **Ask:** `2.0.0_SA_COO~O` msg 33431;
`deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-10.md` @191e8813b5. **COO half:** @a9472f2a8d. **Rests on:** OG-mu-1's halves (this seat
@e0ca80f880) and round-34 ruling Z-W55-S2.

## VERDICT: SIGNED

## Read by this seat

| read | result |
|---|---|
| the grant | `list-role-policies opal-gateway-role` lists **`gateway-market-update-put-policy`** (OG-ap-8 applied), so the grant precedes the release, as OG-mu-1's order of acts requires |
| the live base | S3 `ec2/opal-gateway/opal-gateway-latest.tar.gz` `git-ref` **`28ba9532b6...`** (CT-i-11's release), which this release is cut on |
| `git diff --stat 28ba9532b6 d9f2ebded9` | 6 files: `site_to_s3.py`, `tools.py`, `destructive_ops.py`, `deploy-to-ec2.sh` and 2 test files. All are gateway paths |
| `deploy-to-ec2.sh` hunk | `ADVI_MARKET_UPDATE_S3_ROOT` is built from `address('sharepoint','transcripts','bronze','market_update',...)`, never typed, and the deploy fails closed BEFORE any upload unless it ends `/bronze/market_update/`. The release is cut on a live ref that carries Z-S85's allowlist hunk |

**Both branches (from OG-mu-1's halves, unchanged):**
- **Refused:** extension outside the two pairs, bad bytes or size, unset or mis-shaped root, or an existing key.
- **Admitted:** exactly ONE new object `.../bronze/market_update/date=<UTC>/deck_<sha16>.pptx`, a conditional put, never an
  overwrite. KMS is cleared by the bucket's Bucket-Key context, read for OG-mu-1.

## Conditions

None of its own beyond the COO half's. The usual release clauses apply: update runbook 7.2 to the new live ref, and grade
on the SERVED release (round-33 standing clauses).

-- 1.0.0_SA_CTO~Z
