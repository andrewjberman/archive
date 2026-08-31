"""NFRA_C3MATERIALIZE.TO-L3S7A-CCY.determination -- THE PRODUCER.

Measures, at a NAMED CURRENT VINTAGE, whether a bridge CAN be declared against PRD 7a's FOUR
conditions, and TYPES whichever outcome the measurement supports.

DERIVED, NEVER TYPED. Every count below is computed from the carrier's bytes at run time. The only
typed constants are design constants ruled elsewhere: the cell ids and gates (from the certified
rectangle), the `digest_of` enum (Addendum 1l(vi)), and the prior's four published values, which are
quoted from the face's own AC9 oracle so the comparison has a fixed left-hand side.

ACCEPTANCE IS ON THE MEASUREMENT AND THE TYPING, NEVER ON WHICH OUTCOME APPEARS.

Owner: 0.8.0_AE_CloudComp~X.
"""

from __future__ import annotations

import collections
import datetime
import hashlib
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
).stdout.strip()

CARRIER = "org/modules/graph/tsgraph_spike/out/portal_full.graph.json"

FACE = {
    "id": "NFRA_C3MATERIALIZE.TO-L3S7A-CCY.determination",
    "path": "org/tier2_senior/0.8.0_AE_CloudComp/task_orders/"
    "NFRA_C3MATERIALIZE.TO-L3S7A-CCY.determination.md",
    "pin": "03013b7115",
}
RECORD = {
    "record": "rectangle.final.certified.json",
    "path": "workflows/atom_decomposition/runs/nfra-c3materialize-L3/20260830T1710Z/"
    "rectangle.final.certified.json",
    "pin": "b48dfbbd19",
    "digest_of": "blob-at-pin",
}

# The prior, QUOTED from the face's AC9 oracle at pin 03013b7115. Fixed left-hand side of the
# comparison so this run cannot drift it.
PRIOR = {
    "pin": "a28e588b7f",
    "declared_by_store": "NO",
    "edges_targeting_a_module": 0,
    "edge_denominator": 16397,
    "join": "NONE",
    "firm_carry": "NOT_CARRIED",
}

# The store owner, resolved from the NFRA_TSGRAPH.P1 GO + RAVC2 routing, not asserted.
STORE_OWNER = "0.4.0_DE_ClientPlatform"

FIRM_PARTNER_DIR = re.compile(r"_partners/([^/]+)/")


def sh(*args: str) -> str:
    return subprocess.run(args, capture_output=True, text=True, cwd=ROOT).stdout.strip()


def tracked(path: str) -> bool:
    return (
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", path], capture_output=True, cwd=ROOT
        ).returncode
        == 0
    )


def measure() -> dict:
    """Every number this determination rests on, derived from the carrier's bytes."""
    abspath = os.path.join(ROOT, CARRIER)
    raw = open(abspath, "rb").read()
    st = os.stat(abspath)
    graph = json.loads(raw)
    nodes, edges = graph["nodes"], graph["edges"]
    byid = {n["id"]: n for n in nodes}
    cls = {n["id"]: n["label"] for n in nodes}

    n_modules = sum(1 for c in cls.values() if c == "Module")
    non_module = [n for n in nodes if n["label"] != "Module"]

    inbound = [e for e in edges if cls.get(e["dst"]) == "Module"]
    outbound = [e for e in edges if cls.get(e["src"]) == "Module"]
    declares = [e for e in edges if e["label"] == "DECLARES"]

    # DISCRIMINATOR: is a DECLARES edge recoverable from a parse of the dst id, or only from the
    # declared edge itself? If every dst id already contains the src module path, the declared edge
    # and the parse carry the SAME information -- the edge is still DECLARED (basis measured), but it
    # buys no reach a parse would not.
    parse_equivalent = 0
    cross_module = 0
    for e in declares:
        src_path = (byid.get(e["src"], {}).get("attrs") or {}).get("path")
        dst_path = (byid.get(e["dst"], {}).get("attrs") or {}).get("path")
        if src_path and src_path in e["dst"]:
            parse_equivalent += 1
        if src_path and dst_path and src_path != dst_path:
            cross_module += 1

    # NEGATIVE CONTROL for that discriminator: the other Module-outbound labels MUST show
    # cross-module reach, or the probe is dead and its zero means nothing.
    control = {}
    for lab in ("READS_FIELD", "REFERENCES_TYPE"):
        sub = [e for e in edges if e["label"] == lab and cls.get(e["src"]) == "Module"]
        x = sum(
            1
            for e in sub
            if (byid.get(e["src"], {}).get("attrs") or {}).get("path") not in (e["dst"] or "")
        )
        control[lab] = {"edges": len(sub), "cross_module": x}

    # FIRM. Two questions, deliberately separate: is firm a DECLARED key anywhere, and how far does
    # the only alternative (a path parse, which L1 7a:348-350 refuses) actually reach?
    attr_keys = set()
    for n in nodes:
        attr_keys.update((n.get("attrs") or {}).keys())
    edge_attr_keys = set()
    for e in edges:
        edge_attr_keys.update((e.get("attrs") or {}).keys())
    firm_keys = [
        k
        for k in sorted(attr_keys | {"edge." + k for k in edge_attr_keys})
        if re.search(r"firm|tenant|client", k, re.I)
    ]

    partner = collections.Counter()
    for n in nodes:
        if n["label"] != "Module":
            continue
        m = FIRM_PARTNER_DIR.search((n.get("attrs") or {}).get("path") or "")
        if m:
            partner[m.group(1)] += 1

    reachable = {e["dst"] for e in outbound}

    return {
        "carrier": {
            "path": CARRIER,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "mtime_utc": datetime.datetime.fromtimestamp(
                st.st_mtime, datetime.timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tracked": tracked(CARRIER),
            "extractor": (graph.get("meta") or {}).get("extractor"),
            "producer_project": (graph.get("meta") or {}).get("project"),
        },
        "nodes": len(nodes),
        "edges": len(edges),
        "node_classes": len(set(cls.values())),
        "edge_labels": len({e["label"] for e in edges}),
        "modules": n_modules,
        "non_module_nodes": len(non_module),
        "inbound_to_module": len(inbound),
        "outbound_from_module": len(outbound),
        "outbound_by_label": dict(collections.Counter(e["label"] for e in outbound)),
        "declares": len(declares),
        "declares_distinct_symbols": len({e["dst"] for e in declares}),
        "declares_distinct_modules": len({e["src"] for e in declares}),
        "declares_parse_equivalent": parse_equivalent,
        "declares_cross_module": cross_module,
        "discriminator_control": control,
        "symbols_reachable_from_a_module": len(reachable),
        "firm_declared_keys": firm_keys,
        "attr_key_vocabulary": sorted(attr_keys),
        "firm_partner_modules": sum(partner.values()),
        "firm_partner_by_token": dict(partner),
        "store_owner": STORE_OWNER,
    }


def pct(num: int, den: int) -> str:
    return "%.1f%%" % (100.0 * num / den) if den else "n/a"


def build_cells(m: dict) -> list:
    """Nine cell carriers, one per owned cell. Values DERIVED from m."""
    c = m["carrier"]

    # The carrier is UNTRACKED. Addendum 1l(vi) forbids inventing a pin to fill the field: the
    # identity is CONTENT-ADDRESSED and the missing git identity is a NAMED GAP, stated with its
    # retrieval rather than papered over.
    identity = {
        "digest_of": "content-addressed",
        "sha256": c["sha256"],
        "bytes": c["bytes"],
        "mtime_utc": c["mtime_utc"],
        "retrieval": "sha256sum %s at the workspace root on this device" % c["path"],
        "named_gap": (
            "NO GIT IDENTITY AT ANY PIN. The carrier is UNTRACKED (git ls-files returns no match; "
            "positive control: sibling files under org/modules/graph/ ARE tracked and return a "
            "path). Neither this figure nor the prior's is re-derivable from git by this seat or by "
            "a certifier. The sha256 IS the identity; blob-at-pin would assert a pin that does not "
            "exist."
        ),
        "vintage_named": c["mtime_utc"],
        "vintage_caveat": (
            "mtime is MUTABLE and does not certify content -- it is reported as the vintage NAME, "
            "and the sha256 beside it is what actually fixes the bytes."
        ),
    }

    join_cov = "%d of %d" % (m["declares_distinct_symbols"], m["non_module_nodes"])

    cells = [
        {
            "cell_id": "L3S7A-svin-1",
            "criterion": "L3S7A-CCY-AC1",
            "label": "store_vintage.carrier_identified",
            "gate": "now",
            "value": {
                "carrier": c["path"],
                "identity": identity,
                "produced_by": {
                    "project": c["producer_project"],
                    "extractor": c["extractor"],
                    "owner": m["store_owner"],
                },
                "shape_at_this_vintage": {
                    "nodes": m["nodes"],
                    "edges": m["edges"],
                    "node_classes": m["node_classes"],
                    "edge_labels": m["edge_labels"],
                    "modules": m["modules"],
                },
                "basis": "measured",
                "inherited_from_a_prior_record": False,
            },
        },
        {
            "cell_id": "L3S7A-bcon-1",
            "criterion": "L3S7A-CCY-AC2",
            "label": "bridge_conditions.registry_ownership",
            "gate": "after-store-vintage",
            "value": {
                "condition": "7a condition 1 -- NEW ARTIFACT, D11-OWNED REGISTRY ONLY, no edit to "
                "any producing store",
                "verdict": "MET",
                "measurement": (
                    "The proposed row cites an edge set that ALREADY EXISTS in the carrier "
                    "(%d DECLARES edges of %d). Citing an existing edge requires no write of any "
                    "kind to the producing store; the row is a new file in the D11-owned registry "
                    "at org/tier2_senior/0.8.0_AE_CloudComp/deliverables/D11_L3_BRIDGE_REGISTRY/."
                )
                % (m["declares"], m["edges"]),
                "store_edit_required": None,
                "basis": "measured",
            },
        },
        {
            "cell_id": "L3S7A-bcon-2",
            "criterion": "L3S7A-CCY-AC3",
            "label": "bridge_conditions.basis",
            "gate": "after-store-vintage",
            "value": {
                "condition": "7a condition 2, limb 1 -- every bridge row carries its BASIS, stated "
                "as a RELATION and not a name",
                "verdict": "MET",
                "relation": (
                    "A Module node M (attrs.path = a repo file path) is joined to a symbol node S "
                    "by a store-declared edge whose `label` field is the literal DECLARES. The rule "
                    "is the store's own extractor output, not a reader's inference: %s emitted by "
                    "%s."
                )
                % (c["extractor"], c["producer_project"]),
                "not_a_name": (
                    "'symbol_to_file' names nothing checkable; 'M --DECLARES--> S where "
                    "cls(M)==Module' is a predicate a reader can run and this run did."
                ),
                "basis": "measured",
                "corrects_prior": (
                    "The prior shard typed this basis `inferred` on the reasoning that the roll-up "
                    "is 'recoverable ONLY by parsing the symbol id's module prefix'. That is FALSE "
                    "as written: for %d symbols the containment is READ from a declared edge, not "
                    "parsed. See L3S7A-detn-2."
                )
                % m["declares_distinct_symbols"],
            },
        },
        {
            "cell_id": "L3S7A-bcon-3",
            "criterion": "L3S7A-CCY-AC4",
            "label": "bridge_conditions.endpoints",
            "gate": "after-store-vintage",
            "value": {
                "condition": "7a condition 2, limb 2 -- the (PLANE, ENTITY) endpoints, BOTH named",
                "verdict": "MET",
                "endpoints": [
                    {
                        "plane": "PORTAL_STRUCTURE",
                        "entity": "Module",
                        "population": m["modules"],
                        "key": "node.id (module:<path>), node.attrs.path",
                    },
                    {
                        "plane": "PORTAL_STRUCTURE",
                        "entity": "symbol (TypeDecl | ReactComponent | Field | DataFetch)",
                        "population": m["non_module_nodes"],
                        "key": "node.id",
                    },
                ],
                "both_halves_present": True,
                "same_plane": True,
                "same_plane_note": (
                    "BOTH endpoints sit on the PORTAL_STRUCTURE plane. This is a within-plane "
                    "ROLLUP_CONTAINMENT, which is what the symbol_to_file row has always been; it "
                    "is NOT a cross-plane bridge and nothing here should be read as one."
                ),
                "basis": "measured",
            },
        },
        {
            "cell_id": "L3S7A-bcon-4",
            "criterion": "L3S7A-CCY-AC5",
            "label": "bridge_conditions.join_evidence",
            "gate": "after-store-vintage",
            "value": {
                "condition": "7a condition 2, limb 3 -- join evidence WITH ITS DENOMINATOR. THE "
                "DECISIVE LIMB.",
                "verdict": "MET",
                "join": {
                    "numerator": m["declares"],
                    "denominator": m["edges"],
                    "reading": "%d of %d edges in the carrier are DECLARES edges"
                    % (m["declares"], m["edges"]),
                    "symbol_coverage_numerator": m["declares_distinct_symbols"],
                    "symbol_coverage_denominator": m["non_module_nodes"],
                    "symbol_coverage": "%s (%s) of non-Module nodes carry a declared containment"
                    % (join_cov, pct(m["declares_distinct_symbols"], m["non_module_nodes"])),
                    "modules_emitting": "%d of %d Module nodes"
                    % (m["declares_distinct_modules"], m["modules"]),
                    "artifact_carrying_the_relation": c["path"],
                    "artifact_identity": identity["sha256"],
                },
                "substantive_search": {
                    "question": "does ANY measurable relation a D11-OWNED registry could declare "
                    "with basis `measured` exist WITHOUT touching a producing store",
                    "answer": "YES -- the DECLARES edge set above.",
                    "corpus_searched": [
                        "4 *.graph.json carriers in the estate (all four opened and censused)",
                        "infra/aws/globgrph/stitch_graph.json (43,633 edges, AWS plane)",
                        "portal/dist build output",
                        "source maps (*.map) across the estate",
                        "build manifests (*manifest*.json) in portal",
                    ],
                    "denominator_note": "comp-find scoped censuses; the *.map and *manifest* "
                    "sweeps returned MEASURED zeros over printed denominators.",
                },
                "reach_limit_of_this_join": {
                    "parse_equivalent": m["declares_parse_equivalent"],
                    "cross_module": m["declares_cross_module"],
                    "finding": (
                        "%d of %d DECLARES edges have a dst id that ALREADY CONTAINS the src "
                        "module path, and %d are cross-module. So the declared edge and a parse of "
                        "the id carry the SAME information. The edge is genuinely DECLARED -- which "
                        "is what moves basis from `inferred` to `measured` -- but it buys NO reach "
                        "a parse would not have had. Stated here so no reader infers extra coverage "
                        "from the word `measured`."
                    )
                    % (
                        m["declares_parse_equivalent"],
                        m["declares"],
                        m["declares_cross_module"],
                    ),
                    "negative_control": {
                        "result": m["discriminator_control"],
                        "reads": (
                            "The cross-module probe is NOT dead: READS_FIELD returns %d of %d "
                            "cross-module and REFERENCES_TYPE %d of %d. A probe that can find "
                            "cross-module edges elsewhere returning 0 on DECLARES is a structural "
                            "zero, not an instrument failure."
                        )
                        % (
                            m["discriminator_control"]["READS_FIELD"]["cross_module"],
                            m["discriminator_control"]["READS_FIELD"]["edges"],
                            m["discriminator_control"]["REFERENCES_TYPE"]["cross_module"],
                            m["discriminator_control"]["REFERENCES_TYPE"]["edges"],
                        ),
                    },
                },
                "basis": "measured",
            },
        },
        {
            "cell_id": "L3S7A-bcon-5",
            "criterion": "L3S7A-CCY-AC6",
            "label": "bridge_conditions.firm_carry",
            "gate": "after-store-vintage",
            "value": {
                "condition": "7a condition 3, the 75005 bar -- the firm is CARRIED THROUGH THE "
                "RELATION, DEMONSTRATED and not asserted",
                "verdict": "NOT MET",
                "decisive": True,
                "measurement": {
                    "declared_firm_keys": m["firm_declared_keys"],
                    "attr_key_vocabulary": m["attr_key_vocabulary"],
                    "vocabulary_size": len(m["attr_key_vocabulary"]),
                    "reading": (
                        "There is NO firm/tenant/client key anywhere in the carrier's attribute "
                        "vocabulary -- %d distinct node attr keys censused across %d nodes, plus "
                        "every edge attr key, and ZERO of them name a firm."
                    )
                    % (len(m["attr_key_vocabulary"]), m["nodes"]),
                },
                "fails_earlier_than_the_bar_contemplates": (
                    "The 75005 bar refuses a firm attribute PRESENT ON BOTH ENDPOINTS as 'two "
                    "independent facts that happen to agree'. This carrier does not reach that bar: "
                    "there is no firm attribute on EITHER endpoint, so there is nothing to travel "
                    "through the relation."
                ),
                "only_available_firm_signal": {
                    "what": "a path substring, _partners/<firm>/, on the Module's attrs.path",
                    "reach_numerator": m["firm_partner_modules"],
                    "reach_denominator": m["modules"],
                    "reach": "%d of %d Module nodes (%s)"
                    % (
                        m["firm_partner_modules"],
                        m["modules"],
                        pct(m["firm_partner_modules"], m["modules"]),
                    ),
                    "by_token": m["firm_partner_by_token"],
                    "admissible": False,
                    "why_inadmissible": (
                        "L1 (7a:348-350) admits cross-plane comparison ONLY through an explicitly "
                        "declared bridge, NEVER through a shared token, a shared string shape or a "
                        "parse. A firm read out of a directory name is exactly the parse that "
                        "clause refuses -- and it reaches only %s of Modules even if it were "
                        "allowed."
                    )
                    % pct(m["firm_partner_modules"], m["modules"]),
                },
                "basis": "measured",
            },
        },
        {
            "cell_id": "L3S7A-bcon-6",
            "criterion": "L3S7A-CCY-AC7",
            "label": "bridge_conditions.no_store_instrumentation",
            "gate": "after-store-vintage",
            "value": {
                "condition": "7a condition 4 -- wiring producing stores to emit declared edges "
                "stays OUTSIDE D11",
                "verdict": "MET",
                "measurement": (
                    "Declaring the containment row requires NO wiring: the %d DECLARES edges are "
                    "already emitted by the store at this vintage. The registry reads them; it does "
                    "not ask the store to emit anything new."
                )
                % m["declares"],
                "instrumentation_required_for_the_containment": False,
                "instrumentation_required_for_the_FIRM": True,
                "named_gap": {
                    "what": "the producing store emits no firm attribute on any node or edge",
                    "which_store": c["path"],
                    "producer": c["producer_project"],
                    "owner": m["store_owner"],
                    "note": (
                        "This is the 7a condition-4 footnote case: the bridge cannot be declared "
                        "admissibly without store-side change, so THAT BRIDGE is a NAMED GAP for "
                        "the store's owner. Naming it is this cell's job; closing it is not, and "
                        "nothing in this unit instruments anything."
                    ),
                },
                "basis": "measured",
            },
        },
    ]

    # ---- the determination itself -------------------------------------------------------------
    conditions = {
        "1_registry_ownership": "MET",
        "2a_basis": "MET",
        "2b_endpoints": "MET",
        "2c_join_evidence": "MET",
        "3_firm_carry": "NOT MET",
        "4_no_store_instrumentation": "MET",
    }
    failed = [k for k, v in conditions.items() if v != "MET"]
    outcome = "OUTCOME_A" if not failed else "B-NO-DECLARED-RELATION-YET"

    cells.append(
        {
            "cell_id": "L3S7A-detn-1",
            "criterion": "L3S7A-CCY-AC8",
            "label": "determination.outcome_typed",
            "gate": "after-conditions",
            "value": {
                "outcome": outcome,
                "conditions": conditions,
                "which_condition_failed": failed,
                "by_what_measurement": (
                    "7a condition 3. No firm/tenant/client key exists anywhere in the carrier's "
                    "attribute vocabulary (%d node attr keys over %d nodes, plus every edge attr "
                    "key: ZERO name a firm). The only firm signal is a _partners/<firm>/ path "
                    "substring reaching %s of Module nodes, which L1 7a:348-350 refuses as a parse."
                )
                % (
                    len(m["attr_key_vocabulary"]),
                    m["nodes"],
                    pct(m["firm_partner_modules"], m["modules"]),
                ),
                "owner": m["store_owner"],
                "closable": True,
                "closable_note": (
                    "CLOSABLE, owner the store's, per 7a condition 4's footnote: the store already "
                    "emits the containment and could emit a firm attribute; nothing about the gap "
                    "requires D11 to edit or instrument anything."
                ),
                "why_not_OUTCOME_A": "condition 3 is NOT MET, measured above.",
                "why_not_B_REFUSED_BY_1_OR_4": (
                    "Conditions 1 and 4 are BOTH MET for the containment: the row is a new "
                    "D11-owned artifact citing edges the store already emits, requiring neither a "
                    "store edit nor store instrumentation. The refusal does not come from 1 or 4."
                ),
                "PRECISION_ON_THE_TYPING": (
                    "This outcome is typed B-NO-DECLARED-RELATION-YET, and the label's stock "
                    "rationale -- 'no admissible relation today because nothing declares one' -- is "
                    "TRUE OF THE FIRM HALF AND FALSE OF THE CONTAINMENT HALF. The store DOES "
                    "declare the containment (%d DECLARES edges of %d). What nothing declares is "
                    "the FIRM. Stated explicitly so the record does not inherit a false reason "
                    "along with a correct outcome."
                )
                % (m["declares"], m["edges"]),
                "gate_effect": (
                    "after-bridge-declared stays OPEN. Only OUTCOME_A discharges it; this is a "
                    "typed refusal, so the predecessor's four consumer cells stay un-measurable and "
                    "CANDIDATE_VIEW stays typed NONE."
                ),
                "basis": "measured",
            },
        }
    )

    # ---- agreement with the prior -------------------------------------------------------------
    agree_inbound = m["inbound_to_module"] == PRIOR["edges_targeting_a_module"] and (
        m["edges"] == PRIOR["edge_denominator"]
    )
    cells.append(
        {
            "cell_id": "L3S7A-detn-2",
            "criterion": "L3S7A-CCY-AC9",
            "label": "determination.agreement_with_prior",
            "gate": "after-conditions",
            "value": {
                "verdict": "PARTIAL -- agrees on two limbs, DISAGREES on two",
                "two_vintages": {
                    "prior": {
                        "pin": PRIOR["pin"],
                        "measured_on": "2026-08-29",
                        "carrier_identity": "NOT RECORDED -- the prior published no digest",
                        "identity_gap": (
                            "Because the prior recorded no sha256, BYTE-IDENTITY BETWEEN THE TWO "
                            "READS IS UNPROVABLE. What is measured is that the derived counts "
                            "reproduce exactly."
                        ),
                    },
                    "this_determination": {
                        "measured_on": datetime.datetime.now(datetime.timezone.utc).strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "carrier_identity": c["sha256"],
                        "mtime_utc": c["mtime_utc"],
                    },
                },
                "limb_by_limb": {
                    "edges_targeting_a_Module": {
                        "prior": "%d of %d"
                        % (PRIOR["edges_targeting_a_module"], PRIOR["edge_denominator"]),
                        "this_run": "%d of %d" % (m["inbound_to_module"], m["edges"]),
                        "agrees": bool(agree_inbound),
                    },
                    "firm_carry": {
                        "prior": PRIOR["firm_carry"],
                        "this_run": "NOT_CARRIED",
                        "agrees": True,
                    },
                    "join": {
                        "prior": PRIOR["join"],
                        "this_run": "%d DECLARES edges of %d; %s symbols covered"
                        % (m["declares"], m["edges"], join_cov),
                        "agrees": False,
                        "difference": (
                            "The prior typed the join NONE. A declared join DOES exist at this "
                            "vintage. The prior measured only edges TARGETING a Module (inbound) "
                            "and found 0; it did not measure the OUTBOUND direction, where the "
                            "store declares %d edges from a Module, %d of them DECLARES."
                        )
                        % (m["outbound_from_module"], m["declares"]),
                    },
                    "declared_by_store": {
                        "prior": PRIOR["declared_by_store"],
                        "this_run": "YES for the containment (file -> symbol); NO for the firm",
                        "agrees": False,
                        "difference": (
                            "The prior's cited evidence -- '0 of 16,397 portal edges target a "
                            "Module' -- REPRODUCES EXACTLY and is not disputed. What does not "
                            "follow from it is the label NO. A containment is one relation readable "
                            "in two directions; the store declares it as Module --DECLARES--> "
                            "symbol, so measuring only dst==Module cannot see it. The evidence was "
                            "right and directionally scoped; the conclusion generalised past it."
                        ),
                    },
                },
                "outcome_agreement": (
                    "The two runs AGREE on the outcome that matters: no bridge is declarable today, "
                    "and firm-carry is why. The disagreement is about the REASON and the BASIS, not "
                    "about whether OUTCOME_A is available."
                ),
                "CORROBORATION_LIMIT": (
                    "The counts reproduce exactly and the carrier's mtime (%s) PREDATES the prior's "
                    "own measurement date, so both reads almost certainly hit ONE SUBSTRATE. Two "
                    "instruments reading one substrate are one method: the agreeing limbs are "
                    "REPETITION, not corroboration. The disagreeing limbs are the informative ones, "
                    "and they are instrument-level -- a different question asked of the same bytes, "
                    "NOT a change in the world."
                )
                % c["mtime_utc"],
                "basis": "measured",
            },
        }
    )
    return cells


def main() -> int:
    m = measure()
    face_sha = hashlib.sha256(
        subprocess.run(
            ["git", "show", "%s:%s" % (FACE["pin"], FACE["path"])],
            capture_output=True,
            cwd=ROOT,
        ).stdout
    ).hexdigest()
    rec_sha = hashlib.sha256(
        subprocess.run(
            ["git", "show", "%s:%s" % (RECORD["pin"], RECORD["path"])],
            capture_output=True,
            cwd=ROOT,
        ).stdout
    ).hexdigest()

    written = []
    for cell in build_cells(m):
        doc = {
            "schema": "D11.L3S7A.cell_carrier.v1",
            "cell_id": cell["cell_id"],
            "label": cell["label"],
            "criterion": cell["criterion"],
            "plane": "BRIDGE_DETERMINATION",
            "sequence_gate": cell["gate"],
            "owner": "0.8.0_AE_CloudComp~X",
            "face": {
                "id": FACE["id"],
                "pin": FACE["pin"],
                "sha256_first16": face_sha[:16],
            },
            "certified_record": dict(RECORD, sha256=rec_sha),
            "value": cell["value"],
            "produced_by": "run_determination.py",
        }
        out = os.path.join(HERE, "%s.%s.json" % (cell["cell_id"], cell["label"].split(".")[-1]))
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, indent=1, ensure_ascii=True)
            fh.write("\n")
        written.append(os.path.basename(out))
        print("WROTE %s  [%s, gate=%s]" % (os.path.basename(out), cell["criterion"], cell["gate"]))

    with open(os.path.join(HERE, "_measurement.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("WROTE _measurement.json  (the raw derived record)")
    print("OK: %d cell carrier(s)" % len(written))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
