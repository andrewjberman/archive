# AMGT_RESAPP round 52 -- drain-end packet (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.60, issuance `fb7a8bec00`, on the CTO's round-51 analysis `c5dc123f42`. Six orders, all
terminal. Push state: LOCAL.

## 1. The orders

| cell | risk | holder | close | result |
|---|---|---|---|---|
| ab-1 the D-1 driver splice | LOCAL | ~186 | drain `ffb2a6717f` | AMENDMENT 1 `c7752a8bce` before spawn (CTO msg 27014: the splice records its provenance). `splice_driver` + `--splice-driver`: moves only `thesis_driver` + `thesis_driver_provenance` {analysis key, VersionId}; the served validator accepts it; 127 passed; VALID. Row Z-W186-S1 (AC2's expect text -- the issuer's wording gap) |
| ab-2 every name's dossier block + pack_shape | SERVED | ~188 | drain `5cdc4e1825` | 6501 serves the full block, every field ABSENT with its reason (a broken read stays READ_FAILED); pack_shape passes through (AZN/ADBE pdf, AMD ABSENT); 355 passed; VALID |
| ab-3 the page-FWD mapping | LOCAL read | ~187 | drain `0640ed5a0c` | 9 rows: 8 partly-covers, 1 none (FWD-29's mechanical render check); AC2 JUDGMENT (yours). The CTO executed ruling 4 on it (`44d6bc3e31`): RESAPP FWD-21..29 RE-HOMED to DSGN FWD-12..20 |
| ab-4 the true import comment | LOCAL | ~188 (x2) | drain `5cdc4e1825` | re-opened by AMENDMENT 1 `848821eb39` (a wrapped docstring claim the per-line check missed -- the issuer's check gap); comments + that docstring corrected; VALID. A remaining false clause on harvest.store is row Z-S315 (round 53) |
| ab-5 the own-column gate | LOCAL | ~189 | drain `1f24ab3bf6` | columnar layouts verify by column index; the plant is held, the control 3 of 3, ASML 3 of 3; 122 passed; VALID |
| ab-6 the ONE build + ASML's D-1 splice | WORLD | `0.7.0_AE_CloudOps~A` (respawned 10:43Z: the seat was dead with the GO unread) | entry CLOSED `106ac8a471`, issuer close `86f9373766` | COO half `f8122e4d3f`, CTO half `3ce0240861` (sequenced after CORPUS y-4's leg v, met 10:15Z), conditions `d93731e40e`; pin `a1a70e00eb`, 2 CHANGED of 344; CodeSha `nKWCfQRQ3/lL6cJxgYG3dZr0tcVdOBheeMMNaoWQE+w=` (11:43:22Z); D-1 xUdeA0xU -> qHYfgew8; AC1-AC4 PASS; limbs 5-7 clean |

Worktrees `C:/tmp/r52-186..189`: branches merged, checkouts KEPT pending Andrew's go.

## 2. THE RESULT -- the issuer's real runs on the deployed function, at close

Captures in `round52/captures/ab6_served_*` (true exit codes 0, 0, 0, 0).
- **ASML's thesis-driver chart is SERVED:** source `filing`, 3 points, from the D-1 document's spliced driver (the round-51 AC2 carried
  and met). The move localises to the splice (AE~A: ABSENT before the build, ABSENT after the build, SERVED after the splice).
- **`/thesis` `dossier_fields` for 6501** (no research dossier): the full block, every field ABSENT with "no research dossier exists for
  this name" -- the page can say why.
- **`pack_shape`** passes through for every name with a `/5` dossier (AZN, ADBE pdf; AMD ABSENT with the dossier's reason).
- **The `/5` dossier pick** (CORPUS x-1's METHOD_VERSION): 95 of 95 names read their `/5` object; measured before the GO, 0 names differ
  in any field the adapter serves (93 differ only in `model_rows`, never read).
- **FWD-30** post-deploy: **NOT GRADEABLE at close -- a GRADER reading gap opened by DSGN_AMGTV1 round 12's page (portal DEV `2c01af6a`, 11:52Z), not a value move.** (1) The first close sweep read CAPTURE_FAILED 96 of 96: the grader's `round45/checks/page_render.cjs` stub lacked the page's new hooks (`useModelVersions`, `useInputLedger`, `useModelCompare`); the issuer stubbed them (empty state). (2) The re-run (`round52/captures/fwd30_value_sweep_post_ab6_stubbed_20260930T122939Z.log` + `.tsv`): 32,057 value facts compared, **131 differ, every one a HEADER figure** -- PX_LAST 95, EQY_BETA 35, CURR_ENTP_VAL 1; 1 of 96 names equal. Every sampled line reads the page cell as the displayed figure CONCATENATED with its new hover tooltip (e.g. ASML EQY_BETA page text '1.57' + '1.566303 | RATIO ... | EQY_BETA ...'; PX_LAST 'EUR 1503.20' + '1503.2 | PRICE ...'), i.e. DSGN r12's 'every figure is one hover from its serve' puts the tooltip inside the value cell and the grader reads both. No non-header fact differs; scale-unchecked stays 0. AE~A's limb 6 (/print byte-equal on four names across ab-6) held. The issuer did NOT re-tune the FWD-30 grader at close (it is the instrument that grades the outcome); the grader's displayed-value read is carried as a round-53 cell (section 5).

## 3. Judgment criteria

- **ab-3 AC2 (yours):** each mapping row's `relation` follows from its two quotes read side by side
  (`deliverables/0.9.0_WK_AMGT_RESAPP~187/PAGE_FWD_MAP_ROUND52.json`).

## 4. Rows this round (L8 input)

- **Z-S313** (issuer): a D-1 regeneration drops served sentences (ASML measured) -- round 52 splices instead.
- **Z-S314** (issuer, ARMED): the rebuild regression is a DEFECT carried to round 53 as its own cell (CTO msg 27014).
- **Z-S315** (issuer): the ~:2175 docstring still says harvest.store is unavailable in the deployed package (false; text only).
- **Z-W186-S1** (~186, INERT): ab-1 AC2's expect text still said "only thesis_driver" after AMENDMENT 1 -- the issuer's wording gap.

## 5. Carried to the CTO's round-52 analysis

1. **Z-S314:** the D-1 rebuild that drops served sentences, as its own cell.
2. **Z-S315:** a one-line text correction of the harvest.store clause.
3. **HARVST q-5's `timeline_api` change 91b74a9047** (`/timeline` `publishers_found_codes`) rides the round-53 build (CTO msg 27123).
4. **The slash security_key ruling** (CTO msg 27108, `c9081e03d6`): CORPUS round-24 cell 4 routes the scoped API's pool reads through
   `crosswalk.slash_safe_key`; the 30-object move rides round 25's API deploy -- RESAPP's files are consumers, to sequence.
5. **The FWD-30 grader reads the DISPLAYED value on DSGN r12's hover figures** (section 2): 131 header facts differ only by the
   tooltip text inside the value cell; the grader's page parser must read the visible figure, not the cell's whole text. Also the
   renderer stub for the three new hooks (committed with this packet).
6. **Instrument note:** `to-check.py` reads the FIRST `<status>` tag, so orders whose flips were appended (tt-2, uu-4, vv-4) read
   `pending` though complete; the respawn pre-flight read their LAST tag.
