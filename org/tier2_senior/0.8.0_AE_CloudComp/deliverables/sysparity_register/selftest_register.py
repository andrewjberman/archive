"""
Self-test for the NFRA_SYSPARITY re-ground register.

BUILT AGAINST CVO~Z's S5 ACCEPTANCE TEST, stated verbatim in its spec (170631Z):
  "The mutant: kill the writing process between verdict-formation and session-close, and
   prove the row is already durable. A register that only survives a graceful exit does not
   address the failure that produced it. I will also check that a row whose artifact_pointer
   does not resolve is DETECTED, not silently trusted -- a dangling pointer must be loud."

Both are implemented as real exercises, not assertions about the code:
  K1 hard-kills a live child process (TerminateProcess / SIGKILL -- no cleanup handlers run)
     after record() returns but BEFORE any graceful close, then reads the row back from disk.
  D1 plants a pointer at a path that does not exist and requires the report to say DANGLING
     and exit nonzero.

Plus the control that matters most for a DENOMINATOR instrument:
  N1 swaps in a contract declaring a DIFFERENT number of units and requires the report to
     follow it. If the tool ever hand-copies 22, N1 fails. A denominator instrument that
     cannot detect its own frozen count is the defect it exists to find.

Run:  python selftest_register.py
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "sysparity_register.py")
sys.path.insert(0, HERE)

import sysparity_register as R  # noqa: E402

FAILS = 0


def check(label: str, got, want) -> None:
    global FAILS
    if got == want:
        print(f"PASS  {label:58s} -> {got}")
    else:
        print(f"FAIL  {label:58s} -> got={got!r} want={want!r}")
        FAILS += 1


def check_true(label: str, cond: bool, note: str = "") -> None:
    global FAILS
    if cond:
        print(f"PASS  {label:58s} {note}")
    else:
        print(f"FAIL  {label:58s} {note}")
        FAILS += 1


def main() -> int:
    work = tempfile.mkdtemp(prefix="sysreg_")
    try:
        reg = os.path.join(work, "reg.jsonl")
        units = R.load_units()
        n = len(units)
        some = sorted(units)[0]
        other = sorted(units)[1]
        print(f"DENOMINATOR derived live: {n} units from scope_contract.json")
        print()

        # ---- validation ----------------------------------------------------------------
        print("=== VALIDATION ===")
        rc = subprocess.run(
            [sys.executable, TOOL, "record", "--unit", "NOT-A-REAL-UNIT", "--verdict", "CLEAN",
             "--pointer", "file:README.md", "--register", reg],
            capture_output=True, text=True).returncode
        check("V1 unknown unit_id REJECTED", rc != 0, True)
        check_true("V1b ... and NO row written", not os.path.exists(reg),
                   "(an unknown id cannot become coverage)")

        rc = subprocess.run(
            [sys.executable, TOOL, "record", "--unit", some, "--verdict", "CLEAN",
             "--register", reg],
            capture_output=True, text=True).returncode
        check("V2 CLEAN with NO pointer REJECTED (terminal claim)", rc != 0, True)

        # ---- the three states ----------------------------------------------------------
        print()
        print("=== THE THREE STATES ARE STRUCTURALLY DISTINCT ===")
        R.record(some, "CLEAN", "all 3 managed regions in 06", ["file:infra/system/scope_contract.json"],
                 "cycle-22", "TEST", register_path=reg)
        R.record(other, "UNRECORDED", "", [], "cycle-20", "TEST", register_path=reg)
        rep = R.report(reg)
        check("S1 swept+resolving pointer -> SWEPT", rep["states"][some], "SWEPT")
        check("S2 UNRECORDED distinct from absent", rep["states"][other], "SWEPT_UNRECORDED")
        third = sorted(units)[2]
        check("S3 no row -> NEVER_SWEPT", rep["states"][third], "NEVER_SWEPT")
        check_true("S4 UNRECORDED is NOT counted recoverable",
                   rep["verdicts_recoverable"] == 1 and rep["units_touched"] == 2,
                   f"(touched={rep['units_touched']} recoverable={rep['verdicts_recoverable']})")
        check("S5 the two numbers DIFFER (the gap is the signal)",
              rep["units_touched"] != rep["verdicts_recoverable"], True)

        # ---- D1: dangling pointer must be LOUD -----------------------------------------
        print()
        print("=== D1 -- CVO~Z S5b: a dangling pointer is DETECTED, not silently trusted ===")
        reg2 = os.path.join(work, "reg2.jsonl")
        R.record(some, "CLEAN", "pass over N things",
                 ["file:this/path/does/not/exist/anywhere.txt"], "cycle-22", "TEST",
                 register_path=reg2)
        rep2 = R.report(reg2)
        check("D1 non-resolving pointer -> SWEPT_DANGLING", rep2["states"][some], "SWEPT_DANGLING")
        check("D1b dangling is NOT counted recoverable", rep2["verdicts_recoverable"], 0)
        out = subprocess.run([sys.executable, TOOL, "report", "--register", reg2],
                             capture_output=True, text=True)
        check("D1c report EXITS NONZERO on dangling (loud)", out.returncode, 2)
        check_true("D1d ... and says DANGLING in the output", "DANGLING" in out.stdout, "")

        # git-pointer form against a real repo path + a bogus one
        reg2b = os.path.join(work, "reg2b.jsonl")
        R.record(some, "CLEAN", "d", ["git:HEAD:infra/system/scope_contract.json"], "c", "TEST",
                 register_path=reg2b)
        R.record(other, "CLEAN", "d", ["git:HEAD:no/such/file/at/all.txt"], "c", "TEST",
                 register_path=reg2b)
        rep2b = R.report(reg2b)
        check("D1e git pointer to REAL path resolves", rep2b["states"][some], "SWEPT")
        check("D1f git pointer to BOGUS path -> DANGLING", rep2b["states"][other], "SWEPT_DANGLING")

        # ---- K1: THE KILL TEST ---------------------------------------------------------
        print()
        print("=== K1 -- CVO~Z S5a: HARD-KILL between verdict-formation and session-close ===")
        reg3 = os.path.join(work, "reg3.jsonl")
        ready = os.path.join(work, "ready.marker")
        child_src = os.path.join(work, "child.py")
        with open(child_src, "w", encoding="utf-8") as fh:
            fh.write(
                "import sys, os, time\n"
                f"sys.path.insert(0, {HERE!r})\n"
                "import sysparity_register as R\n"
                f"R.record({some!r}, 'CLEAN', 'the pass was of N things',\n"
                f"         ['file:infra/system/scope_contract.json'], 'cycle-21', 'KILLED-AGENT',\n"
                f"         register_path={reg3!r})\n"
                f"open({ready!r},'w').write('x')\n"
                "# verdict formed + recorded. Now BLOCK FOREVER -- this process will be hard-killed\n"
                "# before it ever writes a session log or exits gracefully.\n"
                "while True: time.sleep(0.05)\n"
            )
        proc = subprocess.Popen([sys.executable, child_src])
        for _ in range(200):
            if os.path.exists(ready):
                break
            time.sleep(0.05)
        killed_after_ready = os.path.exists(ready)
        proc.kill()          # TerminateProcess / SIGKILL -- NO cleanup handlers run
        proc.wait(timeout=10)
        check_true("K1a child reached post-record before kill", killed_after_ready, "")
        check_true("K1b child was hard-killed (nonzero/again-killed)", proc.returncode != 0,
                   f"(rc={proc.returncode})")
        rep3 = R.report(reg3)
        check("K1c THE ROW SURVIVED THE HARD KILL", rep3["states"][some], "SWEPT")
        rows = R.load_rows(reg3)
        check("K1d exactly one durable row", len(rows), 1)
        check("K1e ... written by the killed agent", rows[0]["agent"], "KILLED-AGENT")
        check("K1f ... carrying its cycle", rows[0]["cycle"], "cycle-21")
        check_true("K1g ... and its denominator + pointer (re-derivable)",
                   bool(rows[0]["denominator"]["stated"]) and bool(rows[0]["artifact_pointer"]), "")

        # ---- N1: the denominator is DERIVED, not hand-copied ---------------------------
        print()
        print("=== N1 -- MUTANT: is the denominator really DERIVED? ===")
        fake_contract = os.path.join(work, "fake_contract.json")
        with open(fake_contract, "w", encoding="utf-8") as fh:
            json.dump({"domains": {"d1": {"units": [{"id": "u-alpha", "desc": "x"},
                                                    {"id": "u-beta", "desc": "x"},
                                                    {"id": "u-gamma", "desc": "x"}]}}}, fh)
        fake_units = R.load_units(fake_contract)
        check("N1a tool follows a DIFFERENT contract (3 units)", len(fake_units), 3)
        check_true("N1b ... and 3 != the real denominator", len(fake_units) != n,
                   f"(real={n}) -- a hand-copied 22 would fail this")
        reg4 = os.path.join(work, "reg4.jsonl")
        R.record("u-alpha", "CLEAN", "d", ["file:infra/system/scope_contract.json"], "c", "TEST",
                 register_path=reg4, contract_path=fake_contract)
        rep4 = R.report(reg4, fake_contract)
        check("N1c report denominator follows the contract", rep4["contract_units"], 3)
        # N1d: a REAL unit id must be REJECTED while the fake contract is in force -- proving
        # the id whitelist tracks the contract rather than a baked-in list. Exercised through
        # the API, because the CLI takes no --contract flag; an earlier draft of this case ran
        # the CLI, which silently used the REAL contract and therefore PASSED FOR THE WRONG
        # REASON while its label claimed a rejection. Kept as a scar: a green whose label does
        # not match what it measures is worse than a red.
        rejected = False
        try:
            R.record(some, "UNRECORDED", "", [], "c", "TEST",
                     register_path=reg4, contract_path=fake_contract)
        except SystemExit:
            rejected = True
        check("N1d real unit id REJECTED under the fake contract", rejected, True)
        # and the inverse, so N1d cannot pass by rejecting everything
        accepted = True
        try:
            R.record("u-beta", "UNRECORDED", "", [], "c", "TEST",
                     register_path=reg4, contract_path=fake_contract)
        except SystemExit:
            accepted = False
        check("N1e fake-contract id ACCEPTED (N1d is not reject-everything)", accepted, True)

        # ---- corruption is surfaced ----------------------------------------------------
        print()
        print("=== CORRUPTION IS SURFACED, NEVER SKIPPED ===")
        reg5 = os.path.join(work, "reg5.jsonl")
        R.record(some, "CLEAN", "d", ["file:infra/system/scope_contract.json"], "c", "TEST",
                 register_path=reg5)
        with open(reg5, "a", encoding="utf-8") as fh:
            fh.write("{ this is not json\n")
        rep5 = R.report(reg5)
        check("C1 corrupt line COUNTED and surfaced", len(rep5["corrupt_lines"]), 1)
        check("C1b good row still read", rep5["states"][some], "SWEPT")
        out5 = subprocess.run([sys.executable, TOOL, "report", "--register", reg5],
                              capture_output=True, text=True)
        check("C1c corruption makes report exit nonzero", out5.returncode, 2)

        # ---- append-only supersession --------------------------------------------------
        print()
        print("=== APPEND-ONLY: a correction SUPERSEDES, history retained ===")
        reg6 = os.path.join(work, "reg6.jsonl")
        R.record(some, "UNRECORDED", "", [], "cycle-20", "TEST", register_path=reg6)
        time.sleep(1.05)  # distinct explicit-Z second, so latest-wins is unambiguous
        R.record(some, "CLEAN", "re-swept", ["file:infra/system/scope_contract.json"],
                 "cycle-20", "TEST", register_path=reg6)
        rep6 = R.report(reg6)
        check("A1 latest row wins", rep6["states"][some], "SWEPT")
        check("A1b BOTH rows retained on disk (evidence kept)", len(R.load_rows(reg6)), 2)

        print()
        print(f"TOTAL FAILURES: {FAILS}")
        return FAILS
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
