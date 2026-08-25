"""ADVI_PERFRP TO-R1-DE / AC10(a) -- the closure denominator.

PROTECTED = files reachable from AdvisorsTab.tsx + DistributionTab.tsx.
CHANGE    = files reachable from the d-cell entry points this TO edits.
NON-SHARED = PROTECTED - CHANGE  -> the set AC10(a)'s source diff actually protects.
SHARED     = PROTECTED & CHANGE  -> a source diff CANNOT protect these; AC10(b)
             confinement and AC10(c) masked render carry them.

COO ruling @f696acb8f8: (a) is quoted WITH its denominator or not quoted at all.
This script exists so that denominator is re-derived, never recalled.

Usage:  python ac10_closure.py <workspace-root>
Exit:   0 normally; 2 if an entry point is missing (a silently wrong denominator).
"""
from __future__ import annotations

import os
import re
import sys

IMPORT_FROM = re.compile(r"""^\s*(?:import|export)\b[^'"]*?from\s*['"]([^'"]+)['"]""", re.M)
IMPORT_BARE = re.compile(r"""^\s*import\s*['"]([^'"]+)['"]""", re.M)
EXTS = (".tsx", ".ts", ".jsx", ".js")


def resolve(spec, from_file, src_root):
    """Resolve a '@/...' or relative specifier to a file path, or None if external."""
    if spec.startswith("@/"):
        base = os.path.join(src_root, spec[2:])
    elif spec.startswith("."):
        base = os.path.join(os.path.dirname(from_file), spec)
    else:
        return None  # node_modules / bare package
    for ext in EXTS:
        if os.path.isfile(base + ext):
            return base + ext
    if os.path.isfile(base) and os.path.splitext(base)[1] in EXTS:
        return base
    for ext in EXTS:
        index = os.path.join(base, "index" + ext)
        if os.path.isfile(index):
            return index
    return None


def closure(entries, src_root):
    """Transitive import closure. Returns (files, unresolved_local_spec_count).

    The unresolved count is printed by the caller: a denominator that silently
    dropped an import is worse than no denominator.
    """
    seen = set()
    stack = list(entries)
    unresolved = 0
    while stack:
        path = os.path.abspath(stack.pop())
        if path in seen or not os.path.isfile(path):
            continue
        seen.add(path)
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError:
            continue
        for spec in IMPORT_FROM.findall(text) + IMPORT_BARE.findall(text):
            target = resolve(spec, path, src_root)
            if target:
                stack.append(target)
            elif spec.startswith((".", "@/")):
                unresolved += 1
    return seen, unresolved


def main():
    if len(sys.argv) < 2:
        print("usage: python ac10_closure.py <workspace-root>")
        return 2
    root = sys.argv[1]
    src = os.path.join(root, "portal", "src")
    adv_int = os.path.join(src, "pages", "AdvisorIntelligence")

    def rel(path):
        return os.path.relpath(os.path.abspath(path), src).replace(os.sep, "/")

    protected_entries = [
        os.path.join(adv_int, "_shared", "tabs", "AdvisorsTab.tsx"),
        os.path.join(adv_int, "_shared", "tabs", "DistributionTab.tsx"),
    ]
    change_entries = [
        os.path.join(adv_int, "_shared", "AdvisorBookView.tsx"),
        os.path.join(adv_int, "_shared", "AdvisorBookClientDetail.tsx"),
        os.path.join(adv_int, "_shared", "AdvisorBookAccountModal.tsx"),
        os.path.join(adv_int, "_shared", "AdvisorPublicProfile.tsx"),
        os.path.join(adv_int, "_shared", "panels", "CanonicalBookView.tsx"),
    ]

    for entry in protected_entries + change_entries:
        if not os.path.isfile(entry):
            print("MISSING ENTRY (denominator would be silently wrong): %s" % rel(entry))
            return 2

    protected, prot_unresolved = closure(protected_entries, src)
    change, chg_unresolved = closure(change_entries, src)
    non_shared = sorted(rel(p) for p in (protected - change))
    shared = sorted(rel(p) for p in (protected & change))

    print("AC10(a) CLOSURE DENOMINATORS  (paths relative to portal/src)")
    print("  PROTECTED entries : %d" % len(protected_entries))
    for entry in protected_entries:
        print("      %s" % rel(entry))
    print("  CHANGE entries    : %d" % len(change_entries))
    print("  PROTECTED closure : %d files   (unresolved local specs: %d)"
          % (len(protected), prot_unresolved))
    print("  CHANGE closure    : %d files   (unresolved local specs: %d)"
          % (len(change), chg_unresolved))
    print("  NON-SHARED (what AC10(a) protects) : %d" % len(non_shared))
    print("  SHARED (carried by AC10(b)+(c))    : %d" % len(shared))
    print()
    print("--- NON-SHARED %d : the AC10(a) diff set ---" % len(non_shared))
    for path in non_shared:
        print("    %s" % path)
    print()
    print("--- SHARED %d : a source diff CANNOT protect these ---" % len(shared))
    for path in shared:
        print("    %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
