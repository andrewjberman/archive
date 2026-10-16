"""IRPT_DASHBD round 135, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the INFLECTION TRANSACTION STEP in the Orion gold DISPATCH chain (CTO msg 9486).

  DB-f-2103 (~2103) `data/inf/scripts/gold/orion-gold-dispatch.sh` gains, by PURE INSERTION (one line of the unknown-chain error message gains the word txn), the step
                    INF_G_01 as a BEST-EFFORT, POST-SENTINEL block beside the Eclipse block (Andrew directive 2026-05-15: the portal publish is never gated on a new, unserved
                    table): a catalog row, `CHAIN_TXN`, `run_txn_step`, a `--chain txn` entry and its help line, and a TXN-BLOCK that runs after the Eclipse block and before the
                    auto-shutdown, writes a status marker, and never changes chain_exit. INF_G_01 is in none of the full, incremental, compute or gold-stage chains.
                    DBF135-3-AC1

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import difflib
import hashlib
import re
import subprocess
import sys
from pathlib import Path

DISPATCH = "data/inf/scripts/gold/orion-gold-dispatch.sh"
BASE = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r135/dispatch_base.sh.txt"
BASE_SHA256 = "e9aef66bc8a4a883196a2ba61567e56e645d4ffba82cfc74705cb6e270d59e43"
TESTS = "data/inf/scripts/gold/tests/test_dispatch_txn_block.py"
EXISTING_TESTS = ("data/inf/scripts/gold/tests/test_aor_resolution.py", "data/inf/scripts/gold/tests/test_aor_fold_derivation.py",
                  "data/inf/manual_api/test_pull_inflection_scope_account_returns.py")
ROW = "INF_G_01|INF_G_01.account_transaction_gold.py|--upload --date {date}"
ERR_OLD = "(valid: full, incremental, silver-prep, gold-a, gold-b, gold-c, gold-d, gold-cd, eclipse, partial)"
ERR_NEW = "(valid: full, incremental, silver-prep, gold-a, gold-b, gold-c, gold-d, gold-cd, eclipse, txn, partial)"
MARKER = "gold/irpt_txn/_meta/dispatch_txn_status.json"
CHAIN_VARS = ("CHAIN_PULL", "CHAIN_COMPUTE", "CHAIN_FULL", "CHAIN_INCREMENTAL", "CHAIN_GOLD_A", "CHAIN_GOLD_B", "CHAIN_GOLD_C", "CHAIN_GOLD_D", "CHAIN_GOLD_CD",
              "CHAIN_SILVER_PREP", "CHAIN_ECLIPSE")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def non_ascii_added(base, new):
    """The lines the edit ADDS that carry a non-ASCII character (the pinned base holds non-ASCII lines of its own, which stay)."""
    out = []
    for d in difflib.unified_diff(base.splitlines(), new.splitlines(), lineterm="", n=0):
        if d.startswith("+") and not d.startswith("+++") and not d.isascii():
            out.append(d[1:100])
    return out


def diff_problems(base, new):
    """The edit is a pure insertion, but for the one error-message line that gains the word txn."""
    pr = []
    removed = []
    added = []
    for d in difflib.unified_diff(base.splitlines(), new.splitlines(), lineterm="", n=0):
        if d.startswith("---") or d.startswith("+++") or d.startswith("@@"):
            continue
        (removed if d.startswith("-") else added).append(d[1:])
    for r in removed:
        if ERR_OLD not in r:
            pr.append("a base line was removed or changed: %r" % r[:100])
            continue
        want = r.replace(ERR_OLD, ERR_NEW)
        if want not in added:
            pr.append("the unknown-chain message must gain only the word txn: %r" % r[:100])
    return pr


def block_problems(text):
    pr = []
    lines = text.splitlines()
    catalog = text[text.index("read -r -d '' CATALOG"):text.index("CATALOG_END\n", text.index("read -r -d '' CATALOG") + 30)]
    if catalog.splitlines().count(ROW) != 1:
        pr.append("the catalog must hold the row %r exactly once" % ROW)
    else:
        rows = catalog.splitlines()
        if rows.index(ROW) < rows.index("INF_E_00|INF_E_00.eclipse_model_portfolios.py|--date {date} --upload"):
            pr.append("the INF_G_01 row must come after the INF_E_00 row")
    if not re.search(r'^CHAIN_TXN="INF_G_01"$', text, re.M):
        pr.append('CHAIN_TXN="INF_G_01" is missing')
    for v in CHAIN_VARS:
        for m in re.finditer(r'^%s="([^"]*)"$' % v, text, re.M):
            if "INF_G_01" in m.group(1).split() or "CHAIN_TXN" in m.group(1):
                pr.append("%s must not carry INF_G_01 (the step runs only in the post-sentinel block and under --chain txn)" % v)
    if "run_txn_step()" not in text or 'TXN_STEP_TIMEOUT="${TXN_STEP_TIMEOUT:-1800}"' not in text:
        pr.append('run_txn_step() and TXN_STEP_TIMEOUT="${TXN_STEP_TIMEOUT:-1800}" must be defined')
    else:
        body = text[text.index("run_txn_step()"):]
        body = body[:body.index("\n}\n") + 3]
        for token in ('timeout -k 60 "$TXN_STEP_TIMEOUT"', "TXN_RESULTS", "return 0"):
            if token not in body:
                pr.append("run_txn_step must carry %r (timeout-bounded, results recorded, never non-zero)" % token)
        if "return $rc" in body or "exit " in body:
            pr.append("run_txn_step must never return non-zero or exit")
    if not re.search(r'^\s+txn\)\s+SCRIPT_IDS="\$CHAIN_TXN";\s+CHAIN_LABEL="chain:txn" ;;$', text, re.M):
        pr.append('the --chain case entry txn) SCRIPT_IDS="$CHAIN_TXN"; CHAIN_LABEL="chain:txn" ;; is missing')
    if not re.search(r"^  txn\s+.*INF_G_01", text, re.M):
        pr.append("show_help must list the chain txn with INF_G_01")
    if ERR_NEW not in text:
        pr.append("the unknown-chain message must list txn")
    ecl = text.find("ECLIPSE-BLOCK (best-effort, post-sentinel)")
    txn = text.find("TXN-BLOCK (best-effort, post-sentinel)")
    shutdown = text.find("# Auto-shutdown: fires after all modes")
    if not (0 < ecl < txn < shutdown):
        pr.append("the TXN-BLOCK must come after the ECLIPSE-BLOCK and before the auto-shutdown")
    else:
        seg = text[txn - 600:txn + 2400]
        for token in ('[ "$MODE" = "chain" ]', '[ "$TARGET" = "full" ]', '[ "$TARGET" = "incremental" ]', '[ "$DRY_RUN" = "0" ]', "for _txn_id in $CHAIN_TXN", "run_txn_step", MARKER,
                      "does NOT affect chain_exit"):
            if token not in text[txn - 600:txn + 4200]:
                pr.append("the TXN-BLOCK must carry %r" % token)
        del seg
    del lines
    return pr


def ac1(root):
    new = Path(root, DISPATCH).read_text(encoding="utf-8")
    base_p = Path(root, BASE)
    need(base_p.is_file(), "missing the pinned base copy " + BASE)
    base = base_p.read_text(encoding="utf-8")
    need(hashlib.sha256(base.encode("utf-8")).hexdigest() == BASE_SHA256, "the pinned base copy is not the base the order names (sha256)")
    pr = diff_problems(base, new) + block_problems(new)
    need(not pr, "; ".join(pr[:6]))
    run = subprocess.run(["bash", "-n", str(Path(root, DISPATCH))], capture_output=True, text=True, timeout=120)
    need(run.returncode == 0, "bash -n failed: %s" % (run.stderr or "")[:200])
    na = non_ascii_added(base, new)
    need(not na, "every line the edit adds must be ASCII (the base's own non-ASCII lines stay): %r" % (na[:2],))
    tp = Path(root, TESTS)
    need(tp.is_file(), "missing " + TESTS)
    names = re.findall(r"^def (test_\w+)", tp.read_text(encoding="utf-8"), re.M)
    need(len(names) >= 12, "the dispatch test file must hold at least 12 tests (found %d)" % len(names))
    low = " | ".join(names).lower()
    for w in ("catalog", "chain", "block", "sentinel", "shutdown", "insertion", "syntax", "date"):
        need(w in low, "the dispatch test names lack %r" % w)
    for t in (TESTS,) + EXISTING_TESTS:
        run = subprocess.run([sys.executable, "-m", "pytest", t, "-q", "-p", "no:cacheprovider"], cwd=str(root), capture_output=True, text=True, timeout=600)
        need(run.returncode == 0, "pytest %s failed: %s" % (t, (run.stdout or "")[-250:]))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    base = "a\nb\nerror %s\nc\n" % ERR_OLD
    arm("diff-pure-insertion", diff_problems(base, "a\nNEW\nb\nerror %s\nc\n" % ERR_NEW), [])
    arm("diff-error-line-only", diff_problems(base, "a\nb\nerror %s\nc\n" % ERR_NEW), [])
    arm("diff-removed-line", len(diff_problems(base, "a\nerror %s\nc\n" % ERR_OLD)), 1)
    arm("diff-changed-line", len(diff_problems(base, "a\nB\nerror %s\nc\n" % ERR_OLD)), 1)
    arm("diff-error-line-changed-more", len(diff_problems(base, "a\nb\nerror (valid: x)\nc\n")), 1)
    arm("constants", (ROW.split("|")[0], "{date}" in ROW, MARKER.endswith(".json")), ("INF_G_01", True, True))
    arm("base-sha-form", len(BASE_SHA256), 64)
    e = chr(233)
    nl = chr(10)
    arm("ascii-added-only-green", non_ascii_added("caf" + e + nl + "b" + nl, "caf" + e + nl + "b" + nl + "c" + nl), [])
    arm("ascii-added-red", len(non_ascii_added("a" + nl, "a" + nl + "c" + e + nl)), 1)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    if ac != "DBF135-3-AC1":
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        ac1(root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
