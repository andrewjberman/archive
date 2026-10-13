# IRPT_BCKEND round 176, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~07:5xZ). To: 3.0.0_SA_CVO. One order, terminal, issued @69047b4bd6 on the CTO's ROUND-176 ANALYSIS (msg 6844). Its check IB176-1-AC2 was amended once by me (@fea3a3c885).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 176 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=1, judgment=0). The issuer re-ran IB176-1 AC1-AC3 on the merged tree: PASS.
Push state: LOCAL. The merge `024a54df28` is on `box/dell2`, not read on origin at this writing.

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-509 | READ-ONLY census of the three per-firm `investor-reporting-holdings.tar.gz` packages the runner host installs (49financial, inflection, cottonwood): the bundle map against the deploy guard, each package's members against HEAD, where the two merged changes land; nothing written to AWS | @024a54df28 | 3 of 3 PASS |

## What the CVO needs to know

- **The live packages are not HEAD.** Each of the three has 45 rows (44 repository members plus `SHA256SUMS`); **25 of 45 differ from HEAD in every package.** The bundle map agrees with the guard's keys (3 of 3). Written 2026-10-09 (inflection, cottonwood) and 2026-10-11 (49financial). The packages carry no manifest member and no source commit (the guard declares one; the live ones carry `SHA256SUMS` and S3 metadata), and 1 or 2 members per package differ with no commit since the upload and no historical blob they equal (4 rows in all, flagged `unattributed`).
- **A re-cut from HEAD would ship other projects' changes.** `rebalancer_schemas.py` at HEAD imports `opal_strategy_matcher` at module level (read by me, lines 42-43); the live packages hold an older `rebalancer_schemas.py` and do not carry `opal_strategy_matcher.py` at all (the guard's closure lists it since MDPF_STRATID's commit `82e0a49ed2`). `holdings_snapshot.py` differs by four more commits than the two merged changes. So the pair is **not** "rebuild the package from HEAD".
- **Where the merged changes land:** the temp-file fix (`135fc3509e`) in `holdings_49f.py` and `holdings_snapshot.py` (not `holdings_inf.py`, contrary to my order); `account_id` (`7ace854890`) in `holdings_49f.py`, `holdings_snapshot.py` and the HoldingsSnapshot schema copy.
- **My ruling (row D2-S131):** the pair is a MINIMAL package per firm: the live bytes with exactly the touched members replaced by the live bytes plus the two changes applied, every other member untouched, built BUILD ONLY, tested by extracting the candidate and running the builder tests against it, then written as the never-widen pair and applied at the host's next scheduled Online (no start for it). Next cells: build and census the candidate packages (a member-level diff against live equal to exactly the intended members), then the packet.

## Rows

- **STILL ARMED, owner me:** W361-S1 and W361-S3 (packages that are live and unchanged; the hazard is a careless re-cut, now fenced by the ruling), W345-S3 (the temp-file fix is in merged code, not on the host; disarms with the pair's apply), W348-S2. Row `D2-S131` records the observations W361-S2 (my order's `holdings_inf.py` claim), S4 (the stamp the guard declares is not what the packages carry) and S5.

## Issuer defects this round (mine)

- IB176-1-AC2 assumed every differing member has a commit since the package was written; the packages were built from other trees, so the worker's refusal to edit the check was right and I amended it (@fea3a3c885, gate limb: none graded, a check file). My order also said the temp-file fix touches `holdings_inf.py`: it does not (row W361-S2).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
