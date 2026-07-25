#!/usr/bin/env python3
"""
NFRA_TOOLUNIFY census classifier (lane 0.8.0_AE_CloudComp~D, scope Sec2.D).

MOVED HERE 20260725 (CVO~Z, 20260725T000124Z): originally lived in gitignored
`.comp-graph/tmp/` and would have died with the session -- "the instrument
this whole census rests on... the artifact-with-no-producer shape we have
been finding all night." Committed under this lane's own owned path so it
survives and is re-runnable (by CVO~Z or anyone) without dependency on my
session state. Not a registered comp-tool (no `.tools/` wrapper, no
tools_index entry) -- a one-time census instrument, WS-7 (making a permanent
version a control) is CTO~Z's call to route, not pre-empted here.

HOW TO RUN (self-contained, no companion files required -- enumerates the
tool universe live):
    python census_classifier.py    # -> _classifier_raw_output.json (per-tool AST hits, full grounding evidence)
    python census_annotate.py      # -> _annotated_candidates.json (evaluation/failure_mode/binding candidates)
    python census_finalize.py      # -> D.sidecar.json (merged register; edit its OVERRIDES dict for source-verified rows)
All three write into org/tier1_exec/1.0.0_SA_CTO/deliverables/NFRA_TOOLUNIFY_CENSUS/
(the CTO~Z-owned deliverable path -- writable, not committable by this lane).

KNOWN RESIDUAL LIMITATIONS (recorded so a future fix doesn't have to
rediscover them by reading the whole file):
  - Const resolution is FUNCTION-SCOPED (fixed 20260725 -- see ShallowVisitor
    below), not fully lexically scoped: a NESTED function is seeded from
    MODULE-level consts only, not its immediate enclosing function's locals
    (closures over an outer function's local variable will under-resolve).
    Rare in this codebase's style (mostly flat top-level functions); accepted
    as a bounded, documented gap rather than building a full scope tree.
  - Return-value resolution (_collect_return_consts) only handles a function
    with EXACTLY ONE reachable `return <expr>`; branchy/multi-return helpers
    are left unresolved rather than guessed.
  - No true interprocedural parameter substitution: a helper whose return
    value depends on ITS OWN parameter in a way that varies meaningfully per
    call site (the `_abs(p)` class, see _collect_return_consts's docstring)
    is correctly EXCLUDED from the return-const fast path, but the caller's
    OWN argument still isn't threaded through symbolically -- it falls back
    to resolving that argument's own text directly, which is usually right
    but is not full substitution.

SCRATCH INSTRUMENT -- not a registered comp-tool.

v2 fixes two real under-detection bugs found by hand-verifying v1 against known
source (comp-freshness, comp-tagauthz both came back EMPTY when they plainly
shell out to `aws`):

  1. NO DATA-FLOW: a Call argument that is a bare Name (`_MANIFEST`, `cmd`,
     `exe`) was never resolved to the literal it was assigned from
     (`_MANIFEST = _THIS_DIR / "graph-call-manifest.yaml"`). Fix: a
     whole-module pre-pass collects name -> [literal string fragments] from
     every Assign (module or function scope; last-write-wins per name, which
     is an approximation, not exact scoping -- adequate for a CANDIDATE
     signal that I then verify by reading, per the two-stage discipline).

  2. NO WRAPPER-FUNCTION TAINT: many tools define a thin local wrapper
     (`def sh(cmd): subprocess.run([exe, *cmd[1:]], ...)`) and shell out only
     through it, with the literal ["aws", ...] list at the CALL SITE of the
     wrapper, not inside the wrapper's own body. Fix: after finding which
     local function DEFINITIONS contain a shell/boto3/file-read signal
     (tainted), a second pass finds every CALL SITE of a tainted function
     name anywhere in the closure and attributes the same kind there too,
     resolving that call site's own literal args for the specific target
     (e.g. `sh(["aws","iam","get-account-authorization-details"])`).

Still classify-by-CALL-SITE, never by string presence in comments/docstrings/
regex-pattern literals (the comp-manifest-check / comp-graph FP class) -- the
data-flow resolution above only follows REAL AST Assign/Call structure, never
raw text search over the file.

A SEPARATE, lower-trust secondary pass (`grep_candidates`) does a plain
keyword scan per closure module, kept apart from the authoritative AST-based
reads_typed/writes_typed. Any tool where grep found a surface keyword the AST
pass did not attribute is flagged NEEDS-MANUAL-CHECK -- the two-stage
"comp-tool localizes, raw call verifies" discipline applied to my own
instrument, not just to the tools it audits.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

WS = Path(r"C:\Users\AndrewBerman\Desktop\ajb_workspace")

FROZEN_SNAPSHOTS = [
    "stitch_graph.json", "stitch_marker.json", "graph_contracts.yaml",
    "estate-coverage-resolver.json",
]
DERIVED_CACHES = [
    "platinum.", ".cache", "graph_cache", "tool_activity_cache.parquet",
    "pydeps.json", "baseline.json",
    # added post-scoping-fix (CVO~Z held-back control, 6 real misses): these
    # resolved to UNCLASSIFIED-PATH once the const-resolution bug was fixed
    # and the literal filename became visible for the first time -- a
    # vocabulary gap, not a resolution gap. All 4 are regenerable local
    # artifacts with a named rebuild command (nerves-*: `nerves_lexical
    # build` / `nerves_accrete build`, comp_pulse.py:183 confirms the
    # subprocess rebuild path; the two IAM caches: extract_iam.py /
    # comp_iam_live.py, per-account/policy snapshots refreshed on demand).
    "nerves-edges.json", "nerves-risk-edges.json",
    "managed_policy_actions_cache.json", "comp_aws_derive_iam.json",
]
CONFIG_FILES = [
    "graph-call-manifest.yaml", "comp-tools.yaml", "comp-coverage-map.yaml",
    "comp-output-contracts.yaml", "manifest_check_config.yaml",
    "ec2_manifest.json", "critical-surfaces.yaml", "nfra_ontology_rule_bank.yaml",
    "comp-which-routing", ".yaml", ".yml",
]
SOURCE_SCAN_MARKERS = ["graph.json", "trace_graph", ".comp-graph"]
KUZU_MARKERS = ["kuzu_db", "kuzu_nessie_db", "kuzu.connection", "kuzu.database"]
ICEBERG_MARKERS = ["iceberg", "nessie", "warehouse/globgrph"]
LIVE_AWS_MARKERS = ["boto3", "s3://", "dynamodb", "aws s3", "aws iam", "aws lambda",
                     "aws events", "aws logs", "aws cloudwatch", "aws glue", "aws ssm"]

LOCAL_ROOTS = [
    WS / "org" / "modules" / "graph",
    WS / "org" / "modules" / "graph" / "debtscan",
    WS / "infra" / "aws" / "globgrph",
    WS / ".tools",
    WS / ".tools" / "lib",
    WS,
]


def classify_path_text(text: str) -> str:
    t = text.lower()
    for marker in FROZEN_SNAPSHOTS:
        if marker.lower() in t:
            return "FROZEN-SNAPSHOT"
    for marker in DERIVED_CACHES:
        if marker.lower() in t:
            return "DERIVED-CACHE"
    for marker in KUZU_MARKERS:
        if marker in t:
            return "KUZU-CANONICAL"
    for marker in ICEBERG_MARKERS:
        if marker in t:
            return "ICEBERG-DIRECT"
    for marker in SOURCE_SCAN_MARKERS:
        if marker.lower() in t:
            return "SOURCE-SCAN"
    for marker in LIVE_AWS_MARKERS:
        if marker in t:
            return "LIVE-AWS"
    for marker in CONFIG_FILES:
        if marker.lower() in t:
            return "CONFIG"
    return "UNCLASSIFIED-PATH"


def resolve_expr_text(node, consts: dict, _depth=0) -> str:
    """Best-effort literal text for ANY expression node: direct string
    constants, f-string literal parts, BinOp (Path `/` chains, string concat),
    List/Tuple/Starred elements, and -- the key recursive step -- a bare Name
    is looked up against `consts` (names resolved SO FAR in a single forward
    pass), so `cmd = [AWS, *a]` resolves through to AWS's own already-seen
    literal ("aws") rather than stopping at the unresolved Name `AWS`. Depth-
    capped against pathological recursion; this is a heuristic candidate
    resolver, not an interpreter."""
    if _depth > 6 or node is None:
        return ""
    out = []
    if isinstance(node, ast.Starred):
        return resolve_expr_text(node.value, consts, _depth + 1)
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                out.append(v.value)
        return " ".join(out)
    if isinstance(node, ast.Name):
        return consts.get(node.id, "")
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        for elt in node.elts:
            out.append(resolve_expr_text(elt, consts, _depth + 1))
        return " ".join(x for x in out if x)
    if isinstance(node, ast.BinOp):
        out.append(resolve_expr_text(node.left, consts, _depth + 1))
        out.append(resolve_expr_text(node.right, consts, _depth + 1))
        return " ".join(x for x in out if x)
    if isinstance(node, ast.IfExp):
        out.append(resolve_expr_text(node.body, consts, _depth + 1))
        out.append(resolve_expr_text(node.orelse, consts, _depth + 1))
        return " ".join(x for x in out if x)
    if isinstance(node, ast.BoolOp):  # `shutil.which("aws") or shutil.which("aws.cmd")`
        for v in node.values:
            out.append(resolve_expr_text(v, consts, _depth + 1))
        return " ".join(x for x in out if x)
    if isinstance(node, ast.Call):
        # a call to a known RETURN-VALUE helper (`_managed_policy_cache_path(ws)`
        # -> "managed_policy_actions_cache.json", pre-resolved into `consts` under
        # the function's own name by _collect_return_consts before this runs)
        # takes precedence -- the callee's return literal IS the meaningful text,
        # its own args (e.g. `workspace_root`, unresolvable) are not.
        if isinstance(node.func, ast.Name) and node.func.id in consts:
            return consts[node.func.id]
        # else: e.g. str(X), os.path.join(a,b), Path(a)/b -- resolve args too
        for a in node.args:
            out.append(resolve_expr_text(a, consts, _depth + 1))
        return " ".join(x for x in out if x)
    if isinstance(node, ast.Attribute):
        # fall through to any literal fragments elsewhere in the chain (rare)
        return ""
    return ""


class ConstCollector(ast.NodeVisitor):
    """Whole-module SINGLE FORWARD PASS: name -> resolved literal text for
    that name's Assign RHS (any scope, last-write-wins; resolves Names against
    consts SEEN SO FAR, so a module-level `AWS = "aws"` feeds forward into a
    later `cmd = [AWS, *a]`). A CANDIDATE resolver for bare-Name call
    arguments, not a real interpreter -- verified by hand per tool, never
    trusted standalone."""

    def __init__(self):
        self.consts: dict[str, str] = {}

    def visit_Assign(self, node):
        frag = resolve_expr_text(node.value, self.consts)
        if frag:
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    self.consts[tgt.id] = frag
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if node.value is not None:
            frag = resolve_expr_text(node.value, self.consts)
            if frag and isinstance(node.target, ast.Name):
                self.consts[node.target.id] = frag
        self.generic_visit(node)


class ShallowVisitor(ast.NodeVisitor):
    """Collects Assign/AnnAssign/Call nodes reachable WITHOUT descending into a
    nested FunctionDef/AsyncFunctionDef/ClassDef body. Used to get a scope's
    OWN direct statements (a function's, or the module's) so each function
    gets an INDEPENDENT local-variable namespace instead of one flat
    whole-file dict.

    THE BUG THIS FIXES (CVO~Z held-back control, 20260725T000124Z, 6 real
    misses -- comp-gitdrill/comp-surface-check <- nerves-edges.json/
    nerves-risk-edges.json; comp-iam <- managed_policy_actions_cache.json/
    comp_aws_derive_iam.json): a single forward-pass ConstCollector over the
    WHOLE module treats `rp` (or any short, commonly-reused local name) as
    ONE namespace slot. `cli.py:338  rp = os.path.join(..., "nerves-risk-
    edges.json")` is correct at ITS call site, but `rp` (or a same-shaped
    generic name) reused as a local in a DIFFERENT, unrelated function
    elsewhere in a 700-line file overwrites the dict entry before -- or
    after -- the real call site is visited, depending on file order. Same
    root cause as bug #6 (method-call receivers never resolved) but the
    adjacent hole: that one was about WHICH AST NODE gets inspected, this one
    is about WHICH SCOPE a resolved value is valid in."""

    def __init__(self):
        self.assigns = []
        self.calls = []

    def visit_Assign(self, node):
        self.assigns.append(node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self.assigns.append(node)
        self.generic_visit(node)

    def visit_Call(self, node):
        self.calls.append(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        return  # STOP -- a nested def gets its own independent scope, processed separately

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        return  # STOP -- methods are scope-independent from the enclosing module too


def _single_return_value(fn) -> ast.AST | None:
    """A function's return EXPRESSION, iff it has EXACTLY ONE reachable
    `return <expr>` (no bare `return`, no multiple distinct return sites) --
    the narrow, safe case (`_managed_policy_cache_path`-shaped path-builder
    helpers). Anything with branchy/multiple returns is left unresolved
    rather than guessed."""
    # ast.walk(fn) would include returns from NESTED functions too, which
    # would wrongly attribute an inner closure's return to the outer fn.
    # Exclude by only counting Return nodes reachable via a ShallowVisitor-
    # style traversal (skip nested Function/Async/Class bodies).
    class _RetCollector(ast.NodeVisitor):
        def __init__(self):
            self.rets = []

        def visit_Return(self, node):
            self.rets.append(node)
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            return

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, node):
            return

    rc = _RetCollector()
    for stmt in fn.body:
        rc.visit(stmt)
    if len(rc.rets) == 1 and rc.rets[0].value is not None:
        return rc.rets[0].value
    return None


def _param_names(fn) -> set:
    a = fn.args
    names = {p.arg for p in a.posonlyargs} | {p.arg for p in a.args} | {p.arg for p in a.kwonlyargs}
    if a.vararg:
        names.add(a.vararg.arg)
    if a.kwarg:
        names.add(a.kwarg.arg)
    return names


def _collect_return_consts(all_funcs, module_consts: dict) -> dict:
    """name -> resolved return-literal, for simple single-return helper
    functions whose return does NOT depend on any of their OWN parameters
    (the `_managed_policy_cache_path(ws) -> ws/".comp-graph"/
    "managed_policy_actions_cache.json"` shape -- CVO~Z's held-back control,
    comp-iam miss: the literal suffix is independent of `ws`). The caller
    sees an opaque `p = helper(x); p.read_text()`; the literal lives inside
    the CALLEE's return, not the call site's own args (the mirror-image of
    the wrapper-taint mechanism, which handles the literal living at the
    call site instead).

    REGRESSION FOUND BY THE BEFORE/AFTER DIFF CVO~Z REQUESTED (000358Z), NOT
    GUESSED: a first version of this treated EVERY single-return helper as a
    fixed constant, including ones like `_abs(p): return os.path.join(
    WORKSPACE_ROOT, p)` -- here the interesting, call-site-varying part IS
    the parameter, so caching one resolved value for `_abs` and returning it
    for EVERY call site (discarding that call's own actual argument) was
    WRONG -- e.g. `_abs(ROLLING_LOG)` resolved to WORKSPACE_ROOT's own path
    fragments instead of ROLLING_LOG's literal ("org/compiler-tools-log.md"
    -> ".. .. ..").

    A blunt "skip if a parameter appears anywhere" guard is TOO blunt --
    `_managed_policy_cache_path(workspace_root)` ALSO references its
    parameter (as the path prefix) and must still be kept, because its
    return expression carries its own STRING LITERALS
    (".comp-graph"/"managed_policy_actions_cache.json") that are meaningful
    regardless of what the parameter resolves to. The real discriminator:
    does the return expression contain a literal of its own? If the return
    references a parameter AND has no self-contained string literal (`_abs`
    -- both operands are bare Names, nothing written IN THE RETURN ITSELF is
    a literal), the "constant" is entirely borrowed from whatever the
    parameter/other names happen to resolve to elsewhere and is unsafe to
    cache. If it has a literal too, the literal survives regardless."""
    out = {}
    for fn in all_funcs:
        ret_val = _single_return_value(fn)
        if ret_val is None:
            continue
        params = _param_names(fn)
        has_own_literal = any(isinstance(n, ast.Constant) and isinstance(n.value, str)
                               for n in ast.walk(ret_val))
        references_param = params and any(isinstance(n, ast.Name) and n.id in params
                                           for n in ast.walk(ret_val))
        if references_param and not has_own_literal:
            continue  # entirely parameter/external-name-derived, no self-contained literal
        fn_sv = ShallowVisitor()
        for stmt in fn.body:
            fn_sv.visit(stmt)
        local = _collect_scope_consts(fn_sv.assigns, module_consts)
        text = resolve_expr_text(ret_val, local)
        if text:
            out[fn.name] = text
    return out


def _collect_scope_consts(assign_nodes, base_consts: dict) -> dict:
    """Fold a scope's OWN assigns forward into a dict SEEDED from base_consts
    (the enclosing scope) -- never mutates base_consts."""
    local = dict(base_consts)
    for a in assign_nodes:
        if isinstance(a, ast.Assign):
            frag = resolve_expr_text(a.value, local)
            if frag:
                for tgt in a.targets:
                    if isinstance(tgt, ast.Name):
                        local[tgt.id] = frag
        elif isinstance(a, ast.AnnAssign) and a.value is not None:
            frag = resolve_expr_text(a.value, local)
            if frag and isinstance(a.target, ast.Name):
                local[a.target.id] = frag
    return local


class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.import_bindings = {}

    def visit_Import(self, node):
        for alias in node.names:
            local = alias.asname or alias.name.split(".")[0]
            self.import_bindings[local] = alias.name
            self.imports.append((alias.name, None, node.lineno, False))
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        mod = node.module or ""
        for alias in node.names:
            local = alias.asname or alias.name
            self.import_bindings[local] = f"{mod}.{alias.name}" if mod else alias.name
            self.imports.append((mod, alias.name, node.lineno, True))
        self.generic_visit(node)


class FuncDefCollector(ast.NodeVisitor):
    """Map local function name -> its ast.FunctionDef node (module-level defs
    only; adequate for the wrapper-taint heuristic)."""

    def __init__(self):
        self.funcs: dict[str, ast.FunctionDef] = {}

    def visit_FunctionDef(self, node):
        self.funcs[node.name] = node
        # do not descend into nested defs for THIS map (keep it to top-level
        # callable names that other modules/call-sites could plausibly name)
        for child in ast.iter_child_nodes(node):
            pass

    visit_AsyncFunctionDef = visit_FunctionDef


def name_chain(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


class CallSiteVisitor(ast.NodeVisitor):
    def __init__(self, import_bindings, consts, source_lines, tainted_funcs=None):
        self.bindings = import_bindings
        self.consts = consts
        self.lines = source_lines
        self.tainted_funcs = tainted_funcs or {}  # name -> kind
        self.hits = []
        self.call_targets = set()  # bare function names called (for taint discovery)

    def _snippet(self, lineno, span=1):
        lo = max(0, lineno - 1 - span)
        hi = min(len(self.lines), lineno + span)
        return "\n".join(self.lines[lo:hi])

    def visit_Call(self, node):
        chain = name_chain(node.func)
        if chain:
            root = chain.split(".")[0]
            resolved_root = self.bindings.get(root, root)
            self.call_targets.add(chain.split(".")[-1])

            all_arg_text = " ".join(resolve_expr_text(a, self.consts) for a in node.args)

            if resolved_root == "boto3" and any(chain.endswith(x) for x in (".client", ".resource")):
                self.hits.append({"lineno": node.lineno, "kind": "LIVE-AWS",
                                   "detail": f"call:{chain}", "snippet": self._snippet(node.lineno)})
            elif resolved_root == "kuzu" and any(chain.endswith(x) for x in (".Connection", ".Database")):
                self.hits.append({"lineno": node.lineno, "kind": "KUZU-CANONICAL",
                                   "detail": f"call:{chain}", "snippet": self._snippet(node.lineno)})
            elif "iceberg" in resolved_root.lower() or "nessie" in resolved_root.lower():
                self.hits.append({"lineno": node.lineno, "kind": "ICEBERG-DIRECT",
                                   "detail": f"call:{chain}", "snippet": self._snippet(node.lineno)})
            elif chain in ("open",) or chain.endswith(".read_text") or chain.endswith(".read_bytes") \
                    or chain in ("json.load", "json.loads", "yaml.safe_load") \
                    or chain.endswith(".write_text") or chain.endswith(".unlink") \
                    or chain.endswith(".exists") or chain.endswith(".stat") \
                    or chain == "json.dump":
                # NOTE: json.dumps deliberately excluded -- it serializes to a
                # STRING (no file arg at all), not a file write; counting it
                # produced noise-only "unresolved" hits on tools that merely
                # build a JSON string for stdout.
                is_meta = chain.endswith(".exists") or chain.endswith(".stat")
                is_write = chain.endswith(".unlink") or chain.endswith(".write_text") or chain == "json.dump"
                # for a METHOD-style call (`path.read_text()`, `path.exists()`)
                # the interesting target is the RECEIVER (node.func.value),
                # not node.args -- read_text()/exists()/stat()/unlink()/
                # write_text() take NO positional path arg at all, so
                # all_arg_text is unconditionally "" for every one of them
                # regardless of how resolvable the receiver is. FOUND WHILE
                # WRITING THE DELIVERABLE (not the debug loop): comp-graph's
                # `stitch = _GLOBGRPH_DIR / "stitch_graph.json"; ...
                # stitch.exists()` resolves `stitch` to a real FROZEN-SNAPSHOT
                # literal via consts, but the .exists() call itself was never
                # checked against it -- only node.args (empty) got classified,
                # so this fell through to the generic dynamic-fallback and
                # under-reported comp-graph's real (metadata-only) touch on
                # stitch_graph.json. Resolve the receiver FIRST.
                receiver = node.func.value if isinstance(node.func, ast.Attribute) else None
                receiver_text = resolve_expr_text(receiver, self.consts) if receiver is not None else ""
                receiver_is_bare_name = isinstance(receiver, ast.Name)
                arg0_is_bare_name = bool(node.args) and isinstance(node.args[0], (ast.Name, ast.Attribute))

                combined_text = " ".join(x for x in (all_arg_text, receiver_text) if x)
                if combined_text:
                    kind = classify_path_text(combined_text)
                elif receiver_is_bare_name or arg0_is_bare_name:
                    # a bare-Name (or simple `args.x` Attribute) path target
                    # with NO resolvable literal anywhere in its assignment
                    # history is, empirically (comp-symbols, comp-shell,
                    # comp-honesty, comp-kit-striplist-gate all hit this
                    # shape), a CALLER-SUPPLIED path (a CLI arg threaded
                    # through, e.g. `analyze(path)` -> `open(resolved)`, or
                    # `path.read_text()` on a Path built from `args.file`) --
                    # a real, dynamic SOURCE-SCAN target, not "nothing
                    # found". Tagged distinctly so the register says so
                    # honestly rather than asserting a fixed artifact that
                    # doesn't exist, or silently dropping the call site.
                    kind = "SOURCE-SCAN-DYNAMIC"
                else:
                    kind = "UNRESOLVED-PATH-ARG"
                self.hits.append({
                    "lineno": node.lineno, "kind": kind, "detail": f"call:{chain} arg~={combined_text[:100]!r}",
                    "meta_only": is_meta, "is_write": is_write,
                    "snippet": self._snippet(node.lineno),
                })
            elif chain in ("subprocess.run", "subprocess.check_output", "subprocess.Popen",
                            "run", "check_output", "Popen") or root == "sp":
                is_write = False
                if all_arg_text.strip().lower().startswith("aws"):
                    kind = "LIVE-AWS"
                    is_write = any(v in all_arg_text for v in (" cp ", "put-object", " sync ", "put_object"))
                elif all_arg_text.strip().lower().startswith("git"):
                    kind = "SOURCE-SCAN"
                else:
                    kind = None
                if kind:
                    self.hits.append({"lineno": node.lineno, "kind": kind,
                                       "detail": f"subprocess:{all_arg_text.strip()[:100]}",
                                       "is_write": is_write,
                                       "snippet": self._snippet(node.lineno)})
            elif chain.split(".")[-1] in self.tainted_funcs:
                # a call to a LOCALLY-TAINTED wrapper function -- resolve THIS
                # call site's own literal args for the specific target (the
                # comp-tagauthz `sh(["aws", ...])` shape: the literal lives at
                # the call site, not inside sh()'s own body).
                taint = self.tainted_funcs[chain.split(".")[-1]]
                kind = None
                is_write = False
                if taint["class"] == "SHELL-WRAPPER":
                    at = all_arg_text.strip().lower()
                    if at.startswith("aws"):
                        kind = "LIVE-AWS"
                        is_write = any(v in all_arg_text for v in (" cp ", "put-object", " sync ", "put_object"))
                    elif at.startswith("git"):
                        kind = "SOURCE-SCAN"
                elif taint["class"] == "FILE-WRAPPER":
                    if all_arg_text:
                        k = classify_path_text(all_arg_text)
                        kind = k if k != "UNCLASSIFIED-PATH" else None
                if kind is None:
                    kind = taint.get("default_kind")
                if kind:
                    self.hits.append({"lineno": node.lineno, "kind": kind, "is_write": is_write,
                                       "detail": f"via-wrapper:{chain}({taint['class']}) arg~={all_arg_text[:100]!r}",
                                       "snippet": self._snippet(node.lineno)})
        self.generic_visit(node)


_SHELL_CALL_NAMES = {"run", "check_output", "Popen", "check_call"}
_FILE_CALL_NAMES = {"open", "read_text", "read_bytes", "load", "safe_load"}
# NOTE: "loads" deliberately excluded -- json.loads/yaml differentiate load
# (a file HANDLE) from loads (an in-memory STRING, never a file). Found by
# the held-out self-check: comp-secrets._shape(value) calls json.loads(raw)
# on an already-fetched secret VALUE (never a file), and the taint heuristic
# false-tagged it FILE-WRAPPER, which would have mis-attributed a fixed-
# artifact read to every _shape() call site. "safe_load" stays in the set
# (this codebase's own convention is yaml.safe_load(fh) off an opened
# handle -- manifest_check_cli.py, graph_status_cli.py, etc.) but is a known
# residual ambiguity: safe_load(a_string) exists too and would still
# false-taint. Not fully closed -- flag any safe_load-tainted call site in
# the manual pass rather than trusting it blind.


def find_tainted_functions(tree, import_bindings, consts, source_lines) -> dict:
    """Which local function DEFS are STRUCTURAL wrappers around a shell-out or
    a file-read -- i.e. their body calls subprocess.run/... or open/json.load/
    yaml.safe_load AT ALL, regardless of whether THAT call's own argument
    resolves to a literal (it usually won't: the literal lives at the CALL
    SITE of the wrapper, one level up -- comp-tagauthz's `sh(cmd)` shape,
    where `cmd` is a parameter, not something the wrapper body can see).

    Two taint classes:
      SHELL-WRAPPER -- body shells out (subprocess.*); classify by whatever
                       kind the CALL SITE's own resolved args give.
      FILE-WRAPPER  -- body opens/reads/parses a file by a NAME that is not
                       itself a locally-resolvable literal (i.e. plausibly a
                       parameter); classify by the CALL SITE's own args.
    Also keeps a `default_kind` when the body itself DOES resolve to a fixed
    kind (a wrapper with a hardcoded internal target) as a fallback for call
    sites whose own args are unresolvable either.
    """
    fc = FuncDefCollector()
    fc.visit(tree)
    tainted = {}
    for name, fn_node in fc.funcs.items():
        cv = CallSiteVisitor(import_bindings, consts, source_lines, tainted_funcs={})
        is_shell = is_file = False
        for stmt in ast.walk(fn_node):
            if isinstance(stmt, ast.Call):
                cv.visit_Call(stmt)
                inner_chain = name_chain(stmt.func)
                if inner_chain and inner_chain.split(".")[-1] in _SHELL_CALL_NAMES:
                    is_shell = True
                if inner_chain and inner_chain.split(".")[-1] in _FILE_CALL_NAMES:
                    is_file = True
        real_hits = [h for h in cv.hits if h["kind"] not in ("UNCLASSIFIED-PATH", "UNRESOLVED-PATH-ARG", None)]
        default_kind = real_hits[0]["kind"] if real_hits else None
        if is_shell:
            tainted[name] = {"class": "SHELL-WRAPPER", "default_kind": default_kind}
        elif is_file:
            tainted[name] = {"class": "FILE-WRAPPER", "default_kind": default_kind}
        elif default_kind:
            tainted[name] = {"class": "FIXED", "default_kind": default_kind}
    return tainted


def resolve_local_module(name: str, from_module) -> Path | None:
    candidates = []
    if from_module:
        dotted = from_module.replace(".", "/")
        candidates.append(dotted + ".py")
    else:
        dotted = name.replace(".", "/")
        candidates.append(dotted + ".py")
    for root in LOCAL_ROOTS:
        for cand in candidates:
            p = root / cand
            if p.is_file():
                return p
    bare = (from_module or name).split(".")[-1] + ".py"
    for root in LOCAL_ROOTS:
        p = root / bare
        if p.is_file():
            return p
    return None


def analyze_module(path: Path):
    """Single-module analysis: consts, imports, direct hits, tainted funcs,
    call_targets (for cross-module taint propagation), grep candidates.

    FUNCTION-SCOPED const resolution (fixed 20260725, CVO~Z held-back control
    20260725T000124Z): each function gets its OWN local-variable namespace,
    seeded from module-level consts, rather than one flat whole-file dict.
    The prior flat version didn't just MISS bindings (nerves-edges.json /
    nerves-risk-edges.json / managed_policy_actions_cache.json /
    comp_aws_derive_iam.json, all bound through a locally-named variable like
    `rp` then used later via `open(rp)`) -- CVO~Z's own follow-up (000358Z)
    named the sharper risk a flat namespace implies and the held-back control
    structurally cannot see: a same-named local in an UNRELATED function
    elsewhere in the file can resolve a call site to a CONFIDENTLY WRONG
    artifact, indistinguishable in the register from a correct one. Measured
    via a before/after diff of every resolved call site across all 92 tools
    (see D.md addendum) -- not merely reasoned about."""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src, filename=str(path))
    except Exception as e:
        return None, f"PARSE ERROR: {e}"

    iv = ImportVisitor()
    iv.visit(tree)

    module_sv = ShallowVisitor()
    for stmt in tree.body:
        module_sv.visit(stmt)
    module_consts = _collect_scope_consts(module_sv.assigns, {})

    # RETURN-VALUE resolution (the comp-iam miss: `_managed_policy_cache_path`
    # returns a literal-bearing Path; callers assign it opaquely and use IT,
    # never re-stating the literal). Fold simple single-return helpers' return
    # literals into module_consts UNDER THE FUNCTION'S OWN NAME, so
    # `resolve_expr_text`'s Call branch resolves `helper(x)` -> the literal,
    # taking precedence over trying to resolve `x` (usually a parameter, and
    # irrelevant here -- the callee's return is the meaningful text).
    all_funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    module_consts.update(_collect_return_consts(all_funcs, module_consts))

    tainted = find_tainted_functions(tree, iv.import_bindings, module_consts, src.splitlines())

    all_hits = []
    all_call_targets = set()

    # module-level calls (outside any function)
    csv = CallSiteVisitor(iv.import_bindings, module_consts, src.splitlines(), tainted_funcs=tainted)
    for c in module_sv.calls:
        csv.visit_Call(c)
    all_hits.extend(csv.hits)
    all_call_targets |= csv.call_targets

    # each function (any nesting depth) gets its OWN scope, seeded from
    # module_consts -- NOT from a flat whole-file dict, and NOT polluted by
    # (or polluting) any unrelated function's same-named local
    for fn in all_funcs:
        fn_sv = ShallowVisitor()
        for stmt in fn.body:
            fn_sv.visit(stmt)
        local_consts = _collect_scope_consts(fn_sv.assigns, module_consts)
        csv2 = CallSiteVisitor(iv.import_bindings, local_consts, src.splitlines(), tainted_funcs=tainted)
        for c in fn_sv.calls:
            csv2.visit_Call(c)
        all_hits.extend(csv2.hits)
        all_call_targets |= csv2.call_targets

    # secondary low-trust grep candidate pass (text-level, for recall cross-check only)
    grep_hits = []
    for i, line in enumerate(src.splitlines(), start=1):
        low = line.lower()
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for kw, kind in [("boto3", "LIVE-AWS"), ("kuzu.", "KUZU-CANONICAL"),
                          ("iceberg", "ICEBERG-DIRECT"), ("nessie", "ICEBERG-DIRECT"),
                          ("stitch_graph.json", "FROZEN-SNAPSHOT"),
                          ("graph_contracts.yaml", "FROZEN-SNAPSHOT"),
                          ("estate-coverage-resolver.json", "FROZEN-SNAPSHOT"),
                          (".comp-graph/graph.json", "SOURCE-SCAN"),
                          ('"aws ', "LIVE-AWS"), ("'aws ", "LIVE-AWS"), ("dynamodb", "LIVE-AWS")]:
            if kw in low:
                grep_hits.append({"lineno": i, "kw": kw, "kind": kind})

    return {
        "imports": iv.imports,
        "import_bindings": iv.import_bindings,
        "hits": all_hits,
        "tainted_funcs": tainted,
        "call_targets": all_call_targets,
        "grep_hits": grep_hits,
    }, None


def compute_closure(entry_path: Path, max_depth=10):
    visited = set()
    per_module = {}
    import_edges = []
    errors = []
    queue = [(entry_path, 0)]

    while queue:
        path, depth = queue.pop(0)
        key = str(path.resolve())
        if key in visited or depth > max_depth:
            continue
        visited.add(key)

        analysis, err = analyze_module(path)
        if err:
            errors.append(f"{path}: {err}")
            continue
        per_module[str(path)] = analysis

        for mod, name, lineno, is_from in analysis["imports"]:
            target = resolve_local_module(name if is_from else mod, mod if is_from else None)
            if target:
                import_edges.append((str(path), str(target), lineno, True))
                queue.append((target, depth + 1))
            else:
                import_edges.append((str(path), (mod if is_from else mod), lineno, False))

    return visited, per_module, import_edges, errors


_PATH_PY_RX = re.compile(
    r'(org/[\w./-]+\.py|infra/[\w./-]+\.py|\.tools/[\w./-]+\.py|data/[\w./-]+\.py)\b'
)


def resolve_wrapper_entries(wrapper_path: Path):
    """Robust to ANY bash variable-naming convention for the interpreter
    (`$WORKSPACE`, `${WORKSPACE_ROOT}`, `${COMP_PYTHON:-python}`, ...): match
    on the KNOWN REPO-ROOT-RELATIVE PATH PREFIX itself (org/, infra/,
    .tools/, data/) followed by `.py`, wherever it appears in the wrapper
    text -- not on the syntax that precedes it. v1/v2 anchored on specific
    `python "$WORKSPACE/..."` shapes and silently returned zero entries for
    every wrapper using a differently-named interpreter variable (comp-depth,
    comp-symbols, comp-toolgraph, comp-passcraft, comp-dispatch,
    comp-canon-motif all use `${COMP_PYTHON:-python}` / a bare custom var and
    were entirely unrepresented until this fix -- an entry-resolution miss is
    strictly worse than a call-site miss, since it zeroes the WHOLE tool)."""
    text = wrapper_path.read_text(encoding="utf-8", errors="replace")
    first_line = text.splitlines()[0] if text.splitlines() else ""
    if first_line.startswith("#!") and "python" in first_line:
        entries = [wrapper_path]
        entries.extend(_runpy_shim_targets(wrapper_path, text))
        return entries, text

    entries = []
    for m in _PATH_PY_RX.finditer(text):
        rel = m.group(1)
        p = WS / rel
        if p.is_file() and p not in entries:
            entries.append(p)

    # FOURTH dispatch idiom (comp-genesis): a shim invoking ANOTHER
    # extensionless shim under infra/system/sdk/ (no `.py` at all, so
    # _PATH_PY_RX structurally cannot match), which in turn dispatches to the
    # real `_cli.py`. One more hop: find an extensionless infra/system/sdk/
    # or .tools/ reference and recurse into ITS text for a .py target.
    for m in re.finditer(r'(infra/system/sdk/[\w-]+)\b', text):
        shim = WS / m.group(1)
        if shim.is_file():
            try:
                shim_text = shim.read_text(encoding="utf-8", errors="replace")
                for m2 in _PATH_PY_RX.finditer(shim_text):
                    p2 = WS / m2.group(1)
                    if p2.is_file() and p2 not in entries:
                        entries.append(p2)
                # genesis_cli.py shape: `exec "$py" "$here/genesis_cli.py"` --
                # a BARE filename with none of the 4 known prefixes, resolved
                # relative to the SHIM'S OWN directory (`$here`), not WS.
                # _PATH_PY_RX structurally cannot match this (no org/infra/
                # .tools/data prefix in the text at all); if a shim yields no
                # prefixed match, fall back to a bare `<name>.py` search
                # resolved against the shim's parent dir.
                if not any(WS / mm.group(1) in entries for mm in _PATH_PY_RX.finditer(shim_text)):
                    for m3 in re.finditer(r'([\w-]+\.py)\b', shim_text):
                        p3 = shim.parent / m3.group(1)
                        if p3.is_file() and p3 not in entries:
                            entries.append(p3)
            except Exception:
                pass
    return entries, text


def _runpy_shim_targets(path: Path, text: str) -> list[Path]:
    """THIRD dispatch idiom found by hand-checking the empty-signal tools: a
    'thin PATH wrapper' that does NOT statically `import` its engine at all --
    it resolves an _ENGINE path constant and hands it to
    `runpy.run_path(_ENGINE, run_name='__main__')` (comp-clobber, comp-dups,
    comp-honesty, comp-state, comp-coverage-check all use exactly this shape).
    A depth-1 (or even a naive AST-import) scanner sees a wrapper with almost
    no content and calls it done -- the entire real tool is one dynamic call
    away and invisible to both. Resolve _ENGINE via the SAME const machinery
    used everywhere else, not a new special case."""
    try:
        tree = ast.parse(text, filename=str(path))
    except Exception:
        return []
    if "runpy" not in text:
        return []
    cc = ConstCollector()
    cc.visit(tree)
    targets = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            chain = name_chain(node.func)
            if chain in ("runpy.run_path", "runpy.run_module") and node.args:
                resolved = resolve_expr_text(node.args[0], cc.consts)
                for cand_root in (WS, WS / "org" / "modules" / "graph", WS / "infra" / "aws" / "globgrph"):
                    for piece in resolved.split():
                        if piece.endswith(".py"):
                            p = cand_root / piece if not piece.startswith(str(WS)) else Path(piece)
                            if p.is_file():
                                targets.append(p)
                # also try direct join of collected fragments as a relative path under WS
                joined = "/".join(x for x in resolved.split() if x and x not in ("..",))
                for root in LOCAL_ROOTS:
                    p = root / (joined if joined.endswith(".py") else joined + ".py")
                    if p.is_file() and p not in targets:
                        targets.append(p)
    # de-dup
    seen, uniq = set(), []
    for t in targets:
        if str(t) not in seen:
            uniq.append(t)
            seen.add(str(t))
    return uniq


def scan_bash_wrapper_direct(wrapper_text: str, rel: str):
    """aws/git calls issued DIRECTLY from the bash wrapper (never touching
    python at all) -- comp-stitch-refresh's `aws s3 cp` is this shape.

    BUG FOUND BY THE 3-FP GATE ITSELF: checking `toks[-1]` against the FULL
    line missed the write direction on `aws s3 cp "$ART" "s3://...".. --quiet
    || { echo ERROR; exit 1; }` -- the trailing `|| { ... }` error handler
    makes the line's LAST token `1;`/`}`, not the s3:// destination, so a real
    PRODUCER call read as a false consumer. Exactly the producer-vs-consumer
    class this gate exists to catch, just aimed at my own instrument instead
    of comp-stitch-refresh. Fix: isolate the command up to the first shell
    control-flow operator (`||`, `&&`, `;`, `|`) before tokenizing."""
    hits = []
    for i, line in enumerate(wrapper_text.splitlines(), start=1):
        s = line.strip()
        if s.startswith("#"):
            continue
        m = re.match(r'^aws\s+([a-z0-9-]+)\s+([a-z0-9-]+)', s)
        if m:
            cmd_only = re.split(r'\|\||&&|;|\{', s, maxsplit=1)[0].strip()
            # drop trailing FLAGS (--quiet, --region us-east-1, ...) so the
            # last remaining token is the last real positional arg, not
            # whichever option happened to be typed last (`aws s3 cp SRC DST
            # --quiet` has DST second-to-last once --quiet is stripped), and
            # strip the shell quote characters bash args are wrapped in
            # (`"s3://..."` starts with `"`, not `s` -- .startswith("s3://")
            # silently fails on every quoted arg, which is all of them).
            toks = [t.strip('"\'') for t in cmd_only.split() if not t.startswith("-")]
            is_write = m.group(2) in ("cp", "sync", "put-object", "upload") and toks and toks[-1].startswith("s3://")
            hits.append({"lineno": i, "kind": "LIVE-AWS", "detail": f"bash:{s[:100]}",
                          "is_write": is_write, "module": rel})
    return hits


def enumerate_tool_universe() -> list[str]:
    """Live enumeration -- 91 raw .tools/comp-* files (any extension, no
    .pyc) + pipescript = 92, re-derived at RUN TIME rather than read from a
    frozen scratch list (D.md Sec2's denominator reconciliation). Makes this
    script self-contained: no dependency on a companion file that may not
    exist for a fresh re-run (e.g. CVO~Z's own verification pass)."""
    names = sorted(
        f".tools/{p.name}" for p in (WS / ".tools").iterdir()
        if p.is_file() and p.name.startswith("comp-") and not p.name.endswith(".pyc")
    )
    if (WS / ".tools" / "pipescript").is_file():
        names.append(".tools/pipescript")
    return names


def main():
    names = enumerate_tool_universe()

    report = {}
    for rel in names:
        p = WS / rel
        tool_name = p.name
        result = {"tool": tool_name, "path": rel}
        try:
            entries, wrapper_text = resolve_wrapper_entries(p)
        except Exception as e:
            result["error"] = f"wrapper resolution failed: {e}"
            report[tool_name] = result
            continue

        result["entry_modules"] = [str(e.relative_to(WS)).replace("\\", "/") for e in entries]
        if not entries:
            result["entry_resolution"] = "NONE FOUND -- wrapper text did not match any dispatch pattern"

        all_visited = set()
        all_per_module = {}
        all_edges = []
        all_errors = []
        for entry in entries:
            visited, per_module, edges, errors = compute_closure(entry)
            all_visited |= visited
            all_per_module.update(per_module)
            all_edges.extend(edges)
            all_errors.extend(errors)

        # cross-module taint: a function tainted in module A, called by name
        # from module B (rare but real for shared helpers) -- best-effort:
        # union all tainted-func names across the whole closure, then re-scan
        # each module's call_targets against that union for anything missed.
        global_tainted = {}
        for mod, a in all_per_module.items():
            global_tainted.update(a.get("tainted_funcs", {}))

        result["closure_size"] = len(all_visited)
        result["closure_modules"] = sorted(str(Path(v).relative_to(WS)).replace("\\", "/") for v in all_visited)
        result["errors"] = all_errors
        result["global_tainted_funcs"] = global_tainted

        reads, writes = {}, {}
        unresolved = []  # NEVER silently dropped -- a real Call was detected (open/read/subprocess/
        # tainted-wrapper) but the target text didn't resolve to a known artifact class or was a
        # genuinely dynamic (caller-supplied) path. Surfaced for hand-review, not discarded --
        # dropping these would be the exact "an instrument that cannot find a known-present instance
        # is broken and reporting silence" failure the acceptance gate is designed to catch, just
        # aimed at my own tool instead of the tools it's auditing.
        for mod, a in all_per_module.items():
            for h in a["hits"]:
                kind = h["kind"]
                if kind in ("UNCLASSIFIED-PATH", "UNRESOLVED-PATH-ARG", None):
                    unresolved.append({
                        "module": str(Path(mod).relative_to(WS)).replace("\\", "/"),
                        "lineno": h["lineno"], "detail": h["detail"], "raw_kind": kind,
                        "snippet": h.get("snippet", ""),
                    })
                    continue
                bucket = writes if h.get("is_write") else reads
                bucket.setdefault(kind, []).append({
                    "module": str(Path(mod).relative_to(WS)).replace("\\", "/"),
                    "lineno": h["lineno"], "detail": h["detail"], "meta_only": h.get("meta_only", False),
                })
        result["unresolved_call_sites"] = unresolved

        bash_hits = scan_bash_wrapper_direct(wrapper_text, rel)
        for h in bash_hits:
            bucket = writes if h.get("is_write") else reads
            bucket.setdefault(h["kind"], []).append(
                {"module": rel, "lineno": h["lineno"], "detail": h["detail"], "meta_only": False})

        result["reads_typed"] = reads
        result["writes_typed"] = writes

        # grep candidate cross-check
        grep_candidates = []
        for mod, a in all_per_module.items():
            for g in a.get("grep_hits", []):
                grep_candidates.append({"module": str(Path(mod).relative_to(WS)).replace("\\", "/"),
                                         "lineno": g["lineno"], "kw": g["kw"], "kind": g["kind"]})
        result["grep_candidates"] = grep_candidates

        ast_kinds_found = set(reads.keys()) | set(writes.keys())
        grep_kinds_found = set(g["kind"] for g in grep_candidates)
        missed_by_ast = grep_kinds_found - ast_kinds_found
        result["needs_manual_check"] = bool(missed_by_ast) or not entries or bool(unresolved)
        result["missed_by_ast_kinds"] = sorted(missed_by_ast)

        report[tool_name] = result

    out = WS / "org" / "tier1_exec" / "1.0.0_SA_CTO" / "deliverables" / "NFRA_TOOLUNIFY_CENSUS" / "_classifier_raw_output.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=list), encoding="utf-8")
    print(f"Wrote {out} -- {len(report)} tools processed")

    empty = [t for t, r in report.items() if not r.get("reads_typed") and not r.get("writes_typed") and "error" not in r]
    needs_check = [t for t, r in report.items() if r.get("needs_manual_check")]
    errored = [t for t, r in report.items() if r.get("error") or r.get("errors")]
    print(f"Tools with NO AST-detected reads/writes: {len(empty)} -> {empty}")
    print(f"Tools flagged needs_manual_check (grep found something AST missed, or no entry resolved): {len(needs_check)}")
    print(f"Tools with parse/resolution errors: {len(errored)}")


if __name__ == "__main__":
    main()
