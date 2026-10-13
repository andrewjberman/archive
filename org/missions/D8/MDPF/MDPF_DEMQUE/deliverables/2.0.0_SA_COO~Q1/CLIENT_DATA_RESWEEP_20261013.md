# Client-data re-sweep of the MDPF_DEMQUE seats' commits (2.0.0_SA_COO~Q1, 2026-10-13) -- paths and counts only

Cause: the dell1 hash list was absent (row MDPF_DEMQUE-D1-W35-S3); `0.0.0_AB_MSTR~DELL1` restored it (29,617 hashes, msg 4897). Method: the gate's own
`hits_in` over every text file added or changed in the first-parent diff of each commit authored by `2.0.0_SA_COO~Q1` or a `0.9.0_WK_MDPF_DEMQUE` worker since
2026-10-07: 245 commits, 3,633 text files read, 115 binary or oversize skipped. A hit is a token whose hash is in the list; no token is printed here.

## This project's files (fixed)

| file | what was done |
|---|---|
| `surprise-channel/investigations/INVESTIGATION_v1.md` | ids redacted in place (10 tokens, 72 rows still parse); audited surprise-row override; @84bb84909c |
| `deliverables/2.0.0_SA_COO~Q1/FWD1_REAL_RUN_R2.md` | ids redacted in place (3 tokens) @84bb84909c |
| `deliverables/2.0.0_SA_COO~Q1/FWD4_REAL_RUN_R3.md` | ids redacted in place (1 token) @84bb84909c |
| `surprise-channel/adjudications/ADJUDICATION_v2.md` | clean at HEAD (hit only in an older commit) |
| `deliverables/0.9.0_WK_MDPF_DEMQUE~27/VALUATION_TRACE.json`, `.md` | moved out of the tree, 2 of 2 byte-copied outside the repo, sha256 verified; `MOVED_ACCOUNT_DATA.md`; @121391fb80 under audited override TREE_DELIVERABLES |

Re-check at HEAD: 0 hit lines in the four narrative files; the two trace files are absent from the tree. Git history still holds the bytes: the purge of origin
history is Andrew's act. The acceptance script `R9_CHECKS/dq_t35_trace.py` reads the moved trace and will report it absent.

## Other projects' files that appear in these seats' commit diffs (merge diffs); NOT touched here, owners to act

19 paths, none authored by this project: ADVI_COTBKF (12, workers `~40`, `~48`, COO `~C2`, `~C`), ADVI_FIRMBKTS (1, COO `~B1`), IRPT_BCKEND (2) and IRPT_DASHBD (2)
(COOs `~B`, `~P`, DS `~S`), `org/tier1_exec` CTO deliverables (2: `CTO_ROUND_ANALYSIS_ADVI_COTBKF_ROUND_24_20261009.md`,
`CTO_ROUND_ANALYSIS_MDPF_DEMQUE_ROUND_2_20261009.md`), `org/tier1_exec/2.0.0_SA_COO~C2` drive logs (3), and `data/assets/scripts/silver/` (3 scripts, ADVI_COTBKF `~40`, `~48`).
Each is named by the same sweep; the owning seat re-sweeps its own commits.
