#!/usr/bin/env python3
"""POSN_ASTTAX.TO-X1-1 / cell AT7-s-1 / X1-AC2 -- <SCRATCH_EXERCISE_X1>.

CAN A RE-SEED MOVE management_style? Both arms, with an instrument proved able
to see such a write.

THE SCRATCH TARGET, NAMED
-------------------------
boto3 is replaced in sys.modules BEFORE any seeder byte executes, using V3's
harness definitions imported BY PATH (ac1.make_fake_boto3 /
v3h.ScratchTableWithGet, sha256 of both files asserted below -- never
re-derived). boto3.client() raises. boto3.resource('dynamodb').Table(name)
returns an in-process dict and PRINTS the name it intercepted. The live tables
'etf-classifications' and 'bd-securities' are NEVER opened, read or written by
this process; no network client is ever constructed; --force is never passed.

THE ONE EXTENSION, STATED: RecordingTable subclasses V3's ScratchTableWithGet
to LOG the key of every get_item/update_item and the full kwargs of every
update_item. It adds no behaviour -- every call delegates to the parent -- and
it is what lets row (c) VNQ's "never visited" be a measurement (no read, no
write on that key) rather than an inference from an unchanged value.
PREFLIGHT ITEM 1 (measured separately in x1_preflight_harness_fidelity.py, and
re-measured inline here): the parent's update_item MERGES into the existing
item (real DynamoDB SET semantics), so an unowned field CAN cross a write --
without that, the negative control below could not discriminate.

THE ARMS
--------
  MAIN    : the APPLIED working-tree bytes, seed(upload=True, sync_yang=True)
            -- what `--yang --upload` (no --force) constructs, per the file's
            own __main__ block. Rows (a) QBER, (b) AGG, (c) VNQ.
  NEG-1   : a SCRATCH COPY of those bytes whose SET clause appends
            ', management_style = :ms' (with its value, and the owned tuple
            widened so the new import-time assertion is satisfied). The field
            MUST move on row (b) -- otherwise the MAIN arm's "did not move"
            means nothing.
  NEG-2   : the same clause mutation WITHOUT widening the tuple. The new
            assertion must REFUSE it at import, before any write.
  IDENTITY: the PRE-PATCH bytes (blob 803721e2c1, resolved BY CONTENT) against
            the APPLIED bytes on one frozen clock -- every update_item call and
            all of stdout byte-identical. This is X1-AC6's behaviour arm.
"""
import datetime as _dt
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
DELIV = "org/missions/D4/POSN/POSN_ASTTAX/deliverables"
V3_HARNESS = os.path.join(ROOT, DELIV, "0.9.0_WK_POSN_ASTTAX~21",
                          "v3_mutant_control_re.py")
V3_SHA256 = "6342be43813fff1f8bce87bf47982d926ea67706381a591ea8876fdb48e0daf9"
MACHINERY = os.path.join(ROOT, ".scratch", "u3_ac1_before_control.py")
MACHINERY_SHA256 = ("ae72cab7dfbeb62f9acb2e6e15347672"
                    "a478adce3c0421e12e49750c7bf13aca")
# The seeder as issued (commit cd214384a6), pinned BY CONTENT so this stays
# resolvable after the cell's own commit moves HEAD.
PRE_PATCH_BLOB = "803721e2c15464ed4ba054a02aba2311d5506164"

FROZEN = _dt.datetime(2026, 9, 15, 13, 0, 0, tzinfo=_dt.timezone.utc)


# ---- V3's harness, imported by path, bytes asserted -----------------------
def _sha256(path):
    return hashlib.sha256(io.open(path, "rb").read()).hexdigest()


assert _sha256(MACHINERY) == MACHINERY_SHA256, "round-4 machinery bytes changed"
assert _sha256(V3_HARNESS) == V3_SHA256, "V3 harness bytes changed"
_spec = importlib.util.spec_from_file_location("v3h", V3_HARNESS)
v3h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v3h)
ac1 = v3h.ac1


class RecordingTable(v3h.ScratchTableWithGet):
    """V3's scratch table + a log of which keys were touched and with what."""

    def __init__(self, name):
        v3h.ScratchTableWithGet.__init__(self, name)
        self.read_keys = []
        self.update_keys = []
        self.calls = []

    def get_item(self, Key=None, **kw):
        self.read_keys.append(Key["ticker"])
        return v3h.ScratchTableWithGet.get_item(self, Key=Key, **kw)

    def update_item(self, Key=None, UpdateExpression=None,
                    ExpressionAttributeValues=None,
                    ExpressionAttributeNames=None, **kw):
        self.update_keys.append(Key["ticker"])
        self.calls.append((Key["ticker"], UpdateExpression,
                           dict(ExpressionAttributeNames or {}),
                           dict(ExpressionAttributeValues or {})))
        return v3h.ScratchTableWithGet.update_item(
            self, Key=Key, UpdateExpression=UpdateExpression,
            ExpressionAttributeValues=ExpressionAttributeValues,
            ExpressionAttributeNames=ExpressionAttributeNames, **kw)


class FrozenClock(object):
    """Stands in for the module's `datetime` so two arms stamp one value."""

    @staticmethod
    def now(tz=None):
        return FROZEN


# ---- the three scratch rows ------------------------------------------------
# QBER and VNQ MIRROR the live etf-classifications rows read at the top of this
# cell (x1_ac5_live_read_before.json): QBER structured / Hedge / active /
# 2026-08-18T19:10:00Z and VNQ alternatives / Real Estate / passive /
# 2026-08-18T18:05:00Z. QBER's name is the live value from V3's
# v3_ac7_live_name_read.json and equals the seeder's, so the only disagreements
# are the two class fields. VNQ's name and sector are scratch-chosen and stated
# as such: nothing in this run reads them, because VNQ is not a seeder record.
ROW_A = {
    "ticker": "QBER", "asset_class": "structured", "sub_asset_class": "Hedge",
    "name": "TrueShares Quarterly Bear Hedge ETF",
    "management_style": "active", "sector": "Broad",
    "last_updated": "2026-08-18T19:10:00Z", "updated_by": "posn-asttax-retag",
}
ROW_B = {
    "ticker": "AGG", "asset_class": "fixed_income",
    "sub_asset_class": "Intermediate",
    "name": "iShares Core U.S. Aggregate Bond ETF",
    "management_style": "passive", "sector": "Broad",
    "last_updated": "2026-08-18T18:00:00Z", "updated_by": "posn-asttax-retag",
}
ROW_C = {
    "ticker": "VNQ", "asset_class": "alternatives",
    "sub_asset_class": "Real Estate",
    "name": "Vanguard Real Estate ETF",
    "management_style": "passive", "sector": "Real Estate",
    "last_updated": "2026-08-18T18:05:00Z", "updated_by": "posn-asttax-retag",
}
ROWS = [("a", ROW_A, "the seeder asserts fixed_income / Volatility -> REFUSE"),
        ("b", ROW_B, "agrees with the seeder on all 3 owned fields -> WRITE"),
        ("c", ROW_C, "not a seeder record -> never visited")]


def applied_source():
    raw = io.open(os.path.join(ROOT, REPO_PATH), "rb").read()
    sha = subprocess.check_output(
        ["git", "hash-object", REPO_PATH]).decode().strip()
    return raw.decode("utf-8"), sha


def pre_patch_source():
    """The bytes as issued, resolved BY CONTENT (a ref would move on commit)."""
    raw = subprocess.check_output(["git", "cat-file", "-p", PRE_PATCH_BLOB])
    return raw.decode("utf-8"), PRE_PATCH_BLOB


def run_arm(src, label, store, force=False, freeze=False):
    """Execute real seeder bytes against in-process dicts. No network exists."""
    yang = RecordingTable(ac1.YANG_TABLE)
    bd = RecordingTable(ac1.BD_TABLE)
    yang.store = dict((t, dict(item)) for t, item in store.items())
    before = dict((t, dict(item)) for t, item in yang.store.items())
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
            if freeze:
                mod.datetime = FrozenClock
            rc = mod.seed(upload=True, sync_yang=True, force=force)
    except Exception as exc:  # noqa: BLE001
        err = "%s: %s" % (type(exc).__name__, exc)
    finally:
        assert sys.modules["boto3"].__IS_FAKE__ is True, "the fake boto3 was displaced"
        if saved is None:
            sys.modules.pop("boto3", None)
        else:
            sys.modules["boto3"] = saved
    out = buf.getvalue()
    return {
        "label": label, "rc": rc, "err": err, "out": out,
        "before": before,
        "after": dict((t, dict(item)) for t, item in yang.store.items()),
        "yang": yang, "bd": bd,
        "intercepts": [ln.strip() for ln in out.splitlines()
                       if "SCRATCH TARGET" in ln],
        "preserved": [ln.strip() for ln in out.splitlines() if "[PRESERVED]" in ln],
        "refused": [ln.strip() for ln in out.splitlines()
                    if "REFUSED" in ln or "Nothing was reverted" in ln],
    }


def show_item(tag, item):
    print("      %s (%d field(s)):" % (tag, len(item)))
    for k in sorted(item):
        print("        %-18s %r" % (k, item[k]))


def report_rows(r):
    for tag, row, why in ROWS:
        t = row["ticker"]
        before, after = r["before"][t], r["after"][t]
        print("")
        print("    ROW (%s) %-5s -- %s" % (tag, t, why))
        show_item("BEFORE", before)
        show_item("AFTER ", after)
        moved = sorted(k for k in set(before) | set(after)
                       if before.get(k) != after.get(k))
        print("      FIELDS THAT MOVED: %r  (of %d field(s) before)"
              % (moved, len(before)))
        ms_b = before.get("management_style")
        ms_a = after.get("management_style")
        same_bytes = (repr(ms_b).encode("utf-8") == repr(ms_a).encode("utf-8"))
        print("      management_style : before=%r after=%r  BYTE-IDENTICAL: %s"
              % (ms_b, ms_a, same_bytes))
        print("      touched by the run: get_item %d, update_item %d"
              % (r["yang"].read_keys.count(t), r["yang"].update_keys.count(t)))


def main():
    applied_src, applied_sha = applied_source()
    pre_src, pre_sha = pre_patch_source()
    store = dict((row["ticker"], dict(row)) for _, row, _ in ROWS)

    print("=" * 100)
    print("X1-AC2 -- CAN A RE-SEED MOVE management_style? SCRATCH ONLY.")
    print("=" * 100)
    print("  SCRATCH TARGET  : an in-process dict per table name. boto3 is replaced in")
    print("                    sys.modules before any seeder byte runs; boto3.client()")
    print("                    raises; NO network client is ever constructed. The live")
    print("                    tables 'etf-classifications' and 'bd-securities' are")
    print("                    NEVER opened, read or written by this process.")
    print("  harness         : %s" % V3_HARNESS)
    print("                    sha256 %s (asserted)" % V3_SHA256)
    print("  machinery       : %s" % MACHINERY)
    print("                    sha256 %s (asserted)" % MACHINERY_SHA256)
    print("  APPLIED subject : %s blob %s, %d bytes"
          % (REPO_PATH, applied_sha, len(applied_src.encode("utf-8"))))
    print("  PRE-PATCH subj  : blob %s (as issued @cd214384a6), %d bytes"
          % (pre_sha, len(pre_src.encode("utf-8"))))
    print("  the two subjects DIFFER: %s" % (applied_sha != pre_sha))
    print("  FLAGS           : seed(upload=True, sync_yang=True, force=False) is exactly")
    print("                    what `--yang --upload` builds -- the file's __main__ block")
    print("                    maps --upload->upload, --yang->sync_yang, --force->force.")
    print("                    --force is NEVER passed anywhere in this exercise.")

    # ---- preflight item 1, re-measured inline ------------------------------
    probe = RecordingTable("preflight-probe")
    probe.store["ZZ"] = {"ticker": "ZZ", "asset_class": "old",
                         "management_style": "active"}
    probe.update_item(Key={"ticker": "ZZ"}, UpdateExpression="SET asset_class = :a",
                      ExpressionAttributeValues={":a": "new"})
    merged = (probe.store["ZZ"].get("management_style") == "active"
              and probe.store["ZZ"]["asset_class"] == "new")
    print("  PREFLIGHT-1     : the fake table's update_item %s"
          % ("MERGES (DynamoDB SET semantics) -- an unowned field CAN cross a "
             "write,\n                    so the negative control below can "
             "discriminate." if merged else
             "REPLACES the item -- THE INSTRUMENT IS BLIND; stop."))
    if not merged:
        return 1

    # ---- MAIN --------------------------------------------------------------
    main_arm = run_arm(applied_src, "MAIN -- APPLIED BYTES", store)
    print("")
    print("=" * 100)
    print("  ARM: %s   rc=%r%s" % (main_arm["label"], main_arm["rc"],
                                   "  RAISED: %s" % main_arm["err"]
                                   if main_arm["err"] else ""))
    print("=" * 100)
    for ln in main_arm["intercepts"]:
        print("    " + ln)
    report_rows(main_arm)
    print("")
    for ln in main_arm["refused"]:
        print("    " + ln)
    for ln in main_arm["preserved"]:
        print("    " + ln)
    print("    yang table: get_item %d, update_item %d, rows minted %d "
          "(the MINT CONTROL: the seeder IS writing)"
          % (len(main_arm["yang"].read_keys), len(main_arm["yang"].update_keys),
             len(main_arm["yang"].minted)))
    print("    every key the run WROTE on the yang table, deduped: %d of %d rows"
          % (len(set(main_arm["yang"].update_keys)),
             len(main_arm["yang"].update_keys)))
    print("    VNQ in read keys: %s | VNQ in write keys: %s"
          % ("VNQ" in main_arm["yang"].read_keys,
             "VNQ" in main_arm["yang"].update_keys))
    ms_written = sorted(set(
        k for _, _, _, values in main_arm["yang"].calls for k in values))
    exprs = sorted(set(c[1] for c in main_arm["yang"].calls))
    print("    DISTINCT UpdateExpression(s) the yang table received: %d" % len(exprs))
    for e in exprs:
        print("      %r" % e)
    print("    value tokens passed: %r  ('management_style' among them: %s)"
          % (ms_written, "management_style" in str(ms_written)))

    # ---- the mutation, applied to whichever bytes an arm names -------------
    def mutate_clause(src, tag, widen_tuple=False):
        """Append ', management_style = :ms' to the Yang SET clause + its value.

        Exactly the mutation X1-AC2 names. widen_tuple additionally adds the
        field to YANG_OWNED_FIELDS (NEG-3 only).
        """
        old_expr = "updated_by = :ub'"
        new_expr = "updated_by = :ub, management_style = :ms'"
        old_vals = "':ub': 'canonical_si_seed',"
        new_vals = ("':ub': 'canonical_si_seed',\n"
                    "                        ':ms': 'MUTANT-WROTE-THIS',")
        assert src.count(old_expr) == 1, "SET clause literal not unique in %s" % tag
        assert src.count(old_vals) == 1, "yang values literal not unique in %s" % tag
        out = src.replace(old_expr, new_expr).replace(old_vals, new_vals)
        if widen_tuple:
            old_tuple = "YANG_OWNED_FIELDS = ('asset_class', 'sub_asset_class', 'name')"
            new_tuple = ("YANG_OWNED_FIELDS = ('asset_class', 'sub_asset_class', "
                         "'name',\n                     'management_style')")
            assert src.count(old_tuple) == 1, "owned tuple not unique in %s" % tag
            out = out.replace(old_tuple, new_tuple)
        path = os.path.join(ROOT, ".scratch", "x1ac2_mutant_%s.py" % tag)
        io.open(path, "w", encoding="utf-8", newline="\n").write(out)
        return out, path

    # ---- NEG-1: THE INSTRUMENT CONTROL ------------------------------------
    # The mutation exactly as X1-AC2 names it, on a scratch copy of the seeder
    # bytes AS ISSUED (the pre-patch blob -- the bytes the criterion was written
    # against, and the ones with no import-time guard to stop it). This arm
    # isolates THE INSTRUMENT: can this harness see a management_style write at
    # all? The working tree is never touched.
    neg1_src, neg1_path = mutate_clause(pre_src, "neg1_prepatch")
    neg1 = run_arm(neg1_src, "NEG-1 INSTRUMENT CONTROL -- SCRATCH MUTANT of the "
                             "PRE-PATCH bytes: the SET clause also writes "
                             "management_style", store)
    print("")
    print("=" * 100)
    print("  ARM: %s   rc=%r%s" % (neg1["label"], neg1["rc"],
                                   "  RAISED: %s" % neg1["err"]
                                   if neg1["err"] else ""))
    print("=" * 100)
    print("    mutant: %s (working tree untouched)" % neg1_path)
    print("    its SET clause(s), as received by the fake table:")
    for e in sorted(set(c[1] for c in neg1["yang"].calls)):
        print("      %r" % e)
    report_rows(neg1)

    # ---- NEG-2: the same mutation on the APPLIED bytes --------------------
    neg2_src, neg2_path = mutate_clause(applied_src, "neg2_applied")
    neg2 = run_arm(neg2_src, "NEG-2 -- the SAME mutation on the APPLIED bytes "
                             "(the new import-time assertion must refuse it)",
                   store)
    print("")
    print("=" * 100)
    print("  ARM: %s" % neg2["label"])
    print("=" * 100)
    print("    mutant: %s" % neg2_path)
    print("    rc=%r  RAISED: %s" % (neg2["rc"], neg2["err"]))
    print("    yang update_item calls: %d (the write never happened)"
          % len(neg2["yang"].update_keys))

    # ---- NEG-3: what "add management_style to the tuple" actually does -----
    # The CTO's L10 offered the alternative "adds management_style to the owned
    # tuple". This arm MEASURES that alternative instead of arguing it.
    neg3_src, neg3_path = mutate_clause(applied_src, "neg3_widened_tuple",
                                        widen_tuple=True)
    neg3 = run_arm(neg3_src, "NEG-3 -- clause mutated AND management_style added "
                             "to YANG_OWNED_FIELDS (the rejected alternative)",
                   store)
    print("")
    print("=" * 100)
    print("  ARM: %s" % neg3["label"])
    print("=" * 100)
    print("    mutant: %s" % neg3_path)
    print("    rc=%r  RAISED: %s" % (neg3["rc"], neg3["err"]))
    print("    yang get_item %d, update_item %d before it died; rows minted %d"
          % (len(neg3["yang"].read_keys), len(neg3["yang"].update_keys),
             len(neg3["yang"].minted)))
    print("    the row it died on: %r -- the FIRST row that already EXISTS (an"
          % (neg3["yang"].read_keys[-1] if neg3["yang"].read_keys else None))
    print("    absent row returns [] from _yang_conflicts before any field is read)")
    print("    MEASURED: no record in CANONICAL_SECURITIES carries a")
    print("    'management_style' key, so the guard loop raises KeyError on the")
    print("    first live row. The alternative is not merely vacuous -- it is fatal.")

    # ---- IDENTITY: pre-patch vs applied, one frozen clock ------------------
    id_pre = run_arm(pre_src, "IDENTITY pre-patch", store, freeze=True)
    id_app = run_arm(applied_src, "IDENTITY applied", store, freeze=True)
    calls_equal = id_pre["yang"].calls == id_app["yang"].calls
    bd_equal = id_pre["bd"].calls == id_app["bd"].calls
    out_equal = id_pre["out"] == id_app["out"]
    store_equal = id_pre["after"] == id_app["after"]
    rc_equal = id_pre["rc"] == id_app["rc"]
    print("")
    print("=" * 100)
    print("  ARM: IDENTITY -- pre-patch bytes vs applied bytes, one frozen clock")
    print("=" * 100)
    print("    yang update_item calls  : pre %d, applied %d, IDENTICAL: %s"
          % (len(id_pre["yang"].calls), len(id_app["yang"].calls), calls_equal))
    print("    bd   update_item calls  : pre %d, applied %d, IDENTICAL: %s"
          % (len(id_pre["bd"].calls), len(id_app["bd"].calls), bd_equal))
    print("    stdout                  : pre %d bytes, applied %d bytes, IDENTICAL: %s"
          % (len(id_pre["out"]), len(id_app["out"]), out_equal))
    print("    resulting yang store    : IDENTICAL: %s" % store_equal)
    print("    return code             : pre %r, applied %r, IDENTICAL: %s"
          % (id_pre["rc"], id_app["rc"], rc_equal))
    identical = calls_equal and bd_equal and out_equal and store_equal and rc_equal
    print("    -> the change is STATEMENT AND ASSERTION ONLY: on this input the two")
    print("       builds are BYTE-IDENTICAL in every observable: %s" % identical)

    # ---- the verdict -------------------------------------------------------
    a_t, b_t, c_t = ROW_A["ticker"], ROW_B["ticker"], ROW_C["ticker"]
    a_refused = (len(main_arm["preserved"]) > 0 and main_arm["rc"] == 1
                 and main_arm["after"][a_t]["asset_class"] == "structured"
                 and main_arm["after"][a_t]["sub_asset_class"] == "Hedge")
    a_ms = main_arm["after"][a_t]["management_style"] == ROW_A["management_style"]
    b_written = (main_arm["after"][b_t]["last_updated"] != ROW_B["last_updated"]
                 and main_arm["after"][b_t]["updated_by"] == "canonical_si_seed")
    b_ms = main_arm["after"][b_t]["management_style"] == ROW_B["management_style"]
    c_untouched = (main_arm["after"][c_t] == main_arm["before"][c_t]
                   and c_t not in main_arm["yang"].read_keys
                   and c_t not in main_arm["yang"].update_keys)
    neg1_moved = (neg1["after"][b_t]["management_style"] == "MUTANT-WROTE-THIS"
                  and neg1["before"][b_t]["management_style"] == "passive")
    neg2_refused = ("AssertionError" in (neg2["err"] or "")
                    and len(neg2["yang"].update_keys) == 0)
    neg3_keyerror = ("KeyError" in (neg3["err"] or "")
                     and "management_style" in (neg3["err"] or ""))

    print("")
    print("=" * 100)
    print("X1-AC2 SUMMARY -- each line a measurement, not a restatement")
    print("=" * 100)
    print("  (a) QBER REFUSED, both class fields [PRESERVED], rc 1        : %s" % a_refused)
    print("  (a) QBER management_style 'active' byte-identical after      : %s" % a_ms)
    print("  (b) AGG  WRITTEN (last_updated and updated_by moved)         : %s" % b_written)
    print("  (b) AGG  management_style 'passive' byte-identical after     : %s" % b_ms)
    print("  (c) VNQ  never visited (no get_item, no update_item, ==)     : %s" % c_untouched)
    print("  NEG-1 the mutant MOVES (b)'s management_style                : %s" % neg1_moved)
    print("  NEG-2 the assertion REFUSES that mutation at import          : %s" % neg2_refused)
    print("  NEG-3 the WIDENED TUPLE raises KeyError on the first live row: %s" % neg3_keyerror)
    print("  IDENTITY pre-patch == applied on every observable            : %s" % identical)
    ok = all([a_refused, a_ms, b_written, b_ms, c_untouched, neg1_moved,
              neg2_refused, neg3_keyerror, identical])
    print("")
    if ok:
        print("  OK: 9 of 9. The MAIN and NEG-1 arms read DIFFERENTLY on the same input")
        print("  and the same rows, so 'management_style did not move' is a MEASUREMENT")
        print("  by an instrument that demonstrably can see such a write -- not an")
        print("  absence of evidence. A re-seed cannot write, clear or revert")
        print("  management_style, and never reaches VNQ at all.")
    else:
        print("  ERROR: not every arm read as expected. Report this, not the result.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
