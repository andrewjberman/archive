#!/usr/bin/env python3
"""NFRA_CLDGRPH CG-s-32 (TO-CG-G-1) -- shared reads for the boundary-edge class census.

READ ONLY. Every read goes through the estate's projection client, which is the ONLY
way a laptop seat reaches the served graph (projection_client.py module docstring).
Nothing here opens, names or reads a local store, writes to S3, or runs a producer.

THE POPULATION THIS MODULE DEFINES, stated before it is counted:

  A node class is a BOTH-IDENTITY class when at least one of its nodes carries TWO
  usable identity strings for one resource -- an ARN-shaped primary key (node_id
  starting 'arn:') AND a distinct non-empty `name`. Either string can be typed into
  an edge endpoint by a builder; only one of them is the graph's key.

  QUALIFIER ON THE INSTRUMENT (measured, not assumed): the served CloudNode table has
  an `arn` COLUMN, and it is a copy of `node_id` on every node that has one -- 0 of
  27,665 nodes have arn <> node_id. So the `arn` column is NOT the discriminator; the
  SHAPE of node_id plus the presence of a distinct `name` is. `_arn_column_control()`
  measures that rather than trusting this sentence.

  A SHADOW ID is a node_id that IS the `name` of a both-identity node while belonging
  to a class that is NOT a both-identity class. An edge built onto the second identity
  of a two-named resource lands on the shadow node instead of the resource.
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT / "infra" / "aws" / "globgrph"))

import projection_client as pc  # noqa: E402

QUERY_TIMEOUT_S = 90.0

INSTRUMENT = ("projection_client.query -> POST <base_url>/graph/cypher "
              "(the SERVED graph; no local store is opened, named or read)")


def served_vintage():
    """The SERVICE's own vintage line. Never a client clock, never a file mtime."""
    h = pc.health(timeout_s=30.0)
    return h.get("vintage"), pc.vintage_line(h)


def q(statement):
    return pc.query(statement, timeout_s=QUERY_TIMEOUT_S)["rows"]


def _i(v):
    """Kuzu INT64 arrives as a JSON string through the service. Coerce once, here."""
    return int(v)


def fetch_nodes():
    """Every node in the served graph: id, class, name, arn column. No sampling."""
    rows = q("MATCH (n:CloudNode) RETURN n.node_id AS i, n.node_type AS t, "
             "n.name AS nm, n.arn AS ar")
    return [{"id": r["i"] or "", "type": r["t"] or "", "name": r["nm"] or "",
             "arn": r["ar"] or ""} for r in rows]


def arn_column_control(nodes):
    """Measured falsifier for 'the arn column is a copy of node_id'.

    Returns (mismatches, denominator). A non-zero left value would mean the column IS
    a second identity and this census picked the wrong discriminator.
    """
    bad = sum(1 for n in nodes if n["arn"] and n["arn"] != n["id"])
    return bad, len(nodes)


def class_identity_census(nodes):
    """Per node class: totals, both-identity count, and which field the graph keys on."""
    per = collections.OrderedDict()
    for n in sorted(nodes, key=lambda x: x["type"]):
        c = per.setdefault(n["type"], {"total": 0, "both": 0,
                                       "keyed_on": collections.Counter(),
                                       "alt_names": set()})
        c["total"] += 1
        is_arn_key = n["id"].startswith("arn:")
        has_alt = bool(n["name"]) and n["name"] != n["id"]
        if is_arn_key:
            c["keyed_on"]["ARN"] += 1
        elif n["name"] and n["name"] == n["id"]:
            c["keyed_on"]["NAME"] += 1
        else:
            c["keyed_on"]["OTHER"] += 1
        if is_arn_key and has_alt:
            c["both"] += 1
            c["alt_names"].add(n["name"])
    return per


def population(nodes):
    """(both_identity_classes, alt_names, shadow_ids) -- the census population."""
    per = class_identity_census(nodes)
    pop = {c for c, v in per.items() if v["both"] > 0}
    alt = set()
    for c in pop:
        alt |= per[c]["alt_names"]
    shadow = {n["id"]: n["type"] for n in nodes if n["id"] in alt and n["type"] not in pop}
    return per, pop, alt, shadow


def edge_crosstab():
    """(edge_type, source class, target class) -> edge count. The full family shape."""
    rows = q("MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) "
             "RETURN e.edge_type AS et, a.node_type AS st, b.node_type AS tt, count(*) AS c")
    out = collections.OrderedDict()
    for r in sorted(rows, key=lambda x: (x["et"], x["st"], x["tt"])):
        out.setdefault(r["et"], []).append((r["st"], r["tt"], _i(r["c"])))
    return out


def edge_endpoint_counts(side):
    """(edge_type, endpoint node_id) -> count, for side 'source' or 'target'."""
    var = "a" if side == "source" else "b"
    rows = q("MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) "
             "RETURN e.edge_type AS et, %s.node_id AS nid, count(*) AS c" % var)
    out = collections.defaultdict(dict)
    for r in rows:
        out[r["et"]][r["nid"] or ""] = _i(r["c"])
    return out


def classify_families(cross, src_counts, tgt_counts, pop, shadow):
    """Every family in the served graph, INCLUDED or EXCLUDED, each with its reason.

    LIMB A (CLASS): an endpoint class is a both-identity class -- the edge points at,
      or leaves from, a resource that carries two identity strings.
    LIMB B (NAME-ADDRESSED): an endpoint node_id is a SHADOW ID -- the edge was built
      onto the second identity of a two-named resource and landed on whatever else is
      keyed by that string. This limb is why the family the round inherits is not
      silently dropped: STORED_IN's served target class is S3_BUCKET_POLICY, which is
      NOT a both-identity class, so LIMB A alone would exclude the very family the
      census exists to measure.
    """
    out = collections.OrderedDict()
    for fam in sorted(cross):
        s_classes = sorted({t[0] for t in cross[fam]})
        t_classes = sorted({t[1] for t in cross[fam]})
        a_src = [c for c in s_classes if c in pop]
        a_tgt = [c for c in t_classes if c in pop]
        b_src = sorted({shadow[i] for i in src_counts.get(fam, {}) if i in shadow})
        b_tgt = sorted({shadow[i] for i in tgt_counts.get(fam, {}) if i in shadow})
        limbs = []
        if a_tgt:
            limbs.append("LIMB-A target class(es) %s carry both an ARN key and a name"
                         % ",".join(a_tgt))
        if a_src:
            limbs.append("LIMB-A source class(es) %s carry both an ARN key and a name"
                         % ",".join(a_src))
        if b_tgt:
            limbs.append("LIMB-B target is NAME-ADDRESSED onto a both-identity resource "
                         "and lands on %s" % ",".join(b_tgt))
        if b_src:
            limbs.append("LIMB-B source is NAME-ADDRESSED onto a both-identity resource "
                         "and lands on %s" % ",".join(b_src))
        if limbs:
            out[fam] = ("INCLUDED", "; ".join(limbs))
        else:
            out[fam] = ("EXCLUDED",
                        "no endpoint carries two identities: source class(es) %s and "
                        "target class(es) %s are all single-identity, and no endpoint "
                        "node_id is a shadow id"
                        % (",".join(s_classes), ",".join(t_classes)))
    return out


def facts_per_key(fam, cross, src_counts):
    """A family read as N facts over K keys -- never as N successes.

    keys = distinct SOURCE node_id (the denominator), edges = total edges,
    dist = {edges-on-one-key: how many keys}, by_type = {resolved target class: edges}.
    """
    per_key = src_counts.get(fam, {})
    keys = len(per_key)
    edges = sum(per_key.values())
    dist = dict(sorted(collections.Counter(per_key.values()).items()))
    by_type = collections.Counter()
    for st, tt, c in cross.get(fam, []):
        by_type[tt] += c
    return {"keys": keys, "edges": edges, "dist": dist,
            "by_type": dict(sorted(by_type.items()))}


def fmt_facts(fam, f):
    return ("%s: keys=%d edges=%d dist=%s by_type=%s facts_per_key=%s"
            % (fam, f["keys"], f["edges"], _flat(f["dist"]), _flat(f["by_type"]),
               ("%.2f" % (float(f["edges"]) / f["keys"])) if f["keys"] else "n/a"))


def _flat(d):
    """A one-level map rendered with NO nested brace -- the census reads it back."""
    if not d:
        return "{}"
    return "{" + ", ".join("%s: %s" % (json.dumps(k) if isinstance(k, str) else k, v)
                           for k, v in d.items()) + "}"


def edges_only_detector(lines):
    """Count report lines that state an edge count with NO key denominator beside it.

    The arm that makes the binding condition falsifiable: it CAN return non-zero, and
    `edges_only_detector_control()` proves it does on a planted positive.
    """
    bad = []
    for ln in lines:
        low = ln.lower()
        if "edges=" in low and "keys=" not in low:
            bad.append(ln)
    return bad


def edges_only_detector_control():
    """Positive control: the detector must return 1 on a planted bare edge count."""
    planted = ["STORED_IN resolved edges=135"]
    return len(edges_only_detector(planted))


def disclosure(grain):
    return [
        "INSTRUMENT: %s" % INSTRUMENT,
        "COVERAGE: the whole served CloudNode/CloudEdge artifact, no sampling and no "
        "LIMIT; every count below prints its denominator",
        "GRAIN: %s" % grain,
        "ENVIRONMENT: the stored baseline this census is compared against is round 6's "
        "CLOSING pair from the drained TO-CG-F-11 instance (F11-AC3), stated by the "
        "issuer at the cut; it is NOT re-derived from the producer here, because this "
        "order runs no producer",
    ]
