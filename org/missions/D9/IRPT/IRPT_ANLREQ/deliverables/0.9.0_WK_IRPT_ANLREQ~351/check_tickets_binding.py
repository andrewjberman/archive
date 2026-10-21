"""IRPT_ANLREQ AR-y-483 (worker 0.9.0_WK_IRPT_ANLREQ~351): the resident reads the ticket table from the optional pinned
binding `tickets_table`, never from the environment variable IRPT_TICKETS_TABLE.

Stdlib only, offline, no AWS, no network. It reads the source text of reports/resident_installed.py from this worktree
(the worktree is clean at the commit that carries the change, so that text is the text at HEAD) and grades four things:

    env_read              no IRPT_TICKETS_TABLE / TICKETS_TABLE_ENV, and no os.environ read in or near a tickets_table line
    optional_binding      load_bindings treats "tickets_table" as an optional key (in the document, not required)
    refusal               ResidentInstallRefused("TICKETS_TABLE_INVALID") is raised for a malformed value
    reaches_make_packager the make_packager call in build_resident_runtime passes tickets_table=bindings.get("tickets_table")

    python -I check_tickets_binding.py              -> TICKETS-BINDING-OK ... (rc 0)  or  TICKETS-BINDING-BAD <why> (rc 1)
    python -I check_tickets_binding.py --selftest   -> CONTROL-FIRES (rc 0)  only when all three mutants read BAD

ASCII only.
"""
import ast
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]  # .../org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>/ -> the worktree root
SOURCE = ROOT / "infra/aws/lambda/investor-reporting/reports/resident_installed.py"
REFUSAL = "TICKETS_TABLE_INVALID"
CALL_ARG = "tickets_table=bindings.get(TICKETS_TABLE_BINDING)"


def env_read_present(text):
    """True when the retired variable is named, or an environment read sits within three lines of a tickets_table line."""
    if "IRPT_TICKETS_TABLE" in text or "TICKETS_TABLE_ENV" in text:
        return True
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if re.search(r"tickets_table|TICKETS_TABLE", line, re.IGNORECASE):
            window = lines[max(0, idx - 3): idx + 4]
            if any(re.search(r"os\.environ|getenv|environ\.get", window_line) for window_line in window):
                return True
    return False


def optional_binding_present(text):
    """True when load_bindings tests the presence of the tickets_table key (an optional binding, not a required one)."""
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "load_bindings":
            segment = ast.get_source_segment(text, node) or ""
            return re.search(r'(?:"tickets_table"|TICKETS_TABLE_BINDING)\s+in\s+document', segment) is not None
    return False


def refusal_present(text):
    """True when the refusal text is raised as ResidentInstallRefused(...) for the ticket table."""
    return re.search(r'ResidentInstallRefused\(\s*"' + REFUSAL + r'"\s*\)', text) is not None


def reaches_make_packager(text):
    """True when a make_packager(...) call passes tickets_table=bindings.get("tickets_table") (or the constant)."""
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "make_packager":
            continue
        for keyword in node.keywords:
            if keyword.arg != "tickets_table":
                continue
            value = keyword.value
            if (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute)
                    and value.func.attr == "get" and isinstance(value.func.value, ast.Name)
                    and value.func.value.id == "bindings" and len(value.args) == 1 and not value.keywords):
                arg = value.args[0]
                if (isinstance(arg, ast.Constant) and arg.value == "tickets_table") or (
                        isinstance(arg, ast.Name) and arg.id == "TICKETS_TABLE_BINDING"):
                    return True
    return False


def grade(text):
    """-> (failures, facts): failures is a list of reasons (empty when the change holds)."""
    failures = []
    env = env_read_present(text)
    optional = optional_binding_present(text)
    refusal = refusal_present(text)
    reaches = reaches_make_packager(text)
    if env:
        failures.append("env_read=yes")
    if not optional:
        failures.append("optional_binding=no")
    if not refusal:
        failures.append("refusal=absent")
    if not reaches:
        failures.append("reaches_make_packager=no")
    facts = {"env_read": "yes" if env else "no", "optional_binding": "yes" if optional else "no",
             "refusal": REFUSAL if refusal else "absent", "reaches_make_packager": "yes" if reaches else "no"}
    return failures, facts


def mutants(text):
    """-> {name: mutated text}. Each mutant is the HEAD text with one defect put back."""
    return {
        "env_read_put_back": text.replace(CALL_ARG, 'tickets_table=os.environ.get("IRPT_TICKETS_TABLE")'),
        "refusal_text_removed": text.replace('"' + REFUSAL + '"', '"TICKETS_INVALID"'),
        "make_packager_arg_none": text.replace(CALL_ARG, "tickets_table=None"),
    }


def selftest(text):
    """Each mutant must apply to the text and read BAD; CONTROL-FIRES only when all three do."""
    if grade(text)[0]:
        sys.stderr.write("CONTROL-MISS the unmutated text already reads BAD\n")
        return 1
    missed = []
    for name, mutated in mutants(text).items():
        if mutated == text:
            missed.append(name + "(not applied)")
            continue
        failures, _ = grade(mutated)
        sys.stderr.write("mutant " + name + ": " + ("BAD " + "; ".join(failures) if failures else "READS-OK") + "\n")
        if not failures:
            missed.append(name)
    if missed:
        sys.stderr.write("CONTROL-MISS " + ", ".join(missed) + "\n")
        return 1
    print("CONTROL-FIRES")
    return 0


def main(argv):
    text = SOURCE.read_text(encoding="utf-8")
    if "--selftest" in argv:
        return selftest(text)
    failures, facts = grade(text)
    if failures:
        print("TICKETS-BINDING-BAD " + "; ".join(failures))
        return 1
    print("TICKETS-BINDING-OK env_read=" + facts["env_read"] + " optional_binding=" + facts["optional_binding"]
          + " refusal=" + facts["refusal"] + " reaches_make_packager=" + facts["reaches_make_packager"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
