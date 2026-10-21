"""IRPT_ANLREQ AR-y-494: the swap-model wiring, read as TEXT from the three source files and the builder (offline, stdlib only).

    python -I check_swap_wiring.py             -> SWAP-WIRING-OK producer_composes=yes ... builder_binding=ON   (rc 0)
                                               -> SWAP-WIRING-BAD <axes that read no>                           (rc 1)
    python -I check_swap_wiring.py --selftest  -> CONTROL-FIRES                                                 (rc 0)
                                               -> CONTROL-DEAD <the mutations that did not read BAD>            (rc 1)

The selftest mutates the texts in memory three ways (the producer's proposals= removed; the refusal text removed from the
resident; the builder's True set to False) and fires only when each mutation reads BAD on its own axis. ASCII only.
"""
import sys
from pathlib import Path

# the worktree root: this file sits at org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/<serial>/, seven levels below it
ROOT = Path(__file__).resolve().parents[7]
BASE = ROOT / "infra" / "aws" / "lambda" / "investor-reporting"
PRODUCER = BASE / "ycharts" / "research" / "opal_producer.py"
RESIDENT = BASE / "reports" / "resident_installed.py"
BUILDER = BASE / "reports" / "build_resident_package.py"

COMPOSE_MARKERS = ("def _swap_classify", "answer = lookup(symbol)", "if _usable_class(answer)", "return model_classify(symbol)")
BUILDER_ON = '"opal_swap_model": {"enabled": True}'


def producer_composes(text):
    """The model is consulted only after the lookup: every marker present, in this order."""
    if any(marker not in text for marker in COMPOSE_MARKERS):
        return False
    return (text.index("answer = lookup(symbol)") < text.index("if _usable_class(answer)")
            < text.index("return model_classify(symbol)"))


def axes(producer, resident, builder):
    """Each axis as a bool; a missing source text reads False on every axis it feeds."""
    return {
        "producer_composes": producer_composes(producer),
        "proposals_passed": "proposals=proposals" in producer,
        "binding_validated": "OPAL_SWAP_MODEL_BINDING" in resident and "SWAP_MODEL_BINDING_INVALID" in resident,
        "secrets_client_wired": "SWAP_MODEL_SECRETS_CLIENT_REQUIRED" in resident and 'clients["secretsmanager"]' in resident,
        "builder_binding": BUILDER_ON in builder,
    }


def read_sources():
    return (PRODUCER.read_text(encoding="utf-8"), RESIDENT.read_text(encoding="utf-8"), BUILDER.read_text(encoding="utf-8"))


def run_check():
    got = axes(*read_sources())
    if all(got.values()):
        print("SWAP-WIRING-OK producer_composes=yes proposals_passed=yes binding_validated=yes secrets_client_wired=yes "
              "builder_binding=ON")
        return 0
    print("SWAP-WIRING-BAD " + " ".join(name for name, ok in got.items() if not ok))
    return 1


def run_selftest():
    producer, resident, builder = read_sources()
    checks = (
        ("proposals_passed", axes(producer.replace("proposals=proposals", ""), resident, builder)),
        ("binding_validated", axes(producer, resident.replace("SWAP_MODEL_BINDING_INVALID", ""), builder)),
        ("builder_binding", axes(producer, resident, builder.replace(BUILDER_ON, BUILDER_ON.replace("True", "False")))),
    )
    dead = [axis for axis, got in checks if got[axis]]  # a mutation that leaves its own axis True did not fire the control
    if not dead:
        print("CONTROL-FIRES")
        return 0
    print("CONTROL-DEAD " + " ".join(dead))
    return 1


if __name__ == "__main__":
    sys.exit(run_selftest() if "--selftest" in sys.argv[1:] else run_check())
