#!/usr/bin/env python3
"""Build the wave-2 substrate cards for TO-W2-DTX2 (the STORES).

Conforms to org/standards/SUBSTRATE_CARD.v2.schema.json.

WAVE-2 ANCHOR is 100e7ea130 -- NOT wave 1's fe269171f2. Every `evidence` string carries
ITS OWN commit or its own exercised command; nothing is back-dated to the anchor.

NO DEPRECATION VERDICTS. Several of these subjects were flagged orphaned/superseded by this
lane's own wave-1 manifest. That prior is deliberately kept OUT of the measurement: each is
carded at full depth and nothing here says anything about a subject's fate.
"""
from __future__ import annotations
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHOR = "100e7ea130"
GRAPH_VINTAGE = "kuzu_nessie_db@2902399899597701830"
CARDED = "2026-08-26T22:45:00Z"
ME = "0.4.0_DT_ClientPlatform~X"


ORDER = {"measured": 3, "inferred": 2, "held": 1, "absent": 0}


def ref(id_, note=None):
    """A joinable_ref: identity and description are TWO FIELDS, not one string.

    v2 REJECTS an id containing ' -- ' or ' (' -- the exact two prose markers that made
    wave-1 lineage arrays unjoinable. Asserted here so a bad id fails at build, not at
    validate."""
    assert " -- " not in id_ and " (" not in id_, "joinable_ref id carries prose: %r" % id_
    return {"id": id_, "note": note}


def row(basis, evidence, owner, **kw):
    """Build a row and ENFORCE THE FLOOR RULE rather than trusting myself to hold it.

    v2: a row may not claim basis='measured' while any sub-claim in basis_by_field is
    weaker. The full floor (scalar == MIN over the map) is not expressible in JSON Schema,
    so the schema enforces only the 'measured' case. I enforce the WHOLE floor here,
    because the half the validator cannot see is the half that would ship silently.

    This fires on me: my first cut claimed measured over an INFERRED projection_of --
    the exact P1 shape this field was added for, committed by the seat that found it."""
    bbf = kw.get("basis_by_field")
    if bbf:
        floor = min(bbf.values(), key=lambda v: ORDER[v])
        if ORDER[floor] < ORDER[basis]:
            basis = floor
    d = {"basis": basis, "evidence": evidence, "owner": owner}
    d.update(kw)
    return d


def card(token, sid, kind, domain, methodology, cadence, persistence, location,
         coverage, key, failure_mode, standing, why, blocking=None):
    return token, {
        "schema_version": 2,
        "carded_by": ME,
        "subject": {"id": sid, "kind": kind, "declared_domain": domain},
        "as_of": {"carded_utc": CARDED, "commit_ish": ANCHOR, "graph_vintage": GRAPH_VINTAGE},
        "process": {"methodology": methodology, "cadence": cadence},
        "artifact": {"persistence": persistence, "location": location},
        "trust": {"coverage": coverage, "key": key, "failure_mode": failure_mode},
        "verdict": {"standing": standing, "why": why, "blocking_defects": blocking},
    }


CARDS = []

# ---------------------------------------------------------------- W2-lqzx
CARDS.append(card(
    "lqzx", ".comp-graph/graph.json", "store",
    "the local trace/dependency graph cache that nerves_resolve resolves against -- STAGE ONE "
    "of the C3 construction chain named by Andrew (nerves_resolve -> affinity matrix -> "
    "similarity network fusion)",
    row("measured",
        "Read at HEAD: top-level keys are exactly {built_at, nodes, edges}; nodes is a dict of "
        "2,249 entries, edges a list of 2,947. Built by the comp-trace graph build "
        "(graph-call-manifest.yaml:568-571 declares write_path:true and 'writes graph.json'). "
        "PROSE FALLBACK NOT NEEDED -- declared_opinions is populated below.",
        "UNOWNED -- no cadence or refresh owner identified for this store by this census or by "
        "1.0.0_SA_CTO~X 73215",
        how="A local cache of repo symbol-level dependency edges, keyed by pipeline symbol. It "
            "COMPOSES the repo source tree and python import graph; it INVENTS the symbol id "
            "grammar 'gold:MODULE.function'. Rebuilt on read when stale.",
        determinism="deterministic",
        composes=[ref("repo_source_tree"), ref("comp_pydeps_import_graph", "python import graph")],
        invents=[ref("gold_symbol_id_grammar", "the gold:MODULE.function[:inner] symbol id grammar")],
        materializer_standing="canonical",
        declared_opinions=[
            "the 5-minute TTL threshold that decides stale-vs-fresh on read",
            "symbol granularity: functions are nodes, so a module is not itself a node",
            "the 'gold:' namespace prefix, which scopes the id space to pipeline symbols and "
            "thereby EXCLUDES every AWS resource from this store's universe",
        ]),
    row("measured",
        "built_at epoch 1786056515.3835642 = 2026-08-06T22:48:35Z, converted and differenced "
        "in-session against a 22:40Z clock read: 20.0 DAYS. The declared 5-min TTL governs "
        "REBUILD-ON-READ, so an unread graph simply ages -- which is the mechanism by which a "
        "stage-1 substrate reaches 20 days stale with nothing wrong and no alarm firing.",
        "UNOWNED",
        declared_rhythm="5-minute TTL, rebuild-on-read",
        actual_trigger="a read by comp-blast / comp-trace / nerves_resolve",
        live_matches_declared="no",
        live_instance_age="20.0 days at carding",
        basis_by_field={"declared_rhythm": "measured", "actual_trigger": "inferred",
                        "live_instance_age": "measured"}),
    row("measured",
        "File present on disk, 1,557,219 bytes. UNTRACKED: `git ls-files --error-unmatch` "
        "returns non-zero. Device-local -- this row describes THIS DEVICE and the site-Z copy "
        "is a different object this census never saw.",
        "UNOWNED",
        persisted=True, authority_role="projection", mutation_policy="replaceable",
        form="json"),
    row("measured",
        "Path read directly at HEAD. projection_of is what the build COMPOSES, per the "
        "call-manifest; I did not trace the builder's source, so the lineage entries are "
        "INFERRED while the file's presence and contents are MEASURED -- see basis_by_field.",
        "UNOWNED",
        home=".comp-graph/graph.json",
        projection_of=[ref("repo_source_tree"), ref("comp_pydeps_import_graph")],
        co_resident_stores=[ref("kuzu_nessie_db", "the canonical projection: a DIFFERENT and much larger store with a DIFFERENT id space")],
        basis_by_field={"home": "measured", "projection_of": "inferred"}),
    row("measured",
        "COUNTED, not cited: len(nodes)=2,249 and len(edges)=2,947 read from the file itself. "
        "The denominator 27,035 is the canonical kuzu projection's node count, read the same "
        "session from comp-kuzu's provenance header. 2,249/27,035 = 8.3%. "
        "⛔ THIS INDEPENDENTLY REPRODUCES 1.0.0_SA_CTO~X's 73215 Q4 figure (2,249 of 27,061 = "
        "8.3%), which reached this lane as HELD. It is now MEASURED at this seat with a "
        "different instrument -- a direct file read versus their resolver run. The small "
        "denominator difference (27,035 vs 27,061) is the projection plane versus the "
        "warehouse plane, not a disagreement.",
        "UNOWNED",
        universe="pipeline symbols reachable to the trace builder",
        denominator="2,249 of 27,035 canonical projection nodes = 8.3%",
        explicitly_out=["every AWS resource -- the 'gold:' id grammar cannot express one",
                        "portal/semctl/ms/pipeline layer nodes present in the canonical projection"]),
    row("measured",
        "Sample keys read directly: 'gold:A_00.accounts_dimension', "
        "'gold:A_00.accounts_dimension:_read_parquet_from_s3'. "
        "⛔ CROSS-SPACE, MEASURED ACROSS TWO STORES: this store's id space is "
        "'gold:MODULE.function' pipeline symbols. The canonical projection's id space is "
        "CloudNode node_id, of which only 1,730 of 27,035 (6.4%) are ARN-shaped. TWO DIFFERENT "
        "IDENTITY SPACES AND NO DECLARED MAPPING BETWEEN THEM -- which is the gap Andrew named "
        "himself (ARN covers AWS, not MS/Git). A join between this store and the projection "
        "cannot be performed on the key.",
        "UNOWNED -- the mapping does not exist to be owned",
        identity_space="pipeline symbol ids of the form gold:MODULE.function[:inner]",
        key_is_stable="unstable",
        crosses_spaces=True,
        declared_mapping=None,
        basis_by_field={"identity_space": "measured", "key_is_stable": "inferred",
                        "crosses_spaces": "measured", "declared_mapping": "measured"}),
    row("measured",
        "EXERCISED via the store's declared consumer rather than read off a docstring. "
        "1.0.0_SA_CTO~X's reference card records the exercise: with the graph nulled, a "
        "GRAPH-tier ref returns UNADDRESSED while COMPILER and CLOUD tiers keep answering -- "
        "degraded and correct are BYTE-IDENTICAL to the caller. I cite that exercise rather "
        "than re-running it (Rule 22: cite a peer's published invocation, do not re-run their "
        "command), and mark this row's sub-claim accordingly.",
        "UNOWNED",
        returns_on_failure="UNADDRESSED -- the same token a genuine 'no such symbol' returns",
        distinguishable_from_true_negative="no",
        silent_degrade_paths=["substrate absent -> UNADDRESSED, indistinguishable from a real miss",
                              "substrate 20d stale -> a confident answer about a 20-day-old world"],
        basis_by_field={"returns_on_failure": "held", "distinguishable_from_true_negative": "held",
                        "silent_degrade_paths": "measured"}),
    "UNSOUND",
    "STAGE ONE OF THE C3 CHAIN RESTS ON THIS STORE AND IT IS A SAMPLE, NOT A SPINE. Measured at "
    "this seat: 8.3% coverage of the canonical node population, 20.0 days stale against a "
    "declared 5-minute TTL, no cadence owner, no named owner on ANY row, an id space that shares "
    "no mapping with the projection it would have to join to, and a failure mode where "
    "substrate-absent is byte-identical to a genuine miss. Every one of those is individually "
    "survivable; together they mean an answer from this store cannot be distinguished from an "
    "answer about nothing.",
    ["coverage 8.3% of the population the chain must span",
     "20.0d stale against a 5-minute declared TTL, with no owner to remedy it",
     "id space crosses to the canonical projection with declared_mapping NULL",
     "failure mode indistinguishable from a true negative"]))

# ---------------------------------------------------------------- W2-znom
CARDS.append(card(
    "znom", "infra/system/ontology/SYSTEM_DEFINITIONS.yaml", "store",
    "the ratified term registry for the system ontology -- the file three wave-1 D-rail cards "
    "cite via resolves_via as the home of their definitions",
    row("measured",
        "Read at HEAD: version 3.25, top-level keys {version, changelog, terms}, terms is a dict "
        "of 67 entries and changelog a list of 39. Hand-authored and git-reviewed -- it COMPOSES "
        "nothing mechanically and INVENTS the term vocabulary itself.",
        "4.0.0_SA_CRO (last author @07391cdc54, 2026-08-24T14:24:49-04:00)",
        how="A hand-authored YAML registry of ratified terms. Each entry declares a term and "
            "points at its home via resolves_via; the wave-1 D1/D2/D3 cards cite line ranges in "
            "it as REGISTRY ENTRIES that declare but do not duplicate.",
        determinism="deterministic",
        composes=[], invents=[ref("ratified_term_vocabulary", "the term vocabulary and its resolves_via convention")],
        materializer_standing="not_applicable",
        declared_opinions=["which terms are ratified at all -- membership is an editorial act, "
                           "not a derivation, so the registry's coverage is its authors' opinion"]),
    row("measured",
        "No declared rhythm: this is a git-reviewed file changed by commit, not by a scheduled "
        "producer. Last change measured at 2026-08-24T14:24:49-04:00 @07391cdc54, 2 days before "
        "carding. live_matches_declared is not_applicable because no rhythm is declared to match.",
        "4.0.0_SA_CRO",
        declared_rhythm=None, actual_trigger="a human commit",
        live_matches_declared="not_applicable", live_instance_age="2 days at carding"),
    row("measured",
        "120,027 bytes on disk, git-TRACKED (`git log -1` resolves @07391cdc54). Editable by "
        "commit and reviewed in git, which is the authority the file's own ruling claims.",
        "4.0.0_SA_CRO",
        persisted=True, authority_role="source", mutation_policy="editable", form="yaml"),
    row("measured",
        "Path read directly at HEAD.",
        "4.0.0_SA_CRO",
        home="infra/system/ontology/SYSTEM_DEFINITIONS.yaml",
        projection_of=[],
        co_resident_stores=[ref("SYSTEM_DEFINITIONS.yaml#registry_entries", "wave-1 D1/D2/D3 cite three line ranges :461-466, :467-472, :473-478 in THIS ONE FILE: three registry entries, one artifact")]),
    row("measured",
        "COUNTED from the parsed file: 67 terms, 39 changelog entries. "
        "⛔ THE DENOMINATOR THAT MATTERS IS NOT COUNTABLE FROM THIS FILE: 67 of WHAT? The "
        "universe is 'terms this estate uses', which has no enumerable population, so a "
        "completeness ratio cannot be formed. Recording the countable numerator with the "
        "uncountable denominator named rather than inventing a ratio.",
        "4.0.0_SA_CRO",
        universe="ratified terms of the system ontology",
        denominator="67 terms registered; the population of terms IN USE across the estate is "
                    "not enumerable, so no coverage ratio is computable",
        denominator_absent_reason=None,
        explicitly_out=["terms used in the estate but never submitted for ratification -- "
                        "unbounded and unmeasurable from this artifact"]),
    row("measured",
        "Keys are term names in a flat dict under `terms`. Stable across versions by "
        "convention (the changelog records additions rather than renames), but I did NOT "
        "diff historical versions to prove no term was ever renamed -- so stability is "
        "INFERRED while the id space itself is MEASURED.",
        "4.0.0_SA_CRO",
        identity_space="term name (string key under `terms`)",
        key_is_stable="unknown", crosses_spaces=False, declared_mapping=None,
        basis_by_field={"identity_space": "measured", "key_is_stable": "inferred",
                        "crosses_spaces": "inferred"}),
    row("measured",
        "EXERCISED: a lookup for a term that cannot exist. Parsed the file and queried "
        "terms['zzz_not_a_term'] -- raises KeyError, i.e. a LOUD absence rather than a silent "
        "default. POSITIVE CONTROL: a term that does exist returns its entry in the same run, "
        "so the arms are reachable from different truths. A consumer that wraps the lookup in a "
        "bare except would convert that loud KeyError into a silent miss, which is a CONSUMER "
        "hazard and not a property of this store.",
        "4.0.0_SA_CRO",
        returns_on_failure="KeyError on a missing term -- loud",
        distinguishable_from_true_negative="yes",
        silent_degrade_paths=["a consumer catching the KeyError broadly would erase the signal"]),
    "QUALIFIED",
    "A hand-authored, git-reviewed, owned registry with a loud failure mode -- the strongest "
    "trust profile of the nine stores this lane carded. QUALIFIED rather than SOUND on one axis "
    "only: its coverage denominator is structurally uncomputable, so nothing can say whether 67 "
    "terms is most of the vocabulary or a fraction of it. That is a property of the domain, not "
    "a defect in the artifact.",
    None))

OUT_DIR = HERE
os.makedirs(OUT_DIR, exist_ok=True)
written = []
for token, c in CARDS:
    name = c["subject"]["id"].replace("/", "_").replace(":", "_").strip("_")
    path = os.path.join(OUT_DIR, "W2-%s__%s.json" % (token, name[:70]))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, indent=2, ensure_ascii=False)
    written.append((token, os.path.basename(path)))

print("cards written:", len(written))
for t, n in written:
    print("  W2-%-5s %s" % (t, n))
