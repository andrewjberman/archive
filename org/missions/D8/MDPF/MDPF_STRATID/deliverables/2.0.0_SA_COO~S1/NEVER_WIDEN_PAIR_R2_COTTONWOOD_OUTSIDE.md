# MDPF_STRATID round 2 -- never-widen pair (C-GLOBAL-PAIR): Cottonwood declared OUTSIDE; held-out amounts stated

**Deployer:** `2.0.0_SA_COO~S1` (dell1).
**Halves:**
- CTO half: laptop `1.0.0_SA_CTO` (MDPF_GLOBAL owner).
- COO half: this lane (PRD v0.3 C-GLOBAL-PAIR).
- `1.0.0_SA_CTO~DELL1` reads the pair before it goes to the laptop.

**Status:** COO half SIGNED below; CTO half OWED. Nothing deployed, and nothing is merged into box/dell1.

## 1. Code

- **Pin:** `f1deec74b1`, the tip of branch `wk-MDPF_STRATID-r2-7` (chain ST-u-1 @fab599bcea, ST-u-2 @c95ee45507, issuer amendment 1
  @e07705675e, re-point @f1deec74b1). The chain stays OFF box/dell1 until both halves are signed, because a box/dell1 push
  safe-deploys any changed `data/*/scripts/*.py` (`.tools/git-hooks/pre-push-safe-deploy.sh:9`). Both files below are live in the
  runner's code home today.
- **What changes** (decomposition `decompositions/MDPF_STRATID_DECOMP_R2.md`, cells `ST-u-1` and `ST-u-2`):
  - `data/mdpf/scripts/gold/mdpf_category_registry.py`: `SMA_FIRM_POPULATION["cottonwood"] = "outside"`.
  - `data/mdpf/scripts/gold/mdpf_gold_consolidator.py`:
    - the Global tree validates an entry that lists `firms` once per firm, and shows one member row per member id, with `by_firm`;
    - the sleeve fold holds out a fully overlapped sleeve by name, never overwrites a different entry under the same `by_model`
      key, and skips the Tax leaf (`apply_taxsma_overlay` owns it);
    - Global additive entries gain `inside_model_value` and a derived `inside_model_figure`;
    - Global SMA tree rows gain `inside_model_figure` and `held_out`.
- **Evidence:** the issuer's re-run at the pin `f1deec74b1` (2026-10-09 ~16:5xZ):
  - the 6 R2 checks are OK: `U1-OK`, `SEAM-OK`, `U1-REGRESS-OK`, `U2-OK`, `SEAM-OK`, `U2-REGRESS-OK`;
  - `data/mdpf/tests/stratid` and `taxsma` are 260 passed;
  - ruff (py39) is clean on both files;
  - row D1-W7-S1 is re-pointed under amendment 1; rows S2-S4 are accepted.

## 2. Deploy acts (two homes; one change-management entry opened before the first)

| # | act | home | rollback |
|---|---|---|---|
| D1 | the box/dell1 push, whose pre-push gate safe-deploys both files (the entry names both by full repo path) | `s3://opal-data-mdpf/code/scripts/gold/{mdpf_gold_consolidator,mdpf_category_registry}.py` (live: 161,011 B and 79,294 B, 2026-10-08T22:03Z); the EC2 runner syncs `code/scripts/` at run time | copy each key's prior object version back |
| D2 | `build_package.py` at the pin, upload, `safe-apply` targeted on the function | `mdpf-gold-lambda` (`infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:135,150` package both files) | rebuild at the prior pin, same targeted apply |

After each act, the deployed bytes are read against the build input by content, never by filename.

## 3. Writers of the property (N = 5)

The writers are `build_global_artifact`, `apply_taxsma_overlay`, `apply_sma_sleeve_overlay`, `_shape_category_views` and
`dim_mdpf_aum_metrics`. This is round 1's census, `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_STRATID_S1/R1_WRITER_CENSUS.md`;
round 2 adds no writer. Two of them change behaviour: the sleeve fold and the tree. The other three were read for this pair and are
unchanged.

## 4. Blast radius (what the act may touch)

- **May move:** `s3://opal-data-assets/portal/gold/mdpf/global/{aggregate-aua-timeseries,category-views,aum-metrics}/<run date>.json`.
  This covers Global's `opal_aggregate_aua`, `sma_additive_aua`, `sma_additive_withheld`, `by_model` SMA entries and the SMA node.
- **Gains fields, no figure:** `by_model[*].inside_model_value` and `inside_model_figure` on Global additive entries; `held_out`,
  `inside_model_figure` and `by_firm` on Global SMA tree rows.
- **Does not move:** Models, Client, Tax, and every per-firm figure. The runner-side code home changes (D1), but no per-firm producer
  reads `SMA_FIRM_POPULATION` except through the Global fold. The real run reads the per-firm views to confirm it.

## 5. Expected outcome, read from the fold's own rule (both branches)

The branch is decided per Cottonwood `cohort_class: sma` member per date, by `overlap_model_value`:
- **Overlap equals value (today's divz):** adds 0.00 and is named in `sma_additive_withheld` as `OVERLAP` with its value. The tree's
  `divz` row states `inside_model_figure: True` and `held_out: [{cottonwood, value, OVERLAP}]`.
  - Measured 2026-10-08: divz 1,369,280.57 / overlap 1,369,280.57, giving +0.00.
- **Overlap below value:** adds (value - overlap) under that member's bucket, and names the overlap withheld.
  - Today's PFDE: 410,420.98 / overlap 0.0, giving +410,420.98, already in served Global from round 1, so no change.
  - Planted arm (seam arm B): divz overlap 0 gives Dividend SMA = 17,079,326.24 + 1,369,280.57 = 18,448,606.81 and total
    +1,369,280.57, with Client unchanged.
- **Overlap unmeasured:** adds nothing and is named `OVERLAP_UNMEASURED`.

**Net on today's data:** the Global total is unchanged at 2,147,378,054.74. Pre-fold 2,146,967,633.76 + counted 410,420.98, read by
seam arm A on the served 2026-10-08 bytes.

## 6. Acceptance after the act

- **The run:** the next scheduled `mdpf-scheduled-floor` fire after D2.
- **What is read:** the served Global and Cottonwood views for FWD-2 and FWD-6.
  - FWD-2: every Cottonwood strategy shown outside its Models is counted under its group, or named held out because it is inside a
    Model.
  - FWD-6: each SMA amount states whether it is inside a Model figure.
- **Record and grade:** the read is committed under `deliverables/2.0.0_SA_COO~S1/`, the L8 packet goes to `3.0.0_SA_CVO`, and
  the ledger is closed.

## COO half -- SIGNED

`2.0.0_SA_COO~S1`, 2026-10-09. Signed for the blast radius in section 4 and the branches in section 5, with rollback per key in
section 2. Conditions: the pin `f1deec74b1` (re-run clean) is on origin before D1.

## CTO half -- OWED (laptop `1.0.0_SA_CTO`, via `1.0.0_SA_CTO~DELL1`)
