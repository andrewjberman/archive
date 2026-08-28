#!/usr/bin/env python
"""KEYFILL-DTX AC3 + AC4 -- validate this lane's filled cards, and replay it from a CLEAN CLONE.

Two things this runner refuses to do, both learned the expensive way in this project today:

  IT DOES NOT PASS ON AN EMPTY POPULATION. "0 valid of 0" satisfies every reconciliation I could
  write, so the denominator is asserted against the re-derived expectation and a zero-card run FAILS.

  IT DOES NOT TRUST ITS OWN GREEN WITHOUT A FIXTURE THAT MUST GO RED. The contradiction v3 exists to
  forbid -- a key row reading `measured` while its key_expression is NULL -- is constructed and fed
  to the same validator. If the schema accepts it, the 18 passes above prove nothing about the rule
  they are supposed to be evidence for.

--run-commit <pin> extracts the pin to a fresh unique directory, runs this file INSIDE it, and
RELEASES the extract on exit (--keep for a named forensic case). ~1 GB per extract; leaving them
behind is what filled this device earlier today.
"""
import copy
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
LANE = "0.4.0_DT_ClientPlatform~X"
EXPECTED = 18
SCHEMA = os.path.join(ROOT, "org", "standards", "SUBSTRATE_CARD.v3.schema.json")


def cards():
    out = []
    for f in sorted(glob.glob(os.path.join(
            ROOT, "org", "tier2_senior", "0.4.0_DT_ClientPlatform", "deliverables",
            "D11_CARDS_*", "*.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        if d.get("carded_by") == LANE:
            out.append((f, d))
    return out


def clone_and_run(commit, keep):
    sys.path.insert(0, os.path.join(ROOT, "org", "standards", "isck"))
    from ledger.battery import run_battery as rb
    commit = subprocess.check_output(["git", "rev-parse", "--verify", "%s^{commit}" % commit],
                                     cwd=ROOT).decode().strip()
    dest, owned = rb.choose_clone_dir(None, commit)
    clone = rb.clean_clone(commit, dest, ROOT)
    print("CLEAN CLONE of BUILD commit %s -> %s" % (commit, clone))
    try:
        child = subprocess.run(
            [sys.executable, os.path.join(clone, "org", "tier2_senior", "0.4.0_DT_ClientPlatform",
                                          "deliverables", "D11_CARDS_KEYFILL",
                                          "validate_keyfill.py")],
            cwd=clone, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.write(child.stdout.decode("utf-8", "replace").replace(chr(13), ""))
        return child.returncode
    finally:
        rb.release_clone(owned, keep)


def main():
    if "--run-commit" in sys.argv:
        i = sys.argv.index("--run-commit")
        if i + 1 >= len(sys.argv):
            print("REFUSING: --run-commit needs a commit")
            return 4
        return clone_and_run(sys.argv[i + 1], "--keep" in sys.argv)

    try:
        import jsonschema
    except ImportError:
        print("NOT EXERCISABLE: jsonschema is not installed here -- the validator cannot run, which "
              "is not the same as the cards being invalid")
        return 3

    with open(SCHEMA, encoding="utf-8") as fh:
        V = jsonschema.Draft202012Validator(json.load(fh))
    found = cards()
    print("KEYFILL-DTX VALIDATION")
    print("   cards RE-DERIVED here: %d (expected %d)" % (len(found), EXPECTED))
    if not found:
        print("   FAIL: zero cards -- a reconciliation over an empty set is vacuous, not a pass")
        return 1
    if len(found) != EXPECTED:
        print("   NAMED DIFFERENCE: %d re-derived against %d expected -- not absorbed"
              % (len(found), EXPECTED))

    ok, bad = 0, []
    basis = {}
    for f, d in found:
        errs = sorted(V.iter_errors(d), key=lambda e: e.path)
        if errs:
            bad.append((os.path.basename(f).split("__")[0], errs[0].message[:90]))
        else:
            ok += 1
        b = ((d.get("trust") or {}).get("key") or {}).get("basis_by_field", {}).get("key_expression")
        basis[b] = basis.get(b, 0) + 1
    print("AC3 v3 validation : PASS %d of %d" % (ok, len(found)))
    for n, m in bad:
        print("   INVALID %s -- %s" % (n, m))
    print("AC2 basis census  : %s" % json.dumps(basis, sort_keys=True))
    print("   inferred present: %s (AC2 prohibits it in this fill)" % ("YES" if basis.get("inferred") else "no"))

    fixture = copy.deepcopy(found[0][1])
    k = fixture["trust"]["key"]
    k["key_expression"] = None
    k["basis"] = "measured"
    k.setdefault("basis_by_field", {})["key_expression"] = "measured"
    refused = bool(list(V.iter_errors(fixture)))
    print("AC3 contradiction : measured + NULL expression REFUSED = %s" % refused)
    if not refused:
        print("   the schema ACCEPTS the contradiction -- the 18 passes above are not evidence for "
              "the rule they are meant to demonstrate")

    good = (ok == len(found) and refused and not basis.get("inferred")
            and len(found) == EXPECTED)
    print("VERDICT           : %s" % ("PASS" if good else "FAIL"))
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
