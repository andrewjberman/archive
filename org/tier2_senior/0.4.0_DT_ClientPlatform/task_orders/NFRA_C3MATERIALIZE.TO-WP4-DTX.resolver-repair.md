# TASK ORDER -- DTX · NFRA_C3MATERIALIZE WP-4 · RESOLVER REPAIR (A2)

<status>pending</status>

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X` · **lane owner (grant):** `1.0.0_SA_CTO~X`
**scope:** 7 entities / 28 cells -- 23 executor cells + 5 mechanism cells on this face · **subject:** `org/modules/graph/nerves_resolve.py` @6acff60264 · **contract:** v0.3-candidate+27 FROZEN (untouched) · **decomp:** CERTIFIED PASS @8057c94e7a (`3.0.0_SA_CVO~X` attempt 1; final rectangle sha256 3f165552fd6f08bf73432b8c72b122bd9e4af241d799332ad46904287d65c0da = the sealed dry)

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-wp4/20260828T1442Z/DECOMP.md @8057c94e7a

cells:
WP4-whvg-1 WP4-whvg-2 WP4-whvg-3 WP4-whvg-4 WP4-whvg-5
WP4-zzua-1 WP4-zzua-2 WP4-zzua-3 WP4-zzua-4 WP4-zzua-5
WP4-bcax-1 WP4-bcax-2 WP4-bcax-3
WP4-zgom-1 WP4-zgom-2 WP4-zgom-3 WP4-zgom-4 WP4-zgom-5
WP4-rthi-1 WP4-rthi-2
WP4-qoos-1 WP4-qoos-2 WP4-qoos-3
WP4-mech-1 WP4-mech-2 WP4-mech-3 WP4-mech-4 WP4-mech-5

<owned_cells>
WP4-whvg-1 WP4-whvg-2 WP4-whvg-3 WP4-whvg-4 WP4-whvg-5
WP4-zzua-1 WP4-zzua-2 WP4-zzua-3 WP4-zzua-4 WP4-zzua-5
WP4-bcax-1 WP4-bcax-2 WP4-bcax-3
WP4-zgom-1 WP4-zgom-2 WP4-zgom-3 WP4-zgom-4 WP4-zgom-5
WP4-rthi-1 WP4-rthi-2
WP4-qoos-1 WP4-qoos-2 WP4-qoos-3
</owned_cells>
</decomp_ref>

<proof_of_spec>
  <criterion id="WP4-AC1" cell_refs="WP4-whvg-1, WP4-whvg-2, WP4-whvg-3, WP4-whvg-4, WP4-whvg-5"/>
  <criterion id="WP4-AC2" cell_refs="WP4-zzua-1, WP4-zzua-2, WP4-zzua-3, WP4-zzua-4, WP4-zzua-5"/>
  <criterion id="WP4-AC3" cell_refs="WP4-bcax-1, WP4-bcax-2, WP4-bcax-3"/>
  <criterion id="WP4-AC4" cell_refs="WP4-zgom-1, WP4-zgom-2, WP4-zgom-3, WP4-zgom-4, WP4-zgom-5"/>
  <criterion id="WP4-AC5" cell_refs="WP4-rthi-1, WP4-rthi-2, WP4-qoos-1, WP4-qoos-2, WP4-qoos-3"/>
  <criterion id="WP4-AC6" cell_refs="WP4-mech-1, WP4-mech-2, WP4-mech-3, WP4-mech-4, WP4-mech-5"/>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_C3MATERIALIZE.TO-WP4-DTX_PROOF_OF_SPEC.json</instance_path>

  <expected_criteria>WP4-AC1,WP4-AC2,WP4-AC3,WP4-AC4,WP4-AC5,WP4-AC6</expected_criteria>
  <alignment_denominators>criteria: 6. Cells: 28 of 28 in the certified decomp -- 23 owned by this executor + 5 mechanism cells discharged on this face by AC6; every cell covered by exactly one criterion; backward: every criterion cites >= 3 cells.</alignment_denominators>
</proof_of_spec>

---

## AUTHORITY

D11 ledger row 17 (R1 LIFTED, Andrew-direct 2026-08-28 14:08Z @676604de18) unblock (2); track A2 of `1.0.0_SA_CTO~X` 77876 ("decomposable now, from specs that already exist"), sequenced after WP-3b by the issuer (77886). RULING.md (D11_ISCK_RULING_20260827) EXECUTION SEQUENCE: WP-3 DONE -> **WP-4 resolver repair** -> WP-5. RULING.md:61, verbatim: *"Resolver failure semantics -- RESOLVED: RESOLVED/AMBIGUOUS/GENUINELY_UNADDRESSED/SUBSTRATE_UNAVAILABLE/NOT_APPLICABLE -- the two-state collapse in nerves_resolve is to be repaired."* Rule 27: cut from `rectangle.final.certified.json` @8057c94e7a only. No egress of any kind in this TO.

## THE INPUT, READ AT SOURCE

- SUBJECT: `org/modules/graph/nerves_resolve.py` @6acff60264 -- `resolve(ref) -> Resolution{node_ids, kind, confidence EXACT|STRONG|WEAK|NONE, source}`, `resolve_many`, `_self_test()`; composed tiers DERIVED at c0 = 5 (`_trace_graph`, `_pydeps`, `_graph_index`, `_repo_basenames`, `_tools_on_disk`); broad `except Exception:` -> None at :77 and two siblings (3 measured). Re-derive both counts in your report; the face types neither.
- CARDS: `org/tier1_exec/1.0.0_SA_CTO/deliverables/D11_REFERENCE/nerves_resolve.card.json` (v1: an absent substrate returns UNADDRESSED / NONE / [] byte-identical to a genuine miss) and `org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_CARDS_W4/W4-nerves_resolve.card.json` (v3: staleness is silent).
- LEDGER: `org/standards/isck/WP3_LEDGER_DESIGN.md` @d0398b977d sec 2 (derived read model -- canonical serial for any serial) + 2d (typed reference policies); `org/standards/isck/ledger/engine.py` read surfaces (`Store.get / estate / head / replay`). The contract does not move.
- MEMO: "every resolution result carries source vintage, fabric, evidence, plural candidates, confidence" + "resolver version on every result".

## ORDER OF WORK

Result contract (AC1) -> substrate liveness (AC3) -> spine re-pointing (AC2) -> continuity fixtures (AC4) -> compatibility + battery from a clean clone (AC5) -> report. AC6's mechanism cells are on this face from cut.

## ACCEPTANCE CRITERIA (each cites the cells it discharges)

**WP4-AC1 -- THE FIVE-STATE RESULT CONTRACT** (`WP4-whvg-1..5`): every resolution returns exactly one of RESOLVED / AMBIGUOUS / GENUINELY_UNADDRESSED / SUBSTRATE_UNAVAILABLE / NOT_APPLICABLE, enforced by the result type; SUBSTRATE_UNAVAILABLE names the tier and the exception class and is NEVER byte-identical to GENUINELY_UNADDRESSED (the arm: remove one tier's substrate, the same ref flips state); every result carries per-tier source vintage (artifact path + mtime/commit), fabric, evidence refs, PLURAL candidates, the confidence band (kept, orthogonal), and the resolver version (the file's own digest); AMBIGUOUS returns ALL candidates with per-candidate evidence and never picks one; NOT_APPLICABLE is the wrong-fabric / wrong-plane answer with the fabric named.

**WP4-AC2 -- SPINE RE-POINTED AT THE LEDGER'S MINTED SERIALS, READ-ONLY** (`WP4-zzua-1..5`): a resolved ref returns the canonical `ent:` serial via the derived read model beside the legacy node_ids (an alias serial yields the canonical, not itself); candidate-only serials are never reported canonical; the resolver READS the ledger and never admits, writes or mints (the negative arm greps the resolver for `Store.admit` / any write: zero); a ref that PARSES as a record id is resolved STRICT against the ledger and never basename-fuzzed (a parsed-but-absent id -> GENUINELY_UNADDRESSED with policy STRICT named); `bundle_identity.py --check` MATCH before and after. **AMENDED 2026-08-28 18:5xZ (issuer, on 3.0.0_SA_CVO~X REFUSE 185625Z + 0.4.0_DT_ClientPlatform~X 78716 -- an ISSUER INSTRUMENT DEFECT, not a relaxation of the invariant):** the literal `--check MATCH` predicate compares the whole derivation record incl. `derived_at_commit` / `validator_commit` / `schema_commit`, which move with HEAD, and it reads STALE rc=1 at the PRE-change pin (parent of a3c34f019f, CVO-measured) as well as after -- a predicate that fails before the executor's change cannot discriminate that change, so it measured the tool's provenance pointers, never the invariant this clause protects. THE CLAUSE NOW READS: the frozen bundle is UNMOVED by the resolver repair -- `contract_bundle_id` byte-identical (bundle:sha256:87ed7080...), `candidate_id` unchanged and 0 members differ between the pre-change pin and the run pin, measured via `bundle_identity.py`'s derivation at BOTH pins and printed with both values; a differing member set FAILS. Regeneration of `BUNDLE_IDENTITY.json` so the pointer record MATCHes at HEAD is the label owner's act (`1.0.0_SA_CTO~X`), outside this TO, as with WP-3b's registry write. Cell refs unchanged; the certifier re-reads the clause as amended.

**WP4-AC3 -- SUBSTRATE LIVENESS AND VINTAGE** (`WP4-bcax-1..3`): each composed tier reports AVAILABLE / UNAVAILABLE(reason) per call; the broad excepts are replaced by typed capture (grep for `except Exception:` / bare `except:` returning None or {} in the resolver: zero remaining); each tier's substrate vintage is on the result so staleness is readable; a resolution with one tier UNAVAILABLE is never reported as a clean miss.

**WP4-AC4 -- CONTINUITY TESTS** (`WP4-zgom-1..5`, from RULING.md:106-108): file rename keeps the canonical serial (node_id may change, serial does not); a graph-index / Kuzu rebuild keeps serials; the same ref at the same substrate vintages reproduces a byte-identical result (canonical serialization, two runs one digest); a cross-fabric ref is NOT_APPLICABLE with the fabric named, never resolved by coincidence of name; two serials minted for one subject resolve to ONE canonical via the identity_relation fold (retired -> canonical; canonical -> itself).

**WP4-AC5 -- COMPATIBILITY + BATTERY FROM A CLEAN CLONE, NO EGRESS** (`WP4-rthi-1..2`, `WP4-qoos-1..3`): `resolve` / `resolve_many` keep their call shape and the new fields are ADDITIVE -- every existing `_self_test()` case still passes and the consumer census (callers of `resolve`/`resolve_many`, repo-wide, denominator printed; c0 read 12 files naming the module incl. `org/modules/graph/cli.py`, `nerves_accrete.py`, `nerves_lexical.py`, `census_finalize.py` x2) is re-counted and every caller exercised or named; the self-test is extended (one case per new state and per continuity test) and never weakened; the battery has reject + accept arms per state and per continuity test, each independently load-bearing (mutation-proved one rule at a time), the denominator printed by counting ids; runs from a fresh unique clone at `--run-commit` with `run_battery.py` exit semantics; no PyPI / vendor / cloud call anywhere in the repair or its battery (the negative arm greps for pip / requests / boto3 in the delivered files: zero new).

**WP4-AC6 -- MECHANISM, ON THIS FACE** (`WP4-mech-1..5`): mech-1 the scoped lane grant (LANE below); mech-2 the consumer census before the first commit (printed, never a guess); mech-3 NOT WP-5 -- no bridge cell populated; mech-4 certifier never the author (this decomp was certified by `3.0.0_SA_CVO~X` from the issuer's c0); mech-5 the lift cited verbatim, nothing wider.

## LANE

The subject `org/modules/graph/nerves_resolve.py` and its battery path (name it on your first report; proposed `org/modules/graph/tests/nerves_resolve_battery/**` or the repo's existing test home for that module) sit outside this seat's home lane; the subject's carding lane (`0.8.0_AE_CloudComp`) is dark. **`1.0.0_SA_CTO~X` grants a scoped `.owned-paths.yaml` row for `0.4.0_DT_ClientPlatform~X` on the subject file + the named battery path for this TO's life, exercised by the first refused commit, struck on the flip.** Until it lands, the first commit there is REFUSED -- that is the exercise. The PROOF_OF_SPEC instance and the report live in this seat's own `deliverables/`.

## BOUNDARIES

- No contract byte moves (v0.3-candidate+27 frozen). If the repair needs a contract field, that is a FINDING to the label owner, never an edit here.
- The resolver reads the ledger; it never writes it. No mint on miss.
- Not WP-5: the resolver learns to SAY what it cannot resolve; it learns no new resolutions.
- No egress. The B4 words ("you have egress"; "in an aws container") cover B4 alone.

## REPORT

Route completion to `3.0.0_SA_CVO~X`, cc issuer, with: the derived tier count and broad-except count before/after; the consumer census with its denominator; the battery's printed line (arms run, caught mutants); the five continuity fixtures' outcomes; the run_commit; the proof-of-spec instance VALID line; and **PUSH STATE as a MEASURED value** (ls-remote read). The issuer flips this face on the certifier's verdict.
