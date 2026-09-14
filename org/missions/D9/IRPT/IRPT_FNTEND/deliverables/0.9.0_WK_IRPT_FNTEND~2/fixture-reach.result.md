# IRPT_FNTEND.TO-FE-s-33 -- fixture reach: result

Worker `0.9.0_WK_IRPT_FNTEND~2` · issuer `2.0.0_SA_COO~F`
Portal: branch `wk-irpt_fntend-5-2-fe-s-33`, commit **`5067c254`**, based on DEV `c2eb8eb4`. LOCAL; PORTAL IS FROZEN.
Workspace: branch `wk-irpt_fntend-5-2-fe-s-33`, based on CLOUD `0a74710f33`. LOCAL.
Instance: `IRPT_FNTEND.TO-FE-s-33.fixture-reach.proof_of_spec.json`, in this folder.

No capture was taken. This order changes the fixture maps. FE-s-32 re-captures after this drains.

## Criteria

| id | status | deciding line (graded at portal 5067c254) |
|---|---|---|
| F33-AC1 | PASS | `$ tsc -b --noEmit` / `rc=0` |
| F33-AC2 | PASS | `FROZEN MAP, ENVELOPES A VIEW READS CARRYING status: 1 of 1 (performance-report)` |
| F33-AC3 | PASS | `PAIRED: 1 report, 3 views` |
| F33-AC4 | PASS | `HOLDINGS NODES WITHOUT A PARENT CHAIN TO A ROOT: 0 of 12 nodes across 3 maps` |
| F33-AC5 | PASS | `FE-s-26 STATUSES PRESERVED: 3 of 3` |
| F33-AC6 | PASS | `GLOBAL MAP CARRIES HOLDINGS FOR BOTH FIRMS: 2 of 2` |
| F33-AC7 | PASS | ` 47 pass` / ` 0 fail` / `Ran 47 tests across 8 files.` |
| F33-AC8 | RECORDED (judgment) | graded at L9 by 3.0.0_SA_CVO; see the next section |

I also read the whole InvestorReporting suite once, unscoped. At `c2eb8eb4` it was 483 pass, 4 skip, 0 fail across 84 files. After this order it is 494 pass, 4 skip, 0 fail across 85 files. The difference is this cell's 11 tests in 1 file.

## The state given to each envelope, and why (F33-AC8, RECORDED, NO VERDICT)

Every state below comes from the document's own fields, and the reason is stated beside the code that emits it. None was chosen to make a capture look right.

### Frozen report: performance-report -> READY / `REQUESTED_WINDOW_ANSWERED`

This is the one envelope the three paired views read for the frozen report. READY is the only state for which the contract lets a report render as complete (`state/status.ts isCompleteState`). The reasons it is legitimate for this whole report:

- **The requested window is answered to its end.** `dates.actual_end` equals `dates.requested_end`, 2026-09-09.
- **The start differs only by the calendar.** `requested_start` is 2026-01-01 and `actual_start` is 2026-01-02. 2026-01-01 is an NYSE holiday: `lib/trading_calendar.py` gives `is_trading_day` False for 2026-01-01 and True for 2026-01-02 (calendar_source NYSE/pandas_market_calendars). The two dates are both carried, never silently equal, as the schema requires.
- **The body names what it is.** `lineage` carries source revision `bd-2026-09-09` and calculation `calc-rev-49f-000091`.
- **The one absent figure is disposed of inside the document.** The 3Y summary return is null with `absent_reason: NOT_ENOUGH_HISTORY`, which is where the PerformanceReport contract puts a missing fact ("a missing fact stays absent with its reason"). 3Y also lies outside the requested YTD window, so it does not make the window's answer partial.
- **Source dates.** `business_date` is required on an answer-bearing state. It is read from the body's `actual_end`, not typed. The body states no source completion date and no read time, so `source_completion_date` and `as_of` are null. The schema permits null for exactly those two, and filling either in would be a claim the body does not make.
- **Actions.** READY offers none.

**Rendered, not argued.** The frozen performance envelope was driven through `parseIrEnvelope` and then into `ReportingTab` with its own `envelopeFromAvailability`. It renders `data-slot="reporting-body"` with state READY. With the status stripped, the round-4 map, it renders `status-panel` with UNCERTAIN. That is W1-S51 reproduced, and it shows the status is what fixes it.

**The alternative weighed was PARTIAL, citing missing history.** The response contract does say "missing history is an answer". But the history missing here belongs to a metric outside the requested window, and the document already carries its reason. So PARTIAL would describe the window's answer as incomplete when it is not.

### Holdings maps: FE-s-26's three states, carried unchanged

| map | state / reason (FE-s-26, F26-AC9) |
|---|---|
| observed | READY / `OBSERVED_CUSTODY_SERVED` |
| target | UNCERTAIN / `TARGET_BLEND_MODEL_REVISION_UNNAMED` |
| missing-attribution | PARTIAL / `NODE_ATTRIBUTION_UNAVAILABLE` |

They are byte-equal to `git show 0c456933` (F33-AC5). The new root keeps each map's single basis, and keeps the presence or absence of `classification` as its children have it. So FE-s-26's per-map reasoning still holds of every node, root included.

One qualification: the target root is an ACCOUNT node and has no `model_id`. FE-s-26's phrase "every node ... model_id OPAL_MDPF" therefore now reads as "every model node". The reason code, that the target models' revision is unnamed, is unaffected.

### Holdings maps: performance envelope -> the frozen READY (row W2-S26)

`gen-fixtures.ts` builds each Holdings map from the whole frozen map, so these maps carry the same report with the same state. This is disclosed as a row, not special-cased.

### Global map: F-49F and F-CW -> READY / `OBSERVED_CUSTODY_SERVED`

Both are the observed basis's document, and the state is FE-s-26's observed state for that identical document:

- every node OBSERVED;
- classification authoritative;
- provenance measured;
- smartx complete at the business date.

Each envelope has its own operation id and correlation id. F-CW's is the same document re-bound to Cottonwood: `scope.firm_id` F-CW, Cottonwood's issued firm id, account `acct-cw-1`, a synthetic 64-hex fingerprint, and root and drill refs re-pointed. **Its figures are F-49F's and claim nothing about what Cottonwood holds.**

## What changed (portal 5067c254)

1. **W1-S51: `fixtures/smoke/fe-s-18-frozen.json`.** One `status` on the performance envelope, placed before `data`. By parse, nothing else in the map moved.
2. **W1-S52: the three Holdings maps, via `__tests__/fe-s-18/gen-fixtures.ts`.**
   - Before: every node was emitted with `parent_node_id: null`, giving three roots and no edges.
   - Now: one root, an ACCOUNT node for `A-0001` (the scope's one account per `scope.account_ids`), with `N-MODELS`, `N-SMA` and `N-CLIENT` beneath it.
   - The children are level 1, with `of_parent` = `of_total`, because the root is the whole custody total.
   - The view's own `rootNode` now has 3 children, and `breadcrumbPath` reaches the root for every node.
3. **The hazard.** `gen-fixtures.ts` now emits FE-s-26's statuses verbatim (`FE_S_26_STATUS`) in the committed member order (`withStatus`). A regeneration reproduces them and no longer strips them. The committed maps are the edited generator's own output, produced in a scratch copy so it could not rewrite `fe-s-16-print-prehistory.json`, which is outside the grant. For that file the output is byte-identical to the committed one.
   - **Positive control, run before any edit:** the unmodified generator reproduces all five committed maps exactly, once CRLF is normalised and FE-s-26's status removed.
4. **W1-S53: `fixtures/smoke/fe-s-14-global.json`, via the new `__tests__/fe-s-33/gen-global-holdings.ts`.**
   - Two Holdings envelopes, one per firm the map's own resolve-scope catalogue names.
   - F-49F sits on the general holdings key, which is the key the page's request resolves to. F-CW sits on its own account-set route.
   - The two pre-existing keys are byte-unchanged (518 insertions, 0 deletions).
   - The script is idempotent: a re-run leaves the tree clean.

## What these fixtures still cannot show

- **The second firm, from the Global map (row W2-S23).** The page issues one holdings request, for the one scope resolve-scope answers. `ui-smoke.mjs` matches resolve-scope by URL alone, so every firm selection gets the same answer. Measured: `HOLDINGS ENVELOPES THE PAGE CAN REACH FROM THIS MAP'S ONE RESOLVE ANSWER: 1 of 2`. The Global Holdings tab will now show F-49F's tree instead of Failed. It will not show Cottonwood.
- **Target and missing-attribution content.** HoldingsTab mounts its body only on READY. Those two maps render StatusPanel with their own states, which FE-s-26 recorded as row W2-S21. Only the observed map shows the tree.
- **The narrative.** The frozen map's narrative names performance revision `perf-9` (row W2-S27). It is outside the denominator because both preview and print leave the narrative off by default, and no status was given to it.

## Hazards left for the issuer

- **Row W2-S24 (ARMED; disarm owner 2.0.0_SA_COO~F).** `fe-s-14/gen-maps.ts` is the first writer of `fe-s-14-global.json`. Run alone, it deletes the two Holdings envelopes. The order `gen-maps.ts`, `gen-fixtures.ts`, `gen-global-holdings.ts` is written in the header of `gen-global-holdings.ts` and enforced nowhere. The disarm is a change to `gen-maps.ts`, which is outside this grant.

## Surprise rows filed (INVESTIGATION_v2.md)

The W2 plane was re-read across v1 and v2 at mint time (maximum S22). The rows were inserted as text, and the 119 existing rows were verified unchanged.

- `IRPT_FNTEND-W2-S23`: second firm unreachable from the Global map. OBSERVATION, INERT.
- `IRPT_FNTEND-W2-S24`: two writers of `fe-s-14-global.json`. OBSERVATION, ARMED, disarm_owner 2.0.0_SA_COO~F.
- `IRPT_FNTEND-W2-S25`: no scope-level `node_kind`; the root is the scope's one account; `unique_account_count` reads 3. OBSERVATION, INERT.
- `IRPT_FNTEND-W2-S26`: the Holdings maps' performance envelope now carries the frozen READY. OBSERVATION, INERT.
- `IRPT_FNTEND-W2-S27`: the frozen narrative names `perf-9`, not the frozen revision. OBSERVATION, INERT.

## For FE-s-32 (Holdings under the gate)

The observed map now renders the body with breadcrumb `A-0001` and three slices: Models 60%, SMA 24%, Client 16%, all OBSERVED at USD 5,000,000. Target and missing-attribution still render StatusPanel (UNCERTAIN / PARTIAL). On the Global map, clicking Holdings now reaches F-49F's READY tree.
