"""HVST-p-2 AC2 evidence: each mutant restores a BASE behaviour in the fixed code; the p2 test file
must fail at least one test under it. The file under mutation is restored byte-for-byte in a
`finally` (sha256 checked before and after).

Run: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~67/scripts/p2_mutants.py
"""

import hashlib
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True, check=True)
            .stdout.decode().strip())
TESTS = "lib/opal_data_harvest/test_p2_fetched_and_stored_keys.py"
W = "lib/opal_data_harvest/worker.py"
P = "lib/opal_data_harvest/publishers.py"

MUTANTS = [
    # (name, file, base behaviour restored, old text, new text)
    ("M1 rejected fetch counted fetched again (a)", W, "the reject branch records no outcome, as at base",
     'note_outcome(result, article.get("fetch_key"), OUTCOME_REJECTED,\n                                             issues=list(article["issues"]))',
     "pass"),
    ("M2 run record ignores outcomes (a)", W, "every job fetched_key is keys_fetched, as at base",
     "                outcome = outcomes.get(key) or {}\n", "                outcome = {}\n"),
    ("M3 no stored join recorded (b)", W, "a stored article records no fetch-key -> article-key pair, as at base",
     'note_outcome(result, article.get("fetch_key"), OUTCOME_STORED, article_key=article_key)', "pass"),
    ("M4 articles are not tagged with their fetch key (a+b)", P, "the client tags no article, as at base",
     'article["fetch_key"] = self._last_fetch_key', "pass"),
    ("M5 unresolved fetches stay counted fetched (a)", W, "a fetched key with no outcome is not named, as at base",
     "        if tagged:\n", "        if False:\n"),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_tests():
    proc = subprocess.run([sys.executable, "-m", "pytest", TESTS, "-q", "-p", "no:cacheprovider", "--tb=no",
                           "--color=no", "-rf"], cwd=REPO, capture_output=True)
    out = proc.stdout.decode("utf-8", "replace")
    failed = re.findall(r"^FAILED (\S+)", out, re.M)
    summary = [line for line in out.splitlines() if re.search(r"\d+ (passed|failed)", line)]
    return proc.returncode, failed, (summary[-1].strip() if summary else "?")


rc, failed, summary = run_tests()
print("CONTROL (unmutated fixed code): rc=%d  %s" % (rc, summary))
assert rc == 0 and not failed
killed = 0
for name, rel, base, old, new in MUTANTS:
    path = REPO / rel
    original = path.read_bytes()
    before = hashlib.sha256(original).hexdigest()
    text = original.decode("utf-8")
    assert text.count(old) == 1, "mutation site for %s not unique (%d)" % (name, text.count(old))
    try:
        path.write_bytes(text.replace(old, new).encode("utf-8"))
        rc, failed, summary = run_tests()
    finally:
        path.write_bytes(original)
    assert sha(path) == before, "restore failed for " + rel
    print("\n%s\n  restores: %s\n  rc=%d  %s" % (name, base, rc, summary))
    for test in failed:
        print("    FAILED " + test.split("::", 1)[-1])
    if rc != 0 and failed:
        killed += 1
# M0: BOTH files at their exact BASE bytes (b635dadc66) -- the p2 tests against the base code itself.
saved = {rel: (REPO / rel).read_bytes() for rel in (W, P)}
try:
    for rel in saved:
        (REPO / rel).write_bytes(subprocess.run(["git", "show", "b635dadc66:" + rel], cwd=REPO, capture_output=True,
                                                check=True).stdout)
    rc, failed, summary = run_tests()
finally:
    for rel, data in saved.items():
        (REPO / rel).write_bytes(data)
print("\nM0 the p2 tests against the BASE worker.py + publishers.py (b635dadc66)\n  rc=%d  %s" % (rc, summary))
for test in failed:
    print("    FAILED " + test.split("::", 1)[-1])
assert rc != 0

print("\nMUTANTS KILLED: %d of %d (each failed at least one test); files restored byte-identical" % (killed, len(MUTANTS)))
assert killed == len(MUTANTS)
