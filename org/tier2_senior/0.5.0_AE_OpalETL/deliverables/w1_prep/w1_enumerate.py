"""W1 C1 enumerator -- per-page first-hand structural enumeration, WITH DENOMINATORS.

Counts what it claims to count. The naive `grep -oE '(get|fetch)[A-Z]\w*\('` over a page dir
counts every local helper and hook that happens to be named get*/fetch* -- it reported 23 for
/positioning against 5 censused artifacts. That is not a finding, it is a WRONG DOMAIN: the
question is "which API-layer accessors does this page call", and the instrument answered
"which identifiers matching a name pattern appear".

So resolve the domain explicitly: parse the page's IMPORTS, keep only bindings that come from
an api module, then intersect with identifiers REFERENCED in the page body. Everything the
filter drops is reported, not silently discarded -- a filtered count with no residue line is
indistinguishable from a real absence.

REFERENCED, not called-with-parens, and the distinction is load-bearing: React Query takes the
accessor BY REFERENCE (`queryFn: getCMAData`). A parens test read 0 accessors on /cma,
/valuations and /correlations -- pages that demonstrably fetch. Under-counting consumers is the
dangerous direction, because the remedy for an "orphan" is deletion.

Read-only. Emits JSON for ingestion into each page's rectangle.c0.
"""
from __future__ import annotations

import json
import os
import re
import sys

PORTAL = sys.argv[1] if len(sys.argv) > 1 else "portal"
PAGES = {
    "/cma": "CapitalMarketAssumptions",
    "/positioning": "Positioning",
    "/attribution": "Attribution",
    "/factor-tilts": "FactorTilts",
    "/valuations": "Valuation",
    "/correlations": "Correlation",
}

# an import is API-layer if its module path lands in the api tree
API_MODULE = re.compile(r"(?:^|/)(api|services)(?:/|$)")
IMPORT_RE = re.compile(r"import\s+(type\s+)?(\{[^}]*\}|\w+)\s+from\s+['\"]([^'\"]+)['\"]", re.S)
CALL_RE = re.compile(r"\b([A-Za-z_$][\w$]*)\s*\(")


def page_files(d: str) -> list[str]:
    out = []
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith((".tsx", ".ts")):
                out.append(os.path.join(root, f))
    return sorted(out)


report = {"portal_ref": PORTAL, "pages": {}, "instrument": {
    "api_binding_rule": "import specifier path matches (^|/)(api|services)(/|$)",
    "referenced_rule": "api binding appears as a whole word in the page body with import statements stripped -- covers by-reference use (queryFn: getX) as well as calls",
    "called_with_parens_rule": "STRICTLY NARROWER sub-count: binding appears as `name(`. Reported for contrast; NOT the consumer signal.",
    "known_limits": [
        "static imports only -- a dynamic import() or a re-export barrel indirection is NOT resolved and would UNDER-count",
        "a textual reference does not prove the call EXECUTES at runtime -- this is a SOURCE-class signal, and the served limb still needs a live read (W1 C5)",
        "counts DISTINCT accessors, not call sites",
        "a binding referenced only inside dead code or a commented block would over-count -- the getNonModelAssets shape, where the live fetch targets a non-resolving key",
    ]}}

for route, folder in PAGES.items():
    d = os.path.join(PORTAL, "src", "pages", folder)
    files = page_files(d)
    api_bindings: dict[str, str] = {}
    other_bindings = 0
    for fp in files:
        src = open(fp, encoding="utf-8", errors="replace").read()
        for type_kw, names, mod in IMPORT_RE.findall(src):
            # A TYPE IS NOT A CONSUMER. Both forms must be excluded: a whole-statement
            # `import type { X } from '@/api/...'` and an inline `type X` specifier inside a value
            # import. Counting them inflates the accessor count with compile-time-only bindings.
            # MEASURED 2026-08-11 on /positioning: 3 real accessors + 2 response types read as 5,
            # while the census's 5 rows were 3 distinct artifacts -- the two errors CANCELLED and
            # produced a spurious MATCH that no reconciliation would have investigated. Being right
            # at the wrong grain is exactly what survives review.
            if type_kw:
                continue
            raw = ([n.strip() for n in names.strip("{}").split(",") if n.strip()]
                   if names.startswith("{") else [names.strip()])
            binds = [n.split(" as ")[-1].strip() for n in raw if not n.startswith("type ")]
            if API_MODULE.search(mod):
                for b in binds:
                    api_bindings[b] = mod
            else:
                other_bindings += len(binds)

    # USED != CALLED-WITH-PARENS. React Query takes the accessor BY REFERENCE
    # (`queryFn: getCMAData`), so a parens-only test reports 0 accessors on a page that fetches
    # three artifacts. Measured: /cma, /valuations and /correlations all read 0-of-N that way.
    # An accessor counted as unused is how a live consumer becomes a false "zero callers" orphan
    # finding -- the exact direction that does real damage, since the remedy for an orphan is
    # deletion. So: count REFERENCED (appears outside its own import line) as the consumer signal,
    # and keep called-with-parens as a strictly narrower sub-count rather than the headline.
    called: set[str] = set()
    referenced: set[str] = set()
    for fp in files:
        src = open(fp, encoding="utf-8", errors="replace").read()
        called |= set(CALL_RE.findall(src))
        body = IMPORT_RE.sub("", src)          # strip import statements; keep everything else
        for b in api_bindings:
            if re.search(rf"\b{re.escape(b)}\b", body):
                referenced.add(b)

    api_called = sorted(b for b in api_bindings if b in referenced)
    api_unused = sorted(b for b in api_bindings if b not in referenced)
    api_paren_called = sorted(b for b in api_bindings if b in called)

    panels_dir = os.path.join(d, "panels")
    panels = sorted(os.listdir(panels_dir)) if os.path.isdir(panels_dir) else []

    report["pages"][route] = {
        "component_dir": f"src/pages/{folder}",
        "files_scanned": len(files),
        "panels_dir_entries": panels,
        "api_accessors_referenced": api_called,
        "api_accessors_imported_never_referenced": api_unused,
        "api_accessors_called_with_parens": api_paren_called,
        "denominators": {
            "api_bindings_imported": len(api_bindings),
            "of_which_referenced": len(api_called),
            "of_which_called_with_parens": len(api_paren_called),
            "of_which_imported_but_never_referenced": len(api_unused),
            "non_api_bindings_dropped_by_filter": other_bindings,
            "distinct_called_identifiers_total": len(called),
        },
    }

print(json.dumps(report, indent=1))

# human summary to stderr so stdout stays pipeable JSON
print("\n=== W1 C1 ENUMERATION (denominators stated) ===", file=sys.stderr)
for route, r in report["pages"].items():
    d = r["denominators"]
    print(f"{route:16} files={r['files_scanned']:<3} panels={len(r['panels_dir_entries']):<2} "
          f"api_ref={d['of_which_referenced']:<3} (of {d['api_bindings_imported']} api imports; "
          f"parens={d['of_which_called_with_parens']}; "
          f"{d['of_which_imported_but_never_referenced']} never-referenced; "
          f"{d['non_api_bindings_dropped_by_filter']} non-api bindings dropped)", file=sys.stderr)
