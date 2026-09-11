# WIP / WIND-DOWN HAND-OFF -- IB-rt-7

**Written by:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-2-1` | **worktree:** `/c/tmp/wk-irpt-2-1`
**Written for:** a SUCCESSOR with none of my context, under the managed wind-down of 2026-09-11 ~17:30Z.

---

## 1. STATE: IB-rt-7 IS COMPLETE. NOTHING IS IN FLIGHT.

**There is no open ledger, no half-landed deploy and no uncommitted work of mine.** The order's
`<status>` is flipped to `complete`, its proof-of-spec instance is VALID (rc=0), and RT7-AC1
passes by output.

If you are reading this to decide whether to finish something: **you are not.** Read section 4
before touching anything.

| thing | state |
|---|---|
| `irpt-holdings` Lambda | **LIVE**, `CodeSha256 yOiMCrewFEMtE6GCJzBjNdLQsRpliY8zrM3t1AMyynI=`, handler `snapshot.lambda_handler`, layer `irpt-common:5`, role `irpt-holdings-role` |
| the holdings route | **LIVE** on api `7k3ed8px20`: `GET /api/scoped/investor-reporting/holdings/{accountSetId}` -> `integrations/6ouz1v4`, `CUSTOM`, authorizer `naqxlm` |
| deploy ledger `irpt-bckend-rt7` | **CLOSED**, 4 of 4 legs proven, 0 open; sentinel committed at `2f0cb688de` BEFORE the act, removed by the close at `5a359024a9` |
| terraform roots `holdings` and `api` | both plan `No changes.` |
| QA snapshots, 3 firms | rebuilt and landed under `investor-reporting/qa/holdings/` |
| battery | `IBRT7-HOLDINGS-SERVED`, rc=0, five arms, byte-identical across two runs |

## 2. THE LAYER QUESTION, ANSWERED -- DO NOT REDO IT

The issuer amendment made a rebuild of `irpt-common` this order's FIRST ACT.

- **Version READ at my cut: `irpt-common:5`. Version PUBLISHED by me: NONE.**
- **Why:** the amendment's own escape clause ("if the live version already carries every
  declared member when you start, record that and repoint only") applies, and it was MEASURED,
  not assumed. The live `:5` carries **9 of 9** members the merged tree declares -- 5 of 5
  contracts, `python/ids.py`, `python/raw_keys.json`, `python/keys.py`,
  `python/firm_registry.json` -- and **3 of 3** consumer functions
  (`irpt-performance-adapter`, `irpt-narrative`, `irpt-export-render`) were already on `:5`.
  There was nothing to repoint and no capability missing.
- **The residual:** `carried_forward_members` in
  `infra/aws/lambda/layers/irpt-common/build_layer.py` is now pure duplication (it contributes
  **0** packaged paths the other declared lists do not already carry, at identical pins), so
  removing it **changes zero deployed bytes**. It is NOT in this order's `<paths>` grant.
  Filed as **row `IRPT_BCKEND-W1-S14`** (BLOCKING, INERT, disarm owner `2.0.0_SA_COO~B`).
  IB-rt-4 (slot ~3) rebuilds this layer in its own arm (e) and holds the surface.

**`irpt-holdings` is a FOURTH consumer of `irpt-common`,** attached by data source, so it lands
on whatever the latest version is at apply time. A future layer publish does not require
re-applying the holdings root unless you want the function moved that instant.

## 3. WHAT IS DONE, ARM BY ARM

All five RT7-AC1 arms hold; the evidence is in
`the-holdings-handler-and-the-attribution-holdouts.result.md` and
`IB-rt-7_RT7-AC1_battery_output.txt`. In one line each:
(a) route live under `naqxlm`, 12 of 12 DECLARED, 0 of 1 unguarded, slice schema-valid, six
swaps 6 of 6 refused on the FIRM_ADVISOR plane (5 of 6 on FIRM_OPERATIONS -- see row W1-S16);
(b) one basis per node, holdouts visible (INF 84 / $7,193,856.71, COT 10, 49F 0), before ==
after to the cent, and the redistributing build FAILS while still reconciling;
(c) both clocks on N of N nodes for all three firms, COT's differing by a day, collapse and
re-date fixtures both refused;
(d) `:acct:` 0 everywhere, INF joins 874 of 874;
(e) CodeSha256 equal by content, both roots 0-diff, ledger CLOSED.

## 4. WHAT MUST **NOT** BE RE-DONE

1. **Do not re-publish `irpt-common`.** See section 2. `:5` is correct and complete for every
   declared member. A republish would destroy the live version (`aws_lambda_layer_version`
   REPLACES) for no gain -- that hazard is row `W1-S12` from IB-rt-3.
2. **Do not re-apply either terraform root.** Both plan `No changes`. Re-applying the api root
   is not harmful but is not needed, and the holdings root's apply is what created the live
   function.
3. **Do not re-open the `irpt-bckend-rt7` ledger.** It is CLOSED with all four legs proven. An
   entry a device left open proves only that THAT device saw no completion -- this one is
   committed closed at `5a359024a9`.
4. **Do not rebuild the QA snapshots to "check".** They are landed and the battery reads them
   back through their own pointers. A rebuild costs ~25 minutes of parquet reads on 49F and
   changes nothing; if you want the numbers, run the battery.
5. **Do not "fix" `_authz.Enforcer.covers()`** (row W1-S16) or **`build_layer.py`** (row
   W1-S14). Both are outside this order's `<paths>` and both are recorded for the issuer to
   route. Never fix a neighbouring defect.
6. **Do not flip anything else to complete.** IB-rtb-1 was NOT begun, per the wind-down.

## 5. THE ONE THING A SUCCESSOR SHOULD KNOW THAT IS NOT AN ARM

**The deployed route reads the PRODUCTION prefix (`investor-reporting/holdings`), and the
holdouts exist only in the QA artifacts this cell rebuilt.** That is deliberate -- this order's
bound forbids overwriting a production artifact -- but it means the live route currently serves
the PRE-HOLDOUT production snapshot. A production rebuild on the new runner belongs to whichever
cell owns the production build; it is named in the instance's `declared_exclusions` so it cannot
be discovered by surprise. The handler needs no change when that happens.

## 6. COMMITS ON THIS BRANCH (all LOCAL, never pushed)

| hash | what |
|---|---|
| `d9c940244a` | sources: handler, terraform root, contract flip, runner holdouts, tests |
| `2f0cb688de` | the OPEN sentinel, committed BEFORE the act |
| `5a359024a9` | the deploy, the staged package members, the CLOSED ledger |
| `5f68db528e` | the battery, its output, row W1-S16 |
| *(this commit)* | result.md, the VALID proof-of-spec instance, PATH_MANIFEST rows, the `complete` flip, this file |
