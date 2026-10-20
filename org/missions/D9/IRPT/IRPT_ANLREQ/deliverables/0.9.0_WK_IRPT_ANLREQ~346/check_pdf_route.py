"""AR-y-472 check: the status route's `pdf` method, read by AST from ops/owned_report.py. Stdlib only, offline.

No network, no AWS. The repository root is found from this file's own path (deliverables/<serial>/ is seven levels under it).

  python -I check_pdf_route.py             prints PDF-ROUTE-OK <four properties> and exits 0, or PDF-ROUTE-BAD <why> and exits 1
  python -I check_pdf_route.py --selftest  mutates the source text in memory (two mutants) and prints CONTROL-FIRES and exits 0
                                           only when BOTH mutants read BAD; otherwise CONTROL-SILENT and exits 1

Properties:
  opal_fallback          pdf has the `if opal and ref is None` branch, which resolves the retained Overview through
                         _binding and head, names the `-overview-` logical id, and refuses ANALYSIS_PDF_NOT_RETAINED
  vendor_path_unchanged  every statement of the vendor branch, as it stood before AR-y-472, appears verbatim (AST) in pdf
  sha_bound_to_report    the fallback refuses ANALYSIS_PDF_BINDING when the retained sha differs from the report's sha
  signs_retained_sha     the fallback's sign call takes the retained sha (retained.get('sha256')) as its third argument
"""
import ast
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[7]
SOURCE = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ops" / "owned_report.py"

# The statements of pdf that formed its vendor branch before AR-y-472, verbatim. The docstring is not one of them.
VENDOR_STATEMENTS = '''
report = self.read(principal, request_id, **({"data_firm": data_firm} if data_firm is not None else {}))
opal = _provider(report) == "OPAL_ENGINE"
if opal:
    _require_opal_form(report)
release = report.get("release") if isinstance(report.get("release"), dict) else {}
ref = release.get("protected_pdf_ref")
member = report.get("opal_artifact" if opal else "vendor_artifact")
artifact = member if isinstance(member, dict) else {}
if not isinstance(ref, dict) or ref.get("server_only") is not True:
    raise AnalysisUnavailable("ANALYSIS_PDF_NOT_RETAINED")
sha = ref.get("sha256")
if (not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha) or artifact.get("sha256") != sha
        or type(artifact.get("byte_length")) is not int or artifact["byte_length"] <= 0):
    raise RequestReadRefused("ANALYSIS_PDF_BINDING")
from pdf_link import PdfLinkRefused
try:
    url, expires_at = signer.sign(_data_firm(principal, data_firm), ref.get("storage_key"), sha)
except PdfLinkRefused as exc:
    raise RequestReadRefused(str(exc)) from None
return {"download_route": {"url": url, "expires_at": expires_at}, "sha256": sha,
        "byte_length": artifact["byte_length"]}
'''

OK_LINE = "PDF-ROUTE-OK opal_fallback=yes vendor_path_unchanged=yes sha_bound_to_report=yes signs_retained_sha=yes"


def _pdf_method(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "OwnedAnalysisReader":
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "pdf":
                    return item
    return None


def _fallback_of(method):
    """The top-level `if opal and ref is None:` branch of pdf, or None."""
    for stmt in method.body:
        if isinstance(stmt, ast.If) and ast.unparse(stmt.test) == "opal and ref is None":
            return stmt
    return None


def _assigned_names(block, predicate):
    """Names bound inside the block to an expression whose source satisfies predicate, plain or element-wise (a, b = x, y)."""
    names = set()
    for node in ast.walk(block):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target, value = node.targets[0], node.value
        if isinstance(target, ast.Name) and predicate(ast.unparse(value)):
            names.add(target.id)
        elif (isinstance(target, ast.Tuple) and isinstance(value, ast.Tuple) and len(target.elts) == len(value.elts)):
            for part, expr in zip(target.elts, value.elts):
                if isinstance(part, ast.Name) and predicate(ast.unparse(expr)):
                    names.add(part.id)
    return names


def _calls(block, attr):
    return [node for node in ast.walk(block)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == attr]


def _raises(block, reason):
    for node in ast.walk(block):
        if (isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) and node.exc.args
                and isinstance(node.exc.args[0], ast.Constant) and node.exc.args[0].value == reason):
            return True
    return False


def _opal_fallback(method):
    fallback = _fallback_of(method)
    if fallback is None:
        return ["opal_fallback: pdf has no `if opal and ref is None` branch"]
    reasons = []
    if not _calls(fallback, "_binding"):
        reasons.append("opal_fallback: the fallback resolves no artifact through _binding")
    if not _calls(fallback, "head"):
        reasons.append("opal_fallback: the fallback reads no retained artifact through head")
    if not any(isinstance(node, ast.Constant) and isinstance(node.value, str) and "-overview-" in node.value
               for node in ast.walk(fallback)):
        reasons.append("opal_fallback: the fallback names no `-overview-` logical id")
    if not _raises(fallback, "ANALYSIS_PDF_NOT_RETAINED"):
        reasons.append("opal_fallback: the fallback does not refuse ANALYSIS_PDF_NOT_RETAINED")
    return reasons


def _vendor_path_unchanged(method):
    wrapper = ast.parse("def _vendor():\n" + textwrap.indent(VENDOR_STATEMENTS.strip("\n"), "    ") + "\n")
    present = {ast.dump(node) for node in ast.walk(method) if isinstance(node, ast.stmt)}
    reasons = []
    for stmt in wrapper.body[0].body:
        if ast.dump(stmt) not in present:
            reasons.append("vendor_path_unchanged: vendor statement changed or missing: " + ast.unparse(stmt).splitlines()[0])
    return reasons


def _sha_names(fallback):
    """(names holding the report's sha, names holding the retained sha) assigned inside the fallback."""
    report_names = _assigned_names(fallback, lambda text: "opal_artifact" in text and "sha256" in text)
    retained_names = _assigned_names(fallback, lambda text: text == "retained.get('sha256')")
    return report_names, retained_names


def _sha_bound_to_report(method):
    fallback = _fallback_of(method)
    if fallback is None:
        return ["sha_bound_to_report: no fallback branch"]
    report_names, retained_names = _sha_names(fallback)
    if not report_names or not retained_names:
        return ["sha_bound_to_report: the fallback does not read both the report's sha and the retained sha"]
    for node in ast.walk(fallback):
        if (isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and len(node.test.ops) == 1
                and isinstance(node.test.ops[0], ast.NotEq) and isinstance(node.test.left, ast.Name)
                and isinstance(node.test.comparators[0], ast.Name)):
            pair = {node.test.left.id, node.test.comparators[0].id}
            if (pair & retained_names and pair & report_names and _raises(ast.Module(body=node.body, type_ignores=[]),
                                                                          "ANALYSIS_PDF_BINDING")):
                return []
    return ["sha_bound_to_report: no ANALYSIS_PDF_BINDING refusal on retained sha != report sha"]


def _signs_retained_sha(method):
    fallback = _fallback_of(method)
    if fallback is None:
        return ["signs_retained_sha: no fallback branch"]
    _report_names, retained_names = _sha_names(fallback)
    signs = _calls(fallback, "sign")
    if any(len(call.args) >= 3 and isinstance(call.args[2], ast.Name) and call.args[2].id in retained_names
           for call in signs):
        return []
    return ["signs_retained_sha: the fallback does not sign the retained sha"]


def _checks(source):
    method = _pdf_method(ast.parse(source))
    if method is None:
        return ["NO-PDF-METHOD: OwnedAnalysisReader.pdf not found"]
    return (_opal_fallback(method) + _vendor_path_unchanged(method)
            + _sha_bound_to_report(method) + _signs_retained_sha(method))


def _selftest(source):
    if _checks(source):  # the control is meaningful only if the unmutated source reads clean
        print("CONTROL-SILENT baseline reads BAD: " + "; ".join(_checks(source)))
        return 1
    mutants = {
        "sha_comparison_removed": source.replace("if retained_sha != sha:", "if False:", 1),
        "vendor_branch_altered": source.replace('artifact["byte_length"] <= 0', 'artifact["byte_length"] <= -1', 1),
    }
    silent = []
    for name, mutant in mutants.items():
        if mutant == source:
            silent.append(name + " (not applied)")
        elif not _checks(mutant):
            silent.append(name + " (read OK)")
    if silent:
        print("CONTROL-SILENT " + "; ".join(silent))
        return 1
    print("CONTROL-FIRES")
    return 0


def main(argv):
    if not (ROOT / "org").is_dir() or not SOURCE.is_file():
        print("PDF-ROUTE-BAD source not found at " + str(SOURCE))
        return 1
    source = SOURCE.read_text(encoding="utf-8")
    if "--selftest" in argv:
        return _selftest(source)
    reasons = _checks(source)
    if reasons:
        print("PDF-ROUTE-BAD " + "; ".join(reasons))
        return 1
    print(OK_LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
