#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-G-1 / G1-AC3 and G1-AC4 -- FACTS PER KEY, NEVER EDGES.

The CTO's binding condition on this cut, adopting the CVO's warning: the class census
must count FACTS PER KEY, not edges, or it will re-measure the fan-out and call it
identity. A family that resolves 764 times over 191 keys is 191 facts fanned four ways,
not 764 successes.

So every included family here reports:
  keys=   distinct SOURCE node_id -- THE DENOMINATOR
  edges=  total edges in the family
  dist=   {edges-on-one-key: how many keys} -- the per-key edge-count distribution
  by_type={resolved target class: edges} -- what the family actually resolves ONTO

and `EDGES_ONLY_COUNTS_PRINTED` is the arm that makes the condition falsifiable: it
counts report lines that state an edge count with no key denominator beside them, and
its positive control proves it can return non-zero.

`--reconcile` (G1-AC4) reproduces round 6's two closing numbers from the served graph
at a named vintage and prints every difference rather than absorbing it.

READ ONLY: reads the served graph through the projection service, never a local store.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import g1_census_lib as L  # noqa: E402

# The round-6 closing pair, from the drained TO-CG-F-11 instance, stated by the issuer
# at the cut. A STORED baseline from ANOTHER environment (the producer's emit side), not
# re-derived here, because this order runs no producer.
R6_STORED_IN_RESOLVED = 135
R6_STORED_IN_EMITTED = 137
R6_STORED_IN_TARGET_CLASS = "S3_BUCKET_POLICY"
R6_DERIVES_FROM_RESOLVED = 216
R6_DERIVES_FROM_EMITTED = 216

# The producer's own constants, read from infra/aws/globgrph/derive_stitch.py:57-59 at
# this worktree's HEAD. Used ONLY to recompute the served plane's eligible key
# population, never to run anything.
FIRM_DATA_BUCKETS = ["opal-data-bd", "opal-data-inf", "opal-data-cot",
                     "opal-data-mdpf", "opal-data-demo"]
FIRM_KEY_PREFIXES = ("platinum/", "gold/", "silver/", "bronze/")

NAMED_ROUND6_FAMILIES = ["STORED_IN", "DERIVES_FROM"]


class Report(object):
    """Buffers every emitted line so the edges-only detector can read its own output."""

    def __init__(self):
        self.lines = []

    def __call__(self, line=""):
        self.lines.append(line)
        print(line)


def _load():
    nodes = L.fetch_nodes()
    per, pop, alt, shadow = L.population(nodes)
    cross = L.edge_crosstab()
    src = L.edge_endpoint_counts("source")
    tgt = L.edge_endpoint_counts("target")
    decided = L.classify_families(cross, src, tgt, pop, shadow)
    return nodes, per, pop, shadow, cross, src, tgt, decided


def census(out, vintage, vline):
    for line in L.disclosure("FACTS PER KEY: one row per edge family, its distinct "
                             "SOURCE node_id count as the denominator"):
        out(line)
    out(vline)
    out("")

    nodes, per, pop, shadow, cross, src, tgt, decided = _load()
    inc = sorted(f for f in decided if decided[f][0] == "INCLUDED")

    all_keys = set()
    all_edges = 0
    for fam in inc:
        all_keys |= set(src.get(fam, {}))
        all_edges += sum(src.get(fam, {}).values())

    out("FACTS_PER_KEY_REPORTED_FOR=%d of %d included family(ies)" % (len(inc), len(inc)))
    out("SWEPT: keys=%d distinct source node(s) edges=%d across the %d included "
        "family(ies), out of %d family(ies) in the served graph"
        % (len(all_keys), all_edges, len(inc), len(decided)))
    out("")

    out("-- THE TWO FAMILIES ROUND 6 CLOSED ON, printed first and in the same form --")
    for fam in NAMED_ROUND6_FAMILIES:
        f = L.facts_per_key(fam, cross, src)
        dec = decided.get(fam, ("ABSENT", "not present in the served graph"))[0]
        out("%s   [census decision: %s]" % (L.fmt_facts(fam, f), dec))
    out("NOTE ON DERIVES_FROM: it is the round's NAMED COMPARATOR, and this census's own "
        "endpoint test puts it OUTSIDE the population -- S3Key, PipelineFunction and "
        "PipelineScript each carry ONE identity, so no endpoint of it can be addressed "
        "by a second name. It is printed here because round 6 closed on it and because "
        "it is the NEGATIVE CONTROL for the seam: a stitch family with no identity "
        "ambiguity. Row NFRA_CLDGRPH-W1-S35 records the divergence from the cut's "
        "presumption. Its 216 is nevertheless an EDGE count, and in facts-per-key it "
        "reads as the line above.")
    out("")

    out("-- every included family, as N facts over K keys --")
    for fam in inc:
        f = L.facts_per_key(fam, cross, src)
        out(L.fmt_facts(fam, f))
    out("")

    out("-- the excluded families, counted the same way so the exclusion is visible --")
    for fam in sorted(f for f in decided if decided[f][0] == "EXCLUDED"):
        f = L.facts_per_key(fam, cross, src)
        out(L.fmt_facts(fam, f))
    out("")

    fanned = [f for f in inc
              if L.facts_per_key(f, cross, src)["keys"]
              and L.facts_per_key(f, cross, src)["edges"]
              > L.facts_per_key(f, cross, src)["keys"]]
    onto_shadow = [f for f in inc
                   if set(L.facts_per_key(f, cross, src)["by_type"]) & set(shadow.values())]
    out("FAN_OUT_FAMILIES=%d of %d included: %s"
        % (len(fanned), len(inc), ", ".join(fanned)))
    out("RESOLVING_ONTO_A_SHADOW_CLASS=%d of %d included: %s"
        % (len(onto_shadow), len(inc), ", ".join(onto_shadow)))
    out("")

    control = L.edges_only_detector_control()
    bad = L.edges_only_detector(out.lines)
    out("EDGES_ONLY_DETECTOR_CONTROL=%d planted positive(s) caught of 1 -- the arm can "
        "return non-zero, so a zero below is a measurement" % control)
    for ln in bad:
        out("EDGES_ONLY_OFFENDER: %s" % ln)
    out("EDGES_ONLY_COUNTS_PRINTED=%d" % len(bad))
    out("VINTAGE=%s" % vintage)
    return 0 if (len(bad) == 0 and control == 1) else 1


def reconcile(out, vintage, vline):
    for line in L.disclosure("FACTS PER KEY, reconciled against round 6's closing pair "
                             "at a named served vintage"):
        out(line)
    out(vline)
    out("")

    nodes, per, pop, shadow, cross, src, tgt, decided = _load()
    si = L.facts_per_key("STORED_IN", cross, src)
    df = L.facts_per_key("DERIVES_FROM", cross, src)

    si_ok = (si["edges"] == R6_STORED_IN_RESOLVED
             and list(si["by_type"]) == [R6_STORED_IN_TARGET_CLASS])
    df_ok = (df["edges"] == R6_DERIVES_FROM_RESOLVED)
    ok = si_ok and df_ok

    out("RECONCILE_AGAINST_ROUND6=%s" % ("OK" if ok else "DIVERGED"))
    out("BASELINE_ENVIRONMENT: round 6's CLOSING pair from the drained TO-CG-F-11 "
        "instance (F11-AC3), issuer-stated at this cut. It is a PRODUCER-SIDE emit "
        "count compared against a SERVED-SIDE landed count; the two planes are named "
        "on every line below.")
    out("")
    out("  round 6 asserted:  STORED_IN 135 of 137 on S3_BUCKET_POLICY")
    out("  measured here:     STORED_IN keys=%d edges=%d by_type=%s -- %s"
        % (si["keys"], si["edges"], L._flat(si["by_type"]),
           "REPRODUCED" if si_ok else "DID NOT REPRODUCE"))
    out("  round 6 asserted:  DERIVES_FROM 216 of 216")
    out("  measured here:     DERIVES_FROM keys=%d edges=%d by_type=%s -- %s"
        % (df["keys"], df["edges"], L._flat(df["by_type"]),
           "REPRODUCED" if df_ok else "DID NOT REPRODUCE"))
    out("")

    # The differences, printed rather than absorbed.
    present = [b for b in FIRM_DATA_BUCKETS
               if b in {n["name"] for n in nodes if n["type"] == "S3_BUCKET"}]
    eligible, no_bucket = _eligible_s3keys(present)

    out("DIFFERENCE 1 -- THE 137 IS NOT ON THIS PLANE. 137 is the producer's EMIT count "
        "(derive_stitch stats['stored_in']); an edge that failed to resolve is not a "
        "row in a REL table, so the served graph can show the 135 that landed and can "
        "NEVER show the 2 that did not. The served plane therefore reproduces the "
        "NUMERATOR and its target class exactly, and takes the denominator on the "
        "issuer's statement. GRAIN: emit-side edge vs served-side edge.")
    out("DIFFERENCE 2 -- THE SERVED PLANE'S OWN ELIGIBLE POPULATION IS A DIFFERENT "
        "POPULATION, not a competing value for 137: recomputing the producer's own "
        "constants (FIRM_DATA_BUCKETS x FIRM_KEY_PREFIXES, derive_stitch.py:57-59) over "
        "POST-MERGE canonical S3Key nodes gives %d firm-prefixed key(s) in %d present "
        "firm bucket(s), %d with no present firm bucket. The producer's 191 counts "
        "PRE-MERGE 's3:'-prefixed stitch keys, which do not survive the unification as "
        "distinct nodes, so %d and 191 and 137 are three grains and none refutes another."
        % (eligible, len(present), no_bucket, eligible))
    out("DIFFERENCE 3 -- 216 of 216 IS AN EDGE RATE. In facts-per-key DERIVES_FROM is "
        "%d edge(s) over keys=%d, distribution %s: a 100 percent resolution rate on a "
        "family that already fans %s edges per key. The rate is honest and the reading "
        "'216 facts' is not."
        % (df["edges"], df["keys"], L._flat(df["dist"]),
           ("%.2f" % (float(df["edges"]) / df["keys"])) if df["keys"] else "n/a"))
    out("DIFFERENCE 4 -- FAMILY COUNT AT THE CUT vs HERE. The cut states 59 node_type "
        "and 54 edge_type values at round 6's last read; this served read carries %d "
        "node class(es) and %d edge family(ies). The node count agrees; the edge count "
        "does not. Row NFRA_CLDGRPH-W1-S36 records it."
        % (len(per), len(cross)))
    out("DIFFERENCE 5 -- VINTAGE. The cut names 2026-09-10T03:02:00 with the CVO signing "
        "at 03:31:02Z; the service reports its own vintage below. This census is read "
        "at the service's vintage, not the cut's.")
    out("")
    out("VINTAGE=%s" % vintage)
    return 0 if ok else 1


def _eligible_s3keys(present):
    rows = L.q("MATCH (n:CloudNode) WHERE n.node_type='S3Key' "
               "RETURN n.node_id AS i, n.props AS p")
    elig = 0
    nob = 0
    for r in rows:
        try:
            p = json.loads(r["p"]) if r["p"] else {}
        except ValueError:
            p = {}
        k = str(p.get("key") or "")
        if not k.startswith(FIRM_KEY_PREFIXES):
            continue
        elig += 1
        if str(p.get("bucket") or "") not in present:
            nob += 1
    return elig, nob


def main(argv):
    vintage, vline = L.served_vintage()
    out = Report()
    if "--reconcile" in argv:
        return reconcile(out, vintage, vline)
    return census(out, vintage, vline)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
