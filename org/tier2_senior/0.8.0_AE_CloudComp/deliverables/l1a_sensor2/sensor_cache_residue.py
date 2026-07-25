"""L1a residue sensor #2 -- comp-cache over portal/src (CODE-TEXT shape).

NFRA_COMPLEARN L1a-SENSOR-2 (dispatch 1.0.0_SA_CTO~Z 20260725T090823Z).
Author: 0.8.0_AE_CloudComp~E. PATTERN, not platform: this sensor is bespoke to
comp-cache's shape (code-text source, hook-call-site units) and shares ONLY the
L0a boundary-report type with other sensors (SENSOR_CONTRACT_PLATFORM_OR_PATTERN.md).

THE QUESTION (L1a): what is in comp-cache's OWN source domain (queryKey-bearing
React-Query hook call sites under portal/src) that comp-cache does NOT traverse?

DERIVED, NEVER HAND-DECLARED (IMPLEMENTATION_LEVELS_AND_SEQUENCING.md s4/L1a):
  - the tool's TRAVERSAL is obtained by EXECUTING the tool's own extract()
    (org/modules/graph/cache_cli.py) -- observed walk, method=traversal;
  - the tool's WALKED-HOOK matcher is the tool's own _USEQUERY regex, imported;
  - the tool's DOC-NAMED exclusions are PARSED FROM THE TOOL'S OWN SOURCE TEXT
    (the "useQueries / useInfiniteQuery are NOT audited" contract line + the
    docstring scope block), not typed in by the sensor author;
  - the tool's CLI surface is derived via the registration gate's own extraction
    (manifest_check_cli._established_subcommands), reused not reimplemented.

CELLS (units = queryKey-bearing hook call sites; address_space=code_call_site,
native "path:line:hook", deliberately NOT in KNOWN_ADDRESS_SPACES -- BR008 is the
type's designed visibility for a new shape, not an error):
  covered  = sites the tool's own extract() successfully walked      (traversal)
  member   = sites the tool SAW on its axis and listed unparseable   (traversal)
  doc_only = sites of hooks the tool's own prose names as not-walked (mention)
  orphan   = key-bearing sites the tool neither walks nor names      (mention)
UNKNOWN is first-class: a Query-family identifier whose key-bearing-ness the
sensor cannot establish is REPORTED and EXCLUDED from surface_total, never
silently binned into a cell.

DIRECTION, in-band: enumeration is token-scan (mention) and therefore
UNDER-reports the source; covered/member are exact (traversal). The report's
method enums carry this per-cell (L0a question 2).

EXIT CONTRACT (comp-residue reference): 0 CLEAN / 2 VERDICT (residue found) /
3 REFUSE (nothing could be compared -- never "everything is residue") / 1 FAIL.

READ-ONLY. No writes outside an explicit --out path. ASCII-only output.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

_THIS = Path(__file__).resolve()
_WORKSPACE = _THIS.parents[5]  # l1a_sensor2/deliverables/0.8.0_AE_CloudComp/tier2_senior/org/<ws>
_GRAPH_DIR = _WORKSPACE / "org" / "modules" / "graph"
sys.path.insert(0, str(_GRAPH_DIR))

import cache_cli  # noqa: E402  -- the TOOL UNDER SENSE; its extract() IS the traversal
import boundary_report  # noqa: E402  -- the L0a type; self-validate before emitting

# Query-family identifier token, same lookbehind/lookahead guard as the tool's own
# _USEQUERY so the sensor and the tool count call sites on identical footing.
_QUERY_FAMILY = re.compile(r"(?<![A-Za-z0-9_])(use[A-Za-z]*Quer[A-Za-z]*)(?=\s*[<(])")

# Non-subscription accessor, excluded from the SURFACE (not residue): carries no
# queryKey at its own call site. Grounded in the tool's own matcher comment
# ("useQuery, not useQueryClient / ...") -- the sensor re-derives this from the
# tool source below and REFUSES to hard-code it if the comment vanishes.
_ACCESSOR = "useQueryClient"


def derive_doc_named_exclusions(tool_source: str) -> set[str]:
    """Hooks the TOOL'S OWN TEXT names as adjacent-but-not-audited.

    Parsed from the live denominator-line format string and the docstring scope
    block. Returns identifiers found in a "NOT audited"/"NOT in scope" context.
    Empty set => the tool no longer discloses exclusions (itself reportable).
    """
    named: set[str] = set()
    for m in re.finditer(r"([A-Za-z /]*?)\bare NOT audited\b|NOT in scope[^\n]*:\s*([^\n]*)",
                         tool_source):
        blob = (m.group(1) or "") + (m.group(2) or "")
        named.update(re.findall(r"use[A-Za-z]*Quer[A-Za-z]*", blob))
    # the docstring scope block: "Adjacent hooks NOT in scope (flagged, not folded): X / Y"
    for m in re.finditer(r"Adjacent hooks NOT in scope[^:]*:\s*([^\n]+)", tool_source):
        named.update(re.findall(r"use[A-Za-z]*Quer[A-Za-z]*", m.group(1)))
    return named


def derive_accessor_exclusion(tool_source: str) -> bool:
    """True iff the tool's own matcher comment still names useQueryClient as a
    deliberate non-target. The sensor only excludes the accessor from the surface
    while the tool's source still declares it."""
    return bool(re.search(r"not\s+useQueryClient", tool_source))


def enumerate_sites(root: Path):
    """Token-scan enumeration of Query-family call sites (method=mention).

    Mirrors the tool's own file-set rule (rglob *.tsx + *.ts) so tool and sensor
    disagree only on HOOK coverage, never on FILE coverage.
    Returns list of (relpath, line, hook_identifier).
    """
    sites = []
    if not root.exists():
        return sites
    for f in sorted(list(root.rglob("*.tsx")) + list(root.rglob("*.ts"))):
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "Quer" not in content:
            continue
        blanked = cache_cli._blank_comments(content)  # the tool's own comment-stripper
        rel = str(f.relative_to(_WORKSPACE)).replace("\\", "/")
        for m in _QUERY_FAMILY.finditer(blanked):
            line = blanked.count("\n", 0, m.start()) + 1
            sites.append((rel, line, m.group(1)))
    return sites


def hook_is_key_bearing(hook: str, root: Path) -> bool | None:
    """For a hook the tool neither walks nor names: is it a queryKey-bearing
    subscription? Established from the hook's own DEFINITION in the scanned
    source (definition body mentions queryKey or wraps useQuery). None = UNKNOWN
    (no definition found in-tree -- e.g. a library hook the sensor cannot read)."""
    pat = re.compile(r"(?:function\s+%s\b|(?:const|let)\s+%s\s*=)" % (hook, hook))
    for f in sorted(list(root.rglob("*.tsx")) + list(root.rglob("*.ts"))):
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = pat.search(content)
        if not m:
            continue
        body = content[m.start():m.start() + 4000]
        if "queryKey" in body or re.search(r"\buseQuery\s*[<(]", body):
            return True
        return False
    return None


def git_head(repo: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=30)
        return out.stdout.strip() or "UNRESOLVED"
    except Exception:
        return "UNRESOLVED"


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="sensor_cache_residue",
        description="L1a residue sensor for comp-cache (code-text shape). "
                    "Exit: 0 CLEAN / 2 VERDICT / 3 REFUSE / 1 FAIL.")
    ap.add_argument("--source-root", default=None,
                    help="subtree to sense (default: the tool's own portal/src). "
                         "Controls use real subtrees, never synthetic fixtures.")
    ap.add_argument("--out", default=None, help="write the boundary_report JSON here")
    ap.add_argument("--json", action="store_true", help="print the report JSON to stdout")
    args = ap.parse_args()

    root = Path(args.source_root).resolve() if args.source_root else cache_cli._PORTAL_SRC
    if not root.is_dir():
        # NONEXISTENT input is a FAIL, never a verdict: a REFUSE here would answer garbage
        # with a well-formed epistemic claim (the comp-pulse "MEASURED on a nonexistent
        # file" shape, REC1C_E s4.4). Broken retrieval != empty domain.
        print("FAIL: source root does not exist: %s -- refusing to claim ANY comparison "
              "(a nonexistent domain is not an empty one)." % root)
        return 1
    tool_source = (_GRAPH_DIR / "cache_cli.py").read_text(encoding="utf-8", errors="replace")

    doc_named = derive_doc_named_exclusions(tool_source)
    if not doc_named:
        print("SENSOR-NOTE: the tool's source no longer discloses adjacent-hook exclusions; "
              "doc_only derivation is empty THIS RUN (reportable drift, not a sensor default).")
    accessor_excluded = derive_accessor_exclusion(tool_source)

    # --- the tool's OWN traversal, observed by executing it -------------------------------
    entries, unparseable, tool_total = cache_cli.extract(portal_src=root)

    # --- sensor-side enumeration (mention) ------------------------------------------------
    all_sites = enumerate_sites(root)
    surface_sites = []
    unknown_sites = []
    excluded_accessor = 0
    keybearing_cache: dict[str, bool | None] = {}
    walked_hook = "useQuery"  # from the tool's own _USEQUERY matcher (imported below for control)
    assert cache_cli._USEQUERY.pattern.startswith("(?<![A-Za-z0-9_])useQuery"), \
        "tool matcher drifted; sensor's walked-hook derivation is stale -- FAIL loudly"

    for rel, line, hook in all_sites:
        if hook == _ACCESSOR and accessor_excluded:
            excluded_accessor += 1
            continue
        if hook == walked_hook or hook in doc_named:
            surface_sites.append((rel, line, hook))
            continue
        if hook not in keybearing_cache:
            keybearing_cache[hook] = hook_is_key_bearing(hook, root)
        kb = keybearing_cache[hook]
        if kb is True:
            surface_sites.append((rel, line, hook))
        elif kb is False:
            excluded_accessor += 0  # established non-key-bearing custom hook: out of domain
        else:
            unknown_sites.append((rel, line, hook))

    n_usequery_enum = sum(1 for _, _, h in surface_sites if h == walked_hook)
    n_covered = len(entries)
    n_member = len(unparseable)
    n_doc = sum(1 for _, _, h in surface_sites if h in doc_named)
    orphan_sites = [(r, ln, h) for r, ln, h in surface_sites
                    if h != walked_hook and h not in doc_named]
    n_orphan = len(orphan_sites)

    # --- REFUSE: nothing to compare -------------------------------------------------------
    if not surface_sites and not unknown_sites:
        print("REFUSE: no Query-family call sites under %s -- nothing could be compared. "
              "This is NOT a residue verdict and NOT a clean verdict." % root)
        return 3

    # --- reconciliation guard: tool count vs sensor count on the SAME hook ---------------
    recon_delta = n_usequery_enum - tool_total
    if recon_delta != 0:
        print("SENSOR-WARN: tool saw %d useQuery site(s), sensor enumerated %d "
              "(delta %+d) -- counts derived by different instruments; delta reported, "
              "not smoothed." % (tool_total, n_usequery_enum, recon_delta))

    surface_total = n_covered + n_member + n_doc + n_orphan

    report = {
        "tool": "comp-cache",
        "source": str(root.relative_to(_WORKSPACE)).replace("\\", "/")
                  if root.is_relative_to(_WORKSPACE) else str(root),
        "address_space": "code_call_site",
        "head": "portal@%s" % git_head(_WORKSPACE / "portal"),
        "surface_total": surface_total,
        "cells": {
            "covered": {"applicable": True, "count": n_covered, "method": "traversal"},
            "member": {"applicable": True, "count": n_member, "method": "traversal"},
            "doc_only": {"applicable": True, "count": n_doc, "method": "mention"},
            "orphan": {"applicable": True, "count": n_orphan, "method": "mention"},
        },
        "items": (
            [{"address": "%s:%d:%s" % (r, ln, h), "cell": "doc_only", "method": "mention",
              "evidence": "hook named not-audited by the tool's own contract line"}
             for r, ln, h in surface_sites if h in doc_named]
            + [{"address": "%s:%d:%s" % (r, ln, h), "cell": "orphan", "method": "mention",
                "evidence": "key-bearing (definition wraps useQuery/queryKey); tool neither "
                            "walks nor names it"}
               for r, ln, h in orphan_sites]
            + [{"address": "%s:%d" % (u.file_path, u.line_number), "cell": "member",
                "method": "traversal",
                "evidence": "tool saw and listed unparseable: %s" % u.reason}
               for u in unparseable]
        ),
    }

    violations = boundary_report.validate(report)
    hard = [v for v in violations if v.code != "BR008"]  # BR008 = designed new-shape visibility
    for v in violations:
        print("CONFORMANCE%s: %s at %s: %s"
              % ("" if v.code != "BR008" else " (expected, new shape)", v.code, v.where, v.message))
    if hard:
        print("FAIL: emitted report is NON-CONFORMANT (%d violation(s)) -- a sensor that "
              "cannot emit its own type is broken, not a verdict." % len(hard))
        return 1

    # --- denominator, UNKNOWN, direction: ALWAYS printed, in-band -------------------------
    print("SENSOR comp-cache residue -- source=%s head=%s" % (report["source"], report["head"]))
    print("  DENOMINATOR: surface_total=%d = covered %d (traversal) + member/unparseable %d "
          "(traversal) + doc_only %d (mention) + orphan %d (mention)"
          % (surface_total, n_covered, n_member, n_doc, n_orphan))
    print("  UNKNOWN (first-class, EXCLUDED from surface_total, never binned): %d site(s)%s"
          % (len(unknown_sites),
             " -- " + ", ".join(sorted({h for _, _, h in unknown_sites})) if unknown_sites else ""))
    print("  EXCLUDED by the tool's own declared design (accessor, no key at call site): %d "
          "useQueryClient site(s)" % excluded_accessor)
    print("  DIRECTION: enumeration is mention-derived and UNDER-reports; covered/member are "
          "exact (executed traversal). Residue here can be an UNDERCOUNT, never an overcount.")
    for it in report["items"]:
        if it["cell"] in ("doc_only", "orphan"):
            print("  RESIDUE [%s] %s -- %s" % (it["cell"], it["address"], it["evidence"]))

    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("  REPORT WRITTEN: %s" % args.out)
    if args.json:
        print(json.dumps(report, indent=2))

    if n_doc + n_orphan == 0:
        print("CLEAN: every enumerated key-bearing call site is traversed by the tool "
              "(and the positive-control path is therefore exercised).")
        return 0
    print("VERDICT: %d residue site(s) (doc_only %d + orphan %d) of %d surface -- "
          "the boundary, not a materiality judgment (inference gate's call)."
          % (n_doc + n_orphan, n_doc, n_orphan, surface_total))
    return 2


if __name__ == "__main__":
    sys.exit(main())
