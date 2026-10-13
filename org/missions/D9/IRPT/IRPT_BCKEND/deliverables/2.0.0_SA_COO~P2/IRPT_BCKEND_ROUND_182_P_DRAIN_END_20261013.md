# IRPT_BCKEND round 182, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~18:2xZ). To: 3.0.0_SA_CVO. One order, terminal, issued @790da92969 on the signed pair IB-pr-515 (CTO half @01d0a01db9, msg 7098) and Andrew's word at this seat (row D2-S140). One amendment (mine, below). The round-182 formal analysis follows the CVO's slug.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 182 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). The issuer re-ran IB182-1 AC1 to AC3 on the merged tree: PASS.
Push state: LOCAL for the order's own commits at this writing (`c0a5051a2e` the status flip, `4344e10b11` the ledger close, `8df634fac5` the apply record, `d3fbb27889` the amendment); origin not re-read.

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-516 | `irpt-directory-search` moved to the signed built digest by its Terraform path and `safe-apply` (`handler.py` the only changed member), then a health proof | applied 2026-10-13T17:35:54Z by 0.7.0_AE_CloudOps~IB2; flipped complete @c0a5051a2e | 3 of 3 PASS (AC3 as amended) |

## What the CVO needs to know

- **WORLD act, landed.** Live CodeSha256 `rXHDDz/ZhY2pZFuLDcrPisAs69IuTd6p8Rwflxhvwyw=` equals the signed built digest (I re-read it after the apply and again at ~17:50Z). Plan 0 to add, 1 to change, 0 to destroy; one `safe-apply`, rc 0; the re-plan reads 0 changes; the deployed zip against the pre-apply live zip differs in `handler.py` only. No rollback; Branch B (S3 version named before the upload) was ready and not run. Ledger `irpt-dirsearch-tail-accounts-20261013` CLOSED 5 of 5.
- **What the release does:** a last-four (tail) query returns each permitted account's own ACCOUNT entry with its mask; a pick resolves to exactly that account; a name query is unchanged; permission is unchanged and no figure moves.
- **The gates were measured at the artifact (row D2-S141):** both halves signed at packet sha256 `3c369b9086b3...`; the CTO's portal condition (a) read 0 null `accountId` over 9,441 ACCOUNT entries produced by the built `handler.py` from the three landed directories (positive control reads 1; the portal adapter sets `accountId` from `scope_ids[0]`, identical on PROD and DEV); 0 of 271 open-deploy markers on 15 readable worktrees name the function.
- **ISSUER DEFECT (mine, row D2-S143):** order 516's step 6 told the apply seat to invoke the deployed function with a synthetic `directory_fixture`. The deployed Handler is the guarded `entry.lambda_handler`, which has no fixture path (it resolves scope from a verified principal's headers); the one fixture invoke was refused at CONTRACT_VERSION. I read `handler.py:462` and not which function the deployed Handler names. AMENDMENT 1 struck the second invoke and replaced the proof with a health proof: the deployed `handler.py` member sha256 equals the built member (`d73af1c77aa3...`), and the metrics and log group over 17:35:54Z to 17:48:12Z read 10 invocations, 0 errors, 0 TypeError, with 10 START lines as the positive control. The CTO accepted the substitute and ruled no restore (msg 7116).
- **The served read is met by a person:** Andrew's tail search on his localhost:5174 smoke worked ("last 4 digit search does work", smoke item 1.8; relayed in CTO msg 7140). This is NOT shown for a client login on PROD: the PROD promote is held (dell1-e7f2).
- **Rows:** D2-S144 disarms D2-S139, D2-S141 and D2-S143 (INERT, evidence cited). STILL ARMED, owner me: W349-S1 (the latent `served.py` / `enforce.py` attribute mismatch, identical on live and built), W361-S1, W348-S2. New INERT rows: D2-S142 (the apply seat's report), D2-S145 and D2-S146 (Andrew's two Holdings smoke items, queued behind the O1/O2 release).
- **One call I could not close alone:** my open-calls act for the served read (`dell2-20261013T174656Z-6635`) measures CROSS-BOX and needs a cross-adjudication file to close; it is met on the facts above.
- **Not in this round:** IB-pr-456 (steps 2 and 3 wait on Andrew's own PROD submission and execution ID; the CTO withdrew its ADDENDUM 2 request).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
