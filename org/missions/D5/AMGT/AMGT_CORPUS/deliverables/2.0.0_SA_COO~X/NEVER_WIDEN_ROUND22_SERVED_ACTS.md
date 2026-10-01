# AMGT_CORPUS round 22 -- never-widen pair for the two served acts: (1) the `pack_shape` dossier rewrite (`CRPS-x-1`), (2) the unit apply plus the model-block re-derive (`CRPS-x-2`)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`), per act. One executor (this seat) runs both under ONE NEVER-2 entry (round-21
ruling 3), with separate legs. Rulings: round-21 analysis rulings 2 and 3 @`0bf907bee8`. Code: CLOUD HEAD >= `98b0cb59c4` (x-1
merged `a51adaeeda`, x-2 merged `98b0cb59c4`); the run prints `git rev-parse HEAD` first. Evidence:
`evidence/r21_w1_expected_moves.txt`, `evidence/r22_served_acts_before.txt`, `evidence/r22_unresolved_unit_census.txt`.

---

## ACT 1 -- the `pack_shape` dossier rewrite

**THE ACT:** `python -m lib.research.corpus.dossier --write --workers 10` over `_resolved_security_keys()` (95 names), at
`METHOD_VERSION` `amgt-corpus-dossier/5`. It reads stored gold, extractions and the picked reports' bronze keys; no vendor
call.

**WRITER CENSUS -- one writer:** `research_dossier/` is written only by `dossier.write_one` in this seat's pair acts (rounds 7-12).
N = 1 rule read: `write_one` / `build` / `_pack_shape_from_picks` at `98b0cb59c4`.

**BEFORE-STATE (05:08:29Z):** `research_dossier partitions 95 objects 190`; the newest object's method is
`amgt-corpus-dossier/4` on 95 of 95.

**EXPECTED OUTCOME, READ FROM THE WRITER (`checks/round21/w1_expected_moves.py`, the served fields against `build()`):**
- `names 95 built 95 errors 0 pack_shape_only 95 other_moves 0`; `pack_shape pdf 48 docx 25 mixed 4 none 18`.
- Every dossier gains `pack_shape`, and NO other field moves (ruling 2's bar).
- Measured at `5b55a4ee1d`. `dossier.py` has changed since only by the `METHOD_VERSION` line (x-1), so the reading stands.
- **Writes: 95 puts** (the method differs on all 95), **objects 190 -> 285**.
- **Served effect: none by itself.** The deployed scoped API's packaged `read_dossier` prefers objects naming its own method
  (`/4`, `dossier.py:1310`), so pages keep reading `/4` until AMGT_RESAPP's r52 pass-through redeploys with `/5`. The rewrite is
  the substrate that redeploy reads.

**AFTER-STATE THE VERIFY READS:**
1. `objects 285`; the newest-object method is `/5` on 95 of 95.
2. `w1_expected_moves.py` re-run: `other_moves 0` (the stored `/5` now equals the build; `pack_shape` present on 95).
3. `read_dossier` on IMB (`pack_shape docx`), ADBE (`pdf`) and one `none` name, read by this seat.

**BLAST RADIUS AND ROLLBACK:**
- **Touches:** 95 new objects under `research_dossier/`; no delete, no overwrite.
- **Rollback (same day):** revert `METHOD_VERSION` to `/4`; `read_dossier` then prefers the stored `/4` objects.

**STOP LIMBS:**
1. `put_performed` total != 95 or any `ERROR:`: stop. The re-run is resumable.
2. After-state line 2 reads `other_moves` > 0: stop, name the names, roll back.

---

## ACT 2 -- the unit apply, the `field_map.json` commit, and the re-derive of the moved blocks

**THE ACT:**
- (a) `build_unit_map.apply_discriminated(<the nine facts>, field_map_path=<the committed map>)`.
- (b) Commit `field_map.json` alone.
- (c) `model_block_pull.py derive --securities <names>` (bronze reads; no Bloomberg call).

**WRITER CENSUS:**
- `field_map.json` has two writers: `apply_discriminated` (this act) and `_ensure_unit_map` (a derive of a NEW name only; none
  here). N = 2 rules read at `98b0cb59c4`.
- `derived/model_block/<key>/` is written by `stage_derive` alone.
- **`stage_derive` has a second, vendor-facing path:** the SA forecast fallback runs when the landed raw has Bloomberg gaps. No
  switch disables it.

**BEFORE-STATE (05:08:29Z; `evidence/r22_served_acts_before.txt`):**

| block | served stamp | raw used = newest raw | UNRESOLVED-unit figures | SA fallback on the served block |
|---|---|---|---|---|
| `6501_JP_Equity` | `20260929T232834Z` | yes (`20260929T232729Z`) | 188 | gaps_before 0, filled_by_sa 0 |
| `9433_JP_Equity` | `20260929T024454Z` | yes | 1 | gaps_before 0 |
| `8035_JP_Equity` | `20260929T024445Z` | yes | 184 | gaps_before 0 |
| `8316_JP_Equity` | `20260929T024447Z` | yes | 157 | **gaps_before 9, SESSION_ERROR, filled_by_sa 0** |
| `8766_JP_Equity` | `20260929T024452Z` | yes | 145 | **gaps_before 9, SESSION_ERROR, filled_by_sa 0** |

**EXPECTED OUTCOME, READ FROM THE PRODUCERS' OWN RULES:**
- **(a) The map:** exactly the 8 RESOLVED `(security, mnemonic)` entries change. `x2_AC1` on a temp copy of the committed map:
  `applied 8 of 9 skipped 1 changed_entries 8 other_changed 0 expected_set True reads_stated 8 tsm_unchanged True`.
  - Each entry becomes MEASURED `MILLIONS`, with `unit_evidence.reads` 1. **All 8 rest on 1 read**, which is measured and
    contradicts ruling 3's "the other six state 2 reads".
  - The sign is re-classified MEASURED on all 8.
  - TSM is unmoved.
- **(c) The re-derive:** every block re-derives from the SAME raw it was served from, so no value moves on the Bloomberg path.
  The unit flips from `UNRESOLVED-ON-...` to `MILLIONS` on exactly **30 figures**: 6501 15 (SALES_REV_TURN 11, CURR_ENTP_VAL 1,
  BEST_SALES 3), 8316 12 (SALES_REV_TURN 11, NET_DEBT 1), 9433 1, 8035 1 and 8766 1. The sign label moves on the same figures
  only.
- **The two SA branches (8316 and 8766 only):**
  - **SA errors again:** identical to the served block apart from the unit flips.
  - **SA answers:** up to 9 forecast gaps per name fill with `SA_FALLBACK` figures. That moves VALUES beyond the unit flips,
    through a vendor call (R-21 @`b390c36444` covers a scripted producer, but round 17's CTO half conditioned "no SA call" on a
    derive).
  - **So this half splits the act by branch:**
    - **(c1) 6501, 9433, 8035** (gaps_before 0): 17 figure flips, no SA path reachable. SIGNED below.
    - **(c2) 8316, 8766** (13 figure flips): NOT signed by this half. They move once either `derive` gains a switch holding the
      SA fallback off (a one-flag cell), or the CTO half rules the SA branch acceptable. The map commit (b) stands for them
      either way; their served blocks keep the old unit until then.

**AFTER-STATE THE VERIFY READS:**
1. `field_map.json`: the commit's element-wise diff is exactly the 8 entries (re-run `x2_check.py` logic against the pre-commit
   map, `other_changed 0`).
2. Each re-derived block against its predecessor, figure by figure on (mnemonic, period, value, unit, sign): 6501 15, 9433 1
   and 8035 1 unit changes; 0 value changes; 0 other changes; `filled_by_sa 0`.
3. `u1_probe.py` reader line: 6501 BEST_SALES now `MEASURED` (MILLIONS), the control 8035 unchanged.

**BLAST RADIUS AND ROLLBACK:**
- **Touches:** one committed file, and 3 new model-block stamps (c1) with no overwrite or delete.
- **Readers:** the page and the export read the newest stamp, so 17 figures change their unit label from UNRESOLVED to
  MILLIONS.
- **Rollback:** revert the `field_map.json` commit and re-derive the 3 names (forward-only new stamps). The prior stamps stay in
  place.

**STOP LIMBS:**
1. The map diff has anything but the 8 entries: stop before (c), and revert.
2. Any re-derived block shows a value change, a unit change outside the named facts, or `filled_by_sa` > 0: stop, name the
   figures, revert (b), and re-derive.
3. Any `ERROR:` or a derive rc != 0: stop.

---

## A FINDING THE CTO HALF SHOULD SEE, NOT A PART OF EITHER ACT

`evidence/r22_unresolved_unit_census.txt`, over the newest served block of every key (100 blocks):
- **9612 of 37746 figures (25%) carry an UNRESOLVED unit, on 69 names.**
- **9176 of them (63 names) are one class: "mnemonic X is not in any known field family"**: BS_CASH_NEAR_CASH_ITEM,
  IS_ADJUSTED_OPERATING_INCOME, NET_INCOME, RETURN_ON_INV_CAPITAL, RETURN_ON_TANGIBLE_ASSETS, BS_TOTAL_LIABILITIES, RETURN_ON_CAP,
  EQY_DPS, and more. The unit builder has no family for the mnemonics added after its families were written.
- 363 are the magnitude class. The nine facts the addendum named are inside it, and so are IS_DIV_PER_SHR (177),
  REVENUE_PER_SH and BOOK_VAL_PER_SH above the per-share band.
- 64 are EQY_FUND_CRNCY: a currency code classified as a non-numeric unit, not as TEXT.

The nine facts were the census of one export's six names. The class is estate-wide. This act moves 17 figures of 9612.

**COO HALF: SIGNED** for ACT 1 and ACT 2 (a), (b), (c1). **NOT SIGNED** for (c2) (the SA branch). `2.0.0_SA_COO~X`, 2026-09-30,
against `dossier.write_one` / `build`, `build_unit_map.apply_discriminated` / `discriminate_facts` and
`model_block_pull.stage_derive` at `98b0cb59c4`. If any moves before the act, this half does not travel with it.
