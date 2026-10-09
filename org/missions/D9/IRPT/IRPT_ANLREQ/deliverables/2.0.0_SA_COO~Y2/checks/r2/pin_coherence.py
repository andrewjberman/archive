"""Pin coherence over one function's staged rows (issuer 2.0.0_SA_COO~Y2, rows IRPT_ANLREQ-D2-S16 / IRPT_BCKEND-D2-S60).

A staged file F is pinned at commit P_F. F was written against the modules it imports AS THEY WERE AT P_F. When an
imported module G is packaged at a different version, every call from F into G is untested in that pairing, and
the arity and keyword splits of release 1 revs 4 and 5 were exactly that (composition/retention, served/interactive_access).
This check reads only the source map and git blobs (no zip, no AWS).

Usage: python pin_coherence.py <repo_root> <function> [<ref>]
For every staged .py row F of <function> (source map read at <ref>, default HEAD) and every packaged module G that F imports
at its pin, compare G's blob at P_F with G's PACKAGED blob (its own pin). Different -> SKEW. Last line:
"pin_coherence rows=<n> edges=<e> skewed=<s>"; exit 1 when s > 0. A skew is a pairing nobody has run, not proof of a
defect: an older importer against a newer, compatible callee also skews. Read each one.
"""
import ast
import json
import subprocess
import sys


def git(root, *args):
    return subprocess.run(["git", "-C", root] + list(args), capture_output=True).stdout


def main():
    root, fn = sys.argv[1], sys.argv[2]
    ref = sys.argv[3] if len(sys.argv) > 3 else "HEAD"
    smap = json.loads(git(root, "show", ref + ":infra/aws/lambda/ci/lambda-source-map.json"))
    rows = [r for r in smap["functions"][fn]["staged_from"] if r.get("packaged_as", "").endswith(".py")]
    by_mod = {}
    for r in rows:
        by_mod[r["packaged_as"][:-3].replace("/", ".")] = r
    edges = 0
    skews = []
    for r in rows:
        src = git(root, "show", "%s:%s" % (r["pin"], r["repo_path"]))
        if not src:
            print("ERROR: %s has no blob at its pin %s" % (r["repo_path"], r["pin"][:10]))
            sys.exit(1)
        try:
            tree = ast.parse(src.decode("utf-8"))
        except SyntaxError as e:
            print("ERROR: %s at %s does not parse: %s" % (r["repo_path"], r["pin"][:10], e))
            sys.exit(1)
        imported = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                imported.add(n.module)
            elif isinstance(n, ast.Import):
                imported.update(a.name for a in n.names)
        for mod in sorted(imported & set(by_mod)):
            g = by_mod[mod]
            if g is r:
                continue
            edges += 1
            at_importer = git(root, "show", "%s:%s" % (r["pin"], g["repo_path"]))
            packaged = git(root, "show", "%s:%s" % (g["pin"], g["repo_path"]))
            if at_importer != packaged:
                skews.append("%s@%s imports %s, packaged @%s, differs from %s@%s" % (
                    r["packaged_as"], r["pin"][:10], g["packaged_as"], g["pin"][:10], g["packaged_as"], r["pin"][:10]))
    for s in skews:
        print("SKEW: " + s)
    print("pin_coherence rows=%d edges=%d skewed=%d" % (len(rows), edges, len(skews)))
    sys.exit(1 if skews else 0)


if __name__ == "__main__":
    main()
