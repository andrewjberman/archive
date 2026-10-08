"""AMGT_CORPUS round 40, CRPS-ap-10 -- the scheduled fire's import closure at the tree it is run from, against a list of
changed files. Issuer's file. Read-only: it imports the fire's modules (no fire, no Bloomberg call, no S3 write) and lists which
repository files they loaded.

  python ap10_fire_closure.py <old pin>        (PYTHONPATH=. from the repository root of the NEW pin's tree)

Prints the closure size, then every non-test .py under lib/ and integrations/bloomberg/ changed between <old pin> and HEAD,
marked IN CLOSURE or not, then the forecast field count and whether the budget record exists.
"""
import importlib.util
import os
import subprocess
import sys


def main():
    old = sys.argv[1]
    top = os.path.normcase(os.path.abspath(os.getcwd()))
    import lib.research.corpus.induction_scheduled  # noqa: F401
    import lib.research.corpus.backlog  # noqa: F401
    import lib.research.corpus.library  # noqa: F401
    research = os.path.join("integrations", "bloomberg", "research")
    sys.path.insert(0, research)
    spec = importlib.util.spec_from_file_location("mbp_closure", os.path.join(research, "model_block_pull.py"))
    mbp = importlib.util.module_from_spec(spec)
    sys.modules["mbp_closure"] = mbp  # a spec-loaded module is not registered by itself; without this the pull is missed
    spec.loader.exec_module(mbp)
    closure = set()
    for mod in list(sys.modules.values()):
        path = getattr(mod, "__file__", None)
        if not path:
            continue
        full = os.path.normcase(os.path.abspath(path))
        if full.startswith(top + os.sep):
            closure.add(full[len(top) + 1:].replace(os.sep, "/"))
    out = subprocess.run(["git", "diff", "--name-only", old, "HEAD", "--", "lib", "integrations/bloomberg"],
                         capture_output=True, text=True).stdout
    changed = [ln.strip() for ln in out.splitlines() if ln.strip().endswith(".py") and "/tests/" not in ln]
    inside = [c for c in changed if c.lower() in closure]  # closure paths are normcased: lower case, forward slashes
    print("closure modules %d | changed non-test .py under lib + integrations/bloomberg %d | of them in the closure %d" % (
        len(closure), len(changed), len(inside)))
    for c in changed:
        print("  %s %s" % ("IN CLOSURE    " if c in inside else "not in closure", c))
    print("FORECAST_FIELDS %d record_fire_budget %s" % (len(mbp.FORECAST_FIELDS), callable(getattr(mbp, "record_fire_budget", None))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
