# T4 DECLARATIONS -- fork-or-drift, one per two-homes census row

**TO:** D0_TIGHTENING.TO-5 (supersedes the acceptance of NFRA_DEPLOYCENSUS.T4-DECLARATIONS -- see
"Two TOs, one body of work" below)
**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-08-19
**Census re-read against:** `lambda_census_v3_findings.json`, `ec2_census_v2_rows.json`,
`ec2_onbox_verdicts.json` (the census's MACHINE EVIDENCE, not its prose summary)
**Owner resolution:** `.tools/owned-paths-validate.py` `resolve_lane()` against `.owned-paths.yaml`,
run with a **positive control** (`org/mcp/broker.py -> BASE_EXEC`, the lane that refused my own
commit earlier tonight) and a **negative control** (`zzz/no/such/path.xyz -> None`). My first three
attempts returned `None` for every path including the control -- I was passing the whole config
instead of `config['paths']`. The control is the only reason that did not become 19 rows of
"UNRESOLVED".

---

## T4-1 -- THE DENOMINATOR, AND IT IS NOT THE PRIOR

**The brief's "16+3" is a PRIOR I was chartered to re-read. My read differs. Per CVO P0-1 and the
TO's own instruction, that difference is a RESULT, not a discrepancy to reconcile away.**

### How I enumerated

Lambda: every row in `lambda_census_v3_findings.json` whose `class` contains `TWO-HOMES`, counted
as DISTINCT lambdas (no lambda appears on more than one axis -- verified, 19 rows / 19 distinct).
EC2: every service in `ec2_census_v2_rows.json` / `ec2_onbox_verdicts.json` exhibiting a two-homes
SHAPE, enumerated by hand because -- see below -- the EC2 evidence has no two-homes class at all.

### The Lambda axis: FOUR different numbers exist in the census's own artifacts

| source | value |
|---|---|
| `lambda_census_v3_summary.json` -> `summary_per_lambda["TWO-HOMES-DIVERGED"]` | **15** |
| `CENSUS_REPORT_20260818.md` prose, and BOTH task orders' prior | **16** |
| `summary_per_lambda` -> `findings_per_axis_class` sum (`bundled-vs-canonical` 17 + `own-tree` 2) | **19** |
| **actual finding rows in `lambda_census_v3_findings.json`** | **19** |
| **actual DISTINCT lambdas in those rows** | **19** |

**My denominator for the Lambda axis is 19.** It is the only number that is a direct count of the
evidence rather than a summary of it, and the axis-class breakdown in the same summary file agrees
with it (17+2=19) while that file's own per-lambda roll-up does not. The summary and the prose are
both internally inconsistent with the findings they summarise.

### The EC2 axis: the class does not exist

`ec2_census_v2_rows.json` `staged_class` has exactly four values across 27 services:
`UNREAD 14 · STALE-BY-NEGLECT 6 · CURRENT 5 · STAGED-ORPHAN-ONLY 2` (=27).
**There is no `TWO-HOMES` value in the EC2 vocabulary at all**, so a scan keyed on that string
returns a clean, confident **0** -- the wrong question asked cleanly. The report prose asserts
`CURRENT 6 · STALE-BY-NEGLECT 6 · TWO-HOMES (incl. orphan-bearing) 3 · UNREAD 12`, which matches
neither the values nor the counts in the evidence file.

Enumerated by SHAPE instead, across both EC2 axes:

| # | service | shape | evidence |
|---|---|---|---|
| E1 | `mdpf-daily-runner` | on-box AHEAD of staged | 44 on-box files hashed, 41 equal to staged, **3 differ** (`gold/build_portal_gold_accrual.py`, `gold/partner_roster.json`, +1) |
| E2 | `opal-gateway` | staged objects with no repo home | `staged_counts {STAGED-ORPHAN: 2}` (2 of 2) |
| E3 | `bd-49f-auto-login` | staged object with no repo home | `staged_counts {CURRENT: 3, STAGED-ORPHAN: 1}` |
| E4 | `canonical-schwab-si2` | on-box files with no repo home | every hashed file `repo_exists: false` |

**E4 is declared a BOUNDARY CASE, not silently included or excluded.** E2/E3/E4 are
*orphan*-shaped (one home MISSING) rather than *two-homes-diverged*-shaped (two homes DISAGREEING);
only E1 is unambiguously the latter. I report **EC2 = 3** to match the shape the brief named
("incl. orphan-bearing"), and name E4 as the fourth candidate so the boundary is visible rather
than absorbed into a count.

### DENOMINATOR AS READ

```
LAMBDA  19   (distinct lambdas, findings evidence)
EC2      3   (+1 declared boundary case, E4)
------------
TOTAL   22   (23 counting the boundary case)

PRIOR:  16 + 3 = 19
DELTA:  +3 Lambda rows that the prior would have left UNDECLARED
```

**This is exactly the failure CVO P0-1 named** -- an acceptance pre-committed to "16+3" would have
passed at 16+3 while three real rows sat undeclared. It passes here only because the acceptance was
made denominator-relative first.

---

## T4-2 / T4-3 -- THE DECLARATIONS (22 rows, each with a why or a named owner)

**Owner rule applied:** lane from `resolve_lane()`; where the lane is `ANY` (not an ownership
answer) the owner falls to CLAUDE.md Rule 13 for `data/*/scripts/{gold,silver,bronze}` (DS owns the
commit->QA-deploy cycle), and to COO as ROUTING owner where no rule claims the path.

### Lambda axis (19)

| # | census row | subkind | canonical home | DECLARATION | owner |
|---|---|---|---|---|---|
| L1 | `news-ingestion-scheduler` | bundled-copy diverged | `tools/news_scanner/scripts/utilities/text_cleaner.py` | **DRIFT** | `2.0.0_SA_COO` (routing -- lane ANY claims no owner) |
| L2 | `news-trending-analysis` | bundled-copy diverged (2 members, `stopwords.py` sim 0.554) | `tools/news_scanner/scripts/utilities/` | **DRIFT** | `2.0.0_SA_COO` (routing) |
| L3 | `opal-partners-data` | bundled-copy diverged vs **bd AND cot** | `data/black_diamond/.../etf_classifier.py` + `data/cot/.../etf_classifier.py` | **FORK-DELIBERATE** -- see the note below; this row must NOT be consolidated | `0.4.0_DS_ClientPlatform` (awareness only) |
| L4 | `opal-trending-image-generator` | own-tree: deployed bytes live at ANOTHER repo path (map `source_dir` is not the built-from dir) | n/a | **DRIFT** (source-map defect, not code drift) | `0.7.0_AE_CloudOps` |
| L5 | `opal-smartx-ingestion-pipeline` | bundled-copy diverged (sim 0.213 -- the widest divergence in the set) | `data/smartx/scripts/` | **DRIFT** | `0.5.0_AE_OpalETL` |
| L6 | `exec-summary-generator` | bundled-copy diverged (sim 0.995) | `data/black_diamond/scripts/exec_summary/template_library.py` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L7 | `inf-api-txn` | bundled-copy diverged (sim 0.453) | `data/inf/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L8 | `inf-silver-chain` | bundled-copy diverged (sim 0.865) | `data/inf/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L9 | `inf-api-assets-v2` | bundled-copy diverged (sim 0.848) | `data/inf/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L10 | `inf-api-reps` | bundled-copy diverged (sim 0.676) | `data/inf/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L11 | `inf-api-positions` | bundled-copy diverged (sim 0.675) | `data/inf/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L12 | `inf-accounts-v2-daily` | bundled-copy diverged (sim 0.865) | `data/inf/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L13 | `opal-globgrph-incremental-updater` | own-tree: `_provenance.py` NO-HEAD-SOURCE (deployed carries a member the repo lacks at HEAD) | n/a | **DRIFT** (deployed-only member) | `0.7.0_AE_CloudOps` |
| L14 | `opal-inf-value-parity` | bundled-copy diverged, **cosmetic_only=True** (sim 0.886) | `data/inf/scripts/silver/_orion_vendor_asof.py` | **DRIFT** (cosmetic -- lowest priority) | `0.4.0_DS_ClientPlatform` |
| L15 | `opal-assets-silver-schwab` | bundled-copy diverged, **cosmetic_only=True** (sim 0.966) | `data/assets/scripts/silver/silver_registry.py` | **DRIFT** (cosmetic) | `0.4.0_DS_ClientPlatform` |
| L16 | `opal-assets-silver-orion` | bundled-copy diverged (2 members) | `data/assets/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L17 | `opal-assets-silver-eclipse` | bundled-copy diverged (2 members) | `data/assets/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L18 | `opal-assets-silver-blackdiamond` | bundled-copy diverged (2 members) | `data/assets/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |
| L19 | `opal-assets-silver-etf` | bundled-copy diverged (2 members) | `data/assets/scripts/silver/` | **DRIFT** | `0.4.0_DS_ClientPlatform` |

### EC2 axis (3, +1 boundary)

| # | service | DECLARATION | owner |
|---|---|---|---|
| E1 | `mdpf-daily-runner` | **DRIFT** -- on-box ahead of staged on 3 of 44 files; the executing plane and the staging plane genuinely disagree | `0.7.0_AE_CloudOps` |
| E2 | `opal-gateway` | **DRIFT** -- 2 of 2 staged objects have no repo home | `0.7.0_AE_CloudOps` |
| E3 | `bd-49f-auto-login` | **DRIFT** -- 1 of 4 staged objects has no repo home | `0.7.0_AE_CloudOps` |
| E4 | `canonical-schwab-si2` | **BOUNDARY CASE, DECLARED-UNCONFIRMED** -- every on-box file has `repo_exists: false`. Whether a Windows box with no repo home is a two-homes row or a not-in-repo row is a classification call I do not own | `0.7.0_AE_CloudOps` + `2.0.0_SA_COO` to rule |

### THE ONE FORK-DELIBERATE, AND WHY IT MATTERS MOST

**L3 `opal-partners-data` is the only FORK-DELIBERATE in the set, and declaring it DRIFT would have
been actively dangerous.** Its two canonical homes are `data/black_diamond/scripts/gold/lib/` and
`data/cot/scripts/gold/lib/` -- and CLAUDE.md's NEVER rules make bd<->cot separation **law**: *"cot
is a COMPLETELY separate firm pipeline from bd -- never mirror/sync"*, enforced at commit gate AND
IAM Deny at runtime. A blind subkind-driven DRIFT declaration would have routed a consolidation
that the estate forbids at two independent layers. **The intent that makes two homes correct is
firm separation itself.** No consolidation owner is named because no consolidation may occur.

*(This is why the declarations are made per row from the evidence rather than per subkind: 18 of 19
rows share the subkind `BUNDLED-COPY-DIVERGED-FROM-CANONICAL`, and the 19th shares it too while
meaning the opposite.)*

### Why the other 18 are DRIFT and not FORK-DELIBERATE

Bundling a library copy into a Lambda package is a deliberate PACKAGING act. The copy having
DIFFERENT CONTENT from its canonical home is not -- no source, comment, or ruling states an intent
for the bundled copy to differ, and `deployed==canonical:False` together with
`source_dir-copy==canonical:False` means the divergence is present in the repo's own copy as well
as the deployed bytes. FORK-DELIBERATE requires a stated intent that makes two homes correct; for
these rows there is none. Two are flagged `cosmetic_only=True` (L14, L15) -- still drift, lowest
priority.

---

## T4-4 -- HANDOFF

- Declaration table lands **where the census lives**: this file, beside
  `CENSUS_REPORT_20260818.md` in `NFRA_DEPLOYCENSUS/`.
- Consolidation owners receive their rows **by real send** (per-owner MCP, one send per owner --
  no in-body cc, which copies nobody; LD-0424).
- **Standing check, stated not run:** a census re-run after any future consolidation must show the
  two-homes count fall by **exactly** the consolidated set. A fall by more is a masking event, not
  progress.
- **No consolidations, deletes, or deploys were performed.** Declarations only.

---

## Two TOs, one body of work -- surfaced, not adjudicated

This work is dispatched **twice**, with **conflicting** acceptance:

| | `NFRA_DEPLOYCENSUS.T4-DECLARATIONS` | `D0_TIGHTENING.TO-5` |
|---|---|---|
| issued | 2026-08-19 **14:50Z** | 2026-08-19 **19:45Z** |
| census instruction | *"is the universe -- **do not re-derive it**"* (16+3) | *"a PRIOR you are chartered to **re-read**"*, denominator-relative |
| criteria | T4-1..**T4-5** | T4-1..**T4-4** |
| instance path | `NFRA_DEPLOYCENSUS.T4-DECLARATIONS_PROOF_OF_SPEC.json` | `D0_TIGHTENING.TO-5_PROOF_OF_SPEC.json` |

**Latest + most-restrictive binds -> TO-5's re-read instruction governs**, and the re-read is what
found the +3. I executed to TO-5 and am surfacing the collision rather than adjudicating which TO
survives -- that is COO's call. Both instance paths are satisfied by this one table; the TO-5
instance is authored, and the T4-DECLARATIONS instance can be pointed at it or retired on COO's word.


---

## RULINGS RECEIVED -- the routed rows, recorded ROUTED-WITH-CAUSE

**2.0.0_SA_COO, 2026-08-19T22:38Z.** Recorded as ROUTED-WITH-CAUSE at COO's explicit request:
*"the cause is the more useful half."*

### L1 + L2 -- DRIFT CONFIRMED, and the cause sits UPSTREAM of the drift

My declaration named COO as routing owner because lane `ANY` claims no owner. COO went looking for
*why* and found the finding under the finding:

> **THE CODE ITSELF IS UNOWNED.** `tools/news_scanner`'s last 12 commits span **SIX authors**
> (Andrew, a CRO sweep lane, TWO different COO serials incl. the retired 2.1.0, CTO, DT), and
> `ASTN_WSJFT` -- the consumer project -- carries **NO DECLARED OWNER** in its registry entry.

So these rows had no claimant **because there is nobody to claim them**, not because the routing
rule was ambiguous. COO's reasoning, worth preserving verbatim in substance: *assigning a drift-fix
owner without an owning project just RELOCATES THE ORPHAN* -- the bundled copies would diverge again
under the next six-author month and the next census would route the same rows back.

| row | declaration | REMEDIATION owner | CAUSE |
|---|---|---|---|
| L1 `news-ingestion-scheduler` | **DRIFT** (confirmed) | `0.7.0_AE_CloudOps` -- owns the lambda deploy plane and the bundling that produced the divergence; a **mechanism assignment, not a guess** | canonical home `tools/news_scanner` is unowned (12 commits / 6 authors); consumer project `ASTN_WSJFT` has no declared owner |
| L2 `news-trending-analysis` | **DRIFT** (confirmed) | `0.7.0_AE_CloudOps` (same mechanism) | same |

**The project-ownership gap on `ASTN_WSJFT` is carried as a COO item, deliberately NOT folded into a
DRIFT row** -- *"a registry entry with no owner is the condition that generates rows like these."*

### E4 -- RULED **NOT-IN-REPO**, and therefore NOT a member of this census's universe

`canonical-schwab-si2` is **removed from the two-homes universe** by ruling. COO's taxonomy:

> **TWO-HOMES REQUIRES TWO HOMES.** A box whose files have no repo home at all is not a divergence
> between copies -- it is code running with **NO REPO PROVENANCE**, a different and arguably worse
> class. Two-homes at least gives you something to diff; this gives you nothing to diff against.

Classifying it as two-homes would have hidden it inside a category **whose remedy (reconcile the
copies) is not even applicable**, leaving the census carrying a row whose fix could never be
performed. It keeps its own class and its own remedy question -- *"should this box's code have a
repo home at all"* -- which is a real question, not a cleanup. `0.7.0_AE_CloudOps` holds the other
half of the joint call; if their on-box measurement differs, **theirs is the measurement and COO's
is only the taxonomy.**

**Effect on T4-1's denominator: NONE.** E4 was declared a boundary case and held OUT of the 22 from
the start; the ruling confirms that exclusion rather than changing it. **The denominator stands at
22** (19 Lambda + 3 EC2), with E4 now positively classified rather than left open.

### Owner tally after rulings

`0.4.0_DS_ClientPlatform` 13 - `0.7.0_AE_CloudOps` 8 (6 + L1/L2 by remediation ruling) -
`0.5.0_AE_OpalETL` 1 - **zero rows remain routed to COO as a placeholder owner.**
