"""IRPT_ANLREQ AR-y-484 check: the resident bindings builder's tickets_table equals the Terraform name of the
aws_dynamodb_table that holds ticket_id as its hash key (infra/aws/terraform/ticket-center/main.tf).

stdlib only, offline. It loads the pure helpers from the test module, so the check and the test share one compare()
and one set of three mutants.

  python -I check_tickets_pin.py            -> TICKETS-PIN-OK builder=... terraform=... equal=yes   (rc 0)
                                            -> TICKETS-PIN-BAD <why>                                (rc 1)
  python -I check_tickets_pin.py --selftest -> CONTROL-FIRES                                        (rc 0)
                                               only when ALL THREE mutants read BAD; otherwise CONTROL-SILENT (rc 1)
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEST_REL = "infra/aws/lambda/investor-reporting/reports/tests/test_resident_tickets_table_pin.py"


def load_pin_module():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE),
                         capture_output=True, text=True, check=True)
    root = Path(out.stdout.strip())
    spec = importlib.util.spec_from_file_location("resident_tickets_table_pin", str(root / TEST_REL))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_check(pin):
    try:
        builder, tf = pin.read_real()
    except OSError as exc:
        print("TICKETS-PIN-BAD cannot read the two repository files: %s" % exc)
        return 1
    try:
        value, table = pin.compare(builder, tf)
    except pin.PinError as exc:
        print("TICKETS-PIN-BAD " + str(exc))
        return 1
    print("TICKETS-PIN-OK builder=%s terraform=%s equal=yes" % (value, table))
    return 0


def run_selftest(pin):
    builder, tf = pin.read_real()
    for mutant in pin.MUTANTS:
        try:
            b2, t2 = mutant(builder, tf)
        except RuntimeError:
            print("CONTROL-SILENT")
            return 1
        if pin.refusal(b2, t2) is None:
            print("CONTROL-SILENT")
            return 1
    print("CONTROL-FIRES")
    return 0


def main(argv):
    pin = load_pin_module()
    if "--selftest" in argv:
        return run_selftest(pin)
    return run_check(pin)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
