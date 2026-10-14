#!/usr/bin/env python3
"""AR331-y-AC3 (TO-AR-y-331, AMENDED by AMENDMENT 2 and AMENDMENT 3): the scope check over the commits of this order.

Reads `base` from the record JSON (the parent of the first commit of this order) and prints it. Prints SCOPE-OK only when
ALL of the following hold; otherwise SCOPE-BAD <why>, exit 1:
  (1) `git diff --name-only <base> HEAD` lists only paths under infra/aws/lambda/investor-reporting/, the one published
      route file docs/contracts/investor-reporting/v1/routes.json, the one new response schema file
      docs/contracts/investor-reporting/v1/responses/analysis-request-commentary-pdf.response.schema.json (AMENDMENT 3),
      and paths under org/missions/D9/IRPT/IRPT_ANLREQ/; no other path under docs/;
  (2) ops/pdf_link.py changes at module level ONLY the FAMILIES tuple (by exactly one added family, YCHARTS_OPAL_REPORT)
      and what the destination check needs: the new FAMILY_REVISION constant and the _default_destination function.
      Every other top-level statement of the module is unchanged (compared by AST, so comments do not count);
  (3) routes.json changes ONLY by ADDING one route row (AMENDMENT 3: and by raising the `_denominator` `declared` and
      `total` counts by one each; every other `_denominator` key is unchanged): removing the added row leaves the base
      file's routes list, and every top-level key other than "routes" and "_denominator" is unchanged.
ASCII only. The repository root is derived from this file's location.
"""
import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]  # deliverables/<serial> -> IRPT_ANLREQ -> IRPT -> D9 -> missions -> org -> root
RECORD = Path(__file__).resolve().parent / "r41" / "COMMENTARY_PDF_ROUTE_RECORD.json"
ALLOWED = ("infra/aws/lambda/investor-reporting/", "org/missions/D9/IRPT/IRPT_ANLREQ/")
ROUTES = "docs/contracts/investor-reporting/v1/routes.json"
RESPONSE = "docs/contracts/investor-reporting/v1/responses/analysis-request-commentary-pdf.response.schema.json"
PDF_LINK = "infra/aws/lambda/investor-reporting/ops/pdf_link.py"
ADDED_FAMILY = "YCHARTS_OPAL_REPORT"
# The only top-level names of pdf_link.py that may differ between the base and HEAD: the families tuple, the family-to-
# revision constant that the destination check needs, and the destination function that reads it.
PDF_LINK_CHANGEABLE = {"FAMILIES", "_default_destination"}
PDF_LINK_NEW_OK = {"FAMILY_REVISION"}
ROUTE_KEY = "GET /api/scoped/investor-reporting/analysis/requests/{requestId}/commentary-pdf"


def show(base, path):
    proc = subprocess.run(["git", "show", "%s:%s" % (base, path)], cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError("git show %s:%s rc=%d" % (base, path, proc.returncode))
    return proc.stdout.decode("utf-8")


def head_show(path):
    return show("HEAD", path)


def module_nodes(source):
    """name -> AST dump of each top-level statement (assignments and defs by name; any other statement by its dump)."""
    out = {}
    for index, node in enumerate(ast.parse(source).body):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            key = node.targets[0].id
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            key = node.name
        else:
            key = "<stmt %d>" % index
        out[key] = ast.dump(node)
    return out, ast.parse(source)


def families_of(source):
    """The FAMILIES tuple's values, each resolved through the module's own string constants."""
    tree = ast.parse(source)
    consts, families = {}, None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name == "FAMILIES":
                families = node.value
            elif isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                consts[name] = node.value.value
    if not isinstance(families, ast.Tuple):
        return None
    values = []
    for elt in families.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
            values.append(elt.value)
        elif isinstance(elt, ast.Name) and elt.id in consts:
            values.append(consts[elt.id])
        else:
            return None
    return tuple(values)


def check_pdf_link(base):
    try:
        base_src, head_src = show(base, PDF_LINK), head_show(PDF_LINK)
    except RuntimeError as exc:
        return "pdf_link.py unreadable: %s" % exc
    base_fam, head_fam = families_of(base_src), families_of(head_src)
    if base_fam is None or head_fam is None:
        return "pdf_link.py FAMILIES is not a tuple of resolvable strings (base=%r head=%r)" % (base_fam, head_fam)
    if head_fam != base_fam + (ADDED_FAMILY,):
        return "FAMILIES is %r at HEAD; the grant is %r plus exactly %r" % (head_fam, base_fam, ADDED_FAMILY)
    base_nodes, _ = module_nodes(base_src)
    head_nodes, _ = module_nodes(head_src)
    for name in sorted(set(base_nodes) | set(head_nodes)):
        if name in PDF_LINK_CHANGEABLE:
            continue
        if name in PDF_LINK_NEW_OK and name not in base_nodes:
            continue
        if base_nodes.get(name) != head_nodes.get(name):
            return "pdf_link.py top-level %r differs from the base and is not the families tuple or the destination check" % name
    if "FAMILY_REVISION" in base_nodes:
        return "pdf_link.py FAMILY_REVISION existed at the base"
    return None


def check_routes(base):
    try:
        base_doc = json.loads(show(base, ROUTES))
        head_doc = json.loads(head_show(ROUTES))
    except (RuntimeError, ValueError) as exc:
        return "routes.json unreadable: %s" % exc
    keys = set(base_doc) | set(head_doc)
    for key in sorted(keys):
        if key in ("routes", "_denominator"):
            continue
        if base_doc.get(key) != head_doc.get(key):
            return "routes.json top-level key %r changed; the grant is one added route row and nothing else" % key
    # AMENDMENT 3: the `_denominator` counts `declared` and `total` rise by one each; every other key is unchanged.
    base_den, head_den = base_doc.get("_denominator"), head_doc.get("_denominator")
    if not isinstance(base_den, dict) or not isinstance(head_den, dict):
        return "routes.json _denominator is absent or not an object at the base or at HEAD"
    if set(base_den) != set(head_den):
        return "routes.json _denominator changes its key set; the grant raises declared and total only"
    for key in sorted(base_den):
        if key in ("declared", "total"):
            continue
        if base_den[key] != head_den[key]:
            return "routes.json _denominator.%s changed; the grant raises declared and total only" % key
    for key in ("declared", "total"):
        if head_den[key] != base_den[key] + 1:
            return "routes.json _denominator.%s is %r at HEAD against %r at the base; the grant raises it by one" % (
                key, head_den[key], base_den[key])
    base_rows, head_rows = base_doc["routes"], head_doc["routes"]
    added = [r for r in head_rows if r not in base_rows]
    if len(head_rows) != len(base_rows) + 1 or len(added) != 1:
        return "routes.json has %d row(s) at HEAD against %d at the base; the grant is one added row" % (
            len(head_rows), len(base_rows))
    if added[0].get("route_key") != ROUTE_KEY:
        return "the added routes.json row is %r, not the commentary route" % added[0].get("route_key")
    rest = [r for r in head_rows if r is not added[0]]
    if rest != base_rows:
        return "routes.json changes a row other than adding the commentary route (the other rows must be unchanged)"
    return None


def main():
    try:
        base = json.loads(RECORD.read_text(encoding="utf-8"))["base"]
    except (OSError, ValueError, KeyError) as exc:
        print("SCOPE-BAD the record JSON carries no base: %s" % exc.__class__.__name__)
        return 1
    print("BASE " + base)
    proc = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=120)
    if proc.returncode != 0:
        print("SCOPE-BAD git diff rc=%d" % proc.returncode)
        return 1
    paths = [line.strip() for line in proc.stdout.decode("utf-8", "replace").splitlines() if line.strip()]
    print("PATHS (%d):" % len(paths))
    for path in paths:
        print("  " + path)
    if not paths:
        print("SCOPE-BAD no path changed between the base and HEAD")
        return 1
    outside = [p for p in paths if not (p.startswith(ALLOWED) or p in (ROUTES, RESPONSE))]
    if outside:
        print("SCOPE-BAD %d path(s) outside the granted trees: %s" % (len(outside), "; ".join(outside)))
        return 1
    if RESPONSE in paths:
        print("response schema: the one new file %s" % RESPONSE)
    if PDF_LINK in paths:
        why = check_pdf_link(base)
        if why:
            print("SCOPE-BAD pdf_link.py: " + why)
            return 1
        print("pdf_link.py: FAMILIES gains exactly %s; other top-level statements unchanged" % ADDED_FAMILY)
    if ROUTES in paths:
        why = check_routes(base)
        if why:
            print("SCOPE-BAD routes.json: " + why)
            return 1
        print("routes.json: one added row, %s; _denominator declared and total +1 each; no other row or key changed"
              % ROUTE_KEY)
    print("SCOPE-OK %d paths, all under the granted trees; the widening and the route row are the only non-test changes"
          % len(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
