"""AR-y-470 check: the commentary PDF route binds by the logical id and signs the retained PDF's own sha256.

Reads infra/aws/lambda/investor-reporting/ops/owned_report.py BY AST (stdlib only, offline, no AWS, no network).
Prints COMMENTARY-BINDING-OK <flags> and exits 0 when commentary_pdf has the new checks, or COMMENTARY-BINDING-BAD <why>
and exits 1 otherwise.

--selftest mutates the source text in memory (the old sha comparison put back; the sign call given the draft sha) and
prints CONTROL-FIRES only when BOTH mutants read BAD; otherwise it prints CONTROL-MISSED and exits 1.
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
TARGET = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ops" / "owned_report.py"
METHOD = "commentary_pdf"
HEX64 = "[0-9a-f]{64}"
OK_FLAGS = ("family", "length", "sha_hex", "signs_own_sha", "draft_sha_compare_gone")


def _method(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == METHOD:
            return node
    return None


def _bindings(fn):
    """Name -> the value it was assigned, including the tuple form `a, b = x, y`."""
    out = {}
    for node in ast.walk(fn):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name):
                out[target.id] = node.value
            elif (isinstance(target, ast.Tuple) and isinstance(node.value, ast.Tuple)
                    and len(target.elts) == len(node.value.elts)):
                for elt, value in zip(target.elts, node.value.elts):
                    if isinstance(elt, ast.Name):
                        out[elt.id] = value
    return out


def _resolve(expr, bindings):
    if isinstance(expr, ast.Name) and expr.id in bindings:
        return bindings[expr.id]
    return expr


def _retained_field(expr, field, bindings):
    """True when expr (after one resolution of a local name) is retained.get('field') or retained['field']."""
    text = ast.unparse(_resolve(expr, bindings))
    return text in ("retained.get('%s')" % field, "retained['%s']" % field)


def _is_name(expr, name):
    return isinstance(expr, ast.Name) and expr.id == name


def _compares(fn):
    return [node for node in ast.walk(fn) if isinstance(node, ast.Compare)]


def _calls(fn):
    return [node for node in ast.walk(fn) if isinstance(node, ast.Call)]


def analyse(source):
    """Return (flags, why): flags maps each of OK_FLAGS to a bool; why names the first missing check or is None."""
    tree = ast.parse(source)
    fn = _method(tree)
    if fn is None:
        return {flag: False for flag in OK_FLAGS}, "no commentary_pdf method"
    bindings = _bindings(fn)
    compares = _compares(fn)
    calls = _calls(fn)

    family = False
    length_type = length_floor = False
    for node in compares:
        if len(node.ops) == 1 and isinstance(node.ops[0], ast.NotEq):
            sides = [node.left, node.comparators[0]]
            if (any(_retained_field(side, "family", bindings) for side in sides)
                    and any(_is_name(side, "COMMENTARY_FAMILY") for side in sides)):
                family = True
        if len(node.ops) == 1 and isinstance(node.ops[0], ast.IsNot):
            left = _resolve(node.left, bindings)
            if (isinstance(left, ast.Call) and isinstance(left.func, ast.Name) and left.func.id == "type"
                    and left.args and _retained_field(left.args[0], "byte_length", bindings)
                    and _is_name(node.comparators[0], "int")):
                length_type = True
        if len(node.ops) == 1 and isinstance(node.ops[0], ast.LtE):
            if (_retained_field(node.left, "byte_length", bindings) and isinstance(node.comparators[0], ast.Constant)
                    and node.comparators[0].value == 0):
                length_floor = True

    sha_hex = any(isinstance(call.func, ast.Attribute) and call.func.attr == "fullmatch" and len(call.args) == 2
                  and isinstance(call.args[0], ast.Constant) and call.args[0].value == HEX64
                  and _retained_field(call.args[1], "sha256", bindings) for call in calls)

    signs_own = any(isinstance(call.func, ast.Attribute) and call.func.attr == "sign" and len(call.args) >= 3
                    and _retained_field(call.args[2], "sha256", bindings) for call in calls)

    draft_compare = False
    for node in compares:
        sides = [node.left] + list(node.comparators)
        if any(_is_name(side, "sha") for side in sides):
            others = [side for side in sides if not _is_name(side, "sha")]
            if any("retained" in ast.unparse(_resolve(side, bindings)) for side in others):
                draft_compare = True
    draft_signed = any(isinstance(call.func, ast.Attribute) and call.func.attr == "sign" and len(call.args) >= 3
                       and _is_name(call.args[2], "sha") for call in calls)

    flags = {"family": family, "length": length_type and length_floor, "sha_hex": sha_hex,
             "signs_own_sha": signs_own and not draft_signed, "draft_sha_compare_gone": not draft_compare}
    missing = [flag for flag in OK_FLAGS if not flags[flag]]
    return flags, (None if not missing else "missing or failing: " + ",".join(missing))


def verdict(source):
    flags, why = analyse(source)
    if why is None:
        return True, "COMMENTARY-BINDING-OK " + " ".join("%s=yes" % flag for flag in OK_FLAGS)
    return False, "COMMENTARY-BINDING-BAD " + why


def selftest(source):
    """Two mutants of the CURRENT source; each must read BAD for the control to fire."""
    new_guard = 'if (retained.get("family") != COMMENTARY_FAMILY'
    new_sign = "signer.sign(firm, key, retained_sha, COMMENTARY_FAMILY)"
    if source.count(new_guard) != 1 or source.count(new_sign) != 1:
        return False, "CONTROL-MISSED mutation anchors not found once in the source"
    old_comparison = source.replace(
        new_guard, 'if (retained.get("sha256") != sha or retained.get("family") != COMMENTARY_FAMILY', 1)
    draft_signed = source.replace(new_sign, "signer.sign(firm, key, sha, COMMENTARY_FAMILY)", 1)
    old_ok, _old_line = verdict(old_comparison)
    draft_ok, _draft_line = verdict(draft_signed)
    if not old_ok and not draft_ok:
        return True, "CONTROL-FIRES"
    return False, "CONTROL-MISSED both mutants must read BAD"


def main(argv):
    source = TARGET.read_text(encoding="utf-8")
    if "--selftest" in argv:
        fired, line = selftest(source)
        print(line)
        return 0 if fired else 1
    ok, line = verdict(source)
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
