# 2.0.0_SA_COO~MI2 handoff -- NFRA_MCPINDEX round 18, workstream RESEARCH -- 2026-10-16 ~01:15Z (Site Z winding down on Andrew's word, CTO msg 34632)

**archetype:** COORDINATE

Seated by 0.0.0_AB_MSTR~Z on Andrew-direct ~18:4xZ 2026-10-15 (CRO msg 34538). Finish line (PRD v0.17 @532d1e68bb): every in-scope row carries C-GROUP and a live `read_tool`, by 2026-10-16 ~22:00Z. Push state: everything below is LOCAL on `box/sitez`, nothing pushed.

## Done and merged (all re-graded on the merged tree)

| order | what | commit |
|---|---|---|
| MX-c-30 | the 2 advisor-intelligence rows out (`scope_exclusions.json`, generator `--scope-exclusions`; 214 rows written) | merged 5dad340056 |
| MX-c-34 `-35` `-36` `-37` | curated tags for the 37 `inferred` RESEARCH rows, as `--group-map` files in `deliverables/0.9.0_WK_NFRA_MCPINDEX~52..55/research_group_map_{h1,h2,h3,p1}.json` | merged abaefd2c81 .. f5fa108fae; flips 23b89ba47f |
| drain check | `c30.DRAIN.sh` PASS on the ASSETS issuer's trial catalog (msg 34624): 178 rows, 0 inferred, bucket spelling 0 off | b4d114d3fa |

## In flight

- **MX-c-31** (`--read-links`, 27 rows; workstream `RESEARCH-LINKS`, round 18) cut @c21cb3ce28, worker `0.9.0_WK_NFRA_MCPINDEX~56`, worktree `C:/tmp/mi2-wk56`, branch `wk-NFRA_MCPINDEX-56`. A worker dies with the session; its commits survive on that branch. After the reboot: `git log wk-NFRA_MCPINDEX-56` (is there a proof instance? is the order `complete`?). If it finished: re-run `c31.AC1/2/3.sh` in the shared tree, then `bash .tools/safe-merge.sh wk-NFRA_MCPINDEX-56`, remove the worktree (`.tools/wk-provision.sh remove C:/tmp/mi2-wk56`) and delete the branch. If it did not finish: re-seat slot 56 on the same order, naming its prior commits.
- The link data is the issuer's: `deliverables/2.0.0_SA_COO~MI2/round18/read_links.json` (27 links), `deployed_r18.json` (the 99 tools served today), `deployed_future.json` (99 + 14 built tools). Six links are live now; the other 21 take effect only when I regenerate the rows with the released tools in the deployed list:
  `python workflows/atom_decomposition/gen_silver_rows.py ... --deployed-tools .../round18/deployed_future.json --read-links .../round18/read_links.json` (the full line is in the MX-c-31 order, step 2), then land the 21 row changes, but ONLY after the gateway batch release (OG-ap-22 and the gf-1/gp-1 code) is live.

## Owed after the reboot (CTO msg 34632 ruling: a gap owner does NOT meet the line)

The 43 RESEARCH rows with no tool planned (34 DEFERRED in the OG-gp-1 / OG-gf-1 classification files, `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~109` and `~110`, `CLASSIFICATION.json`; plus the 9 dynamodb/news rows) each get ONE disposition:
(a) in scope: list to `2.0.0_SA_COO~O` as a tool OPLGTW owes, by bucket and table; or
(b) not a served surface: ruled out of scope with its reason in the release record (as MX-c-30 did for advisor intelligence).
Candidates for (b) from the classification reasons: hand-maintained configs, raw plumbing tables and account-grain client feeds that need their own never-widen grant. Read each `reason` field before deciding.

## Waiting on others

- ASSETS issuer `2.0.0_SA_COO~MI` runs the ONE emitter at MX-r-15, about 17:00Z 2026-10-16, with my four group maps; he sends me the release catalog path and I run `bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI2/round18/checks/c30.DRAIN.sh` on it (`C30_CATALOG=<path>`).
- The 60-minute `/canonical-drive` cron is session-only and dies with the reboot; re-arm per `org/ref/LIVE_ARMS.md` (every COO lane on an active project) with `/watcher` first.

## Instruments

All checks are in `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI2/round18/checks/`: `c30.AC1/AC2/DRAIN.sh`, `c31.AC1/AC2/AC3.sh`, `ct.{h1,h2,h3,p1}.sh`, `plant_c30.py` (8 of 8), `plant_ct.py` (12 of 12). Decomposition: `decompositions/NFRA_MCPINDEX_DECOMP.round18-RESEARCH.md`.
