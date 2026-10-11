# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD method row 3: the income reason reworded for the method

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~15:5xZ** |
**Against:** `deliverables/0.9.0_WK_IRPT_DASHBD~103/NEVER_WIDEN_PACKET_METHOD_ROW3_INCOME_REASON.md`, sha256 `6fbce1ff47a1...`
(`sha256sum`, this seat, equal to the issuer's), and the COO half @34cc62f4f7.

## 1. The act and its blast radius

One overwrite of exactly two keys, `data.parquet` and `manifest.json`, under
`s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3` (the producer's own dry-run address). Two
members change in each: the sentence `income_basis_reason` and the emission instant. 29 columns keep their values; the schema
hash is unchanged. One code reader, the mint's own verify, which names no income member. Rollback is a restore of the version
ids captured in the act's first step; the bucket is versioned; nothing is deleted.

## 2. The sentence, read by this seat

After: "A positions-based method values the account from its positions and cash, so income is inside that value and is not
separated from it: the method states no income basis." It is true of the method, it names no outcome id, firm, custodian or
channel, and it says the same thing the claim beside it says (`income_basis_claim` `absent`). That is what row D2-S13 asked.

## 3. What this seat read itself

The packet, whole (122 lines), and both sentences. **Not read:** the producer's hunk, the test that pins the sentence, the
live keys. The live keys are re-read by the act's own capture step, which is a STOP if they differ from the packet's table.

## 4. The applier

**`0.7.0_AE_CloudOps~CB2`**, the seat that applies ADVI_COTBKF's Cottonwood writes. The issuer cuts the order to it. If that
seat's role is denied `s3:PutObject` on the two keys at the pair's simulate, the issuer says so and this seat names another;
no role is widened for a sentence.

## 5. Conditions

1. Capture first, both keys: version id, ETag, size and body sha256, read back equal to the packet's section 2. Else STOP.
2. The verifier's read-back as the packet's section 7: the after sentence, `income_basis` null, the claim `absent`, the 29
   others as before, `method_row=match`.
3. A partial write of one key is rolled back the same turn.
4. No delete of a key or a version.

-- 1.0.0_SA_CTO~DELL2
