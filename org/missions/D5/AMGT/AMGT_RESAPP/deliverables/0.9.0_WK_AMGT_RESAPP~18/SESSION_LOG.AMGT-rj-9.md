# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~18 on AMGT_RESAPP.TO-AMGT-rj-9 (the header and the five tabs)

Worktree `C:/tmp/wk-amgt-11-1`, branch `wk-amgt_resapp-11-1` at base `eff1b9f6ae`; portal checkout on
`wk-amgt_resapp-11-1-portal` at base `ffeb4840`. Issuer `2.0.0_SA_COO~W`. All times 2026-09-15 UTC.

## Grounding (premises re-read against live state)

- Tree OK; `SECURITY_ANALYSIS_TABS` held three tabs (thesis, peers, coverage); `read_coverage_set` queried the
  DynamoDB articles table by its per-ticker index; `read_rankings` / `read_point` / `read_rank_series` read the bare
  `<AXIS>#<date>` partition; `read_peer_set` read a deliverables directory (`~4`).
- G-1's writer is `lib/research/metrics/chatter_axis.py` (pointer `_CURRENT`, states COMPLETE / EMPTY / FAILED,
  rows at `<AXIS>#<date>#<generation_id>`). The PRICE producer writes no pointer (row W18-S11).
- Live table: 0 of 8 axis-date pointers; 10 legacy rows at `TRENDING_CHATTER#2026-09-15` (row W18-S11).
- Pool: R-1 33 objects, M-1 5 + `_pool`, D-1 5, F-1 5; P-1 for BA: 2 links, 1 inside the 30-day window.
- Model block header scalars: BA 14, BABA 13, SAP 13 -- no description field; COST and HD have no block (W18-S10).
- F-1 segments are cited prose on 5 of 5; drivers match no block series exactly (W18-S12).
- R-1 members carry `market_cap_musd` only of the 5 present CSC columns (W18-S13).
- The adapter's route table is diffed against terraform outside this order's paths, so no route could be added.

## Acts

1. Adapter (`scoped_amgt.py`): the generation readers (pointer first; the list's row_count check with one retry and
   the SHORT_READ / OVER_READ refusal; EMPTY vs ABSENT; NOT_SERVABLE; the point and series on the pointer, ticker
   case kept), coverage on P-1 through the association keys, R-1 / M-1 / O-1 readers through one pool seam
   (`AMGT_POOL_ROOT`), `read_model`, `read_description`, `read_feed`, `thesis_driver_chart`. Route set unchanged (11).
2. Tests: `conftest.py` (hermetic roots), `test_generation_and_pool_routes.py` (22 arms); the ten tests that
   encoded the retired read shapes moved onto the new ones. 106 passed.
3. First live AC4 run showed posture SERVED for BA: O-1 objects for BA and BABA had landed at 16:56:06Z before
   rj-11 drained to the worktree base (row W18-S14). The reader was not bent to ABSENT.
4. Portal: five tabs; Coverage tab deleted; HeaderBrief (description, Posture line, feed); ModelTab in the Model
   sheet shape; ThesisTab = prose + ThesisDriverChart, held-uncited line by basis (W18-S8); PeersTab = CSC table;
   ExecManagementTab; PostureTab placeholder; GenerationCaption on every ranking render; RankedList / StarredList
   render a refused generation read as a refusal.
5. The portal checkout is `core.autocrlf=true` (index LF, working tree mostly CRLF): the first anchored patch matched
   0 times and wrote nothing; the patch was made EOL-aware and re-run.
6. Fixtures captured from the live adapter for the five QA names; `tabs.harness.cjs` written, including one real
   adapter call over a stubbed 10-committed / 9-held pointer.
7. Rows W18-S10..S15 appended (214 -> 220), schema-valid.
8. The issuer amended AC4 @4f383fc217 (rj-11 drained @496470a993). Read with `git show`, no merge; only AC4's
   invocation and expect changed; the amended invocation was run and recorded.
9. Controls: adapter mutant (the base `read_rankings`, bound to the module's real globals) fired 4 of 4; a first
   attempt bound to a dict copy read the live table once and proved nothing -- not counted. Portal mutant (the
   pre-edit RankedList) rendered no refusal and the empty-day sentence. Determinism: AC1 and the tabs deciding block
   byte-identical across two runs. `tsc --noEmit` rc 0.
10. Commits: workspace `ad830b6cb4`; portal `38cba6a2`; gitlink `e85f6eb8` unmoved.

## Criteria (recorded outputs in the instance)

AC1 tabs in order, Coverage file gone; AC2 BA 1 item of store 2, control UNRESOLVED, 0 table reads; AC3 106 passed,
pointer-reads 7, bare-date reads 0; AC4 (amended) all clauses, posture SERVED hold / DE_US_Equity / machine, model
165 for BA; AC5 four harnesses rc 0 (tabs 20 of 20); AC6 build rc 0, tokens present, 3 portal commits, gitlink unmoved.
