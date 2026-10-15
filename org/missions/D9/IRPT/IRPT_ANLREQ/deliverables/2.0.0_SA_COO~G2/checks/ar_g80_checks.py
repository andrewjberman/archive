"""IRPT_ANLREQ AR-g-80 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g80_checks.py g80       the total-return level helper answers its ten cases, and the new test file passes
    python ar_g80_checks.py hygiene   the module is ASCII, imports only the allowed standard library names, opens no connection

Prints one RESULT line: AR-G80-OK / AR-G80-FAIL or AR-G80-HYGIENE-OK / AR-G80-HYGIENE-FAIL; rc 0 only on OK. ASCII only.
"""
import ast
import importlib.util
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
MODULE = R + "tr_level.py"
TESTS = R + "tests/test_tr_level.py"
ALLOWED_IMPORTS = {"__future__", "math", "datetime", "re", "collections", "typing"}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def close(a, b):
    return abs(a - b) <= 1e-9 * max(1.0, abs(b))


def cases(m):
    out = {}
    d1, d2, d3, d4 = "2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15"

    # 1: level_0 = base at the first retained date; level_t = level_(t-1) * (1 + r_t); the first row's own return is not applied
    r = m.chain_levels([(d1, 0.5), (d2, 0.10), (d3, -0.05), (d4, 0.0)])
    want = [[d1, 100.0], [d2, 110.0], [d3, 104.5], [d4, 104.5]]
    out["chain from base"] = len(r) == 4 and all(a[0] == b[0] and close(a[1], b[1]) for a, b in zip(r, want))
    # 2: a custom base
    r = m.chain_levels([(d1, None), (d2, 0.5)], base=200.0)
    out["custom base"] = len(r) == 1 and r[0][0] == d2 and close(r[0][1], 200.0)
    # 3: a row with no usable return (None, NaN, inf, bool, text, <= -1) is dropped; the first retained row seeds the base
    r = m.chain_levels([(d1, None), (d2, float("nan")), (d3, 0.02), (d4, -1.0)])
    out["unusable returns dropped, never seed"] = r == [[d3, 100.0]]
    # 4: input order does not matter; a repeated date keeps the later value
    r = m.chain_levels([(d3, 0.1), (d1, 0.0), (d2, 0.1), (d2, 0.2)])
    want = [[d1, 100.0], [d2, 120.0], [d3, 132.0]]
    out["sorted, repeat keeps later"] = len(r) == 3 and all(a[0] == b[0] and close(a[1], b[1]) for a, b in zip(r, want))
    # 5: a bad date is dropped like any bad row
    r = m.chain_levels([("2026-02-30", 0.1), ("bad", 0.1), (d1, 0.0), (d2, 0.1)])
    out["bad dates dropped"] = [x[0] for x in r] == [d1, d2]
    # 6: empty and all-bad input give []
    out["empty"] = m.chain_levels([]) == [] and m.chain_levels([(d1, None)]) == [] and m.chain_levels(None) == []
    # 7: returns_from_levels: L_t / L_(t-1) - 1 from the second row on; non-positive levels are skipped
    r = m.returns_from_levels([(d1, 10.0), (d2, 11.0), (d3, 0.0), (d4, 12.1)])
    out["returns from levels"] = [x[0] for x in r] == [d2, d4] and close(r[0][1], 0.1) and close(r[1][1], 12.1 / 11.0 - 1.0)
    # 8: a levels series round-trips through returns and back to the same shape (scaled to base 100)
    levels = [(d1, 50.0), (d2, 55.0), (d3, 49.5)]
    back = m.chain_levels(m.returns_from_levels(levels))
    out["round trip"] = ([x[0] for x in back] == [d2, d3] and close(back[0][1], 100.0) and close(back[1][1], 90.0))
    # 9: the inputs are not changed and the output rows are new lists
    given = [(d1, 0.0), (d2, 0.1)]
    copy = list(given)
    r = m.chain_levels(given)
    out["inputs untouched"] = given == copy and isinstance(r[0], list)
    # 10: output levels are floats
    out["float levels"] = all(isinstance(x[1], float) for x in m.chain_levels([(d1, 0.0), (d2, 1)]))
    return out


def main(mode):
    if mode == "g80":
        try:
            spec = importlib.util.spec_from_file_location("tr_level", MODULE)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            m.chain_levels
            m.returns_from_levels
        except Exception as exc:
            print("AR-G80-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(m)
        except Exception as exc:
            print("AR-G80-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:200]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        rc, line, passed = pytest_line(TESTS)
        print("cases %d, wrong %s" % (len(got), wrong or "none"))
        print("worker tests: %s" % line)
        if wrong or rc != 0 or bad_count(line) or passed < 6:
            print("AR-G80-FAIL wrong=%s tests rc=%d passed=%d (need >= 6)" % (wrong or "none", rc, passed))
            return 1
        print("AR-G80-OK cases=%d tests=%d" % (len(got), passed))
        return 0
    if mode == "hygiene":
        try:
            with open(MODULE, "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            print("AR-G80-HYGIENE-FAIL no module: %s" % type(exc).__name__)
            return 1
        problems = []
        if any(b > 127 for b in raw):
            problems.append("non-ASCII byte")
        tree = ast.parse(raw.decode("utf-8", errors="replace"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
        extra = sorted(imported - ALLOWED_IMPORTS)
        if extra:
            problems.append("imports outside the allowed set: %s" % ",".join(extra))
        calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        for forbidden in ("open", "print", "exec", "eval", "__import__"):
            if forbidden in calls:
                problems.append("calls %s" % forbidden)
        if problems:
            print("AR-G80-HYGIENE-FAIL " + "; ".join(problems))
            return 1
        print("AR-G80-HYGIENE-OK imports=%s" % ",".join(sorted(imported)))
        return 0
    print("usage: ar_g80_checks.py g80|hygiene")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
