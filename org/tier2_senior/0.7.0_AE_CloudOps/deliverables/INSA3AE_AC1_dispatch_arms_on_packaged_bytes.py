"""INSA3AE-AC1 three dispatch arms, run against the PACKAGED BYTES.

sys.path is set to the BUILT PACKAGE DIR ONLY, so what executes is what ships --
not the worktree copy. Nothing here opens a socket: DRY_RUN is left at its
fail-closed default and each arm is patched AT THE DISPATCH BOUNDARY, so the
question asked is "where does the handler route this event", never "what does
the leg do".
"""
import importlib
import os
import sys

PKG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rp_build")

# Fail-closed config. DRY_RUN deliberately NOT set to "0".
os.environ["DRY_RUN"] = "1"
os.environ.setdefault("MONOLITH_BUCKET", "opal-data-assets")
os.environ.setdefault("BD_BASE", "https://bd3.bdreporting.com")
os.environ.setdefault("BD_SESSION_SECRET_ID", "blackdiamond/49f/session")

sys.path.insert(0, PKG)

FAILS = []


def fresh():
    """Re-import the packaged modules per arm so one arm cannot contaminate another."""
    for m in ("lambda_function", "insurance_leg"):
        sys.modules.pop(m, None)
    lf = importlib.import_module("lambda_function")
    assert os.path.dirname(os.path.abspath(lf.__file__)) == PKG, (
        "WRONG MODULE LOADED: %s -- the arm would be scoring the worktree, not the package"
        % lf.__file__)
    return lf


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not cond:
        FAILS.append(name)


print("ARMS RUN AGAINST: %s" % PKG)
print("lambda_function.__file__ asserted inside the package dir on every arm.\n")

# ---------------------------------------------------------------- ARM 1
# {"leg":"insurance"} MUST reach insurance_leg.run_insurance_leg.
lf = fresh()
import insurance_leg  # noqa: E402  (packaged copy, via sys.path)
called = {}


def fake_run_insurance_leg(pull_date):
    called["pull_date"] = pull_date
    return {"stub": True, "leg": "insurance"}


insurance_leg.run_insurance_leg = fake_run_insurance_leg
sys.modules["insurance_leg"] = insurance_leg
r1 = lf.lambda_handler({"leg": "insurance"}, None)
check("ARM 1 insurance event ENTERS the insurance leg", called != {} and r1.get("leg") == "insurance",
      "run_insurance_leg called with pull_date=%r" % called.get("pull_date"))

# ---------------------------------------------------------------- ARM 2
# A reporting event MUST enter the reporting worker and MUST NOT enter insurance.
lf = fresh()
import insurance_leg  # noqa: E402
tripped = {"insurance": False}


def must_not_run(pull_date):
    tripped["insurance"] = True
    return {}


insurance_leg.run_insurance_leg = must_not_run
sys.modules["insurance_leg"] = insurance_leg
ran = {}


def fake_run(accounts, q_start, q_end, pull_date, **kw):
    ran["hit"] = True
    # The handler prints manifest["count"] / ["by_feed"] / ["accounts"] after run()
    # returns (lambda_function.py:451-453). A stub with the wrong shape raises a
    # KeyError DOWNSTREAM of the dispatch boundary this arm is measuring -- which
    # would leave an unexplained exception sitting in the evidence. Return the real
    # contract shape so the arm is clean end to end.
    return {"count": 0, "by_feed": {}, "accounts": list(accounts), "stub": True}


lf.run = fake_run
ev = {"leg": "reporting", "q_start": "2026-01-01", "q_end": "2026-03-31",
      "pull_date": "2026-08-30", "accounts": ["z01"]}
try:
    r2 = lf.lambda_handler(ev, None)
    entered_reporting = ran.get("hit", False)
except Exception as exc:  # a refusal here is still "insurance not entered"
    r2 = "raised: %s" % type(exc).__name__
    entered_reporting = ran.get("hit", False)
check("ARM 2 reporting event ENTERS the reporting path", entered_reporting, repr(r2)[:70])
check("ARM 2 insurance leg NOT entered", tripped["insurance"] is False)

# ---------------------------------------------------------------- ARM 3
# {} MUST produce a NAMED refusal -- not a bare KeyError.
lf = fresh()
try:
    r3 = lf.lambda_handler({}, None)
    named, why = False, "returned %r instead of refusing" % (r3,)
except KeyError as exc:
    named, why = False, "BARE KeyError %s -- this is the pre-fix failure mode" % exc
except Exception as exc:
    msg = str(exc)
    named = ("REPORTING LEG REFUSED" in msg) or ("UNKNOWN LEG" in msg)
    why = "%s: %s" % (type(exc).__name__, msg[:110])
check("ARM 3 bare {} -> NAMED refusal (not a bare KeyError)", named, why)

# ------------------------------------------------- NEGATIVE CONTROL on ARM 3
# An UNKNOWN leg must also refuse BY NAME, and by a DIFFERENT branch than arm 3
# -- so arm 3 is not passing on a catch-all that swallows everything.
lf = fresh()
try:
    lf.lambda_handler({"leg": "nonsense-leg-xyz"}, None)
    unk, why2 = False, "no refusal raised"
except Exception as exc:
    msg = str(exc)
    unk = "UNKNOWN LEG" in msg
    why2 = "%s: %s" % (type(exc).__name__, msg[:110])
check("CONTROL unknown leg refuses via the UNKNOWN-LEG branch", unk, why2)

print()
print("RESULT: %d FAIL of 6 checks" % len(FAILS))
if FAILS:
    print("FAILED:", FAILS)
sys.exit(1 if FAILS else 0)
