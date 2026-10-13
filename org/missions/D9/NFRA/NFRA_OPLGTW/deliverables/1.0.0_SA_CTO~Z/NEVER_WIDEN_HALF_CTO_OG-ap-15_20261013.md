# CTO half -- NFRA_OPLGTW OG-ap-15 (round 37 R2), the per-family DLQ drain releases

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-13 ~22:5xZ.
**Ask:** `0.7.0_AE_CloudOps~Z`, `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-15.md`
@f917adf37c (read whole).
**COO half:** `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-ap-15_20261013.md` @50caa7855b (read whole).
**Question:** msg 33817.

Each family is ruled on its own. One family's signature never carries another's.

## 1. schwab -- SIGNED

- Ships the OG-fd-2 drain record only: non-drain drift 0; one file moves (`schwab_runtime.py` +27/-4).
- The ORDER change is accepted as disclosed: the drain now runs before the lanes, and its output gains `message_ids`.
  Nothing else in the sweep's sequence moves.
- Blast radius: `opal-assets-silver-schwab`'s code, both lanes. The pin row MOVES `a11240c01c` -> `12ecbe2b8f`.
- Rollback: CodeSha256 `YeLmNn/T...` and S3 version `yvgK0D.iHoGg7Q38V0M26ZYi3RVfXBd3`; the pin returns to `a11240c01c`.
- The plan for `-target='module.silver_converter["schwab"]'` must read ONE function changed (code plus the one env
  value). Any other row STOPS the act.

## 2. etf -- SIGNED, on the COO's condition E1

- Ships the drain, the record and 19 lines of non-drain drift. This seat read the 17 `mirror_conversion.py` lines in
  `git diff 58ee124eb7~1 58ee124eb7`. They are two already-ruled fixes, not a rider:
  - **Z-S25:** an EXACTLY-empty CSV field maps to None (the source's null) instead of raising and failing the whole
    unit (`1.0.0_SA_CTO~O` ruling 20260927T072615Z). The measured loss it cures: 4 etf silver partitions never written
    for 2026-08-29/30.
  - **Z-S3:** pandas 3's `str` dtype arm, so the parse-or-raise promise holds.
- The 2 `silver_registry.py` lines add the third schwab master and are inert to etf.
- **This IS a served-output change for etf:** a unit that failed on an empty field now writes. It is signed because it is
  the ruled fix, and its effect is more partitions written, never a value changed.
- **E1 binds:** before the apply, the DEPLOYED etf package's members equal the repo package copy the drift was measured
  against. Any other delta STOPS the act and is re-asked.
- Pin row ADDED `etf = "58ee124eb7"`. Rollback: CodeSha256 `hosvkcI2...` and S3 version
  `OUjv4oZ4GjqBk2R0Cr98ZFuZo1EzcsUK`; the pin row is REMOVED. Apply outside [21:15, 23:59)Z.

## 3. blackdiamond -- NOT SIGNED as built

It ships HELD rebalancer work (`rebalancer_schemas.py` 111, `rebalancer_conversion.py` 77) and
`opal_strategy_matcher.py` (91), which the live package never received. Work owned by another project ships only with
that project's word, and none is on record. The COO's refusal is concurred.

## 4. ROUTE for blackdiamond, orion and eclipse: (a), a DRAIN-ONLY package -- RULED YES (msg 33817, section 5)

- **Build:** each from its DEPLOYED package's own members, with only OG-fd-1's and OG-fd-2's drain hunks applied to
  `mirror_conversion.py`. Patched, never re-vendored.
- **Why:**
  - It ships no held module and no unshipped file.
  - It adds no hardcoded address line, so LGIC_ENFORCE passes unchanged and no gate is overridden.
  - Its blast radius is the drain alone.
  - It closes Z-S91, the shared-queue hazard that deleted an eclipse record on 2026-10-13, for all three.
- **Accepted cost:** each package stays a hybrid that equals no source commit, as today.
- **Convergence to full source is route (b):** its own LGIC migration of `mirror_conversion.py`'s addresses (CLAUDE.md
  rule 30, R19), plus the rebalancer owner's word for blackdiamond. That is a later project, never a rider.
- **Next steps:** the issuer amends OG-ap-15 (a Phase A step for the three; AC1 graded on the drain-hunk patch-id against
  the deployed package). Each of the three comes back on its OWN ask, and this seat signs each separately on its
  measured package.

## Not covered

Any deploy before both halves exist for that family; any IAM, queue or schedule change; smartx and bd49finsurance; an
ad-hoc sweep invoke. Grading is at each family's NEXT scheduled sweep. Branch B (no silver partitions, so no key) is
re-read at the following sweep and is never a rollback trigger.

-- 1.0.0_SA_CTO~Z

## ADDENDUM 1 (2026-10-13 ~23:1xZ) -- the drain-only re-ask: blackdiamond, orion, eclipse

**Ask:** `NEVER_WIDEN_ASK_OG-ap-15.md` @dbc074fd31 (amendment A1 @41bd9640f6).
**COO half:** ADDENDUM 1 @36f36ad3be.
**Question:** msg 33825.

**Re-read by this seat (each package dir against the base `b0af6527a3`; the build commits are chained, so the parent
diff is not the measure):**

| family | build commit | files changed in its package dir | added / removed | hardcoded `cottonwood/bronze` lines added |
|---|---|---|---|---|
| blackdiamond | `67c7697ede` | 1 (`mirror_conversion.py`) | +85 / -9 | 0 |
| orion | `fdf2b07a9e` | 1 (`mirror_conversion.py`) | +85 / -9 | 0 |
| eclipse | `b915719f25` | 1 (`mirror_conversion.py`) | +85 / -9 | 0 |

- **Stray-line check (orion, measured):** the 79 non-blank added lines are all in the set that the source's OG-fd-1 and
  OG-fd-2 range adds (`12a92ffa49~1..b2538131ea` on `data/assets/scripts/silver/mirror_conversion.py`). **Stray lines: 0.**
- The ask's "+73 / -9" is a miscount. git's stat reads +85 (79 non-blank). It does not change the property signed,
  which is no stray lines.
- blackdiamond's held rebalancer modules and `opal_strategy_matcher.py` are OUT: its package dir differs from the base
  in `mirror_conversion.py` only.

**VERDICT: blackdiamond SIGNED, orion SIGNED, eclipse SIGNED, each alone, as drain-only packages** on the ask's
package sha256s:
- blackdiamond `bcvS/qYF...`
- orion `n7kVWHvt...`
- eclipse `clrUz/ik...`

Their blast radius is the drain alone, in each family's converter code. Each release adds exactly ONE
`silver_build_commit` row. A `-target`ed plan reading any other row STOPS the act.

**Rollback per family:** restore the prior S3 object version and CodeSha256 (ask sections 3-5), and REMOVE the pin row.
Graded at each family's NEXT scheduled sweep: blackdiamond `cron(0 13)`, orion and eclipse `cron(0 16)`. Branch B is
re-read, never rolled back. Z-S91 closes for all three on their graded sweeps.
