# IB-pr-612: who reads the Inflection and Cottonwood holdings-performance run manifests (CTO half of the split pair ADDENDUM 2, condition 1)

Author: 2.0.0_SA_COO~P2 on dell2, 2026-10-16 ~04:4xZ. Read only. Counts and file names only.
**Question (the CTO half):** before Act 1, count every reader of the Inflection and Cottonwood holdings-performance run manifests, with the instrument and denominator printed; a reader that refuses an unknown key (a closed schema or strict key check) is a STOP. The change adds one key, `split_adjust`, to each sibling's run manifest.

## Instrument and denominator

`comp-find 'holdings_performance_manifest' --files --all` and `comp-find 'performance_manifest|TABLE_MANIFEST' --files --all` (two runs, then each by band), corpus `all` at the working tree of `box/dell2` (HEAD `e8f102f8fb` plus the shared index): **263 and 270 hits across 108,407 and 108,429 files scanned**; NOT searched: 130,882 ephemeral-floor files, 25,883 binary files, 2 unreadable files. The table name `holdings_performance_manifest` is the producer's `TABLE_MANIFEST` (`holdings_performance.py` line 132); every address of it is `opal_naming.address()` output, so a reader of the object names the table. Bands of the 270 hits: DEF 5, SURFACED 36 (17 first-party source files at the second run, listed below), CONFIG 114, DOC 115.

## What names the table, by kind (first-party source and definitions; CONFIG and DOC hits are records and prose, not readers)

| file | kind | does it parse the manifest's contents? |
|---|---|---|
| `data/assets/scripts/gold/irpt_holdings_performance/holdings_performance.py` | the PRODUCER (the writer) | no: it writes the manifest |
| `data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_report_reader.py` | Cottonwood's report adapter (DEF) | **no**: it lists `holdings_performance_manifest` in its allowed-table guard `FIRM_TABLES` (line 22) and builds addresses; the file holds no `json.load`/parse of it; the contract `org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json` states in `unread_inputs` that "no member of the filled report names it as a source" |
| `infra/aws/terraform/investor-reporting/holdings-performance/iam.tf`, `locals.tf` | Terraform: the grant and the name | no |
| `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/hand_reproduction_inflection.py` (DEF) | a one-off Inflection hand-reproduction script (names the manifest key, line 38; reads the prior-business-date fields it prints) | it is a deliverable script, not a served path; I did not read its parse for key strictness |
| `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/stale_gap_days_precondition.py` | a one-off precondition script (lists the two tables' keys, line 18) | no: it checks that objects do not exist |
| `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/checks/r2e,r3e,r4e/*.py` (4 files) and `.../IRPT_DASHBD/deliverables/2.0.0_SA_COO~C2/checks/r114,r115,r117,r118/*.py`, `.../2.0.0_SA_COO~D2/checks/r131/p131_cothandler.py` (5 files) | acceptance checks of earlier rounds | not served paths; they read their own round's manifests; not run against the new key |
| `org/mcp/comp-tool-hud.log`, `comp-which-rail.log`, `comp-tool-runs.jsonl`, `.comp-graph/.comp_dedup` | tool logs | no |

## Result

**No first-party SERVING reader of the siblings' run manifests that parses their contents was found, and none that refuses an unknown key.** The single serving-path file that names the Cottonwood manifest (the report adapter) only allow-lists its address, and its contract says no report member reads it. The Inflection manifest has no serving reader by name in this census.

## What this census does NOT cover (so the zero is not read as absence)

- the 130,882 ephemeral-floor, 25,883 binary and 2 unreadable files; a reader that builds the table name from another string than `holdings_performance_manifest` (a typed prefix, a variable) or reads `manifest.json` by a path it computes;
- a reader outside the repository (a person, a notebook, a downloaded script);
- the key-strictness of `hand_reproduction_inflection.py` (named, not read for that);
- the portal and the TypeScript tree beyond what `comp-find` matched by the table name.
The per-sibling DELTA after-read of the addendum (section 4) compares the landed manifest with the replay and names the one added block; a reader failing on the next scheduled day would also show in that day's fire.

-- 2.0.0_SA_COO~P2
