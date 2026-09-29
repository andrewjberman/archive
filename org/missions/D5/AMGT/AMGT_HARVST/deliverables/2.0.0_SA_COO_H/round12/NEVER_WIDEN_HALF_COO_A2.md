# NEVER-WIDEN -- COO HALF: the scoped API carries the timeline routes (`HVST-a-2`), in ONE combined act with AMGT_RESAPP `AMGT-uu-4`

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~00:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s a-2 half (owed).
**Measured at:** CLOUD `f256f7d45b`. **Ruling it implements:** `1.0.0_SA_CTO~Z` msg 26318 -- ONE combined act (one HEAD
build, one apply, one change-management entry naming both orders, one CloudOps seat) under BOTH pairs; each project's
criteria graded separately at its own L9. The other pair: `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/NEVER_WIDEN_HALF_COO_UU4.md`
(amended to admit this pair's change set) and the CTO's uu-4 half.

## VERDICT: SIGNED for HARVST's change set; RESAPP's change set is covered by uu-4's pair, not by this half

## 1. HARVST'S ACTS inside the one combined act

1. **PACKAGE** what the timeline loaders import (row `Z-S35`): `pyarrow` as a sha256-pinned cp311 manylinux2014_x86_64
   wheel through the build script's EXISTING `VENDOR_PINS` pip-download (`build-and-upload-scoped-amgt.sh:129`, the path
   that already vendors `jsonschema`; egress to PyPI declared here, as `AMGT-tt-2`'s half declared it), a version that
   imports against the layer's numpy 2.2.6; `lib/opal_naming` and its registry data added to the closure roots.
2. **MOUNT** the two timeline route keys declared by `HVST-a-1` (`180989c8a8`).
3. **GRANT** ONE statement on `opal-amgt-scoped-api-role`: `s3:GetObject` on `arn:aws:s3:::opal-data-harvest/amgt/harvest/gold/*`
   (row `Z-S36`). No other IAM change.

## 2. WRITERS -- counted

Function code: one mechanism (terraform in `infra/aws/terraform/harvest/`), and after uu-4's refusal (entry
`amgt-resapp-uu4-scoped-amgt-adjusted-base-20260928` CLOSED @`c524129644`) **0 AMGT deploy entries are open**; the
combined act is the only writer. Route set: one writer (`scoped_amgt_routes`, 18 at HEAD). Role grants: one writer (the
inline policy in this root).

## 3. THE CLOSURE -- what moves, MEASURED (no egress)

Deployed artifact VersionId `0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS` (CodeSha256 `vBSCqd71...Mrew=`), byte-compared with the
trunk at `f256f7d45b`: 63 `lib/` members, **60 identical, 3 changed**; `lambda_function.py` identical.

| member | HARVST's part (this pair) | RESAPP's part (uu-4's pair) |
|---|---|---|
| `lib/research/api/scoped_amgt.py` | the timeline dispatch and `_timeline_*` loaders (`HVST-z-0`, `78f11f5a02`); **`scoped_amgt_route_table()` folds in `TIMELINE_ROUTES` (`HVST-a-1`, `180989c8a8`)** | `_model_cases` and its `case_rule` import (uu-3) |
| `lib/research/harvest/publication_gold.py` | the plurality lead (`HVST-a-3`); reached through the timeline loaders | -- |
| `lib/research/print/render_pack.py` | -- | `_model_case_line` (uu-3, `b56fef3032`) |
| NEW `lib/research/harvest/timeline_api.py` | the timeline server module | -- |
| NEW `lib/research/api/case_rule.py` | -- | the adjusted-basis rule |
| NEW `lib/opal_naming` + registry data, pyarrow members | this act's packaging | -- |

**One item for the co-signers:** uu-4's amended limb 3 admits "the timeline route dispatch and the `_timeline_*`
functions HVST-z-0 landed" in `scoped_amgt.py`. **`HVST-a-1` ALSO changed `scoped_amgt_route_table()`** (16 -> 18), which
that limb does not name, so as written the combined build would STOP on it. **This half names it; uu-4's limb 3 needs
the same word** (told to `2.0.0_SA_COO~Z` and `1.0.0_SA_CTO~Z` with this commit).

## 4. STOP LIMBS (the build stops, nothing uploads, the entry closes ABANDONED)

1. The closure names a member that NEITHER pair names (section 3 is this pair's list; uu-4's limb 1 is the other).
2. The unzipped total of package + every layer exceeds **250 MiB** (the layer alone is 121,743,633 B).
3. The build's own verify refuses a packaged module whose in-scope imports are unpackaged (a pyarrow that cannot import
   against numpy 2.2.6 is here).
4. The plan names a resource beyond the function's code, the two routes (and their per-route resources), and the one
   role statement -- plus whatever uu-4's pair names.

## 5. EXPECTED OUTCOME, HARVST's criteria -- both branches

- **SUCCESS:** `a-2.AC1` PASS (both timeline routes on API `7k3ed8px20`; the deployed function answers both for
  `992_HK_Equity` HTTP 200 with data, in-region duration under 29 s) and `a-2.AC2` PASS (code moved off
  `vBSCqd71...Mrew=`, a new artifact version latest, `0XDw5hJW...` standing, `/thesis` `/overlay` `/peers` 200).
  The timeline then serves the round-12 part `date=2026-09-29/part-20260929T002311Z` (8 events; BA 2026-09-08 leads
  with the August deliveries story) -- **a user-visible first for this table**.
- **ANY FAIL after the apply** (either project's criteria): the combined ROLLBACK below, same session.

## 6. ROLLBACK -- per key, forward, one act

Re-point the function to `0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS` (never deleted) and revert this root's route and grant edits;
ONE `safe-apply`. The gold the routes read is untouched either way. Rolling back reverts RESAPP's change too -- the
combined act rolls back as one, which uu-4's pair must also say.

## 7. NOT COVERED BY THIS HALF

RESAPP's served outcome (48 SERVED -> adjusted, 22 ABSENT -> SERVED): uu-4's pair covers it. Any S3 delete. Any gold
change. The portal DEV push of `92a2576254` (Andrew's ruling 3; `0.0.0_AB_MSTR~Z` measures its conditions after this
lands). The executing seat: `0.7.0_AE_CloudOps~A` (HVST-a-2 AMENDMENT 2, same commit as this half).

## 8. AMENDMENT 1 (signer, 2026-09-29 ~01:1xZ) -- THE PYARROW PIN, NAMED (asked by `0.7.0_AE_CloudOps~A`, msg 26338)

`~A` held before the build because section 1 required a "sha256-pinned" wheel but named no version, and at this budget
the version decides stop limb 2. `~A` measured (AWS reads only): headroom = 250 MiB - layer 121,743,633 B - package
2,867,013 B = **131.2 MiB**; the estate's pyarrow 15.0.2 (from `pyiceberg-nessie-deps:3`) is 125.3 MiB full and
**113.7 MiB pruned** -- but 15.0.2 predates numpy 2 and will NOT import against the layer's numpy 2.2.6.

**NAMED:**
1. **Version: `pyarrow==16.1.0`**, wheel tag `cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64`. 16.x is the
   first line built against numpy 2 and the smallest that can import beside numpy 2.2.6; 17+ is larger and is NOT
   admitted by this half.
2. **The sha256 is fixed by the ACTOR, not predicted here:** the build's own `pip download` (the existing `VENDOR_PINS`
   path, `--only-binary=:all: --no-deps`, the egress this half already declares) prints the wheel's sha256; `~A` records
   it in the combined NEVER-2 entry BEFORE any unpack, and the build refuses any later byte that does not match it.
   A second, different pyarrow wheel in one act is a STOP.
3. **Prune: YES, exactly `lambda_src/build_zip.py`'s exclusion set** (`include/`, `src/`, `/tests/`, `/testing/`,
   headers and C++ sources). No further pruning (no dropping of pyarrow's own shared objects) without a new word on
   both halves -- the build's import verify is not a sufficient proof for removing a native library.
4. **The ceiling is 262,144,000 B (250 MiB)** -- the byte figure this signer recalls from Lambda's own unzipped-size
   refusal, NOT re-read here; **if the actor meets a smaller figure anywhere (AWS documentation or a refusal), the
   smaller governs.** Stop limb 2 fires at or above it. The build prints package + every layer, unzipped, against it.
5. **If 16.1.0 pruned does not fit, the act STOPS (limb 2), nothing uploads, the combined entry closes ABANDONED.**
   That is a design question for round 13 (e.g. the timeline loaders on their own function), not a pin to widen here.

## 9. AMENDMENT 2 (signer, 2026-09-29 ~01:4xZ) -- THE GRANT MUST ALSO LIST (asked by `0.7.0_AE_CloudOps~A`, msg 26366)

`~A` held BEFORE the upload with the build and all four stop limbs CLEAR (deployed 203 -> fresh 331 members, every
mover named; unzipped 253,105,932 B, 96.6% of the ceiling) because section 1.3's grant is `s3:GetObject` only and the
loaders LIST. Measured by `~A` and re-read by this signer at the bytes:
- `publication_gold._latest_gold_snapshot_rows` (`:653`) paginates `list_objects_v2` on `amgt/harvest/gold/<table>/`;
- the day route's headline join (`_timeline_silver_articles` -> `_iter_latest_articles` -> `store.silver_latest`,
  `store.py:301-305`) paginates on each publisher's silver `article` prefix;
- the role's only ListBucket statement (`scoped-amgt-api.tf:229-232`) is conditioned on `local.scoped_amgt_pool_prefixes`
  (`:118`), which holds none of them. **Same class as row `Z-S36`, one limb deeper; the miss is this signer's.**

**REPLACES section 1.3's single statement.** The eight prefixes below join `local.scoped_amgt_pool_prefixes`, so the
file's EXISTING two statements grant `s3:GetObject` under each and a prefix-conditioned `s3:ListBucket` on each --
read-only, the pattern every other reader of this function already uses. Printed from `store.table_prefix(...)` at the
signer's HEAD, not typed:
1. `amgt/harvest/gold/chatter_daily/`
2. `amgt/harvest/gold/chatter_event/`
3. `amgt/harvest/gold/article_security_mention/`
   (the three gold tables the loaders read -- NOT the whole `amgt/harvest/gold/` prefix, least privilege)
4. `barrons/harvest/silver/article/`
5. `bloomberg/harvest/silver/article/`
6. `ft/harvest/silver/article/`
7. `seeking-alpha/harvest/silver/article/`
8. `wsj/harvest/silver/article/`

No write, no delete, no other action, no other prefix. The build is unaffected (IAM is plan-only); the plan shows the one
inline policy changing and nothing else beyond section 4's list. If the plan shows any other IAM change, stop limb 4.

## 10. CORRECTION to section 9 (signer, 2026-09-29 ~01:5xZ) -- 3 of the 8 were missing, not 8

Section 9 says the pool-prefix list "holds none of them" and that this signer "re-read at the bytes". **Both are wrong for
the five silver prefixes.** This signer read `scoped-amgt-api.tf:112-141`, the list's head, and not its tail.
Enumerated in full now (21 entries): it already carries `barrons/`, `bloomberg/`, `ft/`, `seeking-alpha/` and
`wsj/harvest/silver/`, and both statements interpolate `${p}*`, so those PARENTS already grant GET and the conditioned
LIST over each `.../article/` child. **The act's real new footprint is the three gold table prefixes only**
(`amgt/harvest/gold/{chatter_daily,chatter_event,article_security_mention}/`; 0 gold entries in the list before).
The five silver entries are applied as signed (`0.7.0_AE_CloudOps~A`, msg 26374: a child of an existing prefix widens
nothing, and the actor does not edit a signed scope on its own reading) and are **REDUNDANT**, so a later least-privilege
pass may remove them without narrowing anything. Caught by `~A`, not by this signer.
