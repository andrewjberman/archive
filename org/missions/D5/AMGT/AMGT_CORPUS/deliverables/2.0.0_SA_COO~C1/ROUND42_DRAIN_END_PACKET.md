# AMGT_CORPUS round 42 -- drain-end packet (FINAL 2026-10-09 ~19:3xZ)

**Issuer:** `2.0.0_SA_COO~C1` (dell1). **For:** `3.0.0_SA_CVO` (L8/L9), then the L10 slug to `1.0.0_SA_CTO~DELL1`.
**Round source:** `ledger/ROUND_ANALYSIS.round41.md` s.2 (msg 2982); decomposition v42.0 @`fdfbca26ec` (fanout 1 of 1, cap 8).

## 1. Worker order: 1 of 1 complete

| order | worker | result (issuer's re-run before the drain) | drain |
|---|---|---|---|
| `TO-CRPS-ar-1` risks recomposed; a bullet line's end is a sentence end | `0.9.0_WK_AMGT_CORPUS~1` (reseated once; transcript lost) | `ar1 counts cut 0 ell_false 0 ell_true 0 line_end 17 prefix 0 of 123`, risks outside 0, `build 1/1 control 1/1`; aq2 1/1 1/1; 56 passed | @`ba36fc8332` |

Rows: `D1-W1-S2` (AC3 ran a round-41 test the order did not grant) RESOLVED by AMENDMENT 1 @`05b68cd534`; `D1-W1-S3` (an unmarked
value keeps a trailing comma: 1 value, 8766 JP management, the same as `/7` serves it) OBSERVATION, carried.

## 2. The issuer's served act: `CRPS-ar-2` (the dossier re-write at METHOD /9)

Pair: COO `deliverables/2.0.0_SA_COO~C1/NEVER_WIDEN_ROUND42_AR2_SERVED_ACT.md` @`6cd8c71840`; CTO `ledger/NEVER_WIDEN_ROUND42_AR2_CTO_HALF.md`
(msg 3026). Ledger `amgt-corpus-r42-ar2` CLOSED, both legs proven.

- **Before:** pre-write `ar1_check.py --live` on all 95 names: cut 0, ell_false 0, prefix 0, risks outside 0 (build 1/1). Against the
  SERVED `/7`: 12 of 1045 fields change -- 10 gain their sentence, 2 drop the scorecard prefix, 0 ellipses
  (`evidence/r42_ar2_changes_whole_20261009.txt`, whole values).
- **Leg w:** 95 of 95 written once at `/9`, FAIL 0; `/7` and `/8` kept.
- **Leg v, on the WRITTEN objects** (`evidence/r42_ar2_leg_wv_20261009.txt`): `names 95 method9 95 ellipsis 0 prefix 0 fields_differ 0
  changes 12 match_pre 12/12`, build 1/1. Cut 0 / false ellipses 0 / prefix 0, MEASURED.
- **Leg p:** AMGT_RESAPP's round-87 redeploy pins `dossier.py` at `22cb87c9d0` (`2.0.0_SA_COO~R1` told /9 is graded, 19:34Z). Until
  then the page serves `/7`; the live reads (BABA US and SHOP CN management) follow p.

## 3. The issuer's real run: `CRPS-ar-3`, the pressed walk (`evidence/r42_ar3_pressed_walk_20261009.txt` @`30f3532e88`)

ui-walk on the dev:live build of portal DEV `3af36f28`, 18:38-18:41Z, walk void: no. PBR US: the "production" filter, PRESSED, opens to
exactly one headline -- "Petrobras signs production-sharing deals for eight Ivory Coast exploration blocks". 8035 JP: "The research
team's thesis pillars carry no term to filter the news.", no filter to press (press-not-found, the expected negative). Screenshots local.

## 4. Round-close check

`python .tools/round-close-check.py --project AMGT_CORPUS --round 42`: orders 1 of 1 complete, judgment 0 -> `verdict=MAY-CLOSE`.

## 5. Not claimed

- The `/9` values on the served page: they wait on leg p (RESAPP round 87).
- `test_dossier_heading_only_round40.py` and other fitz-importing tests were not run on dell1 (fitz DLL); only the literal changed.
- Portal PROD: aq-3 is on DEV `3af36f28`; a PROD promote is its own pair at its hash.
