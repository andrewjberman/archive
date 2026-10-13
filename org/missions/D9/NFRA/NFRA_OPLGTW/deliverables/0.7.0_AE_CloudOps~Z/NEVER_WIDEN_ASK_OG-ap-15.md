# NEVER-WIDEN ASK -- OG-ap-15: the five per-family DLQ drain releases, each family signed alone

To: `1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`. From: `0.7.0_AE_CloudOps~Z`.
Phase A of `NFRA_OPLGTW.TO-OG-ap-15` (round 37 R2). Build branch `rel-nfra-oplgtw-fd2`, base
`b0af6527a3`, worktree `C:/tmp/og-rel-fd2`. **No deploy, no trunk change, nothing uploaded.**
Build record: `ap15_build.json` beside this file. Drift instrument: `ap15_drift.py`, output
`ap15_drift_measured.json`.

**Each section below is signed or refused ON ITS OWN.** The issuer's ruling at the cut: one family's
signature never carries another's, so blackdiamond's held modules cannot ride in on etf's.

## 0. Read this first: what is built, what is not, and one thing the grade depends on

**THREE of the five are built. orion and eclipse are BLOCKED and are not asking for a signature
yet** -- they are here so the set is whole and so the two halves can see why.

| family | built | package sha256 (base64, Lambda's own encoding) | non-drain drift |
|---|---|---|---|
| schwab | yes, `12ecbe2b8f` | `U6l7D4fUe125WC53/GblkfHQKtDbpzRorHLLsvlbFmc=` | 0 |
| etf | yes, `58ee124eb7` | `zNCf2GLiRNSpUYsdQUUPvwuAHtDZBlPevai0YqdzRh4=` | 19 |
| blackdiamond | yes, `e05a80e0d9` | `hi/bL8SV9CKs0FNpo6ftPn4OTdEuF24wOqQ5C0aZln0=` | 298 |
| orion | **no -- BLOCKED** | -- | 282 |
| eclipse | **no -- BLOCKED** | -- | 398 |

**THE BLOCK (row `NFRA_OPLGTW-Z-S102`, BLOCKING, INERT, disarm_owner `2.0.0_SA_COO~O`).**
`safe-commit.sh` refuses both: `LGIC_ENFORCE DEC-6`, NAMING REFUSE on `mirror_conversion.py:103`,
`:105`, `:129` -- three `^blackdiamond/cottonwood/bronze/` regexes resolving to
`lookup('cottonwood')`. **The refusal is correct, not noise, and the measurement is the reason:**
the orion and eclipse package copies carry **2** of those four address patterns, source carries
**4**, and etf and blackdiamond already carry all **4** -- which is why their re-vendor added zero
matching lines and passed the same gate. So for orion and eclipse the rebuild genuinely widens the
package's hardcoded-address surface by two lines. The order's BOUNDS forbid overriding any gate but
the step-2 author escape, and editing the source strings would be an ungraded rider outside this
order's `<paths>`. Three routes, none of them this seat's to pick: **(a)** elect the fd-2 ask's
option (b), a drain-only package for these two, which that ask already names as a build choice the
release order must make explicit; **(b)** let `mirror_conversion.py`'s addresses reach LGIC
conformance under their own migration (CLAUDE.md rule 30 R19), after which the re-vendor passes
unchanged; **(c)** an R20 register entry Andrew acknowledges. The vendored working trees are left in
place, so no re-vendor is needed once a route is chosen.

**THE EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE, BOTH BRANCHES.** AC2 grades on the
sweep's `meta/backfill-status.json` carrying a `dlq_drain` key. **Writers of that key: N = 3**, read
rather than assumed, and the three rules are NOT the same:

| writer | serves | rule |
|---|---|---|
| `mirror_conversion.py:1110` | orion, eclipse, blackdiamond | UNCONDITIONAL inside the status-writing block |
| `etf_conversion.py:667` | etf | UNCONDITIONAL, per tree, via `mc.dlq_drain_record` |
| `schwab_runtime.py:444` | schwab | guarded by `if dlq is not None:` |

`backfill_status.py` writes the file but carries 0 occurrences of the key: the section's caller adds
it, exactly as the fd-2 ask said. schwab's guard **cannot** fail in production: `run_sweep` sets
`dlq` to the drain result or to a fallback dict (`{"drained": 0, ..., "note": "no sqs client"}`),
never to `None`; the `None` default belongs to `_sweep_lane`'s signature for a direct caller.

- **Branch A -- the sweep writes a status section: the key is PRESENT**, for every one of the five.
  An EMPTY queue does not change this: the key still lands carrying `drained: 0`. So the grade is
  robust to a quiet DLQ, which is the normal case at most sweep slots.
- **Branch B -- the sweep writes NO status section** (no silver partitions, the return reads
  `NOT_WRITTEN (no silver partitions -- no frontier to claim)`): there is no section, so there is no
  key, and AC2's `dlq_drain_present` reads false **through no fault of the deploy**. This is an
  input-state branch, not a code branch. If a family's graded sweep lands in branch B, the honest
  grade is to re-read at the next scheduled sweep, not to roll back a correct deploy -- the same
  shape as OG-ap-12's AC2, where a criterion no deployment could satisfy was graded FAIL and the
  code was deliberately left in place.

**ROLLBACK, THE SAME FOR EVERY FAMILY, PER KEY.** Restore the prior S3 object version of
`opal-assets/opal-assets-silver-<family>.zip` in `opal-313476888478-lambda-artifacts`, re-apply, and
REMOVE that family's `silver_build_commit` row. Prior `CodeSha256` was read live at 22:0xZ and every
unpinned value equals the fd-2 ask's 17:2xZ read, so nothing moved in between; it is to be re-read
at release time. Only schwab currently carries `OPAL_BUILD_COMMIT` (`a11240c01c`); the other four
read `None`, so their prior pin is UNPINNED and their prior identity is the `CodeSha256` plus the
package-path commit that built it.

**THE PIN ROW.** `infra/aws/terraform/opal-assets/silver.tf` `local.silver_build_commit` is sparse
ON PURPOSE (today: `schwab = "a11240c01c"` only), so a family absent from the map gets no
`OPAL_BUILD_COMMIT` and therefore no plan row. Each release below adds or moves exactly ONE row, and
the plan for a `-target`ed family must read that one function changed: code fields plus the one
environment value. Any other row is a STOP.

---

## 1. schwab -- SIGN OR REFUSE ALONE

**What ships: the OG-fd-2 drain record and nothing else.** Non-drain drift **0 lines**, measured:
the package copy was byte-equal to source at the pre-fd-2 pin `4c7e933975` before the re-vendor, so
schwab carries no stale drift. `vendor-manifest.sh` copied all 11 manifest modules and `--check`
then read 11 of 11 parity; exactly ONE file moved, `schwab_runtime.py` (27 insertions, 4 deletions).

**DISCLOSED, because it is a change of ORDER and not only of content:** the drain now runs **BEFORE**
the conversion lanes, so each lane's status fold can carry the record. Previously the drain ran after
them. Nothing else in the sweep's sequence moves, and the drain's own output additionally gains
`message_ids`. This is the one item in this ask that changes when an existing action happens rather
than what it writes.

- **Blast radius:** `opal-assets-silver-schwab`'s code; both schwab lanes
  (`sr.DECLARED_SCHWAB_MASTERS`), i.e. the schwab bronze-to-silver conversion for every declared
  master. No IAM, queue or schedule change.
- **Pin row:** schwab already has one, so this MOVES it: `schwab = "a11240c01c"` -> `"12ecbe2b8f"`.
- **Rollback:** prior `CodeSha256` `YeLmNn/Tkz+HYVVrCS/PeE+mISSAnH/8ilUUxPEnCmk=`, prior S3 version
  `yvgK0D.iHoGg7Q38V0M26ZYi3RVfXBd3` (2026-10-12T23:39:26Z, 76,916 bytes), pin returned to
  `a11240c01c`.
- **Row `Z-S91`** does not close for schwab on this release: schwab already drains per-family. What
  this adds is the record that makes the drain READABLE after the fact (row `Z-S100`).

## 2. etf -- SIGN OR REFUSE ALONE

**What ships: the drain, the record, and 19 lines of other drift** -- the closest of the four to
drain-alone.

| file | drift lines | what it is |
|---|---|---|
| `mirror_conversion.py` | 17 | |
| `silver_registry.py` | 2 | the third schwab master `08403355`, inert to etf |

Drift owner (package path): `0.9.0_WK_NFRA_MCPINDEX~7` @`878fd82986`. The newest SOURCE commit inside
the drift: `0.9.0_WK_NFRA_OPLGTW~58` @`12a92ffa49`. 8 manifest modules copied; 3 files moved
(`etf_conversion.py`, `mirror_conversion.py`, `silver_registry.py`), 106 insertions, 13 deletions.

- **Blast radius:** `opal-assets-silver-etf`'s code across its **3** silver trees (`trueshares`,
  `pathfinder`, `msn`) -- etf is the one family whose `silver_families` entry names three sources.
- **Pin row ADDED:** `etf = "58ee124eb7"`.
- **Rollback:** prior `CodeSha256` `hosvkcI2IaY+NBmxqio98+dEqWmXIjBpBQqEpkA30nU=`, prior S3 version
  `OUjv4oZ4GjqBk2R0Cr98ZFuZo1EzcsUK` (2026-09-27T10:07:51Z, 60,076 bytes), pin row REMOVED.

## 3. blackdiamond -- SIGN OR REFUSE ALONE, AND THE HELD MODULES ARE WHY

**What ships: the drain, the record, and 298 lines of drift that INCLUDES work its own manifest note
calls HELD.** This is the family a half is most likely to refuse, and it is sectioned so it can be
refused without touching the other two.

| file | drift lines | what it is |
|---|---|---|
| `rebalancer_schemas.py` | 111 | HELD work the live package never received |
| `opal_strategy_matcher.py` | 91 | **MISSING_IN_PACKAGE** -- in `BUILD_MANIFEST` since `82e0a49ed2`, never vendored |
| `rebalancer_conversion.py` | 77 | HELD work the live package never received |
| `mirror_conversion.py` | 17 | |
| `silver_registry.py` | 2 | |

Drift owner (package path): `0.9.0_WK_MDPF_STRATID~5` @`82e0a49ed2` -- the commit that added
`opal_strategy_matcher.py` to the manifest without the package ever receiving it. The
bd49finsurance manifest note records the same coupling (3F-S5/S7 rebalancer work riding a
blackdiamond rebuild). `vendor-manifest.sh` copies every manifest entry unconditionally, so a
rebuild ships that whole 91-line file; it is counted in the 298 for exactly that reason.

**One build precondition was met inside Phase A and is disclosed here:** `build-and-upload.sh`
REFUSED the package until `opal_strategy_matcher.py` was registered in
`lambda-source-map.json` `files[]` (ADHC_DRIFTD.002: "Files present in source_dir but NOT in
lambda-source-map.json files[]"). That one-line registration is commit `e05a80e0d9` and is the
gate's own named Action -- `BAU_PARITY_SKIP` was NOT used. It is why this family's `build_commit`
is `e05a80e0d9` while its `vendor_commit` is `dabaa1af6b`; the package dir is identical at both.

- **Blast radius:** `opal-assets-silver-blackdiamond`'s code -- the cottonwood xlsx path AND the
  rebalancer path. The rebalancer path is the one that has never run this code.
- **Pin row ADDED:** `blackdiamond = "e05a80e0d9"`.
- **Rollback:** prior `CodeSha256` `DZl5N5IoyMTwGZI1Dl/D+40Ldd+ZzkbF60M6JFwD3Pw=`, prior S3 version
  `bkwEcG7nmfWovKOLKrWMDnymWtOMqKu5` (2026-09-27T10:06:58Z, 57,647 bytes), pin row REMOVED.
- **If this family is refused**, `Z-S91` stays open for blackdiamond and it keeps draining the whole
  shared queue -- which is the hazard that deleted an eclipse record on 2026-10-13. Refusing is a
  defensible choice; it is not a free one.

## 4. orion -- NOT ASKING YET (blocked, see section 0)

Would ship the drain, the record, and **282** lines of drift: `mirror_conversion.py` 256,
`mirror_schemas.py` 11, `silver_registry.py` 15. The package copy of `mirror_conversion.py` is a
HYBRID -- `878fd82986` patched the `Z-S3` and `Z-S25` fixes into an already-stale copy, so it equals
no source commit and a re-vendor replaces its whole text (11 commits in that file's history).
Drift owner `0.9.0_WK_NFRA_MCPINDEX~7` @`878fd82986`.

- **Blast radius if released:** orion bronze-to-silver for every feed.
- **Pin row that would be added:** `orion = "<build commit>"`, once a route unblocks the build.
- **Rollback:** prior `CodeSha256` `dO6YMv6Gi477d6/g4Jbx/WLPro60rXwtFm7hA97ne0Y=`, prior S3 version
  `Jojh09IV6nZPMKLTh5.CTvEQVGHYxCTz` (2026-09-27T10:09:30Z, 38,232 bytes).

## 5. eclipse -- NOT ASKING YET (blocked, see section 0)

Same shape as orion and the **largest** drift of the five: **398** lines --
`mirror_conversion.py` 372, `mirror_schemas.py` 11, `silver_registry.py` 15. Drift owner
`0.9.0_WK_NFRA_MCPINDEX~7` @`878fd82986`.

- **Blast radius if released:** the eclipse converter's code.
- **Pin row that would be added:** `eclipse = "<build commit>"`.
- **Rollback:** prior `CodeSha256` `QsoUUJUhw2lDaga37HU2gKo1VqZwHreRNbeZpRvE2Bg=`, prior S3 version
  `RbbMcE4omBbGLm9IRIBYZTW6Ivoa6bxB` (2026-09-27T10:08:43Z, 36,229 bytes).
- Eclipse is the family whose record blackdiamond's sweep deleted on 2026-10-13 (`Z-S91`). It is
  therefore both the clearest beneficiary of the per-family drain and the hardest to release.

---

## 6. What the two halves are being asked

**Sign or refuse schwab, etf and blackdiamond, each on its own.** For each signed family the
applier opens ledger `nfra-oplgtw-fd2-<family>-drain` (entry and sentinel first), merges that
family's build commit into `box/sitez`, applies with
`-target='module.silver_converter["<family>"]'`, reads back `CodeSha256` against the package sha256
above, and grades at that family's NEXT SCHEDULED sweep -- no ad-hoc invoke. Sweep slots, from
`silver.tf local.silver_sweep_slots`: schwab `cron(15 12)`, blackdiamond `cron(0 13)`, orion and
eclipse `cron(0 16)`, etf `cron(30 23)`, all UTC.

**And rule on orion and eclipse** by naming one of the three routes in section 0, or by refusing
both families outright -- in which case `Z-S91` stays open for them and the row records it.

A family a half refuses is not deployed, and `AP15_GRADE.json` records `released: false` with the
refusal file's `path@hash`.
