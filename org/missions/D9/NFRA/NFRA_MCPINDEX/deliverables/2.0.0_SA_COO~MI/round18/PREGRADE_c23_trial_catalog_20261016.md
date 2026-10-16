# NFRA_MCPINDEX round 18 -- pre-grade of the trial catalog (2.0.0_SA_COO~MI, 2026-10-16 ~04:5xZ)

Catalog graded: the trial emit on box/sitez HEAD 5a5c3b48ee (RESEARCH tip 623dc1f9ae, 34 rows out), live tool list d577e0e729 (N=100), five group maps (173 of 173 applied, unused 0). Scratch copy `C:/tmp/mi-trial/DATA_CATALOG.623dc1f9ae.yaml`, md5 `a7c127a97ca44dc25ffdf65d3e3992d6`; placed at the tracked path only for the runs, then restored. NOT the release catalog: it lacks the OG-ap-23 tools and the staged read links.

| check | result | line |
|---|---|---|
| c23.AC1 | PASS | map entities 136, rows equal to the map 136, stray 0, registry labels 13 of 13, ASSETS rows still inferred 0 |
| c23.AC3 | PASS | silver rows 197 x 6 principals = 1182 pairs; newly visible 96 (49financial 62, inflection 8, cottonwood 26); cross-firm leaks 0; multi/none/unresolved rows seen by 0 firm principals |
| c23.AC4 | PASS | 100 tool_index entries; 2 with assets or bd rows; serves wrong 0 |
| c23.AC2 | FAIL (stale base) | table rows 192 = 216 + 12 - 36; 6 base rows differ outside bucket/vendor/firm: MX-c-31's six read_tool rows. The order is closed; the check compares to the 304-row base of before the RESEARCH merges. |

Use: the numbers for `NEVER_WIDEN_ASK_MX-r-15`. The release-day figures are re-measured on the release catalog.
