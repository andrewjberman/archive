# AMGT_CORPUS -- round 23 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~10:3xZ.**
- ONE issuance on `1.0.0_SA_CTO~Z`'s round-22 analysis (`a940eb6813`): decomposition v23.0, `bbf33b05b4`, merged `46540fd5f6`.
- AMENDMENT 1 (cell y-5) on the CTO's VERDICT B (msg 27053, CVO~Z msg 27051), cut as a MODIFIED TO-CRPS-y-2 (`a03487b604`),
  plus AMENDMENT 2 (`bd28136864`).
- All four cells are complete and re-graded by this seat. The WORLD act y-4 landed under two pairs, and its ledger is CLOSED.

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 4 cells complete, drained

| order / cell | the build | drain | this seat's run at the tip |
|---|---|---|---|
| `TO-CRPS-y-1` | unit families by census (23 unfamilied -> 0, each placed on its FIELD_BASIS text); `EQY_FUND_CRNCY` TEXT; per-share by a same-currency `|v|/PX_LAST` band | `988d0ecfc7` | AC1 `after unresolved 622 pointer_after 0 no_family_after 0 crncy_after 0 per_share_after 199`; AC2 30 passed |
| `TO-CRPS-y-2` | `derive --no-sa-fallback` (the loader is never called; gaps `HELD_OFF`) | `e727eaf6aa` | AC1 dry-run `sa_fallback held_off`; AC2 10 passed |
| `TO-CRPS-y-3` | `unit_anchor.same_currency_anchor` (same-LEI line, or a stored FX object with its date; never invented) | `9d4d373916` | AC1 `tsm anchor none searched 10 reason_set True fx_invented False control_sap anchor CUR_MKT_CAP`; AC2 4 passed |
| `TO-CRPS-y-2` AMENDMENT 1+2 = `CRPS-y-5` | `_resolved_sign` classifies each figure from its OWN value; a superseded test assertion ruled (`Z-W2-S17`) | `94301d5a9c` | AC3 `plain_disagree 0 convention_disagree 0` (base 1568/1); AC4 15 passed |

The issuer's hookup (`a3c4775d7c`) wires `discriminate_facts` to the anchor, fail-closed. Drain hygiene: 170 passed.

## 2. The WORLD act y-4 -- ledger `amgt-corpus-r23-unit-families` CLOSED (all 5 legs proven)

Pairs: COO `13f78a2b1b` / CTO `badff0ef3b` for the units; COO `79ea7ae4ae` / CTO `bb3280c97e` for the signs.

| leg | result |
|---|---|
| a | the map rebuild (PYTHONPATH per CTO condition 1): 3,012 entries across 66 fields, 0 shared, +NVDA, 0 top-level, the 8 round-22 entries unchanged |
| b | map commit `67568b59c4` |
| c (units) | 97 blocks (in batches of 3; the derive cap refused one 97-name call, which wrote nothing): unit changes **15,425 = expected**, 0 value moves, `filled_by_sa 0` |
| c -> **stop limb 2** | unmodelled: sign labels contradicting their own value went 886 -> 1,568 on 49 blocks, and the `cases.base.formula` text changed on 67 blocks. Leg d held; escalation `c68c2a6dfd`; row `Z-S68`; VERDICT B. |
| s (signs) | 50 blocks: **50 of 50 match**, 1,569 sign changes = expected; 0 unit, value or case changes. Landed 09:40Z, inside the 12:00Z bound, so A was not executed. |
| d | 93 dossiers written (287 -> 380), 0 errors |
| v | served census UNRESOLVED 612, POINTER 375, no-family 0; y5 0/0; dossier re-read `other_moves 0` on 95; the CTO's served read (below) |

**The served effect, before round 23 -> now, over the newest block of 100 keys:**
- **not-measured units 16,052 (42.5%) -> 987 (2.6%);**
- **sign labels contradicting their value 1,569 -> 0 on the 97.**

The remaining pointers sit on BP/_LN and NG/_LN, excluded under `Z-S64`.

**The served read (CTO condition 6):** the deployed `opal-amgt-scoped-api` (CodeSha256 `zHpr7FhS...`) `/thesis` for BA_US_Equity
serves PROF_MARGIN-2020 `NEGATIVE` with NET_INCOME-2016 `MILLIONS`. Of BA's three stamps, only `20260930T093755Z` carries both:
`024521Z` has the pointer unit, and `083927Z` has the wrong POSITIVE.

**The formula text (CTO condition 1):** `case_rule` computes from BEST_EPS, so "Bloomberg consensus EPS (FY1, BEST_EPS) ..." is the
true text (AMGT_RESAPP `vv-1`) and is kept.

## 3. Corrections and defects this seat owns

1. **The 25% census was an undercount.** It counted only the UNRESOLVED prefix; the pointer class made the true figure 42.5%. This
   was corrected at L5 and sent to the CTO.
2. **The y-4 pair's writer census traced unit paths only.** It missed the per-figure sign semantics (`Z-S68`) and `case_rule` as a
   second input. Stop limb 2 caught both before leg d.
3. **y-5 came to this seat as a MODIFIED order.** The to-pipeline-gate's "one issuer per round" limb refuses a new order file in a
   round that already has an issuance, and reads no override.

## 4. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-S68` (new) | answered by y-5 + (s) | sign per figure; 0 contradictions served on the 97 |
| `Z-W2-S17` (new) | ruled (AMENDMENT 2) | a superseded test assertion |
| `Z-W2-S16` | carried | TSM: the anchor mechanism is landed; no stored anchor today |
| `Z-S64` | carried, widened | BP/_LN and NG/_LN are excluded from the unit pass as well; their raw-freshness read is untrusted |

## 5. Enrichment candidates for the round-23 analysis

1. **The 622 still-UNRESOLVED figures.** 199 are the per-share names outside their band (currency mismatches, or no PX_LAST); the
   rest are magnitude or other reasons, measured by class in `r23_y4_before.txt`.
2. **BP/_LN and NG/_LN (`Z-S64`):** a trusted raw-freshness read, then the same passes.
3. **The dossier `/5` objects** reach pages only with AMGT_RESAPP's r52 redeploy (`pack_shape` and `model_rows`).
4. **The r-1 acceptance** is read at the 13:00Z fire today.

## 6. Bounds and residue

- No Bloomberg call, no SA call, and no vendor call.
- Drained worktrees `wk-crps23-1/2/3/5` were removed with their branches kept (Andrew 02:5xZ, `8c4f79e531`).
- `2.0.0_SA_COO~Z` was told leg v passed (10:32Z), so AMGT_RESAPP ab-6 may start its captures.
