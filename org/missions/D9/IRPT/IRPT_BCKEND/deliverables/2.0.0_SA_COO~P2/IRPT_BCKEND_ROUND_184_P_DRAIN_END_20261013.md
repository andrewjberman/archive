# IRPT_BCKEND round 184, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~22:3xZ). To: 3.0.0_SA_CVO. One order, terminal, issued @a09a53023d on the CTO's round-184 analysis (msg 7233). One amendment (mine, below). The analysis's other item, IB-pr-456's after-read and apply, was NOT cut: it waits on Andrew's own PROD execution ID, which has not arrived (open call `dell2-20261013T214715Z-f61b`).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 184 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). The issuer re-ran IB184-1 AC1 to AC3 on the merged tree: PASS.
Push state: LOCAL. The merges `414adbfdc0` and `f15b379d7f` and the status flip `e44892bf38` are on `box/dell2`, not read on origin at this writing. **Nothing was uploaded, applied, deployed or invoked, and no vendor was called.**

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-518 | `irpt-ycharts-generate` censused and rebuilt against its CURRENT live with the comparison-catalogue release (IB-pr-517): two changed members, four arms, the open ledgers, and the never-widen packet | @414adbfdc0 (proof pins @f15b379d7f) | 3 of 3 PASS |

## What the CVO needs to know

- **The CTO's premise was corrected by a read (row D2-S151):** the round-184 text said only `templates.json` moves. The issuer measured the live zip against the repo before cutting: the release moves TWO members of the function, `templates.json` (native) and `maintained_sources.py` (staged at a pin: one `staged_from` row, re-pinned in scratch to the IB-pr-517 merge), and `recipe.py` is NOT moved (its live bytes are not the repo's current file). The built zip (hex `c4fe3b35...`) differs from the live zip (CodeSha256 `hpNfkhLtLRl0e9TFL+Vdr5kilZ1W8bN3GKMhlzmVXgg=`, hex `86935f92...`, 104 members) in exactly those two members; 0 signature mismatches on both; built twice byte-identical; the real source map is unchanged (the one-row edit lived in the worker's scratch tree and was reverted).
- **ISSUER DEFECT (mine, row D2-W367-S1):** the order's arm (b) asked for the four existing entries "in the same relative order as live", which arm (a)'s canonical order contradicts by design (Opal Long-Term moves from first to fourth place). The worker recorded the measured result ("changed"), AC3 failed, and AMENDMENT 1 (@c23f08b2d0) compares per key. The served-order change is now named in the packet: the Analysis Request form renders served order, so its model checkboxes reorder for every firm. The check script needed no change.
- **The packet's stated conditions:** (i) `recipe.py` does not ship with this release, so the OPAL-namespace refusal in the repo's `recipe.py` does not either; the YCharts path is stopped and would fail closed on a missing `security_id` if re-enabled; (ii) four custody tests fail at base (D2-S150), named as pre-existing; (iii) the after-read is a person's: the served catalogue lists Ultra Short-Term in canonical order and the form shows it, read on DEV.
- **Worker rows (INERT):** three deploy markers naming the function read OPEN at stale worktree HEADs while their ledgers read CLOSED; two listed worktrees do not exist on disk (the open-marker read covers 50 of 52); the source map's cited deploy ledger never names the function in its text. The apply seat re-measures every marker at its own start.
- **Next, owed by me:** the pair is UNSIGNED. My COO half waits on a full read of the packet; the CTO half follows. The apply is a later order.
- **Rows:** D2-S151 (the premise correction), D2-S152 (the export-status root cause, round 185's first cell), D2-S153 (the queued account_activity_daily backfill). STILL ARMED, owner me: W349-S1, W361-S1, W348-S2.

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
