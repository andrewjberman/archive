#!/usr/bin/env python3
"""TO-L1-DTX deliverable: the 29 lane cells, each with status / value / basis / evidence / owner.

AC1: no cell ships UNMEASURED without a stated reason IN ITS OWN ROW.

⛔ THE CELL IDS ARE READ FROM THE DECOMP RECTANGLE, NEVER TYPED. A hand-typed cell list beside a
generated rectangle is this session's most-repeated defect, and the one this lane ruled on twice.
The builder REFUSES to emit if the id set it produces does not equal the rectangle's lane set.
"""
from __future__ import annotations

import json
import os
import subprocess

WS = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                    capture_output=True, text=True, check=True).stdout.strip()
RECT = os.path.join(WS, "workflows/atom_decomposition/runs/nfra-c3materialize-L1/rectangle.c0.json")
OUT = os.path.join(WS, "org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_L1/L1_CELLS.json")
ME = "0.4.0_DT_ClientPlatform~X"
PIN = "4226a09f74"

# Evidence commits, so every row points at a reproducible probe rather than at prose.
E_CROSS = "probe_symbol_crossing.py + probe_file_crossing.py @38d60dc"
E_CENS = "probe_population_census.py @baca7f07eb, corrected @31b1978428"
E_ROLL = "probe_rollup_cardinality.py @16cd74c870"
E_GATE = "probe_discrimination_gate.py @68cd2f273e"
E_457 = "probe_rows_4_5_7.py @af072a8dc6"

UNMEASURED_SCOPE = ("UNMEASURED, NOT LOW -- the space carries no field a consumer can reject on, so "
                    "out-of-scope and genuinely-absent are indistinguishable. Reason stated per AC1.")

# ---- per-space row values ------------------------------------------------------------
SPACE = {
    "symbol": {
        "token": "gqhb",
        1: ("CROSSES ONLY VIA A HAND-WRITTEN PARSE", "measured",
            "raw join 0 of 2,249 trace-graph ids against kuzu pipeline node_ids; 1,331 (59.2%) after "
            "stripping 'pipeline:<firm>:' (firms bd/inf/mdpf). NEG CONTROL 0 of 1,851 ARNs match the "
            "parse; POS CONTROL the parse yields 1,335 ids. The strip DISCARDS the firm, so the join "
            "is lossy in reverse -- the token 'gold' resolves to 3 firm-qualified nodes. " + E_CROSS),
        2: ("MULTI-SUBSTRATE, UNION 14,447 distinct", "measured",
            "trace-graph 2,249 + kuzu portal non-Module 10,964 + kuzu pipeline 1,337; pairwise "
            "overlaps 103/0/0. PRD-claimed 19,482 matches NO substrate swept and EXCEEDS the union, "
            "so its provenance is UNRESOLVED and is not guessed here. " + E_CENS),
        3: ("RELATION, not a function: 10,265 symbols -> 284 files", "measured",
            "fan-in max 1,290, mean 36.14. DECLARED BY THE STORE? NO -- 0 of 16,811 portal-source "
            "edges target a Module across 20 edge types, so the roll-up is parse-only. Instrument "
            "limit: fan-out=1 is a TAUTOLOGY of the parse, not a property of the estate. " + E_ROLL),
        4: ("UNMEASURED", "absent",
            UNMEASURED_SCOPE + " Missing discriminator: trace ids carry no firm token and no "
            "coverage marker; 918 of 2,249 non-resolving are un-attributable. " + E_457),
        5: ("ABSENT -- no confidence value exists", "measured",
            "structured key scan over the full files returns 0 confidence-ish KEYS. Recorded ABSENT "
            "rather than 1.0: a parse that happens to succeed is unquantified, not confident. " + E_457),
        6: ("NO -- cannot discriminate", "measured",
            "918 of 2,249 non-resolving. The pipeline layer covers firms bd/inf/mdpf and 0 of 2,249 "
            "trace ids carry a firm token, so 'that firm is not loaded' and 'this symbol has no "
            "pipeline node' are indistinguishable. NO field to reject on. " + E_GATE),
        7: ("SILENT", "measured",
            "the parse yields no match, nothing raises, nothing is counted; the fused result is "
            "smaller by an unrecorded amount. The PRD's zero-join reproduced. " + E_457),
    },
    "file": {
        "token": "oqif",
        1: ("CROSSES NATIVELY to the filesystem plane", "measured",
            "declared grain node_type='Module' = 374 paths, 373 of which EXIST on disk (99.7%). "
            "Taken from the store's DECLARED type, not a regex -- two earlier pattern-derived "
            "attempts returned 4,978 and 4,933, both 13x over-counts. " + E_CROSS),
        2: ("MULTI-SUBSTRATE, UNION 430 over the PORTAL PLANE ONLY", "measured",
            "kuzu portal Module 374 + portal/src filesystem 429, shared 373. ⛔ THE PRD'S 3,532 IS "
            "THE CO-CHANGE CORPUS -- a substrate neither of these is. Reporting 374 as the file "
            "population would be a well-formed answer about the wrong object. " + E_CENS),
        3: ("RELATION -- it is the TARGET of symbol->file", "measured",
            "receives 10,265 symbols across 284 files, fan-in max 1,290. See symbol row 3. " + E_ROLL),
        4: ("MEASURED -- graph->disk 373 of 374 (99.7%); disk->graph 373 of 429 (86.9%)", "measured",
            "BOTH DIRECTIONS REPORTED. One alone is a half-truth: a reader given only 99.7% would "
            "conclude the graph covers the tree, and it covers 87% of it. The only space with an "
            "oracle OUTSIDE its own producer. " + E_457),
        5: ("ABSENT -- no confidence value exists", "measured", "as symbol row 5. " + E_457),
        6: ("YES -- discriminates", "measured",
            "the filesystem is a live oracle on a DIFFERENT PLANE from the producer. Both arms "
            "non-empty and reachable from different truths: 1 Module path absent from disk, 56 repo "
            "files absent from the graph. The only one of the four that passes. " + E_GATE),
        7: ("DETECTABLE, but only by leaving the graph", "measured",
            "os.path.exists answers definitively; nothing IN the graph says a path is stale. " + E_457),
    },
    "arn_resource": {
        "token": "vuot",
        1: ("CROSSES NATIVELY", "measured",
            "kuzu_nessie_db 1,851 distinct ARNs vs stitch_graph.json 1,811, shared 1,692 -- two "
            "artifacts, two producers, no parse required. " + E_CROSS),
        2: ("1,851 in kuzu; union with stitch NOT a population fact", "measured",
            "PRD-claimed 1,851 EQUALS the kuzu count EXACTLY -- reported as an instrument result, "
            "never as agreement. ⛔ The union figure 1,970 is UNMEASURED, not a population delta: "
            "neither store records its scan scope. Retracted at " + E_CENS),
        3: ("RELATION: 1,851 ARNs -> 22 services", "measured",
            "fan-in max 678 (service:iam), mean 84.14. DECLARED? NO -- parsed from the ARN string. " + E_ROLL),
        4: ("UNMEASURED", "absent",
            UNMEASURED_SCOPE + " Missing discriminator: neither store records SCAN SCOPE; 278 of "
            "1,970 non-resolving are un-attributable between out-of-scope and deleted. " + E_457),
        5: ("ABSENT -- no confidence value exists", "measured",
            "stitch carries 43 distinct edge keys over 43,633 edges, none a confidence. " + E_457),
        6: ("NO -- cannot discriminate", "measured",
            "159 ARNs only in kuzu, 119 only in stitch. Neither store records its scan scope, so "
            "out-of-scope and genuinely-deleted are byte-identical to a consumer. " + E_GATE),
        7: ("SILENT", "measured",
            "a set difference with no scan scope; neither store errors and the consumer cannot tell "
            "a deleted resource from an unswept one. " + E_457),
    },
    "chain_motif": {
        "token": "bffm",
        1: ("CROSSES NATIVELY at INSTANCE grain", "measured",
            "c2_instances.json 6,138 instance ids vs kuzu semctl 6,207, shared 6,090. Family grain "
            "19/19. CROSS-GRAIN intersection 0, and the control confirms it. ⛔ An earlier figure of "
            "6,113 MIXED the two grains and is withdrawn. " + E_CROSS),
        2: ("MULTI-SUBSTRATE, UNION 6,255 -- but the delta is NOT a population fact", "measured",
            "PRD-claimed 6,207 EQUALS the kuzu semctl INSTANCE count EXACTLY. c2 carries 6,138. ⛔ The "
            "+48 is 19.5 DAYS OF GRAPH DRIFT, not population: c2 declares graph_vintage "
            "8601547680771488785 @2026-08-07 against kuzu 2902399899597701830 @2026-08-26. " + E_CENS),
        3: ("RELATION: 6,207 instances -> 13 families", "measured",
            "fan-in max 1,649 (motif:a-grant), mean 477.46. PARTIALLY declared -- the 19 family ids "
            "exist as nodes in the same store. " + E_ROLL),
        4: ("UNMEASURED for scope; staleness measurable", "inferred",
            "graph_vintage discriminates ONE axis (the 19.5-day gap, measured). Scope is undeclared, "
            "so a coverage ratio would mix drift with scope and name the result coverage. " + E_457),
        5: ("ABSENT -- no confidence value exists", "measured",
            "c2_instances.json structured key scan returns 0. " + E_457),
        6: ("PARTIALLY -- one axis only", "measured",
            "165 of 6,255 non-resolving. graph_vintage tells STALE from ABSENT; it does NOT tell "
            "scope-absent from genuinely-unaddressed. A VINTAGE IS NOT A COVERAGE MARKER. " + E_GATE),
        7: ("SILENT ON SCOPE, WARNS ON VINTAGE", "measured",
            "the only in-band warning in any of the four spaces -- and I did not read it on my first "
            "pass, which measures how easy it is to miss. " + E_457),
    },
}

ROW_FIELDS = ["space_is_crossing", "population_census", "roll_up_to_canonical", "coverage",
              "confidence_distribution", "absent_vs_unaddressed", "failure_mode_downstream"]


def main() -> None:
    rect = json.load(open(RECT, encoding="utf-8"))
    lane_ids = {c["cell_id"] for c in rect["cells"] if c.get("executor_class") == ME}

    cells = []
    for space, spec in SPACE.items():
        tok = spec["token"]
        for i, field in enumerate(ROW_FIELDS, start=1):
            value, basis, evidence = spec[i]
            cells.append({
                "cell_id": "L1-%s-%d" % (tok, i),
                "entity": space,
                "field": field,
                "status": "MEASURED" if basis == "measured" else "UNMEASURED",
                "value": value,
                "basis": basis,
                "evidence": evidence,
                "owner": ME,
            })

    cells.append({
        "cell_id": "L1-m-graindecl",
        "entity": "NFRA_C3MATERIALIZE-L1",
        "field": "graindecl",
        "status": "MEASURED",
        "value": "The canonical grain is the ordered pair (PLANE, ENTITY) -- four grains plus a "
                 "declared-bridge obligation, not one universal entity type.",
        "basis": "measured",
        "evidence": "L1_CANONICAL_GRAIN_DECLARATION.md @16cd74c870, amended @55c6293bd0. Four "
                    "runnable refutations stated. FALSIFIER 1 RUN BY 3.0.0_SA_CVO~X (msg 75044) and "
                    "FAILED TO REFUTE: the one declared cross-plane candidate (stitch CONTAINS "
                    "x12,352) is partial at every plane (ARN 59.5%), many-to-many (a cover, not a "
                    "roll-up), and membership-semantics rather than identity. Falsifiers 2-4 OPEN.",
        "owner": ME,
    })

    produced = {c["cell_id"] for c in cells}
    # ⛔ REFUSE TO EMIT ON ANY DISAGREEMENT WITH THE RECTANGLE.
    if produced != lane_ids:
        raise SystemExit("REFUSING TO EMIT -- cell id set != rectangle lane set.\n"
                         "  missing from mine : %s\n  extra in mine     : %s"
                         % (sorted(lane_ids - produced), sorted(produced - lane_ids)))

    unmeasured_no_reason = [c["cell_id"] for c in cells
                            if c["status"] == "UNMEASURED" and len(c["evidence"]) < 40]
    if unmeasured_no_reason:
        raise SystemExit("REFUSING TO EMIT -- UNMEASURED cells with no stated reason (AC1): %s"
                         % unmeasured_no_reason)

    doc = {
        "to_id": "NFRA_C3MATERIALIZE.TO-L1-DTX",
        "decomp_pin": PIN,
        "produced_by": ME,
        "cell_count": len(cells),
        "cells": sorted(cells, key=lambda c: c["cell_id"]),
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=True)
        f.write("\n")

    from collections import Counter
    print("cells emitted            : %d" % len(cells))
    print("rectangle lane cells     : %d" % len(lane_ids))
    print("id sets identical        : %s" % (produced == lane_ids))
    print("status distribution      : %s" % dict(Counter(c["status"] for c in cells)))
    print("basis distribution       : %s" % dict(Counter(c["basis"] for c in cells)))
    print("UNMEASURED without reason: %d  (AC1 requires 0)" % len(unmeasured_no_reason))
    print("OK: wrote %s" % os.path.relpath(OUT, WS).replace("\\", "/"))


if __name__ == "__main__":
    main()
