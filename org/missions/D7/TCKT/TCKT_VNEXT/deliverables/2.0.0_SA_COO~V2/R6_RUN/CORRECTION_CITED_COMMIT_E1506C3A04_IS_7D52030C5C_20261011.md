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
