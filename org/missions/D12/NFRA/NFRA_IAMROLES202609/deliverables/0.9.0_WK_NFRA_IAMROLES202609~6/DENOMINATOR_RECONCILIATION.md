# NFRA_IAMROLES202609 — IAM-r-2: what 191, 208, 216 (and 219) each count

**Cell:** `IAM-r-2` (FWD-1). **Worker:** `0.9.0_WK_NFRA_IAMROLES202609~6`. **Worktree HEAD at
measurement:** `cccb4fac8351dbcdf547382b0c733f20ffc62667`, branch `wk-NFRA_IAMROLES202609-6`, cut from
SITEZ HEAD. **Measured (this cell), 2026-09-10.**

⛔ **NO NUMBER IS SUBSTITUTED FOR ANOTHER BELOW.** Per figure: which INSTRUMENT produced it, at what
VINTAGE, over what POPULATION, and what that instrument CANNOT SEE. Where a reconciliation is
established it is stated with its own evidence; where it is not, that is recorded as a finding, not
smoothed over.

---

## Figure 191

- **Instrument:** `comp-iam stats` / `comp-iam roles` / `comp-iam gaps` — the DEFAULT, Terraform-ONLY
  parse mode. Chain: `.tools/comp-iam` → `org/modules/graph/iam_cli.py::cmd_stats/cmd_roles` →
  `org/modules/graph/extract_iam.py::build_iam_report()`. It reads `infra/aws/terraform/` source
  directly (AST/regex over committed `.tf` files) and makes **no live AWS call and no graph read at
  all**.
- **Vintage:** first cited as "the round-1 governance disposition['s]... a fresh `comp-iam` parse"
  (PRD `:323`, no timestamp given there). **RE-MEASURED by this cell just now**, at worktree HEAD
  `cccb4fac83`, 2026-09-10 (run twice, back to back, identical both times):
  ```
  IAM roles parsed:     191
  Services scanned:     188
  Lambda services:      167
  EC2 services:         21
  Total operations:     1084
  Permission gaps:      304
  ```
  and `comp-iam roles` independently prints `IAM ROLES (191 found)` with 191 `tf_resource:` lines.
- **Population:** distinct Terraform **IAM-role resource declarations** (one label/block in the
  committed `infra/aws/terraform/` tree), **not** live AWS ARNs and **not** expanded across
  `for_each`/`count` — one TF block counts as ONE regardless of how many live role instances it
  produces.
- **What it cannot see:** (a) by construction, any live role with no Terraform declaration at all —
  the entire undeclared population is structurally invisible to a TF-only parse; (b) multiple live
  instances created by one `for_each`/`count` block collapse to a single count here — `comp-iam live`'s
  own output says so directly: *"That is why `${each.key}` fleets resolve here and do not on the
  Terraform-primary surfaces"*; (c) this exact instrument emits its own NOTEs, reproduced on this
  cell's run above, that the TF role labels `orchestrator` and `scheduler` were **each reused across
  three modules and silently mis-linked before a fix** ("now module-namespaced"), so its role count is
  demonstrably a measurement of the parser's reach as much as of the estate.
- **Claim:** `measured` (this cell's own fresh run, twice, identical).

### ⚠ The arithmetic trap named in this cell's bound, run down

The decomposition's own round-2 battery section states *"195 TF roles / 188 services / 1084 operations
/ 304 gaps"* for this same instrument, and surprise row `NFRA_IAMROLES202609-Z-S1` (`2.0.0_SA_COO~ZI`,
surfaced `2026-09-10T05:39Z`) independently cites the identical `195`. **This cell could not reproduce
195.** Measured directly:

- `services`, `operations` and `gaps` in this cell's fresh run (188 / 1084 / 304) match the
  decomposition's battery section **exactly** — only `roles` differs (191 here vs 195 claimed there).
- `git log --since=2026-09-10T05:00:00Z --until=2026-09-10T13:30:00Z -- infra/aws/terraform/` (spanning
  from before `Z-S1`'s vintage through the decomposition's own commit `5b460996ee` at `12:45:53Z` to
  this cell's HEAD `cccb4fac83` at `12:58:12Z`) returns **zero commits** — the *committed* Terraform
  tree did not move across that whole span.
- `git log -- org/modules/graph/extract_iam.py` shows no commit since `2026-07-25`; the role-counting
  logic itself has not changed today.
- `git status --short -- infra/aws/terraform/` in this worktree is clean; 415 tracked `.tf` files.

Against an unchanged committed tree and an unchanged tool, `195` does not reproduce and `191` does,
twice. **This cell does not assert a cause** (the likeliest is an uncommitted/transient Terraform
state in whichever worktree produced the `195` reading — unprovable from here since nothing of the
kind was ever committed) — only the measurement: **`195` is `held` (repeated without independent
reproduction) and this cell's own attempt to verify it against the committed tree FAILED.** `191` is
the number this cell can stand behind as `measured`.

---

## Figure 208

- **Instrument:** `comp-iam live` (LIVE-PRIMARY mode) as cited in brief `F2`, run by `1.0.0_SA_CTO~Z`.
  It does **not** parse Terraform for its population; it reads a **materialized graph**
  (`kuzu_nessie_db`) that is built by a separate derive/stitch process and cross-references the graph's
  live roles against Terraform only to label each `DECLARED` / `LIVE-no-DECLARED`.
- **Vintage:** `2026-09-03T02:00:31Z`, flagged **STALE** at 158.5h old when the brief cited it;
  incremental-mutation pipe **UNVERIFIED**, population cross-check **UNAVAILABLE** at that time (brief
  `F2`).
- **Population:** live AWS IAM roles present in that graph snapshot as of that vintage — 208 total, 192
  cross-referenced `DECLARED`, 16 `LIVE-no-DECLARED`.
- **What it cannot see:** any role created or deleted in live AWS after the snapshot vintage; at the
  time the figure was cited, the tool itself could not even certify "snapshot plus subsequent
  mutations" because the incremental pipe check had not been run — only the raw snapshot was available,
  and the tool's own banner calls itself a **DETECTOR, not an oracle** (no Deny/boundary/condition/SCP
  evaluated).
- **Claim:** `held` (this cell did not re-run the tool AT that 2026-09-03 vintage — that snapshot is
  superseded and no longer the graph's current state; see the re-measurement below).

### Re-measured by this cell, right now

`comp-iam live` (no flags, this cell, 2026-09-10):
```
LIVE PROVENANCE: materialized graph (kuzu_nessie_db) -- population and vintage read from the ROWS
  cohort vintage (observation time carried by the ROWS, not the table write):
    full-derive: 219 node(s), newest 2026-09-10T02:50:38Z (age 10.4h) (< 24h cadence)
LIVE-PRIMARY IAM  (population = 219 live roles, from the graph)
  DECLARED (live AND governed by IaC) : 203
  LIVE-no-DECLARED                    : 16
```
**This is the SAME instrument reading the SAME substrate at a NEWER vintage** — the tool names its own
provenance as `kuzu_nessie_db`, the identical store `comp-find --corpus aws` reads (see Figure 219
below). The population has moved with time (208 → 219); the undeclared count has not (16 → 16). This
is direct, first-party evidence that `208`'s difference from `216`/`219` is a **vintage** effect on one
instrument family, not a different population definition — see Reconciliation below.

---

## Figure 216

- **Instrument:** `comp-find --corpus aws IAM_ROLE` — a served projection off the same `kuzu_nessie_db`
  graph substrate, cited in the PRD (`:297-298`) as "re-measured at the merged head" and in brief `F2a`.
- **Vintage:** `2026-09-09T14:59:48Z` (brief `F2a` table).
- **Population:** 216 live `IAM_ROLE` graph nodes; `DECLARED=200`, `LIVE-no-DECLARED=16`.
- **What it cannot see:** the same family of blindness as 208/219 below — it is a projection of the
  graph's state as of that vintage, bounded by the derive/stitch cadence; anything created or deleted
  in AWS after that vintage is not reflected until the next derive.
- **Claim:** `held` (this cell did not re-run the tool AT that specific 2026-09-09 vintage — the graph
  has since been re-derived; see the re-measurement below, which is a later vintage of the same
  instrument).

### ⛔ The PRD's own "corroborated across two substrates" framing for this figure is ALREADY WITHDRAWN

The PRD's section-7 correction box (measured at `:312-317`, authored by `1.0.0_SA_CTO~Z`, the same
author who wrote the withdrawn paragraph) states directly: *"Member identity was established by
classing each member against the same instrument's output at two vintages. That shows the classifier
was CONSISTENT, never that it was CORRECT... The two 'substrates' shared the classifier under test."*
This cell does not re-litigate that withdrawal — it is already recorded, and it is the reason `IAM-r-3`
(not this cell) exists to re-check membership against a plane that did not build the set.

---

## Figure 219 — this cell's own re-measurement, its own instrument and its own vintage (AC4)

`comp-find '.' --corpus aws IAM_ROLE --limit 3`, run by this cell, 2026-09-10:
```
VINTAGE: Built from the estate as of 2026-09-10 12:24:50 UTC. Stitch source: stitch-codebuild built 2026-09-10T03:01:17Z.  manifest: aebbd9cef8c4
DENOMINATOR: 219 hit(s) across 219 aws node(s) scanned [corpus=aws types=IAM_ROLE]
DRIFT (scanned): DECLARED=203 LIVE-no-DECLARED=16
```
- **Instrument:** `comp-find --corpus aws`, live-AWS-plane projection of the `kuzu_nessie_db` graph
  (the same substrate `comp-iam live` names explicitly).
- **Vintage:** `2026-09-10 12:24:50 UTC`, manifest `aebbd9cef8c4` (this cell's own read; note this
  differs by manifest and by ~3 minutes from the decomposition's own prior `comp-find` reading —
  `12:21:58 UTC`, manifest `d70b0a16ae79` — while returning the identical `219 / DECLARED=203 /
  LIVE-no-DECLARED=16`, i.e. the graph was stable across that short re-derive-adjacent window).
- **Population:** 219 live `IAM_ROLE` graph nodes; `DECLARED=203`, `LIVE-no-DECLARED=16`.
- **What it cannot see:** same bound as 216 above — a projection bounded by derive/stitch cadence, not
  a synchronous live-AWS call at read time.
- **Claim:** `measured` (this cell's own run, matches the decomposition's own prior run and matches
  `comp-iam live`'s independent read of the same substrate to the digit).

---

## Reconciliation

**208 / 216 / 219 ARE reconcilable, by evidence, not by preference.** They are readings of ONE
instrument family — `comp-iam live` and `comp-find --corpus aws` both name `kuzu_nessie_db` as their
provenance, and this cell's own side-by-side run today returned byte-identical population, `DECLARED`
and `LIVE-no-DECLARED` figures from both entry points. Across the three vintages (`2026-09-03` →
`2026-09-09` → `2026-09-10`, this cell's own measurement) the total population grew (208 → 216 → 219)
entirely inside the `DECLARED` bucket (192 → 200 → 203, deltas of +8 and +3), while
`LIVE-no-DECLARED` held at exactly 16 across all three reads. That is a **vintage** difference on a
live, growing population — not three different scopes — and the undeclared-role finding this project
exists to act on is unaffected by which of the three vintages a reader cites.

**191 is NOT shown reconcilable to 208/216/219 by a vintage adjustment**, and this cell does not invent
one. It is a structurally different population: Terraform-declared role *blocks* rather than live role
*ARNs*, with `for_each`/`count` fleets collapsed to one count each (`comp-iam live`'s own NOTE, quoted
above, names this directly as the reason its DECLARED-plane numbers and the TF-parse plane's numbers
would not match one-for-one). This cell can name the mechanism that would produce a gap between 191 and
the live-plane's `DECLARED` sub-counts (192/200/203); it has **not** run the per-member work that would
turn that mechanism into an exact accounting, and doing that member-by-member read is `IAM-r-3`'s
mandate, not this cell's. **That absence of a settled reconciling arithmetic is itself the honest
answer for this pair, stated with the evidence above rather than left as a shrug.**

**195 is set aside rather than reconciled to anything** — it did not reproduce under this cell's own
re-run of the exact same instrument against an unchanged committed tree (see Figure 191 above), so
there is nothing to reconcile it against until its origin is established.

---

## Value-carries-its-claim summary

| figure | instrument | vintage | claim (this deliverable) |
|---|---|---|---|
| 191 | `comp-iam` TF-only parse (stats/roles/gaps) | this cell, 2026-09-10, HEAD `cccb4fac83` | `measured` |
| 195 | `comp-iam` TF-only parse (claimed, decomposition + `Z-S1`) | claimed `~2026-09-10T05:39Z` or decomposition's own battery run | `held`, and this cell's reproduction attempt **failed** |
| 208 | `comp-iam live` (`kuzu_nessie_db`) | `2026-09-03T02:00:31Z` (brief F2) | `held` (superseded snapshot, not re-run at that vintage) |
| 216 | `comp-find --corpus aws IAM_ROLE` (`kuzu_nessie_db`) | `2026-09-09T14:59:48Z` (brief F2a) | `held` (superseded snapshot, not re-run at that vintage) |
| 219 | `comp-iam live` AND `comp-find --corpus aws IAM_ROLE` (`kuzu_nessie_db`) | this cell, 2026-09-10 12:2x UTC | `measured`, independently from two entry points, identical result |
| 16 (undeclared) | all three live-plane vintages (208/216/219) | 2026-09-03, 2026-09-09, 2026-09-10 | `measured` at every vintage this cell checked or re-derived; stable throughout |

**Bottom line for a reviewer stating our posture (FWD-1):** the live-plane population is a moving
target and should be cited with its own vintage every time (as of this cell, 219, `DECLARED=203`,
`LIVE-no-DECLARED=16`, vintage `2026-09-10 12:24:50 UTC`) rather than any one historical figure; the
TF-only parse plane (191, `measured` by this cell) counts a different thing (declared blocks, not live
ARNs) and is not a substitute for the live count; and `195` should not be cited further until someone
reproduces it, which this cell could not do.
