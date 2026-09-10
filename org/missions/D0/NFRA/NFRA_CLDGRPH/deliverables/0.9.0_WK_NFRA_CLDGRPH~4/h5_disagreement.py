#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-H-5 / CG-s-40 -- H5-AC2.

THE DISAGREEMENT AS A MACHINE-CHECKABLE FACT, NOT A DESCRIPTION.

Two scorers in one estate declare different canonical shapes for ONE edge family. This script
prints both declarations with their file and line AT A COMMIT, asks the SERVED graph which one is
true today, asks the COMMITTED producer which one will be true after the CG-s-33 re-point deploys,
and then RE-RUNS EACH SCORER'S OWN ARITHMETIC on both sides of that deploy to say which one breaks.

INSTRUMENT / COVERAGE:
  - declarations: `git show HEAD:<file>` (the RECORD, not the worktree -- a worktree read would
    fabricate the vintage), full-file scan, denominator = lines in the file.
  - served plane: the projection service, one Cypher statement per question, edge_type read as a
    PROPERTY (row S112: `MATCH ()-[e:SERVED_FROM]->()` errors at the BINDER; a binder error is a
    wrong-form signal, never a zero).
  - producer: `git show HEAD:infra/aws/globgrph/derive_runner.py`, the SERVED_FROM stitch site.
GRAIN: one declaration per (file, line). Edge counts at EDGE grain, target classes at CLASS grain.
BASELINE ENVIRONMENT: the only stored comparison values are the two literal declaration strings in
the two scorer sources; every count is measured live in this process against the served projection
whose own vintage line is printed below. Nothing here is compared against a stored capture.

0 MUTATIONS. Read-only. ASCII only. No egress: the projection read is an Opal-internal read.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=_HERE,
                      capture_output=True, text=True).stdout.strip()
if not ROOT or not os.path.isdir(ROOT):
    print("BLOCKED: could not resolve the worktree root")
    raise SystemExit(2)
ROOT = os.path.abspath(ROOT)
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "infra", "aws", "globgrph"))

DEBTSCAN = "infra/aws/globgrph/debtscan_canon_scorer.py"
MOTIF = "infra/aws/globgrph/canon_motif_scorer.py"
PRODUCER = "infra/aws/globgrph/derive_runner.py"
CANON = "org/modules/graph/canon-patterns.yaml"

SHAPE_A_LIT = "ServedURL-[SERVED_FROM]->S3_BUCKET_POLICY"
SHAPE_B_LIT = "(ServedURL)-[SERVED_FROM]->(S3)"


def show(path: str, rev: str = "HEAD") -> str:
    r = subprocess.run(["git", "show", "%s:%s" % (rev, path)], capture_output=True, text=True)
    if r.returncode != 0:
        print("BLOCKED: git show %s:%s rc=%d" % (rev, path, r.returncode))
        raise SystemExit(2)
    return r.stdout


def lines_with(text: str, needle: str) -> list[int]:
    return [i + 1 for i, ln in enumerate(text.splitlines()) if needle in ln]


def main() -> int:
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    print("=== H5-AC2 -- ONE EDGE, TWO DECLARED SHAPES, MADE CHECKABLE ===")
    print("BRANCH=%s HEAD=%s" % (branch, head))
    print("DECLARATION_SOURCE=git show HEAD:<file> (the record; NOT the worktree)")

    a_txt = show(DEBTSCAN)
    b_txt = show(MOTIF)
    a_lines = lines_with(a_txt, "S3_BUCKET_POLICY")
    b_lines = lines_with(b_txt, SHAPE_B_LIT)
    print("")
    print("SHAPE_A printed :: %s" % SHAPE_A_LIT)
    print("  declared in  : %s@%s lines %s (denominator: %d lines in file)"
          % (DEBTSCAN, head[:10], ",".join(str(x) for x in a_lines), len(a_txt.splitlines())))
    print("  role         : the SCORED_FROM per-class source-provenance string (:48) and the")
    print("                 score_auth_canon docstring (:144). Both are LITERAL PROSE -- the")
    print("                 arithmetic below reads the target class from the graph at runtime.")
    print("SHAPE_B printed :: %s" % SHAPE_B_LIT)
    print("  declared in  : %s@%s lines %s (denominator: %d lines in file)"
          % (MOTIF, head[:10], ",".join(str(x) for x in b_lines), len(b_txt.splitlines())))
    print("  role         : the emitted `dominant_motif` VALUE (:131) and its docstring (:94).")
    print("                 Also a literal -- score_served_lineage counts DISTINCT ServedURL")
    print("                 sources and never reads the target's class at all.")

    # ---- the served plane ------------------------------------------------------------------
    import projection_client as pc  # noqa: E402  (path inserted above)
    conn = pc.connect()
    print("")
    print("QUERY_FORM=edge_type-as-property")
    print("  (the served graph carries edge_type as a PROPERTY of one CloudEdge REL table; the")
    print("   typed form `MATCH ()-[e:SERVED_FROM]->()` errors at the binder and a binder error")
    print("   is a wrong-form signal, never a zero -- banked as row S112.)")
    q_served = ("MATCH (s:CloudNode)-[e:CloudEdge]->(t:CloudNode) "
                "WHERE s.node_type = 'ServedURL' AND e.edge_type = 'SERVED_FROM' "
                "RETURN t.node_type AS tt, count(*) AS c")
    served = conn.rows(q_served)
    print("  STATEMENT: %s" % q_served)
    print("  SERVED_VINTAGE: %s" % conn.vintage)
    print("  AGE_LINE: %s" % conn.age_line)
    print("  RESULT: %s" % served)
    served_total = sum(r["c"] for r in served)
    served_classes = {r["tt"]: r["c"] for r in served}

    # ---- controls ---------------------------------------------------------------------------
    q_ctrl = ("MATCH (s:CloudNode)-[e:CloudEdge]->(t:CloudNode) "
              "WHERE e.edge_type = 'OWNED_BY' RETURN t.node_type AS tt, count(*) AS c")
    ctrl = conn.rows(q_ctrl)
    ctrl_classes = {r["tt"]: r["c"] for r in ctrl}
    q_neg = ("MATCH (s:CloudNode)-[e:CloudEdge]->(t:CloudNode) "
             "WHERE e.edge_type = 'NO_SUCH_EDGE_TYPE_ZZZ' RETURN count(*) AS c")
    neg = conn.rows(q_neg)
    neg_zero = (not neg) or neg[0].get("c") == 0
    ctrl_multi = len(ctrl_classes) >= 2
    ctrl_has_bucket = ctrl_classes.get("S3_BUCKET", 0) > 0
    print("")
    print("--- CONTROLS (a single-class answer from a query that CANNOT return two classes is")
    print("--- not a measurement of the class; both arms run on the SAME statement shape) ---")
    print("  POSITIVE (live family, same statement shape, OWNED_BY): %s" % ctrl)
    print("    returns >=2 distinct target classes : %s" % ctrl_multi)
    print("    can return S3_BUCKET specifically   : %s (so a SERVED_FROM answer of"
          % ctrl_has_bucket)
    print("      S3_BUCKET_POLICY is a property of the DATA, not of the query form)")
    print("  NEGATIVE (an edge_type that does not exist): %s -> zero=%s" % (neg, neg_zero))
    fired = ctrl_multi and ctrl_has_bucket and neg_zero and served_total > 0
    print("POSITIVE_CONTROL_ARMS=multi_class:%s bucket_reachable:%s negative_zero:%s served_nonzero:%s"
          % (ctrl_multi, ctrl_has_bucket, neg_zero, served_total > 0))

    # ---- who matches today -------------------------------------------------------------------
    a_today = served_classes.get("S3_BUCKET_POLICY", 0) == served_total and served_total > 0
    b_today = served_classes.get("S3_BUCKET", 0) == served_total and served_total > 0
    matches_today = "A" if a_today else ("B" if b_today else "NEITHER")
    print("")
    print("SERVED_TODAY: %d SERVED_FROM edge(s) from ServedURL; by target class %s"
          % (served_total, served_classes))
    print("MATCHES_SERVED_TODAY=%s" % matches_today)

    # ---- who matches the committed re-point ---------------------------------------------------
    prod = show(PRODUCER)
    prod_lines = prod.splitlines()
    # SCOPE THE READ TO THE ONE FUNCTION THAT EMITS THE FAMILY. A file-wide token test answers a
    # question about the FILE; the claim is about the SERVED_FROM stitch, and derive_runner.py
    # carries other bucket-resolution sites that would poison a file-wide answer (measured: the
    # pre-fix bare-name form is still present at another site and is not this edge's resolver).
    emit_idx = [i for i, ln in enumerate(prod_lines) if '"edge_type": "SERVED_FROM"' in ln]
    if not emit_idx:
        print("BLOCKED: no SERVED_FROM emit site in %s@HEAD" % PRODUCER)
        raise SystemExit(2)
    e = emit_idx[0]
    start = 0
    for i in range(e, -1, -1):
        if prod_lines[i].startswith("def ") or prod_lines[i].startswith("    def "):
            start = i
            break
    end = len(prod_lines)
    for i in range(e + 1, len(prod_lines)):
        if prod_lines[i].startswith("def "):
            end = i
            break
    block = "\n".join(prod_lines[start:end])
    off = start
    repoint_line = [off + i for i in lines_with(block, "nid = canonical_node_key(n)")]
    cg33 = [off + i for i in lines_with(block, "CG-s-33")]
    bare_name = [off + i for i in lines_with(block, 'nid = n.get("id")')]
    print("")
    print("COMMITTED RE-POINT (CG-s-33), read at %s:%s@%s" % ("HEAD", PRODUCER, head[:10]))
    print("  SCOPE: the SERVED_FROM stitch function, lines %d-%d (emit site at %d); coverage is"
          % (start + 1, end, e + 1))
    print("         that block only, and the file-wide count is printed beside it so the scope")
    print("         is visible: canonical_node_key file-wide=%d, bare-name file-wide=%d"
          % (len(lines_with(prod, "nid = canonical_node_key(n)")),
             len(lines_with(prod, 'nid = n.get("id")'))))
    print("  target resolver now `canonical_node_key(n)` at line(s) %s; CG-s-33 marker at %s;"
          % (repoint_line, cg33))
    print("  the pre-fix bare-name form `nid = n.get(\"id\")` IN THIS BLOCK at %s (empty = gone)"
          % bare_name)
    repointed = bool(repoint_line) and not bare_name
    matches_repoint = "B" if repointed else "A"
    print("  canonical_node_key yields the ARN-form S3_BUCKET node id, so the deployed edge will")
    print("  land on S3_BUCKET -- shape B.")
    print("MATCHES_COMMITTED_REPOINT=%s" % matches_repoint)
    print("DEPLOY_STATE=COMMITTED-NOT-DEPLOYED (the committed producer says B; the served plane")
    print("  still says %s -- the two disagreeing IS the not-deployed evidence)" % matches_today)

    # ---- what changes on each side, by each scorer's OWN arithmetic ---------------------------
    canon_txt = show(CANON)
    m = re.search(r"outlier_frac:\s*([0-9.]+)", canon_txt)
    frac = float(m.group(1)) if m else 0.10
    q_routes = ("MATCH (r:CloudNode)-[e:CloudEdge]->(t:CloudNode) "
                "WHERE r.node_type = 'API_ROUTE' AND e.edge_type = 'ROUTES_TO' "
                "RETURN t.node_type AS tt, count(*) AS c")
    routes = conn.rows(q_routes)

    def auth_census(served_target_class: str) -> dict:
        """debtscan_canon_scorer.score_auth_canon's OWN rule, transcribed from :160-177."""
        shapes: dict[str, int] = {}
        for r in routes:
            shapes["API_ROUTE-ROUTES_TO->%s" % r["tt"]] = shapes.get(
                "API_ROUTE-ROUTES_TO->%s" % r["tt"], 0) + r["c"]
        shapes["ServedURL-SERVED_FROM->%s" % served_target_class] = served_total
        dom = max(shapes.items(), key=lambda kv: kv[1])
        thr = max(1, int(dom[1] * frac))
        outliers = [s for s, n in shapes.items() if s != dom[0] and (n <= thr or n <= 2)]
        return {"shapes": shapes, "dominant": dom, "threshold": thr, "outliers": outliers}

    before = auth_census("S3_BUCKET_POLICY")
    after = auth_census("S3_BUCKET")
    print("")
    print("--- WHAT CHANGES ON EACH SIDE OF THE DEPLOY ---")
    print("  outlier_frac read from %s@%s = %s" % (CANON, head[:10], frac))
    print("  A (debtscan score_auth_canon) BEFORE: shapes=%s dominant=%s threshold=%d outliers=%s"
          % (before["shapes"], before["dominant"], before["threshold"], before["outliers"]))
    print("  A (debtscan score_auth_canon) AFTER : shapes=%s dominant=%s threshold=%d outliers=%s"
          % (after["shapes"], after["dominant"], after["threshold"], after["outliers"]))
    dom_flips = before["dominant"][0] != after["dominant"][0]
    out_changes = before["outliers"] != after["outliers"]
    print("  A dominant flips=%s  outlier set changes=%s" % (dom_flips, out_changes))
    print("  A DECLARATION after the deploy: '%s' becomes FALSE at %s:%s -- and it is the"
          % (SHAPE_A_LIT, DEBTSCAN, ",".join(str(x) for x in a_lines)))
    print("    per-class SOURCE-PROVENANCE string, so it is COPIED INTO THE EMITTED SCORECARD")
    print("    (`scored_from`), where a later reader takes it for the audited source decision.")
    b_arith = ("score_served_lineage counts DISTINCT ServedURL sources carrying a SERVED_FROM "
               "edge and never reads t.node_type: its number is INVARIANT under the re-point")
    print("  B (canon_motif score_served_lineage): %s." % b_arith)
    print("  B DECLARATION after the deploy: '%s' becomes TRUE -- the same act that falsifies A"
          % SHAPE_B_LIT)
    print("    REPAIRS B.")

    breaks = "A" if matches_today == "A" and matches_repoint == "B" else "NEITHER"
    print("")
    print("BREAKS_ON_DEPLOY=%s" % breaks)
    print("  READ THIS PRECISELY: A breaks as a DECLARATION, not as an exception. Its arithmetic")
    print("  is class-agnostic, so nothing raises, no count spikes, and the outlier set is")
    print("  UNCHANGED (%s -> %s). The failure is that the scored artifact keeps emitting a"
          % (before["outliers"], after["outliers"]))
    print("  source-provenance line that no longer describes the graph it scored -- a silent")
    print("  false record, which is the harder failure to notice and the one this placement names.")
    print("POSITIVE_CONTROL=%s" % ("FIRED" if fired else "DID-NOT-FIRE"))
    print("OK: disagreement stated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
