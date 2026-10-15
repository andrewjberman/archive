"""IRPT_ANLREQ AR-g-52 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g52_checks.py g52       the replacement rule answers its fourteen cases, and the new test file passes
    python ar_g52_checks.py hygiene   the module is ASCII, imports only the allowed standard library names, opens no connection

Prints one RESULT line: AR-G52-OK / AR-G52-FAIL or AR-G52-HYGIENE-OK / AR-G52-HYGIENE-FAIL; rc 0 only on OK. ASCII only.
"""
import ast
import importlib.util
import itertools
import json
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
MODULE = R + "swap_replacement.py"
TESTS = R + "tests/test_swap_replacement.py"
ALLOWED_IMPORTS = {"__future__", "re", "collections", "typing"}
EQ = {"asset_class": "Equity", "sub_asset_class": "US Large Cap"}
BOND = {"asset_class": "Fixed Income", "sub_asset_class": "Short Term"}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def row(ticker, cls):
    return {"ticker": ticker, **cls}


def days(table):
    """A history_days callable over a dict; a value of 'boom' raises, a missing key answers None."""
    def fn(ticker):
        v = table.get(ticker)
        if v == "boom":
            raise RuntimeError("secret-xyz-token")
        return v
    return fn


def cases(sr):
    out = {}
    pool = [row("AAA", EQ), row("BBB", EQ), row("CCC", EQ), row("DDD", BOND), row("MISS", EQ)]
    def pick(**kw):
        return sr.choose_replacement(**{"missing": "MISS", "classification": EQ, "pool_rows": pool,
                                        "model_proposals": [], "history_days": days({}), **kw})

    # 1: the longest Yahoo history in the same class wins
    r = pick(history_days=days({"AAA": 100, "BBB": 900, "CCC": 400, "DDD": 5000}))
    out["longest history in class wins"] = (r["status"] == "REPLACED" and r["replacement"] == "BBB" and r["proxy_for"] == "MISS"
                                            and r["method"] == "CLASS_LONGEST_YAHOO_HISTORY")
    # 2: a tie is broken by ticker, alphabetically
    r = pick(history_days=days({"CCC": 500, "AAA": 500, "BBB": 500}))
    out["tie goes to the alphabetically first"] = r["replacement"] == "AAA"
    # 3: the same input in any order gives the same answer
    answers = set()
    for perm in itertools.permutations(pool):
        rr = pick(pool_rows=list(perm), history_days=days({"AAA": 500, "BBB": 500, "CCC": 500}))
        answers.add(json.dumps(rr, sort_keys=True))
    out["deterministic over pool order"] = len(answers) == 1
    # 4: a candidate Yahoo does not price (None, 0, negative, non-int, an error) is dropped with a typed reason
    r = pick(history_days=days({"AAA": None, "BBB": 0, "CCC": "boom"}))
    reasons = {d["ticker"]: d["reason"] for d in r["dropped"]}
    out["unpriced dropped, typed"] = (r["status"] == "NO_REPLACEMENT" and r["why"] == "NONE_PRICED"
                                      and reasons.get("AAA") == "NOT_PRICED_BY_YAHOO" and reasons.get("BBB") == "NOT_PRICED_BY_YAHOO"
                                      and reasons.get("CCC") == "HISTORY_ERROR" and "secret-xyz-token" not in json.dumps(r))
    # 5: the missing security itself and other classes are never candidates
    r = pick(history_days=days({"MISS": 99999, "DDD": 99999, "AAA": 10}))
    out["own ticker and other classes excluded"] = r["replacement"] == "AAA" and all(c["ticker"] not in ("MISS", "DDD") for c in r["candidates"])
    # 6: a model proposal that is not in the pool rows, passes the class match through `classify` and is priced WIDENS the pool and can win
    r = pick(model_proposals=["EEE"], classify=lambda t: dict(EQ) if t == "EEE" else None, history_days=days({"AAA": 100, "EEE": 700}))
    c = {x["ticker"]: x["origin"] for x in r["candidates"]}
    out["model proposal widens the pool"] = r["replacement"] == "EEE" and c.get("EEE") == "MODEL" and c.get("AAA") == "CLASSIFICATIONS"
    # 7: a model proposal in the wrong class, or unknown to the classifier, is dropped with its reason and never decides
    r = pick(model_proposals=["DDD", "QQQQ"], history_days=days({"AAA": 100, "DDD": 9000, "QQQQ": 9000}))
    reasons = {d["ticker"]: d["reason"] for d in r["dropped"]}
    out["bad proposals dropped"] = r["replacement"] == "AAA" and reasons.get("DDD") == "CLASS_MISMATCH" and reasons.get("QQQQ") == "NOT_CLASSIFIED"
    # 8: the `classify` callable can class-check a proposal that is not in the pool rows
    r = pick(model_proposals=["FFF"], classify=lambda t: dict(EQ) if t == "FFF" else None, history_days=days({"AAA": 100, "FFF": 800}))
    out["classify callable admits a proposal"] = r["replacement"] == "FFF"
    # 9: a proposal that is also a pool candidate has origin BOTH and is listed once
    r = pick(model_proposals=["BBB"], history_days=days({"AAA": 100, "BBB": 200}))
    both = [x for x in r["candidates"] if x["ticker"] == "BBB"]
    out["origin BOTH, listed once"] = len(both) == 1 and both[0]["origin"] == "BOTH"
    # 10: the model cannot change the pick when its proposals add nothing that passes
    base = pick(history_days=days({"AAA": 100, "BBB": 900}))["replacement"]
    noisy = pick(model_proposals=["DDD", "ZZZ", "AAA", "", None, 7], history_days=days({"AAA": 100, "BBB": 900, "DDD": 99999, "ZZZ": 99999}))
    out["noise never decides"] = noisy["replacement"] == base == "BBB"
    # 11: no class on the missing security -> NO_REPLACEMENT, why NO_CLASS, and the sentence names the omission
    for bad in (None, {}, {"asset_class": "Equity"}, {"asset_class": "", "sub_asset_class": ""}):
        r = pick(classification=bad, history_days=days({"AAA": 100}))
        if not (r["status"] == "NO_REPLACEMENT" and r["why"] == "NO_CLASS" and r["replacement"] is None):
            out["no class refuses"] = False
            break
    else:
        out["no class refuses"] = "without it" in r["named"]
    # 12: no candidate at all -> NO_REPLACEMENT, why NO_CANDIDATE
    r = pick(pool_rows=[row("MISS", EQ), row("DDD", BOND)], history_days=days({"DDD": 100}))
    out["no candidate"] = r["status"] == "NO_REPLACEMENT" and r["why"] == "NO_CANDIDATE"
    # 13: class comparison ignores case and surrounding blanks, and the record names proxy_for, method, confidence
    r = pick(pool_rows=[{"ticker": "aaa ", "asset_class": " equity", "sub_asset_class": "US LARGE CAP "}], history_days=days({"AAA": 5}))
    out["class match ignores case and blanks"] = (r["replacement"] == "AAA" and r["confidence"] == "CLASS_MATCH_PRICED"
                                                   and "AAA" in r["named"] and "MISS" in r["named"])
    # 14: a model-only winner carries the model confidence word
    r = pick(model_proposals=["EEE"], classify=lambda t: dict(EQ) if t == "EEE" else None, history_days=days({"EEE": 700}))
    out["model-only confidence"] = r["confidence"] == "CLASS_MATCH_PRICED_MODEL_PROPOSED" and r["replacement"] == "EEE"
    return out


def main(mode):
    if mode == "g52":
        try:
            spec = importlib.util.spec_from_file_location("swap_replacement", MODULE)
            sr = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(sr)
            sr.choose_replacement
        except Exception as exc:
            print("AR-G52-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(sr)
        except Exception as exc:
            print("AR-G52-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:200]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        rc, line, passed = pytest_line(TESTS)
        print("cases %d, wrong %s" % (len(got), wrong or "none"))
        print("worker tests: %s" % line)
        if wrong or rc != 0 or bad_count(line) or passed < 8:
            print("AR-G52-FAIL wrong=%s tests rc=%d passed=%d (need >= 8)" % (wrong or "none", rc, passed))
            return 1
        print("AR-G52-OK cases=%d tests=%d" % (len(got), passed))
        return 0
    if mode == "hygiene":
        try:
            with open(MODULE, "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            print("AR-G52-HYGIENE-FAIL no module: %s" % type(exc).__name__)
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
            print("AR-G52-HYGIENE-FAIL " + "; ".join(problems))
            return 1
        print("AR-G52-HYGIENE-OK imports=%s" % ",".join(sorted(imported)))
        return 0
    print("usage: ar_g52_checks.py g52|hygiene")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
