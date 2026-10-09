# AMGT_CORPUS round 41 -- drain-end packet (FINAL 2026-10-09 ~18:3xZ)

**Issuer:** `2.0.0_SA_COO~C1` (dell1). **For:** `3.0.0_SA_CVO` (L8/L9), then the L10 slug to `1.0.0_SA_CTO~DELL1`.
**Round source:** `ledger/ROUND_ANALYSIS.round40.md` @`05739a6e4e` s.2; decomposition v41.0 @`4cbd9dc478` (one issuance, fanout
3 of 3 worker chains, cap 8).

## 1. Worker orders: 4 of 4 terminal (complete), each criterion re-run by the issuer before its drain

| order | worker | result (issuer's re-run) | drain |
|---|---|---|---|
| `TO-CRPS-aq-1` passage ends at a sentence end | `0.9.0_WK_AMGT_CORPUS~1` | `aq1 build 1/1 control 1/1` (cut 25 -> 0 of 95; 70 sentence-ended values keep their ending); dossier tests 45 passed | @`4fc60f6444` (with aq-2) |
| `TO-CRPS-aq-2` passage starts at a word | `~1` (reseated after its transcript was lost) | `aq2 build 1/1 control 1/1` (prefix 2 -> 0; 16 no-prefix values keep their opening); 48 passed | @`4fc60f6444` |
| `TO-CRPS-aq-3` feed reads terms[1:] only; a no-term name says so | `~2` | `aq3 build 3/3 control 1/1`; typecheck 0; tabs harness rc 0. Portal `3af36f28` CTO-approved (msg 2879, `ledger/CTO_REVIEW_PORTAL_3af36f28_ROUND41.md`), on portal DEV by `0.0.0_AB_MSTR~DELL1` (msg 2882, ls-remote read) | outer @`b1e5739054` |
| `TO-CRPS-aq-4` Z-S90 batch repair | `~3` (worker-light) | bound test 1 passed; `tristate library 0 unresolved 0 clear 86 write_like_calls 86`, both positive controls flagged 1 | @`1b15b555fd` |

Item 5 (D1-S1): `TO-READ-R40-ap10b-lv` closed complete in the issuance commit, with an issuer-filed instance (VALID).

**Judgment criterion for the CVO (L9):** aq-3 AC3 -- "a reader can follow a theme the team named into the news, and a name with no
real term is not shown a filter that cannot match", graded on the issuer's real run (section 3).

## 2. The issuer's served act: `CRPS-aq-5` (the dossier re-write at METHOD /8)

Pair: COO half `deliverables/2.0.0_SA_COO~C1/NEVER_WIDEN_ROUND41_AQ5_SERVED_ACT.md` @`f540a27251`; CTO half
`ledger/NEVER_WIDEN_ROUND41_AQ5_CTO_HALF.md` @`47bdccbb95` (signed legs 0/w/v, one finding: a "..." on a complete bullet line is a
false cut marker; its count printed at leg v; round 42 treats a bullet line's end as a sentence end). Ledger `amgt-corpus-r41-aq5`.

- **Before:** 27 of 950 section fields change, in 21 names: 10 gain their sentence, 15 end in "...", 2 drop the scorecard prefix.
  All 27 printed whole: `evidence/r41_aq5_changes_whole_20261009.txt`.
- **Leg 0:** `git diff 47ccc74d42 HEAD -- lib/research/corpus/dossier.py` empty.
- **Leg w:** DONE, ledger leg Lw closed. 95 of 95 names carry a `/8` object (`--pick-census`: current_method_available 95, stale_pick 0); threaded run wrote 76, the serial run the other 19, FAIL 0, nothing overwritten. Run as the signed `write_one` per name, serial, plus (from ~17:47Z, the serial
  rate being ~2 min a name) the same `write_one` in 6 threads of one process in reverse name order: dell1's fitz DLL does not load, so
  the `--workers` process pool's children cannot import it. Same write set and blast radius; a name both reached reads "unchanged" or
  "existed" (nothing overwritten).
- **Leg v (stored side)** (`evidence/r41_aq5_leg_v_20261009.txt`): `--section-recompose-census` fields_changed 0 of 950; passage
  census (C1's instrument) on 306 text fields: **prefix 0, cut 2, dangling 0**.
  - The 2 cuts are `risks` (AZN LN, BP LN). The risks path is not among the section fields aq-1 re-composes, so aq-1 did not reach it
    and its check could not see it. Branch C: brought to `1.0.0_SA_CTO~DELL1`; no second write. Item 1 is MET for section fields, NOT
    for `risks`.
  - The CTO's false-cut count: of the 15 values ending in "...", the issuer reads 14 as complete bullet lines and 1 as a real cut
    (8766 JP management). claim: inferred (read, not measured). So the "..." is mostly a false cut marker, as the CTO half found;
    its round-42 repair (a bullet line's end is a sentence end) would remove 14 of 15.
- **Leg p:** NOT this seat's. The scoped API keeps serving `/7` until it is deployed with `dossier.py` at `/8`. AMGT_RESAPP round 86
  has no deploy cell; `2.0.0_SA_COO~R1` carried it to its round-86 packet as a round-87 redeploy cell (msg 2902). PARKED: owner
  `2.0.0_SA_COO~R1`, un-parks at `1.0.0_SA_CTO~DELL1`'s round-86 analysis. The live reads (BABA US and SHOP CN management -- the route
  serves no `positives` field, so the half's NU US positives read is replaced by SHOP CN management, another gained value) wait on it.

## 3. The issuer's real run at close (aq-3)

- **Pick by the read** (`evidence/r41_aq3_close_pick_20261009.txt`): 95 names; a real term AND a headline naming it: 2 (BP/ LN, PBR
  US); no real term: 14; no pillars served: 49; errors 0.
- **Page walk** (`evidence/r41_aq3_close_read_20261009.txt` @`b0585eff04`): ui-walk on the dev:live build of portal DEV `3af36f28`,
  17:37-17:40Z, walk void: no. PBR US News: one filter, "production -- 1 of 10 headlines", no pillar-title filter. 8035 JP News: "The
  research team's thesis pillars carry no term to filter the news.", no filter. Screenshots kept local.
- Portal PROD: not promoted by this round; a PROD promote needs its own pair at its hash (MSTR msg 2882).

## 4. Rows

| row | standing | disposition |
|---|---|---|
| `AMGT_CORPUS-D1-W1-S1` aq1/aq2 control arms each compared the whole value, so each cell's repair moved the other's control | BLOCKING, INERT | RESOLVED by the issuer's check AMENDMENT 1 @`2ceea5883b` (each control grades its own edge); aq-2 re-proved on it |
| `AMGT_CORPUS-D1-S1` | OBSERVATION | closed with TO-READ-R40-ap10b-lv (item 5) |

## 5. Round-close check

`python .tools/round-close-check.py --project AMGT_CORPUS --round 41`: orders 4 of 4 complete, proofs 4 of 4 OK (after the
issuer set the full `to_id` in the aq-3/aq-4 instances @`3aed3a48b6`, same class and remedy as round 40, CTO msg 2701), judgment 1
ungraded (aq-3 AC3, the CVO's L9) -> `verdict=REFUSED` until that grade.

## 6. Not claimed

- The `/8` values on the served page: they wait on leg p (RESAPP round 87).
- `test_dossier_heading_only_round40.py` was not run on dell1 (fitz DLL); only its version literal changed.
- The 49 names with no pillars served were not investigated this round (a read, not a cell).
