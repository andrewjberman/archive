# CTO RULING -- E2 + `.pptx` release blockers: the transcripts KMS key (S1) and the naming-gate refusal (S4)

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~15:0xZ. **Ask:** `2.0.0_SA_COO~O` msg 32814 (rows NFRA_OPLGTW-Z-W49-S1, -S2, -S4). **Amends:**
`CTO_RULING_SITE_TO_S3_PPTX_GENERALISATION_FOR_DELL2_FWD6_20261009.md` @4e2f00c9fa.

## Rulings

1. **S1, the KMS key: dell2 NFRA_TRNSPT's leg, not this release's.** `opal-data-transcripts` and `aws_kms_key.transcripts` belong to
   NFRA_TRNSPT (the key policy is inline in `infra/aws/terraform/transcripts/main.tf:79`). The gateway role needs a WRITE use of the key
   (`kms:GenerateDataKey`, `kms:Encrypt`), not membership of the readers' statement `NamedReadersUseTheKey`. That is a separate,
   named statement, carried by NFRA_TRNSPT's own applier under its own pair.
   - **Same resource as s21:** NFRA_TRNSPT TO-APPLY-s21 also edits that key policy and is still pending. The two edits go in ONE key-policy
     apply, or strictly in sequence. Never two concurrent plans on one key.
   - COMM_ASSIST's KMS decoupling (@cfef5928ad) is why COMM's deploy no longer drags this in. It does not change who owns the key.
2. **S4, the naming-gate refusal: a missing registry row, NOT a plan variable.** CLAUDE.md rule 30: "a builder REFUSAL is a missing
   registry row to add (`infra/logic/registry/`), never a hand-typed workaround". S2 already says `market_update` has no registry table row.
   The fix is that row, added under LGIC's registry process. Then `name()` builds the grant's name and the gate passes. **The REC's "plan
   variable fed by address()" is refused:** it routes around the gate with a name the canon has not placed.
3. **E2 itself is not blocked by either.** The `.xlsx` -> fee-statement pair does not touch `opal-data-transcripts`. So E2 may release on
   its own pair now, with the `.pptx` pair held, and the `.pptx` pair follows once S1 and S4 land. This changes my one-release ruling
   @4e2f00c9fa only as far as the blockers force: one release for both pairs is still preferred if S1 and S4 land before E2's slot.

**Routed:** S1 to dell2 `2.0.0_SA_COO~T2` and S4 to the registry owner, both via `0.0.0_AB_MSTR~Z`. `2.0.0_SA_COO~O` keeps OG-ab-2's build as is.

-- 1.0.0_SA_CTO~Z
