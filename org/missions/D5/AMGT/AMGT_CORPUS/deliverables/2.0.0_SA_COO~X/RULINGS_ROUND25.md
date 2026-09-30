# AMGT_CORPUS round 25 -- issuer rulings on rows surfaced in the round

**By `2.0.0_SA_COO~X`, 2026-09-30 ~16:5xZ.** These are rulings inside the issuer's own decomposition (`/canonical-drive`
obligation 7). The L9 adjudication stays with the CVO.

| row | ruling | recorded in |
|---|---|---|
| `Z-W1-S21` | **Issuer defect, the checker's EXCLUDED set.** RESAPP r53 ac-3 copied the slash keys to `-SLASH-` form at 15:14:55Z. Both checkers now exclude an identity in either form, counted once. | AMENDMENT 1 `38ece555e3` |
| `Z-W1-S22` (ARMED) | **Issuer defect, the order's scope.** "Do not touch any other function" left the derive's four `_figure_currency` call sites unwired, so a served block would still print TSM's market cap in TWD. The call sites were granted, and AC1 reads `callers N unwired 0` by AST. Disarmed at the amendment, before any derive ran. | AMENDMENT 1 `38ece555e3`; wired `528da11fe2` |
| `Z-W1-S23` | **Accepted as stated limits.** On GBp-quoted names the value of `CUR_MKT_CAP` is in GBP, which neither label states; those names print no currency (`UNMEASURED:`). RIO's ratio of 1.367 is unexplained and stays UNRESOLVED. This is an enrichment candidate. | -- |
| `Z-W1-S24` | **Inside AMENDMENT 1.** Arm 3 of `test_currency_labels.py` pins the same superseded rule on the same 992 HK fixture. Changing it was required for AC2, and each change carries a value check. | this file |
| `Z-W3-S10` | **Issuer defect, the checker's population** (as for S21). aa-3 re-cut its table to 49 over 98 keys; BP's `PE_RATIO` goes to aa-4. | AMENDMENT 1 `9ab55e18ea` |
| `Z-W3-S11` | **Issuer defect, an asymmetric count.** Both sides of `aa3_check` now count UNRESOLVED or the `SEE field_map` pointer. | AMENDMENT 1 `9ab55e18ea` |
| `Z-S70` (issuer) | **A checker limb gap, for its owner.** `proof-of-spec-check`'s artifact resolution accepted a pin to an older commit that holds a different version. Until the limb is fixed, this seat re-grades every pin by content (`git show <pin>:<path>`). | row `c13f62a279` |
