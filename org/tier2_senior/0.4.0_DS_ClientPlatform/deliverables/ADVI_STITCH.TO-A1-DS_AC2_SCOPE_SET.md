# ADVI_STITCH.TO-A1-DS — AC2 / `STI-b-0` — THE MIGRATION SCOPE SET

**Cell:** `STI-b-0` (+ `STI-g-5`) · **Criterion:** `STIA1DS-AC2` · **Grounding class:** SOURCE
**Seat:** `0.4.0_DS_ClientPlatform~Q` · **Issuer:** `2.0.0_SA_COO`
**PINNED VINTAGE (UTC):** `2026-08-25T20:47:26Z` (counts) · `2026-08-25T21:1xZ` (grain enumeration)

⛔ **THIS LIST IS DECLARED BEFORE ANY OBJECT MOVES. NOTHING HAS BEEN COPIED.**

`STI-b-0` exists because a migration scoped to a BUCKET has no denominator and its completeness can
never be checked (decomp finding 1). This file is that denominator.

---

## 1. THE DECLARED SOURCE SET — 4 of 30, and **ONE OF THE FOUR IS PARTIAL**

⚠ **"4 prefixes of 30" is true at top level and MISLEADING on its own.** Three of the four are
whole-prefix members; `gold/` is a **PARTIAL** member contributing **7,273 of its 73,563 keys (9.9%)**.
A scope set that says "gold/ is in territory" without that qualifier implies 73,563 objects move when
7,273 do. **Rule 24(ii), same grain: a whole-prefix member and a partial member cannot sit unmarked in
one list.**

| # | source prefix (`s3://opal-data-bd/`) | membership | keys IN | keys in prefix | bytes IN |
|---|---|---|---|---|---|
| 1 | `backfill_v2/` | **WHOLE** | 292 | 292 | 2,467,990,218 |
| 2 | `forwardfill_v2/` | **WHOLE** | 640 | 640 | 5,244,616,142 |
| 3 | `silver/` | **WHOLE** | 7,916 | 7,916 | 2,788,114,373 |
| 4 | `gold/canonical/performance/` | partial-of-`gold/` | 2,424 | — | 416,347,623 |
| 5 | `gold/canonical/nna/` | partial-of-`gold/` | 2,424 | — | 274,709,638 |
| 6 | `gold/canonical/holdings/` | partial-of-`gold/` | 2,425 | — | 1,805,185,077 |
| | **rows 4–6 = the `gold/` member** | **PARTIAL** | **7,273** | **73,563** | **2,496,242,338** |
| | **TOTAL DECLARED** | | **16,121** | | **12,996,963,071 B (12.10 GiB)** |

**Source root is `s3://opal-data-bd/`.** Measured against the alternative root: the same four prefixes
under `opal-data-assets/blackdiamond/49f/` hold `0 / 0 / 62 / 0` keys against `292 / 640 / 7,916 /
21,828`; `49f/` holds 285 keys total, children exactly `_ops/ bronze/ gold/ meta/ silver/` (5 of 5
enumerated). `49f/` is the legacy ALIAS and **nothing under it moves** (`2.0.0_SA_COO` 71407);
its non-empty `silver/` is the positive-control target `STI-b-4` names, not a migration source.

---

## 2. THE DESTINATION SET

| source | destination |
|---|---|
| `backfill_v2/`, `forwardfill_v2/` | `s3://opal-data-assets/blackdiamond/49financial/bronze_legacy/{family}/{date}/` |
| `silver/` | `s3://opal-data-assets/blackdiamond/49financial/silver_legacy/{table}/date={D}/` |
| `gold/canonical/{performance,nna,holdings}/` | `gold/advi/reference/bd_legacy_{performance,nna,holdings}` |

`49financial/` is the deliberate in-grammar mint (Rule 17b `{vendor}/{firm}/{medallion}`), EMPTY at
issuance because nobody has minted it (`2.0.0_SA_COO` 71407). `0.4.0_DS_ClientPlatform~J` mints
`{bronze,silver}/insurance_*` into the same parent; mine are `*_legacy/`. **Different leaves, same
parent — I touch none of theirs and assume none of their mint exists.**

---

## 3. OUT OF TERRITORY — named so absence is a DECISION, not an omission (`STI-g-5`)

### 3.1 The 26 untouched top-level prefixes (26 of 30, all 26 named)

`GOOD_RUN_2026-01-21_1015AM/` · `_rollback/` · `ajb_workspace/` · `blackdiamond/` · `bronze/` ·
`canonical/` · `code/` · `config/` · `debug/` · `diagnostics/` · `gldrst/` · `lambda-deploy/` ·
`lambda-layers/` · `lambda-packages/` · `logs/` · `platinum/` · `qa-scratch/` · `runs/` · `schwab/` ·
`scripts/` · `smartx/` · `ssm-output/` · `status/` · `temp/` · `tmp/` · `v4_output/`

**COVERAGE CHECK, computed not eyeballed: 4 IN + 26 OUT = 30 = the measured top-level denominator.
Overlap(IN, OUT) = {} and IN-missing-from-tree = {}. CLOSES.**

⚠ **THE SET-DIFFERENCE WAS COMPUTED, AND THE FIRST HAND-WRITTEN VERSION OF THIS LIST WAS WRONG** — it
carried `silver/` into the OUT column with an "→IN" annotation, which would have made a section
asserting "26, all named" enumerate 27. **The same class this TO's AC1 caught in `b-5`: a total that
looks right beside a membership that is not.** Recomputed from the live listing by set difference.

*(Name-collision note: top-level `bronze/` and `canonical/` are distinct objects from the
in-territory `silver/` and from `gold/canonical/` — which is exactly why the scope set is a PATH
list, never a name list.)*

### 3.2 The 8 `gold/canonical/` children that STAY (8 of 11, all named)

| child | keys | | child | keys |
|---|---|---|---|---|
| `account_gains/` | 2,424 | | `nna_atomic/` | 2,374 |
| `advisor_fee_detail/` | 2,244 | | `nna_validation/` | 2,424 |
| `holdings_gaps/` | 654 | | `role_aua/` | 2,374 |
| `lots_realized/` | 1,402 | | `watermarks.json` | 1 (object) |
| `lots_unrealized/` | 658 | | | |

**11 of 11 canonical children enumerated: 3 IN (7,273) + 8 OUT (14,554) = 21,827 + `watermarks.json`.**

### 3.3 What stays in `gold/` overall

`gold/` holds **33 child prefixes + 21 top-level objects**. **73,563 total keys − 7,273 moving =
66,290 STAY PUT**, including every surface `STI-a-3` names by hand (`entities/`, `client_timeseries`,
`positions_cube`, `role_aua`, `advisor_fee_detail`, the dormant `clients/` twin).

---

## 4. BOTH-DIRECTIONS TRACEABILITY — the rule, stated before the copy

- **FORWARD** — every declared source key must land: `16,121` source keys → `16,121` landed keys.
- **REVERSE** — every landed key must trace to a listed source prefix: any landed key not reachable
  from rows 1–6 of s.1 is a **defect**, not a bonus.
- Equality is asserted against the **PINNED MANIFEST captured at copy time**, never a fresh `ls` at
  verification time. Three of the four source planes are still live (`AC1` s.2), so a live re-list
  would report a false mismatch on any day a producer runs between the two reads.

---

## 5. `STI-a-4` / AC6 BASELINE — captured BEFORE any work (NEVER#3)

`s3://opal-data-bd/gold/timeseries/account_performance.parquet` — the LIVE SERVED series, **read-only,
not moved, not touched**.

| field | value at `2026-08-25T21:17:31Z` |
|---|---|
| `VersionId` | `dqCah5NzuhEqJW8UqK0UEjBQIrytzwpz` |
| `ETag` | `"9c22cd22a993da4fb66066ce428ae144-28"` |
| `Size` | 229,138,778 |
| `LastModified` | Tue, 25 Aug 2026 05:03:14 GMT |

⚠ **The `-28` suffix means this ETag is MULTIPART — it is NOT a content digest** and must not be
compared against any single-part hash. **`VersionId` is the sound AC6 oracle:** on a versioned bucket
an unchanged `VersionId` proves the object was never rewritten, which is exactly the AC6 claim.

**It is UNREACHABLE from the scope set by construction** — `gold/timeseries/` is not a declared source
prefix, and the `gold/` member reaches only `gold/canonical/{performance,nna,holdings}/`.

---

## 5a. BINDING AMENDMENTS CARRIED INTO THIS DECLARATION (`2.0.0_SA_COO` 71467)

Both AC1 calls were ruled and are binding from 71467. They constrain how this scope set is consumed:

- **AC5 / `STI-inv-5` amended** — the immutability invariant binds the **LANDED SET**, keyed on the
  **content sha256 of the landed copy against the PINNED MANIFEST**, never a live source re-read. The
  frozen `performance`/`nna` reference is labelled **SNAPSHOT-AT-VINTAGE**, never "the closed period".
  *Operative reason: read against the live source, the alarm and healthy BD restatement are
  byte-identical, and a control that fires on healthy data gets suppressed.*
- **AC13 amended** — reads **16,121 objects / 12.10 GiB**, replacing ~8,800 / ~13 GB.

⛔ **`blackdiamond/49f/` NOW PLAYS TWO ROLES THAT PULL OPPOSITE WAYS, AND IS A SOURCE IN NEITHER**
(`2.0.0_SA_COO` 71467): it is **AC4's DENY TARGET** (no landed key may appear under it) *and*
**`STI-b-4`'s POSITIVE CONTROL** (an existing `49f/silver` key, in a separate invocation, proving the
IAM probe can return ALLOW). A single prefix serving as both the thing that must fail and the thing
that must pass is legitimate here only because the two tests ask different questions of it — but it
must never be read as a migration source.

## 6. VERDICT

`STIA1DS-AC2` **DECLARED — awaiting the copy it gates.** The list is committed before the first copy;
denominators close both directions (4+26=30 top-level; 3+8=11 canonical children); the partial
membership of `gold/` is marked rather than hidden; the served series' pre-state is pinned.

**Nothing has been written to any bucket. No object has moved.**
