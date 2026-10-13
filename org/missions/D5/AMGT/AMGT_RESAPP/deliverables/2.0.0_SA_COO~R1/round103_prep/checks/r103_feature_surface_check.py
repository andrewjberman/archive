"""AMGT_RESAPP round-103 PREP -- FWD-40 promote: the SURFACE of a Security Analysis FEATURE branch cut from the last PROD release (CTO ADDENDUM 1 item 1, NFRA_DEVPLN C-FEATURE).

  python r103_feature_surface_check.py --portal <nested portal checkout> --base 15c9754975 --head HEAD --receipt <receipt.md>
  python r103_feature_surface_check.py --selftest

The branch may change `src/pages/SecurityAnalysis/` and, outside it, ONLY files its receipt names under `## Shared files` (a line `- `<path>` -- other readers: <paths or none>`).
It may NEVER change the paths in FORBIDDEN: the dependency files, `firmAccess.ts` (the partner pages list), `AdvisorBookFeePanel` or any page other than Security Analysis.
Prints the changed files by class and `R103 FEATURE SURFACE: YES|NO (<n> files: <p> page, <s> shared named, <f> forbidden, <u> unnamed)`.
"""
import argparse
import re
import subprocess
import sys

PAGE = "src/pages/SecurityAnalysis/"
FORBIDDEN = (
    re.compile(r"(^|/)package\.json$"), re.compile(r"(^|/)bun\.lockb?$"), re.compile(r"(^|/)firmAccess\.ts$"), re.compile(r"AdvisorBookFeePanel"),
    re.compile(r"^src/pages/(?!SecurityAnalysis/)[^/]+/"),
)


def classify(paths, named):
    out = {"page": [], "shared": [], "forbidden": [], "unnamed": []}
    for p in paths:
        if any(rx.search(p) for rx in FORBIDDEN):
            out["forbidden"].append(p)
        elif p.startswith(PAGE):
            out["page"].append(p)
        elif p in named:
            out["shared"].append(p)
        else:
            out["unnamed"].append(p)
    return out


def named_shared(receipt_text):
    """Paths under `## Shared files`: backticked, with the words `other readers`."""
    m = re.search(r"^## Shared files\s*$(.*?)(?=^## |\Z)", receipt_text, re.M | re.S)
    if not m:
        return set()
    return {mm.group(1) for line in m.group(1).splitlines() if "other readers" in line for mm in [re.search(r"`([^`]+)`", line)] if mm}


def verdict(paths, named):
    c = classify(paths, named)
    ok = bool(paths) and not c["forbidden"] and not c["unnamed"]
    return ok, c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portal")
    ap.add_argument("--base")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--receipt")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        arms = []
        named = {"src/api/x.ts"}
        for name, paths, want in (
            ("A1 page files plus a named shared file: YES", [PAGE + "a.tsx", "src/api/x.ts"], True),
            ("A2 an unnamed shared file: NO", [PAGE + "a.tsx", "src/lib/y.ts"], False),
            ("A3 firmAccess.ts: NO even if named", [PAGE + "a.tsx", "src/lib/firmAccess.ts"], False),
            ("A4 another page's file: NO", [PAGE + "a.tsx", "src/pages/ModelPortfolios/z.tsx"], False),
            ("A5 an empty change: NO (nothing was cut)", [], False),
            ("A6 package.json: NO", ["package.json"], False),
        ):
            ok, _ = verdict(paths, named | {"src/lib/firmAccess.ts"})
            arms.append(ok == want)
            print("   %s %s" % ("PASS" if ok == want else "FAIL", name))
        arms.append(named_shared("## Shared files\n- `src/api/x.ts` -- other readers: none\n- `src/q.ts` -- no readers line\n## Next\n") == {"src/api/x.ts"})
        print("   %s A7 the receipt parser takes only lines that state other readers" % ("PASS" if arms[-1] else "FAIL"))
        print("arms passed %d of %d" % (sum(arms), len(arms)))
        print("R103 FEATURE SURFACE ARMS: %s" % ("YES" if all(arms) else "NO"))
        return 0 if all(arms) else 1
    diff = subprocess.run(["git", "-C", a.portal, "diff", "--name-only", "%s..%s" % (a.base, a.head)], capture_output=True, text=True, check=False)
    paths = [p for p in diff.stdout.splitlines() if p]
    receipt = open(a.receipt, encoding="utf-8").read() if a.receipt else ""
    ok, c = verdict(paths, named_shared(receipt))
    # the receipt names every page changed and its class: a `## Pages changed` section that states `Security Analysis` and `Opal-internal`
    pages = re.search(r"^## Pages changed\s*$(.*?)(?=^## |\Z)", receipt, re.M | re.S)
    if not (pages and "Security Analysis" in pages.group(1) and "Opal-internal" in pages.group(1)):
        ok = False
        print("  receipt   no `## Pages changed` section naming Security Analysis as Opal-internal")
    for k in ("page", "shared", "forbidden", "unnamed"):
        for p in c[k]:
            print("  %-9s %s" % (k, p))
    print("R103 FEATURE SURFACE: %s (%d files: %d page, %d shared named, %d forbidden, %d unnamed)" % ("YES" if ok else "NO", len(paths), len(c["page"]), len(c["shared"]), len(c["forbidden"]), len(c["unnamed"])))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
