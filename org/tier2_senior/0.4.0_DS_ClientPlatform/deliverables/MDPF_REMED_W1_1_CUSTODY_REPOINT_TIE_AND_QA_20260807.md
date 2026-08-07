# MDPF_REMED.W1-1 — 49F custody repoint: the re-derived tie, the QA delta, and two false premises

**Author:** `0.4.0_DS_ClientPlatform` · **TO:** `MDPF_REMED.W1-1` @ef7b320786
**Commit:** `f999fb25f6` (atomic, 4 files) · **Date:** 2026-08-07
**Dispatches:** COO 192846Z · CTO 193650Z · CTO ruling 194804Z · MSTR deploy notice 203351Z

---

## 1. TWO PREMISES IN THE DISPATCH WERE FALSE

Both accepted by CTO at 194804Z; the false-outage framing was stood down to COO and Andrew.

### (a) There was no 09:00 crash risk. The DDB reader was DEAD CODE.

Grounded on the **deployed** artifact (158,853B, non-empty retrieval confirmed), not the repo:
`load_ddb_0824_custody_history` occurred at exactly **one** line — its own `def` at `:326`. No call
site. The live leg has always been `:939 load_rps_custody_history`, and `CUSTODY_LEG_ADAPTERS`
(`:954`) carried only `schwab_rps` and `orion_assets` — **no DDB adapter existed**, so no config
value could route to it either.
**Positive control:** 53 `^def ` matches in the same file, so the search discriminates.
A bare `ddb.scan()` in unreachable code cannot fire. Reporting it as a live crash path was a false
outage (NEVER#1), and it was already propagating through two dispatches.

### (b) "Remove the constants" as written would have MANUFACTURED the outage.

`DDB_AUA_TABLE` / `DDB_0824_CUSTODY_COHORT` are not local to that file. Deleting them alone breaks
three sites on the mdpf gold path:

| site | failure |
|---|---|
| `build_mdpf_spine.py:82` | `AttributeError` (`spine.DDB_AUA_TABLE`) |
| `mdpf_gold_consolidator.py:183` | `AttributeError` (same) |
| `route_bindings_tieout.py:146` | `KeyError` — `_ast_symbol` raises at `:95` on a missing top-level symbol |

## 2. THE REAL DEFECT — a GREEN gate asserting a FALSE fact

`route_bindings.yaml` declared the 49F custody leg as
`{type: ddb-cohort, table: "opal-assets-daily-aua", cohort: "49f_schwab_custody"}`, and its `tie`
rows required the **code constants** to equal it. `assert_bindings_current` compares **config to
those constants**. Both said DDB — so they agreed with each other, and **both disagreed with the
code that actually ran** (`fact_rps_s2`).

**A gate comparing two things that agree with each other cannot detect the drift it exists to
detect.** That is why nobody noticed the binding described a table that no longer existed.
**The fix repoints the gate's premise; it does not remove the gate.**

## 3. THE TIE, RE-DERIVED AT MY OWN SEAT (criterion 2)

I did not take the COO figures on report. Both limbs computed in the **same invocation** against
served `platinum/mdpf/49financial/aggregate-aua-timeseries.json` (`meta.basis` = `"schwab-rps"`).

| date | rows | SERVED | net+cash | net_only | d(net+cash) | d(net_only) |
|---|---:|---:|---:|---:|---:|---:|
| 2026-07-24 | 7098 | 1,681,629,958.02 | 1,681,629,958.02 | 1,649,483,876.28 | **0.00** | −32,146,081.74 |
| 2026-07-27 | 7102 | 1,684,259,082.58 | 1,684,259,082.58 | 1,653,216,875.78 | **0.00** | −31,042,206.80 |
| 2026-07-28 | 7115 | 1,689,768,669.73 | 1,689,768,669.73 | 1,657,682,233.53 | **0.00** | −32,086,436.20 |
| 2026-07-29 | 7123 | 1,678,057,669.35 | 1,678,057,669.35 | 1,650,908,393.08 | **0.00** | −27,149,276.27 |
| 2026-07-30 | 7130 | 1,696,469,951.41 | 1,696,469,951.41 | 1,671,057,021.90 | **0.00** | −25,412,929.51 |
| 2026-07-31 | 7138 | 1,696,400,394.33 | 1,696,400,394.33 | 1,671,631,893.72 | **0.00** | −24,768,500.61 |
| 2026-08-03 | 7141 | 1,706,973,077.81 | 1,706,973,077.81 | 1,681,360,430.85 | **0.00** | −25,612,646.96 |
| 2026-08-04 | 7144 | 1,726,822,601.93 | 1,726,822,601.93 | 1,701,212,997.03 | **0.00** | −25,609,604.90 |
| 2026-08-05 | 7144 | 1,724,877,753.85 | 1,724,877,753.85 | 1,699,571,113.13 | **0.00** | −25,306,640.72 |

**POSITIVE limb** `SUM(net_mv_plus_cash)` — exact (<1c) on **9 of 9**.
**NEGATIVE CONTROL** `SUM(net_mv_positions)` — exact on **0 of 9**, missing **$24,768,500.61 –
$32,146,081.74**.

The negative limb failing on *every* date is what makes the positive limb evidence rather than
coincidence. A run publishing only the passing limb is not a control.

⚠ **BOUND, not overstated:** the tie covers the **9 post-7/23 dates where both series exist**.
**PRE-7/23 IS UNTESTED** and may differ. The repoint only has to be right going forward.

*Minor discrepancy noted, not chased: the served artifact's `meta.as_of_last` reads `None`, not
`2026-08-05` as the TO stated. Immaterial to the tie (the axis ends where it ends), but recorded
rather than smoothed over.*

## 4. WHAT CHANGED — atomic across 4 files

1. **`dim_mdpf_aggregate_aua_timeseries.py`** — dead DDB reader, its FALSE docstring, and both
   constants deleted. No `dynamodb` client remains (verified: zero non-comment lines mention
   `ddb`/`dynamodb`). Replaced with the measurement and the pre-7/23 bound.
2. **`route_bindings.yaml`** — 49F `custody_leg` re-declared as `s3-monolith-silver` /
   `schwab/08242234/silver` / `fact_rps_s2` / `net_mv_plus_cash`; tie rows repointed to
   `SCHWAB_SILVER` + two code-literals. **The old authority text is PRESERVED STRUCK-THROUGH** with
   the `F-1 / C-1` citation visible — CTO-ruled 194804Z: *deleting a false claim also deletes the
   evidence it was ever believed, so the next reader cannot tell whether the basis was decided or
   never considered.*
3. **`build_mdpf_spine.py`** + 4. **`mdpf_gold_consolidator.py`** — both C-1 assertions repointed to
   the new source shape. **Repointed, not removed.**

## 5. EXERCISED, NOT ASSERTED

| check | result |
|---|---|
| `route_bindings_tieout.py` | **34 tie rows, 34 TIE / 0 FAIL** (was 33; 2 rows → 3) |
| both gates, real bindings (control) | **PASS** |
| both gates, mutated `prefix` | **FIRED** |
| both gates, mutated `fact` | **FIRED** |
| both gates, mutated `field` | **FIRED** |
| honest-absent contract (criterion 3) | axis mixing real + partition-less dates → 2/4 covered, both absent dates **NAMED in `__missing__`**, key not present, **0 silently zeroed, 0 silently carried** |
| cross-check | exercised values (08-04 `1,726,822,601.93` / 08-05 `1,724,877,753.85`) equal the tie table's served points exactly |

A gate that cannot fail is not a gate — hence the mutation row for each of the three source fields.

## 6. THE DEPLOY ASYMMETRY THAT WOULD HAVE CAUSED A REAL OUTAGE

MSTR pushed `f999fb25f6` at 20:28Z; the pre-push gate deployed **3 scripts** and flagged that the
**4th file — `route_bindings.yaml` — is not a script and did not ride the script deploy leg.**

That flag was correct and it was load-bearing. Measured immediately after:

```
s3://opal-data-mdpf/code/config/route_bindings.yaml
  dated 2026-08-04, 12,008B  ->  :58  source: {type: ddb-cohort, table: "opal-assets-daily-aua", ...}
```

The EC2 runner **syncs that config from S3** (`mdpf-daily-dispatch.sh:130`, `--delete`) and the
spine refuses without it (`:136`). So the **new code was deployed against the OLD bindings**: the
repointed C-1 assertion would have read `cus.get("prefix")` → `None`, mismatched, and raised
`SystemExit("BINDINGS STALE")` **at the 09:00 fire.**

**Closed:** uploaded to `s3://opal-data-mdpf/code/config/route_bindings.yaml`, pre-state ETag pinned
(`56a03a14…`, key-exists = update, not a first-mint), verified byte-identical on a fresh non-empty
retrieval (13,516B, sha256 `98f5e9c5…`).

> **This is the partial-landing hazard the atomic commit existed to prevent, arriving through the
> DEPLOY layer instead of the code layer.** An atomic commit is not an atomic deploy.

## 7. THE AD-HOC QA RUN (sanctioned for QA; the schedule stays the production path)

Run against the **deployed** bytes and the **deployed** bindings, in a layout mirroring the runner
(`scripts/gold/` + `../../config/`) — not against my working tree.

```
[modelb-spine] bindings asserted current (schema + bucket + firm set + C-1 custody row)
fact_rps_s2 custody history: 440/440 axis dates covered; 0 NAMED gap(s) (no interpolation)
OK: cross-axis gate PASS (49financial) -- no foreign-day roster across 440 dates
OK wrote 49financial_aggregate_aua_timeseries.json (188,940B)   [LOCAL only, never S3]
```

**THE DELTA vs the currently served artifact:**

| measure | value |
|---|---|
| overlapping dates | **439** |
| **49F `partner_custody_total` differing dates** | **0 of 439** |
| dates only in BUILT | 1 (`2026-08-06` — the axis advancing, a new trading day) |
| dates only in SERVED | 0 |
| basis (served vs built) | `schwab-rps` vs `schwab-rps` |

**NEGATIVE CONTROL on the comparator:** injecting +$1.00 on 2026-08-05 → **detected = True**. The
zero is a measurement, not a blind comparator.

**VERDICT: ZERO CHANGE on 49F custody. The repoint is a true no-op on served values, confirmed by
running it rather than by inheriting the claim.**

## 8. PRE-EXISTING FINDINGS THE RUN SURFACED — NOT MINE, NOT REGRESSIONS

The producer's own honest surfacing. Recorded because a QA run that only reports its own success
is not a QA run. **None of these are caused by this change and I did not investigate them:**

- `ROW11 frontier-stamp STALE (49financial)`: the frontier cell wears `2026-08-06` but its count was
  measured as of `2026-08-04` — 2 trading days earlier.
- `FINDING axis diff`: `aum_daily-only (non-canonical)=['2025-01-09']` — a non-canonical day in the
  aum_daily feed; the build correctly proceeds on the canonical NYSE axis.
- `cross-axis (v) SKIPPED for 49financial` — **RETAINED STRUCTURAL EXPOSURE, explicitly "not a clean
  result"**: 205 per-band presence disagreements across 33 dates, **UNCHECKED**. The 49F decouple is
  named as a prerequisite.

## 9. RESIDUAL / NOT CLAIMED

- **The Lambda package is NOT re-cut.** `mdpf-gold-lambda/build_package.py:51` packages
  `route_bindings.yaml` into the zip with a recorded sha256 (`:108`). **If the 09:00 path executes
  via the Lambda rather than the EC2 runner, that package still carries the OLD bindings and my
  repointed assertions would fail there.** Lambda deploys are Terraform-only (Rule 1) and are not
  the DS lane — **surfaced to CTO/AE, not actioned by me.** I verified the EC2 path; I did **not**
  verify the Lambda path, and I am not claiming it.
- `trading_calendar.py` is **not** present in `s3://opal-data-mdpf/code/scripts/gold/` (only the
  retired `_trading_day_calendar.py` shim and `mdpf_calendar_binding.py`). My QA run needed the repo
  root on `PYTHONPATH` to resolve it. Whether the EC2 runner provisions it another way is
  **UNVERIFIED** — flagged, not diagnosed, and explicitly **not** called a break.
- Stale orphan bytecode `__pycache__/mdpf_emit_49f_leg.cpython-312.pyc` matches the old constants;
  its source no longer exists. Not a live site.
- **Cottonwood (`MDPF_COTTONWOOD.FIX1`) rode the same window but is INERT** ($0.00 delta; the binding
  filter is the bronze harvest seed). Per CTO 194804Z, kept as two separate claims: **a clean run
  tonight is evidence Cottonwood is HARMLESS, not evidence it works.**
