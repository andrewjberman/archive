# E3.0 Wave-1 safe-slice retirements -- ZERO EXECUTED, gates exercised

**Agent:** `0.7.0_AE_CloudOps~A` | **Date:** 2026-07-30 | **Dispatch:** COO 20260730T053312Z + 060255Z
**Verdict:** **0 retirements. 6 of 6 eligible candidates -> KEEP-DORMANT (fail-safe default).**
**This is the acceptance criterion met, not a failure** -- the PRD's bar is "the gates exercised,
denominator printed," and the gates were exercised and returned KEEP. A missed corpse is recoverable;
a decommissioned belt is the named failure mode.

## Provenance

```
comp-legacywriter --census --require-live-substrate  run 2026-07-30T061355Z  spec @3af3e04c53
  SOURCE repo-HEAD          : 631e71f4b9 @ 2026-07-30T02:07:06-04:00
  SOURCE static-axis-engine : comp_dataflow.py @ 2026-07-23T190557Z
  --self-test               : 10 of 10 controls PASS (scored on OUTPUT, not rc)
  ENRICHMENT AXES (all four supplied -- see COVERAGE note):
    comp-heat   2026-07-30T060846Z (25157 paths)
    comp-dups   2026-07-30T061206Z (--allow-held; see F3)
    comp-debris 2026-07-30T060947Z (190 resources)
```
The FIRST census run had all three enrichment axes `not supplied`, which lumped 343 surfaces at
"score 3". Supplying them RESOLVED the distribution (235 at 5 / 108 at 3 / 51 at 2 / 43 at 0).
**A score is only as good as its denominator; the 3-axis-blind run was not a weaker version of
this one, it was a different measurement.**

## The narrowing, with a denominator at every step

| Step | Count | Basis |
|---|---|---|
| Written surfaces (census) | **437** of 643 locations; 8915 files scanned | 4-axis census |
| E3.0 name population (`archive/` \| `diagnostics/` \| `test_*`) | **56** of 437 | key regex |
| Structural exclusions | **21** of 56 OUT | below |
| Survivors -> key-grain existence check | **35** | -- |
| **HOLD AN OBJECT -> OUT by definition** | **29** of 35 | live LISTING |
| **Hold NO OBJECT -> eligible** | **6** of 35 | live LISTING |
| **Retired** | **0** of 6 | evidence bar not met |

Structural exclusions (reasons overlap, so they sum above 21): 19 `KEY-TEMPLATED` (a `{*}` key has no
concrete key to check -- a glob listing nothing says nothing about the concrete keys emitted),
3 `BUCKET-UNRESOLVED` (you cannot list a bucket you cannot name, so absence is unverifiable **by
construction** -- comp-legacywriter's own C7/C8 controls call this UNDETERMINABLE, never absence),
2 `HAS-READER`, 2 `SILENT-DEFAULT-READER` (raises retire-risk while lowering nothing).

Key-grain existence used **ListObjectsV2 (key+size)**, never HeadObject -- HeadObject is
`s3:GetObject` and is not the acceptance instrument (OPAL_ASSETS law). Listing denominator: **507
objects** under `s3://opal-data-bd/diagnostics/`. Positive control: a known-present key
(`diagnostics/09_dryrun_output.txt`, 5190 B) resolves in the same listing.

## BOTH counts, as the PRD acceptance requires

- **census-only:** 56 name-matched surfaces
- **derived-from-contracts:** **0** -- no contract registry covers this population. The PRD states it
  outright: *"the 353 were derived from SOURCE; none is contracted yet."* WS-C1's grammar is GATED and
  I am barred from declaring contracts as a side effect of E3.0.
- **COVERAGE DEBT: 56 of 56** -- the entire population is uncontracted-lifecycle.

## Why all 6 are KEEP-DORMANT

The 6: `acat_correlation_summary.txt` · `adhc_histry_005_schwab_crossref.json` ·
`aua_correction_matrix_2026-03-02.json` · `rps_matching_latest.json` ·
`rps_timeseries_holdings.parquet` · `schwab_bd_account_match.json` (all `opal-data-bd/diagnostics/`).

1. **Both available signals are Tier-C.** Every one carries exactly `NO-READER-IN-POPULATION` +
   `ALL-PRODUCER-CODE-COLD`. COO, binding: *"Tier-C mechanical signals ... are NEVER sufficient: they
   ARE the debt signals, and a deliberate belt and a corpse are identical on every one of them."*
   Two Tier-C signals do not make a Tier-A case. These are March-2026 ad-hoc forensics scripts --
   a script retained to re-run during a recurrence is a textbook deliberate belt.
2. **The invocation axis is BLIND on all 6** -- `band=UNAVAILABLE`, `signal_basis=None`,
   `axes_blind=['invocation(resource-not-in-ledger)']` (`opal-data-bd` is absent from comp-debris'
   190-resource ledger). The one axis that could evidence liveness is the one we do not have.
3. **No `keep-dormant.yaml` entry either way.** The registry holds MDPF custody-flip belts; nothing
   for bd/diagnostics. Absence from it is the uncontracted complement, **not** a clearance.
4. **The TRANSIENT guard's pass is uninformative** -- see F2.
5. **Shared-producer constraint (LD-0330):** `adhc_histry_006_rps_matching.py` writes BOTH
   `rps_matching_latest.json` and `rps_timeseries_holdings.parquet`. The unit of retirement is the
   WRITE; removing either must not remove the producer that performs the other.

`_schwab_bd_account_match.py` has **no importers** (only self-references; a manual EC2-run script) --
so retiring it would not break an import, but that is the only limb it clears.

## FINDINGS

### F1 -- `retire_risk=LOW` and `score=5` read IDENTICALLY for keys that HOLD OBJECTS
29 of the 35 name-matched survivors **hold live objects** while presenting `contest=SOLE`,
`deadness_score=5`, `retire_risk=LOW`, `NO-READER-IN-POPULATION`, `ALL-PRODUCER-CODE-COLD` --
every mechanical signal green. Largest: `adhc_histry_004_realized_crossref.json` at **436,489 B**;
also `adhc_histry_002_fifo_walkthrough.json` at 81,516 B.
**The tool does not lie about this** -- it states plainly that its invocation axis is BUCKET-grain and
that key-grain liveness needs `comp-clobber --live` or a head-object, neither of which it runs. The
defect is an AFFORDANCE one: the field is *named* `retire_risk` and *reads* `LOW`, which is a
retire-authorizing phrase on a surface whose existence the tool never checked. **The label invites
precisely the inference the docstring forbids.** An agent retiring off the score alone deletes
writers for keys holding real forensic data. Recommend: `retire_risk` be forced to
`UNKNOWN-KEY-EXISTENCE-UNCHECKED` unless a key-grain listing was supplied.

### F2 -- the TRANSIENT stopgap guard clears by NON-MATCH, not by examination
`comp_legacywriter.py:704` is a 9-entry substring list:
`("trigger-pending","trigger-mode","pipeline-complete","trigger_pending","_probe","boundary_probe","last-probe",".lock","/state.json")`.
All 6 candidates "passed" it by not matching a name -- which is not the same as being examined and
cleared. `rps_matching_latest.json` is a `*_latest` snapshot-pointer shape and `"latest"` is not on
the list.
**I then refuted my own transient hypothesis ON SOURCE:** that writer does `put_object` only, with no
`delete_object` (`adhc_histry_006_rps_matching.py:570,679`), so the key is an overwrite-snapshot, NOT
a written->consumed->deleted marker. **The point stands and is sharper for it: the guard could not
have told me that -- I had to read the source. It returns the same silence for a key that IS a
transient marker under a name nobody listed.** The list is honest about its provenance (the comment
records the 2026-07-29 near-miss that produced it) but it is a denylist of three known incidents,
and the PRD leans on it as *the* stopgap until WS-C1 lands.

### F3 -- a LIFTED sovereign hold is still enforced in code, 16 days on
`org/modules/graph/debtscan/dup_scan.py:358` `_HELD_PREFIXES = ("data/black_diamond/",
"data/canonical/schwab/silver/")` excludes 354 paths from every `comp-dups` corpus, commented *"for
when Andrew lifts."* **Andrew lifted the 49F/bd/Schwab block COMPLETELY on 2026-07-14.** Every
comp-dups run since has had a silently-short corpus on that axis (it announces the exclusion loudly,
so this is visible-but-unheeded, not hidden). I used `--allow-held` for this census and did **not**
flip the guard -- changing a sovereign-hold constant is arch-gated, and the grantee does not remove
its own guard. **Routes to CTO~C.**

## What was NOT done, deliberately

No retirement executed. No contract declared. WS-E1/WS-E2 untouched. Nothing
notification-shaped built. No `keep-dormant.yaml` entry added (adding one is an *intent assertion*
requiring the owner's word, and per RULING 1 every entry needs a grounded reason + rearm_condition +
annotation_cite + revalidate_by -- I have none of those for a March forensics script).

## Recommendation

**Wave 1 closes at 0 retirements.** To make a future wave productive, the blocking input is not more
census work -- it is one of: (a) `opal-data-bd` added to the comp-debris resource ledger, which
un-blinds the invocation axis for this whole population; or (b) WS-C1 contracts landing so a
lifecycle value exists; or (c) an explicit owner ruling that a March-2026 ad-hoc forensics script
with a vanished output is a corpse by intent -- which is a Tier-A judgement, and Tier-A is the one
tier mechanical signals provably cannot supply.
