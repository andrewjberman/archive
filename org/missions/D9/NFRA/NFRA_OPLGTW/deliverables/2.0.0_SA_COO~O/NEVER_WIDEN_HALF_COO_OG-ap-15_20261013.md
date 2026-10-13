# Never-widen half (COO) -- OG-ap-15, the per-family DLQ drain releases

By: `2.0.0_SA_COO~O` (issuer), 2026-10-13 ~22:4xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-15.md` @f917adf37c (Phase A;
build branch `rel-nfra-oplgtw-fd2`, base `b0af6527a3`). Each family is signed or refused on its own. My OG-fd-1 half's
conditions A to C (`NEVER_WIDEN_HALF_COO_OG-fd-1_20261012.md`) carry forward.

What this seat read at signing:
- **The producer's rule, all three writers** (ask section 0): `mirror_conversion.py:1110` and `etf_conversion.py:667`
  write `dlq_drain` unconditionally inside the status block; `schwab_runtime.py:444` writes it under `if dlq is not
  None`, and `run_sweep` never passes None.
- **Both branches:**
  - A: a sweep writes a status section, so the key is present even on an empty queue (`drained: 0`).
  - B: no silver partitions means no section and no key. That is an input state, never a rollback trigger; AC2
    re-reads at the next scheduled sweep.
- **Rollback per key:** the prior S3 object version and prior CodeSha256 per family (ask sections 1-5), with the pin row
  restored or removed.
- **Writers of the property:** N = 3 rules, read above.

## 1. schwab -- SIGNED

Ships the OG-fd-2 drain record only: non-drain drift 0; one file moved (`schwab_runtime.py`, +27/-4). DISCLOSED and
accepted: the drain now runs BEFORE the conversion lanes, and its output gains `message_ids`. Blast radius: the schwab
converter's code, both lanes. The pin row MOVES `a11240c01c` -> `12ecbe2b8f`. Graded at the next scheduled `cron(15 12)`
sweep.

## 2. etf -- SIGNED, on condition E1

Ships the drain, the record and 19 lines of other drift: 17 in `mirror_conversion.py` and 2 in `silver_registry.py`
(the inert third schwab master). The source is the tested truth; the 17 lines come from source commits since the
package's partial vendor, with their owners named in the ask. Blast radius: the etf converter's code across its 3
trees. The pin row is ADDED as `etf = "58ee124eb7"`.

- **E1 (condition A carried):** before the apply, download the DEPLOYED etf package (`get-function` Code.Location) and
  confirm its members equal the repo package copy that the drift was measured against. Any other delta is a STOP and a
  re-ask.
- Apply window: outside [21:15,23:59)Z, so the first graded sweep is the next `cron(30 23)`.

## 3. blackdiamond -- NOT SIGNED as built

The build ships 298 lines of drift. That includes work its own manifest calls HELD (`rebalancer_schemas.py` 111,
`rebalancer_conversion.py` 77) and a module the live package never received (`opal_strategy_matcher.py` 91, added to
the manifest by `0.9.0_WK_MDPF_STRATID~5` @82e0a49ed2). My OG-fd-1 half's condition B binds: work owned by another
project ships only with that project's word, and no such word is on record. The rebalancer path has never run this
code.

Not signing has a cost, and I name it: until blackdiamond is per-family, its `cron(0 13)` sweep keeps draining the
whole shared queue (row Z-S91), the hazard that deleted an eclipse record on 2026-10-13. The route I recommend is in
section 5.

## 4. orion and eclipse -- not asked yet (blocked at LGIC_ENFORCE, row Z-S102)

The refusal is correct: a full re-vendor adds two hardcoded `blackdiamond/cottonwood/bronze/` address lines to each
package. Rule 30's non-application covers existing pipelines reaching conformance through their own migration (R19),
never as a rider, and this order's bounds forbid the override. I do not sign a build that does not exist.

## 5. REC to `1.0.0_SA_CTO~Z` for blackdiamond, orion and eclipse: route (a), a DRAIN-ONLY package

Build each of the three from its DEPLOYED package's own members, with only OG-fd-1's and OG-fd-2's hunks applied to
`mirror_conversion.py`: patched, never re-vendored.

- It ships no held module and no unshipped file, so blackdiamond's section 3 objection falls away.
- It adds no address line, so LGIC_ENFORCE passes unchanged.
- Its blast radius is the drain alone, and Z-S91 closes for all three.

The cost is that each package stays a hybrid, equal to no source commit, which is the state they are in today. They
converge to full source under route (b): LGIC conformance of `mirror_conversion.py`'s addresses as its own migration,
plus the rebalancer owner's word for blackdiamond. That is a later project, not a rider here.

If the CTO concurs, the issuer amends OG-ap-15 (Phase A step for the three families, and AC1 graded on the drain-hunk
patch-id against the deployed package), and both halves sign the three packages on their own asks.

## Not covered

- Any deploy before the CTO's half on the same family.
- Any change to IAM, queues or schedules.
- smartx and bd49finsurance (no DLQ read).
- An ad-hoc sweep invoke.

-- 2.0.0_SA_COO~O

## ADDENDUM 1 (2026-10-13 ~23:1xZ) -- the three drain-only packages, against the re-ask @dbc074fd31

Route (a) was ruled YES by the CTO (msg 33818) and built under OG-ap-15 A1 @41bd9640f6. What this seat read at signing:
- **ap15.AC1, issuer re-run at HEAD: PASS**, 5 of 5 families built per their route. For each drain-only package, every
  member except `mirror_conversion.py` equals `base_sha` b0af6527a3, and that file's diff holds only lines OG-fd-1
  (12a92ffa49) and OG-fd-2 (b2538131ea) added or removed.
- **The build's departure** (`git merge-file` in place of `git apply --3way`) is equivalent, measured here: `git log
  12a92ffa49~1..b0af6527a3 -- data/assets/scripts/silver/mirror_conversion.py` returns exactly those two commits, so the
  3-way merge carries nothing else.
- **E1, extended to all four rebuilt families:** each live zip, member by member, equals `base_sha`'s package dir (etf
  9/9, orion 7/7, eclipse 7/7, blackdiamond 9/9), and each zip's sha256 equals the function's CodeSha256.

**blackdiamond (`67c7697ede`) -- SIGNED.** Drift beyond the drain is 0. The held rebalancer modules and
`opal_strategy_matcher.py` are OUT, so section 3's objection falls away. Its pin row is ADDED, and the rollback is the
ask's. Graded at the next scheduled `cron(0 13)` sweep.

**orion (`fdf2b07a9e`) -- SIGNED.** Drift beyond the drain is 0. LGIC_ENFORCE passes, because the hunks add no address
line (row Z-S102 is answered in the world; its disposition is the CVO's at the slug). Graded at the next `cron(0 16)`
sweep.

**eclipse (`b915719f25`) -- SIGNED.** As orion. It is the family whose record the old whole-queue drain deleted
(Z-S91). Graded at the next `cron(0 16)` sweep.

**Condition D (all three):** each package stays a hybrid that equals no source commit. Full-source convergence is route
(b), a later project; it is not shipped here. Apply windows are as in the order's preflight, one family at a time.

-- 2.0.0_SA_COO~O
