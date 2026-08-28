# TO ETFS_SATELLITES.TO-1 — WEIGHTS from `rebalancer_model_detail`, name→book resolution, and the vintage policy

**Project:** `ETFS_SATELLITES` · **Directive:** D4 (SITEZ) · **Round:** 1
**Issued by:** `1.0.0_SA_CTO~Z` · 2026-08-27 ~17:4xZ
**Issued to:** DS-class. ⛔ **SEAT NOT ASSIGNED** — lane letter is `0.0.0_AB_MSTR~Z`'s to assign.

<issued_to>0.4.0_DS_ClientPlatform~W</issued_to>
> ⛔ **SEATED 2026-08-27 ~18:0xZ by the COO office.** The lane was assigned by MSTR (msg 9354)
> and lived ONLY in that message until now: `to-check.py` rendered this TO **`(unassigned)`**
> or resolved a serial out of prose, while the seat was LIVE AND BUILDING against it.
> ⚠ **A SEATING THAT EXISTS ONLY IN A MESSAGE IS NOT A SEATING** — the record is what every
> instrument reads, and an unresolvable assignee reads as unowned work no matter who is at the
> keyboard. Same class as this round's other three (a re-scoped serial, a class with no
> instance, 11 stale disarm_owner rows).

**Status:** ACTIVE · **Cells:** `SAT-a-1` `SAT-a-2` `SAT-a-3`

---

## 0. RULED BY SOVEREIGN WORD — no cell here re-asks any of it

- **WEIGHTS SOURCE** — *"we should be able to get these weights directly from the Rebalancing
  pipelines via the weights that they literally display there."* Weights are **MEASURED**, never
  hand-frozen, and **not gated on a human confirm**.
- **NAME MAPPING** — *"Opal Conservative Growth is the same as the 'LT Model'."*
- **FIGURE PROVENANCE** — the Teams-thread images bind **STRUCTURE ONLY**. ⛔ **`SAT-inv-1` was
  WIDENED: measured-never-transcribed binds MEMBERS as well as FIGURES** — a wrong member is
  arguably worse than a wrong figure, because a figure is checkable against the data and a member
  changes what the data is queried FOR.

## 1. `SAT-a-1` — weights read from the artifact, and a MUTANT proves the read is real

Source: `s3://opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_model_detail/{date}/{model_id}.json`,
field `hierarchy.children[].relativeAllocation`.

**ORACLE — and the mutant is the load-bearing half:** a satellite's weights reproduce from the
artifact ALONE, with the file's own bytes as the exhibit, **AND** altering one `relativeAllocation`
in a scratch copy **changes the rendered weight**. ⛔ **If the mutant does not move the render, the
read is decorative** — the page is showing something else and passing.

## 2. `SAT-a-2` — name→book resolution is DECLARED, and CVO's F3 names the fixture

Detail files carry **DISPLAY** names; the portal alias map resolves them. One addition is ruled:
`"Opal Conservative Growth"` → **LT**.

⛔ **CVO F3 (P1) — THE JOIN BREAKS ON EXACTLY ONE MEMBER, AND IT IS THE 81-ACCOUNT BOOK:**

```
Opal Satellite 60   name = "Opal Satellite 60"   displayName = "Opal - Satellite 60"   <- A DASH
the other eight     displayName == name exactly
displayName present on only 25 of 65 roster rows -> a NULL branch sits beside the mismatch branch
corroborating it is a roster property, not a typo:  "Opal UST/ Sat 70" -> "Opal UST/ Satellite 70"
```

**THE FAILURE MODE IS SILENCE:** the join returns empty, and empty reads as *"Satellite 60 has no
weights"* — **not** as *"the key did not match."*

**REQUIRED:** `SAT-a-2`'s oracle already prints the **UNRESOLVED count** (good design — keep it).
**What is missing is the FIXTURE: `Opal Satellite 60` is in it BY NAME**, exactly as `SAT-b-4` uses
the `98` pair for the membership path. **A silent drop is the defect, not a tidy result.**

## 3. `SAT-a-3` — the vintage question is a CELL, not a detail

The partition lands daily (~02:00Z measured). ⛔ **A stale-partition read must be DISTINGUISHABLE
FROM A FRESH ONE AT THE CONSUMER** — a marker or a refusal, **never silently older numbers**.

⛔ **NEVER#1 BINDS: any staleness verdict resolves the TRADING CALENDAR FIRST.** Count trading days;
`lib/trading_calendar.py` is the one frontier. **Friday IS Monday's answer** — a naive
wall-clock-age check false-alarms every Monday.

## 4. A DEPENDENCY THAT IS NOT YOURS — `SAT-a-4`

Delivery form (served block vs portal-fetched vs build-time constant) is **`2.0.0_SA_COO~Z`'s call**
by the decomp's own class assignment. ⚠ **It constrains you:** a build-time constant is legal ONLY
if `SAT-a-3`'s staleness behaviour survives it — **and by default it does not.** Do not pick the form
yourself; if it is unmade when you need it, **ask, do not assume**.

## 5. INVARIANTS — binding

`SAT-inv-1` measured-never-transcribed (MEMBERS **and** figures) · `SAT-inv-3` a value carries its
claim, **and the consuming half is the mechanism** — an unpopulated provenance field is the same as
none · `SAT-inv-4` other firms byte-identical (a REGRESSION assertion, exercised not assumed).

## 6. `<compiler_tools_mandate>`

- **Phase 1:** `comp-which` first (Rule 21). `comp-pipescript io` on any producer you touch.
- **Phase 2:** `.tools/commit-gate.sh`; the mutant exercised with before/after values printed.
- **Phase 3:** re-run and confirm the UNRESOLVED count is printed and is **0** with `Opal Satellite
  60` in the fixture (a positive control that the counter can be non-zero).

## 7. `<data_reprocess_scope>`

**`<no_reprocess_needed>`** — reads an existing bronze partition and derives weights; writes no
silver/bronze converter and changes no historical partition.

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md @936b9ae1e9 — cells `SAT-a-1` `SAT-a-2` `SAT-a-3`. ⚠ **VINTAGE `@936b9ae1e9`** — it carries the in-place `SAT-inv-2` amendment at :118. **A build against an earlier vintage reads the FALSIFIED invariant wording.**</decomp_ref>
<certification>**CERTIFIED WITH FINDINGS** — `3.0.0_SA_CVO~Z` @`205546c65c`, amended @`a025e2be91`; the membership-surface TO-mint block was **DISCHARGED** 17:15Z on a read of the amended normative line. ⛔ **What the signature does NOT buy:** it certifies the CELLS are well-formed, MECE over their declared surfaces, and carry oracles that can fail. **It says nothing about whether the build will be correct.**</certification>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued>2026-08-27T17:4xZ</issued>
<status>COMPLETE — DELIVERED **AND CERTIFIED**. Built by `0.4.0_DS_ClientPlatform~W` @`dc56a72c21`, proof instances @`7f44de8371`, **CERTIFIED by `3.0.0_SA_CVO~Z` 2026-08-27 ~18:3xZ** (`cvoZ_D1_D4_ROUND1_INSTANCE_CERTIFICATION_20260827.md` — *"BOTH SETS CERTIFIED. 24 criteria, 0 violations, every control fired"*; this TO rc=0 VALID, 0 violations). **Both commits verified ON ORIGIN by `2.0.0_SA_COO~Z` 2026-08-28 ~01:2xZ** — `merge-base --is-ancestor` vs `origin/SITEZ`, under a POSITIVE control (passes) and a **RE-RUN NEGATIVE control**: the first negative control FAILED because the integrator pushed mid-check and `origin/SITEZ` came to equal the commit chosen as unpushed, so `origin/CLOUD`'s tip was substituted and reads NOT-ON, proving the instrument can still say no. ⛔ **CLOSED BY THE ISSUING OFFICE: THIS FACE READ `ACTIVE — unblocked; waiting on a SEAT` FOR ~7 HOURS AFTER CERTIFICATION.** It is the FIFTH stale-carrier instance of the night and the second this office measured; the class has already manufactured one false re-dispatch. ⚠ **BOUND CARRIED FROM THE CERTIFICATE, NOT WIDENED: `3.0.0_SA_CVO~Z` certified the INSTANCES and their alignment — "No served-artifact claim ... ETFS_SATELLITES remains a portal-only build NOT YET SHIPPED." COMPLETE HERE MEANS THE TO IS DISCHARGED, NEVER THAT ANYTHING SERVES.** ⭐ `satellites_registry.py` is a CONFORMANCE ORACLE — **USE it, do NOT convert it.**</status>

<proof_of_spec>
  <!-- ISSUANCE half (1.0.0_SA_CTO~Z). POSITIONAL:
         python .tools/proof-of-spec-check.py <instance>.json SAT-TO1-AC1,SAT-TO1-AC2,SAT-TO1-AC3,SAT-TO1-AC4
       CHECK THE RC, NEVER THE OUTPUT STRING; WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL. -->
  <criterion id="SAT-TO1-AC1" cell_refs="SAT-a-1"/>
  <criterion id="SAT-TO1-AC2" cell_refs="SAT-a-2"/>
  <criterion id="SAT-TO1-AC3" cell_refs="SAT-a-2"/>
  <criterion id="SAT-TO1-AC4" cell_refs="SAT-a-3"/>
  <expected_criteria>SAT-TO1-AC1,SAT-TO1-AC2,SAT-TO1-AC3,SAT-TO1-AC4</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_SATELLITES.TO-1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`SAT-TO1-AC1`** | Weights reproduce from `rebalancer_model_detail` ALONE, file bytes as the exhibit. ⛔ **PLUS THE MUTANT:** one altered `relativeAllocation` in a scratch copy **changes the rendered weight**. If it does not move, the read is decorative and this FAILS | `SAT-a-1` | **EXERCISED + mutant** |
| **`SAT-TO1-AC2`** | Every constituent name across the satellite set resolves to a book, **with the UNRESOLVED count PRINTED**. A silent drop is the defect, not a tidy result | `SAT-a-2` | **EXERCISED, denominator printed** |
| **`SAT-TO1-AC3`** | ⛔ **CVO F3 — `Opal Satellite 60` IS IN THE FIXTURE BY NAME.** Its `displayName` carries a dash (`"Opal - Satellite 60"`) while the other 8 match exactly, and it is the **81-account** book. Show the join resolves it, and show the counter CAN be non-zero (positive control) | `SAT-a-2` | **EXERCISED (fixture)** |
| **`SAT-TO1-AC4`** | A controlled STALE partition produces a **visibly different state** (marker/refusal), not silently older numbers. ⛔ **Resolve the TRADING CALENDAR first** (NEVER#1) — count trading days via `lib/trading_calendar.py`; a wall-clock check false-alarms every Monday | `SAT-a-3` | **EXERCISED, two arms** |

-- `1.0.0_SA_CTO~Z`, issuer
