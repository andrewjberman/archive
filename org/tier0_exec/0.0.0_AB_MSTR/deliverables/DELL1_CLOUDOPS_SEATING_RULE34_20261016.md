# dell1 CloudOps seating under CLAUDE.md rule 34 (0.0.0_AB_MSTR~DELL1, 2026-10-16 ~15:5xZ)

Basis: rule 34 (Andrew-direct 15:4xZ, record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_154xZ_CLOUDOPS_ONE_SEAT_PER_MACRO_PER_BOX.md`)
and the CTO's order, broker msg 6805. Measured at 15:57Z by `.tools/seat-liveness.py`, `get_agent_status`, `to-check.py --all`
and `org/mcp/agent-spawn-audit.log`. This file is the seating record the COOs asked for (msgs 6808, 6819).

| macro | lane | state at 15:57Z |
|---|---|---|
| MDPF | `0.7.0_AE_CloudOps~DELL1` | DESIGNATED the MDPF lane. Live, holds only MDPF_CANON orders (D1, msg 6819). COO~M1 re-addresses `MDPF_SECCLASS.TO-SC-e108b` from ~SC1 to it. |
| AMGT | `0.7.0_AE_CloudOps~SC1` | live, HVST-cb-15. |
| AMGT | `0.7.0_AE_CloudOps~HV1` | live, spawned 15:31Z by `2.0.0_SA_COO~W1` (HVST-cc-5), before rule 34. A second AMGT lane; W1 has written to it. Whether it stays is the CTO's and W1's call. |
| ADVI | `0.7.0_AE_CloudOps~FB1` | live, 2 open orders (FB-h-5, FB-l-5). |
| TCKT | `0.7.0_AE_CloudOps~TM1` | NOT running: no claude.exe, broker STALE 535s, no open order (TO-MD-r1/r2 complete @797aa123f0). The next TCKT CloudOps order needs it re-seated. |

Closed or already gone: `~CB1` and `~RA1` had no process when `kill-agent.ps1` ran at 15:56:54Z and 15:56:55Z
(`KILL-NOOP`, found=0). Each had 0 open orders and its last commit on origin (`0e47797ffe`, `77cac6580b`). I killed neither.
The worktree `C:/dev/wk-cb1-r88` still exists; its r88 deploy entry has completion records on the trunk
(`20261015T1926Z_..._deploy_completion.md`), so the open-ledger commit on that branch is stale. I left the worktree.

The seating-lint amendment (same-macro CloudOps orders) is `.tools/to-decomp-ref-lint.py`, not in this file.
