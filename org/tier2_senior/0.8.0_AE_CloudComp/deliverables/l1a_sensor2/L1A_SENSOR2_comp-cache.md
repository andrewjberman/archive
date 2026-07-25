# NFRA_COMPLEARN L1a-SENSOR-2 — residue sensor for `comp-cache` (CODE-TEXT shape)

**author:** `0.8.0_AE_CloudComp~E` · 2026-07-25 · **status:** DELIVERED
**reports to:** `1.0.0_SA_CTO~Z` + `3.0.0_SA_CVO~Z` ONLY (off-main-fabric)
**dispatch:** `1.0.0_SA_CTO~Z`, 20260725T090823Z, "DISPATCH NFRA_COMPLEARN L1a-SENSOR-2"
**sensor code:** `sensor_cache_residue.py` (this directory) · **emitted report:**
`boundary_report_comp_cache.json` (this directory)
**spec compliance:** `IMPLEMENTATION_LEVELS_AND_SEQUENCING.md` §4/L1a, all five acceptance criteria — see §5.

---

## 1 · Tool choice + why (stated before building, per dispatch)

**`comp-cache`** (engine `org/modules/graph/cache_cli.py`; source domain `portal/src` `.ts`/`.tsx`).

- **Shape fits the assignment:** the source is CODE-TEXT — inside the dispatch's "yaml/config/code-text"
  class, and a *different* text sub-shape from `comp-residue`'s yaml-schema reference, adding the shape
  diversity the build order asks for (`address_space: code_call_site`, new, surfaced via BR008 by design).
- **The tool's own traversal is executable, not just derivable:** `cache_cli.extract()` is an importable
  function returning `(entries, unparseable, total)` — the sensor OBSERVES the tool walk its source by
  calling the tool's own code (`method: traversal`, exact), no reimplementation and no hand-declaration.
- **The tool has a real doc plane about its own boundary:** its denominator line and docstring name
  `useQueries` / `useInfiniteQuery` as adjacent-but-not-audited — so `doc_only` is *applicable and
  populated* for this shape, and the sensor **parses those names from the tool's own source text** rather
  than declaring them.
- **Known-good residue candidate existed before building** (grounding, not circularity): a pre-build census
  found `useAutoSaveQuery` — a custom key-bearing wrapper the tool neither walks nor names. The sensor was
  built blind to *where* those sites are; it independently located and cell-assigned them.

## 2 · Derivation map — everything from the tool's own code (never hand-declared)

| Sensor input | Derived from | Method label |
|---|---|---|
| walked set (covered) | executing `cache_cli.extract(portal_src=root)` — the tool's OWN traversal | `traversal` (exact) |
| member set | the tool's own `Unparseable` listings (sites it SAW on its axis and reported) | `traversal` (exact) |
| walked-hook identity | the tool's own `_USEQUERY` regex, imported; sensor **asserts** on its pattern and FAILS loudly if the matcher drifts | — |
| doc-named exclusions | parsed from the tool's own source text ("are NOT audited" contract line + "Adjacent hooks NOT in scope" docstring block); empty parse ⇒ printed as reportable drift, never a silent default | `mention` |
| accessor exclusion (`useQueryClient`) | the tool's own matcher comment ("useQuery, not useQueryClient / …"); excluded only while that comment exists in source | — (out of domain, counted + printed) |
| file-set rule | mirrors the tool's own `rglob("*.tsx") + rglob("*.ts")` so tool and sensor can disagree only on HOOK coverage, never FILE coverage | — |
| CLI surface | `manifest_check_cli._established_subcommands("comp-cache")` — **the registration gate's extraction, reused** → `{map, collisions, key}`, unpinned, "static add_parser extraction" | — |
| orphan key-bearing-ness | the candidate hook's own in-tree definition (body wraps `useQuery`/`queryKey`); no definition found ⇒ **UNKNOWN, reported, excluded from surface_total** | `mention` |
| head pin | `git -C portal rev-parse --short HEAD` at scan time (`portal@d1ba89b9`) | — |

## 3 · Main run — VERDICT, 4 residue sites of a 109-site surface *(corrected per verify, see below)*

```
SENSOR comp-cache residue -- source=portal/src head=portal@d1ba89b9
  DENOMINATOR: surface_total=109 = covered 105 (traversal) + member/unparseable 0 (traversal)
               + doc_only 1 (mention) + orphan 3 (mention)
  UNKNOWN (first-class, EXCLUDED from surface_total, never binned): 0 site(s)
  EXCLUDED by the tool's own declared design (accessor, no key at call site): 14 useQueryClient site(s)
  DEFINITION (labeled, NOT counted in any cell): usePortfolioApi.ts:128:useAutoSaveQuery
  TRUE_RC=2 (VERDICT)
```

- **doc_only (1):** `portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx:236:useQueries` —
  a key-bearing subscription the tool's own contract line names as not-audited. The boundary, working as
  the tool discloses it.
- **orphan (3 CALL SITES):** `useAutoSaveQuery` at `usePortfolioFileUpload.ts:17`,
  `PortfolioManagement.tsx:79`, `TradeTab.tsx:95` — a custom wrapper whose definition wraps `useQuery`
  with `portfolioKeys.*` keys. **Nothing downstream of comp-cache knows these subscriptions exist**: a
  cache-key collision involving an `useAutoSaveQuery` site is invisible to `comp-cache collisions` today,
  and the tool's honest denominator line does not name this hook (it cannot — it doesn't know about it).
  Route-C territory per the cells contract; materiality is the inference gate's call, not this sensor's.
- **definition (1, labeled, un-counted):** `usePortfolioApi.ts:128` — the wrapper's declaration, where
  the key is constructed. Reported as a top-level `definitions` row in the emitted JSON (legal extra
  field; cell accounting unaffected), never folded into a call-site count.
- Accounting balances over applicable cells (105+0+1+3=109); reconciliation guard between the tool's own
  count (105) and the sensor's independent enumeration of the same hook (105) agreed exactly this run —
  a nonzero delta prints as SENSOR-WARN, reported not smoothed.

**CORRECTION PROVENANCE (CTO~Z + CVO~Z verify, 20260725T0922Z):** the first emission counted orphan=4 —
the 4th "site" was the wrapper's *function declaration*, which `_QUERY_FAMILY`'s name-followed-by-`(`
lookahead cannot distinguish from an invocation. The fix reuses this sensor's own declaration pattern
(previously applied only in `hook_is_key_bearing`) inside `enumerate_sites()`; declarations now return
separately and render as labeled DEFINITION rows. The finding's validity was never in question — its
severity axis (how many places *use* the hook invisibly) is what the count feeds, per CVO~Z.

## 4 · Controls — all run as separate invocations

| Control | Input (real ws source, no synthetic fixtures) | Expected | Observed |
|---|---|---|---|
| **POSITIVE (can return CLEAN)** | `--source-root portal/src/components` — 10 useQuery sites, all captured | rc=0 CLEAN | **rc=0 CLEAN** ✓ |
| **NEGATIVE (REFUSE, never "everything is residue")** | `--source-root portal/src/types` — real dir, zero Query-family sites | rc=3 REFUSE | **rc=3 REFUSE** ✓ (exercised twice) |
| **Nonexistent-input mutation** (beyond spec; motivated by REC1C_E §4.4) | `--source-root portal/src/zzz-nonexistent-dir-9999` | rc=1 FAIL, distinct from REFUSE | **rc=1 FAIL** ✓ |
| **Declaration-only mutant** (CTO~Z-ordered at verify) | `fixtures/mutant_decl_only/` — a `function useZzzMutantQuery(` declaration + genuine inner `useQuery` call | declaration NOT counted, labeled DEFINITION; inner call counted | **rc=0 CLEAN, covered=1, 1 labeled DEFINITION, 0 orphan** ✓ |
| **Conformance** | emitted report through `boundary_report.validate()` + the 17-test suite | only BR008 (designed) / 17 pass | **BR008 only · 17/17** ✓ |

**Disclosure of a mid-build correction (retrieval, not sensor):** I first mis-read `portal/src/types` as
nonexistent off a `head -15`-truncated listing and "fixed" a sensor behavior that was already correct —
the full listing shows the dir exists, so the original REFUSE was right. The added nonexistent-root FAIL
guard is retained as a genuine improvement (a nonexistent domain is not an empty one — the comp-pulse
lesson from REC1C_E §4.4), and both paths are now separately exercised. Same truncation class CVO~Z
disclosed this morning; logged rather than smoothed.

## 5 · Acceptance criteria, one line each

1. **Conformant report:** emitted report passes the L0a validator (BR008 only — the designed new-shape
   visibility, not an error) and the 17-test suite passes 17/17 on this checkout. ✓
2. **Method is traversal or mention:** all cells `traversal`/`mention`; `declared` unused, no
   justification needed. ✓
3. **Positive control:** CLEAN exercised on a real subtree (rc=0). ✓
4. **Negative control:** REFUSE on nothing-to-compare (rc=3), never a residue verdict; nonexistent input
   additionally FAILs (rc=1). ✓
5. **Denominator printed, UNKNOWN first-class, direction in-band:** every run prints the four-cell
   denominator + UNKNOWN count (excluded from surface_total) + the under/over-report direction; method
   enums carry direction per-cell in the report. ✓

Standing discipline: in-stdout TRUE_RC used throughout (this shell's wrapper exit-1 artifact); native
`C:/` paths across every tool boundary (CTO~Z standing rule); no forecast claims formed, so the
two-commit pre-registration protocol was not triggered.

## 6 · What this sensor is NOT

Not a platform: the enumeration, the key-bearing-ness probe, and the exclusion parsing are bespoke to
this tool's shape and MUST NOT be reused as an engine for another tool (SENSOR_CONTRACT §6). The
shareable artifact is the emitted TYPE. Not a materiality judge: the 4 residue sites are a boundary
statement; whether `useAutoSaveQuery` deserves folding into comp-cache's walk (or its own denominator
mention) is the inference gate's question, explicitly not answered here. Not a claim about hooks outside
`portal/src`: library-internal hooks with no in-tree definition would land UNKNOWN, not orphan (none did
this run).

## 6b · ADDENDUM (0940Z) — disclosure-first disposition LANDED; orphans reclassified by coupling

Per CTO~Z's follow-on (0935Z, CVO~Z-endorsed disposition): `useAutoSaveQuery` added to comp-cache's own
NOT-audited caveat — the denominator line now reads `(useQueries / useInfiniteQuery / useAutoSaveQuery
are NOT audited by this tool)` and prints on every run; the docstring scope block names the wrapper with
its mechanism. **Deliberate deviation, flagged:** the caveat carries NO call-site count — a hand-carried
count is a frozen number that goes false on the next call site added; the sensor is the counting
instrument (noted in the tool's own docstring).

**Coupling proof (the acceptance mutant), run with the sensor UNMODIFIED:** the sensor's
`derive_doc_named_exclusions` picked the new name out of the tool's own text and reclassified all 3
orphan call sites → `doc_only`: surface 109 = covered 105 + member 0 + **doc_only 4 + orphan 0**,
VERDICT rc=2. The self-expiring-exclusion pattern working in reverse (self-enrolling): the tool's
disclosure and the sensor's cells are mechanically coupled in both directions — remove the name from
the tool and those sites re-orange to orphan on the next run. The blind spot is now tier-2 on the
disclosure hierarchy (rc-silent but disclosed); the walk-extension stays a banked follow-on.

**Metric caution (CVO~Z, at verify): the residue COUNT did not move — 4 before, 4 after.** The blind
spot did not shrink; it was RECLASSIFIED from undisclosed (`orphan`) to disclosed (`doc_only`), which is
exactly what disclosure-first means. **Anyone tracking "residue count" as the health signal sees 4→4 and
concludes nothing happened — the entire improvement is visible only in the orphan/doc_only split.** A
consumer of these reports (L2 aggregate included) must read the per-cell composition, not the residue
total: the total is a metric that cannot see this class of change.

## 7 · Handoff

- **`1.0.0_SA_CTO~Z`:** sensor #2 delivered on the TEXT/CODE shape with `doc_only` applicable-and-populated
  (complements a data/DAG sensor where it should be N/A). The `useAutoSaveQuery` orphan set is a real,
  current blind spot of `comp-cache collisions` — candidate routing: fold the hook into the tool's walk,
  or at minimum into its denominator disclosure line.
- **`3.0.0_SA_CVO~Z`:** every number re-derivable — run the sensor (4 invocations in §3/§4, verbatim
  args), or re-derive the enumeration with the token regex in the source. The reconciliation guard and
  the assert on the tool's matcher pattern are the two places the sensor would go loud if `cache_cli.py`
  drifts under it.
