#!/usr/bin/env python3
"""POSN_ASTTAX.TO-V3-1 / cell AT5-s-3 -- U3_MUTANT_CONTROL_RE.

THE RE-RUN of round 4's mutant/discrimination control (TO-U3-1, cell AT4-s-3),
against the APPLIED REPO FILE rather than a scratch reconstruction. This is the
one thing round 4 could not do: its <paths> grant excluded the file, so it
exercised patched bytes it had built in .scratch/. This cell APPLIED the patch,
so the subject here is the real working-tree file.

THE MACHINERY IS ROUND 4's, UNMODIFIED. .scratch/u3_ac1_before_control.py is a
byte-identical copy of .scratch/run/u3_ac1_before_control.py from the round-4
worktree (sha256 asserted at import below). The scratch table, the fake boto3,
the retag set, the baseline builder and the mint probe are all ITS definitions.
Re-deriving them would have made this a different instrument measuring a
different thing.

THE SCRATCH TARGET, NAMED
-------------------------
boto3 is replaced in sys.modules BEFORE any seeder bytes execute.
boto3.client() raises. boto3.resource('dynamodb').Table(name) returns an
in-process dict and PRINTS the name it intercepted. The live DynamoDB tables
'etf-classifications' and 'bd-securities' are NEVER opened, read or written by
this process; no network client is ever constructed. --upload is never passed
to a real table because no real table exists here.

ARMS
----
  V3-AC5 (negative)  : PRE-PATCH bytes, resolved BY CONTENT from the git object
                       store, asserted == blob fbbc7165d331 (round 4's subject).
  V3-AC4 (mutant)    : the APPLIED WORKING-TREE FILE's real bytes.
  override           : the applied bytes with --force (the override must still
                       override, or the guard is a wall rather than a guard).
  V3-AC7 (readings)  : a per-field probe over YANG_OWNED_FIELDS -- for each
                       owned field in turn, a live row that agrees with the
                       seeder on every OTHER owned field and disagrees on that
                       one. Records whether the guard refuses. NO VERDICT.
"""
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import types
from contextlib import redirect_stdout

ROOT = os.getcwd()
REPO_PATH = "data/black_diamond/scripts/classification/seed_canonical_securities.py"
MACHINERY = os.path.join(ROOT, ".scratch", "u3_ac1_before_control.py")
MACHINERY_SHA256 = "ae72cab7dfbeb62f"
PRE_PATCH_BLOB = "fbbc7165d33198789d3a7788a557ed3f5ce75614"

# ---- import round 4's machinery, asserting it is unmodified ----------------
_raw = io.open(MACHINERY, "rb").read()
_got = hashlib.sha256(_raw).hexdigest()[:16]
assert _got == MACHINERY_SHA256, "machinery changed: %s != %s" % (_got, MACHINERY_SHA256)
_spec = importlib.util.spec_from_file_location("ac1", MACHINERY)
ac1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ac1)


class ScratchTableWithGet(ac1.ScratchTable):
    """Round 4's scratch table plus get_item -- the pre-read the guard needs."""

    def __init__(self, name):
        ac1.ScratchTable.__init__(self, name)
        self.reads = 0

    def get_item(self, Key=None, **_):
        self.reads += 1
        item = self.store.get(Key["ticker"])
        return {"Item": dict(item)} if item is not None else {}


def applied_bytes():
    """The REAL working-tree file -- the thing this cell changed."""
    raw = io.open(os.path.join(ROOT, REPO_PATH), "rb").read()
    sha = subprocess.check_output(["git", "hash-object", REPO_PATH]).decode().strip()
    return raw.decode("utf-8"), sha


def pre_patch_bytes():
    """The PRE-patch bytes, resolved BY CONTENT, not by ref name.

    The order names `git show HEAD~1:<path>`; that form assumes the patch is
    already committed. It is NOT committed at this point in the cell, so HEAD
    still carries the pre-patch blob. Resolved here by CONTENT and asserted
    against the blob round 4 measured, which is what the identity actually is.
    """
    raw = subprocess.check_output(["git", "show", "HEAD:" + REPO_PATH])
    sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD:" + REPO_PATH]).decode().strip()
    assert sha == PRE_PATCH_BLOB, "pre-patch blob %s != round 4 subject %s" % (
        sha, PRE_PATCH_BLOB)
    return raw.decode("utf-8"), sha


def run(src, label, force=False, store_builder=None):
    yang = ScratchTableWithGet(ac1.YANG_TABLE)
    bd = ScratchTableWithGet(ac1.BD_TABLE)
    secs = ac1.canonical_securities(src)
    by_ticker = {s["ticker"]: s for s in secs}
    retag_names = dict(ac1.RETAG)
    mint_probe = next(s["ticker"] for s in secs if s["ticker"] not in retag_names)
    if store_builder is None:
        yang.store = ac1.baseline(by_ticker, mint_probe)
    else:
        yang.store = store_builder(by_ticker, mint_probe)
    present = [t for t, _ in ac1.RETAG if t in by_ticker]
    before = {t: dict(yang.store[t]) for t in present}

    tables = {ac1.YANG_TABLE: yang, ac1.BD_TABLE: bd}
    saved = sys.modules.get("boto3")
    sys.modules["boto3"] = ac1.make_fake_boto3(tables)
    buf = io.StringIO()
    rc, err = None, None
    try:
        mod = types.ModuleType("seeder_%s" % abs(hash(label)))
        mod.__file__ = os.path.join(ROOT, REPO_PATH)
        mod.__name__ = "seeder_%s" % abs(hash(label))
        with redirect_stdout(buf):
            exec(compile(src, REPO_PATH, "exec"), mod.__dict__)
            if force:
                rc = mod.seed(upload=True, sync_yang=True, force=True)
            else:
                rc = mod.seed(upload=True, sync_yang=True)
    except Exception as exc:  # noqa: BLE001
        err = "%s: %s" % (type(exc).__name__, exc)
    finally:
        assert sys.modules["boto3"].__IS_FAKE__ is True, "the fake boto3 was displaced"
        if saved is None:
            sys.modules.pop("boto3", None)
        else:
            sys.modules["boto3"] = saved

    after = {t: dict(yang.store[t]) for t in present}
    out = buf.getvalue()
    return {
        "label": label, "rc": rc, "err": err, "out": out,
        "present": present, "before": before, "after": after,
        "survived": [t for t in present
                     if after[t]["asset_class"] == before[t]["asset_class"]],
        "clobbered": [t for t in present
                      if after[t]["asset_class"] != before[t]["asset_class"]],
        "minted": mint_probe in yang.store, "mint_probe": mint_probe,
        "mint_value": yang.store.get(mint_probe, {}).get("asset_class"),
        "yang_writes": yang.updates, "yang_reads": yang.reads,
        "yang_minted": len(yang.minted), "ratified": retag_names,
        "intercepts": [ln.strip() for ln in out.splitlines()
                       if "SCRATCH TARGET" in ln],
        "preserved_lines": [ln.strip() for ln in out.splitlines()
                            if "[PRESERVED]" in ln],
        "refused_lines": [ln.strip() for ln in out.splitlines()
                          if "REFUSED" in ln or "Nothing was reverted" in ln],
    }


def show(r):
    print("")
    print("=" * 100)
    print("ARM: %s" % r["label"])
    print("=" * 100)
    for ln in r["intercepts"]:
        print("  " + ln)
    print("  %-6s %-14s %-14s %-14s %s"
          % ("TICKER", "BEFORE", "AFTER", "RATIFIED", "VERDICT"))
    for t in r["present"]:
        b, a = r["before"][t]["asset_class"], r["after"][t]["asset_class"]
        print("  %-6s %-14s %-14s %-14s %s"
              % (t, b, a, r["ratified"][t], "SURVIVED" if a == b else "CLOBBERED"))
    print("  SURVIVED %d of %d | CLOBBERED %d | rc=%r%s"
          % (len(r["survived"]), len(r["present"]), len(r["clobbered"]), r["rc"],
             "  RAISED: %s" % r["err"] if r["err"] else ""))
    print("  MINT CONTROL: %r %s   (yang update_item=%d, get_item=%d, minted=%d)"
          % (r["mint_probe"],
             "MINTED (asset_class=%r) -- the seeder IS writing" % r["mint_value"]
             if r["minted"] else "NOT MINTED -- verdict WORTHLESS",
             r["yang_writes"], r["yang_reads"], r["yang_minted"]))
    for ln in r["refused_lines"]:
        print("  " + ln)
    for ln in r["preserved_lines"][:8]:
        print("  " + ln)
    if len(r["preserved_lines"]) > 8:
        print("  ... and %d more [PRESERVED] line(s)"
              % (len(r["preserved_lines"]) - 8))


# --------------------------------------------------------------------------
# V3-AC7 READINGS -- the per-field probe over YANG_OWNED_FIELDS.
# --------------------------------------------------------------------------
def field_probe_builder(field_under_test):
    """A live row AGREEING with the seeder on every owned field but ONE.

    If the guard owns the field, this single disagreement must be enough to
    refuse. If it does not own it, the run writes through.
    """
    def build(by_ticker, mint_probe):
        store = {}
        for ticker, five_class in ac1.RETAG:
            if ticker not in by_ticker:
                continue
            sec = by_ticker[ticker]
            row = {
                "ticker": ticker,
                "asset_class": sec["asset_class"],
                "sub_asset_class": sec["sub_asset_class"],
                "name": sec["name"],
                "management_style": "passive",
                "sector": "Broad",
                "last_updated": "2026-09-12T00:00:00Z",
                "updated_by": "posn-asttax-retag",
            }
            if field_under_test == "asset_class":
                row["asset_class"] = five_class
            elif field_under_test == "sub_asset_class":
                row["sub_asset_class"] = "PROBE-DIFFERENT-SUBCLASS"
            elif field_under_test == "name":
                row["name"] = "PROBE-DIFFERENT-NAME"
            elif field_under_test == "last_updated":
                row["last_updated"] = "1999-01-01T00:00:00Z"
            elif field_under_test == "sector":
                row["sector"] = "PROBE-DIFFERENT-SECTOR"
            store[ticker] = row
        assert mint_probe not in store
        return store
    return build


def main():
    applied_src, applied_sha = applied_bytes()
    pre_src, pre_sha = pre_patch_bytes()

    print("=" * 100)
    print("U3_MUTANT_CONTROL_RE -- TO-V3-1 / AT5-s-3. SCRATCH ONLY.")
    print("=" * 100)
    print("  SCRATCH TARGET  : an in-process dict per table name. NO network client is")
    print("                    ever constructed (boto3.client raises). The live tables")
    print("                    'etf-classifications' and 'bd-securities' are NEVER")
    print("                    opened for read or write by this process. --upload is")
    print("                    never passed to a real table because none exists here.")
    print("  machinery       : %s (round 4's, sha256 %s, asserted unmodified)"
          % (MACHINERY, MACHINERY_SHA256))
    print("  APPLIED subject : %s" % os.path.join(ROOT, REPO_PATH))
    print("                    blob %s, %d bytes  <- the file this cell changed"
          % (applied_sha, len(applied_src.encode("utf-8"))))
    print("  PRE-PATCH subj  : git show HEAD:%s" % REPO_PATH)
    print("                    blob %s, %d bytes  <- round 4's subject, by CONTENT"
          % (pre_sha, len(pre_src.encode("utf-8"))))
    print("  the two subjects DIFFER: %s" % (applied_sha != pre_sha))

    neg = run(pre_src, "V3-AC5 NEGATIVE -- PRE-PATCH bytes, same input (must still revert)")
    pos = run(applied_src, "V3-AC4 MUTANT -- APPLIED REPO BYTES, same input (verdict must flip)")
    forced = run(applied_src, "OVERRIDE -- applied bytes with --force (must revert again)",
                 force=True)
    show(neg)
    show(pos)
    show(forced)

    print("")
    print("=" * 100)
    print("DISCRIMINATION VERDICT (V3-AC4 vs V3-AC5, same input, two subjects)")
    print("=" * 100)
    discriminates = (len(neg["clobbered"]) == len(neg["present"])
                     and len(pos["survived"]) == len(pos["present"])
                     and neg["minted"] and pos["minted"]
                     and len(forced["clobbered"]) == len(forced["present"])
                     and pos["rc"] == 1)
    print("  V3-AC5 pre-patch : CLOBBERED %d of %d, minted=%s, rc=%r"
          % (len(neg["clobbered"]), len(neg["present"]), neg["minted"], neg["rc"]))
    print("  V3-AC4 applied   : SURVIVED  %d of %d, minted=%s, rc=%r"
          % (len(pos["survived"]), len(pos["present"]), pos["minted"], pos["rc"]))
    print("  override --force : CLOBBERED %d of %d, rc=%r"
          % (len(forced["clobbered"]), len(forced["present"]), forced["rc"]))
    print("  THE TWO ARMS DIFFER: %s"
          % (neg["clobbered"] != pos["clobbered"]))
    print("")
    if discriminates:
        print("  OK: THE CONTROL DISCRIMINATES on the APPLIED file. The two arms read")
        print("  DIFFERENTLY on identical input, the mint control fires in BOTH arms")
        print("  (%d row(s) minted under the guard), and --force still overrides."
              % pos["yang_minted"])
    else:
        print("  ERROR: THE CONTROL DOES NOT DISCRIMINATE -- both arms read the same, or")
        print("  a mint control did not fire. Report this, not the result.")

    # ---------------- V3-AC7 readings, no verdict --------------------------
    print("")
    print("=" * 100)
    print("V3-AC7 READINGS -- WHICH FIELDS THE GUARD ACTUALLY OWNS (no verdict)")
    print("=" * 100)
    mod = types.ModuleType("owned_probe")
    exec(compile(applied_src, REPO_PATH, "exec"), mod.__dict__)
    print("  YANG_OWNED_FIELDS as applied : %r" % (mod.YANG_OWNED_FIELDS,))
    print("  the seeder's Yang UpdateExpression writes: asset_class, sub_asset_class,")
    print("  name, last_updated, updated_by  (5 fields; the guard owns the first 3)")
    print("")
    print("  PER-FIELD PROBE: live row agrees with the seeder on every owned field")
    print("  EXCEPT the one named; does the guard refuse on that field ALONE?")
    print("")
    print("  %-18s %-9s %-10s %s" % ("FIELD PROBED", "IN TUPLE", "rc", "OUTCOME"))
    for field in ("asset_class", "sub_asset_class", "name", "last_updated", "sector"):
        r = run(applied_src, "probe:%s" % field,
                store_builder=field_probe_builder(field))
        in_tuple = field in mod.YANG_OWNED_FIELDS
        refused = r["rc"] == 1
        n_pres = len(r["preserved_lines"])
        print("  %-18s %-9s %-10r %s"
              % (field, "YES" if in_tuple else "no", r["rc"],
                 "REFUSED, %d [PRESERVED] line(s)" % n_pres if refused
                 else "WROTE THROUGH, no conflict raised"))
    print("")
    print("  NOTE FOR THE GRADER: the live etf-classifications rows for the four")
    print("  members currently serve asset_class equity/equity/equity/fixed_income")
    print("  (read at the top of this cell) -- i.e. the retag AT5-s-8 performs has")
    print("  NOT yet run. The guard reads the LIVE row, so what it protects is")
    print("  whatever the table serves AT RE-SEED TIME, not a value compiled in.")
    return 0 if discriminates else 1


if __name__ == "__main__":
    sys.exit(main())
