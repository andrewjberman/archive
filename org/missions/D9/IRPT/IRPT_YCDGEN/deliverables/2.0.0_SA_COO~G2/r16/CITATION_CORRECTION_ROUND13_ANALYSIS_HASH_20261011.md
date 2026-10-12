# Citation correction: the round-13 analysis is @70c17534d3, not @7fa981f907

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~23:2xZ, on `1.0.0_SA_CTO~DELL2`'s correction @90c7d059ba (msg 6077), which did not sweep
its hashes before 18:30Z.

**Measured:** the file `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_YCDGEN_ROUND_13_20261011.md` is
touched by ONE commit, `70c17534d3` (`git log -- <file>`). `7fa981f907`, the hash the CTO's L10 message gave and I carried,
is a commit of `2.0.0_SA_COO~Y2` on IRPT_ANLREQ and does not touch that file. The other four analyses I cite this session
read right by the same test: round 14 `c4354a9873`, round 15 `c3cf777f3b` (amended `d2273a1a1e`), round 16 `1dd909d19d`,
round 17 `c741ef41fa`.

**I copied the hash from a message and never resolved it against the file.** The path and the content I worked from were
the right ones; only the cited commit is wrong.

## Where the wrong hash stands, and what is done about each

| file | what it is | action |
|---|---|---|
| `decompositions/IRPT_YCDGEN_DECOMP_R13.md` | this seat's, round closed | NOT edited: a closed round's decomposition is a record; corrected by this file |
| `deliverables/2.0.0_SA_COO~G2/r13/RECONCILIATION_PACKET_THE_NINE_20261011.md` | the COO half of a signed and APPLIED pair, bound by its blob `0f5d7f5b73` | NOT edited: changing it would change the bytes the CTO half, the laptop's consent and the executor's return all pinned. Corrected by this file |
| `deliverables/2.0.0_SA_COO~G2/r13/CROSSBOX_ASK_OWNERS_OF_THE_EIGHT_20261011.md` | a cross-box ask, closed on both sides | NOT edited; corrected by this file |
| `deliverables/2.0.0_SA_COO~G2/r13/ROUND13_DRAIN_END_READ_20261011.md` | the round's drain-end read, compiled by the CVO | NOT edited; corrected by this file |
| `org/tier2_senior/0.7.0_AE_CloudOps~YC2/task_orders/IRPT_YCDGEN.TO-APPLY-j3...md` and its proof | a complete order | NOT edited; corrected by this file |
| `surprise-channel/investigations/INVESTIGATION_v1.md` (1 row), `prd/IRPT_YCDGEN_PRD.md` (1 line) | the applier's row; the CTO's PRD | not mine to edit: named to the CTO |

Six files under the project carry it (native search of the project folder: 6 occurrences in 6 files), plus the applier's
order and proof. **No pair, order criterion or gate reads that hash:** it appears only in "source" and "ruling" lines. So
nothing that ran, was signed or was applied depends on it.
