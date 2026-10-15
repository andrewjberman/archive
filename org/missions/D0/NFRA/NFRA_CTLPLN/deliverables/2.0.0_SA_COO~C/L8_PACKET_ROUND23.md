# NFRA_CTLPLN round 23 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-15 ~23:3xZ)

Round 23 is terminal: three orders `complete` (issuance `4073337a9e`; decomposition `NFRA_CTLPLN_DECOMP.round23.md`; merges `a9e9fa8b00`, `0efcd4e8c0`, `a3c8d40ddc`; flips `701fce0d3b`, `23cc90fb83`, `627030e083`). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 23` reads `verdict=MAY-CLOSE`, `orders=26 judgment=2 graded=2 ungraded=0 self_graded=0`. Pins are commits on `box/laptop`, LOCAL (push is `0.0.0_AB_MSTR`'s). Inputs for the analysis: `ROUND23_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 1. Judgment criteria owed to the CVO

None.

## 2. Cells, their orders and the issuer's own re-run

| cell | FWD | merge | issuer re-run |
|---|---|---|---|
| `CT-am-1` | 15, 16, 18, 19 | `a9e9fa8b00` | worker tree: `RECEIVE-COLOR arms=15/15 ok=True`; `INTAKE-RECEIVE-TEST cases=32/32 ok=True` (base 30); the worker's negative control grades the coloured `adbc_driver_duckdb` error `failed` at the base |
| `CT-am-2` | hygiene | `0efcd4e8c0` | worker tree: `HYGIENE-GUARD arms=6/6 ok=True`; `HYGIENE-CHECK8 awaiting=True release_refused=True ok=True`; `HYGIENE-LEGACY device=laptop requests=8 files=2 attributed_by=batch unattributed=0 ok=True` |
| `CT-am-3` | hygiene | `a3c8d40ddc` | worker tree: `HYGIENE-MERGE arms=5/5 ok=True`; `HYGIENE-SPARSE crossbox_cases=69/70 ok=True` (one skip, reason printed); main tree after the merge: `CROSSBOX-TEST cases=76/76 ok=True` |

Every proof instance reads VALID in the main tree after the merge. Diff paths of each branch are inside its order's `<paths>` (read per branch). The three criteria of `CT-am-2` and the two of `CT-am-3` were run in the worker's sparse tree, not repeated in the main tree; only `CT-am-1` and the crossbox suite were read there.

## 3. What each outcome now stands at (evidence, not a grade)

- **The package journey (FWD-15, 16, 18, 19) reached its end on dell1.** Call `XB-20261015T222313Z-90f0` (re-run with colour off) was acknowledged by `1.0.0_SA_CTO~DELL1` at 22:57:54Z (carried by `0.0.0_AB_MSTR`, msg 109535): `prove` read `import_missing_dep=1 failed=0 refused=0 ok=True`; `install --dry-run` `installed=0 dry_run=True ok=True`; `install --target` `installed=1 refused=0 ok=True`; the import from TARGET prints `1.5.0`. The lane `2.0.0_SA_COO~D1` ran its one read-only query; the issuer read the record itself from `origin/box/dell1`: `org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round11/ENRICHMENT_READ_SLEEVE_20261015.md` @5e43159dd9. Its answer: `sma_additive_aua` moved on 26 of 26 consecutive total-bearing day pairs (median $1,875.73, max $355,920.93) and is absent after its first value on 7 of 35 total-bearing dates (2026-08-31 .. 09-09). It writes nothing to S3 and adds no dependency; duckdb stays in TARGET outside git. **Not read by the issuer:** dell1's own terminal output (the CTO's note carries its last lines); the 7-date window versus the earlier CN-r-1 reading of the Total (the lane says it did not re-test it). The call's from-half is closed (`c80d1bea8d`); the CVO's read-back is the remaining step, and Andrew's read-out `318f` can now be given from that record.
- **`CT-am-1`'s tool change** reaches dell1 only after dell1 pulls it. The journey did not need it.
- **FWD-14:** dell1's call `2765` and dell2's `6c75` (carried 21:22Z, 21:23Z): the Security log (event 4625) is UNREAD on both (the shell is not elevated); the remote connection manager log holds 0 of 18 (dell1) and 0 of 20 (dell2) events carrying `100.96.167.100` in the window 2026-10-10 13:00Z to 10-13 14:00Z; firewall dropped-packet logging is off on both. No negative proof either way. `c9a4` and the CTO's laptop act `b87f` stay open for Andrew; an elevated Security-log read needs his word.
- **FWD-11:** `ib549` was NOT interrupted (L1 landed 15:19-15:21Z, before the 15:46Z restart; L2-L5 fire 2026-10-16 14:15Z); dell2's manager reports `0.7.0_AE_CloudOps~IB2` LIVE on dell2.
- **Hygiene:** the map build refuses a linked worktree, a sparse tree and a tree without `portal/`, and the header names `built_from_head`, `portal_sha`, `edge_count`; the committed `nerves-risk-edges.json` keeps its old header until the next main-tree build. An unsigned check 8 is recorded as awaiting and the release refuses with that reason. The two real 20261008 fetch records count for the laptop by a batch declaration (`DEVICE_OF_BATCH.txt`).

## 4. FWD state

CTO table entering the round: REALIZED 1, 3, 5, 24, 28; ADVANCED 2, 4, 6, 7, 8, 10, 11, 12, 14-19, 21, 22, 23, 25, 27; PARKED 9; MOVED 13, 20, 26. This packet grades none. Calls `c9a4`, `b87f` (FWD-14) and `318f` (FWD-17) open for Andrew.

## 5. Rows this round minted and the rulings on them

`W123-S1` (the commit gate's client-data check reports NOT checked on this box, the hashed account-id list is absent; OBSERVATION, INERT). `W124-S1` (the CTO signer folder is outside the sparse cone, so the journey `--check` reads ok=False in a sparse tree until it is added), `S2` (an 8.3 short tree path failed a compare against git's long name and refused a full main tree; fixed with `os.path.samefile`), `S3` (the order's "laptop seat" has no defined source; both real fetch records name `2.0.0_SA_COO~C`, listed in `org/devices/state/laptop/seats.json`; the declaration rests on that). `W125-S1`, `S2`, `S3` below. All OBSERVATION, INERT.

**Dispositions of the carried rows this round touched:**
- `S9121` (the merge verb dropping a null bus id): worker `~125` could NOT reproduce it at base `4073337a9e`; the merge already keeps a null bus id and validates before any write. Five arms now pin that behaviour (a write-before-validate mutant reads `4/5 ok=False`). Issuer reading: the carried claim was wrong at the base or fixed earlier; the row is closed on that basis, from the worker's measurement and my re-run of the arms, not from my own reproduction of the original drop.
- `W79-S2` (the crossbox suite in a sparse tree): the failing case read `org/mcp`, a folder the sparse set lacks, not origin state (`W125-S2`); the suite now skips that one case with a printed reason. Done-when "50/50 on two boxes" is measured on this laptop only.
- `W111-S1` (fetch records unattributed): resolved by `CT-am-2` (attributed by the batch declaration, 0 unattributed).
- `W119-S1` (check 8 recorded as failed when unsigned): resolved by `CT-am-2` (awaiting).
- `W121-S3`/`S4` (the build guard has no portal check; the edge count differs by tree): the guard and header landed in `CT-am-2`; the CTO, as the map's owner, reads whether the rows close at the next main-tree build.
- `S9105`, `S9101`: read and answered in the decomposition (`5e5e9db7a9`, `5882eb4273`).
- `W125-S3`: the order's literal `wk-provision.sh provision NFRA_CTLPLN 125` names the worker's own branch, so the test provisions under serial `125s<pid>`.
- Carried, owner and condition unchanged: `W8-S7` (an infra path, WORLD by the path floor, owes the CRO's research before a cell), `S9103`, `S9120`, `W89-S3`, `W12-S1`, `Z-S3` (before 2027-12-01), `S9125` (dell1, before 2026-12-31), `S9119`, `S9128`.

## 6. Not measured here

The Windows-laptop remote-desktop arm and the off-tailnet refusal (FWD-14); the Security log on any box; the CVO's read-back of the dell1 journey; whether `CT-am-1`'s tool change behaves on dell1 (it has not been pulled there); the CVO's own re-grade of the FWD table.
