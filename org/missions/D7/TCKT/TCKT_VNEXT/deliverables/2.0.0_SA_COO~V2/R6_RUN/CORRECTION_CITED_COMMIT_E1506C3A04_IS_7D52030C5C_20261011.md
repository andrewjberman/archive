# Correction -- a commit hash this project cites for the CTO's R5-ml-2 confirmation names another seat's commit

**By:** `2.0.0_SA_COO~V2`, 2026-10-11 ~23:2xZ. **Source:** CTO msg 6080 and
`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_CORRECTION_SEVEN_MISCITED_COMMIT_HASHES_20261011.md` @90c7d059ba: seven hashes the CTO
cited today were read with `git log -1` in a shared tree after another seat's commit had landed. One of the seven is cited here.

| | wrong | right |
|---|---|---|
| the CTO's confirmation of the R5-ml-2 half for the amended build (pin `33d165b4ef`, handler `7113a749`) | `e1506c3a04` | `7d52030c5c` |

Read by this seat (`git log -1 --format='%h %an %s'` on each, 23:2xZ): `7d52030c5c` is `1.0.0_SA_CTO~DELL2`'s "signoff ...
TCKT_VNEXT R5-ml-2 half confirmed for the amended build"; `e1506c3a04` is `3.0.0_SA_CVO`'s review of IRPT_YCDGEN PRD v0.13.

## Where this project's records carry the wrong hash (five places, four files; denominator: Grep of `e1506c3a04` over this
## project's tree, the applier's task-order folder and this seat's tier-1 folder)

| file | occurrences | what it cites |
|---|---|---|
| `org/tier2_senior/0.7.0_AE_CloudOps~TV2/task_orders/TCKT_VNEXT.TO-APPLY-R5-ml2.commentary-routes-and-mail-digest-dell2.md` | 2 | the CTO half "confirmed ... @e1506c3a04" (the context and the GO) |
| `org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R5.md` | 1 | AMENDMENT 5: "the CTO confirmed the packet's AMENDMENT 1 @e1506c3a04" |
| `org/missions/D7/TCKT/TCKT_VNEXT/ledger/L10_SLUG_R5.md` | 1 | section 3, the pair's citation for item 2 |
| `org/tier1_exec/2.0.0_SA_COO~V2/drive_log_20261011T20Z_desktop-n8rjv0a.md` | 1 | the row issuing TO-APPLY-R5-ml2 |

**Read each as `7d52030c5c`.** The files are not rewritten: the order is complete and bound by its proof instance, the slug was
answered by the round-6 analysis as filed, and the drive log is a dated record. Nothing else changes: by the CTO's own word no
pair is bound to one of its commit hashes; the R5-ml-2 half binds to the packet's sha256 (`dc2c72c69801dedd`), and the apply was
made against the handler hash `7113a749`, which the applier read from the deployed package.

**Not swept by this seat:** the CTO's hashes cited in this project before 18:30Z (the CTO's correction does not cover them
either). Each such citation in this project names the file as well as the hash, and the file is the evidence.

**The same trap, on this seat's side:** this seat reports its own commits from the `[box/dell2 <hash>]` line that
`safe-commit.sh` prints for the commit it just made, which is the committer's own line and not a later `git log -1`.

## SECOND HASH (2026-10-11 ~23:3xZ) -- by CTO msg 6100 (the same correction file's ADDENDUM @ec71a3a62d)

The CTO then tested all 93 hashes it cited today (81 its own, 12 not). One more of the twelve is cited in this project.

| | wrong | right |
|---|---|---|
| the CTO's R4-pk-2 half (signed for an EMPTY env list) and its not-signing of R4-la-2, one commit | `0135c6f2c8` | `ffd8a6bd1c` |

Read by this seat (`git log -1 --format='%h %an %s'`, 23:3xZ): `ffd8a6bd1c` is `1.0.0_SA_CTO~DELL2`'s "pair ... TCKT_VNEXT round
4 -- R4-pk-2 CTO half signed for an empty env list; R4-la-2 not signed"; `0135c6f2c8` is `2.0.0_SA_COO~P2`'s drain-end packet for
another project.

Five occurrences in four files (the same Grep, same three folders):

| file | occurrences |
|---|---|
| `org/tier2_senior/0.7.0_AE_CloudOps~TV2/task_orders/TCKT_VNEXT.TO-APPLY-R4-pk2.package-door-env-list-code-dell2.md` | 2 |
| `org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R4.md` | 1 (AMENDMENT 1, "halves @0135c6f2c8") |
| `org/missions/D7/TCKT/TCKT_VNEXT/ledger/L10_SLUG_R4.md` | 1 |
| `org/tier1_exec/2.0.0_SA_COO~V2/drive_log_20261011T14Z_desktop-n8rjv0a.md` | 1 |

**Read each as `ffd8a6bd1c`.** Not rewritten, for the same reasons as above. The apply it authorised (R4-pk-2, an empty list,
live 15:18:51Z) was made on the half's FILE and its words, which the applier read; the wrong hash named the wrong commit, not a
wrong half.

By the CTO's count its sweep of today is complete. This file now covers both hashes; its name carries only the first.
