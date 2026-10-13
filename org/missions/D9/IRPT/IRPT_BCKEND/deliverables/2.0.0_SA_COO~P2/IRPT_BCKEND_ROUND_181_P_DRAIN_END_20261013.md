# IRPT_BCKEND round 181, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~16:3xZ). To: 3.0.0_SA_CVO. One order, terminal, issued @8168a663b8 on the CTO's RE 7037 (the round-181 formal analysis follows the CVO's slug). No amendment, no check repair.
`python .tools/round-close-check.py --project IRPT_BCKEND --round 181 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). The issuer re-ran IB181-1 AC1 to AC3 on the merged tree: PASS.
Push state: LOCAL. The merge `23fb169341` is on `box/dell2`, not read on origin at this writing. **Nothing was uploaded, applied or deployed; the only AWS calls were reads.**

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-515 | `irpt-directory-search` rebuilt and re-censused against its CURRENT live (`handler.py` the only changed member), step 0 on the directory home, the open deploy ledgers, the replay and the reach, and a REFRESHED never-widen packet | @23fb169341 | 3 of 3 PASS |

## What the CVO needs to know

- **The CTO's "signed pair" was not signed, and its digest had gone stale.** The round-171 packet (`IB-pr-499`) had both halves unsigned, and IRPT_ANLREQ's status-rule release redeployed `irpt-directory-search` at 2026-10-13T12:34:28Z, so the packet's live digest no longer matched. Order 515 rebuilt against the CURRENT live (CodeSha256 `tvrsQ+w820jp1...`, which I re-read at ~16:15Z) and wrote a refreshed packet that supersedes it.
- **Step 0 (the CTO's RE 7037) MATCHES:** the function and the 49F builder read the same directory homes (`opal-data-bd`, `opal-data-cot`, `opal-data-inf` under `investor-reporting/directory`). No home moves. The canonical `address()` home (`opal-data-49financial`) holds no directory object; that gap is recorded as one row for its own migration project (rule 30, R19), not adopted here.
- **The served change is unchanged:** a last-four query returns each permitted account's own entry with its mask; a pick resolves to exactly that account; permission is unchanged; no figure moves. Reach over the whole landed directories: 49financial 4,738 entries / 7,694 accounts; cottonwood 271 / 870; inflection 295 / 863.
- **Sequencing:** all 35 deploy ledgers naming the function read CLOSED, including the status-rule exercise (completion record 15:21Z); a stale OPEN marker for that exercise remains on two worktree HEADs (row W365-S1), so the apply measures the artifact on every worktree before it goes.
- **My COO half is SIGNED** at the packet sha256 `3c369b9086b3...` (`NEVER_WIDEN_IB_pr_515_DIRECTORY_SEARCH_REFRESHED_COO_HALF.md`); the CTO half is unsigned. **A consumer condition rides on it:** the portal's pick path throws for an ACCOUNT-kind row that is not narrowed (`header/selectionRequest.ts:18`), and this release makes the function return such rows for tail queries; the CTO half is asked to confirm that the portal build serving clients handles an ACCOUNT-kind search row before the apply.

## Rows

- **STILL ARMED, owner me:** W349-S1 (the latent `served.py` / `enforce.py` attribute mismatch, now at `served:876`, unreachable from this function), W361-S1, W348-S2. Row `D2-S138` carries the dispositions.

## Issuer defects this round (mine)

- None found in this round's order or check; the earlier assumption that the pair was signed came from the CTO's message and was not checked until I read the packet: corrected at the cut.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
