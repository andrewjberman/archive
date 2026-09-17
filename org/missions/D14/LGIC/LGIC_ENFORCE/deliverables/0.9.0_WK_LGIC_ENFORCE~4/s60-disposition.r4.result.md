# LGIC_ENFORCE.TO-EN-g-27-r4 -- s60-disposition -- result

`0.9.0_WK_LGIC_ENFORCE~4` on cell `EN-g-27` (RULINGS R-16, R-26, R-32). Worktree
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-4-4`, branch
`wk-lgic-enforce-4-4`, base `3de3a4e32a` (CLOUD). Artifact commit `3e1ede5f06`.

## What landed

One record, `S60_DISPOSITION.r4.md`, dispositioning row `LGIC_ENFORCE-S60` (the ship classifier's
undercount) as **FIXED**. No code changed: `lib/opal_naming.py` and `.tools/safe_deploy_core.py`
are unchanged from `3de3a4e32a`; nothing live moved.

## Why FIXED, not CARDED

S60 measured that `.tools/safe_deploy_core.py`, called alone over the generator's 10 targets,
decides only 3 (the S3/DS plane) and returns `None` for the other 7 -- so a single-classifier split
would print at least 5 shipping targets as REPO-ONLY. Round 3's `EN-g-9` cell already built R-26's
remedy before S60's own ruling text existed as a cell: a **per-plane** split, where each of the 10
targets' `measured:` field names the instrument for THAT target's own plane, not one classifier
asked to decide every plane. Re-running `python lib/opal_naming.py targets` at this tree reproduces
exactly the issuer's cut measurement: 10 targets, 5 distinct instruments, 0 UNCLASSIFIED. The
disposition record states the full numbers and the citation for each instrument.

## Criteria

- `G27R4-AC1` (`g27-plane-instruments`): `DENOMINATOR: TARGETS 10 printed; 10 classified row(s);
  rc=0` / `distinct measuring instruments: 5` / `UNCLASSIFIED: 0` -> `PASS-G27-PLANE-INSTRUMENTS`
  (rc=0). Unchanged from the issuer's cut measurement -- this worker did not touch the classifier.
- `G27R4-AC2` (`g27-disposition`): `DENOMINATOR: 1 record; FIXED shape=True CARDED shape=False` ->
  `PASS-G27-DISPOSITION` (rc=0).
- `G27R4-AC3`: JUDGMENT. Recorded `UNVERIFIABLE-BY-INSTRUMENT`, `status_reason` naming
  `3.0.0_SA_CVO`, per the order and Rule 27 (judgment criteria are graded at L9, never
  self-graded).

## Controls

- **Mutant**, on this worker's own artifact (AC1's artifact, `lib/opal_naming.py`, is outside the
  NO-CODE-CHANGE grant and was not mutated). A heading-only rewording of the disposition record left
  `g27-disposition` PASS unchanged (the checker's `fixed`/`carded` test is an unanchored substring
  match over the whole file, not scoped to the disposition heading -- a looseness noted, not this
  cell's fix to make). A full-content replacement with neutral text flipped it to
  `FAIL-G27-DISPOSITION`, rc=1, as expected. Both mutations were reverted from a pre-mutant copy and
  `git diff --stat` confirmed byte-identical to the commit before the next step.
- **Determinism**: AC1 and AC2 each ran twice against the committed tree; both pairs of captured
  output were byte-identical (`diff` produced no output).

## Not claimed

- Nothing live moved; no AWS read, no Terraform apply, `generate()` was never invoked.
- This record does not re-derive R-26's ruling; it re-measures the tree R-26's build landed on.
- This record does not verify or reopen R-16's own earlier act (EN-r-6's comment-only re-render
  that re-minted the investor_reporting bundle and redeployed `perfrp_firm_pin.py`) -- that is
  named as out of this cell's scope, per the order's step 3.
