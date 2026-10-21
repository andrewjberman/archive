"""IRPT_ANLREQ round 60 (issuer 2.0.0_SA_COO~G2): the checks of the resident's retained-reason line (cell AR-g-183).
READ ONLY, offline, no AWS.

    python ar_reason_checks.py reason [--root <lambda tree root>]
    python ar_reason_checks.py tests [--root <lambda tree root>]

Why: run 7I stopped with `IRPT_RESIDENT_POLL retained_for_retry class=RecipeRefused code=-` three times, and the inner message could only be
read by replaying the composition offline. `retained_reason` prints a message only when it is itself a closed code (an upper-case token); the
sentence messages of our own refusal classes print `-`. The rule this check holds `resident_main.retained_reason(exc)` to:
  - a message that is a closed code prints as before: `class=X code=CODE` and nothing else;
  - otherwise `class=X code=-`, and ONLY for a class whose name ends in Refused or Attention (our own refusals, raised with developer-written
    text) one more field ` lead=<token>` when a leading constant token exists:
      * an upper-case code at the start of the message followed by a colon or a space (`COMPARISON_NO_VENDOR_MAPPING: ...`) -> that token;
      * else the leading run of at least two and at most six whole lower-case words (letters only), joined by `_`, ending at the first word that
        is not all lower-case letters (so a quoted id, a number, a capitalised name or a value ends the lead and never appears in it);
  - any other class (RuntimeError, ValueError, a vendor or HTTP error) prints `code=-` and never a lead; a message is never printed otherwise.
`tests`: the four test files that read the retained line pass (49 at the base) and at least 51 ran, so the new rule has tests of its own.
Prints one RESULT line: AR-REASON-reason-OK or AR-REASON-reason-FAIL <the cases that differ>. ASCII only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 8)))
TREE = "infra/aws/lambda/investor-reporting"

TEST_FILES = ['ycharts/generate/tests/test_resident_main.py', 'ycharts/generate/tests/test_package_poll.py', 'ycharts/generate/tests/test_package_on_ready.py', 'ycharts/generate/tests/test_permanent_authority_refusal.py']
MIN_TESTS = 51


def paths(root):
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    sys.path[:0] = [os.path.join(base, p) for p in ("ycharts/generate", "ops", "reports", "intake", "_scope", "_ids", "_keys", "_authz",
                                                      "ycharts/research", "ycharts/session", "ycharts/extract", "lib")] + [base]


def make(name):
    return type(name, (RuntimeError,), {})


RecipeRefused, WorkerAttention, PlainError = make("RecipeRefused"), make("WorkerAttention"), make("PlainError")

CASES = [
    (RecipeRefused("holdings row has no provider receipt"), "class=RecipeRefused code=- lead=holdings_row_has_no_provider_receipt"),
    (RecipeRefused("COMPARISON_NO_VENDOR_MAPPING: opal_x has no YCharts mapping; the YCharts path cannot price it"),
     "class=RecipeRefused code=- lead=COMPARISON_NO_VENDOR_MAPPING"),
    (RecipeRefused("holdings row 'SPY' has no provider check"), "class=RecipeRefused code=- lead=holdings_row"),
    (RecipeRefused("template T-1 (multicomp) takes 2..5 comparison securities and 1 were supplied"), "class=RecipeRefused code=-"),
    (RecipeRefused("an unresolved holding cannot be sent to the vendor; it awaits resolution"),
     "class=RecipeRefused code=- lead=an_unresolved_holding_cannot_be_sent"),
    (RecipeRefused("no captured template for variant 'x'; declared variants: a, b"),
     "class=RecipeRefused code=- lead=no_captured_template_for_variant"),
    (RecipeRefused("https://x.example/a?sig=abc"), "class=RecipeRefused code=-"),
    (RecipeRefused("12 holdings are bad"), "class=RecipeRefused code=-"),
    (RecipeRefused(""), "class=RecipeRefused code=-"),
    (RecipeRefused("FROZEN_WORKER_JOB_BINDING"), "class=RecipeRefused code=FROZEN_WORKER_JOB_BINDING"),
    (WorkerAttention("OPAL_PRODUCER_REFUSED"), "class=WorkerAttention code=OPAL_PRODUCER_REFUSED"),
    (WorkerAttention("the producer refused the run for good reasons"), "class=WorkerAttention code=- lead=the_producer_refused_the_run_for"),
    (PlainError("holdings row has no provider receipt"), "class=PlainError code=-"),
    (PlainError("FROZEN_WORKER_JOB_BINDING"), "class=PlainError code=FROZEN_WORKER_JOB_BINDING"),
]


def arm_tests(root):
    """The owned test files, run with plain python from the lambda tree: all pass and at least MIN_TESTS ran (the baseline plus the new tests)."""
    import re
    import subprocess
    base = os.path.join(root, TREE) if os.path.isdir(os.path.join(root, TREE)) else root
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"] + TEST_FILES
    run = subprocess.run(cmd, capture_output=True, text=True, cwd=base)
    found = re.findall(r"(\d+) passed", run.stdout)
    passed = int(found[-1]) if found else 0
    if run.returncode != 0 or passed < MIN_TESTS:
        print("AR-%s-tests-FAIL rc=%d passed=%d (want rc 0 and at least %d): %s" % ("REASON", run.returncode, passed, MIN_TESTS,
              " ".join(run.stdout.strip().splitlines()[-2:])[:200]))
        sys.exit(1)
    print("AR-%s-tests-OK passed=%d" % ("REASON", passed))


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("reason", "tests"):
        print("usage: ar_reason_checks.py reason|tests [--root <root>]")
        sys.exit(2)
    root = REPO
    if "--root" in sys.argv:
        root = os.path.abspath(sys.argv[sys.argv.index("--root") + 1])
    if sys.argv[1] == "tests":
        arm_tests(root)
        return
    paths(root)
    try:
        import resident_main
    except Exception as exc:  # noqa: BLE001
        print("AR-REASON-reason-FAIL cannot import resident_main: %s: %s" % (type(exc).__name__, str(exc)[:100]))
        sys.exit(1)
    bad = []
    for exc, want in CASES:
        got = resident_main.retained_reason(exc)
        if got != want:
            bad.append("%r -> %r (want %r)" % (str(exc)[:30], got, want))
    if bad:
        print("AR-REASON-reason-FAIL %d of %d cases differ: %s" % (len(bad), len(CASES), " | ".join(bad)[:700]))
        sys.exit(1)
    print("AR-REASON-reason-OK")


if __name__ == "__main__":
    main()
