# NFRA_CTLPLN round 16 -- drain end, L8 packet and inputs for the round-16 analysis, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~07:3xZ)

All three round-16 orders are `complete` (issuance `cb843928c1`, decomposition `NFRA_CTLPLN_DECOMP.round16.md`; flips `edbb9f9863`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 16` reads `verdict=MAY-CLOSE`, `orders=26 judgment=2 graded=2 ungraded=0 self_graded=0`, and for the first time counts the round's own orders: `TREE orders counted by decomposition round: 3 (TO-CT-af-1, TO-CT-af-2, TO-CT-af-3)`. Pins are commits on `box/laptop`, LOCAL unless stated. Each cell carries the issuer's own re-run.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | merge | issuer re-run |
|---|---|---|
| `CT-af-1` | `e2720105d5` | `WORKTREE-GC-OWN-COMMIT arms=8/8 ok=True`; `WORKTREE-GC-SELFTEST cases=3/3 ok=True`; dry run SUMMARY now carries `UNSTARTED=`; the negative control (a branch at its issuance commit, clean and dirty) is never removed |
| `CT-af-2` | `c9424f396f` | `ROUND-CLOSE-DECOMP-ROUND arms=6/6 ok=True`; `ROUND-CLOSE-SELFTEST cases=30/30 ok=True`; on the real project `--round 15` prints `TREE orders counted by decomposition round: 3 (TO-CT-ae-1, TO-CT-ae-2, TO-CT-ae-3)`, verdict MAY-CLOSE |
| `CT-af-3` | `da61dea773` | `PLACEMENT-UNSTAGE arms=4/4 ok=True`; `ROUND15-BATCH arms=9/9 ok=True`; `SAFE-COMMIT-DERIVATION cases=17/17 ok=True`; the issuer read the four-line diff |

Every proof instance reads VALID from `proof-of-spec-check.py` on the committed state. Every worker committed early (a WIP commit before its first criterion): the three branches carried 4 to 5 commits of their own.

## 3. Real runs of the outcomes

- **The own-commit test, used on its own cell:** I ran `worktree_gc.py --check-removable` on the three round-16 worktrees right after their merges. All three read `NOT-REMOVABLE MERGED` because each holds six ignored non-cache paths left by the tests it ran (`.comp-graph/`, `.scratch/`, `org/mcp/comp-tool-runs.jsonl`, `org/mcp/naming-gate-verdicts.log` and others), although `git status --porcelain` is empty, own >= 1 and HEAD is in `box/laptop`. By the CTO's definition (own commit, in trunk, clean porcelain) they were removable, and I removed them by that definition. So the verb as built can never say REMOVABLE for a worktree that ran the repository's own tests. See D1.
- **`round-close-check`:** the first run that counts its own round's tree orders (round 16 above). The worker's blind measure over the project: 144 orders read, 46 change scoping round, all 16 round verdicts stay MAY-CLOSE before and after.
- No UI is touched, so no screenshot.

## 4. FWD state

`FWD-11` is a qualified wait on Andrew's word (open call `laptop-20261014T205216Z-7841`); `FWD-9` PARKED; `FWD-27` waits on Andrew's "another time".

## 5. Rows this round minted

`W100-S1` (ARMED, disarm_owner `1.0.0_SA_CTO`; asked of the CTO, message 20261015T070330Z), `W100-S2`, `W101-S1`, `W102-S1`. `W99-S1` is closed by `CT-af-3`. Carried: `S9125` (dell1), `S9119`, `S9103`, `S9120`, `S9122`, `Z-S3`, `W12-S1`, `W89-S3`.

## 6. Not measured here

A real `worktree_gc.py --go` (never run on the real repository; every arm used a temporary one); the placement-override branch of `safe-commit.sh` (read, not exercised); the PRD FWD grade table, which the CTO's coverage read governs.

## D. Inputs for the round-16 analysis

1. **`--check-removable` is too strict (W100-S2).** The worker added a refusal on non-cache ignored files that the CTO's definition did not carry. Measured in section 3: every worker worktree that ran the tests is refused, so the drain still removes by hand. Candidate round-17 cell: `--check-removable` tests `git status --porcelain` only (ignored files are not work product), one arm changed, one added. Until then the drain applies the definition itself: `git status --porcelain` empty, own commit count >= 1 (`git rev-list --count <issuance commit>..HEAD`), HEAD contained in a box branch.
2. **W100-S1 (ARMED):** `--go` still force-removes a dirty merged worktree with an own commit (Andrew's standing word); `--check-removable` refuses it (the CTO's ruling 1). Asked of the CTO; the issuer's REC is to keep `--go` as it is.
3. **W101-S1 ruled (issuer):** eight untagged seat-folder orders that name a decomposition now scope to its round. That is the intent of ruling 4; no amendment.
4. **Merge needed a quiet index.** `safe-merge.sh` refuses while any seat has staged changes. Twice this drain the shared index held another seat's staged files (46 at one point) for several minutes; a retry loop did not find a clean window for six minutes, then one did. Not a defect in the tool, a cost of a busy tree. The workers' branches were safe throughout.
5. **Proof-instance schema and early commits worked.** All three workers copied field names from the named VALID instance and committed early; none needed a schema re-commit this round.
