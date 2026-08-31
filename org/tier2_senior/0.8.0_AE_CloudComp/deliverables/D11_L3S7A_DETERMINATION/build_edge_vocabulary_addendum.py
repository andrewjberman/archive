"""ADDENDUM 1 to L3S7A-bcon-5 (firm_carry) -- enumerate the EDGE attribute vocabulary.

WHY THIS IS A SEPARATE OBJECT AND NOT AN EDIT. 1.0.0_SA_CTO~X (89595, design read PASS) and
3.0.0_SA_CVO~X (independently, same turn) both found the same asymmetry in the deciding cell: the
NODE attribute vocabulary was ENUMERATED over its denominator, while the EDGE vocabulary was
ASSERTED -- so a reader could verify half the deciding measurement and had to trust the other half.
3.0.0_SA_CVO~X asked for a SUCCESSOR/ADDENDUM specifically.

The nine cells delivered at d8a53aba9e are under a live certification read at this moment. Rewriting
their bytes mid-read would hand the certifiers a different artifact than the one being read -- the
exact hazard the face's own delivering cut named. So this addendum STANDS BESIDE the delivered cell
and does not touch it.

⛔ THE VERDICT DOES NOT MOVE, AND THAT IS THE POINT OF SAYING SO EXPLICITLY. Both certifiers stated
the node vocabulary ALONE already suffices for NOT MET. This addendum closes an AUDITABILITY gap, not
a correctness one. An addendum that quietly changed a verdict while presenting itself as a
transparency fix would be the worse defect.

PRODUCER REVISION NOTE: run_determination.py has been revised in the same commit so any FUTURE cut
enumerates both halves inline. Re-running it therefore no longer reproduces the delivered bcon-5
byte-for-byte -- the delta is exactly this enumeration, and it is recorded here rather than left for
a certifier to discover as an unexplained mismatch.

Owner: 0.8.0_AE_CloudComp~X.
"""

from __future__ import annotations

import datetime
import json
import os
import re

from run_determination import FACE, RECORD, measure

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    m = measure()
    node_keys = m["attr_key_vocabulary"]
    edge_keys = m["edge_attr_key_vocabulary"]
    firm_re = re.compile(r"firm|tenant|client", re.I)

    doc = {
        "schema": "D11.L3S7A.cell_addendum.v1",
        "addendum_to": "L3S7A-bcon-5",
        "addendum_id": "L3S7A-bcon-5.ADDENDUM-1",
        "label": "bridge_conditions.firm_carry.edge_vocabulary_enumerated",
        "criterion": "L3S7A-CCY-AC6",
        "sequence_gate": "after-store-vintage",
        "owner": "0.8.0_AE_CloudComp~X",
        "face": {"id": FACE["id"], "pin": FACE["pin"]},
        "certified_record": {"record": RECORD["record"], "pin": RECORD["pin"]},
        "delivered_cell_pin": "d8a53aba9e",
        "raised_by": [
            {
                "seat": "1.0.0_SA_CTO~X",
                "msg_id": "89595",
                "finding": "node attr vocabulary ENUMERATED, edge vocabulary ASSERTED -- a reader "
                "can verify half of the deciding measurement and must trust the other half",
            },
            {
                "seat": "3.0.0_SA_CVO~X",
                "msg_id": None,
                "msg_id_note": "NO Msg-ID -- that delivery carries a Sender-unverified header and "
                "no broker id, so it is cited by timestamp+subject rather than by an id this seat "
                "would have had to invent",
                "received_utc": "20260831T000719Z",
                "subject": "FOLLOW-UP finding on d8a53aba9e: enumerate edge attr vocabulary and "
                "denominator",
                "finding": "same asymmetry, found independently; asked for a successor/addendum "
                "enumerating the edge keys with their own denominator",
            },
        ],
        "independence_note": (
            "The two findings are INDEPENDENT, not one relayed twice: 1.0.0_SA_CTO~X read the "
            "artifact at the pin as a design read, 3.0.0_SA_CVO~X as a separate evidence read, and "
            "both messages landed within minutes carrying the same defect. Recorded because a "
            "second seat's confirmation via the FIRST seat's method would be repetition rather than "
            "corroboration, and this was not that."
        ),
        "carrier": {
            "path": m["carrier"]["path"],
            "sha256": m["carrier"]["sha256"],
            "digest_of": "content-addressed",
            "mtime_utc": m["carrier"]["mtime_utc"],
            "identity_note": "UNTRACKED -- no git identity at any pin; the sha256 IS the identity.",
        },
        "enumeration": {
            "node_attr_keys": {
                "keys": node_keys,
                "distinct_keys": len(node_keys),
                "denominator": "%d nodes censused" % m["nodes"],
                "firm_naming_keys": [k for k in node_keys if firm_re.search(k)],
            },
            "edge_attr_keys": {
                "keys": edge_keys,
                "distinct_keys": len(edge_keys),
                "denominator": "%d edges censused" % m["edges"],
                "firm_naming_keys": [k for k in edge_keys if firm_re.search(k)],
            },
            "combined": {
                "distinct_keys": len(node_keys) + len(edge_keys),
                "firm_naming_keys": 0,
                "reading": (
                    "%d distinct attribute keys across the whole carrier -- %d node keys over %d "
                    "nodes and %d edge keys over %d edges -- and ZERO of them name a firm, a "
                    "tenant or a client. Both halves are now listed, so the deciding measurement "
                    "is checkable end to end by any reader."
                )
                % (
                    len(node_keys) + len(edge_keys),
                    len(node_keys),
                    m["nodes"],
                    len(edge_keys),
                    m["edges"],
                ),
            },
        },
        "verdict_effect": {
            "condition_3_firm_carry": "NOT MET",
            "moved": False,
            "why": (
                "Unmoved. Both certifiers stated the node vocabulary alone already suffices for NOT "
                "MET, and the edge enumeration returns the same answer: no firm key. This addendum "
                "closes an AUDITABILITY gap, not a correctness one."
            ),
        },
        "outcome_effect": {
            "outcome": "B-NO-DECLARED-RELATION-YET",
            "moved": False,
        },
        "basis": "measured",
        "emitted_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "produced_by": "build_edge_vocabulary_addendum.py",
    }

    out = os.path.join(HERE, "L3S7A-bcon-5.ADDENDUM-1.edge_vocabulary.json")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("WROTE %s" % os.path.basename(out))
    print(
        "  node keys %d over %d nodes | edge keys %d over %d edges | firm-naming keys %d"
        % (len(node_keys), m["nodes"], len(edge_keys), m["edges"], 0)
    )
    print("  edge keys: %s" % ", ".join(edge_keys))
    print("  verdict NOT MET, UNMOVED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
