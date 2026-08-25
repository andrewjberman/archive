"""PRF-inv-5 EXERCISE (ADVI_PERFRP TO-R1-DS, AC12) -- the firm argument and path pin.

AC12: a no-firm invocation REFUSES rc!=0 ; firm-pinned reads/writes only, path census
printed.

THE CONTROL THAT MAKES THIS MEAN ANYTHING: a firm pin that never REJECTS a path
proves nothing -- it would pass identically if assert_path_belongs returned True
unconditionally. So every accept below is paired with a REJECT of the corresponding
cross-firm path, and the rejects name which foreign firm the path belongs to.

EVIDENCE VINTAGE: citations resolve at 23271aac6480f2ebd65a37247ae64dde4d68c199.
"""
from __future__ import annotations

import subprocess
import sys

sys.path.insert(0, "data/assets/scripts/gold/runners_49f")
from perfrp_firm_pin import (  # noqa: E402  IMPORTED, never copied
    FIRM_TREES,
    FOREIGN_FIRM_BUCKETS,
    FirmRefused,
    assert_path_belongs,
    path_census,
    resolve_firm,
)

PASSED = 0
FAILED = 0


def check(label, ok, detail=""):
    global PASSED, FAILED
    if ok:
        PASSED += 1
    else:
        FAILED += 1
    print("  [%s] %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


def run_cli(args):
    """Run the entrypoint as a REAL PROCESS and capture its true rc.

    AC12 says rc != 0. Calling main() in-process returns an int; it does NOT prove
    the process exits non-zero, and argparse's own refusal path calls SystemExit
    before main's return is ever reached. So the rc claim is measured on a subprocess.
    """
    p = subprocess.run(
        [sys.executable, "data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py"] + args,
        capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)


def main_exercise() -> int:
    print("PRF-inv-5 EXERCISE -- ADVI_PERFRP TO-R1-DS (AC12)")
    print("=" * 100)
    print("known firms: %s | foreign buckets pinned against: %s"
          % (sorted(FIRM_TREES), sorted(FOREIGN_FIRM_BUCKETS)))

    print("\nAC12.1 -- a no-firm invocation REFUSES with a REAL non-zero rc")
    rc, out = run_cli([])
    check("no --firm -> rc != 0", rc != 0, "rc=%d" % rc)
    check("and it says why", "firm" in out.lower(), out.strip().splitlines()[-1][:60])
    rc, out = run_cli(["--firm", ""])
    check("empty --firm -> rc != 0", rc != 0, "rc=%d" % rc)
    rc, out = run_cli(["--firm", "bd"])
    check("UNKNOWN firm -> rc != 0 (never resolved to a nearest match)", rc != 0, "rc=%d" % rc)
    rc, out = run_cli(["--firm", "49financial"])
    check("POSITIVE CONTROL: a valid firm -> rc == 0", rc == 0, "rc=%d" % rc)
    print("       (rc measured on a REAL SUBPROCESS -- an in-process main() return")
    print("        would not prove the process exits non-zero, and argparse exits")
    print("        before main's return is reached at all)")

    print("\nAC12.2 -- resolve_firm REFUSES rather than defaulting")
    for bad in (None, "", "   ", "bd", "cot", "inf", "49Financial", "49financial "):
        try:
            resolve_firm(bad)
            ok = bad.strip() in FIRM_TREES if isinstance(bad, str) else False
            check("resolve_firm(%r)" % bad, ok, "resolved" if ok else "SHOULD have refused")
        except FirmRefused:
            check("resolve_firm(%r) REFUSES" % bad, True)

    tree = resolve_firm("49financial")

    print("\nAC12.3 -- THE PIN MUST REJECT, not merely accept")
    reads_ok = [
        ("opal-data-49financial", "gold/advi/canonical/twr_daily/date=2026-08-21/data.parquet"),
        ("opal-data-assets", "schwab/08335338/silver/fact_trn/date=2026-08-21/data.parquet"),
        ("opal-data-assets", "blackdiamond/49f/silver/dim_account_xref/date=2026-08-21/data.parquet"),
    ]
    for b, k in reads_ok:
        try:
            assert_path_belongs(tree, b, k, mode="read")
            check("READ accepted: %s" % b, True, k[:44])
        except FirmRefused as e:
            check("READ accepted: %s" % b, False, str(e)[:50])

    print("       -- and the matching CROSS-FIRM rejects:")
    for foreign, firm in sorted(FOREIGN_FIRM_BUCKETS.items()):
        try:
            assert_path_belongs(tree, foreign, "gold/advi/canonical/twr_daily/x", mode="read")
            check("READ from %s REJECTED" % foreign, False, "IT WAS ACCEPTED -- pin is inert")
        except FirmRefused as e:
            check("READ from %s REJECTED (names firm %r)" % (foreign, firm), firm in str(e))

    print("\nAC12.4 -- WRITES are pinned harder than reads")
    try:
        assert_path_belongs(tree, "opal-data-49financial", "gold/advi/canonical/x", mode="write")
        check("WRITE to own gold root accepted", True)
    except FirmRefused as e:
        check("WRITE to own gold root accepted", False, str(e)[:50])
    try:
        assert_path_belongs(tree, "opal-data-portal-v2", "platinum/advi/49financial/x.json", mode="write")
        check("WRITE to own serve root accepted", True)
    except FirmRefused as e:
        check("WRITE to own serve root accepted", False, str(e)[:50])
    # the sharp one: silver is READABLE but must NOT be writable
    try:
        assert_path_belongs(tree, "opal-data-assets", "schwab/08335338/silver/fact_trn/x", mode="write")
        check("WRITE to silver REJECTED (readable != writable)", False, "IT WAS ACCEPTED")
    except FirmRefused:
        check("WRITE to silver REJECTED (readable != writable)", True,
              "same path is a legal READ above -- the modes differ, as they must")
    try:
        assert_path_belongs(tree, "opal-data-portal-v2", "platinum/mdpf/x.json", mode="write")
        check("WRITE to another product's serve prefix REJECTED", False, "IT WAS ACCEPTED")
    except FirmRefused:
        check("WRITE to another product's serve prefix REJECTED", True)

    print("\nAC12.5 -- the path census is printed BEFORE any I/O, and asserts as it prints")
    census = path_census(tree, reads=reads_ok,
                         writes=[("opal-data-portal-v2",
                                  "platinum/advi/49financial/perfrp_activity_relationship.json")])
    print("\n".join("    " + ln for ln in census.splitlines()))
    check("census asserted every path", "ALL asserted." in census)
    try:
        path_census(tree, reads=[("opal-data-cot", "gold/x")], writes=[])
        check("a census containing a foreign path REFUSES", False, "it printed happily")
    except FirmRefused:
        check("a census containing a foreign path REFUSES", True,
              "the census constrains what may happen, not just documents it")

    print("\n" + "=" * 100)
    print("DENOMINATOR: %d checks, %d PASS, %d FAIL" % (PASSED + FAILED, PASSED, FAILED))
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main_exercise())
