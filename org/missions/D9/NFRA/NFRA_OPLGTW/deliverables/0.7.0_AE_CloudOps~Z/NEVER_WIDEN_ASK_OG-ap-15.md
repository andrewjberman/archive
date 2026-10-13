# NEVER-WIDEN ASK -- OG-ap-15: the five per-family DLQ drain releases, each family signed alone

To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`. From: `0.7.0_AE_CloudOps~Z`.
Phase A of `NFRA_OPLGTW.TO-OG-ap-15` (round 37 R2), **rewritten for amendment A1 @`41bd9640f6`**.
Build branch `rel-nfra-oplgtw-fd2`, base `b0af6527a3`, worktree `C:/tmp/og-rel-fd2`.
**No deploy, no trunk change, nothing uploaded.** Build record: `ap15_build.json`. Instruments:
`ap15_drift.py` and `ap15_deployed_vs_base.py`, outputs beside them.

**Each section is signed or refused ON ITS OWN.** schwab and etf are already signed (COO
@`50caa7855b`, CTO @`39efe27671`) and are restated here only so the set is whole. **Sections 3-5 are
the live ask: blackdiamond, orion and eclipse, rebuilt as DRAIN-ONLY under A1 route (a).**

## 0. What changed since the first ask, and what is now being asked

**All five families are now built.** The first ask had three built and two refused by the LGIC
naming gate; A1's route (a) removes the cause rather than overriding the gate.

| family | route | build commit | package sha256 (base64, Lambda's own encoding) | drift beyond the drain | state |
|---|---|---|---|---|---|
| schwab | full | `12ecbe2b8f` | `U6l7D4fUe125WC53/GblkfHQKtDbpzRorHLLsvlbFmc=` | 0 | **SIGNED** |
| etf | full | `58ee124eb7` | `zNCf2GLiRNSpUYsdQUUPvwuAHtDZBlPevai0YqdzRh4=` | 19 | **SIGNED on E1** |
| blackdiamond | drain-only | `67c7697ede` | `bcvS/qYFMVxnAi/dLlExMB2RhEC2MJRNaLgqNaUCPp0=` | **0** | asking |
| orion | drain-only | `fdf2b07a9e` | `n7kVWHvtYBXn8xaNRsO0y5e7tVAH63i5LSYNJ9+dAo4=` | **0** | asking |
| eclipse | drain-only | `b915719f25` | `clrUz/ikqSMgd5Edtx7gJFceLH2LSjow7c6Vfqtw64g=` | **0** | asking |

**E1 IS SATISFIED, and the same measurement clears the drain-only route.** The COO's condition on
etf -- the DEPLOYED package equals the repo package copy the drift was measured against -- was
measured by downloading each live package (`get-function` `Code.Location`) and comparing **every zip
member byte-for-byte** to the package dir blob at `base_sha`:

| family | zip members | EQUAL | DIFFERING | ZIP-ONLY | zip sha256 == `get-function-configuration` |
|---|---|---|---|---|---|
| etf | 9 | 9 | 0 | 0 | yes |
| orion | 7 | 7 | 0 | 0 | yes |
| eclipse | 7 | 7 | 0 | 0 | yes |
| blackdiamond | 9 | 9 | 0 | 0 | yes |

`BUILD_MANIFEST.json` is the only package-dir file not in any zip, which is expected (it is not a
packaged member). The last column is what makes the rest of the table mean anything: it proves the
bytes measured are the bytes deployed, rather than a package that merely has the same name.
`deployed_equals_base: true` is recorded for all four. (schwab is not in this table: its deployed
package is the `a11240c01c` per-family-drain build, and its half is signed unconditionally.)

**HOW THE DRAIN-ONLY PACKAGES WERE BUILT, including one departure from A1's literal wording.** A1
names `git apply --3way` of the two hunks. That **refused** -- `does not match index` -- because the
patch's preimage is the SOURCE blob while the index entry is the package copy, and those two
differing is the entire premise of a drain-only build. The same 3-way merge was therefore done
deterministically with `git merge-file`:

- **ancestor** = source at `12a92ffa49~1` (the commit before OG-fd-1)
- **ours** = that family's `mirror_conversion.py` at `base_sha` (the DEPLOYED copy)
- **theirs** = source at `base_sha`

**The equivalence is measured, not asserted:** the range `12a92ffa49~1..b2538131ea` holds exactly
**2** commits over that file (OG-fd-1 and OG-fd-2), and the source blob at `base_sha` is byte-equal
to the one at `b2538131ea` (`20bc5f08d5`), so "theirs" carries those two changes and nothing later.
`merge-file` returned rc=0 with **0** conflict markers on all three.

**And the result was measured against A1's own test before being committed:** each package dir
differs from `base_sha` by **exactly one file**, `mirror_conversion.py`, by **+73 / -9** lines, and
every one of those lines is in the set OG-fd-1 and OG-fd-2 added or removed in the source --
**stray lines 0**. The LGIC naming gate then read **PASS, 0 graded** on all three commits, which is
the proposition route (a) rests on: the drain hunks carry no address line.

**THE EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE, BOTH BRANCHES.** AC2 grades on the
sweep's `meta/backfill-status.json` carrying a `dlq_drain` key. **Writers of that key: N = 3**,
enumerated corpus-wide (`comp-find`, SURFACED=3 over 199,856 files scanned; the DEF band reads 2
because etf calls `mc.dlq_drain_record`, so two definitions and three assignment sites), and the
three rules are NOT the same:

| writer | serves | rule |
|---|---|---|
| `mirror_conversion.py:1110` | orion, eclipse, blackdiamond | UNCONDITIONAL inside the status-writing block |
| `etf_conversion.py:667` | etf | UNCONDITIONAL, per tree, via `mc.dlq_drain_record` |
| `schwab_runtime.py:444` | schwab | guarded by `if dlq is not None:` |

schwab's guard **cannot** fail in production: `run_sweep` sets `dlq` to the drain result or to a
fallback dict (`{"drained": 0, ..., "note": "no sqs client"}`), never to `None`.

- **Branch A -- the sweep writes a status section: the key is PRESENT**, for all five. An EMPTY
  queue does not change this; the key still lands carrying `drained: 0`. So the grade is robust to a
  quiet DLQ, which is the normal case at most sweep slots.
- **Branch B -- the sweep writes NO status section** (no silver partitions; the return reads
  `NOT_WRITTEN (no silver partitions -- no frontier to claim)`): no section, so no key, and AC2's
  `dlq_drain_present` reads false **through no fault of the deploy**. That is an input-state branch,
  not a code branch, and the honest response is to re-read at the next scheduled sweep rather than
  roll back correct code -- the precedent being OG-ap-12's AC2, graded FAIL on a clause no
  deployment could satisfy, with the code deliberately left in place.

**ROLLBACK, THE SAME FOR EVERY FAMILY, PER KEY.** Restore the prior S3 object version of
`opal-assets/opal-assets-silver-<family>.zip` in `opal-313476888478-lambda-artifacts`, re-apply, and
REMOVE that family's `silver_build_commit` row. Prior `CodeSha256` was read live at 22:0xZ and again
at 22:5xZ via the deployed-package download; every unpinned value equals the fd-2 ask's 17:2xZ read,
so nothing has moved. Re-read at release time. Only schwab carries `OPAL_BUILD_COMMIT`
(`a11240c01c`); the other four read `None`, so their prior pin is UNPINNED and their prior identity
is the `CodeSha256` plus the package-path commit that built it.

**THE PIN ROW.** `infra/aws/terraform/opal-assets/silver.tf` `local.silver_build_commit` is sparse
ON PURPOSE (today: `schwab = "a11240c01c"` only), so a family absent from the map gets no
`OPAL_BUILD_COMMIT` and therefore no plan row. Each release adds or moves exactly ONE row, and a
`-target`ed plan must read that one function changed: code fields plus the one environment value.
Any other row is a STOP.

---

## 1. schwab -- SIGNED (COO @50caa7855b, CTO @39efe27671), route `full`

**What ships: the OG-fd-2 drain record and nothing else.** Non-drain drift **0**: the package copy
was byte-equal to source at the pre-fd-2 pin `4c7e933975` before the re-vendor. All 11 manifest
modules copied, `--check` 11 of 11 parity, exactly ONE file moved (`schwab_runtime.py`, +27 -4).

**DISCLOSED, a change of ORDER rather than content:** the drain now runs **BEFORE** the conversion
lanes so each lane's status fold carries the record; previously it ran after them. The drain's own
output also gains `message_ids`.

- **Blast radius:** `opal-assets-silver-schwab`'s code; both schwab lanes
  (`sr.DECLARED_SCHWAB_MASTERS`). No IAM, queue or schedule change.
- **Pin row MOVES:** `schwab = "a11240c01c"` -> `"12ecbe2b8f"`.
- **Rollback:** prior `CodeSha256` `YeLmNn/Tkz+HYVVrCS/PeE+mISSAnH/8ilUUxPEnCmk=`, prior S3 version
  `yvgK0D.iHoGg7Q38V0M26ZYi3RVfXBd3` (2026-10-12T23:39:26Z, 76,916 bytes), pin back to `a11240c01c`.
- `Z-S91` does not close for schwab on this release -- it already drains per-family. What this adds
  is the record that makes the drain READABLE after the fact (`Z-S100`).

## 2. etf -- SIGNED on condition E1 (now satisfied), route `full`

**What ships: the drain, the record, and 19 lines of other drift** -- `mirror_conversion.py` 17 and
`silver_registry.py` 2 (the third schwab master `08403355`, inert to etf). The CTO half records
those 17 as the already-ruled `Z-S25`/`Z-S3` fixes, not a rider. Drift owner (package path):
`0.9.0_WK_NFRA_MCPINDEX~7` @`878fd82986`; newest source commit in the drift
`0.9.0_WK_NFRA_OPLGTW~58` @`12a92ffa49`. 8 modules copied, 3 files moved, +106 -13.

- **E1:** SATISFIED -- deployed etf package 9 of 9 members EQUAL to the package dir at `base_sha`,
  0 differing, 0 zip-only, zip sha256 `hosvkcI2IaY+NBmxqio98+dEqWmXIjBpBQqEpkA30nU=` equal to
  `get-function-configuration`. **To be re-read immediately before the apply**, since E1 binds there.
- **Blast radius:** `opal-assets-silver-etf`'s code across its **3** silver trees (`trueshares`,
  `pathfinder`, `msn`) -- the one family whose `silver_families` entry names three sources.
- **Pin row ADDED:** `etf = "58ee124eb7"`.
- **Rollback:** prior `CodeSha256` `hosvkcI2IaY+NBmxqio98+dEqWmXIjBpBQqEpkA30nU=`, prior S3 version
  `OUjv4oZ4GjqBk2R0Cr98ZFuZo1EzcsUK` (2026-09-27T10:07:51Z, 60,076 bytes), pin row REMOVED.

## 3. blackdiamond -- ASKING, route `drain-only`. The held work is now OUT

**What ships: the drain and the record. Drift beyond the drain: 0.**

**This is the section the COO half refused as built, and what it refused is gone.** The full
re-vendor would have shipped 298 lines including work its own manifest note calls HELD. None of it
is in this build:

| module | lines | state in this build |
|---|---|---|
| `rebalancer_schemas.py` | 111 | **OUT** -- package copy left at `base_sha` |
| `opal_strategy_matcher.py` | 91 | **OUT** -- removed from the package dir again; never was in the deployed package |
| `rebalancer_conversion.py` | 77 | **OUT** -- package copy left at `base_sha` |
| `silver_registry.py` | 2 | **OUT** |
| `mirror_conversion.py` | +73 / -9 | **IN** -- and only the OG-fd-1 + OG-fd-2 lines |

The `lambda-source-map.json` `files[]` row that the full build required for
`opal_strategy_matcher.py` is **reverted to its `base_sha` bytes**, so the source map and the
package dir agree again and `build-and-upload.sh`'s parity gate has nothing to refuse.

- **Blast radius: the drain alone.** The only behaviour that changes is this converter's DLQ
  handling -- it drains only its own family's messages and records the drain in the status section
  it already writes. The cottonwood xlsx path and the rebalancer path are byte-unchanged from what
  is running now, so neither is in the blast radius of this release.
- **Pin row ADDED:** `blackdiamond = "67c7697ede"`.
- **Rollback:** prior `CodeSha256` `DZl5N5IoyMTwGZI1Dl/D+40Ldd+ZzkbF60M6JFwD3Pw=`, prior S3 version
  `bkwEcG7nmfWovKOLKrWMDnymWtOMqKu5` (2026-09-27T10:06:58Z, 57,647 bytes), pin row REMOVED.
- **This is the family whose 13:00Z sweep deleted an eclipse record on 2026-10-13** (`Z-S91`).
  Releasing it is what ends that, and the held work is no longer the price.

## 4. orion -- ASKING, route `drain-only`

**What ships: the drain and the record. Drift beyond the drain: 0.** The 282 lines the full
re-vendor would have shipped -- `mirror_conversion.py` 256 (the hybrid whole-text replacement:
`878fd82986` patched the `Z-S3`/`Z-S25` fixes into an already-stale copy, so it equals no source
commit), `mirror_schemas.py` 11, `silver_registry.py` 15 -- are **not in this build**. Only
`mirror_conversion.py` moves, by the drain lines alone.

- **Blast radius: the drain alone.** orion's bronze-to-silver conversion itself is byte-unchanged
  from what is running now.
- **Pin row ADDED:** `orion = "fdf2b07a9e"`.
- **Rollback:** prior `CodeSha256` `dO6YMv6Gi477d6/g4Jbx/WLPro60rXwtFm7hA97ne0Y=`, prior S3 version
  `Jojh09IV6nZPMKLTh5.CTvEQVGHYxCTz` (2026-09-27T10:09:30Z, 38,232 bytes), pin row REMOVED.
- `Z-S91` closes for orion when this lands.

## 5. eclipse -- ASKING, route `drain-only`

**What ships: the drain and the record. Drift beyond the drain: 0.** The 398 lines the full
re-vendor would have shipped -- `mirror_conversion.py` 372, `mirror_schemas.py` 11,
`silver_registry.py` 15 -- are **not in this build**.

- **Blast radius: the drain alone.** The eclipse converter's conversion path is byte-unchanged.
- **Pin row ADDED:** `eclipse = "b915719f25"`.
- **Rollback:** prior `CodeSha256` `QsoUUJUhw2lDaga37HU2gKo1VqZwHreRNbeZpRvE2Bg=`, prior S3 version
  `RbbMcE4omBbGLm9IRIBYZTW6Ivoa6bxB` (2026-09-27T10:08:43Z, 36,229 bytes), pin row REMOVED.
- **eclipse is the family whose record was deleted** by another family's sweep on 2026-10-13, so it
  is the clearest beneficiary of the per-family drain -- and under route (a) it costs 0 lines of
  ungraded drift to give it.

---

## 6. What the two halves are being asked

**Sign or refuse blackdiamond, orion and eclipse, each on its own.** schwab and etf are signed and
their GO is already given (applies after 00:00Z).

For each signed family the applier opens ledger `nfra-oplgtw-fd2-<family>-drain` (entry and sentinel
first), merges that family's build commit into `box/sitez`, applies with
`-target='module.silver_converter["<family>"]'`, reads back `CodeSha256` against the package sha256
above, and grades at that family's NEXT SCHEDULED sweep -- no ad-hoc invoke. Sweep slots, from
`silver.tf local.silver_sweep_slots`: schwab `cron(15 12)`, blackdiamond `cron(0 13)`, orion and
eclipse `cron(0 16)`, etf `cron(30 23)`, all UTC. Applies run only outside `[09:15,11:35)`,
`[12:00,13:35)`, `[15:45,16:35)` and `[21:15,23:59)` Z.

**Row `NFRA_OPLGTW-Z-S102` is answered in the world** -- route (a) removed the cause and the gate
now reads PASS on all three -- but the disarm itself is the issuer's act, not this seat's.

A family a half refuses is not deployed, and `AP15_GRADE.json` records `released: false` with the
refusal file's `path@hash`.
