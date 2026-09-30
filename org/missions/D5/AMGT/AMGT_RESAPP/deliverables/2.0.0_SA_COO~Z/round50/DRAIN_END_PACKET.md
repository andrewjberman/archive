# AMGT_RESAPP round 50 -- drain-end packet (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.58, issuance `7e9fe4c5bb`, on the CTO's round-49 analysis `c95a9a16a4` + cell 5 `61ed59c609`.
Six orders, all terminal. Push state: LOCAL.

## 1. The orders

| cell | risk | holder | close | result |
|---|---|---|---|---|
| yy-1 FWD-30's grader compares VALUES | LOCAL | ~176 | drain `33eddabe73` (worker flipped, all PASS) | AC1 page plant 999.99 -> NOT_OK 'FIGURES(values) differ'; AC2 export plant -> NOT_OK; AC3 3 of 3 values equal; issuer re-ran merged; VALID |
| yy-2 /thesis passes the dossier's served fields | SERVED | ~177 | drain `5941a98591`, close `c77be605b6` | AC1 13 of 13 pillars (AMENDMENT 1 `41b61bd72e`: the check's own miscount, the worker's absent-pillars shape adopted); AC2 338 passed; VALID |
| yy-3 the proxy's officers served as NEOs | SERVED | ~177 (x3 workers: the harness keeps no transcript) | drain `50cc86edd6` (worker flipped) | REOPENED before its drain (AMENDMENT 1 `9d412c9e42`, row Z-W177-S2): the planned M-1 object failed the served store's own schema; now validates. AC1 plan YES, AC2 local YES, AC3 340 passed; VALID |
| yy-4 the base case names its owner | SERVED | ~178 (worker-light) | drain `683420dabf` (worker flipped) | AC1 YES, AC2 329 passed; one constant (`case_rule.BASE_LABEL`); VALID |
| yy-6 the crosswalk never drops a served record | LOCAL | ~179 | drain `c0e7c2dbc1` (worker flipped) | AC1 plant + retire YES, AC2 fork 0 dropped (BZLFY kept), AC3 237 in / 237 out digest-equal; issuer also ran the real CLI path (0 of 237 dropped); VALID |
| yy-5 the ONE build (deploy + NEO persist) | WORLD | `0.7.0_AE_CloudOps~A` (respawned) | flip `59311969b5` | COO half `cc59f06355`, CTO half `87b7bb1afa`, HARVST INERT ruling `6b654a84d4`; entry CLOSED 3/3 `67becd1b9f`; CodeSha256 `pVa+sgzj...B7B0=` (01:46:54Z); two M-1 first mints schema-valid; limbs 6/7 hold; issuer re-measured AC1-AC4 on the served plane; VALID |

Worktrees `C:/tmp/r50-176..179`: branches merged, checkouts KEPT pending Andrew's go (post-crash edict).

## 2. THE RESULT

- **FWD-30 compares VALUES and holds after the deploy.** Issuer real runs, full `--served --live --require-cases`:
  pre-deploy (23:49:50Z) and post-deploy (02:22:43Z) both **equal 96 of 96; values equal 96 of 96**; 19,125 value facts compared,
  0 differing; identity-only 349 -> 359 (+10; plausibly the ten new served NEO officer facts, 5 + 5, which the page carries without a
  value attribute -- NOT measured by a per-fact diff); 6 scale-unchecked (the export's
  UNRESOLVED unit, row Z-W176-S1). The CVO's two plants now fail the grade. `round50/captures/fwd30_value_sweep_*`.
- **/thesis serves the dossier** (CORPUS FWD-10/11/12/15/16/18 render halves, served side): pillars verbatim with terms (13 of 13 over
  the four p-4 names), management / fund of record / last stated position SERVED or ABSENT with the dossier's reason.
- **The base case names its owner:** "Opal's historical-multiple reference", served.
- **Named executive officers, from the proxy, served and labelled:** INTU and HAL 5 each, DEF 14A accessions 000089687825000057 /
  000004501226000033, `officer_set` "named_executive_officers". Real run: `round50/captures/thesis_{AZN_LN,INTU_US}_Equity_*.json`.
- **The crosswalk build is union-first on the CLI path** (yy-6); the second writer (`add_security`) is round 51's first cell (below).

## 3. Judgment criteria

None this round. What the CVO may weigh: (a) the 6 scale-unchecked names are a NAMED exception, not a pass (Z-W176-S1); (b) yy-3's
officers are the proxy's NEO set, labelled -- never the whole roster (CTO ruling 3).

## 4. Rows this round (L8 input)

- **Z-W176-S1** (~176, ARMED -> ruled by the issuer): the export's UNRESOLVED unit on 6 names' header figures (6501/9433/8316/8035/8766
  JP, TSM US); the grader's scale-free compare stands only as a counted exception; FWD-30 is not REALIZED on those 6 until the export
  resolves the unit (carried).
- **Z-W177-S1** (~177): the check's miscount of an ABSENT pillars object -- ruled, AMENDMENT 1.
- **Z-W177-S2..S5** (~177): the M-1 schema refused the proxy object (fixed); `ceo_profile` incomplete (fixed); a fitz stdout line and a
  pinned-test exclusion (INERT); the lane-gate refusal (resolved by the issuer's sync merge `672e524ae0`).
- **Z-W179-S1** (~179, INERT): the plain-build NO-OP that keeps the round trip digest-equal.
- **Z-S306** (AE~A): the scoped-API REGISTRY_HASH stamp is RED on CLOUD HEAD for every seat; the guard is protective.
- **Z-S307** (AE~A) -- **THE ISSUER'S ERROR:** the COO half said `lib/opal_naming.py` is not packaged, read from code comments; the
  build manifest packages it with six registry JSONs and `NAMING_SCHEMA.json`. Nothing wrong shipped only because the build commit
  predated it.
- **Z-S308** (AE~A) -- **THE ISSUER'S ERROR PATTERN:** my "no AMGT sentinel open" reads were shared-tree only; four AMGT sentinels sit
  on undrained worker branches (NEVER-2 requires every worktree).

## 5. Carried to the CTO's round-50 analysis

1. **Round 51's first cell -- the pool union INTO `write_pool`** (CTO @1b2294bbd6; CORPUS Z-S66): refused as a round-50 addendum by the
   one-issuance gate; the check is ready (`round51/checks/zz_choke.py`, base FAIL on both writers). AMGT_CORPUS r-1 waits on it.
2. **Z-W1-S18** (CTO msg 26847): `price_axis_pull.py:97-100` puts a hardcoded main-tree path on sys.path, so a worktree pytest grades main.
3. **The export's UNRESOLVED unit on 6 names** (Z-W176-S1) -- a RESAPP export fix.
4. **The REGISTRY_HASH stamp RED on HEAD** (Z-S306) -- whose restamp, and when, given it is the guard against packaging moved files.
5. **Gate proposal (not implemented; a lesson that must become a mechanism):** a never-widen half that admits or excludes a closure
   file cites the BUILD MANIFEST (build-only file list), never a code comment (Z-S307); and a half's "no sentinel open" read is the
   per-worktree union (Z-S308).
6. **DSGN_AMGTV1's four producer asks for round 51** (CTO msg 26791) and the page attributes FWD-30 still lacks (Z-W173-S1..S4).
7. **Record hygiene:** an order amended after spawn reaches the worker's lane grant only once the worker's HEAD carries it (yy-3); the
   issuer's sync merge into a worker branch was the remedy.
